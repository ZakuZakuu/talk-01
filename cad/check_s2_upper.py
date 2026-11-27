# SPDX-License-Identifier: CERN-OHL-P-2.0
"""Checks of the upper shell.   python3 cad/check_s2_upper.py"""
import os
import numpy as np
import trimesh
import cadquery as cq
import s2_cap as C
import s2_frame as F
import s2_upper as U

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")


def vol(s):
    try:
        return s.val().Volume()
    except Exception:
        return 0.0


fn = "s2_upper_PRINT_front_down.stl"
m = trimesh.load(os.path.join(OUT, fn))
size = m.bounds[1] - m.bounds[0]
print(f"== {fn}: watertight={m.is_watertight} pieces={len(m.split(only_watertight=False))} vol={m.volume / 1000:.2f} cm3 size={size[0]:.1f} x {size[1]:.1f} x {size[2]:.1f}")

u = U.upper()
fr = F.frame(with_extension=False)
cap = C.cap(0.0, groove=False)
tabs = [cq.Workplane("XY").box(2.4, 3.0, 2.4, centered=False).translate((tx - 1.2, 52.0, 6.0)) for tx in U.TABS_X]
print("== fit against the lower frame and the cap (mm3, all expected 0)")
print("  upper x frame:", round(vol(u.intersect(fr)), 3))
print("  upper x cap  :", round(vol(u.intersect(cap)), 3))
print("  upper x the frame's alignment tabs (they poke into the slots; the frame's own tab volume is in `frame`):",
      [round(vol(u.intersect(t)), 3) for t in tabs])
dummy = cq.Workplane("XY").box(U.BD_X1 - U.BD_X0, U.BD_LEN, 1.0, centered=False).translate((U.BD_X0, U.BD_Y0, U.BD_Z_PCB[0]))
comp = cq.Workplane("XY").box(10, 12, 2.0, centered=False).translate((U.BD_X0 + 4, U.BD_Y0 + 6, U.BD_Z_PCB[0] - 2.0))    # a stand-in for the module can
usb = cq.Workplane("XY").box(9.0, 7.4, 3.2, centered=False).translate((U.USB_X - 4.5, U.BD_Y1 - 6.0, U.BD_Z_PCB[0] - 3.2))
print("== a dummy Super Mini (18 x 23.5 pcb 1 mm, a can, a USB-C 9 x 3.2) in the pocket:", [round(vol(u.intersect(x)), 3) for x in (dummy, comp, usb)])
wheel = cq.Workplane("XY").workplane(offset=11.6).center(U.WHEEL_CX, U.WHEEL_CY).circle(10.5).extrude(7.4)
print("== the wheel (Ø21, z 11.6 to 19) in its bore:", round(vol(u.intersect(wheel)), 3), "mm3 (expected 0)")

n, c, a = m.face_normals, m.triangles_center, m.area_faces
H0 = m.bounds[1][1]                  # print y -> assembled y = H0 - y (the shell spans y 52 to 88; the flip keeps the order reversed)
flat = (n[:, 2] < -0.98) & (c[:, 2] > 0.15)
slant = (n[:, 2] < -0.72) & (n[:, 2] >= -0.98) & (c[:, 2] > 0.8)       # above the fillet's foot: the front fillet's first 0.8 mm steps out by 0.3 mm a layer at most
foot = (n[:, 2] < -0.72) & (c[:, 2] > 0.15) & (c[:, 2] <= 0.8)
print("== overhangs in the print orientation (above the first layer). flat = a ceiling to bridge; steep = more than 45 deg from the vertical")
print(f"  steep slanted faces: {a[slant].sum():.2f} mm2 (expected 0); the front fillet's foot (first 0.8 mm, steps of 0.3 mm or less a layer): {a[foot].sum():.1f} mm2")
print(f"  flat ceilings: {a[flat].sum():.1f} mm2; by height:")
for z in sorted(set(np.round(c[flat][:, 2], 1))):
    sel = flat & (np.round(c[:, 2], 1) == z)
    xy = c[sel][:, :2]
    ys = 88.0 - xy[:, 1] if False else xy[:, 1]
    print(f"    height {z:5.1f} (assembled z {17 - z:5.1f}): {a[sel].sum():6.1f} mm2, x {xy[:, 0].min():5.1f} to {xy[:, 0].max():5.1f}, print y {xy[:, 1].min():5.1f} to {xy[:, 1].max():5.1f}")
