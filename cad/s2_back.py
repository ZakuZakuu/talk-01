# SPDX-License-Identifier: CERN-OHL-P-2.0
"""The S2 BACK PLATE, v3 (2026-11-28): a flat plate (1.8 mm) that closes the lower frame and the upper shell.
Printed FLAT with its outer face DOWN on the bed: everything on the inside grows upward from it; the visible face is the smooth bed face.

What is on it (assembled coordinates, z = 0 the back surface):
  * SIX M2 countersunk self-tapping screws in a symmetric pattern (four in the lower frame, two in the upper shell at y 59) and, at the top
    edge, TWO HOOKS that catch in slots in the upper shell's top wall: the plate goes on top first, then swings down onto the screws;
  * the FLAP STAND's pocket (with its hinge pocket, which sets the stop), a pad that thickens the plate behind it, the hinge pin's hole,
    and a fingernail scoop at the bottom edge;
  * the DEBUG HATCH over the Super Mini: an opening for BOOT, RESET and the board's pads, closed by a flush lid (s2_hatch.py) with two
    hooks at its top and an in-plane latch at its bottom; a nail scoop under it;
  * for the KEY: the pin's boss, the stop post and the two switch brackets (each with side walls that guide the switch and its foam);
  * engraved lettering, read from behind.
    python3 cad/s2_back.py
"""
import os
import cadquery as cq
from export_util import export_stl, text_solid
from s2_lower import box, cyl
from s2_params import W, H
import s2_frame as F
import s2_upper as U
import s2_stand as S
import s2_key as K
import s2_graphics as G

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
T = F.BACK_Z                           # 1.8
CLEAR_D, CSINK_D = 2.4, 4.2            # the through hole and the 90 degree countersink (M2 flat head about 3.8 to 4.0: to be measured)
EDGE_R = 1.7                           # the outer edge's round (on the bed side when printed: it steps out 0.3 mm a layer at most)
HOLES = tuple(F.BOSSES) + tuple(U.BOSSES_UP)
# the top hooks (into U's slots in the top wall)
HOOK_Y0, HOOK_LIP = H - 3.1, (2.4, 3.2)          # the hook's inner face is 0.1 clear of the wall (86.4); its lip reaches 0.7 into the slot
# the debug hatch
HATCH = (4.5, 64.0, 17.5, 83.0)        # x0, y0, x1, y1 of the opening (over the Super Mini: x 2 to 20, y 61.9 to 85.4)
HATCH_R = 1.5
LATCH_GROOVE = (13.0, 15.5, 0.4, 1.6, 0.6)       # in the opening's bottom wall: x0, x1, z0, z1, depth
# the stop angle: the hinge pocket is swept to this angle; with the 0.3 mm gap the flap stops a little later (checked in check_s2_back.py)
SWEEP_END = 28.6
LETTERING = (("talk.01", 3.4), ("USB-C MIC", 2.0))
SLIDE_ON = 1.0                         # assembly: the plate is laid on 1 mm low, then pushed up so the top hooks enter their slots


def outline():
    s = cq.Workplane("XY").polyline([(0, 0), (W, 0), (W, H - 15.0), (W - 15.0, H), (0, H)]).close().extrude(T)
    for (x, y, r) in ((0, 0, 5.0), (W, 0, 5.0), (0, H, 5.0), (W, H - 15.0, 3.0), (W - 15.0, H, 3.0)):
        s = s.edges("|Z").edges(cq.selectors.BoxSelector((x - .5, y - .5, -1), (x + .5, y + .5, T + 1))).fillet(r)
    return s


def rrect(x0, y0, x1, y1, r, z0, z1):
    return cq.Workplane("XY").workplane(offset=z0).center((x0 + x1) / 2, (y0 + y1) / 2).rect(x1 - x0, y1 - y0).extrude(z1 - z0).edges("|Z").fillet(r)


def switch_bracket(y, gap):
    face = K.bracket_face_x(gap)
    z1 = K.SW_Z + K.SW_W / 2 + 0.1
    b = box(face, y - 4.0, T - 0.01, face + K.BRACKET_T, y + 4.0, z1)
    for sgn in (-1, 1):                                   # side walls round the foam and the back of the housing (0.15 mm clear)
        y0 = y + sgn * (K.SW_W / 2 + 0.15)
        b = b.union(box(face - 2.5, min(y0, y0 + sgn * 0.9), T - 0.01, face + 0.01, max(y0, y0 + sgn * 0.9), z1))
    return b


def lettering():
    """The two lines, engraved 0.3 mm, mirrored so they read correctly from behind; placed in the upper right of the back."""
    out = None
    y = 72.0
    for (txt, size) in LETTERING:
        t = text_solid(txt, size, 0, 0, -0.1, 0.4, mirror=True)
        bb = t.val().BoundingBox()
        t = t.translate((W - 6.0 - bb.xmax, y, 0))      # seen from behind, the right edge of the text is at x = W - 6 ... flush left as seen
        out = t if out is None else out.union(t)
        y -= size + 1.8
    return out


def back(sweep_end=SWEEP_END):
    s = outline()
    s = s.faces("<Z").edges().fillet(EDGE_R)
    depth = (CSINK_D - CLEAR_D) / 2
    for (x, y) in HOLES:
        s = s.cut(cyl(x, y, CLEAR_D / 2, -0.1, T + 0.1))
        cone = cq.Solid.makeCone(CSINK_D / 2, CLEAR_D / 2, depth, cq.Vector(x, y, 0.0), cq.Vector(0, 0, 1))
        s = s.cut(cq.Workplane("XY").add(cone))
        s = s.cut(cyl(x, y, CSINK_D / 2, -0.1, 0.0))
    # the top hooks
    for hx in U.TOP_HOOKS_X:
        s = s.union(box(hx, HOOK_Y0, T - 0.01, hx + U.HOOK_W, H - 1.7, HOOK_LIP[1]))
        s = s.union(box(hx, H - 1.75, HOOK_LIP[0], hx + U.HOOK_W, H - 0.9, HOOK_LIP[1]))
    # the key: the pin's boss, the stop post, the two switch brackets
    s = s.union(cyl(K.PIN[0], K.PIN[1], 1.4, T - 0.01, K.KZ0 - 0.25))
    # the pin's hole is a short slot (1.2 mm up): the plate goes on 1 mm low and slides up into its top hooks, past the pin already in place
    s = s.cut(cq.Workplane("XY").workplane(offset=0.6).center(K.PIN[0], K.PIN[1] + SLIDE_ON / 2 + 0.1).slot2D(K.PIN_HOLE_FIXED + SLIDE_ON + 0.2, K.PIN_HOLE_FIXED, 90).extrude(K.KZ0))
    stop_y = (K.STOP_Y[0] + K.STOP_Y[1]) / 2
    stop_x = K.X_IN + K.STOP_TRAVEL * (stop_y - K.PIN[1]) / (K.tip_y() - K.PIN[1])
    s = s.union(box(stop_x, K.STOP_Y[0], T - 0.01, stop_x + 1.2, K.STOP_Y[1], 4.0))     # low: it passes under the upper switch while the plate slides on
    for (y, g) in ((K.S1_Y, K.S1_GAP), (K.S2_Y, K.S2_GAP)):
        s = s.union(switch_bracket(y, g))
    # the flap stand: the pad, the pocket (the closed flap's outline plus the hinge pocket swept to the stop), the pin's hole, the scoop
    s = s.union(box(S.PAD[0], S.PAD[1], T - 0.01, S.PAD[2], S.PAD[3], S.PAD_Z1))
    s = s.union(box(S.PAD[0], S.PAD_TAIL[0], T - 0.01, S.PAD[2], S.PAD_TAIL[1], S.PAD_TAIL[2]))
    wire = S.flap_raw().faces("<Z").val().outerWire()
    pocket = cq.Workplane("XY").add(wire).toPending().offset2D(S.GAP).extrude(S.POCKET_DEPTH + 0.1).translate((0, 0, -0.1))
    s = s.cut(pocket).cut(S.swept_cut(sweep_end))
    s = s.cut(cq.Workplane("YZ").workplane(offset=S.PAD[0] - 0.1).center(S.Y_P, S.Z_P).circle(S.HOLE_PLATE / 2).extrude(S.X1 + S.GAP + 0.6 - S.PAD[0] + 0.1))
    s = s.cut(cq.Workplane("XY").workplane(offset=-0.1).center((S.X0 + S.X1) / 2, 0.0).slot2D(12.0, 2 * (S.Y_FOOT + S.GAP), 0).extrude(S.POCKET_DEPTH + 0.1))
    # the debug hatch: the opening, the latch's groove in its bottom wall, a nail scoop under it
    hx0, hy0, hx1, hy1 = HATCH
    s = s.cut(rrect(hx0, hy0, hx1, hy1, HATCH_R, -0.1, T + 0.1))
    g = LATCH_GROOVE
    s = s.cut(box(g[0], hy0 - g[4], g[2], g[1], hy0 + 0.1, g[3]))
    s = s.cut(cq.Workplane("XY").workplane(offset=-0.1).center(8.5, hy0).slot2D(5.0, 3.0, 0).extrude(0.9))
    # the lettering
    s = s.cut(G.back_ink(extra=0.1))     # v4: the graphics layer (s2_graphics.py)
    return s


def to_print(s):
    return s        # printed as modelled: the outer face (z = 0) on the bed


def build():
    os.makedirs(OUT, exist_ok=True)
    b = back()
    export_stl(to_print(b), os.path.join(OUT, "s2_back_PRINT_outer_face_down.stl"), 0.02, 0.1)
    return b


if __name__ == "__main__":
    b = build()
    bb = b.val().BoundingBox()
    print("S2 back plate built into", OUT, [round(v, 1) for v in (bb.xlen, bb.ylen, bb.zlen)], "screws", len(HOLES))
