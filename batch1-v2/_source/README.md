# Batch 1 v2: source

Same engine as `batch2-v2/_source` (page.html is a backward-compatible extension: per-line struck hooks, struck statement lines, a label-less TRY note, and a six-chip beat). Re-rendering a batch2-v2 config with this engine reproduces batch2-v2.

- `videos_b1.py`: wording and timing (`python3 videos_b1.py <outdir>` writes one json per video).
- `render.js`, `check.js`, `cm2.py`: same as batch2-v2 (render, safe-zone audit, contrast audit).
- `make_music_b1.py`: same ragtime piece as batch2-v2, extended to about 38 s so 30 s videos are covered; compress with the ffmpeg line in `batch2-v2/_source/README.md`.

Needs `assets/` and `fonts/` from `julia-redmond-website/public/` next to `page.html` (see batch2-v2 README).
