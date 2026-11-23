# Monday 23 November 2026 — The World in One Page

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/bangfadli121-arch/news-image-20261123-entry/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/bangfadli121-arch/news-image-20261123-entry/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A one-page newspaper front page that sums up the world's news of
**Monday 23 November 2026** in a single 1024×1024 image.

## What is on the page

- **Giant date headline** — Monday 23 November 2026, the day the page sums up.
- **Three hero stories** — COP31 collapses in Antalya; the Iran war widens
  to Bahrain and the Strait of Hormuz; Ukraine sinks the Russian corvette
  Merkury in Benghazi, Libya. Each has a hand-drawn illustration.
- **Six big numbers** — 258 House seats, −5.8% Kospi, 11,762 Ebola cases,
  34 workers missing, 404 flights cancelled, 7 sea drones.
- **Where the news was** — stories counted by region.
- **Ten small cards** with mini illustrations — Ukraine, Kospi, the US
  House, Gaza, the Sputnik-S space nuke, Huang's return, Chapo Isidro,
  the SpaceX lawsuits, Korea's exam scandal, the Denmark plot.
- **A world map** — "Where it happened", with a red dot for each place.
- **Also on Monday** — 22 more stories, numbered, for a total of 35.
- **Date check** — the Shenzhen summit of 19 November is deliberately
  left out: it happened four days before this paper.

Every story happened, or was first reported, on Monday 23 November 2026.
All drawings are original, drawn procedurally with Pillow. No photos.

## How it runs

`draw.py` draws `entry.png` at build time (Pillow). `main.py` is the
entrypoint: it copies `entry.png` to `/output/entry.png` (or
`$MAKEFUN_OUTPUT_DIR/entry.png`). Standard library only, no network,
so two runs write byte-identical output.

```sh
python3 draw.py            # redraw entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Sources

Reuters, AP, CNN, Al Jazeera, UN News, WSJ, The Guardian, and official
statements. Attributions are printed on the page itself.
