# -*- coding: utf-8 -*-
"""Nguon duy nhat: ra soat TUNG HOP DONG so voi nguong cua Quy che thu chi (Dieu 9.2, 6.3.b, 6.3.c, 6.3.e).
Dung chung cho bao cao day du, ban tom tat, dashboard, Excel, Hoi dan, Phan loai, cong van, FAQ."""
import json, os
os.chdir("/home/claude/ssr")
_A = json.load(open("analysis.json"))
_TX = [t for t in _A["tx"] if t.get("debit", 0) > 20_000_000]

MUC = 50_000_000      # Dieu 9.2: BQT tu quyet viec khan cap toi da 50 trieu
TRAN = 500_000_000    # Dieu 9.2: tong sua chua dot xuat toi da 500 trieu/nam


def _sum(*needles):
    v = sum(t["debit"] for t in _TX if any(n in t["desc"] for n in needles))
    assert v > 0, needles
    return v


# (ma, doi tac, ten day du, hop dong va ngay ky, nguon, gia tri HD, da tra, cach tra, ngay tu ky toi tra, ghi chu)
HD = [
    ("F05", "HNB", "Công ty TNHH Kỹ thuật Thương mại HNB", "01HNBSSR24032026 ngày 07/04/2026", "Quỹ",
     round(_sum("01HNBSSR24032026") / 0.5), _sum("01HNBSSR24032026"), "Tạm ứng 50% ngày 14/04/2026, 7 ngày sau ký", "sửa hệ thống cấp nước; số hợp đồng mang ngày 24/03/2026"),
    ("F01", "TK vận hành của Ban quản trị", "TK 118002976372 (Kinh phí quản lý vận hành)", "Hoàn ứng 6 khoản 29/08 – 23/12/2025", "Quỹ",
     _sum("HOAN TAM UNG"), _sum("HOAN TAM UNG"), "Một lệnh ngày 23/12/2025 vào tài khoản của chính Ban quản trị", "thang máy, PCCC, máy phát; chưa tách từng việc"),
    ("F03", "Thép Quang", "Công ty TNHH Thương mại Xây dựng Thép Quang", "080426/HDDV/BQT TQ ngày 08/04/2026", "Quỹ",
     _sum("080426"), _sum("080426"), "Trả 100% ngày 24/04/2026, 16 ngày sau ký", "thiết bị khu vực chung, chưa có danh mục"),
    ("F06", "Schindler", "Công ty TNHH Schindler Việt Nam", "EID/FR/18062025REV01 ngày 19/06/2025", "Quỹ",
     round(_sum("18062025REV01") / 0.5), _sum("18062025REV01"), "Tạm ứng 50% ngày 23/06/2025, 4 ngày sau ký", "sửa chữa thang máy"),
    ("F07", "Thành Công", "Công ty TNHH Xây dựng và Trang trí Nội thất Thành Công", "081225/HDDV/BQTTHANH CONG ngày 08/12/2025", "TK 7784",
     _sum("081225/HDDV"), _sum("081225/HDDV"), "Trả 100% ngày 11/12/2025, 3 ngày sau ký", "vật tư, thiết bị sửa phần sở hữu chung"),
    ("F08", "Khởi Sáng Việt", "Công ty CP Thương mại Dịch vụ Khởi Sáng Việt", "18KSVSSR08082025, ghi hai ngày ký 08/08 và 09/08/2025", "TK 7784",
     round(115_720_000 / 0.4), _sum("18KSVSSR08082025"), "Tạm ứng 40%, đã trả tổng cộng vượt 67,1 triệu", "sửa hệ thống giữ xe"),
    ("F07", "Thành Công", "Công ty TNHH Xây dựng và Trang trí Nội thất Thành Công", "06042026/HDDV/BQTTHANHCONG ngày 06/04/2026", "TK 7784",
     _sum("06042026"), _sum("06042026"), "Tạm ứng 60% ngày 14/04/2026, 8 ngày sau ký", "ốp lát sảnh lễ tân"),
    ("F02", "KTECH", "Công ty TNHH Công nghệ mới KTECH", "000785358/KTECH/KT ngày 10/12/2025", "TK 7784",
     _sum("000785358/KTECH"), _sum("000785358/KTECH"), "Tạm ứng 40% ngày 31/12/2025", "sửa, lắp thiết bị hệ thống camera"),
    ("F06", "Schindler", "Công ty TNHH Schindler Việt Nam", "Phí bảo trì 21/10/2024 – 20/01/2025", "Quỹ",
     _sum("PHI BAO TRI GIAI DOAN"), _sum("PHI BAO TRI GIAI DOAN"), "Trả ngày 06/06/2025, trễ 5 – 6 tháng", "bảo trì định kỳ 18 thang"),
    ("F07", "Thành Công", "Công ty TNHH Xây dựng và Trang trí Nội thất Thành Công", "221025/HDDV/BQT TQ ngày 22/10/2025", "TK 7784",
     _sum("221025"), _sum("221025"), "Tạm ứng 50% ngày 23/10/2025, trả nốt 21/11/2025", "nhà để hàng hóa"),
    ("F07", "Thành Công", "Công ty TNHH Xây dựng và Trang trí Nội thất Thành Công", "1509/2025/PHTHTC ngày 15/09/2025", "TK 7784",
     _sum("1509/2025"), _sum("1509/2025"), "Trả 100% ngày 03/10/2025, 18 ngày sau ký", "thiết bị sửa phần sở hữu chung"),
    ("F06", "Schindler", "Công ty TNHH Schindler Việt Nam", "EID/FR/155768282", "Quỹ",
     round(_sum("155768282") / 0.5), _sum("155768282"), "Tạm ứng 50% ngày 29/05/2025", "sửa chữa thang máy"),
    ("F06", "Schindler", "Công ty TNHH Schindler Việt Nam", "EID/FR/155768383", "Quỹ",
     round(_sum("155768383") / 0.5), _sum("155768383"), "Tạm ứng 50% ngày 29/05/2025", "sửa chữa thang máy"),
    ("F06", "Schindler", "Công ty TNHH Schindler Việt Nam", "7 hợp đồng EID/FR, trả gộp 04/04/2025", "Quỹ",
     _sum("155223985"), _sum("155223985"), "Một lệnh cho 7 hợp đồng, bình quân 25,8 triệu mỗi hợp đồng", "mỗi hợp đồng dưới 50 triệu, cộng lại trên"),
    ("F06", "Schindler", "Công ty TNHH Schindler Việt Nam", "4 hợp đồng EID/FR 26/11 – 24/12/2024", "Quỹ",
     _sum("SUA CHUA THANG MAY CAC HOP DONG"), _sum("SUA CHUA THANG MAY CAC HOP DONG"), "Một lệnh ngày 06/06/2025, trễ 5 – 6 tháng", "mỗi hợp đồng dưới 50 triệu, cộng lại trên"),
]
GOP = {"7 hợp đồng EID/FR, trả gộp 04/04/2025": 7, "4 hợp đồng EID/FR 26/11 – 24/12/2024": 4}
ROWS = []
for code, ngan, ten, hd, nguon, gt, tra, cach, ghi in HD:
    n = GOP.get(hd, 1)
    ROWS.append(dict(code=code, short=ngan, name=ten, hd=hd, src=nguon, val=gt, paid=tra, how=cach, note=ghi, n=n,
                     x=gt / MUC, each=gt / n, over=(gt / n) > MUC, cap=gt / TRAN))
ROWS.sort(key=lambda r: -r["val"])

OVER = [r for r in ROWS if r["over"]]                  # tung hop dong vuot 50 trieu
SPLIT = [r for r in ROWS if not r["over"]]             # nhom hop dong nho cong lai tren 50 trieu
N_OVER = len(OVER)
V_OVER = sum(r["val"] for r in OVER)
FULL = [r for r in ROWS if r["how"].startswith("Trả 100%")]
Y25_Q, Y26_Q = 1_793_827_433, 1_329_060_555
Y25_V, Y26_V = 1_094_281_812, 305_917_736
Y25, Y26 = Y25_Q + Y25_V, Y26_Q + Y26_V
APR26 = [r for r in ROWS if r["hd"].endswith(("07/04/2026", "08/04/2026", "06/04/2026"))]
V_APR26 = sum(r["val"] for r in APR26)
assert abs(sum(t["debit"] for t in _TX if "Chi" in t["cat"] or "HOAN TAM UNG" in t["desc"]) - sum(r["paid"] for r in ROWS)) < 2, "phai khop 20 lenh chi"


def tr(v, d=1):
    return f"{v / 1e6:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".") + " triệu"


def ty(v):
    return f"{v / 1e9:.2f}".replace(".", ",") + " tỷ"


def lan(x):
    return f"{x:.1f}".replace(".", ",")


def pct(x):
    return f"{x * 100:.0f}%"


assert N_OVER == 13 and len(SPLIT) == 2, (N_OVER, len(SPLIT))

TITLE = "Từng hợp đồng so với mức 50 triệu và trần 500 triệu"
KICK = ("Điều 9.2 Quy chế thu chi: việc khẩn cấp Ban quản trị chỉ được tự quyết khi tổng chi phí không quá 50 triệu và phải niêm yết giải trình trong 24 giờ; "
        "trên 50 triệu phải có trên 50% chủ sở hữu, người sử dụng đồng ý; tổng sửa chữa đột xuất không quá 500 triệu mỗi năm, vượt thì phải họp Hội nghị nhà chung cư. "
        "Việc không khẩn cấp phải nằm trong kế hoạch bảo trì được Hội nghị thông qua (Điều 6.3.b, 6.3.c). "
        "Tiền ở TK 117002997784 là tiền khu vực chung, theo luật thuộc quỹ bảo trì, nên cùng áp dụng các mức này.")
H = ["Mã", "Đối tác", "Hợp đồng", "Nguồn", "Giá trị", "Gấp mức 50 triệu", "So với trần năm", "Cách trả"]
ND = [f"{N_OVER} khoản chi, mỗi khoản trên 50 triệu, tổng {ty(V_OVER)}, gồm 12 hợp đồng và lệnh hoàn ứng 986,9 triệu; hai nhóm hợp đồng Schindler nhỏ hơn 50 triệu nhưng cộng lại {tr(sum(r['val'] for r in SPLIT))}.",
      "Với mỗi khoản trên 50 triệu, Ban quản trị phải xuất trình được một trong hai văn bản: kế hoạch bảo trì được Hội nghị thông qua có hạng mục đó, hoặc văn bản lấy ý kiến có trên 50% chủ sở hữu đồng ý; hồ sơ hiện chưa có văn bản nào.",
      f"Ba khoản lớn nhất vượt xa mức tự quyết: HNB {tr(ROWS[0]['val'])} gấp khoảng {lan(ROWS[0]['x'])} lần, Thép Quang gấp {lan(OVER[2]['x'])} lần, hợp đồng Schindler {tr(OVER[3]['val'])} gấp {lan(OVER[3]['x'])} lần; riêng HNB bằng {pct(ROWS[0]['cap'])} trần cả năm.",
      f"Ba hợp đồng HNB, Thép Quang, Thành Công ký trong ba ngày 06 – 08/04/2026, tổng {ty(V_APR26)}, gấp hơn bốn lần trần sửa chữa đột xuất của cả năm.",
      f"Kiểu trả trọn một lần như Thép Quang lặp lại ở Thành Công: hợp đồng 081225 trả 100% chỉ 3 ngày sau ký, hợp đồng 1509/2025 trả 100% sau 18 ngày.",
      f"Chi sửa chữa năm 2025 là {ty(Y25)} (quỹ {ty(Y25_Q)}, TK 7784 {ty(Y25_V)}), gấp {lan(Y25 / TRAN)} lần trần; năm tháng đầu 2026 là {ty(Y26)}, gấp {lan(Y26 / TRAN)} lần.",
      "Nếu các khoản này nằm trong kế hoạch được Hội nghị thông qua thì trần 500 triệu không áp dụng; không có kế hoạch và không có ý kiến chủ sở hữu thì mỗi hợp đồng là một lần chi vượt thẩm quyền theo Điều 9.2."]


def cells(r, E=lambda s: s):
    return [r["code"], E(r["short"]), E(r["hd"]), E(r["src"]), tr(r["val"]),
            (lan(r["x"]) + " lần") if r["over"] else "Từng hợp đồng dưới mức",
            pct(r["cap"]), E(r["how"])]


def ng_rows(E):
    out, rc = [], []
    for r in ROWS:
        c = cells(r, E)
        out.append([c[0], f"<b>{c[1]}</b>", c[2], c[3], f"<b>{c[4]}</b>", c[5], c[6], c[7]])
        rc.append("hl-r" if r["over"] and r["x"] >= 10 else ("hl-o" if r["over"] and r["x"] >= 5 else ""))
    return out, rc


def ng_table(E, table):
    rows, rc = ng_rows(E)
    return table(H, rows, cls=["c", "", "", "c", "n", "n", "n", ""], widths=["6%", "12%", "21%", "7%", "12%", "10%", "8%", "24%"],
                 row_cls=rc, esc=False, tcls="ngt",
                 total=["", "Cộng", f"{N_OVER} khoản trên 50 triệu", "", ty(V_OVER), "", "", f"2025: {ty(Y25)}, gấp {lan(Y25 / TRAN)} lần trần; 5 tháng 2026: {ty(Y26)}"])


ND_LABEL = "NHẬN ĐỊNH · THẨM QUYỀN CHI (ĐIỀU 9.2)"


if __name__ == "__main__":
    for r in ROWS: print(cells(r))
    print(N_OVER, ty(V_OVER), ty(Y25), ty(Y26), ty(V_APR26))
    for s in ND: print("-", s)
