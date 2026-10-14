# -*- coding: utf-8 -*-
"""Khoi HIEU DUNG VAN DE (bon tang): mot nguon chu duy nhat cho bao cao day du, ban tom tat, anh trong tam, dashboard,
cong van, Excel va clip. Sua o day roi dung lai tat ca san pham."""

KM = dict(
    label="HIỂU ĐÚNG VẤN ĐỀ",
    sub="Tiền có mất không, sai ở đâu, thiệt ở đâu",
    head="Tiền không biến mất trên sao kê, nhưng quỹ bị điều hành trái quy định, sinh lời kém, và 1,69 tỷ còn phải có chứng từ mới khẳng định được là không mất.",
    tiers=[
        dict(k="ok", tag="Đã kiểm chứng", t="Trên sao kê, tiền không biến mất",
             d=["198 giao dịch của ba tài khoản khớp số dư tới từng đồng.",
                "Không có rút tiền mặt, không có khoản chuyển cho cá nhân; tiền gốc quỹ vẫn tăng nhờ lãi."],
             v="198", vl="giao dịch khớp từng đồng"),
        dict(k="vp", tag="Chắc chắn", t="Làm trái quy định và thiếu minh bạch",
             d=["986,9 triệu tiền quỹ đi qua tài khoản vận hành của Ban quản trị, 1,71 tỷ tiền khu vực chung nằm ngoài quỹ, 1,40 tỷ chi không qua quy trình của quỹ.",
                "Chuyển về đúng sổ thì tổng tiền không đổi, nhưng không xóa được vi phạm."],
             v="3", vl="vi phạm rõ trên sao kê"),
        dict(k="ct", tag="Hiệu quả thấp", t="Quỹ sinh lời kém hơn mức có thể",
             d=["Cách gửi tiền làm quỹ bỏ lỡ 0,42 – 0,96 tỷ tiền lãi; hợp đồng quảng cáo ký lại thu ít hơn khoảng 182,2 triệu mỗi năm.",
                "Đây là thiệt hại cơ hội, tiền gốc không mất."],
             v="0,96 tỷ", vl="lãi bỏ lỡ, mức cao nhất"),
        dict(k="hs", tag="Cần chứng từ", t="1,69 tỷ có thể thành thất thoát thật",
             d=["986,9 triệu vào tài khoản không có sao kê và chưa có biên bản nghiệm thu; 705,8 triệu trả Thép Quang chưa có danh mục hàng hóa.",
                "Không có chứng từ thì đây là tiền phải hoàn lại quỹ; hợp đồng không qua báo giá cũng gây thiệt nếu giá cao hơn thị trường."],
             v="1,69 tỷ", vl="chờ chứng từ"),
    ],
    end="Kết luận: chưa có bằng chứng tiền bị chiếm đoạt, nhưng chưa thể khẳng định không mất; kết luận cuối cùng phụ thuộc chứng từ của 1,69 tỷ.",
)

# he qua phap ly cua tung tang: mot nguon o legal.py
from legal import KM_HQ as _KMHQ
for _t in KM["tiers"]:
    _t["hq"], _t["hq_s"] = _KMHQ[_t["k"]]

# mau theo nghia: xanh = da kiem chung, do = lam trai quy dinh, vang = hieu qua thap, cam = can chung tu
KM_COLOR = {"ok": ("#1E7A46", "#E6F2EA"), "vp": ("#A93434", "#F8E3E3"), "ct": ("#9A7B12", "#FBF3D9"), "hs": ("#C55A11", "#FCE9DC")}


def km_lines():
    """Dang dong (moi cau mot dong) de chep nguyen van sang ban tom tat va cac noi can van ban thuan."""
    out = [KM["head"]]
    for t in KM["tiers"]:
        out.append(f"{t['tag']}: {t['t']}. " + " ".join(t["d"]) + " Hệ quả: " + t["hq"])
    out.append(KM["end"])
    return out


KM_CSS = """
.kmb{background:#16294A;color:#fff;border-radius:6pt;padding:8pt 10pt 9pt 10pt;break-inside:avoid;}
.kmb .kmh{display:flex;align-items:baseline;gap:8pt;flex-wrap:wrap;}
.kmb .kmh .lab{font-family:'Be Vietnam Pro',sans-serif;font-size:8.6pt;font-weight:800;letter-spacing:.12em;color:#f1d98f;}
.kmb .kmh .sub{font-family:'Be Vietnam Pro',sans-serif;font-size:8.2pt;color:#c9d3e6;font-weight:600;}
.kmb .kmhead{font-size:10pt;font-weight:700;line-height:1.4;margin-top:3pt;text-align:left;}
.kmb .kmt{display:grid;gap:3.2pt;margin-top:5pt;}
.kmb .kmr{display:grid;grid-template-columns:29mm 1fr;gap:8pt;background:#fff;color:#1a1a1a;border-radius:4pt;border-left:4pt solid var(--c);padding:4.5pt 8pt 4.5pt 7pt;align-items:center;}
.kmb .kmr .kmg{display:inline-block;font-family:'Be Vietnam Pro',sans-serif;font-size:6.9pt;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--c);background:var(--t);border-radius:6pt;padding:1pt 5pt;white-space:nowrap;}
.kmb .kmr .kmv{font-family:'Be Vietnam Pro',sans-serif;font-size:15pt;font-weight:800;color:var(--c);line-height:1.05;margin-top:3pt;white-space:nowrap;}
.kmb .kmr .kmvl{font-family:'Be Vietnam Pro',sans-serif;font-size:7pt;color:#5b6474;line-height:1.25;margin-top:1pt;}
.kmb .kmr .kmc b{display:block;font-family:'Be Vietnam Pro',sans-serif;font-size:9.3pt;font-weight:800;color:#16294A;line-height:1.3;}
.kmb .kmr .kmc p{font-size:8.7pt;line-height:1.36;margin:1pt 0 0 0;text-align:left;}
.kmb .kmr .kmc p.kmq{font-size:8.4pt;font-weight:700;color:var(--c);margin-top:2.5pt;line-height:1.34;}
.kmb .kmr .kmc p.kmq span{display:inline-block;font-family:'Be Vietnam Pro',sans-serif;font-size:6.6pt;font-weight:800;letter-spacing:.06em;color:#fff;background:var(--c);border-radius:5pt;padding:0.6pt 4.5pt;margin-right:4pt;vertical-align:1pt;}
.kmb .kme{margin-top:6pt;font-size:9.5pt;font-weight:700;line-height:1.4;color:#fff;border-left:3pt solid #C8992F;padding-left:7pt;text-align:left;}
"""


KSTRIP_CSS = """
.kstrip { display:grid; grid-template-columns: 1.2fr 1fr 1fr 1fr 1fr; gap:5pt; }
.kstrip .ks { border:0.8pt solid #cfd8e6; border-top:3pt solid #1F3864; border-radius:0 0 5pt 5pt; padding:5pt 7pt 6pt 7pt; background:#fff; }
.kstrip .ks.main { background:#1F3864; border-color:#1F3864; color:#fff; }
.kstrip .ks.g { border-top-color:#1E7A46; } .kstrip .ks.r { border-top-color:#A93434; } .kstrip .ks.o { border-top-color:#C55A11; }
.kstrip .k { font-family:'Be Vietnam Pro',sans-serif; font-size:7.2pt; font-weight:700; color:#3d4656; line-height:1.25; }
.kstrip .ks.main .k { color:#f1d98f; }
.kstrip .v { font-family:'Be Vietnam Pro',sans-serif; font-size:17pt; font-weight:800; color:#16294A; line-height:1.05; margin-top:3pt; }
.kstrip .ks.main .v { color:#fff; font-size:19pt; } .kstrip .ks.g .v { color:#1E7A46; } .kstrip .ks.r .v { color:#A93434; } .kstrip .ks.o .v { color:#C55A11; }
.kstrip .v small { font-size:8.5pt; font-weight:600; margin-left:2pt; }
.kstrip .s { font-family:'Be Vietnam Pro',sans-serif; font-size:7pt; color:#5b6474; line-height:1.3; margin-top:2pt; }
.kstrip .ks.main .s { color:#dbe3f2; }
"""


def kstrip_html(A, ty):
    """Dai 5 con so o bia (ban day du, ban tom tat)."""
    return ('<div class="kstrip">'
            f'<div class="ks main"><div class="k">Quỹ còn ngày 31/05/2026</div><div class="v">{ty(A["fund_end"])}<small>tỷ</small></div><div class="s">98% là tiền gửi có kỳ hạn</div></div>'
            f'<div class="ks"><div class="k">Nhận bàn giao 15/08/2024</div><div class="v">{ty(A["fund_in"])}<small>tỷ</small></div><div class="s">Hai lệnh chuyển của chủ đầu tư</div></div>'
            f'<div class="ks g"><div class="k">Lãi đã nhận</div><div class="v">{ty(A["int_td"] + A["int_dda"])}<small>tỷ</small></div><div class="s">Đúng biểu từng thời điểm</div></div>'
            f'<div class="ks r"><div class="k">Đã chi khỏi quỹ</div><div class="v">{ty(A["spend"])}<small>tỷ</small></div><div class="s">1,69 tỷ chờ chứng từ</div></div>'
            f'<div class="ks o"><div class="k">Thu khu vực chung ngoài quỹ</div><div class="v">{ty(A["ca_total"])}<small>tỷ</small></div><div class="s">Đã chi {ty(A["repair7784"])} tỷ ngoài quy trình</div></div>'
            '</div>')


def km_html(esc, cls="kmb"):
    """Khoi HTML dung chung cho bao cao day du, ban tom tat va anh A4 (cung chu, cung mau)."""
    rows = ""
    for t in KM["tiers"]:
        c, tint = KM_COLOR[t["k"]]
        ps = "".join(f"<p>{esc(x)}</p>" for x in t["d"]) + f'<p class="kmq"><span>HỆ QUẢ</span>{esc(t["hq"])}</p>'
        rows += (f'<div class="kmr" style="--c:{c};--t:{tint}"><div class="kml"><span class="kmg">{esc(t["tag"])}</span>'
                 f'<div class="kmv">{esc(t["v"])}</div><div class="kmvl">{esc(t["vl"])}</div></div>'
                 f'<div class="kmc"><b>{esc(t["t"])}</b>{ps}</div></div>')
    return (f'<div class="{cls}"><div class="kmh"><span class="lab">{esc(KM["label"])}</span><span class="sub">{esc(KM["sub"])}</span></div>'
            f'<div class="kmhead">{esc(KM["head"])}</div><div class="kmt">{rows}</div><div class="kme">{esc(KM["end"])}</div></div>')


KMC_CSS = """
.kmcx{background:#16294A;color:#fff;border-radius:6pt;padding:7pt 9pt 8pt 9pt;break-inside:avoid;font-family:'Be Vietnam Pro',sans-serif;}
.kmcx .kx-h{display:flex;align-items:baseline;gap:8pt;flex-wrap:wrap;}
.kmcx .kx-lab{font-size:8.4pt;font-weight:800;letter-spacing:.12em;color:#f1d98f;}
.kmcx .kx-sub{font-size:8pt;color:#c9d3e6;font-weight:600;}
.kmcx .kx-head{font-size:9.6pt;font-weight:700;line-height:1.4;margin-top:3pt;}
.kmcx .kx-g{display:grid;grid-template-columns:repeat(4,1fr);gap:5pt;margin-top:6pt;}
.kmcx .kx-c{background:#fff;color:#1a1a1a;border-radius:4pt;border-top:3.5pt solid var(--c);padding:5pt 7pt 6pt 7pt;}
.kmcx .kx-tg{display:inline-block;font-size:6.8pt;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--c);background:var(--t);border-radius:6pt;padding:1pt 5pt;white-space:nowrap;}
.kmcx .kx-v{font-size:15pt;font-weight:800;color:var(--c);line-height:1.05;margin-top:3pt;white-space:nowrap;}
.kmcx .kx-vl{font-size:6.9pt;color:#5b6474;line-height:1.25;margin-top:1pt;}
.kmcx .kx-t{font-size:8.3pt;font-weight:700;color:#16294A;line-height:1.3;margin-top:3pt;}
.kmcx .kx-q{font-size:7pt;font-weight:700;color:var(--c);line-height:1.3;margin-top:3pt;border-top:0.6pt dashed var(--c);padding-top:2.5pt;}
.kmcx .kx-e{margin-top:6pt;font-size:8.8pt;font-weight:700;line-height:1.4;border-left:3pt solid #C8992F;padding-left:7pt;}
"""


def km_compact_html(esc, cls="kmcx", hq=False):
    """Ban gon cua khoi HIEU DUNG VAN DE (cau chinh, bon o, ket luan) cho file phu va anh thong bao; cung chu, cung mau."""
    cells = ""
    for t in KM["tiers"]:
        c, tint = KM_COLOR[t["k"]]
        cells += (f'<div class="kx-c" style="--c:{c};--t:{tint}"><span class="kx-tg">{esc(t["tag"])}</span>'
                  f'<div class="kx-v">{esc(t["v"])}</div><div class="kx-vl">{esc(t["vl"])}</div><div class="kx-t">{esc(t["t"])}</div>'
                  + (f'<div class="kx-q">Hệ quả: {esc(t["hq_s"])}</div>' if hq else "") + '</div>')
    return (f'<div class="{cls}"><div class="kx-h"><span class="kx-lab">{esc(KM["label"])}</span><span class="kx-sub">{esc(KM["sub"])}</span></div>'
            f'<div class="kx-head">{esc(KM["head"])}</div><div class="kx-g">{cells}</div><div class="kx-e">{esc(KM["end"])}</div></div>')


def _check():
    import re
    txt = " ".join([KM["head"], KM["end"]] + [" ".join([t["t"]] + t["d"]) for t in KM["tiers"]])
    assert "→" not in txt and "->" not in txt
    for need in ("198", "986,9 triệu", "1,71 tỷ", "1,40 tỷ", "0,42 – 0,96 tỷ", "182,2 triệu", "705,8 triệu", "1,69 tỷ", "0,96 tỷ"):
        assert need in txt, need
    # 1,69 ty = 986,9 trieu + 705,8 trieu
    assert round((986_910_176 + 705_769_875) / 1e9, 2) == 1.69


_check()
