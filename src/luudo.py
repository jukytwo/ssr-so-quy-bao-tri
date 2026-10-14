# -*- coding: utf-8 -*-
"""Nguon duy nhat: LUU DO DONG TIEN cho cac khoan thieu minh bach (SVG 1600x900).
Moi luu do: duong di theo Quy che (net dut xanh), duong di thuc te (do), so hieu khiem khuyet tren duong di va bang khiem khuyet ben phai.
Dung chung cho bao cao day du, ban tom tat, dashboard, bo trinh chieu Hoi nghi."""
import html, json, os, re
os.chdir("/home/claude/ssr")
_A = json.load(open("analysis.json"))

NAVY, RED, GREEN, GOLD, GRAY, INK = "#1F3864", "#A93434", "#1E7A46", "#B8860B", "#5B6475", "#1A1F2B"
TR = {"red": "#FBEDED", "green": "#EAF5EE", "navy": "#EDF1F7", "gray": "#F4F5F7", "gold": "#FBF3DF"}
W, H = 1600, 900
FONT = "'Be Vietnam Pro','Liberation Sans',Arial,sans-serif"
E = lambda s: html.escape(str(s), quote=False)


def wrap(t, size, width, k=0.53):
    n = max(8, int(width / (size * k)))
    out, cur = [], ""
    for w in str(t).split():
        if len(cur) + len(w) + (1 if cur else 0) > n:
            out.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur: out.append(cur)
    return out


def text(x, y, t, size=18, color=INK, weight=400, anchor="start", width=None, lh=1.28):
    lines = wrap(t, size, width, 0.64 if weight >= 700 else 0.57) if width else [t]
    s = "".join(f'<tspan x="{x}" dy="{0 if i == 0 else size * lh:.1f}">{E(l)}</tspan>' for i, l in enumerate(lines))
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" text-anchor="{anchor}">{s}</text>', len(lines)


def box(x, y, w, h, title, lines=(), kind="party", sub=None, ts=19):
    st = {"fund": (NAVY, NAVY, "#fff", "#DCE6F1"), "bad": (RED, TR["red"], RED, INK), "party": ("#9AA3B2", "#fff", NAVY, INK),
          "unknown": (GRAY, TR["gray"], GRAY, GRAY), "ok": (GREEN, TR["green"], GREEN, INK), "gold": (GOLD, TR["gold"], "#7A5A00", INK)}[kind]
    dash = ' stroke-dasharray="9 7"' if kind == "unknown" else ""
    o = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{st[1]}" stroke="{st[0]}" stroke-width="2.6"{dash}/>']
    t, n = text(x + 14, y + 28, title, ts, st[2], 800, width=w - 26)
    o.append(t); yy = y + 28 + n * (ts + 5) + 2
    for l in lines:
        t, n = text(x + 16, yy, l, 16, st[3], 400, width=w - 30, lh=1.25); o.append(t); yy += n * 20 + 3
    return "".join(o)


def arrow(pts, color=RED, width=4, dashed=False, label=None, lx=None, ly=None, lcolor=None, lw=260, lsize=16, anchor="start"):
    d = "M" + " L".join(f"{x},{y}" for x, y in pts)
    mk = "ar" if color == RED else ("ag" if color == GREEN else "an")
    da = ' stroke-dasharray="12 9"' if dashed else ""
    o = [f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"{da} marker-end="url(#{mk})" stroke-linejoin="round"/>']
    if label:
        if lx is None:
            (x1, y1), (x2, y2) = pts[-2], pts[-1]; lx, ly = (x1 + x2) / 2, (y1 + y2) / 2 - 12
        t, _ = text(lx, ly, label, lsize, lcolor or color, 700, anchor=anchor, width=lw); o.append(t)
    return "".join(o)


def badge(x, y, n):
    return (f'<circle cx="{x}" cy="{y}" r="17" fill="{RED}" stroke="#fff" stroke-width="3"/>'
            f'<text x="{x}" y="{y + 6}" font-size="18" font-weight="800" fill="#fff" text-anchor="middle">{n}</text>')


def panel(items, need, x=1105, y=40, w=470):
    o = [f'<rect x="{x}" y="{y}" width="{w}" height="{H - 2 * y}" rx="14" fill="#FFFFFF" stroke="#E3C8C8" stroke-width="2"/>',
         f'<rect x="{x}" y="{y}" width="{w}" height="52" rx="14" fill="{RED}"/><rect x="{x}" y="{y + 30}" width="{w}" height="22" fill="{RED}"/>',
         f'<text x="{x + 20}" y="{y + 35}" font-size="21" font-weight="800" fill="#fff">KHIẾM KHUYẾT</text>']
    yy = y + 88
    for i, (t, rule) in enumerate(items, 1):
        o.append(badge(x + 34, yy - 6, i))
        s, n = text(x + 62, yy, t, 17, INK, 600, width=w - 80); o.append(s); yy += n * 21.5
        if rule:
            s, n = text(x + 62, yy + 2, rule, 14.5, GRAY, 400, width=w - 80); o.append(s); yy += n * 18.5 + 2
        yy += 14
    yy = max(yy, y + 20)
    o.append(f'<line x1="{x + 20}" y1="{yy - 4}" x2="{x + w - 20}" y2="{yy - 4}" stroke="#E3E8EF" stroke-width="2"/>')
    s, n = text(x + 20, yy + 24, "Cần chứng từ", 17, NAVY, 800); o.append(s)
    s, n = text(x + 20, yy + 48, need, 16, NAVY, 400, width=w - 40); o.append(s)
    return "".join(o)


def legend(y=872):
    return (f'<g font-size="15" fill="{GRAY}">'
            f'<line x1="40" y1="{y - 5}" x2="92" y2="{y - 5}" stroke="{RED}" stroke-width="4"/><text x="102" y="{y}">Dòng tiền thực tế</text>'
            f'<line x1="280" y1="{y - 5}" x2="332" y2="{y - 5}" stroke="{GREEN}" stroke-width="3" stroke-dasharray="12 9"/><text x="342" y="{y}">Đường đi đúng theo Quy chế</text>'
            f'<rect x="590" y="{y - 16}" width="40" height="22" rx="5" fill="{TR["gray"]}" stroke="{GRAY}" stroke-dasharray="6 5"/><text x="640" y="{y}">Chưa có chứng từ</text>'
            f'<circle cx="836" cy="{y - 5}" r="11" fill="{RED}"/><text x="856" y="{y}">Khiếm khuyết</text></g>')


def svg(body):
    return (f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="{FONT}" role="img">'
            '<defs>'
            f'<marker id="ar" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{RED}"/></marker>'
            f'<marker id="ag" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{GREEN}"/></marker>'
            f'<marker id="an" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{NAVY}"/></marker>'
            '</defs>'
            f'<rect width="{W}" height="{H}" fill="#fff"/>' + body + legend() + '</svg>')


def tr_(v): return f"{v / 1e6:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".") + " triệu"


# ------------------------------------------------------------------ 1. 986,9 trieu
def d1():
    b = []
    b.append(box(40, 330, 300, 150, "Quỹ bảo trì", ["TK 116605084999, VietinBank", "Luôn còn ít nhất 4,22 tỷ"], "fund"))
    b.append(box(430, 560, 330, 205, "TK vận hành 118002976372", ["Ban quản trị đứng tên, 6 thành viên đồng chủ tài khoản", "Quy chế: Công ty quản lý đứng tên", "Chưa có sao kê"], "bad"))
    b.append(box(800, 330, 270, 170, "6 khoản chi", ["29/08 – 23/12/2025", "Thang máy, phòng cháy, máy phát điện", "Chưa biết người nhận"], "unknown"))
    b.append(box(800, 80, 270, 120, "Đơn vị làm bảo trì", ["Nhận tiền thẳng từ quỹ"], "ok"))
    b.append(arrow([(190, 330), (190, 140), (792, 140)], GREEN, 3, True, "Theo Quy chế: chuyển thẳng cho đơn vị bảo trì (Điều 7.2)", 230, 118, GREEN, 700))
    b.append(arrow([(340, 450), (385, 450), (385, 645), (422, 645)], RED, 5, False, "23/12/2025: 986.910.176 đồng, hoàn ứng một lần", 44, 530, RED, 330))
    b.append(arrow([(760, 600), (935, 600), (935, 508)], RED, 4, True, "Chi trước 6 lần, chưa có chứng từ", 780, 632, RED, 300))
    b.append(box(430, 330, 330, 150, "Bảng chi phí 15/05/2026", ["Báo cáo 03-2026/BC-BQTSSR", "Chỉ giải thích 863,8 triệu", "Lệch 123,1 triệu so với 986,9 triệu"], "gold"))
    b.append(arrow([(760, 405), (792, 405)], GOLD, 2, True))
    b += [badge(385, 548, 1), badge(560, 555, 2), badge(760, 700, 3), badge(1070, 330, 4), badge(760, 330, 5), badge(340, 330, 6)]
    b.append(panel([("Tiền quỹ vào tài khoản của chính Ban quản trị, không tới thẳng đơn vị bảo trì", "Quy chế thu chi Điều 7.2"),
                    ("Tài khoản nhận do 6 thành viên Ban quản trị đồng đứng tên, trong khi Quy chế giao Công ty quản lý đứng tên", "Quy chế thu chi Điều 3.2.a"),
                    ("Ứng từ 29/08, gộp hoàn một lần ngày 23/12: không hoàn cuối mỗi tháng, gấp khoảng 20 lần hạn mức 10 triệu", "Quy chế thu chi Điều 7.4"),
                    ("Không có sao kê tài khoản nhận: chưa biết tiền cuối cùng trả cho ai", "Quy chế thu chi Điều 6.1.f"),
                    ("Bảng chi phí của Ban quản trị lệch 123,1 triệu so với số đã chuyển", "Báo cáo 03-2026/BC-BQTSSR"),
                    ("Quỹ luôn đủ tiền, không có lý do phải ứng trước từ tài khoản khác", "")],
                   "Căn cứ của lệnh chuyển ngày 23/12/2025; sao kê TK 118002976372 từ 01/08/2025; hợp đồng, hóa đơn, nghiệm thu của 6 khoản."))
    return svg("".join(x for x in b if x))


# ------------------------------------------------------------------ 2. khu vuc chung
def d2():
    inc, exp = _A["inc7784"], _A["exp7784"]
    b = []
    srcs = [("Chicilon Media", "quảng cáo", inc["Thu khu vực chung – quảng cáo (Chicilon)"]),
            ("Viễn thông ACT", "thuê mặt bằng", inc["Thu khu vực chung – thuê mặt bằng (ACT)"]),
            ("Hưng Thái", "kệ quảng cáo", inc["Thu khu vực chung – standee (Hưng Thái)"])]
    for i, (n, k, v) in enumerate(srcs):
        y = 250 + i * 150
        b.append(box(40, y, 230, 112, n, [f"{k}: {tr_(v)}"], "party"))
        b.append(arrow([(270, y + 56), (402, 470)], RED, 4))
    b.append(box(410, 360, 260, 220, "TK 117002997784", ["Thu phí dịch vụ, Ban quản trị đứng tên", "Nằm ngoài quỹ bảo trì", "Vào 1,71 tỷ, còn 120,3 triệu ngày 31/05/2026"], "bad"))
    b.append(box(410, 70, 260, 110, "Quỹ bảo trì", ["TK 116605084999"], "fund"))
    b.append(arrow([(155, 250), (155, 125), (402, 125)], GREEN, 3, True, "Luật Nhà ở 2023: phải nộp vào quỹ", 40, 80, GREEN, 360))
    b.append(arrow([(560, 188), (560, 352)], RED, 4, False, "24/07/2025: 260,9 triệu đã vào quỹ bị chuyển ra", 575, 250, RED, 250))
    outs = [("Thành Công", "4 hợp đồng", exp["Chi sửa chữa, mua sắm – Thành Công"]), ("Khởi Sáng Việt", "giữ xe", exp["Chi hệ thống giữ xe – Khởi Sáng Việt"]),
            ("KTECH", "camera", exp["Chi hệ thống camera – KTECH"]), ("Nộp thuế", "9 lệnh", exp["Nộp thuế"])]
    for i, (n, k, v) in enumerate(outs):
        y = 250 + i * 130
        b.append(box(800, y, 270, 96, n, [f"{k}: {tr_(v)}"], "party" if n == "Nộp thuế" else "unknown"))
        b.append(arrow([(670, 470), (792, y + 48)], RED if n != "Nộp thuế" else NAVY, 4))
    b += [badge(330, 470, 1), badge(560, 300, 2), badge(735, 395, 3), badge(735, 560, 4), badge(640, 600, 5)]
    b.append(panel([("Tiền khai thác khu vực chung không nộp vào quỹ", "Khoản 4 Điều 153 Luật Nhà ở 2023"),
                    ("260,9 triệu đã vào đúng quỹ bị chuyển ra 8 ngày sau với lý do trả nhầm", ""),
                    ("Chi 1,40 tỷ không qua kế hoạch bảo trì, 3 báo giá, nghiệm thu của quỹ", "Quy chế thu chi Điều 6.3"),
                    ("Cả 6 hợp đồng đều trên 50 triệu, chưa thấy văn bản cho phép của chủ sở hữu", "Quy chế thu chi Điều 9.2"),
                    ("Chưa thấy công khai thu chi của tài khoản này", "Quy chế thu chi Điều 6.1.g")],
                   "Căn cứ mở TK 117002997784; hợp đồng, báo giá, nghiệm thu của Thành Công, Khởi Sáng Việt, KTECH; chuyển số dư về quỹ."))
    return svg("".join(b))


# ------------------------------------------------------------------ 3. Thep Quang
def d3():
    b = []
    steps = ["Kế hoạch được Hội nghị thông qua hoặc trên 50% chủ sở hữu đồng ý", "3 báo giá", "Hợp đồng", "Tạm ứng", "Nghiệm thu", "Thanh toán phần còn lại"]
    x = 40
    for i, s in enumerate(steps):
        w = 250 if i == 0 else 128
        b.append(box(x, 60, w, 120, s, [], "ok", ts=16))
        if i < len(steps) - 1: b.append(arrow([(x + w, 120), (x + w + 16, 120)], GREEN, 3, True))
        x += w + 22
    t, _ = text(40, 215, "Theo Quy chế thu chi (Điều 9.2, 6.3.b, 6.3.c, 6.3.e)", 16, GREEN, 700); b.append(t)
    b.append(box(40, 330, 300, 150, "Quỹ bảo trì", ["TK 116605084999, VietinBank"], "fund"))
    b.append(box(430, 280, 300, 120, "Hợp đồng 080426/HDDV/BQT TQ", ["Ký 08/04/2026", "Chưa thấy văn bản cho phép"], "bad"))
    b.append(box(800, 330, 270, 150, "Công ty Thép Quang", ["TK 2666677777", "Chưa xác minh được mã số thuế"], "bad"))
    b.append(box(800, 560, 270, 150, "Thiết bị khu vực chung", ["Chưa có danh mục, hóa đơn, biên bản giao nhận"], "unknown"))
    b.append(box(430, 560, 300, 150, "Hợp đồng 221025 của Thành Công", ["Cùng ký hiệu BQT TQ", "Hai nhà thầu khác nhau"], "gold"))
    b.append(arrow([(340, 450), (792, 450)], RED, 6, False, "24/04/2026: trả 100% = 705.769.875 đồng, 16 ngày sau ký", 360, 500, RED, 320))
    b.append(arrow([(935, 480), (935, 552)], RED, 3, True))
    b.append(arrow([(705, 560), (705, 408)], GOLD, 2, True, "cùng ký hiệu BQT TQ", 520, 548, GOLD, 180, 15))
    b += [badge(730, 282, 1), badge(560, 452, 2), badge(1070, 600, 3), badge(1070, 360, 4), badge(730, 590, 5)]
    b.append(panel([("Không thấy văn bản cho phép: gấp 14 lần mức 50 triệu Ban quản trị được tự quyết, bằng 141% trần cả năm", "Quy chế thu chi Điều 9.2, 6.3.c"),
                    ("Trả 100% trước nghiệm thu, không có đợt tạm ứng", "Quy chế thu chi Điều 6.3.b"),
                    ("Hàng hóa chỉ ghi chung là thiết bị khu vực sử dụng chung", ""),
                    ("Chưa xác minh được mã số thuế của Thép Quang", "Quy chế thu chi Điều 6.1.c"),
                    ("Ký hiệu BQT TQ trùng với hợp đồng của Thành Công", "")],
                   "Văn bản cho phép; hợp đồng, danh mục thiết bị, hóa đơn, biên bản giao nhận, 3 báo giá; mã số thuế Thép Quang; kiểm đếm thiết bị."))
    return svg("".join(b))


# ------------------------------------------------------------------ 4. chum hop dong thang 4/2026
def d4():
    b = []
    days = [("06/04", 110), ("07/04", 330), ("08/04", 550), ("14/04", 770), ("24/04", 990)]
    b.append(f'<line x1="60" y1="120" x2="1060" y2="120" stroke="{NAVY}" stroke-width="3"/>')
    for d, x in days:
        b.append(f'<circle cx="{x}" cy="120" r="10" fill="{NAVY}"/>'); t, _ = text(x, 92, d + "/2026", 18, NAVY, 800, "middle"); b.append(t)
    b.append(box(40, 170, 200, 130, "Thành Công ký", ["HĐ 06042026", "193,7 triệu"], "bad"))
    b.append(box(245, 170, 190, 130, "HNB ký", ["Cấp nước sinh hoạt", "1.246,6 triệu"], "bad"))
    b.append(box(445, 170, 210, 130, "Thép Quang ký", ["HĐ 080426", "705,8 triệu"], "bad"))
    t, n = text(40, 350, "Ba hợp đồng 2,15 tỷ ký trong ba ngày, gấp hơn 4 lần trần sửa chữa đột xuất 500 triệu của cả năm", 20, RED, 800, width=640); b.append(t)
    b.append(box(40, 470, 300, 120, "Quỹ bảo trì", ["TK 116605084999"], "fund"))
    b.append(box(40, 660, 300, 120, "TK 117002997784", ["Tiền khu vực chung, ngoài quỹ"], "bad"))
    b.append(box(800, 440, 270, 110, "HNB, cấp nước sinh hoạt", ["Còn 623,3 triệu sẽ chi tiếp từ quỹ"], "party"))
    b.append(box(800, 600, 270, 100, "Thép Quang", ["Trả 100%"], "party"))
    b.append(box(800, 730, 270, 110, "Thành Công", ["Tạm ứng 60%"], "party"))
    b.append(arrow([(340, 505), (792, 495)], RED, 5, False, "14/04 lúc 11:26: tạm ứng 50% = 623,3 triệu", 360, 485, RED, 400))
    b.append(arrow([(340, 720), (792, 785)], RED, 5, False, "14/04 lúc 11:28: tạm ứng 60% = 116,2 triệu", 360, 790, RED, 400))
    b.append(arrow([(340, 560), (700, 560), (700, 650), (792, 650)], RED, 5, False, "24/04: 705,8 triệu", 470, 545, RED, 220))
    b += [badge(690, 345, 1), badge(560, 700, 2), badge(760, 470, 3), badge(435, 172, 4), badge(1070, 445, 5)]
    b.append(panel([("Ba hợp đồng lớn ký dồn trong ba ngày, không thấy lấy ý kiến chủ sở hữu", "Quy chế thu chi Điều 9.2"),
                    ("Hai lệnh chi trên hai tài khoản lập cách nhau 2 phút: chưa tách người lập và người duyệt", "Quy chế thu chi Điều 6.3.b (3 chữ ký)"),
                    ("Tạm ứng 50% tới 100% trước khi thi công, nghiệm thu", "Quy chế thu chi Điều 6.3.b"),
                    ("Số hợp đồng HNB mang ngày 24/03/2026, ghi ký 07/04/2026", ""),
                    ("HNB còn 623,3 triệu sẽ chi tiếp, trong khi cư dân phản ánh ống nước vẫn bể, dột nhiều nơi", "")],
                   "Văn bản cho phép từng hợp đồng; báo giá, dự toán, nghiệm thu; bảo hành cấp nước của HNB; nhật ký duyệt lệnh ngày 14/04/2026."))
    return svg("".join(b))


# ------------------------------------------------------------------ 5. tien gui
def d5():
    b = []
    b.append(box(40, 300, 290, 190, "Quỹ ngày 31/05/2026", ["127,15 tỷ", "Tiền gửi 125 tỷ", "TK thanh toán 2,15 tỷ"], "fund"))
    tds = [("VietinBank 45 tỷ", "12 tháng, đáo hạn 20/08/2026"), ("VietinBank 15 tỷ", "3 tháng, tái tục"), ("VietinBank 5 tỷ", "gửi 29/08/2025, không có dấu vết sau đó"),
           ("Agribank 60 tỷ", "gửi lại 22/08/2025, không có dấu vết sau đó")]
    for i, (n, k) in enumerate(tds):
        y = 60 + i * 120
        b.append(box(430, y, 300, 96, n, [k], "unknown" if "không có dấu vết" in k else "party"))
        b.append(arrow([(330, 395), (422, y + 48)], NAVY, 3))
    b.append(box(430, 560, 300, 170, "06 – 08/2026", ["Đáo hạn khoảng 110 tỷ", "Khoảng 5,17 tỷ tiền lãi về tài khoản", "Sao kê dừng ở 31/05/2026"], "unknown"))
    b.append(box(800, 300, 270, 190, "Tái tục 127,5 tỷ", ["5 hợp đồng, lãi 8% một năm", "Theo thông báo 15/09/2026", "Chưa có xác nhận ngân hàng"], "bad"))
    b.append(box(800, 560, 270, 140, "Khoản 2,5 tỷ mở mới", ["Chưa rõ nguồn tiền"], "unknown"))
    b.append(arrow([(730, 640), (765, 640), (765, 420), (792, 420)], RED, 4, True))
    b.append(arrow([(730, 700), (792, 640)], RED, 3, True))
    b += [badge(580, 560, 1), badge(1070, 300, 2), badge(1070, 560, 3), badge(730, 400, 4), badge(935, 490, 5)]
    b.append(panel([("Sao kê in ngày 04/09/2026 nhưng dừng ở 31/05/2026: không thấy dòng tiền đáo hạn và tái tục", "Quy chế thu chi Điều 6.1.g"),
                    ("127,5 tỷ sau tái tục chưa có hợp đồng và giấy xác nhận của ngân hàng", "Quy chế thu chi Điều 3.1.a"),
                    ("Khoản 2,5 tỷ gửi mới chưa rõ lấy từ đâu", ""),
                    ("Khoản 5 tỷ và 60 tỷ không có dấu vết từ ngày gửi tới 31/05/2026", ""),
                    ("Lãi 8% cao hơn biểu 12 tháng tại quầy khoảng 5,9%: cần xem điều kiện kèm theo", "")],
                   "Sao kê ba tài khoản từ 01/06/2026; hợp đồng tiền gửi và giấy xác nhận tại quầy của VietinBank, Agribank."))
    return svg("".join(b))


LD = [
    dict(k="ld1", code="F01", title="986,9 triệu qua tài khoản của chính Ban quản trị, chưa rõ người nhận cuối", fn=d1),
    dict(k="ld2", code="F02, F07", title="1,71 tỷ tiền khu vực chung nằm ngoài quỹ, 1,40 tỷ đã chi ngoài quy trình", fn=d2),
    dict(k="ld3", code="F03", title="705,8 triệu trả trọn cho Thép Quang, chưa có văn bản cho phép và danh mục hàng hóa", fn=d3),
    dict(k="ld4", code="F03, F05, F07, F15", title="Tháng 4/2026: ba hợp đồng 2,15 tỷ ký trong ba ngày, chi trước khi nghiệm thu", fn=d4),
    dict(k="ld5", code="F04, F16", title="127,5 tỷ tiền gửi sau tái tục chưa có xác nhận, sao kê dừng ở 31/05/2026", fn=d5),
]
for x in LD: x["svg"] = x["fn"]()
INTRO = ("Mỗi lưu đồ đặt đường đi của tiền theo Quy chế (nét đứt xanh) cạnh đường đi thực tế trên sao kê (đỏ). "
         "Số đỏ đánh dấu khiếm khuyết, giải thích ở cột bên phải; ô xám nét đứt là phần chưa có chứng từ.")
for x in LD:
    for s in re.findall(r">([^<>]+)<", x["svg"]):
        assert "→" not in s and "->" not in s

if __name__ == "__main__":
    os.makedirs("luudo", exist_ok=True)
    for x in LD:
        open(f"luudo/{x['k']}.svg", "w", encoding="utf-8").write(x["svg"])
    print("ok", len(LD))
