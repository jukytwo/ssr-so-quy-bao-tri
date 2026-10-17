// Dựng kho nội dung cho nút Hỏi đáp: lấy chữ đang hiện trên trang Quỹ bảo trì (đã qua bộ lọc ngôn từ)
// và thư viện quy định, hướng dẫn, thông tin tòa nhà của mục Điều hành. Không lấy dữ liệu mẫu.
// Chạy: node src/hoidap/build_kb.js   (cần Playwright)   ->  web/hoi-dap/kb.json
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const ROOT = path.resolve(__dirname, '..', '..'), OUT = path.join(ROOT, 'web', 'hoi-dap', 'kb.json');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
  await p.goto('file://' + path.join(ROOT, 'web', 'index.html')); await p.waitForTimeout(2500);
  const q = await p.evaluate(() => {
    document.querySelectorAll('details').forEach(d => d.open = true);
    const SKIP = new Set(['cap-nhat', 'tai-ve', 'xem-clip']);
    const HEAD = 'h1,h2,h3,h4,.h3x,summary,.pt';
    const BLOCK = 'p,li,tr,dt,dd,blockquote,figcaption,' + HEAD;
    const clean = s => String(s || '').replace(/\s+/g, ' ').trim();
    const out = [];
    document.querySelectorAll('#hoi-dap details.qa').forEach(d => {
      const qq = clean((d.querySelector('.qa-q') || {}).textContent), aa = [...d.querySelectorAll('.qa-a p, .qa-a li')].map(e => clean(e.textContent)).filter(Boolean).join('\n'), tag = clean((d.querySelector('.qa-meta .pill') || {}).textContent);
      if (qq && aa) out.push({ s: 'hoi-dap', a: d.id, st: 'Hỏi đáp' + (tag ? ' · ' + tag : ''), t: qq, x: aa, k: 'faq' });
    });
    SKIP.add('hoi-dap');
    document.querySelectorAll('#root section[id]').forEach(sec => {
      if (SKIP.has(sec.id)) return;
      const h2 = sec.querySelector('h2'); const secTitle = clean(h2 ? h2.textContent : sec.id);
      let cur = { t: secTitle, x: [] }; const chunks = [cur];
      const take = (el) => {
        if (el.matches('script,style,svg,button,select,input,textarea,.no-kb')) return;
        if (el.matches(HEAD)) { const t = clean(el.textContent); if (t && t.length < 220) { cur = { t, x: [] }; chunks.push(cur); return; } }
        if (el.matches(BLOCK)) {
          let t = el.matches('tr') ? [...el.children].map(c => clean(c.textContent)).filter(Boolean).join(' · ') : clean(el.textContent);
          if (t && t.length > 2) cur.x.push(t); return;
        }
        const own = [...el.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent).join(' ').trim();
        if (own.length > 15 && !el.querySelector(BLOCK + ',div')) { cur.x.push(clean(el.textContent)); return; }
        [...el.children].forEach(take);
      };
      [...sec.children].forEach(take);
      chunks.forEach(c => {
        let buf = [], len = 0, part = 0;
        const flush = () => { if (!buf.length) return; out.push({ s: sec.id, st: secTitle, t: c.t, x: buf.join('\n'), k: sec.id === 'hoi-dap' && /\?$/.test(c.t) ? 'faq' : 'q' }); buf = []; len = 0; part++; };
        const seen = new Set();
        c.x.forEach(t => { if (seen.has(t)) return; seen.add(t); if (len + t.length > 1100) flush(); buf.push(t); len += t.length; });
        flush();
      });
    });
    return out;
  });
  await p.goto('file://' + path.join(ROOT, 'web', 'dieu-hanh', 'index.html')); await p.waitForTimeout(1500);
  const d = await p.evaluate(() => {
    const out = [], st = S.settings;
    LAW.forEach(l => out.push({ s: 'phap-ly', st: 'Kiểm tra pháp lý (mục Điều hành)', t: l.title, x: `${l.rule}\nCăn cứ: ${l.basis}\nTrách nhiệm: ${l.who || ''}`, k: 'law', id: 'law-' + l.id }));
    GUIDE_T.forEach(g => (g[1] || []).forEach(it => out.push({ s: 'huong-dan', st: 'Hướng dẫn dùng mục Điều hành: ' + g[0], t: it[0], x: it[1], k: 'guide' })));
    if (typeof BQT_REAL !== 'undefined') out.push({ s: 'tuan-thu', st: 'Ban Quản trị', t: 'Thành viên Ban Quản trị SSR, trưởng ban và lĩnh vực phụ trách', x: BQT_REAL.map(r => `${r[0]}${(typeof BQT_POS !== 'undefined' && BQT_POS[r[0]]) ? ' (' + BQT_POS[r[0]] + ')' : ' (thành viên)'}: ${r[1]}`).join('\n') + '\nTheo sơ đồ phân công Ban Quản trị. Chức danh phó ban, căn hộ và nhiệm kỳ chưa có trong công cụ.', k: 'fact' });
    const fl = st.floorsByBlock || {};
    out.push({ s: 'cai-dat', st: 'Thông tin tòa nhà', t: 'Thông tin chung SSR: phí quản lý, số block, số tầng, số căn, thang máy', x: [
      `Phí quản lý ${num(st.feeRate || 11000)} đồng/m² mỗi tháng, chưa gồm VAT ${st.vatRate || 10}%.`,
      `Sáu block: ${Object.keys(fl).map(k => 'Block ' + k + ' ' + fl[k] + ' tầng').join(', ')}. Từ tầng 19 trở xuống mỗi tầng 13 căn. Mỗi block 3 thang máy.`,
      'Chung cư đã có Ban Quản trị; Ban Quản trị đang giữ quỹ bảo trì.'].join('\n'), k: 'fact' });
    return out;
  });
  await b.close();
  // tài liệu bổ sung do Ban điều hành trang thêm vào: web/hoi-dap/tai-lieu/*.txt (dòng đầu là tiêu đề)
  const extra = [], dir = path.join(ROOT, 'web', 'hoi-dap', 'tai-lieu');
  if (fs.existsSync(dir)) fs.readdirSync(dir).filter(f => f.endsWith('.txt')).forEach(f => {
    const lines = fs.readFileSync(path.join(dir, f), 'utf8').split(/\r?\n/), title = lines.shift().trim();
    let buf = [], len = 0, head = title; const flush = () => { if (buf.length) extra.push({ s: 'tai-lieu', st: title, t: head, x: buf.join('\n'), k: 'doc', f }); buf = []; len = 0; };
    lines.forEach(l => { const t = l.trim(); if (!t) return; if (/^(Điều|Chương|Mục)\s+\d+/i.test(t) && t.length < 160) { flush(); head = t; } if (len + t.length > 1100) flush(); buf.push(t); len += t.length; });
    flush();
  });
  const all = q.map(c => Object.assign(c, { pg: 'q' })).concat(d.map(c => Object.assign(c, { pg: 'd' })), extra.map(c => Object.assign(c, { pg: 'q' })));
  const crypto = require('crypto'), seen = {};
  all.forEach(c => { let id = c.id || ('k' + crypto.createHash('md5').update(c.pg + '|' + c.s + '|' + c.t + '|' + c.x.slice(0, 80)).digest('hex').slice(0, 10)); while (seen[id]) id += 'x'; seen[id] = 1; c.id = id; });
  const kb = { v: 1, built: new Date().toISOString().slice(0, 10), n: all.length, items: all };
  fs.writeFileSync(OUT, JSON.stringify(kb));
  const by = {}; all.forEach(c => by[c.k] = (by[c.k] || 0) + 1);
  console.log('kb.json', all.length, 'mục', JSON.stringify(by), Math.round(fs.statSync(OUT).size / 1024) + ' KB');
})();
