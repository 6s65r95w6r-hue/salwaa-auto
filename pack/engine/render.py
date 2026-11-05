import sys, subprocess, re, pathlib
from playwright.sync_api import sync_playwright
src, out = sys.argv[1], sys.argv[2]
mode = sys.argv[3] if len(sys.argv) > 3 else "video"
DUR = float(sys.argv[4]) if len(sys.argv) > 4 else 45.0; FPS = 30
html = pathlib.Path(src).read_text()
html = re.sub(r'<link href="https://fonts.googleapis.com[^>]*>', '', html)
tmp = pathlib.Path(out).resolve().with_suffix('.render.html'); tmp.write_text(html)
SEEK = "t => { for (const a of document.getAnimations()) { a.pause(); a.currentTime = t; } }"
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width":1080,"height":1920})
    pg.goto(tmp.as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(500)
    if mode != "video":
        for s in mode.split(","):
            pg.evaluate(SEEK, float(s)*1000); pg.screenshot(path=f"{out}_{s}.jpg", type="jpeg", quality=88)
    else:
        part = out + ".part.mp4"
        ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","image2pipe","-framerate",str(FPS),"-c:v","mjpeg","-i","-",
              "-c:v","libx264","-preset","slow","-crf","15","-pix_fmt","yuv420p","-movflags","+faststart",part], stdin=subprocess.PIPE)
        for i in range(int(DUR*FPS)):
            pg.evaluate(SEEK, i*1000.0/FPS); ff.stdin.write(pg.screenshot(type="jpeg", quality=98))
        ff.stdin.close()
        if ff.wait() == 0: pathlib.Path(part).rename(out)
    b.close()
