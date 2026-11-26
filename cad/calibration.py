# SPDX-License-Identifier: CERN-OHL-P-2.0
"""The calibration set: answers the printing questions that are only known by printing.

  calibration_plate.stl : clearance pockets, ridge gaps, through-slots, raised lines (print face up)
  calibration_tabs.stl  : five tabs that fit the five pockets (print flat, separate from the plate)
  snap_frame.stl        : a frame with a recess, a lip for two hooks and two side grooves (print face up)
  snap_lid.stl          : a small lid with two rigid hooks and two in-plane snap arms (print back down)
    python3 cad/calibration.py
"""
import os
import cadquery as cq
from export_util import export_stl

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")

CLEARANCES = (0.15, 0.20, 0.25, 0.30, 0.40)       # per side, mm
GAPS = (0.8, 1.1, 1.4)                             # gaps between ridges
SLOTS = (0.6, 0.8, 1.0, 1.1, 1.3)                  # through-slot widths
LINES = (0.4, 0.6, 0.8, 1.0, 1.2)                  # raised line widths


def box(x0, y0, z0, x1, y1, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))


def plate():
    p = box(0, 0, 0, 110, 70, 3.0)
    # 1. clearance pockets: 10 mm tabs, each pocket 10 + 2c, 2.0 deep; n small dots beside each pocket mark c
    for i, c in enumerate(CLEARANCES):
        cx, cy = 12 + i * 14, 52
        s = 10 + 2 * c
        p = p.cut(box(cx - s / 2, cy - s / 2, 1.0, cx + s / 2, cy + s / 2, 3.1))
        for k in range(i + 1):
            dot = cq.Workplane("XY").workplane(offset=2.4).center(cx - 4 + k * 2.2, cy - 8.5).circle(0.7).extrude(1.0)
            p = p.cut(dot)
    # 2. ridge gaps: 4 ridges 1.9 wide and 1.4 tall, three gaps
    for gi, g in enumerate(GAPS):
        x0 = 5 + gi * 27
        for k in range(4):
            xr = x0 + k * (1.9 + g)
            p = p.union(box(xr, 8, 3.0, xr + 1.9, 28, 4.4))
    # 3. through-slots (the plate is 3.0 mm thick)
    for i, w in enumerate(SLOTS):
        x0 = 90 + i * 4.0
        p = p.cut(box(x0, 8, -0.1, x0 + w, 24, 3.1))
    # 4. raised lines 0.6 tall
    for i, w in enumerate(LINES):
        x0 = 90 + i * 4.0
        p = p.union(box(x0, 36, 3.0, x0 + w, 56, 3.6))
    return p


def tabs():
    t = None
    for i in range(5):
        piece = box(i * 14, 0, 0, i * 14 + 10, 10, 2.0)
        for k in range(i + 1):
            piece = piece.cut(cq.Workplane("XY").workplane(offset=1.4).center(i * 14 + 2 + k * 2.2, 8.2).circle(0.7).extrude(1.0))
        t = piece if t is None else t.union(piece)
    return t


# --- the snap-fit pair ---------------------------------------------------------------------------------------
L, HH, T, C = 30.0, 24.0, 2.4, 0.2          # lid width, height, thickness, clearance per side
ARM_T, ARM_Y0, ARM_Y1 = 1.2, 0.0, 14.0     # in-plane arm: thickness, free end, root
SLOT_W = 1.0
BUMP = 0.8                                  # how far the bump sticks out
TAB_X = ((4.2, 10.8), (-10.8, -4.2))


def extrude_xz(pts, y0, y1):
    return cq.Workplane("XZ").workplane(offset=-y1).polyline(pts).close().extrude(y1 - y0)


def lid():
    b = box(-L / 2, 0, 0, L / 2, HH, T)
    for (x0, x1) in TAB_X:                                  # rigid hooks on the top edge
        b = b.union(box(x0, HH - 0.2, 0.2, x1, HH + 1.6, 1.2))
    for sgn in (1, -1):
        xo = sgn * L / 2
        xi = sgn * (L / 2 - ARM_T)
        xs = sgn * (L / 2 - ARM_T - SLOT_W)
        lo, hi = sorted((xi, xs))
        b = b.cut(box(lo, -0.5, -0.1, hi, ARM_Y1, T + 0.1))            # the slot beside the arm, open at the bottom
        pts = [(xo, 0.4), (xo + sgn * BUMP, 0.8), (xo + sgn * BUMP, 1.5), (xo, 1.9)]    # the bump profile in (x, z)
        bump = extrude_xz(pts, 0.8, 4.0)
        b = b.union(bump)
    b = b.cut(cq.Workplane("XY").center(0, 0).circle(3.0).extrude(T))   # a thumb notch in the bottom edge
    return b


def frame():
    f = box(-20, -7, -3, 20, HH + C + 1.8 + 5, T)
    f = f.cut(box(-(L / 2 + C), -C, 0, L / 2 + C, HH + C, T + 0.1))     # the recess for the lid
    for (x0, x1) in TAB_X:                                              # the undercut under the lip for the hooks
        lo, hi = sorted((x0 - C, x1 + C))
        f = f.cut(box(lo, HH + C - 0.1, 0, hi, HH + C + 1.8, 1.4))
    for sgn in (1, -1):                                                 # the grooves the bumps click into
        x0 = sgn * (L / 2 + C)
        x1 = sgn * (L / 2 + C + 0.9)
        lo, hi = sorted((x0, x1))
        f = f.cut(box(lo, 0.5, 0.3, hi, 4.4, 1.9))
    f = f.cut(cq.Workplane("XY").workplane(offset=0.8).center(0, -3.0).circle(7.5).extrude(T))   # a scoop to get a nail under the lid
    return f


def build():
    os.makedirs(OUT, exist_ok=True)
    parts = {"calibration_plate": plate(), "calibration_tabs": tabs(), "snap_lid": lid(), "snap_frame": frame()}
    for name, solid in parts.items():
        export_stl(solid, os.path.join(OUT, name + ".stl"), 0.01, 0.1)
    return parts


if __name__ == "__main__":
    build()
    print("calibration set built into", OUT)
