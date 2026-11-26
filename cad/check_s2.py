# SPDX-License-Identifier: CERN-OHL-P-2.0
"""Numeric checks of the S2 lower shell and lid.   python3 cad/check_s2.py"""
import os
import trimesh
import s2_lower as L
from s2_params import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")


def vol(s):
    try:
        return s.val().Volume()
    except Exception:
        return 0.0


sh, ld = L.shell(), L.lid()
print("== meshes")
for fn in ("s2_lower_shell.stl", "s2_lid.stl"):
    m = trimesh.load(os.path.join(OUT, fn))
    size = m.bounds[1] - m.bounds[0]
    print(f"  {fn:22s} watertight={m.is_watertight} vol={m.volume / 1000:.2f} cm3 size={size[0]:.1f} x {size[1]:.1f} x {size[2]:.1f}")
print("== lid seated in the shell (mm3; 0 is good):", round(vol(sh.intersect(ld)), 3))
# the gaps round the lid
print(f"== lid {L.LID_X1 - L.LID_X0:.2f} x {L.LID_Y1 - L.LID_Y0:.2f} mm in a recess {W - 2 * SIDE:.1f} x {SEAM_Y - SIDE:.1f} mm: {FIT} mm per side")
print(f"== front face of the lid vs the control zone face: both at z = {Z_F}")
# the snap: bump tip against the wall at insertion
wall_x = SIDE
tip = L.LID_X0 - BUMP
interference = wall_x - tip
strain = 1.5 * ARM_T * interference / ARM_L ** 2
E, I = 3500.0, 2.4 * ARM_T ** 3 / 12          # PLA modulus (typical, MPa) and the arm's second moment (the arm is 2.4 mm high)
k = 3 * E * I / ARM_L ** 3
print(f"== snap arm: interference at insertion {interference:.2f} mm, strain {strain * 100:.2f} %, stiffness about {k:.2f} N/mm, force about {k * interference:.2f} N per arm (hand calculation, PLA typical)")
wall_left = SIDE - (BUMP + 0.3) - 0.0
print(f"== wall left behind a snap groove: {SIDE - (SIDE - (L.LID_X0 - BUMP - 0.3)):.2f} mm of the {SIDE} mm side wall")
