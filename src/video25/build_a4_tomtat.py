# -*- coding: utf-8 -*-
"""Mot trang A4 tom gon toan bo noi dung quy bao tri SSR (07/10/2026). Tong SSR Dieu Hanh, nhan dien SSR, khong TVN."""
import sys, os
sys.path.insert(0, "/home/claude/vshim")
from tvnkit import LOGO
OUT = "/home/claude/ssr/a4_mot_trang"; os.makedirs(OUT, exist_ok=True)
F = open("/home/claude/ssr/bvp_fonts.css").read() + open("/home/claude/ssr/fonts/cormorant.css").read()

ISS = [("1", "986,9 triệu tiền quỹ chuyển vào tài khoản vận hành do chính 6 thành viên Ban quản trị đồng đứng tên, ngày 23/12/2025",
        "Điều 7.2, 7.4, 3.2.a Quy chế thu chi", "Vi phạm đã rõ", "r"),
       ("2", "1,71 tỷ tiền quảng cáo, thuê mặt bằng khu vực chung không vào quỹ; 1,40 tỷ đã chi từ tài khoản này ngoài quy trình",
        "Khoản 4 Điều 153 Luật Nhà ở 2023; Điều 6 Quy chế", "Vi phạm đã rõ", "r"),
       ("3", "13 khoản chi trên 50 triệu, tổng 5,04 tỷ; lớn nhất HNB 1,25 tỷ, Thép Quang 705,8 triệu, Schindler 477,1 triệu",
        "Điều 9.2: trên 50 triệu cần hơn 50% chủ sở hữu đồng ý", "Chờ văn bản cho phép", "o"),
       ("4", "1,69 tỷ chưa truy được tới cùng: 705,8 triệu trả trọn Thép Quang, hàng hóa ghi chung chung; 986,9 triệu chưa rõ người nhận cuối",
        "Điều 6.3: báo giá, nghiệm thu, chứng từ 3 chữ ký", "Chờ chứng từ", "o"),
       ("5", "127,5 tỷ tiền gửi sau tái tục chưa có hợp đồng, xác nhận của ngân hàng; sao kê mới dừng ở 31/05/2026",
        "Điều 3.1.a; Điều 8.8: kiểm toán hằng năm", "Chờ xác nhận ngân hàng", "y")]
Q10 = ["Căn cứ chuyển 986,9 triệu vào tài khoản vận hành", "Bảng chi phí lệch 123,1 triệu", "Căn cứ thu 1,71 tỷ ngoài quỹ",
       "Hồ sơ 1,40 tỷ đã chi, Thành Công 856,8 triệu", "Giữ xe Khởi Sáng Việt trả vượt 67,1 triệu", "Danh mục, hóa đơn 705,8 triệu Thép Quang",
       "Phí bảo trì thang máy Schindler vắng từ 21/01/2025", "Xác nhận 127,5 tỷ tiền gửi sau tái tục", "Tiền quảng cáo Chicilon Media giảm 17,5%",
       "Sao kê ba tài khoản từ 01/06/2026"]
C = {"r": "#A93434", "o": "#C0662A", "y": "#9A7B12", "g": "#1E7A46"}
iss = "".join(f'<tr><td class="n"><span style="background:{C[t]}">{n}</span></td><td>{d}</td><td class="cc">{c}</td>'
              f'<td><span class="st" style="color:{C[t]};border-color:{C[t]}">{s}</span></td></tr>' for n, d, c, s, t in ISS)
q10 = "".join(f'<li><b>{i + 1}</b>{q}</li>' for i, q in enumerate(Q10))

html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{F}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1240px;height:1754px;font-family:'Be Vietnam Pro';color:#1d2a22;background:#F5F7F2;font-size:15.8px;line-height:1.42;overflow:hidden}}
.serif{{font-family:'Cormorant Garamond',serif;font-size-adjust:.52;font-variant-numeric:lining-nums}}
.hd{{background:radial-gradient(900px 420px at 0% 0%,rgba(70,140,95,.55),transparent 70%),linear-gradient(160deg,#24543A,#12301F 60%,#0B1F14);color:#fff;padding:24px 48px 20px;display:flex;gap:26px;align-items:center}}
.hd img.lg{{width:100px;height:100px;border-radius:50%;flex:none}}
.hd .k{{font-size:15px;font-weight:700;letter-spacing:.14em;color:#E3C878}}
.hd h1{{font-size:39px;line-height:1.18;font-weight:700;color:#F1E6C6;margin:4px 0 6px}}
.hd .s{{font-size:16px;color:#CFE0D3}}
.wrap{{padding:16px 48px 0}}
.kp{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}}
.kp div{{background:#fff;border-radius:14px;padding:11px 16px;border-top:4px solid var(--c)}}
.kp b{{display:block;font-size:31px;line-height:1.05;color:var(--c);font-weight:800}}
.kp span{{font-size:14px;color:#4A5A4F}}
h2{{font-size:25px;color:#1E4630;font-weight:700;margin:17px 0 7px;display:flex;align-items:baseline;gap:12px}}
h2 small{{font-family:'Be Vietnam Pro';font-size:14px;color:#687A6D;font-weight:500}}
table{{width:100%;border-collapse:separate;border-spacing:0;background:#fff;border-radius:14px;overflow:hidden}}
th{{background:#1E4630;color:#F1E6C6;text-align:left;font-size:13.5px;font-weight:600;padding:8px 12px}}
td{{padding:7px 12px;border-top:1px solid #E2E9E1;vertical-align:top;font-size:15.6px}}
td.n span{{display:inline-flex;width:28px;height:28px;border-radius:50%;color:#fff;font-weight:800;align-items:center;justify-content:center}}
td.cc{{color:#4A5A4F;font-size:13.5px}}
.st{{display:inline-block;border:1.5px solid;border-radius:999px;padding:2px 10px;font-size:13px;font-weight:700;white-space:nowrap}}
.g2{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
.bx{{background:#fff;border-radius:14px;padding:10px 16px}}
.bx ul{{list-style:none}} .bx li{{padding:3px 0 3px 16px;position:relative}} .bx li:before{{content:"";position:absolute;left:0;top:11px;width:7px;height:7px;border-radius:50%;background:#B08A2E}}
.nd{{background:#EBF0EA;border-left:4px solid #1E4630;border-radius:0 12px 12px 0;padding:10px 16px}}
.nd p{{margin:2px 0}} .nd p:first-child{{font-weight:700;color:#1E4630}}
.q{{columns:2;column-gap:26px;list-style:none;background:#fff;border-radius:14px;padding:12px 18px}}
.q li{{break-inside:avoid;padding:2px 0;font-size:14.5px}} .q li b{{display:inline-block;width:26px;color:#B08A2E}}
.pa{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}}
.pa div{{background:#fff;border-radius:14px;padding:12px 16px;border-top:4px solid var(--c)}}
.pa b{{font-family:'Cormorant Garamond',serif;font-size-adjust:.52;font-size:24px;color:var(--c);display:block}}
.pa span{{font-size:14px}}
.ft{{position:absolute;left:0;right:0;bottom:0;background:#12301F;color:#CFE0D3;font-size:13px;padding:12px 48px;line-height:1.45}}
.ft b{{color:#E3C878}}
</style></head><body>
<div class="hd">{LOGO}<div><div class="k">SỔ QUỸ BẢO TRÌ SSR · TÓM TẮT MỘT TRANG</div>
<h1 class="serif">Tiền quỹ còn đủ, nhưng đi sai đường ở năm chỗ</h1>
<div class="s">Chung cư Nam Sài Gòn Residences · Sao kê 15/08/2024 tới 31/05/2026 · Quy chế thông qua 26/05/2024</div></div></div>
<div class="wrap">
<div class="kp"><div style="--c:#1E7A46"><b>127,15 tỷ</b><span>tiền gốc còn trong quỹ ngày 31/05/2026</span></div>
<div style="--c:#1E7A46"><b>198</b><span>giao dịch khớp số dư tới từng đồng, không rút tiền mặt</span></div>
<div style="--c:#A93434"><b>3</b><span>vi phạm đã rõ trên sao kê: 986,9 triệu; 1,71 tỷ; 1,40 tỷ</span></div>
<div style="--c:#C0662A"><b>5,04 tỷ</b><span>13 khoản chi trên 50 triệu chưa thấy văn bản cho phép</span></div></div>

<h2 class="serif">Năm vấn đề <small>số tiền, quy định liên quan, tình trạng</small></h2>
<table><tr><th style="width:44px"></th><th>Vấn đề</th><th style="width:250px">Quy định</th><th style="width:190px">Tình trạng</th></tr>{iss}</table>

<div class="g2" style="margin-top:14px">
<div><h2 class="serif" style="margin-top:4px">Ban quản trị đã làm đúng</h2><div class="bx"><ul>
<li>9 lệnh chi từ quỹ chuyển thẳng cho nhà thầu, đúng Điều 7.2.</li>
<li>Tiền gốc tăng từ 124,79 tỷ lên 127,15 tỷ nhờ 5,48 tỷ tiền lãi.</li>
<li>105 tỷ gửi có kỳ hạn tại VietinBank, Agribank, lãi 4,7% một năm.</li>
<li>Ba báo cáo quỹ: 14/05/2025, 15/05/2026, 15/09/2026.</li></ul></div></div>
<div><h2 class="serif" style="margin-top:4px">Mức độ và nguyên nhân</h2><div class="nd">
<p>16 dấu hiệu: 3 mức Đỏ, 7 mức Cam, 6 mức Vàng.</p>
<p>9 do thiếu năng lực, 2 do sơ suất giấy tờ, 1 chưa phát sinh sai.</p>
<p>4 chưa loại trừ khả năng có chủ đích, cần chứng từ để kết luận.</p>
<p>Chưa có khoản nào đủ căn cứ trách nhiệm hình sự.</p></div></div></div>

<div class="g2" style="margin-top:2px">
<div><h2 class="serif">Khung xử lý</h2><div class="nd">
<p>Đã rõ trên sao kê thì phải khắc phục ngay.</p>
<p>Đưa tiền khu vực chung về quỹ, có chứng từ từng khoản; Ban quản trị có thể bị phạt 50 đến 60 triệu và buộc bồi hoàn.</p>
<p>Khoản đang chờ: có chứng từ hợp lệ thì khép lại, không có thì bồi hoàn quỹ theo Điều 10.1.</p></div></div>
<div><h2 class="serif">Quy chế đang áp dụng</h2><div class="bx"><ul>
<li>Bản Hội nghị thông qua ngày 26/05/2024, 42 trang.</li>
<li>So với dự thảo, chỉ đổi cách tổ chức Ban quản trị: 9 thành viên, 2 Phó ban, thù lao 6/5/4 triệu.</li>
<li>Các điều kiểm soát tiền quỹ giữ nguyên.</li>
<li>Điều 6.1.g yêu cầu công khai chi tiêu quỹ hằng tháng.</li></ul></div></div></div>

<h2 class="serif">Mười câu hỏi đã gửi Ban quản trị ngày 29/09/2026 <small>mỗi câu kèm chứng từ cần có</small></h2>
<ul class="q">{q10}</ul>

<h2 class="serif">Hội nghị quyết định theo điều kiện, xét riêng từng thành viên</h2>
<div class="pa"><div style="--c:#1E7A46"><b>Giữ</b><span>Tiền đã về đủ quỹ; có văn bản cho phép, chứng từ; ngân hàng xác nhận tiền gửi.</span></div>
<div style="--c:#C0662A"><b>Xem xét thêm</b><span>Đã khắc phục hai vấn đề đầu nhưng thiếu chứng từ: hạn 30 ngày, kiểm toán độc lập, tạm dừng chi mới trên 50 triệu.</span></div>
<div style="--c:#A93434"><b>Bãi nhiệm</b><span>Không khắc phục, không có văn bản hoặc né tránh chứng từ; khoản không chứng minh được thì bồi hoàn quỹ.</span></div></div>

<h2 class="serif">Cư dân làm gì trước Hội nghị</h2>
<div class="bx"><ul style="columns:3;column-gap:24px">
<li>Đọc 3 file trong thư mục 0 của thư mục chia sẻ, khoảng 20 phút.</li>
<li>Ghi ý kiến vào phiếu mặt sau tờ Năm vấn đề, mang tới Hội nghị.</li>
<li>Theo dõi câu trả lời của Ban quản trị; góp thêm chứng từ nếu có.</li></ul></div>
</div>
<div class="ft"><b>Xem thêm:</b> bộ clip, báo cáo đầy đủ, Excel và sao kê gốc trong thư mục chia sẻ. Mọi con số truy được về sao kê ngân hàng.<br>
Phân tích độc lập của cư dân, không phải văn bản của chủ đầu tư, Ban quản trị hay đơn vị quản lý vận hành. Các nhận định là dấu hiệu cần làm rõ, không phải cáo buộc. Nội dung pháp lý để tham khảo, không thay ý kiến luật sư.</div>
</body></html>"""
open(f"{OUT}/a4.html", "w").write(html)
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1240, "height": 1754}, device_scale_factor=2)
    pg.goto(f"file://{OUT}/a4.html"); pg.wait_for_timeout(700)
    print("noi dung cao", pg.evaluate("(()=>{const w=document.querySelector('.wrap').getBoundingClientRect(); const f=document.querySelector('.ft').getBoundingClientRect(); return [Math.round(w.bottom), Math.round(f.top)]})()"))
    pg.screenshot(path=f"{OUT}/SSR_Quy_bao_tri_tom_tat_mot_trang_A4.png"); b.close()
