#!/usr/bin/env python3
"""Round-4 sheet for talk.01: three variations of CUT, all from the push-to-talk radio lineage.

HANDIE (walkie-talkie brick), PALM (CB hand-mic), POD (small MP3-player bar).
Shared family traits: one 30 degree chamfer, a thumb dial on the chamfer, a slanted
left-edge lever, a coiled cable on the top edge, a small hatch (no full-back cover) and
a small U stand or a hatch that is the stand. Standard library only. Dimensions are TENTATIVE.

    python3 design/concepts/src/make_round4.py design/concepts/round-4
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_concepts import (INK, PAPER, DIM, ORANGE, f, rr, circ, line, poly, path, t,  # noqa: E402
                           panel, px_text, write, SANS, MONO)
from make_lineup import lean  # noqa: E402

BRASS = "#c9a24b"
SC = 4.0     # px per mm for the main front view
SS = 3.0     # px per mm for side/rear views
ZM = 7.0     # zoom factor for the 3 cm detail inset
BASE = 840   # desk baseline (px) shared by all columns
COLX = (40, 660, 1280)


def screw(cx, cy, r=1.5):
    return circ(cx, cy, r, BRASS, INK, 0.2) + line(cx - r * 0.7, cy - r * 0.35, cx + r * 0.7, cy + r * 0.35, INK, 0.25)


def coil(cx, y_bottom, turns=9, pitch=2.6, w=7.0, color=ORANGE):
    """Coiled cable above the top edge: plug, boot, coil, straight tail (all in mm, y negative = up)."""
    g = [rr(cx - 4.5, y_bottom - 3.6, 9, 3.6, 0.8, "#cfcfcf", INK, 0.25),
         rr(cx - 3.2, y_bottom - 9, 6.4, 5.6, 1.4, "#2b2a28", INK, 0.2)]
    y = y_bottom - 11
    for k in range(turns):
        cy = y - k * pitch
        el = f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(w / 2)}" ry="{f(pitch * 0.9)}" fill="none" transform="rotate(-18 {f(cx)} {f(cy)})"'
        g.append(el + ' stroke="#9b3510" stroke-width="1.7"/>')
        g.append(el + f' stroke="{color}" stroke-width="1.1"/>')
    top = y - turns * pitch
    g.append(line(cx, y - turns * pitch + pitch, cx, top - 6, color, 1.4))
    return "".join(g)


def pict(x, y, kind, color=INK):
    """Tiny pictograms: hold (down triangle), click (dot), push (double triangle)."""
    if kind == "hold":
        return poly([(x - 1.1, y - 0.9), (x + 1.1, y - 0.9), (x, y + 0.9)], color, color, 0.05)
    if kind == "click":
        return circ(x, y, 0.95, color, color, 0.05)
    return (poly([(x - 1.1, y - 1.6), (x + 1.1, y - 1.6), (x, y - 0.1)], color, color, 0.05) +
            poly([(x - 1.1, y + 0.1), (x + 1.1, y + 0.1), (x, y + 1.6)], color, color, 0.05))


def pictos(x, y, color, lab_color):
    g = []
    for i, (k, lab) in enumerate((("hold", "HOLD"), ("click", "CLICK"), ("push", "PUSH"))):
        yy = y + i * 4.6
        g.append(pict(x, yy, k, color))
        g.append(t(x + 2.6, yy + 0.6, lab, 1.5, "start", lab_color))
    return "".join(g)


def dial_chamfer(c_text, ink_fill="#2b2a28", tick="#efe9d6"):
    g = [f'<g transform="translate(8,4.5) rotate(-29.4)">{rr(-7.5, -1.8, 15, 3.6, 1.8, ink_fill, INK, 0.2)}'
         + "".join(line(-5 + k * 3.3, -1.0, -5 + k * 3.3, 1.0, tick, 0.2) for k in range(4)) + '</g>',
         f'<g transform="translate(5.3,9.9) rotate(-29.4)">{t(0, 0, "1  2  3  4", 1.7, "start", c_text)}</g>']
    return "".join(g)


def slots(n, cx, y0, pitch, ln, fill):
    return "".join(f'<g transform="translate({cx},{f(y0 + i * pitch)}) rotate(-29.4)">{rr(-ln / 2, -0.9, ln, 1.8, 0.9, fill, fill, 0.05)}</g>'
                   for i in range(n))


def usb_notch(x, w=10, fill="#2b2a28"):
    return rr(x - w / 2, -0.2, w, 1.6, 0.8, fill, fill, 0.05)


def lever_wedge(top, bottom, x_out, fill, ribs=True, edge=INK):
    g = [poly([(0.5, top), (-0.8, top), (x_out, bottom - 2), (0.5, bottom)], fill, edge, 0.3)]
    if ribs:
        for yy in (top + 12, top + 17, top + 22):
            xo = -0.8 + (x_out + 0.8) * (yy - top) / (bottom - 2 - top)
            g.append(line(0.2, yy, xo + 0.7, yy, edge, 0.28))
    return "".join(g)


# ======================================================================= HANDIE
PC = "M16,0 H52 Q58,0 58,6 V86 Q58,92 52,92 H6 Q0,92 0,86 V9 Z"
HB, HC = "#e9e4d8", "#2b2a28"


def handie_front():
    g = [lever_wedge(44, 84, -7, ORANGE), path(PC, HB, INK, 0.35)]
    for i in range(7):
        g.append(line(10, 62 + i * 3.2, 48, 62 + i * 3.2, "#c4bdad", 0.9, 'stroke-linecap="round"'))
    g += [slots(6, 34, 14, 4.4, 30, HC), circ(34, 25, 3.4, "none", ORANGE, 0.25, 'stroke-dasharray="0.8 0.6"'),
          dial_chamfer("#6b665c"), pictos(5.6, 50, INK, "#6b665c"),
          circ(49, 53, 1.8, ORANGE, INK, 0.2), t(49, 58, "ON AIR", 1.6, "middle", "#6b665c"),
          screw(51, 8), screw(6, 87), screw(52, 87), t(14, 88.6, "talk.01", 3.2, "start", HC, "bold", SANS),
          usb_notch(39), coil(39, 0)]
    return "".join(g)


def handie_hatch_rear():
    return "".join([path(PC, HB, INK, 0.35),
                    poly([(16, 40), (46, 40), (46, 76), (40, 82), (12, 82), (12, 46)], "#d4cdbd", INK, 0.3),
                    circ(19, 41.5, 1.1, BRASS, INK, 0.15), circ(43, 41.5, 1.1, BRASS, INK, 0.15),
                    rr(10, 90.2, 12, 1.4, 0.6, HC, HC, 0.05), rr(36, 90.2, 12, 1.4, 0.6, HC, HC, 0.05)])


def handie_side(closed=True):
    g = [rr(0, 0, 20, 92, 5, HB, INK, 0.35)]
    if closed:
        g.append(poly([(0, 40), (2.6, 40), (2.6, 82), (0, 82)], "#d4cdbd", INK, 0.15))
    g.append(rr(6, 46, 10, 36, 4, ORANGE, INK, 0.25))
    g.append(rr(3, 92, 14, 1.1, 0.5, "#3a3836", INK, 0.1))
    return "".join(g)


def handie_local():
    return "".join([rr(0, -92, 20, 92, 5, HB, INK, 0.35), rr(0, -52, 1.8, 42, 0.6, "#8d887b", INK, 0.1),
                    rr(6, -46, 10, 36, 4, ORANGE, INK, 0.25)])


# ======================================================================= PALM
PP = ("M16,0 H50 Q60,0 60,9 V32 C60,46 51,48 51,62 V70 C51,82 57,82 57,88 Q57,92 52,92 "
      "H8 Q3,92 3,88 C3,82 9,82 9,70 V62 C9,48 0,46 0,32 V9 Z")
PBODY, PINK_, PMET = "#34332f", "#1c1b19", "#cdd0d2"
PCREAM = "#efe9d6"


def palm_front():
    g = [poly([(9.4, 42), (7.8, 42), (1.6, 82), (9.4, 86)], PMET, INK, 0.3), path(PP, PBODY, INK, 0.35)]
    for yy in (52, 60, 68, 76):
        xo = 7.8 + (1.6 - 7.8) * (yy - 42) / 40
        g.append(line(8.9, yy, xo + 0.6, yy, "#7d8083", 0.28))
    g += [slots(5, 33, 12, 4.6, 30, PINK_), circ(33, 21, 3.4, "none", ORANGE, 0.25, 'stroke-dasharray="0.8 0.6"'),
          dial_chamfer("#b5ae9d", "#8a8d8f", "#1c1b19"), pictos(14.5, 54, PCREAM, "#b5ae9d"),
          circ(40, 62, 1.8, ORANGE, INK, 0.2), t(40, 67, "ON AIR", 1.6, "middle", "#b5ae9d"),
          screw(52, 7), screw(30, 88), t(18, 78, "talk.01", 3.2, "start", PCREAM, "bold", SANS),
          usb_notch(38, 10, PINK_), coil(38, 0)]
    return "".join(g)


def palm_rear():
    return "".join([path(PP, PBODY, INK, 0.35), path("M19,18 L19,54 L41,54 L41,18", "none", "#b5ae9d", 2.2, 'stroke-linecap="round" stroke-linejoin="round"'),
                    circ(19, 18, 1.4, BRASS, INK, 0.15), circ(41, 18, 1.4, BRASS, INK, 0.15), circ(30, 68, 9, "#2a2926", INK, 0.3),
                    circ(30, 68, 6.5, "none", "#7d8083", 0.3), line(27, 68, 33, 68, "#7d8083", 0.4),
                    rr(10, 90.2, 12, 1.4, 0.6, PINK_, PINK_, 0.05), rr(36, 90.2, 12, 1.4, 0.6, PINK_, PINK_, 0.05)])


def palm_side(closed=True):
    return "".join([rr(0, 0, 20, 92, 6, PBODY, INK, 0.35), rr(5, 42, 10, 44, 5, PMET, INK, 0.25),
                    rr(3, 92, 14, 1.1, 0.5, "#111", INK, 0.1)])


def palm_local():
    return "".join([rr(0, -92, 20, 92, 6, PBODY, INK, 0.35), rr(5, -50, 10, 44, 5, PMET, INK, 0.25)])


# ======================================================================= POD
PD = "M18,0 H40 Q46,0 46,6 V98 Q46,104 40,104 H6 Q0,104 0,98 V10 Z"
DB, DC = "#e4e6e5", "#222222"


def pod_front():
    g = [lever_wedge(36, 60, -5.5, ORANGE), path(PD, DB, INK, 0.35), slots(3, 24, 16, 5, 26, DC),
         circ(24, 21, 3.2, "none", ORANGE, 0.25, 'stroke-dasharray="0.8 0.6"'),
         dial_chamfer("#6b6e6d", "#2b2a28", "#efe9d6"), pictos(5.2, 44, INK, "#6b6e6d"),
         rr(14, 33, 22, 5.2, 2.6, DC, INK, 0.2), circ(18, 35.6, 1.3, ORANGE, INK, 0.1), t(21, 36.3, "ON AIR", 1.6, "start", "#efe9d6"),
         circ(23, 72, 15.5, "#2b2a28", INK, 0.3), circ(23, 72, 10.5, "#f2f3f2", INK, 0.25)]
    for k in range(16):
        a = math.radians(k * 22.5)
        g.append(line(23 + 12.3 * math.sin(a), 72 - 12.3 * math.cos(a), 23 + 14.3 * math.sin(a), 72 - 14.3 * math.cos(a), "#efe9d6", 0.22))
    a0 = math.radians(-50)
    g += [line(23 + 3 * math.sin(a0), 72 - 3 * math.cos(a0), 23 + 9 * math.sin(a0), 72 - 9 * math.cos(a0), ORANGE, 1.3, 'stroke-linecap="round"'),
          t(23, 73.2, "talk", 2.2, "middle", INK, "bold", SANS), screw(6, 99), screw(40, 99), usb_notch(31, 10), coil(31, 0)]
    return "".join(g)


def pod_rear():
    return "".join([path(PD, DB, INK, 0.35), rr(10, 52, 26, 32, 5, "#d3d5d4", INK, 0.3),
                    circ(14, 54, 1.0, BRASS, INK, 0.15), circ(32, 54, 1.0, BRASS, INK, 0.15),
                    path("M13,16 L13,44 L33,44 L33,16", "none", "#8d908f", 2, 'stroke-linecap="round" stroke-linejoin="round"'),
                    rr(7, 102.2, 11, 1.4, 0.6, DC, DC, 0.05), rr(29, 102.2, 11, 1.4, 0.6, DC, DC, 0.05)])


def pod_side(closed=True):
    return "".join([rr(0, 0, 13, 104, 5, DB, INK, 0.35), rr(3, 37, 7, 22, 3.5, ORANGE, INK, 0.25), rr(2, 104, 9, 1.1, 0.5, "#3a3836", INK, 0.1)])


def pod_local():
    return "".join([rr(0, -104, 13, 104, 5, DB, INK, 0.35), rr(3, -67, 7, 22, 3.5, ORANGE, INK, 0.25)])


# ======================================================================= sheet
def mirror(inner, W):
    return f'<g transform="translate({W},0) scale(-1,1)">{inner}</g>'


def zoom(ox, oy, front_inner, rx, ry, rw, rh, uid):
    cid = f"zm{uid}"
    return (f'<clipPath id="{cid}"><rect x="{ox}" y="{oy}" width="{f(rw * ZM)}" height="{f(rh * ZM)}"/></clipPath>'
            f'<rect x="{ox}" y="{oy}" width="{f(rw * ZM)}" height="{f(rh * ZM)}" fill="#faf8f2" stroke="{INK}" stroke-width="1.5"/>'
            f'<g clip-path="url(#{cid})"><g transform="translate({f(ox - rx * ZM)},{f(oy - ry * ZM)}) scale({ZM})">{front_inner}</g></g>')


def column(i, name, lineage, W, H, front, rear, side, local, stand, zr, lines_, lean_args, rear_mirror=True):
    x0 = COLX[i]
    y0 = BASE - H * SC
    out = [f'<rect x="{x0 - 10}" y="150" width="610" height="1340" rx="14" fill="none" stroke="#d3cdbf" stroke-width="2"/>',
           px_text(x0 + 10, 190, name, 26, INK, "bold", SANS), px_text(x0 + 10, 214, lineage, 13, DIM)]
    out.append(panel(x0 + 40, y0, front, SC))
    # zoom box on the front
    rx, ry, rw, rh = zr
    out.append(panel(x0 + 40, y0, rr(rx, ry, rw, rh, 1, "none", ORANGE, 0.3, 'stroke-dasharray="1.2 0.8"'), SC))
    out.append(panel(x0 + 300, BASE - H * SS, side(True), SS))
    th, D, hh, Ls = lean_args
    out.append(lean(x0 + 470, BASE, th, H, D, hh, Ls, local, "#c9c2b3", 2.6))
    out.append(px_text(x0 + 300, BASE + 26, "side · desk", 12, DIM))
    out.append(px_text(x0 + 40, BASE + 26, "front (dashed box = zoom)", 12, DIM))
    out.append(zoom(x0 + 20, BASE + 90, front, rx, ry, rw, rh, i))
    out.append(px_text(x0 + 20, BASE + 78, "3 CM DETAIL", 12, INK, "bold", MONO))
    rear_inner = mirror(rear, W) if rear_mirror else rear
    out.append(px_text(x0 + 330, BASE + 78, "REAR · small hatch + stand", 12, INK, "bold", MONO))
    out.append(panel(x0 + 340, BASE + 90, rear_inner, SS))
    ly = BASE + 90 + H * SS + 40
    out.append("".join(px_text(x0 + 10, ly + k * 18, s, 12.5, c, w) for k, (s, c, w) in enumerate(lines_)))
    return "".join(out)


def build(out):
    G, R = "#2f6f3a", "#9a2f1a"
    cols = []
    cols.append(column(0, "A · HANDIE", "lineage: the walkie-talkie brick (Handie-Talkie, push-to-talk on the side)", 58, 92,
                       handie_front(), handie_hatch_rear(), handie_side, handie_local(), None, (-9, 38, 36, 32),
                       [("hero: the slanted PTT lever on a chamfered brick", INK, "bold"),
                        ("borrows: grip ribs, side PTT, top dial like a radio volume knob", HC, "normal"),
                        ("graphic layer: 1-4 channel numbers, HOLD/CLICK/PUSH icons,", HC, "normal"),
                        ("   ON AIR lamp, brass screws, orange coiled cable", HC, "normal"),
                        ("stand and cover: ONE small hatch that swings out as the stand", HC, "normal"),
                        ("+ most 'real radio'; one motif; easy to print", G, "normal"),
                        ("+ opening the stand opens the bay", G, "normal"),
                        ("- the bay is exposed while the stand is out", R, "normal"),
                        ("- slab with a chamfer: not yet a strong silhouette", R, "normal")],
                       (30, 20, 40, 46)))
    cols.append(column(1, "B · PALM", "lineage: the CB hand microphone (waisted body, long PTT bar, coiled cord)", 60, 92,
                       palm_front(), palm_rear(), palm_side, palm_local(), None, (-4, 36, 34, 34),
                       [("hero: the waisted 'palm mic' body and the long metal bar", INK, "bold"),
                        ("borrows: the CB mic's waist that fits the hand, bar down the side", HC, "normal"),
                        ("graphic layer: same icons and numbers, cream on black,", HC, "normal"),
                        ("   metal bar, brass screws, orange coiled cable", HC, "normal"),
                        ("stand: small U in a groove · cover: round hatch (coin shape)", HC, "normal"),
                        ("+ strongest silhouette; the waist is where the thumb goes", G, "normal"),
                        ("+ black and metal with an orange cable is very striking", G, "normal"),
                        ("- the waist costs inner volume and print is harder", R, "normal"),
                        ("- long bar needs a pivot that survives FDM", R, "normal")],
                       (30, 20, 40, 48)))
    cols.append(column(2, "C · POD", "lineage: the small bar-shaped MP3 player (one chamfer, one round control)", 46, 104,
                       pod_front(), pod_rear(), pod_side, pod_local(), None, (-7, 30, 34, 30),
                       [("hero: a slim white bar with one big round dial ring", INK, "bold"),
                        ("borrows: the MP3 player's slim bar and single round control", HC, "normal"),
                        ("graphic layer: ring ticks 1-4, 'talk' on the button, icons,", HC, "normal"),
                        ("   ON AIR window, brass screws, orange coiled cable", HC, "normal"),
                        ("stand: small U · cover: small rounded hatch", HC, "normal"),
                        ("+ pocketable and very handheld; clean and modern", G, "normal"),
                        ("+ the ring is a good fidget and states the mode", G, "normal"),
                        ("- slim (13 mm): tight for the board and lever", R, "normal"),
                        ("- least like a radio; leans towards a music player", R, "normal")],
                       (30, 13, 40, 48)))
    head = (px_text(60, 62, "talk.01 · ROUND 4 · THREE CUTS FROM THE PUSH-TO-TALK LINE", 30, INK, "bold", SANS) +
            px_text(60, 92, "one family: 30° chamfer · thumb dial on the chamfer · slanted left lever · coiled orange cable on top · small hatch", 15, DIM) +
            px_text(1860, 52, "TENTATIVE · NOT A FINAL DESIGN", 13, ORANGE, "bold", MONO, "end") +
            px_text(1860, 72, "original concepts · dimensions are guesses", 12, DIM, "normal", MONO, "end") +
            px_text(60, 126, "No flipping, tilting or stacking this time: shapes come from old radio gear, details come from the checklist.", 14, INK, "normal", MONO))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1550" width="1920" height="1550">'
           f'<rect width="1920" height="1550" fill="{PAPER}"/>{head}{"".join(cols)}</svg>')
    write(out, "round4.svg", svg)


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else ".")
