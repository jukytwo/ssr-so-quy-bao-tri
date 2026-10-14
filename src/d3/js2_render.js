/* ============================== tooltip ============================== */
function tipEl(){ return $("tip"); }
function showTip(ev, html){ var tip = tipEl(); if (!tip) return; tip.innerHTML = html; tip.hidden = false; var x = ev.clientX + 14, y = ev.clientY + 14; var w = tip.offsetWidth, h = tip.offsetHeight; if (x + w > window.innerWidth - 8) x = ev.clientX - w - 14; if (y + h > window.innerHeight - 8) y = ev.clientY - h - 14; tip.style.left = Math.max(8, x) + "px"; tip.style.top = Math.max(8, y) + "px"; }
function hideTip(){ var tip = tipEl(); if (tip) tip.hidden = true; }
function bindTip(node, html){
  node.addEventListener("mousemove", function(e){ showTip(e, html); });
  node.addEventListener("mouseleave", hideTip);
  node.setAttribute("tabindex", "0");
  node.addEventListener("focus", function(){ var r = node.getBoundingClientRect(); showTip({clientX: r.left + r.width / 2, clientY: r.top}, html); });
  node.addEventListener("blur", hideTip);
  node.addEventListener("click", function(e){ showTip(e, html); });
}
window.addEventListener("scroll", hideTip, {passive: true});

var SEC = D.sec, SECK = Object.keys(SEC).sort();
function secIds(p){ return SECK.filter(function(no){ return SEC[no].p === p; }); }

/* ============================== conclusions, parts ============================== */
function klHtml(no){
  var c = D.concl[no]; if (!c) return "";
  var ft = D.faq && D.faq.sec[no], fn = ft ? D.faq.items.filter(function(i){ return i.t === ft; }).length : 0, fl = "";
  if (fn){ var ftn = D.faq.topics.filter(function(t){ return t.id === ft; })[0]; fl = '<a class="kl-hd" href="#hoi-dap" data-hdt="' + ft + '">' + hdIc("chat", 15) + "Hỏi đáp: " + fn + " câu về " + esc(ftn.l.toLowerCase()) + "</a>"; }
  return '<div class="kl tone-' + c[1] + '"><div class="kh"><span class="lab">Kết luận mục ' + no + '</span><span class="pill"><i class="dot"></i>' + esc(c[0]) + '</span></div>' + c[2].map(function(s){ return "<p>" + esc(s) + "</p>"; }).join("") + fl + "</div>";
}
function renderKL(){ qa(".kl-slot").forEach(function(s){ s.outerHTML = klHtml(s.getAttribute("data-no")); }); }
function renderPartChips(){
  qa(".pchips").forEach(function(box){
    var p = +box.getAttribute("data-part"), items;
    if (box.getAttribute("data-part") === "hd") items = [];
    else if (p === 6) items = [["cap-nhat", "Cập nhật sao kê mới"], ["giao-dich", "Tra cứu giao dịch"], ["tai-ve", "Tải về"], ["tu-dien", "Thuật ngữ"]].map(function(x){ return '<a class="pchip tone-n" href="#' + x[0] + '">' + x[1] + "</a>"; });
    else items = secIds(p).map(function(no){ var c = D.concl[no]; return '<a class="pchip tone-' + (c ? c[1] : "n") + '" href="#' + SEC[no].id + '"><span class="no">' + no + "</span>" + esc(SEC[no].t) + '<i class="dot"></i></a>'; });
    box.innerHTML = items.join("");
  });
}

/* ============================== hero ============================== */
var sevCount = {"Đỏ": 0, "Cam": 0, "Vàng": 0};
D.findings.forEach(function(f){ sevCount[f.sev]++; });
function delta(v){ return M.hasNew && Math.abs(v) >= 1 ? '<div class="dlt">' + signed(v) + " từ dữ liệu mới</div>" : ""; }
function renderHero(){
  var B = D.base, g = M.g;
  $("ansr").textContent = D.verdict.answer;
  $("hero-eyebrow").textContent = "Sao kê ngân hàng 15/08/2024 – " + M.asof + (M.hasNew ? ", gồm dữ liệu nạp thêm" : "");
  $("lede").innerHTML = "Quỹ nhận <b>" + ty(D.fund_in) + " tỷ</b> ngày 15/08/2024 và có thêm <b>" + ty(M.interest) + " tỷ</b> tiền lãi. Đã chi <b>" + ty(M.spend) + " tỷ</b>, trong đó <b>" + ty(D.opaque) + " tỷ</b> đi vào tài khoản của chính Ban quản trị hoặc trả cho Thép Quang mà hàng hóa mô tả chung chung. Ngoài ra <b>" + ty(M.ca_total) + " tỷ</b> thu từ khu vực chung không nộp vào quỹ như Luật Nhà ở 2023 yêu cầu.";
  var chips = [["Đỏ", "dấu hiệu mức Đỏ"], ["Cam", "dấu hiệu mức Cam"], ["Vàng", "dấu hiệu mức Vàng"]].map(function(x){ return '<a class="pill sev-' + x[0] + '" href="#dau-hieu" data-sev="' + x[0] + '" style="text-decoration:none"><i class="dot"></i>' + sevCount[x[0]] + " " + x[1] + "</a>"; }).join("");
  chips += '<a class="pill sev-ok" href="#giam-dinh" style="text-decoration:none"><i class="dot"></i>Không có dấu hiệu làm giả bằng AI</a>';
  var nn = g.cnt["Đỏ"] + g.cnt["Cam"] + g.cnt["Vàng"];
  if (M.hasNew) chips += '<a class="pill ' + (g.cnt["Đỏ"] ? "sev-Đỏ" : nn ? "sev-Cam" : "sev-ok") + '" href="#canh-bao-moi" style="text-decoration:none"><i class="dot"></i>' + nn + " cảnh báo từ dữ liệu mới</a>";
  $("hero-chips").innerHTML = chips;
  var tdShare = M.tdSum / Math.max(1, M.tdSum + M.cash);
  var K = [
    ["Nhận bàn giao từ chủ đầu tư", ty(D.fund_in), "tỷ", "15/08/2024, hai lệnh chuyển", "", 0, "#giao-dich", "Xem hai lệnh chuyển", "Nhận bàn giao KPBT từ chủ đầu tư"],
    ["Lãi đã nhận", ty(M.interest), "tỷ", "Tiền gửi có kỳ hạn và không kỳ hạn", "", M.interest - B.interest, "#lai-suat", "Xem lãi suất từng khoản gửi", ""],
    ["Đã chi khỏi quỹ", ty(M.spend), "tỷ", M.hasNew ? "Bốn nhóm chi tới 31/05/2026 và các khoản chi mới" : "Bốn nhóm khoản chi, 04/2025 – 04/2026", "hot", M.spend - B.spend, "#vi-sao", "Xem tiền đi đâu", ""],
    ["Quỹ còn ngày " + M.asofFund, ty(M.fund_end), "tỷ", Math.round(tdShare * 100) + "% là tiền gửi có kỳ hạn, cần xác nhận", "", M.fund_end - B.fund_end, "#tien-o-dau", "Xem tiền đang nằm ở đâu", ""],
    ["Thu khu vực chung ngoài quỹ", ty(M.ca_total), "tỷ", "Đã chi " + ty(M.repair7784) + " tỷ cho sửa chữa, mua sắm", "warm", M.ca_total - B.ca_total, "#khu-vuc-chung", "Xem thu, chi khu vực chung", ""],
    ["Lãi bỏ lỡ ước tính", ty(D.opp_lo) + "–" + ty(D.opp_hi), "tỷ", "Kỳ hạn ngắn và số dư nhàn rỗi, tới 31/05/2026", "warm", 0, "#lai-bo-lo", "Xem cách tính", ""]];
  var GO = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg>';
  $("kpis").innerHTML = K.map(function(k){ return '<a class="kpi ' + k[4] + '" href="' + k[6] + '"' + (k[8] ? ' data-cat="' + esc(k[8]) + '"' : "") + ' aria-label="' + esc(k[0] + ": " + k[1] + " " + k[2] + ". " + k[7]) + '"><div class="k">' + esc(k[0]) + '</div><div class="v">' + k[1] + "<small>" + k[2] + '</small></div><div class="s">' + esc(k[3]) + "</div>" + delta(k[5]) + '<div class="go">' + esc(k[7]) + GO + "</div></a>"; }).join("");
  var nb = U.batches.filter(function(b){ return !b.rm; }).length;
  $("file-stm").textContent = "8 file scan, 21 trang, 15/08/2024 – 31/05/2026" + (nb ? "; thêm " + nb + " đợt dữ liệu mới tới " + M.asof : "");
  $("file-tx").innerHTML = '<span class="num">' + (198 + M.nw.length) + "</span> dòng" + (M.hasNew ? " (198 dòng gốc, " + M.nw.length + " dòng mới)" : ", chép lại và tính lại số dư");
}
function renderBanner(){
  var b = $("upd-banner");
  if (!M.hasNew){ b.hidden = true; b.innerHTML = ""; return; }
  var g = M.g, nb = U.batches.filter(function(x){ return !x.rm; }).length;
  var unsaved = U.batches.some(function(x){ return !x.rm && !SAVED_BIDS[x.id]; });
  b.innerHTML = '<div class="bx"><b>Đã cập nhật dữ liệu mới tới ' + M.asof + "</b>: " + M.nw.length + " giao dịch từ " + nb + " đợt nạp" + (unsaved ? " (có đợt chưa lưu)" : "") + "; cảnh báo tự động: " + g.cnt["Đỏ"] + " Đỏ, " + g.cnt["Cam"] + " Cam, " + g.cnt["Vàng"] + " Vàng. Con số, biểu đồ và bảng giao dịch đã tính lại; phần nhận định chữ vẫn là của bản phân tích dữ liệu tới 31/05/2026" + (U.ai && U.ai.r ? ", kèm đánh giá bổ sung của Claude ngày " + fmtIso(U.ai.at).slice(0, 10) : "") + '.</div><div class="bt"><a class="tbtn" href="#canh-bao-moi">Cảnh báo mới</a><a class="tbtn" href="#cap-nhat">Chi tiết dữ liệu mới</a></div>';
  b.hidden = false;
}

/* ============================== 01 verdict ============================== */
function codeLinks(codes){ if (!codes) return ""; return String(codes).split(/,\s*/).filter(Boolean).map(function(c){ return '<a class="cd" href="#dau-hieu" data-code="' + esc(c) + '">' + esc(c) + "</a>"; }).join(""); }
function renderVerdict(){
  var V = D.verdict;
  $("vans").innerHTML = '<div><div class="lab">Kết luận chung · câu trả lời ngắn</div><div class="a">' + esc(V.answer) + '</div></div><div class="vst">' + V.stats.map(function(s){ return '<a class="vs" href="#tier-' + s[2] + '"><div class="v ' + s[2] + '">' + esc(s[0]) + '</div><div class="k">' + esc(s[1]) + "</div></a>"; }).join("") + "</div>";
  $("tiers").innerHTML = V.tiers.map(function(t){
    return '<div class="tier ' + t.tone + '" id="tier-' + t.tone + '"><div class="th"><b>' + esc(t.name) + "</b><span>" + esc(t.sub) + "</span></div>" + t.items.map(function(it){
      var m = t.k !== "clean" ? '<div class="m">' + (it.amt ? '<span class="am">' + esc(it.amt) + "</span>" : "") + (it.rule ? '<span class="rl">' + esc(it.rule) + "</span>" : "") + codeLinks(it.code) + "</div>" : "";
      return '<div class="it"><h4>' + esc(it.h) + "</h4><p>" + esc(it.t) + "</p>" + m + "</div>"; }).join("") +
      (t.hq ? '<div class="tsp"></div><div class="thq"><b>Hệ quả</b><span>' + esc(t.hq) + "</span></div>" : "") + "</div>";
  }).join("");
  $("keys").innerHTML = V.keys.map(function(k, i){ return '<div class="key"><b>' + (i + 1) + "</b><div>" + esc(k) + "</div></div>"; }).join("");
  $("nd01").innerHTML = '<div class="lab">Nhận định</div>' + V.nd.map(function(s){ return "<p>" + esc(s) + "</p>"; }).join("");
  $("score").innerHTML = SECK.filter(function(no){ return no !== "01"; }).map(function(no){ var c = D.concl[no]; return '<a href="#' + SEC[no].id + '"><span class="no">' + no + '</span><span class="t">' + esc(SEC[no].t) + '</span><span class="pill tone-' + c[1] + '"><i class="dot"></i>' + esc(c[0]) + '</span><span class="kx">' + esc(D.score_key[no]) + '</span><span class="go" aria-hidden="true">›</span></a>'; }).join("");
}
var TLF = "";
function shortNew(t){
  if (/^(Chi khác|Thu khác)/.test(t.c)) return t.s.length > 110 ? t.s.slice(0, 107) + "…" : t.s;
  return t.c + (t.cp ? " – " + t.cp : "");
}
function newTimelineRows(){
  var rows = M.nw.filter(function(t){ return t.v === "Đỏ" || t.v === "Cam" || t.c === "Gửi tiền có kỳ hạn (HĐTG)" || t.c === "Tất toán HĐTG (gốc + lãi về TK)" || (t.dr + t.cr) >= 100e6; });
  rows = rows.slice(-15);
  return rows.map(function(t){
    var isTd = t.c === "Gửi tiền có kỳ hạn (HĐTG)" || t.c === "Tất toán HĐTG (gốc + lãi về TK)";
    return {d: t.d, t: ACCS[t.a] + ": " + shortNew(t), v: (t.dr ? "−" : "+") + money(t.dr || t.cr), k: t.v === "Đỏ" ? "red" : isTd ? "n" : t.v === "Cam" ? "warn" : t.dr ? "out" : "in", c: "", nw: 1};
  });
}
function renderTimeline(){
  var rows = D.tln.slice();
  if (M.hasNew) rows = rows.concat(newTimelineRows());
  var F = {"": function(){ return true; }, "in": function(r){ return r.k === "in"; }, "out": function(r){ return r.k === "out" || r.k === "red"; }, "att": function(r){ return r.k === "red" || r.k === "warn"; }, "new": function(r){ return !!r.nw; }};
  if (!M.hasNew && TLF === "new") TLF = "";
  $("tl-f").innerHTML = [["", "Tất cả"], ["in", "Tiền vào"], ["out", "Tiền ra"], ["att", "Cần chú ý"]].concat(M.hasNew ? [["new", "Dữ liệu mới"]] : []).map(function(b){ return '<button class="fbtn" type="button" data-f="' + b[0] + '" aria-pressed="' + (TLF === b[0]) + '">' + b[1] + "</button>"; }).join("");
  $("tln").innerHTML = rows.filter(F[TLF] || F[""]).map(function(r){ return '<div class="r tk-' + r.k + '"><div class="d">' + esc(r.d) + '</div><div class="dt"></div><div class="x">' + esc(r.t) + (r.nw ? '<span class="newb">Mới</span>' : "") + codeLinks(r.c) + '</div><div class="v">' + esc(r.v) + "</div></div>"; }).join("");
}

/* ============================== 02 statements ============================== */
function batchStats(b){
  var dr = 0, cr = 0, ks = [];
  b.rows.forEach(function(r){ dr += +r.dr || 0; cr += +r.cr || 0; ks.push(dkey(r.d)); });
  ks.sort();
  var last = b.rows.length ? b.rows[b.rows.length - 1] : null;
  return {dr: dr, cr: cr, from: kdate(ks[0] || ""), to: kdate(ks[ks.length - 1] || ""), closing: last && last.b != null ? +last.b : 0};
}
function checkPill(b){
  var c = b.chk || {};
  if (c.bad) return '<span class="pill sev-Cam"><i class="dot"></i>Lệch số dư ' + c.bad + " dòng</span>";
  if (c.cont === false) return '<span class="pill sev-Cam"><i class="dot"></i>Không nối số dư cũ</span>';
  return '<span class="pill sev-ok"><i class="dot"></i>Khớp số dư</span>';
}
function renderStatements(){
  var rows = D.stm.map(function(s){ return '<tr><td style="white-space:nowrap"><span class="acc">' + s.a + "</span> " + esc(s.bank) + '</td><td data-l="Kỳ">' + esc(s.period) + '</td><td class="n" data-l="Số giao dịch">' + s.n + '</td><td class="n" data-l="Tiền ra">' + vnd(s.debit) + '</td><td class="n" data-l="Tiền vào">' + vnd(s.credit) + '</td><td class="n" data-l="Số dư cuối">' + vnd(s.ending) + '</td><td><span class="pill sev-ok"><i class="dot"></i>Khớp</span></td></tr>'; });
  U.batches.forEach(function(b){
    if (b.rm) return;
    var st = batchStats(b);
    rows.push('<tr><td style="white-space:nowrap"><span class="acc">' + b.acc + "</span> " + BANK[b.acc] + '<span class="newb">Mới</span></td><td data-l="Kỳ">' + st.from + " – " + st.to + '</td><td class="n" data-l="Số giao dịch">' + b.rows.length + '</td><td class="n" data-l="Tiền ra">' + vnd(st.dr) + '</td><td class="n" data-l="Tiền vào">' + vnd(st.cr) + '</td><td class="n" data-l="Số dư cuối">' + vnd(st.closing) + "</td><td>" + checkPill(b) + (SAVED_BIDS[b.id] ? "" : ' <span class="pill sev-Vàng"><i class="dot"></i>Chưa lưu</span>') + "</td></tr>");
  });
  $("stm-body").innerHTML = rows.join("");
  var note = "Tổng số dư cuối của 8 sao kê khớp số in trên sao kê; bảng chuyển đổi đầy đủ ở file Excel tải về.";
  if (M.hasNew){
    note = "Đối chiếu: tiền gửi có kỳ hạn " + ty(M.tdSum) + " tỷ cộng số dư thanh toán " + ty(M.cash) + " tỷ " + (Math.abs(M.recon) <= 1000 ? "khớp với số quỹ tính theo giao dịch." : "lệch " + money(M.recon) + " so với số quỹ tính theo giao dịch; có thể thiếu sao kê một phía của giao dịch chuyển nội bộ, hoặc khoản tất toán chưa khớp hợp đồng nào.");
    if (M.ic.length){
      var ok = M.ic.filter(function(x){ return Math.abs(x.diff) <= 1; }).length;
      note += " Lãi không kỳ hạn tính lại theo 0,2%/năm: " + ok + "/" + M.ic.length + " tháng mới khớp tới từng đồng" + (ok < M.ic.length ? " (" + M.ic.filter(function(x){ return Math.abs(x.diff) > 1; }).map(function(x){ return ACCS[x.a] + " " + x.m + " lệch " + vnd(x.diff) + " đồng, lãi suất suy ra " + pct(x.rate, 2); }).join("; ") + ")" : "") + ".";
    }
  }
  $("stm-note").textContent = note;
  $("dl-h2").textContent = M.hasNew ? (198 + M.nw.length) + " giao dịch: 198 dòng của 8 sao kê gốc và " + M.nw.length + " dòng mới" : "198 giao dịch của 8 sao kê, khớp tuyệt đối với số dư";
}

/* ============================== 04 composition ============================== */
function renderComp(){
  var comp = M.tds.map(function(t){ return {l: t.l, v: t.v, k: "td", st: t.st, nw: t.nw}; }).concat([{l: "Tiền gửi thanh toán", v: M.cash, k: "cash", st: "Có trên sao kê"}]);
  var tot = comp.reduce(function(a, c){ return a + c.v; }, 0);
  $("stack").innerHTML = comp.map(function(c){ var p = c.v / tot; var col = c.k === "td" ? "var(--s1)" : "var(--s3)"; return '<div style="flex:' + c.v + ' 1 0;background:' + col + '" title="' + esc(c.l) + ": " + vnd(c.v) + ' đồng">' + (p > 0.09 ? pct(p, 0) : "") + "</div>"; }).join("");
  $("comp-list").innerHTML = comp.map(function(c){
    var col = c.k === "td" ? "var(--s1)" : "var(--s3)";
    var chip = c.nw ? '<span class="pill sev-Vàng"><i class="dot"></i>Mới, cần xác nhận</span>' : c.st.indexOf("Chưa") === 0 ? '<span class="pill sev-Cam"><i class="dot"></i>Cần xác nhận</span>' : (c.k === "cash" ? '<span class="pill sev-ok"><i class="dot"></i>Có trên sao kê</span>' : '<span class="pill sev-Vàng"><i class="dot"></i>Có dấu vết lãi</span>');
    return '<div class="row"><i class="sw" style="background:' + col + '"></i><div>' + esc(c.l) + '</div><div class="val">' + ty(c.v, 2) + ' tỷ</div><div class="st">' + esc(c.st) + " " + chip + "</div></div>"; }).join("");
  $("comp-h3").textContent = "Cơ cấu quỹ ngày " + M.asofFund;
  $("tod-h2").textContent = ty(M.fund_end) + " tỷ đang nằm ở đâu";
  $("comp-note").textContent = M.hasNew && Math.abs(M.recon) > 1000 ? "Tổng các khoản trên lệch " + money(M.recon) + " so với số quỹ tính theo giao dịch; xem ghi chú ở mục 02." : "";
  var ev = [];
  M.g.tdOpen.forEach(function(t){ ev.push(t.d + ": gửi mới " + money(t.v) + " tại " + BANK[t.a]); });
  M.g.tdClose.forEach(function(t){ ev.push(t.d + ": tất toán " + t.l + ", gốc " + money(t.v) + ", lãi " + money(t.i)); });
  $("td-new").textContent = ev.length ? "Dữ liệu mới: " + ev.join("; ") + "." : "";
}
function renderTdTrace(){
  var host = $("td-trace"); host.innerHTML = "";
  var rows = [["Agribank 60 tỷ (gửi lần 1)", "2024-08-21", "2025-08-21", "Tất toán kèm lãi 2,82 tỷ"], ["Agribank 60 tỷ (gửi lại)", "2025-08-22", "2025-08-22", "Không có dấu vết sau ngày gửi"], ["VietinBank 45 tỷ", "2024-08-20", "2025-08-20", "Trả lãi 2,115 tỷ ngày 20/08/2025"], ["VietinBank 15 tỷ", "2024-08-20", "2026-05-20", "Trả lãi mỗi quý tới 20/05/2026"], ["VietinBank 5 tỷ", "2025-08-29", "2025-08-29", "Không có dấu vết sau ngày gửi"]];
  var W = Math.max(300, Math.min(520, Math.round(host.clientWidth || 520))), H = 34 * rows.length + 46, m = {l: 8, r: 12, t: 10, b: 30}, iw = W - m.l - m.r;
  var t0 = Date.parse("2024-08-01"), t1 = Date.parse("2026-06-15"), x = function(d){ return m.l + (Date.parse(d) - t0) / (t1 - t0) * iw; };
  var svg = el("svg", {viewBox: "0 0 " + W + " " + H, role: "img", "aria-label": "Dấu vết các khoản tiền gửi"}, host);
  (W < 420 ? ["2024-09-01", "2025-03-01", "2025-09-01", "2026-03-01"] : ["2024-09-01", "2025-01-01", "2025-05-01", "2025-09-01", "2026-01-01", "2026-05-01"]).forEach(function(d){ var xx = x(d); el("line", {x1: xx, x2: xx, y1: m.t, y2: H - m.b, "class": "grid-l"}, svg); var p = d.split("-"); txt(svg, xx, H - m.b + 16, p[1] + "/" + p[0].slice(2), "ax", "middle"); });
  var asof = x("2026-05-31"); el("line", {x1: asof, x2: asof, y1: m.t, y2: H - m.b, stroke: "var(--ink-2)", "stroke-width": 1}, svg); txt(svg, asof - 4, m.t + 8, "31/05/2026", "ax", "end");
  rows.forEach(function(r, i){
    var yy = m.t + 18 + i * 34; txt(svg, m.l, yy - 8, r[0], "lbl");
    var a = x(r[1]), b = x(r[2]);
    el("line", {x1: a, x2: Math.max(b, a + 1), y1: yy + 4, y2: yy + 4, stroke: "var(--s1)", "stroke-width": 3, "stroke-linecap": "round"}, svg);
    el("circle", {cx: a, cy: yy + 4, r: 4.5, fill: "var(--s1)", stroke: "var(--surface)", "stroke-width": 2}, svg);
    el("circle", {cx: b, cy: yy + 4, r: 5, fill: r[3].indexOf("Không") === 0 ? "var(--s2)" : "var(--s1)", stroke: "var(--surface)", "stroke-width": 2}, svg);
    if (b < asof - 4) el("line", {x1: b + 6, x2: asof, y1: yy + 4, y2: yy + 4, stroke: "var(--line-2)", "stroke-width": 1.5, "stroke-dasharray": "3 3"}, svg);
    var hit = el("rect", {x: m.l, y: yy - 18, width: iw, height: 30, fill: "transparent"}, svg); bindTip(hit, "<b>" + esc(r[0]) + "</b><br>" + esc(r[3]));
  });
}

/* ============================== 05 waterfall, causes ============================== */
function wfData(){
  var w = D.wf.slice(0, -1);
  if (M.hasNew){
    var up = M.g.int + M.g.oth, dn = M.g.spend + M.g.fees;
    if (up) w.push({l: "Lãi, thu khác sau " + BASE_ASOF.slice(0, 5), v: up, t: "up"});
    if (dn) w.push({l: "Chi sau " + BASE_ASOF.slice(0, 5), v: -dn, t: "down"});
    w.push({l: "Còn lại " + M.asofFund, v: M.fund_end, t: "total"});
  } else w.push(D.wf[D.wf.length - 1]);
  return w;
}
function renderWaterfall(){
  var host = $("wf"); host.innerHTML = "";
  var data = wfData(), run = 0, lo = Infinity, hi = -Infinity;
  data.forEach(function(s){ if (s.t === "total") run = s.v; else run += s.v; lo = Math.min(lo, run); hi = Math.max(hi, run); });
  var y0 = Math.max(0, Math.floor((lo - 4e9) / 2e9) * 2e9), y1 = Math.ceil((hi + 1e9) / 1e9) * 1e9;
  if ((host.clientWidth || 760) < 600) return renderWaterfallV(host, data, y0, y1);
  var W = 760, H = 330, m = {l: 44, r: 10, t: 26, b: 62}, iw = W - m.l - m.r, ih = H - m.t - m.b;
  var y = function(v){ return m.t + ih - (v - y0) / (y1 - y0) * ih; };
  var svg = el("svg", {viewBox: "0 0 " + W + " " + H, role: "img", "aria-label": "Biểu đồ cầu nối quỹ bảo trì"}, host);
  for (var v = y0; v <= y1 + 1; v += 2e9){ var yy = y(v); el("line", {x1: m.l, x2: W - m.r, y1: yy, y2: yy, "class": v === y0 ? "base-l" : "grid-l"}, svg); txt(svg, m.l - 8, yy + 4, String(Math.round(v / 1e9)), "ax", "end"); }
  var n = data.length, bw = iw / n; run = 0;
  data.forEach(function(s, i){
    var w = Math.min(bw * 0.6, 48), x = m.l + i * bw + (bw - w) / 2, top, bot, col;
    if (s.t === "total"){ top = y(s.v); bot = y(y0); col = "var(--s3)"; run = s.v; }
    else { var a = run, b = run + s.v; top = y(Math.max(a, b)); bot = y(Math.min(a, b)); col = s.v >= 0 ? "var(--s1)" : "var(--s2)"; run = b; }
    el("rect", {x: x, y: top, width: w, height: Math.max(bot - top, 2), rx: 3, fill: col}, svg);
    if (s.t === "total") el("path", {d: "M" + (x - 2) + " " + (bot - 7) + " l6 -5 l6 5 l6 -5 l6 5 l6 -5 l6 5 l6 -5 l6 5", stroke: "var(--surface)", "stroke-width": 3, fill: "none"}, svg);
    if (i < n - 1){ var ny = y(run); el("line", {x1: x + w, x2: x + bw, y1: ny, y2: ny, stroke: "var(--line-2)", "stroke-width": 1}, svg); }
    var lab = s.t === "total" ? ty(s.v, 2) : (s.v > 0 ? "+" : "−") + ty(Math.abs(s.v), Math.abs(s.v) < 0.01e9 ? 3 : 2);
    txt(svg, x + w / 2, top - 7, lab, "val", "middle");
    wrapWords(s.l, 15).forEach(function(ln, j){ txt(svg, m.l + i * bw + bw / 2, H - m.b + 16 + j * 13, ln, "lbl", "middle"); });
    var hit = el("rect", {x: m.l + i * bw, y: m.t, width: bw, height: ih, fill: "transparent"}, svg);
    bindTip(hit, "<b>" + esc(s.l) + "</b><br>" + (s.t === "total" ? "" : (s.v > 0 ? "+" : "−")) + vnd(Math.abs(s.v)) + " đồng");
  });
}
function renderWaterfallV(host, data, y0, y1){
  var W = Math.max(300, Math.round(host.clientWidth || 360)), rowH = 46, labW = Math.min(150, Math.round(W * 0.4)), m = {t: 24, r: 10, b: 8}, H = m.t + m.b + rowH * data.length, iw = W - labW - m.r;
  var x = function(v){ return labW + (v - y0) / (y1 - y0) * iw; };
  var svg = el("svg", {viewBox: "0 0 " + W + " " + H, role: "img", "aria-label": "Biểu đồ cầu nối quỹ bảo trì"}, host);
  var step = (y1 - y0) / 1e9 > 8 ? 4e9 : 2e9;
  for (var v = y0; v <= y1 + 1; v += step){ var xx = x(v); el("line", {x1: xx, x2: xx, y1: m.t - 6, y2: H - m.b, "class": v === y0 ? "base-l" : "grid-l"}, svg); txt(svg, xx, m.t - 10, String(Math.round(v / 1e9)), "ax", "middle"); }
  var run = 0;
  data.forEach(function(s, i){
    var yy = m.t + i * rowH, bh = 16, by = yy + 22, a, b, col;
    if (s.t === "total"){ a = y0; b = s.v; col = "var(--s3)"; run = s.v; } else { a = run; b = run + s.v; col = s.v >= 0 ? "var(--s1)" : "var(--s2)"; run = b; }
    var lo = Math.min(a, b), hi = Math.max(a, b), x0 = x(lo), x1 = Math.max(x(hi), x0 + 2);
    wrapWords(s.l, Math.max(12, Math.floor(labW / 6.4))).slice(0, 2).forEach(function(ln, j){ txt(svg, 0, yy + 18 + j * 13, ln, "lbl"); });
    el("rect", {x: x0, y: by - 8, width: x1 - x0, height: bh, rx: 3, fill: col}, svg);
    var lab = s.t === "total" ? ty(s.v, 2) : (s.v > 0 ? "+" : "−") + ty(Math.abs(s.v), Math.abs(s.v) < 0.01e9 ? 3 : 2);
    var right = x1 + 5 + lab.length * 7 < W;
    txt(svg, right ? x1 + 5 : x0 - 5, by + 4, lab, "val", right ? "start" : "end");
    var hit = el("rect", {x: 0, y: yy, width: W, height: rowH, fill: "transparent"}, svg);
    bindTip(hit, "<b>" + esc(s.l) + "</b><br>" + (s.t === "total" ? "" : (s.v > 0 ? "+" : "−")) + vnd(Math.abs(s.v)) + " đồng");
  });
}
var CAUSE = [
 {k: "Chi thang máy – Schindler", sev: "Cam", code: "F06", who: "Schindler Việt Nam · 7 lệnh 04–06/2025", why: "Phí bảo trì 10/2024–01/2025 trả trễ 5–6 tháng; 14 hợp đồng sửa chữa; tạm ứng 50% ba hợp đồng.", rule: "Cần nghiệm thu trước thanh toán; sửa chữa đột xuất tối đa 500 triệu/năm (Điều 6.3.b, 9.2)."},
 {k: "Chuyển KPBT sang TK vận hành của BQT", sev: "Đỏ", code: "F01", who: "TK 118002976372 của Ban quản trị · 23/12/2025", why: "Hoàn ứng gộp 6 khoản chi từ 29/08 tới 23/12/2025 cho thang máy, phòng cháy, máy phát.", rule: "Quỹ chỉ được chuyển tới tài khoản đơn vị bảo trì; tạm dùng tiền vận hành tối đa 10 triệu/tháng (Điều 7.2, 7.4)."},
 {k: "Chi sửa chữa cấp nước – HNB", sev: "Cam", code: "F05", who: "Nhà thầu cấp nước · 14/04/2026", why: "Tạm ứng 50% hợp đồng khoảng 1,25 tỷ; phần còn lại 623 triệu sẽ tiếp tục chi từ quỹ.", rule: "Cần kế hoạch bảo trì được thông qua, đấu thầu công khai, 3 báo giá (Điều 6.3)."},
 {k: "Chi mua thiết bị – Thép Quang", sev: "Đỏ", code: "F03", who: "Nhà cung cấp thiết bị · 24/04/2026", why: "Trả trọn sau 16 ngày ký, nội dung mua thiết bị khu vực chung không nêu chủng loại.", rule: "Chỉ thuê đơn vị đủ năng lực, 3 báo giá, nghiệm thu rồi mới thanh toán (Điều 6.1.c, 6.3)."}];
function renderCauses(){
  $("causes").innerHTML = CAUSE.map(function(c){ var tot = 0; D.timeline.forEach(function(t){ if (t.g === c.k) tot += t.v; });
    return '<div class="cause sev-' + c.sev + '"><div class="top-row"><span class="pill"><i class="dot"></i>Mức ' + c.sev + '</span><a class="cd" href="#dau-hieu" data-code="' + c.code + '">' + c.code + '</a></div><div class="amt">' + tr(tot, 1) + ' triệu</div><div class="who">' + esc(c.who) + '</div><div class="why">' + esc(c.why) + '</div><div class="rule">' + esc(c.rule) + "</div></div>"; }).join("");
}

/* ============================== bars ============================== */
function hbars(host, items, opts){
  opts = opts || {}; host.innerHTML = "";
  var cw = host.clientWidth || 560, W = Math.max(300, Math.min(560, Math.round(cw))), narrow = W < 520;
  var rowH = narrow ? Math.max(opts.rowH || 34, 40) : (opts.rowH || 34), labW = narrow ? Math.round(W * 0.42) : (opts.labW || 210), m = {t: 6, r: narrow ? 64 : 78, b: 6}, H = m.t + m.b + rowH * items.length;
  if (narrow) opts = Object.assign({}, opts, {wrap: Math.max(14, Math.floor(labW / 6.4))});
  var max = opts.max || Math.max.apply(null, items.map(function(i){ return i.v; })); var iw = W - labW - m.r;
  var svg = el("svg", {viewBox: "0 0 " + W + " " + H, role: "img", "aria-label": opts.aria || "Biểu đồ thanh"}, host);
  items.forEach(function(it, i){
    var yy = m.t + i * rowH, bh = Math.min(18, rowH - 12), by = yy + (rowH - bh) / 2;
    var lines = wrapWords(it.l, opts.wrap || 30); lines.slice(0, 2).forEach(function(ln, j){ txt(svg, 0, yy + rowH / 2 + 4 + (j - (lines.length > 1 ? 0.5 : 0)) * 13, ln, "lbl"); });
    var w = Math.max(4, (it.v / max) * iw); var col = it.col || opts.col || "var(--s1)";
    el("path", {d: "M" + labW + " " + by + " h" + (w - 4) + " a4 4 0 0 1 4 4 v" + (bh - 8) + " a4 4 0 0 1 -4 4 h-" + (w - 4) + " z", fill: col}, svg);
    txt(svg, labW + w + 6, by + bh / 2 + 4, opts.fmt ? opts.fmt(it.v) : tr(it.v, 1), "val");
    var hit = el("rect", {x: 0, y: yy, width: W, height: rowH, fill: "transparent"}, svg); bindTip(hit, "<b>" + esc(it.l) + "</b><br>" + vnd(it.v) + " đồng" + (it.note ? "<br>" + esc(it.note) : ""));
  });
  el("line", {x1: labW, x2: labW, y1: m.t, y2: H - m.b, "class": "base-l"}, svg);
}

/* ============================== 06 common area ============================== */
function renderKVC(){
  var g = M.g, inc = D.income.slice();
  if (g.ca7784) inc.push({l: "Thu mới sau 31/05/2026", v: g.ca7784, col: "var(--accent)"});
  hbars($("inc"), inc, {fmt: function(v){ return tr(v, 1) + " tr"; }, aria: "Thu khu vực chung theo đơn vị trả"});
  var out = D.out7784.map(function(o){ if (o.l === "Nộp thuế") return {l: "Nộp thuế", v: o.v + g.tax7784, col: "var(--s3)"}; if (o.l === "Phí ngân hàng") return null; return {l: o.l, v: o.v, col: "var(--s2)"}; }).filter(Boolean);
  if (g.out7784) out.push({l: "Chi mới sau 31/05/2026", v: g.out7784, col: "var(--crit)"});
  out.push({l: "Còn lại trên tài khoản", v: Math.max(0, M.end_v), col: "var(--line-2)"});
  hbars($("out7784"), out, {fmt: function(v){ return tr(v, 1) + " tr"; }, aria: "Tiền ra khỏi tài khoản 7784"});
  var k = M.kAcc["7784"];
  $("inc-h3").textContent = "Tiền vào tài khoản 7784, 07/2025 – " + k.slice(4, 6) + "/" + k.slice(0, 4);
  $("out-sub").textContent = "Còn lại " + tr(M.end_v, 1) + " triệu ngày " + kdate(k);
  var parts = [];
  if (g.ca7784) parts.push("thu vào TK 7784 thêm " + money(g.ca7784));
  if (g.out7784) parts.push("chi từ TK 7784 thêm " + money(g.out7784));
  if (g.caFund) parts.push("tiền khu vực chung vào đúng tài khoản quỹ " + money(g.caFund));
  $("kvc-new").textContent = parts.length ? "Dữ liệu mới: " + parts.join("; ") + ". Tổng thu khu vực chung ngoài quỹ nay là " + ty(M.ca_total) + " tỷ." : "";
}
function renderChic(){
  $("chic-tiles").innerHTML = '<div class="tile"><div class="k">Hợp đồng quảng cáo 01/10/2024</div><div class="v num">' + tr(D.chic.m_2024, 2) + ' triệu/tháng</div><div class="s">3 tháng cuối 2024, trả trễ 7 tháng</div></div>' +
    '<div class="tile"><div class="k">Hợp đồng quảng cáo 05/01/2025</div><div class="v num">' + tr(D.chic.m_2025, 2) + ' triệu/tháng</div><div class="s">Từ 01/2025 tới nay</div></div>' +
    '<div class="tile" style="border-color:var(--warn-line);background:var(--warn-soft)"><div class="k">Mức giảm sau khi ký lại</div><div class="v num" style="color:var(--warn)">' + pct(Math.abs(D.chic.drop), 1) + '</div><div class="s">Khoảng ' + tr(D.chic.year_gap, 0) + " triệu mỗi năm, cần giải trình</div></div>";
}

/* ============================== 07 rates ============================== */
function renderIdle(){
  var host = $("idle"); host.innerHTML = "";
  var S = M.series, W = Math.max(300, Math.min(560, Math.round(host.clientWidth || 560))), H = W < 480 ? 240 : 270, m = {l: 30, r: 10, t: 14, b: 30}, iw = W - m.l - m.r, ih = H - m.t - m.b;
  var t0 = Date.parse(S[0][0]), t1 = Date.parse(S[S.length - 1][0]), x = function(d){ return m.l + (Date.parse(d) - t0) / (t1 - t0) * iw; };
  var mx = Math.max.apply(null, S.map(function(p){ return p[1]; })), ymax = Math.max(10e9, Math.ceil(mx / 2e9) * 2e9), y = function(v){ return m.t + ih - v / ymax * ih; };
  var svg = el("svg", {viewBox: "0 0 " + W + " " + H, role: "img", "aria-label": "Số dư tài khoản thanh toán quỹ bảo trì theo ngày"}, host);
  for (var v = 0; v <= ymax / 1e9 + 0.01; v += 2){ var yy = y(v * 1e9); el("line", {x1: m.l, x2: W - m.r, y1: yy, y2: yy, "class": v === 0 ? "base-l" : "grid-l"}, svg); txt(svg, m.l - 6, yy + 4, String(v), "ax", "end"); }
  var dt = new Date(t0); dt = new Date(Date.UTC(dt.getUTCFullYear(), dt.getUTCMonth() + 1, 1));
  var tstep = W < 420 ? 6 : 4;
  while (dt.getTime() <= t1){ var mo = dt.getUTCMonth(); if (mo % tstep === 0){ var iso = dt.toISOString().slice(0, 10); txt(svg, x(iso), H - m.b + 17, iso.slice(5, 7) + "/" + iso.slice(2, 4), "ax", "middle"); } dt = new Date(Date.UTC(dt.getUTCFullYear(), mo + 1, 1)); }
  var dA = "M" + x(S[0][0]) + " " + y(0), dL = "";
  S.forEach(function(p, i){ var xx = x(p[0]), yy = y(p[1]); dA += " L" + xx + " " + yy; dL += (i ? " L" : "M") + xx + " " + yy; });
  dA += " L" + x(S[S.length - 1][0]) + " " + y(0) + " Z";
  el("path", {d: dA, fill: "var(--s1-wash)"}, svg); el("path", {d: dL, fill: "none", stroke: "var(--s1)", "stroke-width": 2, "stroke-linejoin": "round"}, svg);
  if (M.hasNew){ var bx = x("2026-05-31"); if (bx < W - m.r - 4){ el("line", {x1: bx, x2: bx, y1: m.t, y2: H - m.b, stroke: "var(--accent)", "stroke-width": 1, "stroke-dasharray": "3 3"}, svg); txt(svg, bx + 4, m.t + 10, "Dữ liệu mới", "ax"); } }
  var by = y(1e9); el("line", {x1: m.l, x2: W - m.r, y1: by, y2: by, stroke: "var(--s2)", "stroke-width": 1.5, "stroke-dasharray": "5 4"}, svg); txt(svg, W - m.r, by - 5, "Mức cần giữ 1 tỷ", "ax", "end");
  var last = S[S.length - 1]; el("circle", {cx: x(last[0]), cy: y(last[1]), r: 4.5, fill: "var(--s1)", stroke: "var(--surface)", "stroke-width": 2}, svg);
  var peak = S.reduce(function(a, b){ return b[1] > a[1] ? b : a; }); var pp = peak[0].split("-");
  txt(svg, Math.min(x(peak[0]) + 6, W - 150), y(peak[1]) + 4, ty(peak[1], 2) + " tỷ ngày " + pp[2] + "/" + pp[1] + "/" + pp[0].slice(2), "ax");
  var cross = el("line", {x1: 0, x2: 0, y1: m.t, y2: H - m.b, stroke: "var(--ink-2)", "stroke-width": 1, opacity: 0}, svg), cdot = el("circle", {cx: 0, cy: 0, r: 4, fill: "var(--s1)", stroke: "var(--surface)", "stroke-width": 2, opacity: 0}, svg);
  var hit = el("rect", {x: m.l, y: m.t, width: iw, height: ih, fill: "transparent"}, svg);
  function mv(e){ var r = svg.getBoundingClientRect(); var px = (e.clientX - r.left) / r.width * W; var t = t0 + (px - m.l) / iw * (t1 - t0); var best = S[0], bd = 1e18; for (var i = 0; i < S.length; i++){ var dd = Math.abs(Date.parse(S[i][0]) - t); if (dd < bd){ bd = dd; best = S[i]; } }
    var xx = x(best[0]), yy = y(best[1]); cross.setAttribute("x1", xx); cross.setAttribute("x2", xx); cross.setAttribute("opacity", 1); cdot.setAttribute("cx", xx); cdot.setAttribute("cy", yy); cdot.setAttribute("opacity", 1); var p = best[0].split("-"); showTip(e, "<b>" + p[2] + "/" + p[1] + "/" + p[0] + "</b><br>" + vnd(best[1]) + " đồng"); }
  hit.addEventListener("mousemove", mv); hit.addEventListener("click", mv);
  hit.addEventListener("mouseleave", function(){ cross.setAttribute("opacity", 0); cdot.setAttribute("opacity", 0); hideTip(); });
}
function tile(k, v, s, st){ return '<div class="tile"' + (st ? ' style="' + st + '"' : "") + '><div class="k">' + esc(k) + '</div><div class="v num">' + esc(v) + '</div><div class="s">' + esc(s) + "</div></div>"; }
function renderRateStatic(){
  $("rate-tiles").innerHTML = tile("15 tỷ gửi 3 tháng thay vì 12 tháng", tr(D.gap15, 0) + " triệu", "Lãi bỏ lỡ 20/08/2024 – 20/05/2026") + tile("Số dư thanh toán vượt 1 tỷ", tr(D.idle12, 0) + " triệu", "Bình quân giữ " + ty(D.avg_q, 2) + " tỷ ở mức lãi 0,2%") + tile("Nếu thương lượng thêm 0,5 điểm %", "625 triệu/năm", "Trên 125 tỷ tiền gửi có kỳ hạn");
  $("rt-body").innerHTML = D.rates_time.map(function(r){ var ok = r.note.indexOf("Đúng biểu") === 0; var pill = r.got == null ? '<span class="pill stc-na"><i class="dot"></i>' + esc(r.note) + "</span>" : '<span class="pill ' + (ok ? "stc-ok" : "stc-part") + '"><i class="dot"></i>' + esc(r.note) + "</span>";
    return '<tr><td class="dieu" style="white-space:nowrap">' + esc(r.when) + '</td><td data-l="Khoản gửi">' + esc(r.item) + '</td><td class="n got" data-l="BQT nhận">' + (r.got == null ? "chưa rõ" : pct(r.got, 1)) + '</td><td data-l="Biểu niêm yết cá nhân">' + esc(r.posted) + '</td><td data-l="Biểu doanh nghiệp">' + esc(r.corp) + '</td><td data-l="Thị trường cùng lúc">' + esc(r.market) + '</td><td data-l="Nhận xét">' + pill + "</td></tr>"; }).join("");
  $("k4").innerHTML = D.k4.map(function(s, i){ return "<div><b>" + (i + 1) + "</b><div>" + esc(s) + "</div></div>"; }).join("");
  $("c-q").innerHTML = D.roll.map(function(r){ return '<button class="fbtn" type="button" data-r="' + (r.r * 100).toFixed(2) + '">' + esc(pct(r.r, 1)) + " · " + esc(r.label) + "</button>"; }).join("");
  calcUpd();
}
function numIn(v){ return parseFloat(String(v).replace(",", ".")); }
function calcUpd(){
  var amt = numIn($("c-amt").value) * 1e9, r = numIn($("c-rate").value) / 100;
  if (!(amt > 0) || !(r >= 0) || r > 0.3){ $("c-out").innerHTML = tile("Nhập số tiền và lãi suất hợp lệ", "–", ""); return; }
  var yv = amt * r, d = yv - amt * 0.047;
  $("c-out").innerHTML = tile("Tiền lãi 12 tháng", money(yv), "ở mức " + pct(r, 2) + "/năm") +
    tile("So với gửi lại 4,7%", signed(d), d >= 0 ? "quỹ có thêm mỗi năm" : "quỹ mất đi mỗi năm", d > 0 ? "border-color:var(--ok-line);background:var(--ok-soft)" : d < 0 ? "border-color:var(--crit-line);background:var(--crit-soft)" : "") +
    tile("Mỗi 0,1 điểm % lãi suất", money(amt * 0.001), "mỗi năm trên " + ty(amt, 0) + " tỷ") + tile("Lãi bình quân mỗi tháng", money(yv / 12), "đủ trả nhiều khoản chi thường xuyên");
  qa("#c-q .fbtn").forEach(function(b){ b.setAttribute("aria-pressed", Math.abs(parseFloat(b.getAttribute("data-r")) - r * 100) < 0.001 ? "true" : "false"); });
}

/* ============================== 08 safety ============================== */
function renderSafety(){ hbars($("safety"), D.safety.map(function(s){ return {l: s.l, v: s.v, col: s.g === "safe" ? "var(--s1)" : "var(--s2)"}; }), {labW: 250, wrap: 34, rowH: 38, fmt: function(v){ return tr(v, 1); }, aria: "Hạng mục đã chi"}); }

/* ============================== 09 matrix ============================== */
var MXMAP = {"Tuân thủ": "ok", "Một phần": "part", "Chưa đủ hồ sơ": "na", "Nghi vấn": "q", "Không tuân thủ": "no"}, MXORDER = ["Không tuân thủ", "Nghi vấn", "Chưa đủ hồ sơ", "Một phần", "Tuân thủ"];
var MXF = "Không tuân thủ";
function renderMatrix(){
  var cnt = {}; D.matrix.forEach(function(m){ cnt[m.st] = (cnt[m.st] || 0) + 1; });
  var cols = {"Không tuân thủ": "var(--crit)", "Nghi vấn": "var(--warn)", "Chưa đủ hồ sơ": "var(--na)", "Một phần": "var(--cau)", "Tuân thủ": "var(--ok)"};
  var desc = {"Không tuân thủ": "có bằng chứng trực tiếp trên sao kê", "Nghi vấn": "sao kê cho thấy dấu hiệu, cần hồ sơ khẳng định", "Chưa đủ hồ sơ": "sao kê không đủ để kết luận", "Một phần": "tuân thủ chưa trọn vẹn", "Tuân thủ": "sao kê cho thấy làm đúng"};
  $("dn-lg").innerHTML = MXORDER.map(function(k){ return '<div><i style="background:' + cols[k] + '"></i><b>' + (cnt[k] || 0) + "</b><span><b>" + k + "</b> · " + desc[k] + "</span></div>"; }).join("");
  $("mx-sum").innerHTML = '<button class="fbtn" type="button" data-s="" aria-pressed="' + (MXF === "") + '">Tất cả (' + D.matrix.length + ")</button>" + MXORDER.map(function(k){ return '<button class="fbtn stc-' + MXMAP[k] + '" type="button" data-s="' + k + '" aria-pressed="' + (MXF === k) + '"><i class="dot" style="background:var(--c)"></i>' + k + " (" + (cnt[k] || 0) + ")</button>"; }).join("");
  $("mx-body").innerHTML = D.matrix.filter(function(m){ return !MXF || m.st === MXF; }).map(function(m){ return '<tr><td class="dieu">' + esc(m.dieu) + '</td><td class="mx-req" data-l="Quy chế yêu cầu">' + esc(m.req) + '</td><td class="mx-fact" data-l="Sao kê cho thấy">' + esc(m.fact) + '</td><td data-l="Đánh giá"><span class="pill stc-' + MXMAP[m.st] + '"><i class="dot"></i>' + esc(m.st) + '</span></td><td class="codes" data-l="Mã dấu hiệu">' + (m.codes ? codeLinks(m.codes) : "—") + "</td></tr>"; }).join("");
}

/* ============================== 10 checks ============================== */
var CHK_ALL = false;
function renderChecks(){
  var rank = {"Phát hiện": 0, "Cần hồ sơ": 1, "Lưu ý": 2, "Đạt": 3};
  var list = D.extra.slice().sort(function(a, b){ return (rank[a.st] == null ? 9 : rank[a.st]) - (rank[b.st] == null ? 9 : rank[b.st]); });
  var show = CHK_ALL ? list : list.slice(0, 4);
  $("checks").innerHTML = show.map(function(c){ var cls = c.st === "Đạt" ? "stc-ok" : c.st === "Phát hiện" ? "stc-q" : c.st === "Lưu ý" ? "stc-part" : "stc-na";
    return '<article class="chk"><div class="hd"><h4>' + esc(c.t) + '</h4><span class="pill ' + cls + '"><i class="dot"></i>' + esc(c.st) + '</span></div><div class="ln"><b>Cách làm</b>' + esc(c.m) + '</div><div class="ln"><b>Kết quả</b>' + esc(c.r) + '</div><div class="imp">' + esc(c.i) + "</div></article>"; }).join("");
  $("chk-more").textContent = CHK_ALL ? "Thu gọn" : "Xem thêm " + (list.length - 4) + " phép kiểm tra";
}

/* ============================== 11 findings ============================== */
var FSEV = "Đỏ", FALL = false, FNN = "";
function renderFinds(){
  var list = D.findings.filter(function(f){ return (FALL || !FSEV || f.sev === FSEV) && (!FNN || f.nn === FNN); });
  $("finds").innerHTML = list.map(function(f){
    var lg = f.lst ? '<div class="fhq ls-' + f.lst + '"><div><b>' + esc(f.lhqlab || "Hệ quả") + "</b>" + esc(f.lhq) + "</div><div><b>" + esc(f.liflab) + "</b>" + esc(f.lif) + "</div></div>" : "";
    return '<article class="find sev-' + f.sev + '" id="find-' + f.id + '"><div class="hd"><span class="code">' + f.id + '</span><span class="pill"><i class="dot"></i>Mức ' + f.sev + "</span>" + (f.lst ? '<span class="lst ls-' + f.lst + '">' + esc(D.lg.st[f.lst]) + "</span>" : "") + (f.nn ? '<span class="nnp nn-' + f.nn + '">' + esc(D.nnl[f.nn]) + "</span>" : "") + (f.amount ? '<span class="amt">Liên quan <b>' + money(f.amount) + "</b></span>" : "") + "</div><h4>" + esc(f.title) + '</h4><p class="view">' + esc(f.view) + "</p>" + lg + (f.nn ? '<div class="fnn nn-' + f.nn + '"><b>Nguyên nhân sơ bộ · ' + esc(D.nnl[f.nn]) + "</b>" + esc(f.nnw) + '<span class="nnc"><i>Đổi nhóm khi:</i> ' + esc(f.nnc) + "</span></div>" : "") + '<details><summary>Bằng chứng, quy định, hồ sơ cần đòi</summary><div class="dl"><div><b>Bằng chứng trên sao kê</b>' + esc(f.evidence) + "</div><div><b>Quy định đối chiếu</b>" + esc(f.rule) + "</div><div><b>Hồ sơ cần Ban quản trị cung cấp</b>" + esc(f.ask) + "</div></div></details></article>"; }).join("");
  var cur = FALL ? "" : FSEV;
  $("fchips").innerHTML = '<span class="fnnl">Theo mức độ</span>' + [["", "Tất cả", D.findings.length], ["Đỏ", "Đỏ", sevCount["Đỏ"]], ["Cam", "Cam", sevCount["Cam"]], ["Vàng", "Vàng", sevCount["Vàng"]]].map(function(b){ return '<button class="fbtn ' + (b[0] ? "sev-" + b[0] : "") + '" type="button" data-s="' + b[0] + '" aria-pressed="' + (cur === b[0]) + '">' + (b[0] ? '<i class="dot" style="background:var(--c)"></i>' : "") + b[1] + '<span class="fcnt">' + b[2] + "</span></button>"; }).join("");
  var nnc = {}; D.findings.forEach(function(f){ nnc[f.nn] = (nnc[f.nn] || 0) + 1; });
  $("fnnchips").innerHTML = '<span class="fnnl">Theo nguyên nhân</span>' + ["", "k1", "k2", "k3", "k0"].map(function(k){ return '<button class="fbtn ' + (k ? "nn-" + k : "") + '" type="button" data-n="' + k + '" aria-pressed="' + (FNN === k) + '">' + (k ? '<i class="dot" style="background:var(--c)"></i>' + esc(D.nnl[k]) + '<span class="fcnt">' + (nnc[k] || 0) + "</span>" : 'Tất cả<span class="fcnt">' + D.findings.length + "</span>") + "</button>"; }).join("");
  var fm = $("find-more");
  fm.hidden = !!(FALL || !FSEV);
  fm.textContent = "Hiện cả " + D.findings.length + " dấu hiệu";
}
function renderNewFlags(){
  var box = $("canh-bao-moi");
  var rows = M.nw.filter(function(t){ return WARN[t.v]; });
  if (!M.hasNew){ box.hidden = true; box.innerHTML = ""; return; }
  var ord = {"Đỏ": 0, "Cam": 1, "Vàng": 2};
  rows.sort(function(a, b){ return ord[a.v] - ord[b.v] || (a.k < b.k ? -1 : 1); });
  box.innerHTML = "<h3>Cảnh báo tự động từ dữ liệu mới tới " + M.asof + '</h3><div class="sub">' + (rows.length ? rows.length + " giao dịch cần chú ý theo cùng bộ quy tắc của phân tích gốc; đây là cảnh báo tự động, cần đọc cùng chứng từ." : "Không có giao dịch nào cần cảnh báo trong " + M.nw.length + " giao dịch mới.") + "</div>" +
    (rows.length ? '<div class="tbl-wrap cards" style="margin-top:10px;max-height:420px"><table><thead><tr><th>Mức, TK</th><th>Ngày</th><th>Nội dung</th><th class="n">Số tiền</th><th>Lý do</th></tr></thead><tbody>' + rows.map(function(t){ return '<tr class="f-' + t.v + '"><td><span class="pill sev-' + t.v + '"><i class="dot"></i>' + t.v + '</span> <span class="acc">' + t.a + '</span></td><td class="num" style="white-space:nowrap" data-l="Ngày">' + t.d + '</td><td class="desc">' + esc(t.s) + (t.cp ? '<div class="note" style="margin-top:2px">' + esc(t.cp) + "</div>" : "") + '</td><td class="n" data-l="Số tiền">' + (t.dr ? "−" : "+") + vnd(t.dr || t.cr) + '</td><td style="min-width:220px" data-l="Lý do">' + esc(t.n) + "</td></tr>"; }).join("") + "</tbody></table></div>" : "");
  box.hidden = false;
}

/* ============================== 03 tests ============================== */
function renderTests(){
  var src = "Mở Hợp Đồng Tiền Gửi Có Kỳ Hạn 12 Tháng", printed = "Mở HợP ĐồNG TIềN GửI Có Kỳ HạN 12 THáNG", out = "", res = "";
  for (var i = 0; i < src.length; i++){ var c = src[i]; if (c >= "a" && c <= "z"){ out += '<span class="u">' + c.toUpperCase() + "</span>"; res += c.toUpperCase(); } else if (/[à-ỹđ]/.test(c) && c !== c.toUpperCase()){ out += '<span class="kept">' + c + "</span>"; res += c; } else { out += esc(c); res += c; } }
  $("caps").innerHTML = '<div class="ln"><span class="lb">Câu gốc trong hệ thống</span><span class="tx">' + esc(src) + '</span></div><div class="ln"><span class="lb">Viết hoa chỉ chữ không dấu</span><span class="tx">' + out + '</span></div><div class="ln"><span class="lb">Dòng in trên sổ phụ</span><span class="tx">' + esc(printed) + "</span></div>" +
    '<p class="note" style="margin-top:4px">' + (res === printed ? "Khớp từng ký tự. " : "") + "Chữ gạch chân được viết hoa, chữ tô vàng là nguyên âm có dấu giữ nguyên chữ thường. Lỗi có quy luật cố định như vậy đến từ hàm viết hoa của phần mềm ngân hàng cũ; công cụ AI vẽ chữ thường sai ngẫu nhiên, không theo một quy tắc mã hóa.</p>";
  $("tests").innerHTML = D.tests.map(function(t){ var ok = t.verdict.indexOf("Đạt") === 0; return '<div class="test"><span class="ic" style="background:' + (ok ? "var(--ok)" : "var(--cau)") + '">' + (ok ? '<svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><path d="M3 7.3l2.6 2.6L11 4.4" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>' : '<svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><path d="M7 3.2v4.6M7 10.4v.2" stroke="#fff" stroke-width="2.2" stroke-linecap="round"/></svg>') + "</span><div><h4>" + esc(t.test) + ' <span class="pill ' + (ok ? "sev-ok" : "sev-Vàng") + '" style="margin-left:4px">' + (ok ? "Đạt" : "Lưu ý") + "</span></h4><p>" + esc(t.result) + "</p></div></div>"; }).join("");
}

/* ============================== 12 tracker, road ============================== */
var TST = [["chua", "Chưa yêu cầu"], ["gui", "Đã gửi yêu cầu"], ["thieu", "Nhận chưa đủ"], ["nhan", "Đã nhận đủ"], ["tuchoi", "Bị từ chối, quá hạn"]];
function tstLabel(k){ for (var i = 0; i < TST.length; i++) if (TST[i][0] === k) return TST[i][1]; return TST[0][1]; }
function renderTrkBar(){
  var cnt = {}; TST.forEach(function(s){ cnt[s[0]] = 0; });
  D.requests.forEach(function(r, i){ var st = (U.tracker["rq" + i] || {}).s || "chua"; if (cnt[st] == null) st = "chua"; cnt[st]++; });
  $("trk-bar").innerHTML = '<div class="trk-prog" role="img" aria-label="Tình trạng ' + D.requests.length + ' hồ sơ">' + TST.map(function(s){ return cnt[s[0]] ? '<i class="s-' + s[0] + '" style="flex:' + cnt[s[0]] + '"></i>' : ""; }).join("") + '</div><div class="trk-lg">' + TST.map(function(s){ return '<span class="s-' + s[0] + '"><i class="dot"></i>' + s[1] + ": <b>" + cnt[s[0]] + "</b></span>"; }).join("") + "</div>" + (canWrite() ? "" : '<span class="subx">Chỉ người quản trị trang cập nhật được tình trạng.</span>');
}
function renderReqs(){
  var ed = canWrite();
  renderTrkBar(); if (typeof renderQ10 === "function") renderQ10();
  $("reqs").innerHTML = D.requests.map(function(r, i){
    var id = "rq" + i, t = U.tracker[id] || {}, st = t.s || "chua";
    var right = ed ? '<select data-rq="' + id + '" aria-label="Tình trạng hồ sơ ' + (i + 1) + '">' + TST.map(function(s){ return '<option value="' + s[0] + '"' + (s[0] === st ? " selected" : "") + ">" + s[1] + "</option>"; }).join("") + '</select><input class="nt" data-rqn="' + id + '" type="text" maxlength="200" placeholder="Ghi chú: ngày gửi, số văn bản, trả lời" value="' + esc(t.n || "") + '">' :
      '<span class="pill s-' + st + '"><i class="dot"></i>' + tstLabel(st) + "</span>" + (t.n ? '<div class="ntx">' + esc(t.n) + "</div>" : "");
    return '<div class="req"><span class="pill ' + (r.pri === "Cao" ? "sev-Đỏ" : "sev-Vàng") + '" style="align-self:start;justify-content:center;min-width:28px">' + (i + 1) + '</span><div><div style="font-weight:500;font-size:14px">' + esc(r.doc) + '</div><div class="why">' + esc(r.why) + " · Gửi: " + esc(r.to) + " · Ưu tiên " + esc(r.pri.toLowerCase()) + "</div>" + (t.at ? '<div class="why">Cập nhật ' + fmtIso(t.at) + "</div>" : "") + '</div><div class="st2">' + right + "</div></div>";
  }).join("");
}
/* ============================== neu hach toan dung ============================== */
var HT_ST = null, HT_OPT = [["ok", "Hợp lệ"], ["w", "Chờ hồ sơ"], ["no", "Không hợp lệ"]];
function htPreset(k){ HT_ST = D.ht.presets[k].slice(); }
function htLoad(){
  if (HT_ST) return;
  var s = lsGet("ssr-ht");
  try { s = s ? JSON.parse(s) : null; } catch (e) { s = null; }
  if (s && s.length === D.ht.items.length) HT_ST = s; else htPreset("cudan");
}
function renderHT(){
  var H = D.ht; htLoad();
  $("ht-tiles").innerHTML = tile("Quỹ theo số dư hiện nay", ty(H.fund_now) + " tỷ", "Hai tài khoản quỹ cộng bốn hợp đồng tiền gửi") +
    tile("Quỹ nếu hạch toán đúng", ty(H.fund_right) + " tỷ", "Tổng tiền không đổi, chỉ đưa tiền khu vực chung về đúng sổ của quỹ") +
    tile("Cần chuyển ngay về tài khoản quỹ", tr(H.move, 1) + " triệu", "Số dư TK 7784 ngày 31/05/2026");
  $("ht-pre").innerHTML = [["cudan", "Kịch bản cư dân nêu"], ["all", "Mọi khoản hợp lệ"], ["strict", "Chặt nhất"]].map(function(p){ return '<button type="button" class="tbtn" data-htp="' + p[0] + '">' + p[1] + "</button>"; }).join("");
  renderHTList();
  $("ht-nd").innerHTML = '<div class="nd"><div class="lab">Nhận định</div>' + H.nd.map(function(x){ return "<p>" + esc(x) + "</p>"; }).join("") + "</div>";
}
function renderHTList(){
  var H = D.ht;
  $("ht-list").innerHTML = H.items.map(function(it, i){
    return '<div class="ht-row"><div class="ht-l"><b>' + esc(it.l) + "</b><span>" + esc(it.src) + (it.code ? " · " + it.code : "") + '</span></div><div class="ht-v num">' + vnd(it.v) + '</div><div class="seg" role="group" aria-label="Đánh giá khoản ' + (i + 1) + '">' +
      HT_OPT.map(function(o){ var on = HT_ST[i] === o[0]; return '<button type="button" data-ht="' + i + '" data-v="' + o[0] + '" aria-pressed="' + on + '" class="' + (on ? "on s-" + o[0] : "") + '">' + o[1] + "</button>"; }).join("") + "</div></div>";
  }).join("");
  var ok = 0, w = 0, no = 0;
  H.items.forEach(function(it, i){ if (HT_ST[i] === "ok") ok += it.v; else if (HT_ST[i] === "w") w += it.v; else no += it.v; });
  $("ht-sum").innerHTML = tile("Coi là hợp lệ", ty(ok) + " tỷ", "Tổng các khoản chọn Hợp lệ") + tile("Còn phải làm rõ", ty(w) + " tỷ", "Các khoản Chờ hồ sơ", "") +
    tile("BQT phải hoàn lại quỹ", ty(no) + " tỷ", "Các khoản chọn Không hợp lệ") + tile("Quỹ phải có nếu phần còn lại không chứng minh được", ty(H.fund_right + w + no) + " tỷ", "Quỹ khi hạch toán đúng cộng các khoản chờ hồ sơ và không hợp lệ");
  var t2 = $("ht-sum").children[1]; if (t2) t2.classList.add("hl");
  lsSet("ssr-ht", JSON.stringify(HT_ST));
}
function renderTdNew(){
  var X = D.td_new; if (!X || !$("tdn-tbl")) return;
  var tot = 0, it = 0; X.forEach(function(r){ tot += r.v; it += r.v * r.r; });
  $("tdn-tbl").innerHTML = '<table><thead><tr><th>Hợp đồng</th><th>Ngân hàng</th><th class="n">Số tiền</th><th>Kỳ hạn</th><th class="n">Lãi suất</th><th>Đáo hạn</th></tr></thead><tbody>' +
    X.map(function(r){ return '<tr><td data-l="Hợp đồng" style="font-family:var(--f-mono);font-size:12.5px;font-weight:600">' + esc(r.hd) + '</td><td data-l="Ngân hàng">' + esc(r.bank) + '</td><td class="n" data-l="Số tiền">' + ty(r.v, r.v % 1e9 ? 1 : 0) + ' tỷ</td><td data-l="Kỳ hạn">' + esc(r.ky) + '</td><td class="n" data-l="Lãi suất" style="font-weight:600">' + pct(r.r, 1) + '</td><td data-l="Đáo hạn">' + esc(r.due) + "</td></tr>"; }).join("") + "</tbody></table>";
  $("tdn-note").textContent = "Tổng " + ty(tot, 1) + " tỷ; nếu đúng các mức lãi này, tiền lãi một năm khoảng " + ty(it, 2) + " tỷ. Hai ngân hàng mới xác nhận 120 tỷ tại ngày 20/05/2025; các hợp đồng sau tái tục chưa có giấy xác nhận.";
}
function renderHD(){
  var LB = {over: "hd-over", open: "hd-open", once: "hd-once", ok: ""};
  $("hd-tbl").innerHTML = '<table><thead><tr><th>Mã hợp đồng</th><th>Nhà thầu</th><th>Tạm ứng</th><th class="n">Giá trị suy ra</th><th class="n">Đã trả</th><th>Kết quả</th></tr></thead><tbody>' +
    D.hd.map(function(c){ return '<tr class="' + LB[c.st] + '"><td data-l="Mã hợp đồng" style="font-family:var(--f-mono);font-size:12.5px;font-weight:600">' + esc(c.code) + '</td><td data-l="Nhà thầu">' + esc(c.who) + '</td><td data-l="Tạm ứng">' + esc(c.adv) + '</td><td class="n" data-l="Giá trị suy ra">' + vnd(c.val) + '</td><td class="n" data-l="Đã trả">' + vnd(c.paid) + '</td><td data-l="Kết quả" style="font-weight:600">' + esc(c.res) + "</td></tr>"; }).join("") + "</tbody></table>";
  $("hd-nd").innerHTML = '<div class="nd"><div class="lab">Nhận định</div>' + D.hd_nd.map(function(x){ return "<p>" + esc(x) + "</p>"; }).join("") + "</div>";
}
function renderDocs(){
  var X = D.docs;
  $("docs").innerHTML = X.list.map(function(d){ return '<div class="doc"><div class="dh"><b>' + esc(d.t) + '</b><span class="dd">' + esc(d.d) + '</span></div><div class="dw">' + esc(d.who) + (d.req ? " · Hồ sơ liên quan: " + esc(d.req) : "") + '</div><div class="dc">' + esc(d.c) + '</div><div class="de">' + esc(d.e) + "</div></div>"; }).join("");
  $("docs-chk").innerHTML = '<table><thead><tr><th>Chỉ tiêu</th><th>Tài liệu</th><th class="n">Trên tài liệu</th><th class="n">Theo sao kê</th><th>Kết quả</th></tr></thead><tbody>' +
    X.chk.map(function(c){ var ok = Math.abs(c.doc - c.st) < 1; return '<tr class="' + (ok ? "dk-ok" : "dk-no") + '"><td data-l="Chỉ tiêu" style="font-weight:600">' + esc(c.l) + '</td><td data-l="Tài liệu">' + esc(c.src) + '</td><td class="n" data-l="Trên tài liệu">' + vnd(c.doc) + '</td><td class="n" data-l="Theo sao kê">' + vnd(c.st) + '</td><td data-l="Kết quả" style="font-weight:600">' + (ok ? "Khớp" : "Lệch " + signed(c.doc - c.st)) + (c.n ? '<div class="note" style="margin-top:2px;font-weight:400">' + esc(c.n) + "</div>" : "") + "</td></tr>"; }).join("") + "</tbody></table>";
  $("docs-nd").innerHTML = '<div class="nd"><div class="lab">Nhận định</div>' + X.nd.map(function(x){ return "<p>" + esc(x) + "</p>"; }).join("") + "</div>";
  $("docs-q").innerHTML = X.q.map(function(x){ return "<li>" + esc(x) + "</li>"; }).join("");
}
function renderRoad(){
  $("road").innerHTML = D.road.steps.map(function(s, i){ return '<div class="rs"><div class="n">BƯỚC ' + (i + 1) + '</div><div class="h">' + esc(s[0]) + '</div><div class="t">' + esc(s[1]) + "</div></div>"; }).join("");
  $("road2").innerHTML = D.road.cards.map(function(c){ return '<div class="panel"><h3>' + esc(c[0]) + '</h3><p style="font-size:14px;color:var(--ink-2);margin-top:6px">' + esc(c[1]) + "</p></div>"; }).join("");
}

/* ============================== hoi dap ============================== */
var HDI = {
  check: '<circle cx="12" cy="12" r="9"/><path d="M8 12.5l2.6 2.6L16 9.6"/>',
  doc: '<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5"/><path d="M10 14.5l2 2 4-4"/>',
  bank: '<path d="M3 10l9-6 9 6"/><path d="M5 10v8M9.5 10v8M14.5 10v8M19 10v8M3 20.5h18"/>',
  receipt: '<path d="M6 3h12v18l-3-2-3 2-3-2-3 2z"/><path d="M9 8h6M9 12h6M9 16h3"/>',
  board: '<rect x="3" y="4" width="18" height="11" rx="1.5"/><path d="M8.5 20l2-5M15.5 20l-2-5"/>',
  pct: '<path d="M19 5L5 19"/><circle cx="7" cy="7" r="2.5"/><circle cx="17" cy="17" r="2.5"/>',
  lift: '<rect x="5" y="3" width="14" height="18" rx="1.5"/><path d="M12 3v18"/><path d="M7.5 10l1.5-2 1.5 2M13.5 14l1.5 2 1.5-2"/>',
  scale: '<path d="M12 4v16M7 20h10M5 7h14"/><path d="M5 7l-2.5 6a2.5 2.5 0 0 0 5 0z"/><path d="M19 7l-2.5 6a2.5 2.5 0 0 0 5 0z"/>',
  people: '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><path d="M16 5.2a3 3 0 0 1 0 5.6M21 20c0-2.6-1.6-4.8-4-5.6"/>',
  info: '<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.01"/>',
  star: '<path d="M12 3.5l2.6 5.3 5.9.9-4.3 4.1 1 5.8-5.2-2.7-5.2 2.7 1-5.8-4.3-4.1 5.9-.9z"/>',
  all: '<path d="M4 6h16M4 12h16M4 18h16"/>',
  chat: '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 9.5h8M8 12.5h5"/>'
};
function hdIc(k, sz){ sz = sz || 18; return '<svg width="' + sz + '" height="' + sz + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + (HDI[k] || "") + "</svg>"; }
var FQ = D.faq, FQT = {}, HD = {t: "hot", q: "", terms: [], hlKey: ""};
FQ.topics.forEach(function(t){ FQT[t.id] = t; });
FQ.items.forEach(function(it){ it._s = norm([it.q, it.a, it.d.join(" "), it.k, FQT[it.t].l, it.n.map(function(x){ return x.join(" "); }).join(" "), it.c.join(" ")].join(" ")); });
var HD_VIEWS = {hot: {l: "Nên đọc trước", s: "Những câu trả lời quan trọng nhất, lấy từ các chủ đề", ic: "star"}, all: {l: "Tất cả chủ đề", s: "Xếp theo thứ tự các phần của báo cáo", ic: "all"}};
function hdNumOk(s, k, t){ return !/[0-9]/.test(s.charAt(k - 1)) && !/[0-9]/.test(s.charAt(k + t.length)); }
function hdHas(s, t){ if (!/^[0-9]+$/.test(t)) return s.indexOf(t) >= 0; var p = 0, k; while ((k = s.indexOf(t, p)) >= 0){ if (hdNumOk(s, k, t)) return true; p = k + 1; } return false; }
function hdFold(c){ return c.normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/đ/g, "d").replace(/Đ/g, "D").toUpperCase(); }
function hdHl(s, terms){
  s = String(s == null ? "" : s);
  if (!terms || !terms.length) return esc(s);
  var ch = Array.from(s), fold = "", map = [];
  ch.forEach(function(c, i){ var f = hdFold(c); for (var j = 0; j < f.length; j++){ fold += f.charAt(j); map.push(i); } });
  var mk = ch.map(function(){ return false; });
  terms.forEach(function(t){ if (!t) return; var num = /^[0-9]+$/.test(t), p = 0, k; while ((k = fold.indexOf(t, p)) >= 0){ if (!num || hdNumOk(fold, k, t)){ for (var x = k; x < k + t.length; x++) mk[map[x]] = true; p = k + t.length; } else p = k + 1; } });
  var out = "", on = false;
  ch.forEach(function(c, i){ if (mk[i] && !on){ out += "<mark>"; on = true; } else if (!mk[i] && on){ out += "</mark>"; on = false; } out += esc(c); });
  return out + (on ? "</mark>" : "");
}
function hdItemHtml(it){
  var T = FQT[it.t], h = '<details class="qa" id="hdq-' + it.id + '" data-id="' + it.id + '"><summary><span class="qa-q">' + esc(it.q) + '</span><span class="qa-meta"><span class="pill st-' + it.st + '"><i class="dot"></i>' + esc(FQ.st[it.st]) + '</span><span class="qa-tp">' + hdIc(T.ic, 14) + esc(T.l) + '</span></span><span class="qa-chev">' + CHEV + "</span></summary>";
  h += '<div class="qa-a"><p class="qa-lead">' + esc(it.a) + "</p>" + it.d.map(function(x){ return "<p>" + esc(x) + "</p>"; }).join("");
  if (it.n.length) h += '<div class="qa-nums">' + it.n.map(function(x){ return '<div><b class="num">' + esc(x[0]) + "</b><span>" + esc(x[1]) + "</span></div>"; }).join("") + "</div>";
  if (it.src) h += '<div class="qa-src">Căn cứ: ' + esc(it.src) + "</div>";
  var go = it.go.map(function(g){ return '<a class="qa-lk" href="' + g[0] + '">' + esc(g[1]) + "</a>"; }).join("") + it.c.map(function(c){ return '<a class="cd" href="#dau-hieu" data-code="' + esc(c) + '" title="Xem dấu hiệu ' + esc(c) + '">' + esc(c) + "</a>"; }).join("");
  if (it.dl && D.files[it.dl]) go += '<button type="button" class="tbtn" data-dl="' + it.dl + '">Tải văn bản kiến nghị</button>';
  if (go) h += '<div class="qa-go"><span class="qa-gl">Xem chi tiết</span>' + go + "</div>";
  return h + "</div></details>";
}
function renderFAQ(){
  var F = FQ;
  $("hd-h2").textContent = F.items.length + " câu hỏi thường gặp, chia theo " + F.topics.length + " chủ đề";
  var tops = [{id: "hot", l: HD_VIEWS.hot.l, ic: "star"}, {id: "all", l: "Tất cả", ic: "all"}].concat(F.topics);
  $("hd-tops").innerHTML = tops.map(function(t){ return '<button type="button" class="hd-tb" data-hdt="' + t.id + '" aria-pressed="false">' + hdIc(t.ic, 16) + '<span class="hd-tl">' + esc(t.l) + '</span><span class="hd-tc num"></span></button>'; }).join("");
  $("hd-list").innerHTML = F.topics.map(function(T){
    return '<div class="hd-g" data-t="' + T.id + '"><div class="hd-gh"><span class="hd-gi">' + hdIc(T.ic, 17) + "</span><div><b>" + esc(T.l) + "</b><span>" + esc(T.s) + "</span></div></div>" +
      F.items.filter(function(i){ return i.t === T.id; }).map(hdItemHtml).join("") + "</div>";
  }).join("");
  var stc = {}; F.items.forEach(function(i){ stc[i.st] = (stc[i.st] || 0) + 1; });
  $("hd-leg").innerHTML = "<b>Nhãn tình trạng</b>" + ["vp", "hs", "ct", "ok", "tt"].map(function(k){ return '<span><span class="pill st-' + k + '"><i class="dot"></i>' + esc(F.st[k]) + '</span> <span class="num">' + (stc[k] || 0) + "</span></span>"; }).join("");
  var hq = (location.hash || "").match(/^#hdq-(.+)$/), hit = null;
  if (hq) F.items.forEach(function(i){ if (i.id === decodeURIComponent(hq[1])) hit = i; });
  if (hit) HD.t = hit.t;
  applyFAQ();
  var first = hit ? $("hdq-" + hit.id) : document.querySelector("#hd-list details.qa:not([hidden])");
  if (first) first.open = true;
}
function hdSetTopic(t){ HD.t = t; if (HD.q){ HD.q = ""; HD.terms = []; var i = $("hd-q"); if (i) i.value = ""; } applyFAQ(); }
function hdSearch(v){ HD.q = String(v || "").slice(0, 80); HD.terms = norm(HD.q).split(" ").filter(Boolean).slice(0, 6); applyFAQ(); }
function applyFAQ(){
  var F = FQ, terms = HD.terms, srch = terms.length > 0, view = srch ? "all" : HD.t, cnt = {hot: 0, all: 0}, shown = [], key = terms.join(" ");
  F.topics.forEach(function(t){ cnt[t.id] = 0; });
  F.items.forEach(function(it){ it._m = !srch || terms.every(function(t){ return hdHas(it._s, t); }); if (it._m){ cnt.all++; cnt[it.t]++; if (it.hot) cnt.hot++; } });
  F.items.forEach(function(it){
    var el = $("hdq-" + it.id); if (!el) return;
    var vis = it._m && (view === "all" || (view === "hot" ? !!it.hot : it.t === view));
    el.hidden = !vis; if (vis) shown.push(el);
    if (el._hk !== key && (vis || el._hk)){
      el.querySelector(".qa-q").innerHTML = hdHl(it.q, terms);
      var ps = el.querySelectorAll(".qa-a > p"); ps[0].innerHTML = hdHl(it.a, terms);
      for (var j = 1; j < ps.length; j++) ps[j].innerHTML = hdHl(it.d[j - 1], terms);
      el._hk = key;
    }
  });
  qa("#hd-list .hd-g").forEach(function(g){ g.hidden = !g.querySelector("details.qa:not([hidden])"); });
  var list = $("hd-list"); list.classList.toggle("v-hot", view === "hot"); list.classList.toggle("v-single", view !== "hot" && view !== "all");
  qa("#hd-tops .hd-tb").forEach(function(b){ var id = b.getAttribute("data-hdt"); b.setAttribute("aria-pressed", !srch && id === HD.t ? "true" : "false"); b.querySelector(".hd-tc").textContent = cnt[id]; b.classList.toggle("zero", srch && !cnt[id]); });
  var V = view === "hot" || view === "all" ? HD_VIEWS[view] : FQT[view], ttl = srch ? "Kết quả tìm kiếm" : V.l, sub = srch ? (shown.length ? "Tìm thấy " + shown.length + " câu cho “" + HD.q.trim() + "”" : "Không có câu nào cho “" + HD.q.trim() + "”") : V.s + " · " + shown.length + " câu";
  $("hd-head").innerHTML = '<span class="ic">' + hdIc(srch ? "all" : V.ic, 20) + '</span><div><h3>' + esc(ttl) + "</h3><p>" + esc(sub) + '</p></div><div class="hd-acts"' + (shown.length > 1 ? "" : " hidden") + '><button type="button" data-hdx="open">Mở tất cả</button><button type="button" data-hdx="close">Thu gọn</button></div>';
  var em = $("hd-empty");
  em.hidden = shown.length > 0;
  if (!shown.length) em.innerHTML = "Chưa có câu hỏi đáp nào khớp. Thử từ khóa ngắn hơn, bỏ dấu, hoặc chọn một chủ đề." + (CAP.sample ? '<div><button class="tbtn pri" type="button" data-hdask="1">Hỏi Claude câu này</button></div>' : "");
  if (srch && shown.length && shown.length <= 2) shown.forEach(function(el){ el.open = true; });
  $("hd-clr").hidden = !HD.q;
}
function hdScrollHead(){ var h = $("hd-head"); if (!h) return; var r = h.getBoundingClientRect(); if (r.top < 0 || r.top > window.innerHeight * 0.7) h.scrollIntoView({block: "start"}); }

/* hoi them Claude */
var ASK = {ctl: null, list: []};
function renderAskBox(){ var b = $("hd-ask"); if (b) b.hidden = !CAP.sample && !ASK.list.length; if (b && !CAP.sample) { var f = $("hd-ask-f"); if (f) f.hidden = true; } }
function renderKM(){
  var K = D.km, el = $("km"); if (!K || !el) return;
  var tone = {ok: "ok", vp: "crit", ct: "cau", hs: "warn"};
  el.innerHTML = '<div class="kmw-h"><span class="kmw-lab">' + esc(K.label) + '</span><span class="kmw-sub">' + esc(K.sub) + '</span></div>' +
    '<p class="kmw-head">' + esc(K.head) + '</p>' +
    '<div class="kmw-g">' + K.tiers.map(function(t){
      return '<div class="kmw-t t-' + tone[t.k] + '"><div class="kmw-tg">' + esc(t.tag) + '</div><div class="kmw-v">' + esc(t.v) + '</div><div class="kmw-vl">' + esc(t.vl) + '</div>' +
        '<h3>' + esc(t.t) + '</h3>' + t.d.map(function(x){ return '<p>' + esc(x) + '</p>'; }).join("") + (t.hq ? '<div class="kmw-hq"><b>Hệ quả</b>' + esc(t.hq) + '</div>' : "") + '</div>';
    }).join("") + '</div>' +
    '<p class="kmw-end">' + esc(K.end) + '</p>';
}
function askLevel(lv){
  var L = [], V = D.verdict;
  L.push("CÁC MỤC CỦA TRANG: " + SECK.map(function(no){ return "mục " + no + " " + SEC[no].t; }).join("; ") + "; Hỏi đáp; Cập nhật sao kê mới; Tra cứu giao dịch; Tải về.");
  L.push("KẾT LUẬN CHUNG: " + V.answer + " " + V.nd.join(" "));
  if (D.km) L.push("HIỂU ĐÚNG VẤN ĐỀ (bốn ý): " + D.km.head + " " + D.km.tiers.map(function(t){ return t.tag + ": " + t.t + ". " + t.d.join(" "); }).join(" ") + " " + D.km.end);
  V.tiers.forEach(function(tr){ L.push(tr.name + ":"); tr.items.forEach(function(it){ L.push("- " + it.h + ". " + it.t + (it.rule ? " (" + it.rule + ")" : "") + (it.code ? " [" + it.code + "]" : "")); }); });
  L.push("KẾT LUẬN TỪNG MỤC:");
  SECK.forEach(function(no){ var c = D.concl[no]; if (c) L.push("mục " + no + " " + SEC[no].t + " (" + c[0] + "): " + c[2].join(" ")); });
  L.push("HỎI ĐÁP ĐÃ SOẠN (H là câu hỏi, Đ là trả lời):");
  FQ.items.forEach(function(it){ L.push("H: " + it.q + " Đ: " + it.a + (lv < 2 || it.hot ? " " + it.d.join(" ") : "")); });
  if (D.lg) L.push("HỆ QUẢ PHÁP LÝ (khung chung, không phải kết luận): " + D.lg.nd.join(" ") + " " + D.lg.ladder.map(function(x){ return x.name + ": " + x.lines.join(" "); }).join(" ") + " Hình thức xử lý: " + D.lg.forms.map(function(r){ return r[0] + " (" + r[2] + "): " + r[1]; }).join(" ") + " Bãi nhiệm: " + D.lg.bai.map(function(b){ return b[0] + " (" + b[1] + "): " + b[2]; }).join("; ") + ". " + D.lg.bai_end + " " + D.lg.note);
  L.push("16 DẤU HIỆU (mức độ, tình trạng pháp lý):");
  D.findings.forEach(function(f){ L.push(f.id + " mức " + f.sev + (f.lst ? ", " + D.lg.st[f.lst] : "") + (f.nn ? ", nguyên nhân sơ bộ " + D.nnl[f.nn] : "") + ": " + f.title + ". " + (lv < 1 ? f.view + " " + (f.lhqlab || "Hệ quả") + ": " + f.lhq + " " + f.liflab + ": " + f.lif + " Hồ sơ cần: " + f.ask : lv < 2 && f.lst ? (f.lhqlab || "Hệ quả") + ": " + f.lhq : "")); });
  L.push("TÀI LIỆU BQT CUNG CẤP 28/09/2026: " + D.docs.nd.join(" ") + " Câu hỏi mới: " + D.docs.q.join(" "));
  L.push("NẾU HẠCH TOÁN ĐÚNG: " + D.ht.nd.join(" "));
  L.push("ĐỐI CHIẾU HỢP ĐỒNG: " + D.hd_nd.join(" "));
  L.push("HỒ SƠ CẦN ĐÒI: " + D.requests.map(function(r, i){ return (i + 1) + ". " + r.doc + " (ưu tiên " + r.pri.toLowerCase() + ")"; }).join("; "));
  if (M && M.hasNew) L.push("DỮ LIỆU MỚI NẠP THÊM TỚI " + M.asof + ": quỹ còn " + vnd(M.fund_end) + " đồng; tiền lãi " + vnd(M.interest) + " đồng; chi khỏi quỹ " + vnd(M.spend) + " đồng; thu khu vực chung ngoài quỹ " + vnd(M.ca_total) + " đồng.");
  return L.join("\n");
}
function askContext(){ var s = ""; for (var lv = 0; lv < 3; lv++){ s = askLevel(lv); if (new Blob([s]).size <= 54000) break; } return s; }
function askPrompt(q){
  return "Bạn là trợ lý giải đáp cho cư dân chung cư Nam Sài Gòn Residences (Saigon South Residences) về quỹ bảo trì. Chỉ trả lời dựa trên DỮ LIỆU bên dưới: phân tích độc lập sao kê ngân hàng 15/08/2024 – 31/05/2026 và tài liệu Ban quản trị cung cấp ngày 28/09/2026.\n" +
    "Quy tắc:\n1. Tiếng Việt có dấu, giọng khách quan, câu ngắn; câu đầu trả lời thẳng câu hỏi; tối đa 7 câu, mỗi câu một dòng.\n" +
    "2. Chỉ dùng số liệu có trong dữ liệu, ghi đúng như dữ liệu; nếu tự cộng trừ thì nói rõ là tính thêm.\n" +
    "3. Nếu dữ liệu chưa đủ để trả lời, nói rõ và nêu hồ sơ cần yêu cầu Ban quản trị hoặc ngân hàng cung cấp.\n" +
    "4. Phân biệt điều đã rõ trên sao kê với điều còn nghi vấn; không kết luận ai có tội, không suy đoán động cơ.\n" +
    "5. Không nêu tên cá nhân; gọi là Ban quản trị, ngân hàng hoặc tên doanh nghiệp.\n" +
    "6. Không dùng markdown, không gạch đầu dòng, không ký hiệu mũi tên.\n" +
    "7. Dòng cuối bắt đầu bằng \"Xem thêm:\" rồi nêu một hoặc hai mục liên quan, dạng \"mục 05 Tiền đi đâu\".\n" +
    "Nếu câu hỏi không liên quan tới quỹ bảo trì, tài khoản, chi tiêu, quy chế hay việc cư dân cần làm, trả lời ngắn rằng trang chỉ giải đáp về quỹ bảo trì.\n\n" +
    "DỮ LIỆU:\n" + askContext() + "\n\nCÂU HỎI CỦA CƯ DÂN: " + q;
}
function askErr(e){
  var c = e && e.code;
  if (c === "cancelled") return "Đã dừng.";
  if (c === "not_granted") return "Bạn chưa cho phép trang dùng Claude, nên chưa trả lời được. Các câu hỏi đáp có sẵn vẫn dùng bình thường.";
  if (c === "sampling_disabled" || c === "not_declared" || c === "capability_disabled" || c === "capability_removed") return "Chế độ xem này không dùng được Claude để trả lời. Vui lòng xem các câu hỏi đáp có sẵn.";
  if (c === "rate_limited" || c === "queue_overflow") return "Đã dùng hết lượt Claude trong lúc này; thử lại sau ít phút.";
  if (c === "prompt_too_large") return "Câu hỏi quá dài; hãy hỏi ngắn hơn.";
  if (c === "session_expired") return "Phiên đăng nhập đã hết hạn; hãy đăng nhập lại rồi hỏi lại.";
  if (c === "refused") return "Claude không trả lời câu hỏi này. Vui lòng hỏi cụ thể về quỹ bảo trì.";
  return "Chưa trả lời được lúc này; hãy thử lại sau.";
}
function askFmt(txt){
  var lines = String(txt || "").replace(/\r/g, "").split(/\n+/).map(function(x){ return x.replace(/^\s*(?:[-*•#>]+|\d+[.)]\s)\s*/, "").replace(/\*\*|__|`/g, "").trim(); }).filter(Boolean);
  return lines.map(function(x, i){
    var h = esc(x).replace(/(mục\s+)(0[1-9]|1[0-2])(?![0-9])/gi, function(m, a, no){ return SEC[no] ? '<a href="#' + SEC[no].id + '">' + a + no + "</a>" : m; });
    return '<p class="' + (/^xem thêm/i.test(x) ? "ask-see" : i === 0 ? "ask-lead" : "") + '">' + h + "</p>";
  }).join("");
}
function askCardHtml(r){
  var body = r.a ? askFmt(r.a) : (r.st === "run" ? '<div class="ask-wait"><i></i>Claude đang soạn câu trả lời, thường mất 10 – 40 giây…</div>' : "");
  var foot = r.st === "run" ? "" : r.st === "err" ? '<div class="ask-err">' + esc(r.err) + "</div>" : '<div class="ask-f">Claude trả lời lúc ' + esc(fmtIso(r.at)) + " dựa trên dữ liệu của trang. Câu trả lời tự động, cần đối chiếu với mục chi tiết." + (r.st === "trunc" ? " Câu trả lời bị cắt ngắn." : "") + "</div>";
  return '<div class="ask-card"><div class="ask-q">Câu hỏi: <span>' + esc(r.q) + '</span></div><div class="ask-a">' + body + "</div>" + foot + "</div>";
}
function renderAsk(){ $("hd-ask-out").innerHTML = ASK.list.map(askCardHtml).join(""); $("hd-ask-go").disabled = !!ASK.ctl; $("hd-ask-stop").hidden = !ASK.ctl; renderAskBox(); }
function runAsk(q){
  q = String(q || "").replace(/\s+/g, " ").trim().slice(0, 500);
  if (!q){ toast("Vui lòng nhập câu hỏi."); return; }
  if (!CAP.sample || ASK.ctl) return;
  var ctl = new AbortController(), rec = {q: q, a: "", at: nowIso(), st: "run"};
  ASK.ctl = ctl; ASK.list.unshift(rec); ASK.list = ASK.list.slice(0, 5); renderAsk();
  CAP.sample(askPrompt(q), {signal: ctl.signal, modelTier: "default", onText: function(x){ rec.a = x.text; var c = $("hd-ask-out").firstChild; if (c && ASK.list[0] === rec){ var a = c.querySelector(".ask-a"); if (a) a.innerHTML = askFmt(rec.a); } }}).then(function(r){
    rec.a = (r && r.text) || rec.a; rec.st = r && r.truncated ? "trunc" : "done"; rec.at = nowIso();
  }).catch(function(e){
    rec.st = "err"; rec.err = askErr(e); if (e && e.text) rec.a = e.text;
    if (e && ["not_granted", "sampling_disabled", "not_declared", "capability_disabled", "capability_removed"].indexOf(e.code) >= 0) CAP.sample = null;
  }).then(function(){ if (ASK.ctl === ctl) ASK.ctl = null; renderAsk(); });
}

/* ============================== transactions ============================== */
function txBase(){ return window.matchMedia && window.matchMedia("(max-width: 760px)").matches ? 30 : 120; }
var TXLIM = txBase();
function smallRow(t){ return (t.c === "Phí ngân hàng" || t.c === "Lãi không kỳ hạn") && (t.dr + t.cr) < 5e6; }
function renderTxCats(){
  var cats = []; M.all.forEach(function(t){ if (cats.indexOf(t.c) < 0) cats.push(t.c); }); cats.sort();
  var sel = $("f-cat"), cur = sel.value;
  sel.innerHTML = '<option value="">Mọi phân loại</option>' + cats.map(function(c){ return "<option" + (c === cur ? " selected" : "") + ">" + esc(c) + "</option>"; }).join("");
  $("f-src").disabled = !M.hasNew;
}
function renderTx(){
  var acc = $("f-acc").value, cat = $("f-cat").value, src = $("f-src").value, fl = $("f-flag").checked, sm = $("f-small").checked, q = norm($("f-q").value);
  var rows = M.all.filter(function(t){ if (acc && t.a !== acc) return false; if (cat && t.c !== cat) return false; if (src !== "" && String(t.src) !== src) return false; if (fl && !WARN[t.v]) return false; if (sm && smallRow(t)) return false; if (q && norm(t.s + " " + t.cp + " " + t.c + " " + t.n + " " + t.d).indexOf(q) < 0) return false; return true; });
  var dr = 0, cr = 0; rows.forEach(function(t){ dr += t.dr; cr += t.cr; });
  $("tsum").innerHTML = "Đang hiện <b>" + rows.length + "</b> / " + M.all.length + " giao dịch · tiền ra <b>" + vnd(dr) + "</b> đ · tiền vào <b>" + vnd(cr) + "</b> đ";
  var lim = TXLIM, shown = rows.slice(0, lim);
  $("tb").innerHTML = shown.map(function(t){ return '<tr class="' + (WARN[t.v] ? "f-" + t.v : "") + '"><td class="c-acc"><span class="acc">' + t.a + '</span></td><td class="num c-dt" style="white-space:nowrap">' + t.d + (t.src ? '<span class="newb">Mới</span>' : "") + '</td><td class="desc">' + esc(t.s) + '</td><td class="n c-dr">' + (t.dr ? vnd(t.dr) : "") + '</td><td class="n c-cr">' + (t.cr ? vnd(t.cr) : "") + '</td><td class="n c-bal">' + vnd(t.b) + (t.mis ? '<div class="note" style="color:var(--crit);margin-top:2px">lệch ' + vnd(t.mis) + "</div>" : "") + '</td><td class="cp">' + esc(t.cp) + '</td><td class="cat">' + esc(t.c) + '</td><td class="c-flag">' + (t.v ? '<span class="pill sev-' + t.v + '"><i class="dot"></i>' + t.v + '</span><div class="note" style="margin-top:4px;min-width:200px">' + esc(t.n) + "</div>" : "") + "</td></tr>"; }).join("");
  var more = $("tx-more"); if (more){ more.hidden = rows.length <= lim; more.textContent = "Hiện thêm " + Math.min(txBase() === 30 ? 30 : 100, rows.length - lim) + " giao dịch (còn " + (rows.length - lim) + ")"; }
  $("tx-h2").textContent = M.all.length + " giao dịch của ba tài khoản" + (M.hasNew ? ", gồm " + M.nw.length + " dòng mới" : "");
}

/* ============================== glossary, footer ============================== */
function renderGlossary(){ $("glo").innerHTML = D.glo.map(function(g){ return "<div><b>" + esc(g[0]) + "</b>" + esc(g[1]) + "</div>"; }).join(""); }
function renderFoot(){
  $("foot-upd").textContent = "Bản phân tích lập ngày " + D.built + " trên dữ liệu tới 31/05/2026." + (U.updatedAt ? " Dữ liệu trang cập nhật lần cuối " + fmtIso(U.updatedAt) + "." : "") + (M.hasNew ? " Dữ liệu mới tới " + M.asof + "." : "");
}
var ABBR = {"KPBT": "Kinh phí bảo trì phần sở hữu chung (quỹ bảo trì)", "BQT": "Ban quản trị nhà chung cư", "HNNCC": "Hội nghị nhà chung cư", "HĐTG": "Hợp đồng tiền gửi có kỳ hạn", "PCCC": "Phòng cháy chữa cháy"};
function applyAbbr(){
  var rx = /(^|[^0-9A-Za-zÀ-ỹĐđ])(KPBT|BQT|HNNCC|HĐTG|PCCC)(?=$|[^0-9A-Za-zÀ-ỹĐđ])/;
  qa("main section").forEach(function(sec){
    if (sec.id === "hoi-dap") return;
    var seen = {};
    var w = document.createTreeWalker(sec, NodeFilter.SHOW_TEXT, {acceptNode: function(n){ var p = n.parentNode; while (p && p !== sec){ var tg = p.nodeName.toLowerCase(); if (tg === "svg" || tg === "script" || tg === "style" || tg === "button" || tg === "select" || tg === "option" || tg === "textarea" || tg === "abbr" || tg === "th" || tg === "summary" || (p.classList && (p.classList.contains("cd") || p.classList.contains("acc") || p.classList.contains("pill") || p.id === "tb" || p.id === "pv-body"))) return NodeFilter.FILTER_REJECT; p = p.parentNode; } return rx.test(n.nodeValue) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT; }});
    var nodes = []; while (w.nextNode()) nodes.push(w.currentNode);
    nodes.forEach(function(n){
      var m = rx.exec(n.nodeValue); if (!m || seen[m[2]]) return; seen[m[2]] = 1;
      var start = m.index + m[1].length, ab = document.createElement("abbr"); ab.title = ABBR[m[2]]; ab.textContent = m[2];
      var after = n.splitText(start); after.nodeValue = after.nodeValue.slice(m[2].length); n.parentNode.insertBefore(ab, after);
    });
  });
}
