# SPDX-License-Identifier: CERN-OHL-P-2.0
"""Checks of the support-free lower frame and the tightened cap.   python3 cad/check_s2_frame.py"""
import os
import numpy as np
import trimesh
import s2_cap as C
import s2_frame as F
from s2_params import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")


def vol(s):
    try:
        return s.val().Volume()
    except Exception:
        return 0.0


print("== meshes")
for fn in ("s2_frame_PRINT_front_down.stl", "s2_cap_PRINT_face_down.stl", "s2_stop_bar.stl"):
    m = trimesh.load(os.path.join(OUT, fn))
    size = m.bounds[1] - m.bounds[0]
    print(f"  {fn:32s} watertight={m.is_watertight} vol={m.volume / 1000:.2f} cm3 size={size[0]:.1f} x {size[1]:.1f} x {size[2]:.1f} z from {m.bounds[0][2]:.2f}")

fr = F.frame(with_extension=True)
fr_nonub = fr
print("== cap against the frame along the slide (mm3). The catches' nubs are meant to meet the pegs' necks during the slide (the arms give way).")
cap0 = C.cap(0.0, groove=False)
for off in (-6.0, -4.5, -3.0, -1.5, 0.0):
    v = vol(fr.intersect(C.cap(off, groove=False)))
    print(f"  offset {off:5.1f} mm: {v:.3f}")
print("  (expected: 0 at offset 0, the rest only the 4 nubs against the 4 necks, about 4 x 0.4 mm of interference)")

# a dummy microphone board in its seat
mic = F.cyl(F.HUB_C[0], F.HUB_C[1], 13.8 / 2, 9.5, 12.0)
print("== dummy microphone board (13.8 x 2.5 mm) in the seat tube (inner 14.2):", round(vol(fr.intersect(mic)), 3), "mm3")

# overhangs, in the PRINT orientation (front face down, z up from the bed)
m = trimesh.load(os.path.join(OUT, "s2_frame_PRINT_front_down.stl"))
n = m.face_normals
c = m.triangles_center
a = m.area_faces
steep = (n[:, 2] < -0.707) & (c[:, 2] > 0.15)
print("== overhangs in the print orientation (faces pointing down more than 45 deg from the vertical, above the first layer)")
print(f"  total area {a[steep].sum():.1f} mm2 of {a.sum():.0f} mm2")
if steep.any():
    zs = np.round(c[steep][:, 2], 1)
    for z in sorted(set(zs)):
        sel = steep.copy()
        sel[steep] = (zs == z)
        pts = c[sel]
        print(f"  at height {z:5.1f}: {a[sel].sum():6.1f} mm2, x {pts[:, 0].min():.1f} to {pts[:, 0].max():.1f}, y {pts[:, 1].min():.1f} to {pts[:, 1].max():.1f}")
# the catch arm
L = F.ARM_BELOW + F.ARM_ABOVE
I = 1.6 * F.ARM_W ** 3 / 12   # arm 1.2 (variant C)
k = 3 * 3500.0 * I / L ** 3
dfl = (C.NECK_D / 2) - (C.SLOT_W / 2 - F.NUB)
print(f"== catch arm {F.ARM_W} x {L} x 1.6 mm: deflection {dfl:.2f} mm, strain {1.5 * F.ARM_W * dfl / L ** 2 * 100:.2f} %, about {k:.1f} N/mm, {k * dfl:.1f} N per peg, {4 * k * dfl:.1f} N for four (hand calculation, PLA typical)")
