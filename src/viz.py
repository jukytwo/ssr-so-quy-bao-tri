# -*- coding: utf-8 -*-
"""Hinh truc quan dung chung cho PDF (mau co dinh) va dashboard (bien CSS): so do dong tien, chi theo thang, lai suat theo thoi diem,
vong tuan thu, lai khong ky han tung thang, bieu tuong muc."""
import json, math, html

E = lambda s: html.escape(str(s), quote=False)
PDF = dict(ink="#16294A", ink2="#3d4656", muted="#6a7384", line="#b9c3d3", grid="#e5e9ef", box="#1F3864", boxt="#ffffff", boxt2="#dbe3f2",
           acc="#C8992F", ok="#1E7A46", crit="#A93434", warn="#C0662A", na="#7b8696", cau="#b58a12", soft="#EEF3FA", crit_soft="#fbeaea",
           ok_soft="#e2f1e8", warn_soft="#fdf0e6", surface="#ffffff", s7784="#2E6F95", pill_bg="#C8992F", pill_fg="#1F3864", bar1="#1F3864", bar2="#C0662A", font="'Be Vietnam Pro','Liberation Sans',sans-serif")
DASH = dict(ink="var(--ink)", ink2="var(--ink-2)", muted="var(--muted)", line="var(--line-2)", grid="var(--line)", box="var(--ink)", boxt="var(--surface)",
            boxt2="var(--surface-2)", acc="var(--accent)", ok="var(--ok)", crit="var(--crit)", warn="var(--warn)", na="var(--na)", cau="var(--cau)",
            soft="var(--surface-2)", crit_soft="var(--crit-soft)", ok_soft="var(--ok-soft)", warn_soft="var(--warn-soft)", surface="var(--surface)",
            s7784="var(--s1)", pill_bg="var(--cau-soft)", pill_fg="var(--cau)", bar1="var(--s3)", bar2="var(--s2)", font="var(--f-body)")

def _t(x, y, s, T, size=11, w=400, col="ink", anchor="start", extra=""):
    c = T.get(col, col)
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" style="fill:{c};font-size:{size}px;font-weight:{w};font-family:{T["font"]}" {extra}>{E(s)}</text>'

def _vn(v, d=1):
    s = f"{v:,.{d}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")

# ---------------------------------------------------------------- 1. so do dong tien ba tai khoan
def svg_flow(T=PDF):
    W, H = 700, 430
    o = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Sơ đồ dòng tiền ba tài khoản">',
         '<defs>' + "".join(f'<marker id="ah{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" markerUnits="userSpaceOnUse" orient="auto-start-reverse">'
                            f'<path d="M0 0 L10 5 L0 10 z" style="fill:{T[k]}"/></marker>' for k in ("ok", "warn", "crit")) + '</defs>']
    def box(x, y, w, h, fill, stroke=None, r=8, dash=False):
        st = f"fill:{fill};" + (f"stroke:{stroke};stroke-width:1.6;" if stroke else "") + ("stroke-dasharray:5 4;" if dash else "")
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" style="{st}"/>')
    def path(x1, y1, x2, y2, col, wd, dash=False, label=None, lx=None, ly=None, lcol=None, anchor="middle"):
        mx = (x1 + x2) / 2
        st = f"fill:none;stroke:{T[col]};stroke-width:{wd:.1f};stroke-linecap:round;" + ("stroke-dasharray:6 5;" if dash else "")
        o.append(f'<path d="M{x1:.1f} {y1:.1f} C{mx:.1f} {y1:.1f} {mx:.1f} {y2:.1f} {x2 - 3:.1f} {y2:.1f}" style="{st}" marker-end="url(#ah{col})"/>')
        if label:
            o.append(_t(lx if lx is not None else mx, ly if ly is not None else (y1 + y2) / 2 - 5, label, T, 10.5, 700, lcol or col, anchor))
    wd = lambda v: 1.6 + 7.5 * math.sqrt(v / 124.79e9)
    # cot trai: nguon tien
    box(6, 58, 146, 70, T["ok_soft"], T["ok"])
    o.append(_t(79, 80, "Chủ đầu tư", T, 12, 700, "ink", "middle")); o.append(_t(79, 99, "bàn giao 15/08/2024", T, 10, 400, "ink2", "middle"))
    o.append(_t(79, 118, "124,79 tỷ", T, 14, 800, "ok", "middle"))
    box(6, 292, 146, 76, T["soft"], T["line"])
    o.append(_t(79, 313, "Thuê khu vực chung", T, 12, 700, "ink", "middle")); o.append(_t(79, 331, "quảng cáo, mặt bằng, kệ", T, 10, 400, "ink2", "middle"))
    o.append(_t(79, 355, "1,71 tỷ", T, 14, 800, "ink", "middle"))
    # cot giua: tai khoan
    MX0, MW = 214, 206; MC = MX0 + MW / 2
    box(MX0, 20, MW, 196, T["box"])
    o.append(_t(MC, 46, "QUỸ BẢO TRÌ", T, 13, 800, "boxt", "middle", 'letter-spacing="1.5"'))
    o.append(_t(MC, 64, "VietinBank 116605084999 và Agribank", T, 9.5, 400, "boxt2", "middle"))
    o.append(_t(MC, 100, "127,15 tỷ", T, 26, 800, "boxt", "middle")); o.append(_t(MC, 118, "còn ngày 31/05/2026", T, 10, 400, "boxt2", "middle"))
    box(MX0 + 14, 132, MW - 28, 30, T["pill_bg"], None, 6); o.append(_t(MC, 152, "125 tỷ tiền gửi có kỳ hạn", T, 11, 700, "pill_fg", "middle"))
    box(MX0 + 14, 170, MW - 28, 30, T["boxt2"], None, 6); o.append(_t(MC, 190, "Lãi đã nhận +5,48 tỷ", T, 11, 700, "box", "middle"))
    box(MX0, 276, MW, 108, T["crit_soft"], T["crit"])
    o.append(_t(MC, 298, "TK THU DỊCH VỤ 117002997784", T, 11, 800, "crit", "middle")); o.append(_t(MC, 315, "ngoài quỹ bảo trì", T, 10, 400, "crit", "middle"))
    o.append(_t(MC, 340, "Vào 1,71 tỷ · chi 1,40 tỷ", T, 12, 700, "ink", "middle")); o.append(_t(MC, 358, "thuế 0,19 tỷ · còn 0,12 tỷ", T, 10.5, 400, "ink2", "middle"))
    o.append(_t(MC, 375, "không qua quy trình của quỹ", T, 9.5, 400, "crit", "middle"))
    # dong vao
    path(152, 93, MX0, 93, "ok", 6.5); o.append(_t((152 + MX0) / 2, 82, "124,79 tỷ", T, 10.5, 800, "ok", "middle"))
    path(152, 330, MX0, 330, "crit", 3.2); o.append(_t((152 + MX0) / 2, 320, "1,71 tỷ", T, 10.5, 800, "crit", "middle"))
    path(110, 292, MX0 + 40, 216, "ok", 1.8, dash=True)
    o.append(_t(8, 250, "Luật Nhà ở 2023:", T, 10, 700, "ok")); o.append(_t(8, 263, "lẽ ra phải vào quỹ", T, 10, 700, "ok"))
    path(MX0 + 70, 216, MX0 + 70, 276, "crit", 2.4)
    o.append(_t(MX0 + 76, 247, "260,9 triệu chuyển đi", T, 9.5, 700, "crit")); o.append(_t(MX0 + 76, 259, "ngày 24/07/2025", T, 9.5, 700, "crit"))
    # cot phai: chi tu quy
    RX, RW = 494, 202
    outs = [("Schindler", "806,9 triệu", "warn", 18, 3.0, "phí bảo trì, 14 hợp đồng sửa"), ("HNB · cấp nước", "623,3 triệu", "warn", 64, 2.8, "tạm ứng 50% hợp đồng"),
            ("Thép Quang", "705,8 triệu", "crit", 110, 2.9, "chưa rõ hàng hóa"), ("TK vận hành BQT", "986,9 triệu", "crit", 156, 3.2, "trái Điều 7.2, 7.4")]
    for i, (a, b, col, y, w_, sub) in enumerate(outs):
        box(RX, y, RW, 40, T["crit_soft"] if col == "crit" else T["warn_soft"], T[col], 6)
        o.append(_t(RX + 9, y + 16, a, T, 10.5, 700, "ink")); o.append(_t(RX + RW - 9, y + 16, b, T, 10.5, 800, col, "end"))
        o.append(_t(RX + 9, y + 32, sub, T, 9.5, 400, col))
        path(MX0 + MW, 58 + i * 34, RX, y + 20, col, w_)
    outs2 = [("Thành Công · nội thất", "856,8 triệu", 262), ("Khởi Sáng Việt", "356,4 triệu", 292), ("KTECH · camera", "187,0 triệu", 322), ("Nộp thuế", "187,4 triệu", 352)]
    for i, (a, b, y) in enumerate(outs2):
        box(RX, y, RW, 26, T["warn_soft"], T["warn"], 5)
        o.append(_t(RX + 9, y + 17, a, T, 10.5, 700, "ink")); o.append(_t(RX + RW - 9, y + 17, b, T, 10.5, 800, "warn", "end"))
        path(MX0 + MW, 300 + i * 22, RX, y + 13, "warn", 1.9)
    # chu giai
    ly = 412; x = 6
    for col, lab, dash in (("ok", "Tiền vào", False), ("warn", "Chi cần kiểm tra hồ sơ", False), ("crit", "Làm trái Quy chế hoặc Luật", False), ("ok", "Lẽ ra phải có (nét đứt)", True)):
        st = f"stroke:{T[col]};stroke-width:3;" + ("stroke-dasharray:5 4;" if dash else "")
        o.append(f'<line x1="{x}" y1="{ly - 4}" x2="{x + 22}" y2="{ly - 4}" style="{st}"/>'); o.append(_t(x + 28, ly, lab, T, 10, 400, "ink2"))
        x += 44 + len(lab) * 5.4
    o.append("</svg>")
    return "".join(o)

# ---------------------------------------------------------------- 2. chi theo thang
def svg_monthly(T=PDF):
    A = json.load(open("/home/claude/ssr/analysis.json"))
    cats = set(A["spend_groups"].keys())
    months = ["04/2025", "05/2025", "06/2025", "07/2025", "08/2025", "09/2025", "10/2025", "11/2025", "12/2025", "01/2026", "02/2026", "03/2026", "04/2026", "05/2026"]
    q = {m: 0.0 for m in months}; v = {m: 0.0 for m in months}
    for t in A["tx"]:
        if not t["debit"]: continue
        mm = t["date"][3:]
        if mm not in q: continue
        if t["cat"] in cats: q[mm] += t["debit"] / 1e6
        elif t["key"].startswith("V") and t["cat"] not in ("Phí ngân hàng", "Nộp thuế"): v[mm] += t["debit"] / 1e6
    W, H = 700, 250; L, R, TT, B = 46, 10, 22, 34; iw, ih = W - L - R, H - TT - B; ymax = 1800
    y = lambda val: TT + ih - val / ymax * ih
    o = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Chi theo tháng">']
    for g in range(0, 1801, 300):
        o.append(f'<line x1="{L}" x2="{W - R}" y1="{y(g):.1f}" y2="{y(g):.1f}" style="stroke:{T["grid"] if g else T["line"]};stroke-width:0.8"/>')
        o.append(_t(L - 6, y(g) + 3.5, _vn(g, 0), T, 9.5, 400, "muted", "end"))
    bw = iw / len(months)
    for i, m in enumerate(months):
        x = L + i * bw + bw * 0.18; w_ = bw * 0.64
        a, b = q[m], v[m]
        if a: o.append(f'<rect x="{x:.1f}" y="{y(a):.1f}" width="{w_:.1f}" height="{max(1, y(0) - y(a)):.1f}" rx="2" style="fill:{T["bar1"]}"/>')
        if b: o.append(f'<rect x="{x:.1f}" y="{y(a + b):.1f}" width="{w_:.1f}" height="{max(1, y(a) - y(a + b) - 1.2):.1f}" rx="2" style="fill:{T["bar2"]}"/>')
        if a + b > 250: o.append(_t(x + w_ / 2, y(a + b) - 4, _vn(a + b, 0), T, 9.5, 700, "ink", "middle"))
        o.append(_t(x + w_ / 2, H - B + 14, m[:2] + "/" + m[5:], T, 9.5, 400, "muted", "middle"))
    # chu thich hai dinh
    def note(mm, lines, part):
        i = months.index(mm); x0 = L + i * bw + bw * 0.18; ym = y(part / 2)
        o.append(f'<line x1="{x0 - 22:.1f}" y1="{ym:.1f}" x2="{x0 - 3:.1f}" y2="{ym:.1f}" style="stroke:{T["crit"]};stroke-width:1.2"/>')
        for k, ln in enumerate(lines): o.append(_t(x0 - 26, ym + 4 + (k - (len(lines) - 1) / 2) * 13, ln, T, 10, 700, "crit", "end"))
    note("12/2025", ["986,9 triệu", "sang TK vận hành"], q["12/2025"])
    note("04/2026", ["cấp nước 623,3 triệu", "thiết bị 705,8 triệu"], q["04/2026"])
    for x, col, lab in ((L, "bar1", "Chi từ quỹ bảo trì"), (L + 150, "bar2", "Chi từ TK thu dịch vụ 7784 (không tính thuế)")):
        o.append(f'<rect x="{x}" y="{H - 10}" width="10" height="8" rx="2" style="fill:{T[col]}"/>'); o.append(_t(x + 15, H - 3, lab, T, 9.5, 400, "ink2"))
    o.append("</svg>")
    return "".join(o)

# ---------------------------------------------------------------- 3. lai suat theo thoi diem (bieu do cham)
RATE_ROWS = [("08/2024 · kỳ hạn 3 tháng", "15 tỷ VietinBank", 2.0, 2.0, 1.9, None, None),
             ("08/2024 · kỳ hạn 12 tháng", "45 tỷ VietinBank, 60 tỷ Agribank", 4.7, 4.7, 4.2, (5.75, 6.0), None),
             ("05/2025 – 02/2026 · 3 tháng", "15 tỷ tái tục ba kỳ", 1.9, 1.9, 1.9, None, 4.7),
             ("02/2026 · kỳ hạn 3 tháng", "15 tỷ tái tục", 2.4, 2.4, None, None, 5.2),
             ("08/2025 · tái tục 12 tháng", "45 tỷ, 60 tỷ, gửi thêm 5 tỷ", None, 4.7, 4.2, (6.1, 6.1), None),
             ("08/2026 · đáo hạn 110 tỷ", "sau kỳ sao kê", None, 5.9, 4.5, (6.8, 7.8), None)]
def svg_rates(T=PDF):
    W, rh = 700, 40; L, R, TT = 205, 18, 44; H = TT + rh * len(RATE_ROWS) + 30; xmax = 9.0
    x = lambda v: L + v / xmax * (W - L - R)
    o = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Lãi suất theo thời điểm">']
    # chu giai tren
    lx = 8
    for kind, lab in (("bqt", "BQT nhận"), ("post", "Biểu niêm yết tại quầy"), ("corp", "Biểu dành cho tổ chức"), ("mkt", "Ngân hàng cổ phần cùng lúc"), ("ref", "Kỳ hạn 12 tháng lúc đó")):
        cx = lx + 6
        if kind == "bqt": o.append(f'<circle cx="{cx}" cy="14" r="5.5" style="fill:{T["acc"]}"/>')
        elif kind == "post": o.append(f'<circle cx="{cx}" cy="14" r="6" style="fill:none;stroke:{T["box"]};stroke-width:2"/>')
        elif kind == "corp": o.append(f'<rect x="{cx - 4}" y="10" width="8" height="8" style="fill:{T["na"]}"/>')
        elif kind == "mkt": o.append(f'<rect x="{cx - 7}" y="10" width="14" height="8" rx="4" style="fill:{T["ok"]};opacity:.35"/>')
        else: o.append(f'<line x1="{cx}" y1="7" x2="{cx}" y2="21" style="stroke:{T["muted"]};stroke-width:2;stroke-dasharray:3 2"/>')
        o.append(_t(cx + 11, 18, lab, T, 9.5, 400, "ink2")); lx += 30 + len(lab) * 5.3
    for g in range(0, 10):
        o.append(f'<line x1="{x(g):.1f}" x2="{x(g):.1f}" y1="{TT - 6}" y2="{TT + rh * len(RATE_ROWS)}" style="stroke:{T["grid"]};stroke-width:0.8"/>')
        o.append(_t(x(g), TT + rh * len(RATE_ROWS) + 16, f"{g}%", T, 9.5, 400, "muted", "middle"))
    for i, (lab, sub, bqt, post, corp, mkt, ref) in enumerate(RATE_ROWS):
        cy = TT + i * rh + rh / 2
        if i % 2 == 0: o.append(f'<rect x="4" y="{cy - rh / 2:.1f}" width="{W - 8}" height="{rh}" style="fill:{T["soft"]};opacity:.55"/>')
        o.append(_t(10, cy - 2, lab, T, 10.5, 700, "ink")); o.append(_t(10, cy + 12, sub, T, 9.5, 400, "ink2"))
        if mkt:
            a, b = mkt; o.append(f'<rect x="{x(a) - 7:.1f}" y="{cy - 6:.1f}" width="{x(b) - x(a) + 14:.1f}" height="12" rx="6" style="fill:{T["ok"]};opacity:.35"/>')
            o.append(_t(x(b) + 10, cy + 4, (_vn(a, 2).rstrip("0").rstrip(",") + "%" if a == b else f"{_vn(a, 2).rstrip('0').rstrip(',')} – {_vn(b, 1).rstrip('0').rstrip(',')}%"), T, 9.5, 700, "ok"))
        if ref:
            o.append(f'<line x1="{x(ref):.1f}" y1="{cy - 11:.1f}" x2="{x(ref):.1f}" y2="{cy + 11:.1f}" style="stroke:{T["muted"]};stroke-width:2;stroke-dasharray:3 2"/>')
            o.append(_t(x(ref) + 6, cy + 4, "12 tháng lúc đó " + _vn(ref, 1) + "%", T, 9.5, 400, "muted"))
        if corp is not None: o.append(f'<rect x="{x(corp) - 4:.1f}" y="{cy - 4:.1f}" width="8" height="8" style="fill:{T["na"]}"/>')
        if post is not None: o.append(f'<circle cx="{x(post):.1f}" cy="{cy:.1f}" r="7.5" style="fill:none;stroke:{T["box"]};stroke-width:2.2"/>')
        if bqt is not None:
            o.append(f'<circle cx="{x(bqt):.1f}" cy="{cy:.1f}" r="5.5" style="fill:{T["acc"]}"/>')
            o.append(_t(x(bqt), cy - 10, _vn(bqt, 1) + "%", T, 10, 800, "ink", "middle"))
        else:
            o.append(_t(L + 6, cy + 4, "BQT nhận: chưa có chứng từ", T, 9.5, 700, "warn"))
    o.append("</svg>")
    return "".join(o)

# ---------------------------------------------------------------- 4. vong tuan thu 17 quy dinh
def svg_donut(counts, T=PDF, size=190):
    order = [("Không tuân thủ", "crit"), ("Nghi vấn", "warn"), ("Chưa đủ hồ sơ", "na"), ("Một phần", "cau"), ("Tuân thủ", "ok")]
    tot = sum(counts.get(k, 0) for k, _ in order); cx = cy = size / 2; r = size / 2 - 14; sw = 26
    o = [f'<svg viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Tỷ lệ tuân thủ 17 quy định">']
    a0 = -math.pi / 2; gap = 0.035
    for k, col in order:
        n = counts.get(k, 0)
        if not n: continue
        a1 = a0 + 2 * math.pi * n / tot
        s, e = a0 + gap / 2, a1 - gap / 2
        large = 1 if e - s > math.pi else 0
        p = f"M{cx + r * math.cos(s):.2f} {cy + r * math.sin(s):.2f} A{r} {r} 0 {large} 1 {cx + r * math.cos(e):.2f} {cy + r * math.sin(e):.2f}"
        o.append(f'<path d="{p}" style="fill:none;stroke:{T[col]};stroke-width:{sw}"/>')
        am = (s + e) / 2; o.append(_t(cx + r * math.cos(am), cy + r * math.sin(am) + 4.5, str(n), T, 13, 800, "surface", "middle"))
        a0 = a1
    o.append(_t(cx, cy - 2, str(tot), T, 30, 800, "ink", "middle")); o.append(_t(cx, cy + 18, "quy định", T, 11, 400, "ink2", "middle"))
    o.append("</svg>")
    return "".join(o)

# ---------------------------------------------------------------- 5. lai khong ky han tung thang
def svg_interest(T=PDF):
    IC = json.load(open("/home/claude/ssr/interest_check.json"))
    vm = {x["month"]: x for x in IC["v"]}
    rows = [(x["month"], x["actual"] / 1e6, vm[x["month"]]["actual"] / 1e6 if x["month"] in vm else 0.0, x["expected"] / 1e6, vm[x["month"]]["expected"] / 1e6 if x["month"] in vm else 0.0) for x in IC["q"]]
    W, H = 700, 200; L, R, TT, B = 40, 10, 16, 40; iw, ih = W - L - R, H - TT - B; ymax = 1.2
    y = lambda v: TT + ih - min(v, ymax) / ymax * ih
    o = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Lãi không kỳ hạn từng tháng">']
    for g in (0, 0.3, 0.6, 0.9, 1.2):
        o.append(f'<line x1="{L}" x2="{W - R}" y1="{y(g):.1f}" y2="{y(g):.1f}" style="stroke:{T["grid"] if g else T["line"]};stroke-width:0.8"/>')
        o.append(_t(L - 5, y(g) + 3.5, _vn(g, 1), T, 9.5, 400, "muted", "end"))
    bw = iw / len(rows)
    for i, (m, a, b, ea, eb) in enumerate(rows):
        x = L + i * bw + bw * 0.16; w_ = bw * 0.68
        o.append(f'<rect x="{x:.1f}" y="{y(a):.1f}" width="{w_:.1f}" height="{max(1, y(0) - y(a)):.1f}" rx="2" style="fill:{T["bar1"]}"/>')
        if b: o.append(f'<rect x="{x:.1f}" y="{y(a + b):.1f}" width="{w_:.1f}" height="{max(1, y(a) - y(a + b) - 1):.1f}" rx="2" style="fill:{T["s7784"]}"/>')
        o.append(f'<circle cx="{x + w_ / 2:.1f}" cy="{y(ea + eb):.1f}" r="3.2" style="fill:{T["acc"]};stroke:{T["surface"]};stroke-width:1"/>')
        if a > ymax: o.append(_t(x + w_ / 2, y(ymax) + 12, _vn(a, 2), T, 9, 700, "surface", "middle"))
        if i % 2 == 0: o.append(_t(x + w_ / 2, H - B + 14, m[:2] + "/" + m[5:], T, 9, 400, "muted", "middle"))
    for x, col, lab, dot in ((L, "bar1", "TK 999, triệu đồng", False), (L + 140, "s7784", "TK 7784", False), (L + 230, "acc", "Số tính lại theo 0,2%/năm: trùng từng đồng", True)):
        if dot: o.append(f'<circle cx="{x + 5}" cy="{H - 7}" r="3.5" style="fill:{T[col]}"/>')
        else: o.append(f'<rect x="{x}" y="{H - 11}" width="10" height="8" rx="2" style="fill:{T[col]}"/>')
        o.append(_t(x + 15, H - 3, lab, T, 9.5, 400, "ink2"))
    o.append("</svg>")
    return "".join(o)

# ---------------------------------------------------------------- 6. bieu tuong muc (net manh)
ICON_PATHS = {
    "01": '<path d="M12 3v18M5 7h14M7 7l-3 7h6zM17 7l-3 7h6zM8 21h8"/>',
    "02": '<ellipse cx="12" cy="5.5" rx="7" ry="2.5"/><path d="M5 5.5v13c0 1.4 3.1 2.5 7 2.5s7-1.1 7-2.5v-13M5 12c0 1.4 3.1 2.5 7 2.5s7-1.1 7-2.5"/>',
    "03": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 21 21M8 10.5l2 2 3.5-4"/>',
    "04": '<path d="M3 9 12 4l9 5M5 10v8M9.5 10v8M14.5 10v8M19 10v8M3 20h18"/>',
    "05": '<circle cx="9" cy="9" r="5.5"/><path d="M15.5 4.8A5.5 5.5 0 0 1 15 15M6 20h12M14 17l4 3-4 3"/>',
    "06": '<rect x="4" y="3" width="10" height="18"/><rect x="14" y="9" width="6" height="12"/><path d="M7 7h4M7 11h4M7 15h4"/>',
    "07": '<path d="M5 19 19 5"/><circle cx="7" cy="7" r="2.5"/><circle cx="17" cy="17" r="2.5"/>',
    "08": '<rect x="5" y="3" width="14" height="18" rx="1.5"/><path d="M12 3v18M8.5 10l1.5-2 1.5 2M12.5 14l1.5 2 1.5-2"/>',
    "09": '<path d="M6 3h9l4 4v14H6zM15 3v4h4M9 13l2 2 4-4"/>',
    "10": '<path d="M9 6h11M9 12h11M9 18h11M4 6l1 1 2-2M4 12l1 1 2-2M4 18l1 1 2-2"/>',
    "11": '<path d="M5 21V4M5 4h11l-2 4 2 4H5"/>',
    "12": '<path d="M4 20h4v-4h4v-4h4V8h4"/><circle cx="20" cy="5" r="2"/>',
    "A": '<path d="M6 3h9l4 4v14H6zM15 3v4h4M9 12h7M9 16h7"/>', "B": '<path d="M6 3h9l4 4v14H6zM15 3v4h4M9 12h7M9 16h7"/>', "C": '<path d="M6 3h9l4 4v14H6zM15 3v4h4M9 12h7M9 16h7"/>',
}
def icon(no, col="#C8992F", size=17):
    p = ICON_PATHS.get(no)
    if not p: return ""
    return (f'<svg class="sic" viewBox="0 0 24 24" width="{size}" height="{size}" style="fill:none;stroke:{col};stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round">{p}</svg>')

if __name__ == "__main__":
    import os
    d = "/tmp/claude-0/-home-claude/27b76491-7223-55a8-a17f-5bc571aa439a/scratchpad/viz"; os.makedirs(d, exist_ok=True)
    from collections import Counter
    MX = json.load(open("/home/claude/ssr/matrix.json")); cnt = Counter(m["st"] for m in MX)
    pages = [svg_flow(), svg_monthly(), svg_rates(), svg_donut(cnt), svg_interest()]
    fonts = open("/home/claude/ssr/bvp_fonts.css").read()
    html_ = f"<html><head><meta charset='utf-8'><style>{fonts} body{{width:760px;margin:20px}} svg{{width:700px;height:auto;display:block;margin:0 0 24px 0;border:1px solid #eee}}</style></head><body>" + "".join(pages) + "</body></html>"
    open(d + "/viz.html", "w").write(html_)
    print("ok")
