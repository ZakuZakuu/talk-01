# SPDX-License-Identifier: CERN-OHL-P-2.0
"""The S2 front cap (the lower lid) as a KEYHOLE SLIDE: the owner wants the front to be one complete plane, edge to edge, with no frame and
no visible catches. So the cap lies ON TOP of the body's walls (it forms the front edge itself), and is held from the inside:

  * four mushroom pegs on its back pass through keyholes in the body's floor and slide 6 mm up, locking the cap against being lifted;
  * the cap's top edge stops against the control zone; a small tongue cut into the floor has a bump that clicks into a groove in the
    cap's back (a detent; the tongue lies flat, so it bends along the print layers, the strong direction).
To take it off: push the cap down 6 mm with the thumb on the ridges, then lift it. Nothing shows on the face.

This is a test piece (the lower part of the front shell, cut at z = 9 and y = 58). Print the shell as exported (front up; the detent tongue hangs
over the cavity, so switch on supports from the bed under it) and the cap from s2_cap_PRINT_face_down.stl (front face down, pegs pointing up).
    python3 cad/s2_cap.py
"""
import os
import cadquery as cq
from export_util import export_stl
from s2_lower import box, cyl
from s2_params import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
Z_CUT, Y_TOP = 9.0, 58.0
HOLE_C = (W / 2, 25.0)                         # the round hole, Ø34 (moved 1 mm down to clear the detent)
SLIDE = 6.0
PEGS = ((11.0, 11.0), (W - 11.0, 11.0), (11.0, 46.0), (W - 11.0, 46.0))  # final positions (the cap slid up); inboard of the screw bosses
ENTRY_D, SLOT_W = 6.2, 2.8
NECK_D, NECK_L, CONE_L, HEAD_D, HEAD_L = 2.4, 1.8, 1.6, 5.0, 0.5   # neck 1.8 on a 1.6 floor: 0.2 mm of play (was 0.3)
CAP_INSET, CAP_TOP_GAP = 0.1, 0.15
CAP_X0, CAP_X1 = CAP_INSET, W - CAP_INSET
CAP_Y0, CAP_Y1 = CAP_INSET, SEAM_Y - CAP_TOP_GAP
RIDGES_END = 43.8                              # above this the cap is a plain band (the detent groove lives there)
TONGUE = dict(x0=15.0, x1=29.0, yc=47.5, w=3.0, slot=0.8)
BUMP_X, BUMP_R, BUMP_H = 16.2, 0.6, 0.8          # bump 0.8 (was 0.6): a firmer click, about 30 % more holding force by the beam formula
GROOVE = dict(x0=11.0, x1=21.0, w=1.6, depth=1.0)


def shell(with_bump=True):
    s = cq.Workplane("XY").workplane(offset=Z_CUT).rect(W, Y_TOP, centered=False).extrude(Z_R - Z_CUT)
    s = s.edges(cq.selectors.BoxSelector((-1, -1, Z_CUT - 1), (W + 1, 1, Z_R + 1))).edges("|Z").fillet(R_CORNER)
    s = s.union(box(0, SEAM_Y - 2.0, Z_CUT, W, Y_TOP, Z_R)).union(box(0, SEAM_Y, Z_R, W, Y_TOP, Z_F))   # the control-zone stub; its lower face at the seam is where the cap's top edge stops
    s = s.cut(box(WALL, WALL, Z_CUT - 1, W - WALL, SEAM_Y - 2.0, Z_I))                  # the cavity, open at the back
    s = s.cut(cyl(HOLE_C[0], HOLE_C[1], HOLE_D / 2, Z_I - 0.1, Z_R + 0.1))              # the round hole
    for (px, py) in PEGS:                                                                # the keyholes: an entry, then a slot 6 mm up
        s = s.cut(cyl(px, py - SLIDE, ENTRY_D / 2, Z_I - 0.1, Z_R + 0.1))
        s = s.cut(box(px - SLOT_W / 2, py - SLIDE, Z_I - 0.1, px + SLOT_W / 2, py, Z_R + 0.1))
        s = s.cut(cyl(px, py, SLOT_W / 2, Z_I - 0.1, Z_R + 0.1))                       # the slot ends in a round, where the neck rests
    t = TONGUE                                                                           # the detent tongue: a U-slot round a flat tongue, fixed at x1
    y0, y1 = t["yc"] - t["w"] / 2, t["yc"] + t["w"] / 2
    s = s.cut(box(t["x0"] - t["slot"], y1, Z_I - 0.1, t["x1"], y1 + t["slot"], Z_R + 0.1))
    s = s.cut(box(t["x0"] - t["slot"], y0 - t["slot"], Z_I - 0.1, t["x1"], y0, Z_R + 0.1))
    s = s.cut(box(t["x0"] - t["slot"], y0 - t["slot"], Z_I - 0.1, t["x0"], y1 + t["slot"], Z_R + 0.1))
    if with_bump:
        s = s.union(cyl(BUMP_X, t["yc"], BUMP_R, Z_R - 0.05, Z_R + BUMP_H).faces(">Z").edges().chamfer(0.25))
    return s


def peg(px, py):
    neck = cyl(px, py, NECK_D / 2, Z_R - NECK_L, Z_R + 0.05)
    cone = (cq.Workplane("XY").workplane(offset=Z_R - NECK_L - CONE_L).center(px, py).circle(HEAD_D / 2)
            .workplane(offset=CONE_L).circle(NECK_D / 2).loft())
    head = cyl(px, py, HEAD_D / 2, Z_R - NECK_L - CONE_L - HEAD_L, Z_R - NECK_L - CONE_L + 0.01)
    return neck.union(cone).union(head)


def cap(offset=0.0, groove=True):
    """The cap; offset (negative = slid down) shifts it along y. offset 0 is the locked position."""
    c = cq.Workplane("XY").workplane(offset=Z_R).center((CAP_X0 + CAP_X1) / 2, (CAP_Y0 + CAP_Y1) / 2).rect(CAP_X1 - CAP_X0, CAP_Y1 - CAP_Y0).extrude(LID_T)
    c = c.edges(cq.selectors.BoxSelector((-1, -1, Z_R - 1), (W + 1, CAP_Y0 + 1, Z_F + 1))).edges("|Z").fillet(R_CORNER - CAP_INSET)
    c = c.faces(">Z").edges(cq.selectors.BoxSelector((-1, -1, Z_F - 0.01), (W + 1, CAP_Y1 - 1, Z_F + 0.01))).fillet(1.5)
    y = CAP_Y0 + 2.0
    gaps = []
    while y + RIDGE_W + RIDGE_GAP < RIDGES_END:
        g0 = y + RIDGE_W
        c = c.cut(box(-1, g0, Z_R + LID_BASE, W + 1, g0 + RIDGE_GAP, Z_F + 1))
        gaps.append((g0, g0 + RIDGE_GAP))
        y += RIDGE_PITCH
    disc = cyl(HOLE_C[0], HOLE_C[1], HOLE_D / 2 - 2.0, Z_R - 0.1, Z_R + LID_BASE + 0.1)  # through-slots, only over the round hole
    for (g0, g1) in gaps:
        c = c.cut(box(-1, g0, Z_R - 0.2, W + 1, g1, Z_R + LID_BASE + 0.2).intersect(disc))
    if groove:                                                                            # the old detent groove in the cap's back (not used by the support-free frame)
        gv = GROOVE
        c = c.cut(box(gv["x0"], TONGUE["yc"] - gv["w"] / 2, Z_R - 0.1, gv["x1"], TONGUE["yc"] + gv["w"] / 2, Z_R + gv["depth"]))
    for (px, py) in PEGS:
        c = c.union(peg(px, py))
    return c.translate((0, offset, 0))


def build():
    os.makedirs(OUT, exist_ok=True)
    sh, cp = shell(), cap()
    export_stl(sh, os.path.join(OUT, "s2_cap_shell.stl"), 0.02, 0.1)
    export_stl(cp, os.path.join(OUT, "s2_cap.stl"), 0.02, 0.1)
    export_stl(sh.union(cp), os.path.join(OUT, "s2_cap_assembled_view.stl"), 0.03, 0.15)
    flipped = cp.rotate((0, 0, 0), (1, 0, 0), 180)                     # for printing: front face down on the bed, pegs pointing up
    flipped = flipped.translate((0, 0, -flipped.val().BoundingBox().zmin))
    export_stl(flipped, os.path.join(OUT, "s2_cap_PRINT_face_down.stl"), 0.02, 0.1)
    return sh, cp


if __name__ == "__main__":
    build()
    print("S2 cap (keyhole slide) built into", OUT)
