/* ------------------------------ duong di cua tien: hai lan Le ra / Thuc te, xem tung chang ------------------------------ */
var LDX = {i: 0, timer: null, seq: [], pos: -1, played: {}};
var LDX_VL = {sai: "Sai", giai: "Cần giải trình", ro: "Chưa rõ", dung: "Đúng"};
var LDX_IC = {
  sai: '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>',
  giai: '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" aria-hidden="true"><path d="M12 5v9M12 19v.01"/></svg>',
  ro: '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" aria-hidden="true"><path d="M9.2 9a3 3 0 1 1 4 2.8c-.7.3-1.2.9-1.2 1.7v.5M12 18v.01"/></svg>',
  dung: '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>',
  play: '<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5.5v13l11-6.5z"/></svg>',
  pause: '<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M7 5h4v14H7zM13 5h4v14h-4z"/></svg>',
  chev: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg>'
};
function ldxRef(r){ var m = /Điều [0-9.a-z]+(, [0-9.a-z]+)*/.exec(r || ""); return m ? m[0] : (/Luật/.test(r || "") ? "Luật Nhà ở" : ""); }
function ldxTag(v, ref){ return v ? '<span class="vtag v-' + v + '">' + LDX_IC[v] + LDX_VL[v] + (ref && v !== "dung" ? '<em>' + esc(ref) + "</em>" : "") + "</span>" : ""; }
function renderLDX(){
  var box = $("ldx"); if (!box || !D.ldx) return;
  var C = D.ldx.cases, tot = {sai: 0, giai: 0, ro: 0, dung: 0};
  C.forEach(function(c){ Object.keys(tot).forEach(function(k){ tot[k] += c.cnt[k] || 0; }); });
  box.innerHTML =
    '<div class="ldx-tot">' + ["sai", "giai", "ro", "dung"].map(function(k){ return '<div class="lt v-' + k + '"><b>' + tot[k] + "</b><span>" + LDX_IC[k] + (k === "sai" ? "chặng sai Quy chế hoặc Luật" : k === "giai" ? "chặng cần Ban quản trị giải trình" : k === "ro" ? "chặng chưa rõ, chờ chứng từ" : "chặng đúng") + "</span></div>"; }).join("") + "</div>" +
    '<div class="ldx-tabs" role="tablist" aria-label="Chọn trường hợp">' + C.map(function(c, i){
      return '<button type="button" role="tab" class="ldx-tab" data-ldx="' + i + '" aria-selected="false"><span class="no">' + (i + 1) + '</span><span class="tx"><b>' + esc(c.amt) + "</b><small>" + esc(c.title) + '</small><span class="dots">' +
        ["sai", "giai", "ro", "dung"].map(function(k){ return c.cnt[k] ? '<i class="v-' + k + '" title="' + LDX_VL[k] + '">' + c.cnt[k] + "</i>" : ""; }).join("") + "</span></span></button>";
    }).join("") + "</div>" +
    '<div class="ldx-case" id="ldx-case"></div>';
  box.addEventListener("click", function(e){
    var t = e.target.closest ? e.target.closest("[data-ldx],[data-ldxn],#ldx-play,#ldx-prev,#ldx-next") : null; if (!t) return;
    if (t.hasAttribute("data-ldx")){ ldxShow(+t.getAttribute("data-ldx"), true); return; }
    if (t.hasAttribute("data-ldxn")){ ldxStop(); ldxFocus(+t.getAttribute("data-ldxn")); return; }
    if (t.id === "ldx-play"){ if (LDX.timer) ldxStop(); else ldxPlay(); return; }
    if (t.id === "ldx-prev"){ ldxStop(); ldxGo(LDX.pos - 1); return; }
    if (t.id === "ldx-next"){ ldxStop(); ldxGo(LDX.pos + 1); return; }
  });
  ldxShow(0, false);
  if ("IntersectionObserver" in window){
    var io = new IntersectionObserver(function(es){ es.forEach(function(en){ if (en.isIntersecting && en.intersectionRect.height > Math.min(260, window.innerHeight * 0.4) && !LDX.played[LDX.i] && !ldxReduced()){ LDX.played[LDX.i] = 1; ldxPlay(); } }); }, {threshold: [0, 0.05, 0.1, 0.2, 0.3, 0.5]});
    io.observe($("ldx-case"));
  }
}
function ldxReduced(){ try { return window.matchMedia("(prefers-reduced-motion: reduce)").matches; } catch (e) { return false; } }
function ldxShow(i, user){
  ldxStop(); LDX.i = i; var c = D.ldx.cases[i];
  qa("#ldx .ldx-tab").forEach(function(b){ b.setAttribute("aria-selected", +b.getAttribute("data-ldx") === i ? "true" : "false"); });
  var rule = c.rule.filter(function(x){ return x.t; }).map(function(x, j){ return (j ? '<span class="rc">' + LDX_IC.chev + "</span>" : "") + '<span class="rn"><b>' + esc(x.t) + "</b>" + (x.s ? "<small>" + esc(x.s) + "</small>" : "") + "</span>"; }).join("");
  var real = c.real.map(function(x, j){
    var st = x.n ? c.steps[x.n - 1] : null, tag = ldxTag(x.v, st ? ldxRef(st.ref) : "");
    if (x.lab != null) return '<div class="lk' + (x.v ? " v-" + x.v : "") + '" data-j="' + j + '"' + (x.n ? ' data-n="' + x.n + '"' : "") + '><span class="lk-l"><i class="coin"></i></span><span class="lk-t">' + (x.lab ? "<span>" + esc(x.lab) + "</span>" : "") + tag + "</span></div>";
    return '<div class="nd' + (x.v ? " v-" + x.v : "") + '" data-j="' + j + '"' + (x.n ? ' data-n="' + x.n + '"' : "") + '><div class="nd-h"><b>' + esc(x.t) + "</b>" + tag + "</div>" + (x.s ? '<div class="nd-s">' + esc(x.s) + "</div>" : "") +
      (x.items ? '<ul class="nd-i">' + x.items.map(function(it){ return "<li><span>" + esc(it[0]) + "</span><b>" + esc(it[1]) + "</b></li>"; }).join("") + "</ul>" : "") + "</div>";
  }).join("");
  var steps = c.steps.map(function(s, k){
    return '<button type="button" class="stp v-' + s.v + '" data-ldxn="' + (k + 1) + '"><span class="stp-n">' + (k + 1) + '</span><span class="stp-b"><span class="stp-q">' + esc(s.q) + ldxTag(s.v, "") + "</span>" +
      '<span class="stp-p"><span class="r1"><small>Lẽ ra</small>' + esc(s.rule) + '</span><span class="r2"><small>Thực tế</small>' + esc(s.real) + "</span></span>" + (s.ref ? '<span class="stp-ref">' + esc(s.ref) + "</span>" : "") + "</span></button>";
  }).join("");
  $("ldx-case").innerHTML =
    '<div class="ldx-hd"><div><div class="ldx-k">Trường hợp ' + (i + 1) + " / " + D.ldx.cases.length + " · " + esc(c.code) + "</div><h4>" + esc(c.title) + "</h4><p>" + esc(c.lede) + "</p></div></div>" +
    '<div class="ldx-rule"><span class="ldx-lh">Lẽ ra, theo Quy chế</span><div class="rchain">' + rule + "</div></div>" +
    '<div class="ldx-body"><div class="ldx-real"><div class="ldx-ctl"><span class="ldx-lh red">Thực tế trên sao kê</span><span class="ldx-btns"><button type="button" class="tbtn" id="ldx-prev" aria-label="Chặng trước">Trước</button><button type="button" class="tbtn pri" id="ldx-play">' + LDX_IC.play + '<span>Xem tiền đi</span></button><button type="button" class="tbtn" id="ldx-next" aria-label="Chặng sau">Sau</button></span></div>' +
      '<div class="ldx-cap" id="ldx-cap" aria-live="polite">Bấm Xem tiền đi để theo đồng tiền qua từng chặng, hoặc bấm từng bước bên ' + (window.innerWidth > 980 ? "phải" : "dưới") + ".</div>" +
      '<div class="rlane" id="ldx-lane">' + real + "</div></div>" +
    '<div class="ldx-steps"><div class="ldx-lh">So sánh từng bước</div>' + steps + '<div class="ldx-need"><b>Chứng từ cần để kết luận</b>' + esc(c.need) + "</div></div></div>";
  LDX.seq = qa("#ldx-lane > [data-j]"); LDX.pos = -1;
  if (user && !LDX.played[i] && !ldxReduced()){ LDX.played[i] = 1; setTimeout(ldxPlay, 250); }
}
function ldxGo(p){
  var S = LDX.seq; if (!S.length) return; p = Math.max(0, Math.min(S.length - 1, p)); LDX.pos = p;
  var c = D.ldx.cases[LDX.i];
  S.forEach(function(el, k){ el.classList.toggle("past", k < p); el.classList.toggle("cur", k === p); el.classList.remove("run"); });
  var el = S[p]; void el.offsetWidth; el.classList.add("run");
  var n = el.getAttribute("data-n"), st = n ? c.steps[n - 1] : null;
  qa("#ldx-case .stp").forEach(function(b){ b.classList.toggle("on", !!n && b.getAttribute("data-ldxn") === n); });
  var lab = el.classList.contains("lk") ? (el.querySelector(".lk-t > span:not(.vtag)") || {}).textContent : (el.querySelector(".nd-h b") || {}).textContent;
  $("ldx-cap").innerHTML = '<b>Chặng ' + (p + 1) + "/" + S.length + ":</b> " + esc(lab || "") + (st ? ' <span class="cap-v v-' + st.v + '">' + LDX_VL[st.v] + "</span> " + esc(st.v === "dung" ? st.real : "Lẽ ra " + st.rule.charAt(0).toLowerCase() + st.rule.slice(1) + ".") : "");
}
function ldxFocus(n){
  var S = LDX.seq, k = -1; for (var i = 0; i < S.length; i++) if (S[i].getAttribute("data-n") === String(n)){ k = i; break; }
  if (k >= 0){ ldxGo(k); if (window.innerWidth <= 980){ var r = S[k].getBoundingClientRect(); if (r.top < 60 || r.bottom > window.innerHeight - 70) window.scrollTo({top: window.scrollY + r.top - 140, behavior: ldxReduced() ? "auto" : "smooth"}); } }
  else qa("#ldx-case .stp").forEach(function(b){ b.classList.toggle("on", b.getAttribute("data-ldxn") === String(n)); });
}
function ldxPlay(){
  ldxStop(); var b = $("ldx-play"); if (!b) return;
  b.innerHTML = LDX_IC.pause + "<span>Tạm dừng</span>";
  if (LDX.pos >= LDX.seq.length - 1) LDX.pos = -1;
  var tick = function(){ if (LDX.pos >= LDX.seq.length - 1){ ldxStop(); return; } ldxGo(LDX.pos + 1); LDX.timer = setTimeout(tick, LDX.seq[LDX.pos].classList.contains("lk") ? 1500 : 1100); };
  tick();
}
function ldxStop(){
  if (LDX.timer){ clearTimeout(LDX.timer); LDX.timer = null; }
  var b = $("ldx-play"); if (b) b.innerHTML = LDX_IC.play + "<span>" + (LDX.pos >= LDX.seq.length - 1 && LDX.pos >= 0 ? "Xem lại" : "Xem tiền đi") + "</span>";
}
