"""Builds design/v4.html: the dense front page, the shape the top entries take.

Concentrates illustration in one three-panel hero band, then a 4x4 grid of text
tiles that carries twice as many stories at the same type size, a numbers strip,
a pinned world map and an "also on" column. Everything is inline SVG so the page
renders at 1:1 with no fonts to load and no network.
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
    pts = []
    for i in range(10):
        ang = math.radians(-90 + i * 36)
        rad = r if i % 2 == 0 else r * 0.382
        pts.append(f"{cx + rad * math.cos(ang):.1f},{cy + rad * math.sin(ang):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="{fill}"/>'


def flag_us(x, y, w, h):
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#b8332b"/>']
    sh = h / 13
    for i in range(1, 13, 2):
        out.append(f'<rect x="{x}" y="{y + i * sh}" width="{w}" height="{sh:.1f}" fill="#f2ebdd"/>')
    cw, ch = w * 0.44, sh * 7
    out.append(f'<rect x="{x}" y="{y}" width="{cw:.1f}" height="{ch:.1f}" fill="#2f4b7c"/>')
    for r in range(4):
        for c in range(5):
            cx = x + cw * (c + 1) / 6
            cy = y + ch * (r + 1) / 5
            out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{h * 0.035:.1f}" fill="#f2ebdd"/>')
    return "".join(out)


def flag_cn(x, y, w, h):
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#c8342c"/>']
    out.append(star(x + w * 0.18, y + h * 0.30, h * 0.18, "#f5d76e"))
    for sx, sy in ((0.34, 0.10), (0.43, 0.21), (0.43, 0.40), (0.34, 0.50)):
        out.append(star(x + w * sx, y + h * sy, h * 0.065, "#f5d76e"))
    return "".join(out)


def flag_ru(x, y, w, h):
    cols = ("#f2ebdd", "#2b3a63", "#c8342c")
    return "".join(
        f'<rect x="{x}" y="{y + i * h / 3:.1f}" width="{w}" height="{h / 3 + .4:.1f}" fill="{c}"/>'
        for i, c in enumerate(cols)
    )


def hero_summit(w, h):
    """Three flags around a rostrum: the first trilateral seating of the day."""
    return f'''<rect width="{w}" height="{h}" fill="{INK}"/>
<text x="12" y="17" font-family="Helvetica, Arial, sans-serif" font-size="7.6" font-weight="700"
      letter-spacing="2.2" fill="#c9bda6">SHENZHEN &#183; APEC</text>
{flag_us(12, 24, 80, 48)}
{flag_cn(104, 24, 80, 48)}
{flag_ru(196, 24, 80, 48)}
<text x="52" y="84" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="6.2"
      font-weight="700" letter-spacing="1.3" fill="#8d8271">US</text>
<text x="144" y="84" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="6.2"
      font-weight="700" letter-spacing="1.3" fill="#8d8271">CHINA</text>
<text x="236" y="84" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="6.2"
      font-weight="700" letter-spacing="1.3" fill="#8d8271">RUSSIA</text>
<path d="M96 92 L144 70 L192 92" fill="none" stroke="{AMBER}" stroke-width="1.4" stroke-dasharray="3 3"/>
<circle cx="144" cy="70" r="4" fill="none" stroke="{AMBER}" stroke-width="1.6"/>
<circle cx="144" cy="70" r="1.7" fill="{AMBER}"/>
<rect x="0" y="{h - 22}" width="{w}" height="22" fill="{PAPER}"/>
<text x="{w/2}" y="{h - 6}" text-anchor="middle" font-family="Arial Black, Helvetica, sans-serif"
      font-size="15" fill="{INK}" textLength="176" lengthAdjust="spacingAndGlyphs">SHENZHEN SUMMIT</text>'''


def hero_gta(w, h):
    """A disc on a dashboard: the launch, and the number that got there."""
    return f'''<rect width="{w}" height="{h}" fill="#161513"/>
<text x="12" y="17" font-family="Helvetica, Arial, sans-serif" font-size="7.6" font-weight="700"
      letter-spacing="2.2" fill="#c9bda6">WORLDWIDE &#183; ON SALE</text>
<circle cx="96" cy="60" r="30" fill="none" stroke="{BRIGHT}" stroke-width="2.2"/>
<circle cx="96" cy="60" r="30" fill="{BRIGHT}" opacity=".12"/>
<text x="96" y="57" text-anchor="middle" font-family="Arial Black, Helvetica, sans-serif"
      font-size="24" fill="{PAPER}">VI</text>
<text x="96" y="72" text-anchor="middle" font-family="Helvetica, Arial, sans-serif"
      font-size="6.4" font-weight="700" letter-spacing="1.4" fill="{AMBER}">2013 &#8594; 2026</text>
<g font-family="Helvetica, Arial, sans-serif" font-size="6.4" font-weight="700"
   letter-spacing="1.2" fill="#8d8271">
  <text x="140" y="40">PRE-ORDERS</text>
  <text x="140" y="62">PRICE</text>
  <text x="140" y="84">WAIT</text>
</g>
<g font-family="Arial Black, Helvetica, sans-serif" font-size="12" fill="{PAPER}">
  <text x="198" y="41">10.3m</text>
  <text x="198" y="63">$79.99</text>
  <text x="198" y="85">15 yrs</text>
</g>
<rect x="0" y="{h - 22}" width="{w}" height="22" fill="{BRIGHT}"/>
<text x="{w/2}" y="{h - 6}" text-anchor="middle" font-family="Helvetica, Arial, sans-serif"
      font-size="9" font-weight="700" letter-spacing="1.8" fill="{PAPER}">OUT NOW ON PS5 AND XBOX</text>'''


def hero_gulf(w, h):
    """Strike arcs over the strait, and the two neighbours that were hit."""
    return f'''<rect width="{w}" height="{h}" fill="{INK}"/>
<text x="12" y="17" font-family="Helvetica, Arial, sans-serif" font-size="7.6" font-weight="700"
      letter-spacing="2.2" fill="#c9bda6">GULF &#183; HORMUZ</text>
<path d="M0 {h - 22} L 46 {h - 46} L 92 {h - 34} L 140 {h - 58} L 186 {h - 40} L 232 {h - 64}
         L 280 {h - 46} L {w} {h - 52} L {w} {h} L 0 {h} Z" fill="#2a2621"/>
<g stroke="{AMBER}" stroke-width="1.6" opacity=".85" fill="none">
  <path d="M78 {h - 50} q 10 -18 26 -22"/>
  <path d="M78 {h - 50} q -4 -20 8 -30"/>
  <path d="M162 {h - 62} q 12 -16 28 -18"/>
  <path d="M162 {h - 62} q 0 -20 12 -28"/>
  <circle cx="104" cy="{h - 72}" r="2.2" fill="{BRIGHT}" stroke="none"/>
  <circle cx="190" cy="{h - 80}" r="2.2" fill="{BRIGHT}" stroke="none"/>
</g>
<g font-family="Helvetica, Arial, sans-serif" font-size="6.4" font-weight="700"
   letter-spacing="1.3" fill="{PAPER}">
  <text x="96" y="{h - 30}">KUWAIT</text>
  <text x="184" y="{h - 42}">BAHRAIN</text>
</g>
<rect x="0" y="{h - 22}" width="{w}" height="22" fill="{BRIGHT}"/>
<text x="{w/2}" y="{h - 6}" text-anchor="middle" font-family="Arial Black, Helvetica, sans-serif"
      font-size="10.4" fill="{PAPER}" textLength="242" lengthAdjust="spacingAndGlyphs">IRAN FIRES ON GULF NEIGHBOURS</text>'''


def thumb_bars(w, h, vals, hi):
    """Small bar chart inside a text tile: the shape of a figure, not a decoration."""
    bw = (w - 22) / len(vals)
    out = []
    for i, v in enumerate(vals):
        hh = (h - 12) * v
        out.append(f'<rect x="{8 + i * bw:.1f}" y="{h - 6 - hh:.1f}" width="{bw - 3:.1f}" '
                   f'height="{hh:.1f}" fill="{BRIGHT if i == hi else "#a99e88"}"/>')
    out.append(f'<line x1="6" y1="{h - 4}" x2="{w - 4}" y2="{h - 4}" stroke="{INK}" stroke-width="2"/>')
    return "".join(out)


MAP_PATH = (Path(__file__).with_name("map_path.txt")).read_text().strip()

# (story number, longitude, latitude, label side). Two hero stories share a city
# with a tile, so those are drawn once, at the hero's number.
PIN_SITES = [
    (1, 114.0, 22.5, "right"),    # Shenzhen, the trilateral
    (2, -74.0, 40.7, "left"),     # New York, GTA VI and the Nasdaq listing
    (3, 48.0, 29.3, "right"),     # Kuwait, the Gulf strikes
    (5, 4.4, 50.8, "above"),      # Brussels, the EU loan
    (6, -66.9, 10.5, "left"),     # Caracas, the US accord
    (7, -118.2, 34.1, "left"),    # Pasadena, Voyager's flight team
    (8, 29.2, -1.7, "right"),     # eastern DR Congo, the outbreak
    (9, -74.1, 4.6, "left"),      # Bogota, the strike
    (10, 34.4, 31.5, "right"),    # Gaza, the truce
    (11, 77.2, 28.6, "below"),    # New Delhi, India and Japan
    (12, 30.7, 36.9, "left"),     # Antalya, COP31
    (13, 90.4, 23.8, "right"),    # Dhaka, the handover demand
    (14, 46.7, 24.6, "right"),    # Riyadh, the F-35s
    (15, -77.0, 38.9, "left"),    # Washington, the speaker nod
    (17, 72.9, 19.1, "left"),     # Mumbai, Rohit's home board
    (18, 13.4, 52.5, "above"),    # Berlin, the coalition meeting
    (19, 80.7, 7.6, "right"),     # Sri Lanka, cyclone Ditwah
]

# Short briefs on the map are grey: they carry no number because they have no tile.
BRIEF_PINS = [
    (56.4, 26.6),   # Hormuz
    (16.9, 19.0),   # Myanmar, ICJ ruling
    (13.2, -8.8),   # Vienna, OPEC+
    (35.0, 45.4),   # the Kerch strait / Azov
    (28.0, 43.0),   # Bulgaria, Black Sea
    (35.3, 31.9),   # the West Bank
    (-121.9, 37.4), # Santa Clara, Nvidia
    (151.2, -33.9), # Sydney, the ODI series
    (50.6, 26.1),   # Bahrain, the cleric's family
    (36.8, -1.3),   # Nairobi
    (-77.0, 38.9),  # Washington, the Senate
    (73.1, 33.7),   # Pakistan
]


def dot_map(width, height):
    """Panel-filling map: projected coastlines, graticule, numbered story pins."""
    lon0, lon1, lat0, lat1 = -172, 188, 80, -58

    def px(lon):
        return (lon - lon0) / (lon1 - lon0) * width

    def py(lat):
        return (lat0 - lat) / (lat0 - lat1) * height

    out = [f'<rect width="{width}" height="{height}" fill="#e4dac4"/>']
    out.append('<g stroke="#cfc4ab" stroke-width=".5">')
    for lon in range(-150, 181, 30):
        out.append(f'<line x1="{px(lon):.1f}" y1="0" x2="{px(lon):.1f}" y2="{height}"/>')
    for lat in range(-40, 61, 20):
        out.append(f'<line x1="0" y1="{py(lat):.1f}" x2="{width}" y2="{py(lat):.1f}"/>')
    out.append("</g>")
    out.append(f'<path d="{MAP_PATH}" fill="{LAND}" fill-rule="evenodd" '
               f'stroke="#ab9c81" stroke-width=".7" stroke-linejoin="round"/>')
    for lon, lat in BRIEF_PINS:
        out.append(f'<circle cx="{px(lon):.1f}" cy="{py(lat):.1f}" r="1.4" fill="#9a917f"/>')
    for num, lon, lat, side in PIN_SITES:
        cx, cy = px(lon), py(lat)
        out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="2.9" fill="{RED}"/>')
        dx = {"left": -5.5, "right": 5.5}.get(side, 0)
        dy = {"above": -5, "below": 8}.get(side, 1.4)
        anchor = {"left": "end", "right": "start"}.get(side, "middle")
        out.append(f'<text x="{cx + dx:.1f}" y="{cy + dy:.1f}" text-anchor="{anchor}" '
                   f'font-family="Helvetica, Arial, sans-serif" font-size="5.8" font-weight="700" '
                   f'fill="{INK}" stroke="#e4dac4" stroke-width="1.6" paint-order="stroke">{num}</text>')
    return "".join(out)


# (number, category bar, place, headline, detail)
TILES = [
    (4, "MARKETS &#183; AI", "New York",
     "ANTHROPIC OPENS ON THE NASDAQ AS ANT",
     "825m shares priced at $70-78, one of the largest listings ever. Financial markets, not Silicon Valley, set the price."),
    (5, "EUROPE &#183; UKRAINE", "Brussels",
     "EU PROPOSES A &#8364;45BN LOAN FOR KYIV",
     "&#8364;25bn of arms and &#8364;20bn of budget, repaid only once Russia pays reparations. The bloc borrows so Kyiv need not."),
    (6, "AMERICAS &#183; DEFENCE", "Caracas",
     "US AND VENEZUELA RESUME MILITARY TIES",
     "Hegseth signs an accord on joint training and intelligence sharing, ten months after Maduro was taken."),
    (7, "SPACE &#183; SCIENCE", "Pasadena",
     "VOYAGER 1 IS A FULL LIGHT-DAY OUT",
     "The probe is 173 AU away, so its radio whispers now take a whole day to reach the antennas on Earth."),
    (8, "AFRICA &#183; HEALTH", "Eastern DR Congo",
     "EBOLA DEATH TOLL PASSES 5,433",
     "The Bundibugyo outbreak is the second largest on record, across seven provinces. Medics on the ground say the response is losing ground."),
    (9, "LATIN AMERICA &#183; LABOUR", "Bogot&#225;",
     "A NATIONWIDE STRIKE SHUTS FIVE CITIES",
     "Unions and the opposition walk out against the government's rescue bill; transport, schools and ports halt."),
    (10, "MIDDLE EAST &#183; GAZA", "Gaza",
     "THE TRUCE IS STRAINED BY NEW STRIKES",
     "Israeli raids kill several Palestinians as mediators push both sides towards a second phase of the deal."),
    (11, "ASIA &#183; DIPLOMACY", "New Delhi",
     "INDIA AND JAPAN SIGN A DEFENCE PACT",
     "$10bn of Japanese bank money, a first joint defence project, and new rules on chips, minerals and AI."),
    (12, "CLIMATE &#183; COP31", "Antalya",
     "CLIMATE TALKS ENTER THEIR LAST WEEK",
     "154 national plans add up to a 6% cut by 2035 against 2019; holding 1.5&#176;C needs about 60%."),
    (13, "ASIA &#183; RIGHTS", "Dhaka",
     "DHAKA DEMANDS INDIA RETURN HASINA",
     "Bangladesh asks for the former premier's handover; she says she will be home by December."),
    (14, "MIDDLE EAST &#183; ARMS", "Riyadh",
     "SAUDI ARABIA CLEARED FOR 48 F-35s",
     "A $24bn package advances after Congress declines to block it, the first such sale to Riyadh."),
    (15, "WORLD &#183; JUSTICE", "The Hague",
     "THE ICJ RULES ON MYANMAR'S GENOCIDE",
     "The Gambia's case reaches judgment; the court has never before held a state responsible for genocide."),
    (16, "INDIA &#183; BUSINESS", "India",
     "AMAZON PUTS $7BN INTO INDIAN RENEWABLES",
     "The pledge runs to 2030 and is among the largest clean-power commitments by a foreign firm there."),
    (17, "SPORT &#183; CRICKET", "New Delhi",
     "ROHIT SHARMA QUITS TEST CRICKET",
     "The opener ends an 18-year international career after a home series whitewash."),
    (18, "EUROPE &#183; ENERGY", "Berlin",
     "THE COALITION OF THE WILLING MEETS",
     "Merz gathers leaders to keep Ukraine funded into 2027 and to ring-fence the loan."),
    (19, "ASIA &#183; WEATHER", "Sri Lanka",
     "CYCLONE DITWAH KILLS 212",
     "209,000 people displaced and 218 still missing after the storm crossed the eastern coast."),
]

NUMBERS = [
    ("$45", "bn", "EU loan proposed for Ukraine"),
    ("10.3", "m", "GTA VI copies pre-ordered"),
    ("825", "m", "Anthropic shares sold as ANT"),
    ("5,433", "", "Ebola deaths in DR Congo"),
    ("173", "AU", "Voyager 1, one light-day out"),
    ("$83", "", "A barrel of US crude"),
]

ALSO = [
    "Iran fires on US sites in Kuwait and Bahrain; Brent settles near $83.",
    "The ICJ rules on Myanmar's Rohingya genocide case.",
    "A fallen Kerch span blocks the Azov lane, two days on.",
    "An LPG tanker explodes by Bulgaria's Black Sea coast.",
    "Australia sanctions settlers over the West Bank.",
    "Nvidia warns of a December pay pause as its board weighs a return.",
    "England take an ODI series in Australia on Duckett's 133.",
    "Bahrain expels a top cleric's family after a citizenship ruling.",
    "OPEC+ holds output as Brent slips below $83.",
    "Kenya's Ruto marks a fourth year of state capture claims.",
    "A Nairobi court blocks a disputed finance bill.",
    "The US Senate moves toward a spending deal to avoid a shutdown.",
    "Pakistan's Khan is freed after his ninth bail petition.",
    "Mata retires after 20 years in the professional game.",
]

def build():
    hero = f'''  <div class="hero">
    <div class="panel"><svg width="100%" height="100%" viewBox="0 0 320 116" preserveAspectRatio="xMidYMid slice">{hero_summit(320, 116)}</svg>
      <div class="pcap"><b>1</b> TRUMP, XI AND PUTIN MEET IN SHENZHEN</div>
      <div class="pdet">First trilateral of the three at APEC; no joint communiqué is agreed.</div>
    </div>
    <div class="panel"><svg width="100%" height="100%" viewBox="0 0 320 116" preserveAspectRatio="xMidYMid slice">{hero_gta(320, 116)}</svg>
      <div class="pcap"><b>2</b> GTA VI ARRIVES, FIFTEEN YEARS ON</div>
      <div class="pdet">Midnight launches worldwide; 10.3m pre-orders at $79.99.</div>
    </div>
    <div class="panel"><svg width="100%" height="100%" viewBox="0 0 320 116" preserveAspectRatio="xMidYMid slice">{hero_gulf(320, 116)}</svg>
      <div class="pcap"><b>3</b> IRAN STRIKES US SITES IN THE GULF</div>
      <div class="pdet">Kuwait and Bahrain report hits; Brent settles near $83.</div>
    </div>
  </div>
'''
    tiles = []
    for n, cat, place, head, det in TILES:
        tiles.append(f'''    <div class="tile">
      <div class="catbar">{cat}<span class="tno">{n}</span></div>
      <div class="lab">{head}</div>
      <div class="det"><b>{place}.</b> {det}</div>
    </div>''')
    nums = "".join(
        f'<div class="num"><b>{v}<em>{u}</em></b><span>{cap}</span></div>' for v, u, cap in NUMBERS
    )
    also = "".join(f'<div>&#183; {a}</div>' for a in ALSO)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>19 Nov 2026</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  html, body {{ width:1024px; height:1024px; overflow:hidden; background:{PAPER}; }}
  .page {{ width:1024px; height:1024px; background:{PAPER}; color:{INK};
    font-family:"Helvetica Neue", Helvetica, Arial, sans-serif; padding:14px 26px 0;
    display:flex; flex-direction:column; }}

  .mast {{ border-bottom:6px solid {INK}; padding-bottom:5px; flex:0 0 auto; }}
  .kick {{ font-size:11.5px; font-weight:700; letter-spacing:3.2px; color:{RED}; }}
  .mastrow {{ display:flex; align-items:flex-end; justify-content:space-between; }}
  .date {{ font-family:"Arial Black", Helvetica, sans-serif; font-size:56px; line-height:.94;
          letter-spacing:-1.2px; }}
  .date i {{ font-style:normal; font-size:20px; letter-spacing:0; }}
  .side {{ text-align:right; padding-bottom:4px; }}
  .side b {{ display:block; font-size:12.5px; letter-spacing:2.4px; }}
  .side span {{ display:block; font-size:9.6px; letter-spacing:1.2px; color:#6d6355; margin-top:2px; }}

  .nums {{ display:grid; grid-template-columns:repeat(6,1fr); border-bottom:3px solid {INK};
          flex:0 0 auto; }}
  .num {{ padding:5px 9px 5px 0; border-right:1px solid #c4b8a1; }}
  .num:last-child {{ border-right:0; }}
  .num b {{ display:block; font-family:"Arial Black", Helvetica, sans-serif; font-size:21px;
           letter-spacing:-.5px; line-height:1; }}
  .num b em {{ font-style:normal; font-size:11px; letter-spacing:0; color:{RED}; }}
  .num span {{ display:block; font-size:7.6px; font-weight:700; letter-spacing:.8px;
              text-transform:uppercase; color:{MUTED}; margin-top:2px; line-height:1.2; }}

  .hero {{ display:grid; grid-template-columns:repeat(3,1fr); gap:12px; padding:8px 0 7px;
          border-bottom:3px solid {INK}; flex:0 0 auto; }}
  .panel {{ border-top:3px solid {INK}; padding-top:3px; }}
  .panel svg {{ display:block; width:100%; height:116px; }}
  .pcap {{ font-family:"Arial Black", Helvetica, sans-serif; font-size:15px; line-height:1.06;
          margin-top:5px; letter-spacing:-.2px; }}
  .pcap b {{ color:{RED}; margin-right:4px; }}
  .pdet {{ font-size:10px; line-height:1.2; margin-top:2px; color:#453d31; }}

  .grid {{ display:grid; grid-template-columns:repeat(4,1fr); gap:9px 13px; padding-top:9px;
          flex:0 0 auto; }}
  .tile {{ display:flex; flex-direction:column; }}
  .catbar {{ background:{INK}; color:{PAPER}; font-size:7.4px; font-weight:700;
            letter-spacing:1.1px; padding:2.5px 5px 2px; display:flex; justify-content:space-between; }}
  .tno {{ color:#f5d76e; }}
  .lab {{ font-family:"Arial Black", Helvetica, sans-serif; font-size:16px; line-height:1.05;
         letter-spacing:-.3px; margin-top:3px; }}
  .det {{ font-size:10px; line-height:1.2; margin-top:3px; color:#453d31; }}
  .det b {{ color:{RED}; }}

  .lower {{ display:grid; grid-template-columns:290px 1fr; gap:16px; padding-top:9px;
           margin-top:auto; border-top:3px solid {INK}; flex:0 0 auto; }}
  .maplab {{ font-size:8px; font-weight:700; letter-spacing:1.2px; color:{RED};
            text-transform:uppercase; margin-bottom:3px; }}
  .mapkey {{ font-size:8px; line-height:1.25; color:{MUTED}; margin-top:3px; max-width:286px; }}
  .also h3 {{ font-size:8.6px; font-weight:700; letter-spacing:1.5px; color:{RED};
             text-transform:uppercase; margin-bottom:3px; }}
  .also .items {{ column-count:3; column-gap:12px; }}
  .also .items div {{ font-size:9px; line-height:1.28; color:#453d31; break-inside:avoid;
                     margin-bottom:1px; }}

  .foot {{ flex:0 0 auto; border-top:1px solid {RULE}; padding:4px 0 5px;
          display:flex; justify-content:space-between; align-items:baseline; gap:16px; }}
  .foot .a {{ font-size:8.2px; line-height:1.3; color:{MUTED}; max-width:790px; }}
  .foot .a b {{ color:{RED}; letter-spacing:1.1px; }}
  .foot .b {{ font-size:8.6px; letter-spacing:1px; color:{RED}; font-weight:700; white-space:nowrap; }}
</style>
</head>
<body>
<div class="page">

  <div class="mast">
    <div class="kick">ONE DAY · ONE IMAGE · THE WORLD'S NEWS</div>
    <div class="mastrow">
      <div class="date">19&nbsp;NOV<i>&nbsp;2026</i></div>
      <div class="side"><b>THURSDAY</b><span>33 STORIES · FIVE CONTINENTS</span></div>
    </div>
  </div>

  <div class="nums">{nums}</div>

{hero}
  <div class="grid">
{chr(10).join(tiles)}
  </div>

  <div class="lower">
    <div>
      <div class="maplab">Where it happened</div>
      <svg width="290" height="176" viewBox="0 0 290 176" xmlns="http://www.w3.org/2000/svg">
        {dot_map(290, 172)}
      </svg>
      <div class="mapkey">Red numbers mark the stories on this page; grey dots mark the briefs listed beside the map.</div>
    </div>
    <div class="also">
      <h3>Also on Thursday 19 November</h3>
      <div class="items">{also}</div>
    </div>
  </div>

  <div class="foot">
    <div class="a"><b>DATE CHECK</b> &#183; every story here happened, or was first reported, on
      Thursday 19 November 2026; the Shenzhen summit, the EU loan and Voyager's milestone were filed
      on the 18th and confirmed on the 19th. Sources: Reuters, AP, AFP, BBC, Al Jazeera, UN, NASA,
      IMD. Disputed claims are attributed, not stated as fact.</div>
    <div class="b">THE WORLD ON 19 NOVEMBER 2026</div>
  </div>
</div>
</body>
</html>
'''
    Path(__file__).with_name("v4.html").write_text(html)
    print(f"wrote v4.html {len(html)} bytes")


if __name__ == "__main__":
    build()
