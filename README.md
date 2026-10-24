# Salwaa — vidéos 100 % automatiques

Chaque jour à 7 h, Claude (Cowork ou Claude Code) crée 3 vidéos, les exporte en MP4 avec un son, les met en ligne et les programme dans Buffer à 8 h, 12 h 30 et 20 h sur Instagram, Facebook et TikTok.

## Installation (une seule fois, ~20 min)
1. **Dossier** : décompresse ce dossier, par ex. dans `Documents/salwaa-auto`.
2. **Node.js** : installe la version LTS depuis nodejs.org.
3. **ffmpeg** : sur Mac, dans le Terminal : `brew install ffmpeg` (ou télécharge-le sur ffmpeg.org).
4. Dans le Terminal, dans le dossier :
   ```
   npm install
   npx playwright install chromium
   ```
5. **Hébergement vidéo (Cloudinary, gratuit)** : crée un compte sur cloudinary.com →
   Settings → Upload → *Add upload preset* → Signing mode **Unsigned** → enregistre.
   Crée un fichier `.env` dans le dossier :
   ```
   CLOUDINARY_CLOUD=ton_cloud_name
   CLOUDINARY_PRESET=nom_du_preset
   ```
6. **Buffer** : dans Cowork / Claude, connecte le connecteur Buffer (le même compte qu'ici).
7. **Test** : ouvre le dossier dans Cowork et écris :
   « Lis CLAUDE.md et fais la routine pour 1 seule vidéo, en brouillon Buffer (saveToDraft) ».
   Vérifie le brouillon dans Buffer.
8. **Tâche planifiée** : dans Cowork, crée une tâche quotidienne à 7 h sur ce dossier avec le texte :
   « Lis CLAUDE.md et exécute la routine du jour. »

## Sons
`sons/son1.mp3` … `son4.mp3` sont intégrés directement dans la vidéo. Tu peux en ajouter/retirer.
Attention : des sons téléchargés depuis TikTok peuvent être protégés ; si Instagram ou TikTok coupe le son, remplace-les par des sons libres de droits ou ta propre voix.

## Contrôle
- `historique.md` : tout ce qui a été publié.
- Pour mettre en pause : désactive la tâche planifiée.
