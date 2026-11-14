"""Trois vidéos courtes orientées téléchargement : l'app visible dès les 2 premières secondes."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import build_neon as B
from build_neon import fig, words, rug, box, page, KF, LAND, SNAP, GLIDE, GOLD, RED, REFLECT, P, POSES, ROOT

UI = "/_blob/51353ebe3284512c064a9e50c650e416"      # vraie capture de l'accueil Salwaa (780×3320)
LOGO = "/_blob/33641f46cd42014a7806f0b689266470"
POSES["PHONE"] = P("T M200 146 L200 202 L200 258|AL M200 162 L188 212 L184 258|AR M200 162 L222 206 L250 180|" + B.LEGS + "|H 205,128")

CSS = '''
@keyframes type{from{clip-path:inset(0 100% 0 0)}to{clip-path:inset(0 0 0 0)}}
@keyframes popIn{from{opacity:0;transform:scale(.4)}to{opacity:1;transform:none}}
@keyframes stampIn{from{opacity:0;transform:scale(2.2) rotate(-18deg)}to{opacity:1;transform:scale(1) rotate(-8deg)}}
@keyframes dot{from{background:transparent;border-color:rgba(255,255,255,.3);transform:scale(.7);box-shadow:none}to{background:#F0B429;border-color:#F0B429;transform:scale(1);box-shadow:0 0 22px rgba(240,180,41,.65)}}
@keyframes c35{from{--n:0}to{--n:35}}
.c35::before{counter-reset:n var(--n);content:counter(n)}
'''

def top(text, t0, t1, y=170, size=84, **kw):
    return (f'<div style="position:absolute;left:70px;right:70px;top:{y}px;text-align:center;font-weight:800;font-size:{size}px;line-height:1.06;letter-spacing:-.03em;'
            f'animation:fout .25s ease-in {t1}s forwards">{words(text, t0, **kw)}</div>')

def cta(t0, line, gold=()):
    return f'''<div style="position:absolute;inset:0;background:rgba(8,5,1,.965);animation:fin .4s ease-out {t0-.3}s both"></div>
<div style="position:absolute;left:70px;right:70px;top:330px;display:flex;flex-direction:column;align-items:center;gap:44px;text-align:center">
 <div style="font-weight:800;font-size:82px;line-height:1.08;letter-spacing:-.03em">{words(line, t0, 0.11, gold=gold)}</div>
 <img src="{LOGO}" alt="Logo Salwaa" style="margin-top:20px;width:260px;height:260px;border-radius:58px;box-shadow:0 0 90px rgba(240,163,26,.5);animation:popIn .6s {LAND} {t0+.5}s both">
 <div style="display:flex;align-items:center;gap:26px;width:780px;height:124px;box-sizing:border-box;padding:0 44px;border-radius:999px;background:#1E1608;border:3px solid {GOLD};box-shadow:0 0 40px rgba(240,180,41,.3);animation:in .5s {LAND} {t0+.8}s both">
  <svg width="54" height="54" viewBox="0 0 24 24" fill="none" stroke="{GOLD}" stroke-width="2.6" stroke-linecap="round"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 21 21"/></svg>
  <span style="font-weight:700;font-size:62px;letter-spacing:-.02em;white-space:nowrap;animation:type .7s steps(6) {t0+1.1}s both">Salwaa</span>
 </div>
 <div style="font-weight:700;font-size:50px;color:#E7D9BC;animation:in .5s ease-out {t0+1.5}s both">Tape « Salwaa » et télécharge.</div>
 <div class="mono" style="height:78px;padding:0 42px;box-sizing:border-box;border-radius:999px;border:2px solid {GOLD};color:{GOLD};font-size:26px;display:flex;align-items:center;animation:in .5s ease-out {t0+1.8}s both,glowpill 2s ease-in-out {t0+2.3}s infinite">Lien dans la bio</div>
</div>'''

def pause_icon(size):
    return (f'<div style="width:{size}px;height:{size}px;border-radius:50%;background:{GOLD};display:flex;align-items:center;justify-content:center;gap:{size*0.12}px;box-shadow:0 0 {size*0.5}px rgba(240,180,41,.7)">'
            f'<div style="width:{size*0.14}px;height:{size*0.42}px;border-radius:6px;background:#120C04"></div><div style="width:{size*0.14}px;height:{size*0.42}px;border-radius:6px;background:#120C04"></div></div>')

# ───────────────────────── 11 : LA DÉMO (13 s) ─────────────────────────
def v11():
    W, H, X, Y = 560, 1150, 260, 430
    cols = ["#E8553A", "#3A7BE8", "#2FB37A", "#B04AE8", "#E8B03A"]
    cards = "".join(
        f'<div style="height:{H}px;background:linear-gradient(160deg,{c},#111 140%);position:relative">'
        f'<div style="position:absolute;left:50%;top:44%;width:0;height:0;margin-left:-34px;border-left:86px solid rgba(255,255,255,.85);border-top:54px solid transparent;border-bottom:54px solid transparent"></div>'
        f'<div style="position:absolute;left:34px;bottom:120px;width:300px;height:22px;border-radius:11px;background:rgba(255,255,255,.8)"></div><div style="position:absolute;left:34px;bottom:78px;width:200px;height:18px;border-radius:9px;background:rgba(255,255,255,.5)"></div>'
        f'<div style="position:absolute;right:30px;bottom:140px;width:64px;height:64px;border-radius:50%;background:rgba(255,255,255,.75)"></div><div style="position:absolute;right:30px;bottom:240px;width:64px;height:64px;border-radius:50%;background:rgba(255,255,255,.55)"></div></div>' for c in cols)
    for i in range(3):
        KF.append(f"@keyframes sw{i}{{from{{transform:translateY({-H*i}px)}}to{{transform:translateY({-H*(i+1)}px)}}}}")
    k = (W - 12) / 780.0
    body = f'''
<div class="mono" style="position:absolute;left:0;right:0;top:110px;text-align:center;font-size:30px;color:{GOLD};animation:in .3s ease-out 0s both,fout .3s ease-in 8.9s forwards">Dhuhr · 13:30</div>
{top("L'adhan sonne. Toi, tu scrolles.", 0.0, 1.75, y=180, red=("scrolles.",))}
{top("Salwaa met tes apps en pause.", 1.9, 3.75, y=180, gold=("Salwaa", "pause."))}
{top("Le temps de prier.", 3.95, 6.3, y=220, size=96, gold=("prier.",))}
{top("Tes 5 prières. Ta série. Chaque jour.", 6.5, 8.9, y=180, gold=("série.",))}
<div style="position:absolute;left:{X}px;top:{Y}px;width:{W}px;height:{H}px;animation:in .4s {LAND} 0s both,shake .45s linear 1.8s both">
 <div style="position:absolute;inset:0;border-radius:70px;border:6px solid #3A2C13;background:#000;overflow:hidden;box-shadow:0 0 0 3px #1E1608,0 40px 120px rgba(0,0,0,.7),0 0 90px rgba(240,180,41,.18)">
  <div style="animation:sw0 .28s {GLIDE} .45s forwards,sw1 .28s {GLIDE} .95s forwards,sw2 .28s {GLIDE} 1.4s forwards">{cards}</div>
  <div style="position:absolute;inset:0;background:rgba(18,12,4,.82);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:36px;animation:fin .25s ease-out 1.8s both">
   <div style="animation:popIn .5s {LAND} 1.85s both">{pause_icon(210)}</div>
   <div class="mono" style="font-size:34px;color:{GOLD};animation:in .4s ease-out 2.2s both">Apps en pause</div>
  </div>
  <div style="position:absolute;inset:0;background:#FAF5EB;overflow:hidden;animation:fin .5s ease-out 3.9s both">
   <img src="{UI}" alt="Écran d'accueil de Salwaa" style="display:block;width:{W-12}px;animation:scr 1.5s {GLIDE} 6.3s forwards">
  </div>
 </div>
</div>
<div class="mono" style="position:absolute;left:0;right:0;top:{Y+H+34}px;text-align:center;font-size:24px;color:#8C7E62;animation:fin .4s ease-out 4.2s both,fout .3s ease-in 8.9s forwards">Vraie capture de l'app Salwaa</div>
{cta(9.3, "Prie d'abord. Scrolle après.", gold=("d'abord.",))}
'''
    css = CSS + f"@keyframes scr{{from{{transform:none}}to{{transform:translateY({-int(1150*k)+330}px)}}}}"
    return page("Promo 11 — La démo", body, css).replace("background:#000;font-family", "background:#120C04;font-family"), 13.0

# ───────────────────────── 12 : LE DÉFI 7 JOURS (12,5 s) ─────────────────────────
def v12():
    dots = []
    for c in range(7):
        for r in range(5):
            t = 1.9 + (c * 5 + r) * 0.13
            dots.append(f'<div style="position:absolute;left:{104 + c*130}px;top:{640 + r*124}px;width:92px;height:92px;box-sizing:border-box;border-radius:50%;border:4px solid rgba(255,255,255,.3);animation:dot .3s {LAND} {t:.2f}s both"></div>')
    days = "".join(f'<div class="mono" style="position:absolute;left:{104 + c*130}px;top:570px;width:92px;text-align:center;font-size:30px;letter-spacing:0;color:#BFAE93">{d}</div>' for c, d in enumerate("LMMJVSD"))
    kc = 900 / 780.0
    body = f'''
<div class="mono" style="position:absolute;left:0;right:0;top:130px;text-align:center;font-size:30px;color:#BFAE93;animation:in .3s ease-out 0s both">Défi Salwaa</div>
<div style="position:absolute;left:60px;right:60px;top:190px;text-align:center;font-weight:900;font-size:124px;line-height:1;letter-spacing:-.04em">{words("7 jours.", 0.0, .14, gold=("7",))}</div>
<div style="position:absolute;left:60px;right:60px;top:340px;text-align:center;font-weight:800;font-size:76px;line-height:1.05;letter-spacing:-.03em">{words("Zéro prière ratée.", 0.45, .13, gold=("Zéro",))}</div>
{days}{"".join(dots)}
<div class="mono" style="position:absolute;left:0;right:0;top:1272px;text-align:center;font-size:23px;color:#8C7E62">Fajr · Dhuhr · Asr · Maghrib · Isha</div>
<div style="position:absolute;left:0;right:0;top:1330px;display:flex;justify-content:center;align-items:baseline;gap:14px"><span class="c35" style="font-weight:900;font-size:150px;line-height:1;letter-spacing:-.04em;color:{GOLD};animation:c35 4.55s linear 1.9s both"></span><span style="font-weight:800;font-size:64px;color:#BFAE93">/ 35 prières</span></div>
<div style="position:absolute;left:70px;right:70px;top:1500px;text-align:center;font-weight:700;font-size:48px;line-height:1.15;letter-spacing:-.02em">{words("À chaque adhan, Salwaa met tes apps en pause.", 2.6, .11, gold=("Salwaa",))}</div>
<div style="position:absolute;inset:0;background:rgba(8,5,1,.965);animation:fin .4s ease-out 6.8s both"></div>
<div style="position:absolute;left:70px;right:70px;top:420px;text-align:center;font-weight:800;font-size:88px;line-height:1.06;letter-spacing:-.03em;animation:fout .25s ease-in 9.2s forwards">{words("Ta série se voit dans l'app.", 7.0, .12, gold=("série",))}</div>
<div style="position:absolute;left:90px;top:760px;width:900px;height:318px;border-radius:44px;overflow:hidden;box-shadow:0 0 0 4px {GOLD},0 0 90px rgba(240,180,41,.45);animation:popIn .6s {LAND} 7.4s both,fout .25s ease-in 9.2s forwards">
 <img src="{UI}" alt="Carte « jours d'affilée » de Salwaa" style="display:block;width:900px;margin-top:{-int(1205*kc)}px">
</div>
<div class="mono" style="position:absolute;left:0;right:0;top:1120px;text-align:center;font-size:24px;color:#8C7E62;animation:fin .4s ease-out 7.8s both,fout .25s ease-in 9.2s forwards">Vraie capture de l'app Salwaa</div>
{cta(9.5, "Tu commences ce soir ? Écris « JOUR 1 ».", gold=("JOUR", "1"))}
'''
    return page("Promo 12 — Le défi 7 jours", body, CSS).replace("background:#000;font-family", "background:#120C04;font-family"), 12.8

# ───────────────────────── 13 : SANS / AVEC (13 s) ─────────────────────────
def v13():
    F, S = 1130, 560; k = S / 400.0
    def phone(cx, extra):
        return f'<div style="position:absolute;left:{cx - S/2 + 240*k}px;top:{F - S*0.95 + 150*k}px;width:30px;height:50px;border-radius:7px;border:3px solid #fff;background:rgba(160,200,255,.35);box-shadow:0 0 18px rgba(160,200,255,.8);{extra}"></div>'
    notifs = "".join(box(l, 0, i * 62, 190, 56, 1.5 + i * 0.85, extra=f",toRedB .4s linear {1.9 + i*0.85}s forwards", size=20) for i, l in enumerate(["1 vidéo", "Encore 1", "Notif", "Live", "Story", "…"]))
    lseq = [(0, "PHONE", 0), (7.2, "DESPAIR", .7)]
    rseq = [(0, "PHONE", 0), (2.4, "STAND", .5), (3.1, "RUKU", .7), (3.9, "SUJUD", .8), (5.3, "KNEEL", .6), (6.0, "STAND", .6)]
    def bar(x, col, anim):
        return (f'<div class="mono" style="position:absolute;left:{x}px;top:{F+56}px;width:400px;text-align:center;font-size:22px;color:#8C7E62">Temps de Dhuhr</div>'
                f'<div style="position:absolute;left:{x}px;top:{F+100}px;width:400px;height:16px;border-radius:8px;background:rgba(255,255,255,.14);overflow:hidden"><div style="width:100%;height:100%;background:{col};transform-origin:0 50%;animation:{anim}"></div></div>')
    body = f'''
<div style="position:absolute;left:60px;right:60px;top:150px;text-align:center;font-weight:900;font-size:116px;line-height:1;letter-spacing:-.04em">{words("L'adhan sonne.", 0.0, .16)}</div>
<div class="mono" style="position:absolute;left:0;width:540px;top:330px;text-align:center;font-size:38px;color:#FF5A4E;animation:in .4s {LAND} .5s both">Sans Salwaa</div>
<div class="mono" style="position:absolute;left:540px;width:540px;top:330px;text-align:center;font-size:38px;color:{GOLD};animation:in .4s {LAND} .7s both">Avec Salwaa</div>
<div style="position:absolute;left:539px;top:420px;width:2px;height:{F-420}px;background:linear-gradient(transparent,rgba(255,255,255,.25),transparent)"></div>
<div style="position:absolute;left:0;top:0;width:1080px;height:{F}px;{REFLECT}">
 {fig(210, F, S, lseq)}
 {phone(210, "animation:fout .3s ease-in 7.2s forwards")}
 <div style="position:absolute;left:330px;bottom:0;width:190px;height:10px"><div style="position:absolute;left:0;bottom:0">{notifs}</div></div>
 {rug(815, F, 330, 2.3)}
 {fig(800, F, S, rseq)}
 {phone(800, "animation:fout .3s ease-in 2.4s forwards")}
 <div style="position:absolute;left:{800 - S/2 + 240*k - 26}px;top:{F - S*0.95 + 150*k - 104}px;animation:popIn .45s {LAND} 1.7s both,fout .3s ease-in 2.5s forwards">{pause_icon(84)}</div>
</div>
<div style="position:absolute;left:0;top:{F}px;width:1080px;height:3px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.55) 15%,rgba(255,255,255,.55) 85%,transparent)"></div>
{bar(70, RED, "drainL 5.6s linear 1.4s both")}
{bar(610, GOLD, "drainR 1.6s ease-out 1.4s both")}
<div class="mono" style="position:absolute;left:70px;top:520px;width:400px;text-align:center;font-size:54px;font-weight:500;color:#FF5A4E;border:5px solid #E8382C;border-radius:14px;padding:14px 0;box-sizing:border-box;background:rgba(0,0,0,.6);animation:stampIn .35s {SNAP} 7.0s both">Ratée</div>
<div class="mono" style="position:absolute;left:600px;top:520px;width:420px;text-align:center;font-size:40px;font-weight:500;color:{GOLD};border:4px solid {GOLD};border-radius:14px;padding:18px 0;box-sizing:border-box;background:rgba(0,0,0,.6);box-shadow:0 0 40px rgba(240,180,41,.4);animation:popIn .45s {LAND} 6.3s both">✓ À l'heure</div>
{B.cap("Même adhan. Même téléphone.", 0.9, 3.0, y=1400, size=62)}
{B.cap("À droite, ses apps se mettent en pause.", 3.2, 6.9, y=1400, size=60, gold=("pause.",))}
{B.cap("La seule différence : une app.", 7.5, 9.2, y=1400, size=62, gold=("une", "app."))}
{cta(9.5, "Mets-toi du bon côté.", gold=("bon", "côté."))}
'''
    css = CSS + "@keyframes drainL{from{transform:scaleX(1)}to{transform:scaleX(0)}}@keyframes drainR{from{transform:scaleX(1)}to{transform:scaleX(.82)}}"
    return page("Promo 13 — Sans / Avec", body, css), 13.0

if __name__ == "__main__":
    for name, fn in (("Promo11", v11), ("Promo12", v12), ("Promo13", v13)):
        html, dur = fn()
        (ROOT / f"{name}.dc.html").write_text(html)
        print(name, dur)
