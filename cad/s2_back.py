# SPDX-License-Identifier: CERN-OHL-P-2.0
"""The S2 BACK PLATE: a flat plate (1.8 mm) that closes the lower frame and the upper shell, held by M2 self-tapping COUNTERSUNK screws.
Printed FLAT with its outer face UP (so the countersinks narrow downward: no overhang, and the visible face is the top surface).
The hatch, the BOOT/RESET access, the stand and the microphone hold-down are NOT in this file yet.
    python3 cad/s2_back.py
"""
import os
import cadquery as cq
from export_util import export_stl
from s2_lower import cyl
from s2_params import W, H
import s2_frame as F
import s2_upper as U

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
T = F.BACK_Z                           # 1.8
CLEAR_D, CSINK_D = 2.4, 4.2            # the through hole and the 90 degree countersink (M2 flat head about 3.8 to 4.0: to be measured)
EDGE_R = 1.7                           # the outer edge's round (it is on the top when printed)
HOLES = tuple(F.BOSSES) + tuple(U.BOSSES_UP)
PICK_SLOT = (U.USB_X, U.BD_Y1 - 7.0, 11.0, 3.4)       # centre x, y, length, width: the two small buttons behind the USB-C (position estimated from a photo)


def outline():
    s = cq.Workplane("XY").polyline([(0, 0), (W, 0), (W, H - 15.0), (W - 15.0, H), (0, H)]).close().extrude(T)
    for (x, y, r) in ((0, 0, 5.0), (W, 0, 5.0), (0, H, 5.0), (W, H - 15.0, 3.0), (W - 15.0, H, 3.0)):
        s = s.edges("|Z").edges(cq.selectors.BoxSelector((x - .5, y - .5, -1), (x + .5, y + .5, T + 1))).fillet(r)
    return s


def back():
    s = outline()
    s = s.faces("<Z").edges().fillet(EDGE_R)
    depth = (CSINK_D - CLEAR_D) / 2
    for (x, y) in HOLES:
        s = s.cut(cyl(x, y, CLEAR_D / 2, -0.1, T + 0.1))
        cone = cq.Solid.makeCone(CSINK_D / 2, CLEAR_D / 2, depth, cq.Vector(x, y, 0.0), cq.Vector(0, 0, 1))
        s = s.cut(cq.Workplane("XY").add(cone))
        s = s.cut(cyl(x, y, CSINK_D / 2, -0.1, 0.0))
    cx, cy, ln, wd = PICK_SLOT
    s = s.cut(cq.Workplane("XY").workplane(offset=-0.1).center(cx, cy).slot2D(ln, wd, 0).extrude(T + 0.2))
    return s


def to_print(s):
    f = s.rotate((0, 0, 0), (1, 0, 0), 180)
    bb = f.val().BoundingBox()
    return f.translate((0, -bb.ymin, -bb.zmin))


def build():
    os.makedirs(OUT, exist_ok=True)
    b = back()
    export_stl(to_print(b), os.path.join(OUT, "s2_back_PRINT_outer_face_up.stl"), 0.02, 0.1)
    return b


if __name__ == "__main__":
    b = build()
    bb = b.val().BoundingBox()
    print("S2 back plate built into", OUT, [round(v, 1) for v in (bb.xlen, bb.ylen, bb.zlen)], "holes", len(HOLES))
