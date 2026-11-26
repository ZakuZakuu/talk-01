# SPDX-License-Identifier: CERN-OHL-P-2.0
"""Catch-strength coupon: a flat floor strip with four keyholes whose catches differ in strength, and two one-peg test caps.
Slide a test cap up each keyhole in turn (drop the peg into the round hole, push up 6 mm) and feel how hard it is to push down again.
    A: the first design (symmetric ramps 0.6, arm 0.9, nub 0.6)       B: current default (ramps 0.7 / 0.4, arm 0.9, nub 0.6)
    C: stiffer arm (arm 1.2, nub 0.6, ramps 0.7 / 0.4)                D: more preload (arm 0.9, nub 0.8, ramps 0.7 / 0.4)
Both are printed flat (the strip with the keyhole face down, the cap face down), no supports.
    python3 cad/catch_test.py
"""
import os
import cadquery as cq
from export_util import export_stl
from s2_lower import box
import s2_cap as C
import s2_frame as F

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
VARIANTS = (("A", dict(arm_w=0.9, nub=0.6, ramp_in=0.6, ramp_hold=0.6)),
            ("B", dict(arm_w=0.9, nub=0.6, ramp_in=0.7, ramp_hold=0.4)),
            ("C", dict(arm_w=1.2, nub=0.6, ramp_in=0.7, ramp_hold=0.4)),
            ("D", dict(arm_w=0.9, nub=0.8, ramp_in=0.7, ramp_hold=0.4)))
PITCH, X0, PY = 13.0, 9.0, 11.0


def strip():
    s = box(0, 0, F.Z_I, PITCH * 4 + 2, 21.0, F.Z_R)
    for i, (name, kw) in enumerate(VARIANTS):
        px = X0 + i * PITCH
        s = s.cut(F.cyl(px, PY - C.SLIDE, C.ENTRY_D / 2, F.Z_I - 0.1, F.Z_R + 0.1))
        s = s.cut(box(px - C.SLOT_W / 2, PY - C.SLIDE, F.Z_I - 0.1, px + C.SLOT_W / 2, PY, F.Z_R + 0.1))
        s = s.cut(F.cyl(px, PY, C.SLOT_W / 2, F.Z_I - 0.1, F.Z_R + 0.1))
        s = F.catch(s, px, PY, **kw)
        for k in range(i + 1):                                      # 1 to 4 dots = A to D, on the floor's upper face
            s = s.cut(F.cyl(px - 1.5 + k * 1.0, 19.0, 0.4, F.Z_R - 0.6, F.Z_R + 0.1))
    return s


def test_cap():
    """One peg on a small plate that lies on the strip (the cap's own geometry: 2.4 mm plate, the peg from C.peg)."""
    plate = box(0, 0, F.Z_R, 12.0, 14.0, F.Z_R + 2.4).edges("|Z").fillet(1.5)
    return plate.translate((-6.0, -7.0 + PY, 0)).union(C.peg(0.0, PY))


def build():
    os.makedirs(OUT, exist_ok=True)
    st = strip().translate((0, 0, -F.Z_I))
    export_stl(st.rotate((0, 0, 0), (1, 0, 0), 180).translate((0, 21.0, 1.6)), os.path.join(OUT, "catch_test_strip.stl"), 0.02, 0.1)
    cp = test_cap()
    f = cp.rotate((0, 0, 0), (1, 0, 0), 180)
    f = f.translate((0, 0, -f.val().BoundingBox().zmin))
    export_stl(f, os.path.join(OUT, "catch_test_cap_PRINT.stl"), 0.02, 0.1)
    return st, cp


if __name__ == "__main__":
    st, cp = build()
    print("catch coupon built into", OUT, "strip", [round(v, 1) for v in (st.val().BoundingBox().xlen, st.val().BoundingBox().ylen, st.val().BoundingBox().zlen)])
