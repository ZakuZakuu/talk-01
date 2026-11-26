#!/usr/bin/env python3
"""talk.01 v0.3 study: controls in the upper part, ONE BIG PICKUP AREA in the lower part (TE's layout turned upside down).

The pickup area is a round hole under a square cover plate (the old radio / speaker idea: a circle inside a square), with the
plate's pattern as horizontal lines, vertical slots or small holes. Three variants, all with the key upper-left and the wheel
in the top-right chamfer (v0.2), plus a section of the plate over the hole.

    python3 design/concepts/src/make_v03.py design/concepts/v0.3

Standard library only. Dimensions are TENTATIVE.
"""
import math
import os
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_concepts import INK, PAPER, DIM, ORANGE, f, rr, circ, line, poly, path, t, panel, px_text, write, SANS, MONO  # noqa: E402
from make_round5 import mix, hlines, vslots, dots_disc, plug_notch, coil  # noqa: E402
from make_round4 import screw  # noqa: E402
from make_round6 import rainbow  # noqa: E402
from make_v01 import icon, MODES  # noqa: E402
from make_v02 import body_path, corner_wheel, left_key, W, H, WX  # noqa: E402
import make_round5 as r5  # noqa: E402

RED = "#c9461e"
PX, PY, PW, PH = 6.0, 38.0, 46.0, 48.0          # the cover plate (mm)
CX, CY, CR = 29.0, 62.0, 18.5                    # the round hole under it


def scale_row(g, x, y, ink, cur_col, cur=1):
    for k, (ik, lab) in enumerate(MODES):
        px = x + k * 8.6
        col = cur_col if k == cur else ink
        g.append(icon(ik, px, y, col))
        g.append(t(px + 2.9, y + 0.6, lab, 1.5, "start", col, "bold" if k == cur else "normal", MONO))


def clip_disc(g, cid, inner):
    g.append(f'<clipPath id="{cid}">{circ(CX, CY, CR, "#000", "none", 0)}</clipPath><g clip-path="url(#{cid})">{inner}</g>')


def head(g, sp, bid, upper_fill=None):
    """The body, the (optional) coloured upper block, the wheel, the key and the cable."""
    g.append(f'<path d="{body_path()}" fill="{sp["lower"]}" stroke="{sp["edge"]}" stroke-width="0.5"/>')
    if upper_fill:
        g.append(f'<clipPath id="{bid}u"><path d="{body_path()}"/></clipPath>'
                 f'<g clip-path="url(#{bid}u)">{rr(0, 0, W, 36, 0, upper_fill, "none", 0)}{line(0, 36, W, 36, sp["edge"], 0.5)}</g>')


def tail(g, sp, bid, wheel, rib, pocket):
    corner_wheel(g, bid, wheel, rib, pocket, sp["ink"], 1)
    left_key(g, sp["keyc"], sp["keyedge"], sp["keyink"])
    g += [plug_notch(29, sp["edge"]), coil(29, 0, 3, 2.6, 7, sp["coil"])]


def va_lines(sp, bid):
    """A: a teal plate; horizontal slots cut through the round hole, faint engraved lines continue to the plate edge."""
    g = []
    head(g, sp, bid)
    g.append(rr(PX, PY, PW, PH, 4, sp["upper"], sp["edge"], 0.5))
    for k in range(14):                                                # engraved lines across the whole plate
        yy = PY + 3.2 + k * 3.2
        g.append(line(PX + 2.2, yy, PX + PW - 2.2, yy, mix(sp["upper"], -0.18), 0.45))
    g.append(circ(CX, CY, CR + 0.8, mix(sp["upper"], -0.35), "none", 0))
    clip_disc(g, bid + "d", circ(CX, CY, CR, sp["mic"], "none", 0) + hlines(CX - CR, CY - CR + 1.4, 2 * CR, 11, 3.2, 1.7, sp["upper"]))
    for (sx, sy) in ((PX + 3, PY + 3), (PX + PW - 3, PY + 3), (PX + 3, PY + PH - 3), (PX + PW - 3, PY + PH - 3)):
        g.append(screw(sx, sy, 1.2))
    scale_row(g, 5.6, 15.0, sp["ink"], RED)
    g.append(t(6, 29.6, "talk.01", 5.0, "start", sp["ink"], "bold", SANS))
    g.append(rainbow(30, 25.6, 9, 2.4))
    g.append(circ(51, 31.0, 1.7, "#e03b2d", "#4a0f0a", 0.2)); g.append(t(51, 35.6, "ON AIR", 1.3, "middle", sp["ink"], "normal", MONO))
    g.append(t(WX - 1.5, 24.2, "MODE", 1.4, "middle", sp["ink"], "normal", MONO))
    tail(g, sp, bid, sp["wheel"], sp["rib"], sp["pocket"])
    return "".join(g)


def vb_slots(sp, bid):
    """B: a dark plate with a cream ring round the hole; tall slots through the hole; four screws; a rainbow band under the controls."""
    g = []
    head(g, sp, bid)
    g.append(rr(PX, PY, PW, PH, 4, sp["upper"], sp["edge"], 0.5))
    g.append(circ(CX, CY, CR + 1.4, "none", "#e9dfc0", 0.5))
    clip_disc(g, bid + "d", circ(CX, CY, CR, "#0c0b0a", "none", 0) + vslots(CX - CR + 1.4, CY - CR, 2 * CR, 9, 3.9, 2.1, "#d6d2c2"))
    for (sx, sy) in ((PX + 3, PY + 3), (PX + PW - 3, PY + 3), (PX + 3, PY + PH - 3), (PX + PW - 3, PY + PH - 3)):
        g.append(screw(sx, sy, 1.2))
    scale_row(g, 5.6, 15.0, sp["ink"], RED)
    g.append(rainbow(0.6, 33.2, W - 1.2, 2.0))
    g.append(t(6, 29.0, "talk.01", 5.0, "start", sp["ink"], "bold", SANS))
    g.append(t(31, 28.6, "USB MIC + KEYS", 1.4, "start", sp["ink"], "normal", MONO))
    g.append(circ(51.4, 24.0, 1.5, "#e03b2d", "#4a0f0a", 0.2)); g.append(t(51.4, 28.6, "ON AIR", 1.3, "middle", sp["ink"], "normal", MONO))
    tail(g, sp, bid, sp["wheel"], sp["rib"], sp["pocket"])
    return "".join(g)


def vc_dots(sp, bid):
    """C: the upper block is colour (the control zone); below it a cream plate with a ring of small holes round the hole."""
    g = []
    head(g, sp, bid, upper_fill=sp["upper"])
    g.append(rr(PX, PY, PW, PH, 4, mix(sp["lower"], -0.06), sp["edge"], 0.5))
    g.append(circ(CX, CY, CR + 1.4, "none", sp["edge"], 0.4))
    g.append(circ(CX, CY, CR, sp["upper"], sp["edge"], 0.5))
    g.append(dots_disc(CX, CY, CR - 1.0, 2.7, 0.78, sp["mic"]))
    for k in range(36):
        a = math.radians(k * 10)
        g.append(line(CX + (CR + 2.1) * math.sin(a), CY - (CR + 2.1) * math.cos(a), CX + (CR + (3.1 if k % 3 == 0 else 2.7)) * math.sin(a),
                      CY - (CR + (3.1 if k % 3 == 0 else 2.7)) * math.cos(a), sp["ink"], 0.28))
    for (sx, sy) in ((PX + 2.6, PY + 2.6), (PX + PW - 2.6, PY + 2.6), (PX + 2.6, PY + PH - 2.6), (PX + PW - 2.6, PY + PH - 2.6)):
        g.append(screw(sx, sy, 1.1))
    cream = "#f2efe6"
    scale_row(g, 5.6, 15.0, cream, "#ffd37a")
    g.append(t(6, 30.0, "talk.01", 5.0, "start", cream, "bold", SANS))
    g.append(rainbow(30, 26.0, 9, 2.4))
    g.append(circ(51, 31.0, 1.7, "#e03b2d", "#4a0f0a", 0.2)); g.append(t(51, 35.0, "ON AIR", 1.3, "middle", cream, "normal", MONO))
    g.append(t(WX - 1.5, 24.2, "MODE", 1.4, "middle", cream, "normal", MONO))
    tail(g, sp, bid, "#e8e1cf", "#2f7f85", "#143c40")
    return "".join(g)


def section():
    """Section through the lower area (mm, front at the top): the cover plate, a small gap, the wall with the round hole, the mic behind."""
    g = []
    g.append(rr(0, 0, 46, 1.4, 0.4, "#3d9aa1", "#1f5a5f", 0.2))                       # cover plate with slots (drawn as gaps below)
    for k in range(7):
        g.append(rr(12 + k * 3.2, -0.2, 1.7, 1.8, 0.4, "#f4f0e4", "none", 0))
    for x in (1, 44):
        g.append(rr(x, 1.4, 1.2, 2.4, 0.3, "#9a9585", "#555", 0.15))                   # standoffs
    g.append(rr(0, 3.8, 5.0, 2.2, 0.4, "#e8e1cf", "#6f6a5e", 0.2))                      # front wall left of the hole
    g.append(rr(41, 3.8, 5.0, 2.2, 0.4, "#e8e1cf", "#6f6a5e", 0.2))                     # right of the hole
    g.append(rr(5.0, 3.0, 36, 0.6, 0.2, "#bdb6a2", "#7a7667", 0.12))                    # a fine mesh / felt across the hole
    g.append(rr(0, 6.0, 46, 1.2, 0.3, "#e8e1cf", "#6f6a5e", 0.2))                       # inner wall
    g.append(rr(16, 8.6, 14, 1.6, 0.3, "#2f6b52", "#173d2e", 0.2))                      # a small PCB
    g.append(rr(21.2, 7.2, 3.6, 1.4, 0.3, "#222", "#000", 0.15))                        # the MEMS microphone with its port facing the hole
    g.append(rr(22.6, 6.6, 0.8, 0.8, 0.2, "#fff", "none", 0))
    return "".join(g)


def lab(x, y, tx, ty, text, col=INK, anchor="start"):
    return line(x, y, tx, ty, "#8a857a", 0.8) + circ(x, y, 3, "#8a857a", "none", 0.0) + px_text(tx + (6 if anchor == "start" else -6), ty + 4, text, 12, col, "normal", MONO, anchor)


def study(out):
    from make_v01 import SKINS
    sand, poppy = SKINS[0], SKINS[1]
    body = [px_text(60, 62, "talk.01 · v0.3 study · CONTROLS ABOVE, ONE BIG PICKUP BELOW", 28, INK, "bold", SANS),
            px_text(60, 92, "TE's layout turned upside down · a round hole under a square cover plate (a circle inside a square) · key upper-left, wheel top-right", 15, DIM),
            px_text(1860, 52, "TENTATIVE · NOT A FINAL DESIGN", 13, ORANGE, "bold", MONO, "end"),
            px_text(1860, 72, "front views at 10 mm = 45 px", 12, DIM, "normal", MONO, "end")]
    sets = [("A  LINES", "teal plate, horizontal slots", va_lines, sand, "a",
             ["Lines are the most 'old radio' pattern; the engraved lines carry on across the plate, so the round hole reads as cut through a grille.",
              "Risk: with only the circle slotted, the plate corners are plain; keep or drop the engraved lines? (open)"]),
            ("B  SLOTS", "dark plate, tall slots", vb_slots, poppy, "b",
             ["The strongest contrast: a dark speaker panel with a pale ring. The rainbow band separates controls from pickup.",
              "Risk: the dark plate is heavy next to the cream upper part; the plate may be the colour instead."]),
            ("C  DOTS", "colour block above, ring of holes", vc_dots, sand, "c",
             ["Keeps the colour block of F1 as the control zone and puts the big dotted circle below it: nearest to the F3 idea.",
              "Risk: dots are the easiest to print but the least 'radio'; the tick ring does the radio work."])]
    for i, (name, sub, fn, sp, bid, notes) in enumerate(sets):
        x = 90 + i * 400
        body.append(panel(x + 40, 215, fn(sp, bid), 4.5))
        body.append(px_text(x + 8, 660, name, 20, INK, "bold", SANS))
        body.append(px_text(x + 8, 682, f'{sub} · skin {sp["name"]}', 11.5, DIM))
        for j, ln in enumerate(notes):
            for k2, part in enumerate(textwrap.wrap(ln, 46)):
                body.append(px_text(x + 8, 712 + j * 58 + k2 * 15, ("· " if k2 == 0 else "  ") + part, 11.5, INK if j == 0 else "#9a2f1a"))
    # section
    ox, oy, sc = 1290, 235, 7.4
    body.append(px_text(ox - 10, 150, "THE PLATE OVER THE HOLE (section, a sketch)", 16, INK, "bold", SANS))
    body.append(px_text(ox - 10, 172, "front of the body at the top", 12, DIM))
    body.append(panel(ox, oy, section(), sc))
    X = lambda x: ox + x * sc
    Y = lambda y: oy + y * sc
    body += [lab(X(8), Y(0.7), X(46) + 14, Y(-0.8), "cover plate (printed)"),
             lab(X(1.6), Y(2.6), X(46) + 14, Y(2.4), "standoffs: 1.5 mm gap"),
             lab(X(23), Y(3.3), X(46) + 14, Y(5.4), "fine mesh or felt"),
             lab(X(3), Y(5), X(46) + 14, Y(8.2), "wall with round hole"),
             lab(X(23), Y(7.9), X(46) + 14, Y(11.0), "MEMS mic, port to hole")]
    notes2 = ["What this changes, honestly:",
              "· the big circle is mostly STYLE. The microphone needs only a tiny port (about 1 mm); the big hole just has to leave a clear air path to it.",
              "· so the plate pattern can be whatever looks right, if the mesh and the gap do not block the air. That is cheap to test: print the plate and record with and without it.",
              "· no claim about sound is made here. Nothing has been recorded or measured.",
              "· lower pickup: when it leans back on its stand the mic sits close to the desk. Keep it off the desk by the stand's height; check for desk and key-tap noise.",
              "· F1 note: its slim strip made the pickup small; the upper/lower split gives the pickup roughly half the face."]
    yy = 560
    for k, ln in enumerate(notes2):
        for k2, part in enumerate(textwrap.wrap(ln, 66, subsequent_indent="  ")):
            body.append(px_text(ox - 10, yy, part, 11.5, INK if k == 0 else DIM, "bold" if k == 0 else "normal"))
            yy += 15
        yy += 4
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 900" width="1920" height="900"><defs>{"".join(r5.DEFS)}</defs>'
           f'<rect width="1920" height="900" fill="{PAPER}"/>{"".join(body)}</svg>')
    write(out, "pickup.svg", svg)


if __name__ == "__main__":
    study(sys.argv[1] if len(sys.argv) > 1 else ".")
