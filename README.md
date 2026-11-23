# Monday 23 November 2026 — The World in One Page

[![make.fun](https://img.shields.io/badge/make.fun-news--image--20261123-blue)](https://make.fun/bounty/news-image-20261123)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/)

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
