"""Trois rappels « néon » (fond noir, bonhomme en traits blancs, accent or)."""
import pathlib, itertools
ROOT = pathlib.Path(__file__).parent.parent / "pages"
LAND = "linear(0,.35 10%,.95 26%,1.08 38%,.99 55%,1 100%)"
SNAP = "linear(0,.25 8%,.7 20%,1.04 34%,1.01 48%,1 100%)"
GLIDE = "cubic-bezier(.45,0,.2,1)"
GOLD, RED = "#F0B429", "#E8382C"
_uid = itertools.count()
KF = []          # keyframes générés

def P(s):
    d = {}
    for part in s.split("|"):
        k, v = part.strip().split(" ", 1)
        d[k] = v.strip()
    return d

LEGS = "LL M200 258 L192 320 L186 380|LR M200 258 L208 320 L214 380"
POSES = {
 "STAND": P("T M200 146 L200 202 L200 258|AL M200 162 L188 212 L184 258|AR M200 162 L212 212 L216 258|" + LEGS + "|H 200,126"),
 "REACH": P("T M202 146 L201 202 L200 258|AL M202 162 L192 212 L190 258|AR M202 162 L246 176 L286 150|" + LEGS + "|H 204,126"),
 "REACH2": P("T M202 146 L201 202 L200 258|AL M202 162 L240 150 L278 118|AR M202 162 L246 190 L288 196|" + LEGS + "|H 206,126"),
 "CARRY": P("T M200 146 L200 202 L200 258|AL M200 162 L166 132 L172 96|AR M200 162 L234 132 L228 96|" + LEGS + "|H 200,126"),
 "CROUCH": P("T M200 196 L200 246 L200 296|AL M200 212 L164 182 L172 146|AR M200 212 L236 182 L228 146|LL M200 296 L166 334 L186 380|LR M200 296 L236 334 L214 380|H 200,176"),
 "LOW": P("T M200 246 L200 286 L200 326|AL M200 262 L162 232 L172 196|AR M200 262 L238 232 L228 196|LL M200 326 L156 348 L186 380|LR M200 326 L246 348 L214 380|H 200,226"),
 "RUKU": P("T M250 252 L215 255 L180 258|AL M246 256 L224 290 L204 318|AR M246 256 L232 292 L212 320|LL M180 258 L190 320 L194 380|LR M180 258 L196 320 L204 380|H 270,246"),
 "SUJUD": P("T M230 352 L192 334 L152 320|AL M228 354 L238 372 L256 380|AR M228 354 L244 374 L264 380|LL M152 320 L164 378 L104 380|LR M152 320 L170 378 L112 380|H 262,364"),
 "KNEEL": P("T M212 232 L208 266 L202 300|AL M212 246 L238 290 L262 330|AR M212 246 L244 292 L270 334|LL M202 300 L244 372 L176 378|LR M202 300 L238 376 L170 380|H 218,212"),
 "DESPAIR": P("T M214 240 L208 270 L202 300|AL M214 252 L246 262 L230 222|AR M214 252 L250 266 L236 226|LL M202 300 L244 372 L176 378|LR M202 300 L238 376 L170 380|H 224,218"),
}

def fig(cx, floor, size, seq, flip=False, style=""):
    """seq = [(t, pose, dur)], le premier à t=0."""
    u = f"f{next(_uid)}"
    first = POSES[seq[0][1]]
    out = []
    for part, w in (("T", 9), ("AL", 7), ("AR", 7), ("LL", 7), ("LR", 7)):
        anims = []
        for i in range(1, len(seq)):
            t, pose, dur = seq[i]
            a, b = POSES[seq[i-1][1]][part], POSES[pose][part]
            n = f"{u}{part}{i}"
            KF.append(f"@keyframes {n}{{from{{d:path('{a}')}}to{{d:path('{b}')}}}}")
            anims.append(f"{n} {dur}s {GLIDE} {t}s forwards")
        st = f' style="animation:{",".join(anims)}"' if anims else ""
        out.append(f'<path d="{first[part]}" stroke-width="{w}"{st}/>')
    anims = []
    for i in range(1, len(seq)):
        t, pose, dur = seq[i]
        ax, ay = POSES[seq[i-1][1]]["H"].split(","); bx, by = POSES[pose]["H"].split(",")
        n = f"{u}H{i}"
        KF.append(f"@keyframes {n}{{from{{cx:{ax}px;cy:{ay}px}}to{{cx:{bx}px;cy:{by}px}}}}")
        anims.append(f"{n} {dur}s {GLIDE} {t}s forwards")
    hx, hy = first["H"].split(",")
    st = f' style="animation:{",".join(anims)}"' if anims else ""
    out.append(f'<circle cx="{hx}" cy="{hy}" r="19" fill="#fff" stroke="none"{st}/>')
    tf = "transform:scaleX(-1);" if flip else ""
    return (f'<svg viewBox="0 0 400 400" style="position:absolute;left:{cx-size/2}px;top:{floor-size*0.95}px;width:{size}px;height:{size}px;overflow:visible;'
            f'{tf}filter:drop-shadow(0 0 7px rgba(255,255,255,.55));{style}" fill="none" stroke="#fff" stroke-linecap="round" stroke-linejoin="round">{"".join(out)}</svg>')

def words(text, t0, step=0.13, gold=(), red=()):
    out = []
    for i, w in enumerate(text.split()):
        c = f"color:{GOLD};" if any(g in w for g in gold) else (f"color:#FF5A4E;" if any(g in w for g in red) else "")
        out.append(f'<span style="display:inline-block;margin-right:.24em;{c}animation:wrd .4s {LAND} {t0+i*step:.2f}s both">{w}</span>')
    return "".join(out)

def cap(text, t0, t1, y=1400, size=60, **kw):
    return (f'<div style="position:absolute;left:70px;right:70px;top:{y}px;text-align:center;font-weight:700;font-size:{size}px;line-height:1.16;letter-spacing:-.02em;'
            f'animation:fout .3s ease-in {t1}s forwards">{words(text, t0, **kw)}</div>')

def rug(cx, floor, w, t, flip=False):
    s = w / 240.0
    tf = "scaleX(-1)" if flip else ""
    return (f'<svg viewBox="80 368 246 22" style="position:absolute;left:{cx-w/2}px;top:{floor-14*s}px;width:{w}px;height:{22*s}px;overflow:visible;transform:{tf}">'
            f'<g style="transform-origin:84px 380px;animation:unroll .7s {GLIDE} {t}s both"><polygon points="84,386 306,386 322,373 100,373" fill="rgba(240,180,41,.18)" stroke="{GOLD}" stroke-width="3" style="filter:drop-shadow(0 0 8px rgba(240,180,41,.7))"/></g></svg>')

def box(label, left, bottom, w, h, t, extra="", cls="", size=26):
    return (f'<div class="bx {cls}" style="left:{left}px;bottom:{bottom}px;width:{w}px;height:{h}px;font-size:{size}px;animation:drop .55s {LAND} {t}s both{extra}">{label}</div>')

def hadith(t0, t1, kicker, ar, fr_html, src, top=250, ar_size=58, fr_size=58):
    return f'''<div style="position:absolute;left:80px;right:80px;top:{top}px;animation:panelIn .7s {LAND} {t0}s both,fout .4s ease-in {t1}s forwards">
 <div style="display:flex;align-items:center;gap:20px"><div style="width:90px;height:4px;background:{GOLD};transform-origin:0 50%;animation:line .5s ease-out {t0+.15}s both"></div><div class="mono" style="font-size:26px;color:{GOLD}">{kicker}</div></div>
 <div dir="rtl" style="margin-top:30px;font-family:Amiri,serif;font-weight:700;font-size:{ar_size}px;line-height:1.55;color:{GOLD};text-align:right;text-shadow:0 0 24px rgba(240,180,41,.45);animation:in .6s ease-out {t0+.35}s both">{ar}</div>
 <div style="margin-top:28px;font-weight:700;font-size:{fr_size}px;line-height:1.18;letter-spacing:-.02em">{fr_html}</div>
 <div class="mono" style="margin-top:30px;font-size:25px;color:#BFAE93;animation:fin .5s ease-out {t0+3.0}s both">{src}</div>
</div>'''

def endcard(t0, line, top=470, gold=()):
    return f'''<div style="position:absolute;left:70px;right:70px;top:{top}px;display:flex;flex-direction:column;align-items:center;gap:30px;text-align:center">
 <div style="font-weight:800;font-size:76px;line-height:1.08;letter-spacing:-.03em">{words(line, t0, 0.12, gold=gold)}</div>
 <div style="margin-top:40px;display:flex;align-items:center;gap:26px;animation:in .5s {LAND} {t0+.9}s both">
  <img src="/_blob/33641f46cd42014a7806f0b689266470" alt="Logo Salwaa" style="width:130px;height:130px;border-radius:29px;box-shadow:0 0 60px rgba(240,163,26,.5)">
  <div style="text-align:left"><div style="font-weight:800;font-size:66px;line-height:1;letter-spacing:-.03em">Salwaa</div><div style="margin-top:8px;font-weight:600;font-size:30px;color:#E7D9BC">Tes apps en pause à chaque prière</div></div>
 </div>
 <div class="mono" style="height:74px;padding:0 40px;box-sizing:border-box;border-radius:999px;border:2px solid {GOLD};color:{GOLD};font-size:25px;display:flex;align-items:center;animation:in .5s ease-out {t0+1.2}s both,glowpill 2s ease-in-out {t0+1.7}s infinite">Lien dans la bio</div>
</div>'''

CSS = '''
body{margin:0}
@property --n{syntax:'<integer>';inherits:true;initial-value:0}
@keyframes in{from{opacity:0;transform:translateY(26px)}to{opacity:1;transform:none}}
@keyframes wrd{from{opacity:0;transform:translateY(34px) scale(.92)}to{opacity:1;transform:none}}
@keyframes fin{from{opacity:0}to{opacity:1}}
@keyframes fout{from{opacity:1}to{opacity:0}}
@keyframes drop{from{opacity:0;transform:translateY(-700px) rotate(-4deg)}12%{opacity:1}to{opacity:1;transform:none}}
@keyframes unroll{from{opacity:0;transform:scaleX(0)}30%{opacity:1}to{opacity:1;transform:scaleX(1)}}
@keyframes panelIn{from{opacity:0;transform:translateY(-50px) scale(.95)}to{opacity:1;transform:none}}
@keyframes line{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@keyframes glowpill{0%,100%{box-shadow:0 0 0 0 rgba(240,163,26,0)}50%{box-shadow:0 0 40px 4px rgba(240,163,26,.45)}}
@keyframes toGold{from{border-color:#fff;color:#fff;box-shadow:none}to{border-color:#F0B429;color:#F0B429;box-shadow:0 0 26px rgba(240,180,41,.55),inset 0 0 18px rgba(240,180,41,.18)}}
@keyframes toRedB{from{border-color:#fff;color:#fff}to{border-color:#E8382C;color:#FF5A4E}}
@keyframes shake{0%,100%{transform:none}20%{transform:translateX(-12px)}40%{transform:translateX(10px)}60%{transform:translateX(-7px)}80%{transform:translateX(5px)}}
@keyframes pulse{0%,100%{transform:scale(1)}40%{transform:scale(1.06)}}
@keyframes breathe{0%,100%{transform:scale(1)}50%{transform:scale(1.03)}}
.mono{font-family:'Roboto Mono',monospace;font-weight:500;text-transform:uppercase;letter-spacing:.24em}
.bx{position:absolute;box-sizing:border-box;border:3px solid #fff;border-radius:6px;background:#000;display:flex;align-items:center;justify-content:center;font-family:'Roboto Mono',monospace;font-weight:500;letter-spacing:.2em;text-transform:uppercase;color:#fff}
'''

def page(title, body, extra_css=""):
    kf = "\n".join(KF); KF.clear()
    return f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800;900&amp;family=Roboto+Mono:wght@500&amp;family=Amiri:wght@400;700&amp;display=swap" rel="stylesheet">
<style>{CSS}{extra_css}
{kf}
</style>
</helmet>
<div style="position:relative;width:1080px;height:1920px;overflow:hidden;background:#000;font-family:Poppins,sans-serif;color:#fff">
<div style="position:absolute;inset:0;background:radial-gradient(900px 800px at 50% 45%,rgba(255,255,255,.06),transparent 70%)"></div>
{body}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":1080,"height":1920}}}}'>
class Component extends DCLogic {{
renderVals() {{
return {{}};
}}
}}
</script>
</body>
</html>
'''

REFLECT = "-webkit-box-reflect:below 0 linear-gradient(transparent 62%,rgba(0,0,0,.32))"

# ───────────────────────── VIDÉO 08 : BARAKA (22,5 s) ─────────────────────────
def v08():
    F = 1160
    lt = ["Mails", "Scroll", "Courses", "Réunion", "Série", "Notifs", "Retard"]
    left = []
    falls = [(-150, -14), (120, 22), (-60, 80), (170, -40), (-190, 30), (60, -70), (10, 95)]
    for i, lab in enumerate(lt):
        t = 1.5 + i * 0.8
        dx, rot = falls[i]
        n = f"fall{i}"
        KF.append(f"@keyframes {n}{{from{{transform:none}}to{{transform:translate({dx}px,{i*60 - (i%3)*18}px) rotate({rot}deg)}}}}")
        jit = (-10, 12, -6, 14, -12, 8, -4)[i]
        left.append(box(lab, 20 + jit, i * 60, 200, 56, t, extra=f",{n} .9s cubic-bezier(.5,0,.9,.6) {8.9 + (6-i)*0.05}s forwards,toRedB .4s linear 8.9s forwards", size=22))
    rt = ["Travail", "Famille", "Repos", "Projets"]
    right = [box(lab, 0, i * 84, 240, 78, 6.0 + i * 1.45, extra=f",toGold .8s ease-out {12.4 + i*0.12}s forwards", size=26) for i, lab in enumerate(rt)]
    lseq = [(0, "STAND", 0)]
    t = 1.3; k = 0
    while t < 8.4:
        lseq.append((t, ("REACH", "REACH2")[k % 2], .28)); t += .4; k += 1
    lseq.append((9.3, "DESPAIR", .7))
    rseq = [(0, "STAND", 0), (1.5, "RUKU", .7), (2.3, "SUJUD", .8), (4.5, "KNEEL", .7), (5.3, "STAND", .7)]
    for i in range(4):
        t = 5.9 + i * 1.45
        rseq += [(t, "REACH", .35), (t + .6, "STAND", .4)]
    body = f'''
<div class="mono" style="position:absolute;left:0;right:0;top:230px;text-align:center;font-size:84px;font-weight:500;letter-spacing:.34em;padding-left:.34em;color:{GOLD};text-shadow:0 0 30px rgba(240,180,41,.35);animation:fin .6s ease-out 0s both,glowT 1.2s ease-out 12.4s forwards">Baraka</div>
<div style="position:absolute;left:539px;top:560px;width:2px;height:600px;background:linear-gradient(transparent,rgba(255,255,255,.22),transparent)"></div>
<div style="position:absolute;left:0;top:0;width:1080px;height:{F}px;{REFLECT}">
 {fig(150, F, 520, lseq)}
 <div style="position:absolute;left:270px;bottom:0;width:240px;height:10px;transform-origin:50% 100%;animation:wob 2.6s ease-in-out 6.2s both"><div style="position:absolute;left:0;bottom:0">{"".join(left)}</div></div>
 {rug(900, F, 300, 1.0, flip=True)}
 {fig(900, F, 520, rseq, flip=True)}
 <div style="position:absolute;left:570px;bottom:0;width:240px;height:10px">{"".join(right)}</div>
</div>
<div style="position:absolute;left:0;top:{F}px;width:1080px;height:3px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.55) 15%,rgba(255,255,255,.55) 85%,transparent)"></div>
<div class="mono" style="position:absolute;left:0;width:540px;top:{F+50}px;text-align:center;font-size:34px;color:#FF5A4E;animation:in .4s ease-out .5s both">« Après »</div>
<div class="mono" style="position:absolute;left:540px;width:540px;top:{F+50}px;text-align:center;font-size:34px;color:{GOLD};animation:in .4s ease-out .8s both">« D'abord »</div>
{cap("Deux journées. Les mêmes 24 heures.", 0.15, 3.3, gold=("24",))}
{cap("L'un remet sa prière à « après ». L'autre commence par elle.", 3.6, 8.7, step=.12, red=("après",), gold=("commence", "par", "elle."))}
{cap("Sans Lui, tout s'éparpille.", 9.4, 12.2, red=("s'éparpille.",))}
{cap("Avec Lui, tout se rassemble.", 12.6, 14.5, gold=("se", "rassemble."))}
<div style="position:absolute;inset:0;background:rgba(0,0,0,.86);animation:fin .6s ease-out 14.5s both"></div>
{hadith(14.8, 19.3, 'Le Prophète <span style="font-family:Amiri,serif;letter-spacing:0;font-size:32px;text-transform:none;font-weight:400">صلى الله عليه وسلم</span> a dit',
        "من كانت الآخرة همّه جعل الله غناه في قلبه وجمع له شمله",
        words("Celui dont l'au-delà est le souci, Allah met la richesse dans son cœur et rassemble ses affaires.", 15.6, .11, gold=("rassemble", "ses", "affaires.")),
        "At-Tirmidhî 2465 · authentifié par Al-Albânî", top=400)}
{endcard(19.6, "Tu commences par quoi, toi ?", gold=("quoi,",))}
'''
    css = "@keyframes wob{0%{transform:rotate(0)}25%{transform:rotate(2deg)}50%{transform:rotate(-3deg)}75%{transform:rotate(4.5deg)}100%{transform:rotate(-2deg)}}@keyframes glowT{from{text-shadow:0 0 30px rgba(240,180,41,.35)}to{text-shadow:0 0 60px rgba(240,180,41,.95),0 0 120px rgba(240,180,41,.5)}}"
    return page("Rappel 08 — Baraka", body, css), 22.5

# ───────────────────────── VIDÉO 09 : LE POIDS (20,5 s) ─────────────────────────
def v09():
    F = 1200; S = 780; k = S / 400.0
    labs = ["Loyer", "Examens", "Dettes", "Famille", "Avenir", "Solitude"]
    top0 = F - S * 0.95 + 96 * k          # y des mains en pose CARRY
    bxs = []
    for i, lab in enumerate(labs):
        t = 0.55 + i * 0.8
        jit = (-14, 16, -8, 12, -18, 6)[i]
        n = f"lift{i}"
        KF.append(f"@keyframes {n}{{from{{opacity:1;transform:none}}to{{opacity:0;transform:translateY(-520px) scale(.8)}}}}")
        bxs.append(box(lab, -160 + jit, i * 84, 320, 76, t, extra=f",toGold .5s ease-out {8.0 + (5-i)*0.38}s forwards,{n} 1.1s cubic-bezier(.4,0,.8,.6) {8.3 + (5-i)*0.38}s forwards", size=28))
    seq = [(0, "STAND", 0), (0.25, "CARRY", .35), (2.4, "CROUCH", .6), (4.2, "LOW", .6), (7.3, "SUJUD", .9)]
    dots = []
    for i in range(26):
        x = 300 + (i * 173) % 480; d = 8.6 + (i * 0.137) % 2.4; sz = 6 + (i * 5) % 9
        dots.append(f'<div style="position:absolute;left:{x}px;top:{F-520 + (i*61)%260}px;width:{sz}px;height:{sz}px;border-radius:50%;background:{GOLD};box-shadow:0 0 14px {GOLD};animation:rise 3.2s ease-out {d:.2f}s both"></div>')
    body = f'''
<div style="position:absolute;left:290px;top:0;width:500px;height:{F}px;background:linear-gradient(rgba(240,180,41,.0),rgba(240,180,41,.22));clip-path:polygon(38% 0,62% 0,100% 100%,0 100%);animation:fin 1.6s ease-out 7.8s both"></div>
<div style="position:absolute;left:0;top:0;width:1080px;height:{F}px;{REFLECT}">
 {rug(552, F, 520, 6.4)}
 <div style="animation:shake .5s linear 5.3s both">{fig(540, F, S, seq)}</div>
 <div style="position:absolute;left:540px;top:{top0}px;width:0;height:0;animation:sink1 .6s {GLIDE} 2.4s forwards,sink2 .6s {GLIDE} 4.2s forwards"><div style="position:absolute;left:0;bottom:0">{"".join(bxs)}</div></div>
 {"".join(dots)}
</div>
<div style="position:absolute;left:0;top:{F}px;width:1080px;height:3px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.55) 15%,rgba(255,255,255,.55) 85%,transparent)"></div>
{cap("Tout ce que tu portes…", 0.1, 3.0, y=1420, size=68)}
{cap("…tu crois devoir le porter seul.", 3.2, 6.2, y=1420, size=64, red=("seul.",))}
{cap("Pose-le. Là où ton front touche le sol.", 6.5, 10.8, y=1420, size=64, gold=("Pose-le.",))}
{hadith(11.5, 16.6, "Allah dit · Sourate Ar-Ra'd",
        "أَلَا بِذِكْرِ اللَّهِ تَطْمَئِنُّ الْقُلُوبُ",
        words("N'est-ce pas par le rappel d'Allah que les cœurs s'apaisent ?", 12.4, .15, gold=("s'apaisent",)),
        "Coran · 13:28", top=150, ar_size=70, fr_size=60)}
<div style="position:absolute;inset:0;background:rgba(0,0,0,.86);animation:fin .5s ease-out 16.7s both"></div>
{endcard(17.0, "Envoie ça à quelqu'un qui porte trop.", gold=("porte", "trop."))}
'''
    css = f"@keyframes sink1{{from{{transform:none}}to{{transform:translateY({50*k}px)}}}}@keyframes sink2{{from{{transform:translateY({50*k}px)}}to{{transform:translateY({100*k}px)}}}}@keyframes rise{{from{{opacity:0;transform:translateY(60px)}}20%{{opacity:1}}to{{opacity:0;transform:translateY(-640px)}}}}"
    return page("Rappel 09 — Le poids", body, css), 20.5

# ───────────────────────── VIDÉO 10 : CENT (22 s) ─────────────────────────
def v10():
    T0, TD = 1.6, 12.0
    waves = []
    for i in range(6):
        y = 1290 + i * 44; op = 0.9 - i * 0.12
        d = "M-200 20 " + " ".join(f"q 50 -{26 - i*2} 100 0 t 100 0" for _ in range(8))
        waves.append(f'<svg viewBox="0 0 1080 40" style="position:absolute;left:0;top:{y}px;width:1080px;height:40px;overflow:visible;opacity:{op:.2f};animation:wave{i%2} {3.2 + i*0.5}s linear 0s infinite"><path d="{d}" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round"/></svg>')
    body = f'''
<div class="mono" style="position:absolute;left:0;right:0;top:130px;text-align:center;font-size:30px;color:#BFAE93;animation:in .4s ease-out .1s both">Dis-le avec moi · 100 fois</div>
<div dir="rtl" style="position:absolute;left:0;right:0;top:170px;text-align:center;font-family:Amiri,serif;font-weight:700;font-size:104px;color:{GOLD};text-shadow:0 0 34px rgba(240,180,41,.5);animation:wrd .6s {LAND} .25s both">سُبْحَانَ اللهِ وَبِحَمْدِهِ</div>
<div style="position:absolute;left:0;right:0;top:372px;text-align:center;font-weight:700;font-size:48px;letter-spacing:-.01em;animation:in .5s ease-out .7s both">SubhânAllâhi wa bihamdih</div>
<div style="position:absolute;left:190px;top:500px;width:700px;height:700px;animation:pulse .5s ease-out {T0+3}s 1 both,pulse .5s ease-out {T0+6}s 1 forwards,pulse .5s ease-out {T0+9}s 1 forwards,pulse .8s ease-out {T0+TD}s 1 forwards">
 <svg viewBox="0 0 700 700" style="position:absolute;inset:0;overflow:visible">
  <defs><mask id="pm"><circle cx="350" cy="350" r="318" fill="none" stroke="#fff" stroke-width="44" pathLength="100" stroke-dasharray="100" stroke-dashoffset="100" transform="rotate(-90 350 350)" style="animation:prog {TD}s steps(100,end) {T0}s both"/></mask></defs>
  <circle cx="350" cy="350" r="318" fill="none" stroke="rgba(255,255,255,.28)" stroke-width="16" stroke-linecap="round" pathLength="100" stroke-dasharray="0.001 0.999" transform="rotate(-90 350 350)"/>
  <g mask="url(#pm)"><circle cx="350" cy="350" r="318" fill="none" stroke="{GOLD}" stroke-width="22" stroke-linecap="round" pathLength="100" stroke-dasharray="0.001 0.999" transform="rotate(-90 350 350)" style="filter:drop-shadow(0 0 10px {GOLD})"/></g>
 </svg>
 <div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center">
  <div class="cnt" style="font-weight:900;font-size:250px;line-height:1;letter-spacing:-.04em;animation:cnt {TD}s linear {T0}s both,numGold .6s ease-out {T0+TD}s forwards"></div>
  <div class="mono" style="margin-top:6px;font-size:30px;color:#BFAE93">sur 100</div>
 </div>
</div>
<div style="position:absolute;inset:0;animation:drain 1.1s cubic-bezier(.5,0,.8,.5) {T0+TD+.15}s forwards">
 <div class="mono" style="position:absolute;left:0;right:0;top:1226px;text-align:center;font-size:27px;color:#fff;animation:in .5s ease-out 1.6s both">Tes péchés · comme l'écume de la mer</div>
 {"".join(waves)}
</div>
<div style="position:absolute;left:70px;right:70px;top:1250px;text-align:center;animation:fout .4s ease-in 20.2s forwards">
 <div style="font-weight:800;font-size:112px;letter-spacing:-.03em;color:{GOLD};text-shadow:0 0 40px rgba(240,180,41,.6);animation:wrd .5s {LAND} {T0+TD+.9}s both">Effacés.</div>
 <div style="margin-top:10px;font-weight:700;font-size:44px;line-height:1.22;letter-spacing:-.015em">{words("« Celui qui le dit cent fois par jour, ses péchés sont effacés, même s'ils sont comme l'écume de la mer. »", T0+TD+1.6, .075)}</div>
 <div class="mono" style="margin-top:22px;font-size:25px;color:#BFAE93;animation:fin .5s ease-out {T0+TD+3.3}s both">Al-Bukhârî 6405 · Muslim 2691</div>
</div>
<div style="position:absolute;inset:0;background:rgba(0,0,0,.88);animation:fin .5s ease-out 20.3s both"></div>
{endcard(20.5, "Tu es allé jusqu'à 100 ? Écris-le.", gold=("100",))}
'''
    css = ("@keyframes prog{from{stroke-dashoffset:100}to{stroke-dashoffset:0}}@keyframes cnt{from{--n:0}to{--n:100}}"
           ".cnt::before{counter-reset:n var(--n);content:counter(n)}"
           f"@keyframes numGold{{from{{color:#fff;text-shadow:none}}to{{color:{GOLD};text-shadow:0 0 50px rgba(240,180,41,.7)}}}}"
           "@keyframes wave0{from{transform:translateX(0)}to{transform:translateX(200px)}}@keyframes wave1{from{transform:translateX(200px)}to{transform:translateX(0)}}"
           "@keyframes drain{from{opacity:1;transform:none}to{opacity:0;transform:translateY(520px)}}")
    return page("Rappel 10 — Cent", body, css), 23.5

if __name__ == "__main__":
    for name, fn in (("Rappel08", v08), ("Rappel09", v09), ("Rappel10", v10)):
        html, dur = fn()
        (ROOT / f"{name}.dc.html").write_text(html)
        print(name, dur)
