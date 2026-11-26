#!/usr/bin/env python3
"""talk.01 v0.4 study: the WHOLE lower half is one cover plate (a lid), with a round hole showing through it.

The owner's references (a ridged cover over a round hole, a dot-matrix grille, a square grid over round speaker cones) point to a
full-width plate rather than a small plate inset in the face. Four patterns on that one plate: horizontal ridges, vertical ridges,
a square grid, and dots. Outside the round hole the pattern is relief only; inside it the gaps go through to the dark hole.
Controls stay above (key upper-left, wheel in the top-right chamfer).

    python3 design/concepts/src/make_v04.py design/concepts/v0.4

Standard library only. Dimensions are TENTATIVE.
"""
import math
import os
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_concepts import INK, PAPER, DIM, ORANGE, f, rr, circ, line, poly, path, t, panel, px_text, write, SANS, MONO  # noqa: E402
from make_round5 import mix  # noqa: E402
from make_round4 import screw  # noqa: E402
from make_round6 import rainbow  # noqa: E402
from make_v01 import SKINS  # noqa: E402
from make_v02 import body_path, W, H, WX  # noqa: E402
from make_v03 import scale_row, head, tail, RED  # noqa: E402
import make_round5 as r5  # noqa: E402

SPLIT = 36.0                  # the seam between the control zone and the plate (mm)
CX, CY, CR = 29.0, 64.0, 19.0  # the round hole under the plate
HOLE = "#0c0b0a"


def R(x, y, w, h, c):
    return f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" fill="{c}"/>'


def disc_clip(cid, inner):
    return f'<clipPath id="{cid}">{circ(CX, CY, CR, "#000", "none", 0)}</clipPath><g clip-path="url(#{cid})">{inner}</g>'


def ridges(horizontal, col, gap, with_gap=True):
    """Relief ridges: a ridge 1.9 mm wide, a gap 1.1 mm, a light line along each ridge's top edge."""
    g, k = [], 0
    hi = mix(col, 0.28)
    n = int(((H - SPLIT) if horizontal else W) / 3.0) + 1
    for k in range(n):
        if horizontal:
            y = SPLIT + 1.2 + k * 3.0
            if y > H:
                break
            if with_gap:
                g.append(R(0, y + 1.9, W, 1.1, gap))
            g.append(R(0, y, W, 1.9, col))
            g.append(line(0, y + 0.22, W, y + 0.22, hi, 0.35))
        else:
            x = 1.6 + k * 3.0
            if x > W:
                break
            if with_gap:
                g.append(R(x + 1.9, SPLIT, 1.1, H - SPLIT, gap))
            g.append(R(x, SPLIT, 1.9, H - SPLIT, col))
            g.append(line(x + 0.22, SPLIT, x + 0.22, H, hi, 0.35))
    return "".join(g)


def plate(kind, col, bid):
    """The whole lower half as one plate. Returns SVG for the plate, its seam and its four corner screws."""
    g = [f'<clipPath id="{bid}b"><path d="{body_path()}"/></clipPath><g clip-path="url(#{bid}b)">']
    shade = mix(col, -0.32)
    g.append(R(0, SPLIT, W, H - SPLIT, col))
    if kind in ("hridge", "vridge"):
        horiz = kind == "hridge"
        g.append(ridges(horiz, col, shade))
        g.append(disc_clip(bid + "c", circ(CX, CY, CR, HOLE, "none", 0) + ridges(horiz, col, shade, with_gap=False)))
    elif kind == "grid":
        sq = []
        for i in range(21):
            for j in range(21):
                x, y = 2.4 + i * 2.6, SPLIT + 2.2 + j * 2.6
                if x + 1.7 < W - 1.5 and y + 1.7 < H - 1.5:
                    sq.append(R(x, y, 1.7, 1.7, shade))
        g.append("".join(sq))
        bars = "".join(R(2.4 + i * 2.6 - 0.9, SPLIT, 0.9, H - SPLIT, col) for i in range(22)) + "".join(R(0, SPLIT + 2.2 + j * 2.6 - 0.9, W, 0.9, col) for j in range(22))
        g.append(disc_clip(bid + "c", circ(CX, CY, CR, HOLE, "none", 0) + bars))
    else:  # dots
        dots = []
        for i in range(21):
            for j in range(21):
                x, y = 2.9 + i * 2.7 + (1.35 if j % 2 else 0), SPLIT + 2.6 + j * 2.35
                if x < W - 1.5 and y < H - 1.5:
                    dots.append(circ(x, y, 0.55, shade, "none", 0))
        g.append("".join(dots))
        holes = []
        for i in range(21):
            for j in range(21):
                x, y = 2.9 + i * 2.7 + (1.35 if j % 2 else 0), SPLIT + 2.6 + j * 2.35
                holes.append(circ(x, y, 0.95, HOLE, "none", 0))
        g.append(disc_clip(bid + "c", circ(CX, CY, CR, col, "none", 0) + "".join(holes)))
    g.append(line(0, SPLIT, W, SPLIT, "#1b1a18", 0.55))
    g.append(line(0, SPLIT + 0.7, W, SPLIT + 0.7, mix(col, 0.35), 0.3))
    g.append("</g>")
    for (sx, sy) in ((4.4, SPLIT + 4.4), (W - 4.4, SPLIT + 4.4), (4.4, H - 4.4), (W - 4.4, H - 4.4)):
        g.append(circ(sx, sy, 1.9, mix(col, -0.12), mix(col, -0.4), 0.3))
        g.append(screw(sx, sy, 1.15))
    return "".join(g)


def front(sp, kind, col, bid, light_upper=True):
    g = []
    head(g, sp, bid)
    g.append(plate(kind, col, bid))
    scale_row(g, 5.6, 15.0, sp["ink"], RED)
    g.append(t(6, 29.6, "talk.01", 5.0, "start", sp["ink"], "bold", SANS))
    g.append(rainbow(30, 25.6, 9, 2.4))
    g.append(circ(51, 31.0, 1.7, "#e03b2d", "#4a0f0a", 0.2))
    g.append(t(51, 34.9, "ON AIR", 1.2, "middle", sp["ink"], "normal", MONO))
    g.append(t(WX - 1.5, 24.2, "MODE", 1.4, "middle", sp["ink"], "normal", MONO))
    tail(g, sp, bid, sp["wheel"], sp["rib"], sp["pocket"])
    return "".join(g)


def section():
    """Section across a ridged plate (mm, front at the top): ridges up, a thin base, slots through only over the round hole."""
    g = []
    base = "#3d9aa1"
    g.append(rr(0, 1.6, 44, 1.0, 0.2, base, "#1f5a5f", 0.15))                          # the thin plate base
    for k in range(14):
        x = 0.6 + k * 3.0
        g.append(rr(x, 0.2, 1.9, 1.5, 0.35, base, "#1f5a5f", 0.15))                    # a ridge, 1.4 mm tall, rounded
    for k in range(5, 10):
        x = 0.6 + k * 3.0 + 1.9
        g.append(rr(x + 0.05, 1.5, 1.0, 1.2, 0, "#f4f0e4", "none", 0))                 # slots cut through the base (over the hole only)
    for x in (0.5, 42.5):
        g.append(rr(x, 2.6, 1.2, 2.2, 0.3, "#9a9585", "#555", 0.15))                    # screw bosses
    g.append(rr(0, 4.8, 12, 2.0, 0.4, "#e8e1cf", "#6f6a5e", 0.2))
    g.append(rr(32, 4.8, 12, 2.0, 0.4, "#e8e1cf", "#6f6a5e", 0.2))                      # front wall, open in the middle (the round hole)
    g.append(rr(12, 3.6, 20, 0.6, 0.2, "#bdb6a2", "#7a7667", 0.12))                     # felt across the hole
    g.append(rr(14, 8.4, 16, 1.6, 0.3, "#2f6b52", "#173d2e", 0.2))
    g.append(rr(20.2, 7.0, 3.6, 1.4, 0.3, "#222", "#000", 0.15))                        # MEMS mic, port towards the hole
    return "".join(g)


def lab(x, y, tx, ty, text):
    return line(x, y, tx, ty, "#8a857a", 0.8) + circ(x, y, 3, "#8a857a", "none", 0.0) + px_text(tx + 6, ty + 4, text, 11.5, INK, "normal", MONO)


def study(out):
    sand, poppy = SKINS[0], SKINS[1]
    body = [px_text(60, 62, "talk.01 · v0.4 study · THE WHOLE LOWER HALF IS ONE COVER PLATE", 28, INK, "bold", SANS),
            px_text(60, 92, "a lid with a pattern over a round hole · four patterns · controls above (key upper-left, wheel in the top-right corner)", 15, DIM),
            px_text(1860, 52, "TENTATIVE · NOT A FINAL DESIGN", 13, ORANGE, "bold", MONO, "end"),
            px_text(1860, 72, "front views at 10 mm = 42 px", 12, DIM, "normal", MONO, "end")]
    sets = [("G1  RIDGES", "horizontal relief ridges · SAND", "hridge", "#3d9aa1", sand, "g1",
             "The old-radio classic. The round hole shows where the gaps go through to the dark.",
             "Risk: the nearest to your first reference; keep our own proportions, colour and the control zone above."),
            ("G2  TALL RIDGES", "vertical relief ridges · POPPY", "vridge", "#d8483c", poppy, "g2",
             "Same idea turned 90 degrees: reads as a speaker slat, and prints without bridging over long spans.",
             "Risk: vertical ridges in red next to a red key may be too much red."),
            ("G3  GRID", "square grid · SAND", "grid", "#d6d0bd", sand, "g3",
             "A square grid over the round hole (like your third picture): the circle appears behind the mesh.",
             "Risk: fine grids are slow to print and may string; larger squares help."),
            ("G4  DOTS", "dot matrix · SAND", "dots", "#3a3935", sand, "g4",
             "Dark plate, tiny dimples outside the circle and real holes inside it: the dot-matrix look of your second picture.",
             "Risk: the darkest option; many small holes to print.")]
    sc = 4.2
    for i, (name, sub, kind, col, sp, bid, why, risk) in enumerate(sets):
        x = 70 + i * 345
        body.append(panel(x + 24, 218, front(sp, kind, col, bid), sc))
        body.append(px_text(x + 4, 640, name, 18, INK, "bold", SANS))
        body.append(px_text(x + 4, 660, sub, 11.5, DIM))
        yy = 688
        for ln, c in ((why, INK), (risk, "#9a2f1a")):
            for k2, part in enumerate(textwrap.wrap(ln, 44)):
                body.append(px_text(x + 4, yy, ("· " if k2 == 0 else "  ") + part, 11.5, c))
                yy += 15
            yy += 8
    # section and notes
    ox, oy, sc2 = 1500, 215, 8.2
    body.append(px_text(ox - 6, 150, "A RIDGED PLATE (section, a sketch)", 15, INK, "bold", SANS))
    body.append(panel(ox, oy, section(), sc2))
    X = lambda x: ox + x * sc2
    Y = lambda y: oy + y * sc2
    body += [lab(X(10), Y(0.6), ox - 6, 335, "ridges 1.4 mm tall, rounded"),
             lab(X(18.5), Y(2.2), ox - 6, 357, "slots through only over the hole"),
             lab(X(22), Y(3.9), ox - 6, 379, "felt behind the plate"),
             lab(X(22), Y(7.8), ox - 6, 401, "MEMS mic, port towards the hole")]
    notes = ["The plate is one lid:",
             "· four corner screws; it comes off. That makes patterns swappable and lets us test the sound with and without a plate (the 'removable cover system' already in the backlog).",
             "· over the hole the gaps go through; elsewhere the ridges, grid or dots are relief only, so the plate is stiffer and prints easier.",
             "· print it face up so the ridges build upward. Whether a 1.1 mm gap prints cleanly on your printer is untested.",
             "· the plate is the part your hand rests on, so ridges are rounded (0.4 mm or more) and run across the grip.",
             "",
             "About the pictures you sent:",
             "· I used them for the idea only: a cover over a round hole; relief ridges, dots, a grid.",
             "· The first carries a 'TING FX' mark and a site watermark; I have not checked who made it. No shapes are copied: our proportions, our control zone, colours and graphics differ, and the plate is a separate lid.",
             "· The pictures are not stored in the repository."]
    yy = 450
    for k, ln in enumerate(notes):
        for part in (textwrap.wrap(ln, 52, subsequent_indent="  ") or [""]):
            body.append(px_text(ox - 6, yy, part, 11, INK if ln.endswith(":") else DIM, "bold" if ln.endswith(":") else "normal"))
            yy += 14
        yy += 3
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 900" width="1920" height="900"><defs>{"".join(r5.DEFS)}</defs>'
           f'<rect width="1920" height="900" fill="{PAPER}"/>{"".join(body)}</svg>')
    write(out, "plate.svg", svg)


if __name__ == "__main__":
    study(sys.argv[1] if len(sys.argv) > 1 else ".")
