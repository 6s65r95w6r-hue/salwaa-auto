# Salwaa — vidéos automatiques (3 exécutions par jour, dans le cloud)

Une exécution = UNE vidéo, publiée tout de suite. Créneaux (heure de Paris) : 08:00, 12:30, 18:30. Sans supervision : ne pose AUCUNE question, décide, produis, publie, consigne.

Salwaa = app iPhone qui bloque TikTok, Instagram, YouTube… à l'heure de chaque prière, jusqu'à ce que l'utilisateur appuie sur « J'ai prié ».

## Mise en place de la session (toujours en premier)
- Dépôt : `6s65r95w6r-hue/salwaa-auto` (public). Si le dossier de travail ne le contient pas : `add_repo` (access push) puis `git clone https://github.com/6s65r95w6r-hue/salwaa-auto` (un seul clone, timeout 10 min). `git fetch` + `git pull --rebase` avant de pousser.
- `npm install`. Le Chromium préinstallé correspond à `playwright@1.63.0` ; si le lancement échoue sur « Executable doesn't exist », installe la version indiquée par `npm ls -g playwright`. Le rendu fonctionne hors ligne (React, Babel et polices viennent de `node_modules`).
- Le réseau du sandbox ne joint ni Cloudinary ni les hébergeurs de fichiers : l'hébergement de la vidéo = GitHub (voir étape 6).

## Routine (1 vidéo par exécution)
1. Lire `historique.md` (hadiths déjà utilisés, types récents). Le créneau = celui de l'heure actuelle (08:00 → 1, 12:30 → 2, 18:30 → 3).
2. Choisir le type de la vidéo : jamais le même type que les autres vidéos du jour déjà publiées (voir `historique.md`) :
   - `serieux` : rappel avec hadith/verset
   - `humour` : liste drôle (types de personnes, excuses…) + vrai rappel
   - `demo` : scène téléphone qui se bloque (scène `phone`)
   - `theme` : thème du jour (vendredi = Jumu'a / Al-Kahf ; sinon Fajr, Isha, patience, dhikr…)
3. Ajouter une entrée dans l'objet `VIDEOS` de `videos/salwaa-video-lot.jsx`
   avec un id `d2026_10_25_1` (date + n° du créneau). Briques disponibles (voir les entrées v02…v10 comme exemples) :
   `big` {kicker?, a, b?, gold?} · `list` {mode:'rank'|'check', title?, items:[{n?,t,s?,hi?,x?}]}
   · `hadith` {kicker, q, src} · `phone` {app, prayer, time, caps:[[sec, titre, sous-titre?]]} · `payoff` {a, g}.
   Toujours : 1re scène = accroche forte (< 8 mots si possible), dernière = `payoff`. 4–5 scènes, 15–22 s.
   `theme: 'dark'` par défaut, `'light'` 1 fois sur 3.
4. Créer `videos/<id>.dc.html` en copiant `videos/modele.dc.html` et en remplaçant :
   - la valeur de `window.OM_SCENES` par la liste des scènes `[{"name":"Hook","dur":3.0},…]` (un nom unique par scène, même ordre que `scenes` dans VIDEOS ; durées : big 2.4–3.2, list 4–8, hadith 4–5.4, phone 8.4, payoff 3.0)
   - `window.VIDEO_ID = 'v02'` par le nouvel id.
5. Rendre : `node outils/render.mjs videos/<id>.dc.html sons/sonN.mp3 publie/<id>.mp4` (son au hasard parmi `sons/`, différent de celui de la vidéo précédente dans `historique.md`).
   Vérifier avec ffprobe que le MP4 existe et dure > 10 s. En cas d'échec : 1 nouvel essai, puis arrêter, le noter dans `historique.md` et le dire dans la réponse finale.
6. Mettre en ligne via GitHub : `git add publie/<id>.mp4 videos/ historique.md`, commit, `git push`. URL publique : `https://raw.githubusercontent.com/6s65r95w6r-hue/salwaa-auto/main/publie/<id>.mp4` (vérifiée : Buffer lit ce lien). Contrôle `curl -sI` = HTTP 200 avant de publier.
7. Publier dans Buffer (connecteur Buffer, org `6a29cb123b7e08878e72eeaf`), `mode: shareNow`, `schedulingType: automatic`, asset `{video:{url}}`, un post par canal (une seule fois chacun, jamais de doublon : en cas de timeout, vérifier avec list_posts avant de retenter) :
   - Instagram `6a29cfd08f1d11f9b2729d4c` — `{"instagram":{"type":"reel","shouldShareToFeed":true}}`
   - Facebook `6a4e362f404834462882436c` — `{"facebook":{"type":"reel"}}`
   - TikTok `6a4e2ecf4048344628821d99` — `{"tiktok":{"title":"<accroche courte> | Salwaa"}}`
8. Ajouter 1 ligne dans `historique.md` (date · créneau · id · type · hadith · son · statut + id des posts Buffer), puis commit et push. Réponse finale : id, type, hadith, statut des 3 posts, tout problème.

## Légendes
Instagram / Facebook :
```
<accroche + emoji>

« <hadith> »
Le Prophète صلى الله عليه وسلم — <source>

<1 phrase concrète>
Salwaa bloque tes apps le temps de prier. Lien dans la bio.

#Islam #Rappel #Hadith #Priere #Salah #salwaaapp #rappelislamique #islamfrance #Muslim #Deen
```
Facebook : 7 hashtags max. TikTok : hadith + source + `#islamtiktok #musulman #Priere #Rappel #Salwaa`.
Toujours finir par une question qui pousse à commenter (« Tu es lequel ? 👇 »).

## Règles de contenu (non négociables)
- Français, ton bienveillant ; l'humour vise nos habitudes, jamais la religion, jamais une personne.
- Hadiths : uniquement sahih/hasan connus, avec numéro de référence ; reformulation fidèle, jamais inventée. Pas de hadith utilisé dans les 30 derniers jours.
- Aucun visage, aucune image de prophète ou de compagnon. Pas de musique avec instruments si les sons fournis n'en ont pas.
- Chiffres présentés comme exemples, jamais comme statistiques officielles.
