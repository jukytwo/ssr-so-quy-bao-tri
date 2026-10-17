# -*- coding: utf-8 -*-
"""Ap lop ngon tu len file Word (cv) va Excel (xlsx) nhung trong trang Quy bao tri (khoi FILES), sua thang XML van ban."""
import base64, io, json, re, sys, zipfile
import ngon_tu as NT

_TXT = re.compile(r">([^<>]{6,})<"); _C = {}
def _soft(x):
    if x not in _C: _C[x] = NT.soften(x)
    return _C[x]

def fix_zip(raw, parts):
    zin = zipfile.ZipFile(io.BytesIO(raw)); out = io.BytesIO(); n = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zo:
        for it in zin.infolist():
            d = zin.read(it.filename)
            if re.search(parts, it.filename):
                s = d.decode("utf-8"); t = _TXT.sub(lambda m: ">" + _soft(m.group(1)) + "<", s)
                if t != s: n += 1; d = t.encode("utf-8")
            zo.writestr(it, d)
    return out.getvalue(), n

def run(path):
    h = open(path, encoding="utf-8").read()
    m = re.search(r'(<script id="FILES"[^>]*>)(.*?)(</script>)', h, re.S)
    F = json.loads(m.group(2))
    for k, parts in (("cv", r"^word/(document|header\d*|footer\d*)\.xml$"), ("xlsx", r"^xl/(sharedStrings|worksheets/sheet\d+)\.xml$")):
        if F.get(k, "").startswith("UEsDB"):
            new, n = fix_zip(base64.b64decode(F[k]), parts); F[k] = base64.b64encode(new).decode(); print(k, "parts changed:", n)
    body = json.dumps(F, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    open(path, "w", encoding="utf-8").write(h[:m.start(2)] + body + h[m.end(2):]); print("ok", path)

if __name__ == "__main__":
    for p in sys.argv[1:]: run(p)
