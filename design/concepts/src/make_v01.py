#!/usr/bin/env python3
"""talk.01 v0.1: the converged concept (owner decisions of 2026-11-26).

Layout: a thumb wheel (an edge roller sunk in a pocket; its axis is perpendicular to the face, so from the front it
is a circle) on the left; one big key with a few stages on the right (a mature TE-style lever; no pop-up strip,
no sleeve, no squeeze). USB-C and a coiled cable on top; a small hatch and a small U stand on the back.
TE-style flat graphics: colour-blocked panels, small monospace labels, pictograms, screws. Two skins: Sand and Poppy.

  concept.svg      : the two skins, the sides, the back and a detail
  how-it-works.svg : the key and the wheel in section, the stages, and the wheel axis

Standard library only. Dimensions are TENTATIVE.

    python3 design/concepts/src/make_v01.py design/concepts/v0.1
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_concepts import (INK, PAPER, DIM, ORANGE, f, rr, circ, line, poly, path, t,  # noqa: E402
                           panel, px_text, write, SANS, MONO)
from make_round5 import mix, grad, hlines, vslots, plug_notch, coil  # noqa: E402
from make_round4 import screw  # noqa: E402
from make_round6 import rainbow, ghost, zigzag  # noqa: E402
from make_round4 import zoom  # noqa: E402
from make_lineup import lean  # noqa: E402
from make_back import rear_closed  # noqa: E402
import make_round5 as r5  # noqa: E402

SC = 4.5
W, H = 58, 92


# ---------------------------------------------------------------- small pieces
def icon(kind, x, y, c):
    """Tiny 2 mm pictograms for the four modes."""
    if kind == "dict":     # a text cursor and two lines
        return line(x, y - 1.1, x, y + 1.1, c, 0.3) + line(x + 0.9, y - 0.5, x + 2.3, y - 0.5, c, 0.3) + line(x + 0.9, y + 0.5, x + 2.0, y + 0.5, c, 0.3)
    if kind == "talk":     # a speech triangle
        return poly([(x - 0.2, y - 1.0), (x + 1.8, y - 1.0), (x + 1.8, y + 0.8), (x + 0.9, y + 0.8), (x - 0.2, y + 1.7)], "none", c, 0.3)
    if kind == "open":     # a ring with a dot
        return circ(x + 1, y, 1.1, "none", c, 0.3) + circ(x + 1, y, 0.35, c, "none", 0.0)
    return rr(x, y - 0.1, 2.0, 1.4, 0.3, "none", c, 0.3) + path(f"M{f(x + 0.4)},{f(y - 0.1)} v-0.6 a0.6,0.6 0 0 1 1.2,0 v0.6", "none", c, 0.3)


MODES = (("dict", "DICT"), ("talk", "TALK"), ("open", "OPEN"), ("lock", "LOCK"))


def wheel(g, cy, base, rib, pocket, ink, cur=1, cx=5.0, r=8.0):
    """A thumb wheel whose axis is perpendicular to the face: from the front it is a circle, sunk in a pocket on the left edge."""
    g.append(circ(cx, cy, r + 1.8, pocket, "#000", 0.4))
    g.append(circ(cx, cy, r, base, "#000", 0.45))
    for k in range(30):
        a = math.radians(k * 12)
        g.append(line(cx + (r - 1.4) * math.sin(a), cy - (r - 1.4) * math.cos(a), cx + r * math.sin(a), cy - r * math.cos(a), rib, 0.5))
    g.append(circ(cx, cy, r * 0.6, mix(base, 0.1), mix(base, -0.4), 0.3))
    ang = [45, 78, 112, 145][cur]
    a = math.radians(ang)
    g.append(line(cx, cy, cx + r * 0.58 * math.sin(a), cy - r * 0.58 * math.cos(a), "#f2efe6", 0.9, 'stroke-linecap="round"'))
    g.append(circ(cx, cy, 0.9, "#f2efe6", "none", 0.0))
    for k, (ik, lab) in enumerate(MODES):
        aa = math.radians([45, 78, 112, 145][k])
        x, y = cx + 17.5 * math.sin(aa), cy - 17.5 * math.cos(aa)
        col = "#c9461e" if k == cur else ink
        g.append(icon(ik, x - 0.2, y, col))
        g.append(t(x + 2.9, y + 0.6, lab, 1.6, "start", col, "bold" if k == cur else "normal", MONO))


def big_key(g, kind, color, edge, ink):
    """The one big key on the right edge: slanted like the TE lever, or parallel."""
    if kind == "slanted":
        g.append(ghost(58, 14, 6, 72, 2))
        g.append(poly([(58, 14), (64.4, 19), (61.6, 85), (58, 87)], color, edge, 0.55, 'stroke-linejoin="round"'))
        for k in range(7):
            yy = 30 + k * 7
            xo = 58 + 6.0 * (1 - (yy - 19) / 66) + 0.4
            g.append(line(58.8, yy, xo, yy + 0.4, mix(color, -0.3), 0.4))
        g.append(f'<g transform="translate(60.6,56) rotate(-90)">{t(0, 0, "TALK", 2.6, "middle", ink, "bold", MONO)}</g>')
    else:
        g.append(rr(58, 14, 6.5, 72, 3, color, edge, 0.55))
        g.append(line(58, 14, 58, 86, mix(color, -0.45), 0.4))
        for k in range(8):
            g.append(line(59.2, 26 + k * 6.6, 63.4, 26 + k * 6.6, mix(color, -0.3), 0.4))
        g.append(f'<g transform="translate(61.6,56) rotate(-90)">{t(0, 0, "TALK", 2.6, "middle", ink, "bold", MONO)}</g>')


def front(sp):
    g = [rr(0, 0, W, H, 5, grad(sp["gid"], sp["lower"], 0.06), sp["edge"], 0.5)]
    # upper colour block (the grille panel)
    g.append(rr(0, 0, W, 50, 5, sp["upper"], sp["edge"], 0.5))
    g.append(rr(0.3, 40, W - 0.6, 10, 0, sp["upper"], "none", 0.0))
    g.append(line(0.3, 50, W - 0.3, 50, sp["edge"], 0.5))
    if sp["grille"] == "lines":
        g.append(hlines(9, 9, 40, 9, 3.6, 1.6, sp["slot"]))
    else:
        g.append(vslots(10, 8.5, 33, 10, 4.2, 2.0, sp["slot"]))
    g.append(circ(29, 25.5, 1.5, sp["mic"], "none", 0.0))
    for (sx, sy) in ((4.6, 4.6), (53.4, 4.6), (4.6, 45.4), (53.4, 45.4)):
        g.append(screw(sx, sy, 1.3))
    # lower panel: wheel with its mode scale, lamp, wordmark and a few small prints
    wheel(g, 65, sp["wheel"], sp["rib"], sp["pocket"], sp["ink"], 1)
    g.append(circ(48, 57, 1.7, "#e03b2d", "#4a0f0a", 0.2))
    g.append(t(48, 61.8, "ON AIR", 1.4, "middle", sp["ink"], "normal", MONO))
    g.append(rainbow(10, 83.6, 8, 3.0))
    g.append(t(20, 86.4, "talk.01", 3.2, "start", sp["ink"], "bold", SANS))
    g.append(t(35, 80.4, "USB MIC + KEYS", 1.4, "start", sp["ink"], "normal", MONO))
    g.append(t(35, 83.2, "v0.1", 1.4, "start", "#c9461e", "bold", MONO))
    big_key(g, sp["key"], sp["keyc"], sp["keyedge"], sp["keyink"])
    g += [plug_notch(35, sp["edge"]), coil(35, 0, 6, 2.6, 7, sp["coil"])]
    return "".join(g)


SKINS = [
    dict(name="SAND", sub="beige + teal · slanted key", gid="v1", upper="#3d9aa1", lower="#e8e1cf", edge="#1f3d40", grille="lines", slot="#26696e", mic="#143c40",
         wheel="#2f7f85", rib="#bfe3e6", pocket="#1f5a5f", ink="#4a463e", key="slanted", keyc="#3d9aa1", keyedge="#1f5a5f", keyink="#e9f4f4", coil="#3d9aa1"),
    dict(name="POPPY", sub="cream + red · parallel key", gid="v2", upper="#2b2a28", lower="#efe9d9", edge="#1b1a18", grille="slots", slot="#d6d2c2", mic="#e9dfc0",
         wheel="#d8483c", rib="#f6b9b0", pocket="#4a110c", ink="#4a463e", key="parallel", keyc="#d8483c", keyedge="#6e1a12", keyink="#ffe9e6", coil="#d8483c"),
]


def side_local(sp, which):
    D = 22
    g = [rr(0, -H, D, H, 5, sp["lower"], sp["edge"], 0.45), rr(0, -H, D, 50, 5, sp["upper"], sp["edge"], 0.45), rr(0, -52, D, 10, 0, sp["upper"], "none", 0.0)]
    if which == "right":
        g.append(rr(5, -78, 12, 72, 5.5, sp["keyc"], sp["keyedge"], 0.4))
    else:
        g.append(circ(11, -24, 8.5, sp["pocket"], "#000", 0.4))
        g.append(rr(6, -32, 10, 16, 3, sp["wheel"], "#000", 0.35))
    g.append(rr(0, -84, 1.6, 26, 0.6, "#d9d2bd", "#7a7667", 0.2))
    return "".join(g)


def concept(out):
    body = [px_text(60, 62, "talk.01 · v0.1 · THE CONVERGED CONCEPT", 30, INK, "bold", SANS),
            px_text(60, 92, "a thumb wheel on the left · one big key on the right · TE-style flat graphics · matte print · two skins to choose from", 15, DIM),
            px_text(1860, 52, "TENTATIVE · NOT A FINAL DESIGN", 13, ORANGE, "bold", MONO, "end"),
            px_text(1860, 72, "original concept · dimensions are guesses · front views at 10 mm = 45 px", 12, DIM, "normal", MONO, "end")]
    for i, sp in enumerate(SKINS):
        x = 80 + i * 470
        body.append(px_text(x, 150, f'{sp["name"]}', 22, INK, "bold", SANS))
        body.append(px_text(x, 172, sp["sub"], 12, DIM))
        body.append(panel(x + 40, 330, front(sp), SC))
    # sides and back
    x0 = 1030
    body.append(px_text(x0, 150, "SIDES · BACK · DESK", 20, INK, "bold", SANS))
    body.append(px_text(x0, 190, "left side (wheel)", 11.5, DIM))
    body.append(panel(x0, 510, side_local(SKINS[0], "left"), 3.2))
    body.append(px_text(x0 + 150, 190, "right side (key)", 11.5, DIM))
    body.append(panel(x0 + 150, 510, side_local(SKINS[0], "right"), 3.2))
    body.append(px_text(x0 + 290, 190, "back (closed)", 11.5, DIM))
    body.append(panel(x0 + 290, 200, rear_closed(), 3.2))
    body.append(px_text(x0 + 530, 190, "on a desk", 11.5, DIM))
    body.append(lean(x0 + 700, 520, 30, 92, 22, 40, 48, side_local(SKINS[0], "right"), "#4a463e", 2.6))
    # detail zoom
    body.append(px_text(x0, 610, "3 CM DETAIL: the wheel, its scale and the pocket", 14, INK, "bold", MONO))
    body.append(zoom(x0, 630, front(SKINS[0]), -5, 49, 36, 36, 91))
    body.append(zoom(x0 + 270, 630, front(SKINS[1]), -5, 49, 36, 36, 92))
    notes = [("What is settled (owner, 2026-11-26)", INK, "bold"),
             ("· left: a thumb wheel (an edge roller, its axis perpendicular to the face, sunk in a pocket). Four detents: DICT, TALK, OPEN, LOCK.", INK, "normal"),
             ("· right: one big key with a few stages: the mature TE-style lever. Slanted or parallel, both are fine.", INK, "normal"),
             ("· no pop-up strip, no sleeve, no squeeze, no glowing window in v0.1 (they are in the backlog).", INK, "normal"),
             ("· USB-C and a coiled cable on top; a small hatch and a small U stand on the back; matte printed parts.", INK, "normal"),
             ("", INK, "normal"),
             ("Still open", "#9a2f1a", "bold"),
             ("· body depth (about 22 mm drawn);  · two key stages or three;  · the exact printed labels;  · which skin.", "#9a2f1a", "normal")]
    import textwrap
    lines_, yy = [], 920
    for (txt, col, wt) in notes:
        for part in (textwrap.wrap(txt, 96, subsequent_indent="  ") or [""]):
            lines_.append(px_text(x0, yy, part, 12, col, wt))
            yy += 17
    body.append("".join(lines_))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1180" width="1920" height="1180"><defs>{"".join(r5.DEFS)}</defs>'
           f'<rect width="1920" height="1180" fill="{PAPER}"/>{"".join(body)}</svg>')
    write(out, "concept.svg", svg)


# ---------------------------------------------------------------- how it works
def lab(x, y, tx, ty, text, anchor="start", col=INK):
    return line(x, y, tx, ty, "#8a857a", 0.8) + circ(x, y, 3, "#8a857a", "none", 0.0) + px_text(tx + (6 if anchor == "start" else -6), ty + 4, text, 12.5, col, "normal", MONO, anchor)


def section(sp):
    """A simple front section (mm): the wheel on the left, the board in the middle, the key on the right."""
    g = [rr(0, 0, W, H, 5, "#e0dac8", "#6f6a5e", 0.45)]
    # board with USB-C on top
    g += [rr(18, 4, 22, 18, 1.2, "#2f6b52", "#173d2e", 0.3), rr(24.5, 2.4, 9, 3.8, 0.8, "#cfcfcf", INK, 0.2)]
    # wheel (circle), its pin and a small encoder behind
    g += [rr(9, 56, 10, 8, 1, "#444", "#222", 0.3), circ(5, 68, 9.8, "#1f5a5f", "#000", 0.4), circ(5, 68, 8, "#2f7f85", "#000", 0.4), circ(5, 68, 1.6, "#cfcfcf", "#444", 0.3)]
    for k in range(30):
        a = math.radians(k * 12)
        g.append(line(5 + 6.6 * math.sin(a), 68 - 6.6 * math.cos(a), 5 + 8 * math.sin(a), 68 - 8 * math.cos(a), "#bfe3e6", 0.4))
    g.append(rr(9.4, 64, 3, 8, 0.8, "#b8b19c", "#555", 0.2))          # click ring ball
    # key hinged at the bottom of the right edge: resting (slanted) and pressed (dashed)
    g.append(poly([(58, 14), (58, 87), (54, 87), (54, 14)], "none", "#8a857a", 0.3).replace("<polygon ", '<polygon stroke-dasharray="1.2 0.8" '))
    g.append(poly([(58, 14), (64.4, 19), (61.6, 85), (58, 87)], "#3d9aa1", "#1f5a5f", 0.55, 'stroke-linejoin="round"'))
    g.append(zigzag(50, 36, 60.6, 36, 5, 1.0, "#5a5750"))
    g += [rr(46, 33, 6, 6, 1, "#555", "#222", 0.3)]                      # spring pocket
    g += [rr(50.4, 50, 3.4, 4, 0.5, "#111", "#000", 0.2), rr(50.4, 64, 3.4, 4, 0.5, "#111", "#000", 0.2)]   # two switches
    g += [rr(50.6, 22, 3, 3.4, 0.5, "#2b2a28", "#000", 0.2), rr(59.4, 21.4, 1.6, 3.2, 0.4, "#e9873a", "#6b2509", 0.2)]  # hall + magnet
    g.append(circ(58, 87, 1.7, "#c9a24b", "#4d3d12", 0.3))               # hinge pin
    return "".join(g)


def wheel_axis_inset():
    g = [circ(14, 14, 10, "#2f7f85", "#000", 0.5), circ(19, 9, 10, "#256a70", "#000", 0.5)]
    g.append(line(4.6, 8.4, 9.6, 3.4, "#000", 0.4)); g.append(line(23.4, 20.6, 28.4, 15.6, "#000", 0.4))
    g.append(path("M14,14 L9,19", "none", "#c9461e", 0.8))
    g.append(poly([(8.2, 19.8), (11.4, 19.2), (9.2, 16.8)], "#c9461e", "#c9461e", 0.05))
    for k in range(30):
        a = math.radians(k * 12)
        g.append(line(14 + 8 * math.sin(a), 14 - 8 * math.cos(a), 14 + 10 * math.sin(a), 14 - 10 * math.cos(a), "#bfe3e6", 0.4))
    g.append(circ(14, 14, 1.4, "#cfcfcf", "#444", 0.3))
    return "".join(g)


def how(out):
    body = [px_text(60, 62, "talk.01 · v0.1 · HOW IT WORKS (kept simple)", 30, INK, "bold", SANS),
            px_text(60, 92, "a front section: the thumb wheel on the left, the board at the top, the one big key on the right", 15, DIM),
            px_text(1860, 52, "TENTATIVE · NOT ENGINEERED", 13, ORANGE, "bold", MONO, "end")]
    ox, oy, sc = 900, 130, 7.0
    body.append(panel(ox, oy, section(SKINS[0]), sc))
    X = lambda x: ox + x * sc
    Y = lambda y: oy + y * sc
    body += [lab(X(29), Y(13), X(-1) - 40, Y(8), "dev board with USB-C on top", "end"),
             lab(X(5), Y(68), X(-1) - 40, Y(66), "THUMB WHEEL: a ribbed disc, a pin through its centre", "end"),
             lab(X(11), Y(68), X(-1) - 40, Y(76), "spring-ball click: four detents", "end"),
             lab(X(11), Y(60), X(-1) - 40, Y(54), "small encoder reads the position", "end"),
             lab(X(59.6), Y(30), X(66) + 40, Y(26), "BIG KEY: hinged at the bottom,", "start"),
             lab(X(56), Y(36), X(66) + 40, Y(40), "a spring holds it out (slanted)", "start"),
             lab(X(52), Y(52), X(66) + 40, Y(56), "switch 1: HOLD (talk while held)", "start"),
             lab(X(52), Y(66), X(66) + 40, Y(70), "switch 2: CLICK at the bottom (latch)", "start"),
             lab(X(52), Y(23), X(66) + 40, Y(14), "Hall sensor + magnet (optional)", "start"),
             lab(X(58), Y(87), X(66) + 40, Y(88), "steel hinge pin", "start")]
    body.append(px_text(60, 150, "THE WHEEL", 18, INK, "bold", SANS))
    body.append(px_text(60, 172, "its axis is perpendicular to the face:", 12, DIM))
    body.append(px_text(60, 188, "from the front it is a circle.", 12, DIM))
    body.append(panel(60, 205, wheel_axis_inset(), 6))
    body.append(px_text(60, 360, "the thumb strokes the rim up and", 12, INK))
    body.append(px_text(60, 376, "down along the left edge.", 12, INK))
    body.append(px_text(60, 400, "(My earlier roller drawing was a ribbed", 12, "#9a2f1a"))
    body.append(px_text(60, 416, "bar, which reads as a sideways axis.", 12, "#9a2f1a"))
    body.append(px_text(60, 432, "That was a drawing error; fixed.)", 12, "#9a2f1a"))
    stages = [("rest", "the spring holds the key out", "READY"), ("press to mid-travel", "switch 1 closes", "TALK: key held while pressed"),
              ("press to the bottom", "switch 2 closes (a click)", "LATCH: hands-free"), ("firm push past the click", "Hall sensor (optional)", "SEND")]
    body.append(px_text(60, 840, "THE KEY'S STAGES (the TE lever's idea)", 18, INK, "bold", SANS))
    for k, (a, b, c) in enumerate(stages):
        yy = 870 + k * 24
        body.append(px_text(60, yy, a, 13, INK, "bold", MONO))
        body.append(px_text(330, yy, b, 13, INK, "normal", MONO))
        body.append(px_text(640, yy, c, 13, "#2f6f3a", "bold", MONO))
    body.append(px_text(60, 990, "v0.1 can start with ONE stage (switch 1) and add the rest later: the parts are ordinary micro-switches.", 12.5, DIM))
    body.append(px_text(60, 1008, "Bag safety without a sleeve: the key sits between two raised shoulders, and the wheel's LOCK position makes the firmware ignore it.", 12.5, DIM))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1050" width="1920" height="1050"><defs>{"".join(r5.DEFS)}</defs>'
           f'<rect width="1920" height="1050" fill="{PAPER}"/>{"".join(body)}</svg>')
    write(out, "how-it-works.svg", svg)


if __name__ == "__main__":
    o = sys.argv[1] if len(sys.argv) > 1 else "."
    concept(o)
    how(o)
