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

### Look
- The front should carry **more of our own design** than TE's top-grille / bottom-cream split (owner, 2026-11-26); three compositions are drawn in v0.2.
- A TE-inspired **flat graphic language** applied on the surface (colour-blocked panels, small labels, pictograms, visible screws), with a **retro** feel, not a modern-tech or industrial/military one.
- **Beige with bright colours** (such as teal). The skins **SAND (beige + teal)** and **POPPY (cream + red)** were liked.
- Grilles: horizontal lines, vertical slots or dot-matrix. **No diagonal slots.**
- **Matte** 3D-printed parts. The round parts are printed in a matte material.
- **A coiled cable on top**, with USB-C on the top edge.

### Back
- A **small U stand** and a **small openable hatch** with pins inside for the user's own programs. **Not a full-back cover.**

## Proposed by Claude, **not** decided

- Modes on the wheel: **DICT, TALK, OPEN, LOCK**, with the wheel's click as a latch.
- The key's stages: hold to talk, a click to latch, a firm push to send (the TE lever's idea). Whether v0.1 has one, two or three is open.
- Hardware route: ESP32-S3 with an I2S digital microphone as the primary and an RP2040/RP2350 as the fallback, from [`research/claude-review.md`](research/claude-review.md). Nothing has been bought or tested.
- Body depth: about 22 mm is drawn; a thicker body squeezes better but is less pocketable ([`../design/squeeze-grip.md`](../design/squeeze-grip.md)).
- Hardware, CAD and software licences (MIT for software is the intent in the README; the rest is undecided).

## Moved to the backlog (not in v0.1)

See [`feature-backlog.md`](feature-backlog.md): the pop-up side strip with a sleeve; the four-finger squeeze; the glowing mode window; the walkie-talkie voice effect and other effects; a desktop pet; Bluetooth and battery; a removable cover system with printable plates.

## Not wanted

- A **rugged, military or industrial** look (the yellow walkie's bumper).
- Anything too **complex** for a first version.
