# SPDX-License-Identifier: CERN-OHL-P-2.0
"""SUPERSEDED (2026-11-26): the owner wants a front with no frame and no visible catches; see s2_cap.py.

The lower part of the S2 front shell with the REAL lid (hooks at the top, snap arms in the lid's side rails), as a test piece.

The piece is the front shell cut at z = 9 (open at the back) and at y = 58 (above the seam beam), so it prints in an hour or two and
shows the lid, the recess, the hook lip, the snap grooves, the finger slot and the round hole on the real body.
Print the shell as exported, FRONT FACE UP (the cavity opens toward the bed; the big round hole leaves no ceiling wider than about 9 mm to bridge) and the lid with its ridges UP.
    python3 cad/s2_lower.py
"""
import os
import cadquery as cq
from export_util import export_stl
from s2_params import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
Z_CUT, Y_TOP = 9.0, 58.0
LID_X0, LID_X1 = SIDE + FIT, W - SIDE - FIT
LID_Y0, LID_Y1 = SIDE + FIT, SEAM_Y - FIT
TABS = ((W / 2 - TAB_OFFSET - TAB_W, W / 2 - TAB_OFFSET), (W / 2 + TAB_OFFSET, W / 2 + TAB_OFFSET + TAB_W))


def box(x0, y0, z0, x1, y1, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))


def cyl(cx, cy, r, z0, z1):
    return cq.Workplane("XY").workplane(offset=z0).center(cx, cy).circle(r).extrude(z1 - z0)


def extrude_xz(pts, y0, y1):
    return cq.Workplane("XZ").workplane(offset=-y1).polyline(pts).close().extrude(y1 - y0)


def shell():
    s = cq.Workplane("XY").workplane(offset=Z_CUT).rect(W, Y_TOP, centered=False).extrude(Z_F - Z_CUT)
    s = s.edges(cq.selectors.BoxSelector((-1, -1, Z_CUT - 1), (W + 1, 1, Z_F + 1))).edges("|Z").fillet(R_CORNER)
    s = s.cut(box(SIDE, SIDE, Z_CUT - 1, W - SIDE, SEAM_Y - 2.0, Z_I))                 # the cavity (open at the back)
    s = s.cut(box(SIDE, SIDE, Z_R, W - SIDE, SEAM_Y, Z_F + 1))                          # the recess for the lid
    for (x0, x1) in TABS:                                                                # the undercut under the lip, for the hooks
        s = s.cut(box(x0 - FIT, SEAM_Y - 0.1, Z_R, x1 + FIT, SEAM_Y + 1.8, Z_R + 1.4))
    s = s.cut(cyl(HOLE_CX, HOLE_CY, HOLE_D / 2, Z_I - 0.1, Z_R + 0.1))                  # the round hole
    for sgn, xe in ((1, LID_X0), (-1, LID_X1)):                                          # the grooves the bumps click into
        xo = xe - sgn * (BUMP + 0.3)                                                      # groove bottom
        xi = SIDE if sgn == 1 else W - SIDE
        lo, hi = sorted((xo, xi + sgn * 0.01))        # open into the recess, no thin skin left
        s = s.cut(box(lo, LID_Y0 + 0.5, Z_R + 0.3, hi, LID_Y0 + 4.4, Z_R + 1.9))
    s = s.cut(cyl(W / 2, 0.0, 7.5, Z_R, Z_F + 1))                                        # a scoop in the chin for the fingertip
    s = s.cut(box(W / 2 - 7, 0.6, Z_I - 0.1, W / 2 + 7, LID_Y0 + 1.6, Z_R + 0.1))      # the finger slot through the front wall, under the lid's bottom edge
    return s


def lid():
    b = box(LID_X0, LID_Y0, Z_R, LID_X1, LID_Y1, Z_R + LID_BASE)                          # the base
    rail = 4.0
    b = b.union(box(LID_X0, LID_Y0, Z_R, LID_X0 + rail, LID_Y1, Z_F)).union(box(LID_X1 - rail, LID_Y0, Z_R, LID_X1, LID_Y1, Z_F))   # side rails, full height
    y = LID_Y0 + 2.0                                                                      # the ridges (bars across, between the rails)
    gaps = []
    while y + RIDGE_W < LID_Y1 - 1.5:
        b = b.union(box(LID_X0 + rail, y, Z_R + LID_BASE, LID_X1 - rail, y + RIDGE_W, Z_F))
        gaps.append((y + RIDGE_W, y + RIDGE_W + RIDGE_GAP))
        y += RIDGE_PITCH
    disc = cyl(HOLE_CX, HOLE_CY, HOLE_D / 2 - 2.0, Z_R - 0.1, Z_R + LID_BASE + 0.1)       # through-slots in the gaps, only over the round hole
    for (g0, g1) in gaps:
        if g1 < LID_Y1 - 1.0:
            b = b.cut(box(LID_X0 + rail, g0, Z_R - 0.2, LID_X1 - rail, g1, Z_R + LID_BASE + 0.2).intersect(disc))
    for (x0, x1) in TABS:                                                                 # the rigid hooks on the top edge
        b = b.union(box(x0, LID_Y1 - 0.2, Z_R + 0.2, x1, LID_Y1 + 1.6, Z_R + 1.2))
    for sgn, xe in ((1, LID_X0), (-1, LID_X1)):                                           # the in-plane snap arms
        xi = xe + sgn * ARM_T
        xs = xe + sgn * (ARM_T + SLOT_W)
        lo, hi = sorted((xi, xs))
        b = b.cut(box(lo, LID_Y0 - 0.5, Z_R - 0.1, hi, LID_Y0 + ARM_L, Z_F + 0.1))
        pts = [(xe, Z_R + 0.4), (xe - sgn * BUMP, Z_R + 0.8), (xe - sgn * BUMP, Z_R + 1.5), (xe, Z_R + 1.9)]
        b = b.union(extrude_xz(pts, LID_Y0 + 0.8, LID_Y0 + 4.0))
    return b


def build():
    os.makedirs(OUT, exist_ok=True)
    sh, ld = shell(), lid()
    export_stl(sh, os.path.join(OUT, "s2_lower_shell.stl"), 0.02, 0.1)
    export_stl(ld, os.path.join(OUT, "s2_lid.stl"), 0.02, 0.1)
    export_stl(sh.union(ld), os.path.join(OUT, "s2_lower_assembled_view.stl"), 0.03, 0.15)
    return sh, ld


if __name__ == "__main__":
    build()
    print("S2 lower shell and lid built into", OUT)
