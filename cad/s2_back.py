# SPDX-License-Identifier: CERN-OHL-P-2.0
"""The S2 BACK PLATE: a flat plate (1.8 mm) that closes the lower frame and the upper shell, held by M2 self-tapping COUNTERSUNK screws.
Printed FLAT with its outer face DOWN on the bed (changed 2026-11-27: the stand's pad, and later the hold-down posts, grow inward = upward from the plate;
the countersinks then widen toward the bed, a 45 degree overhang at the limit; the visible face is the smooth bed face).
It holds the stand's pocket (flush), a pad that thickens the plate under the pocket, the stub holes and nubs, and a slot to reach BOOT / RESET.
The hatch and the microphone hold-down are NOT in this file yet.
    python3 cad/s2_back.py
"""
import os
import cadquery as cq
from export_util import export_stl
from s2_lower import box, cyl
from s2_params import W, H
import s2_frame as F
import s2_upper as U
import s2_stand as S

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
    # the stand: a pad on the inner side, then the pocket (the stand's outline plus a gap), the stub holes and the nubs
    s = s.union(box(S.PAD[0], S.PAD[1], S.PAD_Z[0] - 0.01, S.PAD[2], S.PAD[3], S.PAD_Z[1]))
    wire = S.stand().translate((0, 0, -S.ST_Z0 - 0.1)).faces("<Z").val().outerWire()
    pocket = cq.Workplane("XY").add(wire).toPending().offset2D(S.GAP).extrude(S.POCKET_DEPTH + 0.1)
    s = s.cut(pocket)
    s = s.cut(cq.Workplane("YZ").workplane(offset=S.ARMS[0][0] - S.GAP - S.STUB_L - 0.4).center(S.Y_P, S.Z_P).circle(S.HOLE_D / 2).extrude(S.STUB_L + 0.5))
    s = s.cut(cq.Workplane("YZ").workplane(offset=S.ARMS[1][1] + S.GAP - 0.1).center(S.Y_P, S.Z_P).circle(S.HOLE_D / 2).extrude(S.STUB_L + 0.5))
    for nx in (S.ARMS[0][0] - S.GAP + S.NUB_OUT - S.NUB_R, S.ARMS[1][1] + S.GAP - S.NUB_OUT + S.NUB_R):
        s = s.union(cyl(nx, S.NUB_Y, S.NUB_R, 0.0, S.POCKET_DEPTH))
    cx, cy, ln, wd = PICK_SLOT
    s = s.cut(cq.Workplane("XY").workplane(offset=-0.1).center(cx, cy).slot2D(ln, wd, 0).extrude(T + 0.2))
    return s


def to_print(s):
    return s        # printed as modelled: the outer face (z = 0) on the bed


def build():
    os.makedirs(OUT, exist_ok=True)
    b = back()
    export_stl(to_print(b), os.path.join(OUT, "s2_back_PRINT_outer_face_down.stl"), 0.02, 0.1)
    return b


if __name__ == "__main__":
    b = build()
    bb = b.val().BoundingBox()
    print("S2 back plate built into", OUT, [round(v, 1) for v in (bb.xlen, bb.ylen, bb.zlen)], "holes", len(HOLES))
