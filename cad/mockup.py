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


def body(w=W, h=H, d=D, key_depth=KEY_DEPTH):
    """The body blank. w, h, d change the size; the wheel keeps its distance from the top-right corner."""
    Yh = lambda yd: h - yd
    wcx = w - (W - WHEEL_CX)
    b = cq.Workplane("XY").rect(w, h, centered=False).extrude(d).edges("|Z").fillet(R_CORNER)
    c = (w - CHAMFER) + h                       # the chamfer line is x + y = c
    cut = (cq.Workplane("XY").workplane(offset=-1)
           .polyline([(c - (h + 2), h + 2), (w + 2, h + 2), (w + 2, c - (w + 2))]).close().extrude(d + 2))
    b = b.cut(cut)
    for (px, py) in ((w - CHAMFER, h), (w, h - CHAMFER)):
        b = b.edges(cq.selectors.BoxSelector((px - 0.6, py - 0.6, -1), (px + 0.6, py + 0.6, d + 1))).fillet(R_CHAMFER_END)
    b = b.faces(">Z").edges().fillet(FRONT_FILLET)
    b = b.faces("<Z").edges().fillet(BACK_FILLET)
    # the wheel pocket and the axle hole
    cy = Yh(WHEEL_CY_DRAW)
    pocket = cq.Workplane("XY").workplane(offset=d - WHEEL_POCKET_DEPTH).center(wcx, cy).circle(WHEEL_POCKET_R).extrude(WHEEL_POCKET_DEPTH + 1)
    axle = cq.Workplane("XY").workplane(offset=d - WHEEL_POCKET_DEPTH - 10).center(wcx, cy).circle(AXLE_HOLE_R + 0.15).extrude(10.5)
    b = b.cut(pocket).cut(axle)
    # the ridges of the lid, as grooves, and the seam
    yd = SEAM_Y + 1.2 + RIDGE_W
    while yd + RIDGE_GAP < h - 3.0:
        g = cq.Workplane("XY").workplane(offset=d - RIDGE_DEPTH_MOCKUP).center(w / 2, Yh(yd + RIDGE_GAP / 2)).rect(w + 2, RIDGE_GAP).extrude(RIDGE_DEPTH_MOCKUP + 1)
        b = b.cut(g)
        yd += RIDGE_PITCH
    seam = cq.Workplane("XY").workplane(offset=d - 0.5).center(w / 2, Yh(SEAM_Y)).rect(w + 2, 0.5).extrude(1.5)
    b = b.cut(seam)
    # a shallow marking where the key sticks on (0.4 mm deep, on the left edge)
    mark = cq.Workplane("XY").workplane(offset=(d - key_depth) / 2).center(0.0, (Yh(KEY_Y0) + Yh(KEY_Y1)) / 2).rect(0.8, KEY_Y1 - KEY_Y0).extrude(key_depth)
    b = b.cut(mark)
    return b


def _fillet_try(solid, selector, radii):
    for r in radii:
        try:
            return solid.edges(selector).fillet(r)
        except Exception:
            continue
    return solid


def key_block(p, h=H, d=D, key_depth=KEY_DEPTH):
    Yh = lambda yd: h - yd
    z0 = (d - key_depth) / 2
    pts = [(0, Yh(KEY_Y0)), (-p, Yh(KEY_TIP_Y)), (-0.64 * p, Yh(KEY_Y1 - 2)), (0, Yh(KEY_Y1))]
    k = cq.Workplane("XY").workplane(offset=z0).polyline(pts).close().extrude(key_depth)
    outer = cq.selectors.BoxSelector((-p - 1, -1, z0 - 1), (-0.05, h + 1, z0 + key_depth + 1))   # only the edges away from the stuck-on side
    vert = cq.selectors.BoxSelector((-p - 1, -1, z0 + 1), (-0.05, h + 1, z0 + key_depth - 1))
    k = _fillet_try(k, vert, (1.0, 0.8, 0.5))
    k = _fillet_try(k, outer, (2.0, 1.5, 1.0))
    return k


def wheel(hole_r=AXLE_HOLE_R):
    w = cq.Workplane("XY").circle(WHEEL_R).extrude(WHEEL_T)
    import math
    for i in range(WHEEL_RIBS):
        a = i * 360.0 / WHEEL_RIBS
        rib = (cq.Workplane("XY").center(WHEEL_R, 0).rect(WHEEL_RIB_D * 2, WHEEL_RIB_W).extrude(WHEEL_T)
               .rotate((0, 0, 0), (0, 0, 1), a))
        w = w.cut(rib)
    w = w.cut(cq.Workplane("XY").circle(hole_r).extrude(WHEEL_T))
    return w


def wheel_placed():
    return wheel().translate((WHEEL_CX, Y(WHEEL_CY_DRAW), D - WHEEL_POCKET_DEPTH + 0.4))


# the size ladder of round 2: S1 a small step, S2 clearly slimmer, S3 very slim (feel only; the electronics may not fit)
LADDER = (("S1", 52.0, 90.0, 20.0), ("S2", 48.0, 88.0, 17.0), ("S3", 46.0, 86.0, 15.0))


def build_round2():
    os.makedirs(OUT, exist_ok=True)
    out = {}
    for name, w, h, d in LADDER:
        kd = d - 6.0
        out[f"r2_body_{name}_{int(w)}x{int(h)}x{int(d)}"] = body(w, h, d, kd)
        out[f"r2_key5_{name}"] = key_block(5.0, h, d, kd)
    out["r2_wheel"] = wheel(WHEEL_HOLE_R2)
    for nm, solid in out.items():
        export_stl(solid, os.path.join(OUT, nm + ".stl"))
    return out


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
    build_round2()
    print("mockup (round 1 and round 2) built into", OUT)
