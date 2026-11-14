# perso/ — outils de la 3e vidéo quotidienne (tâche « Salwaa — vidéo quotidienne Buffer »)

Ce dossier est indépendant de l'automatisation principale (CLAUDE.md, outils/, videos/). Ne touche pas à ses fichiers.

## Ce qu'il contient
- `scripts/render.py` : filme une page HTML animée (1080×1920, 30 images/s) avec Playwright.
  `python3 scripts/render.py <chemin absolu>/pages/X.dc.html <chemin absolu>/sortie.mp4 video <durée>`
  ou des images fixes : `... <préfixe> "0.5,3,8" <durée>`. Les chemins doivent être absolus.
- `scripts/build_neon.py` : bibliothèque + 3 exemples de rappels « néon » (fond noir, bonhomme en traits blancs, accent or).
  Briques : `fig()` (bonhomme et poses STAND, REACH, CARRY, CROUCH, LOW, RUKU, SUJUD, KNEEL, DESPAIR), `words()`, `cap()`, `rug()`, `box()`, `hadith()`, `endcard()`, `page()`.
- `scripts/build_conv.py` : 3 exemples de vidéos courtes « téléchargement » (13 s) : démo, défi 7 jours, sans/avec.
  Briques : `top()`, `cta()` (logo + barre de recherche « Salwaa »), `pause_icon()`, vraie capture de l'app.
- `scripts/sound_neon.py`, `scripts/sound_conv.py` : son généré en code (numpy/scipy), sans instruments, sans voix, sans souffle aigu.
  Briques : `put(t, son, gain)`, `thud`, `pop`, `whoosh`, `ping`, `key`, `stamp`, `step`, `swell`, `click`.
- `pages/media/` : `logo-salwaa.png` (480 px, à afficher à 320 px au maximum) et `ui-isha.jpg` (vraie capture de l'accueil de l'app, 780×3320).

## Faire une nouvelle vidéo
1. Polices : `git clone --depth 1 --filter=blob:none --sparse https://github.com/google/fonts.git /tmp/gf && cd /tmp/gf && git sparse-checkout set ofl/amiri ofl/poppins ofl/robotomono`, copier les .ttf dans `~/.fonts`, puis `fc-cache -f`.
2. Écrire `scripts/build_jour.py` qui importe `build_neon` (et `build_conv` si besoin), définit UNE fonction vidéo sur le modèle de `v08()`…`v13()` et écrit `pages/Jour.dc.html`.
3. Regarder 6 images fixes avant le rendu complet, corriger les chevauchements et tout texte de moins de 44 px.
4. Écrire le son sur le modèle de `sound_conv.py` (mêmes instants que l'animation), puis mixer :
   `ffmpeg -i video.mp4 -i sfx.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -af "lowpass=f=9000,loudnorm=I=-14:TP=-1:LRA=11" -shortest -movflags +faststart sortie.mp4`

## Leçons tirées des chiffres Buffer (novembre 2026)
- Temps de visionnage moyen : 2,4 à 6 s. Donc 10 à 15 s au maximum, et Salwaa (nom, logo ou vraie capture) visible avant la 3e seconde.
- Finir par la barre de recherche « Salwaa » (`cta()`), pas seulement « lien dans la bio ».
- Ce qui perce : un sujet lié au moment (vendredi, Fajr en hiver, Ramadan, examens…) et un seul message.
- Ne jamais inventer un écran de l'app, un avis, une note ou un chiffre. Ne jamais écrire « app iPhone » ni citer un store.
- Personnages sans visage, tapis quand il prie, pas de musique avec instruments.
