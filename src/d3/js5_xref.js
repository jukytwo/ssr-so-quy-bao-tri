
/* ============================== LIEN KET CHEO: bam vao ten, so tien, tai khoan, dieu khoan, ma dau hieu de xem ngay thong tin lien quan ============================== */
var XR = (D && D.xref) || {};
var XR_RE = null, XR_MAP = {}, XR_HIST = [], XR_BUSY = false;
function xrEsc(s){ return String(s).replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); }
function xrBuild(){
  var al = [];
  Object.keys(XR).forEach(function(k){ (XR[k].a || []).forEach(function(a){ if (!XR_MAP[a]){ XR_MAP[a] = k; al.push(a); } }); });
  al.sort(function(a, b){ return b.length - a.length; });
  if (!al.length) return;
  try { XR_RE = new RegExp("(?<![\\p{L}\\p{N}])(" + al.map(xrEsc).join("|") + ")(?![\\p{L}\\p{N}])", "gu"); }
  catch (e) { XR_RE = new RegExp("(" + al.map(xrEsc).join("|") + ")", "g"); }
}
var XR_SKIP = {SCRIPT:1, STYLE:1, BUTTON:1, A:1, INPUT:1, TEXTAREA:1, SELECT:1, OPTION:1, svg:1, SVG:1, CODE:1, LABEL:1, SUMMARY:0};
function xrWrap(root){
  if (!XR_RE || !root) return;
  var tw = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {acceptNode: function(n){
    if (!n.nodeValue || n.nodeValue.length < 3) return NodeFilter.FILTER_REJECT;
    for (var p = n.parentNode; p && p !== root; p = p.parentNode){
      if (XR_SKIP[p.nodeName] || (p.classList && (p.classList.contains("xr") || p.classList.contains("xr-no") || p.classList.contains("nav") || p.classList.contains("toc")))) return NodeFilter.FILTER_REJECT;
      if (p.namespaceURI && p.namespaceURI.indexOf("svg") >= 0) return NodeFilter.FILTER_REJECT;
    }
    XR_RE.lastIndex = 0; return XR_RE.test(n.nodeValue) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT; }});
  var list = []; while (tw.nextNode()) list.push(tw.currentNode);
  list.forEach(function(n){
    var s = n.nodeValue, frag = document.createDocumentFragment(), last = 0, m; XR_RE.lastIndex = 0;
    while ((m = XR_RE.exec(s))){
      var k = XR_MAP[m[1]]; if (!k) continue;
      if (m.index > last) frag.appendChild(document.createTextNode(s.slice(last, m.index)));
      var sp = document.createElement("span"); sp.className = "xr"; sp.setAttribute("data-x", k); sp.setAttribute("role", "button"); sp.tabIndex = 0;
      sp.textContent = m[1]; frag.appendChild(sp); last = m.index + m[1].length;
    }
    if (last < s.length) frag.appendChild(document.createTextNode(s.slice(last)));
    n.parentNode.replaceChild(frag, n);
  });
}
function xrSecTitle(el){
  var s = el.closest ? el.closest(".panel, section, .card, details") : null, t = "";
  while (s && !t){ var h = s.querySelector("h2, h3, h4, summary"); t = h ? h.textContent.trim() : ""; s = s.parentElement ? s.parentElement.closest(".panel, section") : null; }
  var v = (typeof viewOf === "function") ? viewOf(el) : null; var vn = (typeof VIEW_NAME !== "undefined" && v && VIEW_NAME[v]) ? VIEW_NAME[v] : "";
  return (vn ? vn + " · " : "") + (t || "Nội dung");
}
function xrSnip(el){
  var b = el.closest ? (el.closest("p, li, tr, .nd, div") || el.parentNode) : el.parentNode, s = (b.textContent || "").replace(/\s+/g, " ").trim();
  for (var up = 0; s.length < 50 && up < 3 && b.parentElement; up++){ b = b.parentElement; s = (b.textContent || "").replace(/\s+/g, " ").trim(); }
  var w = el.textContent, i = Math.max(0, s.indexOf(w));
  var a = Math.max(0, i - 70), e = Math.min(s.length, i + w.length + 90);
  return (a > 0 ? "…" : "") + s.slice(a, e) + (e < s.length ? "…" : "");
}
function xrH(s){ return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
function xrMoney(v){ if (!v) return ""; return v >= 1e9 ? (v / 1e9).toFixed(2).replace(".", ",") + " tỷ" : (v / 1e6).toFixed(1).replace(".", ",") + " triệu"; }
var XR_SEV = {"Đỏ": "var(--crit)", "Cam": "var(--warn)", "Vàng": "var(--cau)"};
function xrDrawer(){
  var d = document.getElementById("xr-dr"); if (d) return d;
  d = document.createElement("aside"); d.id = "xr-dr"; d.className = "xr-no"; d.setAttribute("aria-label", "Thông tin liên quan");
  d.innerHTML = '<div class="xr-hd"><button type="button" class="xr-bk" aria-label="Quay lại">&#8249;</button><div class="xr-tt"></div><button type="button" class="xr-x" aria-label="Đóng">&#215;</button></div><div class="xr-bd"></div>';
  document.body.appendChild(d);
  d.querySelector(".xr-x").addEventListener("click", xrClose);
  d.querySelector(".xr-bk").addEventListener("click", function(){ XR_HIST.pop(); var k = XR_HIST.pop(); if (k) xrOpen(k); });
  return d;
}
function xrClose(){ var d = document.getElementById("xr-dr"); if (d) d.classList.remove("on"); XR_HIST = []; document.body.classList.remove("xr-open"); }
function xrOpen(k){
  var e = XR[k]; if (!e) return;
  var d = xrDrawer(); XR_HIST.push(k);
  d.querySelector(".xr-bk").style.visibility = XR_HIST.length > 1 ? "visible" : "hidden";
  d.querySelector(".xr-tt").innerHTML = '<small>' + xrH(e.t) + '</small><b>' + xrH(e.t === "Dấu hiệu" ? e.l + " · " + (e.title || "") : e.l) + '</b>';
  var h = "";
  if (e.t === "Dấu hiệu"){
    h += '<div class="xr-sev" style="--c:' + (XR_SEV[e.sev] || "var(--na)") + '">Mức ' + xrH(e.sev) + (e.amt ? " · " + xrMoney(e.amt) : "") + '</div>';
    h += '<p class="xr-d">' + xrH(e.d) + '</p><div class="xr-k">Căn cứ</div><p class="xr-s">' + xrH(e.rule) + '</p><div class="xr-k">Cần làm rõ</div><p class="xr-s">' + xrH(e.ask) + '</p>';
  } else {
    h += '<p class="xr-d">' + xrH(e.d) + '</p>';
    if (e.f && e.f.length){
      h += '<div class="xr-k">Dấu hiệu liên quan</div><div class="xr-fl">' + e.f.map(function(f){ var F = XR[f] || {};
        return '<button type="button" class="xr-f" data-go="' + f + '" style="--c:' + (XR_SEV[F.sev] || "var(--na)") + '"><b>' + f + '</b><span>' + xrH(F.title || "") + '</span></button>'; }).join("") + '</div>';
    }
  }
  var rel = (e.rel || []).filter(function(r){ return XR[r]; }).slice(0, 14);
  if (rel.length) h += '<div class="xr-k">Liên quan</div><div class="xr-ch">' + rel.map(function(r){ return '<button type="button" class="xr-c" data-go="' + r + '"><small>' + xrH(XR[r].t) + '</small>' + xrH(XR[r].l) + '</button>'; }).join("") + '</div>';
  var occ = Array.prototype.slice.call(document.querySelectorAll('#root .xr[data-x="' + k + '"]')), seen = {}, rows = [];
  occ.forEach(function(el, i){ var t = xrSecTitle(el); if ((seen[t] = (seen[t] || 0) + 1) > 2 || rows.length >= 18) return; rows.push('<button type="button" class="xr-o" data-occ="' + i + '"><small>' + xrH(t) + '</small><span>' + xrH(xrSnip(el)) + '</span></button>'); });
  h += '<div class="xr-k">Xuất hiện trong sổ quỹ · ' + occ.length + ' chỗ</div><div class="xr-ol">' + (rows.join("") || '<p class="xr-s">Chưa có trong phần đang hiển thị.</p>') + '</div>';
  var bd = d.querySelector(".xr-bd"); bd.innerHTML = h; bd.scrollTop = 0;
  xrWrap(bd.querySelector(".xr-d")); xrWrap(bd.querySelectorAll(".xr-s")[0]);
  bd.querySelectorAll(".xr-d .xr, .xr-s .xr").forEach(function(x){ if (x.getAttribute("data-x") === k) x.classList.add("xr-self"); });
  bd.querySelectorAll("[data-go]").forEach(function(b){ b.addEventListener("click", function(){ xrOpen(b.getAttribute("data-go")); }); });
  bd.querySelectorAll("[data-occ]").forEach(function(b){ b.addEventListener("click", function(){ var el = occ[+b.getAttribute("data-occ")]; if (!el) return;
    if (typeof revealTarget === "function") revealTarget(el); var dt = el.closest("details"); if (dt) dt.open = true;
    setTimeout(function(){ el.scrollIntoView({block: "center", behavior: "smooth"}); el.classList.remove("xr-flash"); void el.offsetWidth; el.classList.add("xr-flash"); }, 80);
    if (window.matchMedia && window.matchMedia("(max-width: 760px)").matches) xrClose(); }); });
  d.classList.add("on"); document.body.classList.add("xr-open");
}
function xrInit(){
  xrBuild(); var root = document.getElementById("root"); if (!XR_RE || !root) return;
  XR_BUSY = true; xrWrap(root); XR_BUSY = false;
  document.addEventListener("click", function(ev){ var x = ev.target && ev.target.closest ? ev.target.closest(".xr") : null; if (!x) return; ev.preventDefault(); ev.stopPropagation(); xrOpen(x.getAttribute("data-x")); }, true);
  document.addEventListener("keydown", function(ev){ if (ev.key === "Escape") xrClose(); var x = ev.target; if ((ev.key === "Enter" || ev.key === " ") && x && x.classList && x.classList.contains("xr")){ ev.preventDefault(); xrOpen(x.getAttribute("data-x")); } });
  var tmr = null;
  if (window.MutationObserver) new MutationObserver(function(){ if (XR_BUSY) return; clearTimeout(tmr); tmr = setTimeout(function(){ XR_BUSY = true; xrWrap(root); XR_BUSY = false; }, 350); }).observe(root, {childList: true, subtree: true});
  if (!sessionStorageSafe("xr-hint") && !localOnce("xr-hint")){ setTimeout(function(){ if (typeof VIEW_CUR !== "undefined" && VIEW_CUR === "clip") return; if (typeof toast === "function") toast("Mẹo: bấm vào tên doanh nghiệp, số tiền, tài khoản, điều khoản có gạch chấm để xem ngay thông tin liên quan."); }, 1500); }
}
function localOnce(k){ try { var v = localStorage.getItem(k); localStorage.setItem(k, "1"); return v; } catch (e) { return null; } }
function sessionStorageSafe(k){ try { var v = sessionStorage.getItem(k); sessionStorage.setItem(k, "1"); return v; } catch (e) { return "1"; } }
try { xrInit(); } catch (e) { if (window.console) console.warn("xref", e); }
