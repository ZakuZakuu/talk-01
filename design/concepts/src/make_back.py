#!/usr/bin/env python3
"""The back of talk.01: a small U stand and a small openable hatch with pins (a hackable bay).

Shared by all round-6 and round-7 bodies. Standard library only. Dimensions are TENTATIVE.

    python3 design/concepts/src/make_back.py design/concepts/round-7
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_concepts import INK, PAPER, DIM, ORANGE, f, rr, circ, line, poly, path, t, panel, px_text, write, SANS, MONO  # noqa: E402
from make_round5 import mix, grad  # noqa: E402
from make_round4 import screw  # noqa: E402
from make_round6 import CREAM, TEAL  # noqa: E402
from make_lineup import lean  # noqa: E402
import make_round5 as r5  # noqa: E402

SC = 5.0
BODY = "#e8e1cf"
GROOVE = "#cfc8b4"


def twist_foot(cx, cy):
    return circ(cx, cy, 2.3, ORANGE, INK, 0.25) + line(cx - 1.6, cy, cx + 1.6, cy, INK, 0.3)


def rear_closed():
    g = [rr(0, 0, 58, 92, 5, grad("bk1", BODY, 0.06), INK, 0.5)]
    # hatch (upper rear, near the board)
    g += [rr(13, 8, 32, 26, 4, "#d9d2bd", "#7a7667", 0.45), twist_foot(18, 29.5), twist_foot(40, 29.5), rr(23, 8.8, 12, 2.6, 1.3, "#b8b19c", "none", 0.0),
          t(29, 20.5, "HATCH", 2.2, "middle", "#6f6a5e", "bold", MONO), t(29, 24.2, "quarter-turn feet", 1.5, "middle", "#6f6a5e", "normal", MONO)]
    # U stand nested in its groove
    g += [rr(14, 38, 30, 50, 4, GROOVE, "#8a857a", 0.35), path("M17,41 V82 H41 V41", "none", "#4a463e", 2.4, 'stroke-linecap="round" stroke-linejoin="round"'),
          circ(17, 41, 1.4, "#b79c4a", "#4d3d12", 0.2), circ(41, 41, 1.4, "#b79c4a", "#4d3d12", 0.2), circ(29, 90, 3.2, BODY, INK, 0.25),
          t(29, 61, "U STAND", 2.2, "middle", "#6f6a5e", "bold", MONO), t(29, 64.6, "folds into the groove", 1.5, "middle", "#6f6a5e", "normal", MONO)]
    g += [rr(7, 89.4, 10, 1.4, 0.6, "#2b2a28", "#2b2a28", 0.05), rr(41, 89.4, 10, 1.4, 0.6, "#2b2a28", "#2b2a28", 0.05)]
    return "".join(g)


def rear_open():
    g = [rr(0, 0, 58, 92, 5, grad("bk2", BODY, 0.06), INK, 0.5)]
    # hatch open: bay revealed
    g += [rr(13, 8, 32, 26, 4, "#2a2926", "#000", 0.45), rr(15, 10, 28, 22, 2, "#2f6b52", "#173d2e", 0.3), rr(24, 8.6, 10, 4, 0.8, "#cfcfcf", INK, 0.2)]
    for k in range(8):
        g.append(rr(17.4 + k * 2.6, 22.8, 1.5, 1.5, 0.2, "#2b2a28", INK, 0.05))
        g.append(rr(17.4 + k * 2.6, 25.6, 1.5, 1.5, 0.2, "#2b2a28", INK, 0.05))
    g += [circ(19, 17, 1.2, "#e6e6e6", INK, 0.12), circ(23, 17, 1.2, "#e6e6e6", INK, 0.12), t(27, 17.8, "BOOT  RST", 1.5, "start", "#e8f1ea", "normal", MONO),
          t(29, 21.2, "I/O PINS", 1.5, "middle", "#e8f1ea", "bold", MONO)]
    g += [rr(46, 8, 3, 26, 1.5, "#d9d2bd", "#7a7667", 0.3)]
    # U stand out of its groove (shown straight down, hinged at the top)
    g += [rr(14, 38, 30, 50, 4, GROOVE, "#8a857a", 0.35), path("M17,41 L10,86 H48 L41,41", "none", "#4a463e", 2.4, 'stroke-linecap="round" stroke-linejoin="round"'),
          circ(17, 41, 1.4, "#b79c4a", "#4d3d12", 0.2), circ(41, 41, 1.4, "#b79c4a", "#4d3d12", 0.2)]
    return "".join(g)


def body_local(th_hatch=True):
    g = [rr(0, -92, 20, 92, 5, BODY, INK, 0.45), rr(0, -84, 1.6, 26, 0.6, "#d9d2bd", "#7a7667", 0.2), rr(4, -60, 9, 34, 4, TEAL, "#1f5a5f", 0.3)]
    return "".join(g)


def build(out):
    body = [px_text(60, 62, "talk.01 · THE BACK · a small U stand and a hatch with pins", 30, INK, "bold", SANS),
            px_text(60, 92, "shared by every body in rounds 6 and 7 · the back is NOT one big cover: a small hatch above, a small U stand below", 15, DIM),
            px_text(1860, 52, "TENTATIVE · NOT A FINAL DESIGN", 13, ORANGE, "bold", MONO, "end"),
            px_text(1860, 72, "a sketch of an idea, not engineered; nothing built or measured", 12, DIM, "normal", MONO, "end")]
    body.append(px_text(60, 150, "REAR · closed", 16, INK, "bold", SANS))
    body.append(panel(60, 180, rear_closed(), SC))
    body.append(px_text(450, 150, "REAR · hatch open, stand out", 16, INK, "bold", SANS))
    body.append(panel(450, 180, rear_open(), SC))
    body.append(px_text(840, 150, "SIDE · on a desk (the body leans 30°)", 16, INK, "bold", SANS))
    body.append(lean(1180, 640, 30, 92, 20, 40, 48, body_local(), "#4a463e", 2.6))
    notes = [
        ("The hatch (above)", INK, "bold"),
        ("a small plate over the top of the board: two quarter-turn feet (the OP-Z idea), a thumb notch.", INK, "normal"),
        ("Behind it: BOOT and RESET buttons, a row of I/O pins for the user's own programs, and a place for the label.", INK, "normal"),
        ("Why above: the dev board sits at the top (its USB-C is on the top edge), so the pins are right there.", INK, "normal"),
        ("", INK, "normal"),
        ("The U stand (below)", INK, "bold"),
        ("a small U about 30 mm wide, hinged mid-height; it nests in a groove and folds out to prop the body at about 30°.", INK, "normal"),
        ("It is short, not a full-back panel; a printed U in PETG with a metal hinge pin; two small rubber feet on its ends.", INK, "normal"),
        ("Variant (round 3, Cut): the hatch IS the stand. It swings out as the kickstand and opens the bay in one action,", INK, "normal"),
        ("but leaves the bay exposed while it stands; I prefer the separate U for that reason.", INK, "normal"),
        ("", INK, "normal"),
        ("Open questions", "#9a2f1a", "bold"),
        ("1. How much of the bay should be reachable without opening? (BOOT/RESET is the one often needed.)", "#9a2f1a", "normal"),
        ("2. Which pins to expose: just the free GPIO and 3V3/GND? (Not decided; the chosen board decides.)", "#9a2f1a", "normal"),
        ("3. A rubber or silicone foot on the stand, so desk and keyboard vibration do not reach the mic.", "#9a2f1a", "normal"),
    ]
    body.append("".join(px_text(60, 700 + k * 19, s, 12.5, c, w) for k, (s, c, w) in enumerate(notes)))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1030" width="1920" height="1030"><defs>{"".join(r5.DEFS)}</defs>'
           f'<rect width="1920" height="1030" fill="{PAPER}"/>{"".join(body)}</svg>')
    write(out, "back.svg", svg)


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else ".")
