# SPDX-License-Identifier: CERN-OHL-P-2.0
"""The feel mock-up: a body blank (no electronics), three key blocks (3, 5, 7 mm) and the wheel.

The body has the wheel pocket, the lid ridges (grooves) and a shallow marking where the key sticks on. Print the key blocks and
stick them on with double-sided tape; use a piece of 1.75 mm filament as the wheel's axle.
    python3 cad/mockup.py
"""
import os
import cadquery as cq
from export_util import export_stl
from params import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")


def body():
    b = cq.Workplane("XY").rect(W, H, centered=False).extrude(D).edges("|Z").fillet(R_CORNER)
    c = (W - CHAMFER) + H                       # the chamfer line is x + y = c
    cut = (cq.Workplane("XY").workplane(offset=-1)
           .polyline([(c - (H + 2), H + 2), (W + 2, H + 2), (W + 2, c - (W + 2))]).close().extrude(D + 2))
    b = b.cut(cut)
    for (px, py) in ((W - CHAMFER, H), (W, H - CHAMFER)):
        b = b.edges(cq.selectors.BoxSelector((px - 0.6, py - 0.6, -1), (px + 0.6, py + 0.6, D + 1))).fillet(R_CHAMFER_END)
    b = b.faces(">Z").edges().fillet(FRONT_FILLET)
    b = b.faces("<Z").edges().fillet(BACK_FILLET)
    # the wheel pocket and the axle hole
    cy = Y(WHEEL_CY_DRAW)
    pocket = cq.Workplane("XY").workplane(offset=D - WHEEL_POCKET_DEPTH).center(WHEEL_CX, cy).circle(WHEEL_POCKET_R).extrude(WHEEL_POCKET_DEPTH + 1)
    axle = cq.Workplane("XY").workplane(offset=D - WHEEL_POCKET_DEPTH - 10).center(WHEEL_CX, cy).circle(AXLE_HOLE_R + 0.15).extrude(10.5)
    b = b.cut(pocket).cut(axle)
    # the ridges of the lid, as grooves, and the seam
    yd = SEAM_Y + 1.2 + RIDGE_W
    while yd + RIDGE_GAP < H - 3.0:
        g = cq.Workplane("XY").workplane(offset=D - RIDGE_DEPTH_MOCKUP).center(W / 2, Y(yd + RIDGE_GAP / 2)).rect(W + 2, RIDGE_GAP).extrude(RIDGE_DEPTH_MOCKUP + 1)
        b = b.cut(g)
        yd += RIDGE_PITCH
    seam = cq.Workplane("XY").workplane(offset=D - 0.5).center(W / 2, Y(SEAM_Y)).rect(W + 2, 0.5).extrude(1.5)
    b = b.cut(seam)
    # a shallow marking where the key sticks on (0.4 mm deep, on the left edge)
    mark = cq.Workplane("XY").workplane(offset=KEY_Z0).center(0.0, (Y(KEY_Y0) + Y(KEY_Y1)) / 2).rect(0.8, KEY_Y1 - KEY_Y0).extrude(KEY_DEPTH)
    b = b.cut(mark)
    return b


def _fillet_try(solid, selector, radii):
    for r in radii:
        try:
            return solid.edges(selector).fillet(r)
        except Exception:
            continue
    return solid


def key_block(p):
    pts = [(0, Y(KEY_Y0)), (-p, Y(KEY_TIP_Y)), (-0.64 * p, Y(KEY_Y1 - 2)), (0, Y(KEY_Y1))]
    k = cq.Workplane("XY").workplane(offset=KEY_Z0).polyline(pts).close().extrude(KEY_DEPTH)
    outer = cq.selectors.BoxSelector((-p - 1, -1, KEY_Z0 - 1), (-0.05, H + 1, KEY_Z0 + KEY_DEPTH + 1))   # only the edges away from the stuck-on side
    vert = cq.selectors.BoxSelector((-p - 1, -1, KEY_Z0 + 1), (-0.05, H + 1, KEY_Z0 + KEY_DEPTH - 1))
    k = _fillet_try(k, vert, (1.0, 0.8, 0.5))
    k = _fillet_try(k, outer, (2.0, 1.5, 1.0))
    return k


def wheel():
    w = cq.Workplane("XY").circle(WHEEL_R).extrude(WHEEL_T)
    import math
    for i in range(WHEEL_RIBS):
        a = i * 360.0 / WHEEL_RIBS
        rib = (cq.Workplane("XY").center(WHEEL_R, 0).rect(WHEEL_RIB_D * 2, WHEEL_RIB_W).extrude(WHEEL_T)
               .rotate((0, 0, 0), (0, 0, 1), a))
        w = w.cut(rib)
    w = w.cut(cq.Workplane("XY").circle(AXLE_HOLE_R).extrude(WHEEL_T))
    return w


def wheel_placed():
    return wheel().translate((WHEEL_CX, Y(WHEEL_CY_DRAW), D - WHEEL_POCKET_DEPTH + 0.4))


def build():
    os.makedirs(OUT, exist_ok=True)
    parts = {"mockup_body": body(), "mockup_wheel": wheel()}
    for p in KEY_PROTRUSIONS:
        parts[f"mockup_key_{int(p)}mm"] = key_block(p)
    for name, solid in parts.items():
        export_stl(solid, os.path.join(OUT, name + ".stl"))
    cq.exporters.export(parts["mockup_body"], os.path.join(OUT, "mockup_body.step"))
    asm = body().union(key_block(5.0)).union(wheel_placed())
    export_stl(asm, os.path.join(OUT, "mockup_assembled_view.stl"), 0.03, 0.15)
    return parts


if __name__ == "__main__":
    build()
    print("mockup built into", OUT)
