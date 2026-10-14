# -*- coding: utf-8 -*-
"""Ma QR dan toi trang So quy bao tri SSR: anh A4 de in dan bang tin, ban PDF, ban Word sua duoc, anh 16:9 de chieu Hoi nghi. Nhan dien SSR."""
import base64, io, os, segno, cv2
from playwright.sync_api import sync_playwright
O = "/home/claude/ssr/qr"; URL = "https://claude.ai/artifact/5ZrS77qvrnpcY3R3bXqGGe"
q = segno.make(URL, error="q"); q.save(f"{O}/qr.png", scale=24, border=2, dark="#12301F", light="#FFFFFF")
b64 = lambda p: base64.b64encode(open(p, "rb").read()).decode()
QR = "data:image/png;base64," + b64(f"{O}/qr.png"); LOGO = "data:image/png;base64," + b64("/home/claude/ssr/crops/logo_ssr_512.png")
CSS = open("/home/claude/ssr/bvp_fonts.css").read() + open("/home/claude/ssr/fonts/cormorant.css").read()
SER = "font-family:'Cormorant Garamond',serif;font-size-adjust:.52;font-variant-numeric:lining-nums;font-weight:700;color:#F1E6C6"
INSIDE = ["Câu trả lời ngắn: tiền quỹ có mất không", "Năm vấn đề, mức độ và khung xử lý", "198 giao dịch của ba tài khoản, tra cứu được",
          "Mười câu hỏi đã gửi Ban quản trị", "Bộ clip: bản đầy đủ 22 phút, 6 phần, 11 clip dọc, tóm tắt 90 giây"]
STEPS = [("1", "Mở camera điện thoại, hướng vào mã"), ("2", "Bấm vào đường dẫn hiện ra"), ("3", "Không cần đăng nhập, không cần cài ứng dụng")]
DISC = "Phân tích độc lập phục vụ giám sát của cư dân, không phải văn bản của chủ đầu tư, Ban quản trị hay đơn vị quản lý vận hành. Các nhận định là dấu hiệu cần làm rõ, không phải cáo buộc."
BG = "background:radial-gradient(1200px 900px at 0% 0%,rgba(70,140,95,.55),transparent 70%),linear-gradient(160deg,#24543A,#12301F 55%,#0B1F14)"
A4 = f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}
@page{{size:A4;margin:0}}*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1240px;height:1754px;font-family:'Be Vietnam Pro';color:#fff;{BG};position:relative;overflow:hidden;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.fr{{position:absolute;inset:28px;border:2px solid rgba(227,200,120,.55);border-radius:30px}}
.hd{{position:absolute;left:84px;top:84px;display:flex;gap:24px;align-items:center}}
.hd img{{width:120px;height:120px;border-radius:50%;box-shadow:0 0 0 6px rgba(255,255,255,.12)}}
.hd b{{display:block;font-size:32px;letter-spacing:.12em;color:#E3C878;font-weight:800}} .hd span{{font-size:24px;color:rgba(255,255,255,.82)}}
h1{{position:absolute;left:84px;right:84px;top:262px;{SER};font-size:72px;line-height:1.16}} h1 em{{font-style:normal;color:#E3C878}}
.qrb{{position:absolute;left:50%;top:575px;transform:translateX(-50%);width:580px;background:#fff;border-radius:28px;padding:26px;box-shadow:0 18px 50px rgba(0,0,0,.35)}}
.qrb img{{display:block;width:100%}}
.cap{{position:absolute;left:0;right:0;top:1222px;text-align:center;font-size:34px;font-weight:700;color:#E3C878}}
.st{{position:absolute;left:84px;right:84px;top:1290px;display:grid;grid-template-columns:repeat(3,1fr);gap:18px}}
.st div{{background:rgba(255,255,255,.08);border:1px solid rgba(227,200,120,.35);border-radius:18px;padding:18px 20px;font-size:23px;line-height:1.38;display:flex;gap:14px;align-items:flex-start}}
.st i{{font-style:normal;flex:none;width:40px;height:40px;border-radius:50%;background:#E3C878;color:#12301F;font-weight:800;display:grid;place-items:center;font-size:22px}}
.in{{position:absolute;left:84px;right:84px;top:1448px}}
.in b{{font-size:22px;letter-spacing:.12em;color:#E3C878;font-weight:700}}
.in ul{{list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:6px 30px;margin-top:10px}}
.in li{{font-size:22px;line-height:1.4;color:#EAF2EC;padding-left:22px;position:relative}} .in li::before{{content:"";position:absolute;left:0;top:12px;width:9px;height:9px;border-radius:50%;background:#E3C878}}
.in li:last-child{{grid-column:1/-1}}
.ft{{position:absolute;left:84px;right:84px;bottom:70px;font-size:17px;line-height:1.45;color:rgba(255,255,255,.68)}} .ft u{{text-decoration:none;color:#CFE3D6}}
</style></head><body><div class="fr"></div>
<div class="hd"><img src="{LOGO}"><div><b>SỔ QUỸ BẢO TRÌ SSR</b><span>Chung cư Nam Sài Gòn Residences</span></div></div>
<h1>Quỹ bảo trì chung cư: xem <em>phân tích và bộ clip</em> ngay trên điện thoại</h1>
<div class="qrb"><img src="{QR}"></div>
<div class="cap">Quét mã bằng camera điện thoại</div>
<div class="st">{''.join(f'<div><i>{n}</i><span>{t}</span></div>' for n, t in STEPS)}</div>
<div class="in"><b>TRONG TRANG CÓ</b><ul>{''.join(f'<li>{x}</li>' for x in INSIDE)}</ul></div>
<div class="ft">Đường dẫn: <u>{URL.replace('https://', '')}</u> · Cập nhật 14/10/2026<br>{DISC}</div></body></html>"""
W = f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1920px;height:1080px;font-family:'Be Vietnam Pro';color:#fff;{BG};position:relative;overflow:hidden}}
.fr{{position:absolute;inset:26px;border:2px solid rgba(227,200,120,.55);border-radius:28px}}
.hd{{position:absolute;left:96px;top:86px;display:flex;gap:22px;align-items:center}}
.hd img{{width:110px;height:110px;border-radius:50%;box-shadow:0 0 0 6px rgba(255,255,255,.12)}}
.hd b{{display:block;font-size:30px;letter-spacing:.12em;color:#E3C878;font-weight:800}} .hd span{{font-size:23px;color:rgba(255,255,255,.82)}}
h1{{position:absolute;left:96px;width:1020px;top:250px;{SER};font-size:84px;line-height:1.16}} h1 em{{font-style:normal;color:#E3C878}}
.st{{position:absolute;left:96px;width:1000px;top:625px;display:flex;flex-direction:column;gap:18px}}
.st div{{display:flex;gap:18px;align-items:center;font-size:34px}}
.st i{{font-style:normal;flex:none;width:56px;height:56px;border-radius:50%;background:#E3C878;color:#12301F;font-weight:800;display:grid;place-items:center;font-size:28px}}
.qrb{{position:absolute;right:120px;top:170px;width:640px;background:#fff;border-radius:30px;padding:26px;box-shadow:0 18px 50px rgba(0,0,0,.35)}}
.qrb img{{display:block;width:100%}}
.cap{{position:absolute;right:120px;width:640px;top:850px;text-align:center;font-size:30px;font-weight:700;color:#E3C878}}
.ft{{position:absolute;left:96px;right:96px;bottom:62px;font-size:18px;color:rgba(255,255,255,.66)}}
</style></head><body><div class="fr"></div>
<div class="hd"><img src="{LOGO}"><div><b>SỔ QUỸ BẢO TRÌ SSR</b><span>Chung cư Nam Sài Gòn Residences</span></div></div>
<h1>Xem <em>phân tích Quỹ bảo trì và bộ clip</em> ngay trên điện thoại</h1>
<div class="st">{''.join(f'<div><i>{n}</i><span>{t}</span></div>' for n, t in STEPS)}</div>
<div class="qrb"><img src="{QR}"></div><div class="cap">Quét mã bằng camera điện thoại</div>
<div class="ft">Phân tích độc lập của cư dân, không phải văn bản của chủ đầu tư, Ban quản trị hay đơn vị quản lý vận hành.</div></body></html>"""
open(f"{O}/a4.html", "w").write(A4); open(f"{O}/w.html", "w").write(W)
NA = "Mã QR - Sổ quỹ bảo trì SSR (A4 in dán bảng tin)"; NW = "Mã QR - Sổ quỹ bảo trì SSR (chiếu Hội nghị 16x9)"
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1240, "height": 1754}, device_scale_factor=2); pg.goto(f"file://{O}/a4.html"); pg.wait_for_timeout(600)
    over = pg.evaluate("(()=>{const a=document.querySelector('.in').getBoundingClientRect(), f=document.querySelector('.ft').getBoundingClientRect(), s=document.querySelector('.st').getBoundingClientRect(), c=document.querySelector('.cap').getBoundingClientRect(), q=document.querySelector('.qrb').getBoundingClientRect(), h=document.querySelector('h1').getBoundingClientRect(); return [h.bottom<q.top, q.bottom<c.top, c.bottom<s.top, s.bottom<a.top, a.bottom<f.top]})()")
    print("A4 khong chong:", over)
    pg.screenshot(path=f"{O}/{NA}.png"); pg.pdf(path=f"{O}/{NA}.pdf", width="210mm", height="297mm", print_background=True, scale=1/(1240/793.7))
    pw = b.new_page(viewport={"width": 1920, "height": 1080}); pw.goto(f"file://{O}/w.html"); pw.wait_for_timeout(600)
    print("16:9 khong chong:", pw.evaluate("(()=>{const s=document.querySelector('.st').getBoundingClientRect(), f=document.querySelector('.ft').getBoundingClientRect(), h=document.querySelector('h1').getBoundingClientRect(); return [h.bottom<s.top, s.bottom<f.top, h.right<document.querySelector('.qrb').getBoundingClientRect().left]})()"))
    pw.screenshot(path=f"{O}/{NW}.png"); b.close()
det = cv2.QRCodeDetector()
for f in [f"{O}/{NA}.png", f"{O}/{NW}.png"]:
    im = cv2.imread(f); im = cv2.resize(im, (im.shape[1] // 2, im.shape[0] // 2)); v, *_ = det.detectAndDecode(im); print("quet:", v == URL, os.path.basename(f))
# ban Word sua duoc
from docx import Document
from docx.shared import Pt, Mm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
d = Document(); s = d.sections[0]; s.page_width, s.page_height = Mm(210), Mm(297); s.left_margin = s.right_margin = Mm(20); s.top_margin = s.bottom_margin = Mm(16)
st = d.styles["Normal"]; st.font.name = "Times New Roman"; st.font.size = Pt(13)
st.element.rPr.rFonts.set("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}eastAsia", "Times New Roman")
G = RGBColor(0x1E, 0x46, 0x30); GO = RGBColor(0xA8, 0x83, 0x2E)
def para(t, size=13, bold=False, color=None, align=None, after=6):
    p = d.add_paragraph(); r = p.add_run(t); r.font.size = Pt(size); r.bold = bold
    if color: r.font.color.rgb = color
    if align: p.alignment = align
    p.paragraph_format.space_after = Pt(after); return p
p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.add_run().add_picture("/home/claude/ssr/crops/logo_ssr_512.png", width=Mm(22))
para("SỔ QUỸ BẢO TRÌ SSR", 15, True, GO, WD_ALIGN_PARAGRAPH.CENTER, 0); para("Chung cư Nam Sài Gòn Residences", 12, False, None, WD_ALIGN_PARAGRAPH.CENTER, 12)
para("Quỹ bảo trì chung cư: xem phân tích và bộ clip ngay trên điện thoại", 22, True, G, WD_ALIGN_PARAGRAPH.CENTER, 10)
p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.add_run().add_picture(f"{O}/qr.png", width=Mm(78))
para("Quét mã bằng camera điện thoại", 15, True, GO, WD_ALIGN_PARAGRAPH.CENTER, 8)
for n, t in STEPS: para(f"{n}. {t}", 13, False, None, WD_ALIGN_PARAGRAPH.CENTER, 2)
para("", 6); para("TRONG TRANG CÓ", 12, True, G, None, 2)
for x in INSIDE: para("•  " + x, 12.5, False, None, None, 1)
para("", 6); para("Đường dẫn: " + URL.replace("https://", "") + " · Cập nhật 14/10/2026", 10.5, False, RGBColor(0x55, 0x55, 0x55), None, 2)
para(DISC, 10.5, False, RGBColor(0x55, 0x55, 0x55), None, 0)
d.save(f"{O}/{NA}.docx"); print("docx ok")
