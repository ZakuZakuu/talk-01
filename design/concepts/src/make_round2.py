#!/usr/bin/env python3
"""Round-2 concept sheets for talk.01: D Dial, E Armed, F Handset. Standard library only.

Each concept carries ONE organising idea and deliberately leaves other ideas out.
A small shared baseline (top USB-C, left-edge three-stage lever, swappable back
plate with a hackable bay, quarter-turn feet) is drawn identically in all three.
All dimensions are TENTATIVE.

    python3 design/concepts/src/make_round2.py design/concepts/round-2
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_concepts import (INK, PAPER, DIM, ORANGE, f, rr, circ, line, path, t,  # noqa: E402
                           call, dimh, dimv, panel, px_text, open_side, slab, sheet, write, SANS)

SC = 5.0           # px per mm for round 2 (round 1 used 6)
CREAM = "#efe9d6"
W_, H_, D_ = 58, 92, 18
PF = ("M10,0 H46 Q55,0 55.5,9 L59.6,82 Q60,92 50,92 H10 Q0,92 0.4,82 "
      "L2.2,66 Q9,52 2.2,38 L4.5,10 Q4.8,0 10,0 Z")      # tapered, thumb-scooped outline for F


def P(ox, oy, inner):
    return panel(ox, oy, inner, SC)


def prot(g, x, y, w, h, r, fill, rear, W=W_, sw=0.25):
    """Protrusion beyond the left edge; mirrored to the right edge on the rear view."""
    xx = (W - x - w) if rear else x
    g.append(rr(xx, y, w, h, r, fill, INK, sw))


# ----------------------------------------------------------------- shared bits
def lever_strip(x, y, w=340):
    s = [px_text(x, y - 24, "LEVER TRAVEL · shared baseline (about 3 mm)", 12, INK, "bold")]
    s.append(f'<line x1="{x}" y1="{y}" x2="{x + w}" y2="{y}" stroke="{INK}" stroke-width="3"/>')
    for fr, a, b in ((0.0, "REST", ""), (0.36, "HOLD", "talk"), (0.70, "CLICK", "latch"), (1.0, "PUSH", "send")):
        cx = x + w * fr
        s.append(f'<circle cx="{f(cx)}" cy="{y}" r="6" fill="{ORANGE if fr > 0.5 else PAPER}" stroke="{INK}" stroke-width="2"/>')
        s.append(px_text(cx, y + 26, a, 12, INK, "bold", "monospace", "middle"))
        s.append(px_text(cx, y + 42, b, 12, DIM, "normal", "monospace", "middle"))
    s.append(px_text(x, y + 68, "light press = hold-to-talk · bottom-out click = latch", 11, DIM))
    s.append(px_text(x, y + 84, "extra firm push past the click = send (needs a compliant stop)", 11, DIM))
    return "".join(s)


def info2(x, y, legend, idea, left_out, risks, colw=580):
    s = [px_text(x, y, "CONTROLS (numbers match the callouts)", 13, INK, "bold")]
    for i, ln in enumerate(legend):
        s.append(px_text(x, y + 24 + i * 20, ln, 13))
    x2 = x + colw
    s.append(px_text(x2, y, "THE ONE IDEA", 13, "#2f6f3a", "bold"))
    yy = y + 24
    for ln in idea:
        s.append(px_text(x2, yy, ln, 13))
        yy += 20
    yy += 16
    s.append(px_text(x2, yy, "LEFT OUT ON PURPOSE", 13, DIM, "bold"))
    yy += 24
    for ln in left_out:
        s.append(px_text(x2, yy, ln, 13))
        yy += 20
    x3 = x2 + colw
    s.append(px_text(x3, y, "TRADEOFFS / RISKS", 13, "#9a2f1a", "bold"))
    for i, ln in enumerate(risks):
        s.append(px_text(x3, y + 24 + i * 20, ln, 13))
    return "".join(s)


def top_view(W, D, x0, usb_x, body, extra=""):
    g = [rr(x0, 0, W, D, 4, body, INK, 0.3),
         rr(usb_x - 4.5, D / 2 - 1.6, 9, 3.2, 1.6, "#1b1b1b", INK, 0.15), extra,
         t(x0 + W / 2, -2.2, "back", 2.0, "middle", DIM), t(x0 + W / 2, D + 4.6, "front", 2.0, "middle", DIM),
         call(6, usb_x + 4.5, D / 2, x0 + W + 9, D / 2),
         dimh(x0, x0 + W, D + 10, f"{W}"), dimv(x0 + W + 17, 0, D, f"{D}")]
    return "".join(g)


def bay(kind, body, cx):
    g = []
    if kind == "rect":
        g.append(rr(0, 0, 58, 92, 6, body, INK, 0.3))
        g.append(rr(3, 3, 52, 86, 4.5, "#c9c3b4", "#8a8374", 0.25))
    else:
        g.append(path(PF, body, INK, 0.3))
        g.append(rr(8, 4, 44, 84, 4, "#c9c3b4", "#8a8374", 0.25))
    g.append(rr(cx - 10.5, 6.5, 21, 17.5, 1, "#2f6b52", INK, 0.2))                   # dev board
    g.append(rr(cx - 4.5, 4.6, 9, 3.8, 0.8, "#cfcfcf", INK, 0.15))                    # USB-C shell
    g.append(circ(cx - 5.5, 19.2, 1.1, "#e6e6e6", INK, 0.12))
    g.append(circ(cx - 2.2, 19.2, 1.1, "#e6e6e6", INK, 0.12))
    g.append(t(cx + 0.2, 19.9, "BOOT RST", 1.7, "start", "#e8f1ea"))
    for i in range(4):
        g.append(rr(cx - 5 + i * 2.8, 27.4, 1.7, 1.7, 0.2, "#2b2a28", INK, 0.05))
    g.append(t(cx + 7, 29.0, "header", 1.7, "start", "#4a463e"))
    g.append(rr(cx - 17, 36, 34, 28, 2, "none", DIM, 0.25, 'stroke-dasharray="1.2 0.8"'))
    g.append(t(cx, 49, "space for", 1.9, "middle", "#4a463e"))
    g.append(t(cx, 52, "2xAAA or LiPo", 1.9, "middle", "#4a463e"))
    g.append(t(cx, 55, "(later)", 1.9, "middle", "#4a463e"))
    g.append(rr(cx - 17, 68, 34, 11, 1.2, "#f3efe4", INK, 0.15))
    g.append(t(cx - 15.5, 73.4, "talk.01 v0.1", 2.1, "start", INK, "bold"))
    g.append(t(cx - 15.5, 76.6, "docs: see repo", 1.7, "start", "#4a463e"))
    for i in range(3):
        for j in range(3):
            if (i + j) % 2 == 0 or (i == 1 and j == 1):
                g.append(rr(cx + 10 + i * 1.7, 69.6 + j * 1.7, 1.4, 1.4, 0.1, "#2b2a28", INK, 0.03))
    for sx in (-17.5, 17.5):
        g.append(circ(cx + sx, 85.4, 2.3, ORANGE, INK, 0.2))
        g.append(line(cx + sx - 1.6, 85.4, cx + sx + 1.6, 85.4, INK, 0.25))
    g.append(call("a", cx - 2.2, 19.2, 68, 10))
    g.append(call("b", cx + 3, 28.2, 68, 28))
    g.append(call("c", cx + 17, 50, 68, 50))
    g.append(call("d", cx + 17, 74, 68, 74))
    g.append(call(8, cx + 19.8, 85.4, 68, 86))
    return "".join(g)


def stage_text(x, y, s):
    return px_text(x, y, s, 12, DIM)


# ================================================================ D · DIAL
def concept_d(out):
    W, H, D = W_, H_, D_
    BODY, CHAR, SHADE = "#d9d4c8", "#2f2d2a", "#cbc5b6"
    WC = (15, 50)

    def front(rear=False):
        g = []
        prot(g, -3, 41, 4, 18, 2, CHAR, rear)                             # wheel rim through a slot
        prot(g, -2.4, 66, 4, 16, 2, ORANGE, rear)                         # lever
        prot(g, -3.8, 63.2, 5.2, 2.2, 1.1, BODY, rear)                    # shoulders
        prot(g, -3.8, 82.6, 5.2, 2.2, 1.1, BODY, rear)
        g.append(rr(0, 0, W, H, 7, BODY, INK, 0.3))
        if not rear:
            for i in range(5):
                g.append(line(-2.6, 43 + i * 3.2, -0.4, 43 + i * 3.2, "#8d8a84", 0.18))
            for a in (-50, -37.5, -25, -12.5, 0, 12.5, 25, 37.5, 50):          # sunburst grille
                g.append(f'<g transform="translate(34,34) rotate({a})">{rr(-0.9, -21, 1.8, 12, 0.9, CHAR, CHAR, 0.05)}</g>')
            g.append(circ(34, 34, 1.5, CHAR, CHAR, 0.05))
            g.append(circ(34, 34, 3.6, "none", ORANGE, 0.25, 'stroke-dasharray="0.8 0.6"'))
            g.append(circ(49, 8, 1.9, ORANGE, INK, 0.25))
            g.append(circ(WC[0], WC[1], 10.6, "none", INK, 0.3))
            g.append(circ(WC[0], WC[1], 9, CHAR, INK, 0.3))
            a0 = math.radians(40)
            g.append(line(WC[0], WC[1], WC[0] + 7.2 * math.sin(a0), WC[1] - 7.2 * math.cos(a0), ORANGE, 1.4, 'stroke-linecap="round"'))
            g.append(circ(WC[0], WC[1], 1.6, CREAM, INK, 0.15))
            for ang, lab in ((40, "DICT"), (80, "TALK"), (120, "OPEN"), (160, "LOCK")):
                a = math.radians(ang)
                g.append(line(WC[0] + 11.6 * math.sin(a), WC[1] - 11.6 * math.cos(a), WC[0] + 13.3 * math.sin(a), WC[1] - 13.3 * math.cos(a), INK, 0.25))
                g.append(t(WC[0] + 14.8 * math.sin(a), WC[1] - 14.8 * math.cos(a) + 0.7, lab, 2.0, "start"))
            for x in (38, 41, 44):
                g.append(circ(x, 72, 0.7, CHAR, CHAR, 0.05))
            g.append(t(26, 85, "talk.01", 3.2, "start", CHAR, "bold", SANS))
            g.append(call(1, 34, 34, W + 8, 20))
            g.append(call(2, -2.4, 74, -10, 74))
            g.append(call(3, -3, 50, -10, 50))
            g.append(call(9, -3.2, 64.3, -10, 62))
            g.append(call(4, 49, 8, W + 8, 8))
            g.append(call(5, 41, 72, W + 8, 72))
            g.append(dimh(0, W, H + 6, f"{W}"))
            g.append(dimv(-17, 0, H, f"{H}"))
        else:
            g.append(rr(2.5, 2.5, W - 5, H - 5, 5, SHADE, "#8a8374", 0.2))
            g.append(rr(7, 22, W - 14, 62, 3, "#bfb8a8", INK, 0.25))
            g.append(rr(11, 20, 7, 3.6, 1, CHAR, INK, 0.15))
            g.append(rr(40, 20, 7, 3.6, 1, CHAR, INK, 0.15))
            g.append(circ(29, 84, 3.6, SHADE, INK, 0.2))
            for sx in (12, 46):
                g.append(circ(sx, 88, 2.1, ORANGE, INK, 0.2))
                g.append(line(sx - 1.4, 88, sx + 1.4, 88, INK, 0.22))
            g.append(t(29, 52, "stand slab", 2.1, "middle", DIM))
            g.append(t(29, 55.4, "(part of the back plate)", 1.9, "middle", DIM))
            g.append(call(7, 47, 40, W + 8, 40))
            g.append(call(8, 46, 88, W + 8, 88))
        return "".join(g)

    def side(closed_stand=True):
        g = [rr(0, -H, D, H, 6.5, BODY, INK, 0.3)]
        if closed_stand:
            g.append(rr(0, -H + 22, 2.6, 62, 0.9, SHADE, INK, 0.15))
        g.append(rr(6.5, -H + 41, 5, 18, 2.5, CHAR, INK, 0.2))
        for i in range(5):
            g.append(line(7.2, -H + 43 + i * 3.2, 10.8, -H + 43 + i * 3.2, "#8d8a84", 0.15))
        g.append(rr(3, -H + 63.2, 12, 2.2, 1, BODY, INK, 0.2))
        g.append(rr(3, -H + 82.6, 12, 2.2, 1, BODY, INK, 0.2))
        g.append(rr(4, -H + 66, 10, 16, 5, ORANGE, INK, 0.25))
        g.append(rr(2.5, 0, 13, 1.1, 0.5, "#3a3836", INK, 0.1))
        return "".join(g)

    x0, y0 = 96, 200
    base = y0 + H * SC
    body = [px_text(x0, y0 - 40, "FRONT", 16, INK, "bold", SANS), px_text(486, y0 - 40, "REAR · back plate with stand", 16, INK, "bold", SANS),
            px_text(876, y0 - 40, "REAR · plate off (hackable bay)", 16, INK, "bold", SANS), px_text(1266, y0 - 40, "SIDE · left", 16, INK, "bold", SANS),
            px_text(1450, y0 - 40, "SIDE · stand open, on desk", 16, INK, "bold", SANS),
            P(x0, y0, front(False)), P(486, y0, front(True)), P(876, y0, bay("rect", BODY, 29)),
            P(1266, base, side(True) + dimh(0, D, 6, f"{D}"))]
    svg_open, fx, right = open_side(1725, base, 30, H, D, 22, 64, 34, 40, side(False),
                                    lambda hx, hy, fx_, fy: slab(hx, hy, fx_, fy, 3, "#bfb8a8"),
                                    "stand: slab 64 mm, hinged 22 mm below the top; part of the back plate",
                                    "", SC)
    body.append(svg_open)
    body.append(px_text(96, 790, "TOP EDGE", 16, INK, "bold", SANS))
    body.append(P(100, 810, top_view(W, D, 4, 42, BODY, rr(1, 4.5, 3.2, 9, 1.4, CHAR, INK, 0.2) + rr(1.6, 4, 2.6, 10, 1.2, ORANGE, INK, 0.2))))
    body.append(lever_strip(660, 850))
    legend = ["1 mic port: hole at the centre of the sunburst slots",
              "2 left-edge lever, 3-stage, sits between two shoulders",
              "3 THE WHEEL: mode DICT / TALK / OPEN / LOCK, thumb-rolled",
              "4 on-air lamp (also shows latch)   5 optional buzzer holes",
              "6 USB-C on the top edge (see TOP EDGE)",
              "7 stand slab, part of the swappable back plate",
              "8 quarter-turn feet hold the back plate",
              "9 shoulders: raised edges that guard the lever",
              "a-d bay: BOOT/RST, header, battery space, info label"]
    idea = ["The thumb wheel is the product. One big, satisfying",
            "dial on the left edge chooses the mode, and one of its",
            "positions is LOCK. Everything else stays quiet."]
    left_out = ["no lid or guard (shoulders + the LOCK position do it)",
                "no slider, no row of lamps, no extra buttons",
                "no hidden second control: the wheel is the only mode input"]
    risks = ["The wheel is the hardest mechanism: a click detent plus an",
             "encoder or rotary switch, seen through a round window.",
             "It can be bumped in a bag: needs firm detents and friction.",
             "Wheel and lever share one edge: thumb travel needs a",
             "full-size print to check.",
             "Printing a thin window face needs care (FDM)."]
    info = info2(96, 1030, legend, idea, left_out, risks)
    write(out, "D-dial.svg", sheet(1920, 1340, "talk.01 · ROUND 2 · D — DIAL",
                                   "One idea: a thumb wheel is the whole interface · quiet body · shoulders protect the lever",
                                   "".join(body), info))


# ================================================================ E · ARMED
def concept_e(out):
    W, H, D = W_, H_, D_
    OLIVE, CHAR, DARK, LIGHT = "#5f6652", "#23261f", "#2b2f25", "#7a8062"

    def front(rear=False):
        g = []
        prot(g, -3.4, 36, 5.2, 36, 1.6, ORANGE, rear, sw=0.25)             # guard (closed)
        g.append(rr(0, 0, W, H, 5, OLIVE, INK, 0.3))
        if not rear:
            g.append(circ(-1.2, 36, 1.5, INK, INK, 0.05))
            g.append(rr(-1.6, 3, 3.2, 31, 1.2, "none", ORANGE, 0.2, 'stroke-dasharray="1 0.8"'))
            for i, w in enumerate((38, 34, 30, 26, 22)):                      # pyramid vent
                g.append(rr(29 - w / 2, 9 + i * 4.4, w, 2.2, 1.1, CHAR, CHAR, 0.05))
            g.append(circ(29, 19.9, 3.2, "none", ORANGE, 0.25, 'stroke-dasharray="0.8 0.6"'))
            g.append(circ(6, 6, 1.7, PAPER, INK, 0.2))
            for x0, lab, lit in ((9, "SAFE", False), (31, "ARMED", True)):
                g.append(rr(x0, 32, 18, 5.4, 1, DARK, INK, 0.2))
                g.append(t(x0 + 9, 35.8, lab, 2.1, "middle", ORANGE if lit else "#8a8f78", "bold"))
            for x, lab in ((14, "DICT"), (29, "TALK"), (44, "OPEN")):
                g.append(t(x, 46.2, lab, 2.0, "middle", CREAM))
                g.append(line(x, 47.2, x, 48.9, CREAM, 0.22))
            g.append(rr(9, 50, 40, 4.5, 2.25, DARK, INK, 0.2))
            g.append(rr(10.5, 48.7, 7, 7.3, 1.4, ORANGE, INK, 0.25))
            for x in (40, 43, 46):
                g.append(circ(x, 78, 0.7, CHAR, CHAR, 0.05))
            g.append(t(8, 86, "talk.01", 3.2, "start", CREAM, "bold", SANS))
            g.append(call(1, 29, 19.9, W + 8, 14))
            g.append(call(2, -2.4, 60, -10, 64))
            g.append(call(9, -2, 45, -10, 46))
            g.append(call(3, 17.5, 52, W + 8, 56))
            g.append(call(4, 49, 34.7, W + 8, 34))
            g.append(call(5, 43, 78, W + 8, 78))
            g.append(dimh(0, W, H + 6, f"{W}"))
            g.append(dimv(-17, 0, H, f"{H}"))
        else:
            g.append(rr(2.5, 2.5, W - 5, H - 5, 4, LIGHT, "#454b38", 0.2))
            g.append(rr(21, 20, 16, 66, 2.5, "#9aa07f", INK, 0.25))
            g.append(rr(23, 18.2, 12, 3.4, 1, CHAR, INK, 0.15))
            g.append(circ(29, 79, 3.2, OLIVE, INK, 0.25))
            for sx in (12, 46):
                g.append(circ(sx, 88, 2.1, ORANGE, INK, 0.2))
                g.append(line(sx - 1.4, 88, sx + 1.4, 88, INK, 0.22))
            g.append(t(29, 50, "stand bar", 2.1, "middle", CREAM))
            g.append(call(7, 29, 40, W + 8, 40))
            g.append(call(8, 46, 88, W + 8, 88))
            g.append(t(29, 70, "carabiner", 1.8, "middle", CREAM))
            g.append(t(29, 72.6, "hole", 1.8, "middle", CREAM))
        return "".join(g)

    def side(closed_stand=True, guard_open=False):
        g = [rr(0, -H, D, H, 5, OLIVE, INK, 0.3)]
        if closed_stand:
            g.append(rr(0, -H + 20, 2.6, 66, 0.9, LIGHT, INK, 0.15))
        if guard_open:
            g.append(rr(3, -H + 2, 12, 33, 2, ORANGE, INK, 0.25))
            g.append(rr(4, -H + 42, 10, 26, 5, CREAM, INK, 0.25))
        else:
            g.append(rr(3, -H + 36, 12, 36, 2, ORANGE, INK, 0.25))
            g.append(rr(4, -H + 42, 10, 26, 5, "none", CREAM, 0.15, 'stroke-dasharray="0.8 0.6"'))
        g.append(circ(4, -H + 36, 1.1, INK, INK, 0.05))
        g.append(circ(14, -H + 36, 1.1, INK, INK, 0.05))
        g.append(rr(2.5, 0, 13, 1.1, 0.5, "#111", INK, 0.1))
        return "".join(g)

    x0, y0 = 96, 200
    base = y0 + H * SC
    body = [px_text(x0, y0 - 40, "FRONT · guard closed", 16, INK, "bold", SANS), px_text(486, y0 - 40, "REAR · back plate with stand", 16, INK, "bold", SANS),
            px_text(876, y0 - 40, "REAR · plate off (hackable bay)", 16, INK, "bold", SANS), px_text(1266, y0 - 40, "SIDE · closed", 16, INK, "bold", SANS),
            px_text(1450, y0 - 40, "SIDE · guard up, stand open", 16, INK, "bold", SANS),
            P(x0, y0, front(False)), P(486, y0, front(True)), P(876, y0, bay("rect", OLIVE, 29)),
            P(1266, base, side(True, False) + dimh(0, D, 6, f"{D}"))]
    svg_open, fx, right = open_side(1725, base, 30, H, D, 20, 70, 20, 40, side(False, True),
                                    lambda hx, hy, fx_, fy: slab(hx, hy, fx_, fy, 3.4, "#9aa07f") +
                                    circ(fx_ + (hx - fx_) * 0.1 - 0.4, -2.3, 1.2, PAPER, INK, 0.2),
                                    "stand: single bar 70 mm with a hole, hinged 20 mm below the top",
                                    " · narrow stand can rock", SC)
    body.append(svg_open)
    body.append(px_text(96, 790, "TOP EDGE", 16, INK, "bold", SANS))
    body.append(P(100, 810, top_view(W, D, 4, 42, OLIVE, rr(1, 4, 3.2, 10, 1.4, ORANGE, INK, 0.2))))
    body.append(lever_strip(660, 850))
    legend = ["1 mic port: centre of the middle vent slot",
              "2 left-edge lever, 3-stage, hidden under the guard",
              "3 mode slider DICT / TALK / OPEN (rarely moved)",
              "4 SAFE / ARMED windows (ARMED lit when the guard is up)",
              "5 optional buzzer holes",
              "6 USB-C on the top edge (see TOP EDGE)",
              "7 stand bar with a carabiner hole, on the back plate",
              "8 quarter-turn feet hold the back plate",
              "9 THE GUARD: a flap that flips up over the left face",
              "a-d bay: BOOT/RST, header, battery space, info label"]
    idea = ["Safety-switch language. Anything that can be pressed by",
            "accident sits behind a guard, and the guard is the master",
            "switch: closed = SAFE (muted, lever dead), flipped up =",
            "ARMED (mic live, lever active)."]
    left_out = ["no wheel, no thumb groove, no lid",
                "mode is a plain slider: it changes rarely, so it can be dull",
                "no clever shape: the body stays a utilitarian slab"]
    risks = ["A printed hinge for the guard will fatigue: use a metal pin.",
             "A magnet or Hall sensor is needed to read the guard state.",
             "Opening the guard is one more action before every use;",
             "it must flip fully out of the way of the thumb.",
             "A narrow single bar can rock; a two-prong fork is stabler.",
             "Military look is serious: less playful than D or F."]
    info = info2(96, 1030, legend, idea, left_out, risks)
    write(out, "E-armed.svg", sheet(1920, 1340, "talk.01 · ROUND 2 · E — ARMED",
                                    "One idea: a guard that is also the master switch · SAFE / ARMED · field-gear feel",
                                    "".join(body), info))


# ================================================================ F · HANDSET
def concept_f(out):
    W, H, D = 60, H_, 19
    BROWN, CHAR, SHADE, CR = "#4a3629", "#1f1712", "#3b2a20", "#e9dcc0"

    def front(rear=False):
        g = []
        if not rear:
            g.append(rr(-0.2, 64, 4, 19, 2, ORANGE, INK, 0.25))                 # lever in the heel of the groove
            g.append(path(PF, BROWN, INK, 0.3))
            g.append(rr(1.2, 39, 5.6, 6, 2.2, CR, INK, 0.25))                   # slider knob on the groove
            for yy, lab in ((42, "DICT"), (47, "TALK"), (52, "OPEN"), (57, "LOCK")):
                g.append(line(9.2, yy, 11, yy, CR, 0.25))
                g.append(t(12.2, yy + 0.7, lab, 2.0, "start", CR))
            g.append(circ(30.5, 23, 2.5, CHAR, CHAR, 0.05))
            for k in range(6):
                a = math.radians(k * 60 + 30)
                g.append(circ(30.5 + 6.2 * math.sin(a), 23 - 6.2 * math.cos(a), 2.2, CHAR, CHAR, 0.05))
            g.append(circ(30.5, 23, 4.2, "none", ORANGE, 0.25, 'stroke-dasharray="0.8 0.6"'))
            g.append(rr(29, 45.5, 16, 5.2, 2.6, CHAR, INK, 0.2))
            g.append(circ(32.6, 48.1, 1.4, ORANGE, INK, 0.12))
            g.append(t(35, 49, "ON AIR", 1.8, "start", CR))
            for x in (42, 45, 48):
                g.append(circ(x, 66, 0.7, CHAR, CHAR, 0.05))
            g.append(t(22, 81, "talk.01", 3.4, "start", CR, "bold", SANS))
            g.append(call(1, 30.5, 23, W + 8, 14))
            g.append(call(2, -0.2, 73, -10, 76))
            g.append(call(3, 1.2, 42, -10, 40))
            g.append(call(9, 3.5, 53, -10, 58))
            g.append(call(4, 45, 48, W + 8, 48))
            g.append(call(5, 48, 66, W + 8, 66))
            g.append(dimh(0, W, H + 6, f"{W} (bottom)"))
            g.append(dimv(-17, 0, H, f"{H}"))
            g.append(t(30, -2.5, "top 50 mm wide", 1.9, "middle", DIM))
        else:
            g.append(f'<g transform="translate({W},0) scale(-1,1)">{path(PF, BROWN, INK, 0.3)}</g>')
            g.append(rr(9, 4, 42, 84, 4, SHADE, "#6b5646", 0.2))
            g.append(path("M14,12 L14,82 L46,82 L46,12", "none", CR, 2.4, 'stroke-linecap="round" stroke-linejoin="round"'))
            g.append(circ(14, 12, 1.7, "#a8957a", INK, 0.2))
            g.append(circ(46, 12, 1.7, "#a8957a", INK, 0.2))
            g.append(circ(30, 88.4, 3.0, SHADE, INK, 0.2))
            for sx in (12, 48):
                g.append(circ(sx, 87.4, 2.1, ORANGE, INK, 0.2))
                g.append(line(sx - 1.4, 87.4, sx + 1.4, 87.4, INK, 0.22))
            g.append(t(30, 46, "bail stand", 2.1, "middle", CR))
            g.append(t(30, 49.4, "(also a carry loop)", 1.9, "middle", CR))
            g.append(call(7, 46, 40, W + 8, 40))
            g.append(call(8, 48, 87.4, W + 8, 88))
        return "".join(g)

    def side(closed_stand=True):
        g = [rr(0, -H, D, H, 6, BROWN, INK, 0.3)]
        if closed_stand:
            g.append(rr(0, -H + 12, 2.6, 70, 1.1, CR, INK, 0.15))
        g.append(rr(7, -H + 38, 5, 22, 2.5, CHAR, INK, 0.2))
        g.append(rr(6.5, -H + 39, 6, 6, 2.4, CR, INK, 0.2))
        g.append(rr(4, -H + 64, 11, 19, 5, ORANGE, INK, 0.25))
        g.append(rr(2.5, 0, 14, 1.1, 0.5, "#111", INK, 0.1))
        return "".join(g)

    x0, y0 = 96, 200
    base = y0 + H * SC
    body = [px_text(x0, y0 - 40, "FRONT", 16, INK, "bold", SANS), px_text(486, y0 - 40, "REAR · back plate with stand", 16, INK, "bold", SANS),
            px_text(876, y0 - 40, "REAR · plate off (hackable bay)", 16, INK, "bold", SANS), px_text(1266, y0 - 40, "SIDE · left", 16, INK, "bold", SANS),
            px_text(1450, y0 - 40, "SIDE · stand open, on desk", 16, INK, "bold", SANS),
            P(x0, y0, front(False)), P(486, y0, front(True)), P(876, y0, bay("taper", BROWN, 30.5)),
            P(1266, base, side(True) + dimh(0, D, 6, f"{D}"))]

    def bail(hx, hy, fx_, fy):
        a = math.degrees(math.atan2(fy - hy, fx_ - hx))
        L = math.hypot(fx_ - hx, fy - hy)
        return (f'<g transform="translate({f(hx)},{f(hy)}) rotate({f(a)})">' + rr(0, -1.2, L, 2.4, 1.2, CR, INK, 0.2) + '</g>' +
                circ(hx, hy, 0.9, "#a8957a", INK, 0.1) + rr(fx_ - 1.6, -0.9, 3.2, 1.8, 0.7, "#111", INK, 0.15))

    svg_open, fx, right = open_side(1725, base, 28, H, D, 12, 74, 23, 40, side(False), bail,
                                    "stand: U-frame bail 74 mm, hinged 12 mm below the top",
                                    "", SC)
    body.append(svg_open)
    body.append(px_text(96, 790, "TOP EDGE", 16, INK, "bold", SANS))
    body.append(P(100, 810, top_view(50, D, 9, 38, BROWN, rr(5, 4.5, 3.2, 9, 1.4, ORANGE, INK, 0.2))))
    body.append(lever_strip(660, 850))
    legend = ["1 mic port: centre hole of the rosette",
              "2 lever, 3-stage, in the heel of the thumb groove",
              "3 thumb slider DICT / TALK / OPEN / LOCK, in the groove",
              "4 ON AIR lamp   5 optional buzzer holes",
              "6 USB-C on the top edge (see TOP EDGE)",
              "7 bail stand, also a carry loop",
              "8 quarter-turn feet hold the back plate",
              "9 THE GROOVE: a 3-4 mm scoop for the left thumb",
              "a-d bay: BOOT/RST, header, battery space, info label"]
    idea = ["Form follows the left thumb. The body flares from a",
            "narrow top to a wide base, and a scooped groove on the",
            "left edge holds both controls. It feels like a handset",
            "and stands on its wide base."]
    left_out = ["no wheel, no guard, no lid (the groove shoulders protect)",
                "no symmetry: this is a left-hand shape (mirror to print)",
                "no hard edges: the body is one soft outline"]
    risks = ["Left-hand shape: right-handed users need a mirrored print.",
             "A tapered, curved body is harder to pack and to print flat.",
             "A slider is less fun than a wheel; the fun is in the shape.",
             "The bail is the only stand: no lid or clip alternative.",
             "The groove depth and slider position need a full-size mock",
             "held in a real left hand before any CAD."]
    info = info2(96, 1030, legend, idea, left_out, risks)
    write(out, "F-handset.svg", sheet(1920, 1340, "talk.01 · ROUND 2 · F — HANDSET",
                                      "One idea: the body is shaped around the left thumb · groove, slider, lever, bail",
                                      "".join(body), info))


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    concept_d(out)
    concept_e(out)
    concept_f(out)
