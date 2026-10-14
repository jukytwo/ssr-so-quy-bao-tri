# -*- coding: utf-8 -*-
"""HE QUA PHAP LY: mot nguon chu duy nhat cho bao cao day du, ban tom tat, anh A4, Excel, dashboard,
file Phan loai nguyen nhan, file Hoi dan va cong van. Sua o day roi dung lai tat ca san pham.

Khung dung chung: Van de (dau hieu), Tinh trang (da ro / cho chung minh / hieu qua thap / theo doi),
He qua (neu da ro; neu khong chung minh duoc).
Can cu: Nghi dinh 339/2026/ND-CP (ky va hieu luc 26/08/2026, thay Nghi dinh 16/2022/ND-CP), Dieu 61;
Quy che quan ly, su dung nha chung cu kem Thong tu 05/2024/TT-BXD: Dieu 16, khoan 5 Dieu 19, khoan 2 Dieu 26;
Quy che thu chi tai chinh SSR: Dieu 6.1.f, Dieu 10.1; Luat Nha o 2023: khoan 4 Dieu 153.
Khong neu ten ca nhan. Khong dung ky hieu mui ten."""

LG_TITLE = "Hệ quả pháp lý"
LG_SUB = "Điều gì chắc chắn phải xử lý, điều gì phụ thuộc chứng từ của Ban quản trị"

ND339 = "Nghị định 339/2026/NĐ-CP"
QC05 = "Quy chế kèm Thông tư 05/2024/TT-BXD"

# ---------------------------------------------------------------- tinh trang phap ly cua tung dau hieu
# key: (nhan, mau chu, mau nen) theo nghia: do = da ro, cam = cho chung minh, vang = hieu qua thap, navy = theo doi
LG_ST = {"ro": ("Đã rõ", "#A93434", "#F8E3E3"),
         "cho": ("Chờ chứng minh", "#C55A11", "#FCE9DC"),
         "hq": ("Hiệu quả thấp", "#8A6100", "#FBF3D9"),
         "td": ("Theo dõi", "#1F3864", "#E6ECF5")}

LG_IFLAB = {"ro": "Nếu không có chứng từ", "cho": "Nếu không chứng minh được", "hq": "Nếu tiếp diễn", "td": "Nếu sai khác"}
# nhan cua nhanh thu nhat: nhom cho chung minh doc thanh hai nhanh "Neu chung minh duoc" / "Neu khong chung minh duoc"
LG_HQLAB = {"ro": "", "cho": "Nếu chứng minh được", "hq": "", "td": "Hiện tại"}
# id: (tinh trang, he qua, neu khong chung minh duoc)
LG_F = {
 "F01": ("ro",
         "Chắc chắn phải khắc phục: nộp đủ chứng từ sáu khoản chi được hoàn ứng. Thuộc diện phạt 50 – 60 triệu đồng (khoản 3 Điều 61 Nghị định 339/2026/NĐ-CP) và là căn cứ bãi nhiệm thành viên chịu trách nhiệm.",
         "Phần không có chứng từ hoặc không tới đúng nhà thầu phải bồi hoàn quỹ (Điều 10.1 Quy chế thu chi); có dấu hiệu chiếm đoạt thì chuyển cơ quan điều tra."),
 "F02": ("ro",
         "Chắc chắn phải chuyển toàn bộ số dư và các khoản thu khu vực chung về tài khoản quỹ (khoản 4 Điều 153 Luật Nhà ở 2023). Thuộc diện phạt 50 – 60 triệu đồng và là căn cứ bãi nhiệm.",
         "Khoản nào trong 1,40 tỷ đã chi không có hợp đồng, báo giá, nghiệm thu hợp lệ thì phải bồi hoàn quỹ."),
 "F03": ("cho",
         "Có kế hoạch được Hội nghị thông qua hoặc văn bản trên 50% chủ sở hữu đồng ý, cùng danh mục, hóa đơn, thiết bị kiểm đếm được, giá sát thị trường, mã số thuế của Thép Quang, thì chỉ còn lỗi trả trước 100%.",
         "Không có văn bản cho phép là chi vượt thẩm quyền (Điều 9.2), thuộc diện phạt 50 – 60 triệu đồng; không chứng minh được hàng hóa thì 705,8 triệu phải bồi hoàn quỹ, là căn cứ bãi nhiệm; có dấu hiệu chiếm đoạt thì chuyển cơ quan điều tra."),
 "F04": ("cho",
         "Ngân hàng xác nhận đủ số dư tại ngày gần nhất, không cầm cố, không phong tỏa thì coi như đã giải trình xong.",
         "Thiếu so với 127,5 tỷ là vấn đề nghiêm trọng nhất: báo ngay ngân hàng và cơ quan công an; Ban quản trị chịu trách nhiệm bồi thường."),
 "F05": ("cho",
         "Có kế hoạch bảo trì được Hội nghị thông qua, hoặc văn bản lấy ý kiến trên 50% chủ sở hữu cho việc khẩn cấp trên 50 triệu (Điều 9.2), cùng 3 báo giá, thì coi như đã giải trình xong.",
         "Không có thì là chi vượt thẩm quyền (hợp đồng 1,25 tỷ gấp 25 lần mức tự quyết), thuộc diện phạt 50 – 60 triệu đồng; tạm dừng 623,3 triệu còn lại; giá cao hơn thị trường thì bồi hoàn phần chênh."),
 "F06": ("cho",
         "Có biên bản khảo sát, nghiệm thu từng hợp đồng, và hợp đồng 477,1 triệu cùng các việc trên 50 triệu nằm trong kế hoạch hoặc có trên 50% chủ sở hữu đồng ý, thì coi như đã giải trình xong.",
         "Không có thì là chi vượt Quy chế (Điều 9.2), thuộc diện phạt 50 – 60 triệu đồng; khoản trả trùng hoặc chưa nghiệm thu phải bồi hoàn."),
 "F07": ("cho",
         "Phần chi ngoài quy trình của quỹ đã rõ ở F02. Có văn bản cho phép theo Điều 9.2, 3 báo giá, nghiệm thu từng hợp đồng và Thành Công không có quan hệ với người duyệt thì coi như đã giải trình xong phần còn lại.",
         "Chia nhỏ hợp đồng, không có báo giá hoặc có quan hệ với người duyệt thì phần chênh giá phải bồi hoàn và là căn cứ bãi nhiệm."),
 "F08": ("cho",
         "Có văn bản cho phép theo Điều 9.2, phụ lục phát sinh ký trước khi thanh toán và biên bản quyết toán thì coi như đã giải trình xong.",
         "Không có thì 67,1 triệu là trả vượt không căn cứ, phải bồi hoàn quỹ."),
 "F09": ("cho",
         "Phạm vi quảng cáo thu hẹp hoặc cách tính thuế khác, có văn bản chứng minh, thì coi như đã giải trình xong.",
         "Không giải trình được thì khoảng 182,2 triệu mỗi năm là thiệt hại của quỹ; người quyết định việc ký lại phải giải trình trước Hội nghị nhà chung cư và bồi thường nếu có lỗi."),
 "F10": ("hq",
         "Không phải căn cứ để phạt; Ban quản trị giải trình trước Hội nghị nhà chung cư và chào lãi suất tối thiểu ba ngân hàng từ lần gửi tới.",
         "Vẫn để tiền ở kỳ hạn ngắn hoặc tài khoản thanh toán sau khi đã được nhắc là căn cứ để Hội nghị đánh giá khi bầu lại Ban quản trị."),
 "F11": ("cho",
         "Có biên bản công bố tài khoản tại Hội nghị nhà chung cư và đủ tối thiểu ba thành viên đồng chủ tài khoản thì coi như đã giải trình xong.",
         "Không có thì vi phạm Điều 3.1.a Quy chế thu chi; buộc công khai tài khoản và bổ sung đồng chủ tài khoản."),
 "F12": ("cho",
         "Có báo cáo kiểm toán năm 2024, 2025 và các bản công khai đã niêm yết thì coi như đã giải trình xong.",
         "Không có thì vi phạm Điều 6.1.g, h và 8.8 Quy chế thu chi; không công khai thuộc diện phạt 50 – 60 triệu đồng, không báo cáo Hội nghị về thu chi thuộc diện phạt 10 – 20 triệu đồng (Điều 61 Nghị định 339/2026/NĐ-CP)."),
 "F13": ("cho",
         "Giải thích được ký hiệu TQ và ngày ký thực tế của hợp đồng thì coi như đã giải trình xong.",
         "Nếu một đầu mối soạn hợp đồng cho nhiều nhà thầu thì thành dấu hiệu xung đột lợi ích, cần kê khai theo mục III.11 công văn."),
 "F14": ("cho",
         "Có xác nhận công nợ của Schindler và chứng từ trả phí từ đúng tài khoản quỹ thì coi như đã giải trình xong.",
         "Trả từ tài khoản vận hành là dùng sai nguồn; nếu đang nợ phí, Ban quản trị chịu trách nhiệm về gián đoạn bảo trì và tiền phạt chậm trả nếu có."),
 "F15": ("cho",
         "Có đăng ký tách người lập và người duyệt lệnh, đủ ba chữ ký theo Điều 6.3.b thì coi như đã giải trình xong.",
         "Một người vừa lập vừa duyệt là vi phạm Điều 3.1.a và 6.3.b Quy chế thu chi, thuộc diện quản lý kinh phí bảo trì không đúng quy định."),
 "F16": ("td",
         "Chưa phát sinh sai; nếu hợp đồng đúng như thông báo thì là cải thiện.",
         "Hợp đồng khác thông báo, hoặc tiền lãi không về đủ tài khoản quỹ, thì thành dấu hiệu mới với cùng hệ quả như nhóm chờ chứng minh."),
}

# ---------------------------------------------------------------- thang he qua (ba nac)
LG_LADDER = [
    dict(k="ro", name="Đã rõ trên sao kê", c="#A93434", t="#F8E3E3",
         what="986,9 triệu qua tài khoản vận hành; 1,71 tỷ khu vực chung ngoài quỹ; 1,40 tỷ chi ngoài quy trình (F01, F02).",
         lines=["Chắc chắn phải khắc phục: đưa toàn bộ tiền khu vực chung về tài khoản quỹ, có chứng từ cho từng khoản đã chi.",
                "Thuộc diện phạt Ban quản trị 50 – 60 triệu đồng, kèm buộc bồi hoàn khoản sử dụng sai (khoản 3 Điều 61 Nghị định 339/2026/NĐ-CP).",
                "Là căn cứ để Hội nghị nhà chung cư xem xét bãi nhiệm thành viên chịu trách nhiệm (điểm c khoản 2 Điều 8 Quy chế hoạt động Ban quản trị; khoản 2 Điều 26 Quy chế kèm Thông tư 05/2024/TT-BXD)."]),
    dict(k="cho", name="Chờ Ban quản trị chứng minh", c="#C55A11", t="#FCE9DC",
         what="705,8 triệu thiết bị; 127,5 tỷ tiền gửi; phí bảo trì thang máy; chi vượt trần 500 triệu; giữ xe, quảng cáo, kiểm toán, lệnh chi.",
         lines=["Nghĩa vụ chứng minh thuộc Ban quản trị: mọi khoản dùng kinh phí bảo trì phải có sổ sách, hóa đơn, chứng từ (Điều 6.1.f Quy chế thu chi).",
                "Có chứng từ hợp lệ thì dấu hiệu được xóa.",
                "Không chứng minh được sau khi đã được yêu cầu bằng văn bản thì khoản đó phải bồi hoàn quỹ (Điều 10.1 Quy chế thu chi) và bị coi là vi phạm đã rõ."]),
    dict(k="hs", name="Trách nhiệm hình sự", c="#1F3864", t="#E6ECF5",
         what="Chưa có khoản nào.",
         lines=["Chỉ đặt ra khi có chứng cứ chiếm đoạt tài sản; do cơ quan điều tra xác định.",
                "Trên sao kê chưa có dữ kiện như vậy: không rút tiền mặt, không có khoản chuyển cho cá nhân."]),
]

# ban gon cua thang he qua (anh A4, dashboard tren dien thoai): cung y, it chu hon
LG_LADDER_S = {
    "ro": ["Phải khắc phục: đưa tiền khu vực chung về quỹ, có chứng từ từng khoản.",
           "Phạt Ban quản trị 50 – 60 triệu đồng, buộc bồi hoàn (Điều 61 Nghị định 339/2026/NĐ-CP).",
           "Căn cứ bãi nhiệm thành viên chịu trách nhiệm (khoản 2 Điều 8 Quy chế hoạt động BQT)."],
    "cho": ["Ban quản trị phải chứng minh bằng chứng từ (Điều 6.1.f Quy chế thu chi).",
            "Có chứng từ hợp lệ thì coi như đã giải trình xong.",
            "Không có thì bồi hoàn quỹ (Điều 10.1) và thành vi phạm đã rõ."],
    "hs": ["Chỉ khi có chứng cứ chiếm đoạt tài sản.",
           "Chưa có dữ kiện: không rút tiền mặt, không chuyển cho cá nhân."],
}
LG_BAI_S = [("Căn cứ", "Đã có: thành viên vi phạm Quy chế thu chi (khoản 2 Điều 8 Quy chế hoạt động BQT; khoản 2 Điều 26 Quy chế)."),
            ("Thủ tục", "Đơn của tối thiểu 50% đại diện chủ sở hữu căn hộ để họp Hội nghị bất thường (Điều 16)."),
            ("BQT không họp", "UBND cấp xã tổ chức trong 30 ngày (khoản 5 Điều 16)."),
            ("Khi nào dùng", "Hết hạn 15 ngày trả lời công văn mà không khắc phục; cố tình kéo dài quá 14 ngày làm việc là căn cứ theo khoản 6 Điều 7 Nội quy.")]
ROAD4_S = ("Kiến nghị, bãi nhiệm", "Kiến nghị xử lý theo Nghị định 339/2026/NĐ-CP; đơn 50% đại diện chủ sở hữu để họp bất thường, xem xét bãi nhiệm.")

# ---------------------------------------------------------------- hinh thuc xu ly
LG_FORMS_H = ["Hình thức", "Nội dung, mức", "Căn cứ", "Ai quyết định"]
LG_FORMS = [
    ("Khắc phục bắt buộc", "Đưa tiền về đúng tài khoản quỹ; công khai, báo cáo Hội nghị nhà chung cư; bồi hoàn số tiền sử dụng không đúng quy định.",
     "Khoản 4 Điều 153 Luật Nhà ở 2023; biện pháp khắc phục hậu quả tại Điều 61 Nghị định 339/2026/NĐ-CP", "Cơ quan có thẩm quyền; Hội nghị nhà chung cư"),
    ("Phạt tiền Ban quản trị", "50 – 60 triệu đồng: quản lý, sử dụng kinh phí bảo trì không đúng quy định, hoặc không công khai việc sử dụng. 10 – 20 triệu đồng: không báo cáo Hội nghị về thu, chi kinh phí bảo trì.",
     "Khoản 3, khoản 2 Điều 61 Nghị định 339/2026/NĐ-CP", "Cơ quan nhà nước có thẩm quyền xử phạt"),
    ("Bồi thường", "Thành viên chi sai mục đích, chiếm dụng kinh phí, sai phạm chứng từ, hoặc ra quyết định vượt quyền gây thiệt hại.",
     "Điều 10.1 Quy chế thu chi; khoản 5 Điều 19 Quy chế kèm Thông tư 05/2024/TT-BXD", "Thỏa thuận hoặc tòa án"),
    ("Bãi nhiệm", "Thành viên vi phạm quy chế hoạt động hoặc quy chế thu, chi tài chính; hoặc có đơn đề nghị của tối thiểu 50% chủ sở hữu căn hộ.",
     "Khoản 2 Điều 26, Điều 16 Quy chế kèm Thông tư 05/2024/TT-BXD; khoản 2 Điều 8 Quy chế hoạt động Ban quản trị; khoản 6 Điều 7 Nội quy", "Hội nghị nhà chung cư bất thường; UBND cấp xã công nhận người thay"),
    ("Hình sự", "Chỉ khi có chứng cứ chiếm đoạt tài sản.", "Bộ luật Hình sự", "Cơ quan điều tra, tòa án"),
]

# ---------------------------------------------------------------- dieu kien bai nhiem
LG_BAI_H = ["Điều kiện", "Căn cứ", "Tại SSR hiện nay"]
# (dieu kien, can cu, nhan tinh trang, khoa mau: ok = da co, no = chua co, na = buoc sau, ghi chu)
LG_BAI = [
    ("Có căn cứ: thành viên vi phạm quy chế thu, chi tài chính", "Khoản 2 Điều 26 Quy chế; điểm c khoản 2 Điều 8 Quy chế hoạt động Ban quản trị", "Đã có", "ok",
     "Ba vi phạm đã rõ trên sao kê; cần xác định ai lập, ai duyệt các lệnh chi (hồ sơ số 14 trong danh mục)."),
    ("Hoặc: đơn đề nghị bãi nhiệm của tối thiểu 50% chủ sở hữu căn hộ", "Khoản 2 Điều 26 Quy chế", "Chưa có", "no", ""),
    ("Hoặc: Ban quản trị cố tình kéo dài việc giải quyết quyền lợi chính đáng của cư dân quá 14 ngày làm việc; chủ sở hữu có quyền công khai đề nghị tạm dừng hoạt động, bãi miễn", "Khoản 6 Điều 7 Nội quy", "Chờ hết hạn", "na", ""),
    ("Triệu tập Hội nghị nhà chung cư bất thường: đơn của tối thiểu 50% đại diện chủ sở hữu căn hộ đã nhận bàn giao", "Điều 16 Quy chế", "Chưa có", "no", ""),
    ("Hội nghị hợp lệ: tối thiểu 50% đại diện chủ sở hữu tham dự, hoặc 75% số người đã ký đơn nếu họp theo đơn", "Khoản 3 Điều 16 Quy chế", "Bước sau", "na", ""),
    ("Ban quản trị không tổ chức: UBND cấp xã tổ chức trong 30 ngày", "Khoản 5 Điều 16 Quy chế", "Khi cần", "na", ""),
    ("Biểu quyết theo đa số; UBND cấp xã công nhận người thay thế", "Quy chế kèm Thông tư 05/2024/TT-BXD", "Bước sau", "na", ""),
]
LG_BAI_END = "Căn cứ để bãi nhiệm đã có; thủ tục chưa đủ. Nên dùng khi hết hạn 15 ngày trả lời công văn mà Ban quản trị không trả lời hoặc không khắc phục; nếu Ban quản trị cố tình kéo dài quá 14 ngày làm việc, Nội quy cho chủ sở hữu quyền công khai đề nghị bãi miễn (khoản 6 Điều 7)."

# ---------------------------------------------------------------- nhan dinh (moi cau mot dong, chep nguyen van o moi san pham)
LG_ND = ["Ba vi phạm đã rõ là việc đã xảy ra: chứng từ bổ sung chỉ cho biết tiền đi đâu, không xóa được việc tiền quỹ đi sai tài khoản.",
         "Với nhóm này, khắc phục là bắt buộc, Ban quản trị thuộc diện bị phạt 50 – 60 triệu đồng, và đây là căn cứ để Hội nghị nhà chung cư xem xét bãi nhiệm thành viên chịu trách nhiệm.",
         "Với nhóm chờ chứng minh, nghĩa vụ chứng minh thuộc về Ban quản trị; khoản nào không có chứng từ hợp lệ sau khi đã được yêu cầu bằng văn bản thì phải bồi hoàn quỹ và bị coi là vi phạm đã rõ.",
         "Trách nhiệm hình sự chỉ đặt ra khi có chứng cứ chiếm đoạt; đến nay chưa có dữ kiện nào như vậy.",
         "Căn cứ bãi nhiệm đã có nhưng thủ tục cần đơn của tối thiểu 50% đại diện chủ sở hữu căn hộ, nên dùng sau khi hết hạn 15 ngày trả lời công văn."]
LG_ND_LABEL = "NHẬN ĐỊNH · HỆ QUẢ PHÁP LÝ"

LG_NOTE = ("Nghị định 339/2026/NĐ-CP ký và có hiệu lực ngày 26/08/2026, thay Nghị định 16/2022/NĐ-CP; hành vi xảy ra trước ngày này áp dụng quy định có lợi hơn cho bên vi phạm; "
           "thời hiệu xử phạt 2 năm; mức phạt nêu trên là của tổ chức (Ban quản trị). Đây là khung hệ quả theo quy định; việc xử lý cụ thể do Hội nghị nhà chung cư và cơ quan có thẩm quyền quyết định.")
LG_SRC = ("Nghị định 339/2026/NĐ-CP ngày 26/08/2026 (Điều 61); Quy chế quản lý, sử dụng nhà chung cư kèm Thông tư 05/2024/TT-BXD (Điều 16, khoản 5 Điều 19, khoản 2 Điều 26); "
          "Quy chế thu chi tài chính (Điều 6.1.f, Điều 10.1); Quy chế hoạt động Ban quản trị (khoản 2 Điều 8); Nội quy nhà chung cư (khoản 6 Điều 7); Luật Nhà ở 2023 (khoản 4 Điều 153).")

# ---------------------------------------------------------------- he qua theo tang (khoi Hieu dung van de) va theo tang ket luan
KM_HQ = {"ok": ("Chưa có căn cứ để xử lý hình sự.", "Chưa có căn cứ hình sự"),
         "vp": ("Chắc chắn phải khắc phục; thuộc diện phạt 50 – 60 triệu đồng theo Nghị định 339/2026/NĐ-CP và là căn cứ bãi nhiệm thành viên chịu trách nhiệm.",
                "Phải khắc phục, thuộc diện phạt, căn cứ bãi nhiệm"),
         "ct": ("Không phải căn cứ để phạt, nhưng Ban quản trị phải giải trình trước Hội nghị.", "Không phạt, phải giải trình"),
         "hs": ("Không có chứng từ thì phải bồi hoàn quỹ và bị coi là vi phạm đã rõ; có dấu hiệu chiếm đoạt thì chuyển cơ quan điều tra.", "Không có chứng từ thì bồi hoàn")}
LG_VD = {"r": "Chắc chắn phải khắc phục; thuộc diện phạt 50 – 60 triệu đồng (khoản 3 Điều 61 Nghị định 339/2026/NĐ-CP); là căn cứ bãi nhiệm thành viên chịu trách nhiệm (điểm c khoản 2 Điều 8 Quy chế hoạt động Ban quản trị; khoản 2 Điều 26 Quy chế kèm Thông tư 05/2024/TT-BXD).",
         "o": "Có chứng từ hợp lệ thì coi như đã giải trình xong; không chứng minh được sau khi đã được yêu cầu bằng văn bản thì phải bồi hoàn quỹ (Điều 10.1 Quy chế thu chi) và chuyển lên nhóm đã rõ.",
         "g": "Không có căn cứ xử lý; chưa có dữ kiện về chiếm đoạt."}

# ---------------------------------------------------------------- lo trinh buoc 4 (dung chung)
ROAD4 = ("Kiến nghị, hội nghị, bãi nhiệm",
         "Nếu không được đáp ứng: kiến nghị UBND cấp xã, Sở Xây dựng xử lý theo Nghị định 339/2026/NĐ-CP; gom đơn của tối thiểu 50% đại diện chủ sở hữu để triệu tập Hội nghị nhà chung cư bất thường, xem xét bãi nhiệm (Điều 16, Điều 26 Quy chế).")

# ---------------------------------------------------------------- he qua theo nguyen nhan (file Phan loai, file Hoi dan)
CAUSE_HQ = {1: "Sửa quy trình, thuê kế toán hoặc kiểm toán, quyết toán lại. Vi phạm đã rõ vẫn thuộc diện phạt Ban quản trị (Điều 61 Nghị định 339/2026/NĐ-CP); Hội nghị cân nhắc bãi nhiệm nếu không khắc phục.",
            2: "Điều chỉnh sổ sách, hoàn phần chênh nếu có, rút kinh nghiệm bằng văn bản; thường không tới mức phạt hay bãi nhiệm.",
            3: "Bồi hoàn, bồi thường (Điều 10.1 Quy chế thu chi); kiểm toán đột xuất; Hội nghị nhà chung cư xem xét bãi nhiệm (khoản 2 Điều 26 Quy chế kèm Thông tư 05/2024/TT-BXD); có chiếm đoạt thì chuyển cơ quan điều tra."}

# ---------------------------------------------------------------- he qua cua 10 van de trong file Hoi dan (theo thu tu ISS)
LG_ISS = [
    "Đã rõ việc tiền đi sai tài khoản: phải khắc phục, thuộc diện phạt 50 – 60 triệu đồng, là căn cứ bãi nhiệm. Khoản nào không có chứng từ hoặc không tới đúng nhà thầu phải bồi hoàn quỹ.",
    "Chênh lệch 123,1 triệu không giải thích được thì phải bồi hoàn quỹ; báo cáo sai số liệu là sai phạm chứng từ theo Điều 10.1 Quy chế thu chi.",
    "Đã rõ: phải chuyển toàn bộ số dư và khoản thu về tài khoản quỹ, thuộc diện phạt 50 – 60 triệu đồng, là căn cứ bãi nhiệm.",
    "Khoản chi không có báo giá, nghiệm thu hợp lệ phải bồi hoàn; chia nhỏ hợp đồng hoặc có quan hệ với người duyệt là căn cứ bãi nhiệm.",
    "Không có phụ lục ký trước khi thanh toán thì 67,1 triệu phải bồi hoàn quỹ.",
    "Không có văn bản cho phép là chi vượt thẩm quyền, thuộc diện phạt 50 – 60 triệu đồng; không chứng minh được hàng hóa thì 705,8 triệu phải bồi hoàn, là căn cứ bãi nhiệm; có dấu hiệu chiếm đoạt thì chuyển cơ quan điều tra.",
    "Chi vượt trần hoặc không có nghiệm thu thì thuộc diện phạt, khoản trả trùng phải bồi hoàn; trả phí định kỳ từ tài khoản vận hành là dùng sai nguồn.",
    "Thiếu so với 127,5 tỷ thì báo ngay ngân hàng và cơ quan công an; riêng việc gửi kỳ hạn ngắn không bị phạt nhưng phải giải trình trước Hội nghị.",
    "Không giải trình được thì khoảng 182,2 triệu mỗi năm là thiệt hại của quỹ; người quyết định ký lại phải giải trình và bồi thường nếu có lỗi.",
    "Không cung cấp sao kê sau khi được yêu cầu là không công khai việc sử dụng kinh phí bảo trì, thuộc diện phạt 50 – 60 triệu đồng; né tránh là dấu hiệu của nhóm (3).",
    "Không có kế hoạch được thông qua hoặc ý kiến chủ sở hữu thì mỗi khoản là chi vượt thẩm quyền theo Điều 9.2, thuộc diện phạt 50 – 60 triệu đồng và là căn cứ bãi nhiệm; khoản nào giá cao hơn thị trường hoặc chưa nghiệm thu phải bồi hoàn.",
]

# tinh trang phap ly cua 11 van de trong file Hoi dan (van de gop nhieu dau hieu lay muc nang nhat)
LG_ISS_ST = ["ro", "cho", "ro", "cho", "cho", "cho", "cho", "cho", "cho", "cho", "cho"]

# ---------------------------------------------------------------- trich y cac quy dinh (phu luc C bao cao day du)
LG_QUOTES = [
    ("Khoản 3, khoản 2 Điều 61 Nghị định 339/2026/NĐ-CP (hiệu lực 26/08/2026)",
     "Phạt tiền từ 50.000.000 đồng đến 60.000.000 đồng đối với Ban quản trị nhà chung cư quản lý, sử dụng kinh phí bảo trì không đúng quy định hoặc không công khai việc sử dụng kinh phí bảo trì; "
     "từ 10.000.000 đồng đến 20.000.000 đồng khi không báo cáo Hội nghị nhà chung cư về việc thu, chi kinh phí bảo trì; biện pháp khắc phục gồm buộc công khai, buộc báo cáo Hội nghị và buộc bồi hoàn số tiền sử dụng không đúng quy định (trích ý)."),
    ("Khoản 2 Điều 26 Quy chế quản lý, sử dụng nhà chung cư (Thông tư 05/2024/TT-BXD)",
     "Bãi nhiệm thành viên Ban quản trị khi Ban quản trị không báo cáo kết quả hoạt động cho Hội nghị nhà chung cư hoặc không hoạt động sau khi được bầu; thành viên không thực hiện nhiệm vụ, vắng mặt 03 tháng liên tiếp "
     "hoặc không dự tối thiểu 30% số cuộc họp; thành viên vi phạm quy chế hoạt động hoặc quy chế thu, chi tài chính; thành viên bị xử phạt vi phạm hành chính hoặc bị truy cứu trách nhiệm hình sự; "
     "hoặc có đơn đề nghị của tối thiểu 50% chủ sở hữu căn hộ (trích ý)."),
    ("Điều 16 Quy chế quản lý, sử dụng nhà chung cư",
     "Hội nghị nhà chung cư bất thường xem xét miễn nhiệm, bãi nhiệm và bầu thay thế thành viên Ban quản trị; hội nghị hợp lệ khi có tối thiểu 50% đại diện chủ sở hữu căn hộ đã nhận bàn giao tham dự, "
     "hoặc 75% số người đã có đơn nếu họp theo đơn; Ban quản trị không tổ chức mà có đơn của tối thiểu 50% đại diện chủ sở hữu thì UBND cấp xã tổ chức trong 30 ngày (trích ý)."),
    ("Khoản 5 Điều 19 Quy chế quản lý, sử dụng nhà chung cư",
     "Các quyết định của Ban quản trị nếu vượt quá quyền hạn quy định tại Điều 147 của Luật Nhà ở thì không có giá trị pháp lý; trường hợp gây thiệt hại đến quyền và lợi ích hợp pháp của các tổ chức, "
     "cá nhân thì các thành viên Ban quản trị phải chịu trách nhiệm bồi thường theo quy định của pháp luật."),
]


# CSS dung chung cho ban PDF (bao cao day du, ban tom tat)
LG_CSS = """
.thq { margin-top:7pt; padding:5pt 8pt; border-radius:4pt; background:#fff; border:0.8pt dashed var(--tc,#1F3864); font-size:8.9pt; line-height:1.42; text-align:left; break-inside:avoid; }
.thq b { font-family:'Be Vietnam Pro',sans-serif; font-size:7.2pt; font-weight:800; letter-spacing:.06em; color:#fff; background:var(--tc,#1F3864); border-radius:5pt; padding:0.8pt 5pt; margin-right:5pt; vertical-align:1pt; }
.tier .its .thq { grid-column:1 / -1; margin:6pt 8pt 7pt 8pt; }
.lgp { font-family:'Be Vietnam Pro',sans-serif; font-size:7.3pt; font-weight:800; border-radius:7pt; padding:0.8pt 6pt; white-space:nowrap; border:0.7pt solid; }
.lgl { display:grid; grid-template-columns:repeat(3,1fr); gap:6pt; margin:4pt 0 7pt 0; break-inside:avoid; }
.lgc { border:0.8pt solid #cfd8e6; border-top:4pt solid var(--c); border-radius:0 0 5pt 5pt; padding:6pt 8pt 7pt 8pt; background:var(--t); }
.lgc .n { font-family:'Be Vietnam Pro',sans-serif; font-size:9.6pt; font-weight:800; color:var(--c); line-height:1.25; }
.lgc .w { font-family:'Be Vietnam Pro',sans-serif; font-size:7.6pt; color:#3d4656; margin-top:2pt; line-height:1.35; }
.lgc ul { margin:4pt 0 0 0; padding:0; list-style:none; }
.lgc li { position:relative; padding-left:9pt; font-size:8.6pt; line-height:1.4; margin:2.2pt 0; text-align:left; }
.lgc li:before { content:''; position:absolute; left:0; top:4.6pt; width:4pt; height:4pt; border-radius:50%; background:var(--c); }
.fhq { font-size:8.8pt; line-height:1.42; }
.fhq .if { display:block; margin-top:2.5pt; color:#3d4656; }
.fhq > i { font-style:normal; font-weight:700; color:#1F3864; }
.fhq .if i { font-style:normal; font-weight:700; color:#1F3864; }
.bst { font-family:'Be Vietnam Pro',sans-serif; font-size:7.3pt; font-weight:800; border-radius:7pt; padding:0.8pt 6pt; white-space:nowrap; }
.bst.ok { background:#f7e3e3; color:#A93434; } .bst.no { background:#EDEDED; color:#404040; } .bst.na { background:#E6ECF5; color:#1F3864; }
.lgend { font-size:9.2pt; font-weight:700; color:#16294A; background:#FBF3DF; border-left:3pt solid #C8992F; border-radius:0 4pt 4pt 0; padding:5pt 9pt; margin:5pt 0 6pt 0; line-height:1.45; text-align:left; break-inside:avoid; }
.lgnote { font-family:'Be Vietnam Pro',sans-serif; font-size:7.6pt; color:#5b6474; line-height:1.45; margin-top:4pt; }
"""


def lg_pill(E, fid):
    """Nhan tinh trang phap ly dang vien mau cho ban PDF."""
    st = LG_F[fid][0]; lab, c, bg = LG_ST[st]
    return f'<span class="lgp" style="color:{c};background:{bg};border-color:{c}">{E(lab)}</span>'


def lg_pill_st(E, st):
    """Nhan tinh trang theo khoa tinh trang (ro, cho, hq, td)."""
    lab, c, bg = LG_ST[st]
    return f'<span class="lgp" style="color:{c};background:{bg};border-color:{c}">{E(lab)}</span>'


def lg_pdf_parts(E, table):
    """(thang he qua, bang hinh thuc xu ly, bang dieu kien bai nhiem) cho ban PDF; table la ham cua report_kit."""
    ladder = '<div class="lgl">' + "".join(
        f'<div class="lgc" style="--c:{x["c"]};--t:{x["t"]}"><div class="n">{E(x["name"])}</div><div class="w">{E(x["what"])}</div><ul>'
        + "".join(f"<li>{E(l)}</li>" for l in x["lines"]) + "</ul></div>" for x in LG_LADDER) + "</div>"
    forms = table(LG_FORMS_H, [[f"<b>{E(a)}</b>", E(b), E(c), E(d)] for a, b, c, d in LG_FORMS],
                  cls=["", "", "", ""], widths=["15%", "40%", "27%", "18%"], esc=False, tcls="cp")
    bai = table(LG_BAI_H, [[E(a), E(b), f'<span class="bst {k}">{E(lab)}</span>' + (f" {E(nt)}" if nt else "")] for a, b, lab, k, nt in LG_BAI],
                cls=["", "", ""], widths=["44%", "20%", "36%"], esc=False, tcls="cp")
    return ladder, forms, bai


def lg_of(fid):
    """(nhan tinh trang, mau chu, mau nen, he qua, dong neu, nhan dong neu, khoa tinh trang) cua mot dau hieu."""
    st, hq, hq_if = LG_F[fid]
    lab, c, t = LG_ST[st]
    return lab, c, t, hq, hq_if, LG_IFLAB[st], st


def lg_hq_text(fid):
    """He qua cua mot dau hieu kem nhan nhanh (neu co), dung cho o van ban thuan (Excel)."""
    st, hq, _ = LG_F[fid]; lab = LG_HQLAB[st]
    return f"{lab}: {hq}" if lab else hq


def lg_lines_all():
    """Moi cau hien thi cua khung, dung de kiem tra dong bo va chan ky hieu mui ten."""
    out = [LG_TITLE, LG_SUB, LG_BAI_END, LG_NOTE, LG_SRC, ROAD4[0], ROAD4[1]] + LG_ND + LG_ISS + list(CAUSE_HQ.values()) + list(LG_VD.values())
    for v in LG_F.values(): out += [v[1], v[2]]
    for x in LG_LADDER: out += [x["name"], x["what"]] + x["lines"]
    for r in LG_FORMS: out += list(r)
    for r in LG_BAI: out += [r[0], r[1], r[2], r[4]]
    for a, b in LG_QUOTES: out += [a, b]
    for a, b in KM_HQ.values(): out += [a, b]
    for v in LG_LADDER_S.values(): out += v
    for a, b in LG_BAI_S: out += [a, b]
    out += list(ROAD4_S)
    return out


def _check():
    import re
    txt = " ".join(lg_lines_all())
    assert "→" not in txt and "->" not in txt and "⇒" not in txt
    assert sorted(LG_F) == [f"F{i:02d}" for i in range(1, 17)]
    assert len(LG_ISS) == 11 and len(LG_ISS_ST) == 11 and set(LG_ISS_ST) <= set(LG_ST)
    for need in ("50 – 60 triệu đồng", "10 – 20 triệu đồng", "khoản 2 Điều 26", "Điều 10.1", "26/08/2026", "Nghị định 16/2022/NĐ-CP"):
        assert need in txt, need
    # khong neu ten ca nhan: chi dung vai tro
    assert not re.search(r"\b(ông|bà)\s+[A-ZĐ]", txt)


_check()
