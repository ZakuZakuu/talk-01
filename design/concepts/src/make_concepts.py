#!/usr/bin/env python3
"""Generate the talk.01 concept sheets (flat 2D SVG). Standard library only.

All dimensions are TENTATIVE. Drawing units inside each panel are millimetres
(scaled to pixels by S), so the numbers below can be edited and the sheets
regenerated:

    python3 design/concepts/src/make_concepts.py design/concepts

The sheets are sketches for discussion, not CAD and not a final design.
"""
import math
import os
import sys

S = 6.0  # pixels per millimetre inside a panel
INK = "#2b2a28"
PAPER = "#f4f1ea"
DIM = "#7a756b"
ORANGE = "#e8541e"
MONO = "'DejaVu Sans Mono','Menlo','Consolas',monospace"
SANS = "'DejaVu Sans','Helvetica','Arial',sans-serif"


# ---------------------------------------------------------------- primitives
def f(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return s if s not in ("-0", "") else "0"


def rr(x, y, w, h, r=0.0, fill="none", stroke=INK, sw=0.3, extra=""):
    return (f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{f(r)}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{f(sw)}" {extra}/>')


def circ(cx, cy, r, fill="none", stroke=INK, sw=0.3, extra=""):
    return (f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{f(sw)}" {extra}/>')


def line(x1, y1, x2, y2, stroke=INK, sw=0.2, extra=""):
    return (f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" '
            f'stroke="{stroke}" stroke-width="{f(sw)}" {extra}/>')


def poly(pts, fill="none", stroke=INK, sw=0.3, extra=""):
    p = " ".join(f"{f(x)},{f(y)}" for x, y in pts)
    return f'<polygon points="{p}" fill="{fill}" stroke="{stroke}" stroke-width="{f(sw)}" {extra}/>'


def path(d, fill="none", stroke=INK, sw=0.3, extra=""):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{f(sw)}" {extra}/>'


def t(x, y, s, size=1.9, anchor="start", fill=INK, weight="normal", family=MONO):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return (f'<text x="{f(x)}" y="{f(y)}" font-size="{f(size)}" text-anchor="{anchor}" '
            f'fill="{fill}" font-weight="{weight}" font-family="{family}">{s}</text>')


def arrow(x1, y1, x2, y2, color=INK, sw=0.25):
    a = math.atan2(y2 - y1, x2 - x1)
    hl, hw = 1.8, 0.8
    bx, by = x2 - hl * math.cos(a), y2 - hl * math.sin(a)
    px, py = -math.sin(a) * hw, math.cos(a) * hw
    return (line(x1, y1, bx, by, color, sw) +
            poly([(x2, y2), (bx + px, by + py), (bx - px, by - py)], color, color, 0.05))


def call(n, px, py, cx, cy):
    """Numbered callout: dot on the part, leader line, numbered circle."""
    return (line(px, py, cx, cy, INK, 0.12) + circ(px, py, 0.38, INK, INK, 0.05) +
            circ(cx, cy, 1.75, PAPER, INK, 0.2) + t(cx, cy + 0.68, str(n), 1.9, "middle", INK, "bold"))


def dimh(x1, x2, y, label):
    return (line(x1, y, x2, y, DIM, 0.15) + line(x1, y - 1, x1, y + 1, DIM, 0.15) +
            line(x2, y - 1, x2, y + 1, DIM, 0.15) + t((x1 + x2) / 2, y + 2.7, label, 1.8, "middle", DIM))


def dimv(x, y1, y2, label):
    return (line(x, y1, x, y2, DIM, 0.15) + line(x - 1, y1, x + 1, y1, DIM, 0.15) +
            line(x - 1, y2, x + 1, y2, DIM, 0.15) + t(x + 1.8, (y1 + y2) / 2 + 0.6, label, 1.8, "start", DIM))


def panel(ox, oy, inner):
    return f'<g transform="translate({f(ox)},{f(oy)}) scale({S})">{inner}</g>'


def px_text(x, y, s, size=14, fill=INK, weight="normal", family=MONO, anchor="start"):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return (f'<text x="{f(x)}" y="{f(y)}" font-size="{size}" fill="{fill}" font-weight="{weight}" '
            f'font-family="{family}" text-anchor="{anchor}">{s}</text>')


def l2g(x, y, th):
    """Local body point (pivot origin, y down) -> desk frame after leaning back th degrees."""
    a = math.radians(th)
    return x * math.cos(a) + y * math.sin(a), -x * math.sin(a) + y * math.cos(a)


def stand_geometry(H, hh, Ls, th):
    d = H - hh
    hx, hy = l2g(0, -d, th)
    fx = hx - math.sqrt(max(Ls * Ls - hy * hy, 0.0))
    return (hx, hy), (fx, 0.0)


def desk(x1, x2):
    s = [line(x1, 0, x2, 0, INK, 0.4)]
    x = x1
    while x < x2:
        s.append(line(x, 0, x - 2, 2.2, DIM, 0.12))
        x += 3
    return "".join(s)


def sheet(w, h, title, sub, body, info):
    head = (px_text(60, 62, title, 30, INK, "bold", SANS) + px_text(60, 92, sub, 15, DIM) +
            px_text(w - 60, 52, "TENTATIVE · NOT A FINAL DESIGN", 13, ORANGE, "bold", MONO, "end") +
            px_text(w - 60, 72, "original concept · dimensions are guesses · 2026-11-25", 12, DIM, "normal", MONO, "end") +
            f'<line x1="{w-60-60}" y1="96" x2="{w-60}" y2="96" stroke="{INK}" stroke-width="2"/>' +
            px_text(w - 60 - 30, 114, "10 mm", 11, DIM, "normal", MONO, "middle"))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'<rect width="{w}" height="{h}" fill="{PAPER}"/>{head}{body}{info}</svg>')


def info_block(x, y, legend, pros, cons, col=520):
    s = [px_text(x, y, "CONTROLS (numbers match the callouts)", 13, INK, "bold")]
    for i, ln in enumerate(legend):
        s.append(px_text(x, y + 24 + i * 20, ln, 13))
    x2 = x + col + 60
    s.append(px_text(x2, y, "+ WHY IT MIGHT WORK", 13, "#2f6f3a", "bold"))
    for i, ln in enumerate(pros):
        s.append(px_text(x2, y + 24 + i * 20, ln, 13))
    x3 = x2 + col + 40
    s.append(px_text(x3, y, "- TRADEOFFS / RISKS", 13, "#9a2f1a", "bold"))
    for i, ln in enumerate(cons):
        s.append(px_text(x3, y + 24 + i * 20, ln, 13))
    return "".join(s)


def open_side(Px, Py, th, H, D, hh, Ls, grille_y, mouth_deg, draw_local, draw_stand, note1, note3=""):
    """Side view with the body leaning back `th` degrees on its stand, resting on a desk."""
    (hx, hy), (fx, fy) = stand_geometry(H, hh, Ls, th)
    right = D * math.cos(math.radians(th)) + 14
    s = [desk(fx - 14, right + 40)]
    s.append(f'<g transform="rotate({f(-th)})">{draw_local}</g>')
    s.append(draw_stand(hx, hy, fx, fy))
    # port normal vs direction to mouth
    gx, gy = l2g(D, -(H - grille_y), th)
    nx, ny = math.cos(math.radians(th)), -math.sin(math.radians(th))
    mx, my = math.cos(math.radians(mouth_deg)), -math.sin(math.radians(mouth_deg))
    s.append(arrow(gx, gy, gx + 22 * nx, gy + 22 * ny, "#2f6f3a", 0.3))
    s.append(arrow(gx, gy, gx + 30 * mx, gy + 30 * my, ORANGE, 0.3))
    s.append(t(gx + 22 * nx + 1.5, gy + 22 * ny + 0.8, f"port faces {th:.0f}° up", 1.8, "start", "#2f6f3a"))
    s.append(t(gx + 30 * mx + 1.5, gy + 30 * my - 0.5, f"to mouth ~{mouth_deg:.0f}° up", 1.8, "start", ORANGE))
    stab = stability(H, D, th)
    where = "behind" if stab < 0 else "IN FRONT OF"
    s.append(t(fx, 6.2, note1, 1.7, "start", DIM))
    s.append(t(fx, 9.0, f"opens ~{open_angle(th, hh, H, Ls):.0f}° from the body, body leans {th:.0f}° back from vertical", 1.7, "start", DIM))
    s.append(t(fx, 11.8, f"balance: centre of mass {abs(stab):.0f} mm {where} the pivot{note3}", 1.7, "start", DIM))
    return panel(Px, Py, "".join(s)), fx, right


def open_angle(th, hh, H, Ls):
    (hx, hy), (fx, fy) = stand_geometry(H, hh, Ls, th)
    sd = ((fx - hx), (fy - hy))
    bd = l2g(0, 1, th)  # direction along the rear face, downwards
    n = math.hypot(*sd)
    cosv = (sd[0] * bd[0] + sd[1] * bd[1]) / n
    return math.degrees(math.acos(max(-1, min(1, cosv))))


def stability(H, D, th):
    """Centre of mass (uniform body) relative to the bottom-rear pivot, mm. Negative = rests on the stand."""
    return l2g(D / 2, -H / 2, th)[0]


def slab(hx, hy, fx, fy, thick, color, foot=True):
    a = math.degrees(math.atan2(fy - hy, fx - hx))
    L = math.hypot(fx - hx, fy - hy)
    s = (f'<g transform="translate({f(hx)},{f(hy)}) rotate({f(a)})">' +
         rr(0, -thick / 2, L, thick, thick / 2.2, color, INK, 0.25) + '</g>')
    s += circ(hx, hy, 0.9, INK, INK, 0.05)
    if foot:
        s += rr(fx - 1.6, -0.9, 3.2, 1.8, 0.7, "#3a3836", INK, 0.15)
    return s


# =================================================================== CONCEPT A
def concept_a(out_dir):
    W, H, D = 58, 92, 20
    BODY, CHAR, GREY, SHADE = "#ebe5d8", "#35332f", "#a8a398", "#d8d1c2"
    TH, HH, LS = 30, 20, 68

    def front(rear=False):
        g = []
        sx = -1 if rear else 1
        def X(x):  # mirror for rear view
            return W - x if rear else x
        # protruding parts first
        lx = W - 2 if rear else -4
        g.append(rr(lx, 16, 6, 38, 3, ORANGE, INK, 0.25))                       # lever (viewer's left in front view)
        sbx = -2.5 if rear else W - 0.5
        g.append(rr(sbx, 20, 3, 8, 1.2, GREY, INK, 0.2))                         # optional send button
        g.append(rr(0, 0, W, H, 4, BODY, INK, 0.3))
        if not rear:
            for i in range(4):
                g.append(line(-3, 28 + i * 4, -0.8, 28 + i * 4, INK, 0.2))
            for i in range(9):  # slit grille
                g.append(rr(7, 8.5 + i * 3.3, 44, 1.6, 0.8, CHAR, CHAR, 0.05))
            g.append(circ(29, 22.5, 3.2, "none", ORANGE, 0.25, 'stroke-dasharray="0.8 0.6"'))
            for k, (x, lab) in enumerate(((14, "DICT"), (29, "TALK"), (44, "OPEN"))):
                g.append(circ(x, 43.5, 1.5, ORANGE if k == 0 else "#cfc8b8", INK, 0.2))
                g.append(t(x, 48.2, lab, 1.7, "middle"))
                g.append(line(x, 49.6, x, 51.2, INK, 0.2))
            g.append(rr(9, 54, 40, 4.5, 2.25, CHAR, INK, 0.2))
            g.append(rr(10.5, 52.6, 7, 7.3, 1.4, ORANGE, INK, 0.25))
            for x in (27, 30, 33):
                g.append(circ(x, 76, 0.7, CHAR, CHAR, 0.05))
            g.append(t(9, 87, "talk.01", 3.2, "start", CHAR, "bold", SANS))
            g.append(call(1, 29, 22.5, W + 8, 14))
            g.append(call(2, -3.2, 35, -9.5, 35))
            g.append(call("2b", W + 1.5, 24, W + 8, 24))
            g.append(call(3, 14, 56.2, W + 8, 56))
            g.append(call(4, 14, 43.5, W + 8, 43.5))
            g.append(call(5, 30, 76, W + 8, 76))
            g.append(call(6, W, 70, W + 8, 70))
            g.append(dimh(0, W, H + 6, f"{W}"))
            g.append(dimv(-13.5, 0, H, f"{H}"))
        else:
            g.append(rr(5, 20, 48, 68, 3, SHADE, INK, 0.25))                        # stand slab, closed
            g.append(circ(29, 88, 4, BODY, INK, 0.2))                                # finger notch
            g.append(rr(9, 18, 6, 4, 1, CHAR, INK, 0.15))
            g.append(rr(43, 18, 6, 4, 1, CHAR, INK, 0.15))
            for x in (8, 50):
                g.append(circ(x, 9, 1.1, "none", INK, 0.2))
                g.append(line(x - 0.7, 9, x + 0.7, 9, INK, 0.15))
            g.append(t(29, 55, "stand slab", 1.9, "middle", DIM))
            g.append(t(29, 58, "(flush when closed)", 1.7, "middle", DIM))
            g.append(call(7, 29, 40, W + 8, 40))
            g.append(call(8, 10, H - 0.4, -6, H + 4))
        return panel_wrap(g)

    def panel_wrap(g):
        return "".join(g)

    def side_local(closed_stand=True):
        """Lever-side view, front to the right; local origin = bottom-rear corner."""
        g = []
        g.append(rr(0, -H, D, H, 3, BODY, INK, 0.3))
        if closed_stand:
            g.append(rr(0, -H + HH, 2.4, H - HH - 4, 0.8, SHADE, INK, 0.15))          # closed stand slab (flush)
        g.append(rr(6, -H + 16, 8, 38, 4, ORANGE, INK, 0.25))                       # lever seen from its side
        for i in range(4):
            g.append(line(8, -H + 28 + i * 4, 12, -H + 28 + i * 4, INK, 0.2))
        g.append(rr(2.5, 0, 15, 1.1, 0.5, "#3a3836", INK, 0.1))                      # foot strip
        return "".join(g)

    # --- assemble
    x_front, x_rear, x_side, y0 = 96, 560, 1000, 200
    body = []
    body.append(px_text(x_front, y0 - 30, "FRONT", 16, INK, "bold", SANS))
    body.append(px_text(x_rear, y0 - 30, "REAR · stand closed", 16, INK, "bold", SANS))
    body.append(px_text(x_side, y0 - 30, "SIDE · lever side", 16, INK, "bold", SANS))
    body.append(panel(x_front, y0, front(False)))
    body.append(panel(x_rear, y0, front(True)))
    base = y0 + H * S
    side_closed = side_local() + dimh(0, D, 6, f"{D}")
    body.append(panel(x_side, base, side_closed))
    Px = 1548
    body.append(px_text(1170, y0 - 30, f"SIDE · stand open, on desk", 16, INK, "bold", SANS))

    def stand(hx, hy, fx, fy):
        return slab(hx, hy, fx, fy, 3, "#c9c2b3")

    svg_open, fx, right = open_side(Px, base, TH, H, D, HH, LS, 22.5, 40, side_local(False), stand,
                                    f"stand: flat slab {LS} mm long, hinged {HH} mm below the top")
    body.append(svg_open)

    legend = ["1 mic port, front-firing, behind the slits",
              "2 talk paddle, left edge (thumb); 2b optional send key",
              "3 mode slider: DICT / TALK / OPEN (3-position, detent)",
              "4 three lamps show mode and mute/talk state",
              "5 optional buzzer holes (far from the mic)",
              "6 USB-C, right edge: cable runs to the laptop",
              "7 flat rear stand slab    8 rubber feet"]
    pros = ["Most pager/walkie-like; easy to hold upright",
            "Thumb paddle is the natural walkie push-to-talk",
            "Slider + 3 lamps: mode stays visible, cheap parts",
            "Full-width stand: wide footprint, flush when closed",
            "Slit grille is original (not dot-matrix)"]
    cons = ["Left-edge lever sits closest to TE's layout: give it",
            "  a different shape/position before CAD",
            "Slider can be bumped in a pocket: needs a firm detent",
            "Flat slab adds ~3 mm to depth; use a metal hinge pin",
            "Two-tone body NOT used on purpose (single warm cream)"]
    info = info_block(96, 880, legend, pros, cons)
    svg = sheet(1760, 1060, "talk.01 · CONCEPT A — PAGER",
                "Thumb paddle · slider mode switch · slit grille · full-back flip stand", "".join(body), info)
    write(out_dir, "A-pager.svg", svg)


# =================================================================== CONCEPT B
def concept_b(out_dir):
    W, H, D = 96, 48, 24
    BODY, BAR, CHAR, BRASS = "#464b43", "#ece5d5", "#23251f", "#c9a24b"
    TH, HH, LS = 40, 8, 38

    def front(rear=False):
        g = []
        if not rear:
            g.append(rr(12, -4, 72, 5.5, 1.6, BAR, INK, 0.25))                       # key bar above the body
            g.append(rr(12, -4, 72, 1.2, 0.6, ORANGE, INK, 0.05))
        g.append(rr(0, 0, W, H, 3, BODY, INK, 0.3))
        if not rear:
            for i in range(9):  # vertical slots
                g.append(rr(7 + i * 2.6, 9, 1.4, 30, 0.7, CHAR, "#111", 0.05))
            g.append(circ(18, 24, 3.2, "none", ORANGE, 0.25, 'stroke-dasharray="0.8 0.6"'))
            for k, (x, lab) in enumerate(((43, "DICT"), (55, "TALK"), (67, "OPEN"))):
                g.append(rr(x - 3.6, 17.5, 7.2, 7.2, 1.3, BAR, INK, 0.25))
                g.append(circ(x, 21.1, 1.1, ORANGE if k == 0 else "#b9b3a2", INK, 0.15))
                g.append(t(x, 30.6, lab, 1.7, "middle", BAR))
            for x in (82, 84.6, 87.2):
                g.append(circ(x, 12, 0.7, CHAR, "#111", 0.05))
            g.append(t(77, 41, "talk.01", 3.2, "start", BAR, "bold", SANS))
            g.append(rr(8, H - 0.2, 14, 1.2, 0.5, "#111", INK, 0.1))
            g.append(rr(74, H - 0.2, 14, 1.2, 0.5, "#111", INK, 0.1))
            g.append(call(1, 11, 13, -6, 13))
            g.append(call(4, 43, 21.1, 38, -12))
            g.append(call(2, 48, -4, 48, -12))
            g.append(call(3, 67, 21.1, 66, -12))
            g.append(call(5, 84.6, 12, 84, -12))
            g.append(call(6, W, 30, W + 8, 30))
            g.append(dimh(0, W, H + 6, f"{W}"))
            g.append(dimv(-12.5, 0, H, f"{H}"))
        else:
            g.append(rr(7, 8, 82, 38, 2.5, "#5a6056", INK, 0.25))                    # flap
            g.append(circ(48, 46, 3.6, BODY, INK, 0.2))                               # notch
            g.append(rr(14, 6.5, 8, 3, 1, CHAR, INK, 0.15))
            g.append(rr(74, 6.5, 8, 3, 1, CHAR, INK, 0.15))
            g.append(t(48, 28, "stand flap, full width", 1.9, "middle", BAR))
            g.append(t(48, 31, "(flush when closed)", 1.7, "middle", BAR))
            g.append(call(7, 70, 20, W + 8, 20))
        return "".join(g)

    def side_local(closed_stand=True):
        g = []
        g.append(rr(0, -H, D, H, 2.5, BODY, INK, 0.3))
        if closed_stand:
            g.append(rr(0, -H + HH, 2.2, H - HH - 1.5, 0.8, "#5a6056", INK, 0.15))
        # key bar hinged at the rear, raised ~1.5 mm at the front
        g.append(poly([(3, -H), (3, -H - 3), (22, -H - 4.5), (22, -H - 1.5)], BAR, INK, 0.25))
        g.append(rr(19.8, -H - 4.6, 2.4, 3.2, 0.5, ORANGE, INK, 0.12))
        g.append(circ(3, -H - 1.5, 0.9, INK, INK, 0.05))
        g.append(circ(D / 2, -H / 2, 2.6, "none", ORANGE, 0.22, 'stroke-dasharray="0.7 0.5"'))
        g.append(rr(2.5, 0, 19, 1.1, 0.5, "#111", INK, 0.1))
        return "".join(g)

    x_front, x_rear = 96, 800
    y1 = 210
    body = []
    body.append(px_text(x_front, y1 - 70, "FRONT", 16, INK, "bold", SANS))
    body.append(px_text(x_rear, y1 - 70, "REAR · stand closed", 16, INK, "bold", SANS))
    body.append(panel(x_front, y1, front(False)))
    body.append(panel(x_rear, y1, front(True)))
    y2 = 1000
    body.append(px_text(96, y2 - 390, "SIDE · mic end", 16, INK, "bold", SANS))
    body.append(panel(96, y2, side_local() + dimh(0, D, 6, f"{D}") + t(D + 2, -H - 3, "bar travel ~3 mm", 1.7, "start", DIM)))
    body.append(px_text(400, y2 - 390, "SIDE · stand open, on desk", 16, INK, "bold", SANS))

    def stand(hx, hy, fx, fy):
        return slab(hx, hy, fx, fy, 2.6, "#7a8074")

    svg_open, fx, right = open_side(689, y2, TH, H, D, HH, LS, 24, 40, side_local(False), stand,
                                    f"stand: full-width flap {LS} mm long, hinged {HH} mm below the top",
                                    f" (needs lean > ~{math.degrees(math.atan(D / H)):.0f}°: tan th > D/H)")
    body.append(svg_open)

    legend = ["1 mic port: slots on the front (option: end-fire at left end)",
              "2 key bar on top: press down to talk (telegraph key)",
              "3 three preset keys DICT / TALK / OPEN, lamp inside each",
              "4 lit key = current mode (no hidden state)",
              "5 optional buzzer holes, far end from the mic",
              "6 USB-C on the right end: cable runs to the laptop",
              "7 full-width stand flap    8 rubber feet"]
    pros = ["Most distinctive and toy-like; big satisfying key bar",
            "Preset keys + lamps: current mode is obvious at a glance",
            "Wide body: room for electronics, buzzer, future batteries",
            "Strong desk presence; reads clearly as a 'key'"]
    cons = ["Handheld use is awkward: held like a bar, mic at one end",
            "Needs >= ~30° recline to stand (tall-thin it is not)",
            "Big bar travel may add lever/handling noise: isolate it",
            "Mode keys are momentary: firmware must remember the state",
            "Front slots look like TE's grille idea: keep them vertical"]
    info = info_block(96, 1125, legend, pros, cons)
    svg = sheet(1760, 1290, "talk.01 · CONCEPT B — TELEGRAPH",
                "Top key bar · preset mode keys · vertical-slot grille · full-width flap stand", "".join(body), info)
    write(out_dir, "B-telegraph.svg", svg)


# =================================================================== CONCEPT C
def concept_c(out_dir):
    W, H, D = 60, 92, 22
    BODY, FACE, TEAL, CHAR, SHADE = "#e3d6b9", "#f0e9d9", "#2b7a78", "#2d2924", "#cdbf9f"
    TH, HH, LS = 28, 14, 72

    def front(rear=False):
        g = []
        if not rear:
            g.append(rr(-3.5, 22, 5, 16, 2.5, TEAL, INK, 0.25))                      # slide lever tab
        g.append(rr(0, 0, W, H, 6, BODY, INK, 0.3))
        if not rear:
            g.append(rr(4, 4, W - 8, H - 8, 4, FACE, "#b9ab8a", 0.2))
            for r in (4.5, 8.5, 12.5, 16.5):  # concentric segmented rings
                g.append(circ(30, 26, r, "none", CHAR, 1.3, f'stroke-dasharray="{f(r*0.9)} 0.9"'))
            g.append(circ(30, 26, 1.8, CHAR, CHAR, 0.05))
            g.append(circ(30, 65.5, 12, "#f6f1e4", INK, 0.3))                           # dial
            for k in range(24):
                a = math.radians(k * 15)
                g.append(line(30 + 10.4 * math.sin(a), 65.5 - 10.4 * math.cos(a),
                              30 + 11.5 * math.sin(a), 65.5 - 11.5 * math.cos(a), "#b9ab8a", 0.2))
            a0 = math.radians(-50)
            g.append(line(30, 65.5, 30 + 9 * math.sin(a0), 65.5 - 9 * math.cos(a0), TEAL, 1.6, 'stroke-linecap="round"'))
            g.append(circ(30, 65.5, 1.8, TEAL, INK, 0.2))
            for ang, lab in ((-50, "DICT"), (0, "TALK"), (50, "OPEN")):
                a = math.radians(ang)
                g.append(line(30 + 13.5 * math.sin(a), 65.5 - 13.5 * math.cos(a),
                              30 + 15.6 * math.sin(a), 65.5 - 15.6 * math.cos(a), INK, 0.25))
                g.append(t(30 + 19.3 * math.sin(a), 65.5 - 19.3 * math.cos(a) + 0.6, lab, 1.7, "middle"))
            g.append(circ(51, 85, 1.8, ORANGE, INK, 0.25))
            for x in (27, 30, 33):
                g.append(circ(x, 82, 0.7, CHAR, CHAR, 0.05))
            g.append(t(9, 86.5, "talk.01", 3.2, "start", CHAR, "bold", SANS))
            g.append(line(-1.4, 17, -1.4, 52, TEAL, 0.25, 'stroke-dasharray="1 0.8"'))
            g.append(t(-3.5, 56, "latch", 1.6, "middle", TEAL))
            g.append(call(1, 30, 26, W + 8, 14))
            g.append(call(2, -3.2, 30, -9.5, 30))
            g.append(call(3, 38, 65.5, W + 8, 56))
            g.append(call(4, 51, 85, W + 8, 85))
            g.append(call(5, 30, 82, W + 8, 74))
            g.append(call(6, W, 66, W + 8, 66))
            g.append(dimh(0, W, H + 6, f"{W}"))
            g.append(dimv(-13.5, 0, H, f"{H}"))
        else:
            g.append(rr(3.5, 12.5, W - 7, 76, 4.5, SHADE, INK, 0.25))                # groove
            g.append(path(f"M6,14 L6,86 L{W-6},86 L{W-6},14", "none", CHAR, 2.6, 'stroke-linecap="round" stroke-linejoin="round"'))
            g.append(circ(6, 14, 1.8, "#8a8070", INK, 0.2))
            g.append(circ(W - 6, 14, 1.8, "#8a8070", INK, 0.2))
            g.append(circ(30, H, 3.5, FACE, INK, 0.2))                                 # notch
            g.append(t(30, 52, "bail stand (U-frame)", 1.9, "middle", DIM))
            g.append(t(30, 55, "folds into the groove", 1.7, "middle", DIM))
            g.append(call(7, W - 6, 50, W + 8, 50))
        return "".join(g)

    def side_local(closed_stand=True):
        g = []
        g.append(rr(0, -H, D, H, 4, BODY, INK, 0.3))
        if closed_stand:
            g.append(rr(0, -H + HH, 2.6, H - HH - 6, 1.2, CHAR, INK, 0.15))            # bail in its groove
        g.append(rr(7, -H + 22, 8, 16, 4, TEAL, INK, 0.25))                           # slide lever seen from its side
        g.append(line(11, -H + 17, 11, -H + 52, TEAL, 0.35, 'stroke-dasharray="1 0.8"'))
        g.append(rr(3, 0, 16, 1.1, 0.5, "#3a3836", INK, 0.1))
        return "".join(g)

    x_front, x_rear, x_side, y0 = 96, 580, 1040, 200
    body = []
    body.append(px_text(x_front, y0 - 30, "FRONT", 16, INK, "bold", SANS))
    body.append(px_text(x_rear, y0 - 30, "REAR · stand closed", 16, INK, "bold", SANS))
    body.append(px_text(x_side, y0 - 30, "SIDE · lever side", 16, INK, "bold", SANS))
    body.append(panel(x_front, y0, front(False)))
    body.append(panel(x_rear, y0, front(True)))
    base = y0 + H * S
    body.append(panel(x_side, base, side_local() + dimh(0, D, 6, f"{D}")))
    Px = 1565
    body.append(px_text(1220, y0 - 30, "SIDE · stand open, on desk", 16, INK, "bold", SANS))

    def stand(hx, hy, fx, fy):
        a = math.degrees(math.atan2(fy - hy, fx - hx))
        L = math.hypot(fx - hx, fy - hy)
        s = (f'<g transform="translate({f(hx)},{f(hy)}) rotate({f(a)})">' +
             rr(0, -1.3, L, 2.6, 1.3, CHAR, INK, 0.2) + '</g>' + circ(hx, hy, 0.9, "#8a8070", INK, 0.1) +
             rr(fx - 1.6, -0.9, 3.2, 1.8, 0.7, "#3a3836", INK, 0.15))
        return s

    svg_open, fx, right = open_side(Px, base, TH, H, D, HH, LS, 26, 40, side_local(False), stand,
                                    f"stand: U-frame bail {LS} mm long; a 2nd detent (~45°, not drawn) would aim higher")
    body.append(svg_open)

    legend = ["1 mic port: single hole in the centre of the ring grille",
              "2 slide lever, left edge: push down = talk; click on = latch",
              "3 rotary band dial: DICT / TALK / OPEN (clicks, visible)",
              "4 status lamp (also shows mute / latched)",
              "5 optional buzzer holes",
              "6 USB-C, right edge: cable runs to the laptop",
              "7 bail stand, also a carry loop    8 rubber feet"]
    pros = ["Rotary band dial is the most radio-like; mode is tactile",
            "One lever covers momentary AND hands-free (latch)",
            "Bail stand doubles as a lanyard / carry loop",
            "Ring grille is original (segmented rings)"]
    cons = ["Most mechanics: dial + latch slider + bail: more tuning",
            "Rotary switch must be panel-mount: needs ~20 mm depth",
            "Latch is an extra mode: more firmware states to test",
            "Ring grille is decorative; real port is one small hole",
            "Round dial + side lever: keep it from reading as a TE copy"]
    info = info_block(96, 880, legend, pros, cons)
    svg = sheet(1760, 1060, "talk.01 · CONCEPT C — RADIO",
                "Rotary band dial · slide-latch lever · ring grille · bail stand / carry loop", "".join(body), info)
    write(out_dir, "C-radio.svg", svg)


def write(out_dir, name, svg):
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, name), "w", encoding="utf-8") as fh:
        fh.write(svg)
    print("wrote", os.path.join(out_dir, name))


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    concept_a(out)
    concept_b(out)
    concept_c(out)
