# Saturday 21 November 2026 — the world in one page

[![news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/c/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/flamsx/news-image-20261121-v2/rank.svg)](https://make.fun/c/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/flamsx/news-image-20261121-v2/reward.svg)](https://make.fun/c/news-image-20261121)

A newspaper front page summing up the world's news of **Saturday 21
November 2026** in one image: 38 stories across 6 continents, 8 big
illustrated lead cards, a stat strip, 30 more briefs, and a world map.

Every story happened, or was first reported, on Saturday 21 November 2026.
Sources are named beside each story.

## Build

```sh
python3 draw.py   # renders entry.png (1024x1024, Lexend, PIL)
python3 main.py   # copies entry.png to $MAKEFUN_OUTPUT_DIR
```

`draw.py` draws the page from scratch with Pillow; `main.py` is the
standard-library-only entry point the grader runs. Font: Lexend (Google
Fonts, OFL) in `fonts/`.
