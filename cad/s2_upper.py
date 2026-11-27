# SPDX-License-Identifier: CERN-OHL-P-2.0
"""The S2 UPPER SHELL (control zone, y 52 to 88): designed to be printed FRONT FACE DOWN with NO SUPPORTS.

Everything hangs from the front wall and grows toward the back: the walls, the wheel's tube, the board's stop wall and corner pillars, the
screw bosses, the alignment slots. Overhangs are kept to 45 degrees at most (a 45 degree seat for the dial module, a pentagon-shaped
USB-C opening, ceilings of 3 mm at most). Coordinates are the ASSEMBLED ones (z = 0 the back, the front face at z = 17); the exported file is flipped.

TENTATIVE: the board pocket is sized for an ESP32-S3 Super Mini (23.5 x 18 mm from a web listing; thickness and button places not published), the USB opening
for a typical plug. The dial module (plate, cam, switches), the key's window and the stand are NOT in this file yet.
    python3 cad/s2_upper.py
"""
import math
import os
import cadquery as cq
from export_util import export_stl
from s2_lower import box, cyl
from s2_params import W, H, D, WALL, CHAMFER, R_CORNER, SEAM_Y, WHEEL_R, POCKET_GAP, WHEEL_CX
import s2_frame as F

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
Z_BACK, Z_FRONT = F.BACK_Z, D
FRONT_T = 1.8
Z_FW = Z_FRONT - FRONT_T                # the inner face of the front wall, 15.2
Y0, Y1 = SEAM_Y, H                      # 52 and 88
END_T = 4.0                             # the lower end wall, thick enough to hold the alignment slots
PTS = [(0.0, Y0), (W, Y0), (W, H - CHAMFER), (W - CHAMFER, H), (0.0, H)]
WHEEL_CY = H - 13.0                     # 75
BORE_R = WHEEL_R + POCKET_GAP           # 11.1: the wheel's hole (0.6 mm gap)
SEAT_Z0, SEAT_Z1, SEAT_R0, SEAT_R1 = 10.6, 11.2, 11.7, BORE_R     # the dial module's 45 degree seat (a cone), wheel side up
TUBE_R = 12.7
# the board pocket (an ESP32-S3 Super Mini: 23.5 x 18 mm from a web listing; thickness and the buttons' places are NOT published: tentative)
BD_X0, BD_X1, BD_Y1 = 2.0, 20.0, 85.4   # board outline: x, and the top edge (1 mm under the top wall)
BD_LEN = 23.5                            # espboards.dev lists 23.5 x 18 mm (another listing says 22.52): the longer one is used
BD_Y0 = BD_Y1 - BD_LEN
BD_PCB_T, BD_COMP_H = 1.2, 3.3          # pcb 1.0 to 1.2 plus the USB-C about 3.2 to 3.3: about 4.5 mm in all (owner's estimate, matches a C3 Super Mini listing)
BD_Z_PCB = (10.1, 11.3)                 # the pcb's back and front face: the components face the BACK, so the plug's axis (1.6 above the pcb) sits at z 8.5, mid depth,
                                        # and BOOT / RESET can be pressed through the back plate
USB_X = (BD_X0 + BD_X1) / 2             # the connector's centre
USB_ZC = 8.5                            # its centre in depth
BOSSES_UP = ((16.0, 59.0), (44.4, 56.0))                         # back-plate screws (M2 self-tapping into the pilots)
EAR_BOSSES = ((WHEEL_CX - 8.0, 60.5), (WHEEL_CX + 8.0, 60.5))     # the dial module's two screws, drawing it onto its seat (M2 x 5)
EAR_BOSS_Z = 11.5                       # the boss ends 0.3 mm IN FRONT of the plate's front face (11.2): the seat, not the screws, sets the position
TABS_X = (10.0, W - 10.0)               # the lower frame's alignment tabs (z 6 to 8.4, y 52 to 55)


def prism(z0, z1):
    s = cq.Workplane("XY").workplane(offset=z0).polyline(PTS).close().extrude(z1 - z0)
    s = s.edges("|Z").edges(cq.selectors.BoxSelector((-1, H - 1, z0 - 1), (1, H + 1, z1 + 1))).fillet(R_CORNER)
    for (x, y) in ((W, H - CHAMFER), (W - CHAMFER, H)):
        s = s.edges("|Z").edges(cq.selectors.BoxSelector((x - .5, y - .5, z0 - 1), (x + .5, y + .5, z1 + 1))).fillet(3.0)
    return s


FRONT_FILLET = 1.5                      # the front perimeter, like the cap's (spec: front fillet 1.5); not along the seam edge, which stays flush with the cap


def outer_solid():
    """The outline prism with the front perimeter rounded. The prism is built 3 mm too long at the seam so that the side fillets run out to
    the seam; the extra is cut off afterwards, which leaves the seam edge itself sharp (the cap's top edge is sharp too)."""
    pts = [(0.0, Y0 - 3.0), (W, Y0 - 3.0), (W, H - CHAMFER), (W - CHAMFER, H), (0.0, H)]
    s = cq.Workplane("XY").workplane(offset=Z_BACK).polyline(pts).close().extrude(Z_FRONT - Z_BACK)
    s = s.edges("|Z").edges(cq.selectors.BoxSelector((-1, H - 1, Z_BACK - 1), (1, H + 1, Z_FRONT + 1))).fillet(R_CORNER)
    for (x, y) in ((W, H - CHAMFER), (W - CHAMFER, H)):
        s = s.edges("|Z").edges(cq.selectors.BoxSelector((x - .5, y - .5, Z_BACK - 1), (x + .5, y + .5, Z_FRONT + 1))).fillet(3.0)
    s = s.faces(">Z").edges().fillet(FRONT_FILLET)
    return s.intersect(box(-1, Y0, Z_BACK - 1, W + 1, H + 1, Z_FRONT + 1))


def inset_prism(z0, z1, inset):
    outer = prism(z0, z1)
    w = outer.faces("<Z").val().outerWire()
    return cq.Workplane("XY").workplane(offset=z0).add(w).toPending().offset2D(-inset).extrude(z1 - z0)


def poly_xz(pts, y0, y1):
    """A prism along y from a polygon in (x, z)."""
    return cq.Workplane("XZ").workplane(offset=-y1).polyline(pts).close().extrude(y1 - y0)


def upper(with_pilots=True):
    shell = outer_solid()
    cavity = inset_prism(Z_BACK - 0.1, Z_FW, WALL).intersect(box(-1, Y0 + END_T, Z_BACK - 1, W + 1, H + 1, Z_FW + 1))
    # the cavity's top-left corner is rounded (inner radius 3.4): the board's square corner needs a little relief, leaving a 1 mm skin
    cavity = cavity.union(cyl(R_CORNER, H - R_CORNER, R_CORNER - 1.0, Z_BACK - 0.1, Z_FW).intersect(box(0, H - R_CORNER, 0, R_CORNER, H, 20)))
    s = shell.cut(cavity)
    keep = prism(Z_BACK, Z_FRONT)
    # the wheel's tube, with its seat and the wheel's hole
    tube = cyl(WHEEL_CX, WHEEL_CY, TUBE_R, SEAT_Z0, Z_FW + 0.05).intersect(keep)
    s = s.union(tube)
    s = s.cut(cyl(WHEEL_CX, WHEEL_CY, BORE_R, SEAT_Z1, Z_FRONT + 0.1))
    cone = cq.Solid.makeCone(SEAT_R0, SEAT_R1, SEAT_Z1 - SEAT_Z0, cq.Vector(WHEEL_CX, WHEEL_CY, SEAT_Z0), cq.Vector(0, 0, 1))
    inside = inset_prism(Z_BACK - 0.1, Z_FW, WALL)           # the seat is cut only where the cavity is (not into the chamfer wall: the plate is cut short there)
    s = s.cut(cq.Workplane("XY").add(cone).intersect(inside))
    # notches in the tube's end for the module plate's two ears (only the free end of a wall: no overhang)
    for (bx, by) in EAR_BOSSES:
        ang = math.degrees(math.atan2(by - WHEEL_CY, bx - WHEEL_CX))
        notch = box(0.0, -2.3, SEAT_Z0 - 0.1, TUBE_R + 1.0, 2.3, SEAT_Z1 + 0.25).rotate((0, 0, 0), (0, 0, 1), ang).translate((WHEEL_CX, WHEEL_CY, 0))
        s = s.cut(notch.intersect(inside).intersect(cyl(WHEEL_CX, WHEEL_CY, TUBE_R + 1.0, 0, 20).cut(cyl(WHEEL_CX, WHEEL_CY, SEAT_R1 - 0.05, -1, 20))))
    # the board: a stop wall at the bottom (it takes the plug's push), four pillars on the pcb's front face
    s = s.union(box(BD_X0 - 0.2, BD_Y0 - 1.2, 5.0, BD_X1 + 0.2, BD_Y0, Z_FW + 0.05))
    for px in (BD_X0, BD_X1 - 1.4):
        for py in (BD_Y0, BD_Y1 - 1.4):
            s = s.union(box(px, py, BD_Z_PCB[1], px + 1.4, py + 1.4, Z_FW + 0.05))
    # two little hooks on the left wall that overhang the pcb's back face by 0.8 mm (0.1 mm clear): the board goes in from the back at a slant and drops flat
    for hy in (BD_Y0 + 5.0, BD_Y1 - 9.0):
        s = s.union(box(WALL - 0.05, hy, BD_Z_PCB[0] - 0.6, BD_X0 + 0.8, hy + 4.0, BD_Z_PCB[0] - 0.1))
    # the USB-C opening in the top wall: a pentagon (width 13, 6.8 deep), the ceiling flat 6 mm wide, flanks at 45 degrees
    zt, zb, hw, ch = USB_ZC - 3.4, USB_ZC + 3.4, 6.5, 3.4      # zt the back side (the print's ceiling), zb the front side
    pts = [(USB_X - hw, zb), (USB_X + hw, zb), (USB_X + hw, zt + ch), (USB_X + hw - ch, zt), (USB_X - hw + ch, zt), (USB_X - hw, zt + ch)]
    s = s.cut(poly_xz(pts, H - WALL - 0.1, H + 0.1))
    # alignment slots for the lower frame's tabs (blind, 2.8 wide: a 3 mm bridge)
    for tx in TABS_X:
        s = s.cut(box(tx - 1.4, Y0 - 0.1, 5.8, tx + 1.4, Y0 + 3.3, 8.6))
    # the wire slot through the end wall: a triangle (45 degree flanks, no bridge): base 12 wide at z = 11, apex at z = 5
    s = s.cut(poly_xz([(18.0, 11.0), (30.0, 11.0), (24.0, 5.0)], Y0 - 0.1, Y0 + END_T + 0.1))
    # screw bosses, hanging from the front wall; pilots open to the back
    for (bx, by) in BOSSES_UP:
        s = s.union(cyl(bx, by, F.BOSS_OD / 2, Z_BACK, Z_FW + 0.05))
        if with_pilots:
            s = s.cut(cyl(bx, by, F.PILOT_D / 2, Z_BACK - 0.1, Z_BACK + F.PILOT_DEPTH))
    for (bx, by) in EAR_BOSSES:
        s = s.union(cyl(bx, by, F.BOSS_OD / 2, EAR_BOSS_Z, Z_FW + 0.05))
        s = s.cut(cyl(bx, by, F.PILOT_D / 2, EAR_BOSS_Z - 0.1, EAR_BOSS_Z + 3.7))     # pilot 3.8 deep: M2 x 5 reaches 3.5 mm into the boss, the front wall stays whole
    return s


def build():
    os.makedirs(OUT, exist_ok=True)
    u = upper()
    export_stl(F.to_print(u), os.path.join(OUT, "s2_upper_PRINT_front_down.stl"), 0.02, 0.1)
    return u


if __name__ == "__main__":
    u = build()
    bb = u.val().BoundingBox()
    print("S2 upper shell built into", OUT, [round(v, 1) for v in (bb.xlen, bb.ylen, bb.zlen)])
