#!/usr/bin/env python3
"""talk.01 v0.2 study: the push-to-talk key moves to the upper LEFT (the walkie-talkie / TE convention), the wheel moves to the RIGHT
(top-right chamfer corner), and the front gets three compositions that are not TE's top/bottom split.

  reach.svg    : where the hand reaches (left hand and right hand), the wheel candidates, and how far things may stick out
  layouts.svg  : three front compositions (F1 strip, F2 window, F3 circles) with the key on the left and the wheel on the right

Standard library only. The reach zones are drawn from reasoning about a hand, NOT from measurements. Dimensions are TENTATIVE.

    python3 design/concepts/src/make_v02.py design/concepts/v0.2
"""
import math
import os
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_concepts import INK, PAPER, DIM, ORANGE, f, rr, circ, line, poly, path, t, panel, px_text, write, SANS, MONO  # noqa: E402
from make_round5 import mix, grad, hlines, vslots, dots_disc, plug_notch, coil  # noqa: E402
from make_round4 import screw  # noqa: E402
from make_round6 import rainbow, ghost  # noqa: E402
from make_v01 import icon, MODES, SKINS  # noqa: E402
import make_round5 as r5  # noqa: E402

W, H = 58, 92
CH = 12                      # the top-right chamfer: 12 mm cut
WX, WY, WR = 47.5, 10.5, 7.5  # the wheel: centre and radius; its rim sticks out of the chamfer by about 1.1 mm
RED = "#c9461e"


def body_path():
    return (f"M5,0 H{W - CH} L{W - 1},{CH - 1} Q{W},{CH} {W},{CH + 1.5} V{H - 5} Q{W},{H} {W - 5},{H} H5 Q0,{H} 0,{H - 5} V5 Q0,0 5,0 Z")


def ell(cx, cy, rx, ry, fill, op=0.35, stroke="none", sw=0.3, rot=0):
    return (f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(rx)}" ry="{f(ry)}" fill="{fill}" fill-opacity="{op}" stroke="{stroke}" '
            f'stroke-width="{f(sw)}" transform="rotate({f(rot)} {f(cx)} {f(cy)})"/>')


# ---------------------------------------------------------------- pieces
def left_key(g, color, edge, ink):
    """The one big key on the LEFT edge, upper half: slanted like the TE lever. Sticks out 5 mm at most, with round shoulders."""
    g.append(ghost(0, 12, -5.0, 46, 2))
    g.append(poly([(0, 12), (-5.0, 16.5), (-3.2, 56), (0, 58)], color, edge, 0.55, 'stroke-linejoin="round"'))
    for k in range(6):
        yy = 24 + k * 5.6
        xo = -(5.0 - (yy - 16.5) * 1.8 / 39.5) + 0.4
        g.append(line(-0.8, yy, xo, yy + 0.3, mix(color, -0.3), 0.4))
    g.append(f'<g transform="translate(-1.9,36) rotate(-90)">{t(0, 0, "TALK", 2.3, "middle", ink, "bold", MONO)}</g>')


def corner_wheel(g, body_id, base, rib, pocket, ink, cur=1):
    """The wheel in the top-right chamfer: a circle seen from the front (axis perpendicular to the face)."""
    g.append(f'<clipPath id="{body_id}"><path d="{body_path()}"/></clipPath>')
    g.append(f'<g clip-path="url(#{body_id})">{circ(WX, WY, WR + 1.8, pocket, "#000", 0.4)}</g>')
    g.append(circ(WX, WY, WR, base, "#000", 0.45))
    for k in range(30):
        a = math.radians(k * 12)
        g.append(line(WX + (WR - 1.3) * math.sin(a), WY - (WR - 1.3) * math.cos(a), WX + WR * math.sin(a), WY - WR * math.cos(a), rib, 0.5))
    g.append(circ(WX, WY, WR * 0.58, mix(base, 0.1), mix(base, -0.4), 0.3))
    a = math.radians([200, 230, 260, 290][cur])
    g.append(line(WX, WY, WX + WR * 0.5 * math.sin(a), WY - WR * 0.5 * math.cos(a), "#f2efe6", 0.9, 'stroke-linecap="round"'))
    g.append(circ(WX, WY, 0.9, "#f2efe6", "none", 0.0))


def scale(g, x, y, ink, cur=1, grid=False):
    """The printed mode scale: four tiny pictograms with names."""
    for k, (ik, lab) in enumerate(MODES):
        px, py = (x + (k % 2) * 9.5, y + (k // 2) * 4.6) if grid else (x + k * 8.6, y)
        col = RED if k == cur else ink
        g.append(icon(ik, px, py, col))
        g.append(t(px + 2.9, py + 0.6, lab, 1.5, "start", col, "bold" if k == cur else "normal", MONO))


def common_top(g, sp, bid, grid_xy=None, grid=False):
    corner_wheel(g, bid, sp["wheel"], sp["rib"], sp["pocket"], sp["ink"], 1)
    g.append(t(WX - 1.5, 24.2, "MODE", 1.4, "middle", sp["ink"], "normal", MONO))
    left_key(g, sp["keyc"], sp["keyedge"], sp["keyink"])
    g += [plug_notch(29, sp["edge"]), coil(29, 0, 3, 2.6, 7, sp["coil"])]


# ---------------------------------------------------------------- three front compositions
def f1_strip(sp, bid):
    """F1: a vertical colour strip down the left (the side you touch), cream to the right. A Walkman / pocket-radio split."""
    g = [f'<path d="{body_path()}" fill="{sp["lower"]}" stroke="{sp["edge"]}" stroke-width="0.5"/>']
    g.append(f'<clipPath id="{bid}s"><path d="{body_path()}"/></clipPath>')
    g.append(f'<g clip-path="url(#{bid}s)">{rr(0, 0, 19, H, 0, sp["upper"], "none", 0.0)}{line(19, 0, 19, H, sp["edge"], 0.5)}</g>')
    g.append(vslots(5.2, 8, 54, 5, 2.9, 1.5, sp["slot"]))                     # the grille: tall slots on the strip
    g.append(circ(9.5, 72, 2.0, sp["mic"], "none", 0.0))
    for (sx, sy) in ((4.6, 4.6), (4.6, H - 4.6)):
        g.append(screw(sx, sy, 1.3))
    common_top(g, sp, bid)
    scale(g, 23.4, 17.0, sp["ink"], 1, grid=True)
    g.append(t(23.4, 40, "talk.01", 5.4, "start", sp["ink"], "bold", SANS))
    g.append(rainbow(23.4, 44.2, 20, 2.4))
    g.append(t(23.4, 50.6, "USB MIC + KEYS", 1.5, "start", sp["ink"], "normal", MONO))
    g.append(circ(50, 78, 2.0, "#e03b2d", "#4a0f0a", 0.2)); g.append(t(50, 83.8, "ON AIR", 1.4, "middle", sp["ink"], "normal", MONO))
    g.append(t(23.4, 84.2, "v0.2", 1.5, "start", RED, "bold", MONO))
    return "".join(g)


def f2_window(sp, bid):
    """F2: a dark inset window in the middle (the grille), cream above and below, a rainbow band across the bottom third."""
    g = [f'<path d="{body_path()}" fill="{sp["lower"]}" stroke="{sp["edge"]}" stroke-width="0.5"/>']
    g.append(rr(6, 25, 46, 38, 4, sp["upper"], sp["edge"], 0.5))
    g.append(vslots(10.2, 29.5, 29, 10, 3.9, 2.0, sp["slot"]))
    for (sx, sy) in ((8.4, 27.4), (49.6, 27.4), (8.4, 60.6), (49.6, 60.6)):
        g.append(screw(sx, sy, 1.1))
    common_top(g, sp, bid)
    scale(g, 5.6, 15.0, sp["ink"], 1)
    g.append(rainbow(0.6, 68.6, W - 1.2, 3.4))
    g.append(t(7, 84.5, "talk.01", 5.6, "start", sp["ink"], "bold", SANS))
    g.append(t(7, 78.4, "USB MIC + KEYS  ·  v0.2", 1.5, "start", sp["ink"], "normal", MONO))
    g.append(circ(48.5, 82, 2.0, "#e03b2d", "#4a0f0a", 0.2)); g.append(t(48.5, 87.4, "ON AIR", 1.4, "middle", sp["ink"], "normal", MONO))
    return "".join(g)


def f3_circles(sp, bid):
    """F3: one motif, the circle: a dot-matrix disc as the grille, a ring of ticks round it, and the wheel as its small twin."""
    g = [f'<path d="{body_path()}" fill="{sp["lower"]}" stroke="{sp["edge"]}" stroke-width="0.5"/>']
    cx, cy = 29, 54
    g.append(circ(cx, cy, 19.5, sp["upper"], sp["edge"], 0.5))
    g.append(dots_disc(cx, cy, 17.2, 2.8, 0.8, sp["slot"]))
    for k in range(48):
        a = math.radians(k * 7.5)
        g.append(line(cx + 20.3 * math.sin(a), cy - 20.3 * math.cos(a), cx + (22.0 if k % 4 == 0 else 21.2) * math.sin(a),
                      cy - (22.0 if k % 4 == 0 else 21.2) * math.cos(a), sp["ink"], 0.3))
    g.append(circ(cx, cy, 2.2, sp["mic"], "none", 0.0))
    for (sx, sy) in ((4.6, H - 4.6), (W - 4.6, H - 4.6)):
        g.append(screw(sx, sy, 1.3))
    common_top(g, sp, bid)
    scale(g, 5.6, 15.0, sp["ink"], 1)
    g.append(rainbow(40, 84, 12, 3.0))
    g.append(t(41, 80.6, "talk.01", 3.6, "start", sp["ink"], "bold", SANS))
    g.append(circ(52, 36, 1.8, "#e03b2d", "#4a0f0a", 0.2)); g.append(t(52, 41.4, "ON AIR", 1.4, "middle", sp["ink"], "normal", MONO))
    g.append(t(46.5, 70.6, "USB MIC", 1.4, "middle", sp["ink"], "normal", MONO))
    return "".join(g)


def layouts(out):
    body = [px_text(60, 62, "talk.01 · v0.2 study · THREE FRONTS, KEY ON THE LEFT, WHEEL ON THE RIGHT", 28, INK, "bold", SANS),
            px_text(60, 92, "the walkie / TE convention for the key (upper left) · our own wheel in the top-right corner · three ways to lay out the face", 15, DIM),
            px_text(1860, 52, "TENTATIVE · NOT A FINAL DESIGN", 13, ORANGE, "bold", MONO, "end"),
            px_text(1860, 72, "front views at 10 mm = 45 px · the key may stick out 5 mm, the wheel about 1 mm", 12, DIM, "normal", MONO, "end")]
    sets = [("F1  STRIP", "a colour strip down the side you touch", f1_strip, SKINS[0], "a"),
            ("F2  WINDOW", "a dark inset window and a rainbow band", f2_window, SKINS[1], "b"),
            ("F3  CIRCLES", "one motif: the circle, big and small", f3_circles, SKINS[0], "c")]
    notes = [["Reads as a Walkman / pocket radio, not as TE's top-and-bottom split.",
              "The colour strip is also the colour of the key: the part you touch is the loud part.",
              "Risk: the tall slots sit close to the key; keep the key's 5 mm clear of the grille."],
             ["Closest to a vintage radio: the speaker window is the hero.",
              "The rainbow band gives a horizontal, TE-like stripe without copying its layout.",
              "Risk: the three bands start to look like TE's two tiers again if the window is too wide."],
             ["The wheel is a small circle and the grille a big one: the repeated motif.",
              "The dot disc is the easiest grille to print and to read as a microphone.",
              "Risk: the most 'designed', so the most to get right; the disc must not look like a camera lens."]]
    for i, (name, sub, fn, sp, bid) in enumerate(sets):
        x = 120 + i * 600
        body.append(px_text(x + 215, 150, name, 22, INK, "bold", SANS))
        body.append(px_text(x + 215, 172, f'{sub}  ·  skin {sp["name"]}', 12, DIM))
        body.append(panel(x + 40, 215, fn(sp, bid), 4.5))
        for j, ln in enumerate(notes[i]):
            for k2, part in enumerate(textwrap.wrap(ln, 58)):
                body.append(px_text(x, 660 + j * 40 + k2 * 16, ("· " if k2 == 0 else "  ") + part, 12, INK if j < 2 else "#9a2f1a"))
    body.append(px_text(60, 810, "Same on all three: the key on the left, upper half (y 12 to 58 mm), slanted, 5 mm out at most; the wheel in the top-right chamfer with its rim about 1 mm out;", 12, DIM))
    body.append(px_text(60, 828, "four mode pictograms printed on the face (DICT, TALK, OPEN, LOCK); the coiled cable and USB-C on top; the back is the earlier small hatch and small U stand.", 12, DIM))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 860" width="1920" height="860"><defs>{"".join(r5.DEFS)}</defs>'
           f'<rect width="1920" height="860" fill="{PAPER}"/>{"".join(body)}</svg>')
    write(out, "layouts.svg", svg)


# ---------------------------------------------------------------- reach study
def outline(sp, with_wheel=True):
    g = [f'<path d="{body_path()}" fill="{sp["lower"]}" stroke="{sp["edge"]}" stroke-width="0.5"/>']
    g.append(poly([(0, 12), (-5.0, 16.5), (-3.2, 56), (0, 58)], sp["keyc"], sp["keyedge"], 0.5, 'stroke-linejoin="round"'))
    return "".join(g)


def mark(x, y, label, col, tx=None, ty=None):
    return circ(x, y, 2.4, col, "#fff", 0.4) + t(x, y + 0.8, label, 2.4, "middle", "#fff", "bold", MONO)


def hand_left(sp):
    """LEFT hand holds it, the back in the palm: the thumb on the left edge, four fingers round the right edge."""
    g = [outline(sp)]
    g.append(ell(8, 33, 11, 21, "#3f8fd2", 0.28))                       # thumb pad: the key lives here
    g.append(ell(5, 74, 12, 15, "#d8483c", 0.34, rot=-12))              # the base of the thumb: soft, pressing, no good for a wheel
    for k in range(4):                                                  # four fingers round the right edge
        g.append(ell(54, 30 + k * 14, 5.2, 6, "#8a857a", 0.40))
    g.append(ell(47, 9, 8.5, 6, "#3f9a52", 0.34, rot=-30))             # the index fingertip can curl to the top
    for (x, y, lab, c) in ((WX, WY, "A", "#2b7a3d"), (54, 40, "B", "#9a7a1e"), (54, 74, "C", "#9a2f1a"), (6, 72, "D", "#9a2f1a")):
        g.append(mark(x, y, lab, c))
    return "".join(g)


def hand_right(sp):
    """RIGHT hand holds it: the four fingers round the LEFT edge (so they press the key), the thumb on the right edge."""
    g = [outline(sp)]
    for k in range(4):
        g.append(ell(4, 22 + k * 11, 5.2, 5.5, "#3f8fd2", 0.34))      # fingers on the key side
    g.append(ell(49, 22, 8, 17, "#3f9a52", 0.30, rot=14))             # the thumb sweeps the right edge from the top
    g.append(ell(52, 72, 9, 15, "#d8483c", 0.34, rot=10))             # base of the thumb in the right palm: no good
    g.append(mark(WX, WY, "A", "#2b7a3d"))
    return "".join(g)


def edge_profiles():
    """A top view of the left edge: a key that digs in versus one that does not. mm, 14 px/mm done by the caller."""
    bad = [rr(0, 0, 22, 18, 1.2, "#e8e1cf", "#6f6a5e", 0.2), poly([(0, 3), (-6.5, 3), (-6.5, 15), (0, 15)], "#3d9aa1", "#1f5a5f", 0.2)]
    good = [rr(0, 0, 22, 18, 3, "#e8e1cf", "#6f6a5e", 0.2), path("M0,3.2 Q-4.6,3.2 -4.6,6.6 L-4.6,11.4 Q-4.6,14.8 0,14.8 Z", "#3d9aa1", "#1f5a5f", 0.2)]
    return "".join(bad), "".join(good)


def reach(out):
    sp = SKINS[0]
    body = [px_text(60, 62, "talk.01 · v0.2 study · WHERE DOES THE HAND REACH?", 28, INK, "bold", SANS),
            px_text(60, 92, "a reasoning sketch, not a measurement: zones are drawn from how a hand holds a small slab. A printed mock-up is the real test.", 15, DIM),
            px_text(1860, 52, "TENTATIVE · NOT MEASURED", 13, ORANGE, "bold", MONO, "end")]
    x1, x2 = 130, 640
    body.append(px_text(x1 - 20, 150, "LEFT hand holds it (the owner's way)", 17, INK, "bold", SANS))
    body.append(panel(x1 + 30, 190, hand_left(sp), 5.6))
    body.append(px_text(x2 - 20 + 130, 150, "RIGHT hand holds it", 17, INK, "bold", SANS))
    body.append(panel(x2 + 170, 190, hand_right(sp), 5.6))
    legend = [("#3f8fd2", "thumb pad (left hand) / four fingers (right hand): the key"),
              ("#d8483c", "the base of the thumb or palm: soft, pushes against the body"),
              ("#8a857a", "four fingers round the edge (left hand)"),
              ("#3f9a52", "a fingertip or thumb tip that can reach")]
    for k, (c, s) in enumerate(legend):
        body.append(rr_px(x1 - 20, 730 + k * 24, 16, 14, c))
        body.append(px_text(x1 + 6, 742 + k * 24, s, 12, INK))
    cand = [("A", "#2b7a3d", "top-right corner (chamfer)", "left hand: the index tip curls onto it; right hand: the thumb tip sweeps it from above. Both reach it. The rim sticks out about 1 mm."),
            ("B", "#9a7a1e", "right edge, upper middle", "the four fingers sit here (left hand). You would have to lift one finger: poor."),
            ("C", "#9a2f1a", "right edge, lower", "the small finger and palm: poor. Also the first place a bag pushes on."),
            ("D", "#9a2f1a", "lower left (the old place)", "the base of the thumb. The owner found it hard to reach: confirmed. Rejected.")]
    cx0 = 1180
    body.append(px_text(cx0, 150, "WHERE THE WHEEL CAN GO", 17, INK, "bold", SANS))
    for k, (c, col, ttl, why) in enumerate(cand):
        yy = 190 + k * 92
        body.append(circ(cx0 + 12, yy - 5, 12, col, "#fff", 1.5))
        body.append(px_text(cx0 + 12, yy, c, 14, "#fff", "bold", MONO, "middle"))
        body.append(px_text(cx0 + 36, yy - 4, ttl, 14, INK, "bold", SANS))
        for j, part in enumerate(textwrap.wrap(why, 62)):
            body.append(px_text(cx0 + 36, yy + 16 + j * 16, part, 12, DIM))
    for j, part in enumerate(textwrap.wrap("Also true: mode changes are rare, so the free hand may turn the wheel. Then every position works, and the choice is only about not being touched by accident, which a corner and stiff detents help with.", 80)):
        body.append(px_text(cx0, 580 + j * 16, part, 12, DIM))
    # protrusion section
    bad, good = edge_profiles()
    body.append(px_text(cx0, 650, "HOW FAR MAY THINGS STICK OUT? (top view of the left edge)", 14, INK, "bold", SANS))
    body.append(panel(cx0 + 40, 700, bad, 9))
    body.append(panel(cx0 + 380, 700, good, 9))
    body.append(px_text(cx0 + 10, 890, "digs in: 6.5 mm out, square corners", 12, "#9a2f1a", "bold", MONO))
    body.append(px_text(cx0 + 350, 890, "rule of thumb: 5 mm at most,", 12, "#2f6f3a", "bold", MONO))
    body.append(px_text(cx0 + 350, 906, "corner radius 2 mm or more, sloped", 12, "#2f6f3a", "bold", MONO))
    body.append(px_text(60, 1010, "These limits are my starting numbers from comfort reasoning, not from a study. They are cheap to test: print the body with a key block at 3, 5 and 7 mm and hold each for a few minutes.", 12, DIM))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1050" width="1920" height="1050"><defs>{"".join(r5.DEFS)}</defs>'
           f'<rect width="1920" height="1050" fill="{PAPER}"/>{"".join(body)}</svg>')
    write(out, "reach.svg", svg)


def rr_px(x, y, w, h, c):
    return f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="3" fill="{c}" fill-opacity="0.45" stroke="{c}"/>'


if __name__ == "__main__":
    o = sys.argv[1] if len(sys.argv) > 1 else "."
    reach(o)
    layouts(o)
