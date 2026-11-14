import sys, subprocess, re, pathlib
from playwright.sync_api import sync_playwright

src, out = sys.argv[1], sys.argv[2]
mode = sys.argv[3] if len(sys.argv) > 3 else "video"   # "video" or comma list of seconds
FPS = 30
DUR = float(sys.argv[4]) if len(sys.argv) > 4 else 49.5
MEDIA = pathlib.Path(src).parent / "media"
BLOBS = {"df424c3bec40191e9e60fdca4fd7aa9c": "sky-twilight.jpg", "c2ba293a532f28b2496f0586330e33da": "sky-night.jpg",
         "51353ebe3284512c064a9e50c650e416": "ui-isha.jpg", "b53860df6cc09323b7f1b1f48c48ff41": "frere.png",
         "4e1509b7947185c573993b3763661697": "soeur.png", "4b0187b596e24f9756d54e45a1867f35": "sky-dawn.jpg",
         "2f33859c6a4adb192f9e9d92e87593ad": "sky-day.jpg", "912ac41ee3a243acde862e490f09fd0d": "sky-sunset.jpg", "33641f46cd42014a7806f0b689266470": "logo-salwaa.png"}

html = pathlib.Path(src).read_text()
for k, v in BLOBS.items():
    html = html.replace("/_blob/" + k, (MEDIA / v).as_uri())
html = html.replace('<script src="./support.js"></script>', '')
html = re.sub(r'<link href="https://fonts.googleapis.com[^>]*>', '', html)
tmp = pathlib.Path(out).with_suffix('.render.html')
tmp.write_text(html)

SEEK = """t => { for (const a of document.getAnimations()) { a.pause(); a.currentTime = t; } }"""

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1920})
    pg.goto(tmp.as_uri())
    pg.evaluate("document.fonts.ready")
    pg.wait_for_timeout(500)
    if mode != "video":
        for s in mode.split(","):
            pg.evaluate(SEEK, float(s) * 1000)
            pg.wait_for_timeout(30)
            pg.screenshot(path=f"{out}_{s}.jpg", type="jpeg", quality=88)
    else:
        part = out + ".part.mp4"
        ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-",
                               "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", part],
                              stdin=subprocess.PIPE)
        n = int(DUR * FPS)
        for i in range(n):
            pg.evaluate(SEEK, i * 1000.0 / FPS)
            ff.stdin.write(pg.screenshot(type="jpeg", quality=92))
        ff.stdin.close()
        if ff.wait() == 0:
            pathlib.Path(part).rename(out)
    b.close()
