# Aya cinématique (Three.js, rendu par le code)
- `reel.html` : scène 3D (arc, tapis, poussière dorée) + textes. Expose `window.renderAt(t)` et `window.__ready`.
- Three.js r170 attendu dans `three/build/three.module.js` :
  `git clone --depth 1 --branch r170 --filter=blob:none --sparse https://github.com/mrdoob/three.js.git three && cd three && git sparse-checkout set --no-cone /build/three.module.js`
- Copier `../pages/media/logo-salwaa.png` à côté, servir le dossier en HTTP (`python3 -m http.server 8765`), puis :
  `node render_at.mjs http://127.0.0.1:8765/reel.html video.mp4 12` (images fixes : `... st/s 12 "1.8,4.2,7.2"`).
- Son : `python3 sound.py` puis mixer comme dans ../README.md.
- Pour un autre verset : changer les 3 mots de `#ar`, `#tr`, `#src` et les instants `ap` dans `renderAt`.
