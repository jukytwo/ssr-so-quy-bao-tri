# -*- coding: utf-8 -*-
"""File rieng: HOI DAN de biet cai sai thuoc nguyen nhan nao (1 thieu nang luc, 2 lo tay that, 3 co y).
Ba nguyen nhan va dau hieu, cach hoi ba vong, 10 van de, bang theo doi, ban cong khai 10 cau hoi.
Nhan dien SSR, khong dung nhan dien TVN, khong neu ten ca nhan."""
import base64, os, re
os.chdir("/home/claude/ssr")
from report_kit import CSS, E, nd, table, NAVY, NAVY2, GOLD, RED, CREAM, BAND
from keymsg import km_compact_html, KMC_CSS
import legal as LG
import ketluan5 as K5

LOGO = base64.b64encode(open("crops/logo_480.png", "rb").read()).decode()
TODAY = "30/09/2026"

K = {1: ("(1) Thiếu năng lực", "k1"), 2: ("(2) Lỡ tay thật", "k2"), 3: ("(3) Lỡ tay có chủ đích", "k3")}

CAUSES = [
    (1, "Làm theo thói quen hoặc quy định cũ; không nắm Quy chế thu chi, Luật Nhà ở 2023; thiếu người có chuyên môn kế toán; hồ sơ lưu thiếu, lộn xộn.",
     "Giải thích được lý do nhưng lý do dựa trên hiểu sai quy định. Có chứng từ gốc dù chưa đầy đủ. Tiền về đúng người nhận, không ai hưởng lợi. Chấp nhận sửa khi được chỉ ra.",
     "Sửa quy trình, thuê kế toán hoặc kiểm toán, tập huấn; quyết toán lại; bầu bổ sung người có chuyên môn."),
    (2, "Sai một lần, sai kỹ thuật: nhầm tài khoản, tính trùng phí, ghi sai kỳ, gõ sai số.",
     "Chứng từ gốc đúng, cái sai chỉ nằm ở khâu ghi chép. Tự phát hiện hoặc sửa ngay khi được hỏi. Không lặp lại.",
     "Điều chỉnh sổ sách, hoàn lại phần chênh nếu có, rút kinh nghiệm bằng văn bản."),
    (3, "Cùng một kiểu sai lặp lại; tiền đi qua tài khoản trung gian; hợp đồng chia nhỏ hoặc trả trước toàn bộ; giá cao hơn thị trường.",
     "Né tránh, trả lời chung chung, không đưa chứng từ sau khi được yêu cầu bằng văn bản. Chứng từ lập sau, ngày tháng không khớp. Lời giải thích đổi qua từng lần hỏi. Có bên liên quan hưởng lợi.",
     "Yêu cầu hoàn trả, bồi thường; kiểm toán đột xuất; Hội nghị nhà chung cư xem xét miễn nhiệm; chuyển cơ quan có thẩm quyền."),
]
# huong xu ly va he qua theo nguyen nhan: lay tu legal.py de khop file Phan loai
CAUSES = [(n, a, b, LG.CAUSE_HQ[n]) for n, a, b, c in CAUSES]
RULES = ["Chỉ chốt phân loại cuối khi Ban quản trị đã trả lời bằng văn bản và được yêu cầu cung cấp chứng từ.",
         "Mặc định là (1) hoặc (2) cho tới khi có bằng chứng ngược lại.",
         "Chỉ xếp vào (3) khi có ít nhất hai trong ba dấu hiệu: cùng một kiểu sai lặp lại, có bên hưởng lợi, không đưa hoặc sửa chứng từ sau khi được yêu cầu.",
         "Dù nguyên nhân nào, khoản chi không đủ chứng từ vẫn phải làm rõ và hoàn lại quỹ, vi phạm đã rõ vẫn phải khắc phục và thuộc diện xử phạt; nguyên nhân chỉ quyết định cách xử lý trách nhiệm cá nhân.",
         "Kết luận vi phạm pháp luật thuộc về cơ quan có thẩm quyền; nhóm cư dân chỉ nêu dấu hiệu và yêu cầu giải trình."]

ROUNDS = [("Vòng 1", "Hỏi để hiểu", "Gửi bằng công văn và bản công khai",
           ["Câu hỏi mở, không quy lỗi: vì sao, căn cứ nào, ai đề xuất, ai duyệt.",
            "Câu trả lời đầu tiên là mốc để đối chiếu về sau."]),
          ("Vòng 2", "Đòi chứng từ", "Sau 15 ngày hoặc khi có trả lời",
           ["Đòi đúng tài liệu gốc: hợp đồng, báo giá, biên bản khảo sát, nghiệm thu, hóa đơn, ủy nhiệm chi, sao kê.",
            "Phân biệt (1) có chứng từ nhưng sai quy trình với (3) không có chứng từ.",
            "Không đưa chứng từ sau khi được yêu cầu bằng văn bản thì khoản đó phải bồi hoàn quỹ và thành vi phạm đã rõ (Điều 6.1.f, 10.1 Quy chế thu chi)."]),
          ("Vòng 3", "Hỏi đối chiếu", "Khi chứng từ không khớp",
           ["Đặt từng chỗ lệch cạnh lời giải thích ở vòng 1; hỏi ai chịu trách nhiệm, khắc phục thế nào.",
            "Đề nghị kiểm toán đột xuất (Quy chế Điều 8.8.b) hoặc đưa ra Hội nghị nhà chung cư.",
            "Không khắc phục thì kiến nghị xử phạt theo Nghị định 339/2026/NĐ-CP và xem xét bãi nhiệm."])]
HOWTO = ["Hỏi bằng văn bản, lưu nguyên văn câu trả lời và ngày nhận.",
         "Mỗi câu hỏi chỉ hỏi một việc, gắn với một chứng từ cụ thể.",
         "Không nêu suy đoán về động cơ trong câu hỏi; để chứng từ tự trả lời."]

# ---- 11 van de: (tieu de, su viec, quy dinh, vong1, vong2, vong3, doc (1)(2)(3), so bo, chung tu quyet dinh)
ISS = [
 dict(t="986,9 triệu hoàn ứng qua TK vận hành 118002976372",
      f="Ngày 23/12/2025 quỹ chuyển 986.910.176 đồng sang TK 118002976372 do 6 thành viên Ban quản trị đồng chủ tài khoản, ghi hoàn tạm ứng 6 khoản chi thang máy, phòng cháy, máy phát điện từ 29/08 tới 23/12/2025. Suốt thời gian này tài khoản quỹ luôn còn ít nhất 4,22 tỷ.",
      q="Quy chế Điều 7.2 (chuyển thẳng cho đơn vị bảo trì), 7.4 (tạm dùng tiền vận hành tối đa 10 triệu mỗi tháng), 3.2.a (công ty quản lý đứng tên tài khoản vận hành).",
      v1="Vì sao 6 khoản chi không chuyển thẳng từ tài khoản quỹ cho nhà thầu, khi tài khoản quỹ luôn đủ tiền? Ai đề xuất, ai duyệt việc hoàn ứng một lần 986,9 triệu?",
      v2="Sao kê TK 118002976372 từ 01/08/2025 tới nay; với từng khoản trong 6 khoản: hợp đồng, hóa đơn, biên bản nghiệm thu, ủy nhiệm chi cho nhà thầu.",
      v3="Đối chiếu ngày, số tiền 6 khoản trên sao kê tài khoản vận hành với lệnh hoàn ứng; khoản nào chi sau ngày hoàn ứng hoặc chi cho bên không phải nhà thầu thì đề nghị giải trình và hoàn lại.",
      r=["Có đủ 6 khoản chi thật cho nhà thầu, trước ngày hoàn ứng; chỉ sai ở cách đi tiền.",
         "Khó là lỡ tay: lặp lại 6 lần trong 5 tháng, tổng gấp khoảng 20 lần hạn mức.",
         "Sao kê tài khoản vận hành không có các khoản chi tương ứng, có khoản chuyển cho bên lạ, hoặc không được cung cấp sau khi yêu cầu."],
      lean=("Chưa loại trừ (3)", "k3"), codes="F01", cv="Mục I.1.a, II.2; Phụ lục 1 số 2, 3", key="Sao kê TK 118002976372 và chứng từ 6 khoản"),
 dict(t="Bảng chi phí 863,8 triệu, chênh 123,1 triệu",
      f="Phụ lục 1 báo cáo 03-2026/BC-BQTSSR ngày 15/05/2026 ghi thang máy 597.838.833, phòng cháy 261.135.900, máy phát điện 4.860.000 đồng (tổng 863.834.733 đồng), không có ngày chi, đơn vị nhận, số hợp đồng; sao kê năm 2026 không có lệnh chi tương ứng; thấp hơn khoản hoàn ứng 123.075.443 đồng.",
      q="Quy chế Điều 6.1.f (sổ sách, hóa đơn, chứng từ, quyết toán) và 6.1.g (công khai hằng tháng các khoản chi).",
      v1="Ba dòng chi này chi từ tài khoản nào, ngày nào, cho đơn vị nào? Có phải là 6 khoản đã hoàn ứng ngày 23/12/2025 không?",
      v2="Bảng kê chi tiết từng khoản (ngày, đơn vị, số hợp đồng, số hóa đơn) kèm chứng từ gốc.",
      v3="Nếu tổng khớp 986,9 triệu, vì sao báo cáo chỉ ghi 863,8 triệu? Nếu không khớp, 123.075.443 đồng chênh lệch đã chi cho việc gì?",
      r=["Bảng kê lập vội, gộp sai kỳ, nhưng chứng từ đủ và tổng khớp khi đối chiếu.",
         "Ghi thiếu một hai khoản có chứng từ, sửa ngay khi được hỏi.",
         "Không giải thích được chênh lệch, hoặc chứng từ bổ sung có ngày lập sau ngày hỏi."],
      lean=("(1) hoặc (2)", "k0"), codes="liên quan F01", cv="Mục I.2.i, II.2", key="Bảng kê chi tiết và chứng từ gốc"),
 dict(t="1,71 tỷ tiền khu vực chung không vào quỹ",
      f="Từ 07/2025 tới 05/2026, 1.707.909.092 đồng tiền quảng cáo (Chicilon Media), thuê mặt bằng (Viễn thông ACT), kệ quảng cáo (Hưng Thái) đi vào TK 117002997784 do Ban quản trị đứng tên. Riêng 260.945.454 đồng đã vào đúng tài khoản quỹ ngày 16/07/2025, 8 ngày sau bị chuyển đi với lý do trả nhầm tài khoản.",
      q="Khoản 4 Điều 153 Luật Nhà ở 2023, hiệu lực từ 01/08/2024: thu từ khai thác phần sở hữu chung phải nộp vào tài khoản kinh phí bảo trì.",
      v1="Căn cứ nào để mở TK 117002997784 và thu tiền khai thác phần sở hữu chung vào đây? Hội nghị nhà chung cư có thông qua không?",
      v2="Nghị quyết hoặc biên bản cho phép; văn bản của Chicilon Media về việc trả nhầm; các thông báo công khai thu chi của tài khoản này.",
      v3="Khi nào chuyển số dư (120,3 triệu ngày 31/05/2026) và các khoản thu sau đó về tài khoản quỹ; quyết toán các khoản đã chi.",
      r=["Cho rằng quy định cũ vẫn áp dụng, chưa cập nhật Luật Nhà ở 2023; có công khai thu chi; đồng ý chuyển về quỹ.",
         "Khó là lỡ tay: việc chuyển 260,9 triệu ra khỏi quỹ là thao tác chủ động, có ghi lý do.",
         "Không có nghị quyết, không công khai thu chi, không chuyển về quỹ sau khi được chỉ ra quy định."],
      lean=("(1) Thiếu năng lực", "k1"), codes="F02", cv="Mục I.1.b, III.2; Phụ lục 1 số 10, 11", key="Nghị quyết cho phép và thông báo công khai thu chi"),
 dict(t="1,40 tỷ chi ngoài quy trình; 4 hợp đồng liên tiếp của Thành Công",
      f="Từ TK 117002997784 đã chi 1.400.199.548 đồng: Thành Công 856.792.068 đồng qua 4 hợp đồng từ 15/09/2025 tới 06/04/2026, Khởi Sáng Việt 356.399.800 đồng, KTECH 187.007.680 đồng.",
      q="Quy chế Điều 6.1.b (theo kế hoạch bảo trì được thông qua), 9.2 (việc trên 50 triệu cần trên 50% chủ sở hữu đồng ý), 6.3.a (đấu thầu công khai), 6.3.b (nghiệm thu), 6.3.e (3 báo giá cho khoản trên 10 triệu).",
      v1="Các hạng mục này có trong kế hoạch bảo trì được Hội nghị nhà chung cư thông qua không? Cả 6 hợp đồng đều trên 50 triệu, ai cho phép? Thành Công, Khởi Sáng Việt, KTECH được chọn thế nào?",
      v2="Với từng hợp đồng: dự toán, 3 báo giá, hợp đồng, biên bản nghiệm thu, hóa đơn, ảnh hiện trạng trước và sau.",
      v3="Vì sao Thành Công nhận 4 hợp đồng liên tiếp trong 7 tháng, hai hợp đồng được trả 100% trước nghiệm thu (350,7 triệu sau 3 ngày ký); gộp lại có vượt ngưỡng phải đấu thầu không; Thành Công có quan hệ với người duyệt không.",
      r=["Có báo giá, nghiệm thu nhưng bỏ bước đấu thầu vì không nắm quy trình; giá sát thị trường.",
         "Chỉ thiếu vài giấy tờ, bổ sung được ngay, nội dung khớp.",
         "Không có báo giá cạnh tranh, hợp đồng chia nhỏ dưới ngưỡng, giá cao hơn thị trường, Thành Công có quan hệ với người duyệt."],
      lean=("Chưa loại trừ (3)", "k3"), codes="F07", cv="Mục I.1.c; Phụ lục 1 số 9", key="3 báo giá và biên bản nghiệm thu từng hợp đồng"),
 dict(t="Hệ thống giữ xe, Khởi Sáng Việt: trả vượt 67,1 triệu",
      f="Hợp đồng 18KSVSSR08082025 ngày 09/08/2025. Ngày 15/08/2025 tạm ứng 40% là 115.720.000 đồng, tức giá trị hợp đồng khoảng 289,3 triệu. Ngày 11/12/2025 trả phần còn lại 240.679.800 đồng. Tổng đã trả 356.399.800 đồng, vượt khoảng 67.099.800 đồng (23,2%).",
      q="Quy chế Điều 6.3.b (nghiệm thu trước khi thanh toán), 6.3.e (3 báo giá), 9.2 (hợp đồng 289,3 triệu gấp 5,8 lần mức Ban quản trị được tự quyết); chi từ TK 117002997784, không qua quy trình của quỹ.",
      v1="Giá trị hợp đồng 18KSVSSR08082025 là bao nhiêu? Vì sao tổng thanh toán cao hơn giá trị suy ra từ khoản tạm ứng 40%?",
      v2="Hợp đồng, phụ lục phát sinh nếu có, biên bản khảo sát trước khi làm, biên bản nghiệm thu, bảng quyết toán, hóa đơn.",
      v3="Phụ lục phát sinh ký trước hay sau khi thi công; khối lượng phát sinh có trong biên bản nghiệm thu không; ai duyệt phần tăng thêm.",
      r=["Có phụ lục phát sinh hợp lệ nhưng không công bố; khâu duyệt phát sinh lỏng.",
         "Ghi nhầm tỷ lệ tạm ứng trong nội dung chuyển khoản (thực tế khoảng 32,5%); hợp đồng gốc đúng tổng 356,4 triệu.",
         "Không có phụ lục, hoặc phụ lục lập sau khi đã thanh toán; khối lượng phát sinh không có trong nghiệm thu."],
      lean=("(2) Lỡ tay thật, nếu có phụ lục", "k2"), codes="F08", cv="Mục I.2.e; Phụ lục 1 số 9", key="Hợp đồng, phụ lục phát sinh, nghiệm thu, quyết toán"),
 dict(t="705,8 triệu trả Thép Quang một lần",
      f="Hợp đồng 080426 với Thép Quang ngày 08/04/2026; ngày 24/04/2026 quỹ trả đủ 705.769.875 đồng một lần, 16 ngày sau khi ký. Nội dung chỉ ghi thiết bị khu vực sử dụng chung; báo cáo của Ban quản trị ghi thiết bị điện, nước, Intercom. Giá trước thuế 653.490.625 đồng.",
      q="Quy chế Điều 9.2 (Ban quản trị tự quyết việc khẩn cấp tối đa 50 triệu; trên mức đó cần trên 50% chủ sở hữu đồng ý; trần 500 triệu mỗi năm), 6.3.c (kế hoạch được Hội nghị thông qua), 6.1.c, 6.3.b, 6.3.e.",
      v1="Ai cho phép chi 705,8 triệu, gấp 14 lần mức Ban quản trị được tự quyết: kế hoạch nào của Hội nghị, hay văn bản lấy ý kiến chủ sở hữu nào? Mua những thiết bị gì, số lượng bao nhiêu, lắp ở đâu? Vì sao trả 100% một lần, không tạm ứng và nghiệm thu như các hợp đồng khác?",
      v2="Kế hoạch bảo trì được thông qua hoặc văn bản trên 50% chủ sở hữu đồng ý; hợp đồng, danh mục thiết bị kèm đơn giá, hóa đơn giá trị gia tăng, biên bản giao nhận, lắp đặt, 3 báo giá; ngành nghề đăng ký và mã số thuế của Thép Quang.",
      v3="Đối chiếu đơn giá với giá thị trường; kiểm tra thực tế thiết bị đã lắp; đối chiếu ngày giao hàng với ngày thanh toán.",
      r=["Có danh mục, hóa đơn, thiết bị thật, giá sát thị trường; chỉ sai ở việc trả trước và không đấu thầu.",
         "Khó là lỡ tay: khoản chi đơn lẻ lớn nhất, trả trọn một lần.",
         "Không có danh mục chi tiết, thiết bị không tìm thấy hoặc ít hơn hóa đơn, đơn giá cao hơn thị trường."],
      lean=("Chưa loại trừ (3)", "k3"), codes="F03", cv="Mục I.2.a, II.3; Phụ lục 1 số 4", key="Danh mục thiết bị, hóa đơn, biên bản giao nhận"),
 dict(t="Thang máy Schindler: phí định kỳ vắng, sửa chữa dày",
      f="Quỹ đã trả Schindler Việt Nam 806.917.257 đồng; 14 hợp đồng sửa chữa trong khoảng 7 tháng, riêng hợp đồng EID/FR/18062025REV01 có giá trị suy ra 477,1 triệu; 3 hợp đồng mới tạm ứng 50%, phần còn lại khoảng 298,8 triệu chưa thấy trả. Phí bảo trì định kỳ 57.538.800 đồng mỗi tháng không còn xuất hiện trên tài khoản quỹ từ 21/01/2025. Bảng chi phí 15/05/2026 ghi 597,8 triệu cho thang máy nhưng không thấy trên sao kê năm 2026.",
      q="Quy chế Điều 6.3.b (nghiệm thu), 9.2 (việc trên 50 triệu cần trên 50% chủ sở hữu đồng ý; trần sửa chữa đột xuất 500 triệu mỗi năm); quy định kiểm định thang máy định kỳ.",
      v1="Từ 21/01/2025 phí bảo trì định kỳ được trả từ đâu, hay đang nợ? Ba hợp đồng đã tạm ứng 50% đã làm xong chưa?",
      v2="Hợp đồng bảo trì định kỳ, xác nhận công nợ của Schindler; với từng hợp đồng sửa chữa: biên bản khảo sát sự cố, báo giá, nghiệm thu; giấy kiểm định còn hiệu lực của 18 thang.",
      v3="Đối chiếu 597,8 triệu trong bảng chi phí với các lệnh chi; vì sao cần 14 hợp đồng sửa chữa trong 7 tháng; có hạng mục nào sửa lặp lại không.",
      r=["Phí định kỳ trả từ tài khoản vận hành vì hiểu sai nguồn chi; hồ sơ đủ.",
         "Chậm thanh toán vì thủ tục, có xác nhận công nợ rõ ràng, đã trả sau đó.",
         "Hợp đồng sửa chữa chia nhỏ, không có biên bản sự cố, cùng hạng mục sửa lặp lại, hoặc phí định kỳ bị trả hai nơi."],
      lean=("(1) Thiếu năng lực", "k1"), codes="F06, F14", cv="Mục I.2.c, III.8; Phụ lục 1 số 6", key="Xác nhận công nợ của Schindler, biên bản sự cố, giấy kiểm định"),
 dict(t="Tiền gửi: kỳ hạn ngắn, tái tục 127,5 tỷ",
      f="15 tỷ tái tục kỳ hạn 3 tháng suốt 21 tháng với lãi 1,9 – 2,4% một năm; số dư thanh toán bình quân khoảng 4,24 tỷ chỉ hưởng 0,2%; ước bỏ lỡ 0,42 – 0,96 tỷ tiền lãi. Thông báo 15/09/2026: tái tục 127,5 tỷ, lãi 8% một năm, chưa có hợp đồng và xác nhận của ngân hàng.",
      q="Quy chế Điều 6.1.h (báo cáo Hội nghị nhà chung cư), 8.8.b (kiểm toán); nghĩa vụ quản lý tiền quỹ cẩn trọng.",
      v1="Vì sao chọn kỳ hạn 3 tháng cho 15 tỷ và để vài tỷ ở tài khoản thanh toán? Trước mỗi lần tái tục có lấy chào lãi suất của các ngân hàng không?",
      v2="Hợp đồng 5 khoản tiền gửi sau tái tục; giấy xác nhận số dư tại quầy; văn bản chào lãi suất của các ngân hàng.",
      v3="Mức 8% cao hơn biểu 12 tháng tại quầy (khoảng 5,9% ở cả hai ngân hàng; Agribank gửi trực tuyến 6,8%): có kèm điều kiện gì không (cầm cố, phong tỏa, cam kết)?",
      r=["Thiếu kinh nghiệm quản lý tiền, không có kế hoạch dòng tiền.",
         "Khó là lỡ tay: cách gửi kéo dài 21 tháng.",
         "Chỉ khi có lợi ích riêng gắn với việc chọn ngân hàng, kỳ hạn, hoặc hợp đồng thực tế khác thông báo."],
      lean=("(1) Thiếu năng lực", "k1"), codes="F04, F10, F16", cv="Mục I.2.b, I.2.h, II.1, III.7; Phụ lục 1 số 1, 5", key="Hợp đồng tiền gửi và giấy xác nhận tại quầy"),
 dict(t="Hợp đồng quảng cáo Chicilon Media ký lại giảm 17,5%",
      f="Hợp đồng 01/10/2024 thu khoảng 86,98 triệu mỗi tháng; hợp đồng ký lại ngày 05/01/2025 còn 71,8 triệu mỗi tháng, ít hơn khoảng 182,2 triệu mỗi năm.",
      q="Luật Nhà ở 2023 Điều 153 khoản 4; nghĩa vụ khai thác phần sở hữu chung có lợi nhất cho cư dân.",
      v1="Vì sao giá thuê giảm? Phạm vi (số màn hình, vị trí, thời lượng) có thay đổi không?",
      v2="Hai hợp đồng với Chicilon Media, các chào giá cạnh tranh nếu có, biên bản đàm phán.",
      v3="Có mời đơn vị khác chào giá không; ai quyết định mức giá mới.",
      r=["Đàm phán kém, không mời chào giá cạnh tranh.",
         "Chênh do cách tính thuế hoặc phạm vi thay đổi, có văn bản chứng minh.",
         "Giảm giá không có lý do khi phạm vi giữ nguyên, có lợi ích riêng liên quan."],
      lean=("Chưa loại trừ (3)", "k3"), codes="F09", cv="Mục I.2.g; Phụ lục 1 số 10", key="Hai hợp đồng và các chào giá"),
 dict(t="Sao kê in ngày 04/09/2026 nhưng chỉ tới 31/05/2026",
      f="Sổ phụ Agribank in ngày 04/09/2026 nhưng dừng ở 31/05/2026; sao kê VietinBank cũng dừng ở 31/05/2026. Ba tháng 6 – 8/2026 có đợt đáo hạn khoảng 110 tỷ tiền gửi, khoảng 5,17 tỷ tiền lãi phải về tài khoản và đợt tái tục 127,5 tỷ, nhưng chưa có sao kê.",
      q="Quy chế Điều 6.1.g (công khai hằng tháng các khoản chi tiêu tiền gửi kinh phí bảo trì); quyền được cung cấp thông tin của chủ sở hữu.",
      v1="Vì sao sao kê in ngày 04/09/2026 chỉ lấy tới 31/05/2026? Ai chọn khoảng thời gian này?",
      v2="Sao kê các tài khoản quỹ và TK 117002997784 từ 01/06/2026 tới ngày gần nhất; chứng từ tái tục từng hợp đồng.",
      v3="Đối chiếu tiền lãi đáo hạn (khoảng 5,17 tỷ) với số tiền tái tục và số dư: 2,5 tỷ mở mới lấy từ đâu, phần còn lại đang ở đâu.",
      r=["Chọn kỳ theo báo cáo 15/05/2026 hoặc theo mẫu yêu cầu cũ; cung cấp ngay phần còn lại.",
         "Chọn nhầm kỳ khi đề nghị ngân hàng in; bổ sung ngay khi được nhắc.",
         "Từ chối hoặc trì hoãn cung cấp sao kê từ 01/06/2026; số liệu sau đó không khớp thông báo."],
      lean=("(2) nếu bổ sung ngay", "k2"), codes="điểm bổ sung", cv="Mục I.2.k; Phụ lục 1 số 5", key="Sao kê từ 01/06/2026 tới nay"),
]
ISS.append(dict(t="13 khoản chi trên 50 triệu: ai cho phép",
      f="Mười ba khoản chi, mỗi khoản trên 50 triệu, tổng 5,04 tỷ: HNB 1,25 tỷ, hoàn ứng 986,9 triệu, Thép Quang 705,8 triệu, Schindler 477,1 triệu, Thành Công 350,7 triệu, Khởi Sáng Việt 289,3 triệu, Thành Công 193,7 triệu, KTECH 187,0 triệu và năm khoản khác. Ba hợp đồng HNB, Thép Quang, Thành Công 2,15 tỷ ký trong 06 – 08/04/2026. Chi sửa chữa năm 2025 là 2,89 tỷ, gấp 5,8 lần trần 500 triệu.",
      q="Quy chế Điều 9.2 (việc khẩn cấp Ban quản trị chỉ tự quyết tới 50 triệu, trên mức đó cần trên 50% chủ sở hữu đồng ý; trần 500 triệu mỗi năm), 6.3.b và 6.3.c (việc không khẩn cấp phải theo kế hoạch được Hội nghị thông qua); Quy chế hoạt động Ban quản trị điểm c khoản 3 Điều 3 (chi kinh phí bảo trì cần 75% thành viên đồng ý).",
      v1="Mỗi khoản trên 50 triệu thuộc kế hoạch bảo trì nào được Hội nghị thông qua, hay là việc khẩn cấp đã lấy ý kiến chủ sở hữu? Nếu khẩn cấp, bản giải trình niêm yết ở đâu, ngày nào?",
      v2="Kế hoạch bảo trì 2025, 2026 và biên bản Hội nghị; văn bản lấy ý kiến chủ sở hữu và kết quả; biên bản họp Ban quản trị thông qua từng khoản chi.",
      v3="Vì sao ba hợp đồng HNB, Thép Quang, Thành Công 2,15 tỷ ký dồn trong ba ngày mà không đưa ra lấy ý kiến; vì sao số hợp đồng HNB mang ngày 24/03/2026 trong khi ghi ký ngày 07/04/2026; HNB sửa hệ thống cấp nước sinh hoạt, vậy vì sao cư dân vẫn phản ánh ống nước bể, dột nhiều nơi, và HNB đã bảo hành, xử lý những điểm nào.",
      r=["Hiểu nhầm rằng Ban quản trị được quyết mọi khoản sửa chữa; có biên bản họp Ban quản trị nhưng không biết phải hỏi chủ sở hữu.",
         "Có kế hoạch được Hội nghị thông qua nhưng chưa công bố; xuất trình được ngay.",
         "Không có kế hoạch, không lấy ý kiến, ký dồn nhiều hợp đồng lớn trong vài ngày hoặc chia nhỏ để dưới 50 triệu."],
      lean=("(1) Thiếu năng lực", "k1"), codes="F03, F05, F06, F07, F08", cv="Mục I.2.d; Phụ lục 1 số 8", key="Kế hoạch được thông qua hoặc văn bản ý kiến chủ sở hữu"))
assert len(ISS) == 11

PUBLIC = [
 "Vì sao ngày 23/12/2025 quỹ chuyển 986,9 triệu sang tài khoản vận hành để hoàn ứng 6 khoản chi, thay vì chuyển thẳng cho nhà thầu? Đề nghị cung cấp sao kê tài khoản 118002976372 từ 01/08/2025 và hợp đồng, hóa đơn, biên bản nghiệm thu của 6 khoản.",
 "Bảng chi phí trong Báo cáo 03-2026/BC-BQTSSR ngày 15/05/2026 ghi 863,8 triệu cho thang máy, phòng cháy, máy phát điện, thấp hơn khoản hoàn ứng 123,1 triệu: đề nghị cung cấp bảng kê từng khoản và giải thích phần chênh.",
 "Căn cứ nào để thu 1,71 tỷ tiền quảng cáo của Chicilon Media, Hưng Thái và tiền thuê mặt bằng của Viễn thông ACT vào tài khoản 117002997784 thay vì tài khoản quỹ theo khoản 4 Điều 153 Luật Nhà ở 2023? Khi nào chuyển số dư và các khoản thu về quỹ?",
 "1,40 tỷ chi sửa chữa, mua sắm từ tài khoản 117002997784, trong đó Công ty Thành Công nhận 856,8 triệu qua 4 hợp đồng: đề nghị cung cấp dự toán, 3 báo giá, hợp đồng, biên bản nghiệm thu từng hợp đồng.",
 "Hệ thống giữ xe (Khởi Sáng Việt, hợp đồng 18KSVSSR08082025): tổng đã trả 356,4 triệu, cao hơn khoảng 67,1 triệu so với giá trị suy ra từ khoản tạm ứng 40%. Đề nghị cung cấp hợp đồng, phụ lục phát sinh, biên bản khảo sát, nghiệm thu, quyết toán.",
 "Khoản 705,8 triệu trả Công ty Thép Quang mua thiết bị ngày 24/04/2026 được trả đủ một lần: đề nghị cung cấp danh mục thiết bị, hóa đơn, biên bản giao nhận và 3 báo giá.",
 "Thang máy: vì sao phí bảo trì định kỳ khoảng 57,5 triệu mỗi tháng không còn chi từ tài khoản quỹ từ 21/01/2025? Đề nghị cung cấp hợp đồng bảo trì, xác nhận công nợ của Schindler, biên bản khảo sát và nghiệm thu các hợp đồng sửa chữa, giấy kiểm định còn hiệu lực của từng thang.",
 "Tiền gửi: đề nghị cung cấp hợp đồng và giấy xác nhận tại quầy của 127,5 tỷ tiền gửi tại VietinBank và Agribank sau đợt tái tục tháng 8/2026 với lãi 8% một năm.",
 "Hợp đồng quảng cáo với Chicilon Media ký lại ngày 05/01/2025 giảm từ khoảng 86,98 triệu xuống 71,8 triệu mỗi tháng: vì sao giảm, có mời chào giá cạnh tranh không?",
 "Sao kê in ngày 04/09/2026 nhưng chỉ lấy tới 31/05/2026: đề nghị cung cấp sao kê các tài khoản từ 01/06/2026 tới nay, giai đoạn có đợt đáo hạn khoảng 110 tỷ và khoảng 5,17 tỷ tiền lãi.",
]
assert len(PUBLIC) == 10
POST = ["Gửi công văn cho Ban quản trị trước, rồi mới đăng; ghi ngày gửi và hạn trả lời (15 ngày) ở đầu bài.",
        "Bài đăng nhóm nêu câu hỏi và dữ kiện từ sao kê; phần phân loại để trên dashboard, không trích riêng một nhãn ra khỏi ngữ cảnh.",
        "Cập nhật công khai tình trạng từng câu: chưa trả lời, đã trả lời, đã đưa chứng từ.",
        "Mời Ban quản trị trả lời trên cùng kênh hoặc tại một buổi đối thoại có biên bản."]

for s_ in [x for i in ISS for x in [i["t"], i["f"], i["q"], i["v1"], i["v2"], i["v3"], i["cv"], i["lean"][0]] + i["r"]] + PUBLIC + POST + RULES + [c[3] for c in CAUSES] + [y for r in ROUNDS for y in r[3]]:
    assert "→" not in s_ and "->" not in s_, s_[:60]

EXTRA = """
.hd { display:flex; justify-content:space-between; align-items:center; border-bottom:2pt solid #1F3864; padding-bottom:6pt; }
.hd .br { display:flex; gap:10pt; align-items:center; } .hd img { width:15mm; height:15mm; border-radius:50%; }
.hd .l1 { font-family:'Be Vietnam Pro',sans-serif; font-size:8.3pt; font-weight:800; letter-spacing:.12em; color:#1F3864; }
.hd .l2 { font-family:'Be Vietnam Pro',sans-serif; font-size:8.3pt; font-weight:600; color:#5a6475; }
.hd .dt { font-family:'Be Vietnam Pro',sans-serif; font-size:8pt; font-weight:700; color:#fff; background:#1F3864; border-radius:10pt; padding:2.5pt 9pt; }
.t1 { font-family:'Be Vietnam Pro',sans-serif; font-size:19pt; font-weight:800; color:#1F3864; line-height:1.18; margin-top:9pt; }
.t2 { font-family:'Be Vietnam Pro',sans-serif; font-size:9.8pt; color:#3d4656; margin-top:4pt; line-height:1.45; }
.kset { display:flex; gap:6pt; margin:8pt 0 4pt 0; flex-wrap:wrap; }
.kk { font-family:'Be Vietnam Pro',sans-serif; font-size:8.6pt; font-weight:800; border-radius:12pt; padding:2.5pt 10pt; }
.k1 { background:#FBF3D9; color:#7F6000; border:0.8pt solid #e7cf86; } .k2 { background:#E6ECF5; color:#1F3864; border:0.8pt solid #b9c7dd; }
.k3 { background:#F8E3E3; color:#A93434; border:0.8pt solid #e6b9b9; } .k0 { background:#EDEDED; color:#404040; border:0.8pt solid #cfcfcf; }
.warn { font-family:'Be Vietnam Pro',sans-serif; font-size:8.4pt; color:#6b5216; background:#FBF3DF; border:0.8pt solid #e6cf92; border-radius:4pt; padding:5pt 8pt; margin:6pt 0 2pt 0; line-height:1.45; }
.sh { font-family:'Be Vietnam Pro',sans-serif; display:flex; align-items:center; gap:8pt; background:#DCE6F1; border-radius:4pt; padding:5pt 9pt; margin:11pt 0 6pt 0; break-after:avoid; }
.sh .no { font-size:13pt; font-weight:800; color:#C8992F; } .sh h2 { font-size:12pt; font-weight:800; color:#1F3864; }
table.cz td { font-size:8.9pt; line-height:1.4; vertical-align:top; } table.cz td:first-child { white-space:nowrap; }
.rounds { display:grid; grid-template-columns:repeat(3,1fr); gap:6pt; margin:4pt 0 6pt 0; }
.rd { border:0.8pt solid #cfd8e6; border-top:3pt solid #1F3864; border-radius:0 0 5pt 5pt; padding:6pt 8pt; background:#fff; break-inside:avoid; }
.rd .n { font-family:'Be Vietnam Pro',sans-serif; font-size:8pt; font-weight:800; letter-spacing:.08em; color:#C8992F; }
.rd .h { font-family:'Be Vietnam Pro',sans-serif; font-size:10.5pt; font-weight:800; color:#1F3864; margin-top:1pt; }
.rd .w { font-family:'Be Vietnam Pro',sans-serif; font-size:7.8pt; color:#5b6474; margin:1pt 0 3pt 0; }
.rd p { font-size:9pt; line-height:1.42; margin:2pt 0 0 0; text-align:left; }
.iss { margin:9pt 0 4pt 0; }
.ih { display:flex; align-items:center; gap:7pt; border-bottom:1.2pt solid #1F3864; padding-bottom:3pt; margin-bottom:3pt; break-after:avoid; }
.ih .in { font-family:'Be Vietnam Pro',sans-serif; font-size:8.5pt; font-weight:800; color:#fff; background:#1F3864; border-radius:3pt; padding:1pt 5pt; }
.ih h3 { font-family:'Be Vietnam Pro',sans-serif; font-size:10.8pt; font-weight:800; color:#1F3864; flex:1; }
.ih .lean { font-family:'Be Vietnam Pro',sans-serif; font-size:7.8pt; font-weight:800; border-radius:10pt; padding:1.5pt 8pt; background:#EDF1F7; color:#1F3864; border:0.8pt solid #b9c7dd; white-space:nowrap; }
table.ix { width:100%; border-collapse:collapse; }
table.ix th { width:27mm; text-align:left; vertical-align:top; font-family:'Be Vietnam Pro',sans-serif; font-size:8pt; font-weight:800; color:#1F3864; background:#F3F6FB; border:0.6pt solid #d9e1ec; padding:3pt 5pt; }
table.ix td { font-size:9pt; line-height:1.42; border:0.6pt solid #d9e1ec; padding:3pt 6pt; vertical-align:top; }
table.ix tr { break-inside:avoid; }
table.ix tr.v th { color:#7a5a12; background:#FBF3DF; }
table.ix .rr { display:grid; grid-template-columns:36mm 1fr; gap:2pt 6pt; align-items:start; }
table.ix .rr .kk { font-size:7.4pt; padding:1pt 6pt; text-align:center; white-space:nowrap; }
table.ix .rr div { font-size:8.9pt; line-height:1.38; }
table.trk td { font-size:8.6pt; line-height:1.35; vertical-align:top; } table.trk td { height:24pt; }
.pb { break-before:page; }
table.form td { font-size:8.8pt; height:17pt; vertical-align:top; } table.form td:first-child { font-family:'Be Vietnam Pro',sans-serif; font-weight:700; color:#1F3864; width:34%; }
.notice { min-height:250mm; display:flex; flex-direction:column; }
.notice .nh { display:flex; align-items:center; gap:10pt; border-bottom:2pt solid #1F3864; padding-bottom:6pt; }
.notice .nh img { width:14mm; height:14mm; border-radius:50%; }
.notice .nh .a { font-family:'Be Vietnam Pro',sans-serif; font-size:8.6pt; font-weight:800; letter-spacing:.1em; color:#1F3864; }
.notice .nh .b { font-family:'Be Vietnam Pro',sans-serif; font-size:8.4pt; color:#5a6475; font-weight:600; }
.notice .nt { font-family:'Be Vietnam Pro',sans-serif; font-size:17pt; font-weight:800; color:#1F3864; margin-top:10pt; line-height:1.2; }
.notice .ni { font-family:'Be Vietnam Pro',sans-serif; font-size:9.6pt; color:#3d4656; margin:6pt 0 8pt 0; line-height:1.5; }
.notice ol { margin:0; padding-left:24pt; } .notice li { font-size:11pt; line-height:1.55; margin:0 0 8.5pt 0; padding-left:2pt; text-align:left; }
.notice li::marker { font-family:'Be Vietnam Pro',sans-serif; font-weight:800; color:#C8992F; }
.notice .nf { margin-top:auto; font-family:'Be Vietnam Pro',sans-serif; font-size:8pt; color:#5b6474; line-height:1.45; border-top:0.8pt solid #cfd8e6; padding-top:6pt; }
.ih .lean.k1 { background:#FBF3D9; color:#7F6000; border-color:#e7cf86; } .ih .lean.k2 { background:#E6ECF5; color:#1F3864; border-color:#b9c7dd; }
.ih .lean.k3 { background:#F8E3E3; color:#A93434; border-color:#e6b9b9; } .ih .lean.k0 { background:#EDEDED; color:#404040; border-color:#cfcfcf; }
table.ix tr.h th { color:#A93434; background:#F8E3E3; } table.ix tr.h td { background:#FFFBFB; }
table.ix tr.h.st-cho th { color:#C55A11; background:#FCE9DC; } table.ix tr.h.st-cho td { background:#FFFCF9; }
.ih .lgp { font-size:7.6pt; padding:1.2pt 7pt; }
table.cp td { font-size:8.5pt; line-height:1.36; padding-top:2.6pt; padding-bottom:2.6pt; }
table.ix tr.c th { color:#1E4E79; background:#E8F0F8; } table.ix tr.c td { font-family:'Be Vietnam Pro',sans-serif; font-size:8.4pt; color:#1E4E79; }
.pub { border:1.2pt solid #1F3864; border-radius:6pt; padding:9pt 12pt 8pt 12pt; margin-top:6pt; }
.pub .pt { font-family:'Be Vietnam Pro',sans-serif; font-size:12.5pt; font-weight:800; color:#1F3864; }
.pub .pl { font-family:'Be Vietnam Pro',sans-serif; font-size:8.6pt; color:#3d4656; margin:3pt 0 5pt 0; line-height:1.45; }
.pub ol { margin:0; padding-left:15pt; } .pub li { font-size:9.3pt; line-height:1.45; margin:3pt 0; text-align:left; }
.pub .pf { font-family:'Be Vietnam Pro',sans-serif; font-size:7.8pt; color:#5b6474; margin-top:6pt; line-height:1.4; }
"""

def sh(no, t): return f'<div class="sh"><span class="no">{no}</span><h2>{E(t)}</h2></div>'
def kk(n): return f'<span class="kk {K[n][1]}">{E(K[n][0])}</span>'

head = (f'<div class="hd"><div class="br"><img alt="Logo Saigon South Residences" src="data:image/png;base64,{LOGO}"><div>'
        f'<div class="l1">TÀI LIỆU LÀM VIỆC · NHÓM CƯ DÂN GIÁM SÁT QUỸ BẢO TRÌ</div><div class="l2">Chung cư Nam Sài Gòn Residences</div></div></div>'
        f'<span class="dt">Lập ngày {TODAY}</span></div>'
        '<div class="t1">Hỏi dần để biết mỗi cái sai thuộc nguyên nhân nào</div>'
        '<div class="t2">Ba nguyên nhân: thiếu năng lực, lỡ tay thật, lỡ tay có chủ đích. Mười một vấn đề của quỹ bảo trì, mỗi vấn đề có hệ quả pháp lý, ba vòng câu hỏi, cách đọc câu trả lời và mục tương ứng trong công văn. Kết quả hỏi dần dùng để chốt câu trả lời cho câu hỏi thứ ba và thứ năm của cuộc kiểm tra: mức độ vi phạm và khung xử lý. Dữ liệu: sao kê ba tài khoản 15/08/2024 – 31/05/2026 và tài liệu Ban quản trị gửi ngày 28/09/2026.</div>'
        f'<div class="kset">{kk(1)}{kk(2)}{kk(3)}<span class="kk k3">Chưa loại trừ (3): chờ chứng từ</span></div>'
        '<div class="warn"><b>Tài liệu làm việc của nhóm cư dân, dùng cùng file Phân loại nguyên nhân.</b> File Phân loại cho biết hiện mỗi cái sai nghiêng về nguyên nhân nào; file này dùng để hỏi, ghi nhận câu trả lời và cập nhật phân loại đó. Bản đăng nhóm cư dân là file Mười câu hỏi. Các nhận định là dấu hiệu cần làm rõ, không phải cáo buộc; không thay thế kiểm toán hay kết luận của cơ quan có thẩm quyền.</div>'
        f'<div style="margin:7pt 0 2pt 0">{km_compact_html(E, hq=True)}</div>' + K5.k5_strip(E))

s1 = sh("1", "Ba nguyên nhân và dấu hiệu nhận biết") + table(
    ["Nguyên nhân", "Thường thấy khi", "Dấu hiệu trong câu trả lời", "Hướng xử lý và hệ quả"],
    [[kk(n), E(a), E(b), E(c)] for n, a, b, c in CAUSES], widths=["16%", "23%", "31%", "30%"], esc=False, tcls="cz") + \
    '<p style="font-size:8.8pt;margin-top:4pt"><b>Ví dụ lỡ tay thật đã thấy:</b> báo cáo 01-2025/BC-BQTSSR tính phí ngân hàng hai lần, lệch 247.500 đồng; chứng từ gốc đúng, cái sai chỉ ở khâu tổng hợp.</p>' + \
    nd(RULES, label="NGUYÊN TẮC PHÂN LOẠI")

s2 = sh("2", "Cách hỏi dần: ba vòng") + '<div class="rounds">' + "".join(
    f'<div class="rd"><div class="n">{E(a)}</div><div class="h">{E(b)}</div><div class="w">{E(c)}</div>' + "".join(f"<p>{E(x)}</p>" for x in d) + "</div>"
    for a, b, c, d in ROUNDS) + "</div>" + nd(HOWTO, label="CÁCH GHI NHẬN", gold=True)

def issue(i, it):
    rr = "".join(f'{kk(n + 1)}<div>{E(x)}</div>' for n, x in enumerate(it["r"]))
    st = LG.LG_ISS_ST[i - 1]
    return (f'<div class="iss"><div class="ih"><span class="in">3.{i}</span><h3>{E(it["t"])}</h3>{LG.lg_pill_st(E, st)}<span class="lean {it["lean"][1]}">Sơ bộ: {E(it["lean"][0])} · {E(it["codes"])}</span></div>'
            f'<table class="ix"><tr><th>Sự việc</th><td>{E(it["f"])}</td></tr><tr><th>Quy định</th><td>{E(it["q"])}</td></tr>'
            f'<tr class="h st-{st}"><th>Hệ quả pháp lý</th><td>{E(LG.LG_ISS[i - 1])}</td></tr>'
            f'<tr class="c"><th>Trong công văn</th><td>{E(it["cv"])}</td></tr>'
            f'<tr class="v"><th>Vòng 1 · Hỏi để hiểu</th><td>{E(it["v1"])}</td></tr>'
            f'<tr class="v"><th>Vòng 2 · Đòi chứng từ</th><td>{E(it["v2"])}</td></tr>'
            f'<tr class="v"><th>Vòng 3 · Đối chiếu</th><td>{E(it["v3"])}</td></tr>'
            f'<tr><th>Đọc câu trả lời</th><td><div class="rr">{rr}</div></td></tr></table></div>')

s3 = sh("3", "Mười một vấn đề, câu hỏi ba vòng và cách đọc câu trả lời") + \
     '<p style="font-size:8.8pt">Nhãn “Sơ bộ” lấy từ file Phân loại nguyên nhân, kèm mã dấu hiệu trong báo cáo đầy đủ; nhãn sẽ đổi theo câu trả lời và chứng từ. Dòng “Trong công văn” chỉ mục và hồ sơ tương ứng để đối chiếu khi Ban quản trị trả lời. Dòng (1), (2), (3) mô tả câu trả lời như thế nào thì nghiêng về nguyên nhân đó.</p>' + \
     "".join(issue(i + 1, it) for i, it in enumerate(ISS))

s4 = sh("4", "Bảng theo dõi phân loại") + table(
    ["#", "Vấn đề", "Mục công văn", "Chứng từ quyết định", "Sơ bộ", "Ngày hỏi · trả lời", "Phân loại cuối"],
    [[f"3.{i + 1}", E(it["t"]) + f'<div style="margin-top:2pt">{LG.lg_pill_st(E, LG.LG_ISS_ST[i])}</div>', E(it["cv"].split(";")[0].replace("Mục ", "")), E(it["key"]), E(it["lean"][0]), "", ""] for i, it in enumerate(ISS)],
    widths=["5%", "23%", "11%", "22%", "14%", "13%", "12%"], esc=False, tcls="trk") + \
    nd(["Ưu tiên hỏi trước 3.1, 3.6 và 3.10: ba vấn đề này quyết định câu trả lời cho 1,69 tỷ và giai đoạn chưa có sao kê.",
        "Ghi ngày gửi, ngày trả lời và chứng từ đã nhận vào bảng; chỉ điền cột Phân loại cuối sau vòng 3."], label="THỨ TỰ ƯU TIÊN") + \
    '<div class="cap" style="margin-top:6pt">Mẫu ghi nhận mỗi lần Ban quản trị trả lời</div>' + table(["Mục", "Ghi nhận"],
    [["Vấn đề số, vòng hỏi", ""], ["Ngày gửi câu hỏi, hạn trả lời", ""], ["Ngày nhận, hình thức trả lời", ""], ["Câu trả lời (chép nguyên văn ý chính)", ""],
     ["Chứng từ đã nhận", ""], ["Khớp hoặc lệch với lời giải thích vòng trước", ""], ["Đánh giá tạm: (1), (2), (3) hay chưa đủ căn cứ; câu hỏi vòng sau", ""]],
    widths=["34%", "66%"], tcls="form")

AFTER = ["Ghi câu trả lời vào mẫu ghi nhận, chép nguyên văn ý chính và danh mục chứng từ đã nhận.",
         "Đối chiếu với ba dòng (1), (2), (3) của vấn đề đó để có đánh giá tạm, rồi soạn câu hỏi vòng sau.",
         "Khi điều kiện ở cột “Đổi phân loại khi” của file Phân loại nguyên nhân xảy ra, sửa nhóm tương ứng trong file đó.",
         "Hết hạn 15 ngày, xem lại toàn bộ phân loại; khoản nào vẫn thiếu chứng từ thì chuyển sang vòng 3 và ghi là vi phạm đã rõ, phải bồi hoàn quỹ.",
         "Ba vi phạm đã rõ không phụ thuộc kết quả hỏi: hết hạn mà Ban quản trị không khắc phục thì chuyển sang kiến nghị xử phạt và thủ tục bãi nhiệm ở mục 6."]
s5 = sh("5", "Bản công khai và việc làm sau mỗi vòng") + \
     '<p style="font-size:8.8pt">Bản công khai là file Mười câu hỏi: ảnh để đăng nhóm cư dân và PDF khổ A4 để in dán bảng tin. Câu số n trong bản công khai ứng với vấn đề 3.n ở trên; bản này không có phần phân loại nguyên nhân.</p>' + \
     nd(POST, label="CÁCH ĐĂNG ĐỂ CƯ DÂN HIỂU VÀ XEM BAN QUẢN TRỊ PHẢN HỒI", gold=True) + nd(AFTER, label="SAU MỖI LẦN BAN QUẢN TRỊ TRẢ LỜI")

LADDER, FORMS, BAI = LG.lg_pdf_parts(E, table)
s6 = '<div style="break-inside:avoid">' + sh("6", "Hệ quả pháp lý và khi nào dùng bãi nhiệm") + \
     '<p style="font-size:8.8pt">Nguyên nhân (1), (2), (3) quyết định cách xử lý cá nhân; tình trạng pháp lý quyết định khoản nào chắc chắn phải xử lý.</p>' + \
     LADDER + '</div><div class="cap">Điều kiện bãi nhiệm thành viên Ban quản trị</div>' + BAI + \
     nd(LG.LG_ND, label=LG.LG_ND_LABEL) + f'<div class="lgnote">{E(LG.LG_NOTE)}</div>'

fonts = open("bvp_fonts.css").read()
doc = (f'<!doctype html><html lang="vi"><head><meta charset="utf-8"><style>{fonts}{CSS}{EXTRA}{KMC_CSS}{LG.LG_CSS}{K5.CSS}</style></head><body>'
       + head + s1 + s2 + s3 + s4 + s5 + s6 + "</body></html>")
open("hoidan.html", "w", encoding="utf-8").write(doc)
print("html", len(doc))
