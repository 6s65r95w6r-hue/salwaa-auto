#!/usr/bin/env python3
"""Generate the animated HTML page for the video. Usage: gen.py out.html"""
import sys
DUR = 46.0
GOLD = "#F0B429"; RED = "#E8382C"

POSES = {
 "SIT":   dict(T="M206 268 L196 318 L188 370", AL="M204 278 L222 318 L240 300", AR="M204 278 L228 324 L246 304",
               LL="M188 370 L240 336 L268 378", LR="M188 370 L234 346 L260 378", H=(222,250)),
 "STAND": dict(T="M200 146 L200 202 L200 258", AL="M200 162 L188 212 L184 258", AR="M200 162 L212 212 L216 258",
               LL="M200 258 L192 320 L186 380", LR="M200 258 L208 320 L214 380", H=(200,126)),
 "RUKU":  dict(T="M250 252 L215 255 L180 258", AL="M246 256 L224 290 L204 318", AR="M246 256 L232 292 L212 320",
               LL="M180 258 L190 320 L194 380", LR="M180 258 L196 320 L204 380", H=(270,246)),
 "SUJUD": dict(T="M230 352 L192 334 L152 320", AL="M228 354 L238 372 L256 380", AR="M228 354 L244 374 L264 380",
               LL="M152 320 L164 378 L104 380", LR="M152 320 L170 378 L112 380", H=(262,364)),
}
# (pose, start, duration) transitions
SEQ = [("STAND", 13.0, 1.2), ("RUKU", 19.0, 0.9), ("STAND", 21.0, 0.9), ("SUJUD", 23.0, 1.1)]
LIMBS = ["T", "AL", "AR", "LL", "LR"]

css = []
html = []

def pct(t): return round(t / DUR * 100, 4)

# ---------- limb morph keyframes ----------
anims = {k: [] for k in LIMBS + ["H"]}
prev = "SIT"
for i, (pose, st, du) in enumerate(SEQ):
    fill = "both" if i == 0 else "forwards"
    for k in LIMBS:
        css.append(f'@keyframes {k}{i}{{from{{d:path("{POSES[prev][k]}")}}to{{d:path("{POSES[pose][k]}")}}}}')
        anims[k].append(f"{k}{i} {du}s ease-in-out {st}s {fill}")
    (x0, y0), (x1, y1) = POSES[prev]["H"], POSES[pose]["H"]
    css.append(f"@keyframes H{i}{{from{{cx:{x0}px;cy:{y0}px}}to{{cx:{x1}px;cy:{y1}px}}}}")
    anims["H"].append(f"H{i} {du}s ease-in-out {st}s {fill}")
    prev = pose

css.append("""
*{margin:0;padding:0;box-sizing:border-box}
body{background:#000}
@font-face{font-family:'Amiri';src:local('Amiri')}
.root{width:1080px;height:1920px;position:relative;overflow:hidden;background:#000;font-family:'Poppins',sans-serif;color:#fff}
.abs{position:absolute}
@keyframes in{from{opacity:0}to{opacity:1}}
@keyframes out{from{opacity:1}to{opacity:0}}
@keyframes wrd{from{opacity:0;transform:translateY(24px);filter:blur(8px)}to{opacity:1;transform:none;filter:blur(0)}}
@keyframes up{from{opacity:0;transform:translateY(60px)}to{opacity:1;transform:none}}
@keyframes pop{from{transform:scale(.3);opacity:0}60%{transform:scale(1.25);opacity:1}to{transform:scale(1);opacity:1}}
@keyframes fillgold{from{background:transparent;box-shadow:none}to{background:#F0B429;box-shadow:0 0 28px rgba(240,180,41,.8)}}
@keyframes rise{from{transform:translate(0,0);opacity:0}15%{opacity:1}to{transform:translate(var(--dx),-340px);opacity:0}}
@keyframes notif{from{transform:translateY(80px) scale(.9);opacity:0}15%{opacity:1;transform:translateY(0) scale(1)}85%{opacity:1}to{transform:translateY(-120px);opacity:0}}
@keyframes unroll{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@keyframes beam{from{transform:scaleY(0);opacity:0}to{transform:scaleY(1);opacity:1}}
@keyframes pulse{from{opacity:.55}to{opacity:1}}
.w{display:inline-block;animation:wrd .45s ease-out both}
.hook{font-weight:900;text-transform:uppercase;letter-spacing:-.03em;line-height:1;text-align:center;width:880px;left:100px}
.mono{font-family:'Roboto Mono',monospace;font-weight:500;text-transform:uppercase;letter-spacing:.25em}
.tr{font-weight:600;font-size:44px;line-height:1.28;text-align:center;width:860px;left:110px;color:#fff}
.ar{font-family:'Amiri',serif;direction:rtl;color:#F0B429;font-size:62px;line-height:1.55;text-align:center;width:860px;left:110px;font-weight:700}
.ref{font-size:19px;color:#8a8a8a;text-align:center;width:860px;left:110px}
.gold{color:#F0B429}
.red{color:#E8382C}
svg.stage{overflow:visible}
svg path,svg circle,svg rect,svg line{fill:none;stroke:#fff;stroke-width:3;stroke-linecap:round;stroke-linejoin:round}
""")

def word(text, delay, cls="", style=""):
    return f'<span class="w {cls}" style="animation-delay:{delay}s;{style}">{text}</span> '

def static_word(text, cls="", style=""):
    return f'<span style="display:inline-block;{style}" class="{cls}">{text}</span> '

def scene(sid, t_out, inner, dur_out=0.4):
    html.append(f'<div id="{sid}" class="abs" style="left:0;top:0;width:1080px;height:1920px;animation:out {dur_out}s ease-in {t_out}s forwards">{inner}</div>')

# ---------- stage (character) ----------
chr_filter_kf = []
# brightness / aura timeline
def f(b, glow, col): return f"brightness({b}) drop-shadow(0 0 {glow}px {col})"
WHITE = "rgba(255,255,255,.9)"; FAINT = "rgba(255,255,255,.15)"; GOLDA = "rgba(240,180,41,.95)"
stops = [(0, f(1, 9, WHITE)), (5.8, f(1, 9, WHITE)), (7.0, f(.5, 3, FAINT)), (12.8, f(.5, 3, FAINT)),
         (14.4, f(1, 11, WHITE)), (32.0, f(1, 11, WHITE)), (34.0, f(1, 20, GOLDA)), (DUR, f(1, 20, GOLDA))]
css.append("@keyframes chr{" + "".join(f"{pct(t)}%{{filter:{v}}}" for t, v in stops) + "}")

limb_svg = ""
for k in LIMBS:
    limb_svg += f'<path id="{k}" d="{POSES["SIT"][k]}" style="animation:{", ".join(anims[k])}"/>'
head_svg = f'<circle r="20" cx="222" cy="250" style="animation:{", ".join(anims["H"])}"/>'
phone_svg = ('<g style="animation:out .4s ease-in 12.6s forwards">'
             '<rect x="236" y="284" width="14" height="24" rx="3" transform="rotate(-25 243 296)" style="stroke:#F5D485"/></g>')
rug_svg = ('<g style="transform-box:fill-box;transform-origin:left center;animation:unroll .9s ease-out 14.5s both">'
           '<polygon points="60,380 340,380 316,366 84,366" style="fill:#7A2618;stroke:#F0B429;stroke-width:2"/>'
           '<polygon points="96,376 304,376 292,369 108,369" style="fill:none;stroke:#C9922E;stroke-width:1.5"/>'
           '<path d="M200 376 L200 369" style="stroke:#C9922E;stroke-width:1.5"/></g>')
# SVG polygons need fill override (global CSS sets fill none)
css.append("svg polygon{stroke-linejoin:round}")

html.append('<div class="root" id="root">')
BG='position:absolute;left:0;top:0;width:1080px;height:1920px;background-size:cover;'
html.append(f'<div style="{BG}background-image:url(../media/night.jpg)"></div>')
html.append(f'<div style="{BG}background-image:url(../media/dusk.jpg);animation:out 2s ease-in-out 7s forwards"></div>')
html.append(f'<div style="{BG}background-image:url(../media/dawn.jpg);animation:in 2s ease-in-out 33.5s both"></div>')
html.append(f'<div style="{BG}background:rgba(0,0,0,.40);animation:in 2s ease-in-out 33.5s both"></div>')
html.append(f'<div style="{BG}background:rgba(0,0,0,.30);animation:in 1s ease-in-out 42.8s both"></div>')
html.append(f'<div style="{BG}background:linear-gradient(rgba(0,0,0,.38),rgba(0,0,0,.05) 55%,rgba(0,0,0,0))"></div>')

# halo behind key element
html.append('<div class="abs" style="left:90px;top:760px;width:900px;height:900px;border-radius:50%;'
            'background:radial-gradient(circle,rgba(240,163,26,.22) 0%,rgba(240,163,26,0) 65%);animation:in 1.2s ease-out 14.4s both, out .5s ease-in 40s forwards"></div>')
# light beam
html.append('<div class="abs" style="left:290px;top:720px;width:500px;height:800px;transform-origin:top center;'
            'clip-path:polygon(40% 0,60% 0,100% 100%,0 100%);'
            'background:linear-gradient(to bottom,rgba(245,212,133,.32),rgba(245,212,133,.04));animation:beam 1.4s ease-out 15s both, out .5s ease-in 40s forwards"></div>')

# stage with reflection: height ends exactly at floor
html.append('<div id="stagewrap" class="abs" style="left:60px;top:600px;width:960px;height:912px;'
            '">'
            f'<svg class="stage" viewBox="0 0 400 380" width="960" height="912" style="animation:out .5s ease-in 40s forwards">'
            f'{rug_svg}<g style="animation:chr {DUR}s linear 0s both">{limb_svg}{head_svg}{phone_svg}</g></svg></div>')
# phone glow S1-S2
html.append('<div class="abs" style="left:640px;top:880px;width:300px;height:300px;border-radius:50%;'
            'background:radial-gradient(circle,rgba(142,202,230,.28),rgba(142,202,230,0) 65%);animation:pulse 1s ease-in-out infinite alternate, out .4s ease-in 12.6s forwards"></div>')

# ---------- SCENE 1: hook (0 - 6) ----------
s1 = ('<div class="abs mono" style="top:150px;left:0;width:1080px;text-align:center;font-size:24px;color:#8a8a8a">Il est l&rsquo;heure de la pri&egrave;re</div>'
      '<div class="abs hook" style="top:230px;font-size:168px">'
      + static_word("ENCORE") + '<br>' + word("5 MINUTES", 0.5, style="color:#fff") + '</div>'
      '<div class="abs hook" style="top:620px;font-size:78px;color:#E7D9BC">'
      + word("sur", 1.3) + word("ton", 1.5) + word("t&eacute;l&eacute;phone", 1.7) + word("?", 2.0, "gold") + '</div>')
scene("s1", 5.7, s1)

# ---------- SCENE 2: tension (6 - 13) ----------
notifs = [("Nouveau message", 7.0, 80), ("Une derni&egrave;re vid&eacute;o", 7.8, 560), ("Story &agrave; voir", 8.6, 200), ("+27 notifications", 9.4, 520), ("En direct maintenant", 10.2, 140)]
nh = ""
for txt, t, x in notifs:
    nh += (f'<div class="abs" style="left:{x}px;top:880px;padding:16px 28px;border:2px solid {RED};border-radius:28px;'
           f'background:rgba(232,56,44,.12);color:{RED};font-size:30px;font-weight:600;animation:notif 2.6s ease-out {t}s both">{txt}</div>')
counter = ""
for lab, a, b in [("00:05", 6.4, 8.6), ("00:27", 8.6, 10.6), ("01:12", 10.6, 12.6)]:
    counter += (f'<div class="abs mono red" style="left:0;top:520px;width:1080px;text-align:center;font-size:62px;letter-spacing:.12em;'
                f'animation:in .2s ease-out {a}s both, out .2s ease-in {b-0.2}s forwards">{lab}</div>')
s2 = ('<div class="abs mono" style="top:150px;left:0;width:1080px;text-align:center;font-size:22px;color:#8a8a8a;animation:in .4s 6.2s both">Temps perdu</div>'
      + counter +
      '<div class="abs hook" style="top:240px;font-size:92px;color:#fff">'
      + word("Le", 6.3) + word("temps", 6.5) + word("file.", 6.8, "red") + '</div>'
      '<div class="abs hook" style="top:640px;font-size:70px;color:#E7D9BC">'
      + word("Et", 10.4) + word("la", 10.6) + word("pri&egrave;re", 10.8) + word("attend.", 11.2) + '</div>'
      + nh)
scene("s2", 12.6, s2)

# ---------- SCENE 3A: authority (13 - 22.2) ----------
def card(sid, t0, t1, arabic, fr_words, ref, ar_font=62):
    h = f'<div class="abs ar" style="top:130px;font-size:{ar_font}px;animation:in .8s ease-out {t0}s both">{arabic}</div>'
    d = t0 + 1.0
    words = ""
    for i, (w, gold) in enumerate(fr_words):
        words += word(w, round(d + i * 0.2, 2), "gold" if gold else "")
    h += f'<div class="abs tr" style="top:440px;left:230px;width:680px;font-size:42px">{words}</div>'
    h += f'<div class="abs mono ref" style="top:745px;animation:in .6s ease-out {t1-2.2}s both">{ref}</div>'
    scene(sid, t1, h)

frA = [("Le premier acte dont le serviteur aura &agrave; rendre compte, au Jour de la R&eacute;surrection, c&rsquo;est sa", False), ("pri&egrave;re.", True)]
# split FR words
def toks(s, goldset=()):
    return [(w, w.strip(".,;") in goldset or w in goldset) for w in s.split(" ")]
frA = toks("Le premier acte dont le serviteur aura &agrave; rendre compte, au Jour de la R&eacute;surrection, c&rsquo;est sa pri&egrave;re.", {"pri&egrave;re"})
frB = toks("Si elle est valable, il aura r&eacute;ussi et triomph&eacute; ; si elle est d&eacute;faillante, il aura &eacute;chou&eacute; et perdu.", {"r&eacute;ussi"})
arA = "إِنَّ أَوَّلَ مَا يُحَاسَبُ بِهِ الْعَبْدُ يَوْمَ الْقِيَامَةِ مِنْ عَمَلِهِ صَلاَتُهُ"
arB = "فَإِنْ صَلُحَتْ فَقَدْ أَفْلَحَ وَأَنْجَحَ وَإِنْ فَسَدَتْ فَقَدْ خَابَ وَخَسِرَ"
refA = "Ab&ucirc; Hurayra &middot; At-Tirmidh&icirc; 413 &middot; Authentique (Sah&icirc;h)"
card("s3a", 22.2, 22.2, "", [], "")  # placeholder removed below
html.pop()
card("s3a", 13.2, 22.2, arA, frA, refA)
card("s3b", 22.6, 32.2, arB, frB, refA)

# ---------- SCENE 4: payoff (32.4 - 40) ----------
dots = ""
names = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]
for i, n in enumerate(names):
    x = 150 + i * 190
    t = 35.0 + i * 0.5
    dots += (f'<div class="abs" style="left:{x}px;top:690px;width:60px;height:60px;border-radius:50%;border:3px solid #fff;'
             f'animation:in .3s ease-out 34.6s both, fillgold .4s ease-out {t}s forwards"></div>'
             f'<div class="abs mono" style="left:{x-40}px;top:770px;width:140px;text-align:center;font-size:17px;color:#8a8a8a;animation:in .3s ease-out 34.6s both">{n}</div>')
dust = ""
import random
random.seed(4)
for i in range(18):
    x = random.randint(300, 780); dx = random.randint(-120, 120)
    dust += (f'<div class="abs" style="left:{x}px;top:{1400+random.randint(-40,40)}px;width:8px;height:8px;border-radius:50%;background:#F5D485;'
             f'--dx:{dx}px;animation:rise {2.2+random.random()*1.5:.2f}s ease-out {33.0+random.random()*5:.2f}s both"></div>')
s4 = ('<div class="abs hook" style="top:200px;font-size:112px">'
      + word("Pose", 32.6) + word("ton", 32.9) + word("t&eacute;l&eacute;phone.", 33.2) + '</div>'
      '<div class="abs hook gold" style="top:520px;font-size:130px;color:#F0B429">'
      + word("Va", 34.0) + word("prier.", 34.3) + '</div>' + dots + dust)
scene("s4", 39.8, s4)

# ---------- SCENE 5: dedication + app (40 - 46) ----------
s5a = ('<div class="abs mono" style="top:210px;left:0;width:1080px;text-align:center;font-size:24px;color:#8a8a8a;animation:in .4s 40.2s both">Envoie &ccedil;a &agrave; quelqu&rsquo;un</div>'
       '<div class="abs hook" style="top:290px;font-size:104px">'
       + word("qui", 40.5) + word("retarde", 40.8) + word("sa", 41.1) + word("<span class=gold>pri&egrave;re.</span>", 41.4) + '</div>')
scene("s5a", 42.9, s5a)
lock = ('<div style="width:230px;height:230px;border-radius:24%;overflow:hidden;box-shadow:0 0 60px rgba(240,163,26,.35)">'
        '<img src="../media/logo.png" style="width:100%;height:100%;object-fit:cover;transform:scale(1.04)"></div>')
html.append('<div class="abs" style="left:240px;top:560px;width:600px;height:600px;border-radius:50%;'
            'background:radial-gradient(circle,rgba(240,163,26,.22),rgba(240,163,26,0) 65%);animation:in .8s ease-out 43.1s both"></div>')
html.append(f'<div class="abs" style="left:425px;top:600px;animation:pop .6s ease-out 43.3s both">{lock}</div>')
html.append('<div class="abs" style="left:0;top:870px;width:1080px;text-align:center;font-size:96px;font-weight:800;letter-spacing:-.03em;color:#FCF3E2;animation:up .6s ease-out 43.7s both">Salwaa</div>')
html.append('<div class="abs" style="left:140px;top:1010px;width:800px;text-align:center;font-size:36px;font-weight:400;line-height:1.35;color:#E7D9BC;animation:up .6s ease-out 44.1s both">Ton t&eacute;l&eacute;phone se met en pause<br>&agrave; l&rsquo;heure de la pri&egrave;re.</div>')
html.append('<div class="abs mono" style="left:0;top:1190px;width:1080px;text-align:center;font-size:24px;color:#F0B429;animation:in .5s ease-out 44.7s both">Lien dans la bio</div>')

# watermark
html.append('<div class="abs mono" style="left:0;top:1800px;width:1080px;text-align:center;font-size:18px;color:#555;letter-spacing:.5em">Salwaa &middot; Rappel</div>')
html.append('</div>')

out = f"""<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>Salwaa - Rappel</title>
<style>{''.join(css)}</style></head><body>{''.join(html)}</body></html>"""
open(sys.argv[1], "w").write(out)
print("ok", len(out))
