/* cau moc mo dau (17/10/2026): mot cau co so, viet duoi dang cau hoi, dat ngay duoi tieu de trang dau va tung phan lon */
function hookSet(sel, html){
  var h = document.querySelector(sel); if (!h) return;
  var id = "hk-" + sel.replace(/[^a-z0-9]/gi, ""), o = document.getElementById(id); if (o) o.parentNode.removeChild(o);
  if (!html) return; var p = document.createElement("p"); p.className = "hook"; p.id = id; p.innerHTML = html; h.parentNode.insertBefore(p, h.nextSibling);
}
function renderHooks(){
  try {
    hookSet("#tong-quan .hero h1", "198 giao dịch đều khớp số dư sao kê, nhưng ngày 23/12/2025 có <b>986,9 triệu</b> tiền quỹ chuyển vào tài khoản do chính các thành viên Ban quản trị đồng đứng tên. Căn cứ nào cho khoản chuyển này?");
    hookSet("#phan-clip .pt", "Bản tóm tắt 1 phút 22 giây đi qua đủ năm điểm cần làm rõ, từ <b>986,9 triệu</b> chuyển vào tài khoản Ban quản trị tới <b>127,5 tỷ</b> tiền gửi chưa có xác nhận của ngân hàng.");
    if (D.ldx && D.ldx.cases){
      var t = {sai: 0, giai: 0, ro: 0, dung: 0}; D.ldx.cases.forEach(function(c){ for (var k in t) t[k] += (c.cnt && c.cnt[k]) || 0; });
      var n = t.sai + t.giai + t.ro + t.dung;
      if (n) hookSet("#phan-tien .pt", D.ldx.cases.length + " trường hợp, " + n + " chặng tiền đi, nhưng chỉ <b>" + t.dung + " chặng</b> khớp hồ sơ. " + (n - t.dung) + " chặng còn lại đang chờ Ban quản trị giải trình hoặc bổ sung chứng từ: đó là những chặng nào?");
    }
    if (D.q10 && typeof q10State === "function"){
      var S = q10State(), due = String(D.q10.due || "").split("-").reverse().join("/");
      hookSet("#phan-cauhoi .pt", S.got >= S.n ? "Ban quản trị đã trả lời đủ " + S.n + " câu hỏi. Câu nào kèm chứng từ, câu nào còn thiếu?" :
        "Mười câu hỏi gửi ngày 29/09/2026, hạn trả lời " + due + (S.late ? "; đã quá hạn <b>" + S.late + " ngày</b>" : "") + (S.got ? " mà Ban quản trị mới trả lời " + S.got + " trên " + S.n + " câu." : " mà Ban quản trị chưa trả lời câu nào."));
    }
  } catch (e) { }
}
