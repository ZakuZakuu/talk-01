# SPDX-License-Identifier: CERN-OHL-P-2.0
"""Numeric checks on the parts: watertight, volumes, fits the printer, and the interferences that matter.
    python3 cad/check.py
"""
import os
import cadquery as cq
import trimesh
import mockup
import calibration
from params import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")


def vol(shape):
    try:
        return shape.val().Volume()
    except Exception:
        return 0.0


def main():
    print("== meshes (watertight, volume cm3, size mm, fits the A1 mini)")
    ok = True
    for fn in sorted(os.listdir(OUT)):
        if not fn.endswith(".stl") or fn.endswith("assembled_view.stl"):
            continue
        m = trimesh.load(os.path.join(OUT, fn))
        size = m.bounds[1] - m.bounds[0]
        fits = all(size[i] <= BUILD[i] for i in range(3))
        ok &= bool(m.is_watertight) and fits
        print(f"  {fn:26s} watertight={m.is_watertight!s:5s} vol={m.volume / 1000:7.2f} size={size[0]:6.1f} x {size[1]:6.1f} x {size[2]:5.1f} fits={fits}")
    print("== interference (mm3; 0 is good)")
    body = mockup.body()
    wheel = mockup.wheel_placed()
    print("  wheel in its pocket     :", round(vol(body.intersect(wheel)), 3))
    for p in KEY_PROTRUSIONS:
        print(f"  key {int(p)} mm on the body     :", round(vol(body.intersect(mockup.key_block(p))), 3))
    # how far the wheel sticks out of the chamfer
    import math
    cx, cy = WHEEL_CX, Y(WHEEL_CY_DRAW)
    dist = ((W - CHAMFER) + H - (cx + cy)) / math.sqrt(2)
    print(f"  wheel rim beyond the chamfer line: {WHEEL_R - dist:.2f} mm (distance centre to line {dist:.2f})")
    lid = calibration.lid()
    frame = calibration.frame()
    print("  snap lid seated in frame:", round(vol(frame.intersect(lid)), 3))
    arm_free = calibration.ARM_Y1 - calibration.ARM_Y0
    deflection = 0.6
    strain = 1.5 * calibration.ARM_T * deflection / arm_free ** 2
    print(f"  snap arm strain (1.5 t y / L^2, t={calibration.ARM_T}, y={deflection}, L={arm_free}): {strain * 100:.2f} %")
    print("== round 2")
    for name, w, h, d in mockup.LADDER:
        kd = d - 6.0
        b = mockup.body(w, h, d, kd)
        wp = mockup.wheel(mockup.WHEEL_HOLE_R2).translate((w - (W - WHEEL_CX), h - WHEEL_CY_DRAW, d - WHEEL_POCKET_DEPTH + 0.4))
        k = mockup.key_block(5.0, h, d, kd)
        print(f"  {name} {w:.0f} x {h:.0f} x {d:.0f}: wheel in pocket {vol(b.intersect(wp)):.3f} mm3, key on body {vol(b.intersect(k)):.3f} mm3")
    for bump in (0.8, 0.5):
        l2 = calibration.lid2(bump)
        f2 = calibration.frame2(bump)
        print(f"  snap pair bump {bump}: lid seated in frame {vol(f2.intersect(l2)):.3f} mm3; strain at the insertion deflection {1.5 * calibration.ARM_T * (bump - 0.25 + 0.0) / arm_free ** 2 * 100:.2f} %")
    print("ALL MESHES OK" if ok else "CHECK FAILED")


if __name__ == "__main__":
    main()
