# SPDX-License-Identifier: CERN-OHL-P-2.0
"""The S2 REAR STAND, v3 (2026-11-28): one flat FLAP, flush with the back, that swings out from a hinge near the seam.

The owner found the U-shaped stand ugly and asked for an industrial-design look (Teenage Engineering, Nothing). The flap is a plain
rounded panel (25 x 43.5 mm) set into the back plate with a 0.3 mm split line: closed, the back reads as one plate with an inset panel;
printed in the cap's deeper tone it echoes the front. It is pulled out by a fingernail at the bottom edge (a scoop in the plate and a groove
in the flap's foot) and swings out to a HARD STOP: a short tail above the hinge axis turns into a pocket that ends exactly where the
stand should stop, so the body leans back about 25 degrees on its bottom edge and the flap's foot.
The hinge is a Ø1.75 filament pin along x (the maker's trick: snug in the plate, a light friction in the flap, so it stays where it is put).
Printed with its OUTER face down: the pin hole is a small horizontal hole.
Assembled coordinates: z = 0 the back surface, y up the body.
    python3 cad/s2_stand.py
"""
import math
import os
import cadquery as cq
from export_util import export_stl
from s2_lower import box, cyl

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
X0, X1 = 11.5, 36.5                  # the flap's width (centred on the body)
Y_FOOT = 3.0                         # its bottom edge
Y_P, Z_P = 46.5, 1.8                 # the hinge axis (along x)
T = 2 * Z_P                          # 3.6: the flap's thickness, z 0 to 3.6; its top is a half round about the axis
TAIL = 2.2                           # the tail above the axis on the inner side: it sets the stop
FOOT_R = 4.0                         # the foot's corners
GAP = 0.3                            # round the flap, in the plate's pocket
PIN_D = 1.75
HOLE_FLAP = 2.1                      # a light friction on the pin (small horizontal holes print about 0.3 small)
HOLE_PLATE = 2.0                     # snug
NAIL = (18.5, 29.5, 1.0, 2.4, 1.0)   # the nail groove in the foot's end face: x0, x1, z0, z1, depth
THETA = math.radians(25.0)           # the body's lean from the vertical, when standing
POCKET_DEPTH = T + GAP + 0.2         # 4.1: the floor is a 26 mm bridge when the plate prints face down; 0.2 mm more for its sag
PAD = (10.2, 2.8, 37.8, 50.0)        # the plate is thickened inward here (x0, y0, x1, y1; y0 leaves room for the plate's 1 mm slide past the frame's wall) ...
PAD_Z1 = 5.3                         # ... up to z 5.3, so that the pocket keeps a 1.2 mm floor
PAD_TAIL = (44.0, 50.0, 5.9)         # ... and to z 5.9 at the hinge, where the tail's pocket goes deeper


def profile_pts(n=12):
    """The flap's side profile (y, z): the panel, the half round over the axis on the outer side, and the tail on the inner side."""
    pts = [(Y_FOOT, 0.0)]
    for i in range(n + 1):                                          # the outer quarter round, from the outer face up to the axis height
        a = -math.pi / 2 + (math.pi / 2) * i / n
        pts.append((Y_P + Z_P * math.cos(a), Z_P + Z_P * math.sin(a)))
    pts += [(Y_P + TAIL, Z_P), (Y_P + TAIL, T), (Y_FOOT, T)]
    return pts


def flap_raw():
    prof = cq.Workplane("YZ").workplane(offset=X0).polyline(profile_pts()).close().extrude(X1 - X0)
    for x in (X0, X1):
        prof = prof.edges("|Z").edges(cq.selectors.BoxSelector((x - .1, Y_FOOT - .1, -1), (x + .1, Y_FOOT + .1, T + 1))).fillet(FOOT_R)
    return prof


def flap():
    f = flap_raw()
    f = f.cut(box(NAIL[0], Y_FOOT - 0.1, NAIL[2], NAIL[1], Y_FOOT + NAIL[4], NAIL[3]))
    f = f.cut(cq.Workplane("YZ").workplane(offset=X0 - 1).center(Y_P, Z_P).circle(HOLE_FLAP / 2).extrude(X1 - X0 + 2))
    return f


def open_flap(solid, psi_deg):
    """The flap opened by psi (its foot swings out, toward -z)."""
    return solid.rotate((0, Y_P, Z_P), (1, Y_P, Z_P), psi_deg)


def foot_height(psi_deg, theta=THETA):
    """The lowest foot corner's height above the desk, the body leaning theta back on its back-bottom edge (y = z = 0)."""
    psi = math.radians(psi_deg)
    h = []
    for zc in (0.0, T):
        dy, dz = Y_FOOT - Y_P, zc - Z_P
        y = Y_P + dy * math.cos(psi) - dz * math.sin(psi)
        z = Z_P + dy * math.sin(psi) + dz * math.cos(psi)
        h.append(y * math.cos(theta) + z * math.sin(theta))
    return min(h)


def needed_open_angle(theta=THETA):
    """The opening at which the foot rests on the desk FAR behind the body (the larger of the two solutions; the smaller one
    puts the foot only about 9 mm behind the body's edge, where it would tip over)."""
    last = None
    for k in range(0, 900):
        if foot_height(k / 10.0, theta) < 0 <= foot_height((k + 1) / 10.0, theta):
            last = (k + 1) / 10.0
    return last


def foot_distance(psi_deg, theta=THETA):
    """How far behind the body's resting edge the foot touches (the body's balance point is about 11 mm behind it)."""
    psi = math.radians(psi_deg)
    dy, dz = Y_FOOT - Y_P, -Z_P
    y = Y_P + dy * math.cos(psi) - dz * math.sin(psi)
    z = Z_P + dy * math.sin(psi) + dz * math.cos(psi)
    return -(z * math.cos(theta) - y * math.sin(theta))


STOP_DEG = None   # filled in below


def swept_cut(psi_end, step=2.0):
    """The pocket at the hinge: the flap's upper end turned through 0..psi_end, grown by the gap, across the flap's width."""
    pts = [p for p in profile_pts() if p[0] > Y_P - 8.0] + [(Y_P - 8.0, T), (Y_P - 8.0, 0.0)]
    pts = [pts[-1]] + pts[:-1]
    region = None
    a = 0.0
    while True:
        ang = math.radians(min(a, psi_end))
        rp = []
        for (y, z) in pts:
            dy, dz = y - Y_P, z - Z_P
            rp.append((Y_P + dy * math.cos(ang) - dz * math.sin(ang), Z_P + dy * math.sin(ang) + dz * math.cos(ang)))
        piece = cq.Workplane("YZ").workplane(offset=X0 - GAP).polyline(rp).close().offset2D(GAP).extrude(X1 - X0 + 2 * GAP)
        region = piece if region is None else region.union(piece)
        if a >= psi_end:
            break
        a += step
    return region


def build():
    os.makedirs(OUT, exist_ok=True)
    f = flap()
    export_stl(f, os.path.join(OUT, "s2_stand_PRINT_outer_face_down.stl"), 0.02, 0.1)
    return f


if __name__ == "__main__":
    build()
    psi = needed_open_angle()
    print("flap stand built: %.0f x %.1f x %.1f mm; it must open %.1f deg for a lean of %.0f deg; foot %.1f mm behind the edge" % (
        X1 - X0, Y_P + Z_P - Y_FOOT, T, psi, math.degrees(THETA), foot_distance(psi)))
