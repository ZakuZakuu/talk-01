# Spec v0.1 (frozen 2026-11-26)

Frozen when the owner approved Claude's proposal ("agreed, go ahead"; the owner added: printer Bambu Lab A1 mini, no PETG yet, licence left to Claude). **A change to anything here needs the owner's OK** and is recorded in [`decisions.md`](decisions.md). Everything is **tentative until measured**: sizes marked *typical* come from datasheets or common values, not from parts in hand.

## 1 · Product
A small walkie-talkie-like **wired USB-C microphone**: a real microphone first (voice input by push to talk, and a resident desk microphone), a "small tool plus small toy". Wired, bus-powered; no battery or wireless in v0.1 (room is kept). Full background: [`decisions.md`](decisions.md).

## 2 · Body (mm; the face seen from the front, origin at the top-left)

| Item | Value |
|---|---|
| Outer size | **58 wide × 92 high × 24 deep** (24 chosen over 22 so the real parts fit; to be re-checked) |
| Plan corners | radius 5; the **top-right corner chamfered 15 mm** |
| Edge comfort | front perimeter fillet 1.5, back 2.0; no sharp edge under the hand |
| Control zone | the top 36 mm of the face (wordmark, lamp, small labels) |
| Lid | the whole lower part, **y 36 to 92, full width** |
| Pickup | a round hole **Ø38 at (29, 64)** under the lid |

## 3 · The key (left edge, upper half)
- On the **left edge, y 12 to 58** (46 mm long), **slanted** (the TE-lever idea, our own shape).
- Sticks out **5 mm at most** (the feel mock-up compares **3, 5 and 7 mm**), **12 mm deep**, radii 2 mm or more.
- **Two stages**: a soft first switch starts the talk (hold); a second switch at the bottom is a quiet latch confirm. A **rubber bump** at the bottom stop. The lesson from TE's lever is in [`research/te-ting-reference.md`](research/te-ting-reference.md).
- A spring returns the key; it turns on a steel pin at its bottom.

## 4 · The wheel (top-right chamfer): the "dial"
- **Ø19 mm, 5.4 mm thick**, in a Ø22.6 pocket centred at **(43.3, 12)**; its rim sticks out of the chamfer by about 1.2 mm; 36 ribs on the rim.
- **Four modes** DICT, TALK, OPEN, LOCK on the wheel face as 3 mm icons; a fixed index triangle on the body marks the active one (a camera mode dial). Four detents, 45° apart.
- **Sensing:** a cam on the wheel's back presses **two small switches** (Gray code 00, 01, 11, 10), the switches placed inboard. Absolute: the position is known at power-up.
- Icons: **stickers or multi-colour (AMS lite) inlays**.

## 5 · The lid (no screws)
- **PETG**; base about 1.0 mm plus **1.4 mm ridges**, 2.4 mm in all; **horizontal ridges** (G1) by default, swappable (other patterns later).
- Held by **two rigid hooks** at the top edge and **two in-plane snap arms** at the bottom corners; a **thumb notch** at the bottom edge. Starting clearance 0.2 to 0.3 mm, to be set by the calibration print.
- The microphone **bracket** sits behind the round hole and can be changed from the front with the lid off.

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
