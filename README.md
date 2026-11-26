# Wednesday 25 November 2026 — The World in One Page

[![news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/akbare12/news-25-b151-numbers/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/akbare12/news-25-b151-numbers/reward.svg)](https://make.fun/bounty/news-image-20261125)

**50 stories. One image. Every story dated Wednesday 25 November 2026.**

## What is in the image

- **3 heroes** — Trump tariffs on 14 partners (China 20%, up to 40% if the
  truce fails); Kospi −6.16% with Samsung −9.87% and Hynix −11.05%;
  Shenzhou-24 lifting off at 08:18 Beijing with Pakistan's Ali, 40, the
  first foreign astronaut aboard.
- **10 cards** — including the Hamas security chief killed in Shati and
  the Bogor gold mine flood (9 dead, 17 trapped).
- **37 ALSO items** — one more line each, every one tagged with
  its own `[C]`, `[R]` or `[CL]` chip.
- **A UTC timeline, a numbered world map, and a DATE CHECK** that lists
  exactly the five stories left out because they are not from 25 November.

Every card and every ALSO item carries a chip: `[C]` confirmed,
`[R]` reported, `[CL]` claim.

## Files

- `entry.png` — the 1024x1024 submission image.
- `gen.py` — the build-time renderer (Pillow). Run `python3 gen.py`
  to rebuild `entry.png`; it asserts every text fit, every timeline
  label, every map pin and label before saving.
- `main.py` — the graded entry point. Standard library only: it copies
  `entry.png` into `$MAKEFUN_OUTPUT_DIR` (default `out`).

## Build

```sh
python3 gen.py            # rebuilds entry.png (493 geometry checks)
MAKEFUN_OUTPUT_DIR=out python3 main.py
```
