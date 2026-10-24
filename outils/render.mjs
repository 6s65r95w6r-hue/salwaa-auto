// Usage : node outils/render.mjs "videos/v-2026-10-25-1.dc.html" sons/son2.mp3 sortie/v-2026-10-25-1.mp4
import { chromium } from 'playwright';
import { createServer } from 'node:http';
import { readFile, mkdir, rm } from 'node:fs/promises';
import { extname, join, resolve } from 'node:path';
import { execFileSync } from 'node:child_process';

const [page_, son, out] = process.argv.slice(2);
if (!page_ || !out) { console.error('usage: render.mjs <page.dc.html> <son.mp3|-> <sortie.mp4>'); process.exit(1); }
const ROOT = resolve('videos'), FPS = 30;
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.jsx': 'text/javascript', '.png': 'image/png', '.json': 'application/json' };

const server = createServer(async (req, res) => {
  try {
    const p = join(ROOT, decodeURIComponent(new URL(req.url, 'http://x').pathname));
    res.writeHead(200, { 'Content-Type': MIME[extname(p)] || 'application/octet-stream' });
    res.end(await readFile(p));
  } catch { res.writeHead(404); res.end(); }
}).listen(0);
const port = server.address().port;

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
// Mode hors ligne : sert React, Babel et les polices depuis node_modules si le réseau les bloque.
const NM = resolve('node_modules');
const LOCAL = {
  'react.production.min.js': join(NM, 'react/umd/react.production.min.js'),
  'react-dom.production.min.js': join(NM, 'react-dom/umd/react-dom.production.min.js'),
  'babel.min.js': join(NM, '@babel/standalone/babel.min.js'),
};
const faces = [];
for (const w of [500, 600, 700, 800, 900]) faces.push(`@font-face{font-family:'Poppins';font-weight:${w};src:url(http://fonts.local/p${w}.woff2) format('woff2')}`);
for (const w of [400, 500]) faces.push(`@font-face{font-family:'Roboto Mono';font-weight:${w};src:url(http://fonts.local/m${w}.woff2) format('woff2')}`);
await page.route(/unpkg\.com|fonts\.googleapis\.com|fonts\.gstatic\.com|fonts\.local/, async (route) => {
  const u = route.request().url();
  try {
    if (u.includes('fonts.googleapis.com')) return route.fulfill({ contentType: 'text/css', body: faces.join('\n') });
    if (u.includes('fonts.local')) {
      const m = u.match(/\/([pm])(\d+)\.woff2/);
      const f = join(NM, m[1] === 'p' ? `@fontsource/poppins/files/poppins-latin-${m[2]}-normal.woff2` : `@fontsource/roboto-mono/files/roboto-mono-latin-${m[2]}-normal.woff2`);
      return route.fulfill({ contentType: 'font/woff2', headers: { 'access-control-allow-origin': '*' }, body: await readFile(f) });
    }
    const k = Object.keys(LOCAL).find((n) => u.endsWith(n));
    if (k) return route.fulfill({ contentType: 'text/javascript', body: await readFile(LOCAL[k]) });
  } catch (e) { console.error('route', u, e.message); }
  return route.continue();
});
const rel = page_.replace(/^videos\//, '');
await page.goto(`http://localhost:${port}/${encodeURI(rel)}`, { waitUntil: 'networkidle' });
const stage = page.locator('[data-om-exportable-video-with-duration-secs]');
await stage.waitFor({ timeout: 30000 });
await page.waitForFunction(() => document.fonts.ready.then(() => true));
await page.waitForTimeout(1500);
const dur = parseFloat(await stage.getAttribute('data-om-exportable-video-with-duration-secs'));
const frames = Math.ceil(dur * FPS);

const tmp = resolve('sortie/_frames');
await rm(tmp, { recursive: true, force: true }); await mkdir(tmp, { recursive: true });
for (let i = 0; i < frames; i++) {
  await page.evaluate((t) => {
    const el = document.querySelector('[data-om-exportable-video-with-duration-secs]');
    el.dispatchEvent(new CustomEvent('data-om-seek-to-time-frame', { detail: { time: t, sync: true, playing: false } }));
  }, i / FPS);
  await stage.screenshot({ path: join(tmp, String(i).padStart(5, '0') + '.png') });
  if (i % 60 === 0) console.log(`image ${i}/${frames}`);
}
await browser.close(); server.close();

const args = ['-y', '-framerate', String(FPS), '-i', join(tmp, '%05d.png')];
if (son && son !== '-') args.push('-stream_loop', '-1', '-i', son, '-shortest', '-c:a', 'aac', '-b:a', '160k', '-af', `afade=t=out:st=${Math.max(0, dur - 1)}:d=1`);
args.push('-vf', 'scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-r', String(FPS), '-movflags', '+faststart', out);
execFileSync('ffmpeg', args, { stdio: 'inherit' });
await rm(tmp, { recursive: true, force: true });
console.log('OK ' + out + ' (' + dur.toFixed(1) + ' s)');
