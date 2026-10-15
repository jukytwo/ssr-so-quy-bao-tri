/* ============================== document rebuild (self-publish, HTML download) ============================== */
var SKEL_OPEN = __SKEL_OPEN__, SKEL_CLOSE = __SKEL_CLOSE__, HEAD_FRAG = __HEAD_FRAG__, ROOT_INIT = __ROOT_INIT__;
function stag(id, type, body){ return '<script id="' + id + '"' + (type ? ' type="' + type + '"' : "") + ">" + body + "<\/script>\n"; }
function jsonTxt(o){ return JSON.stringify(o).replace(/</g, "\\u003c"); }
function uForSave(){
  return {v: 1, updatedAt: nowIso(), batches: U.batches.filter(function(b){ return !b.rm; }).map(function(b){ return {id: b.id, acc: b.acc, src: b.src, file: b.file, at: b.at, opening: b.opening, rows: b.rows, chk: b.chk}; }), tracker: U.tracker, ai: U.ai};
}
function buildDoc(u){
  var frag = HEAD_FRAG + '\n<style id="css">' + $("css").textContent + "<\/style>\n" + ROOT_INIT + "\n" +
    stag("tpl", "text/plain", $("tpl").textContent) + stag("D", "application/json", $("D").textContent) + stag("IMG", "application/json", $("IMG").textContent) +
    stag("FILES", "application/json", $("FILES").textContent) + stag("U", "application/json", jsonTxt(u)) + stag("app", "", $("app").textContent);
  return SKEL_OPEN + "\n" + frag + "\n" + SKEL_CLOSE;
}
function verifyDoc(html){
  var doc = new DOMParser().parseFromString(html, "text/html");
  ["css", "root", "tpl", "D", "IMG", "FILES", "U", "app"].forEach(function(id){ if (!doc.getElementById(id)) throw new Error("thiếu phần " + id); });
  ["css", "tpl", "D", "IMG", "FILES", "app"].forEach(function(id){ if (doc.getElementById(id).textContent !== $(id).textContent) throw new Error("phần " + id + " không khớp"); });
  var u = JSON.parse(doc.getElementById("U").textContent);
  if (!u || !Array.isArray(u.batches)) throw new Error("dữ liệu lưu không hợp lệ");
  if (!/^<!doctype html>/i.test(html)) throw new Error("thiếu doctype");
  return true;
}

/* ============================== save / publish ============================== */
var SAVING = false, LOCAL_CHANGED = false, PENDING = null;
function localSave(){
  U.batches = U.batches.filter(function(b){ return !b.rm; });
  var u = uForSave(); U.updatedAt = u.updatedAt;
  if (lsSet("ssr-u-v3", JSON.stringify(u))){ U.batches.forEach(function(b){ SAVED_BIDS[b.id] = 1; }); DIRTY = {batches: false, tracker: false, ai: false}; LOCAL_CHANGED = true; }
}
function publishNow(){
  if (SAVING || CAP.mode !== "writer" || !CAP.art) return;
  var u = uForSave(), html;
  try { html = buildDoc(u); verifyDoc(html); } catch (e) { toast("Chưa tạo được bản lưu: " + e.message, 6000); return; }
  if (html.length > 15.5 * 1024 * 1024){ toast("Dữ liệu quá lớn để lưu vào trang; hãy gỡ bớt đợt dữ liệu.", 6000); return; }
  SAVING = true; updateSavebar();
  ssSet("ssr-pending", JSON.stringify(u));
  /* trang co kem tep clip: luu bang dang files de giu nguyen cac tep clip; khong duoc thi moi dung dang html */
  var pubP = Promise.resolve().then(function(){ return CAP.art.publish({"index.html": html}); }).catch(function(e){
    var c = e && e.code; if (c === "conflict" || c === "rate_limited" || c === "not_writer" || c === "not_granted") throw e;
    return CAP.art.publish(html);
  });
  pubP.then(function(){
    toast("Đã lưu. Trang đang tải lại bản mới cho mọi người.", 6000);
  }).catch(function(e){
    var c = e && e.code;
    if (c === "conflict") toast("Trang vừa có bản mới hơn. Trang sẽ tải lại; thay đổi của bạn được giữ tạm để lưu lại.", 7000);
    else if (c === "not_writer" || c === "not_granted" || c === "not_declared" || c === "consent_required" || c === "capability_disabled"){ ssDel("ssr-pending"); CAP.mode = "reader"; CAP.canEdit = false; toast("Bạn đang ở chế độ chỉ xem nên không lưu được thay đổi.", 6000); renderReqs(); renderBatches(); }
    else if (c === "rate_limited") toast("Lưu quá dày; đợi một lúc rồi bấm Lưu lại.", 6000);
    else if (c === "too_large") toast("Trang quá lớn để lưu; hãy gỡ bớt dữ liệu.", 6000);
    else toast("Chưa lưu được (" + (c || "lỗi") + "). Thử lại sau ít phút.", 6000);
  }).then(function(){ SAVING = false; updateSavebar(); });
}
function undoAll(){
  U = normU(cloneU(U0)); SAVED_BIDS = {}; U.batches.forEach(function(b){ SAVED_BIDS[b.id] = 1; });
  DIRTY = {batches: false, tracker: false, ai: false};
  afterChange(); renderReqs(); toast("Đã bỏ các thay đổi chưa lưu.");
}
function checkPending(){
  var raw = ssGet("ssr-pending"); if (!raw) return;
  var p = null; try { p = normU(JSON.parse(raw)); } catch (e) { ssDel("ssr-pending"); return; }
  if (p.updatedAt && p.updatedAt === U0.updatedAt){ ssDel("ssr-pending"); return; }
  if (CAP.mode !== "writer"){ ssDel("ssr-pending"); return; }
  PENDING = p; updateSavebar();
}
function restorePending(){
  if (!PENDING) return;
  var keep = {}; U.batches.forEach(function(b){ keep[b.id] = 1; });
  PENDING.batches.forEach(function(b){ if (!keep[b.id]) U.batches.push(b); });
  Object.keys(PENDING.tracker).forEach(function(k){ var a = PENDING.tracker[k], b = U.tracker[k]; if (!b || (a.at || "") > (b.at || "")) U.tracker[k] = a; });
  if (PENDING.ai && (!U.ai || (PENDING.ai.at || "") > (U.ai.at || ""))) U.ai = PENDING.ai;
  DIRTY = {batches: true, tracker: true, ai: true}; PENDING = null; ssDel("ssr-pending");
  afterChange(); renderReqs(); toast("Đã khôi phục thay đổi chưa lưu; kiểm tra rồi bấm Lưu.");
}
function updateSavebar(){
  var sb = $("savebar"), h = "";
  if (PENDING && CAP.mode === "writer") h = '<span class="msg">Có thay đổi chưa lưu từ lần trước (trang có thể vừa được cập nhật ở nơi khác).</span><button class="tbtn" type="button" data-act="discard">Bỏ</button><button class="tbtn pri" type="button" data-act="restore">Khôi phục</button>';
  else if (CAP.mode === "writer" && isDirty()){
    var parts = [], nb = U.batches.filter(function(b){ return !b.rm && !SAVED_BIDS[b.id]; }).length, nr = U.batches.filter(function(b){ return b.rm; }).length;
    if (nb) parts.push(nb + " đợt dữ liệu mới"); if (nr) parts.push("gỡ " + nr + " đợt"); if (DIRTY.tracker) parts.push("tình trạng hồ sơ, câu hỏi"); if (DIRTY.ai) parts.push("đánh giá của Claude");
    h = '<span class="msg">Chưa lưu: ' + (parts.join(", ") || "thay đổi") + '. Khi lưu, mọi người xem trang sẽ thấy bản mới.</span><button class="tbtn" type="button" data-act="undo"' + (SAVING ? " disabled" : "") + '>Hoàn tác</button><button class="tbtn pri" type="button" data-act="save"' + (SAVING ? " disabled" : "") + ">" + (SAVING ? "Đang lưu…" : "Lưu cho mọi người xem") + "</button>";
  }
  else if (CAP.mode === "local" && LOCAL_CHANGED) h = '<span class="msg">Đã tự lưu trên trình duyệt này. Tải bản HTML mới để giữ lâu dài hoặc gửi người khác.</span><button class="tbtn" type="button" data-act="hide">Ẩn</button><button class="tbtn pri" type="button" data-act="html">Tải HTML đã cập nhật</button>';
  else if ((CAP.mode === "reader" || CAP.mode === "init") && isDirty()) h = '<span class="msg">Bạn đang xem thử thay đổi trên máy này; chỉ người quản trị trang lưu được cho mọi người.</span><button class="tbtn" type="button" data-act="undo">Bỏ thay đổi</button>';
  sb.innerHTML = h; sb.hidden = !h;
}

/* ============================== downloads ============================== */
var FILES = null;
function files(){ if (!FILES){ try { FILES = JSON.parse($("FILES").textContent); } catch (e) { FILES = {}; } } return FILES; }
function b64Bytes(b64){ var bin = atob(b64), n = bin.length, u8 = new Uint8Array(n); for (var i = 0; i < n; i++) u8[i] = bin.charCodeAt(i); return u8; }
function anchorSave(name, data, mime){
  try { var blob = data instanceof Blob ? data : new Blob([data], {type: mime || "application/octet-stream"}); var url = URL.createObjectURL(blob); var a = document.createElement("a"); a.href = url; a.download = name; a.rel = "noopener"; document.body.appendChild(a); a.click(); setTimeout(function(){ URL.revokeObjectURL(url); a.remove(); }, 60000); return true; }
  catch (e) { return false; }
}
function showHelp(kind, code){
  var box = $("helpbox"), h = "";
  if (kind === "print") h = '<h3>Trình xem này không cho in trực tiếp</h3><p>Trang đang mở trong khung xem của Claude, nơi lệnh in bị chặn. Hai cách in:</p><ol><li>Tải <b>báo cáo PDF đầy đủ</b> (đã dàn trang A4) rồi in.</li><li>Tải <b>bản HTML của trang này</b>, mở bằng trình duyệt (Chrome, Edge, Safari) rồi bấm Ctrl+P, trên Mac là Cmd+P. Bản in tự mở mọi mục thu gọn.</li></ol>';
  else h = '<h3>Chưa tải được tệp ở chế độ xem này</h3><p>Khung xem hiện tại không cho trang tải tệp' + (code ? " (mã: " + esc(code) + ")" : "") + '. Cách khác:</p><ol><li>Mở trang bằng trình duyệt web tại claude.ai theo đường link của trang, đăng nhập, rồi bấm tải lại; trình duyệt sẽ hỏi xác nhận trước khi lưu tệp.</li><li>Nhờ người quản trị trang gửi trực tiếp các tệp PDF, Excel, Word.</li></ol>';
  box.querySelector(".hb-in").innerHTML = h + '<div class="acts">' + (kind === "print" ? '<button class="tbtn pri" type="button" data-dl="pdf">Tải báo cáo PDF</button><button class="tbtn" type="button" data-dl="html">Tải bản HTML</button>' : "") + '<button class="tbtn" type="button" id="help-x">Đóng</button></div>';
  box.hidden = false; setTimeout(function(){ var x = $("help-x"); if (x) x.focus(); }, 30);
}
function saveFile(name, data, mime){
  toast("Đang chuẩn bị " + name + "…", 2500);
  var p = CAP.mode === "local" ? Promise.resolve(null) : withTimeout(capP("downloads"), 4000, null);
  return p.then(function(dl){
    if (dl){
      CAP.dl = dl;
      return Promise.resolve(dl.save({filename: name, data: data})).then(function(r){ toast(r && r.status === "delivered" ? "Đã gửi tệp " + name : "Đã lưu " + name, 4000); }).catch(function(e){
        var c = e && e.code;
        if (c === "declined") { toast("Đã hủy tải " + name); return; }
        if (c === "rate_limited"){ toast("Đang có một hộp thoại tải về chưa đóng; thử lại sau ít giây.", 5000); return; }
        if (c === "too_large"){ toast("Tệp quá lớn để tải ở chế độ xem này.", 5000); return; }
        if (!CAP.framed && anchorSave(name, data, mime)) return;
        showHelp("dl", c || "không rõ");
      });
    }
    if (!CAP.framed && anchorSave(name, data, mime)){ toast("Đã tải " + name, 3500); return; }
    showHelp("dl", "không hỗ trợ tải tệp");
  });
}
function renderDlNote(){
  var n = $("dl-note"); if (!n) return;
  n.hidden = !(CAP.framed && CAP.dlKnown && !CAP.dl);
}
function txAoa(){
  return [["Tài khoản", "Số tài khoản", "Ngày", "Nội dung", "Tiền ra (đồng)", "Tiền vào (đồng)", "Số dư (đồng)", "Đối ứng", "Phân loại", "Mức cảnh báo", "Ghi chú cảnh báo", "Nguồn"]].concat(M.all.map(function(t){ return [t.a, ACCN[t.a], t.d, t.s, t.dr || "", t.cr || "", t.b, t.cp, t.c, t.v, t.n, t.src ? "Mới" : "Gốc"]; }));
}
function exportCsv(){
  var q = function(v){ var s = String(v == null ? "" : v); return /[",\n;]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s; };
  var csv = "﻿" + txAoa().map(function(r){ return r.map(q).join(","); }).join("\r\n");
  return saveFile("SSR_Giao_dich_" + M.kMax + ".csv", csv, "text/csv");
}
function exportXlsx(){
  toast("Đang tạo tệp Excel…", 2500);
  return loadScript(LIBS.xlsx).then(function(){
    var X = window.XLSX, wb = X.utils.book_new();
    var aoa = txAoa().map(function(r, i){ if (!i) return r; var p = String(r[2]).split("/"); var dt = p.length === 3 ? new Date(+p[2], +p[1] - 1, +p[0], 12) : r[2]; return [r[0], r[1], dt].concat(r.slice(3)); });
    var ws = X.utils.aoa_to_sheet(aoa, {cellDates: true, dateNF: "dd/mm/yyyy"});
    ws["!cols"] = [{wch: 6}, {wch: 15}, {wch: 11}, {wch: 62}, {wch: 16}, {wch: 16}, {wch: 18}, {wch: 34}, {wch: 34}, {wch: 8}, {wch: 60}, {wch: 7}];
    ws["!autofilter"] = {ref: "A1:L" + aoa.length};
    X.utils.book_append_sheet(wb, ws, "Giao dịch");
    var B = D.base;
    var sm = [["Chỉ tiêu", "Dữ liệu gốc tới 31/05/2026", "Sau khi thêm dữ liệu mới", "Chênh lệch"],
      ["Quỹ còn (đồng)", B.fund_end, M.fund_end, M.fund_end - B.fund_end], ["Lãi đã nhận", B.interest, M.interest, M.interest - B.interest], ["Đã chi khỏi quỹ", B.spend, M.spend, M.spend - B.spend],
      ["Thu khu vực chung ngoài quỹ", B.ca_total, M.ca_total, M.ca_total - B.ca_total], ["Chi từ TK 7784", B.repair7784, M.repair7784, M.repair7784 - B.repair7784],
      ["Số dư TK 999", B.end_q, M.end_q, M.end_q - B.end_q], ["Số dư TK Agribank", B.end_a, M.end_a, M.end_a - B.end_a], ["Số dư TK 7784", B.end_v, M.end_v, M.end_v - B.end_v],
      [], ["Dữ liệu tới", BASE_ASOF, M.asof, ""], ["Số giao dịch", 198, M.all.length, M.nw.length]];
    var ws2 = X.utils.aoa_to_sheet(sm); ws2["!cols"] = [{wch: 30}, {wch: 24}, {wch: 24}, {wch: 18}];
    X.utils.book_append_sheet(wb, ws2, "Tổng hợp");
    var ck = [["Đợt", "Tài khoản", "Nguồn", "Từ ngày", "Đến ngày", "Số dòng", "Dòng lệch số dư", "Dòng trùng đã bỏ", "Nối số dư cũ", "Tháng thiếu"]].concat(U.batches.filter(function(b){ return !b.rm; }).map(function(b, i){ var st = batchStats(b), c = b.chk || {}; return [i + 1, b.acc, b.src + (b.file ? " · " + b.file : ""), st.from, st.to, b.rows.length, c.bad || 0, c.dup || 0, c.cont === false ? "Không" : "Có", (c.gaps || []).join(" ")]; }));
    ck.push([]); ck.push(["Lãi không kỳ hạn tính lại", "Tài khoản", "Tháng", "Trên sao kê", "Tính lại 0,2%/năm", "Chênh lệch"]);
    M.ic.forEach(function(x){ ck.push(["", x.a, x.m, x.act, x.exp, x.diff]); });
    var ws3 = X.utils.aoa_to_sheet(ck); ws3["!cols"] = [{wch: 24}, {wch: 10}, {wch: 30}, {wch: 12}, {wch: 16}, {wch: 12}, {wch: 14}, {wch: 14}, {wch: 12}, {wch: 20}];
    X.utils.book_append_sheet(wb, ws3, "Kiểm tra dữ liệu mới");
    var tk = [["#", "Hồ sơ", "Mục đích", "Gửi tới", "Ưu tiên", "Tình trạng", "Ghi chú", "Cập nhật"]].concat(D.requests.map(function(r, i){ var t = U.tracker["rq" + i] || {}; return [i + 1, r.doc, r.why, r.to, r.pri, tstLabel(t.s || "chua"), t.n || "", t.at ? fmtIso(t.at) : ""]; }));
    var ws4 = X.utils.aoa_to_sheet(tk); ws4["!cols"] = [{wch: 4}, {wch: 70}, {wch: 46}, {wch: 18}, {wch: 8}, {wch: 18}, {wch: 40}, {wch: 16}];
    X.utils.book_append_sheet(wb, ws4, "Hồ sơ cần đòi");
    var out = X.write(wb, {bookType: "xlsx", type: "array"});
    return saveFile("SSR_Giao_dich_cap_nhat_" + M.kMax + ".xlsx", new Blob([out], {type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"}));
  }).catch(function(e){ toast("Chưa tạo được tệp Excel: " + (e && e.message ? e.message : e)); });
}
function renderDownloads(){
  var F = D.files, items = [
    {k: "pdf", c: "#A93434", t: "PDF", h: "Báo cáo phân tích đầy đủ", p: F.pdf_desc, b: "Tải PDF"},
    {k: "sum", c: "#C0662A", t: "PDF", h: "Báo cáo phân tích tóm tắt", p: F.sum_desc || "", b: "Tải PDF"},
    {k: "xlsx", c: "#1E7A46", t: "XLSX", h: "Sao kê tổng hợp và phân tích", p: F.xlsx_desc, b: "Tải Excel"}];
  if (F.cv) items.push({k: "cv", c: "#1F3864", t: "DOCX", h: "Công văn kiến nghị gửi Ban quản trị", p: F.cv_desc, b: "Tải Word"});
  if (F.q10pdf) items.push({k: "q10pdf", c: "#8a6100", t: "PDF", h: "Mười câu hỏi gửi Ban quản trị", p: F.q10pdf_desc, b: "Tải PDF"});
  if (F.q10png) items.push({k: "q10png", c: "#8a6100", t: "PNG", h: "Mười câu hỏi, bản ảnh", p: F.q10png_desc, b: "Tải ảnh"});
  if (F.pl) items.push({k: "pl", c: "#5b6474", t: "PDF", h: "Phân loại nguyên nhân các sai sót", p: F.pl_desc, b: "Tải PDF"});
  if (F.hdan) items.push({k: "hdan", c: "#5b6474", t: "PDF", h: "Hỏi dần để biết mỗi cái sai thuộc nguyên nhân nào", p: F.hdan_desc, b: "Tải PDF"});
  items.push({k: "txx", c: "#2E6F95", t: "XLSX", h: "Giao dịch cập nhật", p: "Toàn bộ " + M.all.length + " giao dịch gốc và mới, phân loại, cảnh báo, kiểm tra dữ liệu mới, tình trạng hồ sơ", b: "Tải Excel"});
  items.push({k: "csv", c: "#4b5a66", t: "CSV", h: "Giao dịch dạng CSV", p: "Mở được bằng mọi phần mềm bảng tính", b: "Tải CSV"});
  items.push({k: "html", c: "#0b6e69", t: "HTML", h: "Bản lưu trữ của trang này", p: "Một tệp duy nhất, mở bằng trình duyệt, gồm dữ liệu hiện tại", b: "Tải HTML"});
  items.push({k: "print", c: "#8a6100", t: "IN", h: "In hoặc lưu PDF trang này", p: "Bản in tự mở mọi mục đang thu gọn", b: "In"});
  if (!F.sum) items = items.filter(function(f){ return f.k !== "sum"; });
  var pop = items.filter(function(f){ return ["pdf", "sum", "xlsx", "cv", "q10pdf", "txx", "html", "print"].indexOf(f.k) >= 0; });
  var g4 = $("a4g"); if (g4) g4.innerHTML = a4GalleryHtml();
  $("dl-pop").innerHTML = pop.map(function(f){ return '<button type="button" data-dl="' + f.k + '"><span class="ic" style="background:' + f.c + '">' + f.t + "</span><span>" + esc(f.h) + "<small>" + (f.k === "print" ? "Hoặc tải PDF để in" : esc(f.b)) + "</small></span></button>"; }).join("") + '<hr><a href="#tai-ve">Tất cả lựa chọn tải về</a>';
  $("dlg").innerHTML = items.map(function(f){ return '<div class="dlc"><div class="ic" style="background:' + f.c + '">' + f.t + "</div><div><h4>" + esc(f.h) + "</h4><p>" + esc(f.p) + '</p></div><div class="dlc-b"><button class="tbtn" type="button" data-dl="' + f.k + '">' + f.b + "</button>" + (SHR_SEND[f.k] ? '<button class="tbtn shr-f" type="button" data-sendfile="' + f.k + '">' + SHR_IC + "Gửi tệp</button>" : "") + "</div></div>"; }).join("");
}
/* tep tai ve: ban truc tuyen giu tep rieng (f/...), chi tai khi bam; ban offline nhung san trong trang */
function fileBytes(k){
  var v = files()[k]; if (!v) return Promise.reject(new Error("no file"));
  if (v.indexOf("f/") === 0) return fetch(v).then(function(r){ if (!r.ok) throw new Error(r.status); return r.arrayBuffer(); }).then(function(b){ return new Uint8Array(b); });
  return Promise.resolve(b64Bytes(v));
}
function doDownload(k){
  var F = D.files;
  var XM = {pdf: "application/pdf", sum: "application/pdf", xlsx: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", cv: "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            q10png: "image/png", q10pdf: "application/pdf", pl: "application/pdf", hdan: "application/pdf"};
  if (XM[k] && F[k] && files()[k]){
    if (files()[k].indexOf("f/") === 0) toast("Đang chuẩn bị " + F[k] + "…", 3000);
    return fileBytes(k).then(function(u8){ return saveFile(F[k], new Blob([u8], {type: XM[k]}), XM[k]); })
      .catch(function(){ toast("Chưa tải được " + F[k] + " ở chế độ xem này. Mở trang trực tuyến rồi thử lại.", 6000); });
  }
  if (k === "txx") return exportXlsx();
  if (k === "csv") return exportCsv();
  if (k === "html"){ var u = uForSave(); if (!isDirty() && U0.updatedAt) u.updatedAt = U.updatedAt || U0.updatedAt; return saveFile("SSR_So_quy_bao_tri_" + M.kMax + ".html", buildDoc(u), "text/html"); }
  if (k === "print") return doPrint();
}

/* ============================== print ============================== */
var PRINT_STATE = null;
function prepPrint(on){
  var mm = mainEl();
  if (on && mm) mm.classList.remove("paged"); else if (!on && mm && PAGED) mm.classList.add("paged");
  if (on && !PRINT_STATE){
    PRINT_STATE = {hd: {t: HD.t, q: HD.q, terms: HD.terms}};
    HD.t = "all"; HD.q = ""; HD.terms = []; applyFAQ();
    PRINT_STATE.mx = MXF; PRINT_STATE.fa = FALL; PRINT_STATE.ca = CHK_ALL; PRINT_STATE.det = qa("details").filter(function(d){ return !d.open; }); PRINT_STATE.cz = qa("section.cz"); PRINT_STATE.tl = TXLIM;
    PRINT_STATE.cz.forEach(function(sx){ sx.classList.remove("cz"); });
    PRINT_STATE.nn = FNN; FNN = "";
    MXF = ""; FALL = true; CHK_ALL = true; renderMatrix(); renderFinds(); renderChecks(); PRINT_STATE.det.forEach(function(d){ d.open = true; });
  } else if (!on && PRINT_STATE){
    MXF = PRINT_STATE.mx; FALL = PRINT_STATE.fa; FNN = PRINT_STATE.nn || ""; CHK_ALL = PRINT_STATE.ca; renderMatrix(); renderFinds(); renderChecks(); PRINT_STATE.det.forEach(function(d){ d.open = false; }); PRINT_STATE.cz.forEach(function(sx){ sx.classList.add("cz"); });
    HD.t = PRINT_STATE.hd.t; HD.q = PRINT_STATE.hd.q; HD.terms = PRINT_STATE.hd.terms; applyFAQ(); PRINT_STATE = null;
  }
}
function doPrint(){
  prepPrint(true);
  setTimeout(function(){
    var t0 = Date.now();
    try { window.print(); } catch (e) {}
    if (Date.now() - t0 < 250){ prepPrint(false); showHelp("print"); }
  }, 80);
}
window.addEventListener("beforeprint", function(){ prepPrint(true); });
window.addEventListener("afterprint", function(){ prepPrint(false); });

/* ============================== refresh ============================== */
function renderDynamic(){
  renderHero(); renderBanner(); renderTimeline(); renderStatements(); renderComp(); renderWaterfall(); renderKVC(); renderIdle(); renderNewFlags(); renderTxCats(); renderTx(); renderBatches(); renderFoot();
  qa('[data-dl="txx"]').forEach(function(b){ var p = b.parentNode.querySelector("p"); if (p) p.textContent = "Toàn bộ " + M.all.length + " giao dịch gốc và mới, phân loại, cảnh báo, kiểm tra dữ liệu mới, tình trạng hồ sơ"; });
}
function afterChange(){ M = compute(); renderDynamic(); if (CAP.mode === "local") localSave(); updateSavebar(); }
function afterTracker(){ renderTrkBar(); if (CAP.mode === "local") localSave(); updateSavebar(); }

/* ============================== reading on phone and laptop ============================== */
var MOBQ = window.matchMedia ? window.matchMedia("(max-width: 760px)") : {matches: false};
var CHEV = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>';
function setCollapsed(sec, on){
  if (!sec || !sec.querySelector(".sb")) return;
  var was = sec.classList.contains("cz");
  sec.classList.toggle("cz", on);
  var b = sec.querySelector(".sb-t"); if (b){ b.setAttribute("aria-expanded", on ? "false" : "true"); b.innerHTML = (on ? "Xem phân tích chi tiết" : "Thu gọn, chỉ xem kết luận") + CHEV; }
  if (was && !on) redrawIn(sec);
}
function initCollapse(){ qa("main section").forEach(function(s){ setCollapsed(s, true); }); }
function revealTarget(el){
  if (PAGED){ var v = viewOf(el); if (v && v !== "*" && v !== VIEW_CUR) showView(v, {noScroll: true, hash: false}); }
  var s = el && el.closest ? el.closest("section") : null; if (s && s.classList.contains("cz")) setCollapsed(s, false);
  if (el && el.id && el.id.indexOf("hdq-") === 0 && typeof hdSetTopic === "function" && typeof FQ !== "undefined" && FQ){ var it = FQ.items.filter(function(i){ return "hdq-" + i.id === el.id; })[0]; if (it) hdSetTopic(it.t); }
  if (el && el.tagName === "DETAILS") el.open = true;
}
/* ------------------------------ doc theo tung phan: moi lan hien mot phan ------------------------------ */
var PAGED = true, VIEW_CUR = "0", VIEW_ORDER = [];
var VIEW_NAME = {"0": "Trang đầu", "clip": "Xem clip", "tien": "Đường đi của tiền", "cauhoi": "Mười câu hỏi gửi Ban quản trị", "1": "I · Kết luận", "2": "II · Dữ liệu và độ tin cậy", "3": "III · Dòng tiền của quỹ", "4": "IV · An toàn và tuân thủ", "5": "V · Dấu hiệu và hành động", "hd": "VI · Hỏi đáp", "6": "VII · Công cụ và dữ liệu gốc"};
var CHL = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 6l-6 6 6 6"/></svg>';
var CHR = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg>';
function mainEl(){ return document.querySelector("main.wrap"); }
function viewOf(el){ var m = mainEl(); if (!el || !m) return null; while (el && el.parentNode && el.parentNode !== m) el = el.parentNode; return el && el.parentNode === m && el.getAttribute ? el.getAttribute("data-view") : null; }
function initPaged(){
  var m = mainEl(); if (!m) return; var cur = "0";
  Array.prototype.slice.call(m.children).forEach(function(ch){
    if (ch.id === "upd-banner"){ ch.setAttribute("data-view", "*"); return; }
    if (ch.classList.contains("part")) cur = ch.id.replace("phan-", "");
    ch.setAttribute("data-view", cur); if (VIEW_ORDER.indexOf(cur) < 0) VIEW_ORDER.push(cur);
  });
  VIEW_ORDER.forEach(function(v, i){
    var els = qa('main.wrap > [data-view="' + v + '"]'), last = els[els.length - 1]; if (!last) return;
    var prev = VIEW_ORDER[i - 1], next = VIEW_ORDER[i + 1], nav = document.createElement("nav");
    nav.className = "pager"; nav.setAttribute("data-view", v); nav.setAttribute("aria-label", "Chuyển phần");
    nav.innerHTML = (prev != null ? '<button type="button" class="pg-b pv" data-goview="' + prev + '"><small>' + CHL + "Phần trước</small><b>" + esc(VIEW_NAME[prev]) + "</b></button>" : "<span></span>") +
      (next != null ? '<button type="button" class="pg-b nx" data-goview="' + next + '"><small>Phần tiếp theo' + CHR + "</small><b>" + esc(VIEW_NAME[next]) + "</b></button>"
                    : '<button type="button" class="pg-b nx" data-goview="0"><small>Đã hết các phần</small><b>Về trang đầu</b></button>');
    last.parentNode.insertBefore(nav, last.nextSibling);
  });
  m.classList.add("paged"); showView("0", {noScroll: true, hash: false});
}
function showView(v, o){
  if (!PAGED || v == null || VIEW_ORDER.indexOf(v) < 0) return; o = o || {}; VIEW_CUR = v;
  if (v !== "clip"){ var cv = document.getElementById("clp-v"); if (cv && !cv.paused) cv.pause(); }
  qa("main.wrap > [data-view]").forEach(function(el){ el.classList.toggle("v-on", el.getAttribute("data-view") === v); });
  qa(".nav a[data-part], .bnav a[data-part]").forEach(function(a){ a.classList.toggle("on", a.getAttribute("data-part") === v); });
  qa('main.wrap > section[data-view="' + v + '"]').forEach(function(el){ if (!el.classList.contains("cz")) redrawIn(el); });
  if (!o.noScroll) window.scrollTo(0, 0);
  if (o.hash !== false){ try { history.replaceState(null, "", "#" + (v === "0" ? "tong-quan" : "phan-" + v)); } catch (e) {} }
}
function redrawIn(root){
  if (root.querySelector("#wf")) renderWaterfall();
  if (root.querySelector("#idle")) renderIdle();
  if (root.querySelector("#td-trace")) renderTdTrace();
  if (root.querySelector("#inc")) renderKVC();
  if (root.querySelector("#safety")) renderSafety();
}
var PARTN = [["I", "Kết luận", 1], ["II", "Dữ liệu và độ tin cậy", 2], ["III", "Dòng tiền của quỹ", 3], ["IV", "An toàn và tuân thủ", 4], ["V", "Dấu hiệu và hành động", 5], ["VI", "Hỏi đáp", "hd"], ["VII", "Công cụ và dữ liệu gốc", 6]];
function renderToc(){
  var h = '<a href="#tong-quan"><span class="no">·</span><span>Tổng quan, câu trả lời ngắn</span><span></span></a>';
  h += '<div class="tp">Xem nhanh</div>' + [["phan-tien", "Đường đi của tiền: năm trường hợp"], ["phan-cauhoi", "Mười câu hỏi gửi Ban quản trị"]].map(function(x){ return '<a href="#' + x[0] + '"><span class="no">·</span><span>' + x[1] + '</span><span></span></a>'; }).join("");
  if (D.clips) h += '<div class="tp">Xem clip</div>' + [["full", "Bản đầy đủ, 16 chương"], ["phan_1", "Sáu phần ngang"], ["doc_01", "Mười một clip dọc"], ["tom_tat", "Clip tóm tắt 90 giây"]].map(function(x){ return '<a href="#clip-' + x[0] + '" data-clipdeep="' + x[0] + '"><span class="no">▶</span><span>' + x[1] + "</span><span></span></a>"; }).join("");
  PARTN.forEach(function(p, i){
    h += '<div class="tp">Phần ' + p[0] + " · " + p[1] + "</div>";
    if (p[2] === "hd") h += [{id: "hot", l: "Nên đọc trước"}].concat(D.faq.topics).map(function(t){ var n = t.id === "hot" ? D.faq.items.filter(function(x){ return x.hot; }).length : D.faq.items.filter(function(x){ return x.t === t.id; }).length; return '<a href="#hoi-dap" data-hdt="' + t.id + '"><span class="no">?</span><span>' + esc(t.l) + '</span><span class="subx">' + n + " câu</span></a>"; }).join("");
    else if (p[2] === 6) h += [["cap-nhat", "Cập nhật sao kê mới"], ["giao-dich", "Tra cứu giao dịch"], ["tai-ve", "Tải báo cáo, dữ liệu"], ["tu-dien", "Thuật ngữ"]].map(function(x){ return '<a href="#' + x[0] + '"><span class="no">·</span><span>' + x[1] + "</span><span></span></a>"; }).join("");
    else h += secIds(p[2]).map(function(no){ var c = D.concl[no]; return '<a href="#' + SEC[no].id + '"><span class="no">' + no + "</span><span>" + esc(SEC[no].t) + '</span><span class="pill tone-' + c[1] + '"><i class="dot"></i>' + esc(c[0]) + "</span></a>"; }).join("");
  });
  $("toc-list").innerHTML = h;
}
var TOC_OPENER = null;
function openToc(opener){ TOC_OPENER = opener || null; $("toc").hidden = false; document.body.style.overflow = "hidden"; setTimeout(function(){ var x = $("toc-x"); if (x) x.focus(); }, 30); }
function closeToc(){ $("toc").hidden = true; document.body.style.overflow = ""; if (TOC_OPENER && TOC_OPENER.focus) TOC_OPENER.focus(); TOC_OPENER = null; }
var LASTW = window.innerWidth, RZT = null;
window.addEventListener("resize", function(){ clearTimeout(RZT); RZT = setTimeout(function(){ if (Math.abs(window.innerWidth - LASTW) < 30) return; LASTW = window.innerWidth; redrawIn(document); }, 180); });

/* ============================== events ============================== */
function flash(node){ if (!node) return; node.style.transition = "box-shadow .3s"; node.style.boxShadow = "0 0 0 3px var(--accent)"; setTimeout(function(){ node.style.boxShadow = ""; }, 1800); }
var SHR_SEND = {pdf: 1, sum: 1, xlsx: 1, cv: 1, q10pdf: 1, q10png: 1, pl: 1, hdan: 1};
function addSecShare(){
  qa("main section[id] .sec-h").forEach(function(h){
    var s = h.closest("section[id]"), t = h.querySelector("h2"); if (!s || !t || h.querySelector(".shr")) return;
    var ey = h.querySelector(".eyebrow"), b = shareBtn("#" + s.id, t.textContent.trim(), "");
    if (ey) ey.insertAdjacentHTML("beforeend", b); else t.insertAdjacentHTML("afterend", b);
  });
  qa("main .part[id]").forEach(function(p){
    var t = p.querySelector(".pt"); if (!t || p.querySelector(".shr")) return;
    p.insertAdjacentHTML("beforeend", shareBtn("#" + p.id, t.textContent.trim(), "Chia sẻ phần này", "shr shr-p"));
  });
}
function bindEvents(){
  document.addEventListener("click", function(e){
    if (e.target === $("toc")){ closeToc(); return; }
    if (e.target === $("helpbox")){ $("helpbox").hidden = true; return; }
    if (!$("dl-pop").hidden && !(e.target.closest && (e.target.closest("#dl-pop") || e.target.closest("#btn-dl")))) $("dl-pop").hidden = true;
    var t = e.target.closest ? e.target.closest("button, a") : null; if (!t) return;
    if (t.hasAttribute("data-share")){ e.preventDefault(); e.stopPropagation(); $("dl-pop").hidden = true; shareGo(t.getAttribute("data-share"), t.getAttribute("data-st") || ""); return; }
    if (t.id === "shr-send"){ shareSendPending(); return; }
    if (t.hasAttribute("data-sendfile")){ var sk = t.getAttribute("data-sendfile"); shareFileGo(function(){ return fileBytes(sk); }, D.files[sk], D.files[sk]); return; }
    if (t.hasAttribute("data-sendimg")){ var ai = a4Item(t.getAttribute("data-sendimg")); shareFileGo(a4Bytes(ai.k), ai.n, "ảnh " + ai.t); return; }
    if (t.hasAttribute("data-saveimg")){ var as = a4Item(t.getAttribute("data-saveimg")); a4Bytes(as.k)().then(function(b){ saveFile(as.n, b, "image/png"); }).catch(function(){ toast("Chưa tải được ảnh ở chế độ xem này. Mở trang trực tuyến rồi thử lại.", 6000); }); return; }
    if (t.id === "shr-cp"){ var su = $("shr-u"); if (su) copyText(su.value).then(function(){ t.textContent = "Đã sao chép"; toast("Đã sao chép đường dẫn.", 2600); }).catch(function(){ su.focus(); su.select(); toast("Nhấn giữ vào đường dẫn để sao chép.", 3600); }); return; }
    if (t.hasAttribute("data-goview")){ e.preventDefault(); showView(t.getAttribute("data-goview")); return; }
    if (t.hasAttribute("data-clipdeep")){ e.preventDefault(); if (!$("toc").hidden) closeToc(); clpDeep(t.getAttribute("data-clipdeep")); window.scrollTo(0, 0); return; }
    if (t.hasAttribute("data-hdt")){
      hdSetTopic(t.getAttribute("data-hdt"));
      if (t.classList.contains("hd-tb")){ e.preventDefault(); hdScrollHead(); try { t.scrollIntoView({inline: "center", block: "nearest"}); } catch (e2) {} return; }
    }
    if (t.hasAttribute("data-hdx")){ var op = t.getAttribute("data-hdx") === "open"; qa("#hd-list details.qa:not([hidden])").forEach(function(d){ d.open = op; }); if (!op) hdScrollHead(); return; }
    if (t.hasAttribute("data-hdask")){ var ta = $("hd-ask-q"); if (ta){ ta.value = HD.q; $("hd-ask").scrollIntoView({block: "center"}); ta.focus(); } return; }
    if (t.id === "hd-clr"){ var hq = $("hd-q"); hq.value = ""; hdSearch(""); hq.focus(); return; }
    if (t.id === "hd-ask-stop"){ if (ASK.ctl) ASK.ctl.abort(); return; }
    if (t.hasAttribute("data-ht")){ HT_ST[+t.getAttribute("data-ht")] = t.getAttribute("data-v"); renderHTList(); var nb = document.querySelector('[data-ht="' + t.getAttribute("data-ht") + '"][data-v="' + t.getAttribute("data-v") + '"]'); if (nb) nb.focus(); return; }
    if (t.hasAttribute("data-htp")){ htPreset(t.getAttribute("data-htp")); renderHTList(); toast("Đã chọn: " + t.textContent); return; }
    if (t.classList.contains("sb-t")){ var sec = t.closest("section"), on = !sec.classList.contains("cz"); setCollapsed(sec, on); if (on) sec.scrollIntoView({block: "start"}); return; }
    if (t.id === "btn-toc" || t.id === "bnav-toc"){ openToc(t); return; }
    if (t.id === "help-x"){ $("helpbox").hidden = true; return; }
    if (t.id === "btn-dl"){ e.preventDefault(); var pop = $("dl-pop"); pop.hidden = !pop.hidden; t.setAttribute("aria-expanded", pop.hidden ? "false" : "true"); return; }
    if (t.closest && t.closest("#dl-pop") && !t.hasAttribute("data-dl")){ $("dl-pop").hidden = true; }
    if (t.id === "toc-x"){ closeToc(); return; }
    if (t.id === "toc-exp"){ qa("main section").forEach(function(s){ setCollapsed(s, false); }); closeToc(); return; }
    if (t.id === "toc-col"){ qa("main section").forEach(function(s){ setCollapsed(s, true); }); closeToc(); return; }
    if (t.id === "tx-more"){ TXLIM += MOBQ.matches ? 30 : 100; renderTx(); return; }
    if (t.tagName === "A" && (t.getAttribute("href") || "").charAt(0) === "#" && !t.matches("a.cd[data-code]")){
      var tg = document.getElementById(t.getAttribute("href").slice(1));
      if (tg){ var inToc = !!t.closest("#toc"); if (inToc) closeToc(); revealTarget(tg); if (inToc){ e.preventDefault(); setTimeout(function(){ tg.scrollIntoView({block: "start"}); }, 20); } }
    }
    if (t.hasAttribute("data-cat") && t.getAttribute("href") === "#giao-dich"){
      $("f-acc").value = ""; $("f-src").value = ""; $("f-flag").checked = false; $("f-small").checked = false; $("f-q").value = "";
      $("f-cat").value = t.getAttribute("data-cat"); TXLIM = txBase(); renderTx(); setTimeout(function(){ flash($("tb").closest(".tbl-wrap")); }, 350);
    }
    if (t.matches("a.kpi, a.vs")){ var tg2 = document.getElementById((t.getAttribute("href") || "").slice(1)); if (tg2 && tg2.tagName !== "SECTION") setTimeout(function(){ flash(tg2); }, 350); }
    if (t.matches("a.cd[data-code]")){ e.preventDefault(); var code = t.getAttribute("data-code"); FALL = true; revealTarget($("finds")); renderFinds(); var card = $("find-" + code); if (card){ card.scrollIntoView({behavior: "smooth", block: "center"}); flash(card); var dt = card.querySelector("details"); if (dt) dt.open = true; } return; }
    if (t.matches("[data-sev]") && t.getAttribute("href") === "#dau-hieu"){ FSEV = t.getAttribute("data-sev"); FALL = false; renderFinds(); return; }
    if (t.parentNode && t.parentNode.id === "tl-f"){ TLF = t.getAttribute("data-f"); renderTimeline(); return; }
    if (t.parentNode && t.parentNode.id === "mx-sum"){ MXF = t.getAttribute("data-s"); renderMatrix(); return; }
    if (t.parentNode && t.parentNode.id === "fchips"){ FSEV = t.getAttribute("data-s"); FALL = !FSEV; renderFinds(); return; }
    if (t.parentNode && t.parentNode.id === "fnnchips"){ FNN = t.getAttribute("data-n"); if (FNN) FALL = true; renderFinds(); return; }
    if (t.id === "find-more"){ FALL = true; renderFinds(); return; }
    if (t.id === "chk-more"){ CHK_ALL = !CHK_ALL; renderChecks(); if (!CHK_ALL) $("bo-sung").scrollIntoView({block: "start"}); return; }
    if (t.parentNode && t.parentNode.id === "c-q"){ $("c-rate").value = t.getAttribute("data-r"); calcUpd(); return; }
    if (t.hasAttribute("data-tab")){ var tb = t.getAttribute("data-tab"); qa(".tabs .fbtn").forEach(function(b){ b.setAttribute("aria-pressed", b === t ? "true" : "false"); }); $("tab-file").hidden = tb !== "file"; $("tab-man").hidden = tb !== "man"; return; }
    if (t.id === "up-abort"){ if (PDF_CTL) PDF_CTL.abort(); return; }
    if (t.id === "m-add"){ addManual(); return; }
    if (t.hasAttribute("data-del")){ var i = +t.getAttribute("data-del"); DRAFT.rows.splice(i, 1); if (!DRAFT.rows.length){ DRAFT = null; renderPreview(); } else refreshPreview(); return; }
    if (t.id === "pv-addrow"){ var lr = DRAFT.rows[DRAFT.rows.length - 1]; DRAFT.rows.push({d: lr ? lr.d : "", s: "", dr: 0, cr: 0, b: null, cp: ""}); refreshPreview(); var ins = qa("#pv-body tr:last-child input"); if (ins[1]) ins[1].focus(); return; }
    if (t.id === "pv-fill"){ DRAFT.rows.forEach(function(r){ if (r.b == null && r._exp != null) r.b = r._exp; }); refreshPreview(); return; }
    if (t.id === "pv-drop"){ DRAFT = null; renderPreview(); setSt(""); return; }
    if (t.id === "pv-apply"){ applyDraft(); return; }
    if (t.hasAttribute("data-rmb")){ removeBatch(t.getAttribute("data-rmb")); return; }
    if (t.hasAttribute("data-undo")){ U.batches.forEach(function(b){ if (b.id === t.getAttribute("data-undo")) delete b.rm; }); afterChange(); return; }
    if (t.id === "ai-run"){ runAI(); return; }
    if (t.id === "ai-stop"){ if (AI_CTL) AI_CTL.abort(); return; }
    if (t.hasAttribute("data-act")){ var a = t.getAttribute("data-act");
      if (a === "save") publishNow(); else if (a === "undo") undoAll(); else if (a === "html") doDownload("html"); else if (a === "hide"){ LOCAL_CHANGED = false; updateSavebar(); }
      else if (a === "restore") restorePending(); else if (a === "discard"){ PENDING = null; ssDel("ssr-pending"); updateSavebar(); }
      return; }
    if (t.hasAttribute("data-dl")){ $("dl-pop").hidden = true; if (t.closest("#helpbox")) $("helpbox").hidden = true; doDownload(t.getAttribute("data-dl")); return; }
    if (t.id === "btn-print"){ doPrint(); return; }
    if (t.id === "fab"){ window.scrollTo({top: 0, behavior: "smooth"}); return; }
  });
  document.addEventListener("change", function(e){
    var t = e.target;
    if (t.matches("select[data-rq]")){ var id = t.getAttribute("data-rq"), o = U.tracker[id] || {}; U.tracker[id] = {s: t.value, n: o.n || "", at: nowIso()}; DIRTY.tracker = true; afterTracker(); return; }
    if (t.matches("input[data-rqn]")){ var id2 = t.getAttribute("data-rqn"), o2 = U.tracker[id2] || {}; U.tracker[id2] = {s: o2.s || "chua", n: t.value.slice(0, 200), at: nowIso()}; DIRTY.tracker = true; afterTracker(); return; }
    if (t.id === "f-up"){ handleFile(t.files && t.files[0]); t.value = ""; return; }
    if (t.id === "pv-acc"){ DRAFT.acc = t.value; refreshPreview(); return; }
    if (t.closest && t.closest("#pv-body") && t.hasAttribute("data-f")){
      var tr0 = t.closest("tr"), r = DRAFT.rows[+tr0.getAttribute("data-i")], f = t.getAttribute("data-f"), v = t.value;
      if (f === "d") r.d = parseDate(v) || v.trim(); else if (f === "s" || f === "cp") r[f] = v.trim(); else if (f === "b") r.b = v.trim() === "" ? null : parseNum(v); else r[f] = Math.abs(parseNum(v));
      refreshPreview(); return;
    }
    if (["f-acc", "f-cat", "f-src", "f-flag", "f-small"].indexOf(t.id) >= 0){ TXLIM = txBase(); renderTx(); return; }
  });
  $("f-q").addEventListener("input", function(){ TXLIM = txBase(); renderTx(); });
  var HDT = null;
  $("hd-q").addEventListener("input", function(){ var v = this.value; clearTimeout(HDT); HDT = setTimeout(function(){ hdSearch(v); }, 120); });
  $("hd-q").addEventListener("keydown", function(e){ if (e.key === "Enter"){ e.preventDefault(); clearTimeout(HDT); hdSearch(this.value); this.blur(); hdScrollHead(); } else if (e.key === "Escape" && this.value){ e.stopPropagation(); this.value = ""; hdSearch(""); } });
  $("hd-ask-f").addEventListener("submit", function(e){ e.preventDefault(); runAsk($("hd-ask-q").value); });
  $("hd-ask-q").addEventListener("keydown", function(e){ if (e.key === "Enter" && (e.ctrlKey || e.metaKey)){ e.preventDefault(); runAsk(this.value); } });
  document.addEventListener("keydown", function(e){ if (e.key !== "Escape") return; if (!$("toc").hidden) closeToc(); $("helpbox").hidden = true; $("dl-pop").hidden = true; });
  ["c-amt", "c-rate"].forEach(function(id){ $(id).addEventListener("input", calcUpd); });
  var drop = $("drop");
  ["dragenter", "dragover"].forEach(function(ev){ drop.addEventListener(ev, function(e){ e.preventDefault(); drop.classList.add("over"); }); });
  ["dragleave", "drop"].forEach(function(ev){ drop.addEventListener(ev, function(e){ e.preventDefault(); drop.classList.remove("over"); }); });
  drop.addEventListener("drop", function(e){ var f = e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0]; handleFile(f); });
  var ticking = false, parts = qa(".part"), links = qa(".nav a[data-part], .bnav a[data-part]"), prog = $("prog");
  window.addEventListener("scroll", function(){
    if (ticking) return; ticking = true;
    requestAnimationFrame(function(){
      ticking = false; var cur = "";
      if (PAGED) cur = VIEW_CUR; else parts.forEach(function(p){ if (p.getBoundingClientRect().top < 140) cur = p.id.replace("phan-", ""); });
      links.forEach(function(a){ a.classList.toggle("on", a.getAttribute("data-part") === cur); });
      $("fab").hidden = window.scrollY < 900;
      var dh = document.documentElement.scrollHeight - window.innerHeight; if (prog) prog.style.width = (dh > 0 ? Math.min(100, window.scrollY / dh * 100) : 0).toFixed(1) + "%";
    });
  }, {passive: true});
}

/* ============================== init ============================== */
function init(){
  $("root").innerHTML = $("tpl").textContent.replace(/\{\{IMG:(\w+)\}\}/g, function(m, k){ return IMG[k] || ""; });
  initCaps();
  M = compute();
  renderKL(); renderPartChips(); renderVerdict(); renderTests(); renderCauses(); renderChic(); renderRateStatic(); renderSafety(); renderMatrix(); renderChecks(); renderFinds(); renderRoad(); renderGlossary(); renderTdTrace(); renderHT(); renderHD(); renderDocs(); renderTdNew(); initTheme(); renderFAQ(); renderKM(); renderClipStrip(); renderSecClips(); initFileToggle();
  initCollapse(); renderToc(); renderDlNote(); initPaged();
  renderClips(); renderLDX(); renderFive();
  renderDynamic(); renderReqs(); renderDownloads();
  addSecShare();
  applyAbbr();
  bindEvents();
  onCaps(function(){ renderReqs(); renderBatches(); updateSavebar(); checkPending(); renderAskBox(); applyFAQ(); if (CAP.localLoaded){ M = compute(); renderDynamic(); toast("Đang dùng dữ liệu đã lưu trên trình duyệt này."); } });
  var d = new Date(); $("m-d").value = d.getFullYear() + "-" + pad2(d.getMonth() + 1) + "-" + pad2(d.getDate());
  if (location.hash){ var tg = document.getElementById(location.hash.slice(1)); if (tg){ revealTarget(tg); setTimeout(function(){ tg.scrollIntoView(); }, 60); } }
  window.addEventListener("hashchange", function(){ var id = location.hash.slice(1), tg2 = id && document.getElementById(id); if (tg2) revealTarget(tg2); else if (id.indexOf("clip-") === 0 && typeof clpDeep === "function"){ clpDeep(id.slice(5)); window.scrollTo(0, 0); } });
}
init();
