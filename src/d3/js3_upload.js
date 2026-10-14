/* ============================== script loader ============================== */
var LIBS = {
  xlsx: ["https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js", "https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"],
  pdf: ["https://cdn.jsdelivr.net/npm/pdfjs-dist@3.11.174/build/pdf.min.js", "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"],
  pdfw: ["https://cdn.jsdelivr.net/npm/pdfjs-dist@3.11.174/build/pdf.worker.min.js", "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js"]};
var LOADING = {}, LOADED_FROM = {};
function loadOne(url){
  if (LOADING[url]) return LOADING[url];
  LOADING[url] = new Promise(function(res, rej){ var s = document.createElement("script"); s.src = url; s.async = true; s.crossOrigin = "anonymous"; s.onload = function(){ res(url); }; s.onerror = function(){ delete LOADING[url]; s.remove(); rej(new Error("Không tải được thư viện đọc tệp")); }; document.head.appendChild(s); });
  return LOADING[url];
}
function loadScript(list){
  var i = 0;
  function next(){ if (i >= list.length) return Promise.reject(new Error("Không tải được thư viện đọc tệp; kiểm tra kết nối mạng.")); var u = list[i++]; return loadOne(u).then(function(){ LOADED_FROM[list[0]] = i - 1; return u; }, next); }
  return next();
}
function setSt(msg, kind){ var s = $("up-st"); s.textContent = msg || ""; s.className = "stline" + (kind ? " " + kind : ""); }

/* ============================== parsing helpers ============================== */
function parseNum(v){
  if (v == null || v === "") return 0;
  if (typeof v === "number") return isFinite(v) ? Math.round(v) : 0;
  var s = String(v).replace(/\s|đ|VND|VNĐ|vnd/g, "").replace(/[^\d,.\-()]/g, "");
  if (!s) return 0;
  var neg = /^\(.*\)$/.test(s) || s.charAt(0) === "-"; s = s.replace(/[()\-]/g, "");
  var lc = s.lastIndexOf(","), ld = s.lastIndexOf(".");
  if (lc >= 0 && ld >= 0){ if (lc > ld) s = s.replace(/\./g, "").replace(",", "."); else s = s.replace(/,/g, ""); }
  else if (lc >= 0){ s = /^\d{1,3}(,\d{3})+$/.test(s) ? s.replace(/,/g, "") : s.replace(",", "."); }
  else if (ld >= 0){ s = /^\d{1,3}(\.\d{3})+$/.test(s) ? s.replace(/\./g, "") : s; }
  var n = parseFloat(s); if (!isFinite(n)) return 0;
  return Math.round(neg ? -n : n);
}
function pad2(n){ return (n < 10 ? "0" : "") + n; }
function validYmd(y, m, d){ if (y < 100) y += 2000; if (y < 2000 || y > 2100 || m < 1 || m > 12 || d < 1 || d > 31) return ""; var dt = new Date(Date.UTC(y, m - 1, d)); if (dt.getUTCMonth() !== m - 1) return ""; return pad2(d) + "/" + pad2(m) + "/" + y; }
function parseDate(v){
  if (v == null || v === "") return "";
  if (v instanceof Date && !isNaN(v)) return validYmd(v.getFullYear(), v.getMonth() + 1, v.getDate());
  if (typeof v === "number"){ if (v > 20000 && v < 80000){ var d = new Date(Math.round((v - 25569) * 864e5)); return validYmd(d.getUTCFullYear(), d.getUTCMonth() + 1, d.getUTCDate()); } return ""; }
  var s = String(v).trim(), m;
  if ((m = s.match(/^(\d{4})-(\d{1,2})-(\d{1,2})/))) return validYmd(+m[1], +m[2], +m[3]);
  if ((m = s.match(/(\d{1,2})[\/\-.](\d{1,2})[\/\-.](\d{2,4})/))) return validYmd(+m[3], +m[2], +m[1]);
  return "";
}
function detectAcc(text){
  var t = norm(text);
  if (/116605084999/.test(t)) return "999";
  if (/6350201010476|635020101476/.test(t)) return "AGR";
  if (/117002997784/.test(t)) return "7784";
  if (/7784/.test(t)) return "7784";
  if (/AGRIBANK|(^|[^A-Z])AGR([^A-Z]|$)/.test(t)) return "AGR";
  if (/999/.test(t)) return "999";
  return "";
}
var HDR = [
  ["desc", /(NOI DUNG|DIEN GIAI|MO TA|DESCRIPTION|CHI TIET|REMARK|NARRATIVE|DETAILS|TRANSACTION CONTENT)/],
  ["cp", /(DOI UNG|TEN TK|NGUOI (HUONG|NHAN|CHUYEN)|DON VI (HUONG|NHAN|CHUYEN)|BENEFICIARY|COUNTERPARTY|PAYEE|REMITTER|TEN DOI|DOI TAC)/],
  ["bal", /(SO DU|BALANCE|DU CUOI)/],
  ["dr", /((^|[^A-Z])NO([^A-Z]|$)|DEBIT|TIEN RA|(^|[^A-Z])RUT|WITHDRAW|CHI RA|PHAT SINH NO)/],
  ["cr", /((^|[^A-Z])CO([^A-Z]|$)|CREDIT|TIEN VAO|(^|[^A-Z])NOP([^A-Z]|$)|DEPOSIT|THU VAO|PHAT SINH CO)/],
  ["date", /(^NGAY|NGAY GIAO DICH|NGAY GD|NGAY HACH TOAN|NGAY HIEU LUC|(^|[^A-Z])DATE)/],
  ["amt", /(^SO TIEN$|^AMOUNT$|SO TIEN GIAO DICH|^SO TIEN \(|TRANSACTION AMOUNT)/],
  ["type", /(^LOAI$|^TYPE$|C\/D|NO\/CO|DR\/CR|LOAI GIAO DICH)/]
];
function findHeader(aoa){
  var best = null;
  for (var r = 0; r < Math.min(aoa.length, 45); r++){
    var row = aoa[r] || [], map = {}, used = {};
    for (var c = 0; c < row.length; c++){
      var h = norm(row[c]); if (!h || h.length > 60) continue;
      for (var i = 0; i < HDR.length; i++){ var f = HDR[i][0]; if (map[f] != null || used[c]) continue; if (HDR[i][1].test(h)){ map[f] = c; used[c] = 1; break; } }
    }
    var ok = map.date != null && map.desc != null && ((map.dr != null && map.cr != null) || map.amt != null);
    if (!ok) continue;
    var score = Object.keys(map).length;
    if (!best || score > best.score) best = {row: r, map: map, score: score};
  }
  return best;
}
function parseRows(aoa, h){
  var mp = h.map, rows = [], opening = null;
  for (var r = h.row + 1; r < aoa.length; r++){
    var row = aoa[r] || []; if (!row.length) continue;
    var desc = String(row[mp.desc] == null ? "" : row[mp.desc]).trim(), nd = norm(desc);
    var d = parseDate(row[mp.date]);
    var dr = 0, cr = 0;
    if (mp.dr != null || mp.cr != null){ dr = Math.abs(parseNum(row[mp.dr])); cr = Math.abs(parseNum(row[mp.cr])); }
    if (mp.amt != null && !dr && !cr){ var a = parseNum(row[mp.amt]), ty0 = mp.type != null ? norm(row[mp.type]) : ""; if (/^(D|N|NO|DR|DEBIT)/.test(ty0) || a < 0) dr = Math.abs(a); else cr = Math.abs(a); }
    var bal = mp.bal != null && row[mp.bal] !== "" && row[mp.bal] != null ? parseNum(row[mp.bal]) : null;
    var cp = mp.cp != null ? String(row[mp.cp] == null ? "" : row[mp.cp]).trim() : "";
    if (/SO DU DAU/.test(nd) || /OPENING BALANCE/.test(nd)){ if (bal != null) opening = bal; else if (dr || cr) opening = cr - dr; continue; }
    if (!d){
      if (/(TONG CONG|CONG PHAT SINH|SO DU CUOI|TONG SO|TOTAL|CLOSING)/.test(nd)) continue;
      if (desc && rows.length && !dr && !cr && bal == null){ rows[rows.length - 1].s += " " + desc; continue; }
      continue;
    }
    if (!dr && !cr && !desc) continue;
    rows.push({d: d, s: desc, dr: dr, cr: cr, b: bal, cp: cp});
  }
  return {rows: rows, opening: opening};
}

/* ============================== Excel / CSV ============================== */
function readSheet(f){
  setSt("Đang đọc " + f.name + "…");
  var isCsv = /\.csv$/i.test(f.name);
  return loadScript(LIBS.xlsx).then(function(){ return isCsv ? f.text() : f.arrayBuffer(); }).then(function(buf){
    var wb;
    if (isCsv){ var first = String(buf).split(/\r?\n/)[0] || ""; var fs = (first.split(";").length > first.split(",").length) ? ";" : (first.split("\t").length > first.split(",").length ? "\t" : ","); wb = window.XLSX.read(String(buf).replace(/^\ufeff/, ""), {type: "string", raw: true, FS: fs}); }
    else wb = window.XLSX.read(buf, {type: "array", cellDates: false, raw: false});
    var best = null;
    wb.SheetNames.forEach(function(n){
      var aoa = window.XLSX.utils.sheet_to_json(wb.Sheets[n], {header: 1, raw: true, defval: ""});
      var h = findHeader(aoa);
      if (h){ var pr = parseRows(aoa, h); if (pr.rows.length && (!best || pr.rows.length > best.pr.rows.length)) best = {n: n, aoa: aoa, h: h, pr: pr}; }
    });
    if (!best){ setSt("Không tìm thấy bảng giao dịch trong tệp. Tệp cần có các cột Ngày, Nội dung, Tiền ra (Nợ), Tiền vào (Có), nên có Số dư.", "err"); return; }
    var head = best.aoa.slice(0, best.h.row).map(function(r){ return r.join(" "); }).join(" ");
    var acc = $("up-acc").value || detectAcc(f.name + " " + best.n + " " + head);
    openDraft({acc: acc, src: /\.csv$/i.test(f.name) ? "CSV" : "Excel", file: f.name, sheet: best.n, rows: best.pr.rows, opening: best.pr.opening});
    setSt("Đã đọc " + best.pr.rows.length + " dòng từ sheet \"" + best.n + "\". Kiểm tra bảng bên dưới trước khi áp dụng.", "ok");
  }).catch(function(e){ setSt("Không đọc được tệp: " + (e && e.message ? e.message : e), "err"); });
}

/* ============================== PDF (Claude reads) ============================== */
var PDF_CTL = null;
function pdfPrompt(kind, pages, text){
  var head = "Bạn là trợ lý chép số liệu sao kê ngân hàng tiếng Việt, cẩn thận từng chữ số.\n" +
    (kind === "text" ? "Dưới đây là văn bản trích từ trang " + pages + " của một sao kê tài khoản ngân hàng.\n\n" + text + "\n\n" : "Các ảnh đính kèm là các phần liên tiếp từ trên xuống dưới của trang " + pages + " trong một sao kê tài khoản ngân hàng; hai phần liền nhau có một dải chồng lấn nhỏ, dòng nằm trong dải chồng lấn chỉ chép một lần.\n\n");
  return head + "Hãy chép TẤT CẢ các dòng giao dịch theo đúng thứ tự, giữ nguyên nội dung, không bỏ sót, không suy đoán. Không chép dòng tổng cộng, dòng tiêu đề.\n" +
    "Trả về DUY NHẤT một đối tượng JSON dạng:\n" +
    '{"so_tai_khoan":"", "ngan_hang":"", "tu_ngay":"dd/mm/yyyy", "den_ngay":"dd/mm/yyyy", "so_du_dau_ky": null, "so_du_cuoi_ky": null, "giao_dich":[{"ngay":"dd/mm/yyyy","noi_dung":"","ghi_no":0,"ghi_co":0,"so_du":null,"doi_ung":""}]}\n' +
    "Quy tắc: số tiền là số nguyên đồng, không có dấu phân cách; ghi_no là tiền ra khỏi tài khoản, ghi_co là tiền vào (0 nếu không có); so_du là số dư in trên dòng đó, null nếu không in; doi_ung là tên hoặc số tài khoản đối ứng nếu có; thông tin không có thì để chuỗi rỗng hoặc null.";
}
function itemsToLines(items){
  var rows = [];
  items.forEach(function(it){ if (!it.str || !it.str.trim()) return; var y = Math.round(it.transform[5]), x = it.transform[4]; var r = null; for (var i = 0; i < rows.length; i++){ if (Math.abs(rows[i].y - y) <= 2){ r = rows[i]; break; } } if (!r){ r = {y: y, it: []}; rows.push(r); } r.it.push({x: x, s: it.str, w: it.width || 0}); });
  rows.sort(function(a, b){ return b.y - a.y; });
  return rows.map(function(r){ r.it.sort(function(a, b){ return a.x - b.x; }); var out = "", ex = null; r.it.forEach(function(t){ if (ex != null && t.x - ex > 12) out += " | "; else if (out) out += " "; out += t.s; ex = t.x + t.w; }); return out; }).join("\n");
}
function renderSlices(pdf, pn){
  return pdf.getPage(pn).then(function(page){
    var vp0 = page.getViewport({scale: 1}), scale = 1500 / vp0.width, vp = page.getViewport({scale: scale});
    var cv = document.createElement("canvas"); cv.width = Math.round(vp.width); cv.height = Math.round(vp.height);
    var ctx = cv.getContext("2d"); ctx.fillStyle = "#fff"; ctx.fillRect(0, 0, cv.width, cv.height);
    return page.render({canvasContext: ctx, viewport: vp}).promise.then(function(){
      var H = cv.height, n = Math.max(2, Math.ceil(H / 800)), h = Math.ceil(H / n), ov = 60, jobs = [];
      for (var i = 0; i < n; i++){
        (function(i){
          var y0 = Math.max(0, i * h - ov), y1 = Math.min(H, (i + 1) * h + ov), c2 = document.createElement("canvas"); c2.width = cv.width; c2.height = y1 - y0;
          c2.getContext("2d").drawImage(cv, 0, y0, cv.width, y1 - y0, 0, 0, cv.width, y1 - y0);
          jobs.push(new Promise(function(res){ c2.toBlob(function(b){ res(b); }, "image/jpeg", 0.9); }));
        })(i);
      }
      return Promise.all(jobs);
    });
  });
}
function mergePdfResults(parts){
  var rows = [], meta = {acc: "", opening: null, bank: ""};
  parts.forEach(function(res){
    if (!res || typeof res !== "object") return;
    if (!meta.acc && res.so_tai_khoan) meta.acc = detectAcc(String(res.so_tai_khoan));
    if (meta.opening == null && res.so_du_dau_ky != null && res.so_du_dau_ky !== "") meta.opening = parseNum(res.so_du_dau_ky);
    if (!meta.bank && res.ngan_hang) meta.bank = String(res.ngan_hang);
    (Array.isArray(res.giao_dich) ? res.giao_dich : []).forEach(function(g){
      var d = parseDate(g.ngay); if (!d) return;
      var r = {d: d, s: String(g.noi_dung || "").trim(), dr: Math.abs(parseNum(g.ghi_no)), cr: Math.abs(parseNum(g.ghi_co)), b: g.so_du == null || g.so_du === "" ? null : parseNum(g.so_du), cp: String(g.doi_ung || "").trim()};
      var p = rows[rows.length - 1];
      if (p && p.d === r.d && p.dr === r.dr && p.cr === r.cr && p.b === r.b && p.s === r.s) return;
      rows.push(r);
    });
  });
  return {rows: rows, meta: meta};
}
function sampleErr(e){
  var c = e && e.code;
  if (c === "cancelled") return "Đã dừng.";
  if (c === "not_granted" || c === "sampling_disabled" || c === "not_declared" || c === "capability_disabled" || c === "capability_removed") return "Chế độ xem này không dùng được Claude để đọc PDF. Hãy dùng tệp Excel, CSV hoặc nhập tay.";
  if (c === "images_unavailable") return "Chế độ xem này không gửi được ảnh cho Claude. Hãy dùng tệp Excel, CSV hoặc nhập tay.";
  if (c === "rate_limited") return "Đã dùng hết lượt Claude trong lúc này; thử lại sau ít phút.";
  if (c === "invalid_json") return "Claude trả về không đúng định dạng; hãy thử lại.";
  if (c === "prompt_too_large") return "Tệp quá dài; hãy tách sao kê thành từng kỳ ngắn hơn.";
  if (c === "session_expired") return "Phiên đăng nhập đã hết hạn; hãy đăng nhập lại.";
  return "Không đọc được PDF (" + (c || "lỗi") + ").";
}
function readPdf(f){
  if (!CAP.sample){ setSt(CAP.mode === "local" ? "Tệp PDF được Claude đọc giúp nên chỉ dùng được khi mở trang trên Claude. Ở bản lưu trên máy, hãy dùng Excel, CSV hoặc nhập tay." : "Chế độ xem này không dùng được Claude để đọc PDF. Hãy dùng Excel, CSV hoặc nhập tay.", "err"); return Promise.resolve(); }
  PDF_CTL = new AbortController(); $("up-stop").hidden = false;
  setSt("Đang mở " + f.name + "…");
  var pdfDoc = null, lim = null;
  return loadScript(LIBS.pdf).then(function(){
    window.pdfjsLib.GlobalWorkerOptions.workerSrc = LIBS.pdfw[LOADED_FROM[LIBS.pdf[0]] || 0];
    return f.arrayBuffer();
  }).then(function(buf){ return window.pdfjsLib.getDocument({data: new Uint8Array(buf), isEvalSupported: false}).promise; })
  .then(function(pdf){
    pdfDoc = pdf;
    if (pdf.numPages > 12) throw {code: "too_many", n: pdf.numPages};
    return CAP.sample.limits().catch(function(){ return null; });
  }).then(function(l){
    lim = l; var texts = [], p = Promise.resolve();
    for (var i = 1; i <= pdfDoc.numPages; i++){ (function(i){ p = p.then(function(){ return pdfDoc.getPage(i).then(function(pg){ return pg.getTextContent(); }).then(function(tc){ texts[i - 1] = itemsToLines(tc.items); }); }); })(i); }
    return p.then(function(){ return texts; });
  }).then(function(texts){
    var chars = texts.join("").replace(/\s/g, "").length, calls = [];
    if (chars > 250 * pdfDoc.numPages){
      var cur = [], curLen = 0, maxB = Math.min(52000, (lim && lim.maxPromptBytes ? lim.maxPromptBytes : 65536) - 4000);
      texts.forEach(function(t, i){ var b = new Blob([t]).size; if (cur.length && curLen + b > maxB){ calls.push({kind: "text", pages: cur.slice()}); cur = []; curLen = 0; } cur.push(i + 1); curLen += b; });
      if (cur.length) calls.push({kind: "text", pages: cur});
      calls.forEach(function(c){ c.text = c.pages.map(function(pn){ return "=== Trang " + pn + " ===\n" + texts[pn - 1]; }).join("\n\n"); });
      return {calls: calls, mode: "text"};
    }
    if (!lim || !lim.images) throw {code: "images_unavailable"};
    var maxImg = Math.max(1, Math.min(lim.images.maxCount || 4, 8)), q = Promise.resolve(), slices = [];
    for (var i = 1; i <= pdfDoc.numPages; i++){ (function(i){ q = q.then(function(){ setSt("Đang chuẩn bị ảnh trang " + i + "/" + pdfDoc.numPages + "…"); return renderSlices(pdfDoc, i).then(function(bl){ bl.forEach(function(b){ slices.push({p: i, b: b}); }); }); }); })(i); }
    return q.then(function(){
      var cur = [];
      slices.forEach(function(s){ if (cur.length >= maxImg){ calls.push({kind: "img", imgs: cur}); cur = []; } cur.push(s); });
      if (cur.length) calls.push({kind: "img", imgs: cur});
      return {calls: calls, mode: "img"};
    });
  }).then(function(plan){
    var results = [], chain = Promise.resolve();
    plan.calls.forEach(function(c, k){
      chain = chain.then(function(){
        setSt("Claude đang đọc phần " + (k + 1) + "/" + plan.calls.length + (plan.mode === "img" ? " (ảnh scan)" : "") + "… thường mất 20–90 giây mỗi phần.");
        var pages = c.kind === "text" ? c.pages.join(", ") : c.imgs.map(function(x){ return x.p; }).filter(function(v, i, a){ return a.indexOf(v) === i; }).join(", ");
        var opts = {signal: PDF_CTL.signal, modelTier: "default"};
        if (c.kind === "img") opts.images = c.imgs.map(function(x){ return x.b; });
        return CAP.sample.json(pdfPrompt(c.kind, pages, c.text), opts).then(function(r){ results.push(r); });
      });
    });
    return chain.then(function(){ return results; });
  }).then(function(results){
    var mg = mergePdfResults(results);
    if (!mg.rows.length){ setSt("Claude không tìm thấy dòng giao dịch nào trong tệp. Hãy kiểm tra tệp hoặc nhập tay.", "err"); return; }
    var acc = $("up-acc").value || mg.meta.acc || detectAcc(f.name);
    openDraft({acc: acc, src: "PDF", file: f.name, rows: mg.rows, opening: mg.meta.opening});
    setSt("Claude đã chép " + mg.rows.length + " dòng. Hãy đối chiếu với tệp gốc, nhất là các dòng báo lệch số dư, rồi áp dụng.", "ok");
  }).catch(function(e){
    if (e && e.code === "too_many") setSt("PDF dài " + e.n + " trang; hãy tách thành từng kỳ sao kê tối đa 12 trang.", "err");
    else if (e && e.code) setSt(sampleErr(e), e.code === "cancelled" ? "" : "err");
    else setSt("Không đọc được PDF: " + (e && e.message ? e.message : e), "err");
  }).then(function(){ $("up-stop").hidden = true; PDF_CTL = null; });
}
function handleFile(f){
  if (!f) return;
  if (f.size > 25 * 1024 * 1024){ setSt("Tệp lớn hơn 25 MB; hãy tách nhỏ.", "err"); return; }
  var ext = (f.name.split(".").pop() || "").toLowerCase();
  if (ext === "pdf") return readPdf(f);
  if (ext === "xlsx" || ext === "xls" || ext === "csv") return readSheet(f);
  setSt("Chỉ nhận tệp Excel (.xlsx, .xls), CSV hoặc PDF.", "err");
}

/* ============================== draft: validate, preview, apply ============================== */
var DRAFT = null;
function existingRows(acc){ return M.all.filter(function(t){ return t.a === acc; }); }
function validateDraft(){
  var d = DRAFT; if (!d) return;
  var acc = d.acc, ex = acc ? existingRows(acc) : [], keys = {};
  ex.forEach(function(t){ keys[t.k + "|" + t.dr + "|" + t.cr + "|" + t.b] = 1; });
  var firstK = "";
  d.rows.forEach(function(r){ var k = dkey(r.d); if (k && (!firstK || k < firstK)) firstK = k; });
  var prev = null; ex.forEach(function(t){ if (!firstK || t.k <= firstK) prev = t; });
  var run = d.opening != null ? d.opening : (prev ? prev.b : null);
  var res = {n: 0, dup: 0, bad: 0, nodate: 0, filled: 0, dr: 0, cr: 0, flags: {"Đỏ": 0, "Cam": 0, "Vàng": 0, "Xanh": 0}, cont: null, prevB: prev ? prev.b : null, prevD: prev ? prev.d : "", gaps: []};
  if (d.opening != null && prev) res.cont = Math.abs(d.opening - prev.b) <= 1;
  d.rows.forEach(function(r){
    r._k = dkey(r.d); r._dup = false; r._bad = null; r._calc = false;
    if (!r._k){ res.nodate++; r._bad = "Ngày không hợp lệ"; }
    var key = r._k + "|" + (+r.dr || 0) + "|" + (+r.cr || 0) + "|" + r.b;
    if (r.b != null && keys[key]){ r._dup = true; res.dup++; return; }
    var cl = acc ? classify(acc, r) : {c: "", v: "", n: ""}; r._c = cl;
    if (cl.v) res.flags[cl.v]++;
    var exp = run == null ? null : run + (+r.cr || 0) - (+r.dr || 0);
    if (r.b == null){ if (exp != null){ r._exp = exp; r._calc = true; } }
    else if (exp != null && Math.abs(exp - r.b) > 1){ r._bad = "Lệch " + vnd(r.b - exp) + " đồng so với số dư tính lại"; res.bad++; }
    run = r.b != null ? r.b : exp;
    res.n++; res.dr += +r.dr || 0; res.cr += +r.cr || 0;
  });
  if (res.cont == null && prev && d.rows.length){ var f0 = d.rows.filter(function(r){ return !r._dup; })[0]; if (f0 && f0.b != null) res.cont = Math.abs(prev.b + (+f0.cr || 0) - (+f0.dr || 0) - f0.b) <= 1; }
  if (prev && firstK && (acc === "999" || acc === "7784")){
    var y = +prev.k.slice(0, 4), mo = +prev.k.slice(4, 6), fy = +firstK.slice(0, 4), fm = +firstK.slice(4, 6);
    var cnt = 0; while ((y < fy || (y === fy && mo < fm - 1)) && cnt < 36){ mo++; if (mo > 12){ mo = 1; y++; } if (y < fy || (y === fy && mo < fm)) res.gaps.push(pad2(mo) + "/" + y); cnt++; }
  }
  res.closing = run;
  d.res = res;
}
function draftOk(){ return DRAFT && DRAFT.acc && DRAFT.res && DRAFT.res.n > 0 && !DRAFT.res.nodate; }
function openDraft(d){
  DRAFT = {acc: d.acc || "", src: d.src, file: d.file || "", sheet: d.sheet || "", rows: d.rows.map(function(r){ return {d: r.d, s: r.s || "", dr: +r.dr || 0, cr: +r.cr || 0, b: r.b == null ? null : +r.b, cp: r.cp || ""}; }), opening: d.opening == null ? null : +d.opening};
  validateDraft(); renderPreview();
  $("pv").hidden = false;
  try { $("pv").scrollIntoView({behavior: "smooth", block: "start"}); } catch (e) {}
}
function pvSummary(){
  var d = DRAFT, r = d.res, pills = [];
  pills.push('<label class="pill sev-ok" style="gap:6px">Tài khoản <select id="pv-acc" style="font:inherit;font-size:12px;border:0;background:transparent;color:inherit"><option value="">Chọn</option>' + ["999", "AGR", "7784"].map(function(a){ return '<option value="' + a + '"' + (d.acc === a ? " selected" : "") + ">" + ACCL[a] + "</option>"; }).join("") + "</select></label>");
  pills.push('<span class="pill tone-n"><i class="dot"></i>' + r.n + " dòng" + (r.dup ? ", bỏ " + r.dup + " dòng trùng dữ liệu đã có" : "") + "</span>");
  pills.push('<span class="pill tone-n"><i class="dot"></i>Ra ' + money(r.dr) + " · vào " + money(r.cr) + "</span>");
  if (r.prevB != null) pills.push('<span class="pill ' + (r.cont === false ? "sev-Cam" : "sev-ok") + '"><i class="dot"></i>' + (r.cont === false ? "Không nối được số dư cuối cũ " + vnd(r.prevB) + " (" + r.prevD + ")" : "Nối liền số dư cuối cũ " + vnd(r.prevB) + " (" + r.prevD + ")") + "</span>");
  pills.push('<span class="pill ' + (r.bad ? "sev-Đỏ" : "sev-ok") + '"><i class="dot"></i>' + (r.bad ? r.bad + " dòng lệch số dư" : "Số dư từng dòng khớp") + "</span>");
  if (r.nodate) pills.push('<span class="pill sev-Đỏ"><i class="dot"></i>' + r.nodate + " dòng thiếu ngày</span>");
  if (r.gaps.length) pills.push('<span class="pill sev-Cam"><i class="dot"></i>Không có dữ liệu tháng ' + r.gaps.join(", ") + "</span>");
  var fl = r.flags["Đỏ"] + r.flags["Cam"] + r.flags["Vàng"];
  pills.push('<span class="pill ' + (r.flags["Đỏ"] ? "sev-Đỏ" : fl ? "sev-Cam" : "sev-ok") + '"><i class="dot"></i>Cảnh báo: ' + r.flags["Đỏ"] + " Đỏ, " + r.flags["Cam"] + " Cam, " + r.flags["Vàng"] + " Vàng</span>");
  $("pv-sum").innerHTML = pills.join("");
  $("pv-sub").textContent = "Nguồn: " + d.src + (d.file ? " · " + d.file : "") + (d.sheet ? " · sheet " + d.sheet : "") + (d.opening != null ? " · số dư đầu kỳ in trên tệp " + vnd(d.opening) : "") + ". Sửa trực tiếp trong bảng nếu cần; số dư lệch được tô đỏ.";
  $("pv-apply").disabled = !draftOk();
  $("pv-apply").title = draftOk() ? "" : (!d.acc ? "Chọn tài khoản trước" : "Cần ít nhất một dòng hợp lệ");
}
function pvRow(r, i){
  var c = r._c || {c: "", v: "", n: ""};
  var ck = r._dup ? '<span class="pill tone-n">Trùng, bỏ qua</span>' : r._bad ? '<span class="pill sev-Đỏ" title="' + esc(r._bad) + '">' + esc(r._bad.length > 26 ? "Lệch số dư" : r._bad) + "</span>" : r._calc ? '<span class="pill sev-Vàng">Tự tính</span>' : '<span class="pill sev-ok">Khớp</span>';
  return '<tr class="' + (r._dup ? "dup" : r._bad ? "bad" : "") + '" data-i="' + i + '"><td class="num" style="color:var(--muted);font-size:12px">' + (i + 1) + '</td><td class="w-d"><input data-f="d" value="' + esc(r.d) + '" aria-label="Ngày dòng ' + (i + 1) + '"></td><td class="w-s"><input data-f="s" value="' + esc(r.s) + '" aria-label="Nội dung dòng ' + (i + 1) + '"></td><td class="w-n"><input class="n" data-f="dr" value="' + (r.dr ? vnd(r.dr) : "") + '" inputmode="numeric" aria-label="Tiền ra dòng ' + (i + 1) + '"></td><td class="w-n"><input class="n" data-f="cr" value="' + (r.cr ? vnd(r.cr) : "") + '" inputmode="numeric" aria-label="Tiền vào dòng ' + (i + 1) + '"></td><td class="w-n"><input class="n" data-f="b" value="' + (r.b != null ? vnd(r.b) : "") + '" placeholder="' + (r._exp != null ? vnd(r._exp) : "") + '" inputmode="numeric" aria-label="Số dư dòng ' + (i + 1) + '"></td><td class="w-cp"><input data-f="cp" value="' + esc(r.cp) + '" aria-label="Đối ứng dòng ' + (i + 1) + '"></td><td class="cls">' + esc(c.c) + (c.v ? '<div style="margin-top:3px"><span class="pill sev-' + c.v + '" title="' + esc(c.n) + '"><i class="dot"></i>' + c.v + "</span></div>" : "") + '</td><td class="ckc">' + ck + '</td><td><button class="xb" type="button" data-del="' + i + '" aria-label="Xóa dòng ' + (i + 1) + '">×</button></td></tr>';
}
function renderPreview(){
  if (!DRAFT){ $("pv").hidden = true; return; }
  pvSummary();
  $("pv-body").innerHTML = DRAFT.rows.map(pvRow).join("");
}
function refreshPreview(){
  var ae = document.activeElement, keep = null;
  if (ae && ae.closest && ae.closest("#pv-body")){ var tr0 = ae.closest("tr"); keep = {i: tr0 && tr0.getAttribute("data-i"), f: ae.getAttribute("data-f")}; }
  validateDraft(); renderPreview();
  if (keep && keep.i != null){ var n = document.querySelector('#pv-body tr[data-i="' + keep.i + '"] input[data-f="' + keep.f + '"]'); if (n) n.focus(); }
}
function applyDraft(){
  if (!draftOk()) return;
  var d = DRAFT, r = d.res;
  var rows = d.rows.filter(function(x){ return !x._dup && x._k; }).map(function(x){ return {d: x.d, s: x.s, dr: +x.dr || 0, cr: +x.cr || 0, b: x.b != null ? x.b : (x._exp != null ? x._exp : null), cp: x.cp}; });
  var b = {id: uid(), acc: d.acc, src: d.src, file: d.file, at: nowIso(), opening: d.opening, rows: rows, chk: {bad: r.bad, dup: r.dup, cont: r.cont, gaps: r.gaps}};
  U.batches.push(b); DIRTY.batches = true;
  DRAFT = null; $("pv").hidden = true; $("pv-body").innerHTML = "";
  afterChange();
  toast("Đã áp dụng " + rows.length + " giao dịch mới vào báo cáo" + (CAP.mode === "writer" ? ". Bấm Lưu để mọi người cùng thấy." : "."));
  try { $("upd-banner").scrollIntoView({behavior: "smooth", block: "start"}); } catch (e) {}
}
function addManual(){
  var acc = $("m-acc").value, dv = $("m-d").value, s = $("m-s").value.trim(), dr = Math.abs(parseNum($("m-dr").value)), cr = Math.abs(parseNum($("m-cr").value)), bv = $("m-b").value.trim(), cp = $("m-cp").value.trim();
  var d = parseDate(dv);
  if (!d){ setSt("Nhập ngày giao dịch.", "err"); return; }
  if (!dr && !cr){ setSt("Nhập số tiền ra hoặc tiền vào.", "err"); return; }
  if (dr && cr){ setSt("Mỗi dòng chỉ có tiền ra hoặc tiền vào.", "err"); return; }
  var row = {d: d, s: s, dr: dr, cr: cr, b: bv ? parseNum(bv) : null, cp: cp};
  if (DRAFT && DRAFT.src === "Nhập tay" && DRAFT.acc === acc) DRAFT.rows.push(row);
  else openDraft({acc: acc, src: "Nhập tay", file: "", rows: [row], opening: null});
  DRAFT.rows.sort(function(a, b){ var ka = dkey(a.d), kb = dkey(b.d); return ka < kb ? -1 : ka > kb ? 1 : 0; });
  refreshPreview(); $("pv").hidden = false;
  ["m-s", "m-dr", "m-cr", "m-b", "m-cp"].forEach(function(id){ $(id).value = ""; });
  setSt("Đã thêm dòng " + d + " vào bảng kiểm tra.", "ok");
}

/* ============================== batches list ============================== */
function renderBatches(){
  var list = U.batches;
  $("bl-sub").textContent = list.length ? "Mỗi đợt có thể gỡ bỏ; số liệu và biểu đồ tính lại ngay." : "Chưa có dữ liệu mới. Báo cáo đang dùng 8 sao kê gốc tới 31/05/2026.";
  $("bl").innerHTML = list.map(function(b){
    var st = batchStats(b), saved = !!SAVED_BIDS[b.id];
    var fl = {"Đỏ": 0, "Cam": 0, "Vàng": 0}; b.rows.forEach(function(r){ var c = classify(b.acc, r); if (fl[c.v] != null) fl[c.v]++; });
    return '<div class="b"><div><div><span class="acc">' + b.acc + "</span> <b>" + ACCL[b.acc] + "</b> · " + st.from + " – " + st.to + " · " + b.rows.length + ' dòng</div><div class="m">' + esc(b.src) + (b.file ? " · " + esc(b.file) : "") + " · nạp " + fmtIso(b.at) + '</div><div class="pls">' + (b.rm ? '<span class="pill sev-Cam"><i class="dot"></i>Sẽ gỡ khi lưu</span>' : checkPill(b)) + '<span class="pill ' + (saved ? "sev-ok" : "sev-Vàng") + '"><i class="dot"></i>' + (saved ? (CAP.mode === "local" ? "Đã lưu trên máy này" : "Đã lưu cho mọi người") : "Chưa lưu") + "</span>" + (fl["Đỏ"] + fl["Cam"] + fl["Vàng"] ? '<span class="pill sev-' + (fl["Đỏ"] ? "Đỏ" : fl["Cam"] ? "Cam" : "Vàng") + '"><i class="dot"></i>' + fl["Đỏ"] + " Đỏ, " + fl["Cam"] + " Cam, " + fl["Vàng"] + " Vàng</span>" : "") + "</div></div>" +
      '<div>' + (b.rm ? '<button class="tbtn" type="button" data-undo="' + b.id + '">Giữ lại</button>' : (saved && !canWrite() ? "" : '<button class="tbtn dng" type="button" data-rmb="' + b.id + '">Gỡ</button>')) + "</div></div>";
  }).join("");
  var acts = [];
  if (M.hasNew && CAP.sample) acts.push('<button class="tbtn pri" type="button" id="ai-run">Nhờ Claude đánh giá dữ liệu mới</button>');
  if (M.hasNew && !CAP.sample && CAP.mode !== "init") acts.push('<span class="subx">Đánh giá bằng Claude chỉ có khi mở trang trên Claude.</span>');
  $("bl-acts").innerHTML = acts.join("");
  renderAI();
}
function removeBatch(id){
  var b = U.batches.filter(function(x){ return x.id === id; })[0]; if (!b) return;
  if (SAVED_BIDS[b.id]) b.rm = true; else U.batches = U.batches.filter(function(x){ return x.id !== id; });
  DIRTY.batches = true; afterChange();
}

/* ============================== Claude assessment ============================== */
var AI_CTL = null;
function aiContext(){
  var V = D.verdict, B = D.base, g = M.g, lines = [];
  lines.push("BỐI CẢNH: phân tích sao kê quỹ bảo trì chung cư Nam Sài Gòn Residences, dữ liệu gốc 15/08/2024 – 31/05/2026.");
  lines.push("Kết luận gốc: " + V.answer);
  V.tiers[0].items.forEach(function(it){ lines.push("- Đã rõ: " + it.h + " (" + it.amt + ", " + it.rule + ")."); });
  V.tiers[1].items.forEach(function(it){ lines.push("- Nghi vấn: " + it.h + "."); });
  lines.push("Quy định chính: Quy chế Điều 7.2, 7.4 (tiền quỹ chỉ chuyển thẳng tới đơn vị thực hiện bảo trì; tạm dùng tiền vận hành tối đa 10 triệu mỗi tháng); Điều 6.1, 6.3 (đơn vị đủ năng lực, 3 báo giá, nghiệm thu trước khi thanh toán); Điều 9.2 (sửa chữa đột xuất tối đa 500 triệu mỗi năm); Điều 3.1.a (một tài khoản quỹ, công khai); khoản 4 Điều 153 Luật Nhà ở 2023 (thu khai thác phần sở hữu chung phải nộp vào tài khoản kinh phí bảo trì).");
  if (D.lg) lines.push("KHUNG HỆ QUẢ PHÁP LÝ (dùng chung với báo cáo): " + D.lg.ladder.map(function(x){ return x.name + ": " + x.lines.join(" "); }).join(" ") + " " + D.lg.bai_end);
  lines.push("Tài khoản: 999 = VietinBank 116605084999 (quỹ); AGR = Agribank 6350201010476 (quỹ); 7784 = VietinBank 117002997784 (thu dịch vụ khu vực chung); 118002976372 = tài khoản vận hành của Ban quản trị.");
  lines.push("");
  lines.push("SỐ LIỆU TRƯỚC VÀ SAU KHI THÊM DỮ LIỆU MỚI (đồng): quỹ còn " + vnd(B.fund_end) + " thành " + vnd(M.fund_end) + "; lãi " + vnd(B.interest) + " thành " + vnd(M.interest) + "; chi khỏi quỹ " + vnd(B.spend) + " thành " + vnd(M.spend) + "; thu khu vực chung ngoài quỹ " + vnd(B.ca_total) + " thành " + vnd(M.ca_total) + "; chi từ TK 7784 " + vnd(B.repair7784) + " thành " + vnd(M.repair7784) + ".");
  lines.push("KIỂM TRA DỮ LIỆU MỚI: " + U.batches.filter(function(b){ return !b.rm; }).map(function(b){ var st = batchStats(b), c = b.chk || {}; return b.acc + " " + st.from + "–" + st.to + ": " + b.rows.length + " dòng, " + (c.bad ? c.bad + " dòng lệch số dư" : "số dư khớp") + (c.cont === false ? ", không nối số dư cũ" : "") + (c.gaps && c.gaps.length ? ", thiếu tháng " + c.gaps.join(" ") : ""); }).join("; ") + ".");
  if (M.ic.length) lines.push("Lãi không kỳ hạn tính lại: " + M.ic.map(function(x){ return x.a + " " + x.m + (Math.abs(x.diff) <= 1 ? " khớp" : " lệch " + x.diff); }).join("; ") + ".");
  if (Math.abs(M.recon) > 1000) lines.push("Đối chiếu tiền gửi có kỳ hạn + số dư thanh toán với số quỹ theo giao dịch: lệch " + vnd(M.recon) + ".");
  if (g.tdOpen.length || g.tdClose.length) lines.push("Sự kiện tiền gửi: " + g.tdOpen.map(function(t){ return t.d + " gửi " + vnd(t.v) + " (" + t.a + ")"; }).concat(g.tdClose.map(function(t){ return t.d + " tất toán gốc " + vnd(t.v) + " lãi " + vnd(t.i); })).join("; ") + ".");
  lines.push("");
  lines.push("GIAO DỊCH MỚI (ngày | TK | tiền ra | tiền vào | số dư | nội dung | đối ứng | phân loại tự động | cảnh báo tự động):");
  var rows = M.nw.slice(), small = 0, smallSum = 0;
  if (rows.length > 260){ rows = rows.filter(function(t){ if (WARN[t.v] || (t.dr + t.cr) >= 1e6) return true; small++; smallSum += t.cr - t.dr; return false; }); }
  rows.slice(0, 320).forEach(function(t){ lines.push(t.d + " | " + t.a + " | " + (t.dr || "") + " | " + (t.cr || "") + " | " + t.b + " | " + t.s.slice(0, 160) + " | " + t.cp.slice(0, 80) + " | " + t.c + " | " + (t.v ? t.v + ": " + t.n : "")); });
  if (small) lines.push("(Thêm " + small + " giao dịch nhỏ dưới 1 triệu, ròng " + vnd(smallSum) + " đồng, không liệt kê.)");
  var s = lines.join("\n");
  while (new Blob([s]).size > 56000 && lines.length > 20){ lines.splice(lines.length - 2, 1); s = lines.join("\n"); }
  return s;
}
function aiPrompt(){
  return "Bạn là chuyên gia kiểm soát tài chính nhà chung cư tại Việt Nam, viết cho cư dân, giọng khách quan, không suy diễn quá dữ liệu.\n" +
    "Dựa trên bối cảnh và dữ liệu sao kê mới dưới đây, hãy đánh giá dữ liệu mới có làm thay đổi kết luận gốc không, và chỉ ra các giao dịch cần Ban quản trị giải trình.\n\n" + aiContext() + "\n\n" +
    "Trả về DUY NHẤT một đối tượng JSON dạng:\n" +
    '{"tom_tat":"2-3 câu", "anh_huong":"dữ liệu mới làm kết luận gốc nặng hơn, giữ nguyên hay nhẹ hơn, và vì sao, 1-2 câu", "muc_do":"Nặng hơn|Giữ nguyên|Nhẹ hơn", "diem":[{"ngay":"dd/mm/yyyy","tk":"999|AGR|7784","so_tien":0,"noi_dung":"","muc":"Đỏ|Cam|Vàng|Xanh","ly_do":"","can_cu":""}], "ho_so":["hồ sơ cần yêu cầu thêm"], "luu_y_du_lieu":"nhận xét về độ đầy đủ, độ tin cậy của dữ liệu mới"}\n' +
    "Tối đa 12 điểm, xếp từ nghiêm trọng nhất. Mức Xanh dùng cho việc làm đúng hoặc khắc phục. Với điểm đã rõ trên sao kê, ly_do nêu hệ quả theo khung (phải khắc phục, thuộc diện phạt, căn cứ bãi nhiệm); với điểm cần chứng từ, nêu có chứng từ hợp lệ thì khép lại, không có thì phải bồi hoàn quỹ; không kết luận thay cơ quan có thẩm quyền. Viết tiếng Việt có dấu, câu ngắn, không dùng ký hiệu mũi tên.";
}
function cleanAI(r){
  if (!r || typeof r !== "object") return null;
  var S = function(x, n){ return String(x == null ? "" : x).slice(0, n || 600); };
  var MUC = {"Đỏ": 1, "Cam": 1, "Vàng": 1, "Xanh": 1};
  return {tom_tat: S(r.tom_tat, 900), anh_huong: S(r.anh_huong, 700), muc_do: ["Nặng hơn", "Giữ nguyên", "Nhẹ hơn"].indexOf(r.muc_do) >= 0 ? r.muc_do : "Giữ nguyên",
    diem: (Array.isArray(r.diem) ? r.diem : []).slice(0, 12).map(function(p){ return {ngay: S(p.ngay, 12), tk: S(p.tk, 8), so_tien: parseNum(p.so_tien), noi_dung: S(p.noi_dung, 240), muc: MUC[p.muc] ? p.muc : "Vàng", ly_do: S(p.ly_do, 400), can_cu: S(p.can_cu, 160)}; }),
    ho_so: (Array.isArray(r.ho_so) ? r.ho_so : []).slice(0, 8).map(function(x){ return S(x, 240); }), luu_y_du_lieu: S(r.luu_y_du_lieu, 500)};
}
function runAI(){
  if (!CAP.sample || AI_CTL) return;
  AI_CTL = new AbortController();
  var box = $("aibox"); box.hidden = false;
  box.innerHTML = '<h4>Claude đang đánh giá dữ liệu mới…</h4><p class="ai-p subx">Thường mất 30–90 giây. Lượt dùng tính vào tài khoản Claude của bạn.</p><div class="acts"><button class="tbtn dng" type="button" id="ai-stop">Dừng</button></div>';
  CAP.sample.json(aiPrompt(), {signal: AI_CTL.signal, modelTier: "default"}).then(function(r){
    var c = cleanAI(r); if (!c){ throw {code: "invalid_json"}; }
    AI_CTL = null;
    U.ai = {at: nowIso(), basis: U.batches.filter(function(b){ return !b.rm; }).map(function(b){ return b.id; }), r: c};
    DIRTY.ai = true; afterChange();
  }).catch(function(e){
    AI_CTL = null;
    box.innerHTML = '<h4>Chưa đánh giá được</h4><p class="ai-p">' + esc(sampleErr(e)) + "</p>";
    if (e && (e.code === "not_granted" || e.code === "sampling_disabled")){ CAP.sample = null; renderBatches(); box.hidden = false; box.innerHTML = '<h4>Chưa đánh giá được</h4><p class="ai-p">' + esc(sampleErr(e)) + "</p>"; }
  });
}
function aiHtml(full){
  var a = U.ai && U.ai.r; if (!a) return "";
  var stale = (U.ai.basis || []).join(",") !== U.batches.filter(function(b){ return !b.rm; }).map(function(b){ return b.id; }).join(",");
  var tone = a.muc_do === "Nặng hơn" ? "sev-Đỏ" : a.muc_do === "Nhẹ hơn" ? "sev-ok" : "sev-Vàng";
  var h = '<h4>Đánh giá bổ sung của Claude sau dữ liệu mới <span class="pill ' + tone + '" style="margin-left:6px"><i class="dot"></i>Kết luận ' + esc(a.muc_do.toLowerCase()) + "</span></h4>" + '<p class="ai-p"><b>' + esc(a.tom_tat) + "</b></p><p class=\"ai-p\">" + esc(a.anh_huong) + "</p>";
  if (full){
    h += a.diem.map(function(p){ return '<div class="row"><span class="pill sev-' + (p.muc === "Xanh" ? "ok" : p.muc) + '"><i class="dot"></i>' + esc(p.muc) + "</span><div><b>" + esc(p.ngay) + " · " + esc(p.tk) + (p.so_tien ? " · " + money(p.so_tien) : "") + "</b> · " + esc(p.noi_dung) + '<div class="subx" style="margin-top:2px">' + esc(p.ly_do) + (p.can_cu ? " (" + esc(p.can_cu) + ")" : "") + "</div></div></div>"; }).join("");
    if (a.ho_so.length) h += '<div class="row"><span class="pill tone-n"><i class="dot"></i>Hồ sơ</span><div>' + a.ho_so.map(esc).join("; ") + "</div></div>";
    if (a.luu_y_du_lieu) h += '<div class="row"><span class="pill tone-n"><i class="dot"></i>Dữ liệu</span><div>' + esc(a.luu_y_du_lieu) + "</div></div>";
  }
  h += '<div class="meta">Claude đánh giá lúc ' + fmtIso(U.ai.at) + (stale ? ". Dữ liệu đã thay đổi sau lần đánh giá này; có thể nhờ đánh giá lại." : ".") + " Đây là đánh giá tự động trên dữ liệu sao kê, cần đọc cùng chứng từ.</div>";
  return h;
}
function renderAI(){
  var box = $("aibox"), sum = $("ai-sum");
  if (AI_CTL) return;
  if (U.ai && U.ai.r){ box.innerHTML = aiHtml(true); box.hidden = false; sum.innerHTML = '<div class="aibox" style="margin-top:0">' + aiHtml(false) + ' <a href="#aibox">Xem chi tiết</a></div>'; sum.hidden = false; }
  else { box.hidden = true; box.innerHTML = ""; sum.hidden = true; sum.innerHTML = ""; }
}
