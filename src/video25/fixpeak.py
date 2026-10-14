import sys, os, subprocess
sys.path.insert(0, "/home/claude/vshim"); sys.path.insert(1, "/home/claude/vtpl")
import build_video as BV
for f in sys.argv[1:]:
    p = "/home/claude/ssr/video25/" + f; ok, d = BV.audio_check(p)
    if not ok:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", p, "-map", "0", "-map_metadata", "0", "-map_chapters", "0", "-c:v", "copy", "-af",
                        "alimiter=limit=0.82:level=disabled:attack=5:release=50", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-movflags", "+faststart", p + ".fix.mp4"], check=True)
        os.replace(p + ".fix.mp4", p); ok, d = BV.audio_check(p)
    print(f, ok, d, flush=True)
