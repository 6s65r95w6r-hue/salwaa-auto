#!/usr/bin/env python3
import sys, random
DUR = 50.0
GOLD="#F0B429"
css=[]; html=[]
STAND=dict(T="M200 146 L200 202 L200 258", AL="M200 162 L188 212 L184 258", AR="M200 162 L212 212 L216 258",
           LL="M200 258 L192 320 L186 380", LR="M200 258 L208 320 L214 380", H=(200,126))
def pct(t): return round(t/DUR*100,4)
css.append("""
*{margin:0;padding:0;box-sizing:border-box}
body{background:#000}
.root{width:1080px;height:1920px;position:relative;overflow:hidden;background:#120C04;font-family:'Poppins',sans-serif;color:#FCF3E2}
.abs{position:absolute}
@keyframes in{from{opacity:0}to{opacity:1}}
@keyframes out{from{opacity:1}to{opacity:0}}
@keyframes wrd{from{opacity:0;transform:translateY(24px);filter:blur(8px)}to{opacity:1;transform:none;filter:blur(0)}}
@keyframes up{from{opacity:0;transform:translateY(60px)}to{opacity:1;transform:none}}
@keyframes pop{from{transform:scale(.3);opacity:0}60%{transform:scale(1.25);opacity:1}to{transform:scale(1);opacity:1}}
@keyframes pulse{from{opacity:.6}to{opacity:1}}
@keyframes rise{from{transform:translate(0,0);opacity:0}15%{opacity:1}to{transform:translate(var(--dx),-340px);opacity:0}}
.w{display:inline-block;animation:wrd .45s ease-out both}
.hook{font-weight:800;letter-spacing:-.03em;line-height:1.08;text-align:center;width:860px;left:110px}
.mono{font-family:'Roboto Mono',monospace;font-weight:500;text-transform:uppercase;letter-spacing:.22em}
.ar{font-family:'Amiri',serif;direction:rtl;color:#E0A93A;font-size:58px;line-height:1.5;text-align:center;width:860px;left:110px;font-weight:700}
.gold{color:#F0A31A}
svg path,svg circle,svg rect,svg line,svg ellipse{stroke-linecap:round;stroke-linejoin:round}
""")
def word(t,d,cls="",style=""):
    return f'<span class="w {cls}" style="animation-delay:{d}s;{style}">{t}</span> '
def line(words,t0,step=.22,gold=(),style=""):
    return "".join(word(w,round(t0+i*step,2),"gold" if i in gold else "",style) for i,w in enumerate(words.split(" ")))
def scene(sid,t_out,inner,d=.4):
    html.append(f'<div id="{sid}" class="abs" style="left:0;top:0;width:1080px;height:1920px;animation:out {d}s ease-in {t_out}s forwards">{inner}</div>')
BG='position:absolute;left:0;top:0;width:1080px;height:1920px;background-size:cover;'
html.append('<div class="root">')
html.append(f'<div style="{BG}background-image:url(../media/night.jpg)"></div>')
html.append(f'<div style="{BG}background-image:url(../media/dawn.jpg);animation:in 2s ease-in-out 34.4s both"></div>')
html.append(f'<div style="{BG}background:rgba(18,12,4,.55)"></div>')
html.append(f'<div style="{BG}background:rgba(18,12,4,.35);animation:in 1s ease-in-out 43s both"></div>')

# ---- cave + rock + light (svg, full frame) ----
def man(left, i, t0, t1):
    f=lambda b,g,c: f"brightness({b}) drop-shadow(0 0 {g}px {c})"
    W="rgba(255,255,255,.9)"; F="rgba(255,255,255,.15)"; G="rgba(240,163,26,.95)"
    stops=[(0,f(1,9,W)),(t0-.8,f(1,9,W)),(t0,f(1.15,16,G)),(t1-.4,f(1.15,16,G)),(t1+.4,f(.5,3,F)),(34.0,f(.5,3,F)),(35.4,f(1.2,22,G)),(DUR,f(1.2,22,G))]
    if t0<11: stops=[(0,f(1,9,W)),(DUR,f(1,9,W))]
    css.append(f"@keyframes m{i}{{"+"".join(f"{pct(t)}%{{filter:{v}}}" for t,v in stops)+"}")
    paths="".join(f'<path d="{STAND[k]}" fill="none" stroke="#fff" stroke-width="3"/>' for k in ["T","AL","AR","LL","LR"])
    paths+=f'<circle cx="{STAND["H"][0]}" cy="{STAND["H"][1]}" r="20" fill="none" stroke="#fff" stroke-width="3"/>'
    return f'<svg class="abs" viewBox="0 0 400 400" width="420" height="420" style="left:{left}px;top:601px;animation:m{i} {DUR}s linear both">{paths}</svg>'
# rock displacement keyframes
rx=[(0,-640),(1.5,-640),(2.1,0),(13.4,0),(14.4,-70),(21.9,-70),(22.9,-140),(29.9,-140),(30.9,-210),(34.1,-210),(35.6,-620),(DUR,-620)]
css.append("@keyframes rock{"+"".join(f"{pct(t)}%{{transform:translateX({-x}px)}}" for t,x in rx)+"}")
lt=[(0,0),(2.0,.12),(13.4,.12),(14.4,.35),(21.9,.35),(22.9,.55),(29.9,.55),(30.9,.75),(34.1,.75),(35.6,1),(DUR,1)]
css.append("@keyframes lite{"+"".join(f"{pct(t)}%{{opacity:{o}}}" for t,o in lt)+"}")
css.append("@keyframes shake{0%,100%{transform:translateX(0)}25%{transform:translateX(-5px)}75%{transform:translateX(5px)}}")
svg=('<svg class="abs" viewBox="0 0 1080 1920" width="1080" height="1920" style="left:0;top:0">'
 '<defs><radialGradient id="lg" cx="85%" cy="55%" r="60%"><stop offset="0" stop-color="#F5D485" stop-opacity=".9"/><stop offset="1" stop-color="#F5D485" stop-opacity="0"/></radialGradient>'
 '<linearGradient id="cv" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1b130a"/><stop offset="1" stop-color="#0b0703"/></linearGradient></defs>'
 '<path d="M90 1000 L90 700 Q90 330 540 330 Q990 330 990 700 L990 1000 Z" fill="url(#cv)" stroke="#3A2C13" stroke-width="6"/>'
 '<g style="animation:lite @@s linear both"><path d="M780 1000 L1000 1000 L1000 560 L780 700 Z" fill="url(#lg)"/>'
 '<polygon points="800,600 1000,520 1000,1000 700,1000" fill="rgba(245,212,133,.10)"/></g>'
 '<ellipse cx="540" cy="1000" rx="470" ry="26" fill="rgba(240,163,26,.08)"/>'
 '<path d="M90 1000 L990 1000" stroke="#3A2C13" stroke-width="4"/>'
.replace('@@',str(DUR)))
# rock group (shake on impact/moves)
svg+=('<g style="animation:rock @@s linear both"><g>'
 '<circle cx="880" cy="800" r="185" fill="#2b2216" stroke="#7a6743" stroke-width="5"/>'
 '<path d="M770 720 L830 790 L800 860 M930 700 L900 770 L960 830 M850 900 L890 940" fill="none" stroke="#5b4a2e" stroke-width="4"/>'
 '</g></g></svg>').replace('@@',str(DUR))
html.append(svg)
# glow behind men
html.append('<div class="abs" style="left:90px;top:560px;width:900px;height:640px;border-radius:50%;background:radial-gradient(circle,rgba(240,163,26,.16),rgba(240,163,26,0) 65%)"></div>')
html.append(man(40,1,11.0,19.0)); html.append(man(250,2,19.0,26.0)); html.append(man(460,3,26.0,34.0))
# icons inside cave
def icon(inner,t0,t1):
    return (f'<svg class="abs" viewBox="-100 -100 200 200" width="240" height="240" style="left:420px;top:380px;animation:in .6s ease-out {t0}s both,out .5s ease-in {t1}s forwards">{inner}</svg>')
st='fill="none" stroke="#E0A93A" stroke-width="5"'
bowl=f'<path d="M-60 -10 Q0 80 60 -10 Z" {st}/><path d="M-30 -40 Q-20 -60 -30 -80 M0 -40 Q10 -60 0 -80 M30 -40 Q40 -60 30 -80" {st}/>'
lock=f'<rect x="-45" y="-5" width="90" height="70" rx="12" {st}/><path d="M-28 -5 L-28 -35 Q-28 -70 0 -70 Q28 -70 28 -35 L28 -5" {st}/><circle cx="0" cy="30" r="6" {st}/>'
coins=f'<ellipse cx="0" cy="40" rx="55" ry="16" {st}/><ellipse cx="0" cy="12" rx="55" ry="16" {st}/><ellipse cx="0" cy="-16" rx="55" ry="16" {st}/><ellipse cx="0" cy="-44" rx="55" ry="16" {st}/>'
html.append(icon(bowl,12.0,18.4)); html.append(icon(lock,19.8,25.4)); html.append(icon(coins,26.8,33.4))

html.append(f'<div class="abs" style="left:0;top:0;width:1080px;height:1920px;background:rgba(18,12,4,.94);animation:in .6s ease-out 46.4s both"></div>')
LBL='<div class="abs mono" style="top:95px;left:0;width:1080px;text-align:center;font-size:22px;color:#BFAE93;animation:in .5s ease-out .3s both,out .4s ease-in 43s forwards">Hadith &middot; r&eacute;cit authentique</div>'
html.append(LBL)
# ---- S1 hook 0-5 ----
s1=('<div class="abs hook" style="top:1110px;font-size:122px;text-transform:uppercase;color:#FCF3E2;line-height:1">'
    +line("TROIS HOMMES.",0.1,.25,(1,))+'<br>'+line("UNE GROTTE.",0.7,.25)+'</div>'
    '<div class="abs hook" style="top:1480px;font-size:48px;font-weight:600;color:#E7D9BC">'+line("Une pierre bloque la sortie.",2.3,.2,(2,))+'</div>')
scene("s1",4.6,s1)
# ---- S2 5-11 ----
s2=('<div class="abs ar" style="top:150px;animation:in .8s ease-out 5.0s both">انْطَلَقَ ثَلَاثَةُ رَهْطٍ مِمَّنْ كانَ قَبْلَكُمْ</div>'
    '<div class="abs hook" style="top:1130px;font-size:56px;font-weight:700;color:#FCF3E2">'
    +line("Rien ne vous sauvera de cette pierre, sauf d&rsquo;invoquer Allah par vos bonnes actions.",5.2,.19,(11,))+'</div>')
scene("s2",10.7,s2)
def beat(sid,t0,t1,txt,gold,fs=54):
    scene(sid,t1-.3,f'<div class="abs hook" style="top:1130px;font-size:{fs}px;font-weight:700">'+line(txt,t0+.3,.2,gold)+'</div>')
beat("s3",11.0,19.0,"Le premier donnait le lait &agrave; ses parents avant sa famille. Un soir ils dormaient : il a attendu l&rsquo;aube, la coupe &agrave; la main.",(10,),50)
beat("s4",19.0,26.0,"Le deuxi&egrave;me avait l&rsquo;occasion de commettre un grand p&eacute;ch&eacute;. Par crainte d&rsquo;Allah, il s&rsquo;en est &eacute;loign&eacute;.",(14,),52)
beat("s5",26.0,34.0,"Le troisi&egrave;me devait un salaire &agrave; un ouvrier parti sans le prendre. Il l&rsquo;a fait fructifier, puis a tout rendu.",(15,),52)
# ---- S6 reversal 34-38 ----
s6=('<div class="abs hook" style="top:1130px;font-size:80px;font-weight:800">'+line("La pierre s&rsquo;&eacute;carte.",34.4,.25,(2,))+'<br>'+line("Ils sortent.",35.5,.3)+'</div>')
scene("s6",37.7,s6)
# ---- S7 reminder 38-43 ----
s7=('<div class="abs hook" style="top:1080px;font-size:56px;font-weight:700">'+line("Ce que tu fais en secret pour Allah peut devenir ta sortie.",38.2,.2,(7,))+'</div>'
    '<div class="abs hook" style="top:1420px;font-size:40px;font-weight:400;color:#E7D9BC">'+line("Ta pri&egrave;re &agrave; l&rsquo;heure, quand personne ne te voit.",40.9,.18)+'</div>')
scene("s7",43.0,s7)
# ref card 6.5-43
html.append('<div class="abs mono" style="top:1590px;left:110px;width:860px;text-align:center;font-size:17px;letter-spacing:.14em;color:#8C7E62;line-height:1.7;animation:in .6s ease-out 6.5s both,out .4s ease-in 43s forwards">&lsquo;Abdull&acirc;h ibn &lsquo;Umar &middot; Al-Bukh&acirc;r&icirc; 2272 &middot; Muslim 2743<br>Authentique (muttafaq &lsquo;alayh)</div>')
# ---- S8 dedication 43.5-46.5 ----
s8=('<div class="abs mono" style="top:1060px;left:0;width:1080px;text-align:center;font-size:24px;color:#BFAE93;animation:in .4s 43.6s both">Envoie &ccedil;a &agrave; quelqu&rsquo;un</div>'
    '<div class="abs hook" style="top:1140px;font-size:84px">'+line("qui croit que personne ne voit ses efforts.",44.0,.22,(6,))+'</div>')
scene("s8",46.6,s8)
lock_img=('<div style="width:230px;height:230px;border-radius:24%;overflow:hidden;box-shadow:0 0 60px rgba(240,163,26,.35)">'
  '<img src="../media/logo.png" style="width:100%;height:100%;object-fit:cover;transform:scale(1.04)"></div>')
html.append('<div class="abs" style="left:240px;top:520px;width:600px;height:600px;border-radius:50%;background:radial-gradient(circle,rgba(240,163,26,.22),rgba(240,163,26,0) 65%);animation:in .8s ease-out 46.7s both"></div>')
html.append(f'<div class="abs" style="left:425px;top:560px;animation:pop .6s ease-out 46.8s both">{lock_img}</div>')
html.append('<div class="abs" style="left:0;top:830px;width:1080px;text-align:center;font-size:96px;font-weight:800;letter-spacing:-.03em;color:#FCF3E2;animation:up .6s ease-out 47.2s both">Salwaa</div>')
html.append('<div class="abs" style="left:140px;top:970px;width:800px;text-align:center;font-size:36px;font-weight:400;line-height:1.35;color:#E7D9BC;animation:up .6s ease-out 47.6s both">Ton t&eacute;l&eacute;phone se met en pause<br>&agrave; l&rsquo;heure de la pri&egrave;re.</div>')
html.append('<div class="abs mono" style="left:0;top:1150px;width:1080px;text-align:center;font-size:24px;color:#F0A31A;animation:in .5s ease-out 48.2s both">Lien dans la bio</div>')
html.append('</div>')
out=f'<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>Salwaa</title><style>{"".join(css)}</style></head><body>{"".join(html)}</body></html>'
open(sys.argv[1],"w").write(out); print("ok",len(out))
