/* Hỏi đáp SSR: ưu tiên câu trả lời có sẵn trong nội dung trang (Quỹ bảo trì và Điều hành);
   chỉ khi nội dung không đủ mới hỏi Gemini qua máy chủ Google Apps Script (khóa API giữ ở máy chủ). */
(function () {
  'use strict';
  if (window.__ssrHoiDap) return; window.__ssrHoiDap = 1;
  var ME = document.currentScript && document.currentScript.src || '';
  var BASE = ME ? ME.replace(/[^/]*$/, '') : 'https://jukytwo.github.io/ssr-so-quy-bao-tri/web/hoi-dap/';
  var WEB = BASE.replace(/hoi-dap\/$/, '');
  var PAGE = /\/dieu-hanh\//.test(location.pathname) ? 'd' : 'q';
  var CFG = window.SSR_HOIDAP || {};
  var KB = null, IDX = null, BUSY = false;

  /* ---------- chuẩn hóa tiếng Việt và chỉ mục BM25 ---------- */
  var STOPA = ('là và của có không thì cho các những được một này đó với trong trên dưới ra vào đến từ như nào gì sao thế ai ở còn đã sẽ đang phải tôi bạn mình chúng anh chị em hay hoặc nếu vì để khi lại rất quá nữa bị bởi theo về hơn nhất cũng mỗi tại mà nên thấy vậy à nhé ạ ơi nhỉ hỏi xin cảm ơn giúp biết muốn bao nhiêu mấy làm thì đúng thế').split(' ');
  var STOPF = ('la va cua co khong thi cho cac nhung duoc mot nay do voi trong tren duoi ra vao den tu nhu nao gi sao the ai o con da se dang phai toi ban minh chung anh chi em hay hoac neu vi de khi lai rat qua nua bi boi theo ve hon nhat cung moi tai ma nen thay vay a nhe oi nhi hoi xin cam on giup biet muon nhieu may lam dung').split(' ');
  var SA = {}, SF = {}; STOPA.forEach(function (w) { SA[w] = 1; }); STOPF.forEach(function (w) { SF[w] = 1; });
  function base(s) { return String(s || '').toLowerCase().normalize('NFC').replace(/(\d)[.,](\d)/g, '$1$2'); }
  function fold(s) { return base(s).normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/đ/g, 'd'); }
  function hasMark(s) { return /[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]/i.test(s); }
  function terms(s, folded) {
    var t = folded ? fold(s) : base(s), STOPS = folded ? SF : SA;
    var w = t.split(/[^a-z0-9\u00c0-\u1ef9]+/).filter(Boolean), out = [];
    for (var i = 0; i < w.length; i++) {
      if (!STOPS[w[i]] && (w[i].length > 1 || /\d/.test(w[i]))) out.push(w[i]);
      if (i + 1 < w.length && !STOPS[w[i]] && !STOPS[w[i + 1]]) out.push(w[i] + '_' + w[i + 1]);
    }
    return out;
  }
  function build(items) { return { a: build1(items, false), f: build1(items, true) }; }
  function build1(items, folded) {
    var N = items.length, df = {}, docs = [], tot = 0;
    items.forEach(function (c) {
      var tt = terms(c.t, folded), tx = terms(c.x, folded), tf = {}, ttl = {};
      tt.forEach(function (t) { tf[t] = (tf[t] || 0) + 2; ttl[t] = 1; });
      tx.forEach(function (t) { tf[t] = (tf[t] || 0) + 1; });
      var len = tt.length * 2 + tx.length; tot += len;
      Object.keys(tf).forEach(function (t) { df[t] = (df[t] || 0) + 1; });
      docs.push({ tf: tf, ttl: ttl, len: len });
    });
    var idf = {}; Object.keys(df).forEach(function (t) { idf[t] = Math.log(1 + (N - df[t] + 0.5) / (df[t] + 0.5)); });
    return { docs: docs, idf: idf, avg: tot / Math.max(1, N) };
  }
  function search(q) {
    var folded = !hasMark(q), IX = folded ? IDX.f : IDX.a, qt = terms(q, folded), uniq = {}; qt.forEach(function (t) { uniq[t] = 1; }); qt = Object.keys(uniq);
    var W = 0; qt.forEach(function (t) { W += IX.idf[t] || 0; });
    var k1 = 1.4, b = 0.7, res = [];
    IX.docs.forEach(function (d, i) {
      var s = 0, cov = 0, tcov = 0;
      qt.forEach(function (t) {
        var f = d.tf[t]; if (!f) return; var w = IX.idf[t] || 0;
        s += w * (f * (k1 + 1)) / (f + k1 * (1 - b + b * d.len / IX.avg)); cov += w; if (d.ttl[t]) tcov += w;
      });
      if (s > 0) res.push({ i: i, s: s, cov: W ? cov / W : 0, tcov: W ? tcov / W : 0 });
    });
    res.sort(function (a, b) { return b.s - a.s; });
    return { q: qt, W: W, hits: res.slice(0, 8) };
  }

  /* ---------- giao diện ---------- */
  var CSS = '.hdw-fab{position:fixed;right:22px;bottom:calc(22px + env(safe-area-inset-bottom,0px));z-index:70;display:flex;align-items:center;gap:8px;padding:11px 16px 11px 13px;border-radius:999px;border:1px solid #C9A443;background:#063B28;color:#F3E3A6;font:700 14px/1 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;box-shadow:0 10px 26px -8px rgba(3,28,19,.55);cursor:pointer}' +
    '.hdw-fab svg{width:20px;height:20px}@media (max-width:960px){.hdw-fab{right:auto;left:12px;bottom:calc(80px + env(safe-area-inset-bottom,0px));padding:10px 14px 10px 11px;font-size:13px}}@media print{.hdw-fab,.hdw{display:none!important}}' +
    '.hdw{position:fixed;z-index:120;inset:0;display:flex;justify-content:flex-end;background:rgba(3,28,19,.45);font:400 14.5px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;color:#13231B}' +
    '.hdw-p{width:min(520px,100%);height:100%;background:#FBFAF5;display:flex;flex-direction:column;box-shadow:-12px 0 40px rgba(0,0,0,.25)}' +
    '.hdw-h{display:flex;align-items:center;gap:10px;padding:calc(12px + env(safe-area-inset-top,0px)) 16px 12px;background:#063B28;color:#F3E3A6}.hdw-h b{font-size:16px;flex:1}.hdw-h small{display:block;color:#CFE3D6;font-weight:400;font-size:12px}' +
    '.hdw-x{background:none;border:1px solid rgba(243,227,166,.4);color:#F3E3A6;border-radius:10px;width:36px;height:36px;font-size:20px;cursor:pointer}' +
    '.hdw-b{flex:1;overflow:auto;padding:14px 16px 8px;-webkit-overflow-scrolling:touch}' +
    '.hdw-intro{font-size:13.5px;color:#3D4F45;margin:0 0 10px}.hdw-chips{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:12px}' +
    '.hdw-chip{border:1px solid #D9CFA8;background:#FFF;color:#063B28;border-radius:999px;padding:6px 11px;font-size:13px;cursor:pointer;text-align:left}' +
    '.hdw-q{margin:14px 0 6px;padding:9px 12px;border-radius:12px;background:#E7EFE9;color:#063B28;font-weight:600}' +
    '.hdw-c{background:#FFF;border:1px solid #E1E6DF;border-radius:12px;padding:11px 13px;margin:8px 0}' +
    '.hdw-tag{display:inline-block;font-size:11.5px;font-weight:700;letter-spacing:.02em;border-radius:6px;padding:2px 7px;margin-bottom:6px}' +
    '.hdw-tag.k{background:#E3F1E7;color:#14653E}.hdw-tag.ai{background:#FFF1D6;color:#7A5600}.hdw-tag.r{background:#EEF1F4;color:#4B5A66}' +
    '.hdw-c h4{margin:0 0 4px;font-size:14.5px;color:#063B28}.hdw-c p{margin:4px 0}.hdw-c ul{margin:4px 0;padding-left:20px}.hdw-src{font-size:12.5px;color:#5C6B63;margin-top:6px}' +
    '.hdw-a{color:#0B6E47;font-weight:600;text-decoration:none;cursor:pointer;border:0;background:none;padding:0;font-size:13px}.hdw-a:hover{text-decoration:underline}' +
    '.hdw-rel{display:block;width:100%;text-align:left;border:1px solid #E1E6DF;background:#FFF;border-radius:10px;padding:8px 11px;margin:6px 0;cursor:pointer;font-size:13px;color:#13231B}.hdw-rel b{color:#063B28}.hdw-rel span{display:block;color:#5C6B63;font-size:12px}' +
    '.hdw-more{margin-top:8px;border:1px solid #C9A443;background:#FFF8E6;color:#5C4300;border-radius:10px;padding:8px 12px;font-weight:600;cursor:pointer;font-size:13px}' +
    '.hdw-note{font-size:12px;color:#6B5A2E;background:#FFF6DC;border:1px solid #EBD9A2;border-radius:10px;padding:8px 10px;margin:10px 0 4px}' +
    '.hdw-f{border-top:1px solid #E1E6DF;padding:10px 12px calc(10px + env(safe-area-inset-bottom,0px));background:#FFF;display:flex;gap:8px;align-items:flex-end}' +
    '.hdw-f textarea{flex:1;resize:none;border:1px solid #CBD5CE;border-radius:12px;padding:9px 11px;font:inherit;font-size:16px;min-height:44px;max-height:120px}' +
    '.hdw-send{border:0;background:#063B28;color:#F3E3A6;border-radius:12px;padding:0 16px;height:44px;font-weight:700;cursor:pointer}.hdw-send[disabled]{opacity:.5}' +
    '.hdw-wait{color:#5C6B63;font-style:italic;margin:8px 2px}@media (max-width:640px){.hdw-p{width:100%}}';
  var IC = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 5h16v11H9l-5 4z"/><path d="M9.5 9.2a2.5 2.5 0 1 1 3.3 2.4c-.5.2-.8.6-.8 1.1"/><path d="M12 14.6v.01"/></svg>';
  var SUG = PAGE === 'd'
    ? ['Ban Quản trị có phải công khai sổ phụ tài khoản quỹ bảo trì không?', 'Ban Quản lý được cắt nước căn nợ phí không?', 'Nhiệm kỳ Ban Quản trị bao lâu?', 'Phí quản lý SSR là bao nhiêu?']
    : ['986,9 triệu chuyển vào tài khoản Ban quản trị là sao?', 'Ban quản trị có phải công khai sổ phụ không?', 'Muốn bãi nhiệm thành viên Ban quản trị thì làm thế nào?', 'Quy chế hoạt động Ban quản trị quy định họp mấy lần một năm?'];
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function md(s) {
    var L = esc(s).split(/\n+/), h = '', ul = false;
    L.forEach(function (l) {
      l = l.replace(/\*\*(.+?)\*\*/g, '<b>$1</b>');
      if (/^\s*[-*•]\s+/.test(l)) { if (!ul) { h += '<ul>'; ul = true; } h += '<li>' + l.replace(/^\s*[-*•]\s+/, '') + '</li>'; }
      else { if (ul) { h += '</ul>'; ul = false; } if (l.trim()) h += '<p>' + l + '</p>'; }
    });
    return h + (ul ? '</ul>' : '');
  }
  function clip(s, n) { s = String(s || ''); return s.length > n ? s.slice(0, n).replace(/\s+\S*$/, '') + '…' : s; }
  function urlOf(c) {
    var h = '#' + (c.a || c.s || '');
    if (c.pg === PAGE) return h;
    return c.pg === 'd' ? WEB + 'dieu-hanh/index.html' + h : WEB + 'index.html' + h;
  }
  function go(c) {
    var u = urlOf(c);
    if (u.charAt(0) === '#') { close(); if (location.hash === u) { location.hash = ''; } location.hash = u; var el = document.getElementById(u.slice(1)); if (el && el.tagName === 'DETAILS') el.open = true; if (el) setTimeout(function () { el.scrollIntoView({ block: 'start' }); }, 250); }
    else location.href = u;
  }
  var root, body, ta, send;
  function open() {
    if (!root) {
      var st = document.createElement('style'); st.textContent = CSS; document.head.appendChild(st);
      root = document.createElement('div'); root.className = 'hdw'; root.setAttribute('role', 'dialog'); root.setAttribute('aria-label', 'Hỏi đáp');
      root.innerHTML = '<div class="hdw-p"><div class="hdw-h"><div style="flex:1"><b>Hỏi đáp SSR</b><small>Trả lời theo nội dung trang trước, AI chỉ dùng khi trang chưa có</small></div><button class="hdw-x" aria-label="Đóng">×</button></div>' +
        '<div class="hdw-b"><p class="hdw-intro">Gõ câu hỏi về quỹ bảo trì, quy chế, quy định pháp luật về nhà chung cư hoặc cách dùng công cụ. Câu trả lời có sẵn trên trang hiện trước; phần trang chưa có mới hỏi AI Gemini.</p>' +
        '<div class="hdw-chips">' + SUG.map(function (s) { return '<button class="hdw-chip">' + esc(s) + '</button>'; }).join('') + '</div><div class="hdw-log"></div></div>' +
        '<div class="hdw-note" style="margin:4px 16px 0">Đừng ghi tên, số điện thoại, số căn hộ. Câu trang chưa có sẽ gửi tới AI Gemini của Google để trả lời.</div><form class="hdw-f"><textarea rows="1" maxlength="500" placeholder="Nhập câu hỏi, ví dụ: Ban quản trị có phải công khai sổ phụ không?"></textarea><button class="hdw-send" type="submit">Hỏi</button></form></div>';
      document.body.appendChild(root);
      body = root.querySelector('.hdw-log'); ta = root.querySelector('textarea'); send = root.querySelector('.hdw-send');
      root.addEventListener('click', function (e) {
        if (e.target === root || e.target.closest('.hdw-x')) return close();
        var ch = e.target.closest('.hdw-chip'); if (ch) { ta.value = ch.textContent; ask(); return; }
        var lk = e.target.closest('[data-kb]'); if (lk) { go(KB.items[+lk.getAttribute('data-kb')]); return; }
        var ai = e.target.closest('[data-ai]'); if (ai) { ai.disabled = true; askAI(ai.getAttribute('data-ai'), JSON.parse(ai.getAttribute('data-ids')), ai.closest('.hdw-turn')); }
      });
      root.querySelector('form').addEventListener('submit', function (e) { e.preventDefault(); ask(); });
      ta.addEventListener('keydown', function (e) { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); ask(); } });
      document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && root.style.display !== 'none') close(); });
    }
    root.style.display = 'flex'; document.documentElement.style.overflow = 'hidden'; setTimeout(function () { ta.focus(); }, 50); load();
  }
  function close() { if (root) root.style.display = 'none'; document.documentElement.style.overflow = ''; }
  function load(cb) {
    if (KB) return cb && cb();
    fetch(BASE + 'kb.json', { cache: 'no-cache' }).then(function (r) { return r.json(); }).then(function (j) { KB = j; IDX = build(j.items); cb && cb(); })
      .catch(function () { if (body) body.innerHTML = '<div class="hdw-note">Chưa tải được nội dung hỏi đáp. Kiểm tra kết nối mạng rồi thử lại.</div>'; });
  }
  function card(c, tag, cls, full) {
    var x = full ? c.x : clip(c.x, 520);
    return '<div class="hdw-c"><span class="hdw-tag ' + cls + '">' + esc(tag) + '</span><h4>' + esc(c.t) + '</h4>' + md(x) +
      '<div class="hdw-src">' + esc(c.st) + ' · <button class="hdw-a" data-kb="' + KB.items.indexOf(c) + '">Mở trong trang</button></div></div>';
  }
  function rel(list, skip) {
    var seen = {}; if (skip != null) seen[KB.items[skip].t] = 1;
    list = list.filter(function (h) { var t = KB.items[h.i].t; if (seen[t]) return false; seen[t] = 1; return true; });
    return list.length ? '<div class="hdw-src" style="margin-top:10px">Nội dung liên quan trên trang:</div>' + list.map(function (h) {
      var c = KB.items[h.i]; return '<button class="hdw-rel" data-kb="' + h.i + '"><b>' + esc(c.t) + '</b><span>' + esc(c.st) + '</span></button>';
    }).join('') : '';
  }
  function ask() {
    var q = ta.value.trim(); if (q.length < 4 || BUSY) return; ta.value = '';
    load(function () {
      var r = search(q), H = r.hits, top = H[0], turn = document.createElement('div'); turn.className = 'hdw-turn';
      turn.innerHTML = '<div class="hdw-q">' + esc(q) + '</div>'; body.appendChild(turn);
      var qty = /bao lâu|bao nhiêu|mấy|khi nào|bao giờ|mức nào|ngày nào|tỷ lệ|bao lau|bao nhieu|\bmay\b|khi nao|bao gio|muc nao/i.test(q), k = top ? KB.items[top.i].k : '';
      var direct = !!top && r.W > 0 && ((k === 'faq' && top.cov >= 0.7 && top.tcov >= 0.55) ||
        (['law', 'fact', 'guide', 'doc'].indexOf(k) >= 0 && top.cov >= 0.6 && top.tcov >= 0.3 && !qty) ||
        (k === 'q' && top.cov >= 0.85 && top.tcov >= 0.5 && !qty));
      var enough = false;
      var ids = H.slice(0, 6).map(function (h) { return KB.items[h.i].id; });
      var aiOn = !!CFG.url;
      var aiBtn = aiOn ? '<button class="hdw-more" data-ai="' + esc(q) + '" data-ids=\'' + esc(JSON.stringify(ids)) + '\'>Hỏi thêm AI để giải thích</button>' : '';
      if (direct || enough) {
        var c = KB.items[top.i];
        turn.innerHTML += card(c, 'Có sẵn trên trang', 'k', c.k === 'faq' || c.k === 'law') + rel(H.slice(1, 6).filter(function (h) { return h.cov >= 0.4; }), top.i) + aiBtn;
      } else if (aiOn) {
        turn.innerHTML += (H.length ? '<div class="hdw-src">Trang chưa có câu trả lời trực tiếp, nên hỏi AI dựa trên các đoạn liên quan nhất của trang.</div>' : '');
        var rl = document.createElement('div'); rl.innerHTML = rel(H.slice(0, 3).filter(function (h) { return h.cov >= 0.3; }));
        askAI(q, ids, turn); turn.appendChild(rl);
      } else {
        turn.innerHTML += '<div class="hdw-note">Trang chưa có câu trả lời trực tiếp cho câu này. Phần hỏi AI chưa được bật' + (H.length ? '; dưới đây là nội dung gần nhất trên trang.' : '.') + '</div>' + (top && top.cov >= 0.5 ? card(KB.items[top.i], 'Gần nhất trên trang', 'r', false) + rel(H.slice(1, 5), top.i) : rel(H.slice(0, 4)));
      }
      turn.scrollIntoView({ block: 'start', behavior: 'smooth' });
    });
  }
  function askAI(q, ids, turn) {
    if (!CFG.url || BUSY) return; BUSY = true; send.disabled = true;
    var w = document.createElement('div'); w.className = 'hdw-wait'; w.textContent = 'AI đang soạn câu trả lời…'; turn.appendChild(w);
    var ctl = window.AbortController ? new AbortController() : null, tm = setTimeout(function () { ctl && ctl.abort(); }, 45000);
    fetch(CFG.url, { method: 'POST', headers: { 'Content-Type': 'text/plain;charset=utf-8' }, body: JSON.stringify({ q: q, ids: ids, pg: PAGE }), signal: ctl && ctl.signal, redirect: 'follow' })
      .then(function (r) { return r.json(); })
      .then(function (j) {
        w.remove();
        if (!j.ok) { turn.insertBefore(Object.assign(document.createElement('div'), { className: 'hdw-note', textContent: j.error || 'AI chưa trả lời được, vui lòng thử lại sau.' }), turn.lastChild && turn.lastChild.querySelector && turn.lastChild.querySelector('.hdw-rel') ? turn.lastChild : null); return; }
        var used = (j.used || []).map(function (id) { var i = -1; KB.items.some(function (c, k) { if (c.id === id) { i = k; return true; } }); return i; }).filter(function (i) { return i >= 0; });
        var web = (j.web || []).slice(0, 4);
        var box = document.createElement('div'), anchor = turn.lastChild && turn.lastChild.querySelector && turn.lastChild.querySelector('.hdw-rel') ? turn.lastChild : null; turn.insertBefore(box, anchor);
        box.insertAdjacentHTML('beforeend', '<div class="hdw-c"><span class="hdw-tag ai">AI Gemini · tham khảo</span>' + md(j.answer) +
          (used.length ? '<div class="hdw-src">Dựa trên: ' + used.map(function (i) { return '<button class="hdw-a" data-kb="' + i + '">' + esc(clip(KB.items[i].t, 60)) + '</button>'; }).join(' · ') + '</div>' : '') +
          (web.length ? '<div class="hdw-src">Nguồn tra cứu thêm: ' + web.map(function (x) { return '<a class="hdw-a" target="_blank" rel="noopener" href="' + esc(x.uri) + '">' + esc(clip(x.title || x.uri, 50)) + '</a>'; }).join(' · ') + '</div>' : '') +
          '<div class="hdw-src">Câu trả lời do AI soạn, có thể sai. Thông tin tham khảo, không thay cho tư vấn pháp lý.</div></div>');
      })
      .catch(function () { w.remove(); turn.insertAdjacentHTML('beforeend', '<div class="hdw-note">Không kết nối được tới máy chủ hỏi đáp. Vui lòng thử lại sau.</div>'); })
      .then(function () { clearTimeout(tm); BUSY = false; send.disabled = false; });
  }
  function fab() {
    if (document.querySelector('.hdw-fab')) return;
    var st = document.getElementById('hdw-css0'); if (!st) { st = document.createElement('style'); st.id = 'hdw-css0'; st.textContent = CSS; document.head.appendChild(st); }
    var b = document.createElement('button'); b.type = 'button'; b.className = 'hdw-fab'; b.innerHTML = IC + '<span>Hỏi đáp</span>'; b.setAttribute('aria-label', 'Mở hỏi đáp');
    b.addEventListener('click', open); document.body.appendChild(b);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fab); else fab();
  window.SSRHoiDap = { open: open, search: function (q, cb) { load(function () { var r = search(q); cb(r.hits.map(function (h) { var c = KB.items[h.i]; return { t: c.t, k: c.k, s: +h.s.toFixed(2), cov: +h.cov.toFixed(2), tcov: +h.tcov.toFixed(2) }; })); }); } };
})();
