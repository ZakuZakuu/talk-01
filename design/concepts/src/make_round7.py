#!/usr/bin/env python3
"""Round-7 sheet for talk.01: grip-to-talk. The left hand holds the device, four fingers squeeze to talk,
the left thumb rolls a wheel to change mode.

Six forms built on that idea (side strip, handset, bullet, ray gun, pebble, G.I. grip), each with a small
"grip map": blue = the four fingers (squeeze), amber = the thumb (wheel). Beige + bright retro palette,
matte finish. Standard library only. Dimensions are TENTATIVE.

    python3 design/concepts/src/make_round7.py design/concepts/round-7
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_concepts import (INK, PAPER, DIM, ORANGE, f, rr, circ, line, poly, path, t,  # noqa: E402
                           panel, px_text, write, SANS, MONO)
from make_round5 import mix, grad, metal, emboss, hlines, vslots, dots_disc, plug_notch, coil  # noqa: E402
from make_round4 import screw  # noqa: E402
from make_round6 import rainbow, badge, rot, ghost, sleeve, CREAM, TEAL, LAV, ORG, RED, MUST, DARK  # noqa: E402
import make_round5 as r5  # noqa: E402

SC = 4.0
MINI = 2.4


def wheel_left(g, cy, color, h=22, ink="#4a463e", pos=0, labels=True):
    g.append(rr(-3.4, cy - h / 2, 5.6, h, 2.4, color, INK, 0.4))
    for k in range(7):
        yy = cy - h / 2 + 3 + k * (h - 6) / 6
        g.append(line(-3.0, yy, 1.8, yy, mix(color, -0.45), 0.3))
    if labels:
        for k, s in enumerate("1234"):
            yy = cy - 6 + k * 4
            g.append(t(5.6, yy + 0.6, s, 1.7, "start", ink, "bold", MONO))
        g.append(poly([(2.6, cy - 6 + pos * 4 - 0.8), (2.6, cy - 6 + pos * 4 + 0.8), (4.0, cy - 6 + pos * 4)], ORANGE, "none", 0.0))
        g.append(t(10.4, cy - 8.6, "MODE", 1.4, "start", ink, "normal", MONO))


def squeeze_strip(g, x, y0, y1, w, fill, edge, ang, text, text_color, ribs, pivot_y=None, side="right"):
    """A strip on the right edge, hinged at the bottom, popped out `ang` degrees; dashed = flush."""
    pivot_y = y1 if pivot_y is None else pivot_y
    body = path(f"M{x},{y0} H{x + w} V{y1} H{x} Z", fill, edge, 0.5)
    for k in range(ribs):
        yy = y0 + 14 + k * (y1 - y0 - 20) / max(ribs - 1, 1)
        body += line(x + 1.2, yy, x + w - 1.2, yy, mix(fill, -0.3), 0.35)
    body += f'<g transform="translate({x + w / 2 + 0.6},{(y0 + y1) / 2 + 6}) rotate(-90)">{t(0, 0, text, 2.3, "middle", text_color, "bold", MONO)}</g>'
    g.append(ghost(x, y0, w, y1 - y0, 3))
    g.append(rot(body, ang, x + w, pivot_y))
    g.append(circ(x + w, pivot_y, 1.3, "#b79c4a", "#4d3d12", 0.25))


# ----------------------------------------------------------------- A GRIP STRIP
def d_a():
    g = [rr(0, 0, 49, 92, 5, grad("g7a", CREAM, 0.06), INK, 0.45), rr(6, 9, 37, 25, 3, TEAL, "#1f5a5f", 0.4), hlines(9, 12, 31, 8, 2.8, 1.2, "#2a7479"),
         circ(24.5, 21.5, 1.4, "#143c40", "none", 0.0), rr(6, 40, 37, 12, 2, DARK, "#000", 0.4), circ(12, 46, 1.9, RED, "#4a0f0a", 0.2),
         t(16, 46.8, "ON AIR", 2.0, "start", "#e9dfc0", "bold", MONO)]
    wheel_left(g, 66, TEAL, 24)
    g += [rr(30, 58, 13, 13, 3, "#cfc8b4", "#8a857a", 0.3), t(36.5, 70.2, "LOCK", 1.6, "middle", "#6f6a5e", "bold", MONO), sleeve(31, 60, 9, 4.8, LAV),
          badge(13, 82), screw(44, 5), screw(44, 87)]
    squeeze_strip(g, 49, 6, 88, 11, TEAL, "#1f5a5f", 4, "SQUEEZE TO TALK", "#e9dfc0", 11)
    g += [plug_notch(24.5), coil(24.5, 0, 6, 2.6, 7, "#2a7479")]
    return "".join(g)


# ----------------------------------------------------------------- B HANDSET
PP = ("M16,0 H44 Q58,0 58,9 V32 C58,46 49,48 49,62 V70 C49,82 55,82 55,88 Q55,92 50,92 "
      "H8 Q3,92 3,88 C3,82 9,82 9,70 V62 C9,48 0,46 0,32 V9 Q0,0 14,0 Z")


def d_b():
    g = [path(PP, grad("g7b", "#2d2d30", 0.18), "#000", 0.5), rr(11, 8, 36, 25, 3, "#111", "#000", 0.4), hlines(14, 11, 30, 8, 2.8, 1.1, "#9ea3a5"),
         circ(29, 20.5, 1.3, "#e9dfc0", "none", 0.0), rr(11, 37, 36, 11, 2, "#0b0b0b", "#000", 0.3), circ(17, 42.5, 1.9, "#f2a92e", "#6b4309", 0.2),
         t(21, 43.3, "ON AIR", 2.0, "start", "#f2a92e", "bold", MONO)]
    # wheel in the waist (left)
    g.append(rr(4, 52, 8, 20, 3, ORG, "#7a3c0e", 0.45))
    for k in range(7):
        g.append(line(4.8, 55 + k * 2.6, 11.2, 55 + k * 2.6, "#a8561a", 0.3))
    for k, s in enumerate("1234"):
        g.append(t(14.6, 56.6 + k * 4, s, 1.7, "start", "#cfd3d4", "bold", MONO))
    g.append(poly([(13.2, 55.8), (13.2, 57.4), (14.4, 56.6)], ORANGE, "none", 0.0))
    g.append(emboss(16, 85, "talk.01", 3.6, "#cfd3d4", "start", SANS, "bold"))
    # chrome squeeze bar down the right waist, hinged at the bottom
    bar = path("M49.5,40 H55 V84 H49.5 Z", metal("g7bm"), "#444", 0.5) + "".join(line(50.4, 48 + k * 4.6, 54.2, 48 + k * 4.6, "#7d8083", 0.3) for k in range(8))
    g.append(ghost(49.5, 40, 5.5, 44, 2.5))
    g.append(rot(bar, 4.5, 55, 84))
    g += [plug_notch(29, "#000"), coil(29, 0, 6, 2.6, 7, ORG)]
    return "".join(g)


# ----------------------------------------------------------------- C BULLET
def d_c():
    EGG = "M0,38 C0,12 11,0 28,0 C45,0 56,12 56,38 V80 Q56,92 44,92 H12 Q0,92 0,80 Z"
    g = [path(EGG, grad("g7c", CREAM, 0.06), INK, 0.5)]
    g.append(f'<clipPath id="g7cclip"><path d="M0,38 C0,12 11,0 28,0 C45,0 56,12 56,38 V44 H0 Z"/></clipPath>')
    g.append(f'<g clip-path="url(#g7cclip)">{rr(0, 0, 56, 46, 0, metal("g7cm"), "none", 0.0)}{dots_disc(28, 24, 26, 3.4, 0.95, "#3a3d3f")}</g>')
    g.append(path("M0,44 H56", "none", "#7d8083", 0.6))
    g += [circ(28, 16, 1.4, "#111", "none", 0.0), rr(8, 50, 40, 10, 3, DARK, "#000", 0.4), circ(14, 55, 1.8, RED, "#4a0f0a", 0.2), t(18, 55.8, "ON AIR", 1.9, "start", "#e9dfc0", "bold", MONO)]
    # lower sleeve ribs on the left (fixed) and the squeeze half on the right
    for k in range(5):
        g.append(line(3, 64 + k * 2.8, 24, 64 + k * 2.8, "#b9b3a2", 0.5, 'stroke-linecap="round"'))
    shell = (path("M28,62 H56 V80 Q56,92 44,92 H28 Z", LAV, "#4f4d86", 0.5) + "".join(line(31, 66 + k * 3.2, 53, 66 + k * 3.2, "#6e6cb0", 0.4) for k in range(8)) +
             f'<g transform="translate(46,80) rotate(-90)">{t(0, 0, "SQUEEZE", 2.2, "middle", "#eceaf8", "bold", MONO)}</g>')
    g.append(ghost(28, 62, 28, 30, 4))
    g.append(rot(shell, 3.5, 28, 92))
    g.append(rr(-3.4, 28, 5.6, 22, 2.4, ORG, "#7a3c0e", 0.45))
    for k in range(7):
        g.append(line(-3.0, 31 + k * 2.9, 1.8, 31 + k * 2.9, "#a8561a", 0.3))
    for k, s in enumerate("1234"):
        g.append(t(5.6, 31.4 + k * 4, s, 1.6, "start", "#4a463e", "bold", MONO))
    g += [badge(3, 82), plug_notch(28, "#111"), coil(28, 0, 6, 2.6, 7, "#8a89c9")]
    return "".join(g)


# ----------------------------------------------------------------- D RAY (side profile)
def d_d():
    RDB = "#d8483c"
    g = []
    # handle (tilted back) and head
    g.append(f'<g transform="rotate(-12 34 30)">{rr(28, 28, 26, 62, 7, grad("g7d", RDB, 0.1), INK, 0.5)}</g>')
    g.append(rr(0, 4, 58, 32, 10, grad("g7d2", CREAM, 0.06), INK, 0.5))
    g += [hlines(40, 10, 14, 7, 2.8, 1.1, "#8a857a"), rr(38, 8, 17, 21, 3, "none", "#8a857a", 0.35), circ(46.5, 18, 1.3, "#4a463e", "none", 0.0)]
    # fins on the back of the head
    g += [poly([(0, 12), (-9, 6), (-9, 22), (0, 24)], RDB, INK, 0.5), poly([(0, 26), (-7, 24), (-7, 34), (0, 34)], RDB, INK, 0.5)]
    # thumb wheel on the head, near the neck
    g += [circ(22, 20, 7.5, "#2b2a28", "#000", 0.4)]
    for k in range(22):
        a = math.radians(k * 360 / 22)
        g.append(line(22 + 6.0 * math.sin(a), 20 - 6.0 * math.cos(a), 22 + 7.5 * math.sin(a), 20 - 7.5 * math.cos(a), "#8a857a", 0.3))
    g += [circ(22, 20, 3.2, ORG, "#7a3c0e", 0.3), t(22, 31.4, "MODE 1-4", 1.4, "middle", "#6f6a5e", "normal", MONO)]
    # trigger lever on the FRONT of the handle (right), pulled by four fingers toward the palm
    lever = path("M0,0 Q6,2 6,10 V46 Q6,52 0,54 Z", metal("g7dm"), "#444", 0.5)
    g.append(ghost(50, 38, 7, 50, 3))
    g.append(f'<g transform="translate(50.5,38) rotate(5 0 0)">{lever}<g transform="translate(3.6,28) rotate(-90)">{t(0, 0, "SQUEEZE", 2.0, "middle", "#4a463e", "bold", MONO)}</g></g>')
    g += [badge(2, 40.5, "#4a463e"), plug_notch(14), coil(14, 4, 6, 2.6, 7, ORG)]
    return "".join(g)


# ----------------------------------------------------------------- E PEBBLE
def d_e():
    g = [rr(0, 0, 62, 84, 26, "#2f7478", "#17484b", 0.5)]
    g.append(f'<clipPath id="g7eclip"><rect x="41" y="-4" width="40" height="100"/></clipPath>')
    g.append(rr(41, 2, 22, 80, 10, "#10282a", "none", 0.0))
    g.append(f'<g clip-path="url(#g7eclip)"><g transform="translate(2.4,0)">{rr(0, 0, 62, 84, 26, grad("g7e", "#4a9ba0", 0.1), "#17484b", 0.5)}'
             f'<g transform="translate(-2.4,0)"></g></g></g>')
    g.append(f'<g clip-path="url(#g7eclip)"><g transform="translate(2.4,0)">{"".join(line(46, 26 + k * 4, 59, 26 + k * 4, "#2b7c80", 0.4) for k in range(10))}</g></g>')
    g.append(rr(0, 0, 41, 84, 26, "#4a9ba0", "#17484b", 0.5).replace('rx="26"', 'rx="26"'))
    g.append(rr(14, 0, 27, 84, 0, "#4a9ba0", "none", 0.0))
    g.append(line(41, 8, 41, 76, "#10282a", 0.7))
    g += [rr(10, 8, 34, 28, 6, "#2f7478", "#17484b", 0.4), dots_disc(27, 22, 12.5, 3.2, 0.95, "#d9efef"), rr(10, 42, 34, 11, 3, DARK, "#000", 0.4),
          circ(16, 47.5, 1.9, RED, "#4a0f0a", 0.2), t(20, 48.3, "ON AIR", 1.9, "start", "#e9dfc0", "bold", MONO), badge(10, 64, "#e9f4f4"),
          t(52, 70, "SQUEEZE", 2.0, "middle", "#e9f4f4", "bold", MONO)]
    g.append(rr(-3.4, 28, 5.6, 22, 2.4, ORG, "#7a3c0e", 0.45))
    for k in range(7):
        g.append(line(-3.0, 31 + k * 2.9, 1.8, 31 + k * 2.9, "#a8561a", 0.3))
    for k, s in enumerate("1234"):
        g.append(t(5.0, 31.4 + k * 4, s, 1.6, "start", "#e9f4f4", "bold", MONO))
    g += [plug_notch(31, "#17484b"), coil(31, 0, 6, 2.6, 7, ORG)]
    g.append(ghost(41, 2, 21, 80, 10))
    return "".join(g)


# ----------------------------------------------------------------- F G.I. GRIP
def d_f():
    import random
    OL = "#5d6140"
    g = [rr(0, 0, 50, 92, 4, grad("g7f", OL, 0.12), "#1c1e12", 0.5)]
    rnd = random.Random(7)
    for _ in range(150):
        g.append(circ(rnd.uniform(2, 48), rnd.uniform(2, 90), 0.22, mix(OL, rnd.choice((-0.25, 0.22))), "none", 0.0))
    g += [circ(26, 24, 15.5, "#8b8d6e", "#262817", 0.5), circ(26, 24, 13.8, "#171810", "none", 0.0), dots_disc(26, 24, 13.8, 2.9, 0.85, "#a9ab86"),
          rr(6, 46, 38, 20, 1.5, "#cfcaa6", "#262817", 0.4), t(25, 54, "SQUEEZE TO TALK", 3.4, "middle", "#262817", "bold", SANS),
          t(25, 58.6, "TALK-01 · SET No. 1", 1.9, "middle", "#262817", "normal", MONO), t(25, 63, "MODE: WHEEL 1-4", 1.8, "middle", "#262817", "normal", MONO),
          circ(38, 76, 3.0, "#d8362a", "#5a110b", 0.3), t(38, 82, "ON AIR", 1.4, "middle", "#d5d2a8", "normal", MONO)]
    for sx, sy in ((5, 5), (45, 5), (5, 87), (45, 87)):
        g.append(circ(sx, sy, 2.0, "#b79c4a", "#4d3d12", 0.3))
    g.append(rr(-3.4, 28, 5.6, 22, 2.4, "#1c1c1a", "#000", 0.45))
    for k in range(7):
        g.append(line(-3.0, 31 + k * 2.9, 1.8, 31 + k * 2.9, "#4a4d38", 0.3))
    for k, s in enumerate("1234"):
        g.append(t(5.2, 31.4 + k * 4, s, 1.7, "start", "#d5d2a8", "bold", MONO))
    rub = path("M50,10 H60 V86 H50 Z", "#262817", "#0e0f08", 0.5) + "".join(line(51.2, 16 + k * 3.8, 58.8, 16 + k * 3.8, "#4a4d38", 0.4) for k in range(19))
    g.append(ghost(50, 10, 10, 76, 2.5))
    g.append(rot(rub, 4, 60, 86))
    g += [rr(40, -3.4, 6, 6.4, 2, "none", "#9a9c84", 0.7), plug_notch(20, "#171810"), coil(20, 0, 6, 2.6, 7, "#2d2f20")]
    return "".join(g)


# squeeze pads (blue) and thumb (amber) in each design's own coordinates, plus an arrow
GRIP = {
    "A": dict(pads=[(49.5, 14 + k * 18.5, 9, 14) for k in range(4)], thumb=(1, 66, 6), arrow=(62, 50, 55, 50)),
    "B": dict(pads=[(49.5, 40 + k * 11.5, 5.5, 9) for k in range(4)], thumb=(8, 62, 6), arrow=(63, 62, 57, 62)),
    "C": dict(pads=[(31, 63 + k * 7, 22, 5) for k in range(4)], thumb=(0, 39, 6), arrow=(60, 76, 54, 76)),
    "D": dict(pads=[(52, 40 + k * 12, 5, 10) for k in range(4)], thumb=(22, 20, 7.5), arrow=(64, 62, 58, 62)),
    "E": dict(pads=[(44, 14 + k * 17.5, 15, 13) for k in range(4)], thumb=(1, 39, 6), arrow=(68, 44, 63, 44)),
    "F": dict(pads=[(51, 14 + k * 17, 8, 14) for k in range(4)], thumb=(1, 39, 6), arrow=(65, 50, 59, 50)),
}


ROT = {"A": (4, 60, 88), "B": (4.5, 55, 84), "C": (3.5, 28, 92), "D": (5, 50.5, 38), "F": (4, 60, 86)}


def overlay(key):
    gp = GRIP[key]
    g = []
    pads = "".join(rr(x, y, w, h, min(w, h) / 2.2, "#2a6fd0", "#16427f", 0.35, 'opacity="0.55"') for (x, y, w, h) in gp["pads"])
    if key in ROT:
        a, px_, py_ = ROT[key]
        pads = rot(pads, a, px_, py_)
    elif key == "E":
        pads = f'<g transform="translate(2.4,0)">{pads}</g>'
    g.append(pads)
    cx, cy, r = gp["thumb"]
    g.append(circ(cx, cy, r, "#f2a92e", "#7a5410", 0.4, 'opacity="0.6"'))
    x1, y1, x2, y2 = gp["arrow"]
    g.append(line(x1, y1, x2, y2, "#16427f", 1.0, 'stroke-linecap="round"'))
    g.append(poly([(x2, y2), (x2 + 2.6, y2 - 1.8), (x2 + 2.6, y2 + 1.8)], "#16427f", "#16427f", 0.1))
    return "".join(g)


CARDS = [
    ("A", "A · GRIP STRIP", "beige + teal", d_a, 62,
     ["lineage: the round-6 strip moved to the right edge, where the four fingers are",
      "squeeze: a 78 mm strip hinged at the bottom; wheel: a ribbed thumb wheel on the left, with a 1-4 scale; a sleeve still locks it",
      "grille: horizontal lines   cable: teal coil   depth: about 20 mm (thin)",
      "+ the smallest change from round 6; fits a pocket",
      "- a 20 mm slab squeezes like a pinch, not a power grip"]),
    ("B", "B · HANDSET", "black + chrome + orange", d_b, 62,
     ["lineage: the CB hand mic and the telephone handset: a waisted body",
      "squeeze: a chrome bar down the right waist; wheel: an orange ribbed wheel in the waist on the left",
      "grille: horizontal lines   cable: orange coil   waist about 40 mm deep",
      "+ the waist is where the hand sits; the best classic grip",
      "- a waisted body costs inner volume and is harder to print"]),
    ("C", "C · BULLET", "cream + chrome + lavender", d_c, 62,
     ["lineage: the bullet and egg microphones: a perforated metal head, a soft lower body",
      "squeeze: the lower right half is a shell that squeezes; wheel: orange, at the neck on the left",
      "grille: a dot-matrix chrome cap   cable: lavender coil   depth about 38 mm",
      "+ a real power-grip diameter; the most comfortable to hold",
      "- the roundest; the largest in a bag; the egg shell is complex to print"]),
    ("D", "D · RAY", "red + cream + chrome (side view)", d_d, 70,
     ["lineage: the retro ray gun, a label gun and a handheld radar gun: a head and a grip",
      "squeeze: a lever on the front of the handle, pulled by four fingers; wheel: on the head's side",
      "grille: horizontal lines   cable: orange coil from the back of the head",
      "+ the most playful; a natural trigger-like pull with four fingers",
      "- the least like a pocket walkie; the biggest; the strangest to carry"]),
    ("E", "E · PEBBLE", "teal + orange", d_e, 62,
     ["lineage: a squeeze toy / Tamagotchi pebble: two soft shells with a seam",
      "squeeze: the right shell moves in; wheel: orange, on the left; grille: dot-matrix; a flat foot is needed",
      "cable: orange coil   depth about 30 mm",
      "+ squeezing the whole shell is the most intuitive",
      "- anything pressing in a bag squeezes it: the LOCK sleeve is vital"]),
    ("F", "F · G.I. GRIP", "olive + cream + brass", d_f, 66,
     ["lineage: a hand radio with a rubber grip strip (G.I. radio from round 5)",
      "squeeze: a ribbed rubber strip on the right edge; wheel: a black knurled wheel on the left",
      "grille: a dot-matrix disc   cable: olive-black coil   depth about 22 mm",
      "+ rubber is grippy and obviously a grip; a printed data plate is a joke",
      "- heavy, serious look; needs a rubber part or a TPU print"]),
]


def build(out):
    import textwrap
    xs, ys = (40, 660, 1280), (170, 1000)
    body = []
    for i, (key, name, tag, fn, ox, lines) in enumerate(CARDS):
        x, y = xs[i % 3], ys[i // 3]
        body.append(f'<rect x="{x}" y="{y}" width="600" height="820" rx="14" fill="none" stroke="#d3cdbf" stroke-width="2"/>')
        body.append(px_text(x + 16, y + 38, name, 24, INK, "bold", SANS))
        body.append(px_text(x + 16, y + 60, tag, 13, DIM))
        body.append(panel(x + ox, y + 240, fn(), SC))
        body.append(panel(x + 410, y + 250, fn() + overlay(key), MINI))
        body.append(px_text(x + 410, y + 512, "GRIP MAP", 11, INK, "bold", MONO))
        body.append(px_text(x + 410, y + 528, "blue = four fingers", 11, "#16427f", "normal", MONO))
        body.append(px_text(x + 410, y + 544, "amber = thumb (wheel)", 11, "#7a5410", "normal", MONO))
        yy = y + 650
        for s_ in lines:
            col = "#2f6f3a" if s_.startswith("+") else ("#9a2f1a" if s_.startswith("-") else INK)
            for part in textwrap.wrap(s_, 80, subsequent_indent="  "):
                body.append(px_text(x + 16, yy, part, 11.5, col))
                yy += 15
            yy += 3
    head = (px_text(60, 62, "talk.01 · ROUND 7 · GRIP TO TALK", 30, INK, "bold", SANS) +
            px_text(60, 92, "the left hand holds · four fingers squeeze to talk · the left thumb rolls a wheel to change mode", 15, DIM) +
            px_text(1860, 52, "TENTATIVE · NOT A FINAL DESIGN", 13, ORANGE, "bold", MONO, "end") +
            px_text(1860, 72, "original concepts · same scale in the large views (10 mm = 40 px)", 12, DIM, "normal", MONO, "end") +
            px_text(1860, 92, "dashed = the squeeze part in its flush, locked position", 12, DIM, "normal", MONO, "end") +
            px_text(60, 128, "All: USB-C and a coiled cable on top · a small hatch and a small U stand on the back · a sleeve locks the squeeze part flush · mirror for a right hand.", 14, INK, "normal", MONO))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1860" width="1920" height="1860"><defs>{"".join(r5.DEFS)}</defs>'
           f'<rect width="1920" height="1860" fill="{PAPER}"/>{head}{"".join(body)}</svg>')
    write(out, "round7.svg", svg)


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else ".")
