# -*- coding: utf-8 -*-
"""File rieng, noi bo: PHAN LOAI NGUYEN NHAN 16 dau hieu cua bao cao day du vao ba nhom
(1) thieu nang luc, (2) lo tay that, (3) lo tay co chu dich; kem nhom chua loai tru (3) va chua phat sinh sai.
Khong dua vao cong van, khong dang cong khai. Nhan dien SSR, khong TVN, khong neu ten ca nhan."""
import base64, json, os
os.chdir("/home/claude/ssr")
from report_kit import CSS, E, nd, table
from keymsg import km_compact_html, KMC_CSS
import legal as LG

LOGO = base64.b64encode(open("crops/logo_480.png", "rb").read()).decode()
TODAY = "30/09/2026"
FIND = {f["id"]: f for f in json.load(open("findings.json"))}

G1 = [  # (1) thieu nang luc
 ("F02", "Tiền khu vực chung 1,71 tỷ không vào quỹ",
  "Nhiều khả năng làm theo cách hiểu cũ, chưa cập nhật khoản 4 Điều 153 Luật Nhà ở 2023. Việc chuyển 260,9 triệu ra khỏi quỹ với lý do trả nhầm là thao tác chủ động, nên không phải lỡ tay.",
  "Không có nghị quyết, không công khai thu chi của TK 117002997784, hoặc vẫn giữ tiền ngoài quỹ sau khi được chỉ ra quy định.", "Trung bình"),
 ("F04", "Tiền gửi chưa có xác nhận tại ngày gần nhất",
  "Thiếu chủ động công khai. Ban quản trị đã đưa giấy xác nhận 120 tỷ của VietinBank và Agribank tại ngày 20/05/2025, khớp sao kê; còn thiếu xác nhận tại ngày gần nhất.",
  "Không cung cấp được hợp đồng và xác nhận 127,5 tỷ sau tái tục, hoặc số xác nhận khác thông báo.", "Cao"),
 ("F05", "Hợp đồng sửa hệ thống cấp nước sinh hoạt với HNB khoảng 1,25 tỷ, tạm ứng 50%",
  "Hạng mục chính đáng. Điểm sai nằm ở quy trình: hợp đồng gấp 25 lần mức Ban quản trị được tự quyết nhưng chưa thấy văn bản cho phép, và tạm ứng một nửa trước khi thi công. Cư dân phản ánh ống nước vẫn bể, dột nhiều nơi, cần đối chiếu nghiệm thu và bảo hành.",
  "Không có báo giá cạnh tranh, giá cao hơn thị trường, hoặc trả tiếp phần còn lại khi chưa nghiệm thu, trong khi ống nước vẫn bể, dột.", "Trung bình"),
 ("F06", "Schindler 806,9 triệu, 14 hợp đồng sửa chữa trong 7 tháng",
  "Tiền trả thẳng cho Schindler nên rủi ro gian lận thấp. Sửa chữa dày, trả trễ 5 – 6 tháng và hợp đồng 477,1 triệu chưa thấy văn bản cho phép là yếu kém quản lý.",
  "Hợp đồng bị chia nhỏ để dưới trần 500 triệu mỗi năm (Điều 9.2), hoặc phí bảo trì bị trả trùng.", "Trung bình"),
 ("F10", "15 tỷ gửi VietinBank kỳ hạn 3 tháng, tiền nhàn rỗi, lãi bỏ lỡ 0,42 – 0,96 tỷ",
  "Lãi suất đúng biểu niêm yết. Thiệt hại đến từ thiếu kế hoạch dòng tiền kéo dài 21 tháng; không có dấu hiệu ai hưởng lợi.",
  "Có lợi ích riêng gắn với việc chọn ngân hàng hoặc kỳ hạn.", "Cao"),
 ("F11", "Mở tài khoản quỹ thứ hai tại Agribank",
  "Sai thủ tục: Quy chế chỉ cho một tài khoản quỹ, tối thiểu 3 đồng chủ tài khoản. Tài khoản chỉ nhận 60 tỷ, mở tiền gửi và chuyển lãi về tài khoản chính, không có lệnh chi bất thường.",
  "Phát hiện giao dịch rút tiền không qua đồng ký.", "Trung bình"),
 ("F12", "Chưa thấy kiểm toán năm 2025, công khai chưa đầy đủ",
  "Thiếu sót thủ tục, không làm mất tiền.",
  "Từ chối kiểm toán hoặc không công khai sau khi được đề nghị.", "Trung bình"),
 ("F14", "Phí bảo trì Schindler định kỳ vắng trên tài khoản quỹ từ 21/01/2025",
  "Nhiều khả năng phí được trả từ tài khoản vận hành rồi hoàn ứng, vì lệnh hoàn ứng 23/12/2025 ghi cả bảo trì thang máy. Đây là sai cách đi tiền.",
  "Phí bị trả hai nơi, hoặc Schindler xác nhận đang bị nợ trong khi quỹ đã hoàn ứng.", "Thấp"),
 ("F15", "Lệnh chi HNB và Thành Công từ hai tài khoản lập cách nhau hai phút",
  "Cho thấy một người thao tác cả hai tài khoản; khâu lập lệnh và duyệt lệnh chưa tách bạch.",
  "Một người vừa lập vừa duyệt lệnh chi tiền quỹ, bỏ qua quy định 3 chữ ký.", "Trung bình"),
]
G2 = [  # (2) lo tay that
 ("F08", "Hợp đồng giữ xe Khởi Sáng Việt trả vượt 67,1 triệu",
  "Có hai cách giải thích vô hại: ghi nhầm tỷ lệ tạm ứng (thực tế khoảng 32,5%) hoặc có phụ lục phát sinh. Hợp đồng còn ghi hai ngày ký khác nhau, cho thấy giấy tờ làm ẩu.",
  "Không có phụ lục, hoặc phụ lục lập sau khi đã thanh toán; khi đó là trả vượt không có căn cứ.", "Thấp"),
 ("F13", "Các chi tiết nhỏ trên chứng từ",
  "Từng điểm là sai sót giấy tờ. Riêng ký hiệu BQT TQ trên hợp đồng của Thành Công (221025) và Thép Quang (080426) cần giải thích, vì liên quan hai khoản ở nhóm chưa loại trừ (3).",
  "Ký hiệu chung cho thấy cùng một đầu mối lập hợp đồng cho cả Thành Công và Thép Quang.", "Trung bình"),
]
G3 = [  # chua loai tru (3)
 ("F01", "986,9 triệu hoàn ứng qua TK vận hành 118002976372",
  "Cách đi tiền sai có thể chỉ vì thuận tiện. Nhưng việc lặp lại 6 lần trong 5 tháng khi quỹ luôn còn ít nhất 4,22 tỷ, bảng chi phí chỉ giải thích 863,8 triệu, và chưa có sao kê tài khoản nhận tiền.",
  "Sao kê tài khoản vận hành và chứng từ 6 khoản khớp số tiền, trả cho nhà thầu trước ngày hoàn ứng: chuyển về (1).", "Thấp"),
 ("F03", "705,8 triệu trả Thép Quang một lần",
  "Khoản chi đơn lẻ lớn nhất, gấp 14 lần mức Ban quản trị được tự quyết, trả trước 100%. Chưa thấy văn bản cho phép, danh mục hàng hóa và mã số thuế của Thép Quang.",
  "Có văn bản cho phép, danh mục, hóa đơn, thiết bị kiểm đếm được, đơn giá sát thị trường: chuyển về (1).", "Thấp"),
 ("F07", "Thành Công nhận 856,8 triệu qua 4 hợp đồng",
  "4 hợp đồng trong 7 tháng, chiếm 61% tiền sửa chữa chi từ TK 117002997784; hai hợp đồng trả trọn trước nghiệm thu, có hợp đồng 350,7 triệu trả sau 3 ngày; có thể là chia nhỏ để tránh chọn thầu.",
  "Có văn bản cho phép, 3 báo giá, nghiệm thu từng hợp đồng, giá sát thị trường, Thành Công không có quan hệ với người duyệt: chuyển về (1).", "Thấp"),
 ("F09", "Tiền thuê quảng cáo Chicilon Media giảm 17,5% sau khi ký lại",
  "Thu giảm khoảng 182,2 triệu mỗi năm sau khi ký lại với Chicilon Media; chưa rõ có chào giá cạnh tranh và phạm vi quảng cáo có thay đổi không.",
  "Phạm vi thu hẹp hoặc cách tính thuế khác, có văn bản chứng minh: chuyển về (1) hoặc (2).", "Thấp"),
]
G0 = [  # chua phat sinh sai
 ("F16", "Đợt tái tục tiền gửi tháng 8/2026",
  "Thông báo 15/09/2026 cho biết tái tục 127,5 tỷ với lãi 8% một năm; nếu đúng như vậy, đây là cải thiện so với trước.",
  "Hợp đồng thực tế khác thông báo, hoặc khoảng 5,17 tỷ tiền lãi đáo hạn không về đủ tài khoản.", "Chờ hợp đồng"),
]
ALL = G1 + G2 + G3 + G0
assert sorted(x[0] for x in ALL) == sorted(FIND), "phai du 16 dau hieu"
CHECK = [  # bang kiem ba dau hieu cua (3): lap lai | huong loi, gia bat thuong | chung tu ne tranh, mau thuan | so dau hieu ro | chung tu quyet dinh
 ("F01", "986,9 triệu", ("Có", "6 lần trong 5 tháng"), ("Chưa biết", "chưa thấy người nhận cuối"), ("Một phần", "bảng chi phí lệch 123,1 triệu"), 1, "Sao kê TK 118002976372, chứng từ 6 khoản"),
 ("F03", "705,8 triệu", ("Không", "một lần"), ("Chưa biết", "chưa có đơn giá"), ("Một phần", "mô tả chung chung, trả trước 100%"), 0, "Danh mục, hóa đơn, kiểm đếm thực tế, mã số thuế Thép Quang"),
 ("F07", "856,8 triệu", ("Có", "4 hợp đồng liên tiếp"), ("Chưa biết", "chưa có báo giá"), ("Chưa biết", "chưa có nghiệm thu"), 1, "3 báo giá, nghiệm thu, quan hệ của Thành Công"),
 ("F09", "−182,2 triệu/năm", ("Không", "một hợp đồng"), ("Một phần", "thu giảm 17,5%"), ("Chưa biết", "chưa có hợp đồng"), 0, "Hai hợp đồng Chicilon Media, phạm vi, chào giá cạnh tranh"),
]
EXTRA_ITEMS = [
 ("Bổ sung", "Báo cáo 01-2025/BC-BQTSSR tính phí ngân hàng 247.500 đồng hai lần", "(2) Lỡ tay thật",
  "Chứng từ gốc đúng, cái sai chỉ ở khâu tổng hợp số liệu.", "Cao"),
 ("Bổ sung", "Sao kê in ngày 04/09/2026 nhưng chỉ tới 31/05/2026", "(2) nếu bổ sung ngay",
  "Ba tháng còn thiếu có đợt đáo hạn khoảng 110 tỷ, khoảng 5,17 tỷ tiền lãi và đợt tái tục 127,5 tỷ; từ chối hoặc trì hoãn cung cấp là dấu hiệu né tránh.", "Chờ trả lời"),
]
ND_TOP = ["Phần lớn sai sót thuộc nhóm thiếu năng lực: 9 trên 16 dấu hiệu là làm sai quy trình hoặc quản lý tiền kém, không thấy ai hưởng lợi.",
          "2 dấu hiệu là lỡ tay thật: sai giấy tờ, ghi chép, sửa được ngay.",
          "Chưa dấu hiệu nào đủ căn cứ để xếp vào lỡ tay có chủ đích.",
          "Tuy vậy, 4 dấu hiệu chưa loại trừ được khả năng này: 986,9 triệu qua TK vận hành 118002976372, 705,8 triệu trả Thép Quang, 4 hợp đồng liên tiếp của Thành Công và hợp đồng quảng cáo ký lại với Chicilon Media.",
          "Ba khoản chi trong nhóm này cộng lại khoảng 2,55 tỷ; để kết luận cần sao kê TK vận hành, danh mục thiết bị của Thép Quang, báo giá và biên bản nghiệm thu của Thành Công."]
assert round((986_910_176 + 705_769_875 + 856_792_068) / 1e9, 2) == 2.55
RULES = ["Mặc định là (1) hoặc (2) cho tới khi có bằng chứng ngược lại.",
         "Chỉ xếp vào (3) khi có ít nhất hai trong ba dấu hiệu rõ: cùng kiểu sai lặp lại; có bên hưởng lợi hoặc giá bất thường; chứng từ né tránh hoặc mâu thuẫn sau khi đã được yêu cầu.",
         "Dù nguyên nhân nào, khoản chi không đủ chứng từ vẫn phải làm rõ và hoàn lại quỹ, vi phạm đã rõ vẫn phải khắc phục và thuộc diện xử phạt; nguyên nhân chỉ quyết định cách xử lý trách nhiệm cá nhân.",
         "Kết luận vi phạm pháp luật thuộc về cơ quan có thẩm quyền; nhóm cư dân chỉ nêu dấu hiệu và yêu cầu giải trình."]
USE = ["Công văn chỉ nêu dữ kiện, quy định và hồ sơ đề nghị cung cấp; phân loại này là đánh giá sơ bộ, công khai cùng bộ tài liệu để Ban quản trị và cư dân cùng đối chiếu.",
       "Khi trích dẫn, luôn kèm điều kiện đổi nhóm; không tách riêng nhãn “chưa loại trừ (3)” ra khỏi ngữ cảnh.",
       "Với nhóm (1): đề nghị sửa quy trình, tách người lập và người duyệt lệnh, thuê kế toán hoặc kiểm toán hằng năm.",
       "Với 4 dấu hiệu chưa loại trừ (3): đòi đủ chứng từ trước khi chấp thuận bất kỳ khoản chi mới nào.",
       "Xác minh bằng file Hỏi dần: mỗi vấn đề có ba vòng câu hỏi, cách đọc câu trả lời và mục tương ứng trong công văn; kết quả từng vòng dùng để sửa nhóm trong file này.",
       "Xem lại toàn bộ phân loại khi hết hạn 15 ngày trả lời công văn."]
CAUSES = [("k1", "(1) Thiếu năng lực", "Làm theo thói quen hoặc quy định cũ; không nắm Quy chế, Luật Nhà ở 2023; thiếu người chuyên môn; hồ sơ lưu thiếu. Tiền về đúng người nhận, không ai hưởng lợi.",
           LG.CAUSE_HQ[1]),
          ("k2", "(2) Lỡ tay thật", "Sai một lần, sai kỹ thuật: nhầm tài khoản, tính trùng, ghi sai ngày, sai tỷ lệ. Chứng từ gốc đúng; sửa ngay khi được hỏi.",
           LG.CAUSE_HQ[2]),
          ("k3", "(3) Lỡ tay có chủ đích", "Cùng kiểu sai lặp lại; tiền đi qua tài khoản trung gian; hợp đồng chia nhỏ, trả trước toàn bộ; giá cao hơn thị trường; né tránh chứng từ.",
           LG.CAUSE_HQ[3])]
for s_ in [y for x in ALL for y in x[1:4]] + ND_TOP + RULES + USE:
    assert "→" not in s_ and "->" not in s_, s_[:50]

SEVC = {"Đỏ": "red", "Cam": "org", "Vàng": "yel"}
EXTRA = """
.hd { display:flex; justify-content:space-between; align-items:center; border-bottom:2pt solid #1F3864; padding-bottom:6pt; }
.hd .br { display:flex; gap:10pt; align-items:center; } .hd img { width:15mm; height:15mm; border-radius:50%; }
.hd .l1 { font-family:'Be Vietnam Pro',sans-serif; font-size:8.3pt; font-weight:800; letter-spacing:.12em; color:#1F3864; }
.hd .l2 { font-family:'Be Vietnam Pro',sans-serif; font-size:8.3pt; font-weight:600; color:#5a6475; }
.hd .dt { font-family:'Be Vietnam Pro',sans-serif; font-size:8pt; font-weight:700; color:#fff; background:#1F3864; border-radius:10pt; padding:2.5pt 9pt; }
.t1 { font-family:'Be Vietnam Pro',sans-serif; font-size:19pt; font-weight:800; color:#1F3864; line-height:1.18; margin-top:9pt; }
.t2 { font-family:'Be Vietnam Pro',sans-serif; font-size:9.6pt; color:#3d4656; margin-top:4pt; line-height:1.45; }
.warn { font-family:'Be Vietnam Pro',sans-serif; font-size:8.4pt; color:#6b5216; background:#FBF3DF; border:0.8pt solid #e6cf92; border-radius:4pt; padding:5pt 8pt; margin:7pt 0 4pt 0; line-height:1.45; }
.tiles { display:grid; grid-template-columns:repeat(4,1fr); gap:6pt; margin:7pt 0 2pt 0; }
.ptile { border:0.8pt solid #cfd8e6; border-top:4pt solid var(--c); border-radius:0 0 5pt 5pt; padding:6pt 8pt 7pt 8pt; background:var(--t); }
.ptile .n { font-family:'Be Vietnam Pro',sans-serif; font-size:24pt; font-weight:800; color:var(--c); line-height:1; }
.ptile .k { font-family:'Be Vietnam Pro',sans-serif; font-size:8.8pt; font-weight:800; color:#16294A; margin-top:3pt; }
.ptile .s { font-family:'Be Vietnam Pro',sans-serif; font-size:7.6pt; color:#3d4656; margin-top:2pt; line-height:1.35; }
.kk { font-family:'Be Vietnam Pro',sans-serif; font-size:8pt; font-weight:800; border-radius:10pt; padding:1.5pt 8pt; white-space:nowrap; display:inline-block; }
.k1 { background:#FBF3D9; color:#7F6000; border:0.8pt solid #e7cf86; } .k2 { background:#E6ECF5; color:#1F3864; border:0.8pt solid #b9c7dd; }
.k3 { background:#F8E3E3; color:#A93434; border:0.8pt solid #e6b9b9; } .k0 { background:#EDEDED; color:#404040; border:0.8pt solid #cfcfcf; }
.sh { font-family:'Be Vietnam Pro',sans-serif; display:flex; align-items:center; gap:8pt; background:#DCE6F1; border-radius:4pt; padding:5pt 9pt; margin:9pt 0 5pt 0; break-after:avoid; }
.sh .no { font-size:13pt; font-weight:800; color:#C8992F; } .sh h2 { font-size:12pt; font-weight:800; color:#1F3864; flex:1; }
.gh { display:flex; align-items:center; gap:8pt; margin:9pt 0 4pt 0; break-after:avoid; }
.gh .d { font-family:'Be Vietnam Pro',sans-serif; font-size:8.6pt; color:#3d4656; }
table.pl td { font-size:8.8pt; line-height:1.4; vertical-align:top; } table.pl tr { break-inside:avoid; }
table.pl td.code { font-family:'Be Vietnam Pro',sans-serif; font-weight:800; color:#1F3864; white-space:nowrap; }
table.pl .ttl { font-family:'Be Vietnam Pro',sans-serif; font-weight:700; color:#16294A; display:block; margin-bottom:2pt; }
.sev { font-family:'Be Vietnam Pro',sans-serif; font-size:7pt; font-weight:800; border-radius:8pt; padding:0.5pt 5pt; margin-left:3pt; }
.sev.red { background:#f7e3e3; color:#A93434; } .sev.org { background:#fbeadd; color:#C0662A; } .sev.yel { background:#fbf1d2; color:#7d5d00; }
table.ck td { font-size:8.6pt; line-height:1.35; vertical-align:top; } table.ck td b { font-family:'Be Vietnam Pro',sans-serif; }
.st-y { color:#A93434; font-weight:700; } .st-p { color:#C0662A; font-weight:700; } .st-u { color:#5b6474; font-weight:700; } .st-n { color:#1E7A46; font-weight:700; }
table.cz td { font-size:8.8pt; line-height:1.4; vertical-align:top; }
"""

def sh(no, t): return f'<div class="sh"><span class="no">{no}</span><h2>{E(t)}</h2></div>'
def sev(code):
    s = FIND[code]["sev"]; return f'<span class="sev {SEVC[s]}">{E(s)}</span>'
def gtable(rows):
    return table(["Mã", "Dấu hiệu và vì sao xếp vào nhóm này", "Đổi phân loại khi", "Tin cậy"],
                 [[f"{c}{sev(c)}", f'<span class="ttl">{E(t)}</span>{E(w)}', E(ch), E(cf)] for c, t, w, ch, cf in rows],
                 widths=["11%", "52%", "26%", "11%"], esc=False, tcls="pl")
def ghead(cls, lab, desc): return f'<div class="gh"><span class="kk {cls}">{E(lab)}</span><span class="d">{E(desc)}</span></div>'

head = (f'<div class="hd"><div class="br"><img alt="Logo Saigon South Residences" src="data:image/png;base64,{LOGO}"><div>'
        f'<div class="l1">TÀI LIỆU LÀM VIỆC · NHÓM CƯ DÂN GIÁM SÁT QUỸ BẢO TRÌ</div><div class="l2">Chung cư Nam Sài Gòn Residences</div></div></div>'
        f'<span class="dt">Lập ngày {TODAY}</span></div>'
        '<div class="t1">Phân loại nguyên nhân các sai sót của quỹ bảo trì</div>'
        '<div class="t2">16 dấu hiệu của báo cáo đầy đủ được xếp theo nguyên nhân: thiếu năng lực, lỡ tay thật hay lỡ tay có chủ đích. Phân loại này trả lời câu hỏi thứ ba trong năm câu hỏi của cuộc kiểm tra: mức độ vi phạm. Căn cứ: sao kê ba tài khoản 15/08/2024 – 31/05/2026 và tài liệu Ban quản trị gửi ngày 28/09/2026.</div>'
        '<div class="warn"><b>Đánh giá sơ bộ của nhóm cư dân, công khai cùng bộ tài liệu.</b> Phân loại dựa trên dữ liệu hiện có và sẽ xem lại khi Ban quản trị trả lời, cung cấp chứng từ. Các nhận định là dấu hiệu cần làm rõ, không phải cáo buộc; không thay thế kiểm toán hay kết luận của cơ quan có thẩm quyền.</div>')
tiles = ('<div class="tiles">'
         f'<div class="ptile" style="--c:#7F6000;--t:#FDF8EA"><div class="n">{len(G1)}</div><div class="k">(1) Thiếu năng lực</div><div class="s">Sai quy trình, quản lý tiền kém; không thấy ai hưởng lợi</div></div>'
         f'<div class="ptile" style="--c:#1F3864;--t:#F1F4F9"><div class="n">{len(G2)}</div><div class="k">(2) Lỡ tay thật</div><div class="s">Sai giấy tờ, ghi chép; sửa được ngay</div></div>'
         f'<div class="ptile" style="--c:#A93434;--t:#FBF1F1"><div class="n">{len(G3)}</div><div class="k">Chưa loại trừ (3)</div><div class="s">986,9 tr · Thép Quang · Thành Công · Chicilon Media</div></div>'
         f'<div class="ptile" style="--c:#5b6474;--t:#F4F4F4"><div class="n">{len(G0)}</div><div class="k">Chưa phát sinh sai</div><div class="s">Tái tục 127,5 tỷ, chờ hợp đồng</div></div>'
         '</div>')
s1 = sh("1", "Kết quả phân loại") + tiles + nd(ND_TOP, label="NHẬN ĐỊNH")
s2 = sh("2", "Tiêu chí phân loại") + table(["Nguyên nhân", "Biểu hiện trong hồ sơ", "Hướng xử lý và hệ quả"],
      [[f'<span class="kk {c}">{E(l)}</span>', E(a), E(b)] for c, l, a, b in CAUSES], widths=["18%", "44%", "38%"], esc=False, tcls="cz") + \
     nd(RULES, label="NGUYÊN TẮC")
s3 = (sh("3", "Phân loại 16 dấu hiệu")
      + '<p style="font-size:8.8pt;margin:0 0 2pt 0">Cột Tin cậy là mức chắc chắn của việc xếp nhóm với dữ liệu hiện có. Cột Đổi phân loại khi nêu điều kiện để chuyển dấu hiệu sang nhóm khác.</p>'
      + ghead("k1", "(1) Thiếu năng lực", f"{len(G1)} dấu hiệu") + gtable(G1)
      + ghead("k2", "(2) Lỡ tay thật", f"{len(G2)} dấu hiệu") + gtable(G2)
      + ghead("k3", "Chưa loại trừ (3) lỡ tay có chủ đích", f"{len(G3)} dấu hiệu, cần chứng từ để kết luận") + gtable(G3)
      + ghead("k0", "Chưa phát sinh sai", f"{len(G0)} dấu hiệu") + gtable(G0))
def st(v):
    cls = {"Có": "st-y", "Một phần": "st-p", "Chưa biết": "st-u", "Không": "st-n"}[v[0]]
    return f'<span class="{cls}">{E(v[0])}</span>: {E(v[1])}'
s4 = sh("4", "Bảng kiểm ba dấu hiệu của lỡ tay có chủ đích") + table(
    ["Mã", "Khoản", "Lặp lại cùng kiểu", "Hưởng lợi, giá bất thường", "Chứng từ né tránh, mâu thuẫn", "Số dấu hiệu rõ", "Chứng từ quyết định"],
    [[f"<b>{c}</b>", E(a), st(x), st(y), st(z), f"<b>{n}/3</b>", E(k)] for c, a, x, y, z, n, k in CHECK],
    widths=["6%", "10%", "15%", "17%", "17%", "10%", "25%"], esc=False, tcls="ck") + \
    '<p style="font-size:8.8pt;margin-top:4pt">Cần ít nhất 2/3 dấu hiệu rõ mới xếp vào (3). Hiện chưa khoản nào đạt; F01 và F07 mới có một dấu hiệu rõ là lặp lại cùng kiểu.</p>'
s5 = '<div style="break-inside:avoid">' + sh("5", "Hai điểm phát sinh thêm ngoài 16 dấu hiệu") + table(
    ["Điểm", "Phân loại", "Vì sao", "Tin cậy"],
    [[f"<b>{E(b)}</b>", E(c), E(d), E(e)] for a, b, c, d, e in EXTRA_ITEMS],
    widths=["30%", "16%", "43%", "11%"], esc=False, tcls="cz") + nd(USE, label="CÁCH DÙNG", gold=True) + '</div>'

s6 = sh("6", "Hệ quả pháp lý của từng dấu hiệu") + \
     '<p style="font-size:8.8pt;margin:0 0 3pt 0">Cùng khung với báo cáo đầy đủ (mục 11.1, Phụ lục A) và dashboard. Nguyên nhân ở các mục trên chỉ quyết định cách xử lý trách nhiệm cá nhân; hệ quả dưới đây áp dụng theo tình trạng của dấu hiệu.</p>' + \
     table(["Mã", "Tình trạng", "Hệ quả", "Nếu không giải trình được"],
           [[f"<b>{c}</b>{sev(c)}", LG.lg_pill(E, c), (f"<i style=\"font-style:normal;font-weight:700;color:#1F3864\">{E(LG.LG_HQLAB[LG.LG_F[c][0]])}:</i> " if LG.LG_HQLAB[LG.LG_F[c][0]] else "") + E(LG.LG_F[c][1]), f"<i style=\"font-style:normal;font-weight:700;color:#1F3864\">{E(LG.lg_of(c)[5])}:</i> {E(LG.LG_F[c][2])}"] for c in sorted(FIND)],
           widths=["10%", "14%", "38%", "38%"], esc=False, tcls="pl") + \
     nd(LG.LG_ND, label=LG.LG_ND_LABEL) + f'<div class="lgnote">{E(LG.LG_NOTE)}</div>'
if __name__ == "__main__":   # chi dung file khi chay truc tiep; khi import chi lay du lieu (tranh vong import voi ketluan5)
    import ketluan5 as K5
    fonts = open("bvp_fonts.css").read()
    doc = (f'<!doctype html><html lang="vi"><head><meta charset="utf-8"><style>{fonts}{CSS}{EXTRA}{KMC_CSS}{LG.LG_CSS}{K5.CSS}</style></head><body>'
           + head + '<div style="margin:7pt 0 2pt 0">' + km_compact_html(E, hq=True) + '</div>' + K5.k5_strip(E) + s1 + s2 + s3 + s4 + s5 + s6 + "</body></html>")
    open("phanloai.html", "w", encoding="utf-8").write(doc)
    print("html", len(doc), "groups", len(G1), len(G2), len(G3), len(G0))
