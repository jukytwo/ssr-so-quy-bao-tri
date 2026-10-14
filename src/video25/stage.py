# Chuan bi chuyen file ve may: gzip -1, cat 19.000.000 byte; ghi manifest (ten dich, cac phan, sha256)
import sys, os, json, subprocess, hashlib, glob
sys.path.insert(0, "/home/claude/ssr"); os.environ.setdefault("CLIP_RES", "1080")
V = None
X = "/mnt/user-data/outputs/xfer"; os.makedirs(X, exist_ok=True)
D = "/home/claude/ssr/video25"
def mmss_vn(sec):
    s = int(round(sec)); return f"{s // 60} phút {s % 60:02d} giây"
def target(fn):
    import importlib; global V
    if V is None:
        import video_ssr_25 as V_; V = V_
    inf = json.load(open(f"{D}/{fn[:-4]}_info.json")); d = mmss_vn(inf["duration"])
    if "_phan_" in fn:
        n = int(fn.split("_phan_")[1].split("_")[0]); return f"2 - Sáu phần ngang/Phần {n} - {V.PARTS[n]['name'].replace(':', ' -')} ({d}).mp4"
    if "_clip_doc_" in fn:
        k = int(fn.split("_clip_doc_")[1].split("_")[0]); return f"3 - Mười một clip dọc/Clip {k:02d} - {V.SEG[k]['short'].replace(':', ' -')} ({d}).mp4"
    return f"1 - Bản đầy đủ (ngang, {d}).mp4"
man = []
for fn in sys.argv[1:]:
    src = f"{D}/{fn}"; tag = fn[:-4]
    for old in glob.glob(f"{X}/{tag}.gz.part*"): os.remove(old)
    subprocess.run(f"gzip -1 -c '{src}' | split -b 19000000 -d - '{X}/{tag}.gz.part'", shell=True, check=True)
    parts = sorted(os.path.basename(p) for p in glob.glob(f"{X}/{tag}.gz.part*"))
    man.append(dict(tag=tag, target=target(fn), parts=parts, sha=hashlib.sha256(open(src, "rb").read()).hexdigest()))
json.dump(man, open(f"{X}/manifest.json", "w"), ensure_ascii=False, indent=1)
for m in man: print(m["target"], m["parts"], m["sha"][:12])
