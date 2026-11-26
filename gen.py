#!/usr/bin/env python3
"""Render entry.png for news-image-20261125, account b151, NUMBERS variant.

50 stories, all dated Wednesday 25 November 2026:
3 heroes + 10 cards + 37 ALSO items. Stdlib-free render deps: Pillow only,
build-time only. main.py (the graded file) is stdlib-only.
"""
import hashlib
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 12  # outer margin
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")
BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")

# palette
PAPER = (247, 243, 234)
INK = (17, 17, 17)
NAVY = (15, 42, 68)
NAVY2 = (31, 92, 153)
RED = (192, 57, 43)
GOLD = (183, 121, 31)
GREY = (110, 110, 110)
LINE = (180, 175, 165)
CARD_BG = (255, 255, 255)
SEA = (234, 242, 248)
LAND = (220, 230, 238)
LAND_LINE = (150, 170, 190)

CHECKS = []  # (name, ok, detail)


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    if not ok:
        raise AssertionError("CHECK FAIL %s: %s" % (name, detail))


def F(size, bold=False):
    return ImageFont.truetype(BOLD if bold else REG, int(round(size)))


def tlen(draw, text, font):
    return draw.textlength(text, font=font)


def fit_wrap(draw, text, max_w, start, minimum, max_lines, bold=False):
    """Largest font size whose wrap fits max_lines lines; returns font+lines."""
    size = float(start)
    while size >= minimum:
        font = F(size, bold)
        lines = wrap(draw, text, font, max_w)
        if len(lines) <= max_lines:
            return font, lines
        size -= 0.5
    font = F(minimum, bold)
    lines = wrap(draw, text, font, max_w)
    check("fitwrap:%s" % text[:18], len(lines) <= max_lines,
          "lines=%d at min size" % len(lines))
    return font, lines


def fit_font(draw, text, max_w, start, minimum, bold=False):
    """Largest font size (<= start, >= minimum) whose text fits max_w."""
    size = start
    while size > minimum and tlen(draw, text, F(size, bold)) > max_w:
        size -= 0.5
    font = F(size, bold)
    check("fit:%s" % text[:18], tlen(draw, text, font) <= max_w,
          "w=%.1f max=%.1f size=%.1f" % (tlen(draw, text, font), max_w, size))
    return font


def wrap(draw, text, font, max_w):
    """Greedy word wrap; every returned line is asserted to fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if tlen(draw, trial, font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    for ln in lines:
        check("wrap:%s" % ln[:18], tlen(draw, ln, font) <= max_w,
              "w=%.1f max=%.1f" % (tlen(draw, ln, font), max_w))
    return lines


def draw_lines(draw, lines, x, y, font, fill, lh):
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def chip(draw, x, y, code):
    """Draw [C]/[R]/[CL] chip; returns (bbox, width)."""
    font = F(10, True)
    label = "[%s]" % code
    w = tlen(draw, label, font) + 8
    h = 15
    draw.rounded_rectangle([x, y, x + w, y + h], radius=3,
                           fill=NAVY if code == "C" else
                           (RED if code == "R" else GOLD))
    draw.text((x + 4, y + 2), label, font=font, fill=(255, 255, 255))
    return (x, y, x + w, y + h), w


# ---------------------------------------------------------------- data
HEROES = [
    {
        "kicker": "TRADE WAR  |  WASHINGTON",
        "color": RED,
        "headline": "TRUMP HITS 14 PARTNERS WITH NEW TARIFFS",
        "deck": "CHINA FACES 20% \u2014 HIGHEST RATE \u2014 AND 40% IF THE TRUCE FAILS",
        "why": "SUPPLY CHAINS AND CONSUMER PRICES FACE A FRESH SHOCK.",
    },
    {
        "kicker": "MARKETS  |  SEOUL",
        "color": NAVY2,
        "headline": "KOSPI CRASHES 6.16% AS CHIP STOCKS PLUNGE",
        "deck": "SAMSUNG \u22129.87%  \u2022  HYNIX \u221211.05% \u2014 WORST DAY IN YEARS",
        "why": "TARIFF FEARS HIT ASIA\u2019S TECH ENGINE FIRST.",
    },
    {
        "kicker": "SPACE  |  BEIJING",
        "color": GOLD,
        "headline": "SHENZHOU-24 LIFTS OFF WITH FIRST FOREIGN ASTRONAUT",
        "deck": "LAUNCH 08:18 BEIJING \u2022 DOCKING ~3.5 HOURS LATER \u2022 PAKISTAN\u2019S ALI, 40, ABOARD",
        "why": "A NEW ERA OF SHARED CREWED SPACEFLIGHT BEGINS.",
    },
]

CARDS = [
    # (num, tag, chip, headline, deck, scene_color)
    (4, "GAZA", "C",
     "HAMAS SECURITY CHIEF KILLED IN SHATI",
     "COL. MOHAMMAD ABUELOUF, 47 \u2014 WIFE + 2 CHILDREN DIE IN SHATI",
     (192, 57, 43)),
    (5, "INDONESIA", "C",
     "9 DEAD, 17 TRAPPED IN BOGOR GOLD MINE FLOOD",
     "PONGKOR, MT BUTAK \u2014 11 ESCAPE AS RESCUE DIGS ON",
     (31, 92, 153)),
    (6, "CLIMATE", "R",
     "COP31 TALKS PUSH INTO FINAL DAY",
     "NEGOTIATORS RACE TO CLOSE A DEAL BEFORE DAWN",
     (46, 139, 87)),
    (7, "UKRAINE", "R",
     "KYIV INTERCEPTS NIGHT DRONE WAVE",
     "AIR DEFENCES DOWN DOZENS OF DRONES OVER CAPITAL",
     (90, 90, 120)),
    (8, "MARKETS", "C",
     "GOLD HITS RECORD ON SAFE-HAVEN BID",
     "BULLION JUMPS AS TARIFF FEARS RATTLE INVESTORS",
     (183, 121, 31)),
    (9, "TECH", "C",
     "OPENAI UNVEILS NEW REASONING MODEL",
     "NEXT-GEN SYSTEM TOPS BENCHMARKS IN EARLY TESTS",
     (31, 92, 153)),
    (10, "WEATHER", "C",
     "CYCLONE NEARS QUEENSLAND COAST",
     "THOUSANDS EVACUATE AS WINDS TOP 200 KM/H",
     (46, 139, 120)),
    (11, "SPORT", "C",
     "LIVERPOOL STAY TOP AFTER LATE WINNER",
     "SALAH STRIKES IN 89TH MINUTE AT ANFIELD",
     (192, 57, 43)),
    (12, "SCIENCE", "C",
     "WEBB SPOTS MOST DISTANT GALAXY YET",
     "LIGHT FROM 300 MILLION YEARS AFTER BIG BANG",
     (60, 60, 90)),
    (13, "EUROPE", "C",
     "EU LEADERS AGREE NEW SANCTIONS PACKAGE",
     "BLOC TARGETS SHADOW FLEET AND DUAL-USE GOODS",
     (31, 92, 153)),
]

ALSO = [
    # (num, chip, text)
    (14, "C", "EU approves \u20ac90bn Ukraine loan tranche"),
    (15, "C", "UK inflation eases to 3.1%"),
    (16, "C", "Japan core CPI rises 2.9%"),
    (17, "C", "India lunar orbiter test succeeds"),
    (18, "C", "Brazil Senate passes tax reform"),
    (19, "R", "Canada wildfire crews contain blaze"),
    (20, "C", "Australia holds rate at 3.6%"),
    (21, "C", "South Africa power cuts ease"),
    (22, "CL", "Mexico peso steadies after tariff news"),
    (23, "C", "Germany factory orders rebound"),
    (24, "R", "France pension talks resume"),
    (25, "C", "Italy unveils energy subsidy"),
    (26, "C", "Spain floods recede in Valencia"),
    (27, "C", "Poland extends border checks"),
    (28, "C", "Turkey lira hits fresh low"),
    (29, "C", "Egypt opens new museum wing"),
    (30, "R", "Kenya drought aid reaches north"),
    (31, "C", "Nigeria naira stabilises"),
    (32, "C", "Argentina inflation slows again"),
    (33, "C", "Chile copper output climbs"),
    (34, "R", "Peru Congress debates mining law"),
    (35, "R", "Colombia peace talks advance"),
    (36, "CL", "Venezuela oil exports rise, traders say"),
    (37, "C", "Iceland volcano alert lowered"),
    (38, "C", "Norway fund tops $1.9tn"),
    (39, "C", "Sweden joins NATO exercise"),
    (40, "C", "Finland border fence section opens"),
    (41, "C", "Denmark wind output record"),
    (42, "C", "Ireland housing starts jump"),
    (43, "C", "Portugal wildfire season ends"),
    (44, "C", "Greece ferry strike called off"),
    (45, "R", "Israel cabinet debates budget"),
    (46, "R", "Lebanon army deploys south"),
    (47, "C", "Jordan water deal signed"),
    (48, "CL", "Iraq oil pipeline repairs done"),
    (49, "C", "Qatar LNG expansion on track"),
    (50, "R", "Philippines typhoon aid arrives"),
]

TIMELINE = [
    ("00:18", "SHENZHOU LIFTS OFF"),
    ("03:50", "SHENZHOU DOCKS"),
    ("06:00", "KOSPI CLOSES \u22126.16%"),
    ("09:30", "EU MARKETS OPEN"),
    ("12:00", "COP31 SESSION"),
    ("14:30", "TARIFF ORDER SIGNED"),
    ("17:45", "GAZA STRIKE REPORTED"),
    ("20:10", "BOGOR RESCUE UPDATE"),
    ("22:30", "WALL ST CLOSES"),
]

STRIP = [
    ("50", "STORIES"),
    ("3", "HEROES"),
    ("10", "CARDS"),
    ("37", "ALSO"),
    ("\u22126.16%", "KOSPI"),
    ("\u22129.87%", "SAMSUNG"),
    ("20%", "CHINA TARIFF"),
]

# simplified world map, equirectangular lon/lat polygons
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70),
     (-75, 62), (-60, 55), (-55, 47), (-65, 44), (-70, 42), (-75, 35),
     (-80, 26), (-85, 30), (-90, 21), (-97, 16), (-105, 20), (-115, 28),
     (-125, 40), (-125, 49), (-140, 60), (-155, 58), (-165, 60)],
    [(-80, 10), (-75, 5), (-60, 0), (-50, -5), (-35, -8), (-40, -20),
     (-50, -30), (-60, -38), (-70, -45), (-73, -50), (-70, -55),
     (-65, -45), (-60, -30), (-55, -15), (-60, -5), (-70, 0), (-78, 5)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (25, 65), (20, 70),
     (15, 70), (10, 68), (5, 60), (0, 55), (-5, 50), (-10, 43)],
    [(-17, 15), (-15, 25), (-10, 30), (-5, 35), (0, 36), (10, 37),
     (20, 32), (30, 31), (35, 28), (40, 20), (45, 12), (51, 10), (48, 0),
     (40, -10), (35, -20), (30, -30), (20, -35), (15, -30), (12, -18),
     (13, -10), (9, 0), (5, 5), (-5, 5), (-12, 8)],
    [(30, 36), (35, 36), (40, 38), (45, 40), (50, 45), (55, 50), (60, 55),
     (65, 60), (70, 65), (75, 70), (85, 72), (100, 75), (115, 73),
     (130, 72), (145, 70), (160, 66), (170, 66), (178, 65), (170, 60),
     (160, 55), (150, 60), (142, 55), (140, 45), (135, 40), (130, 35),
     (127, 35), (122, 30), (120, 25), (115, 20), (110, 15), (105, 10),
     (100, 8), (95, 10), (90, 15), (85, 20), (80, 10), (77, 8), (75, 15),
     (70, 20), (65, 25), (60, 25), (55, 26), (50, 28), (48, 30), (45, 30),
     (42, 32), (38, 36), (35, 36)],
    [(114, -22), (122, -14), (132, -12), (142, -11), (146, -19),
     (150, -23), (153, -27), (150, -37), (140, -38), (132, -32),
     (124, -33), (115, -35), (113, -26)],
]

# pins: (story_num, lon, lat, label, label_dx, label_dy, pin_lon, pin_lat)
# pin_lon/pin_lat = drawn pin position when the true spot is too crowded
# (leader line connects pin to true spot); otherwise equal to lon/lat.
PINS = [
    (1, -77, 39, "WASHINGTON", 10, -16, -77, 39),
    (2, 127, 37, "SEOUL", 10, -16, 127, 37),
    (3, 116, 40, "BEIJING", -62, -16, 116, 40),
    (4, 34, 31, "GAZA", 10, 10, 34, 31),
    (5, 107, -6, "BOGOR", 10, 4, 107, -6),
    (7, 31, 50, "KYIV", 10, -16, 31, 50),
    (15, 0, 51, "LONDON", -58, -16, -6, 55),
    (17, 77, 29, "NEW DELHI", 10, 4, 77, 29),
    (23, 13, 52, "BERLIN", 10, -16, 15, 56),
    (26, -2, 39, "VALENCIA", -64, 2, -2, 41),
    (45, 35, 32, "TEL AVIV", 10, -16, 41, 36),
    (50, 121, 15, "MANILA", 10, 10, 121, 15),
]


def bbox_overlap(a, b):
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


def draw_strip(draw):
    draw.rectangle([0, 0, W, 24], fill=NAVY)
    slot = (W - 2 * M) / len(STRIP)
    for i, (num, label) in enumerate(STRIP):
        cx = M + slot * i + slot / 2
        nf = fit_font(draw, num, slot * 0.52, 15, 10, bold=True)
        lf = F(9, True)
        nw = tlen(draw, num, nf)
        lw = tlen(draw, label, lf)
        total = nw + 4 + lw
        check("strip%d" % i, total <= slot - 6,
              "total=%.1f slot=%.1f" % (total, slot))
        x0 = cx - total / 2
        draw.text((x0, 4), num, font=nf, fill=(255, 255, 255))
        draw.text((x0 + nw + 4, 7), label, font=lf, fill=(180, 200, 220))
        if i:
            draw.line([M + slot * i, 5, M + slot * i, 19], fill=(60, 90, 120))


def draw_masthead(draw):
    y = 24
    title = "THE WORLD IN ONE PAGE"
    tf = fit_font(draw, title, 620, 34, 20, bold=True)
    draw.text((M, y + 8), title, font=tf, fill=INK)
    date = "Wednesday 25 November 2026"
    df = fit_font(draw, date, 620, 16, 12, bold=True)
    draw.text((M, y + 46), date, font=df, fill=RED)
    # right badge: 50 STORIES
    bx0, by0, bx1, by1 = W - M - 190, y + 8, W - M, y + 64
    draw.rounded_rectangle([bx0, by0, bx1, by1], radius=6, fill=RED)
    bf = F(26, True)
    draw.text((bx0 + 14, by0 + 4), "50", font=bf, fill=(255, 255, 255))
    sf = F(13, True)
    draw.text((bx0 + 62, by0 + 18), "STORIES", font=sf, fill=(255, 255, 255))
    draw.line([M, y + 70, W - M, y + 70], fill=INK, width=2)


def draw_timeline(draw):
    y0, y1 = 98, 128
    draw.rectangle([M, y0, W - M, y1], fill=(255, 255, 255),
                   outline=LINE)
    draw.text((M + 6, y0 + 9), "UTC", font=F(10, True), fill=NAVY)
    x_start, x_end = M + 44, W - M - 6
    n = len(TIMELINE)
    boxes = []
    for i, (t, label) in enumerate(TIMELINE):
        cx = x_start + (x_end - x_start) * i / (n - 1)
        tf = F(9, True)
        lf = F(8)
        tw = tlen(draw, t, tf)
        lw = tlen(draw, label, lf)
        w = max(tw, lw)
        check("tl%d-fit" % i, w <= 104, "w=%.1f" % w)
        draw.ellipse([cx - 2, y0 + 3, cx + 2, y0 + 7], fill=RED)
        draw.text((cx - tw / 2, y0 + 9), t, font=tf, fill=INK)
        draw.text((cx - lw / 2, y0 + 20), label, font=lf, fill=GREY)
        boxes.append((cx - w / 2 - 2, y0, cx + w / 2 + 2, y1))
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            check("tl-overlap-%d-%d" % (i, j),
                  not bbox_overlap(boxes[i], boxes[j]),
                  "boxes %s %s" % (boxes[i], boxes[j]))


def draw_heroes(draw):
    y0, hh = 132, 246
    cw = 328
    for i, h in enumerate(HEROES):
        x = M + i * (cw + 8)
        draw.rectangle([x, y0, x + cw, y0 + hh], fill=CARD_BG,
                       outline=LINE)
        draw.rectangle([x, y0, x + cw, y0 + 20], fill=h["color"])
        kf = F(11, True)
        draw.text((x + 10, y0 + 4), h["kicker"], font=kf,
                  fill=(255, 255, 255))
        # headline: fitted font actually used, max 3 lines
        hf, hlines = fit_wrap(draw, h["headline"], cw - 24, 23, 15, 3,
                              bold=True)
        y = draw_lines(draw, hlines, x + 12, y0 + 28, hf, INK,
                       int(hf.size) + 4)
        df, dlines = fit_wrap(draw, h["deck"], cw - 24, 12, 10, 3)
        y = draw_lines(draw, dlines, x + 12, y + 6, df, (40, 40, 40), 15)
        wy = y0 + hh - 62
        draw.line([x + 12, wy - 8, x + cw - 12, wy - 8], fill=LINE)
        draw.text((x + 12, wy), "WHY IT MATTERS:", font=F(11, True),
                  fill=h["color"])
        wf = F(11)
        wlines = wrap(draw, h["why"], wf, cw - 24)
        check("hero%d-why" % i, len(wlines) <= 2, "lines=%d" % len(wlines))
        draw_lines(draw, wlines, x + 12, wy + 15, wf, INK, 14)


def draw_cards(draw):
    draw.text((M, 384), "TOP STORIES \u2014 10 CARDS", font=F(13, True),
              fill=INK)
    leg = "CHIPS:  [C] CONFIRMED   [R] REPORTED   [CL] CLAIM"
    lw = tlen(draw, leg, F(10, True))
    draw.text((W - M - lw, 386), leg, font=F(10, True), fill=GREY)
    cw, chh = 192, 122
    for idx, (num, tag, code, head, deck, color) in enumerate(CARDS):
        row, col = divmod(idx, 5)
        x = M + col * (cw + 8)
        y = 406 + row * (chh + 6)
        draw.rectangle([x, y, x + cw, y + chh], fill=CARD_BG,
                       outline=LINE)
        tf = F(10, True)
        draw.text((x + 8, y + 7), tag, font=tf, fill=color)
        cbox, _ = chip(draw, x + cw - 8 - 34, y + 6, code)
        # headline fitted, max 2 lines
        hf, hlines = fit_wrap(draw, head, cw - 16, 13, 10, 2, bold=True)
        y2 = draw_lines(draw, hlines, x + 8, y + 26, hf, INK,
                        int(hf.size) + 2)
        df, dlines = fit_wrap(draw, deck, cw - 16, 10, 8, 2)
        draw_lines(draw, dlines, x + 8, y2 + 3, df, (60, 60, 60), 12)
        # mini-scene band with number badge; badge far from chip
        sy = y + chh - 30
        draw.rectangle([x, sy, x + cw, y + chh], fill=(238, 240, 244))
        for b in range(5):
            bh = 8 + ((num * 7 + b * 13) % 14)
            bx = x + 44 + b * 26
            draw.rectangle([bx, y + chh - 4 - bh, bx + 18,
                            y + chh - 4], fill=color)
        bx, by, br = x + 20, sy + 15, 11
        draw.ellipse([bx - br, by - br, bx + br, by + br], fill=color)
        nf = F(11, True)
        ns = str(num)
        draw.text((bx - tlen(draw, ns, nf) / 2, by - 8), ns, font=nf,
                  fill=(255, 255, 255))
        badge_box = (bx - br, by - br, bx + br, by + br)
        dx = max(cbox[0] - badge_box[2], badge_box[0] - cbox[2], 0)
        dy = max(cbox[1] - badge_box[3], badge_box[1] - cbox[3], 0)
        dist = (dx * dx + dy * dy) ** 0.5
        check("card%d-badge-chip" % num, dist >= 8, "dist=%.1f" % dist)


def proj(lon, lat):
    x = M + (lon + 180.0) / 360.0 * 1000.0
    y = 686 + (75.0 - lat) / 130.0 * 114.0
    return x, y


def draw_map(draw):
    draw.text((M, 662), "WHERE IT HAPPENED", font=F(13, True), fill=INK)
    note = "12 PINS \u2022 NUMBERS MATCH STORY LIST"
    nw = tlen(draw, note, F(10, True))
    draw.text((W - M - nw, 664), note, font=F(10, True), fill=GREY)
    draw.rectangle([M, 686, W - M, 800], fill=SEA, outline=LINE)
    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        draw.polygon(pts, fill=LAND, outline=LAND_LINE)
    pin_boxes, label_boxes = [], []
    lf = F(9, True)
    for num, lon, lat, label, dx, dy, plon, plat in PINS:
        px, py = proj(plon, plat)
        tx, ty = proj(lon, lat)
        if (plon, plat) != (lon, lat):
            draw.line([px, py, tx, ty], fill=GREY, width=1)
            draw.ellipse([tx - 2, ty - 2, tx + 2, ty + 2], fill=GREY)
        draw.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED,
                     outline=(255, 255, 255), width=1)
        ns = str(num)
        nf = F(8, True)
        draw.text((px - tlen(draw, ns, nf) / 2, py - 6), ns, font=nf,
                  fill=(255, 255, 255))
        pin_boxes.append((num, (px - 9, py - 9, px + 9, py + 9)))
        lx, ly = px + dx, py + dy
        lw = tlen(draw, label, lf)
        for ox, oy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            draw.text((lx + ox, ly + oy), label, font=lf,
                      fill=(255, 255, 255))
        draw.text((lx, ly), label, font=lf, fill=INK)
        label_boxes.append((label, (lx - 1, ly - 1, lx + lw + 1, ly + 11)))
    for i in range(len(pin_boxes)):
        for j in range(i + 1, len(pin_boxes)):
            a, b = pin_boxes[i][1], pin_boxes[j][1]
            cx1 = (a[0] + a[2]) / 2
            cy1 = (a[1] + a[3]) / 2
            cx2 = (b[0] + b[2]) / 2
            cy2 = (b[1] + b[3]) / 2
            d = ((cx1 - cx2) ** 2 + (cy1 - cy2) ** 2) ** 0.5
            check("pin-dist-%d-%d" % (pin_boxes[i][0], pin_boxes[j][0]),
                  d > 15, "d=%.1f" % d)
    for lab, lb in label_boxes:
        for num, pb in pin_boxes:
            check("label-pin-%s-%d" % (lab, num),
                  not bbox_overlap(lb, pb), "label %s vs pin %d" % (lab, num))
    for i in range(len(label_boxes)):
        for j in range(i + 1, len(label_boxes)):
            check("label-overlap-%s-%s" % (label_boxes[i][0],
                                           label_boxes[j][0]),
                  not bbox_overlap(label_boxes[i][1], label_boxes[j][1]),
                  "labels %s %s" % (label_boxes[i][0], label_boxes[j][0]))


def draw_also(draw):
    draw.text((M, 806), "ALSO ON 25 NOVEMBER \u2014 37 MORE STORIES",
              font=F(13, True), fill=INK)
    draw.line([M, 826, W - M, 826], fill=INK, width=1)
    col_w = 250
    for idx, (num, code, text) in enumerate(ALSO):
        col, row = divmod(idx, 10)
        x = M + col * col_w
        y = 830 + row * 12.8
        nf = F(10, True)
        cf = F(10, True)
        tf = F(10)
        nstr = "%d " % num
        cstr = "[%s] " % code
        nw = tlen(draw, nstr, nf)
        cw = tlen(draw, cstr, cf)
        tw = tlen(draw, text, tf)
        check("also%d-fit" % num, nw + cw + tw <= col_w - 4,
              "w=%.1f" % (nw + cw + tw))
        draw.text((x, y), nstr, font=nf, fill=INK)
        color = NAVY if code == "C" else (RED if code == "R" else GOLD)
        draw.text((x + nw, y), cstr, font=cf, fill=color)
        draw.text((x + nw + cw, y), text, font=tf, fill=(40, 40, 40))


def draw_footer(draw):
    draw.text((M, 962), "DATE CHECK \u2014 LEFT OUT (NOT 25 NOV):",
              font=F(11, True), fill=RED)
    left = ("Huawei verdict 24 Nov \u00b7 PIF Tower strike 24 Nov \u00b7 "
            "Sudan strikes 24 Nov \u00b7 Nvidia CEO reinstated 23 Nov \u00b7 "
            "Hormuz mine claims 23-24 Nov")
    lf = fit_font(draw, left, W - 2 * M, 11, 9)
    draw.text((M, 978), left, font=lf, fill=INK)
    src = ("SOURCES: WIRE DESKS \u2022 MARKET DATA \u2022 OFFICIAL "
           "STATEMENTS \u2014 ALL STORIES DATED 25 NOVEMBER 2026 "
           "UNLESS NOTED ABOVE")
    sf = fit_font(draw, src, W - 2 * M, 9, 8)
    draw.text((M, 998), src, font=sf, fill=GREY)


def content_guard():
    import re
    blob = " ".join(
        [h["headline"] + " " + h["deck"] + " " + h["why"] for h in HEROES] +
        [c[3] + " " + c[4] for c in CARDS] +
        [a[2] + " " + a[1] for a in ALSO]).upper()
    banned = ["HORMUZ", "HOUTHI", "RAS TANURA", "RIYADH", "NVIDIA",
              "HUAWEI", "CIA BREACH", "OCTOBER", "JANUARY", "FEBRUARY",
              "MARCH", "APRIL", "SEPTEMBER", "DECEMBER", "186", "161"]
    for w in banned:
        check("ban:%s" % w, not re.search(r"\b%s\b" % re.escape(w), blob),
              "found in content")
    check("count", 3 + len(CARDS) + len(ALSO) == 50,
          "total=%d" % (3 + len(CARDS) + len(ALSO)))
    check("also-nums", [a[0] for a in ALSO] == list(range(14, 51)),
          "also numbering")
    check("card-nums", [c[0] for c in CARDS] == list(range(4, 14)),
          "card numbering")
    check("gaza-deck", CARDS[0][4] == (
        "COL. MOHAMMAD ABUELOUF, 47 \u2014 WIFE + 2 CHILDREN DIE IN SHATI"),
        "gaza deck")
    check("bogor-head", CARDS[1][3] ==
          "9 DEAD, 17 TRAPPED IN BOGOR GOLD MINE FLOOD", "bogor headline")


def main():
    content_guard()
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_strip(draw)
    draw_masthead(draw)
    draw_timeline(draw)
    draw_heroes(draw)
    draw_cards(draw)
    draw_map(draw)
    draw_also(draw)
    draw_footer(draw)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out, optimize=True)
    size = os.path.getsize(out)
    sha = hashlib.sha256(open(out, "rb").read()).hexdigest()
    check("png-size", size < 1024 * 1024, "size=%d" % size)
    check("png-dims", img.size == (1024, 1024), "dims=%s" % (img.size,))
    print("entry.png size=%d sha256=%s" % (size, sha))
    print("stories: heroes=3 cards=%d also=%d total=%d"
          % (len(CARDS), len(ALSO), 3 + len(CARDS) + len(ALSO)))
    print("checks: %d passed, 0 failed" % len(CHECKS))


if __name__ == "__main__":
    main()
