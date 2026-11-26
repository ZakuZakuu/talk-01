# Spec v0.1 (frozen 2026-11-26)

Frozen when the owner approved Claude's proposal ("agreed, go ahead"; the owner added: printer Bambu Lab A1 mini, no PETG yet, licence left to Claude). **A change to anything here needs the owner's OK** and is recorded in [`decisions.md`](decisions.md). Everything is **tentative until measured**: sizes marked *typical* come from datasheets or common values, not from parts in hand.

## 1 · Product
A small walkie-talkie-like **wired USB-C microphone**: a real microphone first (voice input by push to talk, and a resident desk microphone), a "small tool plus small toy". Wired, bus-powered; no battery or wireless in v0.1 (room is kept). Full background: [`decisions.md`](decisions.md).

## 2 · Body (mm; the face seen from the front, origin at the top-left)

> **S2 chosen by the owner, 2026-11-26** (after the round-1 and round-2 prints): the first body (58 × 92 × 24) was too thick and too wide. Plan: [`mechanical-plan-S2.md`](mechanical-plan-S2.md); results: [`test-results/round-1.md`](test-results/round-1.md).

| Item | Value |
|---|---|
| Outer size | **48 wide × 88 high × 17 deep** (slim; assembly to be confirmed with the real parts) |
| Plan corners | radius 5; the **top-right corner chamfered 15 mm** |
| Edge comfort | front perimeter fillet 1.5, back 2.0; no sharp edge under the hand |
| Control zone | the top 36 mm of the face (wordmark, lamp, small labels) |
| Cap (lid) | the lower face, **y 36 to 88**, edge to edge (47.8 × 51.75 mm); on top of 1.6 mm walls |
| Pickup | a round hole **Ø34** under the cap, centred 24 from the left and 63 from the top |

## 3 · The key (left edge, upper half)
- On the **left edge, y 12 to 58** (46 mm long), **slanted** (the TE-lever idea, our own shape).
- Sticks out **5 mm** (the owner found the middle block, 5 mm, the most comfortable), **11 mm deep**, radii 2 mm or more.
- **Two stages**: a soft first switch starts the talk (hold); a second switch at the bottom is a quiet latch confirm. A **rubber bump** at the bottom stop. The lesson from TE's lever is in [`research/te-ting-reference.md`](research/te-ting-reference.md).
- A spring returns the key; it turns on a steel pin at its bottom.

## 4 · The wheel (top-right chamfer): the "dial"
- **Ø19 mm, 5.4 mm thick**, in a pocket with a **0.6 mm gap** (the owner found 1.8 mm too big) centred at **(33.3, 12)** from the top-left; its rim sticks out of the chamfer by about 1.2 mm; 36 ribs on the rim; the axle hole 2.3 mm.
- **Four modes** DICT, TALK, OPEN, LOCK on the wheel face as 3 mm icons; a fixed index triangle on the body marks the active one (a camera mode dial). Four detents, 45° apart.
- **Sensing:** a cam on the wheel's back presses **two small switches** (Gray code 00, 01, 11, 10), the switches placed inboard. Absolute: the position is known at power-up.
- Icons: **stickers or multi-colour (AMS lite) inlays**.

## 5 · The cap (the lower lid; no screws, nothing visible)
- **PETG** is the aim (PLA for the tests); base about 1.0 mm plus **1.4 mm ridges**, 2.4 mm in all; **horizontal ridges** (G1) by default, with a plain band at the top; swappable.
- **One complete plane edge to edge, no frame, no visible catches** (owner, 2026-11-26). It lies on the body's walls and forms the front edge. Held by **four mushroom pegs on its back that slide 6 mm through keyholes in the floor** and a **small detent tongue** in the floor that clicks into a groove in the cap's back. Taken off by pushing it down 6 mm and lifting. Mechanism and open questions: [`mechanical-plan-S2.md`](mechanical-plan-S2.md) §4. A magnet version is the fallback.
- The cap's outline is the body's outline (0.1 mm inside); 0.15 mm gap to the control zone.
- The microphone **bracket** sits behind the round hole and can be changed from the front with the cap off.

## 6 · Electronics (stage 1)
| Role | Choice |
|---|---|
| Controller | **Seeed XIAO ESP32S3** (plain, not Sense); 21 × 17.5 mm; USB-C on top; wires, no custom PCB |
| Microphone | **INMP441 and ICS-43434 modules**, both tried in the same bracket; the T5848 later if needed |
| Key | two small switches (a silent type for the bottom one) |
| Wheel | two small switches and a printed cam |
| Cable | a coiled USB-C cable, bought, at the top edge |
| Space | a **general expansion space** (about 43 × 28 × 11 mm), not a battery bay |
| Back | a small **hatch with the pins** and a **BOOT/RESET access**; a **small U stand** |

Firmware is not part of this freeze: a bench test comes first ([`research/claude-review.md`](research/claude-review.md)). The key mapping stays configurable (Alt by default).

## 7 · Look
WARM (warm grey body, a shade deeper lid, orange key, dark wheel); circles and ridges; hand-drawn wordmark and pixel-dot labels. Pictures: [`../design/concepts/v0.6/README.md`](../design/concepts/v0.6/README.md), [`../design/concepts/v0.5/README.md`](../design/concepts/v0.5/README.md).

## 8 · Printing
Bambu Lab A1 mini: **180 × 180 × 180 mm**, 0.4 mm nozzle ([maker's listing](https://uk.store.bambulab.com/collections/a1-series/products/a1-mini)); **PLA now, PETG to buy** (the lid); AMS lite for colour. Every part must fit in the volume and print without supports where possible.

## 9 · Open (to be settled by measuring or testing)
- the real sizes of the controller, the microphone modules, the switches, the cable's plug (the measuring sheet in [`parts-list.md`](parts-list.md));
- the key protrusion (3, 5 or 7 mm) and the body's feel (mock-up);
- the lid clearance, the snap arms in PETG, the minimum rib gap, text and inlay sizes (calibration print);
- depth: the fit was tight (about 1.6 mm spare at 22 mm), so 24 mm is the working value;
- whether the plug sits near the back of the top edge (the board lies behind the wheel stack);
- the microphone choice (by recording), and any firmware.

## 10 · Process
Claude designs and checks by numbers; the owner prints, measures with calipers and reports (photos help); Claude revises. Files: [`../cad/README.md`](../cad/README.md).
