# SPDX-License-Identifier: CERN-OHL-P-2.0
"""A small coupon for M2 self-tapping screws in printed bosses: four bosses with pilot holes of 1.7, 1.8, 1.9 and 2.0 mm (1 to 4 dots
beside each), and a plate with clearance holes and counterbores. Print the bosses as exported (they stand up, as in the real parts).
    python3 cad/boss_test.py
"""
import os
import cadquery as cq
from export_util import export_stl
from s2_lower import box, cyl

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
PILOTS = (1.7, 1.8, 1.9, 2.0)
BOSS_OD, BOSS_H, PILOT_DEPTH = 5.0, 9.0, 7.0
PLATE_T, CLEAR_D, CBORE_D, CBORE_DEPTH = 1.8, 2.4, 4.6, 1.2


def bosses():
    p = box(0, 0, 0, 46, 14, 2.0)
    for i, d in enumerate(PILOTS):
        x = 6 + i * 11.5
        p = p.union(cyl(x, 6.0, BOSS_OD / 2, 1.9, BOSS_H))
        p = p.cut(cyl(x, 6.0, d / 2, BOSS_H - PILOT_DEPTH, BOSS_H + 0.1))
        for k in range(i + 1):
            p = p.cut(cyl(x - 1.5 + k * 1.5, 12.2, 0.5, 1.2, 2.1))
    return p


def plate():
    p = box(0, 0, 0, 46, 14, PLATE_T)
    for i in range(len(PILOTS)):
        x = 6 + i * 11.5
        p = p.cut(cyl(x, 6.0, CLEAR_D / 2, -0.1, PLATE_T + 0.1))
        p = p.cut(cyl(x, 6.0, CBORE_D / 2, PLATE_T - CBORE_DEPTH, PLATE_T + 0.1))
    return p


def build():
    os.makedirs(OUT, exist_ok=True)
    export_stl(bosses(), os.path.join(OUT, "boss_test_bosses.stl"), 0.02, 0.1)
    export_stl(plate(), os.path.join(OUT, "boss_test_plate.stl"), 0.02, 0.1)


if __name__ == "__main__":
    build()
    print("boss coupon built into", OUT)
