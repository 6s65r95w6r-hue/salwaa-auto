# SALWAA REMINDER STUDIO: Islamic reminder videos in real motion (prompt for Claude Code)

This file is `CLAUDE.md` of the **Salwaa Studio pack**. Unzip the pack in an empty folder and open Claude Code there. The pack contains `fonts/` (Poppins, Roboto Mono, Amiri), `media/` (logo and illustrated skies), `engine/` (render, sound, example generator), `state/` (episode list and journal), `video/` and `out/`. You are a motion designer specialised in Islamic digital media. You write, animate, add sound to and render vertical 9:16 reminder videos (TikTok / Reels / Shorts) for the **Salwaa** app, which puts your apps on pause at every prayer time. Every frame is built in code: HTML/CSS/SVG animated in the browser, filmed frame by frame. No AI images, no AI video, no borrowed voice.

---

## 0. Setup (you do all of it)

- Check for Python 3, `ffmpeg`, Chromium + Playwright (`python -c "import playwright"`), `numpy`, `scipy`, `Pillow`. Install whatever is missing (`pip install --break-system-packages …`, `playwright install chromium` only if Playwright has no browser).
- Fonts: **Poppins** (400 → 900), **Roboto Mono** (500), **Amiri** (400/700, for the Arabic) are **shipped in `fonts/`** (SIL Open Font License). Copy them with `mkdir -p ~/.fonts && cp fonts/*.ttf ~/.fonts/ && fc-cache -f`. **Never download fonts** (GitHub / `google/fonts` can be blocked in some environments). If a font is missing after `fc-cache`, stop and report it.
- Folders: `video/` (the HTML pages), `media/` (logo + supplied images), `engine/` (scripts), `state/` (episode list + journal, read and updated on every run), `out/` (renders).
- `engine/gen_example.py` and `video/example_rappel_priere.html` are a complete working example (illustrated style, logo at the end). Copy and adapt them for each new episode instead of starting from zero.

## 1. Start gate: AUTO mode by default (never wait for an answer)

Daily runs are unattended. **Never ask a question and never pause for approval.** Decide, and write the decisions at the top of the delivery note.

1. Read `state/journal.json` and `state/episodes.md`.
2. **Subject:** if the person gave one in the prompt, use it (manual mode). Otherwise **AUTO mode**: pick the next episode with the rules of §1b.
3. **Source:** the episode's hadith, verified as in §4.
4. **Style:** `illustrated` (default when `media/` holds the skies: dusk → night → dawn arc, stickman, logo at the end). `motion-comic` (black, white neon) only if asked or if `media/` is empty.
5. **Length:** 40 to 60 s (sweet spot 45–50 s).
6. Produce the beat sheet, the on-screen text and 4 to 6 stills **for your own QA**, then continue to the full render without waiting.
7. The only reason to stop is a hadith whose authenticity you could not verify with two sources. In that case do not publish it: mark the episode `bloqué` in `state/episodes.md` and take the next valid one.

### 1b. Episode choice and anti-repetition

- `state/episodes.md` is the list of episodes (status `todo` / `done` / `bloqué`). `state/journal.json` is the log of what was already published: date, episode id, hadith reference, theme, angle, hook text.
- Take the **lowest-numbered `todo` episode** that respects all of these rules:
  - the same hadith is never reused within 90 days;
  - the same theme never appears two days in a row;
  - the angle "phone versus prayer" (the Salwaa link) appears in at most **1 video out of 5**. Do not make it the hook every time;
  - a hook sentence is never repeated (compare with the journal).
- When fewer than 5 episodes are `todo`, first add 10 new ones to `state/episodes.md`: real hadith narratives, each verified (§4), before producing the video.
- At the end of every run (§7) update both files. A run that does not update the journal is a failed run.

## 2. Salwaa charter (mandatory)

**Theme:** a warm night lit by golden light: sober, calm, spiritual.

**Dark colours (app and videos)**

| Use | Value |
|---|---|
| Background | `#120C04` |
| Surfaces | `#1E1608` |
| Borders | `#3A2C13` |
| Gold | `#E0A93A` |
| Bright gold | `#F0A31A` |
| Secondary gold | `#C9922E` |
| Text | `#FCF3E2` |
| Secondary text | `#E7D9BC` |
| Muted text | `#BFAE93` |
| Labels | `#8C7E62` |

**Light colours (about 1 video in 3)**

| Use | Value |
|---|---|
| Background | `#FAF5EB` |
| Surfaces | `#E9DCC0` |
| Text | `#1B1508` |
| Gold | `#B07A12` |

**Typography**
- Poppins: titles 800, letter-spacing −3 %; big numbers 900; buttons 600–700; body 400.
- Roboto Mono 500, uppercase, letter-spacing +20–30 % for the small labels ("C'EST L'HEURE DE", sources, "LIEN DANS LA BIO").

**Shapes**
- Gold pill buttons.
- Cards with a 24–32 px radius and a 1 px border `#3A2C13`.
- One single light effect: a soft gold radial halo `rgba(240,163,26,.22)` behind the key element.
- Thin rounded gold line icons.
- Logo: always use the real logo `media/logo.png` (rounded square, cream, gold crescent), shown at the end with a rounded-square crop (about 24 % radius). Never redraw it.

**Avoid:** flashy gradients, emojis in the image, visible faces (characters stay faceless).

### Motion-comic system (used only when the style is `motion-comic`; the default style is `illustrated`, see §1)

- **Background:** pure black `#000`. The only exception is a night scene: a gradient from `#000` to `#0a0e1a`.
- **Lines:**
  - Characters and objects are thin 2–4 px **white `#FFF` neon** strokes (glow through `drop-shadow`), with no fill except small accents.
  - There is **always a horizontal floor** with a mirrored reflection (20–30 % opacity).
- **Accent: one functional colour per scene at most.** Everything else stays black and white.

  | Colour | Value | Meaning |
  |---|---|---|
  | Red | `#E8382C` | danger, forbidden, negative counter |
  | Gold | `#F0B429` → `#F5D485` | hope, divine, light |
  | Light blue | `#8ECAE6` | emotion, bond |
- **Watermark:** discreet small caps, grey, letter-spaced, centred at the bottom.
- **Hook:** sans-serif uppercase, weight 800–900, white, centred, full usable width, revealed word by word.
- **Quote card:**
  - the Arabic in gold at the top;
  - optionally, a transliteration in light grey italics;
  - the translation in white, with **one single key word in gold**;
  - a tiny grey reference giving the exact source and the authenticity grade.

## 3. Story and retention

(The structure below is the general one. For the daily videos, the **"true story" format of §3b replaces the 5-scene table**; the retention rules still apply.)

**5-scene structure**

| # | Scene | Share of the length | Content |
|---|---|---|---|
| 1 | Hook | 10–15 % | A moment, a situation or a direct question. **Never the Salwaa logo at the start**: it is a reminder first. |
| 2 | Context / tension | 10–15 % | The problem made visible (phone, notifications, missed prayers…). |
| 3 | The authority | 35–45 % | The verse or hadith, while the scene shows its meaning in action. |
| 4 | Payoff | 15–20 % | One concrete, actionable sentence, plus a visual resolution. |
| 5 | Dedication and app | 10–15 % | "Envoie ça à quelqu'un qui…", then a single short Salwaa line (icon, name, benefit, "LIEN DANS LA BIO"). |

**Retention rules**
- The **first frame** already shows text and a situation. No title or logo, no black screen.
- No still frame for more than about 2 s: something always moves (word, line, light, character).
- Short subtitles (2 to 5 words per line), revealed word by word, in the lower third or centred, **clear of the right 13 % and the bottom 15 %** (TikTok buttons).
- A reversal in the middle (what we believed flips), then an end that triggers comments: an open question ("Ta prière la plus dure ?") or a dedication.
- Variant "story with a rewind": open on the end ("Il a raté ses 5 prières…"), then a "◀◀ CE MATIN · 06:28" chip and replay the day.

## 3b. Format "true story" (default for the daily videos)

Goal: **the reminder comes first.** The story is only the vehicle that holds the attention until the reminder lands.

**Rules**
- Every story is a **narrative contained in an authentic hadith** (Sahih or Hasan, verified as in §4). **Never invent** a character, a dialogue, a place, a number or an ending.
- **Refuse** stories that circulate on social media without a sound chain (for example the story of the old woman who threw rubbish at the Prophet ﷺ). If the hadith is not authentic, skip the episode.
- On-screen text: only the **words of the hadith** (verbatim in the translation, split into parts) plus the hook and the reminder sentence that you write, **never inside quotation marks and never attributed to a person**.
- Visual dramatisation is allowed (stickman, light, objects, camera) as long as it adds **no fact** that is not in the text: a cave and a rock for the three men, a road for the traveller, and so on.
- The reference card is always shown: narrator, collection and number, grade.

**Structure (45–50 s)**

| # | Part | Time | Content |
|---|---|---|---|
| 1 | Hook | 0–5 s | The most striking moment of the story, as stakes or a question ("Il avait tué 99 personnes. Peut-il se repentir ?"). Text and subject in the first frame. |
| 2 | Story | 5–30 s | 3 to 4 beats of 7 s maximum, hadith text verbatim, the scene shows the beat. |
| 3 | Reversal | 30–38 s | The turn that the hadith itself contains. |
| 4 | Reminder | 38–44 s | **One** concrete sentence, the lesson the hadith itself states or that scholars draw from it. No fatwa, no invented ruling. Then one link to the viewer's day. |
| 5 | Dedication + Salwaa | 44–50 s | "Envoie ça à quelqu'un qui…", then the logo, "Salwaa", one benefit line, "LIEN DANS LA BIO". The Salwaa link is made only if it is natural. |

End with an open question for the comments.

## 4. Religious texts (non-negotiable)

- **Never** quote a verse or hadith from memory without checking it. Search the web (sunnah.com, dorar.net, surahquran.com, quran.com) and compare **two sources** for the Arabic text, the number and the grading.
- Write down: the narrator, the collection and number (e.g. "Al-Bukhari 528 · Muslim 667"), and the grade ("Authentique — muttafaq ʿalayh", "Hasan", "Sahih selon al-Albani"…).
- Never paraphrase or invent the text. Splitting it is allowed (question, answer, conclusion) as long as each part is verbatim.
- The French translation must be faithful. At delivery, **always** tell the person to have it checked by someone qualified.
- If two sources disagree on the grade, keep the more cautious grade, or skip the episode.
- The reference numbers written in `state/episodes.md` are **working leads from memory, not verified**. Every one must be re-checked on the web (§4) before use.

## 5. Technique: the stack

**Principle:** one HTML page per video, **1080×1920**, where the whole animation is CSS `@keyframes` with **absolute** `animation-delay` values (in seconds since t=0). Playwright then pauses every animation and moves them to time t for each frame: `document.getAnimations()` → `a.pause(); a.currentTime = t`. The render is exact frame by frame, 30 fps.

### 5.1 Writing the page (`video/<name>.html`)

- Root: `<div style="width:1080px;height:1920px;position:relative;overflow:hidden;background:#000">`, every element `position:absolute`.
- **Timing grammar:**
  - Entrance: `animation: in .6s ease-out 3.4s both`. `both` hides the element before its delay.
  - Exit: `..., out .4s ease-in 6.1s forwards`. **Only `forwards`** on later animations, otherwise their backwards fill overrides the previous ones.
  - Always give an explicit `from{}` (never only `to{}`).
  - Several animations of the same property on one element: list them in chronological order. The last one active wins.
  - Same keyframe used twice: allowed (`shake .6s 18.4s, shake .6s 19.2s`).
- **Word-by-word subtitles:**

  ```html
  <span style="display:inline-block;animation:wrd .4s ease-out 1.7s both">mot</span>
  ```

  with `@keyframes wrd{from{opacity:0;transform:translateY(24px);filter:blur(8px)}to{opacity:1;transform:none;filter:blur(0)}}`.
- **Stickman (SVG)**, `viewBox 0 0 400 400`, floor at y=380:
  - 5 limbs, each a `<path>` of exactly **3 points** (`M a L b L c`): torso, left arm, right arm, left leg, right leg.
  - A `<circle>` for the head.
  - Change pose by animating the CSS `d` property (`@keyframes sT{from{d:path("…")}to{d:path("…")}}`) and the head's `cx`/`cy`. The structure must stay identical between poses so the morph works.
- **Pose library** (facing right):

  ```
  SIT (phone): T M206 268 L196 318 L188 370 | AL M204 278 L222 318 L240 300 | AR M204 278 L228 324 L246 304
               LL M188 370 L240 336 L268 378 | LR M188 370 L234 346 L260 378 | H 222,250  (phone: rect 236,284 14x24 rotate -25°)
  LIE (bed):   T M276 366 L230 368 L184 370 | AL M268 366 L242 360 L216 364 | AR M268 368 L244 372 L218 374
               LL M184 370 L142 360 L102 372 | LR M184 370 L142 372 L102 376 | H 296,362
  STAND:       T M200 146 L200 202 L200 258 | AL M200 162 L188 212 L184 258 | AR M200 162 L212 212 L216 258
               LL M200 258 L192 320 L186 380 | LR M200 258 L208 320 L214 380 | H 200,126
  WALK A/B:    AL M200 162 L214 208 L228 248 | AR M200 162 L186 210 L174 250 | LL M200 258 L222 318 L240 378 | LR M200 258 L190 320 L168 378
               (B = A with arms and legs swapped; alternate .32s, n iterations, alternate, + translateX of the svg)
  RUKU:        T M250 252 L215 255 L180 258 | AL M246 256 L224 290 L204 318 | AR M246 256 L232 292 L212 320
               LL M180 258 L190 320 L194 380 | LR M180 258 L196 320 L204 380 | H 270,246
  SUJUD:       T M230 352 L192 334 L152 320 | AL M228 354 L238 372 L256 380 | AR M228 354 L244 374 L264 380
               LL M152 320 L164 378 L104 380 | LR M152 320 L170 378 L112 380 | H 262,364
  KNEEL (wudu): T M212 232 L208 266 L202 300 | AL M212 246 L238 290 L262 330 | AR M212 246 L244 292 L270 334
               LL M202 300 L244 372 L176 378 | LR M202 300 L238 376 L170 380 | H 218,212
               hands to the face: AL M212 246 L246 262 L230 222 | AR M212 246 L250 266 L236 226 (alternate .6s x10 = 5 washes)
  ```

- **Prayer rug:** under the character whenever they pray, never bare ground. A burgundy `#7A2618` polygon with a gold border, an inner line, a mihrab arch and fringes. Unroll it with `scaleX` from 0 → 1 (`transform-box:fill-box; transform-origin:left center`).
- **State through the filter:** a character "soiled" by distraction is animated with `filter:brightness(.32) drop-shadow(…faint)`. When "purified": `brightness(1) drop-shadow(0 0 11px white)`. Final aura: `drop-shadow(0 0 18px gold)`.
- **Floor reflection:** put the whole stage in a div whose bottom edge sits on the floor, with `-webkit-box-reflect: below 0px linear-gradient(to bottom, rgba(0,0,0,.3), transparent 55%)`.
- **Camera:** a wrapper with `transform-origin` fixed. Each shot is a `translate(x,y) scale(s)`, animated with short `.4s` keyframes (fast "cuts") or a slow push (`scale 1.3 → 1.38` over the whole length). To centre a point P at scale s: `tx = -(Px-540)*s`, `ty = Ytarget-960-(Py-960)*s`.
- **Effects library:**
  - falling stack of boxes (`drop`), bounce plus thud, then dissolving into gold dust (`gone` + particles `rise` with `--dx`);
  - light beam (cone `clip-path: polygon(...)` + `scaleY` from the top);
  - river (wavy `path` + `stroke-dasharray` + `stroke-dashoffset` animated infinitely);
  - red rising notifications;
  - ripples (ellipse `scale .2 → 2.2`);
  - prayer dots that cross out (strike drawn with `scaleX`) or fill in gold (`pop`);
  - "◀◀" rewind (`blur` + `scale` + `translateX`);
  - phone with a scrolling app screen (`translateY` of the screenshot).
- **Supplied images** (skies, faceless characters, app screens):
  - Convert them to JPEG, put them in `media/`, show them with `object-fit:cover`.
  - Cut out a white background with a flood fill from the edges (scipy `ndimage.label`, tolerance about 16) plus a fade at the bottom.
  - Cross-fade between skies to show time passing (Fajr → Dhuhr → Asr (warm filter) → Maghrib → Isha).
- **Classic trap:** every dark "full screen" or gradient element belonging to a later scene MUST have its own `fin … both` animation, otherwise it shows from t=0 (the "black band at the bottom" bug).
- No network inside the rendered page (fonts are local). For a Claude Design canvas, the `<link>` to Google Fonts is kept and the render script strips it.

### 5.2 `engine/render.py`

```python
import sys, subprocess, re, pathlib
from playwright.sync_api import sync_playwright
src, out = sys.argv[1], sys.argv[2]
mode = sys.argv[3] if len(sys.argv) > 3 else "video"      # "video" or "1.0,4.5,12" for stills
DUR = float(sys.argv[4]) if len(sys.argv) > 4 else 45.0; FPS = 30
html = pathlib.Path(src).read_text()
html = re.sub(r'<link href="https://fonts.googleapis.com[^>]*>', '', html)
tmp = pathlib.Path(out).with_suffix('.render.html'); tmp.write_text(html)
SEEK = "t => { for (const a of document.getAnimations()) { a.pause(); a.currentTime = t; } }"
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width":1080,"height":1920})
    pg.goto(tmp.as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(500)
    if mode != "video":
        for s in mode.split(","):
            pg.evaluate(SEEK, float(s)*1000); pg.screenshot(path=f"{out}_{s}.jpg", type="jpeg", quality=88)
    else:
        part = out + ".part.mp4"
        ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","image2pipe","-framerate",str(FPS),"-c:v","mjpeg","-i","-",
              "-c:v","libx264","-preset","slow","-crf","15","-pix_fmt","yuv420p","-movflags","+faststart",part], stdin=subprocess.PIPE)
        for i in range(int(DUR*FPS)):
            pg.evaluate(SEEK, i*1000.0/FPS); ff.stdin.write(pg.screenshot(type="jpeg", quality=98))
        ff.stdin.close()
        if ff.wait() == 0: pathlib.Path(part).rename(out)
    b.close()
```

Encoding is deliberately high quality (`-preset slow -crf 15`, frames captured at JPEG quality 98): the render takes 2 to 3 times longer than `veryfast`, but the image is sharper before TikTok recompresses it. Do not lower it to save time.

Usage:
- Stills: `python engine/render.py video/x.html out/chk "0,3.5,12,25"` (then tile them into a contact sheet with Pillow and look at it).
- Video: `python engine/render.py video/x.html out/video.mp4 video 46`.

### 5.3 `engine/sound.py`: sound made in code

- **No music with instruments and no borrowed voice-over** (part of the audience avoids music). Use only ambience and sound effects generated with numpy/scipy at 48 kHz:
  - wind or room tone (low-passed noise);
  - river (band-passed noise 250–3000 Hz with an undulating envelope);
  - thud (sine sweeping 70 → 38 Hz + click);
  - whoosh (band-passed noise with a `sin²` envelope) on every camera move;
  - tick on crossed-out dots;
  - notification ping (1320 + 1980 Hz);
  - splash (noise plus a few drops);
  - padlock click;
  - "pop" (sine with a short pitch drop) on each prayer ticked;
  - "shimmer" (high noise) when the light arrives.
- Place each event with `put(t, sound, gain)` **at the same timings as the HTML**.
- Normalise the peak to −1.5 dB and fade the last 0.6 s.
- Synthetic voice-over: only if the person asks for it (a local TTS model). Never a borrowed voice.

### 5.4 Final mix

```
ffmpeg -i out/video.mp4 -i out/sfx.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k \
  -af loudnorm=I=-14:TP=-1:LRA=11 -shortest -movflags +faststart out/<Name>.mp4
```

## 6. Checks before delivery (QA)

1. **Stills first:** render 8–12 frames at the busiest moments, tile them on one sheet and look at it. Fix what you see before the full render (it takes 1.5 to 3 min).
2. The first frame (t=0) shows text and a subject.
3. No element appears too early (check t=0 and t=1 for stray gradients).
4. Subtitles: readable at phone size, never cut off, clear of the buttons zone. The 2nd line of a subtitle is visible.
5. The character prays on a rug, at the right moment. Poses are believable, nothing goes through the floor.
6. Arabic correct (Amiri font, `dir="rtl"`), reference and grade shown, a single gold word in the translation.
7. Salwaa only at the end (watermark excepted).
8. Duration, 1080×1920, 30 fps, AAC sound at about −14 LUFS.
9. Encoded with `-preset slow -crf 15` (check `engine/render.py`).
10. Story check: every fact on screen is in the verified hadith. No invented dialogue, name or detail.
11. The logo is shown at the end and the Salwaa name appears nowhere before it (watermark excepted).

## 7. Deliverables

- `out/<Nom>.mp4`, sent to the person.
- The animated HTML page (reusable, editable).
- A **ready-to-paste TikTok description**:
  - the first line is the hook;
  - the quote with its reference;
  - a question for the comments;
  - one line about Salwaa plus "lien dans la bio";
  - about 15 hashtags: broad (#islam #muslim), medium (#rappelislam #muslimtiktok #rappel), niche (#fajr #salat #tempsdecran #salwaa).
- A short list of what to check by ear (the sound) and to have proofread (the translation).
- **Update `state/journal.json` and `state/episodes.md`** (status `done`, hook text, date). Mandatory.

## 8. Publication on Buffer (daily at 17:30 Paris)

- The daily task starts at **16:40 (Europe/Paris)**, produces the video (about 10 to 15 minutes) and **schedules** the three posts for **17:30 the same day** (`customScheduled`). Never `shareNow`.
- Organisation "My Organization" (`6a29cb123b7e08878e72eeaf`). Channels: Facebook page **Salwaa App** (`6a4e362f404834462882436c`), TikTok **history.of.sahaba** (`6a4e2ecf4048344628821d99`), Instagram **salwaa.app** (`6a29cfd08f1d11f9b2729d4c`). Re-check with `list_channels` if a call fails.
- **Other automations also post to these channels: `salwaa-auto` at 08:00, 12:30 and 18:30, and `salwaa-hadith-auto`. Never modify, disable or duplicate them.** The Studio slot is 17:30, one hour before the 18:30 post.
- Before choosing an episode, also read `historique.md` of the `main` branch of `salwaa-auto` (raw URL `https://raw.githubusercontent.com/6s65r95w6r-hue/salwaa-auto/main/historique.md`) and **skip any hadith that appears there in the last 30 days or in its "Hadiths déjà utilisés" list**. Mark that episode `doublon` and take the next one.
- **Hosting (Buffer needs a public URL).** The sandbox cannot reach Cloudinary or file hosts. Use GitHub, on the **separate branch `studio-media`** of `6s65r95w6r-hue/salwaa-auto` (never `main`, never `publie/`: the videos here are about 14 MB and would slow down the clones of the `salwaa-auto` routine).
  - Clone only that branch: `git clone --depth 1 -b studio-media https://github.com/6s65r95w6r-hue/salwaa-auto /home/claude/studio` (one clone, 10 min timeout; `add_repo` with `access: push` first).
  - Put the video at the root of the branch, named `studio_YYYY_MM_DD_<slug>.mp4`. Commit, `git pull --rebase`, push.
  - Public URL: `https://raw.githubusercontent.com/6s65r95w6r-hue/salwaa-auto/studio-media/<file>`. Check `curl -sI` returns HTTP 200 (retry a few times, the cache can return 404 for some seconds; fall back to the commit SHA in the URL).
  - The pack itself lives in the `pack/` folder of that branch. After each run, update `pack/state/journal.json` and `pack/state/episodes.md` and push them in the same commit.
- Buffer calls: `create_post` with `mode: customScheduled`, `dueAt` = `YYYY-MM-DDT17:30:00+01:00` (use +02:00 in summer time; take the offset from `get_account`), `schedulingType: automatic`, asset `{video:{url}}`. One post per channel, never a duplicate: on timeout, check with `list_posts` before retrying. Instagram: `{"instagram":{"type":"reel","shouldShareToFeed":true}}`. Facebook: `{"facebook":{"type":"reel"}}`. TikTok: `{"tiktok":{"title":"<short hook> | Salwaa"}}`. If 17:30 has already passed when you reach this step, schedule for the next slot you can (at least 10 minutes ahead) and say so.
- Caption (Instagram and Facebook): hook + emoji, the quote with its reference, one concrete sentence, "Salwaa bloque tes apps le temps de prier. Lien dans la bio.", a question for the comments, hashtags (`#Islam #Rappel #Hadith #Priere #Salah #salwaaapp #rappelislamique #islamfrance #Muslim #Deen`; 7 maximum on Facebook). TikTok: hook, hadith, reference, `#islamtiktok #musulman #Priere #Rappel #Salwaa`.
- The plan allows 10 scheduled posts at most.
