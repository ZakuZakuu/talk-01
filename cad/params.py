# SPDX-License-Identifier: CERN-OHL-P-2.0
"""Shared parameters for talk.01 (mm). Everything is TENTATIVE until the real parts are measured: see docs/parts-list.md.

Coordinates: X to the right, Y up (the top of the device is y = H), Z toward the front (z = 0 is the back, z = D the front face).
Drawings in design/concepts use y DOWN from the top; use Y(y_draw) to convert.
"""
W, H, D = 58.0, 92.0, 24.0          # outer size (width, height, depth)
R_CORNER = 5.0                       # plan corner radius
CHAMFER = 15.0                       # the top-right chamfer
R_CHAMFER_END = 3.0                  # the two corners where the chamfer meets the edges
FRONT_FILLET, BACK_FILLET = 1.5, 2.0

SEAM_Y = 36.0                        # the lid starts here (drawing y, from the top)

# the key (left edge, drawing y 12 to 58)
KEY_Y0, KEY_Y1 = 12.0, 58.0
KEY_TIP_Y = 16.5                     # where the slanted edge sticks out most
KEY_DEPTH = 12.0                     # along z
KEY_Z0 = (D - KEY_DEPTH) / 2.0
KEY_PROTRUSIONS = (3.0, 5.0, 7.0)    # the feel mock-up compares these

# the wheel (the dial) in the top-right chamfer
WHEEL_CX, WHEEL_CY_DRAW = 43.3, 12.0
WHEEL_R, WHEEL_T = 9.5, 5.4
WHEEL_POCKET_R = WHEEL_R + 1.8
WHEEL_POCKET_DEPTH = 6.4
WHEEL_RIBS, WHEEL_RIB_W, WHEEL_RIB_D = 36, 0.5, 0.5
AXLE_HOLE_R = 1.0                    # a piece of 1.75 mm filament as the axle in the mock-up

# the lid ridges and the round hole
RIDGE_W, RIDGE_GAP, RIDGE_PITCH = 1.9, 1.1, 3.0
RIDGE_DEPTH_MOCKUP = 0.8
HOLE_CX, HOLE_CY_DRAW, HOLE_R = 29.0, 64.0, 19.0

# the printer: Bambu Lab A1 mini
BUILD = (180.0, 180.0, 180.0)


def Y(y_draw):
    """Convert a drawing y (down from the top) to a CAD y (up)."""
    return H - y_draw


# --- lessons from the round-1 prints (owner, 2026-11-26) on a Bambu A1 mini, PLA, 0.4 mm nozzle, 0.2 mm layers
FIT_PUSH = 0.20      # per side: a push fit that holds ("2 is best"); 0.15 is too tight, 0.25 a little loose, 0.30 and more fall out
FIT_LID = 0.25       # per side for the lid in its frame (it must also come out again)
HOLE_EXTRA = 0.30    # a small round hole prints about this much too small: model it this much bigger
WHEEL_HOLE_R2 = 1.15 # the wheel's axle hole for 1.75 mm filament (the 2.0 mm hole of round 1 was far too tight)
