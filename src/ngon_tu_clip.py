# -*- coding: utf-8 -*-
"""Loi doc va chu tren hinh cua clip (15/10/2026): dat nghi van, de nghi lam ro; ap truoc lop ngon_tu chung.
Chi dung cho clip tong 22 phut, clip tom tat 90 giay va Phan 2 (theo anh Vu); khong doi ten file clip khac."""
import ngon_tu as NT
CR = [
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
