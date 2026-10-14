# -*- coding: utf-8 -*-
"""KHUNG KET LUAN NAM CAU: co sai pham khong, sai pham toi dau, muc do, quy mo, khung xu ly.
Mot nguon chu duy nhat cho bao cao day du (muc 1), ban tom tat (muc 1), dashboard (trang dau va Phan I),
file Excel (sheet Nam cau hoi), file Phan loai nguyen nhan, file Hoi dan va clip Phan loai nguyen nhan.
So lieu tinh tu findings.json, dash_data.json; phan loai nguyen nhan lay tu build_phanloai.py; he qua tu legal.py.
Khong neu ten ca nhan. Khong dung ky hieu mui ten."""
import json, os
os.chdir("/home/claude/ssr")
import legal as LG
import build_phanloai as PL
import nguong as NG

_F = {f["id"]: f for f in json.load(open("findings.json"))}
_D = json.load(open("dash_data.json"))


def _vn(x, d=2):
    return f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def ty(v, d=2): return _vn(v / 1e9, d) + " tỷ"
def tr(v, d=1): return _vn(v / 1e6, d) + " triệu"
def pc(v, d=1): return _vn(v * 100, d) + "%"


# ---------------------------------------------------------------- so lieu (tinh, khong go tay)
AMT = {k: v["amount"] for k, v in _F.items()}
FUND = _D["fund_end"]                                    # so du quy 31/05/2026
DA_RO = AMT["F01"] + AMT["F02"]                          # 986,9 trieu roi quy + 1,71 ty le ra vao quy
CHI_NGOAI = _D["repair7784"]                             # 1,40 ty chi tu TK 7784 ngoai quy trinh
CHO_CT = AMT["F01"] + AMT["F03"]                         # 1,69 ty chua truy duoc toi cung
K3_CHI = AMT["F01"] + AMT["F03"] + AMT["F07"]            # 2,55 ty ba khoan chi chua loai tru (3)
QC_NAM = AMT["F09"]                                      # 182,2 trieu moi nam
OPP = (_D["opp_lo"], _D["opp_hi"])                       # 0,42 - 0,96 ty lai bo lo
assert ty(DA_RO) == "2,69 tỷ" and ty(CHO_CT) == "1,69 tỷ" and ty(K3_CHI) == "2,55 tỷ" and ty(CHI_NGOAI) == "1,40 tỷ"
assert pc(DA_RO / FUND) == "2,1%" and tr(QC_NAM) == "182,2 triệu" and ty(FUND) == "127,15 tỷ"
assert ty(OPP[0]) == "0,42 tỷ" and ty(OPP[1]) == "0,96 tỷ"

# phan loai nguyen nhan cua 16 dau hieu (cung nguon file Phan loai, dashboard)
NNL = {"k1": "(1) Thiếu năng lực", "k2": "(2) Lỡ tay thật", "k3": "Chưa loại trừ (3)", "k0": "Chưa phát sinh sai"}
NNG = (("k1", PL.G1), ("k2", PL.G2), ("k3", PL.G3), ("k0", PL.G0))
NN = {c: dict(k=k, lab=NNL[k], why=w, change=ch, conf=cf) for k, g in NNG for c, _t, w, ch, cf in g}
assert sorted(NN) == sorted(_F) == sorted(LG.LG_F)
NNC = {k: [c for c in sorted(NN) if NN[c]["k"] == k] for k in NNL}
ST = {k: [c for c in sorted(LG.LG_F) if LG.LG_F[c][0] == k] for k in ("ro", "cho", "hq", "td")}
SEVN = {s: sum(1 for f in _F.values() if f["sev"] == s) for s in ("Đỏ", "Cam", "Vàng")}
assert [len(NNC[k]) for k in ("k1", "k2", "k3", "k0")] == [9, 2, 4, 1]
assert [len(ST[k]) for k in ("ro", "cho", "hq", "td")] == [2, 12, 1, 1] and [SEVN[s] for s in ("Đỏ", "Cam", "Vàng")] == [3, 7, 6]
ST_ORDER = ["ro", "cho", "hq", "td"]
NN_ORDER = ["k1", "k2", "k3", "k0"]

# ---------------------------------------------------------------- nam cau hoi
TITLE = "Năm câu hỏi của cuộc kiểm tra"
SUB = "Có sai phạm không, sai phạm tới đâu, mức độ, quy mô và khung xử lý"
INTRO = ("Mục tiêu của việc soi sao kê là trả lời năm câu hỏi dưới đây. Câu trả lời dựa trên dữ liệu tới 31/05/2026 và tài liệu Ban quản trị gửi ngày 28/09/2026; "
         "phần còn phụ thuộc chứng từ được ghi rõ. Các nhận định là dấu hiệu cần làm rõ, không phải cáo buộc.")

Q = [
    dict(n=1, id="co-sai-pham", q="Có sai phạm không?", tone="r", v="3", vl="vi phạm đã rõ trên sao kê",
         a="Có. Ba vi phạm đã rõ ngay trên sao kê, không cần thêm hồ sơ để khẳng định.",
         s="Có: 3 vi phạm đã rõ trên sao kê; 12 dấu hiệu chờ chứng minh.",
         lines=["986,9 triệu tiền quỹ đi qua tài khoản vận hành của Ban quản trị, trái Điều 3.2.a, 7.2 và 7.4 Quy chế thu chi (F01).",
                "1,71 tỷ tiền khai thác khu vực chung không nộp vào tài khoản quỹ, trái khoản 4 Điều 153 Luật Nhà ở 2023 (F02).",
                "1,40 tỷ trong số đó đã chi cho Thành Công, Khởi Sáng Việt, KTECH, không qua kế hoạch, chọn thầu và nghiệm thu của quỹ (F02, F07).",
                "Ngoài ba vi phạm này, 12 dấu hiệu chờ Ban quản trị chứng minh bằng chứng từ, trong đó có năm nghi vấn lớn ở ba tầng kết luận; 1 dấu hiệu hiệu quả thấp và 1 dấu hiệu đang theo dõi."]),
    dict(n=2, id="toi-dau", q="Sai phạm tới đâu?", tone="o", v="1,69 tỷ", vl="phần còn chờ chứng từ",
         a="Tới mức làm trái Quy chế và Luật Nhà ở, tiền đi ngoài quy trình kiểm soát; chưa có bằng chứng chiếm đoạt.",
         s="Làm trái Quy chế và Luật Nhà ở; chưa có bằng chứng chiếm đoạt.",
         lines=["198 giao dịch khớp số dư tới từng đồng; không rút tiền mặt, không chuyển cho cá nhân; tiền gốc quỹ không giảm.",
                "Phần chưa kết luận được là 1,69 tỷ chưa truy được tới cùng: 986,9 triệu chưa có sao kê tài khoản nhận và biên bản nghiệm thu, 705,8 triệu trả Thép Quang chưa có danh mục hàng hóa.",
                "Có chứng từ hợp lệ thì dừng ở mức sai quy trình; không có chứng từ thì phải bồi hoàn và thành vi phạm đã rõ."]),
    dict(n=3, id="muc-do", q="Mức độ vi phạm?", tone="y", v="9/16", vl="dấu hiệu do thiếu năng lực",
         a="Thuộc diện xử phạt hành chính về quản lý, sử dụng kinh phí bảo trì; phần lớn do thiếu năng lực, chưa dấu hiệu nào đủ căn cứ là có chủ đích.",
         s="Diện xử phạt hành chính; 9/16 do thiếu năng lực, chưa dấu hiệu nào đủ căn cứ là có chủ đích.",
         lines=["Theo mức nghiêm trọng: 3 dấu hiệu mức Đỏ cần giải trình ngay, 7 mức Cam cần hồ sơ chứng minh, 6 mức Vàng cần cải thiện.",
                "Theo nguyên nhân, đánh giá sơ bộ: 9 dấu hiệu do thiếu năng lực, 2 dấu hiệu là lỡ tay thật, 1 dấu hiệu chưa phát sinh sai.",
                "4 dấu hiệu chưa loại trừ được khả năng lỡ tay có chủ đích: 986,9 triệu qua TK vận hành 118002976372, 705,8 triệu trả Thép Quang, 4 hợp đồng liên tiếp của Thành Công và hợp đồng quảng cáo ký lại với Chicilon Media.",
                "Nguyên nhân không làm nhẹ vi phạm đã rõ; nó quyết định cách xử lý trách nhiệm cá nhân."]),
    dict(n=4, id="quy-mo", q="Quy mô vi phạm?", tone="r", v="2,69 tỷ", vl="đã đi sai tài khoản, khoảng 2,1% quỹ",
         a="2,69 tỷ đã đi sai tài khoản, bằng khoảng 2,1% số dư quỹ; 1,69 tỷ còn phải có chứng từ mới khẳng định được là không mất.",
         s="2,69 tỷ đi sai tài khoản (khoảng 2,1% quỹ); 1,69 tỷ chờ chứng từ.",
         lines=["Đã rõ: 986,9 triệu rời quỹ và 1,71 tỷ lẽ ra phải vào quỹ, cộng 2,69 tỷ.",
                "Chờ chứng từ: 1,69 tỷ gồm 986,9 triệu và 705,8 triệu, có thể thành thất thoát thật.",
                "Chưa loại trừ có chủ đích: ba khoản chi cộng khoảng 2,55 tỷ; hợp đồng quảng cáo ký lại thu giảm khoảng 182,2 triệu mỗi năm.",
                f"Vượt thẩm quyền nếu không có văn bản: {NG.N_OVER} khoản chi trên 50 triệu, tổng {NG.ty(NG.V_OVER)}, chưa thấy kế hoạch được thông qua hoặc ý kiến chủ sở hữu (Điều 9.2); chi sửa chữa năm 2025 gấp {NG.lan(NG.Y25 / NG.TRAN)} lần trần 500 triệu.",
                "Thiệt hại cơ hội: 0,42 – 0,96 tỷ tiền lãi bỏ lỡ, tiền gốc không mất.",
                "Các nhóm chồng lấn một phần (khoản 986,9 triệu có ở bốn nhóm), nên không cộng dồn."]),
    dict(n=5, id="khung-xu-ly", q="Khung xử lý?", tone="n", v="50 – 60", vl="triệu đồng, mức phạt Ban quản trị",
         a="Vi phạm đã rõ phải khắc phục, thuộc diện phạt Ban quản trị 50 – 60 triệu đồng và là căn cứ bãi nhiệm; khoản nào không chứng minh được thì bồi hoàn quỹ.",
         s="Khắc phục, phạt 50 – 60 triệu, căn cứ bãi nhiệm; không chứng minh được thì bồi hoàn.",
         lines=["Đã rõ: khắc phục bắt buộc; phạt 50 – 60 triệu đồng (khoản 3 Điều 61 Nghị định 339/2026/NĐ-CP); căn cứ bãi nhiệm thành viên chịu trách nhiệm (điểm c khoản 2 Điều 8 Quy chế hoạt động Ban quản trị; khoản 2 Điều 26 Quy chế kèm Thông tư 05/2024/TT-BXD).",
                "Chờ chứng minh: có chứng từ hợp lệ thì coi như đã giải trình xong; không chứng minh được sau khi đã được yêu cầu bằng văn bản thì bồi hoàn quỹ (Điều 10.1 Quy chế thu chi) và thành vi phạm đã rõ.",
                "Theo nguyên nhân: thiếu năng lực thì sửa quy trình, thuê kế toán hoặc kiểm toán; lỡ tay thật thì điều chỉnh sổ sách; có chủ đích thì bồi hoàn, bồi thường, kiểm toán đột xuất và xem xét bãi nhiệm.",
                "Hình sự chỉ đặt ra khi có chứng cứ chiếm đoạt, do cơ quan điều tra xác định; đến nay chưa có dữ kiện như vậy."]),
]
ND = ["Có sai phạm: ba vi phạm đã rõ trên sao kê, thuộc diện xử phạt hành chính, chưa có dữ kiện hình sự.",
      "Sai phạm dừng ở việc tiền đi ngoài quy trình kiểm soát; là sai quy trình hay thất thoát thì phải chờ chứng từ của 1,69 tỷ.",
      "Quy mô đã rõ là 2,69 tỷ, khoảng 2,1% số dư quỹ; phần lớn sai sót do thiếu năng lực, chưa dấu hiệu nào đủ căn cứ là có chủ đích.",
      "Vì vậy hướng xử lý chính là khắc phục và sửa quy trình, kèm mức phạt theo quy định; bồi hoàn và bãi nhiệm đặt ra khi không chứng minh được hoặc không khắc phục."]
ND_LABEL = "NHẬN ĐỊNH · NĂM CÂU HỎI"

# ---------------------------------------------------------------- quy mo
QM_H = ["Nhóm", "Số tiền", "So với quỹ", "Gồm", "Tình trạng"]
QM = [  # (nhom, so tien hoac (thap, cao), gom, tinh trang, tone)
    ("Đã đi sai tài khoản", DA_RO, "986,9 triệu rời quỹ sang tài khoản vận hành (F01); 1,71 tỷ tiền khu vực chung không vào quỹ (F02)", "Đã rõ", "r"),
    ("Trong đó chi ngoài quy trình", CHI_NGOAI, "Chi từ tài khoản thu dịch vụ, không qua chọn thầu, nghiệm thu của quỹ (F02, F07)", "Đã rõ", "r"),
    ("Chưa truy được tới cùng", CHO_CT, "986,9 triệu chưa có sao kê tài khoản nhận (F01); 705,8 triệu trả Thép Quang chưa có danh mục hàng hóa (F03)", "Chờ chứng từ", "o"),
    ("Chưa loại trừ có chủ đích", K3_CHI, "Hoàn ứng 986,9 triệu (F01), Thép Quang (F03), Thành Công (F07); thêm hợp đồng Chicilon Media thu giảm 182,2 triệu mỗi năm (F09)", "Chờ chứng từ", "o"),
    ("Chi vượt mức tự quyết, chưa thấy văn bản cho phép", NG.V_OVER, f"{NG.N_OVER} khoản trên 50 triệu: HNB, hoàn ứng 986,9 triệu, Thép Quang, Schindler, Thành Công, Khởi Sáng Việt, KTECH (Điều 9.2)", "Chờ văn bản", "o"),
    ("Thiệt hại cơ hội", OPP, "Tiền lãi bỏ lỡ do kỳ hạn ngắn và tiền nhàn rỗi (F10); tiền gốc không mất", "Hiệu quả thấp", "y"),
    ("Số dư quỹ ngày 31/05/2026", FUND, "Tiền gốc không giảm, cao hơn lúc nhận bàn giao nhờ tiền lãi", "Đã kiểm chứng", "g"),
]
QM_NOTE = "Các nhóm chồng lấn một phần: khoản 986,9 triệu có ở bốn nhóm, 1,40 tỷ nằm trong 1,71 tỷ; vì vậy không cộng dồn các dòng."


def qm_amt(v):
    return (ty(v[0]) + " – " + ty(v[1])).replace(" tỷ – ", " – ") if isinstance(v, tuple) else ty(v)


def qm_pct(v):
    if isinstance(v, tuple):
        return pc(v[0] / FUND) + " – " + pc(v[1] / FUND)
    return "100%" if v == FUND else pc(v / FUND)


# ---------------------------------------------------------------- khung xu ly
KX_H = ["Tình trạng", "Dấu hiệu", "Khắc phục", "Phạt Ban quản trị", "Bồi hoàn quỹ", "Bãi nhiệm", "Hình sự"]
KX = [
    ("Đã rõ trên sao kê", ", ".join(ST["ro"]), "Bắt buộc", "50 – 60 triệu đồng", "Phần không có chứng từ hợp lệ", "Đã có căn cứ", "Chỉ khi có chứng cứ chiếm đoạt", "r"),
    ("Chờ chứng minh, có chứng từ hợp lệ", f"{len(ST['cho'])} dấu hiệu", "Sửa quy trình nếu sai", "Không", "Không", "Không", "Không", "g"),
    ("Chờ chứng minh, không chứng minh được", f"{len(ST['cho'])} dấu hiệu", "Bắt buộc", "50 – 60 triệu đồng", "Toàn bộ khoản đó", "Có căn cứ", "Chuyển cơ quan điều tra nếu có dấu hiệu chiếm đoạt", "o"),
    ("Hiệu quả thấp", ", ".join(ST["hq"]), "Giải trình trước Hội nghị, đổi cách gửi", "Không", "Không", "Hội nghị đánh giá khi bầu lại", "Không", "y"),
    ("Theo dõi", ", ".join(ST["td"]), "Công khai hợp đồng tái tục", "Không", "Không", "Không", "Không", "n"),
]
KXC_H = ["Nguyên nhân", "Số dấu hiệu", "Xử lý trách nhiệm cá nhân"]
KXC = [("(1) Thiếu năng lực", f"{len(NNC['k1'])}", LG.CAUSE_HQ[1], "k1"),
       ("(2) Lỡ tay thật", f"{len(NNC['k2'])}", LG.CAUSE_HQ[2], "k2"),
       ("(3) Lỡ tay có chủ đích", f"0 đủ căn cứ, {len(NNC['k3'])} chưa loại trừ", LG.CAUSE_HQ[3], "k3")]
KX_NOTE = ("Tình trạng quyết định hệ quả với Ban quản trị như một tổ chức; nguyên nhân quyết định cách xử lý trách nhiệm cá nhân. "
           "Căn cứ: khoản 3 Điều 61 Nghị định 339/2026/NĐ-CP; Điều 10.1 Quy chế thu chi; điểm c khoản 2 Điều 8 Quy chế hoạt động Ban quản trị; khoản 2 Điều 26 Quy chế kèm Thông tư 05/2024/TT-BXD. "
           "Việc xử lý cụ thể do Hội nghị nhà chung cư và cơ quan có thẩm quyền quyết định.")

# ---------------------------------------------------------------- hoi dan ba vong
HD_TITLE = "Đi tới kết luận cuối: hỏi dần ba vòng"
HD3 = [("Vòng 1", "Hỏi để hiểu", "Câu hỏi mở bằng văn bản, không quy lỗi: vì sao, căn cứ nào, ai đề xuất, ai duyệt. Câu trả lời đầu tiên là mốc đối chiếu."),
       ("Vòng 2", "Đòi chứng từ", "Hợp đồng, báo giá, nghiệm thu, hóa đơn, ủy nhiệm chi, sao kê. Không đưa được sau khi yêu cầu bằng văn bản thì khoản đó bồi hoàn quỹ và thành vi phạm đã rõ."),
       ("Vòng 3", "Hỏi đối chiếu", "Đặt từng chỗ lệch cạnh lời giải thích ở vòng 1; đề nghị kiểm toán đột xuất; không khắc phục thì kiến nghị xử phạt và xem xét bãi nhiệm.")]
HD_RULE = ("Chỉ xếp vào lỡ tay có chủ đích khi có ít nhất 2 trong 3 dấu hiệu rõ: cùng kiểu sai lặp lại; có bên hưởng lợi hoặc giá bất thường; "
           "chứng từ né tránh hoặc mâu thuẫn sau khi đã được yêu cầu. Hiện chưa khoản nào đạt; F01 và F07 mới có một dấu hiệu rõ là lặp lại cùng kiểu.")

for _s in [TITLE, SUB, INTRO, QM_NOTE, KX_NOTE, HD_TITLE, HD_RULE] + ND + [y for x in Q for y in [x["q"], x["a"], x["s"], x["vl"]] + x["lines"]] + \
          [y for r in QM for y in (r[0], r[2], r[3])] + [y for r in KX for y in r[:7]] + [y for r in KXC for y in r[:3]] + [y for r in HD3 for y in r]:
    assert "→" not in _s and "->" not in _s and "⇒" not in _s, _s[:60]


# ---------------------------------------------------------------- ban PDF (bao cao day du, ban tom tat, hai tai lieu lam viec)
CSS = """
.k5i { font-family:'Be Vietnam Pro',sans-serif; font-size:8.6pt; color:#3d4656; line-height:1.45; margin:0 0 5pt 0; }
.k5 { margin:4pt 0 6pt 0; }
.k5 .r { display:grid; grid-template-columns:20pt 1fr 30mm; gap:0 8pt; padding:6pt 9pt 6pt 8pt; border:0.8pt solid #cfd8e6; border-left:3pt solid var(--c); border-radius:0 5pt 5pt 0; margin:0 0 5pt 0; background:#fff; break-inside:avoid; }
.k5 .no { font-family:'Be Vietnam Pro',sans-serif; width:17pt; height:17pt; border-radius:50%; background:var(--c); color:#fff; font-size:9pt; font-weight:800; display:flex; align-items:center; justify-content:center; margin-top:1pt; }
.k5 .qq { font-family:'Be Vietnam Pro',sans-serif; font-size:8pt; font-weight:800; letter-spacing:.06em; text-transform:uppercase; color:var(--c); }
.k5 .aa { font-family:'Be Vietnam Pro',sans-serif; font-size:9.6pt; font-weight:700; color:#16294A; line-height:1.38; margin-top:1pt; }
.k5 ul { margin:3pt 0 0 0; padding:0; list-style:none; }
.k5 li { position:relative; padding-left:9pt; font-size:9pt; line-height:1.42; margin:1.4pt 0; text-align:left; }
.k5 li:before { content:''; position:absolute; left:0; top:5pt; width:4pt; height:4pt; border-radius:50%; background:var(--c); }
.k5 .kv { border-left:0.8pt solid #dde3ec; padding-left:7pt; display:flex; flex-direction:column; justify-content:center; }
.k5 .kv .v { font-family:'Be Vietnam Pro',sans-serif; font-size:17pt; font-weight:800; color:var(--c); line-height:1.05; }
.k5 .kv .l { font-family:'Be Vietnam Pro',sans-serif; font-size:7.4pt; color:#3d4656; line-height:1.3; margin-top:2pt; }
.k5.cmp .r { grid-template-columns:18pt 1fr 26mm; padding:4.5pt 8pt; }
.k5.cmp .aa { font-size:9.2pt; }
.k5.cmp .kv .v { font-size:14pt; }
.t-r { --c:#A93434; } .t-o { --c:#C55A11; } .t-y { --c:#8A6100; } .t-n { --c:#1F3864; } .t-g { --c:#1E7A46; }
.k5s { width:100%; border-collapse:collapse; margin:3pt 0 6pt 0; }
.k5s td { font-size:8.6pt; line-height:1.38; padding:3pt 5pt; border:0.6pt solid #cfd6e2; vertical-align:top; background:#fff !important; }
.k5s td.q { font-family:'Be Vietnam Pro',sans-serif; font-weight:800; color:var(--c); white-space:nowrap; width:27mm; }
.k5s td.v { font-family:'Be Vietnam Pro',sans-serif; font-weight:800; color:var(--c); white-space:nowrap; text-align:right; width:19mm; }
.nnm td { font-size:8.6pt; vertical-align:middle; }
.nnm .cc { display:inline-block; font-family:'Be Vietnam Pro',sans-serif; font-size:7.6pt; font-weight:800; border-radius:4pt; padding:0.6pt 4pt; margin:1pt 2pt 1pt 0; border:0.7pt solid; }
.cc.s-Đỏ { color:#A93434; background:#F8E3E3; border-color:#e6b9b9; } .cc.s-Cam { color:#C55A11; background:#FCE9DC; border-color:#efc6a6; } .cc.s-Vàng { color:#7d5d00; background:#FBF3D9; border-color:#ead58f; }
.kk5 { font-family:'Be Vietnam Pro',sans-serif; font-size:7.8pt; font-weight:800; border-radius:9pt; padding:1pt 7pt; white-space:nowrap; display:inline-block; }
.kk5.k1 { background:#FBF3D9; color:#7F6000; border:0.8pt solid #e7cf86; } .kk5.k2 { background:#E6ECF5; color:#1F3864; border:0.8pt solid #b9c7dd; }
.kk5.k3 { background:#F8E3E3; color:#A93434; border:0.8pt solid #e6b9b9; } .kk5.k0 { background:#EDEDED; color:#404040; border:0.8pt solid #cfcfcf; }
.nnt { display:grid; grid-template-columns:repeat(4,1fr); gap:6pt; margin:4pt 0 5pt 0; break-inside:avoid; }
.nnt .t { border:0.8pt solid #cfd8e6; border-top:4pt solid var(--c); border-radius:0 0 5pt 5pt; padding:5pt 8pt 6pt 8pt; background:var(--b); }
.nnt .t .n { font-family:'Be Vietnam Pro',sans-serif; font-size:21pt; font-weight:800; color:var(--c); line-height:1; }
.nnt .t .k { font-family:'Be Vietnam Pro',sans-serif; font-size:8.6pt; font-weight:800; color:#16294A; margin-top:2pt; }
.nnt .t .s { font-family:'Be Vietnam Pro',sans-serif; font-size:7.5pt; color:#3d4656; margin-top:1.5pt; line-height:1.35; }
.qmb { display:block; height:5pt; border-radius:2pt; background:var(--c); margin-top:2pt; }
table.qmt td { font-size:8.8pt; vertical-align:top; }
table.qmt td.amt { font-family:'Be Vietnam Pro',sans-serif; font-weight:800; color:var(--c); white-space:nowrap; }
table.ngt { table-layout:fixed; width:100%; } table.ngt td { font-size:8.2pt; line-height:1.3; vertical-align:top; overflow-wrap:anywhere; word-break:break-word; } table.ngt th { font-size:8pt; white-space:normal !important; line-height:1.2; } table.ngt td.n { white-space:normal !important; } table.ngt td:first-child { white-space:nowrap; overflow-wrap:normal; word-break:normal; } table.ngt tr.tot td { font-size:8.2pt; }
@page land { size: A4 landscape; margin: 14mm 16mm 18mm 16mm; }
.ldland { page: land; }
.ldfig { margin:0 0 4pt 0; break-before: page; } .ldland .ldfig:first-child { break-before: auto; } .ldfig .ldt { font-family:'Be Vietnam Pro',sans-serif; font-size:10pt; font-weight:800; color:#1F3864; margin-bottom:3pt; display:flex; gap:6pt; align-items:baseline; }
.ldfig .ldt b { background:#A93434; color:#fff; border-radius:9pt; padding:0 6pt; font-size:9pt; } .ldfig .ldt span { margin-left:auto; font-size:8pt; color:#6b7384; font-weight:600; white-space:nowrap; }
.ldfig .figbox svg { width:100%; height:auto; display:block; }
table.kxt td { font-size:8.4pt; line-height:1.34; vertical-align:top; }
table.kxt td.st { font-family:'Be Vietnam Pro',sans-serif; font-weight:800; color:var(--c); }
table.kxt td.no { color:#6a7384; }
.hd3 { display:grid; grid-template-columns:repeat(3,1fr); gap:6pt; margin:4pt 0 5pt 0; break-inside:avoid; }
.hd3 .v { border-top:3pt solid #1F3864; background:#F1F4F9; border-radius:0 0 4pt 4pt; padding:5pt 8pt 6pt 8pt; }
.hd3 .v .n { font-family:'Be Vietnam Pro',sans-serif; font-size:7.8pt; font-weight:800; color:#C8992F; letter-spacing:.08em; text-transform:uppercase; }
.hd3 .v .h { font-family:'Be Vietnam Pro',sans-serif; font-size:9pt; font-weight:800; color:#1F3864; margin:1pt 0 2pt 0; }
.hd3 .v .t { font-size:8.8pt; line-height:1.4; text-align:left; }
.hdr5 { font-family:'Be Vietnam Pro',sans-serif; font-size:8.4pt; color:#16294A; background:#FBF3DF; border-left:3pt solid #C8992F; border-radius:0 4pt 4pt 0; padding:4pt 8pt; margin:3pt 0 6pt 0; line-height:1.45; break-inside:avoid; }
"""

_TONEC = {"r": "#A93434", "o": "#C55A11", "y": "#8A6100", "n": "#1F3864", "g": "#1E7A46"}
_NNBG = {"k1": ("#7F6000", "#FDF8EA"), "k2": ("#1F3864", "#F1F4F9"), "k3": ("#A93434", "#FBF1F1"), "k0": ("#5b6474", "#F4F4F4")}
NN_SUB = {"k1": "Sai quy trình, quản lý tiền kém; không thấy ai hưởng lợi", "k2": "Sai giấy tờ, ghi chép; sửa được ngay",
          "k3": "Lỡ tay có chủ đích: cần chứng từ để kết luận", "k0": "Tái tục 127,5 tỷ, chờ hợp đồng"}
# muc do cua tung nguyen nhan (dung chung bao cao, dashboard, clip)
NN_MUC = {"k1": "Làm sai quy trình hoặc quản lý tiền kém, không thấy ai hưởng lợi. Vi phạm đã rõ vẫn phải khắc phục và thuộc diện phạt.",
          "k2": "Sai sót kỹ thuật, chứng từ gốc đúng; mức nhẹ nhất, sửa được ngay khi được hỏi.",
          "k3": "Mức nặng nhất. Chỉ xếp vào nhóm này khi có ít nhất 2 trong 3 dấu hiệu rõ; kết luận vi phạm pháp luật thuộc cơ quan có thẩm quyền."}
NN_N = {"k1": f"{len(NNC['k1'])} dấu hiệu", "k2": f"{len(NNC['k2'])} dấu hiệu", "k3": f"0 dấu hiệu đủ căn cứ · {len(NNC['k3'])} chưa loại trừ"}
NN_ND_LABEL = "NHẬN ĐỊNH · PHÂN LOẠI NGUYÊN NHÂN"


def causes_table(E, table):
    """Ba nguyen nhan: bieu hien, muc do, dau hieu (bao cao day du muc 1.3)."""
    rows = []
    for (k, lab, bh, _hq) in PL.CAUSES:
        rows.append([f'<span class="kk5 {k}">{E(lab)}</span>', E(bh), E(NN_MUC[k]), ", ".join(NNC[k]) + (f'<span class="sm">{E(NN_N[k])}</span>')])
    return table(["Nguyên nhân", "Biểu hiện trong hồ sơ", "Mức độ", "Dấu hiệu"], rows, widths=["17%", "38%", "30%", "15%"], esc=False, tcls="kxt")


def check_table(E, table):
    """Bang kiem ba dau hieu cua lo tay co chu dich (cung file Phan loai)."""
    def st(v):
        c = {"Có": "#A93434", "Một phần": "#C55A11", "Chưa biết": "#5b6474", "Không": "#1E7A46"}[v[0]]
        return f'<b style="color:{c}">{E(v[0])}</b>: {E(v[1])}'
    return table(["Mã", "Khoản", "Lặp lại cùng kiểu", "Hưởng lợi, giá bất thường", "Chứng từ né tránh, mâu thuẫn", "Số dấu hiệu rõ", "Chứng từ quyết định"],
                 [[f"<b>{c}</b>", E(a), st(x), st(y), st(z), f"<b>{n}/3</b>", E(k)] for c, a, x, y, z, n, k in PL.CHECK],
                 cls=["", "", "", "", "", "c", ""], widths=["6%", "11%", "15%", "17%", "17%", "9%", "25%"], esc=False, tcls="kxt")


def cause_pill(E, code):
    k = NN[code]["k"]
    return f'<span class="kk5 {k}">{E(NNL[k])}</span>'


def k5_html(E, compact=False):
    """Nam cau hoi dang the: so, cau hoi, cau tra loi, cac y, con so chinh."""
    out = []
    for x in Q:
        lis = "" if compact else "<ul>" + "".join(f"<li>{E(l)}</li>" for l in x["lines"]) + "</ul>"
        out.append(f'<div class="r t-{x["tone"]}"><div class="no">{x["n"]}</div><div><div class="qq">{E(x["q"])}</div><div class="aa">{E(x["a"])}</div>{lis}</div>'
                   f'<div class="kv"><div class="v">{E(x["v"])}</div><div class="l">{E(x["vl"])}</div></div></div>')
    return f'<div class="k5{" cmp" if compact else ""}">' + "".join(out) + "</div>"


def k5_strip(E):
    """Ban mot bang cho tai lieu lam viec: cau hoi, tra loi ngan, con so."""
    rows = "".join(f'<tr class="t-{x["tone"]}"><td class="q">{x["n"]}. {E(x["q"])}</td><td>{E(x["s"])}</td><td class="v">{E(x["v"])}</td></tr>' for x in Q)
    return (f'<div class="cap" style="margin-top:6pt">{E(TITLE)}: {E(SUB.lower())}</div><table class="k5s"><tbody>{rows}</tbody></table>')


def nn_tiles(E):
    return '<div class="nnt">' + "".join(
        f'<div class="t" style="--c:{_NNBG[k][0]};--b:{_NNBG[k][1]}"><div class="n">{len(NNC[k])}</div><div class="k">{E(NNL[k])}</div><div class="s">{E(NN_SUB[k])}</div></div>'
        for k in NN_ORDER) + "</div>"


def nn_matrix(E, table):
    """Bang 16 dau hieu theo nguyen nhan va tinh trang phap ly; mau cua ma la muc do."""
    def cc(c): return f'<span class="cc s-{_F[c]["sev"]}">{c}</span>'
    rows = []
    for k in NN_ORDER:
        rows.append([f'<span class="kk5 {k}">{E(NNL[k])}</span>'] + ["".join(cc(c) for c in NNC[k] if LG.LG_F[c][0] == st) for st in ST_ORDER] + [f"<b>{len(NNC[k])}</b>"])
    rows.append(["<b>Tổng</b>"] + [f"<b>{len(ST[st])}</b>" for st in ST_ORDER] + ["<b>16</b>"])
    return table(["Nguyên nhân"] + [LG.LG_ST[st][0] for st in ST_ORDER] + ["Tổng"], rows, cls=["", "", "", "", "", "c"],
                 widths=["22%", "14%", "30%", "14%", "11%", "9%"], esc=False, tcls="nnm")


def qm_table(E, table):
    mx = max(v if not isinstance(v, tuple) else v[1] for _, v, _, _, _ in QM if v != FUND)
    rows = []
    for g, v, gom, st, tone in QM:
        w = 100 if v == FUND else round(100 * (v[1] if isinstance(v, tuple) else v) / mx)
        bar = "" if v == FUND else f'<span class="qmb" style="width:{w}%"></span>'
        rows.append([f"<b>{E(g)}</b>", f'<span class="amt" style="--c:{_TONEC[tone]}">{E(qm_amt(v))}</span>{bar}', E(qm_pct(v)), E(gom), E(st)])
    return table(QM_H, rows, cls=["", "", "n", "", ""], widths=["21%", "17%", "12%", "37%", "13%"], esc=False, tcls="qmt",
                 row_cls=[f"t-{r[4]}" for r in QM])


def kx_table(E, table):
    rows = []
    for r in KX:
        rows.append([f'<span style="color:{_TONEC[r[7]]};font-family:\'Be Vietnam Pro\',sans-serif;font-weight:800">{E(r[0])}</span>', E(r[1])] +
                    [f'<span class="{"" if v != "Không" else "no"}">{E(v)}</span>' for v in r[2:7]])
    return table(KX_H, rows, widths=["17%", "10%", "15%", "13%", "15%", "13%", "17%"], esc=False, tcls="kxt")


def kxc_table(E, table):
    return table(KXC_H, [[f'<span class="kk5 {k}">{E(a)}</span>', E(b), E(c)] for a, b, c, k in KXC], cls=["", "c", ""],
                 widths=["22%", "14%", "64%"], esc=False, tcls="kxt")


def hd3_html(E):
    return '<div class="hd3">' + "".join(f'<div class="v"><div class="n">{E(a)}</div><div class="h">{E(b)}</div><div class="t">{E(c)}</div></div>' for a, b, c in HD3) + "</div>"


def all_lines():
    out = [TITLE, SUB, INTRO, QM_NOTE, KX_NOTE, HD_TITLE, HD_RULE] + ND
    for x in Q: out += [x["q"], x["a"], x["s"], x["vl"]] + x["lines"]
    return out
