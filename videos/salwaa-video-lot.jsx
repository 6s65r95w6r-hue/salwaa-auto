const { useComposition, Easing, animate, CompositionStage, useTweaks, TweaksPanel, TweakSection, TweakToggle } = window;
const POP = "'Poppins', system-ui, sans-serif", MONO = "'Roboto Mono', monospace";
const W = 1080, H = 1920;
const THEMES = {
  dark: { bg: '#120C04', ink: '#FCF3E2', gold: '#E0A93A', muted: '#9C8B70', soft: '#2A2112', onGold: '#120C04', glow: 'rgba(224,169,58,0.2)' },
  light: { bg: '#FAF5EB', ink: '#1B1508', gold: '#B07A12', muted: '#7A6A4E', soft: '#E9DCC0', onGold: '#FAF5EB', glow: 'rgba(176,122,18,0.12)' },
};
const ease = (T, s, d, e = Easing.easeOutCubic) => animate({ from: 0, to: 1, start: s, end: s + d, ease: e })(T);
const fade = (T, s, e, d = 0.35) => ease(T, s, d) * (1 - ease(T, e - 0.3, 0.3));

const VIDEOS = {
  v02: { theme: 'dark', scenes: [
    { type: 'big', a: 'Les 4 types de personnes quand l’adhan retentit', b: 'Tu es lequel ?' },
    { type: 'list', mode: 'rank', items: [
      { n: '01', t: 'Le négociateur', s: '« Encore 5 minutes… » depuis 2 heures.' },
      { n: '02', t: 'Le DJ', s: 'Il baisse le son de sa vidéo. Par respect.' },
      { n: '03', t: 'Le fantôme', s: 'Il a entendu. Il fait comme si de rien n’était.' },
      { n: '04', t: 'Le vrai', s: 'Il pose tout et va prier.', hi: true }] },
    { type: 'hadith', kicker: 'L’ŒUVRE LA PLUS AIMÉE D’ALLAH ?', q: '« La prière à son heure. »', src: 'AL-BOUKHÂRÎ N° 527 · MUSLIM N° 85' },
    { type: 'big', a: 'Sois le n°4.', b: 'Même en plein milieu d’une vidéo.', gold: true },
    { type: 'payoff', a: 'Salwaa t’aide à être', g: 'le n°4.' }] },
  v03: { theme: 'light', scenes: [
    { type: 'big', a: 'Imagine une rivière devant ta porte.', b: 'Tu t’y laves 5 fois par jour.' },
    { type: 'big', a: 'Resterait-il la moindre saleté sur toi ?' },
    { type: 'hadith', kicker: 'LE PROPHÈTE ﷺ A DIT', q: '« C’est l’exemple des cinq prières : par elles, Allah efface les péchés. »', src: 'AL-BOUKHÂRÎ N° 528 · MUSLIM N° 667' },
    { type: 'list', mode: 'check', title: 'Ta rivière aujourd’hui', items: [{ t: 'Fajr' }, { t: 'Dhuhr' }, { t: 'Asr' }, { t: 'Maghrib' }, { t: 'Isha' }] },
    { type: 'payoff', a: '5 fois par jour.', g: 'Ne la laisse pas passer.' }] },
  v04: { theme: 'dark', scenes: [
    { type: 'big', a: 'Le réveil de Fajr que personne n’attendait.' },
    { type: 'phone', app: 'Instagram', prayer: 'Fajr', time: '06:12', caps: [
      [0, '06 h 11. Tu scrolles au lit.', 'Les yeux à moitié fermés.'], [1.4, '06 h 12. L’adhan.', 'Salwaa bloque Instagram.'],
      [3.4, 'Tu essaies de rouvrir.', 'Bloqué. Bloqué. Bloqué.'], [5.6, 'Wudu. Tapis. Deux rak‘a.', 'Débloqué.']] },
    { type: 'hadith', kicker: 'LE PROPHÈTE ﷺ A DIT', q: '« Celui qui prie Fajr est sous la protection d’Allah. »', src: 'MUSLIM N° 657' },
    { type: 'payoff', a: 'Commence ta journée', g: 'sous Sa protection.' }] },
  v05: { theme: 'dark', scenes: [
    { type: 'big', kicker: 'VENDREDI', a: 'Une lumière pour toute ta semaine.' },
    { type: 'big', a: 'Sourate Al-Kahf.', b: 'À lire chaque vendredi.', gold: true },
    { type: 'hadith', kicker: 'LE PROPHÈTE ﷺ A DIT', q: '« Celui qui lit la sourate Al-Kahf le vendredi, une lumière l’éclairera entre les deux vendredis. »', src: 'AL-HÂKIM · SAHÎH AL-JÂMI‘ N° 6470' },
    { type: 'list', mode: 'check', title: 'Ce vendredi', items: [{ t: 'Al-Kahf' }, { t: 'Salawat sur le Prophète ﷺ' }, { t: 'Jumu‘a en avance' }, { t: 'Douaa avant Maghrib' }] },
    { type: 'payoff', a: 'Jumu‘a Moubaraka.', g: 'Pose le téléphone, ouvre le Coran.' }] },
  v06: { theme: 'dark', scenes: [
    { type: 'big', a: 'Top 3 des excuses pour repousser la prière', b: 'Le n°1 va te piquer.' },
    { type: 'list', mode: 'rank', items: [
      { n: '03', t: '« La flemme du wudu. »', s: 'Mais pas la flemme d’aller au frigo 6 fois.' },
      { n: '02', t: '« Je la rattrape avec la suivante. »', s: 'Et la suivante avec la suivante…' },
      { n: '01', t: '« Encore une vidéo. »', s: 'Il y aura toujours une autre vidéo.', hi: true }] },
    { type: 'hadith', kicker: 'ALLAH DIT', q: '« La prière demeure, pour les croyants, une prescription à des temps déterminés. »', src: 'SOURATE AN-NISÂ’ · 4:103' },
    { type: 'payoff', a: 'Plus d’excuse.', g: 'Salwaa bloque tes apps le temps de prier.' }] },
  v07: { theme: 'light', scenes: [
    { type: 'big', a: 'Une maison au Paradis.', b: 'Pour 12 rak‘a par jour.' },
    { type: 'list', mode: 'check', title: 'Les sunna régulières', items: [{ t: '2 avant Fajr' }, { t: '4 avant Dhuhr' }, { t: '2 après Dhuhr' }, { t: '2 après Maghrib' }, { t: '2 après Isha' }] },
    { type: 'hadith', kicker: 'LE PROPHÈTE ﷺ A DIT', q: '« Celui qui prie douze rak‘a par jour, une maison lui sera bâtie au Paradis. »', src: 'MUSLIM N° 728 · AT-TIRMIDHÎ N° 415' },
    { type: 'big', a: 'Quelques minutes par jour.', b: 'Pour l’éternité.', gold: true },
    { type: 'payoff', a: 'Commence aujourd’hui.', g: 'Rak‘a par rak‘a.' }] },
  v08: { theme: 'dark', scenes: [
    { type: 'big', a: 'Ce que fait Salwaa, en 10 secondes.' },
    { type: 'phone', app: 'TikTok', prayer: 'Maghrib', time: '19:02', caps: [
      [0, '1. Elle connaît l’heure de chaque prière.'], [1.4, '2. À l’adhan, tes apps se bloquent.'],
      [3.4, '3. Impossible de tricher.'], [5.6, '4. Tu pries, tu débloques.']] },
    { type: 'hadith', kicker: 'LE PROPHÈTE ﷺ A DIT', q: '« La prière est une lumière. »', src: 'MUSLIM N° 223' },
    { type: 'payoff', a: 'Ton téléphone travaille enfin', g: 'pour ton akhira.' }] },
  v09: { theme: 'dark', scenes: [
    { type: 'big', kicker: 'CE SOIR', a: 'Prier la moitié de la nuit… sans te réveiller ?' },
    { type: 'hadith', kicker: 'LE PROPHÈTE ﷺ A DIT', q: '« Celui qui prie Isha en groupe, c’est comme s’il avait prié la moitié de la nuit. »', src: 'MUSLIM N° 656' },
    { type: 'big', a: 'Et s’il prie aussi Fajr en groupe…', b: 'c’est comme s’il avait prié la nuit entière.' },
    { type: 'payoff', a: 'Ce soir, Isha.', g: 'Demain, Fajr.' }] },
  v10: { theme: 'dark', scenes: [
    { type: 'big', a: 'Ton téléphone vibre.', b: 'Tu réponds en 2 secondes.' },
    { type: 'list', mode: 'check', title: 'Aujourd’hui', items: [
      { t: 'Snap de ton pote', s: 'répondu' }, { t: 'Like sur ta story', s: 'vu' }, { t: 'Message du groupe', s: 'lu' },
      { t: 'L’adhan', s: '« encore 5 min »', x: true }] },
    { type: 'big', a: 'Allah t’appelle 5 fois par jour.', b: 'Le seul appel qui compte vraiment.', gold: true },
    { type: 'hadith', kicker: 'LE PROPHÈTE ﷺ A DIT', q: '« Ô Bilal, appelle à la prière, qu’elle nous apporte le repos. »', src: 'ABÛ DÂWÛD N° 4985' },
    { type: 'payoff', a: 'Réponds au bon appel.', g: 'Salwaa s’occupe des autres.' }] },
  d2026_10_25_2: { theme: 'dark', scenes: [
    { type: 'big', a: 'Tu pars juste après le salam ?' },
    { type: 'big', a: '33 · 33 · 34', b: 'Trois minutes qui effacent beaucoup.', gold: true },
    { type: 'hadith', kicker: 'LE PROPHÈTE ﷺ A DIT', q: '« Celui qui dit après chaque prière 33 fois Subhan Allah, 33 fois Alhamdulillah, 33 fois Allahou akbar, ses péchés sont pardonnés, fussent-ils comme l’écume de la mer. »', src: 'MUSLIM N° 597' },
    { type: 'list', mode: 'check', title: 'Après le salam', items: [{ t: 'Subhan Allah', s: '33 fois' }, { t: 'Alhamdulillah', s: '33 fois' }, { t: 'Allahou akbar', s: '34 fois' }] },
    { type: 'payoff', a: 'Reste encore un instant.', g: 'Salwaa garde ton écran fermé.' }] },
  d2026_10_25_1: { theme: 'dark', scenes: [
    { type: 'big', a: 'Tu es quel réveil à Fajr ?' },
    { type: 'list', mode: 'rank', items: [
      { n: '01', t: 'Le snooze', s: '7 alarmes, 7 « encore 5 min ».' },
      { n: '02', t: 'Le négociateur', s: '« Je prie à 7 h, ça compte presque. »' },
      { n: '03', t: 'Le lève-tôt', s: 'Debout, wudu, deux rak‘a. Le sourire en plus.', hi: true }] },
    { type: 'hadith', kicker: 'LE PROPHÈTE ﷺ A DIT', q: '« Les deux rak‘a du Fajr valent mieux que le bas monde et tout ce qu’il contient. »', src: 'MUSLIM N° 725' },
    { type: 'big', a: 'Deux rak‘a.', b: 'Plus précieuses que tout ce qui brille.', gold: true },
    { type: 'payoff', a: 'Demain, sois le n°3.', g: 'Salwaa s’occupe du réveil.' }] },
  d2026_10_24_3: { theme: 'dark', scenes: [
    { type: 'big', a: 'Deux prières.', b: 'Une promesse du Paradis.' },
    { type: 'hadith', kicker: 'LE PROPHÈTE ﷺ A DIT', q: '« Celui qui accomplit les deux prières fraîches entrera au Paradis. »', src: 'AL-BOUKHÂRÎ N° 574 · MUSLIM N° 635' },
    { type: 'list', mode: 'check', title: 'Les deux fraîches', items: [{ t: 'Fajr', s: 'avant le lever du soleil' }, { t: 'Asr', s: 'avant que la journée file' }] },
    { type: 'big', a: 'Asr, c’est maintenant.', b: 'Pose le téléphone.', gold: true },
    { type: 'payoff', a: 'Ne rate pas Asr.', g: 'Salwaa s’occupe du reste.' }] },
  d2026_10_24_t: { theme: 'dark', scenes: [
    { type: 'big', a: 'Prier par habitude ou par intention ?' },
    { type: 'big', a: 'Même prière.', b: 'Pas la même valeur.', gold: true },
    { type: 'hadith', kicker: 'LE PROPHÈTE ﷺ A DIT', q: '« Les actes ne valent que par les intentions. »', src: 'AL-BOUKHÂRÎ N° 1 · MUSLIM N° 1907' },
    { type: 'list', mode: 'check', title: 'Avant ta prochaine prière', items: [{ t: 'Pose le téléphone' }, { t: 'Respire' }, { t: 'Renouvelle ton intention' }] },
    { type: 'payoff', a: 'Prie pour Allah.', g: 'Salwaa s’occupe du reste.' }] },
};

function Big({ T, s, e, c, k }) {
  const op = fade(T, s, e), a = ease(T, s, 0.5), b = ease(T, s + 0.8, 0.45);
  if (op <= 0.001) return null;
  return (
    <div style={{ position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', justifyContent: 'center', padding: '0 100px', opacity: op }}>
      {c.kicker ? <div style={{ fontFamily: MONO, fontWeight: 500, fontSize: 32, letterSpacing: '0.26em', color: k.gold, marginBottom: 30 }}>{c.kicker}</div> : null}
      <div style={{ fontFamily: POP, fontWeight: 800, fontSize: c.a.length > 40 ? 96 : 112, lineHeight: 1.04, letterSpacing: '-0.035em', color: c.gold ? k.gold : k.ink, opacity: a, transform: `translateY(${(1 - a) * 30}px)`, textWrap: 'balance' }}>{c.a}</div>
      {c.b ? <div style={{ marginTop: 36, fontFamily: POP, fontWeight: 600, fontSize: 56, lineHeight: 1.2, color: c.gold ? k.ink : k.gold, opacity: b, textWrap: 'balance' }}>{c.b}</div> : null}
    </div>
  );
}

function List({ T, s, e, c, k }) {
  const op = fade(T, s, e);
  if (op <= 0.001) return null;
  const n = c.items.length, step = Math.min(1.6, (e - s - 1.2) / n);
  const rank = c.mode === 'rank';
  return (
    <div style={{ position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', justifyContent: 'center', padding: '0 100px', gap: rank ? 56 : 36, opacity: op }}>
      {c.title ? <div style={{ fontFamily: POP, fontWeight: 800, fontSize: 84, lineHeight: 1.04, letterSpacing: '-0.03em', color: k.ink, marginBottom: 20 }}>{c.title}</div> : null}
      {c.items.map((it, i) => {
        const at = s + 0.3 + i * step, a = ease(T, at, 0.4), sub = ease(T, at + 0.45, 0.4);
        const past = rank ? ease(T, at + step - 0.1, 0.3) * (i < n - 1 ? 1 : 0) : 0;
        return (
          <div key={i} style={{ display: 'flex', gap: 30, alignItems: rank ? 'flex-start' : 'center', opacity: a * (1 - past * 0.55), transform: `translateX(${(1 - a) * -40}px)` }}>
            {rank
              ? <div style={{ flex: 'none', width: 110, fontFamily: POP, fontWeight: 900, fontSize: 80, lineHeight: 1, color: it.hi ? k.gold : 'transparent', WebkitTextStroke: it.hi ? '0' : `3px ${k.gold}` }}>{it.n}</div>
              : <div style={{ flex: 'none', width: 66, height: 66, borderRadius: 33, background: it.x ? '#C8473D' : k.gold, color: k.onGold, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: POP, fontWeight: 800, fontSize: 34, transform: `scale(${a})` }}>{it.x ? '✕' : '✓'}</div>}
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              <div style={{ fontFamily: POP, fontWeight: 700, fontSize: rank ? 70 : 60, lineHeight: 1.1, letterSpacing: '-0.02em', color: it.hi || it.x ? k.gold : k.ink }}>{it.t}</div>
              {it.s ? <div style={{ fontFamily: POP, fontWeight: 500, fontSize: rank ? 44 : 40, lineHeight: 1.25, color: k.muted, opacity: sub }}>{it.s}</div> : null}
            </div>
          </div>
        );
      })}
    </div>
  );
}

function Hadith({ T, s, e, c, k }) {
  const op = fade(T, s, e), a = ease(T, s + 0.1, 0.6), b = ease(T, s + 1.5, 0.5);
  if (op <= 0.001) return null;
  return (
    <div style={{ position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', justifyContent: 'center', padding: '0 100px', opacity: op }}>
      <div style={{ fontFamily: MONO, fontWeight: 500, fontSize: 30, letterSpacing: '0.24em', color: k.gold, opacity: a }}>{c.kicker}</div>
      <div style={{ marginTop: 40, fontFamily: POP, fontWeight: 700, fontSize: c.q.length > 70 ? 70 : 92, lineHeight: 1.18, letterSpacing: '-0.02em', color: k.ink, opacity: a, transform: `translateY(${(1 - a) * 30}px)`, textWrap: 'pretty' }}>{c.q}</div>
      <div style={{ marginTop: 50, fontFamily: MONO, fontSize: 30, letterSpacing: '0.12em', color: k.muted, opacity: b }}>{c.src}</div>
    </div>
  );
}

const FEED = ['#3A2A55', '#5A2E2E', '#24414A', '#4A3A1E', '#2E4A2E'];
function Phone({ T, s, e, c, k }) {
  const op = fade(T, s, e, 0.5);
  if (op <= 0.001) return null;
  const t = T - s, gold = '#E0A93A', ink = '#120C04', cream = '#FCF3E2';
  const sc = Math.max(0, Math.min(t, 1.4)) * 2.2, fi = Math.floor(sc) % FEED.length, snap = Easing.easeInOutCubic(Math.min(1, (sc % 1) * 2.5));
  const notif = fade(T, s + 1.2, s + 2.6), blk = ease(T, s + 2.4, 0.35), l = ease(T, s + 2.5, 0.6, Easing.easeOutBack);
  const shake = [3.6, 4.2, 4.8].some((x) => t > x && t < x + 0.3) ? Math.sin(T * 90) * 18 : 0;
  const pr = e - s - 2.2, press = ease(T, s + pr, 0.25), done = ease(T, s + pr + 0.35, 0.4) > 0.5;
  const cap = [...c.caps].reverse().find(([at]) => t >= at);
  const capIdx = c.caps.indexOf(cap), capA = cap ? ease(T, s + cap[0], 0.35) : 0;
  const capOut = capIdx < c.caps.length - 1 ? 1 - ease(T, s + c.caps[capIdx + 1][0] - 0.25, 0.25) : 1;
  return (
    <div style={{ position: 'absolute', inset: 0, opacity: op }}>
      {cap ? <div style={{ position: 'absolute', left: 60, right: 60, top: 110, textAlign: 'center', opacity: capA * capOut, transform: `translateY(${(1 - capA) * 20}px)` }}>
        <div style={{ fontFamily: POP, fontWeight: 800, fontSize: 64, lineHeight: 1.08, letterSpacing: '-0.03em', color: k.ink, textWrap: 'balance' }}>{cap[1]}</div>
        {cap[2] ? <div style={{ marginTop: 12, fontFamily: POP, fontWeight: 700, fontSize: 44, color: k.gold }}>{cap[2]}</div> : null}
      </div> : null}
      <div style={{ position: 'absolute', left: 180, top: 470, width: 720, height: 1340, borderRadius: 92, background: '#0A0703', padding: 18, boxSizing: 'border-box', boxShadow: '0 40px 120px rgba(0,0,0,0.6), 0 0 0 3px #3A2E18' }}>
        <div style={{ position: 'relative', width: '100%', height: '100%', borderRadius: 76, overflow: 'hidden', background: '#000' }}>
          {[0, 1].map((j) => <div key={j} style={{ position: 'absolute', inset: 0, transform: `translateY(${(j - snap) * 100}%)`, background: `linear-gradient(160deg, ${FEED[(fi + j) % FEED.length]}, #0A0703)` }}>
            <div style={{ position: 'absolute', left: 32, right: 130, bottom: 90, display: 'flex', flexDirection: 'column', gap: 12 }}>
              <div style={{ width: 220, height: 22, borderRadius: 11, background: 'rgba(255,255,255,0.55)' }}></div>
              <div style={{ width: '90%', height: 18, borderRadius: 9, background: 'rgba(255,255,255,0.3)' }}></div>
            </div>
          </div>)}
          <div style={{ position: 'absolute', left: 22, right: 22, top: 80, zIndex: 5, opacity: notif, transform: `translateY(${(1 - ease(T, s + 1.2, 0.45, Easing.easeOutBack)) * -160}px)` }}>
            <div style={{ background: 'rgba(252,243,226,0.96)', borderRadius: 34, padding: '24px 26px', display: 'flex', gap: 20, alignItems: 'center' }}>
              <img src="assets/logo.png" style={{ width: 76, height: 76, borderRadius: 18, flex: 'none' }} />
              <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
                <div style={{ fontFamily: POP, fontWeight: 700, fontSize: 30, color: ink }}>Salwaa · maintenant</div>
                <div style={{ fontFamily: POP, fontWeight: 500, fontSize: 28, color: '#4A3D26' }}>C’est l’heure de {c.prayer}. Tes apps se bloquent.</div>
              </div>
            </div>
          </div>
          <div style={{ position: 'absolute', inset: 0, zIndex: 6, background: ink, opacity: blk, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '0 60px', textAlign: 'center', gap: 30 }}>
            <div style={{ width: 180, height: 180, borderRadius: 90, background: done ? gold : 'rgba(224,169,58,0.14)', display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `scale(${l}) translateX(${shake}px)` }}>
              {done ? <span style={{ fontFamily: POP, fontWeight: 800, fontSize: 90, color: ink }}>✓</span>
                : <svg width="84" height="84" viewBox="0 0 24 24" fill="none" stroke={gold} strokeWidth="2" strokeLinecap="round"><rect x="5" y="11" width="14" height="10" rx="2"></rect><path d="M8 11V7a4 4 0 0 1 8 0v4"></path></svg>}
            </div>
            <div style={{ fontFamily: POP, fontWeight: 800, fontSize: 60, lineHeight: 1.05, color: cream }}>{done ? 'Qu’Allah accepte.' : `${c.app} est bloqué`}</div>
            <div style={{ fontFamily: POP, fontWeight: 500, fontSize: 34, color: '#9C8B70' }}>{done ? 'Tes apps sont débloquées.' : `${c.prayer} · ${c.time}`}</div>
            <div style={{ marginTop: 30, background: gold, color: ink, fontFamily: POP, fontWeight: 700, fontSize: 38, padding: '24px 64px', borderRadius: 999, opacity: done ? 0 : 1, transform: `scale(${1 - press * 0.08})` }}>J’ai prié</div>
          </div>
          <div style={{ position: 'absolute', top: 22, left: '50%', marginLeft: -80, width: 160, height: 44, borderRadius: 22, background: '#000', zIndex: 9 }}></div>
        </div>
      </div>
    </div>
  );
}

function Payoff({ T, s, c, k }) {
  const a = ease(T, s, 0.5), l = ease(T, s + 0.6, 0.6, Easing.easeOutBack), d = ease(T, s + 1.2, 0.5);
  if (a <= 0) return null;
  return (
    <div style={{ position: 'absolute', inset: 0, background: `radial-gradient(70% 45% at 50% 50%, ${k.glow}, rgba(0,0,0,0) 70%), ${k.bg}`, opacity: a, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '0 80px', textAlign: 'center' }}>
      <div style={{ fontFamily: POP, fontWeight: 800, fontSize: 84, lineHeight: 1.06, letterSpacing: '-0.03em', color: k.ink, textWrap: 'balance' }}>{c.a} <span style={{ color: k.gold }}>{c.g}</span></div>
      <div style={{ marginTop: 90, display: 'flex', alignItems: 'center', gap: 28, transform: `scale(${l})` }}>
        <img src="assets/logo.png" style={{ width: 140, height: 140, borderRadius: 34, boxShadow: `0 0 90px ${k.glow}` }} />
        <span style={{ fontFamily: POP, fontWeight: 800, fontSize: 84, color: k.ink }}>Salwaa</span>
      </div>
      <div style={{ marginTop: 50, fontFamily: MONO, fontWeight: 500, fontSize: 34, letterSpacing: '0.2em', color: k.gold, opacity: d }}>LIEN DANS LA BIO</div>
    </div>
  );
}

const PARTS = { big: Big, list: List, hadith: Hadith, phone: Phone, payoff: Payoff };

function Piece({ id }) {
  const { T, CUES: C } = useComposition();
  const v = VIDEOS[id], k = THEMES[v.theme];
  const names = JSON.parse(window.OM_SCENES).map((x) => x.name);
  return (
    <div data-screen-label={`t=${Math.floor(T)}s`} style={{ position: 'absolute', inset: 0, overflow: 'hidden', background: k.bg }}>
      {v.scenes.map((c, i) => {
        const P = PARTS[c.type], s = C[names[i]], e = i < names.length - 1 ? C[names[i + 1]] : 9999;
        return <P key={i} T={T} s={s} e={e} c={c} k={k} />;
      })}
    </div>
  );
}

function SalwaaLot() {
  const [t, setTweak] = useTweaks(window.TWEAK_DEFAULTS || { motionEditor: true });
  const k = THEMES[VIDEOS[window.VIDEO_ID].theme];
  return (
    <>
      <CompositionStage width={W} height={H} scenes={window.OM_SCENES} playback={window.OM_PLAYBACK} bg={k.bg}>
        <Piece id={window.VIDEO_ID} />
      </CompositionStage>
      <TweaksPanel>
        <TweakSection label="Vidéo" />
        <TweakToggle label="Motion editor" value={t.motionEditor} onChange={(v) => setTweak('motionEditor', v)} />
      </TweaksPanel>
    </>
  );
}
window.SalwaaLot = SalwaaLot;
