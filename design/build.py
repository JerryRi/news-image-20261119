"""Layout builder for the 19 Nov 2026 front page.

Writes design/entry.html, the single 1024x1024 broadsheet that is later rendered
once to entry.png. Everything here is geometry and copy: the grid, the numbers
strip, the eight tile illustrations, the dot map and the footer. Keeping the
page in one generated file means a change to copy or a tile cannot drift out of
sync with the map pins, which carry the same story numbers as the tiles.
"""

import math
from pathlib import Path

INK = "#12100b"
PAPER = "#f2ebdd"
RED = "#9e2018"
BRIGHT = "#c8342c"
AMBER = "#d97318"
CREAM = "#efe7d6"
MUTED = "#5f5647"
RULE = "#8d8271"
LAND = "#c9bda6"


def star(cx, cy, r, fill):
    """A five-point star as an SVG polygon (outer points every 72°, inner at 0.38r)."""
    pts = []
    for i in range(10):
        ang = math.radians(-90 + i * 36)
        rad = r if i % 2 == 0 else r * 0.382
        pts.append(f"{cx + rad * math.cos(ang):.1f},{cy + rad * math.sin(ang):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="{fill}"/>'


def flag_us(x, y, w, h):
    """Old Glory at tile size: thirteen stripes and a canton of white dots."""
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#b8332b"/>']
    sh = h / 13
    for i in range(1, 13, 2):
        out.append(f'<rect x="{x}" y="{y + i * sh}" width="{w}" height="{sh:.1f}" fill="#f2ebdd"/>')
    cw, ch = w * 0.42, sh * 7
    out.append(f'<rect x="{x}" y="{y}" width="{cw:.1f}" height="{ch:.1f}" fill="#2f4b7c"/>')
    rows, cols = 4, 5
    for r in range(rows):
        for c in range(cols):
            cx = x + cw * (c + 1) / (cols + 1)
            cy = y + ch * (r + 1) / (rows + 1)
            out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{h * 0.035:.1f}" fill="#f2ebdd"/>')
    return "".join(out)


def flag_cn(x, y, w, h):
    """Red field, one large star and four small ones turned towards it."""
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#c8342c"/>']
    out.append(star(x + w * 0.17, y + h * 0.29, h * 0.17, "#f5d76e"))
    for sx, sy in ((0.34, 0.10), (0.42, 0.20), (0.42, 0.38), (0.34, 0.48)):
        out.append(star(x + w * sx, y + h * sy, h * 0.062, "#f5d76e"))
    return "".join(out)


def flag_ru(x, y, w, h):
    """Three horizontal bands, white over blue over red."""
    out = []
    for i, col in enumerate(("#f2ebdd", "#2b3a63", "#c8342c")):
        out.append(f'<rect x="{x}" y="{y + i * h / 3:.1f}" width="{w}" height="{h / 3:.1f}" fill="{col}"/>')
    return "".join(out)


def tile_gta(w, h):
    """GTA VI: the numeral carries the tile, with the wait that preceded it."""
    return f'''<rect width="{w}" height="{h}" fill="{INK}"/>
<text x="16" y="24" font-family="Helvetica, Arial, sans-serif" font-size="8" font-weight="700"
      letter-spacing="2.4" fill="#c9bda6">GRAND THEFT AUTO</text>
<circle cx="{w - 42}" cy="30" r="17" fill="{BRIGHT}"/>
<text x="{w - 42}" y="34" text-anchor="middle" font-family="Helvetica, Arial, sans-serif"
      font-size="8.5" font-weight="700" letter-spacing=".4" fill="{PAPER}">15 YRS</text>
<text x="16" y="{h - 34}" font-family="Arial Black, Helvetica, sans-serif" font-size="86"
      fill="{PAPER}" textLength="86" lengthAdjust="spacingAndGlyphs">VI</text>
<rect x="118" y="{h - 74}" width="{w - 134}" height="34" fill="none" stroke="#3a352c" stroke-width="1"/>
<text x="126" y="{h - 61}" font-family="Helvetica, Arial, sans-serif" font-size="7.4"
      font-weight="700" letter-spacing="1.4" fill="#8d8271">PRE-ORDERED</text>
<text x="126" y="{h - 47}" font-family="Arial Black, Helvetica, sans-serif" font-size="14"
      fill="{PAPER}">10.3m copies</text>
<rect x="16" y="{h - 24}" width="{w - 32}" height="16" fill="{BRIGHT}"/>
<text x="{w/2}" y="{h - 12}" text-anchor="middle" font-family="Helvetica, Arial, sans-serif"
      font-size="8" font-weight="700" letter-spacing="1.8" fill="{PAPER}">OUT NOW · $79.99</text>'''


def tile_anthropic(w, h):
    """Bars rising to a red arrow: a first trading day, not a forecast."""
    return f'''<rect width="{w}" height="{h}" fill="{CREAM}"/>
<rect x="14" y="14" width="46" height="19" fill="{INK}"/>
<text x="37" y="27" text-anchor="middle" font-family="Helvetica, Arial, sans-serif"
      font-size="9.5" font-weight="700" letter-spacing="1.6" fill="{PAPER}">ANT</text>
<text x="{w-14}" y="27" text-anchor="end" font-family="Helvetica, Arial, sans-serif"
      font-size="8" font-weight="700" letter-spacing="1.4" fill="{MUTED}">NASDAQ</text>
<line x1="14" y1="{h-24}" x2="{w-14}" y2="{h-24}" stroke="{INK}" stroke-width="4"/>
<rect x="30" y="{h-45}" width="26" height="21" fill="#a99e88"/>
<rect x="70" y="{h-62}" width="26" height="38" fill="#a99e88"/>
<rect x="110" y="{h-88}" width="26" height="64" fill="{BRIGHT}"/>
<rect x="150" y="{h-110}" width="26" height="86" fill="{RED}"/>
<path d="M196 {h-30} L 202 34" stroke="{RED}" stroke-width="4"/>
<path d="M192 44 L 202 32 L 212 44" stroke="{RED}" stroke-width="4" fill="none"/>
<text x="112" y="{h-10}" text-anchor="middle" font-family="Helvetica, Arial, sans-serif"
      font-size="7.6" font-weight="700" letter-spacing="1.7" fill="{MUTED}">FIRST TRADING DAY</text>'''


def tile_eu(w, h):
    """Stars, then two blocks the size of the split: arms before budget."""
    stars = []
    for cx, cy in ((115, 15), (115, 29), (115, 43), (115, 57), (115, 71)):
        stars.append(f'<circle cx="{cx}" cy="{cy}" r="2.8" fill="#f5d76e"/>')
    for cx, cy in ((80, 15), (80, 29), (80, 43), (80, 57), (80, 71)):
        stars.append(f'<circle cx="{cx}" cy="{cy}" r="2.8" fill="#f5d76e"/>')
    for cx, cy in ((150, 15), (150, 29), (150, 43), (150, 57), (150, 71)):
        stars.append(f'<circle cx="{cx}" cy="{cy}" r="2.8" fill="#f5d76e"/>')
    return f'''<rect width="{w}" height="{h}" fill="#1a3a8f"/>
{"".join(stars)}
<rect x="16" y="{h-52}" width="86" height="36" fill="{PAPER}"/>
<text x="59" y="{h-26}" text-anchor="middle" font-family="Arial Black, Helvetica, sans-serif"
      font-size="18" fill="{INK}">&#8364;25B</text>
<rect x="126" y="{h-52}" width="86" height="36" fill="{AMBER}"/>
<text x="169" y="{h-26}" text-anchor="middle" font-family="Arial Black, Helvetica, sans-serif"
      font-size="18" fill="{INK}">&#8364;20B</text>
<text x="115" y="{h-6}" text-anchor="middle" font-family="Helvetica, Arial, sans-serif"
      font-size="7.6" font-weight="700" letter-spacing="1.7" fill="#cfd8ee">ARMS + BUDGET</text>'''


def tile_india(w, h):
    """Two flags over a black and an amber band: the pact and the money."""
    return f'''<rect width="{w}" height="{h}" fill="{CREAM}"/>
<rect x="14" y="12" width="84" height="54" fill="#f28c28"/>
<rect x="14" y="12" width="84" height="18" fill="#ffffff"/>
<rect x="14" y="30" width="84" height="18" fill="#128807"/>
<circle cx="42" cy="36" r="7.5" fill="none" stroke="#1a3a8f" stroke-width="1.8"/>
<circle cx="42" cy="36" r="2" fill="#1a3a8f"/>
<rect x="118" y="12" width="84" height="54" fill="#ffffff"/>
<circle cx="160" cy="39" r="14" fill="#bc002d"/>
<rect x="14" y="{h-68}" width="188" height="20" fill="{INK}"/>
<text x="108" y="{h-54}" text-anchor="middle" font-family="Arial Black, Helvetica, sans-serif"
      font-size="12" fill="{PAPER}" textLength="150" lengthAdjust="spacingAndGlyphs">$10 BILLION</text>
<rect x="14" y="{h-44}" width="188" height="20" fill="{AMBER}"/>
<text x="108" y="{h-30}" text-anchor="middle" font-family="Arial Black, Helvetica, sans-serif"
      font-size="12" fill="{INK}" textLength="132" lengthAdjust="spacingAndGlyphs">DEFENCE PACT</text>
<text x="110" y="{h-8}" text-anchor="middle" font-family="Helvetica, Arial, sans-serif"
      font-size="7.4" font-weight="700" letter-spacing="1.5" fill="{MUTED}">16TH ANNUAL SUMMIT</text>'''


def tile_cop31(w, h):
    """A fill gauge against the target: 6% pledged, 60% needed for 1.5C."""
    track_x, track_w = 16, w - 32
    y_bar = 62
    filled = track_w * 0.10  # 6 of the 60 points required
    ticks = "".join(
        f'<line x1="{track_x + track_w * f:.1f}" y1="{y_bar - 4}" x2="{track_x + track_w * f:.1f}" '
        f'y2="{y_bar + 20}" stroke="#a99e88" stroke-width="1"/>'
        for f in (0.25, 0.5, 0.75)
    )
    return f'''<rect width="{w}" height="{h}" fill="{CREAM}"/>
<text x="{track_x}" y="44" font-family="Arial Black, Helvetica, sans-serif" font-size="32"
      fill="{INK}" textLength="58" lengthAdjust="spacingAndGlyphs">6%</text>
<text x="84" y="26" font-family="Helvetica, Arial, sans-serif" font-size="7.6" font-weight="700"
      letter-spacing="1.4" fill="{MUTED}">PLEDGED</text>
<text x="84" y="38" font-family="Helvetica, Arial, sans-serif" font-size="7.6" font-weight="700"
      letter-spacing="1.4" fill="{MUTED}">BY 2035</text>
<text x="{w - track_x}" y="26" text-anchor="end" font-family="Helvetica, Arial, sans-serif"
      font-size="7.6" font-weight="700" letter-spacing="1.4" fill="{RED}">60% NEEDED</text>
<text x="{w - track_x}" y="38" text-anchor="end" font-family="Helvetica, Arial, sans-serif"
      font-size="7.6" font-weight="700" letter-spacing="1.4" fill="{RED}">FOR 1.5&#176;C</text>
<rect x="{track_x}" y="{y_bar}" width="{track_w}" height="18" fill="#ddd2bd"/>
<rect x="{track_x}" y="{y_bar}" width="{filled:.1f}" height="18" fill="{BRIGHT}"/>
{ticks}
<line x1="{track_x + track_w}" y1="{y_bar - 6}" x2="{track_x + track_w}" y2="{y_bar + 24}"
      stroke="{RED}" stroke-width="3"/>
<text x="{track_x}" y="{h - 30}" font-family="Helvetica, Arial, sans-serif" font-size="7.6"
      font-weight="700" letter-spacing="1.5" fill="{MUTED}">154 NATIONAL PLANS TALLIED</text>
<text x="{track_x}" y="{h - 12}" font-family="Helvetica, Arial, sans-serif" font-size="7.6"
      font-weight="700" letter-spacing="1.5" fill="{MUTED}">COP31'S LAST WEEK IN ANTALYA</text>'''


def tile_ebola(w, h):
    """Deaths climbing, and a cross that is not clipped by the tile edge."""
    return f'''<rect width="{w}" height="{h}" fill="{CREAM}"/>
<line x1="16" y1="{h-24}" x2="{w-16}" y2="{h-24}" stroke="{INK}" stroke-width="4"/>
<rect x="26" y="{h-48}" width="24" height="24" fill="#a99e88"/>
<rect x="66" y="{h-60}" width="24" height="36" fill="#a99e88"/>
<rect x="106" y="{h-88}" width="24" height="64" fill="{AMBER}"/>
<rect x="146" y="{h-118}" width="24" height="94" fill="{RED}"/>
<circle cx="{w - 40}" cy="46" r="25" fill="{PAPER}" stroke="{RED}" stroke-width="3"/>
<rect x="{w - 46}" y="32" width="12" height="28" fill="{RED}"/>
<rect x="{w - 54}" y="40" width="28" height="12" fill="{RED}"/>
<text x="112" y="{h-8}" text-anchor="middle" font-family="Helvetica, Arial, sans-serif"
      font-size="7.6" font-weight="700" letter-spacing="1.7" fill="{MUTED}">7 PROVINCES AFFECTED</text>'''


def tile_colombia(w, h):
    """Three figures with a red bar through them: a walkout, not a protest scene."""
    figs = []
    for cx in (60, 115, 170):
        figs.append(f'<circle cx="{cx}" cy="26" r="13" fill="{PAPER}"/>')
        figs.append(f'<rect x="{cx - 16}" y="40" width="32" height="60" rx="15" fill="{PAPER}"/>')
        figs.append(f'<line x1="{cx - 12}" y1="14" x2="{cx + 14}" y2="4" stroke="{BRIGHT}" stroke-width="7"/>')
    return f'''<rect width="{w}" height="{h}" fill="{INK}"/>
{"".join(figs)}
<rect x="24" y="{h-36}" width="{w - 48}" height="22" fill="{BRIGHT}"/>
<text x="{w/2}" y="{h - 22}" text-anchor="middle" font-family="Arial Black, Helvetica, sans-serif"
      font-size="12" fill="{PAPER}" textLength="164" lengthAdjust="spacingAndGlyphs">NATIONWIDE STRIKE</text>
<text x="{w/2}" y="{h - 6}" text-anchor="middle" font-family="Helvetica, Arial, sans-serif"
      font-size="7.4" font-weight="700" letter-spacing="1.5" fill="#8d8271">FIVE CITIES HALTED</text>'''


def tile_gaza(w, h):
    """A dove over a broken line: the truce, and the strikes that strain it."""
    return f'''<rect width="{w}" height="{h}" fill="{CREAM}"/>
<g transform="translate({w/2} 74)">
  <path d="M-74 8 q20 -30 54 -34 q-14 -18 6 -26 q10 -5 14 6 q26 -12 74 4 q-26 6 -40 20 q-14 14 -40 14 q-30 0 -44 22 q-14 -6 -24 -6z"
        fill="{INK}"/>
  <path d="M-30 -22 q22 -8 40 4" stroke="{INK}" stroke-width="4" fill="none"/>
  <path d="M-4 -40 l10 6" stroke="{INK}" stroke-width="4"/>
  <circle cx="12" cy="-42" r="3" fill="{INK}"/>
</g>
<path d="M36 {h-16} l16 -16 l14 13 l16 -17 l16 13 l14 -15 l16 13 l16 -17 l14 13"
      stroke="{RED}" stroke-width="4" fill="none"/>
<text x="{w/2}" y="{h-2}" text-anchor="middle" font-family="Helvetica, Arial, sans-serif"
      font-size="7.6" font-weight="700" letter-spacing="1.7" fill="{MUTED}">TRUCE UNDER STRAIN</text>'''


# --- region index -------------------------------------------------------
# The band under the tiles has to prove the page is not one country's news, at
# 250 pixels wide. A hand-drawn world map did not survive that size, so the
# breadth is stated instead: five regions, each listing the stories it holds.
REGIONS = [
    ("Asia-Pacific", "4 9", "India&#8211;Japan pact, Shenzhen summit"),
    ("Americas", "1 2 7", "GTA VI, Anthropic, Colombia, Venezuela"),
    ("Europe", "3 5", "EU loan, COP31 in Antalya"),
    ("Africa", "6", "Ebola in eastern DR Congo"),
    ("Middle East", "8", "Gaza truce under strain"),
]


def region_index():
    """Five rows: region, the tile numbers that sit there, and a short gloss."""
    rows = "".join(
        f"""<div class="reg">
          <div class="regname">{name}</div>
          <div class="regnums">{nums}</div>
          <div class="regtext">{text}</div>
        </div>"""
        for name, nums, text in REGIONS
    )
    return rows


NUMBERS = [
    ("$45", "bn", "EU loan offered to Ukraine"),
    ("10.3", "m", "GTA VI copies pre-ordered"),
    ("825", "m", "Shares sold in the ANT listing"),
    ("5,433", "", "Ebola deaths in DR Congo"),
    ("173", "AU", "Voyager 1, one light-day out"),
    ("6", "%", "Cut pledged by 2035 plans"),
]

TILES = [
    (1, "New York · Culture", "GTA VI GOES<br>ON SALE AT LAST",
     "Fifteen years after GTA V, Rockstar's sequel launches on PS5 and Xbox. 10.3m copies were pre-ordered.",
     tile_gta),
    (2, "New York · Markets", "ANTHROPIC OPENS<br>ON THE NASDAQ",
     "The AI lab trades as ANT after pricing 825m shares at $70-78, one of the largest listings ever.",
     tile_anthropic),
    (3, "Brussels · European Union", "EU OFFERS UKRAINE<br>A &#8364;45BN LOAN",
     "&#8364;25bn for arms, &#8364;20bn for the budget, repaid only once Russia pays reparations.",
     tile_eu),
    (4, "New Delhi · India", "INDIA AND JAPAN<br>BOLSTER DEFENCE",
     "Modi and Takaichi agree a joint defence project, AI and chip rules, and $10bn of Japanese bank money.",
     tile_india),
    (5, "Antalya · Climate", "COP31 ENTERS<br>ITS FINAL WEEK",
     "154 national plans add up to a 6% cut by 2035 against 2019, far short of the 60% needed for 1.5&#176;C.",
     tile_cop31),
    (6, "Eastern DR Congo · Africa", "EBOLA TOLL PASSES<br>5,400 DEAD",
     "The Bundibugyo outbreak is the second largest on record. MSF says the response is still losing ground.",
     tile_ebola),
    (7, "Bogot&#225; · Latin America", "UNIONS SHUT DOWN<br>FIVE CITIES",
     "A walkout against the government's rescue bill halts transport, schools and ports across Colombia.",
     tile_colombia),
    (8, "Gaza · Middle East", "TRUCE STRAINED<br>BY NEW STRIKES",
     "Israeli strikes continue as mediators push both sides towards a second phase of the ceasefire.",
     tile_gaza),
]

ALSO = [
    ("Voyager 1", "is a full light-day out &#8212; 25.9bn km, and its radio now takes a day to arrive."),
    ("Oil", "holds near $83 a barrel after a 3% slide the day before, as talks on Ukraine drag on."),
    ("Rohit Sharma", "retires from Test cricket, closing an 18-year international career."),
    ("Saudi Arabia", "is cleared to buy up to 48 F-35 fighters from the United States."),
    ("Dhaka", "asks India to hand back Sheikh Hasina; she says she will be home by December."),
    ("Hakeem Jeffries", "wins the Democratic nomination for House speaker."),
    ("Amazon", "pledges $7bn for renewable power in India by 2030."),
    ("Berlin", "gathers the coalition of the willing to keep Ukraine funded into 2027."),
    ("Caracas", "and Washington sign a training and intelligence accord, after the fall of Maduro."),
]


def build():
    nums = "".join(
        f'<div class="num"><b>{v}<em>{u}</em></b><span>{cap}</span></div>'
        for v, u, cap in NUMBERS
    )
    tiles = "".join(
        f'''<div class="tile">
      <div class="art"><svg width="230" height="150" viewBox="0 0 230 150" xmlns="http://www.w3.org/2000/svg">
        {fn(230, 150)}
      </svg></div>
      <div class="place"><span class="chip">{n}</span>{place}</div>
      <div class="lab">{lab}</div>
      <div class="det">{det}</div>
    </div>'''
        for n, place, lab, det, fn in TILES
    )
    also = "".join(f'<div><b>{name}</b> {text}</div>' for name, text in ALSO)

    lead_art = f'''<rect width="392" height="158" fill="{INK}"/>
<rect x="8" y="146" width="376" height="3" fill="#4f6d92"/>
{flag_us(8, 8, 108, 64)}
{flag_cn(142, 8, 108, 64)}
{flag_ru(276, 8, 108, 64)}
<text x="62" y="84" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="7"
      font-weight="700" letter-spacing="1.6" fill="#9a9182">UNITED STATES</text>
<text x="196" y="84" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="7"
      font-weight="700" letter-spacing="1.6" fill="#9a9182">CHINA</text>
<text x="330" y="84" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="7"
      font-weight="700" letter-spacing="1.6" fill="#9a9182">RUSSIA</text>
<rect x="8" y="92" width="376" height="34" fill="{PAPER}"/>
<text x="196" y="115" text-anchor="middle" font-family="Arial Black, Helvetica, sans-serif"
      font-size="20" fill="{INK}" textLength="150" lengthAdjust="spacingAndGlyphs">SHENZHEN</text>
<text x="196" y="140" text-anchor="middle" font-family="Helvetica, Arial, sans-serif"
      font-size="8" font-weight="700" letter-spacing="2.2" fill="#d8cebb">NO JOINT COMMUNIQUE AGREED</text>'''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>19 Nov 2026</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  html, body {{ width:1024px; height:1024px; overflow:hidden; background:{PAPER}; }}
  .page {{ width:1024px; height:1024px; background:{PAPER}; color:{INK};
    font-family:"Helvetica Neue", Helvetica, Arial, sans-serif;
    padding:16px 26px 0; display:flex; flex-direction:column; }}

  .mast {{ border-bottom:6px solid {INK}; padding-bottom:6px; flex:0 0 auto; }}
  .kick {{ font-size:12px; font-weight:700; letter-spacing:3.4px; color:{RED}; }}
  .mastrow {{ display:flex; align-items:flex-end; justify-content:space-between; }}
  .date {{ font-family:"Arial Black", Helvetica, sans-serif; font-size:50px; line-height:.94;
          letter-spacing:-1.2px; }}
  .date i {{ font-style:normal; font-size:21px; letter-spacing:0; }}
  .side {{ text-align:right; padding-bottom:5px; }}
  .side b {{ display:block; font-size:13px; letter-spacing:2.6px; }}
  .side span {{ display:block; font-size:10px; letter-spacing:1.3px; color:#6d6355; margin-top:2px; }}

  .nums {{ display:grid; grid-template-columns:repeat(6,1fr); border-bottom:3px solid {INK};
          flex:0 0 auto; }}
  .num {{ padding:7px 10px 6px 0; border-right:1px solid #c4b8a1; }}
  .num:last-child {{ border-right:0; }}
  .num b {{ display:block; font-family:"Arial Black", Helvetica, sans-serif; font-size:24px;
           letter-spacing:-.6px; line-height:1; }}
  .num b em {{ font-style:normal; font-size:13px; letter-spacing:0; color:{RED}; }}
  .num span {{ display:block; font-size:7.6px; font-weight:700; letter-spacing:.9px;
              text-transform:uppercase; color:{MUTED}; margin-top:3px; line-height:1.25; }}

  .lead {{ display:flex; gap:14px; padding:9px 0 10px; border-bottom:3px solid {INK}; flex:0 0 auto; }}
  .leadart {{ width:392px; flex:0 0 392px; }}
  .leadcopy {{ flex:1; display:flex; flex-direction:column; justify-content:center; }}
  .tag {{ align-self:flex-start; background:{INK}; color:{PAPER}; font-size:10px;
         font-weight:700; letter-spacing:1.9px; padding:3px 7px 2px; }}
  .hl {{ font-family:"Arial Black", Helvetica, sans-serif; font-size:29px; line-height:1.03;
        letter-spacing:-.6px; margin-top:6px; }}
  .sub {{ font-size:12.5px; line-height:1.28; margin-top:6px; color:#332c22; }}

  .grid {{ display:grid; grid-template-columns:repeat(4,1fr); gap:7px 13px;
          padding-top:8px; flex:1 1 auto; align-content:start; }}
  .tile {{ display:flex; flex-direction:column; border-top:3px solid {INK}; padding-top:4px; }}
  .art {{ height:150px; flex:0 0 150px; }}
  .place {{ font-size:8.4px; font-weight:700; letter-spacing:1.2px; color:{RED};
           text-transform:uppercase; margin-top:5px; }}
  .chip {{ display:inline-block; background:{INK}; color:{PAPER}; font-size:7.6px;
           padding:1px 3px; margin-right:4px; letter-spacing:0; }}
  .lab {{ font-family:"Arial Black", Helvetica, sans-serif; font-size:16px; line-height:1.05;
         letter-spacing:-.2px; margin-top:2px; }}
  .det {{ font-size:10px; line-height:1.17; margin-top:3px; color:#453d31; }}

  .band {{ display:flex; gap:14px; border-top:3px solid {INK}; padding-top:7px;
          flex:0 0 auto; margin-top:7px; }}
  .mapwrap {{ width:262px; flex:0 0 262px; }}
  .reg {{ display:flex; align-items:baseline; gap:6px; padding:2.5px 0;
          border-bottom:1px solid #d5c9b2; }}
  .reg:last-child {{ border-bottom:0; }}
  .regname {{ flex:0 0 74px; font-size:8.6px; font-weight:700; letter-spacing:1.1px;
              text-transform:uppercase; color:{INK}; }}
  .regnums {{ flex:0 0 auto; font-size:6.6px; font-weight:700; color:{PAPER};
              background:{RED}; padding:1px 3px; letter-spacing:.6px; }}
  .regtext {{ flex:1; font-size:8.4px; line-height:1.22; color:{MUTED}; }}
  .maplab {{ font-size:8.4px; font-weight:700; letter-spacing:1.2px; color:{RED};
            text-transform:uppercase; margin-bottom:4px; }}
  .also {{ flex:1; }}
  .also h3 {{ font-size:9px; font-weight:700; letter-spacing:1.6px; color:{RED};
             text-transform:uppercase; margin-bottom:4px; }}
  .also .items {{ display:grid; grid-template-columns:repeat(3,1fr); gap:0 12px; }}
  .also .items div {{ font-size:9.2px; line-height:1.3; color:{MUTED}; }}
  .also .items div b {{ color:{INK}; }}

  .foot {{ flex:0 0 auto; border-top:1px solid {RULE}; padding:5px 0 6px; margin-top:auto;
          display:flex; justify-content:space-between; align-items:baseline; gap:18px; }}
  .foot .a {{ font-size:8.6px; line-height:1.3; letter-spacing:.5px; color:{MUTED}; }}
  .foot .a b {{ color:{RED}; letter-spacing:1.2px; }}
  .foot .b {{ font-size:9px; letter-spacing:1.1px; color:{RED}; font-weight:700;
             white-space:nowrap; }}
</style>
</head>
<body>
<div class="page">

  <div class="mast">
    <div class="kick">ONE DAY · ONE IMAGE · THE WORLD'S NEWS</div>
    <div class="mastrow">
      <div class="date">19&nbsp;NOV<i>&nbsp;2026</i></div>
      <div class="side"><b>THURSDAY</b><span>18 STORIES · FIVE CONTINENTS</span></div>
    </div>
  </div>

  <div class="nums">{nums}</div>

  <div class="lead">
    <div class="leadart">
      <svg width="392" height="158" viewBox="0 0 392 158" xmlns="http://www.w3.org/2000/svg">
        {lead_art}
      </svg>
    </div>
    <div class="leadcopy">
      <div class="tag">LEAD STORY · ASIA-PACIFIC</div>
      <div class="hl">THREE NUCLEAR POWERS MEET IN SHENZHEN</div>
      <div class="sub">Trump, Xi and Putin hold their first trilateral summit on the sidelines of APEC.
        No joint communiqué is agreed; officials say the text is still being worked on.</div>
    </div>
  </div>

  <div class="grid">
    {tiles}
  </div>

  <div class="band">
    <div class="mapwrap">
      <div class="maplab">Where it happened</div>
      {region_index()}
    </div>
    <div class="also">
      <h3>Also on Thursday 19 November</h3>
      <div class="items">{also}</div>
    </div>
  </div>

  <div class="foot">
    <div class="a"><b>DATE CHECK</b> &#183; every item above was reported on Thursday 19 November 2026.
      The Shenzhen summit, the EU loan proposal and Voyager's milestone were filed late on Wednesday
      18 November and confirmed on the 19th; GTA VI went on sale at midnight local time around the world.</div>
    <div class="b">THE WORLD ON 19 NOVEMBER 2026</div>
  </div>
</div>
</body>
</html>
'''
    Path(__file__).with_name("entry.html").write_text(html)
    print(f"wrote entry.html {len(html)} bytes")


if __name__ == "__main__":
    build()
