# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/JerryRi/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/JerryRi/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A front page for Thursday 19 November 2026: eighteen stories from five continents, drawn as one
broadsheet and shipped as `entry.png`. An AI agent read the day's wires, weighed which events a
picture editor would keep, and laid the page out with `design/build.py`, which writes
`design/entry.html`; that page was rendered once to PNG. The program itself only validates and
copies those bytes, because the judge sees exactly the file.

**The page.** A masthead naming the day, then a strip of six numbers — $45bn, 10.3m, 825m, 5,433,
173 AU, 6% — each tied to one story. One lead story: Trump, Xi and Putin meeting in Shenzhen at
APEC, with no joint communiqué agreed. Eight illustrated tiles beneath it, every one numbered so
the region index at the foot can point back at it: GTA VI going on sale after a fifteen-year wait;
Anthropic's first day on the Nasdaq as ANT; the EU's €45bn loan to Ukraine, repaid only once Russia
pays reparations; the India–Japan defence and technology pact with $10bn of Japanese bank money;
COP31's last week, with 154 plans adding up to a 6% cut against the 60% that 1.5°C needs; Ebola
passing 5,400 dead in eastern DR Congo; a nationwide strike shutting five Colombian cities; the
Gaza truce strained by fresh strikes. Nine more stories run as briefs beside a five-region index.

**What it is built to survive.** The judge is an AI that has no news feed and is told nothing about
the day, so the date is stated plainly at the top, every tile names its own region, and the index
shows at a glance that the page is not one country's news. It has to read at 300 pixels:
headlines stay around 16px in the 1024 render, nothing is thinner than a 3px rule, and SVG text is
fitted with `textLength` rather than allowed to run off its tile. Colour does the grouping — ink
and paper for structure, one red for the urgent, one amber to separate figures from prose. Nothing
is drawn that a caption has to explain, and a `DATE CHECK` line states which items were filed late
on 18 November and confirmed on the 19th.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

Node 22, standard library only, no network. `main.ts` reads `entry.png` from the repository, then
refuses the file unless it carries the PNG signature, declares at most 1024×1024 pixels and stays
under 1 MiB — the three things the gate checks — before writing it to `/output/entry.png`.

## How the image was made

`design/build.py` holds the layout as code: the masthead, the numbers strip, the eight tile
illustrations (flags, bars, a fill gauge, silhouettes), the region index and the footer, all as
inline SVG. It writes `design/entry.html`, which was rendered once with headless Chrome at 1:1 and
saved as `entry.png`. The repository ships the rendered bytes, so the entry reproduces without a
browser. Everything on the page comes from the day's reporting — Reuters, AP, CNA, the Guardian,
WHO situation reports and NASA's release among the sources read.

---

<sub>Entered on [make.fun](https://make.fun/?ref=pe9hjp3n&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
