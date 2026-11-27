# Decisions

What the owner has decided, and what is still open. Recorded from the discussion; newer entries override older ones. **Anything not listed under "Decided" is open**, including everything Claude has only proposed or recommended. See also [`discussion-log.md`](discussion-log.md) for the history and [`../design/concepts/v0.1/README.md`](../design/concepts/v0.1/README.md) for the picture.

## Decided (owner, up to 2026-11-26)

### Product
- A small, walkie-talkie-like handheld **USB microphone**. First of all a real microphone (the owner's laptop microphone is broken): voice input by push to talk, and a resident desk microphone.
- A hobby project: it can be playful, but **first versions stay simple**. Anything hard to build goes to the backlog.
- Wired USB-C for v0.1. No battery or wireless in v0.1 (space may be reserved).

### Interaction (v0.1, decided 2026-11-26; layout updated the same day)
- **Layout (updated 2026-11-26, replaces "wheel left, key right"):** the owner moved the wheel because the lower left is where the base of the thumb sits and is hard to reach. Follow the walkie-talkie / TE convention: **the push-to-talk key is on the left, in the upper half**; **our own wheel is on the right** (upper right or lower right, to be judged by which turns more easily; mode changes are rare). Claude's recommendation, not yet decided: a **top-right chamfered corner** ([`../design/concepts/v0.2/README.md`](../design/concepts/v0.2/README.md)).
- **The wheel** is an **edge roller** sunk into a pocket, with its **axis perpendicular to the face** (from the front it is a circle). It is a wheel, not a switch, because a wheel supports more positions.
- **Edges that stick out must not dig into the hand** (owner). Claude's starting numbers, not decided: key 5 mm out at most, radii 2 mm or more, wheel about 1 mm out.
- **The key** is **a mature TE-style big key with a few stages, fixed in position**. It may be slanted (like TE) or parallel to the edge. **No pop-up strip, no sleeve, no four-finger squeeze, in v0.1.**
- **No glowing window.**

### Front layout (owner, 2026-11-26, later)
- The v0.2 layout (key upper-left, wheel on the right) was accepted: "quite good".
- **Upper / lower structure:** controls, lamp and other parts in the **upper** part; **one big pickup area in the lower half**. (TE is the reverse: grille on top.)
- The pickup is a **round hole under a square cover plate** (a circle inside a square), the plate patterned as lines, slots or small holes. F1, F2 and F3 were all liked; F1's pickup was felt to be too small. Which pattern and colour is open ([`../design/concepts/v0.3/README.md`](../design/concepts/v0.3/README.md)).
- **Then (same day):** the owner prefers **the whole lower half as one cover plate** (like a ridged cover over a round hole, a dot-matrix grille, or a grid), rather than a small plate inset in the face; several patterns to choose from ([`../design/concepts/v0.4/README.md`](../design/concepts/v0.4/README.md)). The owner's references were used for the idea only.

### Refinements (owner, 2026-11-26, night)
- The prototype is accepted as "good looking"; the lid is replaceable anyway. Details to be polished, **designed with real mechanics and electronics in mind**, not as a pure styling exercise.
- **Colour:** default is a **dark/light, tone-on-tone** scheme, **not** the key's colour for the body or plate. The key is bright; the body one colour or a small tonal difference.
- **Panel:** more personal, with carefully designed lettering.
- **Lid:** **no screws**; a **snap-fit**, removable and swappable like a battery cover. The exact catch design is open ([`../design/concepts/v0.5/README.md`](../design/concepts/v0.5/README.md)).
- **Mode indication** and the rotary sensing are open (arc, row with guide lines, other); a top rotary knob for volume or gain is optional and later.

### Choices (owner, 2026-11-26, night)
- **Palette 1, WARM** (warm grey body, a shade deeper lid, orange key, dark wheel).
- **The dial** for showing the modes (the icons on the wheel, a fixed index on the body).
- **Labels: keep it simple**: stickers, or multi-colour (AMS-style) printing; no painting or filling.
- **A bigger wheel** (the owner; now 19 mm in the drawings) because the icons must be printed on it.
- **Wheel sensing: two switches and a cam**, with the sensors placed inboard to leave room.
- Next step (owner): **fix the part choices first**, then design a buildable version from the real part sizes. A proposal is in [`research/component-selection.md`](research/component-selection.md) and awaits confirmation.

### Look
- The front should carry **more of our own design** than TE's top-grille / bottom-cream split (owner, 2026-11-26); three compositions are drawn in v0.2.
- A TE-inspired **flat graphic language** applied on the surface (colour-blocked panels, small labels, pictograms, visible screws), with a **retro** feel, not a modern-tech or industrial/military one.
- **Beige with bright colours** (such as teal). The skins **SAND (beige + teal)** and **POPPY (cream + red)** were liked.
- Grilles: horizontal lines, vertical slots or dot-matrix. **No diagonal slots.**
- **Matte** 3D-printed parts. The round parts are printed in a matte material.
- **A coiled cable on top**, with USB-C on the top edge.

### Back
- A **small U stand** and a **small openable hatch** with pins inside for the user's own programs. **Not a full-back cover.**

## Frozen spec v0.1 (owner approved 2026-11-26)
The owner approved Claude's proposed freeze: [`spec-v0.1.md`](spec-v0.1.md). It records, as decided: body 58 × 92 × 24 mm; XIAO ESP32S3; INMP441 and ICS-43434 modules in a replaceable bracket (T5848 later if needed); the two-stage slanted key with a soft stop; the Ø19 mm dial wheel read by two switches and a cam; a PETG snap-fit lid with hooks and in-plane arms, G1 ridges by default; a BOOT/RESET access in the hatch; a general expansion space instead of a battery bay; parametric CAD in `cad/`. Printer: **Bambu Lab A1 mini** (no PETG yet, to be bought; multi-colour possible). Licences chosen by Claude at the owner's request: [`../LICENSING.md`](../LICENSING.md). The owner will buy the parts from [`parts-list.md`](parts-list.md) and does not hurry. CAD and mechanical design are now in scope ([`../CLAUDE.md`](../CLAUDE.md), Phase 2).

## Owner feedback after the round-1 prints (2026-11-26)
The body of 58 × 92 × 24 mm is **too thick and too wide**; make it slimmer and narrower (length may stay or shrink a little, keeping the look in proportion). The wheel size (Ø19) and how it sits in the pocket are good. Measured fits on the owner's printer: push fit 0.20 mm per side. Details: [`test-results/round-1.md`](test-results/round-1.md). The new body size is **to be chosen** from a size ladder (round 2).

## Chosen after round 2 (owner, 2026-11-26)
- **Body S2: 48 × 88 × 17 mm** (compact; slim; assembly must work but not squeezed to the extreme). **Key block: 5 mm** (the middle one was the most comfortable). **Wheel close to its pocket** (gap 0.6 mm). **The lid's snap arms are designed on the real body** (no miniature). No further size round. See [`mechanical-plan-S2.md`](mechanical-plan-S2.md).
- Noted by the owner: the **right hand is more comfortable** than the left (the right thumb reaches the wheel). The owner holds it in the left hand: **left or right layout is a question for the owner**.

## Owner direction on the cap, the hands and the wheel (2026-11-26, later)
- **The front must be one complete plane, running to the edge, with no frame, and no visible catches.** Snap or slide, whichever works; magnets are too complex. Claude researched the options: proposed a **keyhole slide with a hidden detent** ([`mechanical-plan-S2.md`](mechanical-plan-S2.md) §4); **not yet tested**.
- **Both hands:** no mirrored version. Left hand: thumb on the key, index finger on the wheel; right hand: index and middle fingers on the key, thumb on the wheel.
- **The wheel: bigger and thicker, a conspicuous hero.** **Option P chosen (owner, 2026-11-26): Ø21, standing 2 mm proud of the face** ([`mechanical-plan-S2.md`](mechanical-plan-S2.md) §8). The keyhole-slide cap was found "interesting, good" and will be printed to try.
- Hand size: no measuring needed (about an iPhone's); grip described (thumb reaches the middle finger's pad, barely the little finger, not the index finger).

## Purchases decided by the owner (2026-11-26)
The owner buys: an **ESP32-S3 Super Mini** (about 20 yuan; instead of the XIAO at about 50), an **ICS-43434 round module** (one piece), **6 × 6 through-hole tact switches** (10 to 20) from the microphone shop, and a caliper if one cannot be borrowed. The cable, wires and breadboard are the owner's own. The orders (the owner's screenshot): the "ESP32-S3-SuperMini" variant of a C3/S3/C6 listing (20.48 yuan), 6 × 6 × 4.3 through-hole tact switches, 20 pieces (0.69 yuan), and a **"domestic (国产) ICS-43434"** omnidirectional microphone module (11.55 yuan). **"Domestic" most likely means a compatible part, not necessarily the TDK chip**, so the datasheet figures of the TDK part (about 65 dBA signal-to-noise) are **not guaranteed** for this board; it is judged by listening. On arrival: photos of both sides of each board with a ruler and the seller's sizes; the shell's board pocket is designed around the Super Mini actually received ([`parts-list.md`](parts-list.md)).

## Firmware preparation (owner's go-ahead, 2026-11-26)
The owner left the order of work to Claude and allowed the firmware to be prepared ahead of the hardware. Prepared, **unbuilt and untested**: [`../firmware/`](../firmware/README.md): stage 1 is the upstream usb-mic project unchanged; stage 2 is a microphone plus a keyboard in one USB device (the BOOT button as the push-to-talk key). The owner builds, flashes and tests when the hardware arrives.

## Round-3 print results and the assembly direction (owner, 2026-11-27)
- The **keyhole-slide cap** was printed and **works very well**; it is **a little loose** (to be tightened). The size (S2) is "very suitable, small and refined"; the look "very good, a retro feel".
- **Assembly: M2 self-tapping screws** (as in the owner's robots). **Design the shells so they print with as few supports as possible**, by adding assembly structures instead.
- Screws (owner, 2026-11-27): **M2 self-tapping, countersunk head** (as in the owner's robots) for now; the body is not meant to be opened often, and what must be reached (later) goes behind the sliding cap. Heat-set inserts (pushed in with a soldering iron) are a method the owner has used and likes, and remain the fallback.
- Cap catch (owner): "slides down too easily", otherwise stable; a bowed (preloaded) tongue holds firmer: more preload wanted, strength to be chosen by feel from a coupon.
- **Catch strength (owner tried the coupon, 2026-11-27):** dots 1 and 2 (A, B) are fine for something opened often but may loosen with long use; dots 3 and 4 (C, D) are a little firmer and both good, nothing too tight. **Claude's choice: C** (arm 1.2 mm, nub 0.6 mm, ramps 0.7 / 0.4): the same firmness with the lower strain (1.5 % against 1.7 %), so it should creep less. Revisit when PETG is used (softer, so the hold will drop).
- **Owner (2026-11-27): "try it, and print with as few supports as possible; support hurts quality and is a pain to remove; use fixed assembly structures to avoid them."** Done as far as the shells go: see [`mechanical-plan-S2.md`](mechanical-plan-S2.md) §11 (the upper shell, the back plate; the front-edge fillet vs chamfer question is open for the owner).
- Claude's design choices in answer (**the owner may veto**): the body is split into a **lower frame and an upper shell** (each printed with its face on the bed) plus a flat back plate; the cap's catch becomes an in-plane catch at the keyholes; details in [`mechanical-plan-S2.md`](mechanical-plan-S2.md) §10.

## Proposed by Claude, **not** decided

- Modes on the wheel: **DICT, TALK, OPEN, LOCK**, with the wheel's click as a latch.
- The key's stages: hold to talk, a click to latch, a firm push to send (the TE lever's idea). Whether v0.1 has one, two or three is open.
- Stage-1 microphones: the INMP441 and the ICS-43434 modules together (the owner's Taobao prices make this cheap); T5848 later. A TING-style route (RP2350 + analog capsule + codec) is kept as a documented alternative ([`research/te-ting-reference.md`](research/te-ting-reference.md)).
- Key stage design (lesson from TE's lever): start on the soft first switch, a soft stop at the bottom, the microphone on foam; the second switch is a quiet latch confirm.
- Microphone staging: a cheap I2S module first, in the real body, then listen; a higher-SNR chip (for example T5848) only if the noise floor is audible; the pickup on a replaceable bracket reachable through the removable lid ([`research/microphone-quality.md`](research/microphone-quality.md)). A general expansion space instead of a dedicated battery bay.
- Hardware route: ESP32-S3 with an I2S digital microphone as the primary and an RP2040/RP2350 as the fallback, from [`research/claude-review.md`](research/claude-review.md). Nothing has been bought or tested.
- Body depth: about 22 mm is drawn; a thicker body squeezes better but is less pocketable ([`../design/squeeze-grip.md`](../design/squeeze-grip.md)).
- Hardware, CAD and software licences (MIT for software is the intent in the README; the rest is undecided).

## Moved to the backlog (not in v0.1)

See [`feature-backlog.md`](feature-backlog.md): the pop-up side strip with a sleeve; the four-finger squeeze; the glowing mode window; the walkie-talkie voice effect and other effects; a desktop pet; Bluetooth and battery; a removable cover system with printable plates.

## Not wanted

- A **rugged, military or industrial** look (the yellow walkie's bumper).
- Anything too **complex** for a first version.
