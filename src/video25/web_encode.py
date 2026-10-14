# -*- coding: utf-8 -*-
"""Nen clip cho web app: 720p H.264 main + AAC 96k, faststart, moi file < 14,5 MB.
Ban day du tach theo chuong (16 file). Poster JPEG tu anh chu de. Ghi web/clips.json."""
import json, os, subprocess, sys, glob
D = "/home/claude/ssr/video25"; W = f"{D}/web"; os.makedirs(f"{W}/v", exist_ok=True); os.makedirs(f"{W}/p", exist_ok=True)
LIM = 14.5 * 1024 * 1024

def dur(f):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).decode())

def enc(src, out, vert, crf, extra=None, ss=None, to=None):
    sc = "scale=720:1280" if vert else "scale=1280:720"
    cmd = ["ffmpeg", "-y", "-v", "error"]
    if ss is not None: cmd += ["-ss", f"{ss:.3f}"]
    cmd += ["-i", src]
    if to is not None: cmd += ["-t", f"{to - (ss or 0):.3f}"]
    cmd += ["-map", "0:v:0", "-map", "0:a:0", "-vf", sc + ":flags=lanczos,format=yuv420p", "-c:v", "libx264", "-profile:v", "main", "-level", "3.1",
            "-preset", "medium", "-crf", str(crf), "-g", "120", "-maxrate", "900k", "-bufsize", "1800k",
            "-c:a", "aac", "-b:a", "96k", "-ac", "2", "-ar", "44100", "-movflags", "+faststart", out]
    subprocess.check_call(cmd)
    return os.path.getsize(out)

def enc_fit(src, out, vert, **kw):
    for crf in (26, 29, 32):
        s = enc(src, out, vert, crf, **kw)
        if s <= LIM: return s
    return s

def ts(c):
    m, s = c.split(" ")[0].split(":"); return int(m) * 60 + int(s)

jobs = []
for n in range(1, 7): jobs.append((f"SSR_Quy_bao_tri_phan_{n}_tren_6.mp4", f"phan_{n}.mp4", False))
for k in range(1, 12): jobs.append((f"SSR_Quy_bao_tri_clip_doc_{k:02d}_tren_11.mp4", f"doc_{k:02d}.mp4", True))
jobs.append(("SSR_Quy_bao_tri_clip_doc_tom_tat.mp4", "tom_tat.mp4", True))
only = sys.argv[1:]
res = {}
for src, out, vert in jobs:
    if only and out not in only: continue
    s = enc_fit(f"{D}/{src}", f"{W}/v/{out}", vert); res[out] = s; print(out, round(s / 1048576, 2), "MB", flush=True)

if not only or "full" in only:
    full = f"{D}/SSR_Quy_bao_tri_ban_day_du_25p.mp4"; info = json.load(open(f"{D}/SSR_Quy_bao_tri_ban_day_du_25p_info.json"))
    T = [ts(c) for c in info["chapters"]] + [dur(full)]
    for i in range(len(T) - 1):
        out = f"full_{i + 1:02d}.mp4"
        s = enc_fit(full, f"{W}/v/{out}", False, ss=T[i], to=T[i + 1]); print(out, round(s / 1048576, 2), "MB", flush=True)
print("xong")
