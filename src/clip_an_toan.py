# -*- coding: utf-8 -*-
"""Tam go cac clip chua dung lai theo lop ngon tu an toan phap ly (17/10/2026).
Giu: ban day du (bo chuong 11 "Muc do, nguyen nhan"), Phan 2, clip tom tat 90 giay (deu dung lai ngay 15/10 theo ngon_tu_clip).
Go: Phan 1, 3, 4, 5, 6 (dung 04/10, ban day du da phu het noi dung voi cach dien dat moi), clip doc 01, 02, 03, 09 va chuong full_11
(loi doc hoac chu tren hinh con "tien co mat khong", "da ro", "co chu dich"); cac clip doc con lai da soat chu tren hinh bang OCR.
Tam rut PDF bao cao day du, tom tat, phan loai, hoi dan va anh A4 tom tat, phan loai; trang van co nut In de luu PDF tu noi dung moi.
Khi dung lai cac clip nay bang video_ssr_25.py (da co lop ngon tu moi), chi can them lai vao clips.json.
Cach dung: python3 clip_an_toan.py  (sua src/d3/js6_clip.js, src/d3/js4_app.js, web/clips.json, index.html, web/index.html)"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GO = {"phan_1", "phan_3", "phan_4", "phan_5", "phan_6", "full_11", "doc_01", "doc_02", "doc_03", "doc_09"}
# tai lieu PDF va anh A4 con cach dien dat cu (phan loai "co chu dich", "can cu bai nhiem da co"): tam rut, xuat lai sau tu bo dung bao cao
FGO = ["pdf", "sum", "pl", "hdan"]; A4GO = ["a4_pl", "a4_tomtat"]

JS = [  # (cu, moi): giao dien tu thich ung so clip con lai
    ('["full", "parts", "docs", "short"].map(function(g){\n    return \'<button type="button" role="tab" class="clp-tab" data-clg="\' + g + \'" aria-selected="false"><b>\' + CLP_GN[g] + "</b><small>" + (g === "full" ? "16 chương · " : "")',
     '["full", "parts", "docs", "short"].filter(function(g){ return CLP.groups[g].length; }).map(function(g){\n    return \'<button type="button" role="tab" class="clp-tab" data-clg="\' + g + \'" aria-selected="false"><b>\' + clpGN(g) + "</b><small>" + (g === "full" ? CLP.groups.full.length + " chương · " : "")'),
    ('var CLP_GN = {full: "Bản đầy đủ", parts: "6 phần ngang", docs: "11 clip dọc", short: "Tóm tắt 90 giây"};',
     'var CLP_GN = {full: "Bản đầy đủ", parts: "phần ngang", docs: "clip dọc", short: "Tóm tắt 90 giây"};\n'
     'function clpGN(g){ var L = CLP.groups[g] || [], n = L.length; return g === "parts" ? (n === 1 ? "Phần " + L[0].n + " · ngang" : n + " phần ngang") : g === "docs" ? n + " clip dọc" : CLP_GN[g]; }'),
    ('var sh = "<b>" + CLP_GN[g] + "</b>', 'var sh = "<b>" + clpGN(g) + "</b>'),
    ('" · 6 phần ngang · 11 clip dọc · tóm tắt "', '" · " + C.docs.length + " clip dọc · tóm tắt "'),
    ('var SEC_CLIPS = {"ket-luan": ["tom_tat", "doc_09"], "du-lieu": ["doc_01"], "tien-o-dau": ["doc_02"], "vi-sao": ["doc_03", "doc_05", "doc_06"],\n  "khu-vuc-chung": ["doc_04"], "lai-suat": ["doc_07"], "quy-che": ["doc_08"], "dau-hieu": ["doc_09", "doc_11"], "ho-so": ["doc_10"], "muoi-cau-hoi": ["doc_10"]};',
     'var SEC_CLIPS = {"ket-luan": ["tom_tat", "phan_2"], "vi-sao": ["doc_05", "doc_06"], "khu-vuc-chung": ["doc_04"], "lai-suat": ["doc_07"], "quy-che": ["doc_08"],\n  "dau-hieu": ["doc_11"], "ho-so": ["doc_10"], "muoi-cau-hoi": ["doc_10"]};'),
    ('  if (!F.sum) items = items.filter(function(f){ return f.k !== "sum"; });',
     '  items = items.filter(function(f){ return ["pdf", "sum", "pl", "hdan"].indexOf(f.k) < 0 || (F[f.k] && files()[f.k]); });'),
    ('  $("dlg").innerHTML = items.map(', '  setTimeout(hideMissingDl, 0);\n  $("dlg").innerHTML = items.map('),
    ('function doDownload(k){', 'function hideMissingDl(){ qa("[data-dl]").forEach(function(b){ var k = b.getAttribute("data-dl"); if (["pdf", "sum", "pl", "hdan"].indexOf(k) >= 0 && !(D.files[k] && files()[k])){ var c = b.closest(".dlc"); (c || b).remove(); } }); }\nfunction doDownload(k){'),
    ("""(kind === "print" ? '<button class="tbtn pri" type="button" data-dl="pdf">Tải báo cáo PDF</button>""", """(kind === "print" ? (D.files.pdf ? '<button class="tbtn pri" type="button" data-dl="pdf">Tải báo cáo PDF</button>' : "") + '"""),
    ('  {k: "a4_tomtat", t: "Tóm tắt một trang A4", d: "Năm điểm đề nghị Ban quản trị làm rõ", n: "SSR - Tom tat mot trang A4.png"},\n', ''),
    (',\n  {k: "a4_pl", t: "Phân loại nguyên nhân", d: "Quy trình chưa chặt, lỡ tay hay có chủ đích", n: "SSR - Phan loai nguyen nhan.png"}', ''),
    ('[["full", "Bản đầy đủ, 16 chương"], ["phan_1", "Sáu phần ngang"], ["doc_01", "Mười một clip dọc"], ["tom_tat", "Clip tóm tắt 90 giây"]]',
     '[["full", "Bản đầy đủ"], ["phan_2", "Phần 2: hai điểm nghi vấn trên sao kê"], ["doc_04", "Clip dọc cho điện thoại"], ["tom_tat", "Clip tóm tắt 90 giây"]]'),
]

def fix_clips(C):
    full = C["full"]; full["chapters"] = [c for c in full["chapters"] if c["id"] not in GO]
    full["dur"] = round(sum(c["dur"] for c in full["chapters"]), 2)
    full["desc"] = re.sub(r"chia \d+ chương", f"chia {len(full['chapters'])} chương", full["desc"])
    C["parts"] = [p for p in C["parts"] if p["id"] not in GO]
    for p in C["parts"]:
        m = re.match(r"phan_(\d+)", p["id"])
        if m: p["n"] = int(m.group(1)); p["kind"] = re.sub(r"Phần (\d+) / \d+", r"Phần \1", p.get("kind", ""))
    C["docs"] = [p for p in C["docs"] if p["id"] not in GO]
    for p in C["docs"]:
        m = re.match(r"doc_(\d+)", p["id"])
        if m: p["n"] = int(m.group(1))
    return C

def patch_js(s, where):
    for a, b in JS:
        if a in s: s = s.replace(a, b)
        elif b not in s and a.split("(")[0] in s: print("  chua khop:", where, a[:60])
    return s

def run(extra=()):
    for f in ("src/d3/js6_clip.js", "src/d3/js4_app.js", "src/d3/js1_core.js"):
        p = os.path.join(ROOT, f); s = open(p, encoding="utf-8").read(); open(p, "w", encoding="utf-8").write(patch_js(s, f))
    p = os.path.join(ROOT, "web/clips.json"); C = fix_clips(json.load(open(p, encoding="utf-8")))
    json.dump(C, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for f in ("index.html", "web/index.html") + tuple(extra):
        p = os.path.join(ROOT, f); h = open(p, encoding="utf-8").read()
        m = re.search(r'<script id="D"[^>]*>(.*?)</script>', h, re.S); D = json.loads(m.group(1))
        if D.get("clips"): D["clips"] = fix_clips(D["clips"])
        for k in FGO: D["files"].pop(k, None); D["files"].pop(k + "_desc", None)
        m2 = re.search(r'<script id="FILES"[^>]*>(.*?)</script>', h, re.S); F = json.loads(m2.group(1))
        for k in FGO: F.pop(k, None)
        h = h[:m2.start(1)] + json.dumps(F, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c") + h[m2.end(1):]
        m = re.search(r'<script id="D"[^>]*>(.*?)</script>', h, re.S)
        body = json.dumps(D, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
        h = h[:m.start(1)] + body + h[m.end(1):]
        m = re.search(r'<script id="app">(.*?)</script>', h, re.S)
        h = h[:m.start(1)] + patch_js(m.group(1), f) + h[m.end(1):]
        open(p, "w", encoding="utf-8").write(h); print("ok", f)
    for d in ("web/v", "v"):
        for i in GO:
            q = os.path.join(ROOT, d, i + ".mp4")
            if os.path.exists(q): os.remove(q)
    for d in ("web/f", "f"):
        for k in FGO + A4GO:
            for ext in (".pdf", ".png"):
                q = os.path.join(ROOT, d, k + ext)
                if os.path.exists(q): os.remove(q)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--chi":  # chi sua cac trang chi dinh, khong dong vao nguon va clips.json
        def run_only(paths):
            global JS
            for f in paths:
                p = os.path.join(ROOT, f); h = open(p, encoding="utf-8").read()
                m = re.search(r'<script id="D"[^>]*>(.*?)</script>', h, re.S); D = json.loads(m.group(1))
                if D.get("clips"): D["clips"] = fix_clips(D["clips"])
                for k in FGO: D["files"].pop(k, None); D["files"].pop(k + "_desc", None)
                h = h[:m.start(1)] + json.dumps(D, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c") + h[m.end(1):]
                m2 = re.search(r'<script id="FILES"[^>]*>(.*?)</script>', h, re.S); F = json.loads(m2.group(1))
                for k in FGO: F.pop(k, None)
                h = h[:m2.start(1)] + json.dumps(F, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c") + h[m2.end(1):]
                m = re.search(r'<script id="app">(.*?)</script>', h, re.S)
                h = h[:m.start(1)] + patch_js(m.group(1), f) + h[m.end(1):]
                open(p, "w", encoding="utf-8").write(h); print("ok", f)
        run_only(sys.argv[2:])
    else:
        run()
