# -*- coding: utf-8 -*-
"""Anh danh muc bo clip Quy bao tri (04/10/2026): chu de va thoi luong THUC cua 1 ban day du, 6 phan ngang, 11 clip doc.
Nhan dien SSR, khong TVN. Thoi luong doc tu *_info.json do video_ssr_25 ghi."""
import json, os, sys, glob
sys.path.insert(0, "/home/claude/vshim")
from tvnkit import LOGO
sys.path.insert(0, "/home/claude/ssr")
os.environ.setdefault("CLIP_RES", "1080")
import video_ssr_25 as V

D = V.OUT
def info(name):
    f = f"{D}/{name}_info.json"
    return json.load(open(f)) if os.path.exists(f) else None
def mmss(x): x = int(round(x)); return f"{x // 60}:{x % 60:02d}"
def E(s): return str(s).replace("&", "&amp;").replace("<", "&lt;")

full = info("SSR_Quy_bao_tri_ban_day_du_25p")
parts = [(n, V.PARTS[n]["name"], info(f"SSR_Quy_bao_tri_phan_{n}_tren_6")) for n in V.PARTS]
docs = [(k, V.SEG[k]["short"], info(f"SSR_Quy_bao_tri_clip_doc_{k:02d}_tren_11")) for k in V.SEG]
short = info("SSR_Quy_bao_tri_clip_doc_tom_tat")
missing = [x for x in [full, short] + [p[2] for p in parts] + [d[2] for d in docs] if x is None]
if missing and "draft" not in sys.argv: raise SystemExit("chua du clip")
dur = lambda i: mmss(i["duration"]) if i else "--:--"
tot_p = sum(p[2]["duration"] for p in parts if p[2]); tot_d = sum(d[2]["duration"] for d in docs if d[2])

chap = full["chapters"] if full else []
chap = [c for c in chap if not c.split(" ", 1)[1].startswith(("Mở đầu", "Liên hệ"))]
chap_html = "".join(f'<div class="ch"><b>{E(c.split(" ")[0])}</b><span>{E(c.split(" ", 1)[1])}</span></div>' for c in chap)
part_html = "".join(f'<div class="row"><div class="no">{n}</div><div class="tt">{E(nm)}</div><div class="du">{dur(i)}</div></div>' for n, nm, i in parts)
drow = lambda k, nm, i: f'<div class="row s"><div class="no">{k}</div><div class="tt">{E(nm)}</div><div class="du">{dur(i)}</div></div>'
doc_l = "".join(drow(*d) for d in docs[:6]); doc_r = "".join(drow(*d) for d in docs[6:])

CSS = open("/home/claude/ssr/bvp_fonts.css").read() + open("/home/claude/ssr/fonts/cormorant.css").read()
html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1600px;padding-bottom:44px;font-family:'Be Vietnam Pro';color:#1b2433;background:#F5F7F2}}
.hd{{background:radial-gradient(900px 500px at 0% 0%,rgba(70,140,95,.55),transparent 70%),linear-gradient(160deg,#24543A,#12301F 60%,#0B1F14);color:#fff;padding:56px 72px 48px;display:flex;gap:36px;align-items:center}}
.hd img.lg{{width:150px;height:150px;border-radius:50%;box-shadow:0 0 0 6px rgba(255,255,255,.12)}}
.hd .k{{font-size:26px;letter-spacing:.14em;color:#E3C878;font-weight:600}}
.hd h1{{font-family:'Cormorant Garamond',serif;font-size-adjust:.52;font-variant-numeric:lining-nums;font-size:66px;line-height:1.3;font-weight:700;color:#F1E6C6;margin:6px 0 16px}}
.hd .s{{font-size:26px;color:#CFE3D6}}
.wrap{{padding:40px 72px 0}}
.sec{{background:#fff;border-radius:22px;padding:30px 38px;margin-bottom:28px;box-shadow:0 2px 10px rgba(19,40,74,.07)}}
.sh{{display:flex;align-items:baseline;gap:18px;margin-bottom:18px}}
.sh .tag{{background:#12301F;color:#fff;font-weight:700;font-size:24px;padding:6px 16px;border-radius:999px}}
.sh h2{{font-family:'Cormorant Garamond',serif;font-size-adjust:.52;font-variant-numeric:lining-nums;font-size:40px;color:#1E4630;font-weight:700}}
.sh .m{{margin-left:auto;font-size:24px;color:#566459}}
.big{{display:flex;gap:34px;align-items:center}}
.big .du{{font-size:92px;font-weight:700;color:#A8832E;line-height:1}}
.big .du small{{display:block;font-size:22px;color:#566459;font-weight:500;margin-top:6px}}
.chs{{display:grid;grid-template-columns:1fr 1fr;gap:6px 30px;flex:1}}
.ch{{display:flex;gap:14px;font-size:22px;line-height:1.35}}
.ch b{{color:#12301F;min-width:64px}}
.row{{display:grid;grid-template-columns:60px 1fr 110px;align-items:center;gap:18px;padding:12px 6px;border-top:1px solid #E2E9E1;font-size:28px}}
.row:first-of-type{{border-top:none}}
.row .no{{width:50px;height:50px;border-radius:50%;background:#E9EFE7;color:#12301F;font-weight:700;display:flex;align-items:center;justify-content:center;font-size:24px}}
.row .du{{text-align:right;font-weight:700;color:#A8832E}}
.grid2{{display:grid;grid-template-columns:1fr 1fr;column-gap:34px}}
.row.s{{font-size:24px;grid-template-columns:50px 1fr 84px;padding:10px 4px}}
.row.s .no{{width:42px;height:42px;font-size:20px}}
.use{{display:flex;gap:16px;margin-top:4px;font-size:22px;color:#566459}}
.ft{{padding:6px 72px 0;font-size:21px;color:#566459;line-height:1.45}}
.ft b{{color:#12301F}}
</style></head><body>
<div class="hd">{LOGO}<div><div class="k">SỔ QUỸ BẢO TRÌ SSR · BỘ CLIP</div><h1>Quỹ bảo trì: sai ở đâu, tới mức nào, Hội nghị quyết định gì</h1>
<div class="s">Sao kê 15/08/2024 tới 31/05/2026 · Phát hành 04/10/2026</div></div></div>
<div class="wrap">
<div class="sec"><div class="sh"><span class="tag">1 bản đầy đủ</span><h2>Clip ngang, toàn bộ nội dung</h2><span class="m">Chiếu Hội nghị, xem trên máy tính, TV</span></div>
<div class="big"><div class="du">{dur(full)}<small>phút · có chia chương</small></div><div class="chs">{chap_html}</div></div></div>
<div class="sec"><div class="sh"><span class="tag">6 phần ngang</span><h2>Chiếu từng phần tại Hội nghị</h2><span class="m">Tổng {mmss(tot_p)} phút</span></div>{part_html}</div>
<div class="sec"><div class="sh"><span class="tag">Clip dọc tóm tắt</span><h2>Năm vấn đề trong một clip ngắn</h2><span class="m">Gửi trước, mời xem bộ đầy đủ</span></div><div class="row"><div class="no">★</div><div class="tt">Quỹ bảo trì: năm vấn đề trong 90 giây</div><div class="du">{dur(short)}</div></div></div>
<div class="sec"><div class="sh"><span class="tag">11 clip dọc</span><h2>Xem trên điện thoại, gửi lẻ từng chủ đề</h2><span class="m">Tổng {mmss(tot_d)} phút</span></div>
<div class="grid2"><div>{doc_l}</div><div>{doc_r}</div></div></div>
</div>
<div class="ft"><b>Nơi xem:</b> thư mục chia sẻ, mục 1.5 Clip. Mỗi clip có câu mở và câu kết riêng, xem lẻ vẫn hiểu.<br>
Phân tích độc lập phục vụ giám sát của cư dân, không phải văn bản của chủ đầu tư, Ban quản trị hay đơn vị quản lý vận hành. Các nhận định là dấu hiệu cần làm rõ, không phải cáo buộc.</div>
</body></html>"""
out_html = f"{D}/danh_muc_clip.html"; open(out_html, "w").write(html)
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1600, "height": 1000})
    pg.goto("file://" + out_html); pg.wait_for_timeout(600)
    h = pg.evaluate("document.body.scrollHeight"); print("cao", h)
    pg.screenshot(path=f"{D}/SSR_Danh_muc_bo_clip_Quy_bao_tri.png", full_page=True); b.close()
print("ok")
