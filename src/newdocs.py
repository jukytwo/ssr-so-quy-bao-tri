# -*- coding: utf-8 -*-
"""Du lieu dung chung cho dashboard, bao cao day du va ban tom tat: Neu hach toan dung, doi chieu tam ung voi quyet toan,
tai lieu BQT cung cap ngay 28/09/2026 (danh sach, 13 chi tieu doi chieu, nhan dinh, cau hoi moi), hop dong tien gui sau tai tuc."""
import json, os
os.chdir("/home/claude/ssr")
A = json.load(open("analysis.json"))
def vnd(n): return f"{round(n):,}".replace(",", ".")
# ---- Neu hach toan dung + doi chieu hop dong (cung so lieu voi Excel va ban tom tat)
import re as _re
SG = A["spend_groups"]; KVC = sum(A["inc7784"].values()); TAX = A["exp7784"]["Nộp thuế"]
NET7 = A["int7784"] - A["exp7784"]["Phí ngân hàng"]; PAY = A["spend"] + A["repair7784"]
RQ = A["fund_in"] + 1_000_000 + A["int_td"] + A["int_dda"] + KVC - TAX + NET7 - PAY - A["fees"]
assert round(RQ) == round(A["fund_end"] + A["end_v"])
MF = 172_616_400
HT_ITEMS = [dict(l="Schindler: sửa chữa thang máy (14 hợp đồng EID/FR, 3 hợp đồng tạm ứng 50%)", v=SG["Chi thang máy – Schindler"]["total"] - MF, src="Quỹ", code="F06"),
            dict(l="Schindler: phí bảo trì định kỳ 21/10/2024 – 20/01/2025", v=MF, src="Quỹ", code="F14"),
            dict(l="Chuyển sang TK vận hành 118002976372 (hoàn ứng 6 khoản chi bảo trì)", v=SG["Chuyển KPBT sang TK vận hành của BQT"]["total"], src="Quỹ", code="F01"),
            dict(l="Thuế nộp trên tiền khu vực chung", v=TAX, src="TK 7784", code=""),
            dict(l="HNB: tạm ứng 50% hợp đồng sửa hệ thống cấp nước", v=SG["Chi sửa chữa cấp nước – HNB"]["total"], src="Quỹ", code="F05"),
            dict(l="Thép Quang: mua thiết bị, trả một lần", v=SG["Chi mua thiết bị – Thép Quang"]["total"], src="Quỹ", code="F03"),
            dict(l="Thành Công: 4 hợp đồng sửa chữa, mua sắm, ốp lát", v=A["exp7784"]["Chi sửa chữa, mua sắm – Thành Công"], src="TK 7784", code="F07"),
            dict(l="Khởi Sáng Việt: hệ thống giữ xe (trả vượt 67,1 triệu)", v=A["exp7784"]["Chi hệ thống giữ xe – Khởi Sáng Việt"], src="TK 7784", code="F08"),
            dict(l="KTECH: hệ thống camera", v=A["exp7784"]["Chi hệ thống camera – KTECH"], src="TK 7784", code="F02")]
HT_TOT = sum(x["v"] for x in HT_ITEMS); assert HT_TOT == PAY + TAX
HT = dict(items=HT_ITEMS, fund_now=A["fund_end"], fund_right=RQ, move=A["end_v"], kvc=KVC, tax=TAX, pay=PAY,
          presets=dict(cudan=["ok", "ok", "ok", "ok", "w", "w", "w", "w", "w"], all=["ok"] * 9, strict=["ok", "w", "w", "ok", "w", "w", "w", "w", "w"]),
          nd=["Nếu hạch toán đúng, quỹ bảo trì ngày 31/05/2026 phải là 127,27 tỷ đồng, cao hơn số đang thể hiện 120,3 triệu vì số dư TK 7784 là tiền khu vực chung chưa nộp về quỹ.",
              "Đưa về đúng tài khoản không làm mất hay thêm tiền; chỉ chuyển 1,71 tỷ thu khu vực chung, 187,4 triệu tiền thuế và 1,40 tỷ chi sửa chữa từ TK 7784 về đúng sổ của quỹ.",
              "Theo kịch bản cư dân nêu, vẫn còn 2,73 tỷ phải có hồ sơ: Thép Quang 705,8 triệu, HNB 623,3 triệu và 1,40 tỷ chi từ TK 7784 cho Thành Công, Khởi Sáng Việt, KTECH.",
              "Ngay cả khi mọi khoản chi đều hợp lệ, ba chỗ làm sai quy trình vẫn còn: tiền quỹ đi qua tài khoản vận hành của BQT, tiền khu vực chung nằm ngoài quỹ và chi sửa chữa không qua quy trình của quỹ.",
              "Khoản nào không đủ chứng từ là số BQT phải hoàn lại quỹ; theo kịch bản chặt nhất, phần phải làm rõ tới 3,89 tỷ đồng."])
TXD = [t for t in A["tx"] if t["debit"] and t["cat"] != "Phí ngân hàng"]
HD = []
for code, who in [("18KSVSSR08082025", "Khởi Sáng Việt · giữ xe"), ("000785358/KTECH", "KTECH · camera"), ("221025", "Thành Công · nhà để hàng"),
                  ("06042026", "Thành Công · ốp lát sảnh"), ("01HNBSSR24032026", "HNB · cấp nước"), ("EID/FR/155768383", "Schindler · thang máy"),
                  ("EID/FR/155768282", "Schindler · thang máy"), ("EID/FR/18062025REV01", "Schindler · thang máy"), ("080426", "Thép Quang · thiết bị")]:
    ps = [t for t in TXD if code in t["desc"]]; tot = sum(t["debit"] for t in ps)
    adv = [t for t in ps if "TAM UNG" in t["desc"] and "HOAN TAM UNG" not in t["desc"]]
    if adv:
        pc = int(_re.search(r"TAM UNG (\d\d)", adv[0]["desc"]).group(1)); val = adv[0]["debit"] * 100 / pc; diff = tot - val
        st = "ok" if abs(diff) <= 1000 else ("over" if diff > 0 else "open")
        res = {"ok": "Khớp, đã trả đủ", "over": f"Trả vượt {vnd(diff)} đồng ({str(round(diff / val * 100, 1)).replace('.', ',')}%)", "open": f"Còn {vnd(-diff)} đồng chưa thấy trả"}[st]
        HD.append(dict(code=code, who=who, adv=f"{pc}% · {vnd(adv[0]['debit'])}", val=round(val), paid=tot, st=st, res=res))
    else:
        HD.append(dict(code=code, who=who, adv="Không tạm ứng", val=tot, paid=tot, st="once", res="Trả một lần 100%, không qua nghiệm thu từng đợt"))
HD_ND = ["Hợp đồng giữ xe 18KSVSSR08082025 là trường hợp duy nhất trả vượt: tạm ứng 40% là 115,7 triệu nên giá trị hợp đồng khoảng 289,3 triệu, nhưng tổng đã trả 356,4 triệu, cao hơn 67,1 triệu (23,2%).",
         "Hợp đồng camera của KTECH và hai hợp đồng có tạm ứng của Thành Công đều quyết toán khớp giá trị suy ra (lệch dưới 100 đồng do làm tròn), cho thấy cách suy từ tỷ lệ tạm ứng là đáng tin.",
         "Phần 50% còn lại của hợp đồng cấp nước HNB (623,3 triệu) và của ba hợp đồng Schindler (298,8 triệu) chưa thấy trả trên sao kê tới 31/05/2026; nếu phần Schindler đã trả qua tài khoản vận hành thì phải nằm trong 986,9 triệu hoàn ứng.",
         "Khoản 705,8 triệu của Thép Quang được trả một lần 100%, không có đợt tạm ứng và nghiệm thu như các hợp đồng khác.",
         "Phần vượt 67,1 triệu chỉ hợp lệ khi có phụ lục phát sinh ký trước khi thi công và biên bản quyết toán; nội dung này đã được đưa vào văn bản kiến nghị gửi Ban quản trị."]
# ---- tai lieu BQT cung cap ngay 28/09/2026
import datetime as _dt
_q, _a = dict(A["series"]["q"]), dict(A["series"]["a"])
def _at(sr, d): ks = sorted(k for k in sr if k <= d); return sr[ks[-1]]
_P = lambda s_: _dt.datetime.strptime(s_, "%d/%m/%Y")
_QQ = [t for t in A["tx"] if t["key"].startswith("Q") and _P(t["date"]) <= _dt.datetime(2025, 5, 20)]
_INT = sum(t["credit"] for t in A["tx"] if t["key"].startswith("Q") and t["cat"].startswith("Lãi") and _dt.datetime(2024, 8, 21) <= _P(t["date"]) <= _dt.datetime(2025, 5, 12))
_SCH = sum(t["debit"] for t in A["tx"] if "Schindler" in t["cat"] and _P(t["date"]) <= _dt.datetime(2025, 5, 12))
_PAY26 = sum(t["debit"] for t in A["tx"] if t["cat"] in ("Chi sửa chữa cấp nước – HNB", "Chi mua thiết bị – Thép Quang", "Chi sửa chữa, mua sắm – Thành Công", "Chi hệ thống camera – KTECH")
             and _dt.datetime(2026, 1, 1) <= _P(t["date"]) <= _dt.datetime(2026, 5, 15))
DOCS = dict(list=[
  dict(t="Thư xác nhận mở tài khoản 118002976372", d="22/07/2024", who="VietinBank CN Sài Gòn", req="số 2, số 11",
       c="Tên tài khoản: BQT nhà chung cư Nam Sài Gòn Residences - Kinh phí quản lý vận hành; mở ngày 04/07/2024; 6 thành viên BQT đồng chủ tài khoản.",
       e="Xác nhận tài khoản vận hành do BQT đứng tên (Quy chế Điều 3.2.a quy định công ty quản lý đứng tên). Không có giao dịch nên chưa truy được 986,9 triệu."),
  dict(t="Giấy xác nhận số dư tại 24:00 ngày 20/05/2025", d="21/05/2025", who="VietinBank CN Sài Gòn", req="số 1",
       c="TK 116605084999: 4.843.654.006 đồng; HĐTG 912/2024/70677 15 tỷ (3 tháng); HĐTG 912/2024/70435 45 tỷ (12 tháng).",
       e="Khớp sao kê; xác nhận 60 tỷ gửi tại VietinBank ở thời điểm 20/05/2025."),
  dict(t="Sao kê TK 116605084999 từ 01/07/2024 tới 20/05/2025", d="2025", who="VietinBank CN Sài Gòn", req="",
       c="36 giao dịch; tổng Nợ 120.181.083.438; tổng Có 125.024.737.444; cột đối ứng ghi rõ 60 tỷ chuyển sang TK Agribank 6350201010476.",
       e="Khớp tuyệt đối với dữ liệu của trang này."),
  dict(t="Thư xác nhận số dư tài khoản ngày 20/05/2025", d="20/05/2025", who="Agribank CN Đông TP.HCM", req="số 1",
       c="TK 6350201010476 (Kinh phí bảo trì): 417.400 đồng; HĐTG 6350633000355: 60 tỷ.",
       e="Khớp sao kê; xác nhận 60 tỷ gửi tại Agribank ở thời điểm 20/05/2025."),
  dict(t="Báo cáo kinh phí bảo trì số 01-2025/BC-BQTSSR", d="14/05/2025", who="BQT", req="công khai (F12)",
       c="Số dư 12/05/2025: HĐTG 120 tỷ (45 tỷ 4,7%; 15 tỷ 2,0%; 60 tỷ 4,7%); TK thanh toán 4.770.503.321; bảng thu chi: thang máy 181.083.438, phí 247.500, lãi 161.699.196.",
       e="Số dư trang 1 khớp sao kê; bảng thu chi tính phí ngân hàng hai lần nên lệch 247.500."),
  dict(t="Báo cáo kinh phí bảo trì số 03-2026/BC-BQTSSR", d="15/05/2026", who="BQT", req="công khai (F12); số 3, 4, 6, 7",
       c="Quỹ 127.054.769.278: HĐTG 125 tỷ (45 tỷ 4,7%; 5 tỷ 4,7%; 15 tỷ 2,4%; 60 tỷ 4,7%), TK thanh toán 2.054.769.278; Phụ lục chi phí 2.421.327.773.",
       e="Số dư khớp sao kê; chưa tính TK Agribank và TK 7784; 863,8 triệu chi thang máy, PCCC, máy phát không thấy trên sao kê."),
  dict(t="Thông báo hợp đồng tiền gửi số 05-2026/TB-BQTSSR", d="15/09/2026", who="BQT", req="số 5 (F10, F16)",
       c="5 HĐTG tổng 127,5 tỷ: 45 tỷ và 15 tỷ (12 tháng, 8%), 2,5 tỷ mở mới (12 tháng, 8%), 5 tỷ (6 tháng, 7,8%), 60 tỷ Agribank (12 tháng, 8%). Toàn bộ tiền lãi chuyển về TK 116605084999 để thanh toán định kỳ các hạng mục bảo trì.",
       e="Lãi suất cao hơn biểu 12 tháng tại quầy (khoảng 5,9%) và cả mức gửi trực tuyến 6,8% của Agribank; 15 tỷ đã chuyển sang 12 tháng. Cần hợp đồng và xác nhận ngân hàng.")],
  chk=[dict(l="Số dư TK 116605084999 cuối ngày 20/05/2025", src="Giấy xác nhận, sao kê VietinBank", doc=4_843_654_006, st=_q["2025-05-20"], n=""),
       dict(l="Tổng Nợ TK 116605084999, 01/07/2024 – 20/05/2025", src="Sao kê VietinBank", doc=120_181_083_438, st=sum(t["debit"] for t in _QQ), n=""),
       dict(l="Tổng Có TK 116605084999, 01/07/2024 – 20/05/2025", src="Sao kê VietinBank", doc=125_024_737_444, st=sum(t["credit"] for t in _QQ), n=""),
       dict(l="Số giao dịch TK 116605084999, 01/07/2024 – 20/05/2025", src="Sao kê VietinBank", doc=36, st=len(_QQ), n=""),
       dict(l="Số dư TK Agribank 6350201010476 ngày 20/05/2025", src="Thư xác nhận Agribank", doc=417_400, st=_at(_a, "2025-05-20"), n=""),
       dict(l="Số dư TK 116605084999 ngày 12/05/2025", src="Báo cáo BQT 14/05/2025", doc=4_770_503_321, st=_q["2025-05-12"], n=""),
       dict(l="Tiền lãi TK 116605084999, 21/08/2024 – 12/05/2025", src="Báo cáo BQT 14/05/2025", doc=161_699_196, st=_INT, n=""),
       dict(l="Chi sửa chữa thang máy tới 12/05/2025", src="Báo cáo BQT 14/05/2025", doc=181_083_438, st=_SCH, n="BQT cộng cả phí ngân hàng 247.500 vào khoản chi thang máy"),
       dict(l="Số dư TK 116605084999 ngày 15/05/2026", src="Báo cáo BQT 15/05/2026", doc=2_054_769_278, st=_q["2026-05-15"], n=""),
       dict(l="Quỹ bảo trì ngày 15/05/2026", src="Báo cáo BQT 15/05/2026", doc=127_054_769_278, st=125e9 + _q["2026-05-15"] + _at(_a, "2026-05-15"), n="BQT chưa tính số dư TK Agribank 6350201010476"),
       dict(l="Bốn dòng chi 2026 trong Phụ lục chi phí (HNB, Thép Quang, sảnh, camera)", src="Báo cáo BQT 15/05/2026", doc=1_557_493_040, st=_PAY26, n="Hai dòng sảnh và camera chi từ TK 7784, không phải TK quỹ"),
       dict(l="Ba dòng thang máy, PCCC, máy phát điện năm 2026", src="Báo cáo BQT 15/05/2026", doc=863_834_733, st=0, n="Không có lệnh chi tương ứng trên sao kê ba tài khoản năm 2026"),
       dict(l="Ba dòng trên so với khoản hoàn ứng ngày 23/12/2025", src="Báo cáo BQT 15/05/2026", doc=863_834_733, st=986_910_176, n="Cùng loại việc (thang máy, PCCC, máy phát điện) nhưng thấp hơn 123.075.443 đồng")],
  nd=["Tài liệu của ngân hàng khớp tới từng đồng với dữ liệu của trang này: 9 trên 13 chỉ tiêu khớp, bốn chỉ tiêu lệch đều nằm ở báo cáo do BQT tự lập.",
      "Hai ngân hàng xác nhận 120 tỷ tiền gửi có kỳ hạn tại ngày 20/05/2025, nên phần lớn quỹ đã được chứng minh tồn tại ở thời điểm đó; vẫn cần xác nhận tại ngày gần nhất cho cả 127,5 tỷ.",
      "Nếu đúng như thông báo 15/09/2026, lãi suất 8%/năm giúp quỹ có thêm khoảng 4,7 tỷ tiền lãi mỗi năm; đây là thay đổi tích cực nhưng phải có hợp đồng để chốt.",
      "Bảng chi phí của BQT có 863,8 triệu chi thang máy, PCCC, máy phát điện không thấy trên sao kê năm 2026 và thấp hơn khoản 986,9 triệu đã hoàn ứng 123,1 triệu; đây là câu hỏi mới quan trọng nhất.",
      "Các tài liệu mới chưa giải thích sao kê tài khoản vận hành, chứng từ 6 khoản hoàn ứng, hồ sơ Thép Quang, hợp đồng giữ xe, kế hoạch bảo trì và báo cáo kiểm toán."],
  q=["Ba dòng chi thang máy 597.838.833, PCCC 261.135.900 và máy phát điện 4.860.000 đồng (tổng 863.834.733) trong Phụ lục chi phí báo cáo 15/05/2026 chi từ tài khoản nào, ngày nào, cho đơn vị nào; có phải là 6 khoản đã hoàn ứng 986.910.176 đồng ngày 23/12/2025 không; nếu phải, 123.075.443 đồng chênh lệch là khoản gì.",
     "Vì sao bảng chi phí quỹ bảo trì gồm cả khoản chi từ TK 117002997784 (sảnh 116.227.877 và camera 112.204.608), trong khi số dư và nguồn thu của tài khoản này không được báo cáo.",
     "Cung cấp hợp đồng tiền gửi và giấy xác nhận của ngân hàng cho 5 hợp đồng theo thông báo 15/09/2026, đặc biệt lãi suất 8%/năm và khoản 2,5 tỷ mở mới.",
     "Sao kê TK 116605084999 và TK Agribank từ 01/06/2026 để thấy tiền lãi đáo hạn tháng 8/2026 đã về tài khoản thanh toán quỹ.",
     "Lý do Điều 3.2.a Quy chế quy định công ty quản lý đứng tên tài khoản vận hành, nhưng TK 118002976372 do 6 thành viên BQT đồng chủ tài khoản; kèm sao kê tài khoản này từ 01/08/2025.",
     "Kế hoạch sử dụng khoảng 10,2 tỷ tiền lãi mỗi năm mà thông báo 15/09/2026 nói sẽ dùng thanh toán định kỳ các hạng mục bảo trì: danh mục hạng mục, dự toán và nghị quyết Hội nghị nhà chung cư thông qua kế hoạch bảo trì; khẳng định tiền lãi không dùng cho chi phí vận hành."])
_ok = sum(1 for c in DOCS["chk"] if abs(c["doc"] - c["st"]) < 1); assert _ok == 9, _ok

# ---- hop dong tien gui sau dot tai tuc thang 8/2026 theo Thong bao 05-2026/TB-BQTSSR ngay 15/09/2026
TD_NEW = [dict(hd="912/2024/70435", bank="VietinBank", v=45_000_000_000, ky="12 tháng", r=0.08, due="20/08/2027"),
          dict(hd="912/2024/70677", bank="VietinBank", v=15_000_000_000, ky="12 tháng", r=0.08, due="20/08/2027"),
          dict(hd="912/2026/21360", bank="VietinBank", v=2_500_000_000, ky="12 tháng", r=0.08, due="24/08/2027"),
          dict(hd="912/2025/28319", bank="VietinBank", v=5_000_000_000, ky="6 tháng", r=0.078, due="28/02/2027"),
          dict(hd="2208/2026/HĐTG/NHNo-SSR", bank="Agribank", v=60_000_000_000, ky="12 tháng", r=0.08, due="22/08/2027")]
TD_NEW_TOTAL = sum(x["v"] for x in TD_NEW); assert TD_NEW_TOTAL == 127_500_000_000
TD_NEW_INT = sum(x["v"] * x["r"] for x in TD_NEW)
TD_OLD_INT = 45e9 * .047 + 15e9 * .024 + 5e9 * .047 + 60e9 * .047 + 2.5e9 * .002
assert round(TD_NEW_INT) == 10_190_000_000 and round(TD_NEW_INT - TD_OLD_INT) == 4_655_000_000
# ---- cac o "tai lieu moi" dung chung voi ban tom tat
UPD = dict(
    td=["Hai ngân hàng xác nhận 120 tỷ tiền gửi có kỳ hạn tại ngày 20/05/2025: VietinBank 45 tỷ và 15 tỷ, Agribank 60 tỷ.",
        "Khoản 5 tỷ gửi ngày 29/08/2025 chưa có xác nhận của ngân hàng; báo cáo BQT ngày 15/05/2026 ghi khoản này kỳ hạn 1 năm, lãi 4,7%.",
        "Báo cáo BQT ngày 15/05/2026 ghi quỹ 127.054.769.278 đồng, khớp tiền gửi và số dư TK VietinBank nhưng chưa tính 3,66 triệu ở TK Agribank và 120,3 triệu ở TK 7784."],
    cost=["Phụ lục chi phí trong báo cáo BQT ngày 15/05/2026 ghi 2,42 tỷ; bốn dòng khớp từng đồng với lệnh chi trên sao kê: HNB 623,3 triệu, Thép Quang 705,8 triệu (mô tả là thiết bị điện, nước, intercom), sảnh 116,2 triệu và camera 112,2 triệu.",
          "Hai dòng sảnh và camera được chi từ TK 7784 nhưng BQT tự đưa vào bảng chi phí quỹ bảo trì, củng cố cách hạch toán đúng: tiền khu vực chung phải đi qua quỹ.",
          "Ba dòng thang máy 597,8 triệu, PCCC 261,1 triệu và máy phát điện 4,9 triệu (tổng 863,8 triệu) không có lệnh chi tương ứng trên sao kê ba tài khoản năm 2026; cùng loại việc với khoản 986,9 triệu hoàn ứng ngày 23/12/2025 nhưng thấp hơn 123,1 triệu.",
          "BQT cần cho biết 863,8 triệu chi từ tài khoản nào, có phải là 6 khoản đã hoàn ứng không, và 123,1 triệu chênh lệch là khoản gì."],
    roll=["Theo thông báo của BQT ngày 15/09/2026, 127,5 tỷ đã được gửi lại với lãi suất 8%/năm kỳ hạn 12 tháng (khoản 5 tỷ 7,8%, kỳ hạn 6 tháng), cao hơn biểu 12 tháng tại quầy (khoảng 5,9% ở cả hai ngân hàng) và mức gửi trực tuyến 6,8% của Agribank.",
          "Khoản 15 tỷ đã chuyển từ kỳ hạn 3 tháng sang 12 tháng và có thêm hợp đồng mới 2,5 tỷ, đúng hướng báo cáo khuyến nghị.",
          "Nếu đúng như thông báo, tiền lãi mỗi năm khoảng 10,2 tỷ, tăng khoảng 4,7 tỷ so với mức cũ; đây mới là thông báo của BQT, cần hợp đồng và xác nhận của ngân hàng để chốt.",
          "Thông báo cũng nêu toàn bộ tiền lãi sẽ chuyển về TK 116605084999 để thanh toán định kỳ các hạng mục bảo trì; tiền lãi là tiền của quỹ, chỉ được chi theo kế hoạch bảo trì được Hội nghị nhà chung cư thông qua và không dùng cho chi phí vận hành (Điều 6.1.b, 6.1.d Quy chế)."],
    req=["Tài liệu nhận ngày 28/09/2026 mới đáp ứng một phần hồ sơ số 1 (xác nhận tiền gửi tại 20/05/2025) và số 5 (thông báo hợp đồng tái tục tháng 8/2026).",
         "Thư VietinBank ngày 22/07/2024 xác nhận TK 118002976372 do 6 thành viên BQT đồng chủ tài khoản, nhưng chưa có sao kê của tài khoản này.",
         "Chưa có tài liệu nào cho 13 hồ sơ còn lại; quan trọng nhất là sao kê TK vận hành, chứng từ 6 khoản hoàn ứng, hồ sơ Thép Quang, hợp đồng giữ xe 18KSVSSR08082025, kế hoạch bảo trì và báo cáo kiểm toán.",
         "Báo cáo BQT ngày 14/05/2025 cộng phí ngân hàng 247.500 đồng hai lần, cho thấy sổ sách của BQT cần được kiểm toán."],
    auth=["Sao kê TK 116605084999 do VietinBank cấp cho giai đoạn 01/07/2024 – 20/05/2025 (36 giao dịch, tổng Nợ 120.181.083.438, tổng Có 125.024.737.444 đồng) khớp tuyệt đối với dữ liệu chuyển đổi từ bản scan.",
          "Giấy xác nhận số dư của VietinBank và Agribank tại ngày 20/05/2025 trùng số dư tính lại của hai tài khoản quỹ.",
          "Rủi ro in bản đã sửa rồi scan lại đã được loại trừ cho giai đoạn tới 20/05/2025; giai đoạn sau vẫn cần ngân hàng xác nhận trực tiếp."])
HT_INTRO = "Dựng lại quỹ theo hai bước: đưa mọi dòng tiền khu vực chung về đúng tài khoản quỹ, rồi xét khoản chi nào hợp lệ. Mặc định theo kịch bản cư dân nêu: khoản 986,9 triệu chuyển sang TK vận hành, các khoản trả Schindler và tiền thuế được coi là hợp lệ."
