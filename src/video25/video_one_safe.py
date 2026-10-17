# -*- coding: utf-8 -*-
"""17/10/2026: dung lai clip "toan bo van de" (ban 11 phut, ngang va doc) voi lop ngon tu an toan phap ly va tong mau SSR.
Nap video_ssr_25 (da ap tong mau SSR cho cac module dung clip), roi ap ngon_tu_clip len loi doc, chu tren hinh, tieu de, so lieu bia."""
import os, sys, json, time
os.environ.setdefault("CLIP_RES", "1080")
sys.path.insert(0, "/home/claude/ssr"); os.chdir("/home/claude/ssr")
import video_ssr_25 as V
import ngon_tu_clip as NC
O = V.O; BV = O.BV
VS1 = [(x[0], NC.soften(x[1])) + tuple(x[2:]) for x in O.VS_ONE]
C1 = dict(O.C_ONE)
C1.update(hero_title=NC.soften(C1["hero_title"]), video_cover_stats=NC.walk(C1["video_cover_stats"]), video_script=VS1, video_visuals=NC.walk(C1["video_visuals"]))
C1["meta"] = dict(C1["meta"], date="Bản 17/10/2026")
TEXTS = [x[1] for x in VS1]
if __name__ == "__main__":
    t0 = time.time(); OUT = "/home/claude/ssr/video_one_safe"; os.makedirs(OUT, exist_ok=True)
    pre = f"{OUT}/SSR_Mot_clip_an_toan"
    if "list" in sys.argv:
        print(C1["hero_title"], C1["video_cover_stats"]); sys.exit()
    mp4, info = BV.build_video(C1, pre, speed=1.18, formats=("16x9",))
    _m, _i = BV.build_video(C1, pre, speed=1.18, formats=("9x16",))
    json.dump({k: v for k, v in info.items() if k != "script"}, open(pre + "_info.json", "w"), ensure_ascii=False, indent=1)
    out = O.overlay(pre + "_Video.mp4", info, f"{OUT}/SSR_Quy_bao_tri_toan_bo_van_de_ngang.mp4", f"{OUT}/tmp")
    out_t = O.overlay(pre + "_Video_Doc.mp4", info, f"{OUT}/SSR_Quy_bao_tri_toan_bo_van_de_doc.mp4", f"{OUT}/tmp", fmt="t")
    print(json.dumps(json.load(open(out[:-4] + "_info.json")), ensure_ascii=False), json.dumps(json.load(open(out_t[:-4] + "_info.json")), ensure_ascii=False), round(time.time() - t0))
