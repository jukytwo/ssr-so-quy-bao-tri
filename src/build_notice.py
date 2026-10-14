# -*- coding: utf-8 -*-
"""Anh thong bao cong khai (A4, 1800x2546): muoi cau hoi da gui Ban quan tri bang cong van, kem khoi HIEU DUNG VAN DE ban gon.
Cung khung voi ba anh trong tam; logo SSR, khong nhan dien TVN, khong neu ten ca nhan, khong so trang."""
import base64, html, os
os.chdir("/home/claude/ssr")
from keymsg import km_compact_html, KMC_CSS

E = lambda s: html.escape(str(s), quote=False)
LOGO = "data:image/png;base64," + base64.b64encode(open("crops/logo_192.png", "rb").read()).decode()
FONTS = open("bvp_fonts.css").read()

# (chu de, cau hoi) - cung noi dung voi cong van (muc I.1, I.2, Phu luc 1)
QS = [
 ("986,9 triệu", "Vì sao ngày 23/12/2025 quỹ chuyển 986,9 triệu sang tài khoản vận hành để hoàn ứng 6 khoản chi, thay vì chuyển thẳng cho nhà thầu? Đề nghị cung cấp sao kê tài khoản 118002976372 từ 01/08/2025 và hợp đồng, hóa đơn, biên bản nghiệm thu của 6 khoản."),
 ("Bảng chi phí", "Bảng chi phí trong Báo cáo 03-2026/BC-BQTSSR ngày 15/05/2026 ghi 863,8 triệu cho thang máy, phòng cháy, máy phát điện, thấp hơn khoản hoàn ứng 123,1 triệu: đề nghị cung cấp bảng kê từng khoản và giải thích phần chênh."),
 ("Khu vực chung", "Căn cứ nào để thu 1,71 tỷ tiền quảng cáo của Chicilon Media, Hưng Thái và tiền thuê mặt bằng của Viễn thông ACT vào tài khoản 117002997784 thay vì tài khoản quỹ theo khoản 4 Điều 153 Luật Nhà ở 2023? Khi nào chuyển số dư và các khoản thu về quỹ?"),
 ("Chi 1,40 tỷ", "1,40 tỷ chi sửa chữa, mua sắm từ tài khoản 117002997784, trong đó Công ty Thành Công nhận 856,8 triệu qua 4 hợp đồng: đề nghị cung cấp dự toán, 3 báo giá, hợp đồng, biên bản nghiệm thu từng hợp đồng."),
 ("Giữ xe", "Hệ thống giữ xe (Khởi Sáng Việt, hợp đồng 18KSVSSR08082025): tổng đã trả 356,4 triệu, cao hơn khoảng 67,1 triệu so với giá trị suy ra từ khoản tạm ứng 40%. Đề nghị cung cấp hợp đồng, phụ lục phát sinh, biên bản khảo sát, nghiệm thu, quyết toán."),
 ("705,8 triệu", "Khoản 705,8 triệu trả Công ty Thép Quang mua thiết bị ngày 24/04/2026 được trả đủ một lần: đề nghị cung cấp danh mục thiết bị, hóa đơn, biên bản giao nhận và 3 báo giá."),
 ("Thang máy", "Vì sao phí bảo trì thang máy Schindler định kỳ khoảng 57,5 triệu mỗi tháng không còn chi từ tài khoản quỹ từ 21/01/2025? Đề nghị cung cấp hợp đồng bảo trì, xác nhận công nợ của Schindler, biên bản khảo sát hoặc kiểm tra sự cố, báo giá và nghiệm thu từng hợp đồng sửa chữa, giấy kiểm định còn hiệu lực của từng thang."),
 ("Tiền gửi", "Đề nghị cung cấp hợp đồng và giấy xác nhận tại quầy của 127,5 tỷ tiền gửi tại VietinBank và Agribank sau đợt tái tục tháng 8/2026 với lãi 8% một năm."),
 ("Quảng cáo", "Hợp đồng quảng cáo với Chicilon Media ký lại ngày 05/01/2025 giảm từ khoảng 86,98 triệu xuống 71,8 triệu mỗi tháng: vì sao giảm, có mời chào giá cạnh tranh không?"),
 ("Sao kê", "Sổ phụ Agribank in ngày 04/09/2026 nhưng chỉ lấy tới 31/05/2026: vì sao, và đề nghị cung cấp sao kê ba tài khoản từ 01/06/2026 tới nay, giai đoạn có ba khoản tiền gửi 110 tỷ đáo hạn và khoảng 5,17 tỷ tiền lãi."),
]
assert len(QS) == 10
for t, q in QS:
    assert "→" not in q and "->" not in q
# kiem tra so lieu dung chung
assert round((86.98 - 71.8) * 12, 1) == 182.2 and round(1 - 71.8 / 86.98, 3) == 0.175

CSS = FONTS + KMC_CSS + """
*{box-sizing:border-box;margin:0;padding:0}
body{width:1800px;height:2546px;background:#fff;color:#141414;font-family:'Liberation Serif','Times New Roman',serif;font-size:29px;line-height:1.42}
.pg{height:2546px;padding:64px 88px 56px;display:flex;flex-direction:column}
.hdr,.eb,h1,.intro,.q .n,.q .tp,.foot{font-family:'Be Vietnam Pro','Liberation Sans',sans-serif}
.hdr{display:flex;align-items:center;gap:22px;border-bottom:5px solid #1F3864;padding-bottom:18px}
.hdr img{width:96px;height:96px;border-radius:50%}
.hdr .t1{font-weight:800;font-size:29px;letter-spacing:.05em;color:#1F3864}
.hdr .t2{font-size:22px;color:#4A5566;margin-top:2px}
.hdr .pn{margin-left:auto;text-align:right;font-weight:700;color:#C8992F;font-size:24px;line-height:1.3}
.hdr .pn b{display:block;font-size:40px;color:#1F3864}
.eb{margin-top:28px;font-weight:700;font-size:24px;letter-spacing:.14em;text-transform:uppercase;color:#8A6A1E}
h1{font-weight:800;font-size:62px;line-height:1.12;color:#1F3864;margin-top:6px;letter-spacing:-.01em}
.intro{font-size:25px;line-height:1.5;color:#3d4656;margin-top:14px}
.intro b{color:#1F3864}
.kmz{zoom:2.14;margin-top:9px}
.qs{margin-top:26px;border-top:3px solid #1F3864}
.q{display:grid;grid-template-columns:62px 250px 1fr;gap:0 18px;align-items:start;padding:21px 0 20px;border-bottom:1.5px solid #E3E8EF}
.q .n{width:52px;height:52px;border-radius:50%;background:#C8992F;color:#fff;font-weight:800;font-size:26px;display:grid;place-items:center;margin-top:2px}
.q .tp{font-weight:800;font-size:25px;color:#1F3864;line-height:1.25;padding-top:12px}
.q .tx{font-size:28px;line-height:1.42}
.foot{margin-top:auto;padding-top:16px;border-top:3px solid #C8992F;display:flex;justify-content:space-between;gap:30px;font-size:19px;color:#4A5566;line-height:1.35}
.foot b{color:#1F3864}
"""

qh = "".join(f'<div class="q"><div class="n">{i}</div><div class="tp">{E(t)}</div><div class="tx">{E(q)}</div></div>' for i, (t, q) in enumerate(QS, 1))
PAGE = (f'<!doctype html><html lang="vi"><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="pg">'
        f'<div class="hdr"><img src="{LOGO}" alt=""><div><div class="t1">SỔ QUỸ BẢO TRÌ · CHUNG CƯ NAM SÀI GÒN RESIDENCES</div>'
        f'<div class="t2">Nhóm cư dân giám sát quỹ bảo trì · thông tin cho cư dân</div></div><div class="pn"><b>10</b>câu hỏi gửi BQT</div></div>'
        '<div class="eb">Cư dân cùng theo dõi câu trả lời</div>'
        '<h1>Mười câu hỏi cần Ban quản trị làm rõ về quỹ bảo trì</h1>'
        '<div class="intro">Các câu hỏi đã được gửi Ban quản trị bằng văn bản ngày ....../....../2026, <b>đề nghị trả lời trong 15 ngày</b>. '
        'Mỗi câu gắn với một hồ sơ cụ thể để cư dân theo dõi được câu trả lời.</div>'
        f'<div class="kmz">{km_compact_html(E)}</div>'
        f'<div class="qs">{qh}</div>'
        '<div class="foot"><div><b>Nguồn:</b> 8 sao kê ngân hàng của ba tài khoản, 15/08/2024 – 31/05/2026; tài liệu Ban quản trị gửi ngày 28/09/2026.</div>'
        '<div style="text-align:right;max-width:820px">Câu hỏi nhằm làm rõ thông tin, không nhằm cáo buộc cá nhân nào. Tình trạng cung cấp từng hồ sơ được cập nhật trên dashboard Sổ quỹ bảo trì SSR.</div></div>'
        '</div></body></html>')

if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    os.makedirs("a4", exist_ok=True)
    open("a4/muoi_cau_hoi.html", "w", encoding="utf-8").write(PAGE)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1800, "height": 2546}, device_scale_factor=1)
        pg.goto("file:///home/claude/ssr/a4/muoi_cau_hoi.html"); pg.evaluate("() => document.fonts.ready"); pg.wait_for_timeout(500)
        m = pg.evaluate("() => { const f=document.querySelector('.foot').getBoundingClientRect(); const q=document.querySelector('.qs').getBoundingClientRect();"
                        " return {qsBottom: Math.round(q.bottom), footTop: Math.round(f.top), sh: document.documentElement.scrollHeight}; }")
        print(m)
        pg.screenshot(path="a4/SSR_Muoi_cau_hoi_can_lam_ro.png", full_page=False)
        b.close()
