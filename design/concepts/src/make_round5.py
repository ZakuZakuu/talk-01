#!/usr/bin/env python3
"""Round-5 retro lineup for talk.01: eight different push-to-talk devices from the 1950s to about 2000.

Each design starts from one real kind of old device (Walkman, toy voice gadget, transistor radio,
military hand radio, pager, Game Boy, tape recorder ...). Grilles are horizontal lines, vertical slots or
dot-matrix perforations (no diagonal slots). Panels are colour-blocked. Standard library only.
Dimensions are TENTATIVE.

    python3 design/concepts/src/make_round5.py design/concepts/round-5
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_concepts import (INK, PAPER, DIM, ORANGE, f, rr, circ, line, poly, path, t,  # noqa: E402
                           panel, px_text, write, SANS, MONO)
from make_round4 import screw, pict  # noqa: E402

SC = 4.0
DEFS = []


def mix(c, k):
    """Lighten (k>0) or darken (k<0) a #rrggbb colour."""
    c = c.lstrip("#")
    r, g, b = (int(c[i:i + 2], 16) for i in (0, 2, 4))
    if k >= 0:
        r, g, b = (int(v + (255 - v) * k) for v in (r, g, b))
    else:
        r, g, b = (int(v * (1 + k)) for v in (r, g, b))
    return f"#{r:02x}{g:02x}{b:02x}"


def grad(gid, c, d=0.18, horizontal=False):
    x2, y2 = ("1", "0") if horizontal else ("0.35", "1")
    DEFS.append(f'<linearGradient id="{gid}" x1="0" y1="0" x2="{x2}" y2="{y2}">'
                f'<stop offset="0" stop-color="{mix(c, d)}"/><stop offset="0.55" stop-color="{c}"/>'
                f'<stop offset="1" stop-color="{mix(c, -d)}"/></linearGradient>')
    return f"url(#{gid})"


def metal(gid):
    DEFS.append(f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8f9496"/>'
                '<stop offset="0.25" stop-color="#e9ecec"/><stop offset="0.55" stop-color="#b6babb"/>'
                '<stop offset="0.8" stop-color="#e3e6e6"/><stop offset="1" stop-color="#8c9193"/></linearGradient>')
    return f"url(#{gid})"


def emboss(x, y, s, size, color, anchor="start", family=SANS, weight="bold", hi="#ffffff", lo="#000000", op=0.35):
    return (t(x + 0.18, y + 0.18, s, size, anchor, lo, weight, family).replace("<text ", f'<text opacity="{op}" ') +
            t(x - 0.12, y - 0.12, s, size, anchor, hi, weight, family).replace("<text ", f'<text opacity="{op}" ') +
            t(x, y, s, size, anchor, color, weight, family))


def hlines(x, y, w, n, pitch, th, color):
    return "".join(rr(x, y + i * pitch, w, th, th / 2, color, color, 0.02) for i in range(n))


def vslots(x, y, h, n, pitch, w, color):
    return "".join(rr(x + i * pitch, y, w, h, w / 2, color, color, 0.02) for i in range(n))


def dots_rect(x, y, cols, rows, pitch, r, color):
    return "".join(circ(x + c * pitch, y + rw * pitch, r, color, color, 0.02) for c in range(cols) for rw in range(rows))


def dots_disc(cx, cy, R, pitch, r, color):
    g = []
    rows = int(R / (pitch * 0.866)) + 1
    for j in range(-rows, rows + 1):
        for i in range(-rows, rows + 1):
            x = cx + (i + (0.5 if j % 2 else 0)) * pitch
            y = cy + j * pitch * 0.866
            if math.hypot(x - cx, y - cy) <= R - r:
                g.append(circ(x, y, r, color, color, 0.02))
    return "".join(g)


def knob(cx, cy, r, base, mark="#f2efe6", ticks=22, ang=40, light=0.0):
    g = [circ(cx, cy, r + 0.9, "#111", "#000", 0.2), circ(cx, cy, r, base, "#000", 0.25)]
    for k in range(ticks):
        a = math.radians(k * 360 / ticks)
        g.append(line(cx + (r - 1.1) * math.sin(a), cy - (r - 1.1) * math.cos(a), cx + r * math.sin(a), cy - r * math.cos(a), mix(base, 0.35 + light), 0.3))
    g.append(circ(cx, cy, r * 0.68, mix(base, 0.12), "#000", 0.15))
    a = math.radians(ang)
    g.append(line(cx, cy, cx + r * 0.62 * math.sin(a), cy - r * 0.62 * math.cos(a), mark, 0.9, 'stroke-linecap="round"'))
    return "".join(g)


def coil(cx, yb, turns=6, pitch=2.6, w=7.0, color="#1b1b1b"):
    """Coiled cable above the top edge, drawn in the given colour with a matching dark edge."""
    edge, hi = mix(color, -0.55), mix(color, 0.3)
    g = [rr(cx - 4.5, yb - 3.6, 9, 3.6, 0.8, "#cfcfcf", INK, 0.25), rr(cx - 3.2, yb - 9, 6.4, 5.6, 1.4, "#2b2a28", INK, 0.2)]
    y = yb - 11
    for k in range(turns):
        cy = y - k * pitch
        el = f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(w / 2)}" ry="{f(pitch * 0.9)}" fill="none" transform="rotate(-18 {f(cx)} {f(cy)})"'
        g.append(el + f' stroke="{edge}" stroke-width="1.7"/>')
        g.append(el + f' stroke="{color}" stroke-width="1.1"/>')
        g.append(el + f' stroke="{hi}" stroke-width="0.25" stroke-dasharray="1.2 6"/>')
    g.append(line(cx, y - turns * pitch + pitch, cx, y - turns * pitch - 6, color, 1.4))
    return "".join(g)


def plug_notch(x, color="#1b1b1b"):
    return rr(x - 5, -0.3, 10, 1.7, 0.8, color, color, 0.02)


def shade_rect(x, y, w, h, r, gid, base, d=0.18, stroke=INK, sw=0.4, horizontal=False):
    return rr(x, y, w, h, r, grad(gid, base, d, horizontal), stroke, sw)


# ----------------------------------------------------------------- 1 TPS (Walkman colour blocks)
def d_tps():
    BLUE = "#2f5da8"
    g = [path("M15,0 H51 Q56,0 56,5 V87 Q56,92 51,92 H15 Z", grad("tpsB", BLUE, 0.2), INK, 0.5),
         path("M5,0 H15 V92 H5 Q0,92 0,87 V5 Q0,0 5,0 Z", metal("tpsS"), INK, 0.5), line(15, 0, 15, 92, "#0a1630", 0.5),
         line(15.5, 1, 15.5, 91, "#6f93d1", 0.25)]
    for yy in range(4, 90, 2):
        g.append(line(0.6, yy, 14.4, yy, "#ffffff", 0.05))
    g += [rr(4.2, 8, 6.6, 15, 3, "#1c1c1c", "#000", 0.2), rr(4.5, 9, 6, 6, 1.4, ORANGE, "#6b2509", 0.25),
          t(7.5, 27.5, "HOLD", 1.7, "middle", "#1c1c1c", "bold", MONO),
          rr(3.6, 36, 7.8, 34, 3.4, "#1c1c1c", "#000", 0.2),
          poly([(3.2, 38), (-3, 42), (-3, 66), (3.2, 69)], ORANGE, "#6b2509", 0.35),
          poly([(7.5, 76), (5.6, 79.6), (9.4, 79.6)], "#1c1c1c", "#1c1c1c", 0.05), line(7.5, 79, 7.5, 84, "#1c1c1c", 0.7),
          t(7.5, 88.4, "PUSH", 1.7, "middle", "#1c1c1c", "bold", MONO)]
    g += [rr(19, 6, 33, 27, 3.2, "#244786", "#0d1a38", 0.4), vslots(22.2, 9, 21, 9, 3.4, 1.7, "#0b1226")]
    g += [rr(19, 38, 33, 22, 3, "#10161f", "#000", 0.4), poly([(20, 39), (36, 39), (28, 59), (20, 59)], "#ffffff", "none", 0.0).replace("<polygon ", '<polygon opacity="0.07" '),
          poly([(40, 49), (45, 46), (45, 52)], "#e9eef7", "#e9eef7", 0.05), line(31, 49, 40, 49, "#e9eef7", 0.7),
          circ(26, 49, 2.0, "#e03b2d", "#4a0f0a", 0.2), t(26, 56.8, "ON AIR", 1.6, "middle", "#c9d3e6", "bold", MONO)]
    g += [emboss(19, 77, "TALK", 9, "#f3f1ea"), t(19, 85, "PERSONAL PUSH-TO-TALK", 1.8, "start", "#c9d6ee", "normal", MONO),
          t(19, 88.4, "talk.01  type TK-1", 1.6, "start", "#a9bddf", "normal", MONO), screw(51, 4.5), screw(51, 87.5), plug_notch(35), coil(35, 0, 6, 2.6, 7, "#1b1b1b")]
    return "".join(g)


# ----------------------------------------------------------------- 2 WAND (toy voice gadget)
def d_wand():
    BLUE = "#2a6fd0"
    g = [rr(0, 0, 58, 88, 17, grad("wandB", BLUE, 0.22), INK, 0.5), rr(19, 7, 20, 7, 3.5, PAPER, INK, 0.4),
         rr(19.6, 7.6, 18.8, 5.8, 2.9, "none", "#0f3c82", 0.3)]
    g += [circ(29, 38, 17, "#1b4a97", "#0f3c82", 0.5), circ(29, 38, 15.5, "#0f2f66", "none", 0.0), dots_disc(29, 38, 15.5, 3.0, 0.95, "#8fb6f2"),
          circ(29, 38, 1.7, "#e9f1ff", "none", 0.0)]
    g += [circ(12, 70, 3.3, "#111", "#000", 0.25), circ(12, 70, 2.3, "#2a2a2a", "none", 0.0), t(12, 76.5, "MODE", 1.6, "middle", "#eaf2ff", "bold", MONO)]
    for i, c in enumerate(("#e03b2d", "#f2b82e", "#41b45b", "#f3f3f3")):
        g.append(circ(25 + i * 6, 70, 1.8, c, "#0b2347", 0.3))
        g.append(t(25 + i * 6, 76.5, str(i + 1), 1.8, "middle", "#eaf2ff", "bold", MONO))
    g.append(emboss(29, 84, "talk.01", 4, "#f6fbff", "middle", SANS, "bold"))
    g.append(f'<g transform="translate(4.5,58) rotate(-28)">{rr(-14, -5.2, 17, 10.4, 5.2, "#d8362a", "#5a110b", 0.45)}{rr(-12.6, -3.4, 9, 2.2, 1.1, "#f08a80", "none", 0.0)}</g>')
    g += [t(-4.5, 66.5, "TALK", 1.8, "middle", "#fff", "bold", MONO), plug_notch(29, "#0f3c82"), coil(29, 0, 6, 2.6, 7, BLUE)]
    return "".join(g)


# ----------------------------------------------------------------- 3 CUBE (wood + dot grille + brass)
def d_cube():
    WOOD = "#6b4423"
    DEFS.append('<linearGradient id="cubeW" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7a4f2b"/><stop offset="0.5" stop-color="#6b4423"/><stop offset="1" stop-color="#55341a"/></linearGradient>')
    g = [rr(0, 0, 56, 88, 2.5, "url(#cubeW)", "#2a170a", 0.5)]
    for i in range(16):
        yy = 4 + i * 5.2
        g.append(path(f"M1,{yy} C20,{yy - 1.2} 36,{yy + 1.2} 55,{yy}", "none", "#4d2f17", 0.25))
    g += [rr(6, 6, 44, 46, 2, "#1c1208", "#0f0904", 0.4), dots_rect(9.5, 9.5, 11, 11, 3.7, 1.15, "#b78a4a")]
    g += [circ(34, 70, 13.5, "#d9b35a", "#7a5a1a", 0.5), circ(34, 70, 11.8, "#c79d3f", "none", 0.0)]
    for k in range(4):
        a = math.radians(-60 + k * 40)
        g.append(t(34 + 8.6 * math.sin(a), 70 - 8.6 * math.cos(a) + 0.7, str(k + 1), 2.4, "middle", "#3a2a0a", "bold", SANS))
    g += [line(34, 70, 34 + 6 * math.sin(math.radians(-60)), 70 - 6 * math.cos(math.radians(-60)), "#1b1208", 0.7, 'stroke-linecap="round"'),
          circ(34, 70, 2.2, "#1b1208", "#000", 0.15), circ(50, 60.5, 3.0, "#111", "#000", 0.3), line(50, 60.5, 50, 58, "#f2efe6", 0.6),
          circ(10.5, 66, 3.0, "#d9b35a", "#7a5a1a", 0.4), circ(10.5, 66, 1.9, "#d8362a", "#5a110b", 0.3),
          rr(6, 79, 26, 5.2, 1, "#d9b35a", "#7a5a1a", 0.3), t(19, 82.8, "talk.01 · PTT", 2.3, "middle", "#2a1a05", "bold", SANS)]
    g.append(poly([(1, 22), (-4, 26), (-4, 60), (1, 62)], "#1b1b1b", "#000", 0.4))
    g += [t(10.5, 72.8, "ON AIR", 1.5, "middle", "#e7c978", "normal", MONO), plug_notch(28), coil(28, 0, 6, 2.6, 7, "#1b1b1b")]
    return "".join(g)


# ----------------------------------------------------------------- 4 TUNER (transistor radio)
def d_tuner():
    g = [rr(0, 0, 58, 92, 5, metal("tunM"), INK, 0.5), rr(4.5, 4.5, 49, 83, 3, "#1b1b1d", "#000", 0.4)]
    g += [rr(8.5, 9, 18, 66, 2, "#efe4c8", "#3a3220", 0.4)]
    for k in range(21):
        yy = 12 + k * 3
        g.append(line(9.5, yy, 9.5 + (4.2 if k % 5 == 0 else 2.2), yy, "#3a3220", 0.25))
    for k, lab in enumerate(("DICT", "TALK", "OPEN", "LOCK")):
        g.append(t(12.0, 15 + k * 15 + 3.8, lab, 1.8, "start", "#3a3220", "bold", MONO))
    g += [line(9, 15, 26, 15, "#d8362a", 0.8), circ(27.5, 15, 0.9, "#d8362a", "none", 0.0), t(17.5, 71, "CH 1-4", 1.5, "middle", "#3a3220", "normal", MONO)]
    g += [vslots(31, 9, 50, 6, 3.6, 2.0, "#c9ccce"), knob(17, 83, 3.6, "#1b1b1b", "#f2efe6", 18, -30)]
    g += [circ(41, 83, 4.3, "#d9b35a", "#7a5a1a", 0.4), circ(41, 83, 2.2, "#d8362a", "#5a110b", 0.3), t(41, 89.6, "ON AIR", 1.4, "middle", "#c9ccce", "normal", MONO),
          t(29, 80.8, "PTT", 1.7, "middle", "#c9ccce", "bold", MONO), poly([(5.5, 20), (-3.2, 25), (-3.2, 64), (5.5, 68)], metal("tunL"), "#2a2c2d", 0.4),
          screw(54, 5.5), screw(54, 86.5), plug_notch(40), coil(40, 0, 6, 2.6, 7, "#1b1b1b")]
    return "".join(g)


# ----------------------------------------------------------------- 5 G.I. (military hand radio)
def d_gi():
    OL = "#5d6140"
    g = [rr(0, 0, 54, 92, 4, grad("giB", OL, 0.12), "#1c1e12", 0.5)]
    import random
    rnd = random.Random(4)
    for _ in range(170):
        g.append(circ(rnd.uniform(2, 52), rnd.uniform(2, 90), 0.22, mix(OL, rnd.choice((-0.25, 0.22))), "none", 0.0))
    g += [circ(22, 24, 15.5, "#8b8d6e", "#262817", 0.5), circ(22, 24, 13.8, "#171810", "none", 0.0), dots_disc(22, 24, 13.8, 2.9, 0.85, "#a9ab86")]
    g += [knob(44, 13, 5.6, "#1c1c1a", "#f2efe6", 22, 40)]
    for ang, lab in ((-60, "1"), (-20, "2"), (20, "3"), (60, "4")):
        a = math.radians(ang)
        g.append(t(44 + 9.0 * math.sin(a), 13 - 9.0 * math.cos(a) + 0.6, lab, 1.8, "middle", "#d5d2a8", "bold", MONO))
    g += [rr(6, 44, 42, 20, 1.5, "#cfcaa6", "#262817", 0.4), t(27, 52, "PRESS TO TALK", 4, "middle", "#262817", "bold", SANS),
          t(27, 56.4, "TALK-01 · SET No. 1", 2, "middle", "#262817", "normal", MONO), t(27, 61.2, "DICT · TALK · OPEN · LOCK", 1.8, "middle", "#262817", "normal", MONO)]
    for sx, sy in ((6, 6), (48, 6), (6, 86), (48, 86)):
        g.append(circ(sx, sy, 2.1, "#b79c4a", "#4d3d12", 0.3))
        g.append(path(f"M{sx - 1.2},{sy} h2.4 M{sx},{sy - 1.2} v2.4", "none", "#4d3d12", 0.25))
    g += [circ(40, 74, 3.2, "#d8362a", "#5a110b", 0.3), t(40, 80.2, "ON AIR", 1.5, "middle", "#d5d2a8", "normal", MONO),
          rr(46, -3.4, 6, 6.4, 2, "none", "#9a9c84", 0.7), poly([(1, 18), (-6, 20), (-6, 70), (1, 72)], "#2a2c20", "#0e0f08", 0.5)]
    for yy in range(26, 68, 4):
        g.append(line(-4.8, yy, 0.2, yy + 0.5, "#4a4d38", 0.35))
    g += [plug_notch(24, "#171810"), coil(24, 0, 6, 2.6, 7, "#2d2f20")]
    return "".join(g)


# ----------------------------------------------------------------- 6 PAGEBOY (pager)
def d_page():
    g = [rr(0, 0, 44, 70, 5, grad("pgB", "#222224", 0.25), "#000", 0.5), rr(0.8, 0.8, 42.4, 68.4, 4.2, "none", "#8e9395", 0.4)]
    g += [rr(5, 5, 34, 17, 2, "#111", "#000", 0.3), hlines(8, 7.5, 28, 7, 2.2, 0.9, "#9ea3a5")]
    g += [rr(5, 26, 34, 12, 2, "#0b0b0b", "#000", 0.3), circ(11, 32, 2.0, "#f2a92e", "#6b4309", 0.2), t(15.5, 32.8, "ON AIR", 2.4, "start", "#f2a92e", "bold", MONO),
          rr(5, 43, 34, 5, 2.5, "#111", "#000", 0.3), rr(6, 43.8, 7.5, 3.4, 1.4, metal("pgK"), "#333", 0.2)]
    for k, lab in enumerate(("DICT", "TALK", "OPEN")):
        g.append(t(9.8 + k * 12.4, 51.8, lab, 1.5, "middle", "#c9ccce", "normal", MONO))
    g += [emboss(8, 62, "talk.01", 4.2, "#cfd3d4", "start", SANS, "bold"), screw(38.5, 64.2, 1.4), screw(5.5, 64.2, 1.4),
          poly([(1, 20), (-4.2, 23), (-4.2, 54), (1, 56)], metal("pgL"), "#1b1b1b", 0.4), plug_notch(22), coil(22, 0, 6, 2.6, 6.5, "#161616")]
    return "".join(g)


# ----------------------------------------------------------------- 7 GAMEBOY (handheld)
def d_gb():
    GREY = "#cdcbc0"
    g = [path("M5,0 H53 Q58,0 58,5 V76 Q58,94 40,94 H5 Q0,94 0,89 V5 Q0,0 5,0 Z", grad("gbB", GREY, 0.14), "#6f6d63", 0.5),
         rr(4, 5, 50, 46, 4, "#5c6075", "#34374a", 0.4, ""), rr(10, 14, 38, 30, 2, "#8fa77a", "#4b5f3d", 0.4), hlines(12.5, 16.5, 33, 11, 2.4, 0.9, "#3a4a2f")]
    g += [circ(7, 31, 1.3, "#e03b2d", "#5a110b", 0.2), t(6.2, 40, "ON", 1.3, "middle", "#c9cbd6", "bold", MONO).replace("middle", "start"),
          t(10, 11.5, "talk.01", 3.6, "start", "#d6d8e4", "bold", SANS).replace('font-weight="bold"', 'font-weight="bold" font-style="italic"'),
          t(51, 11.5, "PERSONAL PTT", 1.4, "end", "#aeb2c4", "normal", MONO)]
    g += [line(4, 54, 54, 54, "#a8325f", 0.7), line(4, 56, 54, 56, "#2d56a8", 0.7)]
    g += [circ(15, 73, 7.0, "#a8325f", "#4d1228", 0.45), circ(15, 73, 5.6, "#c0457a", "none", 0.0), t(15, 83.6, "TALK", 2.0, "middle", "#4a4740", "bold", SANS),
          circ(31, 78, 4.3, "#a8325f", "#4d1228", 0.4), t(31, 85.4, "SEND", 1.9, "middle", "#4a4740", "bold", SANS)]
    for k, lab in enumerate(("HOLD", "MODE")):
        g.append(f'<g transform="translate({42 + k * 0},{67 + k * 10}) rotate(-25)">{rr(-5.5, -1.7, 11, 3.4, 1.7, "#8e8c84", "#4a4740", 0.35)}</g>')
        g.append(t(42, 71.4 + k * 10, lab, 1.5, "middle", "#4a4740", "bold", MONO))
    g += [rr(-2.2, 56, 3.6, 16, 1.6, "#8e8c84", "#4a4740", 0.4), poly([(0.8, 22), (-4, 25), (-4, 48), (0.8, 50)], "#a8325f", "#4d1228", 0.4),
          plug_notch(32, "#5a5850"), coil(32, 0, 6, 2.6, 7, "#8e8c84")]
    for yy in range(58, 70, 3):
        g.append(line(-1.8, yy, 1, yy, "#4a4740", 0.25))
    return "".join(g)


# ----------------------------------------------------------------- 8 RECORDER (tape deck / dictation)
def d_rec():
    g = [rr(0, 0, 54, 94, 4, grad("rcB", "#26262a", 0.2), "#000", 0.5), rr(4, 4, 46, 28, 2.5, metal("rcM"), "#555", 0.4)]
    g.append(hlines(8, 8, 38, 9, 2.6, 1.0, "#2a2b2e"))
    g += [circ(27, 51, 11.5, "#e9e4d3", "#3a3a3a", 0.5), circ(27, 51, 10.3, "#f6f1e0", "#8a8576", 0.2)]
    for k in range(11):
        a = math.radians(-60 + k * 12)
        g.append(line(27 + 8.4 * math.sin(a), 51 + 3 - 8.4 * math.cos(a), 27 + 9.8 * math.sin(a), 51 + 3 - 9.8 * math.cos(a), "#2a2a2a", 0.3))
    for k, lab in enumerate(("1", "2", "3", "4")):
        a = math.radians(-60 + k * 40)
        g.append(t(27 + 6.4 * math.sin(a), 54 - 6.4 * math.cos(a) + 0.7, lab, 1.9, "middle", "#2a2a2a", "bold", SANS))
    a0 = math.radians(-60)
    g += [line(27, 54, 27 + 9.2 * math.sin(a0), 54 - 9.2 * math.cos(a0), "#d8362a", 0.7, 'stroke-linecap="round"'), circ(27, 54, 1.4, "#222", "#000", 0.1),
          t(27, 59.4, "DICT·TALK·OPEN·LOCK", 1.15, "middle", "#3a3a3a", "normal", MONO), t(27, 36.5, "talk.01", 2.4, "middle", "#c9ccce", "bold", SANS)]
    g += [rr(4, 68, 46, 21, 2.5, "#16161a", "#000", 0.4)]
    g += [rr(6, 70, 24, 17, 2, "#34343a", "#000", 0.45), circ(18, 77, 3.4, "#d8362a", "#5a110b", 0.3), t(18, 84.6, "PUSH TO TALK", 1.5, "middle", "#e9e9e9", "bold", MONO)]
    for k, lab in enumerate(("HOLD", "SEND")):
        g += [rr(32 + k * 9.2, 70, 8, 17, 2, "#34343a", "#000", 0.45), t(36 + k * 9.2, 85, lab, 1.2, "middle", "#e9e9e9", "bold", MONO)]
    g += [pict(36, 76, "hold", "#e9e9e9"), pict(45.2, 76, "push", "#e9e9e9"), screw(46, 91, 1.2), screw(8, 91, 1.2),
          poly([(1, 38), (-4, 41), (-4, 64), (1, 66)], metal("rcL"), "#222", 0.4), plug_notch(27), coil(27, 0, 6, 2.6, 7, "#161616")]
    return "".join(g)


CARDS = [
    ("1 · TPS", "Walkman colour blocks", d_tps, 56, 92,
     ["lineage: Sony Walkman TPS-L2 (blue body, silver strip, orange hold slider)",
      "grille: vertical slots   panels: blue / silver / orange",
      "lever: orange wedge in the silver strip   cable: black coil",
      "+ the clearest TE-style colour-blocking  + HOLD slider = LOCK",
      "stand: small U on the back; cover: small hatch",
      "- the silver strip needs real metal or paint to sell it"]),
    ("2 · WAND", "toy voice gadget", d_wand, 58, 88,
     ["lineage: Texas Instruments Magic Wand (blue toy, red tip, same-colour cable)",
      "grille: round dot-matrix speaker disc   panels: blue / red / white",
      "lever: red wand tip   cable: same blue as the body",
      "+ the most playful; 4 colour LEDs show the mode   + hand-strap hole",
      "stand: a flat foot (a round body would roll); cover: small hatch",
      "- the most toy-like; the least 'serious tool'"]),
    ("3 · CUBE", "wood and brass", d_cube, 56, 88,
     ["lineage: 1960s transistor radios (a walnut cube with a perforated front, a gold dial)",
      "grille: dot-matrix perforations   materials: wood, brass, black",
      "lever: black slanted bar   cable: black coil",
      "+ warm and unusual; wood filament or veneer is printable",
      "stand: a small brass-look U; cover: small hatch",
      "- wood grain must look real; brass is paint or a printed plate"]),
    ("4 · TUNER", "transistor radio", d_tuner, 58, 92,
     ["lineage: a 1960s transistor radio (silver case, black panel, cream tuning scale)",
      "grille: vertical slots   panels: silver / black / cream / gold",
      "mode: a scale with a red needle (DICT TALK OPEN LOCK)   cable: black",
      "+ the scale shows the mode like a real tuner  + gold lamp badge",
      "stand: the battery-door style hatch swings out as the stand",
      "- the needle needs a mechanism (a thumb knob and a slider)"]),
    ("5 · G.I.", "military hand radio", d_gi, 54, 92,
     ["lineage: a WWII-to-1960s hand radio (olive hammertone, data plate, wing screws)",
      "grille: round dot-matrix disc   panels: olive / cream plate / black",
      "lever: wide ribbed PTT bar   mode: a ribbed knob with 1-4   cable: olive-black",
      "+ the most 'real radio'; a printed data plate is a joke and a label",
      "stand: a fold-out bail with the strap loop; cover: small hatch",
      "- heavy, serious look; texture needs a spray finish"]),
    ("6 · PAGEBOY", "pager", d_page, 44, 70,
     ["lineage: a 1980s pager (black, chrome trim, a belt clip)",
      "grille: horizontal lines   panels: black / chrome / amber",
      "lever: slim chrome bar   mode: a small slide switch   cable: black coil",
      "+ small and pocketable; the chrome clip can be the stand",
      "stand: the chrome belt clip is the stand; cover: small hatch",
      "- tiny; the lever and board need a tight fit"]),
    ("7 · GAMEBOY", "90s handheld", d_gb, 58, 94,
     ["lineage: an early handheld console (grey body, blue-grey bezel, magenta buttons)",
      "grille: a 'screen' made of horizontal lines   panels: grey / blue-grey / magenta",
      "PTT: a big round TALK button on the thumb side   cable: grey coil",
      "+ instantly friendly; the line-grille 'screen' is a good joke",
      "stand: a battery-door hatch that is the stand",
      "- the iconic layout: keep it an abstract nod"]),
    ("8 · RECORDER", "tape deck and dictation", d_rec, 54, 94,
     ["lineage: a tape recorder (black, brushed metal, a dial, piano keys)",
      "grille: horizontal lines   panels: black / metal / cream dial / red",
      "PTT: a big latching key   mode: a dial with a needle   cable: black coil",
      "+ the key stays down when latched (visible state)",
      "stand: small U; cover: small hatch",
      "- a latching key is a harder mechanism"]),
]


def build(out):
    cx0 = (40, 510, 980, 1450)
    cy0 = (170, 1050)
    body = []
    for i, (name, tag, fn, W, H, lines) in enumerate(CARDS):
        x, y = cx0[i % 4], cy0[i // 4]
        body.append(f'<rect x="{x}" y="{y}" width="440" height="860" rx="14" fill="none" stroke="#d3cdbf" stroke-width="2"/>')
        body.append(px_text(x + 16, y + 38, name, 24, INK, "bold", SANS))
        body.append(px_text(x + 16, y + 60, tag, 13, DIM))
        fx, fy = x + 120, y + 240
        body.append(panel(fx, fy, fn(), SC))
        import textwrap
        yy = y + 650
        for s_ in lines:
            col = "#2f6f3a" if s_.startswith("+") else ("#9a2f1a" if s_.startswith("-") else INK)
            for j, part in enumerate(textwrap.wrap(s_, 58, subsequent_indent="  ")):
                body.append(px_text(x + 16, yy, part, 11.5, col))
                yy += 16
            yy += 3
    head = (px_text(60, 62, "talk.01 · ROUND 5 · EIGHT RETRO PUSH-TO-TALK DEVICES", 30, INK, "bold", SANS) +
            px_text(60, 92, "each starts from one real kind of old device · grilles are lines, slots or dot-matrix · panels are colour-blocked", 15, DIM) +
            px_text(1860, 52, "TENTATIVE · NOT A FINAL DESIGN", 13, ORANGE, "bold", MONO, "end") +
            px_text(1860, 72, "original concepts · same scale in every card (10 mm = 40 px)", 12, DIM, "normal", MONO, "end") +
            px_text(1860, 92, "all: USB-C on top · small hatch, no full-back cover · three-stage PTT", 12, DIM, "normal", MONO, "end") +
            px_text(60, 128, "These are not variations of one shape. Pick the ones that feel right; ignore the rest.", 14, INK, "normal", MONO))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1940" width="1920" height="1940"><defs>{"".join(DEFS)}</defs>'
           f'<rect width="1920" height="1940" fill="{PAPER}"/>{head}{"".join(body)}</svg>')
    write(out, "round5.svg", svg)


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else ".")
