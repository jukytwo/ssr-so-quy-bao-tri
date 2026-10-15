"use strict";
/* ============================== helpers ============================== */
var $ = function(id){ return document.getElementById(id); };
function qa(sel, root){ return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }
function esc(s){ return String(s == null ? "" : s).replace(/[&<>"]/g, function(c){ return {"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;"}[c]; }); }
function vnd(n){ var neg = n < 0; var s = Math.round(Math.abs(n)).toString().replace(/\B(?=(\d{3})+(?!\d))/g, "."); return (neg ? "−" : "") + s; }
function ty(n, d){ d = d == null ? 2 : d; return (n / 1e9).toFixed(d).replace(".", ","); }
function tr(n, d){ d = d == null ? 1 : d; return (n / 1e6).toFixed(d).replace(".", ","); }
function pct(x, d){ d = d == null ? 1 : d; return (x * 100).toFixed(d).replace(".", ",") + "%"; }
function money(n){ var a = Math.abs(n); if (a >= 1e9) return ty(n, 2) + " tỷ"; if (a >= 1e6) return tr(n, 1) + " triệu"; return vnd(n) + " đồng"; }
function signed(n){ return (n > 0 ? "+" : n < 0 ? "−" : "") + money(Math.abs(n)); }
function norm(s){ return String(s == null ? "" : s).normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/đ/g, "d").replace(/Đ/g, "D").toUpperCase().replace(/\s+/g, " ").trim(); }
function dkey(d){ var p = String(d || "").split("/"); return p.length === 3 ? p[2] + p[1] + p[0] : ""; }
function kdate(k){ return k ? k.slice(6, 8) + "/" + k.slice(4, 6) + "/" + k.slice(0, 4) : ""; }
function kiso(k){ return k.slice(0, 4) + "-" + k.slice(4, 6) + "-" + k.slice(6, 8); }
function uid(){ return "b" + Date.now().toString(36) + Math.random().toString(36).slice(2, 6); }
function nowIso(){ try { return new Date().toISOString(); } catch (e) { return ""; } }
function fmtIso(s){ if (!s) return ""; var d = new Date(s); if (isNaN(d)) return ""; var p = function(n){ return (n < 10 ? "0" : "") + n; }; return p(d.getDate()) + "/" + p(d.getMonth() + 1) + "/" + d.getFullYear() + " " + p(d.getHours()) + ":" + p(d.getMinutes()); }
function lsGet(k){ try { return window.localStorage.getItem(k); } catch (e) { return null; } }
function lsSet(k, v){ try { window.localStorage.setItem(k, v); return true; } catch (e) { return false; } }
function ssGet(k){ try { return window.sessionStorage.getItem(k); } catch (e) { return null; } }
function ssSet(k, v){ try { window.sessionStorage.setItem(k, v); } catch (e) {} }
function ssDel(k){ try { window.sessionStorage.removeItem(k); } catch (e) {} }
var NS = "http://www.w3.org/2000/svg";
function el(tag, attrs, parent){ var e = document.createElementNS(NS, tag); for (var k in attrs) e.setAttribute(k, attrs[k]); if (parent) parent.appendChild(e); return e; }
function txt(parent, x, y, s, cls, anchor){ var t = el("text", {x: x, y: y, "class": cls || "lbl", "text-anchor": anchor || "start"}, parent); t.textContent = s; return t; }
function wrapWords(s, max){ var w = String(s).split(" "), lines = [], cur = ""; w.forEach(function(x){ if ((cur + " " + x).trim().length > max && cur){ lines.push(cur); cur = x; } else cur = (cur + " " + x).trim(); }); if (cur) lines.push(cur); return lines; }
var toastT = null;
function toast(msg, ms){ var t = $("toast"); if (!t) return; t.textContent = msg; t.hidden = false; clearTimeout(toastT); toastT = setTimeout(function(){ t.hidden = true; }, ms || 4200); }

/* ============================== data ============================== */
var D = JSON.parse($("D").textContent);
var IMG = JSON.parse($("IMG").textContent);
var U0 = {};
try { U0 = JSON.parse($("U").textContent || "{}") || {}; } catch (e) { U0 = {}; }
function normU(u){
  u = u && typeof u === "object" ? u : {};
  return {v: 1, updatedAt: u.updatedAt || "", batches: Array.isArray(u.batches) ? u.batches.filter(function(b){ return b && b.acc && Array.isArray(b.rows); }) : [],
          tracker: u.tracker && typeof u.tracker === "object" ? u.tracker : {}, ai: u.ai && typeof u.ai === "object" ? u.ai : null};
}
function cloneU(u){ return JSON.parse(JSON.stringify(u)); }
var U = normU(cloneU(U0));
var SAVED_BIDS = {};
U.batches.forEach(function(b){ SAVED_BIDS[b.id] = 1; });
var DIRTY = {batches: false, tracker: false, ai: false};
function isDirty(){ return DIRTY.batches || DIRTY.tracker || DIRTY.ai; }

var ACCN = {"999": "116605084999", "AGR": "6350201010476", "7784": "117002997784"};
var ACCL = {"999": "VietinBank 116605084999 (quỹ)", "AGR": "Agribank 6350201010476 (quỹ)", "7784": "VietinBank 117002997784 (thu dịch vụ)"};
var ACCS = {"999": "TK 999", "AGR": "TK Agribank", "7784": "TK 7784"};
var BANK = {"999": "VietinBank", "AGR": "Agribank", "7784": "VietinBank"};
var FUNDA = {"999": 1, "AGR": 1};
var BASE_ASOF = D.base.asof;
var BASE_K = dkey(BASE_ASOF);

/* ============================== capabilities ============================== */
var CAP = {mode: "init", art: null, sample: null, dl: null, user: null, canEdit: false};
var CAP_CBS = [];
function onCaps(fn){ CAP_CBS.push(fn); }
function useCap(n){ try { return Promise.resolve(window.claude.use(n)).catch(function(){ return null; }); } catch (e) { return Promise.resolve(null); } }
var CAPP = {};
function capP(n){ if (!CAPP[n]) CAPP[n] = useCap(n); return CAPP[n]; }
function withTimeout(p, ms, v){ return Promise.race([p, new Promise(function(r){ setTimeout(function(){ r(v); }, ms); })]); }
function initCaps(){
  if (window.claude && typeof window.claude.use === "function"){
    CAP.mode = "reader"; CAP.framed = true;
    capP("downloads").then(function(d){ CAP.dl = d; CAP.dlKnown = true; if (typeof renderDlNote === "function") renderDlNote(); });
    capP("sample").then(function(sm){ CAP.sample = sm; if (typeof renderBatches === "function" && M) renderBatches(); try { renderAskBox(); applyFAQ(); } catch (e) {} });
    Promise.all([capP("artifact"), capP("user")]).then(function(r){
      CAP.art = r[0]; CAP.user = r[1];
      var p = CAP.user && CAP.user.canEdit ? Promise.resolve(CAP.user.canEdit()).catch(function(){ return false; }) : Promise.resolve(false);
      return p.then(function(ce){ CAP.canEdit = !!ce && !!CAP.art; CAP.mode = CAP.canEdit ? "writer" : "reader"; });
    }).catch(function(){ CAP.mode = "reader"; }).then(function(){ CAP_CBS.forEach(function(f){ try { f(); } catch (e) { if (window.console) console.error(e); } }); });
  } else if (/github\.io$/i.test(location.hostname)){
    /* ban dang tren GitHub Pages: ai cung chi xem, khong sua, khong luu tren may */
    CAP.mode = "reader"; CAP.framed = false; CAP.pages = true;
    setTimeout(function(){ CAP_CBS.forEach(function(f){ try { f(); } catch (e) { if (window.console) console.error(e); } }); }, 0);
  } else {
    CAP.mode = "local"; CAP.framed = window.self !== window.top;
    var raw = lsGet("ssr-u-v3");
    if (raw){ try { var lu = normU(JSON.parse(raw)); if ((lu.updatedAt || "") > (U.updatedAt || "")){ U = lu; U.batches.forEach(function(b){ SAVED_BIDS[b.id] = 1; }); CAP.localLoaded = true; } } catch (e) {} }
    setTimeout(function(){ CAP_CBS.forEach(function(f){ try { f(); } catch (e) { if (window.console) console.error(e); } }); }, 0);
  }
}
function canWrite(){ return CAP.mode === "writer" || CAP.mode === "local"; }

/* ============================== classification of new rows ============================== */
var COMPANY_RX = /(CONG TY|CTY|TNHH|CO PHAN|\bCP\b|\bJSC\b|\bLTD\b|DNTN|HTX|HOP TAC XA|NGAN HANG|\bBANK\b|KHO BAC|\bBQT\b|BAN QUAN TRI|CHI NHANH|TRUNG TAM|UBND|BAO HIEM|TAP DOAN|VIEN |TRUONG |DICH VU|THUONG MAI|XAY DUNG|KY THUAT|CO DIEN|THIET BI|MEDIA|SCHINDLER|COMPANY|CORP|GROUP|NHA CHUNG CU|RESIDENCES|KINH PHI|NOI THAT|CONG NGHE|VIEN THONG|DIEN LUC|CAP NUOC|\bSO\b)/;
function personLike(cp){
  var c = norm(cp).replace(/[^A-Z ]/g, " ").replace(/\s+/g, " ").trim();
  if (!c || COMPANY_RX.test(norm(cp))) return false;
  var w = c.split(" ");
  return w.length >= 2 && w.length <= 5;
}
function classify(acc, r){
  var u = norm(r.s), cp = norm(r.cp), both = u + " | " + cp, dr = +r.dr || 0, cr = +r.cr || 0, fund = !!FUNDA[acc];
  var other = acc === "999" ? "6350201010476" : "116605084999";
  var c = "";
  if (/MO TAI KHOAN/.test(u)) c = "Mở tài khoản (tiền nộp ban đầu)";
  else if (cr && /NAM SAI GON RESIDENCES/.test(cp) && /(CT CP|CONG TY CP|CONG TY CO PHAN)/.test(cp)) c = "Nhận bàn giao KPBT từ chủ đầu tư";
  else if (dr && /(TRICH TIEN MO HDTG|GUI HDTG|^HDTG |HOP DONG TIEN GUI|MO HOP DONG|GUI TIET KIEM|TIEN GUI CO KY HAN|MO SO TIET KIEM)/.test(u)) c = "Gửi tiền có kỳ hạn (HĐTG)";
  else if (cr && /TAT TOAN/.test(u)) c = "Tất toán HĐTG (gốc + lãi về TK)";
  else if (/CHUYEN KHOAN TIEN LAI HDTG/.test(u)) c = "Chuyển nội bộ giữa hai TK KPBT";
  else if (fund && (both.indexOf(other) >= 0 || (acc === "AGR" && u === "CHUYEN TIEN") || /^912A2480ZC1GGR25/.test(u))) c = "Chuyển nội bộ giữa hai TK KPBT";
  else if (cr && /(TRA LAI TK TIEN GUI|TRA LAI HDTG|LAI TIEN GUI CO KY HAN)/.test(u)) c = "Lãi tiền gửi có kỳ hạn";
  else if (cr && /(TRA LAI TAI KHOAN DDA|LAI TIEN GUI|TRA LAI|LAI NHAP GOC|INTEREST|LAI KHONG KY HAN)/.test(u)) c = cr >= 50e6 ? "Lãi tiền gửi có kỳ hạn" : "Lãi không kỳ hạn";
  else if (fund && cr && /(117002997784|THU PHI DICH VU)/.test(both)) c = "Nhận tiền khu vực chung chuyển về quỹ";
  else if (!fund && dr && /(116605084999|6350201010476|KINH PHI BAO TRI|QUY BAO TRI|KPBT)/.test(both)) c = "Chuyển tiền khu vực chung về quỹ bảo trì";
  else if (/SCHINDLER/.test(both)) c = "Chi thang máy – Schindler";
  else if (/(118002976372|HOAN TAM UNG|HOAN UNG|KINH PHI QUAN LY VAN HANH)/.test(both)) c = dr ? "Chuyển KPBT sang TK vận hành của BQT" : "Nhận tiền từ TK vận hành của BQT";
  else if (/(^|[^A-Z])HNB([^A-Z]|$)/.test(cp)) c = "Chi sửa chữa cấp nước – HNB";
  else if (/THEP QUANG/.test(both)) c = "Chi mua thiết bị – Thép Quang";
  else if (/CHICILON/.test(both)) c = cr ? "Thu khu vực chung – quảng cáo (Chicilon)" : "Chuyển thu khu vực chung ra khỏi KPBT";
  else if (cr && /(CT ACT|VIEN THONG ACT)/.test(both)) c = "Thu khu vực chung – thuê mặt bằng (ACT)";
  else if (cr && /(STANDEE|HUNG THAI)/.test(both)) c = "Thu khu vực chung – standee (Hưng Thái)";
  else if (cr && /(QUANG CAO|THUE MAT BANG|MAT BANG|KHAI THAC|CHO THUE|KHU VUC CHUNG|STANDEE|\bBTS\b|SAN THUONG)/.test(both)) c = "Thu khu vực chung – khác";
  else if (dr && /(NOP THUE|NSNN|NGAN SACH NHA NUOC|KHO BAC)/.test(both)) c = "Nộp thuế";
  else if (dr && /THANH CONG/.test(cp)) c = "Chi sửa chữa, mua sắm – Thành Công";
  else if (dr && /KHOI SANG VIET/.test(both)) c = "Chi hệ thống giữ xe – Khởi Sáng Việt";
  else if (dr > 22000 && /KTECH/.test(both)) c = "Chi hệ thống camera – KTECH";
  else if (dr && /(RUT TIEN MAT|TIEN MAT|RUT TM|\bATM\b)/.test(u)) c = "Rút tiền mặt";
  else if (dr && dr <= 2e6 && /(PHI|VAT|SMS|QUAN LY TK|FEE|DUY TRI)/.test(u)) c = "Phí ngân hàng";
  else if (dr && dr <= 300000 && !cp) c = "Phí ngân hàng";
  else if (dr) c = "Chi khác – chưa phân loại";
  else if (cr) c = "Thu khác – chưa phân loại";
  else c = "Không có số tiền";
  var v = "", n = "";
  if (c === "Chuyển KPBT sang TK vận hành của BQT"){ v = "Đỏ"; n = "Tiền quỹ chuyển vào tài khoản vận hành của chính Ban quản trị, không phải tài khoản đơn vị bảo trì (Quy chế Điều 7.2, 7.4)"; }
  else if (c === "Rút tiền mặt"){ v = "Đỏ"; n = "Rút tiền mặt từ tài khoản " + (fund ? "quỹ bảo trì" : "thu dịch vụ") + "; cần chứng từ chi và lý do không chuyển khoản"; }
  else if (c === "Chuyển thu khu vực chung ra khỏi KPBT"){ v = "Đỏ"; n = "Thu khai thác phần sở hữu chung bị chuyển ra khỏi tài khoản quỹ (khoản 4 Điều 153 Luật Nhà ở 2023)"; }
  else if (c === "Chi mua thiết bị – Thép Quang"){ v = "Đỏ"; n = "Nhà cung cấp đã có dấu hiệu F03; cần danh mục hàng hóa, 3 báo giá, biên bản nghiệm thu"; }
  else if (dr && dr >= 10e6 && personLike(r.cp)){ v = "Cam"; n = "Người nhận có vẻ là cá nhân; cần chứng từ và lý do chi"; }
  else if (fund && dr && (c === "Chi khác – chưa phân loại" || c === "Chi thang máy – Schindler" || c === "Chi sửa chữa cấp nước – HNB")){
    if (dr >= 50e6){ v = "Cam"; n = "Khoản chi mới từ quỹ: cần kế hoạch bảo trì được thông qua, 3 báo giá và biên bản nghiệm thu trước khi trả (Điều 6.3)"; }
    else { v = "Vàng"; n = "Khoản chi nhỏ từ quỹ, cần hóa đơn và nghiệm thu"; }
  }
  else if (!fund && cr && c.indexOf("Thu khu vực chung") === 0){ v = "Cam"; n = "Thu khai thác phần sở hữu chung vẫn vào TK 7784, không vào tài khoản quỹ (khoản 4 Điều 153 Luật Nhà ở 2023)"; }
  else if (!fund && dr && ["Nộp thuế", "Phí ngân hàng", "Chuyển tiền khu vực chung về quỹ bảo trì"].indexOf(c) < 0){ v = "Cam"; n = "Chi từ tiền khu vực chung ngoài quy trình của quỹ (F07)"; }
  else if (c === "Gửi tiền có kỳ hạn (HĐTG)" && /(^|[^0-9])(1|2|3|6) ?THANG|(^|[^0-9])(1|3|6)M([^A-Z]|$)/.test(u)){ v = "Vàng"; n = "Kỳ hạn ngắn, lãi thấp hơn kỳ hạn 12 tháng"; }
  else if (c === "Nhận tiền khu vực chung chuyển về quỹ" || c === "Chuyển tiền khu vực chung về quỹ bảo trì"){ v = "Xanh"; n = "Đúng hướng khắc phục: tiền khu vực chung về tài khoản quỹ"; }
  else if (fund && cr && c.indexOf("Thu khu vực chung") === 0){ v = "Xanh"; n = "Đúng tài khoản quỹ theo khoản 4 Điều 153 Luật Nhà ở 2023"; }
  else if (c === "Chi khác – chưa phân loại" && !fund && dr){ v = "Cam"; n = "Chi từ tiền khu vực chung ngoài quy trình của quỹ (F07)"; }
  return {c: c, v: v, n: n};
}
var WARN = {"Đỏ": 1, "Cam": 1, "Vàng": 1};

/* ============================== model ============================== */
function matchPrincipal(amount, acc, tds){
  var bank = BANK[acc], best = null;
  tds.forEach(function(t, i){
    if (t.gone) return;
    var ok = t.v <= amount && (amount - t.v) <= 0.12 * t.v;
    if (!ok) return;
    var score = (t.bank === bank ? 2e13 : 0) + t.v;
    if (!best || score > best.score) best = {i: i, score: score};
  });
  if (!best) return null;
  tds[best.i].gone = true;
  return tds[best.i];
}
function compute(){
  var M = {};
  var base = D.tx.map(function(t, i){ return {a: t.a, d: t.d, k: dkey(t.d), s: t.s, dr: t.dr, cr: t.cr, b: t.b, cp: t.cp, c: t.c, v: t.v, n: t.n, src: 0, i: i}; });
  var nw = [];
  U.batches.forEach(function(bt, bi){
    if (bt.rm) return;
    bt.rows.forEach(function(r, i){
      var cl = classify(bt.acc, r);
      nw.push({a: bt.acc, d: r.d, k: dkey(r.d), s: r.s || "", dr: +r.dr || 0, cr: +r.cr || 0, b: (r.b == null || r.b === "") ? null : +r.b, cp: r.cp || "", c: cl.c, v: cl.v, n: cl.n, src: 1, bid: bt.id, i: 100000 + bi * 10000 + i});
    });
  });
  var all = base.concat(nw).sort(function(x, y){ return x.k < y.k ? -1 : x.k > y.k ? 1 : x.i - y.i; });
  var last = {};
  all.forEach(function(t){
    var L = last[t.a], exp = L ? L.b + t.cr - t.dr : null;
    if (t.b == null) t.b = exp == null ? t.cr - t.dr : exp;
    if (t.src && exp != null && Math.abs(exp - t.b) > 1) t.mis = t.b - exp;
    last[t.a] = {b: t.b, k: t.k};
  });
  M.all = all; M.nw = nw; M.hasNew = nw.length > 0; M.last = last;
  var tds = D.comp.filter(function(c){ return c.k === "td"; }).map(function(c){ return {l: c.l, v: c.v, st: c.st, bank: c.l.indexOf("Agribank") >= 0 ? "Agribank" : "VietinBank"}; });
  var g = {int: 0, oth: 0, spend: 0, fees: 0, ca7784: 0, out7784: 0, tax7784: 0, caFund: 0, tdOpen: [], tdClose: [], cnt: {"Đỏ": 0, "Cam": 0, "Vàng": 0, "Xanh": 0}};
  nw.forEach(function(t){
    if (t.v) g.cnt[t.v] = (g.cnt[t.v] || 0) + 1;
    if (FUNDA[t.a]){
      if (t.cr){
        if (t.c === "Lãi không kỳ hạn" || t.c === "Lãi tiền gửi có kỳ hạn") g.int += t.cr;
        else if (t.c === "Tất toán HĐTG (gốc + lãi về TK)"){ var m = matchPrincipal(t.cr, t.a, tds); var p = m ? m.v : t.cr; g.int += t.cr - p; g.tdClose.push({a: t.a, d: t.d, v: p, i: t.cr - p, l: m ? m.l : "không xác định được hợp đồng"}); }
        else if (t.c === "Chuyển nội bộ giữa hai TK KPBT"){}
        else { g.oth += t.cr; if (t.c.indexOf("Thu khu vực chung") === 0 || t.c === "Nhận tiền khu vực chung chuyển về quỹ") g.caFund += t.cr; }
      }
      if (t.dr){
        if (t.c === "Gửi tiền có kỳ hạn (HĐTG)"){ g.tdOpen.push({a: t.a, d: t.d, v: t.dr}); tds.push({l: "HĐTG mới " + BANK[t.a] + " " + ty(t.dr, t.dr % 1e9 ? 2 : 0) + " tỷ", v: t.dr, st: "Gửi ngày " + t.d + ", cần giấy xác nhận", bank: BANK[t.a], nw: 1}); }
        else if (t.c === "Chuyển nội bộ giữa hai TK KPBT"){}
        else if (t.c === "Phí ngân hàng") g.fees += t.dr;
        else g.spend += t.dr;
      }
    } else {
      if (t.cr && t.c !== "Lãi không kỳ hạn") g.ca7784 += t.cr;
      if (t.dr && t.c === "Nộp thuế") g.tax7784 += t.dr;
      else if (t.dr && t.c !== "Phí ngân hàng" && t.c !== "Chuyển tiền khu vực chung về quỹ bảo trì") g.out7784 += t.dr;
    }
  });
  M.g = g;
  var B = D.base;
  M.fund_end = B.fund_end + g.int + g.oth - g.spend - g.fees;
  M.interest = B.interest + g.int;
  M.spend = B.spend + g.spend;
  M.ca_total = B.ca_total + g.ca7784;
  M.repair7784 = B.repair7784 + g.out7784;
  M.end_q = last["999"] ? last["999"].b : B.end_q;
  M.end_a = last["AGR"] ? last["AGR"].b : B.end_a;
  M.end_v = last["7784"] ? last["7784"].b : B.end_v;
  M.kAcc = {"999": last["999"] ? last["999"].k : BASE_K, "AGR": last["AGR"] ? last["AGR"].k : BASE_K, "7784": last["7784"] ? last["7784"].k : BASE_K};
  var kf = M.kAcc["999"] > M.kAcc["AGR"] ? M.kAcc["999"] : M.kAcc["AGR"];
  M.kFund = kf; M.asofFund = kdate(kf);
  var kmax = [M.kAcc["999"], M.kAcc["AGR"], M.kAcc["7784"]].sort().pop();
  M.kMax = kmax; M.asof = kdate(kmax);
  M.tds = tds.filter(function(t){ return !t.gone; });
  var tdSum = M.tds.reduce(function(a, t){ return a + t.v; }, 0);
  M.cash = M.end_q + M.end_a; M.tdSum = tdSum;
  M.recon = tdSum + M.cash - M.fund_end;
  M.series = D.series.slice();
  if (M.hasNew){
    var mp = {};
    all.forEach(function(t){ if (t.a === "999" && t.src) mp[t.k] = t.b; });
    Object.keys(mp).sort().forEach(function(k){ M.series.push([kiso(k), mp[k]]); });
    M.series.sort(function(a, b){ return a[0] < b[0] ? -1 : a[0] > b[0] ? 1 : 0; });
  }
  M.ic = interestChecks(all, nw);
  return M;
}
/* monthly DDA interest re-computation: round(sum of start-of-day balances x 0.2% / 365) from the 1st of the month to the posting day */
function interestChecks(all, nw){
  var out = [];
  ["999", "7784"].forEach(function(acc){
    var rows = all.filter(function(t){ return t.a === acc; });
    if (!rows.length) return;
    var ints = nw.filter(function(t){ return t.a === acc && t.c === "Lãi không kỳ hạn"; });
    ints.forEach(function(t){
      var y = +t.k.slice(0, 4), mo = +t.k.slice(4, 6) - 1, dd = +t.k.slice(6, 8), sum = 0;
      for (var day = 1; day <= dd; day++){
        var dk = y + ("0" + (mo + 1)).slice(-2) + ("0" + day).slice(-2), bal = 0;
        for (var j = 0; j < rows.length; j++){ if (rows[j].k < dk) bal = rows[j].b; else break; }
        sum += bal;
      }
      var exp = Math.round(sum * 0.002 / 365);
      out.push({a: acc, d: t.d, m: t.k.slice(4, 6) + "/" + t.k.slice(0, 4), act: t.cr, exp: exp, diff: t.cr - exp, rate: sum ? t.cr / (sum / 365) : 0});
    });
  });
  return out;
}
var M = null;
/* ------------------------------ chia se: duong dan toi muc, cau hoi, clip, tep (15/10/2026) ------------------------------ */
var SHARE_BASE = "https://jukytwo.github.io/ssr-so-quy-bao-tri/";
var SHR_IC = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="M8.6 13.5l6.8 4M15.4 6.5l-6.8 4"/></svg>';
var SHR_FILE = {pdf: "f/pdf.pdf", sum: "f/sum.pdf", q10pdf: "f/q10pdf.pdf", q10png: "f/q10png.png", pl: "f/pl.pdf", hdan: "f/hdan.pdf"};
function shareBtn(path, title, label, cls){
  return '<button type="button" class="' + (cls || "shr") + '" data-share="' + esc(path) + '" data-st="' + esc(title) + '" title="Chia sẻ đường dẫn" aria-label="Chia sẻ: ' + esc(title) + '">' + SHR_IC + (label === "" ? "" : "<span>" + (label || "Chia sẻ") + "</span>") + "</button>";
}
function shareUrl(path){ return SHARE_BASE + String(path || ""); }
function copyText(s){
  if (navigator.clipboard && navigator.clipboard.writeText) return navigator.clipboard.writeText(s).catch(function(){ return copyOld(s); });
  return copyOld(s);
}
function copyOld(s){
  return new Promise(function(ok, no){
    var ta = document.createElement("textarea"); ta.value = s; ta.setAttribute("readonly", ""); ta.style.position = "fixed"; ta.style.opacity = "0"; document.body.appendChild(ta); ta.select();
    var r = false; try { r = document.execCommand("copy"); } catch (e) {} document.body.removeChild(ta); r ? ok() : no(new Error("copy"));
  });
}
function shareGo(path, title){
  var url = shareUrl(path), t = "Sổ quỹ bảo trì SSR: " + title;
  var touch = window.matchMedia && window.matchMedia("(pointer: coarse)").matches;
  if (touch && navigator.share){
    navigator.share({title: t, text: t, url: url}).catch(function(e){ if (!e || e.name !== "AbortError") shareBox(url, t); });
    return;
  }
  shareBox(url, t);
}
function shareBox(url, t){
  var box = $("helpbox"); if (!box) return;
  var u = encodeURIComponent(url), tt = encodeURIComponent(t);
  box.querySelector(".hb-in").innerHTML = '<h3>Chia sẻ</h3><p class="shr-t">' + esc(t) + "</p>" +
    '<div class="shr-row"><input type="text" id="shr-u" readonly value="' + esc(url) + '" aria-label="Đường dẫn"><button type="button" class="tbtn pri" id="shr-cp">Sao chép</button></div>' +
    '<p class="shr-n">Dán đường dẫn vào Zalo, Messenger hoặc tin nhắn. Người nhận bấm vào là mở đúng phần này, không cần đăng nhập.</p>' +
    '<div class="acts"><a class="tbtn" target="_blank" rel="noopener" href="https://www.facebook.com/sharer/sharer.php?u=' + u + '">Facebook</a>' +
    '<a class="tbtn" href="mailto:?subject=' + tt + "&body=" + tt + "%0A" + u + '">Email</a>' +
    '<button type="button" class="tbtn" id="help-x">Đóng</button></div>';
  box.hidden = false;
  var inp = $("shr-u");
  copyText(url).then(function(){ toast("Đã sao chép đường dẫn. Dán vào Zalo hoặc tin nhắn để gửi.", 3600); $("shr-cp").textContent = "Đã sao chép"; })
    .catch(function(){ if (inp){ inp.focus(); inp.select(); } });
}
/* gui tep that (anh, clip, PDF) qua bang chia se cua dien thoai; may khong ho tro thi tai ve (15/10/2026) */
var SHR_PEND = null;
var SHR_MIME = {pdf: "application/pdf", png: "image/png", jpg: "image/jpeg", mp4: "video/mp4", xlsx: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", docx: "application/vnd.openxmlformats-officedocument.wordprocessingml.document"};
var A4IMG = [
  {k: "a4_tomtat", t: "Tóm tắt một trang A4", d: "Năm điểm đề nghị Ban quản trị làm rõ", n: "SSR - Tom tat mot trang A4.png"},
  {k: "a4_tt1", t: "Những điểm nào cần làm rõ", d: "Ba hồ sơ quyết định kết luận cuối cùng", n: "SSR - Anh trong tam 1 - Nhung diem can lam ro.png"},
  {k: "a4_tt2", t: "Sơ đồ dòng tiền ba tài khoản", d: "Tiền rời quỹ và tiền không vào quỹ", n: "SSR - Anh trong tam 2 - So do dong tien.png"},
  {k: "a4_tt3", t: "Ba điểm nghi vấn và việc cần làm", d: "Đối chiếu 17 quy định", n: "SSR - Anh trong tam 3 - Diem nghi van.png"},
  {k: "a4_pl", t: "Phân loại nguyên nhân", d: "Quy trình chưa chặt, lỡ tay hay có chủ đích", n: "SSR - Phan loai nguyen nhan.png"}
];
function fileExt(n){ var m = /\.([a-z0-9]+)$/i.exec(n || ""); return m ? m[1].toLowerCase() : ""; }
function shareFileGo(getBytes, name, label){
  var mime = SHR_MIME[fileExt(name)] || "application/octet-stream";
  toast("Đang chuẩn bị " + label + "…", 8000);
  getBytes().then(function(b){
    var blob = b instanceof Blob ? b : new Blob([b], {type: mime}), f = null;
    try { f = new File([blob], name, {type: mime}); } catch (e) {}
    var can = false; try { can = !!(f && navigator.canShare && navigator.canShare({files: [f]})); } catch (e) {}
    if (!can){ shareFileFallback(blob, name, mime, label); return; }
    navigator.share({files: [f]}).then(function(){ toast("Đã gửi " + label + ".", 2600); }).catch(function(e){
      if (e && e.name === "AbortError"){ $("toast").hidden = true; return; }
      SHR_PEND = {f: f, blob: blob, name: name, mime: mime, label: label}; shareReady(label, blob.size);
    });
  }).catch(function(){ toast("Chưa lấy được " + label + " ở chế độ xem này. Mở trang trực tuyến rồi thử lại.", 6000); });
}
function shareReady(label, size){
  var box = $("helpbox"); if (!box) return; $("toast").hidden = true;
  box.querySelector(".hb-in").innerHTML = "<h3>Đã sẵn sàng để gửi</h3><p class=\"shr-t\">" + esc(label) + " · " + (size / 1048576).toFixed(1).replace(".", ",") + " MB</p>" +
    '<p class="shr-n">Bấm nút dưới để mở bảng chia sẻ của máy, rồi chọn Zalo, Messenger hoặc ứng dụng khác.</p>' +
    '<div class="acts"><button type="button" class="tbtn pri" id="shr-send">' + SHR_IC + "Gửi ngay</button><button type=\"button\" class=\"tbtn\" id=\"help-x\">Đóng</button></div>";
  box.hidden = false;
}
function shareSendPending(){
  var p = SHR_PEND; if (!p) return; $("helpbox").hidden = true;
  navigator.share({files: [p.f]}).then(function(){ toast("Đã gửi " + p.label + ".", 2600); SHR_PEND = null; }).catch(function(e){
    if (e && e.name === "AbortError") return; shareFileFallback(p.blob, p.name, p.mime, p.label); SHR_PEND = null;
  });
}
function shareFileFallback(blob, name, mime, label){
  toast("Máy này chưa gửi tệp thẳng được. Đang tải " + label + " về máy; sau đó mở Zalo và đính kèm tệp vừa tải.", 7000);
  if (typeof saveFile === "function") saveFile(name, blob, mime);
}
function a4GalleryHtml(){
  return A4IMG.map(function(a){
    return '<figure class="a4c"><a class="a4t" href="f/' + a.k + '.png" target="_blank" rel="noopener"><img alt="' + esc(a.t) + '" loading="lazy" src="p/' + a.k + '.jpg" onerror="this.parentNode.classList.add(\'na\')"></a>' +
      "<figcaption><b>" + esc(a.t) + "</b><small>" + esc(a.d) + "</small>" +
      '<span class="a4b"><button type="button" class="tbtn pri" data-sendimg="' + a.k + '">' + SHR_IC + 'Gửi ảnh</button><button type="button" class="tbtn" data-saveimg="' + a.k + '">Tải</button></span></figcaption></figure>';
  }).join("");
}
function a4Item(k){ return A4IMG.filter(function(a){ return a.k === k; })[0]; }
function a4Bytes(k){ return function(){ return fetch("f/" + k + ".png").then(function(r){ if (!r.ok) throw new Error(r.status); return r.blob(); }); }; }
