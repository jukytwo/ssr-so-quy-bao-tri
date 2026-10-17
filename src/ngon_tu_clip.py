# -*- coding: utf-8 -*-
"""Loi doc va chu tren hinh cua clip (15/10/2026): dat nghi van, de nghi lam ro; ap truoc lop ngon_tu chung.
Chi dung cho clip tong 22 phut, clip tom tat 90 giay va Phan 2 (theo anh Vu); khong doi ten file clip khac."""
import ngon_tu as NT
CR = [
    # ---- 17/10/2026, an toan phap ly (anh Vu: "dung tu chuyen nghiep, an toan, trang trong"); ap truoc, lop 2 cua ngon_tu chay sau ----
    ("Chưa dấu hiệu nào đủ căn cứ để xếp vào nhóm có chủ đích, nhưng 4 dấu hiệu chưa loại trừ được khả năng này.", "Bốn dấu hiệu còn lại cần thêm hồ sơ để làm rõ nguyên nhân."),
    ("Nhóm ba, lỡ tay có chủ đích: cùng một kiểu lặp lại, tiền đi qua tài khoản trung gian, hợp đồng chia nhỏ hoặc trả trước toàn bộ, né tránh chứng từ.",
     "Nhóm ba, cần hồ sơ để làm rõ nguyên nhân: cùng một kiểu lặp lại, tiền đi qua tài khoản trung gian, hợp đồng chia nhỏ hoặc trả trước toàn bộ, chứng từ chưa được cung cấp."),
    ("Nhóm ba, lỡ tay có chủ đích: cùng kiểu sai lặp lại, tiền đi qua tài khoản trung gian, hợp đồng chia nhỏ hoặc trả trước toàn bộ, né tránh chứng từ.",
     "Nhóm ba, cần hồ sơ để làm rõ nguyên nhân: cùng một kiểu lặp lại, tiền đi qua tài khoản trung gian, hợp đồng chia nhỏ hoặc trả trước toàn bộ, chứng từ chưa được cung cấp."),
    ("Trách nhiệm hình sự chỉ đặt ra khi có chứng cứ chiếm đoạt, do cơ quan điều tra xác định; đến nay chưa có dữ kiện như vậy.",
     "Trách nhiệm hình sự, nếu có, chỉ do cơ quan tiến hành tố tụng xem xét; clip không đánh giá nội dung này."),
    ("Bãi nhiệm, khi không khắc phục, không có văn bản cho phép, hoặc né tránh cung cấp chứng từ.",
     "Việc bãi nhiệm thuộc thẩm quyền Hội nghị nhà chung cư, được xem xét khi việc khắc phục, văn bản cho phép hoặc chứng từ không được cung cấp theo yêu cầu."),
    ("Tiền quỹ bảo trì có mất không, và Ban quản trị đã làm đúng những gì.", "Sao kê quỹ bảo trì cho thấy gì, và những điểm nào đã kiểm tra và khớp."),
    ("Phần này trả lời câu hỏi đầu tiên: tiền quỹ có mất không, và tiền đã đi qua những tài khoản nào.", "Phần này trả lời câu hỏi đầu tiên: sao kê cho thấy gì, và tiền đã đi qua những tài khoản nào."),
    ("lưu đồ cho thấy đường nào đúng, đường nào sai.", "lưu đồ đặt đường tiền theo Quy chế cạnh đường tiền thực tế trên sao kê."),
    ("đường đỏ là chỗ làm trái Quy chế hoặc Luật.", "đường đỏ là chỗ chưa phù hợp Quy chế hoặc Luật, cần giải trình."),
    ("Hội nghị có ba phương án, xét riêng từng thành viên: giữ, xem xét thêm, hoặc bãi nhiệm.", "Hội nghị có ba phương án theo Quy chế, xét riêng từng thành viên: tiếp tục, xem xét thêm, hoặc bãi nhiệm."),
    ("Mức nặng nhất; cần ít nhất 2 trong 3 dấu hiệu rõ.", "Chỉ đánh giá được khi có đủ hồ sơ; kết luận thuộc cơ quan có thẩm quyền."),
    ("(3) Lỡ tay có chủ đích", "(3) Cần hồ sơ làm rõ"),
    ("(2) Lỡ tay thật", "(2) Sơ suất ghi chép"),
    ("Mức nhẹ nhất, thường không tới mức phạt hay bãi nhiệm.", "Mức nhẹ nhất, thường chỉ cần điều chỉnh và rút kinh nghiệm."),
    ("Cũng cần ghi nhận những việc Ban quản trị đã làm đúng.", "Cũng cần ghi nhận những điểm đã kiểm tra và khớp."),
    ("9 dấu hiệu thuộc nhóm thiếu năng lực: làm sai quy trình hoặc quản lý tiền kém, không thấy ai hưởng lợi.", "9 dấu hiệu có thể do quy trình chưa chặt hoặc quản lý tiền chưa hiệu quả, chưa thấy ai hưởng lợi."),
    ("Với vi phạm đã rõ: khắc phục là bắt buộc, Ban quản trị thuộc diện phạt 50 đến 60 triệu đồng theo khoản 3 Điều 61 Nghị định 339 năm 2026, và đây là căn cứ để Hội nghị nhà chung cư xem xét bãi nhiệm.",
     "Với điểm nghi vấn trên sao kê: cần giải trình và khắc phục; nếu cơ quan có thẩm quyền xác định là vi phạm, khung phạt Ban quản trị là 50 đến 60 triệu đồng theo khoản 3 Điều 61 Nghị định 339 năm 2026, và Hội nghị nhà chung cư có thể xem xét bãi nhiệm."),
    ("trái Điều 7.2, 7.4 và 3.2.a.", "chưa thấy căn cứ theo Điều 7.2, 7.4 và 3.2.a."),
    ("Clip này trả lời ba câu: tiền có mất không, sai ở đâu, và Hội nghị cần quyết định gì.", "Clip này trả lời ba câu: tiền đi đâu, điểm nào cần làm rõ, và Hội nghị cần quyết định gì."),
    ("Trước hết, tiền có mất không?", "Trước hết, sao kê cho thấy điều gì?"),
    ("Chưa thấy mất: 198 giao dịch của ba tài khoản khớp số dư tới từng đồng.", "198 giao dịch của ba tài khoản khớp số dư tới từng đồng."),
    ("Vì vậy, câu hỏi không phải là tiền có biến mất hay không, mà là tiền có đi đúng đường và đúng thẩm quyền hay không.",
     "Nhưng số dư khớp chưa cho biết tiền chi có đúng giá trị hợp đồng, và quỹ có nhận đúng hàng hóa, dịch vụ hay không. Điều đó cần Ban quản trị làm rõ bằng hợp đồng, nghiệm thu, kể cả hậu kiểm."),
    ("Nhưng sao kê cũng cho thấy tiền đi sai đường ở nhiều chỗ.", "Sao kê cũng cho thấy nhiều chỗ tiền chưa đi theo quy trình của Quy chế."),
    ("Đường xanh là đường đúng theo Quy chế, đường đỏ là đường tiền đã đi.", "Đường xanh là đường theo Quy chế, đường đỏ là đường tiền đã đi trên sao kê."),
    ("không có thì thành vi phạm và phải bồi hoàn quỹ.", "không có thì cư dân có cơ sở đề nghị bồi hoàn quỹ."),
    ("Thước đo thứ hai là nguyên nhân: cái sai do đâu mà có.", "Thước đo thứ hai là nguyên nhân: mỗi dấu hiệu có thể do đâu mà có."),
    ("Nhóm hai, lỡ tay thật: sai một lần, sai kỹ thuật, chứng từ gốc đúng và sửa được ngay.", "Nhóm hai, lỡ tay thật: chỉ một lần, lỗi kỹ thuật, chứng từ gốc đầy đủ và sửa được ngay."),
    ("Tiền chưa mất: 198 giao dịch khớp tới từng đồng, tiền gốc còn 127,15 tỷ.", "198 giao dịch khớp số dư tới từng đồng, số dư 127,15 tỷ; nhưng như vậy chưa đủ để đánh giá tiền chi có đúng giá trị."),
    ("Nhưng tiền đi sai đường ở năm chỗ.", "Có năm điểm cần Ban quản trị làm rõ."),
    ("Tiền không biến mất, tiền gốc còn đủ", "Số dư khớp sao kê, chưa đủ căn cứ đánh giá thiệt hại"),
    ("Ghi nhận việc làm đúng", "Những điểm đã kiểm tra và khớp"),
    ("Những việc Ban quản trị đã làm đúng", "Những điểm đã kiểm tra và khớp"),
    ("Đúng **Điều 7.2** Quy chế.", "Phù hợp **Điều 7.2** Quy chế."),
    ("Ba điều đã rõ, hai điều chờ văn bản", "Ba điều thể hiện trên sao kê, hai điều chờ văn bản"),
    ("Hai vấn đề đã rõ, ba vấn đề chờ chứng minh", "Hai vấn đề thể hiện trên sao kê, ba vấn đề cần chứng từ"),
    ("Hai vấn đề đã rõ, ba vấn đề cần làm rõ", "Hai vấn đề thể hiện trên sao kê, ba vấn đề cần chứng từ"),
    ("Nguyên nhân: cái sai do đâu mà có", "Nguyên nhân: dấu hiệu có thể do đâu"),
    ("Sai một lần, sai kỹ thuật; chứng từ gốc đúng; sửa ngay khi được hỏi.", "Một lần, lỗi kỹ thuật; chứng từ gốc đầy đủ; sửa ngay khi được hỏi."),
    ("Sai quy trình, quản lý tiền kém; **không thấy ai hưởng lợi**.", "Quy trình chưa chặt, quản lý tiền chưa hiệu quả; **chưa thấy ai hưởng lợi**."),
    ("Điều gì chắc chắn phải xử lý, điều gì phụ thuộc chứng từ", "Điều gì cần giải trình ngay, điều gì phụ thuộc chứng từ"),
    ("Quỹ bảo trì: **sai ở đâu**, tới mức nào, Hội nghị quyết định gì", "Quỹ bảo trì: **điểm nào cần làm rõ**, tới mức nào, Hội nghị quyết định gì"),
    ("Tiền có mất không", "Sao kê cho thấy gì"),
    ("tiền gốc còn", "số dư theo sao kê"),
]
def soften(t):
    if not isinstance(t, str): return t
    for a, b in CR:
        if a in t and not (a in b and b in t): t = t.replace(a, b)
    return NT.soften(t)
def walk(o):
    if isinstance(o, str): return soften(o)
    if isinstance(o, list): return [walk(x) for x in o]
    if isinstance(o, tuple): return tuple(walk(x) for x in o)
    if isinstance(o, dict): return {k: walk(v) for k, v in o.items()}
    return o
