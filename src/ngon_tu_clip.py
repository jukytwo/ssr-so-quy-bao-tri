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
# ---- 17/10/2026 (phien Sao ke): lop cuoi cho clip, chay sau ngon_tu; trang trong, khong suy dien, che tai luon co dieu kien ----
CR3 = [
    ("Không có lệnh rút tiền mặt, không có khoản chuyển cho cá nhân.", "Trên sao kê, không có lệnh rút tiền mặt, không có khoản chuyển cho cá nhân."),
    ("không có lý do phải ứng trước từ tài khoản khác.", "nên cần làm rõ lý do phải ứng trước từ tài khoản khác."),
    ("không vào quỹ như khoản 4 Điều 153 Luật Nhà ở 2023 quy định.", "chưa nộp vào tài khoản quỹ theo khoản 4 Điều 153 Luật Nhà ở 2023."),
    ("và phải chuyển toàn bộ số dư về quỹ.", "và đề nghị chuyển toàn bộ số dư về quỹ."),
    ("dù theo luật tài khoản quỹ mới là tài khoản đúng.", "trong khi theo Luật Nhà ở, khoản thu này cần nộp vào tài khoản quỹ."),
    ("Xây mới trên phần sở hữu chung không phải bảo trì, phải do Hội nghị quyết định.", "Xây mới trên phần sở hữu chung có thể không thuộc phạm vi bảo trì; cần làm rõ việc này đã được Hội nghị quyết định hay chưa."),
    ("Cả ba đều không qua kế hoạch bảo trì, ba báo giá và nghiệm thu như tiền quỹ phải có.", "Với cả ba, chưa thấy hồ sơ kế hoạch bảo trì, ba báo giá và nghiệm thu theo quy trình chi tiền quỹ."),
    ("không qua kế hoạch bảo trì, ba báo giá và nghiệm thu của quỹ.", "chưa thấy hồ sơ kế hoạch bảo trì, ba báo giá và nghiệm thu theo quy trình của quỹ."),
    ("và 187,4 triệu nộp thuế, không qua quy trình của quỹ.", "và 187,4 triệu nộp thuế, chưa qua quy trình chi của quỹ."),
    ("Rõ nhất là tháng 4/2026", "Đáng chú ý là tháng 4/2026"),
    ("Không thấy lấy ý kiến chủ sở hữu theo Điều 9.2.", "Chưa thấy văn bản lấy ý kiến chủ sở hữu theo Điều 9.2."),
    ("cho thấy người lập và người duyệt lệnh chưa tách riêng.", "cần làm rõ việc tách riêng người lập và người duyệt lệnh."),
    ("tiền lãi bỏ lỡ khoảng", "chênh lệch tiền lãi ước tính khoảng"),
    ("Chưa thấy dấu hiệu bất thường, nhưng chỉ nhìn sao kê tài khoản thanh toán thì chưa thể khẳng định tiền còn đủ.", "Chỉ dựa vào sao kê tài khoản thanh toán thì chưa thể xác nhận đầy đủ số tiền gửi; cần xác nhận của ngân hàng."),
    ("hồ sơ lưu thiếu, nhưng tiền về đúng người nhận và chưa thấy ai hưởng lợi.", "hồ sơ lưu thiếu, tiền về đúng người nhận theo sao kê."),
    ("hoặc quản lý tiền chưa hiệu quả, chưa thấy ai hưởng lợi.", "hoặc quản lý tiền chưa hiệu quả."),
    ("tiền về đúng người nhận, chưa thấy ai hưởng lợi.", "tiền về đúng người nhận theo sao kê."),
    ("quản lý tiền chưa hiệu quả; **chưa thấy ai hưởng lợi**.", "quản lý tiền chưa hiệu quả; **cần hồ sơ để xác nhận**."),
    ("Bốn dấu hiệu chưa loại trừ.", "Bốn dấu hiệu cần thêm hồ sơ."),
    ("Bốn dấu hiệu chưa loại trừ", "Bốn dấu hiệu cần thêm hồ sơ"),
    ("Chưa loại trừ khả năng có chủ đích", "Cần hồ sơ để làm rõ nguyên nhân"),
    ("chưa loại trừ có chủ đích", "cần hồ sơ làm rõ nguyên nhân"),
    ("chưa từng vào quỹ.", "đang nằm ngoài tài khoản quỹ."),
    ("đề nghị bồi hoàn quỹ", "đề nghị hoàn trả khoản chi về quỹ"),
    ("né tránh chứng từ.", "chứng từ chưa được cung cấp."),
    ("Điểm nghi vấn trên sao kê vẫn cần được khắc phục và có khung phạt.", "Điểm nghi vấn trên sao kê cần được giải trình, khắc phục theo Quy chế."),
    ("Nếu xác định vi phạm: phạt 50 – 60 triệu đồng, buộc bồi hoàn (Điều 61 Nghị định 339/2026/NĐ-CP).", "Khung phạt 50 – 60 triệu đồng nếu cơ quan có thẩm quyền xác định vi phạm (Điều 61 NĐ 339/2026)."),
    ("Có thể là căn cứ bãi nhiệm thành viên liên quan (khoản 2 Điều 8 Quy chế hoạt động BQT).", "Hội nghị xem xét trách nhiệm (khoản 2 Điều 8 Quy chế hoạt động)."),
    ("Chưa có dữ kiện: không rút tiền mặt, không chuyển cho cá nhân.", "Tài liệu này chỉ đối chiếu sao kê với Quy chế và Luật Nhà ở."),
    ("Không có văn bản, né tránh chứng từ; khoản không chứng minh được thì **bồi hoàn quỹ**", "Theo thẩm quyền Hội nghị, khi văn bản, chứng từ không được cung cấp; khoản không chứng minh được, cư dân có cơ sở đề nghị **hoàn trả về quỹ**"),
    ("Hai hợp đồng **trả 100%** trước nghiệm thu", "Hai hợp đồng **trả 100%** ngay sau khi ký"),
    ("Không có văn bản, chứng từ chưa được cung cấp; khoản không chứng minh được thì **bồi hoàn quỹ**", "Theo thẩm quyền Hội nghị, khi văn bản, chứng từ không được cung cấp; khoản không chứng minh được, cư dân có cơ sở đề nghị **hoàn trả về quỹ**"),
    ("đề nghị hoàn trả quỹ", "đề nghị hoàn trả khoản chi về quỹ"),
    ("4,22 tỷ, cần làm rõ lý do phải ứng trước", "4,22 tỷ, nên cần làm rõ lý do phải ứng trước"),
    ("Đề nghị khắc phục: đưa tiền khu vực chung về quỹ, có chứng từ từng khoản.", "Đề nghị đưa tiền khu vực chung về quỹ, kèm chứng từ."),
    ("Không có thì cư dân có cơ sở đề nghị hoàn trả khoản chi về quỹ (Điều 10.1).", "Không có: cư dân có cơ sở đề nghị hoàn trả về quỹ (Điều 10.1)."),
    ("Đề nghị Ban quản trị chứng minh bằng chứng từ (Điều 6.1.f Quy chế thu chi).", "Đề nghị chứng minh bằng chứng từ (Điều 6.1.f Quy chế thu chi)."),
    ("trong đó 1,40 tỷ đã chi ngoài quy trình.", "trong đó 1,40 tỷ đã chi chưa qua quy trình của quỹ."),
    ("vào tài khoản của Ban quản trị,", "vào tài khoản do Ban quản trị đứng tên,"),
]
EXACT = {"Điểm nghi vấn trên sao kê; đã chi 1,40 tỷ": "Nghi vấn trên sao kê; đã chi 1,40 tỷ", "Điểm nghi vấn trên sao kê": "Nghi vấn trên sao kê", "Đã rõ": "Trên sao kê", "Chưa có khoản nào.": "Ngoài phạm vi đánh giá.", "Bãi nhiệm": "Xem xét bãi nhiệm",
         "Khi không khắc phục": "Thuộc thẩm quyền Hội nghị", "chi ngoài quy trình": "chi chưa qua quy trình quỹ"}
def soften(t):
    if not isinstance(t, str): return t
    for a, b in CR:
        if a in t and not (a in b and b in t): t = t.replace(a, b)
    t = NT.soften(t)
    for a, b in CR3:
        if a in t and not (a in b and b in t): t = t.replace(a, b)
    return EXACT.get(t, t)
def walk(o):
    if isinstance(o, str): return soften(o)
    if isinstance(o, list): return [walk(x) for x in o]
    if isinstance(o, tuple): return tuple(walk(x) for x in o)
    if isinstance(o, dict): return {k: walk(v) for k, v in o.items()}
    return o
