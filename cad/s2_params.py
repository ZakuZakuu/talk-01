# SPDX-License-Identifier: CERN-OHL-P-2.0
"""Parameters for the S2 body (chosen by the owner, 2026-11-26): 48 x 88 x 17 mm. Everything is TENTATIVE until the real parts are measured.

Same axes as params.py: X to the right, Y up (the top is y = H), Z toward the front (z = 0 is the back, z = D the front face).
params.py keeps the round-1 and round-2 numbers so those files stay reproducible.
"""
W, H, D = 48.0, 88.0, 17.0
R_CORNER = 5.0
CHAMFER = 15.0
WALL = 1.6                    # back and ordinary walls
SIDE = 2.4                    # the walls round the lid (the snap grooves are cut into them)
LID_T, LID_BASE, RIDGE_H = 2.4, 1.0, 1.4
RIDGE_W, RIDGE_GAP, RIDGE_PITCH = 1.9, 1.1, 3.0
FIT = 0.25                    # per side, lid in its recess (round 1: 0.20 is a firm fit, 0.25 a little loose)
SEAM_DRAW = 36.0              # drawing y (down from the top) where the lid starts
SEAM_Y = H - SEAM_DRAW        # 52
Z_F = D                       # the front face
Z_R = Z_F - LID_T             # the recess floor, 14.6
Z_I = Z_R - WALL              # inner face of the front wall under the lid, 13.0

# the round hole under the lid (mic port); smaller than before because the body is narrower
HOLE_D = 34.0
HOLE_CX, HOLE_CY = W / 2, 26.0

# the wheel: option P chosen by the owner (2026-11-26): Ø21, standing 2 mm proud of the face; the rim sticks out of the chamfer by about 1.2 mm;
# the gap to its pocket is 0.6 mm (round 1 had 1.8, "a bit big"). Round-1 values were R 9.5 at (W - 14.7, 12).
WHEEL_R, WHEEL_T = 10.5, 5.4          # radius; the thickness INSIDE the face
WHEEL_PROUD = 2.0                     # how far the wheel stands out of the face (7.4 mm of wheel in all)
POCKET_GAP = 0.6
WHEEL_CY_DRAW = 13.0
WHEEL_CX = WHEEL_CY_DRAW + (W - CHAMFER) - 1.4142 * (WHEEL_R - 1.2)    # keeps the rim 1.2 mm beyond the chamfer line: about 32.9

# snap system (per side)
ARM_T, ARM_L, SLOT_W, BUMP = 1.2, 14.0, 1.0, 0.8
TAB_W, TAB_OFFSET = 6.6, 7.2            # hook tabs on the lid's top edge: width, distance of the nearer edge from the centre
