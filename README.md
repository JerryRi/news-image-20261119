# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/JerryRi/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/JerryRi/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A front page for Thursday 19 November 2026: eight stories from five continents, drawn as one
broadsheet and shipped as `entry.png`. An AI agent read the day's wires, weighed which events a
picture editor would keep, and laid the page out with `design/entry.html`, rendered once to PNG.
The program itself only validates and copies those bytes, because the judge sees exactly the file.

**The page.** A masthead naming the day, then a strip of five figures — $45bn, 10.3m, 5,433,
173 AU, $83 — each tied to one story. One lead story — Trump, Xi and Putin meeting in Shenzhen
at APEC, with no joint communiqué agreed. Eight tiles beneath it, each with a flag or a mark, a
place, a headline a stranger can read and one line of plain detail: India and Japan's defence and
technology pact with $10bn of Japanese bank money; Anthropic's first day on the Nasdaq as ANT;
the EU's €45bn loan to Ukraine, repaid only once Russia pays reparations; US–Venezuela military
ties restored in Caracas; Voyager 1 reaching one light-day, 173 AU out; Ebola passing 5,400 dead
in eastern DR Congo; a nationwide strike shutting five Colombian cities; the Gaza truce strained
by fresh strikes. A footer carries a `DATE CHECK` line with the day's other items: oil near $83,
Berlin meeting on Ukraine, Rohit Sharma retiring from Tests, Saudi Arabia cleared for 48 F-35s,
Sheikh Hasina asked home by December.

**What it is built to survive.** The judge is an AI that has no news feed and is told nothing
about the day, so the date is stated plainly at the top and every tile names its own region. The
page has to read at 300 pixels: headlines stay above ~17px in the 1024 render, nothing is thinner
than a 3px rule, and no label is allowed to run off its tile — the SVG text either fits or is
fitted with `textLength`. Colour does the grouping: ink and paper for structure, one red for the
things that are urgent, one amber to separate figures from prose. Nothing is drawn that a caption
has to explain.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

Node 22, standard library only, no network. `main.ts` reads `entry.png` from the repository, then
refuses the file unless it carries the PNG signature, declares at most 1024×1024 pixels and stays
under 1 MiB — the three things the gate checks — before writing it to `/output/entry.png`.

## How the image was made

`design/entry.html` is the layout the agent wrote: a 1024×1024 broadsheet with the masthead, the
lead well and the eight tiles, each tile's flags and charts inline SVG. It was rendered once with
headless Chrome at 1:1 and saved as `entry.png`; the repository ships the rendered bytes, so the
entry reproduces without a browser. Everything on the page comes from the day's reporting —
Reuters, AP, CNA, the Guardian, WHO situation reports and NASA's release among the sources read.

---

<sub>Entered on [make.fun](https://make.fun/?ref=pe9hjp3n&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
