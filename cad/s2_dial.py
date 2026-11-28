# SPDX-License-Identifier: CERN-OHL-P-2.0
"""The S2 DIAL: the wheel (hero part), its bearing plate, the cam that reads the four modes through two switches (Gray code), the switch carrier.
Assembled coordinates (z = 0 the back, the face at z = 17), the wheel's axis at (WHEEL_CX, WHEEL_CY).

  wheel:   Ø21, z 11.6 to 19.0 (2.0 proud of the face), a D-shaped axle stub (Ø3) behind it, grooves on the rim; printed FRONT FACE DOWN.
  plate:   1.2 mm (z 10.0 to 11.2), with a 45 degree bevel that sits on the upper shell's cone seat, a Ø3.5 bearing hole, two ears for M2 x 5 screws,
           two shoulder bosses with pegs on its back that locate and stop the carrier, and a DETENT ARM (a flat tongue cut in the plate, bending in z
           like the cap's old tongue) whose nub clicks into four dimples on the cam's front face; printed front face down.
  cam:     Ø14 disc pressed on the stub behind the plate (D hole, a hub for grip): four dimples on its front face (the detent) and two arc ridges
           with stair ramps on its back that press the two switches. Printed with its front face down, the ridges growing up.
  carrier: a thin plate behind the cam with a window for each button; corner pillars hold each switch housing; two holes take the plate's pegs.
           The two 6 x 6 x 4.3 tact switches rest on 2 mm foam pads against the back plate and are pushed up against the carrier's underside, so
           the foam takes the overtravel after the button bottoms out. Printed top face down, the pillars growing up.

The wheel's four modes are 45 degrees apart (k = 0..3 at wheel angle 45 k). Switch A is pressed at k = 2, 3 and switch B at k = 1, 2: Gray code 00, 01, 11, 10.
Both switches sit at radius 6 so that a Ø3.5 button spans only +-17 degrees (a smaller radius would be wider than the 45 degree steps can resolve).
The cam works with its front face held 0.3 mm off the plate's back by the detent nub (the nub's spring pushes the cam toward the buttons).
Heights are typical values for a 6 x 6 x 4.3 mm tact switch (housing 3.5, button 0.8): to be confirmed with the real part.
    python3 cad/s2_dial.py
"""
import math
import os
import cadquery as cq
from export_util import export_stl, text_solid
from s2_lower import box, cyl
from s2_params import W, H, WHEEL_R
import s2_upper as U

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
CX, CY = U.WHEEL_CX, U.WHEEL_CY
WHEEL_Z0, WHEEL_Z1 = 11.6, 19.0
STUB_D, STUB_FLAT = 3.0, 0.4                          # the stub's diameter and the D flat's depth
WHEEL_FILLET = 1.0                                    # the face edge (a fillet on the bed face prints fine: each layer steps out 0.3 mm or less)
GROOVES, GROOVE_R = 24, 0.8
# the modes on the wheel's face, engraved (owner's spec: icons by sticker or multi-colour inlay; these letters are the base). The index is
# on the body at the wheel's left (180 deg); turning the wheel 45 deg counter-clockwise brings the next one to it. Which turn direction
# goes with which Gray code is set in the firmware.
MODE_MARKS = (("D", 180.0), ("T", 135.0), ("O", 90.0), ("L", 45.0))     # DICT, TALK, OPEN, LOCK
MARK_R, MARK_DEPTH = 6.6, 0.4
PLATE_Z0, PLATE_Z1, PLATE_HOLE = 10.0, 11.2, 3.5
PLATE_R_FRONT, PLATE_R_BACK = U.SEAT_R1 - 0.1, U.SEAT_R0 - 0.2      # the bevel runs 45 degrees (kept 0.1 clear of the shell's cone)
# --- the cam and the switches
CAM_Z1, CAM_BASE, RIDGE_H, CAM_R = 9.5, 0.6, 0.8, 7.0     # the cam's working position: its front face 0.5 below the plate's back (the nub holds it there)
CAM_Z0 = CAM_Z1 - CAM_BASE - RIDGE_H                       # 8.1: the ridges' lower face
HUB_R = 2.4                                                # a hub round the D hole: 1.4 mm of grip on the stub
RIDGE_R0, RIDGE_R1 = 4.9, 6.9
SWITCH_R = 6.0
SWITCH_ANGLES = {"A": 125.0, "B": 270.0}
RIDGE_RAMP = 7.0                                           # the stair ramps at the ridges' ends, in degrees
RIDGES = {"A": (-35.0, 60.0), "B": (155.0, 250.0)}         # cam-frame ranges INCLUDING the ramps; the plateaus are 7 degrees inside
BTN_H, HOUSING_H = 0.8, 3.5
PRESS = 0.6                                                # a plateau presses the button 0.6 mm: sure to actuate (about 0.25); the foam takes the rest
BTN_REST_TOP = CAM_Z0 + PRESS                              # 8.7
CARRIER_T = 0.8
CARRIER_TOP = BTN_REST_TOP - BTN_H                         # 7.9
CARRIER_Z0 = CARRIER_TOP - CARRIER_T                       # 7.1: the housings' top faces rest against this; the housings span 3.6 to 7.1; foam: 3.6 down to 1.8
FOAM_T = 2.0                                               # a 6 x 6 x 2 pad under each switch (compressed to 1.8)
PEG_ANGLES, PEG_R = (190.0, 345.0), 9.3                    # two shoulder bosses with pegs: the carrier hangs between them and the two switches' foam
BOSS_R, PEG_D = 2.0, 3.0
CAM_HOLE_CLEAR = 0.1
# --- the detent: the nub at world angle DET_ANGLE, radius DET_R; dimples in the cam's front face at DET_ANGLE - 45 k
DET_ANGLE, DET_R = 60.0, 5.0
DET_ARM_L, DET_ARM_W, DET_SLOT = 8.0, 2.4, 0.8
NUB_LEN, NUB_R0, NUB_R1 = 0.8, 1.0, 0.4                    # protrudes 0.8 below the plate's back face (z 9.2); on the flat cam face (z 9.5) the arm bends 0.3
DIMPLE_R, DIMPLE_D = 1.1, 0.4
CHAMFER_LINE = (W + H - 15.0) - math.sqrt(2) * U.WALL - 0.4       # x + y <= this: the plate is cut short before the chamfer wall


def d_stub(z0, z1, extra=0.0):
    """The Ø3 stub with a flat on the +x side (a D), centred on the axis; extra widens it (the cam's hole)."""
    s = cyl(CX, CY, STUB_D / 2 + extra, z0, z1)
    return s.cut(box(CX + STUB_D / 2 - STUB_FLAT + extra, CY - 5, z0 - 1, CX + 5, CY + 5, z1 + 1))


def wheel():
    w = cyl(CX, CY, WHEEL_R, WHEEL_Z0, WHEEL_Z1).faces(">Z").edges().fillet(WHEEL_FILLET)
    for i in range(GROOVES):
        a = 2 * math.pi * i / GROOVES
        w = w.cut(cyl(CX + (WHEEL_R + 0.25) * math.cos(a), CY + (WHEEL_R + 0.25) * math.sin(a), GROOVE_R, WHEEL_Z0 - 1, WHEEL_Z1 + 1))
    for (letter, ang) in MODE_MARKS:      # the four modes, engraved; each one is upright when it stands at the index (on the left, 180 deg)
        t = text_solid(letter, 2.6, 0, 0, WHEEL_Z1 - MARK_DEPTH, MARK_DEPTH + 0.1, halign="center", valign="center")
        t = t.rotate((0, 0, 0), (0, 0, 1), ang - 180.0).translate((CX + MARK_R * math.cos(math.radians(ang)), CY + MARK_R * math.sin(math.radians(ang)), 0))
        w = w.cut(t)
    return w.union(d_stub(CAM_Z0 + 0.2, WHEEL_Z0 + 0.05))


def polar(r, a_deg):
    return CX + r * math.cos(math.radians(a_deg)), CY + r * math.sin(math.radians(a_deg))


def detent_arm_cut():
    """The tongue cut in the plate: a U-slot round an arm that runs along the tangent at the nub; its free end carries the nub."""
    nx, ny = polar(DET_R, DET_ANGLE)
    tx, ty = -math.sin(math.radians(DET_ANGLE)), math.cos(math.radians(DET_ANGLE))      # the counter-clockwise tangent
    rx, ry = nx + 7.0 * tx, ny + 7.0 * ty                                              # the root, 7 mm back along the tangent
    ang = math.degrees(math.atan2(-ty, -tx))                                           # the arm points from the root to the nub: direction -t
    w, s, L = DET_ARM_W, DET_SLOT, DET_ARM_L
    cut = box(0.0, w / 2, PLATE_Z0 - 1, L + s, w / 2 + s, PLATE_Z1 + 1)                  # the long slots on both sides and the end slot, built along +x then placed
    cut = cut.union(box(0.0, -w / 2 - s, PLATE_Z0 - 1, L + s, -w / 2, PLATE_Z1 + 1)).union(box(L, -w / 2 - s, PLATE_Z0 - 1, L + s, w / 2 + s, PLATE_Z1 + 1))
    return cut.rotate((0, 0, 0), (0, 0, 1), ang).translate((rx, ry, 0)), (nx, ny)


def plate():
    z0, z1 = PLATE_Z0, PLATE_Z1
    cone = cq.Solid.makeCone(PLATE_R_BACK, PLATE_R_FRONT, 0.6, cq.Vector(CX, CY, z1 - 0.6), cq.Vector(0, 0, 1))
    body = cq.Workplane("XY").add(cone).union(cyl(CX, CY, PLATE_R_BACK, z0, z1 - 0.6 + 0.01))
    for (bx, by) in U.EAR_BOSSES:
        ang = math.degrees(math.atan2(by - CY, bx - CX))
        arm = box(0, -2.0, z0, math.hypot(bx - CX, by - CY), 2.0, z1).rotate((0, 0, 0), (0, 0, 1), ang).translate((CX, CY, 0))
        body = body.union(arm).union(cyl(bx, by, 3.0, z0, z1))
    keep = cq.Workplane("XY").polyline([(-50, -50), (CHAMFER_LINE + 50, -50), (-50, CHAMFER_LINE + 50)]).close().extrude(50).translate((0, 0, -20))
    body = body.intersect(keep).intersect(box(0, 0, z0 - 1, W - 2.4, H - 2.4, z1 + 1))     # cut short of the chamfer wall, the top and the right wall
    for a in PEG_ANGLES:               # shoulder boss (stops the carrier at its top face) and a peg through the carrier's hole, hanging from the plate's back face
        px, py = polar(PEG_R, a)
        body = body.union(cyl(px, py, BOSS_R, CARRIER_TOP, z0 + 0.01)).union(cyl(px, py, PEG_D / 2, CARRIER_Z0, CARRIER_TOP + 0.01))
    cut, (nx, ny) = detent_arm_cut()
    body = body.cut(cut)
    nub = cq.Solid.makeCone(NUB_R0, NUB_R1, NUB_LEN, cq.Vector(nx, ny, z0 + 0.01 - 0.0), cq.Vector(0, 0, -1))      # hangs from the arm's back face (toward -z)
    body = body.union(cq.Workplane("XY").add(nub))
    body = body.cut(cyl(CX, CY, PLATE_HOLE / 2, z0 - 1, z1 + 1))
    depth = 0.9
    for (bx, by) in U.EAR_BOSSES:       # the screw: Ø2.4 through, 90 degree countersink on the back face (z = z0)
        body = body.cut(cyl(bx, by, 1.2, z0 - 1, z1 + 1))
        cs = cq.Solid.makeCone(2.1, 1.2, depth, cq.Vector(bx, by, z0), cq.Vector(0, 0, 1))
        body = body.cut(cq.Workplane("XY").add(cs))
    return body


def sector(r0, r1, a0, a1, z0, z1, n=24):
    pts_o = [(CX + r1 * math.cos(math.radians(a0 + (a1 - a0) * i / n)), CY + r1 * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
    pts_i = [(CX + r0 * math.cos(math.radians(a1 - (a1 - a0) * i / n)), CY + r0 * math.sin(math.radians(a1 - (a1 - a0) * i / n))) for i in range(n + 1)]
    return cq.Workplane("XY").workplane(offset=z0).polyline(pts_o + pts_i).close().extrude(z1 - z0)


def cam():
    zb = CAM_Z1 - CAM_BASE                         # the base's back face
    c = cyl(CX, CY, CAM_R, zb, CAM_Z1).union(cyl(CX, CY, HUB_R, CAM_Z0, zb + 0.01))
    steps = 4                                      # the ridge ends climb in 4 stair steps over RIDGE_RAMP degrees
    for k, (a0, a1) in RIDGES.items():
        c = c.union(sector(RIDGE_R0, RIDGE_R1, a0 + RIDGE_RAMP, a1 - RIDGE_RAMP, CAM_Z0, zb + 0.01))
        for i in range(steps):                     # step i is (i + 1)/(steps + 1) of the full height
            h = RIDGE_H * (i + 1) / (steps + 1)
            da = RIDGE_RAMP * (steps - i) / steps
            c = c.union(sector(RIDGE_R0, RIDGE_R1, a0 + RIDGE_RAMP - da, a0 + RIDGE_RAMP, zb - h, zb + 0.01))
            c = c.union(sector(RIDGE_R0, RIDGE_R1, a1 - RIDGE_RAMP, a1 - RIDGE_RAMP + da, zb - h, zb + 0.01))
    for k in range(4):                             # the detent's dimples, conical, in the front face
        dx, dy = polar(DET_R, DET_ANGLE - 45.0 * k)
        cone = cq.Solid.makeCone(DIMPLE_R, 0.25, DIMPLE_D, cq.Vector(dx, dy, CAM_Z1 + 0.001), cq.Vector(0, 0, -1))
        c = c.cut(cq.Workplane("XY").add(cone))
    return c.cut(d_stub(CAM_Z0 - 1, CAM_Z1 + 1, extra=CAM_HOLE_CLEAR))


def switch_centres():
    return {k: polar(SWITCH_R, a) for k, a in SWITCH_ANGLES.items()}


def carrier():
    keep = cq.Workplane("XY").polyline([(-50, -50), (CHAMFER_LINE + 50, -50), (-50, CHAMFER_LINE + 50)]).close().extrude(50).translate((0, 0, -20))
    body = cyl(CX, CY, 10.9, CARRIER_Z0, CARRIER_TOP).intersect(keep).intersect(box(0, 0, CARRIER_Z0 - 1, W - 2.4, H - 2.4, CARRIER_TOP + 1))
    for (sx, sy) in switch_centres().values():
        body = body.cut(box(sx - 2.7, sy - 2.7, CARRIER_Z0 - 1, sx + 2.7, sy + 2.7, CARRIER_TOP + 1))
        for dx in (-1, 1):
            for dy in (-1, 1):
                x0 = sx + (3.1 if dx > 0 else -4.2)
                y0 = sy + (3.1 if dy > 0 else -4.2)
                body = body.union(box(x0, y0, CARRIER_Z0 - 2.0, x0 + 1.1, y0 + 1.1, CARRIER_Z0 + 0.01))
    for a in PEG_ANGLES:
        px, py = polar(PEG_R, a)
        body = body.cut(cyl(px, py, PEG_D / 2 + 0.2, CARRIER_Z0 - 3, CARRIER_TOP + 1))
    return body


def dummy_switches():
    out = None
    for (sx, sy) in switch_centres().values():
        h = box(sx - 3.0, sy - 3.0, CARRIER_Z0 - HOUSING_H, sx + 3.0, sy + 3.0, CARRIER_Z0).union(cyl(sx, sy, 1.75, CARRIER_Z0 - 0.01, BTN_REST_TOP))
        out = h if out is None else out.union(h)
    return out


def flip(solid):
    f = solid.rotate((0, 0, 0), (1, 0, 0), 180)
    bb = f.val().BoundingBox()
    return f.translate((-bb.xmin, -bb.ymin, -bb.zmin))


def build():
    os.makedirs(OUT, exist_ok=True)
    wh, pl, cm = wheel(), plate(), cam()
    export_stl(flip(wh), os.path.join(OUT, "s2_wheel_PRINT_front_down.stl"), 0.02, 0.1)
    export_stl(flip(pl), os.path.join(OUT, "s2_dial_plate_PRINT_front_down.stl"), 0.02, 0.1)
    export_stl(flip(cm), os.path.join(OUT, "s2_cam_PRINT_front_down.stl"), 0.02, 0.1)      # flipped: the front face on the bed, the ridges growing up
    export_stl(flip(carrier()), os.path.join(OUT, "s2_dial_carrier_PRINT_top_down.stl"), 0.02, 0.1)
    return wh, pl, cm


if __name__ == "__main__":
    build()
    print("dial parts built into", OUT)
