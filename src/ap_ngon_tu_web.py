# -*- coding: utf-8 -*-
"""Ap lop ngon tu (ngon_tu.soften, ca lop 2 an toan phap ly 17/10/2026) len trang Quy bao tri DA DUNG san,
khi khong co moi truong dung day du. Giu nguyen D["clips"] (phu de khop loi doc da ghi am), IMG, FILES, U.
Cach dung: python3 ap_ngon_tu_web.py ../index.html [../web/index.html ...]"""
import json, re, sys
import ngon_tu as NT

def jtxt(o):
    return json.dumps(o, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")

def fix_tiles(o):
    if isinstance(o, list):
        if o == ["0", "đủ căn cứ có chủ đích"]: return ["4", "dấu hiệu cần hồ sơ để làm rõ nguyên nhân"]
        return [fix_tiles(x) for x in o]
    if isinstance(o, dict): return {k: fix_tiles(v) for k, v in o.items()}
    return o

KEEP = ("D", "IMG", "FILES", "U")
def run(path):
    h = open(path, encoding="utf-8").read()
    out, pos = [], 0
    for m in re.finditer(r'<script id="(D|IMG|FILES|U)"([^>]*)>(.*?)</script>', h, re.S):
        out.append(NT.soften(h[pos:m.start()]))
        sid, attrs, body = m.groups()
        if sid == "D":
            D = json.loads(body); clips = D.pop("clips", None)
            D = NT.walk(fix_tiles(D)); D["clips"] = clips
            body = jtxt(D)
        out.append(f'<script id="{sid}"{attrs}>{body}</script>'); pos = m.end()
    out.append(NT.soften(h[pos:]))
    new = "".join(out)
    open(path, "w", encoding="utf-8").write(new)
    print("ok", path, len(h), "->", len(new))

if __name__ == "__main__":
    for p in sys.argv[1:]: run(p)
    NT.report()
