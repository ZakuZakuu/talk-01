# SPDX-License-Identifier: CERN-OHL-P-2.0
"""The S2 body put together as one view model (frame + upper shell + cap + back plate + a plain stand-in wheel), for the previews only.
    python3 cad/assemble.py"""
import os
import cadquery as cq
from export_util import export_stl
import s2_frame as F
import s2_upper as U
import s2_back as B
import s2_cap as C

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")

if __name__ == "__main__":
    wheel = cq.Workplane("XY").workplane(offset=11.6).center(U.WHEEL_CX, U.WHEEL_CY).circle(10.5).extrude(7.4)
    body = F.frame(False).union(U.upper()).union(C.cap(0.0, groove=False)).union(B.back()).union(wheel)
    export_stl(body, os.path.join(OUT, "s2_body_assembled_view.stl"), 0.03, 0.15)
    inner = F.frame(False).union(U.upper()).union(wheel)
    export_stl(inner, os.path.join(OUT, "s2_body_open_view.stl"), 0.03, 0.15)
    print("assembled views written")
