// Usage : node outils/upload.mjs sortie/v-2026-10-25-1.mp4  → affiche l'URL publique permanente
// Nécessite un fichier .env à la racine : CLOUDINARY_CLOUD=xxx et CLOUDINARY_PRESET=yyy (preset « unsigned »)
import { readFile } from 'node:fs/promises';
import { basename } from 'node:path';

const env = Object.fromEntries((await readFile('.env', 'utf8')).split('\n').filter((l) => l.includes('=')).map((l) => l.split('=').map((s) => s.trim())));
const file = process.argv[2];
const fd = new FormData();
fd.append('file', new Blob([await readFile(file)], { type: 'video/mp4' }), basename(file));
fd.append('upload_preset', env.CLOUDINARY_PRESET);
fd.append('folder', 'salwaa');
const r = await fetch(`https://api.cloudinary.com/v1_1/${env.CLOUDINARY_CLOUD}/video/upload`, { method: 'POST', body: fd });
const j = await r.json();
if (!j.secure_url) { console.error(j); process.exit(1); }
console.log(j.secure_url);
