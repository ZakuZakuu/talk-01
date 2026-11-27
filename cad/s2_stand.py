# SPDX-License-Identifier: CERN-OHL-P-2.0
"""The S2 REAR STAND: a U-shaped kickstand that folds INTO a pocket in the back plate (flush with the back, owner's choice 2026-11-27).

Assembled coordinates (z = 0 the back surface, y up the body). The U's two arms hinge near the top (y = Y_P) on two integral stubs that snap
into holes in the pocket's side walls (the arms are springy: pinch them to fit); the foot bar joins them at the bottom. Open, the foot rests on the
desk and the body leans back by THETA (about 25 degrees from vertical). No hard stop: the hinge is held by two little nubs in the pocket that press
the arms by 0.2 mm (a light detent when closed) and by friction when open; if the body sags a stop is to be added.
Printed with its OUTER face down (flat on the bed): the stubs are short horizontal cylinders.
    python3 cad/s2_stand.py
"""
import math
import os
import cadquery as cq
from export_util import export_stl
from s2_lower import box, cyl

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
ST_Z0, ST_Z1 = 0.2, 3.8                  # the stand's thickness range (its outer face 0.2 mm inside the back surface: a fine seam line)
ARMS = ((12.0, 17.0), (31.0, 36.0))      # the two arms' x ranges (5 wide); the island between them stays flush with the plate
FOOT_Y0, FOOT_Y1 = 2.5, 8.0              # the foot bar
Y_P, Z_P = 46.5, 2.0                     # the hinge axis (along x)
ARM_R = 2.5                              # the arms' rounded top ends
STUB_D, STUB_L = 2.2, 1.6
GAP = 0.3                                # the pocket's clearance round the stand
POCKET_DEPTH = 3.9
HOLE_D = 2.5                             # the pocket walls' stub holes (small holes print small: the owner's wheel axle was 2.3 for 2.0)
PAD = (7.5, 2.0, 40.5, 49.5)             # the plate is thickened inward here (x0, y0, x1, y1) ...
PAD_Z = (1.8, 5.1)                       # ... from z 1.8 to 5.1, so that the pocket (3.9 deep) keeps a 1.2 mm floor
THETA = math.radians(25.0)               # the body's lean from the vertical
NUB_Y = Y_P - 8.0
NUB_R, NUB_OUT = 0.8, 0.5


def stand():
    s = None
    for (x0, x1) in ARMS:
        a = box(x0, FOOT_Y0, ST_Z0, x1, Y_P, ST_Z1).union(cyl((x0 + x1) / 2, Y_P, ARM_R, ST_Z0, ST_Z1))
        s = a if s is None else s.union(a)
    foot = box(ARMS[0][0], FOOT_Y0, ST_Z0, ARMS[1][1], FOOT_Y1, ST_Z1)
    s = s.union(foot)
    s = s.edges(cq.selectors.BoxSelector((ARMS[0][0] - .1, FOOT_Y0 - .1, ST_Z0 - 1), (ARMS[0][0] + .1, FOOT_Y0 + .1, ST_Z1 + 1))).edges("|Z").fillet(2.2)
    s = s.edges(cq.selectors.BoxSelector((ARMS[1][1] - .1, FOOT_Y0 - .1, ST_Z0 - 1), (ARMS[1][1] + .1, FOOT_Y0 + .1, ST_Z1 + 1))).edges("|Z").fillet(2.2)
    # the stubs, pointing outward along x
    s = s.union(cq.Workplane("YZ").workplane(offset=ARMS[0][0] - STUB_L).center(Y_P, Z_P).circle(STUB_D / 2).extrude(STUB_L + 0.05))
    s = s.union(cq.Workplane("YZ").workplane(offset=ARMS[1][1] - 0.05).center(Y_P, Z_P).circle(STUB_D / 2).extrude(STUB_L + 0.05))
    return s


def open_angle(length):
    """The opening angle psi (from folded) at which the foot's centre line touches the desk when the body leans THETA."""
    c = (Y_P * math.cos(THETA) + Z_P * math.sin(THETA)) / length
    return THETA + math.acos(c)


def build():
    os.makedirs(OUT, exist_ok=True)
    st = stand()
    export_stl(st.translate((0, 0, -ST_Z0)), os.path.join(OUT, "s2_stand_PRINT_outer_face_down.stl"), 0.02, 0.1)
    return st


if __name__ == "__main__":
    st = build()
    L = Y_P - FOOT_Y0
    psi = open_angle(L)
    print("stand built; leg length %.1f, opening angle %.1f deg for a lean of %.0f deg" % (L, math.degrees(psi), math.degrees(THETA)))
