// node render_at.mjs <url> <out.mp4|prefix> <durée> [stills "0.5,3,8"]
import pw from '/opt/npm-tools/node_modules/playwright/index.js'; const { chromium } = pw;
import { spawn } from 'node:child_process';
const [url, out, durS, stills] = process.argv.slice(2);
const DUR = parseFloat(durS), FPS = 30;
const browser = await chromium.launch(process.env.NOGL ? {} : { args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
page.on('console', m => { if (m.type() === 'error') console.error('page:', m.text()); });
page.on('pageerror', e => console.error('pageerror:', e.message));
await page.goto(url);
await page.waitForFunction(() => window.__ready === true, null, { timeout: 60000 });
if (stills) {
  for (const s of stills.split(',')) {
    await page.evaluate(t => window.renderAt(t), parseFloat(s));
    await page.screenshot({ path: `${out}_${s}.png` });
  }
} else {
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const n = Math.round(DUR * FPS);
  for (let i = 0; i < n; i++) {
    await page.evaluate(t => window.renderAt(t), i / FPS);
    const buf = await page.screenshot({ type: 'jpeg', quality: 95 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 60 === 0) console.log(`frame ${i}/${n}`);
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r));
}
await browser.close();
