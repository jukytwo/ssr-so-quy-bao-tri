# -*- coding: utf-8 -*-
"""Duong di cua tien, ban tuong tac cho web app (14/10/2026): moi truong hop dat hai lan "Theo Quy che" va "Thuc te tren sao ke",
moi buoc co ket luan Dung, Sai, Can giai trinh, Chua ro, kem so sanh tung buoc. Noi dung lay tu luudo.py (ban so do tinh), khong them so moi."""
import luudo as L

def tr(v): return L.tr_(v)
_inc, _exp = L._A["inc7784"], L._A["exp7784"]

# v: sai (trai Quy che, Luat) | giai (can giai trinh) | ro (chua ro, cho chung tu) | dung
# lane: danh sach nut va mui noi; nut: dict(t, s, items, v); noi: dict(lab, v, n) - n la so buoc trong bang so sanh
CASES = [
 dict(k="c1", code="F01", amt="986,9 triệu", title="986,9 triệu qua tài khoản của chính Ban quản trị, chưa rõ người nhận cuối",
  lede="Tiền quỹ không đi thẳng tới đơn vị làm bảo trì mà vòng qua một tài khoản do chính các thành viên Ban quản trị đứng tên, rồi mới chi ra.",
  rule=[dict(t="Quỹ bảo trì", s="TK 116605084999, VietinBank"), dict(lab="Chuyển thẳng, có hồ sơ"), dict(t="Đơn vị làm bảo trì", s="Nhận tiền thẳng từ quỹ")],
  real=[dict(t="Quỹ bảo trì", s="TK 116605084999 · luôn còn ít nhất 4,22 tỷ"),
        dict(lab="23/12/2025: 986.910.176 đồng, hoàn ứng một lần", v="sai", n=1),
        dict(t="TK vận hành 118002976372", s="6 thành viên Ban quản trị đồng đứng tên · chưa có sao kê", v="sai", n=2),
        dict(lab="Đã chi trước 6 lần, 29/08 – 23/12/2025", v="sai", n=3),
        dict(t="6 khoản chi", s="Thang máy, phòng cháy, máy phát điện · chưa biết người nhận", v="ro", n=4)],
  steps=[("Tiền từ quỹ đi tới đâu", "Chuyển thẳng cho đơn vị làm bảo trì", "986,9 triệu vào tài khoản vận hành của Ban quản trị ngày 23/12/2025", "sai", "Quy chế thu chi Điều 7.2"),
         ("Ai đứng tên tài khoản nhận", "Công ty quản lý vận hành đứng tên", "6 thành viên Ban quản trị đồng đứng tên tài khoản 118002976372", "sai", "Quy chế thu chi Điều 3.2.a"),
         ("Ứng và hoàn ứng", "Tạm ứng trong hạn mức 10 triệu, hoàn cuối mỗi tháng", "Ứng từ 29/08, gộp hoàn một lần ngày 23/12, gấp khoảng 20 lần hạn mức", "sai", "Quy chế thu chi Điều 7.4"),
         ("Tiền cuối cùng trả cho ai", "Có sao kê và chứng từ cho từng khoản", "Chưa có sao kê tài khoản nhận, chưa biết người nhận cuối", "ro", "Quy chế thu chi Điều 6.1.f"),
         ("Báo cáo có khớp số đã chuyển", "Bảng chi phí khớp số tiền đã chuyển", "Báo cáo 03-2026/BC-BQTSSR chỉ giải thích 863,8 triệu, lệch 123,1 triệu", "giai", "Báo cáo 03-2026/BC-BQTSSR"),
         ("Có cần ứng trước không", "Quỹ chi trực tiếp khi đủ hồ sơ", "Quỹ luôn còn ít nhất 4,22 tỷ, không có lý do phải ứng từ tài khoản khác", "giai", "")],
  need="Căn cứ của lệnh chuyển ngày 23/12/2025; sao kê TK 118002976372 từ 01/08/2025; hợp đồng, hóa đơn, nghiệm thu của 6 khoản."),
 dict(k="c2", code="F02, F07", amt="1,71 tỷ", title="1,71 tỷ tiền khu vực chung nằm ngoài quỹ, 1,40 tỷ đã chi ngoài quy trình",
  lede="Tiền cho thuê khu vực chung lẽ ra vào quỹ bảo trì, nhưng nằm ở tài khoản thu dịch vụ và được chi ra mà không qua quy trình của quỹ.",
  rule=[dict(t="Thu khu vực chung", s="Quảng cáo, mặt bằng, kệ"), dict(lab="Nộp vào quỹ"), dict(t="Quỹ bảo trì", s="TK 116605084999"),
        dict(lab="Kế hoạch, 3 báo giá, nghiệm thu"), dict(t="Chi đúng quy trình", s="Trên 50 triệu cần văn bản cho phép, công khai thu chi")],
  real=[dict(t="3 nguồn thu khu vực chung", items=[("Chicilon Media · quảng cáo", tr(_inc["Thu khu vực chung – quảng cáo (Chicilon)"])),
                                                     ("Viễn thông ACT · mặt bằng", tr(_inc["Thu khu vực chung – thuê mặt bằng (ACT)"])),
                                                     ("Hưng Thái · kệ quảng cáo", tr(_inc["Thu khu vực chung – standee (Hưng Thái)"]))]),
        dict(lab="1,71 tỷ vào tài khoản ngoài quỹ", v="sai", n=1),
        dict(t="TK 117002997784", s="Thu dịch vụ, nằm ngoài quỹ · 24/07/2025 nhận thêm 260,9 triệu từ quỹ · còn 120,3 triệu ngày 31/05/2026", v="giai", n=2),
        dict(lab="Chi 1,40 tỷ không qua quy trình của quỹ", v="sai", n=3),
        dict(t="Người nhận tiền", items=[("Thành Công · 4 hợp đồng", tr(_exp["Chi sửa chữa, mua sắm – Thành Công"])),
                                         ("Khởi Sáng Việt · giữ xe", tr(_exp["Chi hệ thống giữ xe – Khởi Sáng Việt"])),
                                         ("KTECH · camera", tr(_exp["Chi hệ thống camera – KTECH"])),
                                         ("Nộp thuế · 9 lệnh", tr(_exp["Nộp thuế"]))], v="ro", n=4)],
  steps=[("Tiền khu vực chung vào đâu", "Nộp vào tài khoản quỹ bảo trì", "1,71 tỷ vào TK 117002997784, nằm ngoài quỹ", "sai", "Khoản 4 Điều 153 Luật Nhà ở 2023"),
         ("Tiền đã vào quỹ", "Giữ trong quỹ", "24/07/2025: 260,9 triệu đã vào quỹ bị chuyển sang TK 117002997784, 8 ngày sau, với lý do trả nhầm", "giai", ""),
         ("Cách chi", "Theo kế hoạch bảo trì, 3 báo giá, nghiệm thu", "Chi 1,40 tỷ không qua quy trình của quỹ", "sai", "Quy chế thu chi Điều 6.3"),
         ("Hợp đồng trên 50 triệu", "Có văn bản cho phép của chủ sở hữu", "Cả 6 hợp đồng đều trên 50 triệu, chưa thấy văn bản cho phép", "ro", "Quy chế thu chi Điều 9.2"),
         ("Công khai", "Công khai thu chi cho cư dân", "Chưa thấy công khai thu chi của tài khoản này", "ro", "Quy chế thu chi Điều 6.1.g"),
         ("Nộp thuế", "Kê khai, nộp thuế khoản thu cho thuê", "9 lệnh nộp thuế, 187,4 triệu", "dung", "")],
  need="Căn cứ mở TK 117002997784; hợp đồng, báo giá, nghiệm thu của Thành Công, Khởi Sáng Việt, KTECH; chuyển số dư về quỹ."),
 dict(k="c3", code="F03", amt="705,8 triệu", title="705,8 triệu trả trọn cho Thép Quang, chưa có văn bản cho phép và danh mục hàng hóa",
  lede="Quy chế đòi sáu bước trước khi trả hết tiền. Trên sao kê, tiền đi một bước: ký hợp đồng rồi 16 ngày sau trả đủ 100%.",
  rule=[dict(t="Cho phép", s="Hội nghị thông qua hoặc trên 50% chủ sở hữu đồng ý"), dict(lab=""), dict(t="3 báo giá"), dict(lab=""), dict(t="Hợp đồng"), dict(lab=""),
        dict(t="Tạm ứng"), dict(lab=""), dict(t="Nghiệm thu"), dict(lab=""), dict(t="Trả phần còn lại")],
  real=[dict(t="Quỹ bảo trì", s="TK 116605084999"),
        dict(lab="Ký 08/04/2026, chưa thấy văn bản cho phép", v="ro", n=1),
        dict(t="Hợp đồng 080426/HDDV/BQT TQ", s="Cùng ký hiệu BQT TQ với hợp đồng 221025 của Thành Công", v="giai", n=6),
        dict(lab="24/04/2026: trả 100% = 705.769.875 đồng, 16 ngày sau ký", v="sai", n=3),
        dict(t="Công ty Thép Quang", s="TK 2666677777 · chưa xác minh được mã số thuế", v="ro", n=5),
        dict(lab="Giao hàng", v="ro", n=4),
        dict(t="Thiết bị khu vực chung", s="Chưa có danh mục, hóa đơn, biên bản giao nhận", v="ro", n=4)],
  steps=[("Cho phép chi", "Hội nghị thông qua hoặc trên 50% chủ sở hữu đồng ý", "Không thấy văn bản cho phép; số tiền gấp 14 lần mức 50 triệu Ban quản trị được tự quyết, bằng 141% trần cả năm", "ro", "Quy chế thu chi Điều 9.2, 6.3.c"),
         ("Báo giá", "3 báo giá", "Chưa thấy báo giá", "ro", "Quy chế thu chi Điều 6.3.e"),
         ("Thanh toán", "Tạm ứng, nghiệm thu rồi mới trả phần còn lại", "Trả 100% ngày 24/04/2026, 16 ngày sau ký, không có đợt tạm ứng", "sai", "Quy chế thu chi Điều 6.3.b"),
         ("Hàng hóa", "Danh mục, hóa đơn, biên bản giao nhận", "Chỉ ghi chung là thiết bị khu vực sử dụng chung", "ro", ""),
         ("Nhà cung cấp", "Xác minh được thông tin, mã số thuế", "Chưa xác minh được mã số thuế của Thép Quang", "ro", "Quy chế thu chi Điều 6.1.c"),
         ("Số hợp đồng", "Mỗi nhà thầu một ký hiệu riêng", "Ký hiệu BQT TQ trùng với hợp đồng 221025 của Thành Công", "giai", "")],
  need="Văn bản cho phép; hợp đồng, danh mục thiết bị, hóa đơn, biên bản giao nhận, 3 báo giá; mã số thuế Thép Quang; kiểm đếm thiết bị."),
 dict(k="c4", code="F03, F05, F07, F15", amt="2,15 tỷ", title="Tháng 4/2026: ba hợp đồng 2,15 tỷ ký trong ba ngày, chi trước khi nghiệm thu",
  lede="Ba hợp đồng lớn ký dồn trong ba ngày, gấp hơn 4 lần trần sửa chữa đột xuất 500 triệu của cả năm, rồi tạm ứng 50% tới 100% trước khi thi công.",
  rule=[dict(t="Lấy ý kiến chủ sở hữu", s="Từng hợp đồng trên 50 triệu"), dict(lab=""), dict(t="Báo giá, dự toán"), dict(lab=""), dict(t="Ký hợp đồng"), dict(lab=""),
        dict(t="Thi công, nghiệm thu"), dict(lab=""), dict(t="Thanh toán theo tiến độ")],
  real=[dict(t="06/04/2026", s="Thành Công ký HĐ 06042026 · 193,7 triệu"),
        dict(lab="1 ngày", v="ro", n=1),
        dict(t="07/04/2026", s="HNB ký hợp đồng cấp nước sinh hoạt · 1.246,6 triệu · số hợp đồng mang ngày 24/03/2026", v="giai", n=4),
        dict(lab="1 ngày", v="ro", n=1),
        dict(t="08/04/2026", s="Thép Quang ký HĐ 080426 · 705,8 triệu"),
        dict(lab="14/04, 11:26 và 11:28: hai lệnh chi cách nhau 2 phút", v="giai", n=2),
        dict(t="Tạm ứng trước thi công", items=[("HNB · 50%, từ quỹ", "623,3 triệu"), ("Thành Công · 60%, từ TK 117002997784", "116,2 triệu")], v="sai", n=3),
        dict(lab="24/04/2026", v="sai", n=3),
        dict(t="Thép Quang", s="Trả 100% · 705,8 triệu · HNB còn 623,3 triệu sẽ chi tiếp", v="giai", n=5)],
  steps=[("Lấy ý kiến chủ sở hữu", "Văn bản cho phép cho từng hợp đồng", "Ba hợp đồng 2,15 tỷ ký trong ba ngày, không thấy lấy ý kiến chủ sở hữu", "ro", "Quy chế thu chi Điều 9.2"),
         ("Duyệt lệnh chi", "Tách người lập và người duyệt, đủ 3 chữ ký", "Hai lệnh chi trên hai tài khoản lập cách nhau 2 phút ngày 14/04/2026", "giai", "Quy chế thu chi Điều 6.3.b"),
         ("Tạm ứng", "Chi theo tiến độ, sau nghiệm thu", "Tạm ứng 50% tới 100% trước khi thi công, nghiệm thu", "sai", "Quy chế thu chi Điều 6.3.b"),
         ("Ngày hợp đồng", "Số và ngày hợp đồng khớp nhau", "Số hợp đồng HNB mang ngày 24/03/2026, ghi ký 07/04/2026", "giai", ""),
         ("Chi tiếp", "Chỉ chi khi nghiệm thu đạt", "HNB còn 623,3 triệu sẽ chi tiếp, trong khi cư dân phản ánh ống nước vẫn bể, dột nhiều nơi", "giai", "")],
  need="Văn bản cho phép từng hợp đồng; báo giá, dự toán, nghiệm thu; bảo hành cấp nước của HNB; nhật ký duyệt lệnh ngày 14/04/2026."),
 dict(k="c5", code="F04, F16", amt="127,5 tỷ", title="127,5 tỷ tiền gửi sau tái tục chưa có xác nhận, sao kê dừng ở 31/05/2026",
  lede="Tiền gốc còn đủ tới 31/05/2026. Sau mốc này sao kê dừng lại, nên đoạn đáo hạn và tái tục tiền gửi chưa nhìn thấy được.",
  rule=[dict(t="Tiền gửi đáo hạn"), dict(lab=""), dict(t="Sao kê ghi nhận đáo hạn, tái tục"), dict(lab=""), dict(t="Hợp đồng và xác nhận ngân hàng"), dict(lab=""), dict(t="Công khai cho cư dân")],
  real=[dict(t="Quỹ ngày 31/05/2026", s="127,15 tỷ: tiền gửi 125 tỷ, tài khoản thanh toán 2,15 tỷ", v="dung", n=6),
        dict(lab="Bốn khoản tiền gửi", v="ro", n=4),
        dict(t="Tiền gửi", items=[("VietinBank 45 tỷ · 12 tháng", "đáo hạn 20/08/2026"), ("VietinBank 15 tỷ · 3 tháng", "tái tục"),
                                  ("VietinBank 5 tỷ · gửi 29/08/2025", "không có dấu vết sau đó"), ("Agribank 60 tỷ · gửi lại 22/08/2025", "không có dấu vết sau đó")]),
        dict(lab="06 – 08/2026: đáo hạn khoảng 110 tỷ, sao kê dừng ở 31/05/2026", v="ro", n=1),
        dict(t="Tái tục 127,5 tỷ", s="5 hợp đồng, lãi 8% một năm, theo thông báo 15/09/2026 · khoản 2,5 tỷ mở mới chưa rõ nguồn", v="ro", n=2)],
  steps=[("Sao kê", "Sao kê đầy đủ tới ngày in", "Sao kê in ngày 04/09/2026 nhưng dừng ở 31/05/2026, không thấy dòng đáo hạn và tái tục", "ro", "Quy chế thu chi Điều 6.1.g"),
         ("Tái tục", "Hợp đồng và giấy xác nhận của ngân hàng", "127,5 tỷ sau tái tục chưa có hợp đồng và giấy xác nhận", "ro", "Quy chế thu chi Điều 3.1.a"),
         ("Khoản mở mới", "Rõ nguồn tiền", "Khoản 2,5 tỷ gửi mới chưa rõ lấy từ đâu", "ro", ""),
         ("Dấu vết từng khoản", "Mỗi khoản có dòng đáo hạn, lãi trên sao kê", "Khoản 5 tỷ và 60 tỷ không có dấu vết từ ngày gửi tới 31/05/2026", "ro", ""),
         ("Lãi suất", "Lãi đúng biểu, rõ điều kiện", "Lãi 8% cao hơn biểu 12 tháng tại quầy khoảng 5,9%, cần xem điều kiện kèm theo", "giai", ""),
         ("Tiền gốc", "Tiền gốc còn đủ", "127,15 tỷ còn ngày 31/05/2026; lãi 33/33 tháng khớp tới từng đồng", "dung", "")],
  need="Sao kê ba tài khoản từ 01/06/2026; hợp đồng tiền gửi và giấy xác nhận tại quầy của VietinBank, Agribank."),
]
VL = {"sai": "Sai", "giai": "Cần giải trình", "ro": "Chưa rõ", "dung": "Đúng"}
for c in CASES:
    c["steps"] = [dict(q=a, rule=b, real=d, v=v, ref=r) for a, b, d, v, r in c["steps"]]
    n = len(c["steps"])
    for x in c["real"]:
        if x.get("n"): assert 1 <= x["n"] <= n, (c["k"], x)
        if x.get("items"): x["items"] = [list(i) for i in x["items"]]
    c["cnt"] = {k: sum(1 for s in c["steps"] if s["v"] == k) for k in VL}
    import json
    s = json.dumps(c, ensure_ascii=False)
    assert "→" not in s and "->" not in s
INTRO = ("Mỗi trường hợp đặt hai đường cạnh nhau: tiền lẽ ra phải đi theo Quy chế, và tiền đã đi thực tế trên sao kê. "
         "Bấm Xem tiền đi để theo đồng tiền qua từng chặng; mỗi chặng có kết luận Đúng, Sai, Cần giải trình hoặc Chưa rõ.")
if __name__ == "__main__":
    for c in CASES: print(c["k"], c["cnt"])
