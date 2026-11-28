# SPDX-License-Identifier: CERN-OHL-P-2.0
"""The S2 PUSH-TO-TALK KEY on the left edge (owner, 2026-11-28: shortened from 46 mm to what fits below the Super Mini).

A slanted block (it sticks out 5 mm at its top, 3.2 mm near its bottom, as the owner's 5 mm mock-up block) that passes through a window
in the left wall of both shells (the window crosses the seam at y = 52). It turns on a Ø1.75 filament pin along z near its bottom end
(the pin sits in a blind hole in a small boss on the back plate and a blind hole in the frame's floor), so pressing the top moves it inward.
Two tact switches (6 x 6 x 4.3) on 2 mm foam, on brackets that stand up from the back plate, read it:
  * S1, high up (28 mm from the pin): touches the key at rest (0.05 mm of preload, so the key does not rattle) and clicks after about
    0.2 mm at the key's top: the soft first stage (hold to talk);
  * S2, lower (13.4 mm from the pin): clicks at about 1.0 mm at the key's top: the second stage (the latch);
  * a stop post on the back plate ends the travel at 1.3 mm; the foam behind both switches takes what is left (S1's foam about 0.9 mm).
At rest the key is held out by S1 against a lip along its inner face (the lip bears on the wall's inner face above the window).
Printed lying on its BACK face (z low on the bed): the lip is on the front side, so nothing overhangs; the outer fillets on the bed side step
out 0.3 mm a layer at most. All sizes of the switches are typical (6 x 6 x 4.3 with a 0.8 mm button), not measured.
    python3 cad/s2_key.py
"""
import math
import os
import cadquery as cq
from export_util import export_stl
from s2_lower import box, cyl
from s2_params import WALL

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
# the window in the left wall (both shells)
WIN_Y0, WIN_Y1 = 25.0, 60.5          # the side boss below (y 22) and the board's stop wall above (y 60.7) bound it
WIN_Z0, WIN_Z1 = 3.0, 12.2           # the back plate (1.8) and the frame's floor (13.0) bound it
WIN_R = 1.5                          # its corners, in the y-z plane
GAP_Z, GAP_Y0, GAP_Y1 = 0.25, 0.3, 0.35
KY0, KY1 = WIN_Y0 + GAP_Y0, WIN_Y1 - GAP_Y1       # 25.3 to 60.15
KZ0, KZ1 = WIN_Z0 + GAP_Z, WIN_Z1 - GAP_Z         # 3.25 to 11.95
PROTRUDE, TIP_FROM_TOP, LOW_FRAC = 5.0, 4.5, 0.64  # the mock-up's slant: 5 mm out 4.5 mm below the top, 3.2 mm out near the bottom
X_IN = 3.6                           # the key's inner face (the wall's inner face is at 1.6)
PIN = (3.2, 27.6)                    # the pivot, a Ø1.75 filament pin along z
PIN_HOLE_KEY = 2.1                   # free in the key (small horizontal holes print small)
PIN_HOLE_FIXED = 2.0                 # blind holes in the plate's boss and the frame's floor: snug
PIVOT_X1, PIVOT_Y1 = 5.0, 30.6       # the key is thicker round the pin
LIP_Y0, LIP_Z1 = 33.0, 12.8          # the lip on the inner face's front edge: y 33 to the top, z up to 12.8 (the frame's floor is at 13.0)
# the switches: housing 6 x 6 x 3.5 plus a 0.8 button (Ø3.5); foam 2 mm between the housing and the bracket
SW_W, SW_HOUSING, SW_BTN, SW_BTN_D, FOAM = 6.0, 3.5, 0.8, 3.5, 2.0
SW_Z = 7.2                           # the switches' centre in depth (clear of the cap's peg head at z 10.7)
S1_Y, S1_GAP = 55.5, -0.05           # negative gap = preload
S2_Y, S2_GAP = 41.0, 0.22
ACTUATE = 0.25                       # a tact switch's typical travel to the click
STOP_TRAVEL = 1.3                    # at the key's tip
BRACKET_T = 2.0
STOP_Y = (58.6, 60.2)


def tip_y():
    return KY1 - TIP_FROM_TOP


def bracket_face_x(gap):
    return X_IN + gap + SW_BTN + SW_HOUSING + FOAM


def key():
    """The key in its rest position (assembled coordinates)."""
    p = PROTRUDE
    pts = [(0.0, KY1), (-p, tip_y()), (-LOW_FRAC * p, KY0 + 2.0), (0.0, KY0)]
    outer = cq.Workplane("XY").workplane(offset=KZ0).polyline(pts).close().extrude(KZ1 - KZ0)
    outer = outer.edges("|Z").edges(cq.selectors.BoxSelector((-p - 1, KY0 - 1, KZ0 - 1), (-0.5, KY1 + 1, KZ1 + 1))).fillet(1.2)
    body = outer.union(box(-0.01, KY0, KZ0, X_IN, KY1, KZ1))
    body = body.union(box(X_IN - 0.01, KY0, KZ0, PIVOT_X1, PIVOT_Y1, KZ1))
    # the round on the outer part: every edge of the protruding faces (x < 0)
    sel = cq.selectors.BoxSelector((-p - 1, KY0 - 1, KZ0 - 0.01), (-0.3, KY1 + 1, KZ0 + 0.01))
    sel2 = cq.selectors.BoxSelector((-p - 1, KY0 - 1, KZ1 - 0.01), (-0.3, KY1 + 1, KZ1 + 0.01))
    for s in (sel, sel2):
        for r in (2.0, 1.8, 1.5, 1.2):
            try:
                body = body.edges(s).fillet(r)
                break
            except Exception:
                continue
    # the window's corners are rounded (r 1.5 in y-z): round the key's section to match (r 1.25, 0.25 clear)
    sect = (cq.Workplane("YZ").workplane(offset=-PROTRUDE - 1).center((KY0 + KY1) / 2, (KZ0 + KZ1) / 2)
            .rect(KY1 - KY0, KZ1 - KZ0).extrude(PIVOT_X1 + PROTRUDE + 2).edges("|X").fillet(WIN_R - GAP_Z))
    body = body.intersect(sect)
    body = body.union(box(WALL + 0.05, LIP_Y0, KZ1 - 0.01, X_IN, KY1 - 1.5, LIP_Z1))   # the lip (bears on the wall above the window), short of the rounded top end
    body = body.cut(cyl(PIN[0], PIN[1], PIN_HOLE_KEY / 2, KZ0 - 1, KZ1 + 1))
    return body


def rotate_pressed(solid, travel_at_tip):
    """The key turned about its pin so that its tip has moved inward by travel_at_tip."""
    d = tip_y() - PIN[1]
    ang = -math.degrees(travel_at_tip / d)          # clockwise seen from the front: the top moves toward +x
    return solid.rotate((PIN[0], PIN[1], 0), (PIN[0], PIN[1], 1), ang)


def switch(y, gap):
    """A dummy tact switch whose button faces the key (-x), with its foam behind it."""
    xb = X_IN + gap
    btn = cq.Workplane("YZ").workplane(offset=xb).center(y, SW_Z).circle(SW_BTN_D / 2).extrude(SW_BTN + 0.01)
    house = box(xb + SW_BTN, y - SW_W / 2, SW_Z - SW_W / 2, xb + SW_BTN + SW_HOUSING, y + SW_W / 2, SW_Z + SW_W / 2)
    foam = box(xb + SW_BTN + SW_HOUSING, y - SW_W / 2, SW_Z - SW_W / 2, bracket_face_x(gap), y + SW_W / 2, SW_Z + SW_W / 2)
    return btn.union(house), foam


def actuation_travel(y, gap):
    """Travel at the key's tip at which the switch at y clicks."""
    return (gap + ACTUATE) * (tip_y() - PIN[1]) / (y - PIN[1])


def window_cut(y0, y1):
    """The window through the left wall, limited to y0..y1 (each shell cuts its own part)."""
    w = (cq.Workplane("YZ").workplane(offset=-0.5).center((WIN_Y0 + WIN_Y1) / 2, (WIN_Z0 + WIN_Z1) / 2)
         .rect(WIN_Y1 - WIN_Y0, WIN_Z1 - WIN_Z0).extrude(WALL + 1.0).edges("|X").fillet(WIN_R))
    return w.intersect(box(-1, y0, 0, WALL + 1, y1, 20))


def to_print(k):
    bb = k.val().BoundingBox()
    return k.translate((-bb.xmin, -bb.ymin, -bb.zmin))       # as modelled: the back face (z = KZ0) on the bed


def build():
    os.makedirs(OUT, exist_ok=True)
    k = key()
    export_stl(to_print(k), os.path.join(OUT, "s2_key_PRINT_back_down.stl"), 0.02, 0.1)
    return k


if __name__ == "__main__":
    k = build()
    bb = k.val().BoundingBox()
    print("key built: %.1f x %.1f x %.1f mm" % (bb.xlen, bb.ylen, bb.zlen))
    for n, (y, g) in (("S1", (S1_Y, S1_GAP)), ("S2", (S2_Y, S2_GAP))):
        print("  %s at y %.1f: clicks at %.2f mm of travel at the key's tip" % (n, y, actuation_travel(y, g)))
    print("  stop at %.2f mm; S1 foam takes %.2f mm, S2 foam %.2f mm" % (STOP_TRAVEL,
          STOP_TRAVEL * (S1_Y - PIN[1]) / (tip_y() - PIN[1]) - (S1_GAP + ACTUATE),
          STOP_TRAVEL * (S2_Y - PIN[1]) / (tip_y() - PIN[1]) - (S2_GAP + ACTUATE)))
