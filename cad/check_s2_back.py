# SPDX-License-Identifier: CERN-OHL-P-2.0
"""Checks of the back plate, the flap stand, the debug hatch lid and the key (2026-11-28).   python3 cad/check_s2_back.py
Fit (interference volumes in mm3, by solid intersection) and printability (faces that point down in the print orientation, from the STLs)."""
import math
import os
import numpy as np
import trimesh
import s2_frame as F
import s2_upper as U
import s2_back as B
import s2_stand as S
import s2_hatch as HT
import s2_key as K
import s2_cap as C

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")


def vol(s):
    try:
        return round(s.val().Volume(), 3)
    except Exception:
        return 0.0


fr, up, bk, cap = F.frame(False), U.upper(), B.back(), C.cap(0.0, groove=False)
print("== the plate on the shells (expected 0):", vol(bk.intersect(fr)), vol(bk.intersect(up)))
fl = S.flap_raw()
print("== the flap stand: closed in its pocket:", vol(S.flap().intersect(bk)), "(expected 0)")
stop = None
for k in range(300, 450):
    if vol(S.open_flap(fl, k / 10.0).intersect(bk)) > 0.005:
        stop = k / 10.0
        break
need = S.needed_open_angle()
print(f"   it swings free to {stop} deg, where its tail meets the end of the hinge pocket (the stop); the lean of {math.degrees(S.THETA):.0f} deg needs {need} deg")
print(f"   standing, the foot touches the desk {S.foot_distance(need):.1f} mm behind the body's edge (the body's balance point is about 11 mm behind it)")
lid = HT.lid()
print("== the hatch lid in its opening (expected 0):", vol(lid.intersect(bk)), vol(lid.intersect(up)))
key = K.key()
print("== the key at rest (expected 0 against the shells and the plate):", vol(key.intersect(fr)), vol(key.intersect(up)), vol(key.intersect(bk)), vol(key.intersect(cap)))
for t in (0.5, 1.0, 1.25, 1.35):
    kp = K.rotate_pressed(key, t)
    print(f"   pressed {t:.2f} mm at its tip: shells {vol(kp.intersect(fr))}, {vol(kp.intersect(up))}; plate (the stop post at 1.3) {vol(kp.intersect(bk))}")
for (n, y, g) in (("S1", K.S1_Y, K.S1_GAP), ("S2", K.S2_Y, K.S2_GAP)):
    sw, foam = K.switch(y, g)
    both = sw.union(foam)
    print(f"   {n}: clicks at {K.actuation_travel(y, g):.2f} mm at the tip; against the plate {vol(both.intersect(bk))}, frame {vol(both.intersect(fr))}, upper {vol(both.intersect(up))}, cap {vol(both.intersect(cap))}; button x key at rest {vol(sw.intersect(key))} (S1: the 0.05 mm preload)")

print("== overhangs in the print orientation (faces pointing down more than 45 deg, above 0.8 mm: the bed-side rounds below that step out 0.3 mm a layer at most)")
for fn in ("s2_back_PRINT_outer_face_down.stl", "s2_stand_PRINT_outer_face_down.stl", "s2_hatch_PRINT_outer_face_down.stl", "s2_key_PRINT_back_down.stl"):
    m = trimesh.load(os.path.join(OUT, fn))
    n, c, a = m.face_normals, m.triangles_center, m.area_faces
    flat = (n[:, 2] < -0.98) & (c[:, 2] > 0.15)
    steep = (n[:, 2] < -0.72) & (n[:, 2] >= -0.98) & (c[:, 2] > 0.8)
    print(f"  {fn}: closed={m.is_watertight}, {len(m.split(only_watertight=False))} piece(s); steep {a[steep].sum():.1f} mm2; flat ceilings {a[flat].sum():.1f} mm2")
    for z in sorted(set(np.round(c[flat][:, 2], 1))):
        sel = flat & (np.round(c[:, 2], 1) == z)
        xy = c[sel][:, :2]
        if a[sel].sum() > 0.5:
            print(f"     at {z:4.1f}: {a[sel].sum():6.1f} mm2, x {xy[:, 0].min():5.1f} to {xy[:, 0].max():5.1f}, y {xy[:, 1].min():5.1f} to {xy[:, 1].max():5.1f}")
