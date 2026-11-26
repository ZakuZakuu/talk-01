# Round 1 prints: results (owner, 2026-11-26)

Printer: Bambu Lab A1 mini, PLA, 0.4 mm nozzle, 0.2 mm layers. Files: [`../../cad/`](../../cad/README.md). The owner reported by text and one photo; **what is marked "from the photo" is my reading of a small, angled picture and needs the owner's confirmation.**

## Results

| Test | Result | Consequence |
|---|---|---|
| Clearance tabs (per side: 1 = 0.15, 2 = 0.20, 3 = 0.25, 4 = 0.30, 5 = 0.40 mm) | **2 (0.20) is best**: it holds, presses in with a solid feel. 1 (0.15) is too tight, hard to press in fully. 3 (0.25) presses fully in, a little loose. **4 and 5 fall out.** | push fit **0.20 mm per side**; 0.25 for parts that must come out |
| Wheel in the body | the wheel sits in its pocket and **turns without wobble**; the size is good | keep Ø19 |
| Axle hole in the **body** (2.3 mm) | right | keep |
| Axle hole in the **wheel** (2.0 mm) | **far too tight**: a 1.75 mm filament could barely be pushed in a little | wheel hole 2.3 mm; small round holes print about 0.3 mm small |
| Size and feel (58 × 92 × 24) | **too thick**: the index finger cannot reach the wheel in the top-right corner. **Too wide** to grip well; the owner's hand is large-ish and it was tiring, so smaller hands (women, children) would struggle. Length is fine, could shrink a little, but the look has to be kept in proportion | slimmer and narrower: the size ladder of round 2 |
| Snap lid in its frame | once in, **it could not be taken out** | a design fault of mine: no way to get a nail under the lid; fixed in round 2 |
| Ridge groups, through-slots, raised lines (from the photo) | all three ridge groups look clean; all five slots look open; the raised lines look printed | to be confirmed by the owner |
| Key blocks 3, 5 and 7 mm | **not reported yet** | asked again |
| Did the snap lid click? Did an arm break? | **not reported yet** | asked again |

## What changes
1. Fit numbers in `cad/params.py`: push fit 0.20, lid 0.25, small holes +0.30, the wheel hole 2.3 mm.
2. A size ladder (S1 52 × 90 × 20, S2 48 × 88 × 17, S3 46 × 86 × 15) to hold and compare, with paper-fit notes ([`../print-test-guide/round2-size-ladder.png`](../print-test-guide/round2-size-ladder.png)).
3. A new snap pair with a **finger slot** under the lid's bottom edge, a scoop to the floor, a clearance of 0.25 and two bump sizes (0.8 and 0.5 mm).
