# Mechanical plan for the S2 body (48 × 88 × 17 mm)

Status: **a plan with numbers from typical part sizes; nothing here is measured.** S2 and the middle (5 mm) key block were chosen by the owner on 2026-11-26. Files: [`../cad/`](../cad/README.md).

## 1 · What the owner said after round 2
- **S2 (48 × 88 × 17 mm)** is the body ("super small, no problem"): keep it **compact and slim**, assembly must work, but **not squeezed to the extreme**. The current shape was "too fat"; slim and long is easier to grip.
- **The middle key block (5 mm) was the most comfortable.**
- **Hands:** the right hand felt more comfortable, but **both hands work** (§6); no mirrored version.
- **The wheel's gap to its pocket was too large**: make the wheel sit close, looking whole. Done: the gap is now 0.6 mm (it was 1.8).
- **Snap lid:** the arms did **not go fully in** and there was **no click**. Design it **directly on the real body**, not a miniature (§4). Then, looking at that piece: the two arms on the front are **too conspicuous**; the front must be **one complete plane, edge to edge, no frame** (§4, now a keyhole slide).

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

## 4 · The lid (the cap): a keyhole slide, nothing on the face

**The owner's requirement (2026-11-26, after the round-3 look at the lid test piece):** the front must be **one complete plane, running out to the edge, with no frame**, and the catches must not show. Visible snap arms in the face were "too conspicuous".

**Options considered**

| Option | Verdict |
|---|---|
| Arms or hooks on the face, in a frame (the round-2 piece, [`../cad/s2_lower.py`](../cad/s2_lower.py)) | **dropped**: visible, and it needs a frame |
| Slide-in rails like a battery door | needs the walls to overlap the cap's edges, which is a **visible lip or frame**: rejected |
| Hooks on the cap's back that snap into the walls from inside (like a phone case) | invisible, but a hook standing up from the cap prints with its layers across the bend: weak; and taking it off needs prying notches |
| Press or friction fit | round 1 showed that 0.05 mm separates "tight" from "falls out": unreliable |
| Magnets | invisible and robust; the owner finds it too complex; **kept as the fallback** |
| **Keyhole slide with a hidden detent** | **proposed, now built** ([`../cad/s2_cap.py`](../cad/s2_cap.py)) |

**How the proposed cap works** (diagram: [`print-test-guide/cap-keyhole.png`](print-test-guide/cap-keyhole.png)):
- The cap lies **on top of the body's walls** and forms the front edge itself: no frame; the seam is a fine line round it. Its outline is the body's outline (0.1 mm inside), edge to edge.
- On its back are **four mushroom pegs** (neck Ø2.4, head Ø5.0). The body's floor (1.6 mm) has **four keyholes**: a round entry (Ø6.2) and a slot (2.8 wide) running 6 mm up. You put the cap on **6 mm too low** (its bottom edge overhangs the chin), pegs through the entries, then **slide it up 6 mm**: the heads are now behind the floor and the cap cannot be lifted. Its top edge stops against the control zone.
- A small **tongue is cut in the floor** (14 × 3 mm, lying flat, with a 0.6 mm bump at its tip); the cap's back has a groove there. At the end of the slide the bump drops into the groove: the **"click"** that holds it. The tongue bends **along the print layers** (the strong direction); by hand calculation 0.73 % strain, about 2.4 N (PLA typical).
- **To take it off:** thumb on the ridges (the grip), push the cap **down 6 mm** (over the click), lift it off.
- The checks in [`../cad/check_s2_cap.py`](../cad/check_s2_cap.py): the cap does not touch the shell (the bump left out) at any position of the slide; locked, with the bump in its groove, it does not touch either; in mid-slide only the 0.6 mm bump meets it (the elastic part).

**What is not known (nothing is printed yet):**
- whether the click is clear and the holding force right; the round-1 snap never clicked, and I do not know why;
- whether the tongue (it hangs over the cavity) prints: it needs **supports from the bed** under it, which I have not checked in a slicer;
- how it feels to slide off with a thumb; a small notch in the **body's** chin could expose the cap's bottom edge for a nail (later, only if needed);
- the pegs' heads use the cavity's depth from z = 10.6 to 13; nothing else may sit there in the lower zone.

## 5 · Printing notes
- Front shell **front face up** (as exported): the cavity opens toward the bed; the big round hole leaves no ceiling wider than about 9 mm, so it should print without supports. The lid face up. Untested in a slicer by me.
- Wheel: hole **2.3 mm** (round 1: 2.0 was too tight; small round holes print about 0.3 mm small). Push fits 0.20 mm per side; the lid 0.25.

## 6 · Left hand or right hand?
**Both** (owner, 2026-11-26): no mirrored version. With the **left hand**: the thumb presses the key, the index finger turns the wheel. With the **right hand**: the index and middle fingers press the key, the thumb turns the wheel. Both feel fine to the owner; a smaller body helps both. Grip, in the owner's words: the thumb just reaches the middle finger's pad; it touches the little finger only barely; it cannot reach the index finger. (The owner's hand is "about an iPhone" in size; no measuring needed.) Keep the wheel reachable by the index finger as well as by the thumb.

## 7 · Still open (needs real parts)
- the real sizes of the controller board, switches, the microphone module and the cable's plug (the top opening is sized by the plug);
- the board's thickness with its USB-C, and where the plug sits in the depth;
- the axle and cam: a 2 mm steel pin with a printed cam, or a printed axle (first design to be drawn);
- the key's hinge and spring; the back shell, hatch and stand.

## 8 · The wheel: bigger, thicker, a hero (owner's wish) and what it costs

The owner wants a **bigger and thicker wheel**, very conspicuous: easier to flick, more character, and (the owner's thought) the sensing could sit deeper, with more room. The honest trade-offs at S2 (48 × 88 × 17, USB-C on top, the controller board beside the wheel):

| Option | What it is | Cost |
|---|---|---|
| **P (CHOSEN by the owner)** | **Ø21, standing 2 mm PROUD of the face** (2 mm outside plus the same 5.4 mm inside = 7.4 mm of wheel), a bold rim | nothing inside: the depth stack is unchanged; the largest wheel that still leaves the controller board beside it (Ø21 is about the limit at width 48) |
| Q | Ø24 or bigger | the wheel's pocket would cover the board's place, so the board must move to the lower zone (behind the microphone), and the **USB-C could no longer be on the top edge** (the cable would have to come from the bottom, or via a wire to a port on top): a change to a decided point |
| R | thicker **inside** (7 to 8 mm) | the stack (wheel, floor, cam, switches, board) grows by 2 to 3 mm: there is only 2.4 mm spare at 17 mm depth; the body would have to be about 19 mm |

An absolute magnetic sensor (an AS5600 module and a magnet) in place of the two switches and the cam makes the stack a little thinner but does not change the plan view, so it does not rescue Q. **Asked of the owner:** is P (proud Ø21) acceptable? A proud wheel is also easier to reach with the index finger, since its rim stands out of the face. (An ergonomic estimate, not tested.)

## 9 · Next
1. The owner prints **`s2_cap_shell.stl`** (front up, supports from the bed under the detent tongue) and **`s2_cap_PRINT_face_down.stl`** ([`../cad/out/`](../cad/out/)) and tries the cap: does it go on, slide, click, hold, come off?
2. ~~The owner decides the wheel~~: **P chosen**.
3. Once the parts arrive and are measured, the full shells.
