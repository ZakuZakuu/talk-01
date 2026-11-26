#!/usr/bin/env python3
"""talk.01 v0.5 study: tone-on-tone colour, our own lettering, how the mode wheel shows its position, a snap-fit lid, and the stack inside.

  palette.svg : three tone-on-tone palettes (bright key, body and plate in one family) with our own pixel-dot labels and a hand-drawn wordmark
  mode.svg    : four ways to show the four modes, and five ways to sense the wheel (absolute vs relative)
  lid.svg     : the removable lid (hooks at the top, in-plane snap arms at the bottom) and a side section of what sits inside

    python3 design/concepts/src/make_v05.py design/concepts/v0.5

Standard library only. Dimensions are TENTATIVE; part sizes are typical values to be checked against datasheets.
"""
import math
import os
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_concepts import INK, PAPER, DIM, ORANGE, f, rr, circ, line, poly, path, t, panel, px_text, write, SANS, MONO  # noqa: E402
from make_round5 import mix, plug_notch, coil  # noqa: E402
from make_round4 import screw  # noqa: E402
from make_round6 import rainbow  # noqa: E402
from make_v01 import icon, MODES  # noqa: E402
from make_v02 import body_path, left_key, W, H, WX, WY, WR  # noqa: E402
from make_v04 import plate, R, SPLIT  # noqa: E402
import make_round5 as r5  # noqa: E402

# ---------------------------------------------------------------- our own pixel font (5 x 7), drawn as squares or dots
_G = {
    "A": ".XXX.|X...X|X...X|XXXXX|X...X|X...X|X...X", "B": "XXXX.|X...X|X...X|XXXX.|X...X|X...X|XXXX.",
    "C": ".XXXX|X....|X....|X....|X....|X....|.XXXX", "D": "XXXX.|X...X|X...X|X...X|X...X|X...X|XXXX.",
    "E": "XXXXX|X....|X....|XXXX.|X....|X....|XXXXX", "H": "X...X|X...X|X...X|XXXXX|X...X|X...X|X...X", "I": "XXXXX|..X..|..X..|..X..|..X..|..X..|XXXXX",
    "K": "X...X|X..X.|X.X..|XX...|X.X..|X..X.|X...X", "L": "X....|X....|X....|X....|X....|X....|XXXXX",
    "M": "X...X|XX.XX|X.X.X|X.X.X|X...X|X...X|X...X", "N": "X...X|XX..X|X.X.X|X..XX|X...X|X...X|X...X",
    "O": ".XXX.|X...X|X...X|X...X|X...X|X...X|.XXX.", "P": "XXXX.|X...X|X...X|XXXX.|X....|X....|X....",
    "R": "XXXX.|X...X|X...X|XXXX.|X.X..|X..X.|X...X", "S": ".XXXX|X....|X....|.XXX.|....X|....X|XXXX.",
    "T": "XXXXX|..X..|..X..|..X..|..X..|..X..|..X..", "U": "X...X|X...X|X...X|X...X|X...X|X...X|.XXX.",
    "V": "X...X|X...X|X...X|X...X|X...X|.X.X.|..X..", "Y": "X...X|X...X|.X.X.|..X..|..X..|..X..|..X..",
    "0": ".XXX.|X...X|X..XX|X.X.X|XX..X|X...X|.XXX.", "1": "..X..|.XX..|..X..|..X..|..X..|..X..|.XXX.",
    "5": "XXXXX|X....|XXXX.|....X|....X|X...X|.XXX.", ".": ".....|.....|.....|.....|.....|.....|..X..",
    "+": ".....|..X..|..X..|XXXXX|..X..|..X..|.....", "<": "...X.|..X..|.X...|X....|.X...|..X..|...X.",
}
PIX = {k: v.split("|") for k, v in _G.items()}


def pix(x, y, text, cell, col, dot=False):
    """Text in the pixel font; (x, y) is the top-left corner, the height is 7 cells."""
    out, cx = [], x
    for ch in text.upper():
        g = PIX.get(ch)
        if g is None:
            cx += 4 * cell
            continue
        for r, row in enumerate(g):
            for c, v in enumerate(row):
                if v == "X":
                    out.append(circ(cx + (c + .5) * cell, y + (r + .5) * cell, cell * .47, col, "none", 0) if dot else R(cx + c * cell, y + r * cell, cell * .92, cell * .92, col))
        cx += 6 * cell
    return "".join(out)


def pix_w(text, cell):
    return sum(6 * cell if ch.upper() in PIX else 4 * cell for ch in text) - cell


# ---------------------------------------------------------------- our own wordmark: monoline, round ends, a bowl for the a, an accent dot, 0 and 1
_WG = [("t", 3.0, "M1.4,0.4 V5.0 Q1.4,6 2.6,6 M0.2,2.3 H2.9", 0), ("a", 4.4, None, 0), ("l", 1.2, "M0.6,0 V6", 0),
       ("k", 3.8, "M0.6,0 V6 M3.4,2.2 L0.6,4.3 M1.7,3.5 L3.6,6", 0), (".", 1.4, None, 1), ("0", 4.2, None, 1), ("1", 3.0, "M0.4,1.3 L2.0,0 V6", 1)]


def wordmark(x, y, sc, col, acc, sw=1.15):
    """Hand-drawn 'talk.01', 6 units tall; sc = mm per unit; the dot, 0 and 1 take the accent colour."""
    parts, cx = [], 0.0
    for name, w, d, a in _WG:
        c = acc if a else col
        if name == "a":
            parts.append(f'<g transform="translate({f(cx)},0)"><circle cx="1.95" cy="4.05" r="1.95" fill="none" stroke="{c}"/><path d="M3.9,2.2 V6" fill="none" stroke="{c}"/></g>')
        elif name == ".":
            parts.append(f'<circle cx="{f(cx + 0.75)}" cy="5.25" r="0.8" fill="{c}" stroke="none"/>')
        elif name == "0":
            parts.append(f'<ellipse cx="{f(cx + 2.1)}" cy="3" rx="2.0" ry="2.9" fill="none" stroke="{c}"/>')
        else:
            parts.append(f'<path transform="translate({f(cx)},0)" d="{d}" fill="none" stroke="{c}"/>')
        cx += w + 1.0
    return (f'<g transform="translate({f(x)},{f(y)}) scale({f(sc)})" stroke-width="{f(sw)}" stroke-linecap="round" stroke-linejoin="round">'
            + "".join(parts) + "</g>")


# ---------------------------------------------------------------- palettes: body and plate in one family, a bright key
PALETTES = [
    dict(name="WARM", sub="warm grey body, a shade deeper plate, orange key", lower="#e4dcc8", plate="#cdc3aa", edge="#3d382d", ink="#4a443a",
         keyc="#ee6a2c", keyedge="#8a2f0e", keyink="#fff2e6", wheel="#3e3b35", rib="#d8d0bb", pocket="#1c1a17", coil="#3e3b35", gid="p1"),
    dict(name="GRAPHITE", sub="charcoal body, a shade deeper plate, amber key", lower="#46443f", plate="#363531", edge="#12110d", ink="#e9e3d2",
         keyc="#f2b630", keyedge="#7a4f0a", keyink="#2b2410", wheel="#e4dcc8", rib="#77736a", pocket="#14130f", coil="#e4dcc8", gid="p2"),
    dict(name="SAGE", sub="sage body, a deeper sage plate, red key", lower="#b8c3a9", plate="#9fac8f", edge="#2d3a2a", ink="#33402f",
         keyc="#e5432b", keyedge="#6d170b", keyink="#fff0ec", wheel="#34493a", rib="#bfd0b6", pocket="#17241b", coil="#34493a", gid="p3"),
]


def key_plain(g, color, edge):
    g.append(poly([(0, 12), (-5.0, 16.5), (-3.2, 56), (0, 58)], color, edge, 0.55, 'stroke-linejoin="round"'))
    for k in range(6):
        yy = 24 + k * 5.6
        xo = -(5.0 - (yy - 16.5) * 1.8 / 39.5) + 0.4
        g.append(line(-0.8, yy, xo, yy + 0.3, mix(color, -0.3), 0.4))


def dial_wheel(g, bid, sp, cur=1, dial=True):
    """The wheel in the top-right chamfer. With dial=True it carries the four mode icons on a ring (a camera mode dial); the fixed
    index triangle on the body points at the active one."""
    g.append(f'<clipPath id="{bid}k"><path d="{body_path()}"/></clipPath><g clip-path="url(#{bid}k)">{circ(WX, WY, WR + 1.8, sp["pocket"], "#000", 0.4)}</g>')
    g.append(circ(WX, WY, WR, sp["wheel"], "#000", 0.45))
    for k in range(30):
        a = math.radians(k * 12)
        g.append(line(WX + (WR - 1.1) * math.sin(a), WY - (WR - 1.1) * math.cos(a), WX + WR * math.sin(a), WY - WR * math.cos(a), sp["rib"], 0.5))
    if dial:
        g.append(circ(WX, WY, WR - 1.3, mix(sp["wheel"], 0.08), mix(sp["wheel"], -0.3), 0.25))
        for k, (ik, lab) in enumerate(MODES):
            th = math.radians(225 + (k - cur) * 45)
            x, y = WX + 4.9 * math.sin(th), WY - 4.9 * math.cos(th)
            col = sp["keyc"] if k == cur else sp["rib"]
            g.append(icon(ik, x - 1.0, y, col))
        g.append(circ(WX, WY, 1.5, mix(sp["wheel"], 0.18), mix(sp["wheel"], -0.4), 0.25))
        th = math.radians(225)                                   # the fixed index triangle, on the body
        ix, iy = WX + (WR + 3.9) * math.sin(th), WY - (WR + 3.9) * math.cos(th)
        g.append(f'<g transform="translate({f(ix)},{f(iy)}) rotate(45)">{poly([(0, -1.0), (1.0, 1.0), (-1.0, 1.0)], sp["keyc"], sp["keyedge"], 0.2)}</g>')
    else:
        g.append(circ(WX, WY, WR * 0.55, mix(sp["wheel"], 0.1), mix(sp["wheel"], -0.4), 0.3))


def body_front(sp, bid, dial=True):
    g = [f'<path d="{body_path()}" fill="{sp["lower"]}" stroke="{sp["edge"]}" stroke-width="0.5"/>']
    g.append(plate("hridge", sp["plate"], bid))
    # our own panel graphics: the wordmark, small pixel-dot labels, a rule, the lamp
    g.append(wordmark(6, 15.5, 1.0, sp["ink"], sp["keyc"]))
    g.append(rainbow(6, 25.4, 12, 2.2))
    g.append(pix(20.4, 25.6, "USB MIC + KEYS", 0.27, sp["ink"], dot=True))
    g.append(line(6, 29.8, 40, 29.8, mix(sp["lower"], -0.35), 0.3))
    g.append(pix(6, 31.6, "<", 0.3, sp["keyc"]))
    g.append(pix(9.4, 31.6, "PUSH TO TALK", 0.3, sp["ink"], dot=True))
    g.append(circ(51, 29.8, 1.7, "#e03b2d", "#4a0f0a", 0.2))
    g.append(pix(51 - pix_w("ON AIR", 0.27) / 2, 32.4, "ON AIR", 0.27, sp["ink"], dot=True))
    g.append(pix(6, 5.2, "V0.5", 0.3, mix(sp["ink"], 0.0), dot=True))
    dial_wheel(g, bid, sp, 1, dial)
    key_plain(g, sp["keyc"], sp["keyedge"])
    g.append(f'<g transform="translate(-3.15,38.4) rotate(-90)">{pix(0, 0, "TALK", 0.3, sp["keyink"])}</g>')
    g += [plug_notch(29, sp["edge"]), coil(29, 0, 3, 2.6, 7, sp["coil"])]
    return "".join(g)


def palette(out):
    body = [px_text(60, 62, "talk.01 · v0.5 study · TONE-ON-TONE COLOUR AND OUR OWN LETTERING", 28, INK, "bold", SANS),
            px_text(60, 92, "body and lid in one colour family, only a bright key · a hand-drawn wordmark and a pixel-dot label font made for this device", 15, DIM),
            px_text(1860, 52, "TENTATIVE · NOT A FINAL DESIGN", 13, ORANGE, "bold", MONO, "end"),
            px_text(1860, 72, "front views at 10 mm = 40 px", 12, DIM, "normal", MONO, "end")]
    for i, sp in enumerate(PALETTES):
        x = 60 + i * 335
        body.append(panel(x + 30, 215, body_front(sp, sp["gid"]), 4.0))
        body.append(px_text(x + 4, 620, sp["name"], 18, INK, "bold", SANS))
        for k2, part in enumerate(textwrap.wrap(sp["sub"], 36)):
            body.append(px_text(x + 4, 640 + k2 * 15, part, 11.5, DIM))
    # type specimen
    ox = 1120
    body.append(px_text(ox, 150, "OUR OWN LETTERING", 16, INK, "bold", SANS))
    body.append(px_text(ox, 172, "the wordmark is drawn, not typed: one stroke weight, round ends, an open bowl, the dot, 0 and 1 in the accent colour", 11, DIM))
    body.append(panel(ox, 190, wordmark(0, 0, 1.0, INK, ORANGE, 1.15), 8))
    body.append(px_text(ox, 270, "W1 · stroke 1.15 mm, 6 mm tall (on the fronts)", 11, DIM))
    body.append(panel(ox + 400, 190, wordmark(0, 0, 1.0, INK, ORANGE, 1.9), 8))
    body.append(px_text(ox + 400, 270, "W2 · stroke 1.9 mm: chunkier", 11, DIM))
    body.append(px_text(ox, 316, "THE LABEL FONT (5 x 7 dots, drawn here as squares and as dots)", 14, INK, "bold", SANS))
    body.append(panel(ox, 336, pix(0, 0, "DICT TALK OPEN LOCK", 0.62, INK) + pix(0, 6, "ON AIR  USB MIC + KEYS  V0.5", 0.62, INK, dot=True) + pix(0, 12, "< PUSH TO TALK", 0.62, ORANGE), 7))
    notes = ["What the lettering has to respect (FDM):",
             "· a 0.4 mm nozzle prints lines of about 0.8 mm or more. The wordmark (1.15 mm strokes) can be raised or engraved; the pixel labels at 2 mm tall cannot, so they are decals, UV print or paint-filled engraving. If they must be printed, use cells of 0.7 mm and a text 5 mm tall (a few big words only).",
             "· the font is original: 5 x 7 dot letters drawn for this project (no third-party font). The wordmark is hand-drawn too.",
             "",
             "Tone-on-tone, in short:",
             "· the key is the only loud thing; the body and lid stay in one family, the lid a shade deeper so the seam reads;",
             "· the wheel is the dark (or the light) part, as the pair of the key; the dot, the 0 and the 1 carry the key's colour.",
             "· all three palettes also work with the red lamp; the lamp is the second spot of colour."]
    yy = 490
    for ln in notes:
        for part in (textwrap.wrap(ln, 76, subsequent_indent="  ") or [""]):
            head = ln.endswith(":")
            body.append(px_text(ox, yy, part, 11.5, INK if head else DIM, "bold" if head else "normal"))
            yy += 15
        yy += 4
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 780" width="1920" height="780"><defs>{"".join(r5.DEFS)}</defs>'
           f'<rect width="1920" height="780" fill="{PAPER}"/>{"".join(body)}</svg>')
    write(out, "palette.svg", svg)


# ---------------------------------------------------------------- the modes: how does the wheel show where it is?
def corner(kind, sp):
    """The top-right corner of the face, drawn four ways (mm). Returns inner SVG for a cropped nested svg."""
    g = [f'<path d="{body_path()}" fill="{sp["lower"]}" stroke="{sp["edge"]}" stroke-width="0.5"/>']
    cur = 1
    if kind == "dial":
        dial_wheel(g, "mz" + kind, sp, cur, True)
        for k, (ik, lab) in enumerate(MODES):
            pass
        return "".join(g)
    # plain wheel with a notch that points at the position
    g.append(f'<clipPath id="mz{kind}"><path d="{body_path()}"/></clipPath><g clip-path="url(#mz{kind})">{circ(WX, WY, WR + 1.8, sp["pocket"], "#000", 0.4)}</g>')
    g.append(circ(WX, WY, WR, sp["wheel"], "#000", 0.45))
    for k in range(30):
        a = math.radians(k * 12)
        g.append(line(WX + (WR - 1.1) * math.sin(a), WY - (WR - 1.1) * math.cos(a), WX + WR * math.sin(a), WY - WR * math.cos(a), sp["rib"], 0.5))
    g.append(circ(WX, WY, WR * 0.55, mix(sp["wheel"], 0.1), mix(sp["wheel"], -0.4), 0.3))
    if kind == "arc":
        angs = [180, 210, 240, 270]
        a = math.radians(angs[cur])
        g.append(line(WX, WY, WX + WR * .55 * math.sin(a), WY - WR * .55 * math.cos(a), sp["keyc"], 1.0, 'stroke-linecap="round"'))
        for k, (ik, lab) in enumerate(MODES):
            th = math.radians(angs[k])
            x, y = WX + 13.2 * math.sin(th), WY - 13.2 * math.cos(th)
            g.append(circ(x, y, 0.5, sp["ink"], "none", 0))
            col = sp["keyc"] if k == cur else sp["ink"]
            g.append(icon(ik, WX + 16.2 * math.sin(th) - 1.0, WY - 16.2 * math.cos(th), col))
    elif kind == "leaders":
        angs = [265, 240, 215, 190]
        rowx = [16.0, 24.5, 33.0, 41.5]
        a = math.radians(angs[cur])
        g.append(line(WX, WY, WX + WR * .55 * math.sin(a), WY - WR * .55 * math.cos(a), sp["keyc"], 1.0, 'stroke-linecap="round"'))
        for k, (ik, lab) in enumerate(MODES):
            th = math.radians(angs[k])
            tx, ty = WX + (WR + 2.4) * math.sin(th), WY - (WR + 2.4) * math.cos(th)
            px_, py_ = tx + 1.4 * math.sin(th), ty - 1.4 * math.cos(th)
            col = sp["keyc"] if k == cur else sp["ink"]
            g.append(f'<polyline points="{f(tx)},{f(ty)} {f(px_)},{f(py_)} {f(rowx[k])},{f(py_)} {f(rowx[k])},25.2" fill="none" stroke="{col}" stroke-width="0.35" stroke-linejoin="round"/>')
            g.append(circ(tx, ty, 0.45, col, "none", 0))
            g.append(icon(ik, rowx[k] - 1.0, 27.0, col))
            g.append(pix(rowx[k] - pix_w(lab, 0.26) / 2, 30.4, lab, 0.26, col, dot=True))
    elif kind == "list":
        angs = [270, 250, 230, 210]
        a = math.radians(angs[cur])
        g.append(line(WX, WY, WX + WR * .55 * math.sin(a), WY - WR * .55 * math.cos(a), sp["keyc"], 1.0, 'stroke-linecap="round"'))
        for k, (ik, lab) in enumerate(MODES):
            th = math.radians(angs[k])
            tx, ty = WX + (WR + 2.4) * math.sin(th), WY - (WR + 2.4) * math.cos(th)
            col = sp["keyc"] if k == cur else sp["ink"]
            yy = 20.0 + k * 3.8
            g.append(f'<polyline points="{f(tx)},{f(ty)} {f(37.6)},{f(yy)}" fill="none" stroke="{col}" stroke-width="0.3" stroke-linejoin="round"/>')
            g.append(circ(tx, ty, 0.45, col, "none", 0))
            g.append(icon(ik, 34.4, yy, col))
            g.append(pix(26.4, yy - 1.0, lab, 0.26, col, dot=True))
    return "".join(g)


def mode(out):
    sp = PALETTES[0]
    body = [px_text(60, 62, "talk.01 · v0.5 study · HOW THE FOUR MODES SHOW, AND HOW THE WHEEL SENSES THEM", 28, INK, "bold", SANS),
            px_text(60, 92, "the owner's question: how to read 'which mode' from a wheel, arc or row, and is there a 4-position encoder", 15, DIM),
            px_text(1860, 52, "TENTATIVE · NOT A FINAL DESIGN", 13, ORANGE, "bold", MONO, "end")]
    schemes = [("A  ARC", "arc", "The icons sit on an arc round the wheel; the wheel's notch points at one.",
                "The most honest picture of a rotary switch; one glance, no learning. Needs a 30 mm arc of free face, close to the cable and the wordmark."),
               ("B  LEADERS", "leaders", "Ticks on the pocket, folded lines down to a row of icons and names.",
                "Neat and flexible: the row can sit anywhere. The lines take about 24 x 12 mm and must be drawn without crossing; the staircase here does not cross."),
               ("C  LIST", "list", "The same ticks, straight lines fanning out to a short vertical list.",
                "Reads like a legend, with names. Takes the most width; the list shares the space of the wordmark."),
               ("D  DIAL", "dial", "The icons ride ON the wheel; a fixed triangle on the body marks the active one (a camera mode dial).",
                "The smallest and the surest: the mode sits right at your thumb, nothing else on the face. But the icons are 2 mm, so a decal or a UV print.")]
    for i, (name, kind, what, note) in enumerate(schemes):
        x = 60 + i * 450
        vb = (14, -1, 46, 40)
        body.append(f'<svg x="{x}" y="125" width="414" height="360" viewBox="{vb[0]} {vb[1]} {vb[2]} {vb[3]}" overflow="hidden">'
                    f'<rect x="{vb[0]}" y="{vb[1]}" width="{vb[2]}" height="{vb[3]}" fill="{PAPER}"/>{corner(kind, sp)}</svg>')
        body.append(px_text(x, 515, name, 17, INK, "bold", SANS))
        for k2, part in enumerate(textwrap.wrap(what, 50)):
            body.append(px_text(x, 537 + k2 * 15, part, 11.5, INK))
        for k2, part in enumerate(textwrap.wrap(note, 50)):
            body.append(px_text(x, 585 + k2 * 15, part, 11.5, DIM))
    body.append(px_text(60, 700, "Recommendation (a proposal): D, the dial, as the default, with A as a printed backup on a lid; B and C only if the face has room.", 13, "#2f6f3a", "bold", MONO))
    # sensing
    body.append(px_text(60, 745, "HOW TO SENSE FOUR POSITIONS  (the thing that decides what the firmware can know)", 16, INK, "bold", SANS))
    rows = [("1  encoder + detent", "relative", "An EC11-class incremental encoder (Alps EC11 comes with 12 to 36 detents and several shaft lengths; the body drawing must be checked). Cheap and common. BUT it is relative: after a reset the firmware does not know where the wheel is. Fix: hard end stops plus a home switch at one end."),
            ("2  two switches + printed cam", "absolute", "A cam on the wheel presses two small switches in a Gray-code pattern: 00, 01, 11, 10 = four positions. Two GPIO pins, no special part, the position is known at power-up. The detent is a spring ball or a printed flexure."),
            ("3  magnet + AS5600", "absolute", "A diametric magnet on the wheel axis over an AS5600 (12-bit, I2C, about 1 deg linearity; the datasheet asks for at least 8 mT). Any number of positions, and later a volume use. More parts; the magnet must be placed over the chip."),
            ("4  potentiometer + ADC", "absolute", "Four voltage zones on one analog pin. Simple wiring, but the track wears and the zones drift; the detent is separate."),
            ("5  a ready 4-position rotary switch", "absolute", "Such switches exist, but I have not checked a small panel-mount one with a thumb-wheel mount, so it is not recommended yet.")]
    yy = 772
    for (nm, kind_, desc) in rows:
        body.append(px_text(60, yy, nm, 12.5, INK, "bold", MONO))
        body.append(px_text(330, yy, kind_, 12.5, "#2f6f3a" if kind_ == "absolute" else "#9a2f1a", "bold", MONO))
        for part in textwrap.wrap(desc, 150):
            body.append(px_text(430, yy, part, 11.5, DIM))
            yy += 15
        yy += 8
    body.append(px_text(60, yy + 10, "Proposal: option 2 for v0.1 (two switches and a cam, absolute, nothing to buy), with option 3 kept for a later volume or fine control.", 12.5, "#2f6f3a", "bold", MONO))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1030" width="1920" height="1030"><defs>{"".join(r5.DEFS)}</defs>'
           f'<rect width="1920" height="1030" fill="{PAPER}"/>{"".join(body)}</svg>')
    write(out, "mode.svg", svg)


# ---------------------------------------------------------------- the removable lid and the stack inside
def lid_front(sp):
    """The lid from the front (mm): two rigid hook tabs on the top edge, two in-plane snap arms at the bottom corners, a thumb notch."""
    g = []
    lw, lh = 58, 56
    g.append(f'<path d="M0,0 H{lw} V{lh - 5} Q{lw},{lh} {lw - 5},{lh} H5 Q0,{lh} 0,{lh - 5} Z" fill="{sp["plate"]}" stroke="{sp["edge"]}" stroke-width="0.4"/>')
    for x in (8, 41):                                      # hook tabs poking out of the top edge
        g.append(rr(x, -2.2, 9, 2.4, 0.5, mix(sp["plate"], -0.12), sp["edge"], 0.3))
    for x, side in ((2.4, 1), (lw - 2.4, -1)):             # in-plane snap arms: a slot beside a slender arm with a bump on the outside
        ax = x if side == 1 else x - 1.2
        g.append(rr(ax + (1.2 if side == 1 else -1.1), 30, 1.0, 22, 0.4, "#15130f", "none", 0))   # the slot (dark)
        g.append(rr(ax, 30, 1.2, 22, 0.4, mix(sp["plate"], -0.2), sp["edge"], 0.2))                # the arm, 1.2 mm thick, 22 mm long (here 12 is free)
        bx = ax - 0.6 if side == 1 else ax + 1.8
        g.append(poly([(bx, 32), (bx + side * -0.0, 32), (bx - side * 0.8 + 0.6 * side * 0, 34)], "none", "none", 0))
        g.append(poly([(ax + (0 if side == 1 else 1.2), 31), (ax + (-0.9 if side == 1 else 2.1), 33), (ax + (0 if side == 1 else 1.2), 35)], sp["keyc"], sp["keyedge"], 0.2))
    g.append(path(f"M{lw / 2 - 4},{lh} a4,4 0 0 1 8,0", "#15130f", "none", 0))                       # the thumb notch
    return "".join(g)


def hook_steps():
    """Three steps (side view, mm): tab in under the lip, swing down, snap."""
    out = []
    for i, ang in enumerate((28, 10, 0)):
        ox = i * 36
        g = []
        g.append(rr(0, 0, 3, 24, 0.5, "#e4dcc8", "#3d382d", 0.25))              # the body wall with a lip at the top
        g.append(rr(0, 0, 8, 2.4, 0.5, "#e4dcc8", "#3d382d", 0.25))
        a = math.radians(ang)
        lx, ly = 4.2, 3.4
        g.append(f'<g transform="translate({f(lx)},{f(ly)}) rotate({f(-ang)})">{rr(0, 0, 2.4, 22, 0.4, "#cdc3aa", "#3d382d", 0.25)}{rr(-1.6, -0.8, 2.0, 1.8, 0.3, "#cdc3aa", "#3d382d", 0.2)}</g>')
        g.append(rr(0, 24, 8, 1.8, 0.4, "#e4dcc8", "#3d382d", 0.25))
        out.append(f'<g transform="translate({ox},0)">{"".join(g)}</g>')
    return "".join(out)


def stack():
    """A side section (mm, front at the left): lid, felt, front wall, board, encoder behind the wheel, battery space, back wall, hatch."""
    g = []
    g.append(rr(0, 0, 22, 92, 3, "#f0ece0", "#3d382d", 0.4))
    g.append(rr(0, 0, 1.8, 36, 0.3, "#e4dcc8", "#3d382d", 0.25))                 # front wall, controls zone
    g.append(rr(0, 36, 2.4, 56, 0.3, "#cdc3aa", "#3d382d", 0.25))                # the lid, 2.4 mm with ridges
    for k in range(18):
        g.append(rr(-0.7, 37.2 + k * 3.0, 0.8, 1.9, 0.3, "#cdc3aa", "#3d382d", 0.1))
    g.append(rr(2.4, 36.6, 0.6, 55, 0.2, "#bdb6a2", "none", 0))                  # felt
    g.append(rr(3.0, 36, 1.6, 56, 0.3, "#e4dcc8", "#3d382d", 0.25))              # front wall under the lid, with the round hole
    g.append(rr(2.9, 45, 1.8, 38, 0, "#15130f", "none", 0))
    g.append(rr(20.4, 0, 1.6, 92, 0.3, "#e4dcc8", "#3d382d", 0.25))              # back wall
    g.append(rr(13.8, 4, 6.6, 21, 0.4, "#2f6b52", "#173d2e", 0.25))              # a development board with headers, about 21 mm long
    g.append(rr(8.0, -0.4, 5, 3.4, 0.6, "#cfcfcf", INK, 0.2))                    # USB-C on top (shown against the board)
    g.append(rr(4.6, 62, 2.2, 14, 0.3, "#2f6b52", "#173d2e", 0.25)); g.append(rr(6.8, 66.5, 1.2, 3.6, 0.3, "#222", "#000", 0.15))   # mic board and MEMS mic
    g.append(rr(0.6, 3.8, 5.4, 13.4, 0.8, "#3e3b35", "#000", 0.3))               # the wheel, edge-on, 5.4 mm thick
    g.append(rr(6.0, 6.6, 6.8, 7.8, 0.6, "#8a857a", "#444", 0.25))               # the encoder body behind it, about 7 mm
    g.append(rr(7.4, 30, 11.6, 24, 0.8, "none", "#8a857a", 0.3).replace("<rect ", '<rect stroke-dasharray="1 0.8" '))   # reserved space (battery later)
    g.append(rr(20.4, 8, 1.6, 22, 0.3, "#cdc3aa", "#3d382d", 0.25))              # the back hatch with pins
    g.append(rr(17.4, 12, 3.0, 14, 0.3, "#222", "#000", 0.2))                    # pin header
    g.append(rr(20.4, 52, 5.5, 38, 1, "#cdc3aa", "#3d382d", 0.3))                # the U stand, closed against the back (drawn open at 90 deg for scale)
    return "".join(g)


def lid(out):
    sp = PALETTES[0]
    body = [px_text(60, 62, "talk.01 · v0.5 study · THE LID WITHOUT SCREWS, AND WHAT SITS INSIDE", 28, INK, "bold", SANS),
            px_text(60, 92, "a battery-cover style lid: two hooks tuck in at the top, two snap arms click in at the bottom, a thumb notch lifts it", 15, DIM),
            px_text(1860, 52, "TENTATIVE · NOT ENGINEERED · NOTHING PRINTED", 13, ORANGE, "bold", MONO, "end")]
    body.append(px_text(60, 140, "THE LID, FROM THE FRONT", 16, INK, "bold", SANS))
    body.append(panel(110, 190, lid_front(sp), 5.2))
    X = lambda x: 110 + x * 5.2
    Y = lambda y: 190 + y * 5.2
    body += [px_text(X(60) + 8, Y(-1.0), "two rigid hook tabs (they do not flex)", 11.5, INK),
             px_text(X(60) + 8, Y(40), "two snap arms: they bend in the plane of the lid", 11.5, INK),
             px_text(X(60) + 8, Y(40) + 15, "bumps (orange) click into recesses in the body wall", 11.5, DIM),
             px_text(X(60) + 8, Y(55) + 8, "thumb notch: put a nail in and lift", 11.5, INK)]
    body.append(px_text(60, 520, "HOW IT GOES ON (side view): tab under the lip, swing down, press until it clicks", 16, INK, "bold", SANS))
    body.append(panel(90, 545, hook_steps(), 5.0))
    for i, s in enumerate(("1 · tabs in", "2 · swing down", "3 · click")):
        body.append(px_text(110 + i * 180, 700, s, 12, INK, "bold", MONO))
    notes = ["Why the snap arms bend in the plane (an FDM reason):",
             "· a printed part is weakest between layers. If the lid lies flat while printing, an arm that bends up and down would stress the layers. An arm that bends sideways (in the plane) bends along its layers.",
             "· so the hooks are rigid and only the two side arms flex, in plane.",
             "",
             "A first size, from the beam formula (a hand calculation, not a test):",
             "· strain at the root = 1.5 x t x y / L^2, with t = 1.2 mm thick, L = 12 mm free length, y = 0.8 mm deflection → 1.5 x 1.2 x 0.8 / 144 = 1.0 %.",
             "· published guidance (informal sources, not checked) gives roughly 8 % elongation at break for PLA and 24 % for PETG, and says to design to only 10 to 15 % of that: about 1 % for PLA (marginal) and 2 to 4 % for PETG (comfortable). So print the lid in PETG, fillet the arm root, and test a coupon first.",
             "· a gap of 0.2 to 0.3 mm round the lid is a usual starting clearance on FDM; to be tuned on the owner's printer."]
    yy = 740
    for ln in notes:
        for part in (textwrap.wrap(ln, 98, subsequent_indent="  ") or [""]):
            head = ln.endswith(":")
            body.append(px_text(60, yy, part, 11.5, INK if head else DIM, "bold" if head else "normal"))
            yy += 15
        yy += 3
    # the stack on the right
    ox, oy, sc = 1150, 150, 7.6
    body.append(px_text(ox - 20, 130, "WHAT SITS INSIDE (side section, front at the left)", 16, INK, "bold", SANS))
    body.append(panel(ox, oy, stack(), sc))
    X2 = lambda x: ox + x * sc
    Y2 = lambda y: oy + y * sc
    def lab(x, y, tx, ty, text):
        return line(X2(x), Y2(y), tx, ty, "#8a857a", 0.8) + circ(X2(x), Y2(y), 3, "#8a857a", "none", 0.0) + px_text(tx + 6, ty + 4, text, 11, INK, "normal", MONO)
    body += [lab(11, 14, X2(24) + 20, Y2(6), "dev board, about 21 mm"),
             lab(10.5, 4, X2(24) + 20, Y2(0), "USB-C on top"),
             lab(3.4, 10, X2(24) + 20, Y2(16), "wheel 5.4 mm + encoder ~7 mm"),
             lab(13, 42, X2(24) + 20, Y2(36), "space kept for a battery later"),
             lab(1.2, 70, X2(24) + 20, Y2(60), "lid 2.4 mm: ridges + base"),
             lab(7.4, 68, X2(24) + 20, Y2(70), "MEMS mic board behind the hole"),
             lab(21, 18, X2(24) + 20, Y2(24), "back hatch with pins"),
             lab(23, 70, X2(24) + 20, Y2(82), "small U stand")]
    notes2 = ["A depth budget (22 mm, tentative):",
              "· front wall 1.8 to 3 + back wall 1.6 leaves about 17 mm inside;",
              "· wheel (5.4) + encoder (~7) + a little air fits in about 13 mm;",
              "· a dev board with headers is about 8 to 9 mm thick, so it fits behind the controls zone;",
              "· part sizes are typical values; check each datasheet (the EC11 drawing, the board you buy)."]
    yy = 880
    for ln in notes2:
        for part in textwrap.wrap(ln, 62, subsequent_indent="  "):
            head = ln.endswith(":")
            body.append(px_text(ox - 20, yy, part, 11.5, INK if head else DIM, "bold" if head else "normal"))
            yy += 15
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1070" width="1920" height="1070"><defs>{"".join(r5.DEFS)}</defs>'
           f'<rect width="1920" height="1070" fill="{PAPER}"/>{"".join(body)}</svg>')
    write(out, "lid.svg", svg)


if __name__ == "__main__":
    o = sys.argv[1] if len(sys.argv) > 1 else "."
    palette(o)
    mode(o)
    lid(o)
