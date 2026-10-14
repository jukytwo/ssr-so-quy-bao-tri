# -*- coding: utf-8 -*-
"""Du lieu LIEN KET CHEO cho So quy bao tri (anh Vu 30/09/2026: bam vao bat ky noi dung nao la xem ngay thong tin lien quan).
Moi thuc the: ten, loai, cac cach viet (alias) de nhan dien trong trang, mo ta ngan, dau hieu (F) lien quan, dieu khoan lien quan.
Quan he tinh tu nguon chung content.FINDINGS va content.MATRIX; mo ta viet tay cho doanh nghiep, tai khoan, so tien chinh.
Khong neu ten ca nhan."""
import re
import content as C

ENT = [
 # id, nhan, loai, alias, mo ta
 ("hnb", "HNB", "Doanh nghiệp", ["HNB", "1,25 tỷ", "623,3 triệu", "1.246,6 triệu"],
  "Công ty TNHH Kỹ thuật Thương mại HNB, đơn vị sửa hệ thống cấp nước sinh hoạt. Hợp đồng 01HNBSSR24032026 ghi ký ngày 07/04/2026, khoảng 1,25 tỷ, gấp 25 lần mức Ban quản trị được tự quyết. Đã tạm ứng 623,3 triệu ngày 14/04/2026; còn 623,3 triệu sẽ chi tiếp từ quỹ. Cư dân phản ánh ống nước vẫn bể, dột nhiều nơi."),
 ("tq", "Thép Quang", "Doanh nghiệp", ["Thép Quang", "705,8 triệu"],
  "Nhận 705,8 triệu ngày 24/04/2026, trả đủ một lần 16 ngày sau khi ký hợp đồng ngày 08/04/2026. Gấp 14 lần mức Ban quản trị được tự quyết, bằng 141% trần sửa chữa đột xuất cả năm. Hàng hóa chỉ ghi chung là thiết bị khu vực sử dụng chung; chưa xác minh được mã số thuế."),
 ("sch", "Schindler", "Doanh nghiệp", ["Schindler", "477,1 triệu", "806,9 triệu"],
  "Đơn vị bảo trì, sửa thang máy. Tổng 806,9 triệu gồm phí bảo trì và 14 hợp đồng sửa. Phí bảo trì định kỳ khoảng 57,5 triệu mỗi tháng không còn chi từ quỹ từ 21/01/2025. Hợp đồng lớn nhất 477,1 triệu, gấp 9,5 lần mức tự quyết."),
 ("tc", "Thành Công", "Doanh nghiệp", ["Thành Công", "856,8 triệu", "350,7 triệu"],
  "Nhà thầu nội thất, nhận 856,8 triệu qua 4 hợp đồng, chi từ tài khoản 117002997784 ngoài quy trình của quỹ. Hợp đồng 350,7 triệu trả 100% chỉ 3 ngày sau khi ký; hợp đồng 193,7 triệu ký ngày 06/04/2026."),
 ("ksv", "Khởi Sáng Việt", "Doanh nghiệp", ["Khởi Sáng Việt", "289,3 triệu"],
  "Hệ thống giữ xe, hợp đồng 18KSVSSR08082025. Đã trả 356,4 triệu, cao hơn khoảng 67,1 triệu so với giá trị suy ra từ khoản tạm ứng 40%."),
 ("kt", "KTECH", "Doanh nghiệp", ["KTECH", "187,0 triệu"],
  "Hệ thống camera, 187,0 triệu, chi từ tài khoản 117002997784 ngoài quy trình của quỹ."),
 ("chi", "Chicilon Media", "Doanh nghiệp", ["Chicilon Media", "Chicilon"],
  "Thuê vị trí quảng cáo. Tiền thuê vào tài khoản 117002997784 thay vì tài khoản quỹ. Hợp đồng ký lại ngày 05/01/2025 giảm từ khoảng 86,98 triệu xuống 71,8 triệu mỗi tháng, khoảng 182,2 triệu mỗi năm."),
 ("act", "Viễn thông ACT", "Doanh nghiệp", ["Viễn thông ACT"],
  "Thuê mặt bằng đặt thiết bị viễn thông. Tiền thuê vào tài khoản 117002997784, không vào quỹ."),
 ("ht", "Hưng Thái", "Doanh nghiệp", ["Hưng Thái"],
  "Thuê kệ quảng cáo. Tiền thuê vào tài khoản 117002997784, không vào quỹ."),
 ("vtb", "VietinBank", "Ngân hàng", ["VietinBank", "Vietinbank"],
  "Nơi mở tài khoản quỹ 116605084999, tài khoản vận hành 118002976372, tài khoản thu phí dịch vụ 117002997784 và một phần tiền gửi có kỳ hạn."),
 ("agr", "Agribank", "Ngân hàng", ["Agribank"],
  "Tài khoản quỹ thứ hai 6350201010476, mở ngày 04/07/2024, giữ 60 tỷ tiền gửi. Sổ phụ in ngày 04/09/2026 nhưng chỉ lấy tới 31/05/2026."),
 ("tk999", "TK 116605084999", "Tài khoản", ["116605084999"],
  "Tài khoản quỹ bảo trì tại VietinBank, nơi nhận quỹ từ chủ đầu tư. Luôn còn ít nhất 4,22 tỷ không kỳ hạn."),
 ("tk372", "TK 118002976372", "Tài khoản", ["118002976372"],
  "Tài khoản kinh phí quản lý vận hành tại VietinBank, mở ngày 04/07/2024, 6 thành viên Ban quản trị là đồng chủ tài khoản; Quy chế Điều 3.2.a giao Công ty quản lý đứng tên. Nhận 986,9 triệu từ quỹ ngày 23/12/2025. Chưa có sao kê."),
 ("tk784", "TK 117002997784", "Tài khoản", ["117002997784", "TK 7784"],
  "Tài khoản thu phí dịch vụ do Ban quản trị đứng tên. Nhận 1,71 tỷ tiền khai thác khu vực chung lẽ ra phải vào quỹ; đã chi 1,40 tỷ cho Thành Công, Khởi Sáng Việt, KTECH; còn 120,3 triệu ngày 31/05/2026."),
 ("tk476", "TK 6350201010476", "Tài khoản", ["6350201010476"],
  "Tài khoản quỹ thứ hai tại Agribank, mở ngày 04/07/2024 trước khi nhận quỹ; ngày 21/08/2024 nhận 60 tỷ và gửi có kỳ hạn 12 tháng."),
 ("a9869", "986,9 triệu", "Số tiền", ["986,9 triệu", "986.910.176"],
  "Ngày 23/12/2025 quỹ chuyển 986,9 triệu sang TK vận hành 118002976372 để hoàn ứng 6 khoản chi từ 29/08 tới 23/12/2025. Trái Điều 3.2.a, 7.2, 7.4 Quy chế. Vi phạm đã rõ; chưa có sao kê tài khoản nhận."),
 ("a171", "1,71 tỷ", "Số tiền", ["1,71 tỷ"],
  "Tiền khai thác khu vực chung của Chicilon Media, Hưng Thái, Viễn thông ACT vào TK 117002997784, không vào quỹ như khoản 4 Điều 153 Luật Nhà ở 2023. Vi phạm đã rõ."),
 ("a140", "1,40 tỷ", "Số tiền", ["1,40 tỷ"],
  "Chi từ TK 117002997784 cho Thành Công, Khởi Sáng Việt, KTECH, không qua kế hoạch bảo trì, báo giá, nghiệm thu của quỹ."),
 ("a504", "5,04 tỷ", "Số tiền", ["5,04 tỷ", "13 khoản"],
  "Tổng 13 khoản chi trên mức 50 triệu Ban quản trị được tự quyết, chưa thấy văn bản cho phép của chủ sở hữu (Điều 9.2). Lớn nhất: HNB 1,25 tỷ, hoàn ứng 986,9 triệu, Thép Quang 705,8 triệu, Schindler 477,1 triệu."),
 ("a1275", "127,5 tỷ", "Số tiền", ["127,5 tỷ"],
  "Tiền gửi có kỳ hạn sau đợt tái tục tháng 8/2026, lãi 8% một năm; chưa có hợp đồng và giấy xác nhận của ngân hàng."),
 ("a169", "1,69 tỷ", "Số tiền", ["1,69 tỷ"],
  "Phần chưa truy được tới cùng: 986,9 triệu chưa có sao kê tài khoản nhận và 705,8 triệu trả Thép Quang chưa có danh mục hàng hóa."),
 ("a269", "2,69 tỷ", "Số tiền", ["2,69 tỷ"],
  "Tổng đã đi sai tài khoản: 986,9 triệu rời quỹ và 1,71 tỷ lẽ ra phải vào quỹ, khoảng 2,1% số dư quỹ."),
 ("a1231", "123,1 triệu", "Số tiền", ["123,1 triệu", "863,8 triệu"],
  "Chênh lệch giữa khoản hoàn ứng 986,9 triệu và bảng chi phí 863,8 triệu trong Báo cáo 03-2026/BC-BQTSSR ngày 15/05/2026."),
 ("a215", "2,15 tỷ", "Số tiền", ["2,15 tỷ"],
  "Ba hợp đồng HNB, Thép Quang, Thành Công ký trong ba ngày 06 tới 08/04/2026, gấp hơn 4 lần trần sửa chữa đột xuất 500 triệu của cả năm."),
 ("a12715", "127,15 tỷ", "Số tiền", ["127,15 tỷ"],
  "Số dư tiền gốc của quỹ ngày 31/05/2026. Tiền gốc không giảm; không có lệnh rút tiền mặt hay chuyển cho cá nhân."),
]


MANF = {"a504": ["F01", "F03", "F05", "F06", "F07", "F08"], "a169": ["F01", "F03"], "a269": ["F01", "F02"], "a1275": ["F04", "F16"],
        "a215": ["F03", "F05", "F07", "F15"], "a140": ["F02", "F07"], "a171": ["F02", "F09"], "a1231": ["F01"]}


def _fx(f):
    return " ".join(str(f.get(k, "")) for k in ("title", "evidence", "rule", "view", "ask"))


def _has(txt, al):
    return any(re.search(r"(?<![\w])" + re.escape(a) + r"(?![\w])", txt) for a in al)


def build():
    X = {}
    for fid, lab, typ, al, desc in ENT:
        X[fid] = dict(l=lab, t=typ, a=al, d=desc)
    # dieu khoan Quy che tu bang doi chieu; mot dong co the neu nhieu dieu ("Điều 6.1.b, 6.3.c"): tach va gop
    for m in C.MATRIX:
        d = m["dieu"]
        nums = re.findall(r"\d+(?:\.\d+)+(?:\.[a-z])?|(?<=Điều )\d+", d)
        codes = [c.strip() for c in m["codes"].split(",") if c.strip()]
        for num in nums:
            key = "d" + num.replace(".", "_")
            line = f"{m['req']}. Thực tế: {m['fact']} Đánh giá: {m['st']}."
            if key in X:
                X[key]["d"] += " " + line; X[key]["codes"] = sorted(set(X[key]["codes"]) | set(codes))
            else:
                al = ["Điều " + num] + (["Điều 153", "khoản 4 Điều 153"] if num == "11" else [])
                X[key] = dict(l="Điều " + num + (" và khoản 4 Điều 153 Luật Nhà ở 2023" if num == "11" else ""), t="Điều khoản", a=al, d=line, codes=codes, st=m["st"])
    # dau hieu F
    for f in C.FINDINGS:
        X[f["id"]] = dict(l=f["id"], t="Dấu hiệu", a=[f["id"]], d=f["view"], title=f["title"], sev=f["sev"], amt=f.get("amount") or 0, ask=f["ask"], rule=f["rule"])
    # quan he: thuc the voi dau hieu (tim alias trong van ban dau hieu), dieu khoan voi dau hieu
    for k, v in X.items():
        if v["t"] == "Dấu hiệu": continue
        fs = set(v.get("codes", []))
        if v["t"] != "Điều khoản":
            fs |= {f["id"] for f in C.FINDINGS if _has(_fx(f), v["a"])}
        else:
            num = v["a"][0].replace("Điều ", "")
            fs |= {f["id"] for f in C.FINDINGS if re.search(r"(?<![\d.])" + re.escape(num) + r"(?![\d])", f["rule"])}
        v["f"] = sorted(fs | set(MANF.get(k, [])))
    # dieu khoan cua moi dau hieu, thuc the cua moi dau hieu
    for f in C.FINDINGS:
        X[f["id"]]["f"] = []
        X[f["id"]]["rel"] = [k for k, v in X.items() if v["t"] not in ("Dấu hiệu",) and f["id"] in v.get("f", [])]
    for k, v in X.items():
        if v["t"] == "Dấu hiệu": continue
        rel = set()
        for fid in v["f"]: rel |= set(X[fid]["rel"])
        rel.discard(k); v["rel"] = sorted(rel, key=lambda z: ["Doanh nghiệp", "Tài khoản", "Số tiền", "Điều khoản", "Ngân hàng"].index(X[z]["t"]) if X[z]["t"] in ["Doanh nghiệp", "Tài khoản", "Số tiền", "Điều khoản", "Ngân hàng"] else 9)
    return X


if __name__ == "__main__":
    X = build()
    for k in ("hnb", "tk372", "d7_4", "F01", "a504"):
        v = X.get(k); print(k, v and (v["l"], v["a"], v.get("f"), v.get("rel")[:8]))
    print(len(X), sorted(k for k in X if k.startswith("d")))
