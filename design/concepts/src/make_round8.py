#!/usr/bin/env python3
"""Round-8 sheets for talk.01.

wheel-study.svg : which way the thumb wheel turns (a top knob, an edge roller, a face dial) and how it sits in a pocket
round8.svg      : one converged layout in four skins (colour, grille and corner differ; the layout does not)

The layout: four fingers squeeze a strip on the right; a ribbed roller sits in a pocket on the left edge and the
left thumb strokes it up and down; a glowing frosted window shows the mode by colour; a sleeve locks the strip
flush; USB-C and a coiled cable on top; a small hatch and a small U stand on the back (see round-7/back.svg).
Standard library only. Dimensions are TENTATIVE.

    python3 design/concepts/src/make_round8.py design/concepts/round-8
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_concepts import (INK, PAPER, DIM, ORANGE, f, rr, circ, line, poly, path, t,  # noqa: E402
                           panel, px_text, write, SANS, MONO)
from make_round5 import mix, grad, hlines, vslots, dots_disc, plug_notch, coil  # noqa: E402
from make_round4 import screw  # noqa: E402
from make_round6 import rainbow, rot, ghost, sleeve  # noqa: E402
import make_round5 as r5  # noqa: E402

SC = 4.0


def roller_in_pocket(g, cy, base, rib, h=26, pocket="#1d1b19"):
    """An edge roller sunk in a pocket on the left edge (axis points out of the page toward the viewer)."""
    g.append(rr(-1.0, cy - h / 2 - 2.2, 11.6, h + 4.4, 4, pocket, "#000", 0.4))
    g.append(rr(-3.2, cy - h / 2, 8.6, h, 3.2, base, "#000", 0.4))
    for k in range(18):
        yy = cy - h / 2 + 2 + k * (h - 4) / 17
        g.append(line(-2.8, yy, 4.8, yy, rib, 0.28))
    g.append(rr(-2.6, cy - h / 2 + 1.2, 1.4, h - 2.4, 0.7, "#ffffff", "none", 0.0).replace("<rect ", '<rect opacity="0.18" '))


def mode_dots(g, cy, lit, color_on, color_off="#8a857a"):
    for k in range(4):
        g.append(circ(12.8, cy - 6 + k * 4, 0.85, color_on if k == lit else color_off, "none", 0.0))
    g.append(poly([(10.8, cy - 6 + lit * 4 - 0.9), (10.8, cy - 6 + lit * 4 + 0.9), (11.9, cy - 6 + lit * 4)], color_on, "none", 0.0))


def dimples7(g, cx, cy, dish="#5a5650", hole="#15130f", rim="#6e6a63"):
    g.append(circ(cx, cy, 15.5, rim, "none", 0.0))
    g.append(circ(cx, cy, 14.4, dish, "#2a2724", 0.35))
    pts = [(cx, cy)] + [(cx + 7.6 * math.sin(math.radians(a)), cy - 7.6 * math.cos(math.radians(a))) for a in range(0, 360, 60)]
    for (x, y) in pts:
        g.append(circ(x, y, 3.9, mix(dish, 0.1), "#2a2724", 0.25))
        for j in range(7):
            if j == 0:
                g.append(circ(x, y, 0.38, hole, "none", 0.0))
            else:
                a = math.radians((j - 1) * 60)
                g.append(circ(x + 1.5 * math.sin(a), y - 1.5 * math.cos(a), 0.38, hole, "none", 0.0))


def glow_window(g, x, y, w, h, c0, c1, frame, screw_c="#cfcfcf", gid="gw"):
    r5.DEFS.append(f'<radialGradient id="{gid}" cx="0.3" cy="0.75" r="1.0"><stop offset="0" stop-color="{c0}"/><stop offset="1" stop-color="{c1}"/></radialGradient>')
    g.append(rr(x - 1.4, y - 1.4, w + 2.8, h + 2.8, 2.4, frame, "#000", 0.4))
    g.append(rr(x, y, w, h, 1.4, f"url(#{gid})", "none", 0.0))
    g.append(rr(x, y, w, h, 1.4, "none", mix(frame, -0.4), 0.3))
    for (sx, sy) in ((x + 1.6, y + 1.6), (x + w - 1.6, y + 1.6), (x + 1.6, y + h - 1.6), (x + w - 1.6, y + h - 1.6)):
        g.append(circ(sx, sy, 0.95, screw_c, "#444", 0.15))
        g.append(line(sx - 0.55, sy, sx + 0.55, sy, "#444", 0.15))


def squeeze_strip(g, x, y0, y1, w, fill, edge, ang, ribs=11, text="SQUEEZE TO TALK", tcol="#fff"):
    body = path(f"M{x},{y0} H{x + w} V{y1} H{x} Z", fill, edge, 0.5)
    for k in range(ribs):
        yy = y0 + 14 + k * (y1 - y0 - 20) / max(ribs - 1, 1)
        body += line(x + 1.2, yy, x + w - 1.2, yy, mix(fill, -0.3), 0.35)
    body += f'<g transform="translate({x + w / 2 + 0.6},{(y0 + y1) / 2 + 6}) rotate(-90)">{t(0, 0, text, 2.3, "middle", tcol, "bold", MONO)}</g>'
    g.append(ghost(x, y0, w, y1 - y0, 3))
    g.append(rot(body, ang, x + w, y1))
    g.append(circ(x + w, y1, 1.3, "#b79c4a", "#4d3d12", 0.25))


# ================================================================ wheel study
def study(out):
    CREAM, TEAL = "#e8e1cf", "#3d9aa1"
    body = [px_text(60, 62, "talk.01 · WHICH WAY DOES THE THUMB WHEEL TURN?", 30, INK, "bold", SANS),
            px_text(60, 92, "three ways to put a wheel under the left thumb · the second is the owner's reference (the roller in a pocket)", 15, DIM),
            px_text(1860, 52, "TENTATIVE · NOT A FINAL DESIGN", 13, ORANGE, "bold", MONO, "end")]

    def device():
        return [rr(0, 0, 50, 80, 5, CREAM, INK, 0.45), rr(50, 4, 9, 70, 3, TEAL, "#1f5a5f", 0.4), rr(8, 6, 32, 20, 3, "#cfc8b4", "#8a857a", 0.3),
                t(24, 17, "mic", 2.2, "middle", "#8a857a", "normal", MONO)]

    def arrow_curve(cx, cy, r, a0, a1, col="#c9461e"):
        x0, y0 = cx + r * math.sin(math.radians(a0)), cy - r * math.cos(math.radians(a0))
        x1, y1 = cx + r * math.sin(math.radians(a1)), cy - r * math.cos(math.radians(a1))
        return (path(f"M{f(x0)},{f(y0)} A{r},{r} 0 0 1 {f(x1)},{f(y1)}", "none", col, 0.9, 'stroke-linecap="round"') +
                poly([(x1, y1), (x1 - 2.2 * math.cos(math.radians(a1)) - 1.2 * math.sin(math.radians(a1)), y1 - 2.2 * math.sin(math.radians(a1)) + 1.2 * math.cos(math.radians(a1))),
                      (x1 - 2.2 * math.cos(math.radians(a1)) + 1.2 * math.sin(math.radians(a1)), y1 - 2.2 * math.sin(math.radians(a1)) - 1.2 * math.cos(math.radians(a1)))], col, col, 0.05))

    # A: top knob (the walkie photo)
    a = device()
    a += [rr(7, -8, 13, 9, 2, "#2b2a28", "#000", 0.4)] + [line(8 + k * 1.6, -7.4, 8 + k * 1.6, 0.4, "#8a857a", 0.3) for k in range(7)]
    a += [line(13.5, -14, 13.5, 6, "#c9461e", 0.45, 'stroke-dasharray="1.2 0.8"'), arrow_curve(13.5, -4, 8.5, -80, 80)]
    a += [t(24, -2, "axis: up", 2.0, "start", "#c9461e", "bold", MONO)]
    # B: edge roller (the owner's reference)
    b = device()
    roller_in_pocket(b, 40, "#2b2927", "#7a756c", 24)
    b += [line(-10, 28, -10, 52, "#c9461e", 0.9, 'stroke-linecap="round"'), poly([(-10, 26), (-11.6, 29), (-8.4, 29)], "#c9461e", "#c9461e", 0.05),
          poly([(-10, 54), (-11.6, 51), (-8.4, 51)], "#c9461e", "#c9461e", 0.05), circ(1.2, 40, 1.4, "none", "#c9461e", 0.45), circ(1.2, 40, 0.35, "#c9461e", "none", 0.0),
          t(-8, 60, "axis: toward you", 2.0, "start", "#c9461e", "bold", MONO)]
    # C: face dial
    c = device()
    c += [circ(24, 52, 9.5, "#2b2a28", "#000", 0.4), circ(24, 52, 6.5, "#4a463e", "none", 0.0), line(24, 52, 24, 46.4, "#e8672a", 1.0, 'stroke-linecap="round"'),
          arrow_curve(24, 52, 12.5, -50, 60), circ(24, 52, 1.2, "none", "#c9461e", 0.4), t(24, 70, "axis: toward you", 2.0, "middle", "#c9461e", "bold", MONO)]
    labels = [("A · TOP KNOB", "like the yellow walkie in the reference photo", "the thumb TWISTS it; the axis points up. Natural for a radio, but the top is where the USB-C and the cable go; twisting while holding is awkward."),
              ("B · EDGE ROLLER", "like the corner roller in the dark gadget", "the thumb STROKES it up and down along the edge; the axis points toward you. Sunk in a pocket so it is protected. My reading of what you want."),
              ("C · FACE DIAL", "like the dials in rounds 2 to 5", "the thumb turns it on the face; the axis points toward you. It uses face area that the grille and window need.")]
    for i, (pn, sub, desc) in enumerate((labels)):
        x = 80 + i * 600
        body.append(px_text(x, 160, pn, 20, INK, "bold", SANS))
        body.append(px_text(x, 182, sub, 12, DIM, "normal", MONO))
        body.append(panel(x + 70, 270, "".join([a, b, c][i]), 5.2))
        import textwrap
        for k, s in enumerate(textwrap.wrap(desc, 62)):
            body.append(px_text(x, 760 + k * 17, s, 12.5, INK))
    body.append("".join(px_text(80, 860 + k * 19, s, 12.5, c_, w_) for k, (s, c_, w_) in enumerate((
        ("How the roller would work", INK, "bold"),
        ("a ribbed cylinder, about 14 mm across and 24 mm long, on a pin; a spring-ball click gives the four detents (DICT, TALK, OPEN, LOCK); a small switch under it could make it clickable (click = latch).", INK, "normal"),
        ("It sits in a pocket on the left edge and sticks out 2 to 3 mm; the pocket's walls protect it in a bag. Four small dots beside it show the mode.", INK, "normal"),
        ("The wheel's position is read by a tiny rotary encoder or four contacts. The roller tends to get dust and wear in a matte print; a metal pin is advised.", INK, "normal"),
        ("", INK, "normal"),
        ("What I assumed: you meant B. Tell me if you meant A or C.", "#9a2f1a", "bold")))))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080"><defs>{"".join(r5.DEFS)}</defs>'
           f'<rect width="1920" height="1080" fill="{PAPER}"/>{"".join(body)}</svg>')
    write(out, "wheel-study.svg", svg)


# ================================================================ four skins
def skin(sp):
    cx = 0
    body = sp["body"]
    g = []
    if sp["cut"]:
        outline = "M16,0 H44 Q49,0 49,5 V87 Q49,92 44,92 H5 Q0,92 0,87 V9 Z"
    else:
        outline = "M5,0 H44 Q49,0 49,5 V87 Q49,92 44,92 H5 Q0,92 0,87 V5 Q0,0 5,0 Z"
    g.append(path(outline, grad(sp["gid"], body, 0.07), sp["edge"], 0.5))
    # grille
    if sp["grille"] == "dimples":
        dimples7(g, 25, 22, sp["dish"], sp["hole"], sp["rim"])
    elif sp["grille"] == "lines":
        g += [rr(8, 9, 34, 26, 3, sp["frame"], mix(sp["frame"], -0.4), 0.4), hlines(11.5, 12.5, 27, 8, 2.7, 1.2, mix(sp["frame"], -0.35))]
    elif sp["grille"] == "slots":
        g += [rr(8, 9, 34, 26, 3, "#2b2a28", "#000", 0.4), vslots(12, 12.5, 19, 8, 3.7, 1.8, "#d6d2c2")]
    else:
        g += [rr(8, 9, 34, 26, 3, sp["frame"], mix(sp["frame"], -0.4), 0.4)] + [circ(12.5 + c * 3.8, 13.5 + r * 3.8, 1.0, mix(sp["frame"], 0.6), "none", 0.0) for c in range(8) for r in range(6)]
    # glow window (mode display)
    glow_window(g, 16.5, 42, 26, 24, sp["glow0"], sp["glow1"], sp["wframe"], gid=sp["gid"] + "w")
    g.append(t(29.5, 72, "MODE = COLOUR", 1.5, "middle", sp["ink"], "normal", MONO))
    # roller and mode dots
    roller_in_pocket(g, 50, sp["roller"], sp["rib"], 26, sp["pocket"])
    mode_dots(g, 50, 1, sp["dot"], mix(sp["ink"], 0.4))
    # lock sleeve + badge + screws
    g += [rr(19, 3.4, 41, 5.2, 2.6, mix(sp["body"], -0.12), mix(sp["body"], -0.4), 0.25), sleeve(21, 3.6, 11, 4.8, sp["sleeve"]), ghost(47.5, 3.6, 11, 4.8, 2.4),
          t(35, 7.5, "LOCK ►", 1.3, "start", sp["ink"], "normal", MONO)]
    g += [rainbow(10, 82, 8, 3.2), t(20, 84.8, "talk.01", 3.0, "start", sp["ink"], "bold", SANS), screw(44, 87)]
    squeeze_strip(g, 49, 6, 88, 11, sp["strip"], sp["strip_edge"], 4, 11, "SQUEEZE TO TALK", sp["strip_text"])
    g += [plug_notch(31, sp["edge"]), coil(31, 0, 6, 2.6, 7, sp["coil"])]
    return "".join(g)


SKINS = [
    dict(name="1 · EMBER", tag="gunmetal + orange glow", gid="e1", body="#4d4944", edge="#241f1b", cut=True, grille="dimples", dish="#5e5953", hole="#12100d", rim="#6e6a63",
         glow0="#ff6a22", glow1="#ffd9b8", wframe="#2a2724", roller="#2b2927", rib="#7a756c", pocket="#171513", dot="#ff7a30", ink="#cbc5b9",
         sleeve="#e8672a", strip="#e8672a", strip_edge="#7a2f0c", strip_text="#fff1e6", coil="#e8672a",
         lines=["reference: the dark gadget: 7-dimple speaker, glowing screw-cornered window, ribbed roller in a pocket, a cut corner",
                "grille: seven dimples, each a tiny cluster of holes (the centre one is the mic)", "mode: the window glows amber, red, green or off; four dots beside the roller",
                "+ the closest to the TE feel; the glowing window is the hero", "- all-dark looks serious; the glow needs a real diffuser; dimples are fiddly to print"]),
    dict(name="2 · SAND", tag="beige + teal", gid="s2", body="#e8e1cf", edge="#3a3832", cut=False, grille="lines", frame="#3d9aa1", dish="", hole="", rim="",
         glow0="#f6a935", glow1="#fff0c4", wframe="#3d9aa1", roller="#2f7f85", rib="#bfe3e6", pocket="#1f5a5f", dot="#e9873a", ink="#4a463e",
         sleeve="#8e8cc9", strip="#3d9aa1", strip_edge="#1f5a5f", strip_text="#e9f4f4", coil="#3d9aa1",
         lines=["reference: the beige cassette deck and boombox (beige with teal); the round-6 and round-7 layout",
                "grille: horizontal lines in a teal frame", "mode: the window glows amber, teal, green or off",
                "+ the softest and friendliest; matches the retro palette you like", "- the least bold; the window colour must stay readable on beige"]),
    dict(name="3 · POPPY", tag="cream + red", gid="p3", body="#efe9d9", edge="#2b2a28", cut=True, grille="slots", frame="#2b2a28", dish="", hole="", rim="",
         glow0="#e0301f", glow1="#ffc1a8", wframe="#2b2a28", roller="#d8483c", rib="#f6b9b0", pocket="#4a110c", dot="#d8483c", ink="#4a463e",
         sleeve="#2b2a28", strip="#d8483c", strip_edge="#6e1a12", strip_text="#ffe9e6", coil="#d8483c",
         lines=["reference: the Walkman and the toy radio; red as the one loud colour on cream", "grille: vertical slots",
                "mode: the window glows red, orange, green or off", "+ the most eye-catching at a glance; a clear hero colour",
                "- a strong red can feel toy-like; the cut corner needs care at the thumb"]),
    dict(name="4 · SAGE", tag="sage + black + orange", gid="g4", body="#aebfa9", edge="#2b3a2a", cut=False, grille="dots", frame="#8aa384", dish="", hole="", rim="",
         glow0="#d4e84a", glow1="#f7ffd0", wframe="#2b2a28", roller="#e8672a", rib="#ffd2b0", pocket="#4a2008", dot="#e8672a", ink="#2f3d2e",
         sleeve="#e8672a", strip="#2b2a28", strip_edge="#000", strip_text="#d9e6d3", coil="#2b2a28",
         lines=["reference: the dot-matrix cube and the olive hand radio, softened to sage", "grille: a dot-matrix field",
                "mode: the window glows lime, amber, red or off", "+ calm and unusual; sage with black and orange is distinctive",
                "- sage may print greyish; the dot field needs 0.8 mm holes"]),
]


def lineup(out):
    import textwrap
    body = []
    for i, sp in enumerate(SKINS):
        x, y = 40 + i * 470, 170
        body.append(f'<rect x="{x}" y="{y}" width="450" height="880" rx="14" fill="none" stroke="#d3cdbf" stroke-width="2"/>')
        body.append(px_text(x + 16, y + 38, sp["name"], 24, INK, "bold", SANS))
        body.append(px_text(x + 16, y + 60, sp["tag"], 13, DIM))
        body.append(panel(x + 150, y + 250, skin(sp), SC))
        yy = y + 650
        for s_ in sp["lines"]:
            col = "#2f6f3a" if s_.startswith("+") else ("#9a2f1a" if s_.startswith("-") else INK)
            for part in textwrap.wrap(s_, 60, subsequent_indent="  "):
                body.append(px_text(x + 16, yy, part, 11.5, col))
                yy += 15
            yy += 3
    head = (px_text(60, 62, "talk.01 · ROUND 8 · ONE LAYOUT, FOUR SKINS", 30, INK, "bold", SANS) +
            px_text(60, 92, "squeeze strip on the right · roller in a pocket on the left · a glowing window shows the mode · colour and grille are the variables", 15, DIM) +
            px_text(1860, 52, "TENTATIVE · NOT A FINAL DESIGN", 13, ORANGE, "bold", MONO, "end") +
            px_text(1860, 72, "original concepts · same scale (10 mm = 40 px) · the strip is drawn popped out; dashed = flush", 12, DIM, "normal", MONO, "end") +
            px_text(60, 128, "Not borrowed: the rugged yellow walkie's bumper and military look. Borrowed: the roller in a pocket, the 7-dimple grille, the glowing window, the cut corner.", 14, INK, "normal", MONO))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1090" width="1920" height="1090"><defs>{"".join(r5.DEFS)}</defs>'
           f'<rect width="1920" height="1090" fill="{PAPER}"/>{head}{"".join(body)}</svg>')
    write(out, "round8.svg", svg)


if __name__ == "__main__":
    o = sys.argv[1] if len(sys.argv) > 1 else "."
    study(o)
    lineup(o)
