#!/usr/bin/env python3
"""Round-6 sheets for talk.01: the side-strip push-to-talk lever.

strip-lever.svg : how the idea works (mechanism, sleeve lock, hand zones, states, feasibility)
round6.svg      : six designs built around the idea, in a beige + bright retro palette, matte finish

The owner's idea: the whole left side of the body is the push-to-talk key. A spring pops it out;
pressing it talks, pressing to the bottom latches, a firm extra push sends. A sliding sleeve holds it
flush so the body is a full rectangle again, which protects it in a bag.
Standard library only. Dimensions are TENTATIVE.

    python3 design/concepts/src/make_round6.py design/concepts/round-6
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_concepts import (INK, PAPER, DIM, ORANGE, f, rr, circ, line, poly, path, t,  # noqa: E402
                           panel, px_text, write, SANS, MONO, dimh)
from make_round5 import mix, grad, emboss, hlines, vslots, dots_rect, knob, plug_notch, coil  # noqa: E402
from make_round4 import screw  # noqa: E402
import make_round5 as r5  # noqa: E402

SC = 4.0
CREAM, TEAL, LAV, ORG, RED, MUST, SAGE = "#e8e1cf", "#3d9aa1", "#8e8cc9", "#e9873a", "#d8483c", "#e1b84f", "#8fb49a"
DARK = "#22262a"


def rainbow(x, y, w=9, h=3.6):
    cols = ("#6dbb58", "#f1c232", "#f08a24", "#d8483c", "#8e6bb8", "#3f8fd2")
    return "".join(rr(x, y + i * h / 6, w, h / 6 + 0.02, 0, c, c, 0.0) for i, c in enumerate(cols))


def badge(x, y, color="#4a463e"):
    return rainbow(x, y) + t(x + 11, y + 3.2, "talk.01", 3.4, "start", color, "bold", SANS)


def rot(inner, ang, px, py):
    return f'<g transform="rotate({f(ang)} {f(px)} {f(py)})">{inner}</g>'


def ghost(x, y, w, h, r=1.5):
    return rr(x, y, w, h, r, "none", "#8a857a", 0.25, 'stroke-dasharray="1.2 0.9"')


def sleeve(x, y, w=10, h=4.8, color=LAV):
    return rr(x, y, w, h, h / 2, color, INK, 0.3) + line(x + 3, y + h / 2, x + w - 3, y + h / 2, mix(color, -0.3), 0.3)


def zigzag(x1, y1, x2, y2, n=5, amp=0.9, color="#5a5750"):
    pts = []
    for i in range(n * 2 + 1):
        u = i / (n * 2)
        px, py = x1 + (x2 - x1) * u, y1 + (y2 - y1) * u
        nx, ny = -(y2 - y1), (x2 - x1)
        ln = math.hypot(nx, ny) or 1
        s = 0 if i in (0, n * 2) else (amp if i % 2 else -amp)
        pts.append((px + nx / ln * s, py + ny / ln * s))
    return f'<polyline points="{" ".join(f"{f(a)},{f(b)}" for a, b in pts)}" fill="none" stroke="{color}" stroke-width="0.3"/>'


# =========================================================================== mechanism sheet
def state_drawing(label, ang, locked=False, push=False):
    """Front-section view of the left strip hinged at its bottom-outer corner (mm)."""
    g = [rr(8, 0, 34, 92, 4, "#d9d3c2", "#6f6a5e", 0.3),
         rr(8.5, 20, 5.5, 9, 1, "#5d5a52", "#3a3832", 0.2)]
    strip = rr(0, 3, 7, 85, 1.5, TEAL, "#1f5a5f", 0.4) + "".join(line(1, 28 + k * 4, 6, 28 + k * 4, "#2c777c", 0.25) for k in range(10))
    dx = 0.9 if push else 0.0
    g.append(rot(f'<g transform="translate({dx},0)">{strip}</g>', -ang, 0, 88))
    # spring between pocket and strip (spring follows the strip)
    a = math.radians(ang)
    sy = 25
    sx = 7 * math.cos(a) - (sy - 88) * math.sin(a) * -1
    xs = 7 * math.cos(a) + (88 - sy) * math.sin(a) * -1
    xs = 7 * math.cos(a) - (88 - sy) * math.sin(a)
    g.append(zigzag(12.5, 24.5, max(xs, 7.2) + dx, 24.5, 5, 0.9))
    # switches and hall
    g.append(rr(8, 50, 2.4, 3, 0.4, "#111", "#000", 0.1)); g.append(rr(8, 68, 2.4, 3, 0.4, "#111", "#000", 0.1))
    g.append(rr(8, 6, 2.2, 3.2, 0.4, "#2b2a28", "#000", 0.1))
    g.append(rot(rr(5.6, 6, 1.4, 3.2, 0.3, ORG, "#6b2509", 0.15), -ang, 0, 88))
    g.append(circ(0.0, 88, 1.3, "#999", "#333", 0.25))
    if locked:
        g.append(sleeve(-1.6, 3.4, 15, 6.4, LAV))
    else:
        g.append(ghost(-1.6, 3.4, 15, 6.4, 3.2))
    g.append(line(-6, 92, 44, 92, INK, 0.4))
    return "".join(g)


def mechanism(out):
    states = [("1 · LOCKED", 0, True, False, "sleeve over the strip: flush rectangle, mic muted, strip ignored"),
              ("2 · READY", 4.0, False, False, "spring holds the strip out about 4°; mic open, lamp on"),
              ("3 · HOLD", 2.0, False, False, "press to mid-travel: switch 1 closes: key down while held"),
              ("4 · CLICK", 0, False, False, "bottom-out: switch 2 closes: latch (hands-free talk)"),
              ("5 · PUSH", 0, False, True, "firm push past the stop: Hall sensor trips: send")]
    body = []
    body.append(px_text(60, 62, "talk.01 · THE SIDE-STRIP LEVER · how it could work", 30, INK, "bold", SANS))
    body.append(px_text(60, 92, "the whole left side is the push-to-talk key · a sleeve holds it flush · the body becomes a full rectangle again", 15, DIM))
    body.append(px_text(1860, 52, "TENTATIVE · NOT A FINAL DESIGN", 13, ORANGE, "bold", MONO, "end"))
    body.append(px_text(1860, 72, "sketches of an idea, not engineered; nothing built or measured", 12, DIM, "normal", MONO, "end"))
    x0 = 70
    for i, (lab, ang, lk, ps, note) in enumerate(states):
        x = x0 + i * 370
        body.append(px_text(x, 150, lab, 16, INK, "bold", SANS))
        body.append(panel(x + 20, 180, state_drawing(lab, ang, lk, ps), 3.3))
        words = note.split(" ")
        ln, lines_ = "", []
        for w in words:
            if len(ln) + len(w) + 1 > 38:
                lines_.append(ln); ln = w
            else:
                ln = (ln + " " + w).strip()
        lines_.append(ln)
        for k, s in enumerate(lines_):
            body.append(px_text(x, 510 + k * 16, s, 11.5, DIM))
    body.append(px_text(70, 126, "front section of the left strip (hinged at its bottom outer corner)   1 = hold switch   2 = click switch   3 = Hall sensor + magnet", 11.5, DIM))

    # sleeve detail
    body.append(px_text(70, 600, "THE SLEEVE (the lock)", 16, INK, "bold", SANS))
    sl = [rr(0, 0, 40, 14, 3, "#d9d3c2", "#6f6a5e", 0.3), rr(0, 3, 8, 8, 1, TEAL, "#1f5a5f", 0.3), rr(2, 4.2, 28, 5.6, 2.8, "#c9c2ae", "#8a857a", 0.25),
          sleeve(16, 4.6, 12, 4.8, LAV), ghost(0.4, 4.6, 12, 4.8, 2.4), t(14, 12.6, "LOCK ◄", 1.5, "end", "#6f6a5e", "normal", MONO), t(30, 12.6, "► READY", 1.5, "start", "#6f6a5e", "normal", MONO)]
    body.append(panel(70, 625, "".join(sl), 8))
    body.append("".join(px_text(70, 770 + k * 17, s, 11.5, DIM) for k, s in enumerate((
        "A slide on a short rail across the top",
        "of the strip. Slid over it, it holds the",
        "strip flush (dashed outline). A magnet or",
        "Hall sensor tells the firmware: LOCKED.",
        "Careful: 'held down by the sleeve' must",
        "NOT count as 'talking'. In LOCK the",
        "firmware reads the sleeve, not the strip."))))

    # hand map
    body.append(px_text(520, 600, "HAND ZONES (left hand holds, right hand on the mouse)", 16, INK, "bold", SANS))
    hm = [rr(0, 0, 58, 92, 5, CREAM, INK, 0.4), rr(0, 2, 11, 88, 3, "#bfe1e3", "#3d9aa1", 0.3), circ(25, 68, 9, "#f6d9a3", "#c98a1f", 0.3),
          rr(51, 12, 7, 22, 3, "#c9d9f0", "#3f6fb0", 0.3), rr(51, 40, 7, 46, 3, "#e4e1d8", "#8a857a", 0.3, 'stroke-dasharray="1 0.8"'),
          t(5.5, 52, "THUMB", 1.8, "middle", "#1f5a5f", "bold", MONO), t(5.5, 56, "strip", 1.8, "middle", "#1f5a5f", "normal", MONO),
          t(25, 66.6, "THUMB PAD", 1.7, "middle", "#7a5410", "bold", MONO), t(25, 70, "wheel (mode)", 1.6, "middle", "#7a5410", "normal", MONO),
          t(54.5, 21, "INDEX", 1.5, "middle", "#27508a", "bold", MONO), t(54.5, 24.4, "rocker", 1.5, "middle", "#27508a", "normal", MONO),
          t(54.5, 62, "GRIP", 1.7, "middle", "#6f6a5e", "bold", MONO), t(54.5, 65.8, "no keys", 1.5, "middle", "#6f6a5e", "normal", MONO),
          rr(16, 14, 30, 28, 3, "#f3efe3", "#b9b3a2", 0.3), t(31, 29, "mic + grille", 1.8, "middle", "#8a857a", "normal", MONO)]
    body.append(panel(520, 625, "".join(hm), 3.4))
    body.append("".join(px_text(760, 640 + k * 16, s, 11.5, DIM) for k, s in enumerate((
        "Only three controls matter:",
        "· push to talk (the strip, left thumb)",
        "· switch mode (a thumb-pad wheel, or an",
        "   index-finger rocker on the right edge)",
        "· lock (the sleeve, which can also be power)",
        "",
        "The gripping fingers (middle, ring, little)",
        "rest on the right edge: put NO keys there,",
        "or they will be pressed by holding it.",
        "Index finger: the top of the right edge",
        "is the one place that is easy to reach."))))

    # state table
    body.append(px_text(1240, 600, "WHAT THE FIRMWARE WOULD DO", 16, INK, "bold", SANS))
    rows = [("sleeve", "strip", "meaning"), ("over strip", "any", "LOCK: mic muted, strip ignored"), ("off", "rest", "READY"),
            ("off", "mid-travel", "TALK / DICT: key held (by mode)"), ("off", "bottom click", "LATCH: hands-free"), ("off", "firm push", "SEND: end and send")]
    for i, (a, b, c) in enumerate(rows):
        yy = 632 + i * 22
        w_ = "bold" if i == 0 else "normal"
        body.append(px_text(1240, yy, a, 12.5, INK, w_, MONO))
        body.append(px_text(1350, yy, b, 12.5, INK, w_, MONO))
        body.append(px_text(1470, yy, c, 12.5, INK, w_, MONO))
        body.append(line(1240, yy + 6, 1860, yy + 6, "#d3cdbf", 0.5).replace("<line", '<line').replace('stroke-width="0.5"', 'stroke-width="1"'))
    body.append(px_text(1240, 785, "Variants: a FULL strip (hinged at the bottom or the top);", 11.5, DIM))
    body.append(px_text(1240, 801, "a HALF strip (the upper part pops, the rest is fixed);", 11.5, DIM))
    body.append(px_text(1240, 817, "a PLUNGER (an inset key moving straight out on springs).", 11.5, DIM))

    # feasibility
    body.append(px_text(70, 960, "IS IT FEASIBLE? My reading: yes, as a hobby build. It is not proven until a mock is printed.", 17, INK, "bold", SANS))
    feas = [
        ("Parts (cheap):", INK, "bold"), ("a 2-3 mm steel pin as the hinge; one or two small compression springs (a retractable pen spring is a cheap test);", INK, "normal"),
        ("two micro-switches (hold, click) and a Hall sensor with a magnet (push, and the sleeve position); matte PETG for the strip and sleeve.", INK, "normal"),
        ("", INK, "normal"),
        ("Why it is plausible:", "#2f6f3a", "bold"), ("a hinged strip with a spring is a simple lever. The sleeve is a printed slide on a rail. The mock-up costs little and can", "#2f6f3a", "normal"),
        ("be done without any electronics first, to check the feel.", "#2f6f3a", "normal"), ("", INK, "normal"),
        ("Risks I can see:", "#9a2f1a", "bold"),
        ("1. A 80 mm strip wobbles or twists: a pin through its full length, or a second pin at the top, helps.", "#9a2f1a", "normal"),
        ("2. The gap between strip and body shows: FDM tolerance is about 0.2-0.3 mm, so the seam must be a design feature.", "#9a2f1a", "normal"),
        ("3. Spring force and feel (about 1-2 N, a crisp click) need tuning; printed springs creep, so use metal ones.", "#9a2f1a", "normal"),
        ("4. 'Extra firm push = send' needs a slightly compliant stop; hard to tune, may be replaced by a second button.", "#9a2f1a", "normal"),
        ("5. Matte printed surfaces rub: the strip will wear; the pivot needs a metal pin.", "#9a2f1a", "normal"),
        ("6. The sleeve can be bumped open in a bag: it needs a detent and a Hall sensor so the firmware knows.", "#9a2f1a", "normal")]
    body.append("".join(px_text(70, 990 + k * 18, s, 12.5, c, w) for k, (s, c, w) in enumerate(feas)))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1360" width="1920" height="1360"><defs>{"".join(r5.DEFS)}</defs>'
           f'<rect width="1920" height="1360" fill="{PAPER}"/>{"".join(body)}</svg>')
    write(out, "strip-lever.svg", svg)


# =========================================================================== designs
def common_top(g, cx, coil_color, notch_color="#1b1b1b"):
    g.append(plug_notch(cx, notch_color))
    g.append(coil(cx, 0, 6, 2.6, 7, coil_color))


def corner_screws(g, pts, r=1.2):
    for x, y in pts:
        g.append(screw(x, y, r))


def small_legends(g, items, color="#4a463e"):
    for x, y, s, anchor in items:
        g.append(t(x, y, s, 1.5, anchor, color, "normal", MONO))


def knob_numbers(g, cx, cy, r, color="#4a463e"):
    for k, s in enumerate("1234"):
        a = math.radians(-70 + k * 46)
        g.append(t(cx + (r + 2.4) * math.sin(a), cy - (r + 2.4) * math.cos(a) + 0.6, s, 1.8, "middle", color, "bold", MONO))


def d_a():
    """FULL STRIP: beige + teal, hinged at the bottom, cut top corner, lower line grille."""
    g = [rr(9, 0, 49, 92, 5, grad("a1", CREAM, 0.06), INK, 0.45), rr(16, 14, 38, 25, 3, TEAL, "#1f5a5f", 0.4), hlines(19.5, 17, 31, 8, 2.8, 1.2, "#2a7479"),
         circ(35, 26.5, 1.4, "#143c40", "none", 0.0),
         rr(16, 44, 38, 13, 2, DARK, "#000", 0.4), circ(22.5, 50.5, 1.9, RED, "#4a0f0a", 0.2), t(26.5, 51.2, "ON AIR", 2.0, "start", "#e9dfc0", "bold", MONO)]
    for k in range(9):
        g.append(line(40 + k * 1.1, 48.6, 40 + k * 1.1, 48.6 + (2.2 if k % 4 == 0 else 1.2), "#e9dfc0", 0.2))
    g += [knob(27, 72, 6.6, TEAL, "#f2efe6", 22, 30, 0.0)]
    knob_numbers(g, 27, 72, 6.6)
    g += [rr(56.4, 14, 3.8, 18, 1.9, LAV, INK, 0.35), rr(12, 3, 27, 6, 3, "#cfc8b4", "#8a857a", 0.3), sleeve(24, 3.6, 12, 4.8, LAV), ghost(1.4, 3.6, 12, 4.8, 2.4),
          t(15, 12.2, "LOCK", 1.5, "start", "#4a463e", "normal", MONO), badge(35, 82), t(27, 84.6, "MODE", 1.5, "middle", "#4a463e", "normal", MONO)]
    corner_screws(g, [(54, 5), (54, 87)])
    strip = (path("M6,3 H11 V88 H3.5 Q0,88 0,84.5 V9 Z", TEAL, "#1f5a5f", 0.5) + "".join(line(1.2, 30 + k * 4.2, 9.8, 30 + k * 4.2, "#2a7479", 0.35) for k in range(11)) +
             f'<g transform="translate(6.4,66) rotate(-90)">{t(0, 0, "PUSH TO TALK", 2.4, "middle", "#e9dfc0", "bold", MONO)}</g>')
    g.append(ghost(0, 3, 11, 85, 3))
    g.append(rot(strip, -4, 0, 88))
    common_top(g, 41, "#2a7479")
    return "".join(g)


def d_b():
    """HALF STRIP: only the upper part pops; cream + orange + lavender; vertical slots."""
    g = [rr(9, 0, 49, 92, 5, grad("b1", "#ece5d2", 0.06), INK, 0.45), rr(16, 10, 38, 28, 3, ORG, "#7a3c0e", 0.4), vslots(20, 14, 20, 9, 3.3, 1.7, "#a9561a"),
         circ(35, 24, 1.4, "#5a2a08", "none", 0.0),
         rr(16, 43, 38, 12, 2, DARK, "#000", 0.4), circ(22.5, 49, 1.9, RED, "#4a0f0a", 0.2), t(26.5, 49.8, "ON AIR", 2.0, "start", "#e9dfc0", "bold", MONO),
         knob(27, 74, 6.6, "#f6f1e0", "#e9873a", 22, -30, 0.0), rr(56.4, 16, 3.8, 18, 1.9, ORG, INK, 0.35),
         rr(0, 58, 11, 32, 4, LAV, "#4f4d86", 0.4), sleeve(1.6, 54.6, 12, 4.8, LAV), badge(35, 82)]
    knob_numbers(g, 27, 74, 6.6)
    g.append(t(27, 85.4, "MODE", 1.5, "middle", "#4a463e", "normal", MONO))
    for k in range(5):
        g.append(line(1.6, 64 + k * 4.5, 9.4, 64 + k * 4.5, "#6e6cb0", 0.3))
    corner_screws(g, [(54, 5), (54, 87)])
    strip = (path("M5,2 H11 V56 H0 V8 Q0,2 5,2 Z", ORG, "#7a3c0e", 0.5) + "".join(line(1.2, 22 + k * 4.2, 9.8, 22 + k * 4.2, "#b9591a", 0.35) for k in range(7)) +
             f'<g transform="translate(6.2,40) rotate(-90)">{t(0, 0, "PUSH", 2.4, "middle", "#fff6e6", "bold", MONO)}</g>')
    g.append(ghost(0, 2, 11, 54, 3))
    g.append(rot(strip, -5, 0, 56))
    common_top(g, 41, "#b9591a")
    return "".join(g)


def d_c():
    """PLUNGER: an inset key that moves straight out; teal body, cream strip, dot field, orange buttons."""
    g = [rr(9, 0, 49, 92, 5, grad("c1", "#4a9ba0", 0.06), INK, 0.45), rr(16, 10, 38, 30, 3, "#2f7478", "#17484b", 0.4), dots_rect(19.5, 13.6, 9, 7, 3.9, 1.15, "#d9efef"),
         rr(16, 45, 38, 12, 2, DARK, "#000", 0.4), circ(22.5, 51, 1.9, RED, "#4a0f0a", 0.2), t(26.5, 51.8, "ON AIR", 2.0, "start", "#e9dfc0", "bold", MONO)]
    for i, (cx, lab) in enumerate(((24, "◄ MODE"), (42, "MODE ►"))):
        g += [circ(cx, 71, 5.4, "#bb5c14", "#6b2e07", 0.3), circ(cx, 71, 4.6, ORG, "none", 0.0), circ(cx - 0.8, 70, 2.2, "#f7b27a", "none", 0.0).replace("<circle ", '<circle opacity="0.6" '),
              t(cx, 80, lab, 1.6, "middle", "#e9f4f4", "normal", MONO)]
    g += [badge(24, 85, "#e9f4f4"), sleeve(0.6, 84.6, 14, 4.8, ORG)]
    corner_screws(g, [(54, 5), (54, 87)])
    strip = (rr(0, 3, 9, 84, 2.5, CREAM, "#7a7667", 0.5) + "".join(line(1.2, 30 + k * 4.2, 7.8, 30 + k * 4.2, "#bdb6a2", 0.35) for k in range(11)) +
             f'<g transform="translate(4.8,68) rotate(-90)">{t(0, 0, "PUSH TO TALK", 2.4, "middle", "#4a463e", "bold", MONO)}</g>')
    g.append(ghost(0, 3, 9, 84, 2.5))
    g.append(f'<g transform="translate(-2.4,0)">{strip}</g>')
    g.append(rr(8.8, 5, 1.2, 80, 0.5, "#10282a", "none", 0.0))
    g.append(rr(56.4, 14, 3.8, 18, 1.9, ORG, INK, 0.35))
    common_top(g, 41, "#2f7478")
    return "".join(g)


def d_d():
    """TRAPDOOR: hinged at the top, flares at the bottom; mustard body, red strip."""
    g = [rr(9, 0, 49, 92, 5, grad("d1", MUST, 0.06), INK, 0.45), rr(16, 10, 38, 28, 3, "#2b2a28", "#000", 0.4), vslots(20, 13.5, 21, 9, 3.3, 1.7, "#d6d2c2"),
         circ(35, 24, 1.4, "#5a5a54", "none", 0.0), rr(16, 43, 38, 12, 2, "#fff4cf", "#7a6a1e", 0.4), circ(22.5, 49, 1.9, RED, "#4a0f0a", 0.2),
         t(26.5, 49.8, "ON AIR", 2.0, "start", "#4a3a08", "bold", MONO), knob(27, 72, 6.6, "#2b2a28", "#f2efe6", 22, 30, 0.1), rr(56.4, 14, 3.8, 18, 1.9, RED, INK, 0.35),
         sleeve(0.4, 80.6, 14, 4.8, "#2b2a28"), badge(35, 82, "#4a3a08")]
    knob_numbers(g, 27, 72, 6.6, "#4a3a08")
    g.append(t(27, 84.6, "MODE", 1.5, "middle", "#4a3a08", "normal", MONO))
    corner_screws(g, [(54, 5), (54, 87)])
    strip = (path("M0,3 H11 V88 H0 Z", RED, "#6e1a12", 0.5).replace("M0,3", "M3,3") + "".join(line(1.2, 18 + k * 4.2, 9.8, 18 + k * 4.2, "#a8322a", 0.35) for k in range(12)) +
             f'<g transform="translate(6.2,46) rotate(-90)">{t(0, 0, "PUSH TO TALK", 2.4, "middle", "#ffe9e6", "bold", MONO)}</g>')
    g.append(ghost(0, 3, 11, 85, 3))
    g.append(rot(strip, 4, 0, 3))
    common_top(g, 41, "#8a6d1c")
    return "".join(g)


def d_e():
    """DECK: after the beige + teal + lavender tape deck; teal top window, piano keys."""
    g = [rr(9, 0, 49, 92, 5, grad("e1", CREAM, 0.06), INK, 0.45), rr(9, 0, 49, 30, 5, TEAL, "#1f5a5f", 0.45), rr(9, 14, 49, 16, 0, TEAL, "none", 0.0),
         rr(14, 6, 39, 18, 2, DARK, "#000", 0.4), hlines(17, 8.5, 33, 5, 2.6, 1.0, "#6f787b")]
    g += [circ(33.5, 15, 1.2, "#e9dfc0", "none", 0.0), rr(14, 34, 39, 18, 3, LAV, "#4f4d86", 0.4), rr(17, 37, 33, 12, 2, "#2a2a4a", "#000", 0.3), circ(23, 43, 1.9, RED, "#4a0f0a", 0.2),
          t(27.5, 43.8, "ON AIR", 2.0, "start", "#d8d6f0", "bold", MONO)]
    for k in range(9):
        g.append(line(14 + k * 4, 56, 14 + k * 4, 57.5 + (1.2 if k % 2 == 0 else 0), "#8a857a", 0.25))
    g += [rr(14, 59, 39, 3.4, 1.7, "#cfc8b4", "#8a857a", 0.3), rr(16, 59.3, 8, 2.8, 1.2, TEAL, "#1f5a5f", 0.25), t(14, 66.8, "MODE", 1.5, "start", "#6f6a5e", "normal", MONO)]
    for k, (lab, c) in enumerate((("◄", "#bfc3c5"), ("►", "#bfc3c5"), ("LOCK", RED))):
        x = 14 + k * 13.2
        g += [rr(x, 70, 12, 10, 1.6, "#a9aeb0", "#5a5e60", 0.35), rr(x + 0.8, 70.8, 10.4, 5.4, 1, "#dfe2e3", "none", 0.0), t(x + 6, 78.4, lab, 1.9, "middle", "#2b2a28", "bold", MONO)]
    g += [badge(14, 84.6), rr(56.4, 14, 3.8, 18, 1.9, LAV, INK, 0.35)]
    corner_screws(g, [(54, 5), (54, 87)])
    strip = (path("M0,3 H11 V88 H3.5 Q0,88 0,84.5 Z", "#dfe2e3", "#6f7476", 0.5) + "".join(rr(1.2, 20 + k * 3.2, 8.6, 1.2, 0.6, "#8e9496", "none", 0.0) for k in range(16)))
    g.append(ghost(0, 3, 11, 85, 3))
    g.append(rot(strip, -4, 0, 88))
    g.append(sleeve(1.2, 3.6, 12, 4.8, TEAL))
    common_top(g, 41, "#2a7479")
    # side profile (wedge)
    g.append(path("M66,92 L66,6 Q66,0 72,0 H76 Q79,0 80,3 L96,86 Q97,92 91,92 Z", CREAM, INK, 0.4))
    g.append(path("M66,40 L66,6 Q66,0 72,0 H76 Q79,0 80,3 L84,24 Z", TEAL, "none", 0.0))
    g.append(line(62, 92, 100, 92, INK, 0.5))
    g.append(t(81, -5, "wedge profile", 1.8, "middle", DIM, "normal", MONO))
    g.append(t(81, -2.4, "(leans back ~17°)", 1.8, "middle", DIM, "normal", MONO))
    return "".join(g)


def d_f():
    """COMPO: modular stacked panels with visible screws; silver-cream + orange."""
    SIL = "#e3e0d6"
    g = [rr(9, 0, 49, 92, 4, SIL, "#77736a", 0.5)]
    g += [rr(11, 2, 45, 30, 2, "#ece9df", "#8a867b", 0.4), rr(11, 34, 45, 38, 2, "#ece9df", "#8a867b", 0.4), rr(11, 74, 45, 16, 2, "#ece9df", "#8a867b", 0.4)]
    g += [hlines(16, 7, 35, 9, 2.6, 1.1, "#b7b3a6"), circ(33.5, 20, 1.4, "#6f6b60", "none", 0.0), rr(16, 5, 35, 25, 2, "none", "#9a968a", 0.25)]
    for i, lab in enumerate(("TALK", "MODE", "LOCK", "SEND")):
        x, y = 16 + (i % 2) * 14, 38 + (i // 2) * 11
        g += [rr(x, y, 12, 9, 1.4, "#e58a38", "#8a4510", 0.4), rr(x + 0.6, y + 0.6, 10.8, 3.8, 1, "#f6b985", "none", 0.0).replace("<rect ", '<rect opacity="0.55" '),
              t(x + 6, y + 6.6, lab, 1.6, "middle", "#5a2c08", "bold", MONO)]
    g += [circ(48, 49, 7.2, "#efe3c4", "#a8924e", 0.4), circ(48, 49, 3.6, "#e58a38", "#8a4510", 0.3), circ(48, 49, 1.7, "#cfd2d3", "#555", 0.2)]
    for k in range(8):
        a = math.radians(k * 45)
        g.append(circ(48 + 5.4 * math.sin(a), 49 - 5.4 * math.cos(a), 0.5, "#b8a265", "none", 0.0))
    g += [circ(20, 66, 1.9, RED, "#4a0f0a", 0.2), t(24, 66.8, "ON AIR", 1.8, "start", "#6f6b60", "bold", MONO), badge(15, 79, "#4a463e"),
          rr(56.4, 14, 3.8, 18, 1.9, "#e58a38", INK, 0.35), sleeve(0.6, 3.6, 12, 4.8, "#e58a38")]
    corner_screws(g, [(13, 4), (54, 4), (13, 30), (54, 30), (13, 36), (54, 36), (13, 70), (54, 70), (13, 76), (54, 88), (13, 88)])
    strip = (path("M0,3 H11 V88 H3.5 Q0,88 0,84.5 Z", "#cfd2d3", "#77736a", 0.5) + "".join(rr(1.2, 22 + k * 3.2, 8.6, 1.2, 0.6, "#a9adae", "none", 0.0) for k in range(15)))
    g.append(ghost(0, 3, 11, 85, 3))
    g.append(rot(strip, -4, 0, 88))
    g.append(sleeve(1.2, 3.6, 12, 4.8, "#e58a38"))
    common_top(g, 41, "#e58a38")
    return "".join(g)


CARDS = [
    ("A · FULL STRIP", "beige + teal", d_a, 58, 92,
     ["lineage: the tape-deck / boombox reference (beige with teal), the whole left side as the key",
      "strip: full height, hinged at the bottom, a cut top corner; the sleeve slides over its top",
      "grille: horizontal lines   mode: a thumb-pad wheel (1-4)   cable: teal coil",
      "+ the cleanest version of your idea; the cut corner makes the pop-up look intentional",
      "- an 85 mm strip may wobble; the seam shows"]),
    ("B · HALF STRIP", "beige + orange + lavender", d_b, 58, 92,
     ["lineage: colour-blocked tape-deck panels; only the upper part pops, the lower part is fixed",
      "strip: upper 58% hinged at its lower end; a sleeve on the join holds it flush",
      "grille: vertical slots   mode: a cream wheel with an orange index   cable: orange coil",
      "+ shorter strip: less wobble; the fixed lavender block is a thumb rest",
      "- two parts on the left edge: the join must look deliberate"]),
    ("C · PLUNGER", "teal + cream + orange", d_c, 58, 92,
     ["lineage: boombox buttons (teal) and the compo's orange translucent keys; an inset key",
      "strip: moves straight out on springs (about 2 mm), inset in a groove; a sleeve at the bottom",
      "grille: a dot-matrix field   mode: two orange round buttons   cable: teal coil",
      "+ simplest motion; the gap is a dark seam; no angle to sell",
      "- the whole strip must slide straight without sticking (two guides)"]),
    ("D · TRAPDOOR", "mustard + red", d_d, 58, 92,
     ["lineage: a toy/transistor radio in mustard; the strip is hinged at the TOP and flares at the bottom",
      "strip: red, opens from the bottom, which is where the thumb rests; the sleeve is at the bottom",
      "grille: vertical slots   mode: a black ribbed wheel   cable: mustard coil",
      "+ more travel where the thumb is; very eye-catching",
      "- a long arm from the hinge: the bottom opens widest, so the angle must be small"]),
    ("E · DECK", "cream + teal + lavender", d_e, 58, 92,
     ["lineage: the first reference (a micro-cassette deck): teal top window, lavender panel, piano keys",
      "strip: silver, ribbed like the deck's side block; the sleeve is teal; a wedge body leans back",
      "grille: horizontal lines   mode: a slider plus piano-key buttons   cable: teal coil",
      "+ the most 'deck'; the wedge profile builds in the desk angle",
      "- a wedge body is thicker at the base; a slider needs space"]),
    ("F · COMPO", "silver-cream + orange", d_f, 58, 92,
     ["lineage: the compo stereo (stacked modules, exposed screws, orange translucent keys and dial)",
      "strip: silver; the orange sleeve; three panels with screws; the bottom panel is the hatch",
      "grille: horizontal lines   mode: four orange keys + a translucent dial   cable: orange coil",
      "+ screws as ornament; the modular look suits printed parts",
      "- many small parts and keys; the busiest of the six"]),
]


def lineup(out):
    import textwrap
    xs, ys = (40, 660, 1280), (170, 1000)
    body = []
    for i, (name, tag, fn, W, H, lines) in enumerate(CARDS):
        x, y = xs[i % 3], ys[i // 3]
        body.append(f'<rect x="{x}" y="{y}" width="600" height="800" rx="14" fill="none" stroke="#d3cdbf" stroke-width="2"/>')
        body.append(px_text(x + 16, y + 38, name, 24, INK, "bold", SANS))
        body.append(px_text(x + 16, y + 60, tag, 13, DIM))
        body.append(panel(x + 60, y + 240, fn(), SC))
        yy = y + 650
        for s_ in lines:
            col = "#2f6f3a" if s_.startswith("+") else ("#9a2f1a" if s_.startswith("-") else INK)
            for part in textwrap.wrap(s_, 78, subsequent_indent="  "):
                body.append(px_text(x + 16, yy, part, 11.5, col))
                yy += 15
            yy += 3
    head = (px_text(60, 62, "talk.01 · ROUND 6 · THE SIDE STRIP AS THE PUSH-TO-TALK KEY", 30, INK, "bold", SANS) +
            px_text(60, 92, "six takes on one idea · beige with bright retro colours · matte printed finish · exposed screws · rainbow badge", 15, DIM) +
            px_text(1860, 52, "TENTATIVE · NOT A FINAL DESIGN", 13, ORANGE, "bold", MONO, "end") +
            px_text(1860, 72, "original concepts · same scale in every card (10 mm = 40 px)", 12, DIM, "normal", MONO, "end") +
            px_text(1860, 92, "dashed = the strip in its flush, locked position · see strip-lever.svg", 12, DIM, "normal", MONO, "end") +
            px_text(60, 128, "All: USB-C and a coiled cable on top · a small hatch and a small U stand on the back · the sleeve holds the strip flush.", 14, INK, "normal", MONO))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1840" width="1920" height="1840"><defs>{"".join(r5.DEFS)}</defs>'
           f'<rect width="1920" height="1840" fill="{PAPER}"/>{head}{"".join(body)}</svg>')
    write(out, "round6.svg", svg)


if __name__ == "__main__":
    o = sys.argv[1] if len(sys.argv) > 1 else "."
    mechanism(o)
    lineup(o)
