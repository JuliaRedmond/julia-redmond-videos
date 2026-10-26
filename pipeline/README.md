# Julia Redmond video pipeline

Make a 1080x1920, 20-40 s, silent MP4 from one short JSON script. Brand: ivory `#FAF6EE`, navy `#1C2E46`, muted gold `#A89477` (sampled from the JR monogram). Fonts: Poppins (headings), Nunito Sans (body), Lora (parent quotes/scripts), all bundled in `template/fonts/` (SIL OFL).

## Make a video

```bash
cd pipeline
node tools/render.js scripts/V01_homework-first-step.json ../videos/batch-01/JR_V01_homework-first-step_parent.mp4
```

Needs Node + Playwright (Chromium) + ffmpeg. Also writes `<name>_copy.md` (caption + 3-5 hashtags, YouTube Shorts title, Pinterest title + description).

- `--check` audits that all text stays inside the safe zone (top 250 px, bottom 380 px, sides 60 px clear of app UI).
- `--stills=0.3,5,12` dumps PNG frames at those seconds instead of rendering.

## Script file

`tag` (top chip), `scenes[]`, `end` (tagline + one CTA), `copy` (caption, hashtags, YT title, Pinterest). Scene types:

| type | fields |
|---|---|
| `hook` | `lines[]`, `sub` (on screen from 0 s) |
| `not` | `quote`, `note` (struck-through "NOT THIS" card) |
| `say` | `quote`, `note` (navy Lora "SAY THIS" card) |
| `steps` | `title`, `steps[]`, `at[]` (reveal times) |
| `statement` | `lines[]` |

Every scene takes `dur` (seconds) and optional `k` (text scale, e.g. 0.9 for long lines). `*word*` gets a gold highlight swipe. Total length is the sum of scene durations plus `end.dur`.

## Brand rules baked in

- Logo `assets/logo/jr-monogram.png` is used unmodified on the end card only.
- No people/faces, no photos: type, cards and soft gold glow only.
- Audio is a silent track; add trending sounds in-app.
- CTA says "Link in bio". No URL appears on screen or in captions until the exact landing-page links are supplied.

## Calendar

`python3 tools/make_calendar.py` regenerates `../calendar/content-calendar.csv` and `.md`.

## Older work in this repo

`batch1-v2/`, `batch2-v2/`, `teens-40s/` and the root-level MP4s were made earlier with a different look (royal-blue/teal, Nunito + Kalam, a synthesised ragtime track, desk photo background). They are untouched. The new `pipeline/` is the ivory/navy/gold system.
