#!/usr/bin/env python3
"""Round-3 silhouette lineup for talk.01: six bold, deliberately different shapes. Standard library only.

The point of this sheet is the *logo test*: can you tell the shapes apart in solid black,
and does one of them make you want to pick it up? Details are minimal on purpose.
All dimensions are TENTATIVE.

    python3 design/concepts/src/make_lineup.py design/concepts/round-3
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_concepts import (INK, PAPER, DIM, ORANGE, f, rr, circ, line, poly, path, t,  # noqa: E402
                           panel, px_text, stand_geometry, desk, slab, write, SANS, MONO)

SC = 3.0
CHAR, CREAM, SLATE, GREY = "#2f2d2a", "#ece6d8", "#44525a", "#a8a398"


def P(ox, oy, inner, sc=SC):
    return panel(ox, oy, inner, sc)


def lean(Px, Py, th, H, D, hh, Ls, local, stand_fill="#c9c2b3", thick=2.6, extra=""):
    (hx, hy), (fx, fy) = stand_geometry(H, hh, Ls, th)
    s = [desk(fx - 8, D * math.cos(math.radians(th)) + 16), f'<g transform="rotate({f(-th)})">{local}</g>',
         slab(hx, hy, fx, fy, thick, stand_fill), extra]
    return P(Px, Py, "".join(s))


def lines(x, y, items, size=12.5, gap=18):
    return "".join(px_text(x, y + i * gap, s, size, c, w) for i, (s, c, w) in enumerate(items))


def card(x, y, w, h, name, tag):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="none" stroke="#d3cdbf" stroke-width="2"/>' +
            px_text(x + 24, y + 38, name, 24, INK, "bold", SANS) + px_text(x + 24, y + 60, tag, 13, DIM))


# ------------------------------------------------------------------ FLIP
def flip_front():
    g = [poly([(0.5, 54), (-1, 54), (-5.5, 80), (0.5, 82)], ORANGE, INK, 0.3),
         rr(0, 0, 58, 92, 6, CREAM, INK, 0.35), line(5, 46, 53, 46, INK, 0.5),
         rr(-2.2, 41.5, 6, 9, 3, ORANGE, INK, 0.3), rr(54.2, 41.5, 6, 9, 3, ORANGE, INK, 0.3)]
    for r in (7, 12, 17):
        g.append(path(f"M{29 - r},27 A{r},{r} 0 0 1 {29 + r},27", "none", CHAR, 2.2, 'stroke-linecap="round"'))
    g += [circ(29, 27, 1.6, CHAR, CHAR, 0.05), circ(29, 66, 1.9, ORANGE, INK, 0.2),
          t(9, 86, "talk.01", 3.4, "start", CHAR, "bold", SANS), rr(38, -0.2, 10, 1.6, 0.8, CHAR, CHAR, 0.05)]
    return "".join(g)


def flip_closed():
    return "".join([rr(0, 0, 28, 46, 5, CREAM, INK, 0.35), line(14, 3, 14, 46, INK, 0.35, 'stroke-dasharray="1 0.8"'),
                    circ(14, 0.6, 3, ORANGE, INK, 0.3), rr(2, 16, 10, 20, 4, ORANGE, INK, 0.25)])


def flip_L():
    g = [rr(14, -14, 46, 14, 4, CREAM, INK, 0.35), rr(18, 0, 8, 1.2, 0.5, CHAR, INK, 0.1), rr(48, 0, 8, 1.2, 0.5, CHAR, INK, 0.1),
         f'<g transform="translate(14,-14) rotate(-15)">{rr(-14, -46, 14, 46, 4, CREAM, INK, 0.35)}{circ(0, -27, 1.5, CHAR, CHAR, 0.05)}</g>',
         circ(14, -14, 3, ORANGE, INK, 0.3), line(0, 0, 66, 0, INK, 0.4)]
    for i in range(22):
        g.append(line(i * 3, 0, i * 3 - 2, 2.2, DIM, 0.12))
    return "".join(g)


# ------------------------------------------------------------------ TILT
def tilt_front():
    g = [poly([(0.5, 52), (-1, 52), (-5.5, 78), (0.5, 80)], ORANGE, INK, 0.3),
         rr(0, 40, 58, 52, 6, SLATE, INK, 0.35), rr(0, 0, 58, 36, 6, CREAM, INK, 0.35),
         rr(18, 34, 22, 8, 4, ORANGE, INK, 0.3), circ(22, 38, 0.8, CHAR, CHAR, 0.05), circ(36, 38, 0.8, CHAR, CHAR, 0.05)]
    for i, h in enumerate((10, 16, 22, 16, 10)):
        g.append(rr(12.5 + i * 8.5, 18 - h / 2, 3.6, h, 1.8, CHAR, CHAR, 0.05))
    g += [circ(29, 18, 3.4, "none", ORANGE, 0.25, 'stroke-dasharray="0.8 0.6"'), rr(10, 55, 38, 4, 2, "#1e272c", INK, 0.15),
          rr(11, 53.8, 6, 6.4, 1.4, CREAM, INK, 0.2), circ(48, 72, 1.8, ORANGE, INK, 0.2),
          t(9, 86, "talk.01", 3.4, "start", CREAM, "bold", SANS), rr(40, -0.2, 10, 1.6, 0.8, CHAR, CHAR, 0.05)]
    for x, lab in ((14, "DICT"), (29, "TALK"), (44, "OPEN")):
        g.append(t(x, 52.5, lab, 2, "middle", CREAM))
    return "".join(g)


def tilt_straight():
    return "".join([rr(0, 40, 18, 52, 5, SLATE, INK, 0.35), rr(0, 0, 18, 36, 5, CREAM, INK, 0.35), circ(9, 38, 4, ORANGE, INK, 0.3)])


def tilt_local():
    return "".join([rr(0, -52, 18, 52, 5, SLATE, INK, 0.35),
                    f'<g transform="translate(9,-52) rotate(-25)">{rr(-9, -36, 18, 36, 5, CREAM, INK, 0.35)}{circ(0, 0, 4, ORANGE, INK, 0.3)}</g>'])


# ------------------------------------------------------------------ CUT
PC = "M16,0 H52 Q58,0 58,6 V86 Q58,92 52,92 H6 Q0,92 0,86 V9 Z"


def cut_front():
    g = [poly([(0.5, 46), (-0.8, 46), (-7, 82), (0.5, 84)], ORANGE, INK, 0.3), path(PC, CREAM, INK, 0.35)]
    for i in range(7):
        g.append(f'<g transform="translate(34,{f(16 + i * 4.6)}) rotate(-29.4)">{rr(-17, -0.9, 34, 1.8, 0.9, CHAR, CHAR, 0.05)}</g>')
    g.append(f'<g transform="translate(8,4.5) rotate(-29.4)">{rr(-7.5, -1.8, 15, 3.6, 1.8, CHAR, INK, 0.2)}'
             + "".join(line(-5 + k * 3.3, -1.0, -5 + k * 3.3, 1.0, CREAM, 0.2) for k in range(4)) + '</g>')
    g += [circ(34, 28, 3.4, "none", ORANGE, 0.25, 'stroke-dasharray="0.8 0.6"'), circ(49, 54, 1.8, ORANGE, INK, 0.2),
          t(9, 86, "talk.01", 3.4, "start", CHAR, "bold", SANS), rr(34, -0.2, 10, 1.6, 0.8, CHAR, CHAR, 0.05)]
    return "".join(g)


def cut_closed():
    return "".join([rr(0, 0, 18, 92, 5, CREAM, INK, 0.35), rr(0, 40, 2.6, 44, 0.8, "#cfc9bb", INK, 0.15), rr(5, 46, 9, 34, 4, ORANGE, INK, 0.25)])


def cut_local():
    return "".join([rr(0, -92, 18, 92, 5, CREAM, INK, 0.35), rr(0, -52, 1.8, 44, 0.6, "#8d887b", INK, 0.1), rr(5, -46, 9, 34, 4, ORANGE, INK, 0.25)])


# ------------------------------------------------------------------ LAYERS
def layers_front():
    g = [poly([(0.5, 38), (-1, 38), (-6, 62), (0.5, 62)], CREAM, INK, 0.3),
         rr(0, 0, 58, 34, 6, "#d6dde0", INK, 0.35), rr(0, 36, 58, 28, 6, ORANGE, INK, 0.35), rr(0, 66, 58, 26, 6, CHAR, INK, 0.35)]
    for r in range(5):
        for x in range(6 if r % 2 == 0 else 12, 52, 12):
            g.append(rr(x, 7 + r * 5, 8, 1.6, 0.8, CHAR, CHAR, 0.05))
    g += [circ(29, 17, 3.6, "none", ORANGE, 0.25, 'stroke-dasharray="0.8 0.6"'), rr(9, 47, 40, 4.5, 2.25, CHAR, INK, 0.2),
          rr(10.5, 45.6, 7, 7.3, 1.4, CREAM, INK, 0.25), t(29, 44.4, "DICT · TALK · OPEN", 2, "middle", CHAR)]
    for sx in (5, 53):
        g += [circ(sx, 50, 1.5, CREAM, INK, 0.2), line(sx - 1, 50, sx + 1, 50, INK, 0.2), circ(sx, 79, 1.5, CREAM, INK, 0.2),
              line(sx - 1, 79, sx + 1, 79, INK, 0.2)]
    g += [t(11, 82, "talk.01", 3.4, "start", CREAM, "bold", SANS), circ(46, 79, 1.8, ORANGE, INK, 0.2), rr(38, -0.2, 10, 1.6, 0.8, CHAR, CHAR, 0.05)]
    return "".join(g)


def layers_side(ox_px=0.0):
    return "".join([rr(0, 0, 18, 34, 5, "#d6dde0", INK, 0.35), rr(0, 36, 18, 28, 5, ORANGE, INK, 0.35), rr(0, 66, 18, 26, 5, CHAR, INK, 0.35),
                    line(5, 3, 5, 89, INK, 0.3, 'stroke-dasharray="1.2 0.8"'), line(13, 3, 13, 89, INK, 0.3, 'stroke-dasharray="1.2 0.8"')])


def layers_local():
    return "".join([rr(0, -92, 18, 34, 5, "#d6dde0", INK, 0.35), rr(0, -56, 18, 28, 5, ORANGE, INK, 0.35), rr(0, -26, 18, 26, 5, CHAR, INK, 0.35)])


# ------------------------------------------------------------------ WEDGE
def wedge_front():
    g = [rr(0, 0, 58, 92, 6, ORANGE, INK, 0.35), path("M0,64 V6 Q0,0 6,0 H52 Q58,0 58,6 V64 Z", CREAM, INK, 0.35),
         line(0, 64, 58, 64, INK, 0.35), poly([(0.5, 32), (-1, 32), (-6, 58), (0.5, 58)], CHAR, INK, 0.3)]
    for cx, cy in ((29, 16), (19.5, 31), (38.5, 31)):
        g.append(circ(cx, cy, 3.4, CHAR, CHAR, 0.05))
    g += [circ(29, 16, 5.4, "none", ORANGE, 0.25, 'stroke-dasharray="0.8 0.6"'), circ(48, 54, 1.8, ORANGE, INK, 0.2),
          t(9, 83, "talk.01", 3.4, "start", CHAR, "bold", SANS), rr(38, -0.2, 10, 1.6, 0.8, CHAR, CHAR, 0.05)]
    return "".join(g)


def wedge_side():
    prof = "M0,6 Q0,0 6,0 H10 Q13,0 14.2,2.8 L46.4,86 Q48,92 42,92 H6 Q0,92 0,86 Z"
    g = [path(prof, ORANGE, INK, 0.35), path("M0,6 Q0,0 6,0 H10 Q13,0 14.2,2.8 L37,64 H0 Z", CREAM, INK, 0.35), line(0, 64, 37, 64, INK, 0.3),
         rr(5, 34, 9, 24, 4, CHAR, INK, 0.25), line(-6, 92, 62, 92, INK, 0.4)]
    for i in range(23):
        g.append(line(-6 + i * 3, 92, -8 + i * 3, 94.2, DIM, 0.12))
    return "".join(g)


# ------------------------------------------------------------------ PEBBLE
def peb_front():
    cx, cy, R = 34, 34, 33
    g = [circ(cx, cy, R, CHAR, INK, 0.35), rr(18, 63, 32, 5, 2, "#3a3836", INK, 0.2), circ(cx, cy, 26, CREAM, INK, 0.3)]

    def pt(a, r):
        return cx + r * math.sin(math.radians(a)), cy - r * math.cos(math.radians(a))
    x1, y1 = pt(235, 34.4)
    x2, y2 = pt(305, 34.4)
    g.append(path(f"M{f(x1)},{f(y1)} A34.4,34.4 0 0 1 {f(x2)},{f(y2)}", "none", ORANGE, 5, 'stroke-linecap="round"'))
    for k in range(24):
        a = k * 15
        (xa, ya), (xb, yb) = pt(a, 27.6), pt(a, 29.4)
        g.append(line(xa, ya, xb, yb, CREAM, 0.2))
    for a, lab in ((38, "DICT"), (78, "TALK"), (118, "OPEN"), (158, "LOCK")):
        xx, yy = pt(a, 30.6)
        g.append(t(xx, yy + 0.7, lab, 1.8, "middle", CREAM))
    xa, ya = pt(38, 18)
    xb, yb = pt(38, 25)
    g.append(line(xa, ya, xb, yb, ORANGE, 1.2, 'stroke-linecap="round"'))
    for k in range(12):
        xx, yy = pt(k * 30, 13)
        g.append(circ(xx, yy, 1.1, CHAR, CHAR, 0.05))
    g += [circ(cx, cy, 1.8, CHAR, CHAR, 0.05), circ(cx, cy, 4, "none", ORANGE, 0.25, 'stroke-dasharray="0.8 0.6"'),
          t(cx, 52, "talk.01", 3, "middle", CHAR, "bold", SANS), circ(cx, 57.5, 1.6, ORANGE, INK, 0.2), rr(29, -0.4, 10, 1.8, 0.9, CREAM, INK, 0.1)]
    return "".join(g)


def peb_closed():
    return "".join([rr(0, 0, 20, 66, 8, CHAR, INK, 0.35), rr(2, 64, 16, 3, 1.2, "#3a3836", INK, 0.15), rr(5, 18, 10, 30, 5, ORANGE, INK, 0.25)])


def peb_local():
    return "".join([rr(0, -66, 20, 66, 8, CHAR, INK, 0.35), rr(5, -48, 10, 30, 5, ORANGE, INK, 0.25)])


# ------------------------------------------------------------------ silhouettes (logo test)
def sil_strip(x0, y0, sc=1.25):
    K = "#1c1b19"
    items = []
    # FLIP
    items.append(("FLIP", P(x0, y0, rr(0, 0, 58, 92, 6, K, K, 0.1) + line(2, 46, 56, 46, PAPER, 0.9) +
                           rr(-2.2, 41.5, 6, 9, 3, K, K, 0.1) + rr(54.2, 41.5, 6, 9, 3, K, K, 0.1) +
                           poly([(0.5, 54), (-1, 54), (-5.5, 80), (0.5, 82)], K, K, 0.1), sc)))
    items.append(("TILT", P(x0 + 270, y0, rr(0, 40, 58, 52, 6, K, K, 0.1) + rr(0, 0, 58, 36, 6, K, K, 0.1) +
                           rr(18, 34, 22, 8, 4, K, K, 0.1) + poly([(0.5, 52), (-1, 52), (-5.5, 78), (0.5, 80)], K, K, 0.1), sc)))
    items.append(("CUT", P(x0 + 540, y0, path(PC, K, K, 0.1) + poly([(0.5, 46), (-0.8, 46), (-7, 82), (0.5, 84)], K, K, 0.1), sc)))
    items.append(("LAYERS", P(x0 + 810, y0, rr(0, 0, 58, 34, 6, K, K, 0.1) + rr(0, 36, 58, 28, 6, K, K, 0.1) + rr(0, 66, 58, 26, 6, K, K, 0.1) +
                            poly([(0.5, 38), (-1, 38), (-6, 62), (0.5, 62)], K, K, 0.1), sc)))
    items.append(("WEDGE (side)", P(x0 + 1080, y0, path("M0,6 Q0,0 6,0 H10 Q13,0 14.2,2.8 L46.4,86 Q48,92 42,92 H6 Q0,92 0,86 Z", K, K, 0.1), sc)))
    items.append(("PEBBLE", P(x0 + 1350, y0, circ(34, 34, 33, K, K, 0.1) + rr(18, 63, 32, 5, 2, K, K, 0.1) +
                             path("M5.8,53.7 A34.4,34.4 0 0 1 5.8,14.3", "none", K, 5, 'stroke-linecap="round"'), sc)))
    out = []
    for i, (nm, svg) in enumerate(items):
        out.append(svg)
        out.append(px_text(x0 + i * 270 + 36, y0 + 92 * sc + 24, nm, 13, INK, "bold", MONO, "middle"))
    return "".join(out)


# ------------------------------------------------------------------ cards
def build(out):
    W, Hc = 580, 570
    xs, ys = (50, 670, 1290), (330, 930)
    base_off = 84 + 92 * SC          # baseline (desk) y inside a card
    body = []

    def put_card(i, name, tag, front, closed, lean_svg, lines_):
        cx, cy = xs[i % 3], ys[i // 3]
        body.append(card(cx, cy, W, Hc, name, tag))
        body.append(P(cx + 28, cy + 84, front))
        if closed:
            body.append(closed(cx, cy))
        if lean_svg:
            body.append(lean_svg(cx, cy))
        body.append(lines(cx + 24, cy + 408, lines_))

    # FLIP
    put_card(0, "1 · FLIP", "a clamshell that changes shape: closed, desk L, straight",
             flip_front(), lambda cx, cy: P(cx + 222, cy + base_off - 46 * SC, flip_closed()),
             lambda cx, cy: P(cx + 330, cy + base_off, flip_L()),
             [("hero: the seam and the orange hinge barrels; it transforms", INK, "bold"),
              ("closed = pocket-safe + muted · L = desk mic · straight = handheld", CHAR, "normal"),
              ("stand: the hinge itself · cover: small hatch under the base", CHAR, "normal"),
              ("+ pager-clamshell nostalgia, fully protected when closed", "#2f6f3a", "normal"),
              ("+ the pose is the mode (hinge angle sensor)", "#2f6f3a", "normal"),
              ("- needs a friction/detent hinge that FDM can hold", "#9a2f1a", "normal"),
              ("- thin blocks (about 14 mm) pack electronics tightly", "#9a2f1a", "normal")])
    # TILT
    put_card(1, "2 · TILT", "a grip and a head: the head tilts to aim at your mouth",
             tilt_front(), lambda cx, cy: P(cx + 222, cy + base_off - 92 * SC, tilt_straight()),
             lambda cx, cy: lean(cx + 460, cy + base_off, 15, 52, 18, 14, 38, tilt_local()),
             [("hero: the two-block shape with an orange joint", INK, "bold"),
              ("head tilts +-30° in detents · EQ-bar grille is the identity", CHAR, "normal"),
              ("stand: a short foot (small U) · cover: round hatch in the grip", CHAR, "normal"),
              ("+ solves 'aim at the mouth' with a toy-like mechanism", "#2f6f3a", "normal"),
              ("+ strong silhouette and a fun joint to fidget with", "#2f6f3a", "normal"),
              ("- joint strength and the cable moving with the head", "#9a2f1a", "normal"),
              ("- more parts than any slab", "#9a2f1a", "normal")])
    # CUT
    put_card(2, "3 · CUT", "one 30° angle used on everything, plus a big slanted lever",
             cut_front(), lambda cx, cy: P(cx + 222, cy + base_off - 92 * SC, cut_closed()),
             lambda cx, cy: lean(cx + 470, cy + base_off, 30, 92, 18, 40, 48, cut_local(), "#cfc9bb", 3),
             [("hero: the chamfered corner with the dial, and the wedge lever", INK, "bold"),
              ("every cut, slot and the hatch corner share one angle", CHAR, "normal"),
              ("cover = stand: the small hatch swings out as the kickstand", CHAR, "normal"),
              ("+ logo-like silhouette; one motif = strong identity", "#2f6f3a", "normal"),
              ("+ opening the stand opens the bay: one action", "#2f6f3a", "normal"),
              ("- the bay is exposed whenever the stand is out", "#9a2f1a", "normal"),
              ("- wedge lever is close to the reference's idea", "#9a2f1a", "normal")])
    # LAYERS
    put_card(3, "4 · LAYERS", "three stacked plates, colour-blocked, screws as ornament",
             layers_front(), lambda cx, cy: P(cx + 222, cy + base_off - 92 * SC, layers_side()),
             lambda cx, cy: lean(cx + 470, cy + base_off, 30, 92, 18, 40, 48, layers_local(), "#d6dde0", 2.4),
             [("hero: the colour-blocked stack and the exposed screws", INK, "bold"),
              ("top plate = grille, middle = controls, bottom = base + battery", CHAR, "normal"),
              ("stand: small U on the middle plate · cover: the bottom plate", CHAR, "normal"),
              ("+ print each plate in a different colour; swap to customise", "#2f6f3a", "normal"),
              ("+ the cover idea becomes the whole identity", "#2f6f3a", "normal"),
              ("- alignment of three parts; seams must look deliberate", "#9a2f1a", "normal"),
              ("- the stack look can feel generic without the details", "#9a2f1a", "normal")])
    # WEDGE
    put_card(4, "5 · WEDGE", "a doorstop: the body is the stand, no mechanism at all",
             wedge_front(), lambda cx, cy: P(cx + 222, cy + base_off - 92 * SC, wedge_side()), None,
             [("hero: the doorstop profile and three big round holes", INK, "bold"),
              ("front face leans back about 21°; battery lives in the heavy base", CHAR, "normal"),
              ("stand: none needed · cover: the base plate underneath", CHAR, "normal"),
              ("+ nothing to break; very stable; low centre of mass", "#2f6f3a", "normal"),
              ("+ a desk object with a clear face", "#2f6f3a", "normal"),
              ("- bulky in a bag; not a folding stand (changes the brief)", "#9a2f1a", "normal"),
              ("- handheld shape is a wedge in the palm: needs a mock", "#9a2f1a", "normal")])
    # PEBBLE
    put_card(5, "6 · PEBBLE", "a round puck: the bezel ring turns for the mode",
             peb_front(), lambda cx, cy: P(cx + 272, cy + base_off - 66 * SC, peb_closed()),
             lambda cx, cy: lean(cx + 500, cy + base_off, 25, 66, 20, 10, 54, peb_local(), "#c9c2b3", 2.4),
             [("hero: the circle, the turning bezel and the arc lever", INK, "bold"),
              ("ring marks DICT / TALK / OPEN / LOCK; a flat foot stops rolling", CHAR, "normal"),
              ("stand: a small U ring on the back · cover: round hatch", CHAR, "normal"),
              ("+ the most distinct silhouette; fits a pocket and a palm", "#2f6f3a", "normal"),
              ("+ bezel is a great fidget; arc lever follows the thumb", "#2f6f3a", "normal"),
              ("- furthest from the pager/radio feel; round parts are harder", "#9a2f1a", "normal"),
              ("- rolling and thumb reach need physical mocks", "#9a2f1a", "normal")])

    head = (px_text(60, 62, "talk.01 · ROUND 3 · SILHOUETTE LINEUP", 30, INK, "bold", SANS) +
            px_text(60, 92, "six deliberately different shapes · judge the shape first, details second", 15, DIM) +
            px_text(1860, 52, "TENTATIVE · NOT A FINAL DESIGN", 13, ORANGE, "bold", MONO, "end") +
            px_text(1860, 72, "original concepts · same scale in every card (10 mm = 30 px)", 12, DIM, "normal", MONO, "end") +
            px_text(60, 150, "LOGO TEST: in solid black, can you tell them apart, and does one make you want to pick it up?", 14, INK, "bold", MONO))
    strip = sil_strip(70, 176)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1540" width="1920" height="1540">'
           f'<rect width="1920" height="1540" fill="{PAPER}"/>{head}{strip}{"".join(body)}</svg>')
    write(out, "lineup.svg", svg)


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else ".")
