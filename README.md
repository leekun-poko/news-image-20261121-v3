# News in one picture - 21 November 2026

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/leekun-poko/news-image-20261121-v3/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/leekun-poko/news-image-20261121-v3/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A single poster that sums up one day of world news:
Saturday 21 November 2026 (UTC).

## Contents of the poster

| # | Section | Story |
|---|---------|-------|
| 1 | Climate | COP31 talks in Antalya deadlocked over fossil fuels |
| 2 | Middle East | Iran struck an industrial site in Bahrain |
| 3 | Diplomacy | Zelenskyy open to Trump-Putin talks at the December G20 |
| 4 | Baltic | Russian cargo ship Sparta II hit by a drone |
| 5 | Security | FBI probe into a suspected crime database hack |
| 6 | Science | A claimed Riemann solution and an IPO stumble |
| 7 | Mexico | Cartel leader El Chapo Isidro captured in Sinaloa, 11 killed |
| 8 | Disaster | Magnitude 6.7 earthquake in central Peru |

## Running it

```sh
mkdir -p out
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

The poster lands in `out/entry.png`. With no environment
variable set, the program writes to `/output/entry.png`,
which is where the grading container expects it.

## Notes on the implementation

* Pure Python standard library; nothing to install.
* The page is a flat RGB canvas. Text uses a small bitmap
  typeface described row by row in the source.
* The PNG encoder is written out in the program itself and
  compresses at a fixed level, and the drawing code reads
  no clock and no random source, so repeated runs produce
  exactly the same bytes.
* Output size: 1024 x 1024 pixels, well under the 1 MiB cap.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
