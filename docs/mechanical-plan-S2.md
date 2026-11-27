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

## 9 · How the boards are held (they have no screw holes)

The XIAO ESP32S3 and the round microphone boards have **no mounting holes** (the XIAO has edge pads; the round boards have pads). They are held by **the shape of the shell, a little foam and one or two printed tabs**, not by screws. A plan (sizes from the push-fit test: 0.20 mm per side holds; the real board sizes are still to be measured):

| Part | How it is held |
|---|---|
| **XIAO ESP32S3** | in a printed **pocket** (the board's outline plus 0.2 mm a side) on posts; the **USB-C end sits in an opening of the top wall**, and a **stop wall at the other end** takes the push of the plug (plugging a cable pushes about 20 N, which has to go into the wall, not into the solder joints); **two small tabs overhanging 0.8 mm** hold it down. The board goes in at a slant under the tabs and then drops flat; no part has to bend. A 0.5 to 1 mm **foam pad** under it stops buzzing |
| **Round microphone board (Ø13 to 13.8)** | in a **round seat** in a small bracket behind the Ø34 hole; a **foam ring** (about 1 mm) between the board's sound side and the wall around the hole seals the sound path; two printed tabs or one clip hold it. It is changed **from the front, with the cap off**; thin soft wires carry the six signals, with a notch to relieve the strain |
| **Switch boards** (the wheel's two switches, the key's two switches) | small pieces of perfboard (or the switches soldered on short wires) on printed posts; a printed clip each |
| **The cable** | the plug's own sleeve is held in a notch in the top wall; the first design needs the real plug's size |

For the **first bench test** nothing is mounted: the boards sit on the breadboard or on their wires.

## 10 · The body, designed to print without supports (owner's request, 2026-11-27)

**The owner:** the cap slide works and fits well, a little loose; the size is right; the look is good. Print the shells **with as few supports as possible**, by adding assembly structures rather than relying on supports. Assemble with **self-tapping screws** (as the owner's robots are).

**The rule used:** every part has a print orientation in which nothing overhangs more than 45° and no bridge is wider than about 12 mm, and anything that "hangs" hangs from the face that lies on the bed. That decides the body's structure:

| Part | Printed | Why no supports |
|---|---|---|
| **Lower frame** (the floor under the cap, its walls, the screw bosses, the microphone seat) | **cap-seat face down on the bed** | the floor is a flat profile on the bed: the keyholes, the catches and the hub's spokes are free; walls, bosses and the seat grow upward |
| **Upper shell** (the control zone, the wheel's tube, the board pocket, the key's hinge) | **front face down** | the same: everything hangs from the front wall and grows toward the back |
| **Back plate** | flat | a plate |
| **Cap** | front face down (pegs up) | the pegs' heads have a 39° cone underneath |
| Keys, wheel, small parts | flat | |

**Why two shells, not one:** the lower zone's floor sits 2.4 mm behind the control zone's face (the cap lies in that depth). In one piece, printed face down, the whole floor would float above the bed. So the body is split at the seam (y = 52, under the cap's top edge), joined by two alignment tabs, the flat back plate and the screws. A visible joint line runs across the sides at that height, like a panel gap.

**What changed in the cap's catch, and why:** the tongue with a bump (which the owner printed and liked) has its bump in front of the cap seat, which would sit **below** the bed when printed face down. It is replaced by an **in-plane catch at each keyhole**: a flat arm (0.9 × 7 mm) cut from the floor beside the slot, with a 0.6 mm nub pushing into the slot just behind the resting peg; the peg's neck pushes it aside while sliding and it springs back. It is all in the floor plane (a flat profile when printed), hidden under the cap, and the holding force is set by the nub and the arm (by hand calculation about 1.2 N per peg, 4.8 N for four, against about 2.4 N for the old tongue; PLA strain about 1.1 %, a little high: PETG is better). **New.** Owner's coupon test, 2026-11-27: C and D hold firmly and well, A and B are fine but may loosen; **C is now the default** (arm 1.2 mm), and the two left-hand catches' arms are moved to the outer side of their slots, because a check found the lower-left arm's root would have been cut away by the Ø34 round opening (the coupon had no such opening). Owner feedback, 2026-11-27: with the old tongue the cap "slides down too easily" (it does not rattle once seated), and bending the tongue up a little made the hold clearly firmer: the hold is set by the **preload (interference)**. So the catch's ramp that resists sliding down is now **steeper than the one the peg climbs when pushed up** (0.4 mm against 0.7 mm run for a 0.6 mm nub: about 56° against 49°), which raises the hold without making the push-up harder, and a **catch coupon** ([`../cad/catch_test.py`](../cad/catch_test.py)) has four strengths side by side (A the first design; B the new default; C a stiffer arm 1.2 mm; D a 0.8 mm nub) for the owner to choose from by feel. Rough hand figures (friction 0.35, PLA typical; only the ordering means anything): pull-down per peg A 2.5 N, B 4.6 N, C 11 N, D 14 N; strain 1.1 / 1.1 / 1.5 / 1.7 %. Also: neck 1.8 mm on a 1.6 mm floor (0.2 mm of play instead of 0.3), the pegs moved inboard (x = 11 and 37).

**The screws** (guidance read: pilot hole about the screw's outer diameter minus 0.4 mm, small vertical holes print small, boss outer diameter at least twice the screw, several wall perimeters round the boss, not for parts taken apart often; [Bambu forum](https://forum.bambulab.com/t/how-to-design-screw-holes-for-3d-printing/217352), [Hubs](https://www.hubs.com/blog/knowledge-base/how-assemble-3d-printed-parts-threaded-fasteners), [Hackaday](https://hackaday.com/2026/05/07/how-to-avoid-failed-screw-holes-in-3d-printed-parts/); the sources disagree on numbers):
- **M2 self-tapping, countersunk (flat head) as on the owner's robots, 8 mm long** (owner, 2026-11-27: M2 or M3, round or countersunk are all fine; the robots use M2 countersunk, and a flush countersunk screw is the cleaner retro look); the back plate gets a 90° countersink Ø4.2 (the head is about 3.8 to 4.0, to be measured) printed outer face down (a 45° limit-case overhang). Previously: pan head, 8 mm long (the plate is 1.8 mm, so about 6 mm in the boss); boss Ø5, a pilot hole **modelled at 1.9 mm** (the 1.6 mm rule plus 0.3 for the printed shrink seen in round 1); (the old plan: Ø2.4 holes with a Ø4.6 counterbore). Print the boss coupon (`boss_test_*.stl`: pilot holes of 1.7, 1.8, 1.9, 2.0 mm) to choose.
- Self-tapping screws wear the plastic if the back plate comes off many times: fine for a prototype; if it will be opened often, heat-set inserts are the alternative.

**Done and checked by numbers** ([`../cad/s2_frame.py`](../cad/s2_frame.py), [`../cad/check_s2_frame.py`](../cad/check_s2_frame.py)): the lower frame is a closed mesh; the cap seated on it does not touch it; during the slide only the four nubs meet the four necks; a dummy microphone board fits its seat; the **only overhang in the print orientation is the 12 mm wire slot in the end wall**. **Still to design:** the upper shell (control zone, wheel tube and the dial module, the board pocket, the key's hinge), the back plate (hatch, stand, hold-down for the microphone board), the key, the wheel.

## 11 · The upper shell and the back plate (first version, 2026-11-27)

Files: [`../cad/s2_upper.py`](../cad/s2_upper.py), [`../cad/s2_back.py`](../cad/s2_back.py), [`../cad/check_s2_upper.py`](../cad/check_s2_upper.py), [`../cad/assemble.py`](../cad/assemble.py); picture: [`../cad/out/preview_s2_body.png`](../cad/out/preview_s2_body.png). **Built and checked by numbers only; not printed; every size of a bought part is a typical value.**

**The upper shell** (y 52 to 88, printed **front face down**): 1.8 mm front wall, 1.6 mm walls, a **4 mm end wall** at the seam (it holds the two **alignment slots** for the lower frame's tabs and the wire slot), the **wheel's tube** (outer Ø25.4, bore Ø22.2 = wheel Ø21 plus 0.6 a side), the **board pocket**, the **USB-C opening** in the top wall, **two back-plate bosses** (16, 59) and (44.1, 56.5), and **two bosses for the dial module's plate**. The wheel's rim leaves through a window in the chamfer wall, as designed.
- **How each feature avoids supports:** walls, tube, pillars and bosses all hang from the front wall. The **dial module's seat is a 45° cone** (r 11.7 to 11.1 over 0.6 mm) with matching bevel on its plate, so the plate centres itself; the two M2 x 5 screws only draw it onto the seat (their bosses end 0.3 mm short of the plate's face). The **USB opening is a pentagon** (13 mm wide, 6.8 deep, corners cut at 45°: the flat ceiling is 6 mm). The **wire slot is a triangle** with 45° flanks (the lower frame's too: the 12 mm bridge there is gone). The alignment slots are 2.8 mm wide (a 3 mm bridge).
- **Facts the owner gave (2026-11-27, with photos):** the Super Mini is **23.5 × 18 mm without the USB-C's protruding part**, as on the official page (the 22.52 listing was a different product); the thickness is estimated as pcb 1.0 to 1.2 + USB-C 3.2 to 3.3 = **about 4.5 mm** (a guess, to be measured); **USB-C at one short end on the component face, BOOT and RESET right behind it on the same face, the ceramic antenna at the other end**. **The board now lies with its components facing the BACK**: the plug's axis (1.6 mm above the pcb) falls at mid depth (z 8.5), the pcb's bare face rests against four corner pillars from the front wall, two small hooks on the left wall overhang its back face by 0.8 mm (the board enters from the back at a slant), and BOOT / RESET are reached through an **11 × 3.4 mm slot in the back plate** about 7 mm from the board's end (position estimated from a photo: to be confirmed on the real board). The onboard RGB LED then faces the back (a lamp on the face needs its own LED).
- **The microphone board's sound inlet** is the small hole next to the microphone symbol on the silkscreen face (the gold can is on the other face; the sound goes through the pcb): **the symbol face must face the FRONT**, the opening in the hub's flange is now **Ø5.5, 2.8 mm off the centre** (the hole is about 3 mm off the board's centre; its exact place to be checked on the real board).
- **The board pocket** (an ESP32-S3 Super Mini, **23.5 x 18 mm per [espboards.dev](https://espboards.dev/esp32/esp32-s3-super-mini/); another listing says 22.52, so the longer is used; the thickness and the places of the USB-C, BOOT and RESET are not published on the pages read (checked 2026-11-27)**): a stop wall at the bottom (it takes the plug's push, as planned in §9), four 1.4 mm pillars that press on the pcb's front face at its corners, the tube as the right-hand guide; the board is pressed forward by the back plate with a spacer and foam (the back plate's posts are still to design). The pcb is placed with its components facing the front, so the USB-C's centre sits at the middle of the depth (z 8.6). The top-left corner of the cavity is relieved (the board's corner is square, the cavity's inner radius is 3.4), leaving a 1 mm skin.
- **Checked:** a closed mesh, one piece; it does not touch the lower frame or the cap; the frame's tabs enter the slots; a dummy board, can and plug fit; the wheel (Ø21, z 11.6 to 19) clears the bore. **Overhangs in the print orientation: no face steeper than 45°; the only ceilings are the 2.8 mm tab slots, the 6 mm USB flat, and one short bridge: the chamfer wall's window under the wheel (the wall continues behind the bore at z 11.2), about 12 mm at the outer face and 15.6 mm at the inner face, 1.6 mm thick.** That bridge is the one place that may need attention in the slicer (a 12 to 15 mm bridge of a 1.6 mm wall usually prints; if not, a thin rib across the window is the fix).

**The back plate** (1.8 mm, the full outline): printed **flat with its outer face up**, so the countersinks narrow downward and nothing overhangs; **seven M2 countersunk holes** (90° countersink Ø4.2) at the five lower and the two upper bosses; the outer edge rounded 1.2 mm. **Not yet in it:** the hatch, the BOOT/RESET access, the stand, the microphone hold-down posts and the board's spacer.

**Changes to the lower frame:** the **left boss at y = 46 is gone** and the left side has no boss between y 28 and 78 (the key's lane, below); the wire slot is a triangle.

**The key is not designed yet.** It lives on the left edge, y 30 to 76, so it crosses the seam; the lane x < 10, y 28 to 78 is kept free of bosses. Its window, hinge pin and the two switches need both shells to be cut, so they come next, together.

**Known weak points of this version (honest list):**
1. The upper half of the back plate is held only at y about 57 to 59 (two screws) and by the shell's walls: the board and the wheel take the corners where bosses would go. If the plate's top edge gaps, a post from the plate onto the tube, or a lip, is the fix; I have not found a better boss place.
2. The dial module (plate, cam, two switches, wheel's axle) is **not drawn**; only its seat and screws exist.
3. ~~The front-edge treatment~~ **Corrected 2026-11-27 (owner noticed the upper shell's edge was sharp while the cap's is rounded):** the cap has always had the spec's 1.5 mm front fillet on three sides, and I was wrong that a fillet on the bed face is a problem: after the first layer each layer steps out only 0.3 mm or less. The upper shell now has the **1.5 mm front fillet** too (not along the seam edge, which stays flush with the cap), the **wheel 1.0 mm**, and the **back plate's outer edge 1.7 mm**. Remaining worry: the wall at the fillet is 1.2 mm thick at its thinnest.

### The dial: wheel, plate, cam (first version, same day)
Files: [`../cad/s2_dial.py`](../cad/s2_dial.py). **Not printed. Switch-dependent parts are NOT decided.**
- **Wheel:** Ø21, 7.4 mm (2.0 proud of the face), 24 round grooves on the rim for grip, a **1.0 mm fillet** on the face edge, a **Ø3 D-shaped stub** behind it (to z 8.4). Printed face down. The stub passes the plate; the cam is **pressed onto the stub behind the plate** (D hole, 0.1 mm clearance): it is also what holds the wheel in. Axial play about 0.6 mm in all (the wheel can be pushed in a little).
- **Plate:** 1.2 mm, a 45° bevel that sits on the shell's cone seat, a Ø3.5 bearing hole, two ears with countersunk M2 x 5 screws into the two bosses; cut short on the chamfer-wall side and under the top and right walls.
- **Cam:** a disc Ø14.6 with **two arc ridges** on its back (0.8 high, 90° long each) that press the two switches at 150° and 270° around the axis; the wheel's four positions at 45° steps give **00, 01, 11, 10** (checked by calculation, each state 22.5° from a ridge end). The cam is **small (radius 7.3) because the chamfer wall passes only 7.7 mm from the wheel's axis**; the switches' button circle is therefore only 5.2 mm; the two 6 x 6 bodies at 150° and 270° do not overlap (at 180° and 270° they would).
- **Checked:** closed meshes; none of the dial's parts touches the shell, each other, or the dummy switches; no overhang steeper than 45° in the print orientation (the cam printed base down, ridges up).
- **Found and fixed while doing it:** the first cam (Ø20) hit the chamfer wall; the plate hit the upper wall and a back-plate boss; the ear bosses ended 0.3 mm on the wrong side of the plate; the back-plate boss moved to (44.4, 56).
- **Open, and needs the switches in hand:** a tact switch **bottoms out after about 0.3 mm**, so a rigid cam ridge is only right within about 0.1 mm: the printed tolerance is not that good. The fix is **compliance**: either (a) the switch carrier floats on a small spring or foam, (b) a printed flat finger (like the cap's catch arm, which is known to work) lies between cam and button and flexes the excess, or (c) a **lever micro switch** (about 1 to 2 yuan, travel of a millimetre or more) instead of the tact switch. **Owner (2026-11-27): no lever micro switch, solve it by design: (b) it is.** **The switch carrier (a part behind the cam, holding the two switches) is not drawn.**

## 12 · Next
1. ~~The owner prints `s2_cap_shell.stl`~~ done in round 3. Old text: the owner prints **`s2_cap_shell.stl`** (front up, supports from the bed under the detent tongue) and **`s2_cap_PRINT_face_down.stl`** ([`../cad/out/`](../cad/out/)) and tries the cap: does it go on, slide, click, hold, come off?
2. ~~The owner decides the wheel~~: **P chosen**.
3. Once the parts arrive and are measured, the full shells.
