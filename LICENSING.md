# Licensing

Chosen 2026-11-26 by Claude, as the owner asked ("pick the most suitable"). The owner can change it before the first public release; a change affects only later releases. This is a practical choice, **not legal advice**.

| What | Licence | Where |
|---|---|---|
| **Software**: scripts, generators, later firmware | [MIT](LICENSES/MIT.txt) (`SPDX: MIT`) | `design/concepts/src/`, future firmware |
| **Hardware design files**: parametric CAD, STL, STEP, drawings of the parts | [CERN-OHL-P-2.0](LICENSES/CERN-OHL-P-2.0.txt) (`SPDX: CERN-OHL-P-2.0`) | `cad/` |
| **Documentation and artwork**: text, concept sheets, images, diagrams | [CC BY 4.0](LICENSES/CC-BY-4.0.txt) (`SPDX: CC-BY-4.0`) | `docs/`, `design/` (except `design/concepts/src/`), `README.md` |

## Why these

- `CLAUDE.md` asks to prefer permissive licences and to keep hardware/CAD and software licensing separate.
- **MIT** is the usual permissive software licence and matches the earlier stated intent.
- **CERN-OHL-P-2.0** is the permissive variant of the CERN Open Hardware Licence v2, written for hardware design files (software licences and Creative Commons were not written for hardware). Anyone may build, modify and sell, keeping the notices. It is the hardware counterpart of MIT.
- **CC BY 4.0** suits text and pictures: free reuse with credit.

## Not covered

- The **name and logo "talk.01"**: no trademark rights are granted by these licences.
- **Third-party material** keeps its own licence. The owner's reference pictures are not stored here, and nothing from them is copied.
- Code from other projects is only used if its licence allows it. Notably the repository `JR-One-Yard/ep-2350-usb-mic` has no licence file, so **none of its code is used**; the Adafruit TING demo is MIT and may be reused with attribution ([`docs/research/te-ting-reference.md`](docs/research/te-ting-reference.md)).

## A trade-off to know

Permissive licences allow closed-source derivatives, including commercial ones. If the owner later prefers that improvements stay open, the alternatives are CERN-OHL-S-2.0 (strongly reciprocal) for hardware and a copyleft licence for software. This was weighed and the permissive route chosen because it matches the stated preference.
