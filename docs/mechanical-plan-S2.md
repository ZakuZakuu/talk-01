# Mechanical plan for the S2 body (48 × 88 × 17 mm)

Status: **a plan with numbers from typical part sizes; nothing here is measured.** S2 and the middle (5 mm) key block were chosen by the owner on 2026-11-26. Files: [`../cad/`](../cad/README.md).

## 1 · What the owner said after round 2
- **S2 (48 × 88 × 17 mm)** is the body ("super small, no problem"): keep it **compact and slim**, assembly must work, but **not squeezed to the extreme**. The current shape was "too fat"; slim and long is easier to grip.
- **The middle key block (5 mm) was the most comfortable.**
- **The right hand is much more comfortable** than the left: the right thumb reaches the wheel more easily. The owner holds it in the left hand. (See §6.)
- **The wheel's gap to its pocket was too large**: make the wheel sit close, looking whole. Done: the gap is now 0.6 mm (it was 1.8).
- **Snap lid:** the arms did **not go fully in** and there was **no click**. Design the arms **directly on the real body**, not a miniature (§4).

## 2 · The parts (proposal)

| Part | What | Printed how |
|---|---|---|
| Front shell | the face: control zone, wheel pocket, the lid recess with its walls, the hook lip, grooves, finger slot, round hole | front face up, as exported |
| Back shell | a tray with posts for the boards, the hatch and the stand pivot | open side up |
| Lid | the whole lower face (the ridged pattern) | ridges up |
| Key | the slanted key on the left edge, hinged on a steel pin | as exported |
| Dial wheel | Ø19, with a short axle and the cam behind the pocket floor | flat |
| Switch board | a small board with two switches for the wheel and two for the key | bought parts |
| Mic bracket | holds the microphone module behind the round hole, changed from the front with the lid off | flat |

The two shells join with **four M2 screws into heat-set inserts** at the back (the parts list has them); the lid needs none.

## 3 · The stack in the control zone (depth 17, from the front face, mm)

| Layer | Thickness | z (from the back) |
|---|---|---|
| front wall | 1.8 | 15.2 to 17.0 |
| the wheel (it sits 0.6 below the face) | 5.4 | 11.0 to 16.4 |
| pocket floor (0.4 clearance behind the wheel, floor 1.0) | 1.0 | 9.6 to 10.6 |
| the cam, on the axle behind the floor | 1.4 | 8.2 to 9.6 |
| the two switches | 3.0 (low profile) or 4.3 | 5.2 to 8.2, or 3.9 to 8.2 |
| their board | 1.2 | 4.0 to 5.2, or 2.7 to 3.9 |
| back wall | 1.6 | 0 to 1.6 |
| **spare** | | **2.4 mm** (3.0 switches), **1.1 mm** (4.3 switches) |

**The controller board lies beside the wheel, not behind it:** the pocket's outer wall begins about x = 22 (from the left); the board (21 × 17.5, typical) takes x = 2.7 to 20.2, y 3 to 24 from the top; its USB-C therefore sits **about 11.5 mm from the left edge** of the top, so the plug is **left of centre** (the wheel balances it on the right). The key's switches sit below it (y 25 to 45), against the left wall.

**The lower zone:** lid 2.4, front wall 1.6, a 1 mm foam under the microphone module (1.8), then about **8 mm of free depth** to the back wall: the expansion space (a thin pack of 4 to 5 mm fits; not in v0.1).

## 4 · The lid on the real body (built in [`../cad/s2_lower.py`](../cad/s2_lower.py))

- **Where the arms are:** the lid spans the lower face (y 36 to 88 from the top) inside walls of **2.4 mm** on both sides and the chin. The **two in-plane snap arms are in the lid's side rails, low down**, each 14 mm long, 1.2 mm thick, with an 0.8 mm bump at the free end that clicks into a **groove in the side wall** (the wall keeps 1.55 mm there). The **two rigid hooks** are on the lid's top edge and tuck under a lip of the control zone's lower edge (the seam beam). A **scoop in the chin** and a **slot through the front wall under the lid's bottom edge** let a nail get under it.
- **Sizes:** lid 42.7 × 49.1 × 2.4 mm in a recess of 43.2 × 49.6 mm: 0.25 mm per side (round 1: 0.20 mm was a firm fit, 0.25 a little loose, 0.30 and more fell out). The lid's face is flush with the control zone (z = 17).
- **Numbers (hand calculation, PLA typical):** interference at insertion 0.55 mm; strain 0.51 %; the arm is soft, about 1.3 N/mm, so about 0.7 N per arm.
- **Why round 1 did not click: I do not know.** By the numbers the arms are soft and the bumps should engage. Possible causes: the lid was not pushed fully down; a printed 1 mm slot narrower than modelled (the slot must be open); the groove not deep enough in the print. **The new test piece will show.** It is the real geometry, so what works there is what works in the product.
- **Fallback if the snap stays unreliable:** four small **magnets** (for example 6 × 2 mm) set in pockets in the lid and the front wall. No flexing parts, tolerant of print errors, a satisfying "clack", easy to lift with the finger slot; one more part to buy and glue. Offered, not chosen.

## 5 · Printing notes
- Front shell **front face up** (as exported): the cavity opens toward the bed; the big round hole leaves no ceiling wider than about 9 mm, so it should print without supports. The lid face up. Untested in a slicer by me.
- Wheel: hole **2.3 mm** (round 1: 2.0 was too tight; small round holes print about 0.3 mm small). Push fits 0.20 mm per side; the lid 0.25.

## 6 · Left hand or right hand?
The layout is **right-hand-friendly**: the fingers wrap the left edge and press the key, the right thumb sweeps the wheel on the right. For the **left hand** it is the mirror image: the key on the right edge, the wheel in the top-left corner. CAD can mirror the whole thing with one parameter. **Question for the owner:** in daily use, which hand holds it while talking? If it is the left, a mirrored build may be better for the owner than the current layout.

## 7 · Still open (needs real parts)
- the real sizes of the controller board, switches, the microphone module and the cable's plug (the top opening is sized by the plug);
- the board's thickness with its USB-C, and where the plug sits in the depth;
- the axle and cam: a 2 mm steel pin with a printed cam, or a printed axle (first design to be drawn);
- the key's hinge and spring; the back shell, hatch and stand.

## 8 · Next
1. The owner prints **`s2_lower_shell.stl` and `s2_lid.stl`** ([`../cad/out/`](../cad/out/)) and tries the lid: does it click, does it seat flush, does it come out with the finger slot?
2. Once the parts arrive and are measured, the full shells.
