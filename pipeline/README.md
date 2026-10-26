# Julia Redmond video pipeline

Make a 1080x1920, 20-27 s MP4 from one short JSON script, in the established format of `batch1-v2/JuliaRedmond_B1v2_HR6_Done_Means_Checked.mp4`: faded desk photo, skill tag pill + progress bar, dark label chip, bold Nunito headline with yellow highlighter sweeps, six-skill pills, ivory end card with the JR logo, and the same ragtime music.

## Make a video

```bash
cd pipeline
node tools/render.js scripts/V01_homework-first-step.json ../videos/batch-01/JR_V01_homework-first-step_parent.mp4
node tools/render.js scripts/V01_homework-first-step.json x.mp4 --check     # audits, no render
```

Needs Node + Playwright (Chromium) + ffmpeg. Also writes `<name>_copy.md` (caption + 3-5 hashtags, YouTube Shorts title, Pinterest title + description). Other flags: `--stills=0.4,5,12` (PNG frames), `--silent` (no music).

`--check` does two audits: every text element stays inside the safe zone (top 250 px, bottom 350 px, sides 60 px), and **no two visible text elements ever overlap**, sampled every 1/20 s including mid-transition.

## Script file (`scripts/*.json`)

Timings are planned automatically (`tools/plan.js`) to land at about 20-27 s; you only write content.

```
id, title, audience, theme, skills:["START"] (tag pill + bar colour), focus (background pan 0-1), cta, copy{...}
beats[]: first beat is always a hook; the rest are in any order
```

| beat | fields |
|---|---|
| `hook` | `label` (e.g. "PARENT SCRIPT #1"), `lines[]` (string or `{t,hl}`), `strike:[line indexes]` |
| `try` | `label` ("SAY"/"ASK"/"TRY"), `note` (yellow sticky), `pre[]`, `post[]` |
| `statement` | `lines[]` of `{t, hl, strike}` (`hl` = substring that gets the yellow sweep) |
| `checks` | `header[]`, `items[]` (tick cards in the skill colour) |
| `chips` | `skills[]` (six pills pop in one at a time; use for six-skill videos) |

Label series so far: PARENT SCRIPT #n, STUDY HACK #n, ROUTINE #n, HOMEWORK RULE #n.

## What's in `assets/` and `template/`

- `assets/logo/jr-monogram.png`: logo, used unmodified on the end card.
- `assets/bg/desk-hero.webp`: desk area of the kids' book cover only (no people, no cover text), faded to cream at the top. Built from the front-cover image in the cover PDF; the PDF's other photo (people) is not used.
- `assets/ragtime-loop.m4a`: the original synthesized ragtime (`batch1-v2/_source/make_music_b1.py` + the compressor line in `batch2-v2/_source/README.md`). Matches the reference video's audio (0.99 correlation, same loudness, -20.7 LUFS). No samples.
- `template/fonts/`: Nunito and Kalam (the reference's fonts; SIL OFL).
- Skill colours: START green, PLAN blue, TIME orange, FOCUS purple, ORGANIZE red, FINISH deep blue (exactly as in the reference).

## Brand rules still enforced

No AI people or faces; no invented stats, testimonials or credentials; EF is framed as buildable skills, never as treatment; CTA says "link in bio" and no URL appears until the real landing-page links are supplied; nothing is published or scheduled from here.

## Calendar

`python3 tools/make_calendar.py` regenerates `../calendar/content-calendar.csv` and `.md`.

## Older work in this repo

`batch1-v2/`, `batch2-v2/`, `teens-40s/` and the root-level MP4s are untouched. `homework-calm-instrumental.wav` is a different, unused track.
