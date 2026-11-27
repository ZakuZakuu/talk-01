# SPDX-License-Identifier: CERN-OHL-P-2.0
"""The S2 LOWER FRAME: the part under the cap. Designed to be printed FRONT FACE DOWN with NO SUPPORTS.

Why a split body: a hollow shell printed face down needs every feature to hang from the face and grow toward the back. The lower zone's
floor (the cap seat) sits 2.4 mm behind the control zone's face, so in one piece it would float above the bed. So the body is two shells:
this lower frame (its cap-seat face on the bed) and an upper shell (its front face on the bed), joined at y = 52 under the cap's top edge,
and closed by a flat back plate; all held with M2 self-tapping screws.

Face down, the floor is just a flat profile on the bed: the keyholes, the detent tongue (a flat cantilever lying on the bed) and the spokes
of the microphone hub cost nothing. Walls, screw bosses and the microphone seat grow upward from the floor. Coordinates here are the
ASSEMBLED ones (z = 0 the back, the cap seat at z = 14.6); the exported print file is flipped.
    python3 cad/s2_frame.py
"""
import math
import os
import cadquery as cq
from export_util import export_stl
from s2_lower import box, cyl, extrude_xz
from s2_params import W, WALL, Z_R, Z_I, SEAM_Y, R_CORNER
import s2_cap as C

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
BACK_Z = 1.8                        # the back plate seats here
Y_TOP = SEAM_Y                      # the seam with the upper shell, 52
END_T = 1.6                         # the end wall at the seam
BOSS_OD, PILOT_D, PILOT_DEPTH = 5.0, 1.9, 7.0     # M2 self-tapping; the pilot is modelled 0.3 over the 1.6 rule because small holes print small
BOSSES = ((4.6, 4.6), (W - 4.6, 4.6), (WALL + 2.3, 26.0), (W - WALL - 2.3, 26.0), (W - WALL - 2.3, 46.0))   # no boss on the left at y 46: the key's lane (x < 10, y 28 to 78) is kept free;   # side bosses overlap the wall by 0.2 mm (a tangent boss makes a non-manifold edge)
HUB_C = C.HOLE_C
HUB_OD, SEAT_ID, SEAT_BOT = 17.0, 14.2, 9.0       # the microphone seat: the round board (13 to 13.8) is to be measured
SOUND_D = 7.0                                      # the opening in the hub's flange in front of the board's sound hole
SPOKES = (90.0, 210.0, 330.0)
# the in-plane CATCH at each keyhole: a flat arm cut from the floor beside the slot, a nub on its free end pushes into the slot and sits just behind the peg
ARM_W, ARM_CUT = 1.2, 0.8          # arm width (owner picked coupon variant C, 2026-11-27), the cut round it
ARM_BELOW, ARM_ABOVE = 3.0, 4.0    # the arm runs from 3 mm below the peg's resting point to 4 mm above it (fixed at the top)
NUB = 0.6                          # how far the nub reaches into the slot: the neck (2.4 in a 2.8 slot) meets 0.4 mm of interference
NUB_Y0, NUB_Y1 = 0.1, 1.6          # the nub's footprint along the arm from its free end; its top edge stays 0.2 mm below the resting neck
RAMP_IN, RAMP_HOLD = 0.7, 0.4      # the ramp the peg climbs when the cap is pushed up (gentle, about 49 deg) and the one that holds it against sliding down (steep, about 56 deg): owner 2026-11-27, 'slides down too easily'


def outline_solid(z0, z1, y_top):
    s = cq.Workplane("XY").workplane(offset=z0).rect(W, y_top, centered=False).extrude(z1 - z0)
    return s.edges(cq.selectors.BoxSelector((-1, -1, z0 - 1), (W + 1, 1, z1 + 1))).edges("|Z").fillet(R_CORNER)


def catch(s, px, py, arm_w=ARM_W, nub=NUB, ramp_in=RAMP_IN, ramp_hold=RAMP_HOLD, side=None):
    """Cut one catch arm beside the keyhole slot at (px, py) and add its nub (also used by the catch coupon with other strengths).
    side = +1: the arm is on the +x side of the slot, -1: on the -x side. Default: away from the middle of the body (the left keyholes
    would otherwise put the arm's root inside the round opening)."""
    if side is None:
        side = 1 if px > W / 2 else -1
    xs0 = px + side * C.SLOT_W / 2                       # the slot's edge on the arm's side
    xa1 = xs0 + side * arm_w                             # the arm's outer face
    xc = xa1 + side * ARM_CUT                            # the far side of the cut
    ya0, ya1 = py - ARM_BELOW, py + ARM_ABOVE
    s = s.cut(box(min(xa1, xc), ya0 - ARM_CUT, Z_I - 0.1, max(xa1, xc), ya1, Z_R + 0.1))           # the outer cut
    s = s.cut(box(min(xs0, xc), ya0 - ARM_CUT, Z_I - 0.1, max(xs0, xc), ya0, Z_R + 0.1))           # the cut under the free end
    n = (cq.Workplane("XY").workplane(offset=Z_I).polyline([(xs0, ya0 + NUB_Y0), (xs0 - side * nub, ya0 + NUB_Y0 + ramp_in), (xs0 - side * nub, ya0 + NUB_Y1 - ramp_hold), (xs0, ya0 + NUB_Y1)]).close().extrude(Z_R - Z_I))
    return s.union(n)


def frame(with_extension=False):
    y_top = Y_TOP + (8.0 if with_extension else 0.0)          # the test piece gets a plate beyond the seam for the stop bar
    s = outline_solid(BACK_Z, Z_R, y_top)
    s = s.cut(box(WALL, WALL, BACK_Z - 1, W - WALL, Y_TOP - END_T, Z_I))        # the cavity, open at the back
    # the wire slot through the end wall (between the zones)
    s = s.cut(extrude_xz([(18.0, 11.0), (30.0, 11.0), (24.0, 5.0)], Y_TOP - END_T - 0.1, Y_TOP + 0.1))      # a triangle, apex toward the back: 45 degree flanks, no bridge
    # the floor features
    for (px, py) in C.PEGS:                                                      # the keyholes
        s = s.cut(cyl(px, py - C.SLIDE, C.ENTRY_D / 2, Z_I - 0.1, Z_R + 0.1))
        s = s.cut(box(px - C.SLOT_W / 2, py - C.SLIDE, Z_I - 0.1, px + C.SLOT_W / 2, py, Z_R + 0.1))
        s = s.cut(cyl(px, py, C.SLOT_W / 2, Z_I - 0.1, Z_R + 0.1))
    for (px, py) in C.PEGS:                                                      # the catches: a flat arm beside each slot, in the floor plane
        s = catch(s, px, py)
    # the round opening Ø34, with a hub in the middle held by three spokes (the floor is a flat profile: free to draw)
    ring = cyl(HUB_C[0], HUB_C[1], C.HOLE_D / 2, Z_I - 0.1, Z_R + 0.1)
    keep = cyl(HUB_C[0], HUB_C[1], HUB_OD / 2, Z_I - 0.2, Z_R + 0.2)
    for a in SPOKES:
        ang = math.radians(a)
        cx, cy = HUB_C[0] + (C.HOLE_D / 4 + HUB_OD / 4) * math.cos(ang), HUB_C[1] + (C.HOLE_D / 4 + HUB_OD / 4) * math.sin(ang)
        sp = box(-(C.HOLE_D / 4 - HUB_OD / 4 + 1.0), -1.5, Z_I - 0.2, (C.HOLE_D / 4 - HUB_OD / 4 + 1.0), 1.5, Z_R + 0.2).rotate((0, 0, 0), (0, 0, 1), a).translate((cx, cy, 0))
        keep = keep.union(sp)
    s = s.cut(ring.cut(keep))
    s = s.cut(cyl(HUB_C[0], HUB_C[1], SOUND_D / 2, Z_I - 0.1, Z_R + 0.1))      # the sound opening in the hub's flange
    s = s.union(cyl(HUB_C[0], HUB_C[1], HUB_OD / 2, SEAT_BOT, Z_I + 0.01).cut(cyl(HUB_C[0], HUB_C[1], SEAT_ID / 2, SEAT_BOT - 0.1, Z_I + 0.02)))   # the seat tube
    s = s.cut(cyl(HUB_C[0], HUB_C[1], SOUND_D / 2, Z_I - 0.1, Z_R + 0.1))
    # screw bosses (hang from the floor, open toward the back)
    for (bx, by) in BOSSES:
        boss = cyl(bx, by, BOSS_OD / 2, BACK_Z, Z_I + 0.01)
        s = s.union(boss)
        s = s.cut(cyl(bx, by, PILOT_D / 2, BACK_Z - 0.1, BACK_Z + PILOT_DEPTH))
    # two alignment tabs poking up from the end wall into the upper shell
    for tx in (10.0, W - 10.0):
        s = s.union(box(tx - 1.2, Y_TOP - 0.01, 6.0, tx + 1.2, Y_TOP + 3.0, 8.4))
    return s


def stop_bar():
    """The test piece's stand-in for the upper shell's lower face: a bar the cap stops against (glue it on the extension plate)."""
    return box(WALL + 0.0, 0.0, 0.0, W - WALL, 6.0, 2.4)


def to_print(solid, zmax=Z_R):
    f = solid.rotate((0, 0, 0), (1, 0, 0), 180)
    bb = f.val().BoundingBox()
    return f.translate((0, -bb.ymin, -bb.zmin))


def build():
    os.makedirs(OUT, exist_ok=True)
    fr = frame(with_extension=True)
    export_stl(to_print(fr), os.path.join(OUT, "s2_frame_PRINT_front_down.stl"), 0.02, 0.1)
    export_stl(stop_bar(), os.path.join(OUT, "s2_stop_bar.stl"), 0.02, 0.1)
    cap = C.cap(0.0, groove=False)
    export_stl(fr.union(cap).union(stop_bar().translate((0, Y_TOP, Z_R))), os.path.join(OUT, "s2_frame_assembled_view.stl"), 0.03, 0.15)
    flipped = cap.rotate((0, 0, 0), (1, 0, 0), 180)
    flipped = flipped.translate((0, 0, -flipped.val().BoundingBox().zmin))
    export_stl(flipped, os.path.join(OUT, "s2_cap_PRINT_face_down.stl"), 0.02, 0.1)      # the tightened cap
    return fr


if __name__ == "__main__":
    build()
    print("S2 lower frame and tightened cap built into", OUT)
