#!/usr/bin/env python3
"""talk.01 v0.6 study: the chosen look (WARM, dial) with a BIGGER wheel, and a first fit check with real part sizes.

  front.svg : the WARM front with a 19 mm wheel (the old one was 15 mm), the dial close-up and the old/new wheel
  fit.svg   : an x-ray of the face and a side section with the parts at their sizes (typical or datasheet values; see
              docs/research/component-selection.md), the cam and two switches that read the four wheel positions

    python3 design/concepts/src/make_v06.py design/concepts/v0.6

Standard library only. Everything is TENTATIVE; part sizes are marked verified or typical in the selection note.
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
from make_v04 import plate, R  # noqa: E402
from make_v05 import pix, pix_w, wordmark, key_plain, PALETTES  # noqa: E402
import make_round5 as r5  # noqa: E402

W, H = 58, 92
CHM = 15                               # the chamfer is 15 mm now (it was 12)
WX, WY, WR = 43.3, 12.0, 9.5           # the wheel: 19 mm across (it was 15); the rim sticks out of the chamfer by about 1.2 mm
SP = PALETTES[0]                       # WARM, chosen by the owner


def body6():
    return (f"M5,0 H{W - CHM} L{W - 1},{CHM - 1} Q{W},{CHM} {W},{CHM + 1.5} V{H - 5} Q{W},{H} {W - 5},{H} H5 Q0,{H} 0,{H - 5} V5 Q0,0 5,0 Z")


def sc_icon(kind, x, y, c, k=1.5):
    return f'<g transform="translate({f(x)},{f(y)}) scale({k}) translate({f(-x)},{f(-y)})">{icon(kind, x, y, c)}</g>'


def dial6(g, bid, sp, cur=1):
    g.append(f'<clipPath id="{bid}k"><path d="{body6()}"/></clipPath><g clip-path="url(#{bid}k)">{circ(WX, WY, WR + 1.8, sp["pocket"], "#000", 0.4)}</g>')
    g.append(circ(WX, WY, WR, sp["wheel"], "#000", 0.45))
    for k in range(36):
        a = math.radians(k * 10)
        g.append(line(WX + (WR - 1.2) * math.sin(a), WY - (WR - 1.2) * math.cos(a), WX + WR * math.sin(a), WY - WR * math.cos(a), sp["rib"], 0.5))
    g.append(circ(WX, WY, WR - 1.5, mix(sp["wheel"], 0.07), mix(sp["wheel"], -0.3), 0.25))
    for k, (ik, lab) in enumerate(MODES):
        th = math.radians(225 + (k - cur) * 45)
        x, y = WX + 6.0 * math.sin(th), WY - 6.0 * math.cos(th)
        g.append(sc_icon(ik, x - 1.0, y, sp["keyc"] if k == cur else sp["rib"], 1.5))
    g.append(circ(WX, WY, 1.7, mix(sp["wheel"], 0.18), mix(sp["wheel"], -0.4), 0.25))
    th = math.radians(225)
    ix, iy = WX + (WR + 4.2) * math.sin(th), WY - (WR + 4.2) * math.cos(th)
    g.append(f'<g transform="translate({f(ix)},{f(iy)}) rotate(45)">{poly([(0, -1.2), (1.2, 1.2), (-1.2, 1.2)], sp["keyc"], sp["keyedge"], 0.2)}</g>')


def front6(sp, bid):
    g = [f'<path d="{body6()}" fill="{sp["lower"]}" stroke="{sp["edge"]}" stroke-width="0.5"/>']
    g.append(plate("hridge", sp["plate"], bid))
    g.append(wordmark(6, 16.0, 0.88, sp["ink"], sp["keyc"]))
    g.append(rainbow(6, 25.0, 11, 2.2))
    g.append(pix(19.0, 25.2, "USB MIC + KEYS", 0.27, sp["ink"], dot=True))
    g.append(line(6, 29.8, 40, 29.8, mix(sp["lower"], -0.35), 0.3))
    g.append(pix(6, 31.6, "<", 0.3, sp["keyc"]))
    g.append(pix(9.4, 31.6, "PUSH TO TALK", 0.3, sp["ink"], dot=True))
    g.append(circ(51, 29.8, 1.7, "#e03b2d", "#4a0f0a", 0.2))
    g.append(pix(51 - pix_w("ON AIR", 0.27) / 2, 32.4, "ON AIR", 0.27, sp["ink"], dot=True))
    g.append(pix(6, 5.2, "V0.6", 0.3, sp["ink"], dot=True))
    dial6(g, bid, sp, 1)
    key_plain(g, sp["keyc"], sp["keyedge"])
    g.append(f'<g transform="translate(-3.15,38.4) rotate(-90)">{pix(0, 0, "TALK", 0.3, sp["keyink"])}</g>')
    g += [plug_notch(29, sp["edge"]), coil(29, 0, 3, 2.6, 7, sp["coil"])]
    return "".join(g)


def front(out):
    body = [px_text(60, 62, "talk.01 · v0.6 · WARM + DIAL, WITH A BIGGER WHEEL", 28, INK, "bold", SANS),
            px_text(60, 92, "the owner's choices: palette 1 (WARM), the dial for the modes, labels as stickers or multi-colour print, a bigger wheel", 15, DIM),
            px_text(1860, 52, "TENTATIVE · NOT A FINAL DESIGN", 13, ORANGE, "bold", MONO, "end")]
    body.append(panel(110, 215, front6(SP, "w6"), 7.0))
    # close-up of the dial
    vb = (26, -1, 36, 36)
    body.append(px_text(700, 150, "THE DIAL, CLOSE (about 6x)", 15, INK, "bold", SANS))
    g2 = []
    dial6(g2, "wz", SP)
    body.append(f'<svg x="700" y="165" width="468" height="468" viewBox="{vb[0]} {vb[1]} {vb[2]} {vb[3]}" overflow="hidden">'
                f'<rect x="{vb[0]}" y="{vb[1]}" width="{vb[2]}" height="{vb[3]}" fill="{PAPER}"/>'
                f'<path d="{body6()}" fill="{SP["lower"]}" stroke="{SP["edge"]}" stroke-width="0.5"/>{"".join(g2)}</svg>')
    # old and new wheel
    body.append(px_text(1260, 150, "OLD AND NEW WHEEL (same scale)", 15, INK, "bold", SANS))
    old = circ(10, 10, 7.5, SP["wheel"], "#000", 0.45) + "".join(line(10 + 6.3 * math.sin(math.radians(k * 12)), 10 - 6.3 * math.cos(math.radians(k * 12)), 10 + 7.5 * math.sin(math.radians(k * 12)), 10 - 7.5 * math.cos(math.radians(k * 12)), SP["rib"], 0.5) for k in range(30))
    new = circ(30, 11, 9.5, SP["wheel"], "#000", 0.45) + "".join(line(30 + 8.3 * math.sin(math.radians(k * 10)), 11 - 8.3 * math.cos(math.radians(k * 10)), 30 + 9.5 * math.sin(math.radians(k * 10)), 11 - 9.5 * math.cos(math.radians(k * 10)), SP["rib"], 0.5) for k in range(36))
    body.append(panel(1260, 170, old + new, 10))
    body.append(px_text(1300, 345, "15 mm", 12, DIM, "normal", MONO))
    body.append(px_text(1500, 345, "19 mm", 12, DIM, "normal", MONO))
    notes = ["What changed",
             "· wheel 15 → 19 mm across; the chamfer 12 → 15 mm, so the rim still sticks out only about 1.2 mm;",
             "· the dial ring now holds 3 mm icons, easier to read and to make;",
             "· the wordmark is 12 % smaller and the labels moved a little so nothing touches the bigger pocket.",
             "",
             "Labels (the owner: keep it simple)",
             "· stickers, or multi-colour printing (an AMS-style system): the icons and wordmark become flat colour inlays. Features of about 1 mm and up should be possible; to be tested on the printer. Nothing to paint or fill.",
             "· so the plan is: print the dial's icons in colour if the printer allows, else a sticker on a blank dial.",
             "",
             "Still true from before",
             "· palette WARM (orange key, dark wheel); the lid is a snap-fit with PETG; the dial is read by two switches and a cam."]
    yy = 380
    for ln in notes:
        for part in (textwrap.wrap(ln, 60, subsequent_indent="  ") or [""]):
            head = ln and not ln.startswith("·")
            body.append(px_text(1260, yy, part, 11.5, INK if head else DIM, "bold" if head else "normal"))
            yy += 15
        yy += 3
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 900" width="1920" height="900"><defs>{"".join(r5.DEFS)}</defs>'
           f'<rect width="1920" height="900" fill="{PAPER}"/>{"".join(body)}</svg>')
    write(out, "front.svg", svg)


# ---------------------------------------------------------------- fit check
def xray():
    """The face seen through (mm): the parts behind it, drawn at their sizes. Nothing is placed final."""
    g = [f'<path d="{body6()}" fill="#f6f2e6" stroke="#3d382d" stroke-width="0.4"/>']
    g.append(rr(20.25, 1.0, 17.5, 21, 1.0, "#2f6b52", "#173d2e", 0.25))                      # the XIAO-class board 21 x 17.5, USB-C at the top
    g.append(rr(25.2, -0.8, 7.6, 3.0, 0.6, "#cfcfcf", INK, 0.2))                              # its USB-C
    g.append(circ(WX, WY, WR + 1.8, "none", "#8a857a", 0.3))                                  # the wheel pocket
    g.append(circ(WX, WY, WR, "#3e3b35", "#000", 0.3))
    g.append(rr(36.0, 12.5, 14, 11, 1.0, "#444", "#222", 0.25).replace("<rect ", '<rect fill-opacity="0.8" '))   # the small PCB with the two switches, behind the wheel
    for (sx, sy) in ((38.2, 14.2), (38.2, 19.0)):
        g.append(rr(sx, sy, 4.5, 4.5, 0.6, "#111", "#000", 0.2))
    g.append(rr(8, 40, 16.7, 12.7, 1.0, "#2f6b52", "#173d2e", 0.25))                          # an I2S mic breakout (the Adafruit SPH0645 board is 16.7 x 12.7)
    g.append(circ(16.35, 46.35, 2.0, "#111", "none", 0))
    g.append(circ(29, 64, 19, "none", "#0c0b0a", 0.4))                                        # the round hole
    g.append(rr(7, 33, 44, 2, 0, "none", "#8a857a", 0.2))
    g.append(rr(7.5, 56, 43, 28, 1, "none", "#8a857a", 0.3).replace("<rect ", '<rect stroke-dasharray="1 0.8" '))   # reserved: a battery later (about 43 x 28)
    for (sy, lab) in ((25, "S1"), (42, "S2")):                                                # the two key switches under the key, near its hinge side
        g.append(rr(2.4, sy, 4, 4, 0.5, "#111", "#000", 0.2))
    g.append(poly([(0, 12), (-5.0, 16.5), (-3.2, 56), (0, 58)], "#ee6a2c", "#8a2f0e", 0.4, 'stroke-linejoin="round"'))
    return "".join(g)


def side():
    """Side section, front at the left (mm): how the parts stack in the 22 mm depth."""
    g = [rr(0, 0, 22, 92, 3, "#f6f2e6", "#3d382d", 0.4)]
    g.append(rr(0, 0, 1.8, 36, 0.3, "#e4dcc8", "#3d382d", 0.25))
    g.append(rr(0, 36, 2.4, 56, 0.3, "#cdc3aa", "#3d382d", 0.25))
    g.append(rr(3.0, 36, 1.6, 56, 0.3, "#e4dcc8", "#3d382d", 0.25))
    g.append(rr(2.9, 45, 1.8, 38, 0, "#15130f", "none", 0))
    g.append(rr(20.4, 0, 1.6, 92, 0.3, "#e4dcc8", "#3d382d", 0.25))
    g.append(rr(0.6, 2.5, 5.4, 19, 0.9, "#3e3b35", "#000", 0.3))                              # the wheel, 19 mm across, 5.4 thick
    g.append(rr(6.0, 6.5, 1.4, 11, 0.4, "#8a857a", "#444", 0.2))                              # the cam on its back
    g.append(rr(7.6, 7.0, 4.4, 10, 0.5, "#111", "#000", 0.2))                                 # the two switches, about 4.3 high
    g.append(rr(12.0, 4.5, 1.2, 15, 0.3, "#2f6b52", "#173d2e", 0.2))                          # their small PCB
    g.append(rr(13.8, 1.0, 5.0, 21, 0.4, "#2f6b52", "#173d2e", 0.25))                         # the board and its parts, about 5 mm in all (unverified)
    g.append(rr(14.6, -0.6, 3.2, 2.8, 0.5, "#cfcfcf", INK, 0.2))                              # the USB-C receptacle, near the back
    g.append(rr(4.7, 40, 1.4, 12.7, 0.3, "#2f6b52", "#173d2e", 0.25))                         # the mic board against the front wall
    g.append(rr(6.1, 45.4, 0.9, 2.0, 0.2, "#222", "#000", 0.15))                              # the mic chip
    g.append(rr(7.4, 56, 11.6, 28, 0.8, "none", "#8a857a", 0.3).replace("<rect ", '<rect stroke-dasharray="1 0.8" '))
    g.append(rr(20.4, 12, 1.6, 20, 0.3, "#cdc3aa", "#3d382d", 0.25))
    g.append(rr(17.2, 15, 3.2, 14, 0.3, "#222", "#000", 0.2))
    return "".join(g)


def cam_diagram():
    """The back of the wheel: two lobes, two switches, four positions (Gray code)."""
    g = [circ(0, 0, 9.5, "#e4dcc8", "#3d382d", 0.3)]
    # four positions every 45 deg; the lobe A covers positions 1-2, lobe B positions 2-3 (each 90 deg wide, centred between)
    def lobe(a0, a1, col):
        r0, r1 = 3.4, 5.4
        pts = []
        n = 12
        for i in range(n + 1):
            a = math.radians(a0 + (a1 - a0) * i / n)
            pts.append((r1 * math.sin(a), -r1 * math.cos(a)))
        for i in range(n, -1, -1):
            a = math.radians(a0 + (a1 - a0) * i / n)
            pts.append((r0 * math.sin(a), -r0 * math.cos(a)))
        return poly(pts, col, "#333", 0.2)
    g.append(lobe(180 - 22.5, 180 + 67.5, "#ee6a2c"))      # lobe A: positions 1 and 2
    g.append(lobe(180 + 22.5, 180 + 112.5, "#c9a24b"))     # lobe B: positions 2 and 3
    for k, ang in enumerate((135, 180, 225, 270)):
        a = math.radians(ang)
        g.append(circ(7.6 * math.sin(a), -7.6 * math.cos(a), 0.4, "#3d382d", "none", 0))
    for (nm, ang, col) in (("A", 215, "#ee6a2c"), ("B", 250, "#c9a24b")):
        a = math.radians(ang)
        g.append(rr(4.4 * math.sin(a) - 1.2, -4.4 * math.cos(a) - 1.2, 2.4, 2.4, 0.4, "#111", "#000", 0.15))
    return "".join(g)


def fit(out):
    body = [px_text(60, 62, "talk.01 · v0.6 · A FIRST FIT CHECK WITH REAL PART SIZES (on paper)", 28, INK, "bold", SANS),
            px_text(60, 92, "the parts at their sizes inside the 58 × 92 × 22 mm body: what fits, what is tight, what the bigger wheel moves", 15, DIM),
            px_text(1860, 52, "TENTATIVE · NOTHING BOUGHT OR MEASURED", 13, ORANGE, "bold", MONO, "end"),
            px_text(1860, 72, "x-ray front 10 mm = 60 px · side 10 mm = 60 px", 12, DIM, "normal", MONO, "end")]
    ox, oy, sc = 90, 170, 6.0
    body.append(px_text(ox, 150, "THE FACE, SEEN THROUGH", 15, INK, "bold", SANS))
    body.append(panel(ox + 40, oy + 30, xray(), sc))
    X = lambda x: ox + 40 + x * sc
    Y = lambda y: oy + 30 + y * sc

    def lab(x, y, tx, ty, text, anchor="start"):
        return line(X(x), Y(y), tx, ty, "#8a857a", 0.8) + circ(X(x), Y(y), 3, "#8a857a", "none", 0.0) + px_text(tx + (6 if anchor == "start" else -6), ty + 4, text, 11, INK, "normal", MONO, anchor)
    body += [lab(29, 12, X(60) + 20, Y(8), "board 21 × 17.5 mm, USB-C on top"),
             lab(43, 12, X(60) + 20, Y(18), "wheel 19 mm; the board sits BEHIND it"),
             lab(44, 17, X(60) + 20, Y(28), "small PCB + two switches (about 4.5 mm)"),
             lab(16, 46, X(60) + 20, Y(46), "mic breakout, 16.7 × 12.7 mm"),
             lab(29, 64, X(60) + 20, Y(66), "round hole, 38 mm"),
             lab(29, 70, X(60) + 20, Y(76), "battery room 43 × 28 mm"),
             lab(4.4, 27, X(60) + 20, Y(36), "key switches S1, S2 (under the key)")]
    # side
    sx, sy, ss = 760, 190, 6.0
    body.append(px_text(sx, 150, "SIDE SECTION (front at the left)", 15, INK, "bold", SANS))
    body.append(panel(sx + 20, sy, side(), ss))
    SX = lambda x: sx + 20 + x * ss
    SY = lambda y: sy + y * ss
    def sl(x, y, tx, ty, text):
        return line(SX(x), SY(y), tx, ty, "#8a857a", 0.8) + circ(SX(x), SY(y), 3, "#8a857a", "none", 0.0) + px_text(tx + 6, ty + 4, text, 11, INK, "normal", MONO)
    body += [sl(3.4, 8, SX(22) + 20, SY(2), "wheel, 5.4 mm"),
             sl(6.7, 10, SX(22) + 20, SY(9), "cam on the back, 1.4 mm"),
             sl(9.8, 12, SX(22) + 20, SY(16), "two switches, about 4.3 mm"),
             sl(16.3, 14, SX(22) + 20, SY(24), "board + parts: about 5 mm (not verified)"),
             sl(16.2, 0.8, SX(22) + 20, SY(-3), "USB-C near the back"),
             sl(5.4, 46, SX(22) + 20, SY(42), "mic board on the front wall"),
             sl(1.2, 60, SX(22) + 20, SY(58), "lid 2.4 mm"),
             sl(12.8, 64, SX(22) + 20, SY(72), "battery room: about 11 mm deep")]
    # cam diagram
    body.append(px_text(1260, 150, "HOW TWO SWITCHES READ FOUR POSITIONS (the back of the wheel)", 15, INK, "bold", SANS))
    body.append(panel(1380, 330, cam_diagram(), 11))
    rows = [("position", "A", "B"), ("0 DICT", "0", "0"), ("1 TALK", "1", "0"), ("2 OPEN", "1", "1"), ("3 LOCK", "0", "1")]
    for i, (a, b, c) in enumerate(rows):
        body.append(px_text(1560, 215 + i * 22, a, 12, INK, "bold" if i == 0 else "normal", MONO))
        body.append(px_text(1690, 215 + i * 22, b, 12, INK, "bold" if i == 0 else "normal", MONO))
        body.append(px_text(1740, 215 + i * 22, c, 12, INK, "bold" if i == 0 else "normal", MONO))
    body.append(px_text(1560, 330, "the lobes press the switches; only one", 11, DIM))
    body.append(px_text(1560, 345, "switch changes at each step (Gray code),", 11, DIM))
    body.append(px_text(1560, 360, "so a half-made click never reads as a", 11, DIM))
    body.append(px_text(1560, 375, "wrong mode. The switches sit inboard,", 11, DIM))
    body.append(px_text(1560, 390, "toward the body centre, as the owner asked.", 11, DIM))
    body.append(px_text(1560, 408, "(schematic: lobe angles are set once the", 11, DIM))
    body.append(px_text(1560, 423, "switch spacing is known.)", 11, DIM))
    notes = ["What the fit check finds (on paper):",
             "· Depth: the wheel (5.4) + cam (1.4) + switches (4.3) + their PCB (1.2) end near 13.2 mm from the front; the board sits behind that at 13.8 to 18.8, and the back wall starts at 20.4: about 1.6 mm to spare. TIGHT.",
             "· The board lies BEHIND the wheel stack (they overlap in plan, not in depth). The cable's USB-C is therefore near the back of the top edge, not centred in the thickness: acceptable, but decide it.",
             "· The mic breakout sits against the front wall behind the hole; its port must line up with the hole. Port side varies between modules: check before designing the carrier.",
             "· Battery room is kept: about 43 × 28 × 11 mm, enough for a small LiPo pack (not v0.1).",
             "· Unverified: the board's thickness with its USB-C, whether it has castellated pads, and the exact module sizes. Measure on arrival; the CAD waits for that."]
    yy = 810
    for ln in notes:
        for part in textwrap.wrap(ln, 175, subsequent_indent="  "):
            body.append(px_text(60, yy, part, 11.5, INK if ln.endswith(":") else DIM, "bold" if ln.endswith(":") else "normal"))
            yy += 15
        yy += 2
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1000" width="1920" height="1000"><defs>{"".join(r5.DEFS)}</defs>'
           f'<rect width="1920" height="1000" fill="{PAPER}"/>{"".join(body)}</svg>')
    write(out, "fit.svg", svg)


if __name__ == "__main__":
    o = sys.argv[1] if len(sys.argv) > 1 else "."
    front(o)
    fit(o)
