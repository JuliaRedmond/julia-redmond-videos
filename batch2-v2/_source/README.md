# Batch 2 v2: source

Renderer for the livelier Batch 2 videos (1080x1920, 30 fps, 18-22 s). Rendered MP4s are one folder up.

- `videos.py`: wording and timing for videos 02-12 (`python3 videos.py <outdir>` writes `vNN.json`). `video01.json` is Video 01.
- `page.html`: the animation engine. A pure function of time `setT(t)`, so every frame is deterministic.
- `render.js`: `node render.js <cfg.json> <out.mp4> <audio.wav>` captures each frame with headless Chromium and encodes with ffmpeg. Add `--stills=1.0,5.5` to dump PNGs instead.
- `check.js` + `cm2.py`: safe-zone audit (no text in the top 250 px / bottom 350 px or within 60 px of the sides) and worst-case text/background contrast (>= 4.5:1).
- `make_music.py`: the original ragtime backing track (synthesised, no samples).

Needs `assets/` (monogram.png, wordmark.png, desk-hero-1600.webp) and `fonts/` (nunito-regular.woff2, kalam-regular.woff2) copied from `julia-redmond-website/public/` next to `page.html`.

Music: after `make_music.py`, compress to match loudness: `ffmpeg -i silent_film_rag_long.wav -af "acompressor=threshold=-26dB:ratio=4:attack=5:release=90:makeup=8dB,alimiter=limit=0.5:level=disabled" rag_long_c.wav`.
