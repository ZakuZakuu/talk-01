# SPDX-License-Identifier: CERN-OHL-P-2.0
"""The S2 DEBUG HATCH LID (2026-11-28): a flush lid in the back plate over the Super Mini.

Open it to press BOOT and RESET (with a pen tip: the buttons sit about 5 mm in), to see the board's LED, and to reach the board's pads.
The lid's INNER face carries the pin map, engraved (it can be reprinted if the wiring changes; the GPIO numbers are a plan, not yet wired).
It is held by two hooks at its top (they go under the plate) and an in-plane latch at its bottom: a 9 mm arm along the bottom edge, cut
free by a slit, with a nub that clicks into a groove in the opening's bottom wall (the same kind of catch as the cap's, which the owner
tested; arm 1.2 mm wide, strain about 1 % by hand calculation). To open: a fingernail in the scoop under the lid, lift the bottom edge.
To close: top edge first, hooks under the plate, then press the bottom until it clicks.
Printed with its OUTER face DOWN: the hooks and the lettering are on top.
    python3 cad/s2_hatch.py
"""
import os
import cadquery as cq
from export_util import export_stl, text_solid
from s2_lower import box
import s2_back as B

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
CLEAR = 0.15
T = B.T
HX0, HY0, HX1, HY1 = B.HATCH
LX0, LY0, LX1, LY1 = HX0 + CLEAR, HY0 + CLEAR, HX1 - CLEAR, HY1 - CLEAR
TABS = ((6.4, 9.4), (12.6, 15.6))         # the top hooks' x ranges
HOOK_REACH = 0.75                          # beyond the opening's top edge, under the plate
ARM = dict(x_root=6.0, x_free=15.3, w=1.2, slit=0.5)
NUB = dict(x0=13.3, x1=15.0, depth=0.55, z=(0.45, 0.95, 1.1, 1.55))   # z: hold ramp start, flat, flat end, entry ramp end (seen from outside: the hold side is outward)
PIN_MAP = ("MIC 4 5 6", "KEY 7 8", "DIAL 9 10", "FREE 1 2 3")


def lid():
    s = B.rrect(LX0, LY0, LX1, LY1, B.HATCH_R - CLEAR, 0.0, T)
    # the top hooks: tabs on the inner face, a lip reaching over the plate's inner face (0.15 mm clear of it)
    for (x0, x1) in TABS:
        s = s.union(box(x0, LY1 - 2.0, T - 0.01, x1, LY1 + 0.01, T + 0.9))
        s = s.union(box(x0, LY1 - 0.01, T + 0.15, x1, HY1 + HOOK_REACH, T + 0.9))
    # the latch: a slit along the bottom edge and one at the arm's free end make an arm fixed at x_root
    a = ARM
    yb = LY0 + a["w"]
    s = s.cut(box(a["x_root"], yb, -0.1, a["x_free"] + a["slit"], yb + a["slit"], T + 0.1))
    s = s.cut(box(a["x_free"], LY0 - 0.1, -0.1, a["x_free"] + a["slit"], yb + a["slit"], T + 0.1))
    # the nub on the arm's outer edge (toward -y), shaped in (y, z): a steeper ramp on the outer (hold) side, a gentler one on the entry side
    z0, z1, z2, z3 = NUB["z"]
    d = NUB["depth"]
    prof = [(LY0 + 0.01, z0), (LY0 - d, z1), (LY0 - d, z2), (LY0 + 0.01, z3)]
    s = s.union(cq.Workplane("YZ").workplane(offset=NUB["x0"]).polyline(prof).close().extrude(NUB["x1"] - NUB["x0"]))
    # the pin map on the inner face (reads from the inside: no mirror), 0.3 mm deep
    y = LY1 - 3.6
    for line in PIN_MAP:
        s = s.cut(text_solid(line, 1.9, LX0 + 0.8, y, T - 0.3, 0.4))
        y -= 3.25
    return s


def build():
    os.makedirs(OUT, exist_ok=True)
    l = lid()
    export_stl(l, os.path.join(OUT, "s2_hatch_PRINT_outer_face_down.stl"), 0.02, 0.1)
    return l


if __name__ == "__main__":
    l = build()
    bb = l.val().BoundingBox()
    print("hatch lid built: %.1f x %.1f x %.1f mm" % (bb.xlen, bb.ylen, bb.zlen))
