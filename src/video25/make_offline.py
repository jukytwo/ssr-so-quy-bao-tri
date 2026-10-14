# -*- coding: utf-8 -*-
"""Ban offline cua dashboard: nhung anh poster nho (data URI) de danh sach clip van dep khi mo file; clip thi xem tren trang truc tuyen."""
import base64, glob, io, os, re
from PIL import Image
W = "/home/claude/ssr/video25/web"
doc = open("/home/claude/ssr/d3/dashboard_v3_standalone.html").read()
n = 0
for f in sorted(glob.glob(f"{W}/p/*.jpg")):
    key = '"p/' + os.path.basename(f) + '"'
    if key not in doc: continue
    im = Image.open(f).convert("RGB"); w = 200 if im.height > im.width else 360
    im = im.resize((w, round(w * im.height / im.width)), Image.LANCZOS); b = io.BytesIO(); im.save(b, "JPEG", quality=70, optimize=True)
    doc = doc.replace(key, '"data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode() + '"'); n += 1
open(f"{W}/offline.html", "w").write(doc)
print("anh", n, "MB", round(len(doc.encode()) / 1048576, 2))
