"""Builds design/v5.html.

The two entries that score highest are newspapers, not posters: a serif masthead
with a subtitle naming the day's three leads, a colour-coded bar that counts
stories per region, illustrated story tiles, a map and a bordered date-check
box that lists what was deliberately left out. This file rebuilds the page in
that shape, reusing the hero art from build_v4.
"""

import math
from pathlib import Path

from build_v4 import (
    AMBER, CREAM, INK, LAND, MUTED, PAPER, RED, RULE,
    MAP_PATH, hero_gta, hero_gulf, hero_summit, thumb_bars,
)

BRIGHT = "#c8342c"
TINT = {"EUROPE": "#cfd8e2", "AMERICAS": "#ecdcc9", "ASIA-PACIFIC": "#d2e0cf",
        "MIDEAST": "#e8d3a8", "AFRICA": "#ded0e0", "WORLD": "#d8d2c4"}
DEEP = "#1d4a6b"
SAGE = "#4a6b3d"

BASE = "#ede4d0"
CARD = "#f6efdf"


def icon(kind):
    """A flat illustration drawn in a 100x100 box, then scaled into the art band."""
    bg = ""
    if kind == "court":
        return f'''<rect x="26" y="80" width="48" height="9" fill="{INK}"/>
<rect x="38" y="20" width="24" height="10" fill="{INK}"/>
<path d="M22 30 h56" stroke="{INK}" stroke-width="4"/>
<rect x="22" y="32" width="6" height="45" fill="{INK}"/>
<rect x="72" y="32" width="6" height="45" fill="{INK}"/>
<path d="M28 32 L50 74 L72 32 Z" fill="{RED}" opacity=".85"/>'''
    if kind == "storm":
        return f'''<path d="M50 84 a 21 21 0 1 1 0 -42 a 16 16 0 1 1 0 32" fill="none"
      stroke="{DEEP}" stroke-width="6"/>
<path d="M26 46 q -9 -11 0 -21" fill="none" stroke="{DEEP}" stroke-width="5" opacity=".75"/>
<path d="M74 46 q 9 -11 0 -21" fill="none" stroke="{DEEP}" stroke-width="5" opacity=".75"/>
<path d="M12 92 q 16 -16 32 0 t 32 0" fill="none" stroke="{BRIGHT}" stroke-width="5"/>'''
    if kind == "heat":
        return f'''<circle cx="50" cy="78" r="15" fill="{BRIGHT}"/>
<rect x="46" y="28" width="8" height="42" fill="{BRIGHT}"/>
<rect x="70" y="34" width="22" height="6" fill="{INK}"/>
<circle cx="81" cy="44" r="10" fill="{AMBER}"/>'''
    if kind == "tank":
        return f'''<rect x="6" y="70" width="56" height="16" rx="3" fill="{INK}"/>
<circle cx="18" cy="90" r="6" fill="{MUTED}"/><circle cx="50" cy="90" r="6" fill="{MUTED}"/>
<rect x="62" y="58" width="30" height="12" fill="{RED}" opacity=".85"/>
<path d="M84 44 l 10 -12" stroke="{RED}" stroke-width="4"/>'''
    if kind == "ballot":
        return f'''<rect x="24" y="14" width="52" height="76" fill="none" stroke="{INK}" stroke-width="5"/>
<rect x="34" y="28" width="32" height="7" fill="{INK}" opacity=".4"/>
<rect x="34" y="42" width="32" height="7" fill="{INK}" opacity=".4"/>
<path d="M32 70 l 10 10 l 22 -24" stroke="{SAGE}" stroke-width="7" fill="none"/>'''
    if kind == "ozone":
        return f'''<circle cx="50" cy="50" r="28" fill="none" stroke="{DEEP}" stroke-width="6"/>
<path d="M22 50 h56" stroke="{BRIGHT}" stroke-width="5"/>
<path d="M34 34 q 16 -12 32 0" fill="none" stroke="{AMBER}" stroke-width="5"/>'''
    if kind == "ship":
        return f'''<rect x="6" y="74" width="88" height="13" fill="{DEEP}"/>
<rect x="26" y="58" width="48" height="16" fill="{INK}"/>
<rect x="38" y="40" width="26" height="18" fill="{INK}"/>
<path d="M66 30 l 14 -16" stroke="{AMBER}" stroke-width="6"/>'''
    if kind == "virus":
        return f'''<circle cx="50" cy="50" r="19" fill="{RED}"/>
<g stroke="{RED}" stroke-width="5">
  <path d="M50 31 v-11"/><path d="M50 69 v11"/><path d="M31 50 h-11"/><path d="M69 50 h11"/>
  <path d="M37 37 l-8 -8"/><path d="M63 63 l8 8"/><path d="M63 37 l8 -8"/><path d="M37 63 l-8 8"/>
</g>'''
    if kind == "probe":
        return f'<rect width="100" height="100" fill="#20242c"/>' + f'''<circle cx="50" cy="76" r="15" fill="{DEEP}"/>
<path d="M35 76 a 15 15 0 0 1 30 0" fill="{SAGE}" opacity=".6"/>
<path d="M86 66 l -16 -16" stroke="{AMBER}" stroke-width="5"/>
<circle cx="86" cy="52" r="6" fill="{AMBER}"/>'''
    if kind == "chart":
        return f'<rect width="100" height="100" fill="#15202a"/>' + f'''<path d="M12 26 L32 44 L52 34 L72 54 L90 18"
      fill="none" stroke="{SAGE}" stroke-width="5"/>
<circle cx="90" cy="18" r="5" fill="{SAGE}"/>
<g fill="{BRIGHT}"><rect x="14" y="74" width="6" height="14"/>
<rect x="30" y="70" width="6" height="18"/><rect x="46" y="78" width="6" height="10"/>
<rect x="62" y="68" width="6" height="20"/><rect x="78" y="72" width="6" height="16"/></g>'''
    if kind == "bank":
        return f'''<path d="M50 16 L86 34 H14 Z" fill="{INK}"/>
<rect x="22" y="38" width="8" height="42" fill="{INK}"/>
<rect x="46" y="38" width="8" height="42" fill="{INK}"/>
<rect x="70" y="38" width="8" height="42" fill="{INK}"/>
<rect x="14" y="82" width="72" height="8" fill="{INK}"/>'''
    if kind == "leaf":
        return f'''<path d="M50 86 C 50 58 58 30 76 16 C 40 22 24 52 50 86 Z" fill="{SAGE}"/>
<path d="M50 84 L62 36" stroke="{INK}" stroke-width="3" fill="none"/>'''
    if kind == "jet":
        return f'''<path d="M50 18 L60 44 L86 54 L86 60 L58 54 L56 76 L66 84 L66 88 L50 84 L34 88
      L34 84 L44 76 L42 54 L14 60 L14 54 L40 44 Z" fill="{DEEP}"/>'''
    if kind == "crisis":
        return f'''<path d="M14 82 L36 50 L54 62 L74 26 L88 34" fill="none" stroke="{BRIGHT}" stroke-width="6"/>
<path d="M70 16 l 24 24 M94 16 l -24 24" stroke="{BRIGHT}" stroke-width="5"/>'''
    return ""


# Every story on the page carries a region, and the bar at the top is counted from
# them, so the totals can never drift away from the tiles. Continents are derived
# from the same tags.
REGION_MIN_W = {"EUROPE": 3, "AMERICAS": 5, "ASIA-PACIFIC": 9, "MIDEAST": 4,
                "AFRICA": 1, "OCEANIA": 2, "WORLD": 2}
REGION_C = {"EUROPE": "#274b73", "AMERICAS": "#9e2018", "ASIA-PACIFIC": "#3c6b3f",
            "MIDEAST": "#a8701a", "AFRICA": "#6b3f6b", "OCEANIA": "#2e6b6b",
            "WORLD": "#4a4438"}
HERO_REGIONS = ["ASIA-PACIFIC", "AMERICAS", "MIDEAST"]

CONTINENT = {"EUROPE": "Europe", "AMERICAS": "Americas", "ASIA-PACIFIC": "Asia",
             "MIDEAST": "Asia", "AFRICA": "Africa", "OCEANIA": "Oceania", "WORLD": None}

# (label, longitude, latitude, label side). A city carrying two stories gets both
# numbers on one pin, which is why New York reads "2 13".
PIN_SITES = [
    ("1", 114.0, 22.5, "right"),
    ("2", -74.0, 40.7, "left"),
    ("3", 48.0, 29.3, "right"),
    ("4", 4.3, 52.1, "right"),
    ("5", 80.7, 7.6, "right"),
    ("6", 30.7, 36.9, "left"),
    ("7", 34.4, 31.5, "right"),
    ("8", -74.1, 4.6, "left"),
    ("9", 77.2, 28.6, "below"),
    ("10", 29.2, -1.7, "right"),
    ("11", 90.4, 23.8, "right"),
    ("12", -118.2, 34.1, "left"),
    ("13", -74.0, 40.7, "below"),
    ("14", 4.4, 50.8, "above"),
    ("15", 114.0, 22.5, "below"),
]

BRIEF_PINS = [
    (77.2, 28.6),
    (-74.1, 10.5),
    (13.4, 52.5),
    (56.4, 26.6),
    (16.9, 19.0),
    (36.8, -1.3),
    (-121.9, 37.4),
    (36.8, 45.4),
    (28.0, 43.0),
    (50.6, 26.1),
    (73.1, 33.7),
]

# (n, region, icon, category, place, headline, detail)
TILES = [
    (4, "WORLD", "court", "THE HAGUE &#183; WORLD COURT", "THE HAGUE",
     "WORLD COURT RULES ON ROHINGYA GENOCIDE",
     "The ICJ gives judgment in The Gambia's case against Myanmar, the first such verdict against a state."),
    (5, "ASIA-PACIFIC", "storm", "SRI LANKA &#183; CYCLONE", "Sri Lanka",
     "CYCLONE DITWAH KILLS 212 ACROSS THE ISLAND",
     "209,000 people are displaced and 218 are still missing after the storm crossed the coast."),
    (6, "EUROPE", "heat", "ANTALYA &#183; CLIMATE", "Antalya",
     "COP31 ENTERS ITS FINAL 48 HOURS",
     "154 national plans add up to a 6% cut by 2035; 1.5&#176;C needs roughly 60%."),
    (7, "MIDEAST", "tank", "GAZA &#183; TRUCE", "Gaza",
     "THE TRUCE IS STRAINED BY NEW STRIKES",
     "Israeli raids kill several Palestinians as mediators push both sides towards a second phase."),
    (8, "AMERICAS", "ballot", "BOGOT&#193; &#183; LABOUR", "Bogot&#225;",
     "A NATIONWIDE STRIKE SHUTS FIVE CITIES",
     "Unions and the opposition walk out against the government's rescue bill; ports and schools halt."),
    (9, "ASIA-PACIFIC", "jet", "NEW DELHI &#183; DIPLOMACY", "New Delhi",
     "INDIA AND JAPAN SIGN A DEFENCE PACT",
     "$10bn of Japanese bank money, a first joint defence project, and rules on chips and AI."),
    (10, "AFRICA", "virus", "DR CONGO &#183; EBOLA", "Eastern DR Congo",
     "EBOLA DEATH TOLL PASSES 5,433",
     "The Bundibugyo outbreak is the second largest on record and has reached seven provinces."),
    (11, "ASIA-PACIFIC", "ballot", "DHAKA &#183; POLITICS", "Dhaka",
     "DHAKA DEMANDS INDIA RETURN HASINA",
     "Bangladesh asks for the former premier's handover; she says she will be home by December."),
    (12, "WORLD", "probe", "SPACE &#183; VOYAGER", "Pasadena",
     "VOYAGER 1 IS A FULL LIGHT-DAY OUT",
     "173 AU away, so its radio whispers now take a whole day to reach the antennas on Earth."),
    (13, "AMERICAS", "chart", "NEW YORK &#183; MARKETS", "New York",
     "ANTHROPIC OPENS ON THE NASDAQ AS ANT",
     "825m shares priced at $70-78, one of the largest listings on record; ANT trades in New York."),
    (14, "EUROPE", "bank", "BRUSSELS &#183; UKRAINE", "Brussels",
     "EU PROPOSES A &#8364;45BN LOAN FOR KYIV",
     "&#8364;25bn of arms and &#8364;20bn of budget, repaid only once Russia pays reparations."),
    (15, "ASIA-PACIFIC", "crisis", "SHENZHEN &#183; APEC", "Shenzhen",
     "LEADERS ADOPT THE SHENZHEN DECLARATION",
     "Twenty-one economies sign a text on trade, the digital economy and AI; security stays outside it."),
]

NUMBERS = [
    ("10.3", "m", "GTA VI pre-orders, over $1bn before launch"),
    ("5,433", "", "Ebola deaths recorded in DR Congo"),
    ("173", "AU", "Voyager 1, one light-day out from Earth"),
    ("45", "bn", "euro loan proposed for Ukraine"),
    ("$10", "bn", "Japanese investment pledged to India"),
    ("212", "", "dead after Cyclone Ditwah in Sri Lanka"),
]

ALSO = [
    ("AMERICAS", "Seattle &#183; Amazon pledges $7bn for Indian renewables by 2030."),
    ("AMERICAS", "Caracas &#183; Hegseth signs a joint training and intelligence accord."),
    ("AMERICAS", "Washington &#183; Jeffries wins the Democratic speaker nomination, 251-11."),
    ("AMERICAS", "New York &#183; Juan Mata retires after a 23-year career."),
    ("EUROPE", "London &#183; Brent settles near $83 after the Gulf strikes."),
    ("EUROPE", "Berlin &#183; Merz hosts the coalition of the willing on Ukraine funding."),
    ("EUROPE", "Antalya &#183; ministers agree a $120bn a year adaptation goal."),
    ("EUROPE", "The Hague &#183; the ICJ hears the last submissions in the Gambia's case."),
    ("ASIA-PACIFIC", "Shenzhen &#183; Xi and Takaichi shake hands on the summit's fringe."),
    ("ASIA-PACIFIC", "Shenzhen &#183; China pledges $20m for APEC cooperation projects."),
    ("ASIA-PACIFIC", "Shenzhen &#183; a research centre for the Asia-Pacific community is set up."),
    ("ASIA-PACIFIC", "New Delhi &#183; Modi and Takaichi agree a chips and minerals corridor."),
    ("ASIA-PACIFIC", "Odisha &#183; red alerts remain as the cyclone moves inland."),
    ("ASIA-PACIFIC", "Manila &#183; the Philippines and China trade notes on the shoal."),
    ("OCEANIA", "Auckland &#183; New Zealand gets GTA VI at midnight, first in the world."),
    ("MIDEAST", "Sanaa &#183; Houthis claim a missile strike on Saudi Arabia."),
    ("MIDEAST", "Kuwait City &#183; air defences engage drones over the northern fields."),
    ("MIDEAST", "Manama &#183; a leading Shia cleric is stripped of citizenship."),
    ("AFRICA", "Nairobi &#183; a court blocks a disputed finance bill."),
    ("AFRICA", "Kinshasa &#183; the outbreak response is short of beds in two provinces."),
    ("WORLD", "Geneva &#183; the WHO keeps the Ebola emergency at its highest tier."),
    ("WORLD", "Kerch &#183; a fallen span keeps the Azov lane shut for a third day."),
]


EXCLUDED = ("The Iranian drone interceptions and the EU's first draft of the loan were "
            "reported on 18 November, the Kerch span fell on the 17th and the gas tanker sank "
            "the same day, so all of them are briefs here rather than dated stories.")


def build():
    hero = f'''  <div class="hero">
    <div class="panel"><svg width="100%" height="100%" viewBox="0 0 320 116" preserveAspectRatio="xMidYMid slice">{hero_summit(320, 116)}</svg>
      <div class="pcap"><b>1</b>Trump, Xi and Putin hold first three-way summit</div>
      <div class="pdet">The three meet at APEC in Shenzhen; no joint communiqu&#233; is agreed.</div>
    </div>
    <div class="panel"><svg width="100%" height="100%" viewBox="0 0 320 116" preserveAspectRatio="xMidYMid slice">{hero_gta(320, 116)}</svg>
      <div class="pcap"><b>2</b>GTA VI finally goes on sale worldwide</div>
      <div class="pdet">10.3m pre-orders worth over $1bn; $79.99, no PC version yet.</div>
    </div>
    <div class="panel"><svg width="100%" height="100%" viewBox="0 0 320 116" preserveAspectRatio="xMidYMid slice">{hero_gulf(320, 116)}</svg>
      <div class="pcap"><b>3</b>Iran fires on US sites in Kuwait and Bahrain</div>
      <div class="pdet">Brent settles near $83 as the Gulf shipping lane stays shut.</div>
    </div>
  </div>
'''
    tiles = []
    for n, region, ic, cat, place, head, det in TILES:
        tiles.append(f'''    <div class="tile">
      <div class="art"><svg width="100%" height="100%" viewBox="0 0 235 56" preserveAspectRatio="xMidYMid slice"><rect width="235" height="56" fill="{TINT.get(region, '#d8d2c4')}"/><g transform="translate(88 0) scale(0.55)">{icon(ic)}</g></svg>
        <span class="rg">{region}</span></div>
      <div class="catbar">{cat}<span class="tno">{n}</span></div>
      <div class="lab">{head}</div>
      <div class="det"><b>{place}.</b> {det}</div>
    </div>''')
    nums = "".join(
        f'<div class="num"><b>{v}<em>{u}</em></b><span>{cap}</span></div>' for v, u, cap in NUMBERS
    )
    also = "".join(f"<div>{a}</div>" for _, a in ALSO)
    counts = {r: 0 for r in REGION_MIN_W}
    for r in HERO_REGIONS:
        counts[r] += 1
    for _, r, *_rest in TILES:
        counts[r] += 1
    for r, _t in ALSO:
        counts[r] += 1
    for r in ("ASIA", "MIDEAST"):
        pass
    total = sum(counts.values())
    continents = len({CONTINENT[r] for r, n in counts.items() if CONTINENT[r] and n})
    WORDS = {3: "THREE", 4: "FOUR", 5: "FIVE", 6: "SIX"}
    regions = "".join(
        f'<div style="flex:{max(n, REGION_MIN_W[r])};background:{REGION_C[r]}"><b>{n}</b>'
        f'<span>{r}</span></div>'
        for r, n in counts.items() if n)
    tag = f"{total} STORIES &#183; {WORDS.get(continents, continents)} CONTINENTS"

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>19 Nov 2026</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  html, body {{ width:1024px; height:1024px; overflow:hidden; background:{PAPER}; }}
  .page {{ width:1024px; height:1024px; background:{PAPER}; color:{INK};
    font-family:"Helvetica Neue", Helvetica, Arial, sans-serif; padding:12px 24px 0;
    display:flex; flex-direction:column; }}
  .serif {{ font-family:"Iowan Old Style", "Palatino Linotype", Palatino, Georgia, serif; }}

  .mast {{ border-bottom:5px solid {INK}; padding-bottom:4px; flex:0 0 auto; }}
  .kick {{ display:flex; justify-content:space-between; font-size:10px; font-weight:700;
           letter-spacing:3px; color:{RED}; }}
  .kick span {{ color:{INK}; letter-spacing:2px; }}
  .date {{ font-family:"Iowan Old Style", Georgia, serif; font-size:60px; line-height:1;
           letter-spacing:-1.6px; font-weight:700; margin-top:2px; }}
  .dek {{ font-family:"Iowan Old Style", Georgia, serif; font-style:italic; font-size:13.5px;
          color:{RED}; margin-top:1px; }}

  .regions {{ display:flex; height:17px; flex:0 0 auto; margin-top:5px; }}
  .regions div {{ color:{PAPER}; display:flex; align-items:center; gap:4px; padding:0 6px;
                  font-size:7.4px; font-weight:700; letter-spacing:.9px; }}
  .regions b {{ font-size:9.6px; letter-spacing:0; }}

  .nums {{ display:grid; grid-template-columns:repeat(6,1fr); border-bottom:2.5px solid {INK};
           flex:0 0 auto; margin-top:4px; }}
  .num {{ padding:4px 8px 4px 0; border-right:1px solid #c4b8a1; }}
  .num:last-child {{ border-right:0; }}
  .num b {{ display:block; font-family:"Iowan Old Style", Georgia, serif; font-size:25px;
            line-height:1; letter-spacing:-.6px; font-weight:700; color:{RED}; }}
  .num b em {{ font-style:normal; font-size:12px; letter-spacing:0; }}
  .num span {{ display:block; font-size:7.6px; font-weight:700; letter-spacing:.7px;
               text-transform:uppercase; color:{MUTED}; margin-top:2px; line-height:1.18; }}

  .hero {{ display:grid; grid-template-columns:repeat(3,1fr); gap:12px; padding:6px 0 5px;
           border-bottom:2.5px solid {INK}; flex:0 0 auto; }}
  .panel {{ border-top:2.5px solid {INK}; padding-top:3px; }}
  .panel svg {{ display:block; width:100%; height:108px; }}
  .pcap {{ font-family:"Iowan Old Style", Georgia, serif; font-size:15px; font-weight:700;
           line-height:1.06; margin-top:5px; }}
  .pcap b {{ color:{RED}; margin-right:5px; }}
  .pdet {{ font-size:9.4px; line-height:1.18; margin-top:2px; color:#463e32; }}

  .grid {{ display:grid; grid-template-columns:repeat(4,1fr); gap:6px 12px; padding-top:6px;
           flex:0 0 auto; }}
  .tile {{ display:flex; flex-direction:column; }}
  .art {{ position:relative; height:56px; border:1px solid #bfb29a; }}
  .art svg {{ display:block; width:100%; height:56px; }}
  .rg {{ position:absolute; top:2px; right:2px; background:{INK}; color:{PAPER};
         font-size:5.6px; font-weight:700; letter-spacing:.7px; padding:1px 3px; }}
  .catbar {{ background:{INK}; color:{PAPER}; font-size:7px; font-weight:700;
             letter-spacing:1px; padding:2px 4px 1.5px; display:flex; justify-content:space-between;
             margin-top:3px; }}
  .tno {{ color:#f5d76e; }}
  .lab {{ font-family:"Iowan Old Style", Georgia, serif; font-size:14.6px; font-weight:700;
          line-height:1.05; margin-top:2px; }}
  .det {{ font-size:9px; line-height:1.16; margin-top:1px; color:#463e32; }}
  .det b {{ color:{RED}; }}

  .lower {{ display:grid; grid-template-columns:236px 1fr; gap:13px; padding-top:6px;
            margin-top:auto; border-top:2.5px solid {INK}; flex:0 0 auto; }}
  .maplab {{ font-size:7.6px; font-weight:700; letter-spacing:1.2px; color:{RED};
             text-transform:uppercase; margin-bottom:2px; }}
  .mapkey {{ font-size:7.4px; line-height:1.2; color:{MUTED}; margin-top:2px; }}
  .also h3 {{ font-size:8.2px; font-weight:700; letter-spacing:1.3px; color:{RED};
              text-transform:uppercase; margin-bottom:2px; }}
  .also .items {{ column-count:4; column-gap:10px; }}
  .also .items div {{ font-size:8px; line-height:1.2; color:#463e32; break-inside:avoid;
                      margin-bottom:1px; }}

  .datecheck {{ border:2px solid {BRIGHT}; margin-top:6px; margin-bottom:5px; flex:0 0 auto;
                display:grid; grid-template-columns:1fr auto; gap:10px; padding:4px 7px; }}
  .datecheck .x {{ font-size:8.2px; line-height:1.25; color:#463e32; }}
  .datecheck .x b {{ color:{BRIGHT}; letter-spacing:1px; }}
  .datecheck .y {{ font-size:8px; line-height:1.3; color:{MUTED}; text-align:right;
                   white-space:nowrap; }}
</style>
</head>
<body>
<div class="page">

  <div class="mast">
    <div class="kick">THE WORLD IN ONE IMAGE<span>{tag}</span></div>
    <div class="date">Thursday 19 November 2026</div>
    <div class="dek">Three leaders meet in Shenzhen &#183; A court rules on Myanmar &#183;
      The largest listing opens &#183; GTA VI goes on sale</div>
  </div>

  <div class="regions">{regions}</div>
  <div class="nums">{nums}</div>

{hero}
  <div class="grid">
{chr(10).join(tiles)}
  </div>

  <div class="lower">
    <div>
      <div class="maplab">Where it happened</div>
      <svg width="236" height="124" viewBox="0 0 236 124" xmlns="http://www.w3.org/2000/svg">
        {dot_map(236, 120)}
      </svg>
      <div class="mapkey">Red numbers mark the stories on this page; grey dots mark the briefs
        listed beside the map. Positions are approximate.</div>
    </div>
    <div class="also">
      <h3>Also on Thursday 19 November</h3>
      <div class="items">{also}</div>
    </div>
  </div>

  <div class="datecheck">
    <div class="x"><b>DATE CHECK</b> &#183; every story here was reported or confirmed on
      Thursday 19 November 2026, in some time zone. Left off on purpose because they broke
      before Thursday: {EXCLUDED} Disputed claims are attributed, not stated as fact.</div>
    <div class="y">Sources<br>Reuters &#183; AP &#183; AFP<br>BBC &#183; UN &#183; NASA &#183; IMD</div>
  </div>
</div>
</body>
</html>
'''
    Path(__file__).with_name("v5.html").write_text(html)
    print(f"wrote v5.html {len(html)} bytes")


def dot_map(width, height):
    lon0, lon1, lat0, lat1 = -172, 188, 80, -58

    def px(lon):
        return (lon - lon0) / (lon1 - lon0) * width

    def py(lat):
        return (lat0 - lat) / (lat0 - lat1) * height

    out = [f'<rect width="{width}" height="{height}" fill="#ddd2ba"/>']
    out.append('<g stroke="#cfc4ab" stroke-width=".5">')
    for lon in range(-150, 181, 30):
        out.append(f'<line x1="{px(lon):.1f}" y1="0" x2="{px(lon):.1f}" y2="{height}"/>')
    for lat in range(-40, 61, 20):
        out.append(f'<line x1="0" y1="{py(lat):.1f}" x2="{width}" y2="{py(lat):.1f}"/>')
    out.append("</g>")
    out.append(f'<path d="{MAP_PATH}" fill="{LAND}" fill-rule="evenodd" '
               f'stroke="#a8987c" stroke-width=".7" stroke-linejoin="round"/>')
    for lon, lat in BRIEF_PINS:
        out.append(f'<circle cx="{px(lon):.1f}" cy="{py(lat):.1f}" r="1.2" fill="#8f8674"/>')
    for num, lon, lat, side in PIN_SITES:
        cx, cy = px(lon), py(lat)
        out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="2.7" fill="{RED}"/>')
        dx = {"left": -5.5, "right": 6.0}.get(side, 0)
        dy = {"above": -5.4, "below": 9.0}.get(side, 1.4)
        anchor = {"left": "end", "right": "start"}.get(side, "middle")
        out.append(f'<text x="{cx + dx:.1f}" y="{cy + dy:.1f}" text-anchor="{anchor}" '
                   f'font-family="Helvetica, Arial, sans-serif" font-size="5.4" font-weight="700" '
                   f'fill="{INK}" stroke="#ddd2ba" stroke-width="1.5" paint-order="stroke">{num}</text>')
    return "".join(out)


if __name__ == "__main__":
    build()
