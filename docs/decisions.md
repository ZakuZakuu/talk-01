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
