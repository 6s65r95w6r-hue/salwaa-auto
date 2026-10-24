# Salwaa — vidéos automatiques (tâche quotidienne)

Tu tournes chaque jour à 7 h (heure de Paris) sans supervision. Ne pose AUCUNE question : décide, produis, publie, consigne.

Salwaa = app iPhone qui bloque TikTok, Instagram, YouTube… à l'heure de chaque prière, jusqu'à ce que l'utilisateur appuie sur « J'ai prié ».

## Routine (3 vidéos par jour)
1. Lire `historique.md` (hadiths déjà utilisés, types récents).
2. Choisir 3 types en alternance (jamais 2 fois le même le même jour) :
   - `serieux` : rappel avec hadith/verset
   - `humour` : liste drôle (types de personnes, excuses…) + vrai rappel
   - `demo` : scène téléphone qui se bloque (scène `phone`)
   - `theme` : thème du jour (vendredi = Jumu'a / Al-Kahf ; sinon Fajr, Isha, patience, dhikr…)
3. Pour chaque vidéo, ajouter une entrée dans l'objet `VIDEOS` de `videos/salwaa-video-lot.jsx`
   avec un id `d2026_10_25_1` (date + n°). Briques disponibles (voir les entrées v02…v10 comme exemples) :
   `big` {kicker?, a, b?, gold?} · `list` {mode:'rank'|'check', title?, items:[{n?,t,s?,hi?,x?}]}
   · `hadith` {kicker, q, src} · `phone` {app, prayer, time, caps:[[sec, titre, sous-titre?]]} · `payoff` {a, g}.
   Toujours : 1re scène = accroche forte (< 8 mots si possible), dernière = `payoff`. 4–5 scènes, 15–22 s.
   `theme: 'dark'` par défaut, `'light'` 1 fois sur 3.
4. Créer `videos/<id>.dc.html` en copiant `videos/modele.dc.html` et en remplaçant :
   - la valeur de `window.OM_SCENES` par la liste des scènes `[{"name":"Hook","dur":3.0},…]` (un nom unique par scène, même ordre que `scenes` dans VIDEOS ; durées : big 2.4–3.2, list 4–8, hadith 4–5.4, phone 8.4, payoff 3.0)
   - `window.VIDEO_ID = 'v02'` par le nouvel id.
5. Rendre : `node outils/render.mjs videos/<id>.dc.html sons/sonN.mp3 sortie/<id>.mp4` (son tiré au hasard parmi `sons/`, sans répéter celui de la vidéo précédente).
   Vérifier que le MP4 existe et dure > 10 s. En cas d'échec : 1 nouvel essai, puis passer et le noter.
6. Mettre en ligne : `node outils/upload.mjs sortie/<id>.mp4` → URL publique permanente.
7. Programmer dans Buffer (connecteur Buffer, org `6a29cb123b7e08878e72eeaf`), `mode: customScheduled`, `schedulingType: automatic`,
   `dueAt` aujourd'hui à 08:00, 12:30 et 20:00 (Europe/Paris, avec le bon décalage horaire), asset `{video:{url}}` :
   - Instagram `6a29cfd08f1d11f9b2729d4c` — `{"instagram":{"type":"reel","shouldShareToFeed":true}}`
   - Facebook `6a4e362f404834462882436c` — `{"facebook":{"type":"reel"}}`
   - TikTok `6a4e2ecf4048344628821d99` — `{"tiktok":{"title":"<accroche courte> | Salwaa"}}`
   Si un créneau est déjà passé au moment où tu tournes, décale-le d'1 h après l'heure actuelle.
8. Ajouter 3 lignes dans `historique.md` (date · créneau · id · type · hadith · son · statut + id des posts Buffer).

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
