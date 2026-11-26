# SPDX-License-Identifier: CERN-OHL-P-2.0
"""Numeric checks of the keyhole-slide cap.   python3 cad/check_s2_cap.py"""
import os
import trimesh
import s2_cap as C
from s2_params import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")


def vol(s):
    try:
        return s.val().Volume()
    except Exception:
        return 0.0


print("== meshes")
for fn in ("s2_cap_shell.stl", "s2_cap.stl"):
    m = trimesh.load(os.path.join(OUT, fn))
    size = m.bounds[1] - m.bounds[0]
    print(f"  {fn:20s} watertight={m.is_watertight} vol={m.volume / 1000:.2f} cm3 size={size[0]:.1f} x {size[1]:.1f} x {size[2]:.1f}")
nb = C.shell(with_bump=False)
wb = C.shell(with_bump=True)
print("== cap against the shell WITHOUT the detent bump, along the slide (mm3; 0 is good)")
for off in (-6.0, -4.5, -3.0, -1.5, 0.0):
    print(f"  offset {off:5.1f} mm: {vol(nb.intersect(C.cap(off))):.3f}")
print("== locked position (offset 0) WITH the bump in its groove:", round(vol(wb.intersect(C.cap(0.0))), 3), "mm3")
print("== mid-slide WITH the bump (the intended elastic interference, the tongue gives way):", round(vol(wb.intersect(C.cap(-3.0))), 3), "mm3 (the bump is", C.BUMP_H, "mm high)")
t = C.TONGUE
L = t["x1"] - t["x0"]
y = C.BUMP_H
th = WALL
E, I = 3500.0, t["w"] * th ** 3 / 12
k = 3 * E * I / L ** 3
print(f"== detent tongue {L:.0f} x {t['w']:.0f} x {th} mm: strain at {y} mm = {1.5 * th * y / L ** 2 * 100:.2f} %, stiffness ~{k:.1f} N/mm, force ~{k * y:.1f} N (PLA typical, hand calculation; the lateral push needed to slide is about this force plus friction)")
print(f"== peg: neck {C.NECK_D} mm in a {C.SLOT_W} mm slot, head {C.HEAD_D} mm through a {C.ENTRY_D} mm entry; floor {WALL} mm, neck length {C.NECK_L} mm: {C.NECK_L - WALL:.1f} mm of play")
print(f"== cap {C.CAP_X1 - C.CAP_X0:.1f} x {C.CAP_Y1 - C.CAP_Y0:.2f} mm, {C.CAP_INSET} mm inside the body outline on each side; gap to the control zone {C.CAP_TOP_GAP} mm")
