# SPDX-License-Identifier: CERN-OHL-P-2.0
"""The S2 DIAL: the wheel (hero part), its bearing plate and the cam that reads the four modes through two switches (Gray code).
Assembled coordinates (z = 0 the back, the face at z = 17), the wheel's axis at (WHEEL_CX, WHEEL_CY).
  wheel: Ø21, z 11.6 to 19.0 (2.0 proud of the face), a D-shaped axle stub (Ø3) down to z 8.4, rim grooves; printed FRONT FACE DOWN.
  plate: 1.2 mm (z 10.0 to 11.2) with the 45 degree bevel that sits on the upper shell's cone seat, a Ø3.5 bearing hole, two ears for M2 x 5 screws;
         printed front face down (bevel overhang 45 degrees at most). Cut short on the side of the chamfer wall.
  cam:   a disc pressed on the stub behind the plate (D hole), with two arc ridges on its back that press the two switches; printed back face UP.
Modes 45 degrees apart: k = 0..3 at wheel angle 45 k; switch A (at 150 degrees) pressed at k = 2, 3; switch B (at 270 degrees) pressed at k = 1, 2: 00, 01, 11, 10.
NOT DECIDED / NOT DRAWN: the switch carrier and how the ridge height is made tolerant (a tact switch bottoms out after about 0.3 mm): see mechanical-plan-S2.md section 12.
    python3 cad/s2_dial.py
"""
import math
import os
import cadquery as cq
from export_util import export_stl
from s2_lower import box, cyl
from s2_params import W, H, WHEEL_R, WHEEL_CX
import s2_upper as U

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
CX, CY = U.WHEEL_CX, U.WHEEL_CY
WHEEL_Z0, WHEEL_Z1 = 11.6, 19.0
STUB_D, STUB_FLAT, STUB_Z0 = 3.0, 0.4, 8.4          # the stub's diameter, the D flat's depth (from the axis side: the flat is at r - ...), the stub's end
WHEEL_FILLET = 1.0                                   # the face edge (a fillet on the face that lies on the bed prints fine: each layer steps out only 0.3 mm or less)
GROOVES, GROOVE_R = 24, 0.8
PLATE_Z0, PLATE_Z1, PLATE_HOLE = 10.0, 11.2, 3.5
PLATE_R_FRONT, PLATE_R_BACK = U.SEAT_R1 - 0.1, U.SEAT_R0 - 0.2      # the bevel runs 45 degrees (0.6 mm in z: radius 11.0 to 11.6 -> kept 0.1 clear of the cone)
CAM_Z0, CAM_Z1, CAM_BASE, CAM_R = 8.4, 9.8, 0.6, 7.3            # ridges 0.8 high on a 0.6 base; the cam stops 0.2 short of the plate
RIDGE_R0, RIDGE_R1 = 3.4, 7.0                                    # the cam must stay inside r 7.6: the chamfer wall passes 7.7 from the axis
SWITCH_R = 5.2                                                   # the switches' button circle
CAM_HOLE_CLEAR = 0.1
SWITCH_ANGLES = {"A": 150.0, "B": 270.0}      # 120 degrees apart: two 6 x 6 bodies at radius 5.2 do not overlap (180 / 270 degrees would)
RIDGES = {"A": (-7.5, 82.5), "B": (157.5, 247.5)}               # cam-frame angle ranges; see the docstring
CHAMFER_LINE = (W + H - 15.0) - math.sqrt(2) * U.WALL - 0.4       # x + y <= this: the plate is cut short before the chamfer wall


def d_stub(z0, z1, extra=0.0):
    """The Ø3 stub with a flat on the +x side (a D), centred on the axis."""
    s = cyl(CX, CY, STUB_D / 2 + extra, z0, z1)
    return s.cut(box(CX + STUB_D / 2 - STUB_FLAT - extra * 0 + 0.0 * 0, CY - 5, z0 - 1, CX + 5, CY + 5, z1 + 1)) if extra == 0 else s.cut(box(CX + STUB_D / 2 - STUB_FLAT + extra, CY - 5, z0 - 1, CX + 5, CY + 5, z1 + 1))


def wheel():
    w = cyl(CX, CY, WHEEL_R, WHEEL_Z0, WHEEL_Z1).faces(">Z").edges().fillet(WHEEL_FILLET)
    for i in range(GROOVES):
        a = 2 * math.pi * i / GROOVES
        w = w.cut(cyl(CX + (WHEEL_R + 0.25) * math.cos(a), CY + (WHEEL_R + 0.25) * math.sin(a), GROOVE_R, WHEEL_Z0 - 1, WHEEL_Z1 + 1))
    return w.union(d_stub(STUB_Z0, WHEEL_Z0 + 0.05))


def plate():
    z0, z1 = PLATE_Z0, PLATE_Z1
    cone = cq.Solid.makeCone(PLATE_R_BACK, PLATE_R_FRONT, z1 - (z1 - 0.6), cq.Vector(CX, CY, z1 - 0.6), cq.Vector(0, 0, 1))
    body = cq.Workplane("XY").add(cone).union(cyl(CX, CY, PLATE_R_BACK, z0, z1 - 0.6 + 0.01))
    for (bx, by) in U.EAR_BOSSES:
        ang = math.degrees(math.atan2(by - CY, bx - CX))
        arm = box(0, -2.0, z0, math.hypot(bx - CX, by - CY), 2.0, z1).rotate((0, 0, 0), (0, 0, 1), ang).translate((CX, CY, 0))
        body = body.union(arm).union(cyl(bx, by, 3.0, z0, z1))
    # cut short before the chamfer wall
    keep = cq.Workplane("XY").polyline([(-50, -50), (CHAMFER_LINE + 50, -50), (-50, CHAMFER_LINE + 50)]).close().extrude(50).translate((0, 0, -20))
    body = body.intersect(keep).intersect(box(0, 0, z0 - 1, W - 2.4, H - 2.4, z1 + 1))     # and short of the top and right walls
    body = body.cut(cyl(CX, CY, PLATE_HOLE / 2, z0 - 1, z1 + 1))
    depth = 0.9
    for (bx, by) in U.EAR_BOSSES:       # the screw: Ø2.4 through, 90 degree countersink on the back face (z = z0)
        body = body.cut(cyl(bx, by, 1.2, z0 - 1, z1 + 1))
        cs = cq.Solid.makeCone(2.1, 1.2, depth, cq.Vector(bx, by, z0), cq.Vector(0, 0, 1))
        body = body.cut(cq.Workplane("XY").add(cs))
    return body


def cam():
    c = cyl(CX, CY, CAM_R, CAM_Z1 - CAM_BASE, CAM_Z1)
    for k, (a0, a1) in RIDGES.items():
        n = 24
        pts_o = [(CX + RIDGE_R1 * math.cos(math.radians(a0 + (a1 - a0) * i / n)), CY + RIDGE_R1 * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
        pts_i = [(CX + RIDGE_R0 * math.cos(math.radians(a1 - (a1 - a0) * i / n)), CY + RIDGE_R0 * math.sin(math.radians(a1 - (a1 - a0) * i / n))) for i in range(n + 1)]
        ridge = cq.Workplane("XY").workplane(offset=CAM_Z0).polyline(pts_o + pts_i).close().extrude(CAM_Z1 - CAM_BASE - CAM_Z0 + 0.01)
        c = c.union(ridge)
    hole = d_stub(CAM_Z0 - 1, CAM_Z1 + 1, extra=CAM_HOLE_CLEAR)
    return c.cut(hole)


def flip(solid):
    f = solid.rotate((0, 0, 0), (1, 0, 0), 180)
    bb = f.val().BoundingBox()
    return f.translate((-bb.xmin, -bb.ymin, -bb.zmin))


def build():
    os.makedirs(OUT, exist_ok=True)
    wh, pl, cm = wheel(), plate(), cam()
    export_stl(flip(wh), os.path.join(OUT, "s2_wheel_PRINT_front_down.stl"), 0.02, 0.1)
    export_stl(flip(pl), os.path.join(OUT, "s2_dial_plate_PRINT_front_down.stl"), 0.02, 0.1)
    export_stl(flip(cm), os.path.join(OUT, "s2_cam_PRINT_back_up.stl"), 0.02, 0.1)      # flipped: the base on the bed, the ridges growing up
    return wh, pl, cm


if __name__ == "__main__":
    wh, pl, cm = build()
    print("dial parts built into", OUT)
