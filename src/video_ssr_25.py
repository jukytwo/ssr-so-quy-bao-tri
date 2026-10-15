# -*- coding: utf-8 -*-
"""BO CLIP 25 PHUT (04/10/2026, anh Vu duyet): 1 ban ngang day du, 6 phan ngang, 11 clip doc theo chu de.
Mo rong tu video_ssr_one2 (ban 11 phut): moi van de them canh chung tu, dieu khoan, viec can lam ro; them phan Quy che ap dung;
doc du muoi cau hoi. File moi, khong dung toi file cu. Nhan dien SSR, khong TVN, khong ten ca nhan. Giong Gemini Achernar.
Chay:  CLIP_RES=1080 python3 video_ssr_25.py full|part N|doc N|list"""
import sys, os, json, time, subprocess
os.environ.setdefault("CLIP_RES", "1080")
sys.path.insert(0, "/home/claude/ssr"); os.chdir("/home/claude/ssr")
# ---- TONG MAU SSR (anh Vu 04/10/2026: "tong mau clip phai theo tong mau chu dao theo logo SSR"): xanh luc bao cua logo Phu My Hung
# va vang kim cua vanh logo thay cho navy. Nap ban to mau cua cac module dung clip ngay khi import, khong sua file goc (clip cu van dung lai duoc).
import re as _re, types as _types
THEME = [  # tong SSR Dieu Hanh (anh Vu 04/10/2026 gui mau): xanh rung sau chuyen dam, quang sang xanh goc tren trai, chu kem vang, tieu de serif
    (".wm{{font-weight:700;font-size:46px;letter-spacing:.04em;color:#E3C070", ".wm{{font-family:'Cormorant Garamond',serif;font-size-adjust:.52;font-variant-numeric:lining-nums;font-weight:700;font-size:46px;letter-spacing:.02em;color:#E8D59A"),
    ("<style>{fonts}", "<style>{fonts}@import url(file:///home/claude/ssr/fonts/cormorant.css);"),
    ("radial-gradient(900px 560px at 88% 0%,rgba(200,153,47,.22),transparent 70%)", "radial-gradient(1200px 760px at 0% 0%,rgba(70,140,95,.50),transparent 70%)"),
    ("radial-gradient(900px 520px at 85% 8%,rgba(200,153,47,.20),transparent 70%)", "radial-gradient(1000px 700px at 0% 0%,rgba(70,140,95,.50),transparent 70%)"),
    ("#1F3864", "#1E4630"), ("31, 56, 100", "30, 70, 48"), ("#13294B", "#12301F"), ("19, 41, 75", "18, 48, 31"),
    ("#16305A", "#24543A"), ("#0E1F3A", "#0B1F14"), ("(0, 50, 100)", "(30, 70, 48)"),
    ("#E3C070", "#E3C878"), ("227, 192, 112", "227, 200, 120"), ("#C8992F", "#B8913A"), ("200, 153, 47", "184, 145, 58"), ("200,153,47", "184,145,58"),
    ("#D9E1EC", "#DCE5DC"), ("#C9D3E3", "#C9D6CB"), ("#E8EEF8", "#E9EFE7"), ("#DCE4F2", "#DDE7DC"), ("#EEF2F7", "#EEF2EC"),
    ("#E3E8EF", "#E2E9E1"), ("#EDF1F7", "#EBF0EA"), ("#F4F6F9", "#F5F7F2"), ("#9AA7B8", "#95A598"),
    ("#4A5566", "#4A5A4F"), ("#5B6475", "#5A6B60"), ("#5B6474", "#5A6B60"), ("#6B7686", "#687A6D")]
SERIF_CSS = open("/home/claude/ssr/fonts/cormorant.css").read() + """
h1.ttl,.t-cover h1,.t-contact h1{font-family:'Cormorant Garamond','Times New Roman',serif;font-size-adjust:.52;font-weight:700;letter-spacing:0;font-variant-numeric:lining-nums;line-height:1.24}
.dark h1.ttl,.t-cover h1.ttl,.t-contact h1.ttl{color:#F1E6C6}"""
def _themed(name, path):
    src = open(path, encoding="utf-8").read()
    for a, b in THEME: src = _re.sub(_re.escape(a), b, src, flags=_re.I)
    m = _types.ModuleType(name); m.__file__ = path; sys.modules[name] = m
    exec(compile(src, path, "exec"), m.__dict__); return m
for _p in ("/home/claude/gv", "/home/claude/vtpl", "/home/claude/vshim"): sys.path.insert(0, _p)
_themed("build_video", "/home/claude/vtpl/build_video.py")
for _n in ("luudo", "video_ssr", "video_ssr_nn", "flowclip"): _themed(_n, f"/home/claude/ssr/{_n}.py")
import video_ssr_one2 as O
O.BV._SCENE_CSS += SERIF_CSS
VS, NN, FC, BV = O.VS, O.NN, O.FC, O.BV
OUT = "/home/claude/ssr/video25"; os.makedirs(OUT, exist_ok=True)

def S(sec, icon): return dict(sec=sec, icon=icon)
S1, S2 = S("Tiền có mất không", "view"), S("Toàn cảnh dòng tiền", "money")
SV = {i: S(f"Vấn đề {i}", "money") for i in range(1, 6)}
SQC = S("Quy chế áp dụng", "company")
FL = {sid: (v, [x for x in O.VS_FLOW if x[0].split("#")[0] == sid]) for sid, v in zip(["f0", "f1", "f2", "f3", "f4", "f5"], O.V_FLOW)}

# ---------------- 11 chu de: (canh, loi doc) ----------------
SEG = {}
SEG[1] = dict(name="Tiền quỹ có mất không", short="Tiền có mất không", vis=[
 O.V_ONE[0],
 dict(id="kt", type="timeline", **S1, tag="Cách kiểm tra", title="Bốn bước trước khi kết luận",
      items=[{"d": "Bước 1", "h": "Sao kê", "t": "Đọc **3 tài khoản** từ 15/08/2024 tới 31/05/2026"},
             {"d": "Bước 2", "h": "Khớp số dư", "t": "**198 giao dịch**, khớp tới từng đồng"},
             {"d": "Bước 3", "h": "Đối chiếu", "t": "Từng khoản chi với **Quy chế thu chi** và Luật Nhà ở"},
             {"d": "Bước 4", "h": "Hỏi bằng văn bản", "t": "**Mười câu hỏi** gửi Ban quản trị ngày 29/09/2026"}]),
 dict(id="dung", type="stats", **S1, tag="Ghi nhận việc làm đúng", title="Những việc Ban quản trị đã làm đúng",
      tiles=[["9", "lệnh chi chuyển thẳng cho nhà thầu", "g", "Đúng **Điều 7.2** Quy chế."],
             ["127,15 tỷ", "tiền gốc, từ 124,79 tỷ lúc nhận bàn giao", "g", "Nhờ **5,48 tỷ** tiền lãi."],
             ["105 tỷ", "gửi có kỳ hạn, lãi 4,7% một năm", "g", "Tại **VietinBank và Agribank**."],
             ["3", "báo cáo quỹ Ban quản trị đã lập", "g", "**14/05/2025, 15/05/2026, 15/09/2026**."]])],
 vs=[("ok#-2", "Trước hết, tiền có mất không?", True),
     ("ok#0", "Chưa thấy mất: 198 giao dịch của ba tài khoản khớp số dư tới từng đồng."),
     ("ok#1", "Không có lệnh rút tiền mặt, không có khoản chuyển cho cá nhân."),
     ("ok#1", "Tiền chỉ đi tới doanh nghiệp, Kho bạc, hoặc tài khoản do Ban quản trị đứng tên."),
     ("ok#2", "Tiền gốc còn 127,15 tỷ đồng vào ngày 31/05/2026."),
     ("ok#-1", "Vì vậy, câu hỏi không phải là tiền có biến mất hay không, mà là tiền có đi đúng đường và đúng thẩm quyền hay không."),
     ("kt#-1", "Câu trả lời này đến từ bốn bước kiểm tra."),
     ("kt#0", "Bước một, đọc sao kê của ba tài khoản từ ngày 15/08/2024 tới ngày 31/05/2026."),
     ("kt#1", "Bước hai, cộng trừ lại 198 giao dịch, số dư khớp tới từng đồng."),
     ("kt#2", "Bước ba, đặt từng khoản chi cạnh Quy chế thu chi mà Hội nghị đã thông qua, và Luật Nhà ở."),
     ("kt#3", "Bước bốn, những chỗ chưa rõ được hỏi Ban quản trị bằng văn bản, mười câu, gửi ngày 29/09/2026."),
     ("dung#-1", "Cũng cần ghi nhận những việc Ban quản trị đã làm đúng."),
     ("dung#0", "Chín lệnh chi từ quỹ được chuyển thẳng cho nhà thầu, đúng Điều 7.2 Quy chế."),
     ("dung#1", "Tiền gốc tăng từ 124,79 tỷ lúc nhận bàn giao lên 127,15 tỷ, nhờ 5,48 tỷ tiền lãi."),
     ("dung#2", "Phần lớn tiền quỹ, 105 tỷ, được gửi có kỳ hạn tại VietinBank và Agribank với lãi 4,7% một năm."),
     ("dung#3", "Ban quản trị đã lập báo cáo quỹ ba lần, ngày 14/05/2025, 15/05/2026 và 15/09/2026."),
     ("dung#-1", "Nhưng sao kê cũng cho thấy tiền đi sai đường ở nhiều chỗ.")])

SEG[2] = dict(name="Toàn cảnh dòng tiền của quỹ", short="Toàn cảnh dòng tiền", vis=[
 dict(id="tk4", type="tickets", **S2, tag="Trước khi xem lưu đồ", title="Bốn tài khoản cần nhớ",
      items=[{"t": "4999", "a": "VietinBank", "tone": "g", "z": "Tài khoản quỹ bảo trì", "note": "Nhận **124,79 tỷ** ngày 15/08/2024"},
             {"t": "0476", "a": "Agribank", "tone": "y", "z": "Tài khoản quỹ thứ hai", "note": "Nhận **60 tỷ** ngày 21/08/2024"},
             {"t": "7784", "a": "Thu phí dịch vụ", "tone": "r", "z": "Nằm ngoài quỹ", "note": "Nhận **1,71 tỷ** tiền khu vực chung"},
             {"t": "6372", "a": "Vận hành", "tone": "r", "z": "Ban quản trị đứng tên", "note": "Nhận **986,9 triệu** từ quỹ, chưa có sao kê"}]),
 FL["f0"][0]],
 vs=[("tk4#-2", "Trước khi xem lưu đồ, có bốn tài khoản cần nhớ.", True),
     ("tk4#0", "Tài khoản quỹ chính tại VietinBank, đuôi 4999, nhận 124,79 tỷ từ chủ đầu tư ngày 15/08/2024."),
     ("tk4#1", "Tài khoản thứ hai tại Agribank, đuôi 0476, nhận 60 tỷ ngày 21/08/2024 để gửi có kỳ hạn."),
     ("tk4#2", "Tài khoản thu phí dịch vụ, đuôi 7784, nhận 1,71 tỷ tiền khai thác khu vực chung, nằm ngoài quỹ."),
     ("tk4#3", "Và tài khoản vận hành do Ban quản trị đứng tên, đuôi 6372, nhận 986,9 triệu từ quỹ, hiện chưa có sao kê.")] + FL["f0"][1])

SEG[3] = dict(name="Vấn đề 1: 986,9 triệu vào tài khoản của Ban quản trị", short="Vấn đề 1: 986,9 triệu vào tài khoản Ban quản trị", vis=[
 FL["f1"][0],
 dict(id="v1a", type="timeline", **SV[1], tag="Sáu khoản được hoàn ứng", title="Ứng từ tháng 8, hoàn gộp một lần tháng 12",
      items=[{"d": "29/08/2025", "h": "Khoản 1", "t": "Chứng từ **đầu tiên** được ứng"},
             {"d": "Tháng 10", "h": "Khoản 2 tới 4", "t": "Ngày **03, 14 và 21/10**"},
             {"d": "11/12/2025", "h": "Khoản 5", "t": "Thang máy, **PCCC**, máy phát điện"},
             {"d": "23/12/2025", "h": "Khoản 6", "t": "Chứng từ cuối, **cùng ngày** lệnh hoàn"},
             {"d": "23/12/2025", "h": "Hoàn gộp", "t": "**986,9 triệu** vào tài khoản đuôi 6372"}]),
 dict(id="v1b", type="tickets", **SV[1], tag="Năm quy định liên quan", title="Ba điều đã rõ, hai điều chờ văn bản",
      items=[{"t": "Đ 7.2", "a": "Đã rõ", "tone": "r", "z": "Chỉ chuyển cho đơn vị bảo trì", "note": "Tiền lại vào **tài khoản Ban quản trị**"},
             {"t": "Đ 7.4", "a": "Đã rõ", "tone": "r", "z": "Tạm dùng tối đa 10 triệu mỗi tháng", "note": "Gấp **khoảng 20 lần**, không hoàn cuối tháng"},
             {"t": "Đ 3.2.a", "a": "Đã rõ", "tone": "r", "z": "Công ty quản lý đứng tên", "note": "VietinBank xác nhận **6 thành viên** đồng chủ tài khoản"},
             {"t": "Đ 9.2", "a": "Chờ văn bản", "tone": "o", "z": "Trên 50 triệu cần hơn 50% chủ sở hữu", "note": "Chưa thấy **văn bản lấy ý kiến**"},
             {"t": "75%", "a": "Chờ biên bản", "tone": "o", "z": "Thành viên đồng ý chi kinh phí bảo trì", "note": "Quy chế hoạt động, **Điều 3**"}]),
 dict(id="v1c", type="stats", **SV[1], tag="Một câu hỏi đi kèm", title="Phí bảo trì thang máy vắng mặt từ 21/01/2025",
      tiles=[["57,5 triệu", "phí bảo trì Schindler mỗi tháng", "n", "**18 thang** máy."],
             ["16", "tháng không thấy phí trên tài khoản quỹ", "o", "Từ **21/01/2025** tới 31/05/2026."],
             ["0,94 tỷ", "phí ước tính của 16 tháng", "o", "Nếu hợp đồng **vẫn tiếp tục**."]])],
 vs=FL["f1"][1] + [
     ("v1a#-1", "Nhìn kỹ hơn sáu khoản được hoàn ứng."),
     ("v1a#0", "Khoản đầu tiên có chứng từ ngày 29/08/2025."),
     ("v1a#1", "Ba khoản tiếp theo trong tháng 10, ngày 03, 14 và 21."),
     ("v1a#2", "Nội dung ghi chung là sửa chữa thang máy, phòng cháy chữa cháy và máy phát điện, chưa tách từng việc."),
     ("v1a#3", "Khoản cuối có chứng từ ngày 23/12, cùng ngày với lệnh hoàn."),
     ("v1a#4", "Cả sáu khoản được hoàn gộp một lần, 986,9 triệu đồng, vào tài khoản vận hành."),
     ("v1b#-1", "Lệnh chuyển này chạm tới năm quy định."),
     ("v1b#0", "Điều 7.2: tiền quỹ chỉ được chuyển cho đơn vị làm bảo trì, không qua tài khoản trung gian."),
     ("v1b#1", "Điều 7.4: chỉ được tạm dùng tiền vận hành tối đa 10 triệu mỗi tháng và phải hoàn ngay cuối tháng."),
     ("v1b#2", "Điều 3.2.a: tài khoản vận hành do công ty quản lý đứng tên. Nhưng thư xác nhận của VietinBank cho thấy tài khoản này do 6 thành viên Ban quản trị đồng đứng tên."),
     ("v1b#3", "Điều 9.2: sửa chữa khẩn cấp trên 50 triệu phải được hơn một nửa chủ sở hữu đồng ý. Chưa thấy văn bản này."),
     ("v1b#4", "Và Quy chế hoạt động yêu cầu 75% thành viên Ban quản trị đồng ý khi chi kinh phí bảo trì. Cần xem biên bản họp."),
     ("v1b#-1", "Ba điều đầu đã rõ trên sao kê; hai điều sau cần văn bản để kết luận."),
     ("v1c#-1", "Đi kèm vấn đề này là một câu hỏi về thang máy."),
     ("v1c#0", "Phí bảo trì Schindler là 57,5 triệu đồng mỗi tháng cho 18 thang."),
     ("v1c#1", "Từ ngày 21/01/2025 tới 31/05/2026, tài khoản quỹ không còn khoản phí định kỳ nào, ngoài khoản hoàn gộp 986,9 triệu."),
     ("v1c#2", "Nếu hợp đồng vẫn tiếp tục, phí của 16 tháng này vào khoảng 0,94 tỷ đồng."),
     ("v1c#-1", "Hoặc phí đã trả từ tài khoản vận hành, hoặc Schindler đang bị nợ phí. Sao kê tài khoản vận hành sẽ trả lời câu này.")])

SEG[4] = dict(name="Vấn đề 2: tiền khu vực chung nằm ngoài quỹ", short="Vấn đề 2: tiền khu vực chung ngoài quỹ", vis=[
 FL["f2"][0],
 dict(id="v2a", type="timeline", **SV[2], tag="Dòng tiền khu vực chung", title="Từ đúng tài khoản quỹ sang tài khoản ngoài quỹ",
      items=[{"d": "01/10/2024", "h": "Chicilon Media", "t": "Quảng cáo khoảng **87 triệu** mỗi tháng"},
             {"d": "05/01/2025", "h": "Ký lại", "t": "Còn **71,8 triệu** mỗi tháng, giảm 17,5%"},
             {"d": "16/07/2025", "h": "Vào đúng quỹ", "t": "**260,9 triệu** tiền thuê quý 4/2024"},
             {"d": "24/07/2025", "h": "Chuyển ra", "t": "Sang tài khoản **đuôi 7784**, ghi là trả nhầm"},
             {"d": "07/2025 tới 05/2026", "h": "Ngoài quỹ", "t": "**1,71 tỷ** từ Chicilon, Viễn thông ACT, Hưng Thái"}]),
 dict(id="v2b", type="tickets", **SV[2], tag="1,40 tỷ đã chi từ tài khoản ngoài quỹ", title="Ba nhà thầu, sáu hợp đồng, đều trên 50 triệu",
      items=[{"t": "856,8", "a": "4 hợp đồng", "tone": "o", "z": "triệu, Thành Công", "note": "Hai hợp đồng **trả 100%** trước nghiệm thu"},
             {"t": "356,4", "a": "vượt 23%", "tone": "o", "z": "triệu, Khởi Sáng Việt", "note": "Giữ xe, trả **hơn 67,1 triệu** so với hợp đồng"},
             {"t": "187,0", "a": "tạm ứng 40%", "tone": "o", "z": "triệu, KTECH", "note": "Sửa, lắp **camera**"}])],
 vs=FL["f2"][1] + [
     ("v2a#-1", "Dòng tiền khu vực chung đi qua năm mốc."),
     ("v2a#0", "Ngày 01/10/2024, hợp đồng quảng cáo với Chicilon Media có giá khoảng 87 triệu đồng mỗi tháng."),
     ("v2a#1", "Ngày 05/01/2025, hợp đồng ký lại chỉ còn 71,8 triệu mỗi tháng, giảm 17,5%, tức khoảng 182 triệu mỗi năm."),
     ("v2a#2", "Ngày 16/07/2025, Chicilon trả 260,9 triệu vào đúng tài khoản quỹ."),
     ("v2a#3", "Tám ngày sau, khoản này bị chuyển sang tài khoản đuôi 7784 với lý do trả nhầm, dù theo luật tài khoản quỹ mới là tài khoản đúng."),
     ("v2a#4", "Từ tháng 7/2025 tới tháng 5/2026, toàn bộ 1,71 tỷ từ Chicilon Media, Viễn thông ACT và Hưng Thái đều vào tài khoản ngoài quỹ."),
     ("v2a#-1", "Nếu giá quảng cáo giảm vì đổi số màn hình hay vị trí, Ban quản trị cần văn bản giải thích."),
     ("v2b#-1", "Từ tài khoản ngoài quỹ này, 1,40 tỷ đã chi cho ba nhà thầu."),
     ("v2b#0", "Thành Công nhận 856,8 triệu qua bốn hợp đồng, chiếm 61% số tiền sửa chữa. Hai hợp đồng được trả trọn chỉ 3 và 18 ngày sau khi ký."),
     ("v2b#0", "Một hợp đồng là xây nhà để hàng hóa, 165,8 triệu. Xây mới trên phần sở hữu chung không phải bảo trì, phải do Hội nghị quyết định."),
     ("v2b#1", "Khởi Sáng Việt sửa hệ thống giữ xe: tạm ứng 40% là 115,7 triệu, tức hợp đồng khoảng 289,3 triệu, nhưng tổng đã trả 356,4 triệu, cao hơn 67,1 triệu."),
     ("v2b#2", "KTECH sửa và lắp camera, 187 triệu."),
     ("v2b#-1", "Cả ba đều không qua kế hoạch bảo trì, ba báo giá và nghiệm thu như tiền quỹ phải có.")])

SEG[5] = dict(name="Vấn đề 3: 13 khoản chi trên 50 triệu", short="Vấn đề 3: 13 khoản chi trên 50 triệu", vis=[
 FL["f3"][0],
 dict(id="v3a", type="tickets", **SV[3], tag="Điều 9.2 · Ban quản trị tự quyết tới 50 triệu", title="13 khoản trên 50 triệu, tổng 5,04 tỷ",
      items=[{"t": "1,25", "a": "25 lần", "tone": "r", "z": "tỷ, HNB, cấp nước", "note": "Ký 07/04/2026, **tạm ứng 50%**"},
             {"t": "986,9", "a": "20 lần", "tone": "r", "z": "triệu, hoàn ứng", "note": "Vào **tài khoản Ban quản trị**"},
             {"t": "705,8", "a": "14 lần", "tone": "r", "z": "triệu, Thép Quang", "note": "**Trả 100%** sau 16 ngày"},
             {"t": "477,1", "a": "9,5 lần", "tone": "o", "z": "triệu, Schindler", "note": "Sửa thang máy, tạm ứng 50%"},
             {"t": "350,7", "a": "7 lần", "tone": "o", "z": "triệu, Thành Công", "note": "**Trả 100%** sau 3 ngày"},
             {"t": "289,3", "a": "5,8 lần", "tone": "o", "z": "triệu, Khởi Sáng Việt", "note": "Giữ xe, trả vượt 67,1 triệu"}]),
 dict(id="v3b", type="stats", **SV[3], tag="Thang máy", title="806,9 triệu cho Schindler qua 7 lệnh",
      tiles=[["806,9 triệu", "chuyển cho Schindler", "o", "Từ **04/04 tới 23/06/2025**."],
             ["14", "hợp đồng sửa chữa mã EID FR", "o", "Trong khoảng **7 tháng**."],
             ["5 tới 6", "tháng trả trễ", "o", "Phí bảo trì và **4 hợp đồng** cuối 2024."]]),
 dict(id="v3c", type="timeline", **SV[3], tag="Quy trình một khoản chi lớn", title="Năm bước trước khi tiền rời quỹ",
      items=[{"d": "1", "h": "Kế hoạch", "t": "Hội nghị thông qua, hoặc **hơn 50% chủ sở hữu** đồng ý"},
             {"d": "2", "h": "Chọn thầu", "t": "Công khai, **3 báo giá** cho việc trên 10 triệu"},
             {"d": "3", "h": "Ban quản trị", "t": "**50%** chọn nhà thầu, **75%** đồng ý chi"},
             {"d": "4", "h": "Nghiệm thu", "t": "Biên bản, chứng từ **3 chữ ký**"},
             {"d": "5", "h": "Thanh toán", "t": "Chuyển thẳng cho **nhà thầu**"}])],
 vs=FL["f3"][1] + [
     ("v3a#-1", "Điều 9.2 chỉ cho Ban quản trị tự quyết việc khẩn cấp tới 50 triệu. Có 13 khoản vượt mức này, tổng 5,04 tỷ."),
     ("v3a#0", "Lớn nhất là hợp đồng cấp nước với HNB, khoảng 1,25 tỷ, gấp 25 lần mức tự quyết."),
     ("v3a#1", "Tiếp theo là khoản hoàn ứng 986,9 triệu, gấp khoảng 20 lần."),
     ("v3a#2", "Thép Quang 705,8 triệu, gấp 14 lần."),
     ("v3a#3", "Hợp đồng sửa thang máy Schindler 477,1 triệu, gấp 9,5 lần."),
     ("v3a#4", "Thành Công 350,7 triệu và Khởi Sáng Việt 289,3 triệu, gấp 7 và 5,8 lần."),
     ("v3a#-1", "Tính cả hai tài khoản, chi sửa chữa năm 2025 là 2,89 tỷ, năm tháng đầu 2026 là 1,63 tỷ, đều vượt trần 500 triệu mỗi năm nếu không nằm trong kế hoạch bảo trì được thông qua."),
     ("v3b#-1", "Riêng thang máy, quỹ đã trả Schindler 806,9 triệu qua 7 lệnh, từ ngày 04/04 tới 23/06/2025."),
     ("v3b#1", "Bảy hợp đồng sửa chữa được trả gộp một lệnh 180,8 triệu, bốn hợp đồng khác gộp 154,7 triệu. Từng hợp đồng dưới 50 triệu, nhưng cộng lại vượt mức."),
     ("v3b#2", "Phí bảo trì và bốn hợp đồng cuối năm 2024 được trả trễ 5 tới 6 tháng."),
     ("v3b#-1", "Tiền trả thẳng cho Schindler nên rủi ro gian lận thấp. Điều cần xem là sửa chữa lặp lại mà cư dân vẫn phản ánh thang máy, và giấy kiểm định an toàn của từng thang."),
     ("v3c#-1", "Theo Quy chế, một khoản chi lớn phải qua năm bước."),
     ("v3c#0", "Một, có trong kế hoạch bảo trì Hội nghị đã thông qua, hoặc được hơn một nửa chủ sở hữu đồng ý."),
     ("v3c#1", "Hai, chọn thầu công khai, việc trên 10 triệu phải có ba báo giá."),
     ("v3c#2", "Ba, ít nhất một nửa thành viên Ban quản trị chọn nhà thầu, và 75% thành viên đồng ý chi."),
     ("v3c#3", "Bốn, nghiệm thu, chứng từ thanh toán có đủ ba chữ ký."),
     ("v3c#4", "Năm, chuyển tiền thẳng cho nhà thầu."),
     ("v3c#-1", "Với 13 khoản trên, sao kê chỉ cho thấy tiền đã chuyển. Bốn bước đầu cần Ban quản trị đưa văn bản ra.")])

SEG[6] = dict(name="Vấn đề 4: tiền chưa truy được tới hàng hóa", short="Vấn đề 4: 705,8 triệu trả Thép Quang", vis=[
 FL["f4"][0],
 dict(id="v4a", type="tickets", **SV[4], tag="Để khép lại 1,69 tỷ", title="Sáu loại chứng từ cần có",
      items=[{"t": "1", "a": "Danh mục", "tone": "o", "z": "Chủng loại, số lượng, đơn giá", "note": "Thiết bị **Thép Quang** đã giao"},
             {"t": "2", "a": "Hóa đơn", "tone": "o", "z": "Hóa đơn giá trị gia tăng", "note": "Khớp **705,8 triệu**"},
             {"t": "3", "a": "Nghiệm thu", "tone": "o", "z": "Biên bản giao nhận, nghiệm thu", "note": "Đủ **3 chữ ký**"},
             {"t": "4", "a": "Báo giá", "tone": "o", "z": "Ba báo giá cạnh tranh", "note": "Điều **6.3.e**"},
             {"t": "5", "a": "Mã số thuế", "tone": "o", "z": "Hồ sơ năng lực nhà thầu", "note": "Chưa tra được **đúng tên**"},
             {"t": "6", "a": "Sao kê", "tone": "r", "z": "Tài khoản vận hành đuôi 6372", "note": "Biết **986,9 triệu** trả cho ai"}])],
 vs=FL["f4"][1] + [
     ("v4a#-1", "Để khép lại 1,69 tỷ này, cần sáu loại chứng từ."),
     ("v4a#0", "Danh mục thiết bị Thép Quang đã giao: chủng loại, số lượng, đơn giá, xuất xứ."),
     ("v4a#1", "Hóa đơn giá trị gia tăng khớp với 705,8 triệu."),
     ("v4a#2", "Biên bản giao nhận và nghiệm thu, có đủ ba chữ ký."),
     ("v4a#3", "Ba báo giá cạnh tranh theo Điều 6.3.e."),
     ("v4a#4", "Mã số thuế và hồ sơ năng lực của Thép Quang, vì tra cứu nhanh trên các trang công khai chưa thấy doanh nghiệp đúng tên này."),
     ("v4a#5", "Và sao kê tài khoản vận hành, để biết 986,9 triệu cuối cùng đã trả cho ai."),
     ("v4a#-1", "Có đủ chứng từ hợp lệ thì khép lại. Không có thì phải bồi hoàn quỹ theo Điều 10.1.")])

SEG[7] = dict(name="Vấn đề 5: 127,5 tỷ tiền gửi sau tái tục", short="Vấn đề 5: 127,5 tỷ tiền gửi", vis=[
 FL["f5"][0],
 dict(id="v5a", type="timeline", **SV[5], tag="Tiền gửi qua các mốc", title="Tiền gửi có kỳ hạn chiếm 98% quỹ",
      items=[{"d": "04/07/2024", "h": "Agribank", "t": "Mở tài khoản thứ hai, **trước khi nhận quỹ**"},
             {"d": "21/08/2024", "h": "60 tỷ", "t": "Chuyển sang Agribank, gửi **12 tháng**"},
             {"d": "Hằng quý", "h": "15 tỷ", "t": "Kỳ hạn 3 tháng, lãi **1,9 tới 2,4%**"},
             {"d": "21/05/2025", "h": "Kiểm toán", "t": "Xác nhận số dư năm 2024; **năm 2025 chưa thấy**"},
             {"d": "15/09/2026", "h": "Tái tục", "t": "Thông báo **127,5 tỷ**, lãi 8%, chưa có xác nhận"}])],
 vs=FL["f5"][1] + [
     ("v5a#-1", "Tiền gửi có kỳ hạn chiếm 98% quỹ, nên đây là phép kiểm tra quan trọng nhất."),
     ("v5a#0", "Tài khoản Agribank mở ngày 04/07/2024, trước khi nhận quỹ. Sổ phụ ghi không phải tài khoản đồng sở hữu, trong khi Điều 3.1.a yêu cầu ít nhất ba thành viên cùng đứng tên."),
     ("v5a#1", "Ngày 21/08/2024, 60 tỷ được chuyển sang Agribank và gửi kỳ hạn 12 tháng."),
     ("v5a#2", "Khoản 15 tỷ chỉ gửi kỳ hạn 3 tháng, lãi 1,9 tới 2,4% một năm, trong khi các khoản lớn hưởng 4,7%. Tính cả số dư nhàn rỗi, tiền lãi bỏ lỡ khoảng 0,42 tới 0,96 tỷ."),
     ("v5a#3", "Chỉ thấy một lần phí xác nhận số dư ngày 21/05/2025, thường dùng cho kiểm toán năm 2024. Chưa thấy dấu vết kiểm toán năm 2025, trong khi Quy chế yêu cầu kiểm toán độc lập hằng năm."),
     ("v5a#4", "Ngày 15/09/2026, Ban quản trị thông báo đã tái tục thành năm hợp đồng, tổng 127,5 tỷ, lãi 8% một năm, nhưng chưa có hợp đồng và xác nhận của ngân hàng."),
     ("v5a#-1", "Chưa có dấu hiệu thất thoát, nhưng chỉ nhìn sao kê tài khoản thanh toán thì chưa thể khẳng định tiền còn đủ.")])

SEG[8] = dict(name="Quy chế đang áp dụng", short="Quy chế áp dụng", vis=[
 dict(id="qc1", type="stats", **SQC, tag="Hai bộ quy chế đang lưu hành", title="Clip dùng bản Hội nghị thông qua ngày 26/05/2024",
      tiles=[["50 trang", "bản dự thảo", "y", "Gửi kèm công văn **16/11/2023**, còn để ngỏ phương án."],
             ["42 trang", "bản Hội nghị thông qua", "g", "Ngày **26/05/2024**, đã chốt từng phương án."]]),
 dict(id="qc2", type="tickets", **SQC, tag="Điều đã thay đổi so với dự thảo", title="Thay đổi nằm ở tổ chức Ban quản trị",
      items=[{"t": "9", "a": "thành viên", "tone": "n", "z": "Tối thiểu, mỗi block ít nhất 1", "note": "Dự thảo: **7 hoặc 11**"},
             {"t": "2", "a": "Phó ban", "tone": "n", "z": "Một người đại diện chủ đầu tư", "note": "Dự thảo: **1 hoặc 2**"},
             {"t": "CTCP", "a": "mô hình", "tone": "n", "z": "Hội đồng quản trị công ty cổ phần", "note": "Bỏ phương án **hợp tác xã**"},
             {"t": "6/5/4", "a": "triệu", "tone": "n", "z": "Thù lao Trưởng ban, Phó ban, thành viên", "note": "Dự thảo có thêm mức **7/6/5**"}]),
 dict(id="qc3", type="stats", **SQC, tag="Điều giữ nguyên", title="Các điều kiểm soát tiền quỹ không đổi một chữ",
      tiles=[["3.1.a", "tài khoản quỹ, ít nhất 3 người đứng tên", "g", "Không được **đổi tài khoản**."],
             ["7.2 tới 7.4", "chuyển thẳng cho nhà thầu, tạm dùng tối đa 10 triệu", "g", "Dùng ở **vấn đề 1**."],
             ["9.2", "trên 50 triệu cần hơn một nửa chủ sở hữu", "g", "Dùng ở **vấn đề 3**."]])],
 vs=[("qc1#-2", "Quy chế nào đang áp dụng?", True),
     ("qc1#0", "Có hai bộ quy chế đang lưu hành. Bản dự thảo 50 trang gửi kèm công văn ngày 16/11/2023, còn để ngỏ nhiều phương án."),
     ("qc1#1", "Và bản Hội nghị thông qua ngày 26/05/2024, 42 trang, đã chốt từng phương án. Mọi đối chiếu trong clip này dùng bản thông qua."),
     ("qc2#-1", "So với dự thảo, thay đổi nằm ở cách tổ chức Ban quản trị."),
     ("qc2#0", "Ban quản trị có tối thiểu 9 thành viên, mỗi block ít nhất một người; dự thảo chỉ có hai phương án 7 hoặc 11 người."),
     ("qc2#1", "Có hai Phó ban, trong đó một người đại diện chủ đầu tư."),
     ("qc2#2", "Ban quản trị hoạt động theo mô hình Hội đồng quản trị của công ty cổ phần."),
     ("qc2#3", "Thù lao chốt ở mức 6, 5 và 4 triệu đồng mỗi tháng cho Trưởng ban, Phó ban và thành viên."),
     ("qc3#-1", "Các điều kiểm soát tiền quỹ thì giữ nguyên, không đổi một chữ."),
     ("qc3#0", "Điều 3.1.a: tài khoản quỹ có ít nhất ba thành viên cùng đứng tên và không được thay đổi."),
     ("qc3#1", "Điều 7.2 tới 7.4: tiền quỹ chuyển thẳng cho nhà thầu, tạm dùng tiền vận hành tối đa 10 triệu mỗi tháng."),
     ("qc3#2", "Điều 9.2: khoản trên 50 triệu cần hơn một nửa chủ sở hữu đồng ý."),
     ("qc3#-1", "Quy chế có một chỗ tự mâu thuẫn: Điều 3.1.a công khai chi tiêu 6 tháng một lần, Điều 6.1.g yêu cầu hằng tháng. Cư dân có thể đề nghị áp dụng mức hằng tháng.")])

_V1 = {v["id"]: v for v in O.V_ONE}
_VS9 = [x for x in O.VS_ONE if x[0].split("#")[0] in ("tong", "sev", "cause", "nnt", "k3", "lad")]
SEG[9] = dict(name="Tóm lại, mức độ, nguyên nhân, khung xử lý", short="Tóm lại, mức độ và khung xử lý",
              vis=[_V1[k] for k in ("tong", "sev", "cause", "nnt", "k3", "lad")], vs=_VS9)

Q10 = O.Q10
SEG[10] = dict(name="Mười câu hỏi đã gửi Ban quản trị", short="Mười câu hỏi đã gửi Ban quản trị", vis=[
 dict(_V1["q10"], tag="Đã gửi Ban quản trị ngày 29/09/2026", title="Mười câu hỏi và chứng từ cần có")],
 vs=[("q10#-2", "Mười câu hỏi đã gửi Ban quản trị ngày 29/09/2026, hạn trả lời ngày 04/10/2026.", True),
     ("q10#0", "Câu một: vì sao 986,9 triệu tiền quỹ chuyển vào tài khoản vận hành, căn cứ là biên bản hay văn bản nào."),
     ("q10#0", "Kèm theo là biên bản họp, sao kê tài khoản nhận từ 01/08/2025, và hợp đồng, hóa đơn, nghiệm thu của sáu khoản."),
     ("q10#1", "Câu hai: bảng chi phí ngày 15/05/2026 chỉ giải thích 863,8 triệu, phần lệch 123,1 triệu là gì."),
     ("q10#1", "Kèm theo là bảng đối chiếu từng khoản với chứng từ gốc."),
     ("q10#2", "Câu ba: căn cứ nào để thu 1,71 tỷ tiền khu vực chung vào tài khoản ngoài quỹ."),
     ("q10#2", "Kèm theo là hợp đồng với Chicilon Media, Viễn thông ACT, Hưng Thái, và quyết định mở tài khoản."),
     ("q10#3", "Câu bốn: hồ sơ của 1,40 tỷ đã chi, trong đó 856,8 triệu cho Thành Công."),
     ("q10#3", "Kèm theo là dự toán, ba báo giá, biên bản nghiệm thu và ảnh hiện trạng trước, sau của từng hợp đồng."),
     ("q10#4", "Câu năm: vì sao hợp đồng giữ xe với Khởi Sáng Việt được trả vượt 67,1 triệu."),
     ("q10#4", "Kèm theo là hợp đồng gốc, phụ lục phát sinh và biên bản quyết toán."),
     ("q10#5", "Câu sáu: danh mục thiết bị và hóa đơn của 705,8 triệu trả Thép Quang."),
     ("q10#5", "Kèm theo là biên bản giao nhận, mã số thuế của nhà cung cấp, và kiểm đếm thiết bị thực tế."),
     ("q10#6", "Câu bảy: vì sao phí bảo trì thang máy Schindler vắng trên tài khoản quỹ từ ngày 21/01/2025."),
     ("q10#6", "Kèm theo là giấy xác nhận công nợ của Schindler và nhật ký bảo trì từng thang."),
     ("q10#7", "Câu tám: xác nhận của ngân hàng cho 127,5 tỷ tiền gửi sau tái tục."),
     ("q10#7", "Kèm theo là hợp đồng tiền gửi và giấy xác nhận số dư tại quầy, ghi rõ không cầm cố, không phong tỏa."),
     ("q10#8", "Câu chín: vì sao tiền quảng cáo của Chicilon Media giảm 17,5% sau khi ký lại hợp đồng."),
     ("q10#8", "Kèm theo là hai hợp đồng, phụ lục, và lý do điều chỉnh giá."),
     ("q10#9", "Câu mười: sao kê của ba tài khoản từ ngày 01/06/2026 tới nay."),
     ("q10#9", "Vì sổ phụ in ngày 04/09/2026 nhưng chỉ tới 31/05/2026, nên chưa thấy dòng tiền đáo hạn và tái tục."),
     ("q10#-1", "Mỗi câu đều kèm danh sách chứng từ cụ thể. Ban quản trị trả lời đủ thì từng dấu hiệu được khép lại.")])

_VS11 = [x for x in O.VS_ONE if x[0].split("#")[0] in ("pa", "cuda")]
_VS11 = [(x[0], "Theo dõi câu trả lời của Ban quản trị cho mười câu hỏi, và góp thêm chứng từ nếu có.") if x[0] == "cuda#2" else x for x in _VS11]
_VS11 = [x for x in _VS11 if x[0] != "pa#-2"]
_VS11 = [("pa#-2", "Hội nghị quyết định theo điều kiện, xét riêng từng thành viên.", True),
         ("pa#-1", "Mỗi thành viên được xét riêng, vì vai trò ký duyệt và mức độ tham gia của từng người khác nhau.")] + _VS11 + [
         ("cuda#-1", "Chủ sở hữu không dự được có thể ủy quyền cho người khác tham dự Hội nghị.")]
SEG[11] = dict(name="Hội nghị quyết định gì, cư dân làm gì", short="Hội nghị quyết định gì, cư dân làm gì",
               vis=[_V1["pa"], _V1["cuda"]], vs=_VS11)

PARTS = {1: dict(segs=[1, 2], name="Tiền có mất không và toàn cảnh dòng tiền"),
         2: dict(segs=[3, 4], name="Hai điểm nghi vấn trên sao kê: vấn đề 1 và 2"),
         3: dict(segs=[5, 6], name="Hai khoản chờ chứng từ: vấn đề 3 và 4"),
         4: dict(segs=[7, 8], name="Tiền gửi sau tái tục và Quy chế áp dụng"),
         5: dict(segs=[9], name="Tóm lại, mức độ, nguyên nhân, khung xử lý"),
         6: dict(segs=[10, 11], name="Mười câu hỏi, Hội nghị và việc cư dân cần làm")}

# cau mo, cau ket rieng cho tung clip nho
HOOK = {1: "Tiền quỹ bảo trì có mất không, và Ban quản trị đã làm đúng những gì.",
        2: "Tiền quỹ đi qua bốn tài khoản; lưu đồ cho thấy đường nào đúng, đường nào sai.",
        3: "Ngày 23/12/2025, 986,9 triệu tiền quỹ chuyển vào một tài khoản do chính các thành viên Ban quản trị đồng đứng tên.",
        4: "1,71 tỷ tiền quảng cáo và thuê mặt bằng khu vực chung chưa từng vào quỹ.",
        5: "13 khoản chi trên 50 triệu, tổng 5,04 tỷ, chưa thấy văn bản cho phép của chủ sở hữu.",
        6: "705,8 triệu trả trọn cho Thép Quang, nhưng hàng hóa chỉ ghi chung chung.",
        7: "127,5 tỷ tiền gửi sau tái tục chưa có xác nhận của ngân hàng.",
        8: "Có hai bộ quy chế đang lưu hành; clip này nói bản nào áp dụng và điều gì đã thay đổi.",
        9: "Năm vấn đề nặng nhẹ ra sao, do đâu mà có, và xử lý theo khung nào.",
        10: "Mười câu hỏi đã gửi Ban quản trị, mỗi câu kèm chứng từ cần có.",
        11: "Hội nghị có ba phương án, xét riêng từng thành viên; cư dân có ba việc nên làm."}
PHOOK = {1: "Phần này trả lời câu hỏi đầu tiên: tiền quỹ có mất không, và tiền đã đi qua những tài khoản nào.",
         2: "Phần này nói hai điểm nghi vấn thể hiện trên sao kê: 986,9 triệu vào tài khoản Ban quản trị, và 1,71 tỷ tiền khu vực chung nằm ngoài quỹ.",
         3: "Phần này nói hai vấn đề đang chờ chứng từ: 13 khoản chi trên 50 triệu, và 705,8 triệu trả Thép Quang.",
         4: "Phần này nói 127,5 tỷ tiền gửi sau tái tục, và bộ quy chế đang áp dụng.",
         5: "Phần này tóm lại năm vấn đề, đo mức độ, tìm nguyên nhân và đặt khung xử lý.",
         6: "Phần cuối gồm mười câu hỏi đã gửi Ban quản trị, ba phương án cho Hội nghị và việc cư dân cần làm."}
END = "Toàn bộ số liệu truy được về sao kê gốc trong thư mục chia sẻ. Các nhận định là dấu hiệu cần làm rõ, không phải cáo buộc."


def make_C(segs, hook, outro, title, stats, date):
    vis, vs = [], []
    for k in segs: vis += SEG[k]["vis"]; vs += SEG[k]["vs"]
    vs = [("bia", h) for h in hook] + vs + [("lienhe", outro)]
    import ngon_tu_clip as _NC  # 15/10/2026: dat nghi van, de nghi lam ro
    vs = _NC.walk(vs); vis = _NC.walk(vis); title = _NC.soften(title); stats = _NC.walk(stats)
    for s_ in vs: assert "→" not in s_[1] and "->" not in s_[1] and "(" not in s_[1], s_[1][:60]
    C = dict(VS.C)
    C.update(hero_title=title, video_cover_stats=stats, video_script=vs, video_visuals=vis)
    C["meta"] = dict(VS.C["meta"], date=date)
    C.pop("video_script_short", None)
    return C


def C_full():
    return make_C(list(range(1, 12)), [x[1] for x in O.VS_ONE if x[0] == "bia"],
                  END + " Xin cảm ơn quý cư dân.", O.C_ONE["hero_title"], O.C_ONE["video_cover_stats"], "Bản đầy đủ · 04/10/2026")


def C_part(n):
    p = PARTS[n]
    nxt = f"Phần {n + 1} trên 6: {PARTS[n + 1]['name']}. " if n < 6 else ""
    return make_C(p["segs"], [f"Quỹ bảo trì, phần {n} trên 6: {p['name']}.", PHOOK[n]], nxt + END,
                  f"Phần {n}/6 · **{p['name']}**", PART_STATS[n], f"Phần {n}/6 · 04/10/2026")


def C_doc(k):
    s = SEG[k]
    nxt = f"Clip tiếp theo, số {k + 1} trên 11: {SEG[k + 1]['short']}. " if k < 11 else "Đây là clip cuối của bộ 11 clip. "
    return make_C([k], [f"Quỹ bảo trì, clip {k} trên 11: {s['short']}.", HOOK[k]], nxt + END,
                  f"Clip {k}/11 · **{s['short']}**", DOC_STATS[k], f"Clip {k}/11 · 04/10/2026")


PART_STATS = {1: [["127,15 tỷ", "tiền gốc còn trong quỹ", "g"], ["198", "giao dịch khớp tới từng đồng", "g"], ["4", "tài khoản cần nhớ", "n"]],
              2: [["986,9 triệu", "vào tài khoản Ban quản trị", "r"], ["1,71 tỷ", "khu vực chung ngoài quỹ", "r"], ["1,40 tỷ", "chi ngoài quy trình", "r"]],
              3: [["13", "khoản trên 50 triệu", "o"], ["5,04 tỷ", "chưa thấy văn bản cho phép", "o"], ["705,8 triệu", "trả trọn Thép Quang", "o"]],
              4: [["127,5 tỷ", "tiền gửi sau tái tục", "y"], ["98%", "quỹ là tiền gửi kỳ hạn", "n"], ["26/05/2024", "ngày thông qua Quy chế", "g"]],
              5: [["3", "vi phạm đã rõ", "r"], ["16", "dấu hiệu được phân loại", "o"], ["0", "khoản có căn cứ hình sự", "g"]],
              6: [["10", "câu hỏi đã gửi", "o"], ["3", "phương án cho Hội nghị", "n"], ["3", "việc cư dân nên làm", "g"]]}
DOC_STATS = {1: [["127,15 tỷ", "tiền gốc còn", "g"], ["0", "lệnh rút tiền mặt", "g"]],
             2: [["4", "tài khoản", "n"], ["3,12 tỷ", "đã rời quỹ", "o"]],
             3: [["986,9 triệu", "vào TK Ban quản trị", "r"], ["3", "điều đã rõ", "r"]],
             4: [["1,71 tỷ", "ngoài quỹ", "r"], ["1,40 tỷ", "đã chi", "r"]],
             5: [["13", "khoản trên 50 triệu", "o"], ["5,04 tỷ", "chưa thấy văn bản", "o"]],
             6: [["705,8 triệu", "trả trọn", "o"], ["6", "chứng từ cần có", "o"]],
             7: [["127,5 tỷ", "sau tái tục", "y"], ["98%", "quỹ là tiền gửi", "n"]],
             8: [["42 trang", "bản thông qua", "g"], ["26/05/2024", "ngày thông qua", "g"]],
             9: [["3", "vi phạm đã rõ", "r"], ["16", "dấu hiệu", "o"]],
             10: [["10", "câu hỏi", "o"], ["29/09/2026", "ngày gửi", "n"]],
             11: [["3", "phương án", "n"], ["3", "việc cư dân làm", "g"]]}

CHAP_NAMES = {"f0": "Toàn cảnh dòng tiền của quỹ", "f1": "Vấn đề 1: 986,9 triệu qua tài khoản Ban quản trị", "f2": "Vấn đề 2: tiền khu vực chung ngoài quỹ",
              "f3": "Vấn đề 3: 13 khoản trên 50 triệu", "f4": "Vấn đề 4: Thép Quang 705,8 triệu", "f5": "Vấn đề 5: 127,5 tỷ tiền gửi"}


def _dur(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)


def overlay(main, info, out, tmp, fmt, title):
    """Phu hinh dong tien len tung canh luu do co trong clip (theo dong thoi gian that cua clip nay), ghi moc chuong."""
    os.makedirs(tmp, exist_ok=True)
    tl = info["timeline"]; cards = info["card_times"]; segs = {s[0]: (s[1], s[2]) for s in info["seg_times"]}
    parts = []
    for sid, (k, steps) in O.FLOW_STEPS.items():
        sents = [x for x in tl if x[0].split("#")[0] == sid]
        if not sents: continue
        c_end = next(b for a, b in cards if abs(b - sents[0][3]) < 1e-3)
        t0, t1 = c_end + 0.05, segs[sid][1]
        st = [("all", 0, 0.0)] + [(kind, n, max(0.0, x[2] - 0.15 - t0)) for (kind, n), x in zip(steps, sents[1:])]
        f = f"{tmp}/{sid}_{fmt}_{t1 - t0:.2f}.mp4"
        if not os.path.exists(f): FC.render_scene(k, t1 - t0, st, f, fmt=fmt)
        parts.append((t0, t1, f)); print("[luu do]", sid, round(t0, 2), round(t1, 2), flush=True)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", main]
    for t0, t1, f in parts: cmd += ["-itsoffset", str(round(t0, 3)), "-i", f]
    fc, last = [], "0:v"
    for i, (t0, t1, f) in enumerate(parts, 1):
        fc.append(f"[{last}][{i}:v]overlay=0:{0 if fmt == 'w' else BV.T_SLY}:eof_action=pass:enable='between(t,{t0:.3f},{t1:.3f})'[v{i}]"); last = f"v{i}"
    vmap = ["-filter_complex", ";".join(fc), "-map", f"[{last}]"] if parts else ["-map", "0:v"]
    cmd += vmap + ["-map", "0:a", "-c:v", "libx264", "-preset", "medium", "-crf", "24", "-pix_fmt", "yuv420p",
                   "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out + ".tmp.mp4"]
    subprocess.run(cmd, check=True)
    total = _dur(out + ".tmp.mp4")
    rev = {"Toàn cảnh dòng tiền": "f0", "Vấn đề 1": "f1", "Vấn đề 2": "f2", "Vấn đề 3": "f3", "Vấn đề 4": "f4", "Vấn đề 5": "f5"}
    chaps = []
    for c in info["chapters"]:
        m, s2 = c.split(" ")[0].split(":"); nm = c.split(" ", 1)[1]
        chaps.append((int(m) * 60 + int(s2), CHAP_NAMES.get(rev.get(nm, ""), nm)))
    meta = f";FFMETADATA1\ntitle={title}\n" + "".join(
        f"[CHAPTER]\nTIMEBASE=1/1000\nSTART={int(a * 1000)}\nEND={int((chaps[i + 1][0] if i + 1 < len(chaps) else total) * 1000)}\ntitle={n}\n" for i, (a, n) in enumerate(chaps))
    open(out + ".meta", "w", encoding="utf-8").write(meta)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", out + ".tmp.mp4", "-i", out + ".meta", "-map_metadata", "1", "-map_chapters", "1", "-c", "copy", out], check=True)
    os.remove(out + ".tmp.mp4"); os.remove(out + ".meta")
    fm = lambda x: f"{int(round(x)) // 60:02d}:{int(round(x)) % 60:02d}"
    res = dict(file=os.path.basename(out), duration=round(total, 1), size_mb=round(os.path.getsize(out) / 1e6, 1), chapters=[f"{fm(a)} {n}" for a, n in chaps])
    json.dump(res, open(out[:-4] + "_info.json", "w"), ensure_ascii=False, indent=1)
    return res


def build(C, name, fmt, title):
    """fmt 'w' ngang 1920x1080, 't' doc 1080x1920. Dung mot lan lien mach roi phu luu do."""
    pre = f"{OUT}/_{name}"
    mp4, info = BV.build_video(C, pre, speed=1.18, formats=(("16x9",) if fmt == "w" else ("9x16",)))
    src = pre + ("_Video.mp4" if fmt == "w" else "_Video_Doc.mp4")
    json.dump({k: v for k, v in info.items() if k != "script"}, open(pre + "_info.json", "w"), ensure_ascii=False, indent=1)
    res = overlay(src, info, f"{OUT}/{name}.mp4", f"{OUT}/tmp", fmt, title)
    res["voice"] = info.get("voice"); print(json.dumps(res, ensure_ascii=False), flush=True)
    os.remove(src)
    return res


ALL_TEXTS = lambda: sorted({x[1] for C in [C_full()] + [C_part(n) for n in PARTS] + [C_doc(k) for k in SEG] for x in C["video_script"]})

if __name__ == "__main__":
    a = sys.argv[1:]
    t0 = time.time()
    if a[0] == "list":
        for nm, C in [("full", C_full())] + [(f"p{n}", C_part(n)) for n in PARTS] + [(f"d{k}", C_doc(k)) for k in SEG]:
            sc = C["video_script"]; syl = sum(len(BV.speakable(x[1]).split()) for x in sc)
            nsc = len({x[0].split("#")[0] for x in sc}); print(nm, len(sc), round((syl / 3.9 + len(sc) * 0.24 + nsc * 1.05 + 4.7) / 60, 1))
        print("cau khac nhau:", len(ALL_TEXTS()))
    elif a[0] == "prepare":
        import audit_voice as AV
        AV.prepare(ALL_TEXTS())
    elif a[0] == "full":
        build(C_full(), "SSR_Quy_bao_tri_ban_day_du_25p", "w", "Quỹ bảo trì SSR: bản đầy đủ")
    elif a[0] == "part":
        for n in map(int, a[1:]):
            build(C_part(n), f"SSR_Quy_bao_tri_phan_{n}_tren_6", "w", f"Quỹ bảo trì SSR, phần {n}/6: {PARTS[n]['name']}")
    elif a[0] == "doc":
        for k in map(int, a[1:]):
            build(C_doc(k), f"SSR_Quy_bao_tri_clip_doc_{k:02d}_tren_11", "t", f"Quỹ bảo trì SSR, clip {k}/11: {SEG[k]['short']}")
    print("xong", round(time.time() - t0))
