# -*- coding: utf-8 -*-
"""Anh chu de cho tung clip (04/10/2026): 1 ban day du + 6 phan ngang (1920x1080), 11 clip doc (1080x1920).
Tong mau logo SSR (xanh luc bao, vang kim), nhan dien SSR, khong TVN. Thoi luong lay tu *_info.json."""
import json, os, sys, re
sys.path.insert(0, "/home/claude/vshim")
from tvnkit import LOGO
sys.path.insert(0, "/home/claude/ssr"); os.environ.setdefault("CLIP_RES", "1080")
import video_ssr_25 as V
D = V.OUT; OUTD = f"{D}/anh_chu_de"; os.makedirs(OUTD, exist_ok=True)
CSS_F = open("/home/claude/ssr/bvp_fonts.css").read() + open("/home/claude/ssr/fonts/cormorant.css").read()
def E(s): return str(s).replace("&", "&amp;").replace("<", "&lt;")
def rich(s): return re.sub(r"\*\*(.+?)\*\*", r"<em>\1</em>", E(s))
def dur(name):
    i = json.load(open(f"{D}/{name}_info.json")); x = int(round(i["duration"])); return f"{x // 60}:{x % 60:02d}", f"{x // 60} phút {x % 60:02d} giây"
TONE = {"r": "#F2A3A3", "o": "#F4C08F", "y": "#EBCB7A", "g": "#8FE0B0", "n": "#FFFFFF"}

BASE = """*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Be Vietnam Pro';color:#fff;overflow:hidden;
background:radial-gradient(1300px 900px at 0% 0%,rgba(70,140,95,.55),transparent 70%),linear-gradient(160deg,#24543A,#12301F 55%,#0B1F14)}
.frame{position:absolute;inset:26px;border:2px solid rgba(227,192,112,.55);border-radius:28px}
.br{display:flex;align-items:center;gap:22px}
.br img.lg{border-radius:50%;box-shadow:0 0 0 6px rgba(255,255,255,.12)}
.br .wm{font-weight:800;letter-spacing:.12em;color:#E3C878}
.br .sl{color:rgba(255,255,255,.8);font-weight:500}
.pill{display:inline-block;background:#E3C878;color:#12301F;font-weight:800;border-radius:999px;letter-spacing:.04em}
h1{font-family:'Cormorant Garamond',serif;font-size-adjust:.52;font-variant-numeric:lining-nums;font-weight:700;line-height:1.22;text-wrap:balance;color:#F1E6C6} h1 em{font-style:normal;color:#E3C878}
.kp .num{font-weight:800;line-height:1} .kp .lb{color:rgba(255,255,255,.82);font-weight:500;margin-top:8px}
.du{position:absolute;display:flex;align-items:center;gap:14px;background:rgba(0,0,0,.35);border:2px solid #E3C878;border-radius:18px;font-weight:800;color:#fff}
.du .tri{width:0;height:0;border-style:solid;border-color:transparent transparent transparent #E3C878}
.ft{position:absolute;color:rgba(255,255,255,.66);font-weight:500}"""
W_CSS = """body{width:1920px;height:1080px}
.br{position:absolute;left:84px;top:78px} .br img.lg{width:118px;height:118px} .br .wm{font-size:30px} .br .sl{font-size:24px;margin-top:4px}
.pill{position:absolute;left:84px;top:262px;font-size:30px;padding:10px 28px}
h1{position:absolute;left:84px;top:340px;width:1560px;font-size:92px}
.kps{position:absolute;left:84px;bottom:150px;display:flex;gap:80px} .kp .num{font-size:72px} .kp .lb{font-size:26px}
.du{right:84px;bottom:140px;font-size:64px;padding:14px 30px} .du .tri{border-width:20px 0 20px 32px}
.ft{left:84px;bottom:66px;font-size:22px}"""
T_CSS = """body{width:1080px;height:1920px}
.br{position:absolute;left:72px;top:96px} .br img.lg{width:132px;height:132px} .br .wm{font-size:32px} .br .sl{font-size:25px;margin-top:6px}
.pill{position:absolute;left:72px;top:330px;font-size:34px;padding:12px 32px}
.no{position:absolute;right:72px;top:250px;font-size:300px;font-weight:800;color:rgba(227,192,112,.16);line-height:1}
h1{position:absolute;left:72px;top:440px;width:936px;font-size:92px}
.kps{position:absolute;left:72px;top:1180px;display:flex;flex-direction:column;gap:46px} .kp .num{font-size:96px} .kp .lb{font-size:32px}
.du{left:72px;bottom:230px;font-size:72px;padding:16px 34px} .du .tri{border-width:22px 0 22px 36px}
.ft{left:72px;right:72px;bottom:96px;font-size:24px;line-height:1.45}"""

def page(fmt, pill, title, stats, d_short, no=""):
    kps = "".join(f'<div class="kp"><div class="num" style="color:{TONE.get((s + ["n"])[2], "#fff")}">{E(s[0])}</div><div class="lb">{E(s[1])}</div></div>' for s in stats)
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS_F}{BASE}{W_CSS if fmt == "w" else T_CSS}</style></head><body><div class="frame"></div>'
            f'<div class="br">{LOGO}<div><div class="wm">SỔ QUỸ BẢO TRÌ SSR</div><div class="sl">Chung cư Nam Sài Gòn Residences</div></div></div>'
            + (f'<div class="no">{E(no)}</div>' if no else "") +
            f'<div class="pill">{E(pill)}</div><h1>{rich(title)}</h1><div class="kps">{kps}</div>'
            f'<div class="du"><span class="tri"></span>{E(d_short)}</div>'
            f'<div class="ft">Phân tích độc lập của cư dân · 04/10/2026 · Các nhận định là dấu hiệu cần làm rõ, không phải cáo buộc</div></body></html>')

jobs = []
ds, dl = dur("SSR_Quy_bao_tri_ban_day_du_25p")
jobs.append(("w", f"00 - Bản đầy đủ ({dl})", page("w", "BẢN ĐẦY ĐỦ · CLIP NGANG · CÓ CHIA CHƯƠNG", "Quỹ bảo trì: **sai ở đâu**, tới mức nào, Hội nghị quyết định gì",
                                                  O_STATS if (O_STATS := V.O.C_ONE["video_cover_stats"]) else [], ds)))
for n, p in V.PARTS.items():
    ds, dl = dur(f"SSR_Quy_bao_tri_phan_{n}_tren_6")
    t = p["name"]; t = t.replace(": ", ": **", 1) + "**" if ": " in t else "**" + t + "**"
    jobs.append(("w", f"Phần {n} - {p['name'].replace(':', ' -')} ({dl})", page("w", f"PHẦN {n} / 6 · CLIP NGANG", t, V.PART_STATS[n], ds)))
for k, s in V.SEG.items():
    ds, dl = dur(f"SSR_Quy_bao_tri_clip_doc_{k:02d}_tren_11")
    t = s["short"]; t = t.replace(": ", ": **", 1) + "**" if ": " in t else "**" + t + "**"
    jobs.append(("t", f"Clip {k:02d} - {s['short'].replace(':', ' -')} ({dl})", page("t", f"CLIP {k} / 11 · XEM TRÊN ĐIỆN THOẠI", t, V.DOC_STATS[k], ds, no=f"{k:02d}")))

ds, dl = dur("SSR_Quy_bao_tri_clip_doc_tom_tat")
jobs.append(("t", f"Clip tóm tắt - Năm vấn đề trong 90 giây ({dl})", page("t", "CLIP TÓM TẮT · XEM TRÊN ĐIỆN THOẠI", "Quỹ bảo trì: **năm vấn đề** trong 90 giây",
             [["5", "vấn đề", "r"], ["127,15 tỷ", "tiền gốc còn", "g"]], ds, no="5")))
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    b = pw.chromium.launch()
    for fmt, name, html in jobs:
        w, h = (1920, 1080) if fmt == "w" else (1080, 1920)
        pg = b.new_page(viewport={"width": w, "height": h}); hp = f"{OUTD}/_tmp.html"; open(hp, "w").write(html)
        pg.goto("file://" + hp); pg.wait_for_timeout(250)
        over = pg.evaluate("(()=>{const h=document.querySelector('h1').getBoundingClientRect(), k=document.querySelector('.kps').getBoundingClientRect(); return h.bottom > k.top - 20})()")
        pg.screenshot(path=f"{OUTD}/{name}.png"); pg.close(); print(("CHONG " if over else "ok ") + name)
    b.close()
os.remove(f"{OUTD}/_tmp.html")
