/* ------------------------------ xem clip: trinh phat va danh sach ------------------------------ */
var CLP = {g: "full", cur: null, items: {}, groups: {}, auto: true, lastSave: 0, ready: false};
var CLP_ICON = {
  play: '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5.5v13l11-6.5z"/></svg>',
  dl: '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12M7 10l5 5 5-5M4 21h16"/></svg>',
  back: '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5"/></svg>'
};
function clpT(s){ s = Math.max(0, Math.round(s || 0)); var m = Math.floor(s / 60), x = s % 60; return m + ":" + (x < 10 ? "0" : "") + x; }
function clpLong(s){ s = Math.round(s || 0); var m = Math.floor(s / 60), x = s % 60; return (m ? m + " phút " : "") + (x ? x + " giây" : (m ? "" : "0 giây")).trim(); }
function clpGet(k){ try { return localStorage.getItem("ssrclip:" + k); } catch (e) { return null; } }
function clpSet(k, v){ try { if (v == null) localStorage.removeItem("ssrclip:" + k); else localStorage.setItem("ssrclip:" + k, String(v)); } catch (e) {} }
function clpIndex(){
  var C = D.clips; if (!C) return false; var t0 = 0;
  CLP.groups = {full: [], parts: [], docs: [], short: []};
  C.full.chapters.forEach(function(c, i){ var it = {id: c.id, src: c.src, title: c.title, dur: c.dur, poster: i === 0 ? C.full.poster : c.poster, thumb: c.poster, vert: false, g: "full", n: i + 1, t0: t0, mb: c.mb, tx: c.tx || [],
    kind: "Bản đầy đủ · chương " + (i + 1) + " / " + C.full.chapters.length, desc: C.full.desc}; t0 += c.dur; CLP.items[it.id] = it; CLP.groups.full.push(it); });
  C.parts.forEach(function(p, i){ var it = Object.assign({g: "parts", n: i + 1, thumb: p.poster}, p); CLP.items[it.id] = it; CLP.groups.parts.push(it); });
  C.docs.forEach(function(p, i){ var it = Object.assign({g: "docs", n: i + 1, thumb: p.poster}, p); CLP.items[it.id] = it; CLP.groups.docs.push(it); });
  var s = Object.assign({g: "short", n: 1, thumb: C.short.poster}, C.short); CLP.items[s.id] = s; CLP.groups.short.push(s);
  return true;
}
var CLP_GN = {full: "Bản đầy đủ", parts: "phần ngang", docs: "clip dọc", short: "Tóm tắt 90 giây"};
function clpGN(g){ var L = CLP.groups[g] || [], n = L.length; return g === "parts" ? (n === 1 ? "Phần " + L[0].n + " · ngang" : n + " phần ngang") : g === "docs" ? n + " clip dọc" : CLP_GN[g]; }
function clpGroupDur(g){ return CLP.groups[g].reduce(function(a, x){ return a + x.dur; }, 0); }
function renderClips(){
  var box = $("clip-app"); if (!box || !clpIndex()) return;
  var a = clpGet("auto"); CLP.auto = a == null ? true : a === "1";
  var tabs = ["full", "parts", "docs", "short"].filter(function(g){ return CLP.groups[g].length; }).map(function(g){
    return '<button type="button" role="tab" class="clp-tab" data-clg="' + g + '" aria-selected="false"><b>' + clpGN(g) + "</b><small>" + (g === "full" ? CLP.groups.full.length + " chương · " : "") + clpT(clpGroupDur(g)) + "</small></button>";
  }).join("");
  box.innerHTML =
    '<div class="clp-tabs" role="tablist" aria-label="Chọn bộ clip">' + tabs + "</div>" +
    '<div class="clp">' +
      '<div class="clp-main">' +
        '<div class="clp-stage" id="clp-stage"><video id="clp-v" controls playsinline webkit-playsinline preload="metadata" controlslist="nodownload"></video>' +
          '<button type="button" class="clp-big" id="clp-big" aria-label="Phát clip">' + CLP_ICON.play.replace('width="16" height="16"', 'width="34" height="34"') + "</button>" +
          '<div class="clp-spin" id="clp-spin" hidden><i></i></div><div class="clp-err" id="clp-err" hidden></div></div>' +
        '<div class="clp-meta"><div class="clp-kind" id="clp-kind"></div><h3 class="clp-t" id="clp-t"></h3><p class="clp-d" id="clp-d"></p>' +
          '<div class="clp-acts"><span class="clp-res" id="clp-res" hidden></span>' +
          '<label class="clp-auto"><input type="checkbox" id="clp-auto"' + (CLP.auto ? " checked" : "") + "> Tự phát clip tiếp theo</label>" +
          '<button type="button" class="tbtn" id="clp-dl">' + CLP_ICON.dl + "<span>Tải clip</span></button>" +
          '<button type="button" class="tbtn pri" id="clp-send">' + SHR_IC + "<span>Gửi clip</span></button>" +
          '<button type="button" class="tbtn" id="clp-share" data-share="#clip-full" data-st="Bộ clip Quỹ bảo trì">' + SHR_IC + "<span>Gửi link</span></button></div>" +
          '<button type="button" class="clp-back" id="clp-back" hidden></button>' +
          '<details class="clp-trd" id="clp-trd"><summary>Đọc lời thuyết minh <span id="clp-trn"></span></summary><div class="clp-tr" id="clp-tr"></div></details></div>' +
      "</div>" +
      '<aside class="clp-side" aria-label="Danh sách clip"><div class="clp-sh" id="clp-sh"></div><div class="clp-list" id="clp-list"></div></aside>' +
    "</div>" +
    (D.clips.qr_svg ? '<div class="clp-qr"><div class="qr">' + D.clips.qr_svg + '</div><div><b>Xem trên điện thoại</b><span>Mở camera điện thoại, hướng vào mã rồi bấm vào đường dẫn hiện ra. Không cần đăng nhập, không cần cài ứng dụng.</span></div></div>' : "") +
    '<p class="note">Clip trên trang là bản 720p để xem nhanh trên điện thoại. Bản gốc 1080p để chiếu Hội nghị nằm trong thư mục chia sẻ, mục 1.5 Clip. Trang nhớ chỗ bạn đang xem dở trên từng thiết bị.</p>';
  var v = $("clp-v");
  v.addEventListener("timeupdate", clpTick);
  v.addEventListener("play", function(){ $("clp-big").hidden = true; $("clp-stage").classList.add("on"); });
  v.addEventListener("ended", clpEnded);
  var spin = function(on){ $("clp-spin").hidden = !on; };
  v.addEventListener("waiting", function(){ spin(true); }); v.addEventListener("seeking", function(){ if (!v.paused) spin(true); });
  ["playing", "pause", "canplay", "seeked", "error", "ended"].forEach(function(ev){ v.addEventListener(ev, function(){ spin(false); }); });
  v.addEventListener("play", clpMark); v.addEventListener("pause", clpMark);
  v.addEventListener("error", function(){ clpErr(); });
  $("clp-big").addEventListener("click", function(){ var p = v.play(); if (p && p.catch) p.catch(function(){}); });
  $("clp-auto").addEventListener("change", function(){ CLP.auto = this.checked; clpSet("auto", this.checked ? "1" : "0"); });
  $("clp-dl").addEventListener("click", clpDownload);
  $("clp-send").addEventListener("click", clpSend);
  box.classList.add("xr-no");
  $("clp-back").addEventListener("click", clpGoBack);
  try { if (clpGet("trd") === "1") $("clp-trd").open = true; } catch (e) {}
  $("clp-trd").addEventListener("toggle", function(){ clpSet("trd", this.open ? "1" : "0"); CLP.trI = -2; clpTick(); });
  box.addEventListener("click", function(e){
    var t = e.target.closest ? e.target.closest("[data-clg],[data-clp],[data-clseek],[data-clres],[data-clt]") : null; if (!t) return;
    if (t.hasAttribute("data-clt")){ v.currentTime = +t.getAttribute("data-clt") + 0.01; var pp = v.play(); if (pp && pp.catch) pp.catch(function(){}); return; }
    if (t.hasAttribute("data-clg")){ clpGroup(t.getAttribute("data-clg"), true); return; }
    if (t.hasAttribute("data-clp")){ clpPlay(t.getAttribute("data-clp"), {play: true}); return; }
    if (t.hasAttribute("data-clres")){ v.currentTime = 0; clpSet("pos:" + CLP.cur.id, null); $("clp-res").hidden = true; var p = v.play(); if (p && p.catch) p.catch(function(){}); return; }
    if (t.hasAttribute("data-clseek")){
      var r = t.getBoundingClientRect(), f = Math.min(1, Math.max(0, (e.clientX - r.left) / r.width)), it = CLP.items[t.getAttribute("data-clseek")];
      clpPlay(it.id, {play: true, t: f * it.dur}); return;
    }
  });
  var last = clpGet("last"), it = last && CLP.items[last];
  clpGroup(it ? it.g : "full", false);
  clpPlay(it ? it.id : CLP.groups.full[0].id, {play: false});
  CLP.ready = true;
  var h = location.hash.slice(1);
  if (h.indexOf("clip-") === 0) clpDeep(h.slice(5));
}
function clpDeep(id){
  var it = CLP.items[id] || (id === "full" ? CLP.groups.full[0] : null); if (!it) return;
  if (typeof showView === "function") showView("clip", {hash: false});
  clpGroup(it.g, false); clpPlay(it.id, {play: false});
}
function clpGroup(g, loadFirst){
  CLP.g = g;
  qa("#clip-app .clp-tab").forEach(function(b){ b.setAttribute("aria-selected", b.getAttribute("data-clg") === g ? "true" : "false"); });
  var L = CLP.groups[g], vert = L[0].vert;
  var sh = "<b>" + clpGN(g) + "</b><span>" + L.length + (g === "full" ? " chương" : " clip") + " · " + clpLong(clpGroupDur(g)) + "</span>";
  if (g === "full") sh += '<div class="clp-bar" role="group" aria-label="Thanh tiến độ bản đầy đủ, bấm để tua">' + L.map(function(c){
      return '<button type="button" class="clp-seg" data-clseek="' + c.id + '" style="flex:' + c.dur.toFixed(1) + '" title="' + esc(c.n + ". " + c.title + " · " + clpT(c.t0)) + '" aria-label="' + esc("Chương " + c.n + ": " + c.title) + '"><i></i></button>';
    }).join("") + '</div><div class="clp-gt" id="clp-gt"></div>';
  $("clp-sh").innerHTML = sh;
  $("clp-list").className = "clp-list" + (vert ? " vert" : "");
  $("clp-list").innerHTML = L.map(function(it){
    var pos = +clpGet("pos:" + it.id) || 0, seen = clpGet("done:" + it.id);
    return '<button type="button" class="clp-it" data-clp="' + it.id + '"><span class="clp-th"><img alt="" loading="lazy" src="' + esc(it.thumb) + '" onerror="this.style.visibility=\'hidden\'">' +
      '<span class="clp-now"><i></i><i></i><i></i>Đang phát</span><span class="clp-du">' + (g === "full" ? clpT(it.t0) : clpT(it.dur)) + "</span>" + (pos > 5 && !seen ? '<span class="clp-pg" style="width:' + Math.min(100, pos / it.dur * 100).toFixed(1) + '%"></span>' : "") + "</span>" +
      '<span class="clp-tx"><small>' + (g === "full" ? "Chương " + it.n + " · " + clpT(it.dur) : g === "parts" ? "Phần " + it.n : g === "docs" ? "Clip " + it.n : "Tóm tắt") + (seen ? ' · <em>đã xem</em>' : "") + "</small><b>" + esc(it.title) + "</b></span></button>";
  }).join("");
  clpMark();
  if (loadFirst){
    var pick = L.filter(function(x){ return CLP.cur && x.id === CLP.cur.id; })[0] || L.filter(function(x){ return !clpGet("done:" + x.id); })[0] || L[0];
    if (!CLP.cur || CLP.cur.g !== g) clpPlay(pick.id, {play: false});
  }
}
function clpMark(){
  var v = $("clp-v"), playing = v && !v.paused && !v.ended;
  qa("#clp-list .clp-it").forEach(function(b){ var on = CLP.cur && b.getAttribute("data-clp") === CLP.cur.id; b.classList.toggle("on", on); b.classList.toggle("playing", !!(on && playing)); if (on) b.setAttribute("aria-current", "true"); else b.removeAttribute("aria-current"); });
}
function clpPlay(id, o){
  var it = CLP.items[id], v = $("clp-v"); if (!it || !v) return; o = o || {};
  if (CLP.g !== it.g) clpGroup(it.g, false);
  CLP.cur = it; clpSet("last", it.id);
  $("clp-err").hidden = true; $("clp-stage").classList.toggle("vert", !!it.vert); $("clp-stage").classList.remove("on");
  v.poster = it.poster; v.src = it.src; v.load();
  $("clp-kind").textContent = it.kind + " · " + clpLong(it.dur);
  $("clp-t").textContent = it.g === "full" ? D.clips.full.title : it.title;
  $("clp-d").textContent = it.g === "full" ? "Chương " + it.n + ": " + it.title + ". " + it.desc : it.desc;
  var shb = $("clp-share"); if (shb){ shb.setAttribute("data-share", "#clip-" + it.id); shb.setAttribute("data-st", it.g === "full" ? "Chương " + it.n + ": " + it.title : it.title); }
  $("clp-send").querySelector("span").textContent = it.g === "full" ? "Gửi chương này" : "Gửi clip";
  $("clp-dl").querySelector("span").textContent = (it.g === "full" ? "Tải chương này" : "Tải clip") + " (" + String(it.mb).replace(".", ",") + " MB)";
  var pos = o.t != null ? o.t : (+clpGet("pos:" + it.id) || 0), res = $("clp-res");
  if (o.t == null && pos > 8 && pos < it.dur - 8){ res.innerHTML = "Xem tiếp từ " + clpT(pos) + ' <button type="button" class="lnk" data-clres="1">' + CLP_ICON.back + "Xem từ đầu</button>"; res.hidden = false; }
  else { res.hidden = true; if (o.t == null) pos = 0; }
  var seek = function(){ if (pos > 0) { try { v.currentTime = pos; } catch (e) {} } };
  if (v.readyState >= 1) seek(); else v.addEventListener("loadedmetadata", seek, {once: true});
  $("clp-big").hidden = !!o.play;
  if (o.play){ var p = v.play(); if (p && p.catch) p.catch(function(){ $("clp-big").hidden = false; }); }
  var tx = it.tx || []; CLP.trI = -2;
  $("clp-trn").textContent = tx.length ? "(" + tx.length + " câu)" : "";
  $("clp-tr").innerHTML = tx.map(function(x, i){ return '<button type="button" class="clp-tl" data-clt="' + x[0] + '" data-i="' + i + '"><span>' + clpT(x[0]) + "</span>" + esc(x[2]) + "</button>"; }).join("");
  $("clp-trd").hidden = !tx.length;
  clpMark(); clpTick();
  if (o.play && window.innerWidth < 761){ var st = $("clp-stage"), r = st.getBoundingClientRect(); if (r.top < 50 || r.top > window.innerHeight * 0.5) window.scrollTo(0, window.scrollY + r.top - 60); }
}
function clpTick(){
  var it = CLP.cur, v = $("clp-v"); if (!it || !v) return; var t = v.currentTime || 0;
  if (it.g === "full"){
    var gt = $("clp-gt"); if (gt) gt.textContent = "Đang ở " + clpT(it.t0 + t) + " / " + clpT(D.clips.full.dur) + " · Chương " + it.n + ": " + it.title;
    qa("#clp-sh .clp-seg").forEach(function(s){ var c = CLP.items[s.getAttribute("data-clseek")], f = c.n < it.n ? 1 : c.n > it.n ? 0 : (t / c.dur); s.firstChild.style.width = (Math.min(1, f) * 100).toFixed(1) + "%"; s.classList.toggle("cur", c.n === it.n); });
  }
  var tx = it.tx || [], k = -1;
  for (var i = 0; i < tx.length; i++){ if (tx[i][0] <= t + 0.05) k = i; else break; }
  if (k !== CLP.trI){
    CLP.trI = k; var box = $("clp-tr"), on = box.querySelector(".clp-tl.on"); if (on) on.classList.remove("on");
    var ln = k >= 0 ? box.querySelector('.clp-tl[data-i="' + k + '"]') : null;
    if (ln){ ln.classList.add("on"); if ($("clp-trd").open && !CLP.trHold) box.scrollTop = Math.max(0, ln.offsetTop - box.offsetTop - box.clientHeight / 3); }
  }
  var now = Date.now(); if (t > 3 && now - CLP.lastSave > 4000){ CLP.lastSave = now; clpSet("pos:" + it.id, t.toFixed(1)); }
}
function clpEnded(){
  var it = CLP.cur; if (!it) return; clpSet("pos:" + it.id, null); clpSet("done:" + it.id, "1");
  var L = CLP.groups[it.g], i = L.indexOf(it), nx = L[i + 1];
  if (nx && (it.g === "full" || CLP.auto)){ clpPlay(nx.id, {play: true, t: 0}); clpGroup(it.g, false); clpMark(); toast((it.g === "full" ? "Chương tiếp: " : "Clip tiếp: ") + nx.title, 2600); }
  else { clpGroup(it.g, false); $("clp-big").hidden = false; }
}
function clpErr(){
  var e = $("clp-err"); e.hidden = false; $("clp-big").hidden = true;
  e.innerHTML = "<b>Chưa phát được clip ở chế độ xem này.</b><span>Nếu đang mở bản HTML đã tải về máy, clip chỉ xem được trên trang trực tuyến. Bản gốc có trong thư mục chia sẻ, mục 1.5 Clip.</span>";
}
function clpDownload(){
  var it = CLP.cur; if (!it) return;
  var name = (it.g === "full" ? "Ban day du - Chuong " + (it.n < 10 ? "0" : "") + it.n + " - " + it.title : it.g === "parts" ? "Phan " + it.n + " - " + it.title : it.g === "docs" ? "Clip " + (it.n < 10 ? "0" : "") + it.n + " - " + it.title : "Clip tom tat - " + it.title);
  name = name.replace(/[:\/\\?*"<>|]/g, " -").replace(/\s+/g, " ").trim() + ".mp4";
  toast("Đang tải " + it.mb.toString().replace(".", ",") + " MB…", 6000);
  fetch(it.src).then(function(r){ if (!r.ok) throw new Error(r.status); return r.arrayBuffer(); })
    .then(function(b){ return saveFile(name, new Uint8Array(b), "video/mp4"); })
    .catch(function(){ toast("Chưa tải được clip ở chế độ xem này. Bản gốc có trong thư mục chia sẻ, mục 1.5 Clip.", 6000); });
}
function clpFileName(it){
  var name = (it.g === "full" ? "Ban day du - Chuong " + (it.n < 10 ? "0" : "") + it.n + " - " + it.title : it.g === "parts" ? "Phan " + it.n + " - " + it.title : it.g === "docs" ? "Clip " + (it.n < 10 ? "0" : "") + it.n + " - " + it.title : "Clip tom tat - " + it.title);
  return "SSR - " + name.replace(/[:\/\\?*"<>|]/g, " -").replace(/\s+/g, " ").trim() + ".mp4";
}
function clpSend(){
  var it = CLP.cur; if (!it) return; var v = $("clp-v"); if (v && !v.paused) v.pause();
  shareFileGo(function(){ return fetch(it.src).then(function(r){ if (!r.ok) throw new Error(r.status); return r.blob(); }); }, clpFileName(it), "clip " + String(it.mb).replace(".", ",") + " MB");
}
function renderClipStrip(){
  var s = $("clip-strip"); if (!s || !D.clips) return; var C = D.clips;
  s.innerHTML = '<div class="cs-img"><img alt="" src="' + esc(C.full.poster) + '" onerror="this.parentNode.style.display=\'none\'"><span class="cs-play">' + CLP_ICON.play.replace('width="16" height="16"', 'width="28" height="28"') + "</span></div>" +
    '<div class="cs-tx"><span class="cs-k">Xem thay vì đọc</span><b>Bộ clip Quỹ bảo trì</b><small>Bản đầy đủ ' + clpT(C.full.dur) + " · " + C.docs.length + " clip dọc · tóm tắt " + clpT(C.short.dur) + "</small>" +
    '<span class="cs-bt"><button type="button" class="tbtn pri" data-clipgo="full">' + CLP_ICON.play + "Xem bản đầy đủ</button>" +
    '<button type="button" class="tbtn" data-clipgo="tom_tat">Tóm tắt 90 giây</button><button type="button" class="tbtn" data-clipgo="docs">Clip dọc cho điện thoại</button></span></div>' +
    (C.qr_svg ? '<div class="cs-qr"><div class="qr">' + C.qr_svg + "</div><small>Quét để xem<br>trên điện thoại</small></div>" : "");
  s.classList.add("xr-no");
  s.addEventListener("click", function(e){
    var t = e.target.closest ? e.target.closest("[data-clipgo]") : null, g = t ? t.getAttribute("data-clipgo") : "full";
    showView("clip"); if (!CLP.ready) return;
    if (g === "docs"){ clpGroup("docs", true); }
    else { var it = g === "full" ? CLP.groups.full[0] : CLP.items[g]; clpGroup(it.g, false); clpPlay(it.id, {play: false}); }
  });
}

/* nut Xem clip ngay trong tung muc phan tich, va nut quay lai muc dang doc */
var SEC_CLIPS = {"ket-luan": ["tom_tat", "doc_09"], "du-lieu": ["doc_01"], "tien-o-dau": ["doc_02"], "vi-sao": ["doc_03", "doc_05", "doc_06"],
  "khu-vuc-chung": ["doc_04"], "lai-suat": ["doc_07"], "quy-che": ["doc_08"], "dau-hieu": ["doc_09", "doc_11"], "ho-so": ["doc_10"], "muoi-cau-hoi": ["doc_10"]};
function renderSecClips(){
  if (!D.clips || !clpIndex()) return;
  Object.keys(SEC_CLIPS).forEach(function(sid){
    var sec = document.getElementById(sid); if (!sec) return;
    var anchor = sec.querySelector(":scope > .sec-h") || sec.querySelector(":scope > h3"); if (!anchor) return;
    var d = document.createElement("div"); d.className = "sclip xr-no";
    d.innerHTML = SEC_CLIPS[sid].map(function(id){ var it = CLP.items[id]; if (!it) return "";
      return '<button type="button" class="scl" data-sclip="' + id + '" data-from="' + sid + '"><span class="scl-th' + (it.vert ? " v" : "") + '"><img alt="" loading="lazy" src="' + esc(it.thumb) + '" onerror="this.style.visibility=\'hidden\'"><i>' + CLP_ICON.play + "</i></span>" +
        '<span class="scl-tx"><small>Xem clip · ' + clpLong(it.dur) + "</small><b>" + esc(it.title) + "</b></span></button>"; }).join("");
    anchor.parentNode.insertBefore(d, anchor.nextSibling);
  });
  document.addEventListener("click", function(e){
    var t = e.target.closest ? e.target.closest("[data-sclip]") : null; if (!t) return; e.preventDefault();
    var it = CLP.items[t.getAttribute("data-sclip")]; if (!it) return;
    showView("clip"); clpGroup(it.g, false); clpPlay(it.id, {play: true});
    var from = t.getAttribute("data-from"), sec = document.getElementById(from), h = sec && sec.querySelector("h2, h3");
    CLP.back = from; var b = $("clp-back"); b.hidden = false;
    b.innerHTML = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 6l-6 6 6 6"/></svg>Quay lại mục đang đọc' + (h ? ": <b>" + esc(h.textContent.slice(0, 70)) + "</b>" : "");
  });
}
function clpGoBack(){
  var el = CLP.back && document.getElementById(CLP.back); $("clp-back").hidden = true; CLP.back = null; if (!el) return;
  revealTarget(el); setTimeout(function(){ el.scrollIntoView({block: "start"}); }, 30);
}

/* nut chuyen nen sang, toi: nho theo tung may; lan dau theo cai dat cua may */
function initTheme(){
  var root = document.documentElement, saved = null;
  try { saved = localStorage.getItem("ssr-theme"); } catch (e) {}
  var cur = saved || (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
  root.setAttribute("data-theme", cur);
  var b = document.getElementById("btn-theme"); if (!b) return;
  var lab = function(){ var d = root.getAttribute("data-theme") === "dark"; b.setAttribute("aria-label", d ? "Chuyển sang nền sáng" : "Chuyển sang nền tối"); b.title = d ? "Nền sáng" : "Nền tối"; };
  lab();
  b.addEventListener("click", function(){
    var n = root.getAttribute("data-theme") === "dark" ? "light" : "dark"; root.setAttribute("data-theme", n); lab();
    try { localStorage.setItem("ssr-theme", n); } catch (e) {}
    if (typeof redrawIn === "function") redrawIn(document);
  });
}
/* muoi cau hoi: tinh trang tra loi cua Ban quan tri, nhom cu dan cap nhat; hien o trang dau va trong muc Muoi cau hoi */
var QST = [["chua", "Chưa trả lời"], ["mot", "Trả lời một phần"], ["thieu", "Đã trả lời, thiếu chứng từ"], ["du", "Đã trả lời đủ, có chứng từ"]];
function qstLabel(k){ for (var i = 0; i < QST.length; i++) if (QST[i][0] === k) return QST[i][1]; return QST[0][1]; }
function q10State(){
  var Q = D.q10, n = Q.t.length, cnt = {chua: 0, mot: 0, thieu: 0, du: 0}, last = "", st = [];
  for (var i = 0; i < n; i++){ var t = U.tracker["q" + i] || {}, s = cnt[t.s] != null ? t.s : "chua"; cnt[s]++; st.push(s); if (t.at && t.at > last) last = t.at; }
  var today = new Date(), due = new Date(Q.due + "T23:59:59+07:00"), late = Math.floor((today - due) / 86400000) + (today > due ? 1 : 0);
  return {n: n, cnt: cnt, st: st, last: last, late: late > 0 ? late : 0, got: n - cnt.chua};
}
function renderQ10(){
  if (!D.q10) return; var S = q10State(), Q = D.q10;
  var bar = '<div class="q10-bar" aria-hidden="true">' + S.st.map(function(s){ return '<i class="q-' + s + '"></i>'; }).join("") + "</div>";
  var lg = '<div class="q10-lg">' + QST.map(function(q){ return S.cnt[q[0]] ? '<span><i class="q-' + q[0] + '"></i>' + q[1] + ": <b>" + S.cnt[q[0]] + "</b></span>" : ""; }).join("") + "</div>";
  var noneTx = S.got === 0 && S.last ? "<p><b>Ban quản trị chưa trả lời câu nào.</b></p>" : "";
  var lateTx = S.got < S.n && S.late ? '<p class="q10-late">Tính tới hôm nay đã quá thời hạn đề nghị <b>' + S.late + " ngày</b>.</p>" : "";
  var upd = S.last ? "Tình trạng do nhóm cư dân cập nhật, lần cuối " + fmtIso(S.last).split(" ")[0] + "." : "Tình trạng do nhóm cư dân cập nhật khi nhận được trả lời.";
  var w = $("q10s");
  if (w){
    w.className = "q10s xr-no";
    w.innerHTML = '<div class="q10s-n"><b>' + S.got + "<small>/" + S.n + "</small></b><span>câu hỏi Ban quản trị đã trả lời</span></div>" +
      '<div class="q10s-tx"><div class="q10s-k">Mười câu hỏi gửi Ban quản trị</div><p>Gửi ngày ' + Q.sent_l + " qua email và kênh Zalo của Ban quản trị, đề nghị trả lời trong 5 ngày (tới " + Q.due_l + ").</p>" + noneTx + lateTx + bar + lg +
      '<p class="q10s-u">' + upd + '</p><a class="tbtn" href="#muoi-cau-hoi">Xem mười câu hỏi và tình trạng từng câu</a></div>';
  }
  var sum = $("q10-sum"); if (sum) sum.innerHTML = '<div class="q10-sumt"><b>' + S.got + "/" + S.n + "</b> câu Ban quản trị đã trả lời" + (S.cnt.du ? ", trong đó " + S.cnt.du + " câu đủ chứng từ" : "") + ". " + (S.got < S.n && S.late ? "Đã quá thời hạn đề nghị " + S.late + " ngày." : "") + "</div>" + bar;
  var ed = canWrite();
  qa(".q10-st[data-q]").forEach(function(el){
    var i = +el.getAttribute("data-q"), t = U.tracker["q" + i] || {}, s = S.st[i];
    el.innerHTML = ed ? '<select data-q10="' + i + '" aria-label="Tình trạng trả lời câu ' + (i + 1) + '">' + QST.map(function(q){ return '<option value="' + q[0] + '"' + (q[0] === s ? " selected" : "") + ">" + q[1] + "</option>"; }).join("") + '</select><input class="nt" data-q10n="' + i + '" type="text" maxlength="200" placeholder="Ghi chú: ngày trả lời, chứng từ đã nhận" value="' + esc(t.n || "") + '">'
      : '<span class="q10-pill q-' + s + '"><i></i>' + qstLabel(s) + "</span>" + (t.n ? '<span class="q10-nt">' + esc(t.n) + "</span>" : "");
  });
}
document.addEventListener("change", function(e){
  var t = e.target; if (!t || !t.matches) return;
  if (t.matches("select[data-q10]")){ var k = "q" + t.getAttribute("data-q10"), o = U.tracker[k] || {}; U.tracker[k] = {s: t.value, n: o.n || "", at: nowIso()}; DIRTY.tracker = true; afterTracker(); renderQ10(); }
  else if (t.matches("input[data-q10n]")){ var k2 = "q" + t.getAttribute("data-q10n"), o2 = U.tracker[k2] || {}; U.tracker[k2] = {s: o2.s || "chua", n: t.value.slice(0, 200), at: nowIso()}; DIRTY.tracker = true; afterTracker(); renderQ10(); }
});
/* dien thoai: nut mo khung Ho so da phan tich (mac dinh thu gon) */
function initFileToggle(){
  var f = document.querySelector("#tong-quan .file"); if (!f || f.querySelector(".file-t")) return;
  var b = document.createElement("button"); b.type = "button"; b.className = "file-t"; b.textContent = "Xem hồ sơ đã phân tích";
  b.addEventListener("click", function(){ var o = f.classList.toggle("open"); b.textContent = o ? "Thu gọn hồ sơ đã phân tích" : "Xem hồ sơ đã phân tích"; });
  f.appendChild(b);
}
/* nam van de o trang dau: trong tam de xem, moi van de mot the, di thang toi clip va duong tien cua chinh van de do */
var FIV = [
  {n: 1, v: "sai", st: "Thể hiện trên sao kê", h: "986,9 triệu tiền quỹ vào tài khoản của Ban quản trị", s: "Ngày 23/12/2025, chuyển vào tài khoản do chính các thành viên Ban quản trị đồng đứng tên. Đề nghị giải trình căn cứ theo Điều 7.2, 7.4 và 3.2.a Quy chế thu chi.", clip: "doc_03", ld: 0, sec: "vi-sao"},
  {n: 2, v: "sai", st: "Thể hiện trên sao kê", h: "1,71 tỷ tiền khu vực chung chưa vào quỹ", s: "Trong đó 1,40 tỷ đã chi ra, chưa thấy qua quy trình của quỹ. Cần hợp đồng, nghiệm thu từng khoản.", clip: "doc_04", ld: 1, sec: "khu-vuc-chung"},
  {n: 3, v: "ro", st: "Cần chứng từ", h: "13 khoản chi trên 50 triệu, tổng 5,04 tỷ", s: "Chưa thấy văn bản cho phép của chủ sở hữu, báo giá và nghiệm thu.", clip: "doc_05", ld: 3, sec: "quy-che"},
  {n: 4, v: "ro", st: "Cần chứng từ", h: "1,69 tỷ chưa truy được tới cùng", s: "Trong đó 705,8 triệu trả trọn cho Thép Quang; cần danh mục hàng hóa, biên bản giao nhận và kiểm đếm thực tế.", clip: "doc_06", ld: 2, sec: "vi-sao"},
  {n: 5, v: "ro", st: "Cần chứng từ", h: "127,5 tỷ tiền gửi sau tái tục chưa có xác nhận", s: "Sao kê dừng ở 31/05/2026; cần hợp đồng và xác nhận của ngân hàng.", clip: "doc_07", ld: 4, sec: "lai-suat"}
];
function renderFive(){
  var el = $("fiv"); if (!el) return; var hasClip = D.clips && clpIndex();
  el.className = "fiv xr-no";
  el.innerHTML = '<div class="fiv-h"><span class="fiv-k">Trọng tâm</span><h2>Năm điểm đề nghị Ban quản trị làm rõ</h2><p>198 giao dịch đã đối chiếu khớp số dư sao kê. Số dư khớp chưa cho biết tiền chi có đúng giá trị hợp đồng và quỹ có nhận đúng hàng hóa, dịch vụ hay không. Hai điểm đầu thể hiện trực tiếp trên sao kê; ba điểm sau cần hợp đồng, nghiệm thu, hóa đơn, kể cả hậu kiểm.</p></div>' +
    '<ol class="fiv-l">' + FIV.map(function(f){
      var it = hasClip ? CLP.items[f.clip] : null;
      return '<li class="fv fv-' + f.v + '"><div class="fv-top"><span class="fv-n">' + f.n + '</span><span class="fv-st">' + f.st + "</span></div><b class=\"fv-h\">" + esc(f.h) + '</b><p class="fv-s">' + esc(f.s) + "</p>" +
        '<div class="fv-a">' + (it ? '<button type="button" class="tbtn pri" data-fivclip="' + f.clip + '">' + CLP_ICON.play + "Xem clip " + clpT(it.dur) + "</button>" : "") +
        '<button type="button" class="tbtn" data-fivld="' + f.ld + '">Xem đường tiền</button><a class="fv-more" href="#' + f.sec + '">Đọc phân tích</a></div></li>';
    }).join("") + "</ol>";
  el.addEventListener("click", function(e){
    var t = e.target.closest ? e.target.closest("[data-fivclip],[data-fivld]") : null; if (!t) return;
    if (t.hasAttribute("data-fivclip")){ var it = CLP.items[t.getAttribute("data-fivclip")]; showView("clip"); clpGroup(it.g, false); clpPlay(it.id, {play: true}); return; }
    showView("tien"); if (typeof ldxShow === "function") ldxShow(+t.getAttribute("data-fivld"), true);
  });
}
