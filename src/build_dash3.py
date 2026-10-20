# -*- coding: utf-8 -*-
"""Dashboard v3: 6 phan, ket luan tung muc, nap sao ke moi, tu cap nhat (artifact publish)."""
import json, base64, os, subprocess, sys
PAGES = os.environ.get("DASH_PAGES") == "1"
PAGES_URL = "https://jukytwo.github.io/ssr-so-quy-bao-tri/"
from collections import Counter
sys.path.insert(0, "/home/claude/ssr")
import viz
import legal as LG

os.chdir("/home/claude/ssr")
D = json.load(open("dash_data.json"))
A = json.load(open("analysis.json"))
C2 = json.load(open("content2.json"))
MX = json.load(open("matrix.json"))
for _t in C2["verdict"]["tiers"]:
    _t["hq"] = LG.LG_VD[_t["tone"]]
for _f in D["findings"]:
    _lab, _c, _bg, _hq, _hqif, _iflab, _st = LG.lg_of(_f["id"])
    _f.update(lst=_st, lhq=_hq, lif=_hqif, liflab=_iflab, lhqlab=LG.LG_HQLAB[_st] or "Hệ quả")
assert sorted(f["id"] for f in D["findings"]) == sorted(LG.LG_F)
# ---- phan loai nguyen nhan (cung nguon build_phanloai.py voi file Phan loai, anh Phan loai)
import build_phanloai as PL
import ketluan5 as K5
import build_hoidan as _HDN
K5_ISS = _HDN.ISS
NNL = {"k1": "(1) Thiếu năng lực", "k2": "(2) Lỡ tay thật", "k3": "Chưa loại trừ (3)", "k0": "Chưa phát sinh sai"}
_NNG = (("k1", PL.G1), ("k2", PL.G2), ("k3", PL.G3), ("k0", PL.G0))
_NNMAP = {c: (k, w, ch, cf) for k, g in _NNG for c, _t, w, ch, cf in g}
assert sorted(_NNMAP) == sorted(f["id"] for f in D["findings"])
for _f in D["findings"]:
    _k, _w, _ch, _cf = _NNMAP[_f["id"]]
    _f.update(nn=_k, nnw=_w, nnc=_ch, nnt=_cf)

SEC = {"01": ("ket-luan", "Có sai phạm không, tới đâu, xử lý thế nào", 1), "02": ("du-lieu", "Nguồn dữ liệu", 2), "03": ("giam-dinh", "Sao kê thật hay giả", 2),
       "04": ("tien-o-dau", "Quỹ còn bao nhiêu", 3), "05": ("vi-sao", "Tiền đi đâu", 3), "06": ("khu-vuc-chung", "Tiền khu vực chung", 3), "07": ("lai-suat", "Lãi suất", 3),
       "08": ("an-toan", "Thang máy, phòng cháy", 4), "09": ("quy-che", "Tuân thủ Quy chế", 4), "10": ("bo-sung", "Kiểm tra bổ sung", 4),
       "11": ("dau-hieu", "Mức độ, nguyên nhân, xử lý", 5), "12": ("ho-so", "Việc cần làm", 5)}
SCORE_KEY = {"02": "198 giao dịch khớp; còn thiếu sao kê TK vận hành và giấy xác nhận tiền gửi.",
             "03": "Bản thật do ngân hàng lập; tiền lãi 33 tháng khớp tới từng đồng.",
             "04": "Tiền gốc 127,15 tỷ không giảm; 98% là tiền gửi, ngân hàng mới xác nhận 120 tỷ tại 20/05/2025.",
             "05": "1,69 tỷ không truy được tới cùng; 986,9 triệu trái Điều 7.2 và 7.4.",
             "06": "1,71 tỷ giữ ngoài quỹ, trái khoản 4 Điều 153 Luật Nhà ở 2023.",
             "07": "Đúng biểu từng thời điểm; bỏ lỡ 0,42 – 0,96 tỷ vì cách gửi.",
             "08": "14 hợp đồng sửa trong 7 tháng; chưa thấy giấy kiểm định và biên bản phòng cháy.",
             "09": "3 vi phạm và 6 nghi vấn trong 17 quy định được đối chiếu.",
             "10": "Không có tiền mặt hay chuyển cho cá nhân; ba điểm mới cần trả lời.",
             "11": "3 Đỏ, 7 Cam, 6 Vàng; ba vi phạm đã rõ thuộc diện xử phạt; 9 dấu hiệu do thiếu năng lực, chưa dấu hiệu nào đủ căn cứ là có chủ đích.",
             "12": "Đòi ba hồ sơ chính, tạm dừng khoảng 0,92 tỷ chi còn lại."}
K4 = ["Gửi kỳ hạn 12 tháng cho phần quỹ chưa có kế hoạch dùng trong năm, thay vì tái tục 3 tháng.",
      "Giữ tài khoản thanh toán khoảng 1 tỷ, đủ cho khoản chi lớn nhất, phần dư chuyển sang tiền gửi có kỳ hạn.",
      "Chào lãi suất từ ít nhất ba ngân hàng uy tín trước mỗi lần tái tục, lưu văn bản chào giá như Quy chế yêu cầu.",
      "Công khai hợp đồng tiền gửi, lãi suất và ngày đáo hạn trên bảng tin sau mỗi lần gửi hoặc tái tục."]
ROAD = {"steps": [["Gửi văn bản yêu cầu", "Nhiều chủ sở hữu cùng ký, nêu danh mục hồ sơ ưu tiên cao, đề nghị trả lời trong 15 ngày; căn cứ khoản 1 Điều 7 Nội quy và Điều 7 Quy chế hoạt động Ban quản trị."],
                  ["Xác nhận tại ngân hàng", "Đại diện cư dân cùng Ban quản trị nhận giấy xác nhận số dư và sao kê có dấu tại quầy VietinBank, Agribank."],
                  ["Kiểm toán đột xuất", "Đề nghị kiểm toán độc lập quỹ bảo trì đột xuất; Quy chế cho phép không chờ hết năm tài chính (Điều 8.8.b)."],
                  list(LG.ROAD4)],
        "cards": [["Tạm dừng cho tới khi có hồ sơ", "Đề nghị Ban quản trị chưa chi tiếp 623,3 triệu còn lại của hợp đồng cấp nước và phần còn lại của các hợp đồng sửa thang máy đã tạm ứng, cho tới khi công khai hợp đồng, báo giá và biên bản nghiệm thu."],
                  ["Một chỗ Quy chế cần thống nhất", "Tần suất công khai chi tiêu kinh phí bảo trì trên bảng tin ghi ba mức: 6 tháng (Điều 3.1.a Quy chế thu chi), hằng tháng (Điều 6.1.g Quy chế thu chi) và 3 tháng (điểm b khoản 1 Điều 9 Quy chế hoạt động Ban quản trị). Nên thống nhất theo mức hằng tháng tại Hội nghị nhà chung cư gần nhất."]]}

stm = []
for k in ["AG24", "AG25", "AG26", "Q24", "Q25", "Q26", "V25", "V26"]:
    s = A["statements"][k]
    stm.append(dict(a={"AG": "AGR", "Q2": "999", "V2": "7784"}[k[:2]], bank=s["bank"].split(" – ")[0], period=s["period"] if k != "Q24" else "15/08/2024 – 31/12/2024",
                    n=s["n"], debit=s["debit"], credit=s["credit"], ending=s["ending"]))

PDF_SRC = "/mnt/user-data/outputs/SSR_Bao_cao_phan_tich_quy_bao_tri_full.pdf"
XLSX_SRC = "/mnt/user-data/outputs/SSR_Sao_ke_tong_hop_va_phan_tich.xlsx"
CV_SRC = "/mnt/user-data/outputs/Cong_van_kien_nghi_gui_BQT_SSR.docx"
subprocess.run(["qpdf", "--object-streams=generate", "--compress-streams=y", "--recompress-flate", "--compression-level=9", PDF_SRC, "/home/claude/ssr/d3/report_embed.pdf"], check=False)
pdf_b = open("/home/claude/ssr/d3/report_embed.pdf", "rb").read()
xlsx_b = open(XLSX_SRC, "rb").read()
import pypdfium2
npg = len(pypdfium2.PdfDocument(PDF_SRC))
import openpyxl
nsh = len(openpyxl.load_workbook(XLSX_SRC, read_only=True).sheetnames)
files_meta = dict(pdf="SSR_Bao_cao_phan_tich_quy_bao_tri_full.pdf", pdf_desc=f"{npg} trang: năm câu hỏi kết luận, phân loại nguyên nhân, kết luận ba tầng, 12 mục có kết luận riêng, hệ quả pháp lý và điều kiện bãi nhiệm, 3 phụ lục · dữ liệu tới 31/05/2026",
                  xlsx="SSR_Sao_ke_tong_hop_va_phan_tich.xlsx", xlsx_desc=f"{nsh} sheet: năm câu hỏi tính bằng công thức, 8 sao kê chuyển đổi, 32 phép kiểm tra tự động, nếu hạch toán đúng, đối chiếu hợp đồng, kiểm soát từng khoản chi, nhập sao kê mới, theo dõi hồ sơ")
FILES = dict(pdf=base64.b64encode(pdf_b).decode(), xlsx=base64.b64encode(xlsx_b).decode())
if os.path.exists(CV_SRC):
    FILES["cv"] = base64.b64encode(open(CV_SRC, "rb").read()).decode()
    files_meta.update(cv="Cong_van_kien_nghi_gui_BQT_SSR.docx", cv_desc="Văn bản của cư dân đề nghị cung cấp hồ sơ, giải trình và khắc phục; kèm danh mục hồ sơ và danh sách ký tên")

SUM_SRC = "/mnt/user-data/outputs/SSR_Bao_cao_phan_tich_quy_bao_tri_tom_tat.pdf"
if os.path.exists(SUM_SRC):
    subprocess.run(["qpdf", "--object-streams=generate", "--compress-streams=y", "--recompress-flate", "--compression-level=9", SUM_SRC, "/home/claude/ssr/d3/summary_embed.pdf"], check=False)
    FILES["sum"] = base64.b64encode(open("/home/claude/ssr/d3/summary_embed.pdf", "rb").read()).decode()
    files_meta.update(sum="SSR_Bao_cao_phan_tich_quy_bao_tri_tom_tat.pdf",
                      sum_desc=f"{len(pypdfium2.PdfDocument(SUM_SRC))} trang: năm câu hỏi kết luận và phân loại nguyên nhân; giữ nguyên văn các ô Kết luận, Nhận định, Chiến lược; thêm phần Nếu hạch toán đúng và Đối chiếu hợp đồng")
# ---- Muoi cau hoi (ban cong khai) va hai tai lieu lam viec cua nhom cu dan
EXTRA_DL = [("q10png", "/mnt/user-data/outputs/muoi_cau_hoi/Mười câu hỏi cần làm rõ.png", "Ảnh A4 để đăng nhóm chung; các câu hỏi đã gửi Ban quản trị ngày 29/09/2026, đề nghị trả lời trong 5 ngày"),
            ("q10pdf", "/mnt/user-data/outputs/muoi_cau_hoi/Mười câu hỏi - bản in bảng tin.pdf", "Một trang A4 để in dán bảng tin; cùng nội dung với bản ảnh"),
            ("pl", "/mnt/user-data/outputs/SSR_Phan_loai_nguyen_nhan.pdf", "Đánh giá sơ bộ 16 dấu hiệu theo ba nguyên nhân: thiếu năng lực, lỡ tay thật, lỡ tay có chủ đích; hệ quả pháp lý từng dấu hiệu; cập nhật theo chứng từ"),
            ("hdan", "/mnt/user-data/outputs/SSR_Hoi_dan_phan_loai_nguyen_nhan.pdf", "Mười một vấn đề kèm hệ quả pháp lý, ba vòng câu hỏi, cách đọc câu trả lời, bảng theo dõi, mẫu ghi nhận và khi nào dùng bãi nhiệm")]
for _k, _p, _d in EXTRA_DL:
    assert os.path.exists(_p), _p
    FILES[_k] = base64.b64encode(open(_p, "rb").read()).decode()
    files_meta[_k] = os.path.basename(_p); files_meta[_k + "_desc"] = _d
import build_notice as _BN
from html import escape as _esc
Q10 = ('<div class="panel q10-p" id="muoi-cau-hoi"><h3>Mười câu hỏi đã gửi Ban quản trị</h3>'
       '<div class="sub">Các câu hỏi đã được gửi Ban quản trị bằng văn bản điện tử qua email và kênh Zalo do Ban quản trị lập và quản trị vào ngày 29/09/2026, đề nghị trả lời trong 5 ngày. Bản ảnh để đăng nhóm chung, bản PDF khổ A4 để in dán bảng tin.</div>'
       '<div class="q10-sum" id="q10-sum"></div><ol class="q10">' + "".join(f'<li><b>{_esc(t)}</b><span>{_esc(q)}</span><div class="q10-st" data-q="{i}"></div></li>' for i, (t, q) in enumerate(_BN.QS)) + '</ol>'
       '<div class="q10-acts"><button class="tbtn pri" type="button" data-sendfile="q10png"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="M8.6 13.5l6.8 4M15.4 6.5l-6.8 4"/></svg>Gửi ảnh</button><button class="tbtn" type="button" data-dl="q10png">Tải ảnh</button><button class="tbtn" type="button" data-dl="q10pdf">Tải PDF khổ A4</button></div>'
       '<div class="h3x">Tài liệu làm việc của nhóm cư dân</div>'
       '<div class="sub">Đánh giá sơ bộ theo dữ liệu hiện có, sẽ cập nhật khi Ban quản trị trả lời và cung cấp chứng từ. Các nhận định là dấu hiệu cần làm rõ, không phải cáo buộc.</div>'
       '<div class="dlg q10-docs">'
       '<div class="dlc"><div class="ic" style="background:#5b6474">PDF</div><div><h4>Phân loại nguyên nhân các sai sót</h4><p>' + _esc(files_meta["pl_desc"]) + '</p></div><button class="tbtn" type="button" data-dl="pl">Tải PDF</button></div>'
       '<div class="dlc"><div class="ic" style="background:#5b6474">PDF</div><div><h4>Hỏi dần để biết mỗi cái sai thuộc nguyên nhân nào</h4><p>' + _esc(files_meta["hdan_desc"]) + '</p></div><button class="tbtn" type="button" data-dl="hdan">Tải PDF</button></div>'
       '</div></div>')
assert len(_BN.QS) == 10
D["q10"] = dict(t=[t for t, q in _BN.QS], sent="2026-09-29", due="2026-10-04", sent_l="29/09/2026", due_l="04/10/2026")
from newdocs import HT, HD, HD_ND, DOCS, RQ, vnd, TD_NEW
D.update(ht=HT, hd=HD, hd_nd=HD_ND, docs=DOCS, td_new=TD_NEW)
# ---- hoi dap theo chu de: kiem tra so lieu trong cau tra loi khop du lieu
import faq_data
FAQ = faq_data.build()
_T = json.dumps(FAQ, ensure_ascii=False)
def _f(x, d): return f"{x:.{d}f}".replace(".", ",")
_U = D["units"]; _SG = A["spend_groups"]
_SAFE = sum(x["v"] for x in D["safety"] if x["g"] == "safe"); _OTH = sum(x["v"] for x in D["safety"] if x["g"] != "safe")
_NEWINT = 45e9 * .08 + 15e9 * .08 + 2.5e9 * .08 + 5e9 * .078 + 60e9 * .08; _OLDINT = 45e9 * .047 + 15e9 * .024 + 5e9 * .047 + 60e9 * .047 + 2.5e9 * .002
_INC = {x["l"].split(" (")[0]: x["v"] for x in D["income"]}
_TC = A["exp7784"]["Chi sửa chữa, mua sắm – Thành Công"]
for _need in [_f(D["fund_in"] / _U / 1e6, 1) + " triệu mỗi căn", _f(986_910_176 / _U / 1e3, 0) + " nghìn đồng mỗi căn", _f(D["ca_total"] / _U / 1e3, 0) + " nghìn đồng mỗi căn",
              _f(D["opp_lo"] / _U / 1e3, 0) + " – " + _f(D["opp_hi"] / _U / 1e3, 0) + " nghìn", _f((_NEWINT - _OLDINT) / _U / 1e6, 1) + " triệu đồng mỗi căn",
              _f(D["fund_end"] / 1e9, 2) + " tỷ", _f((D["fund_end"] - D["fund_in"]) / 1e9, 2) + " tỷ", _f(D["interest"] / 1e9, 2) + " tỷ", _f(D["spend"] / 1e9, 2) + " tỷ",
              _f(D["opaque"] / 1e9, 2) + " tỷ", _f(D["ca_total"] / 1e9, 2) + " tỷ", _f(D["repair7784"] / 1e9, 2) + " tỷ", _f(D["end_v"] / 1e6, 1) + " triệu", _f(D["taxes"] / 1e6, 1) + " triệu",
              _f(D["opp_lo"] / 1e9, 2) + " – " + _f(D["opp_hi"] / 1e9, 2) + " tỷ", _f(RQ / 1e9, 2) + " tỷ", _f((_SG["Chi sửa chữa cấp nước – HNB"]["total"] + _SG["Chi mua thiết bị – Thép Quang"]["total"] + D["repair7784"]) / 1e9, 2) + " tỷ",
              _f(_SAFE / 1e9, 2) + " tỷ", _f(_OTH / 1e9, 2) + " tỷ", _f(D["comp"][-1]["v"] / 1e9, 2) + " tỷ", _f(_INC["Chicilon Media"] / 1e9, 2) + " tỷ",
              _f(_INC["Viễn thông ACT"] / 1e6, 1) + " triệu", _f(_INC["Công nghệ Hưng Thái"] / 1e6, 1) + " triệu", _f(_TC / 1e6, 1) + " triệu", f"{round(_TC / D['repair7784'] * 100)}%",
              _f(D["chic"]["m_2024"] / 1e6, 2) + " triệu", _f(D["chic"]["m_2025"] / 1e6, 1) + " triệu", _f(-D["chic"]["drop"] * 100, 1) + "%", _f(D["chic"]["year_gap"] / 1e6, 1) + " triệu",
              _f(_NEWINT / 1e9, 2) + " tỷ", _f((_NEWINT - _OLDINT) / 1e9, 1) + " tỷ", _f(sum(x["v"] for x in _SG.values() if False) if False else 986_910_176 - 863_834_733, 0)]:
    if _need.isdigit():
        assert f"{int(_need):,}".replace(",", ".") in _T, _need
    else:
        assert _need in _T, _need
assert sum(1 for f in D["findings"] if f["sev"] == "Đỏ") == 3 and sum(1 for f in D["findings"] if f["sev"] == "Cam") == 7 and sum(1 for f in D["findings"] if f["sev"] == "Vàng") == 6
from keymsg import KM
D.update(faq=FAQ, km=KM)

D.update(sec={k: dict(id=v[0], t=v[1], p=v[2]) for k, v in SEC.items()}, score_key=SCORE_KEY, concl=C2["concl"], verdict=C2["verdict"], tln=C2["timeline"],
         glo=C2["glossary"], roll=C2["roll"], roll_base=C2["roll_base"], stm=stm, k4=K4, road=ROAD, files=files_meta, built="30/09/2026",
         base=dict(fund_end=A["fund_end"], interest=D["interest"], spend=D["spend"], ca_total=D["ca_total"], repair7784=D["repair7784"],
                   end_q=A["end_q"], end_a=A["end_a"], end_v=A["end_v"], asof="31/05/2026"))
D.pop("rates", None)

# ---- khung he qua phap ly (cung nguon legal.py voi bao cao, ban tom tat, Excel, tai lieu lam viec)
_TONE = {"ro": "crit", "cho": "warn", "hs": "na"}
_BST = {"ok": "b-ok", "no": "b-no", "na": "b-na"}
LEGAL = ('<div class="panel lgw" id="he-qua"><h3>Hệ quả pháp lý: điều gì chắc chắn phải xử lý, điều gì phụ thuộc chứng từ</h3>'
         '<div class="sub">Cùng khung với báo cáo đầy đủ (mục 11.1), bản tóm tắt, file Excel và hai tài liệu làm việc. Đây là hệ quả theo quy định, không phải kết luận; việc xử lý cụ thể do Hội nghị nhà chung cư và cơ quan có thẩm quyền quyết định.</div>'
         '<div class="lg-lad">' + "".join(
             f'<div class="lg-c t-{_TONE[x["k"]]}"><div class="lg-n">{_esc(x["name"])}</div><div class="lg-w">{_esc(x["what"])}</div><ul>'
             + "".join(f"<li>{_esc(l)}</li>" for l in x["lines"]) + "</ul></div>" for x in LG.LG_LADDER) + '</div>'
         '<div class="h3x">Hình thức xử lý, mức và căn cứ</div>'
         '<div class="tbl-wrap cards lg-t"><table><thead><tr>' + "".join(f"<th>{_esc(h)}</th>" for h in LG.LG_FORMS_H) + '</tr></thead><tbody>' + "".join(
             f'<tr><td data-l="{_esc(LG.LG_FORMS_H[0])}" class="lg-f">{_esc(a)}</td><td data-l="{_esc(LG.LG_FORMS_H[1])}">{_esc(b)}</td><td data-l="{_esc(LG.LG_FORMS_H[2])}" class="lg-cc">{_esc(c)}</td><td data-l="{_esc(LG.LG_FORMS_H[3])}" class="lg-cc">{_esc(d)}</td></tr>'
             for a, b, c, d in LG.LG_FORMS) + '</tbody></table></div>'
         '<div class="h3x">Điều kiện bãi nhiệm thành viên Ban quản trị</div>'
         '<div class="tbl-wrap cards lg-t"><table><thead><tr>' + "".join(f"<th>{_esc(h)}</th>" for h in LG.LG_BAI_H) + '</tr></thead><tbody>' + "".join(
             f'<tr><td data-l="{_esc(LG.LG_BAI_H[0])}">{_esc(a)}</td><td data-l="{_esc(LG.LG_BAI_H[1])}" class="lg-cc">{_esc(b)}</td><td data-l="{_esc(LG.LG_BAI_H[2])}"><span class="bst {_BST[k]}">{_esc(lab)}</span>' + (f' <span class="lg-nt">{_esc(nt)}</span>' if nt else "") + '</td></tr>'
             for a, b, lab, k, nt in LG.LG_BAI) + '</tbody></table></div>'
         f'<div class="lg-end">{_esc(LG.LG_BAI_END)}</div>'
         '<div class="nd"><div class="lab">Nhận định · Hệ quả pháp lý</div>' + "".join(f"<p>{_esc(x)}</p>" for x in LG.LG_ND) + '</div>'
         f'<p class="note">{_esc(LG.LG_NOTE)}</p><p class="note" style="margin-top:4px">Nguồn: {_esc(LG.LG_SRC)}</p></div>')
# ---- khoi phan loai nguyen nhan: muc do va huong xu ly (cung nguon ketluan5.py voi bao cao, ban tom tat, Excel, clip)
_FS = {f["id"]: f for f in D["findings"]}
def _cd(c): return f'<a class="cd sev-{_FS[c]["sev"]}" href="#find-{c}" data-code="{c}">{c}</a>'
_NNC = K5.NNC
_CK = {"Có": "y", "Một phần": "p", "Chưa biết": "u", "Không": "no"}
_ST_ORDER = K5.ST_ORDER
def _tbl(cls, heads, rows):
    """Bang doc tren may tinh, thanh the tren dien thoai (data-l la nhan cot)."""
    return (f'<div class="tbl-wrap cards {cls} lg-t"><table><thead><tr>' + "".join(f"<th>{_esc(h)}</th>" for h in heads) + '</tr></thead><tbody>'
            + "".join("<tr>" + "".join(f'<td data-l="{_esc(h)}"{(" class=" + chr(34) + c + chr(34)) if c else ""}>{v}</td>' for h, (v, c) in zip(heads, r)) + "</tr>" for r in rows)
            + '</tbody></table></div>')
_ISS_ROWS = [[(str(i + 1), "c"), (_esc(x["t"]), ""), (_esc(x["codes"]), "lg-cc"), (f'<span class="nnp nn-{x["lean"][1]}">{_esc(x["lean"][0])}</span>', ""), (_esc(x["key"]), "")]
             for i, x in enumerate(K5_ISS)]
NNP = ('<div class="panel nnw" id="nguyen-nhan"><h3>Mức độ theo nguyên nhân: thiếu năng lực, lỡ tay thật hay lỡ tay có chủ đích</h3>'
       '<div class="sub">Câu hỏi thứ ba của cuộc kiểm tra. Đánh giá sơ bộ của nhóm cư dân theo dữ liệu hiện có, công khai cùng bộ tài liệu; phân loại sẽ xem lại khi Ban quản trị trả lời và cung cấp chứng từ. Các nhận định là dấu hiệu cần làm rõ, không phải cáo buộc.</div>'
       '<div class="nn-tiles">' + "".join(f'<div class="nn-tile nn-{k}"><div class="v">{len(_NNC[k])}</div><div class="k">{_esc(NNL[k])}</div><div class="s">{_esc(K5.NN_SUB[k])}</div></div>' for k in ("k1", "k2", "k3", "k0")) + '</div>'
       '<div class="nd"><div class="lab">Nhận định · Phân loại nguyên nhân</div>' + "".join(f"<p>{_esc(x)}</p>" for x in PL.ND_TOP) + '</div>'
       '<div class="h3x">Ba nguyên nhân: mức độ và hướng xử lý</div>'
       '<div class="nn-cards">' + "".join(
           f'<div class="nn-card nn-{k}"><h4>{_esc(lab)}</h4><div class="n">{_esc(K5.NN_N[k])}</div>'
           f'<div class="r"><b>Biểu hiện</b>{_esc(bh)}</div><div class="r"><b>Mức độ</b>{_esc(K5.NN_MUC[k])}</div><div class="r"><b>Hướng xử lý và hệ quả</b>{_esc(hq)}</div>'
           f'<div class="cds">' + "".join(_cd(c) for c in _NNC[k]) + '</div></div>'
           for (cls, lab, bh, hq), k in zip(PL.CAUSES, ("k1", "k2", "k3"))) + '</div>'
       '<div class="h3x">16 dấu hiệu theo nguyên nhân và tình trạng pháp lý</div>'
       '<div class="subx">Màu của mã là mức độ: đỏ cần giải trình ngay, cam cần hồ sơ chứng minh, vàng cần cải thiện. Bấm mã để mở thẻ dấu hiệu.</div>'
       '<div class="tbl-wrap cards nn-m lg-t"><table><thead><tr><th>Nguyên nhân</th>' + "".join(f'<th>{_esc(LG.LG_ST[st][0])}</th>' for st in _ST_ORDER) + '<th class="c">Tổng</th></tr></thead><tbody>' + "".join(
           f'<tr><td class="nn-h" data-l="Nguyên nhân"><span class="nnp nn-{k}">{_esc(NNL[k])}</span></td>' + "".join(
               f'<td data-l="{_esc(LG.LG_ST[st][0])}">' + "".join(_cd(c) for c in _NNC[k] if _FS[c]["lst"] == st) + '</td>' for st in _ST_ORDER)
           + f'<td class="nn-t c" data-l="Tổng">{len(_NNC[k])}</td></tr>' for k in ("k1", "k2", "k3", "k0")) + '</tbody></table></div>'
       '<div class="nd"><div class="lab">Nguyên tắc phân loại</div>' + "".join(f"<p>{_esc(x)}</p>" for x in PL.RULES) + '</div>'
       f'<div class="h3x" id="hoi-dan">{_esc(K5.HD_TITLE)}</div>'
       '<div class="subx">Phân loại chỉ chốt sau khi hỏi bằng văn bản theo ba vòng; kết quả từng vòng dùng để đổi nhóm của dấu hiệu. Câu hỏi từng vòng và cách đọc câu trả lời ở file Hỏi dần.</div>'
       '<div class="hd3">' + "".join(f'<div class="hd3-v"><div class="n">{_esc(a)}</div><div class="h">{_esc(b)}</div><div class="t">{_esc(c)}</div></div>' for a, b, c in K5.HD3) + '</div>'
       '<div class="h3x">Bảng kiểm ba dấu hiệu của lỡ tay có chủ đích</div>'
       '<div class="tbl-wrap cards nn-ck lg-t"><table><thead><tr><th>Mã</th><th>Khoản</th><th>Lặp lại cùng kiểu</th><th>Hưởng lợi, giá bất thường</th><th>Chứng từ né tránh, mâu thuẫn</th><th class="c">Số dấu hiệu rõ</th><th>Chứng từ quyết định</th></tr></thead><tbody>' + "".join(
           f'<tr><td data-l="Mã">{_cd(c)}</td><td data-l="Khoản">{_esc(a)}</td>' + "".join(f'<td data-l="{h}"><span class="{_CK[v[0]]}">{_esc(v[0])}</span>: {_esc(v[1])}</td>' for h, v in zip(("Lặp lại cùng kiểu", "Hưởng lợi, giá bất thường", "Chứng từ né tránh, mâu thuẫn"), (x, y, z)))
           + f'<td class="c" data-l="Số dấu hiệu rõ"><b>{n}/3</b></td><td data-l="Chứng từ quyết định">{_esc(k2)}</td></tr>' for c, a, x, y, z, n, k2 in PL.CHECK) + '</tbody></table></div>'
       f'<p class="nn-note">{_esc(K5.HD_RULE)}</p>'
       '<div class="h3x">Mười một vấn đề cần hỏi dần: phân loại sơ bộ và chứng từ quyết định</div>'
       + _tbl("nn-iss", ["#", "Vấn đề", "Mã", "Sơ bộ", "Chứng từ quyết định"], _ISS_ROWS) +
       '<div class="q10-acts"><button class="tbtn pri" type="button" data-dl="pl">Tải file Phân loại nguyên nhân (PDF)</button><button class="tbtn" type="button" data-dl="hdan">Tải file Hỏi dần (PDF)</button></div></div>')
# ---- nam cau hoi: trang dau (ban gon) va muc 01 (ban day du, quy mo, khung xu ly)
_K5T = {"r": "t-r", "o": "t-o", "y": "t-y", "n": "t-n", "g": "t-g"}
_K5GO = {1: [("#dau-hieu", "16 dấu hiệu"), ("#tiers", "Ba tầng kết luận")], 2: [("#tiers", "Ba tầng kết luận"), ("#keys", "Ba hồ sơ quyết định")],
         3: [("#nguyen-nhan", "Phân loại nguyên nhân"), ("#hoi-dan", "Hỏi dần ba vòng")], 4: [("#quy-mo", "Bảng quy mô"), ("#nguong", "Từng hợp đồng so với ngưỡng")],
         5: [("#khung-xu-ly", "Khung xử lý"), ("#he-qua", "Hệ quả pháp lý chi tiết")]}
KL5S = ('<div class="k5s-w" id="nam-cau"><div class="k5s-h"><div><div class="eyebrow">Năm câu hỏi và câu trả lời</div><h2>' + _esc(K5.SUB) + '</h2></div>'
        '<a class="tbtn pri" href="#nam-cau-hoi">Xem đầy đủ</a></div><ol class="k5s">' + "".join(
            f'<li class="{_K5T[x["tone"]]}"><a href="#q-{x["n"]}"><span class="n">{x["n"]}</span><span class="q">{_esc(x["q"])}</span><span class="a">{_esc(x["s"])}</span><b class="v">{_esc(x["v"])}</b></a></li>'
            for x in K5.Q) + '</ol></div>')
_QM_ROWS = []
_qmx = max(v if not isinstance(v, tuple) else v[1] for _g, v, _m, _s, _t in K5.QM if v != K5.FUND)
for g, v, gom, st, tone in K5.QM:
    w = 100 if v == K5.FUND else round(100 * (v[1] if isinstance(v, tuple) else v) / _qmx)
    bar = "" if v == K5.FUND else f'<i class="qmb" style="width:{w}%"></i>'
    _QM_ROWS.append([(f"<b>{_esc(g)}</b>", ""), (f'<span class="qma">{_esc(K5.qm_amt(v))}</span>{bar}', f"qm-v {_K5T[tone]}"), (_esc(K5.qm_pct(v)), "n"), (_esc(gom), ""), (_esc(st), "")])
import nguong as NG
_NG_T = {True: "t-r", False: ""}
_NG_ROWS = [[(r['code'], 'lg-cc'), (f"<b>{_esc(r['short'])}</b>", ''), (_esc(r['hd']), ''), (_esc(r['src']), ''),
             (f'<b>{NG.tr(r["val"])}</b>', 'n'), ((NG.lan(r['x']) + ' lần') if r['over'] else 'Từng hợp đồng dưới mức', 'n' + (' ngx' if r['over'] and r['x'] >= 5 else '')),
             (NG.pct(r['cap']), 'n'), (_esc(r['how']), '')] for r in NG.ROWS]
_KX_ROWS = [[(f'<span class="kxs">{_esc(r[0])}</span>', _K5T[r[7]]), (_esc(r[1]), "lg-cc")] + [(_esc(v), "kx-no" if v == "Không" else "") for v in r[2:7]] for r in K5.KX]
_KXC_ROWS = [[(f'<span class="nnp nn-{k}">{_esc(a)}</span>', ""), (_esc(b), "c"), (_esc(c), "")] for a, b, c, k in K5.KXC]
KL5 = ('<div class="panel k5w" id="nam-cau-hoi"><h3>' + _esc(K5.TITLE) + '</h3><div class="sub">' + _esc(K5.INTRO) + '</div><div class="k5g">' + "".join(
           f'<article class="k5c {_K5T[x["tone"]]}" id="q-{x["n"]}"><div class="k5m"><div class="k5h"><span class="k5n">{x["n"]}</span><span class="k5q">{_esc(x["q"])}</span></div>'
           f'<p class="k5a">{_esc(x["a"])}</p><ul class="k5l">' + "".join(f"<li>{_esc(l)}</li>" for l in x["lines"]) + '</ul>'
           '<div class="k5go">' + "".join(f'<a href="{h}">{_esc(t)}</a>' for h, t in _K5GO[x["n"]]) + '</div></div>'
           f'<div class="k5v"><b>{_esc(x["v"])}</b><span>{_esc(x["vl"])}</span></div></article>' for x in K5.Q) + '</div>'
       '<div class="nd"><div class="lab">Nhận định · Năm câu hỏi</div>' + "".join(f"<p>{_esc(x)}</p>" for x in K5.ND) + '</div>'
       '<div class="h3x" id="quy-mo">Quy mô vi phạm</div><div class="subx">Số tiền của từng nhóm, so với số dư quỹ 127,15 tỷ ngày 31/05/2026; thanh màu cho thấy độ lớn tương đối.</div>'
       + _tbl("qm-t", K5.QM_H, _QM_ROWS) + f'<p class="note">{_esc(K5.QM_NOTE)}</p>'
       + '<div class="h3x" id="nguong">' + _esc(NG.TITLE) + '</div><div class="subx">' + _esc(NG.KICK) + '</div>'
       + _tbl("ng-t", NG.H, _NG_ROWS) + f'<p class="note">Cộng: {NG.N_OVER} khoản trên 50 triệu, {NG.ty(NG.V_OVER)}. Chi sửa chữa năm 2025: {NG.ty(NG.Y25)}, gấp {NG.lan(NG.Y25 / NG.TRAN)} lần trần; 5 tháng đầu 2026: {NG.ty(NG.Y26)}, gấp {NG.lan(NG.Y26 / NG.TRAN)} lần. Giá trị hợp đồng suy ra từ tỷ lệ tạm ứng khi chưa trả hết.</p>'
       + '<div class="nd"><div class="lab">' + 'Nhận định · Thẩm quyền chi (Điều 9.2)' + '</div>' + ''.join(f'<p>{_esc(x)}</p>' for x in NG.ND) + '</div>'
       '<div class="h3x" id="khung-xu-ly">Khung xử lý</div><div class="subx">Tình trạng của dấu hiệu quyết định hệ quả với Ban quản trị; nguyên nhân quyết định cách xử lý trách nhiệm cá nhân. Chi tiết hình thức xử lý và điều kiện bãi nhiệm ở mục 11.</div>'
       + _tbl("kx-t", K5.KX_H, _KX_ROWS) + '<div class="subx" style="margin-top:12px">Theo nguyên nhân</div>' + _tbl("kxc-t", K5.KXC_H, _KXC_ROWS)
       + f'<p class="note">{_esc(K5.KX_NOTE)}</p><div class="q10-acts"><a class="tbtn" href="#he-qua">Hệ quả pháp lý và điều kiện bãi nhiệm</a><a class="tbtn" href="#nguyen-nhan">Phân loại nguyên nhân</a></div></div>')
for _s in (KL5, KL5S, NNP):
    assert "→" not in _s and "->" not in _s
assert "Cần ít nhất 2/3 dấu hiệu rõ mới xếp vào (3). Hiện chưa khoản nào đạt; F01 và F07 mới có một dấu hiệu rõ là lặp lại cùng kiểu." in open("build_phanloai.py", encoding="utf-8").read()
D["nnl"] = NNL
D["lg"] = dict(st={k: v[0] for k, v in LG.LG_ST.items()}, nd=LG.LG_ND, ladder=[dict(name=x["name"], lines=x["lines"]) for x in LG.LG_LADDER],
               forms=[list(r) for r in LG.LG_FORMS], bai=[[a, b, lab] for a, b, lab, k, nt in LG.LG_BAI], bai_end=LG.LG_BAI_END, note=LG.LG_NOTE)

IMGJ = json.load(open("dash_img.json"))
IMG = dict(logo="data:image/webp;base64," + IMGJ["logo"], logo96="data:image/webp;base64," + IMGJ["logo96"],
           rows="data:image/jpeg;base64," + IMGJ["rows"], acct="data:image/jpeg;base64," + IMGJ["acct"], zoom="data:image/jpeg;base64," + IMGJ["zoom"])

T = viz.DASH
tpl = open("d3/tpl.html").read()
import re as _re
def wrap_sections(t):
    out, pos = [], 0
    for m in _re.finditer(r'<div class="kl-slot" data-no="(\d\d)"></div>', t):
        end_sec = t.index("</section>", m.end())
        out += [t[pos:m.end()], '\n    <button class="sb-t" type="button" aria-expanded="true">Thu gọn mục này</button><div class="sb">', t[m.end():end_sec], "</div>\n  "]
        pos = end_sec
    out.append(t[pos:])
    return "".join(out)
tpl = wrap_sections(tpl)
FM_OUT = [("Schindler", "phí bảo trì, 14 hợp đồng sửa", "806,9 triệu", "o"), ("HNB · sửa cấp nước", "tạm ứng 50% hợp đồng", "623,3 triệu", "o"),
          ("Thép Quang · thiết bị", "chưa rõ hàng hóa", "705,8 triệu", "r"), ("TK vận hành của Ban quản trị", "trái Điều 7.2, 7.4", "986,9 triệu", "r")]
FM_OUT2 = [("Thành Công · nội thất", "4 hợp đồng liên tiếp", "856,8 triệu"), ("Khởi Sáng Việt · giữ xe", "tăng 23% khi quyết toán", "356,4 triệu"), ("KTECH · camera", "", "187,0 triệu"), ("Nộp thuế", "9 lệnh", "187,4 triệu")]
def fm_rows(rows, tone=None):
    return "".join(f'<div class="fm-out tone-{tone or r[3]}"><span><b>{r[0]}</b>' + (f'<small>{r[1]}</small>' if r[1] else "") + f'</span><em>{r[2]}</em></div>' for r in rows)
FLOW_M = ('<div class="flow-m" role="img" aria-label="Sơ đồ dòng tiền ba tài khoản">'
          '<div class="fm-box fm-in"><div class="fm-k">Chủ đầu tư bàn giao 15/08/2024</div><div class="fm-v">124,79 tỷ</div></div><div class="fm-ln ok"></div>'
          '<div class="fm-box fm-fund"><div class="fm-k">QUỸ BẢO TRÌ · VietinBank 116605084999 và Agribank</div><div class="fm-v">127,15 tỷ</div><div class="fm-s">còn ngày 31/05/2026</div>'
          '<div class="fm-pills"><span>125 tỷ tiền gửi có kỳ hạn</span><span>Lãi đã nhận +5,48 tỷ</span></div></div><div class="fm-ln"></div>'
          '<div class="fm-lab">Chi ra khỏi quỹ, 04/2025 – 04/2026</div>' + fm_rows(FM_OUT) +
          '<div class="fm-gap"></div><div class="fm-box fm-ca"><div class="fm-k">Thuê khu vực chung: quảng cáo, mặt bằng, kệ</div><div class="fm-v">1,71 tỷ</div><div class="fm-s fm-law">Luật Nhà ở 2023: lẽ ra phải vào tài khoản quỹ</div></div><div class="fm-ln crit"></div>'
          '<div class="fm-box fm-v7"><div class="fm-k">TK THU DỊCH VỤ 117002997784 · ngoài quỹ bảo trì</div><div class="fm-v">Vào 1,71 tỷ · chi 1,40 tỷ</div><div class="fm-s">260,9 triệu chuyển từ quỹ sang ngày 24/07/2025 · thuế 0,19 tỷ · còn 0,12 tỷ · không qua quy trình của quỹ</div></div><div class="fm-ln"></div>'
          '<div class="fm-lab">Chi từ tài khoản thu dịch vụ</div>' + fm_rows([(a, b, c, "o") for a, b, c in FM_OUT2]) + '</div>')
tpl = tpl.replace("{{FLOW_M}}", FLOW_M)
assert tpl.count("{{Q10}}") == 1
tpl = tpl.replace("{{Q10}}", Q10)
import luudo as LDM
import luudo2 as LD2
D["ldx"] = dict(cases=LD2.CASES)
LDP = ('<div class="h3x" id="luu-do">Đường đi của tiền: năm trường hợp thiếu minh bạch</div><div class="subx">' + _esc(LD2.INTRO) + '</div><div class="ldx" id="ldx"></div><div class="ld-print">'
       + "".join(f'<figure class="ldf"><figcaption><b>{i}</b>{_esc(x["title"])}<span>{_esc(x["code"])}</span></figcaption><div class="ldscroll">{x["svg"]}</div></figure>' for i, x in enumerate(LDM.LD, 1)) + '</div>')
assert tpl.count("{{LD}}") == 1
tpl = tpl.replace("{{LD}}", LDP)
assert tpl.count("{{LEGAL}}") == 1 and tpl.count("{{NFAQ}}") == 1
assert tpl.count("{{KL5}}") == 1 and tpl.count("{{KL5S}}") <= 1 and tpl.count("{{NN}}") == 1  # 20/10/2026: KL5S bỏ khỏi Tổng quan
tpl = tpl.replace("{{KL5}}", KL5).replace("{{KL5S}}", KL5S).replace("{{NN}}", NNP).replace("{{LEGAL}}", LEGAL).replace("{{NFAQ}}", str(len(FAQ["items"])))
tpl = tpl.replace("{{SVG_FLOW}}", viz.svg_flow(T)).replace("{{SVG_MONTHLY}}", viz.svg_monthly(T)).replace("{{SVG_RATES}}", viz.svg_rates(T)) \
         .replace("{{SVG_DONUT}}", viz.svg_donut(Counter(m["st"] for m in MX), T, 210)).replace("{{SVG_INTEREST}}", viz.svg_interest(T))
assert "</script" not in tpl.lower() and "<!--" not in tpl
import xref_data as _XRD
D["xref"] = _XRD.build()
D["clips"] = json.load(open("/home/claude/ssr/video25/web/clips.json")) if os.path.exists("/home/claude/ssr/video25/web/clips.json") else None
css = open("d3/base.css").read() + open("d3/extra.css").read() + open("d3/clip.css").read() + open("d3/ldx.css").read()
assert "</style" not in css.lower()

SKEL_OPEN = ('<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover"><style>'
             ':root{color-scheme:light;box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
             'html{scroll-padding-top:env(safe-area-inset-top,0px)}body{margin:0;padding:0;font:14px -apple-system,BlinkMacSystemFont,sans-serif;background:#faf9f5;color:#141413}'
             'img{max-width:100%}[hidden]:not([hidden=until-found i]){display:none!important}</style></head><body>')
SKEL_OPEN += open("ssr_switch.html", encoding="utf-8").read()  # thanh chuyen hai muc Quy bao tri va Dieu hanh (17/10/2026)
SKEL_CLOSE = "</body></html>"
HEAD_FRAG = ('<title>Sổ quỹ bảo trì SSR</title>\n'
             '<meta name="description" content="Quỹ bảo trì chung cư Nam Sài Gòn Residences có khuất tất hay không: phân tích sao kê ba tài khoản, đối chiếu Quy chế thu chi tài chính, cập nhật được khi có sao kê mới.">\n'
             '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
             '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lexend:wght@400;500;600;700&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&family=IBM+Plex+Mono:wght@400;500;600&family=Cormorant+Garamond:wght@600;700&display=swap">')
ROOT_INIT = '<div id="root"><div class="boot">Đang tải sổ quỹ bảo trì…</div></div>'

if PAGES:
    import segno as _sg, io as _io2
    _q = _sg.make(PAGES_URL, error="m"); _bq = _io2.BytesIO(); _q.save(_bq, kind="svg", scale=4, border=2, dark="#12301F", light="#FFFFFF", xmldecl=False, svgns=True)
    D["clips"]["qr_svg"] = _bq.getvalue().decode(); D["clips"]["url"] = PAGES_URL
    HEAD_FRAG = HEAD_FRAG + '\n<meta name="robots" content="noindex, nofollow">'
def jsstr(s):
    return json.dumps(s, ensure_ascii=False).replace("</", "<\\/")
js = "".join(open(f"d3/{f}").read() for f in ["js1_core.js", "js2_render.js", "js3_upload.js", "js6_clip.js", "js7_ldx.js", "js8_hook.js", "js4_app.js", "js5_xref.js"])
js = js.replace("__SKEL_OPEN__", jsstr(SKEL_OPEN)).replace("__SKEL_CLOSE__", jsstr(SKEL_CLOSE)).replace("__HEAD_FRAG__", jsstr(HEAD_FRAG)).replace("__ROOT_INIT__", jsstr(ROOT_INIT))
APP = "(function(){\n" + js + "\n})();\n"
assert "</script" not in APP.lower() and "<!--" not in APP, "app has forbidden sequence"
# ngon tu dat nghi van, de nghi lam ro (15/10/2026); clip giu nguyen vi loi doc da ghi am
import ngon_tu as NT
tpl = NT.soften(tpl); APP = NT.soften(APP); HEAD_FRAG = NT.soften(HEAD_FRAG)
_clips = D.pop("clips", None); D = NT.walk(D); D["clips"] = _clips
NT.report()

LIGHT = os.environ.get("DASH_LIGHT") == "1" or PAGES
if LIGHT:
    _FD = "/home/claude/ssr/video25/web/f"; os.makedirs(_FD, exist_ok=True)
    _EXT = {"pdf": "pdf", "sum": "pdf", "xlsx": "xlsx", "cv": "docx", "q10png": "png", "q10pdf": "pdf", "pl": "pdf", "hdan": "pdf"}
    _FL = {}
    for _k, _v in FILES.items():
        if _EXT[_k] not in ("pdf", "png"): _FL[_k] = _v; continue
        _name = f"{_k}.{_EXT[_k]}"; open(f"{_FD}/{_name}", "wb").write(base64.b64decode(_v)); _FL[_k] = "f/" + _name
    FILES = _FL
def jtxt(o):
    return json.dumps(o, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
def stag(i, t, body):
    return f'<script id="{i}"' + (f' type="{t}"' if t else "") + ">" + body + "</script>\n"

U = dict(v=1, updatedAt="", batches=[], tracker={}, ai=None)
if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
    U = json.load(open(sys.argv[1]))
frag = (HEAD_FRAG + '\n<style id="css">' + css + "</style>\n" + ROOT_INIT + "\n" + stag("tpl", "text/plain", tpl) + stag("D", "application/json", jtxt(D)) +
        stag("IMG", "application/json", jtxt(IMG)) + stag("FILES", "application/json", jtxt(FILES)) + stag("U", "application/json", jtxt(U)) + stag("app", "", APP))
doc = SKEL_OPEN + "\n" + frag + "\n" + SKEL_CLOSE
# bieu tuong SSR cho tab trinh duyet va man hinh dien thoai (14/10/2026)
_meta_app = '<meta name="theme-color" content="#12301f"><meta name="apple-mobile-web-app-title" content="Sổ quỹ SSR"><meta name="application-name" content="Sổ quỹ SSR">'
if PAGES:
    _ic = ('<link rel="icon" href="favicon.ico" sizes="any"><link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">'
           '<link rel="apple-touch-icon" href="apple-touch-icon.png"><link rel="manifest" href="manifest.webmanifest">' + _meta_app)
else:
    import base64 as _b64i
    _r = lambda f: _b64i.b64encode(open(f"icons/{f}", "rb").read()).decode()
    _ic = ('<link rel="icon" type="image/png" sizes="32x32" href="data:image/png;base64,' + _r("favicon-32.png") + '">'
           '<link rel="apple-touch-icon" href="data:image/png;base64,' + _r("apple-touch-icon.png") + '">' + _meta_app)
doc = doc.replace("</style></head>", "</style>" + _ic + "</head>", 1)
if LIGHT:
    (open("video25/pages/index.html", "w").write(doc) if PAGES else (open("video25/web/so_quy_bao_tri.html", "w").write(frag), open("video25/web/_test_light.html", "w").write(doc)))
else:
    open("d3/dashboard_v3.html", "w").write(frag)
    open("d3/dashboard_v3_standalone.html", "w").write(doc)
open("d3/app.js", "w").write(APP)
print("frag", len(frag.encode()), "doc", len(doc.encode()), "D", len(jtxt(D)), "FILES", sum(len(v) for v in FILES.values()), "tpl", len(tpl), "app", len(APP))
