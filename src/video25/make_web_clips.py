# -*- coding: utf-8 -*-
"""Sau web_encode.py: tao poster JPEG va web/clips.json cho phan Xem clip cua dashboard."""
import json, os, subprocess, sys, glob
sys.path.insert(0, "/home/claude/ssr"); os.environ.setdefault("CLIP_RES", "1080")
import video_ssr_25 as V
from PIL import Image
D = "/home/claude/ssr/video25"; W = f"{D}/web"; TH = f"{D}/anh_chu_de"
def dur(f): return round(float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).decode()), 2)
def thumb(prefix):
    m = [f for f in glob.glob(f"{TH}/*.png") if os.path.basename(f).startswith(prefix)]; assert len(m) == 1, (prefix, m); return m[0]
def poster(src, out, vert, w=None):
    im = Image.open(src).convert("RGB"); w = w or (540 if vert else 960); h = round(w * im.height / im.width)
    im.resize((w, h), Image.LANCZOS).save(f"{W}/p/{out}", "JPEG", quality=80, optimize=True, progressive=True)
    return "p/" + out
def frame(video, t, out):
    subprocess.check_call(["ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i", video, "-frames:v", "1", "-vf", "scale=480:270", "-q:v", "5", f"{W}/p/{out}"])
    return "p/" + out
def item(id_, file, title, kind, desc, post, vert):
    f = f"{W}/v/{file}"
    return dict(id=id_, src="v/" + file, title=title, kind=kind, desc=desc, poster=post, vert=vert, dur=dur(f), mb=round(os.path.getsize(f) / 1048576, 1))

info = json.load(open(f"{D}/SSR_Quy_bao_tri_ban_day_du_25p_info.json"))
chs = []
for i, c in enumerate(info["chapters"], 1):
    f = f"full_{i:02d}.mp4"; d = dur(f"{W}/v/{f}")
    chs.append(dict(id=f"full_{i:02d}", src="v/" + f, title=c.split(" ", 1)[1], dur=d, poster=frame(f"{W}/v/{f}", min(4, d / 2), f"full_{i:02d}.jpg"),
                    mb=round(os.path.getsize(f"{W}/v/{f}") / 1048576, 1)))
full = dict(id="full", title="Quỹ bảo trì: điểm nào cần làm rõ, tới mức nào, Hội nghị quyết định gì", kind="Bản đầy đủ · ngang",
            desc="Toàn bộ nội dung trong một clip, chia 16 chương. Hợp để chiếu tại Hội nghị hoặc xem trên máy tính, TV.",
            poster=poster(thumb("00 - "), "full.jpg", False), vert=False, dur=round(sum(c["dur"] for c in chs), 2), chapters=chs)
parts = [item(f"phan_{n}", f"phan_{n}.mp4", p["name"], f"Phần {n} / 6 · ngang", V.PHOOK[n], poster(thumb(f"Phần {n} - "), f"phan_{n}.jpg", False), False) for n, p in V.PARTS.items()]
docs = [item(f"doc_{k:02d}", f"doc_{k:02d}.mp4", s["short"], f"Clip {k} / 11 · dọc", V.HOOK[k], poster(thumb(f"Clip {k:02d} - "), f"doc_{k:02d}.jpg", True), True) for k, s in V.SEG.items()]
short = item("tom_tat", "tom_tat.mp4", "Quỹ bảo trì: năm vấn đề trong 90 giây", "Clip tóm tắt · dọc",
             "Năm vấn đề của quỹ trong một clip ngắn. Gửi trước để mời xem bộ đầy đủ.", poster(thumb("Clip tóm tắt"), "tom_tat.jpg", True), True)
J = dict(date="04/10/2026", full=full, parts=parts, docs=docs, short=short)
json.dump(J, open(f"{W}/clips.json", "w"), ensure_ascii=False, indent=1)
tot = sum(os.path.getsize(f) for f in glob.glob(f"{W}/v/*.mp4") + glob.glob(f"{W}/p/*.jpg"))
print("ok", len(chs), "chuong", len(parts), "phan", len(docs), "doc", round(tot / 1048576, 1), "MB")
big = [f for f in glob.glob(f"{W}/v/*.mp4") if os.path.getsize(f) > 14.5 * 1048576]; print("qua lon:", big)

# ---- loi thuyet minh theo thoi gian (lay tu timeline da luu luc dung clip, khong doc lai giong) va ma QR dan toi trang ----
import re as _re, segno, io as _io
def _clean(t): return _re.sub(r"\*\*(.+?)\*\*", r"\1", t).strip()
def _tl(name): return [(round(a, 2), round(b, 2), _clean(t)) for s, t, a, b in json.load(open(f"{D}/_{name}_info.json"))["timeline"]]
J = json.load(open(f"{W}/clips.json"))
ftl = _tl("SSR_Quy_bao_tri_ban_day_du_25p"); t0 = 0
for c in J["full"]["chapters"]:
    t1 = t0 + c["dur"]
    c["tx"] = [[round(a - t0, 2), round(b - t0, 2), t] for a, b, t in ftl if t0 - 0.01 <= a < t1 - 0.01]; t0 = t1
assert sum(len(c["tx"]) for c in J["full"]["chapters"]) == len(ftl)
for n, p in enumerate(J["parts"], 1): p["tx"] = [list(x) for x in _tl(f"SSR_Quy_bao_tri_phan_{n}_tren_6")]
for k, p in enumerate(J["docs"], 1): p["tx"] = [list(x) for x in _tl(f"SSR_Quy_bao_tri_clip_doc_{k:02d}_tren_11")]
J["short"]["tx"] = [list(x) for x in _tl("SSR_Quy_bao_tri_clip_doc_tom_tat")]
URL = "https://jukytwo.github.io/ssr-so-quy-bao-tri/"
q = segno.make(URL, error="m"); b = _io.BytesIO(); q.save(b, kind="svg", scale=4, border=2, dark="#12301F", light="#FFFFFF", xmldecl=False, svgns=True)
J["qr_svg"] = b.getvalue().decode(); J["url"] = URL
json.dump(J, open(f"{W}/clips.json", "w"), ensure_ascii=False, indent=1)
print("tx ok", sum(len(x["tx"]) for x in J["parts"] + J["docs"]) + len(J["short"]["tx"]) + len(ftl), "cau; qr", len(J["qr_svg"]))
