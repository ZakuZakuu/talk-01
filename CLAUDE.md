# Claude Code collaboration guide

## Context
talk.01 is a public open-source personal hobby project. Owner wants a compact, satisfying handheld USB microphone for frequent voice typing/AI conversations and occasional normal recording, with a built-in folding rear stand. Inspired by retro pager and radio instruments and Teenage Engineering's tactile design language; original product identity. Owner can assemble electronics and 3D-print parts. Low priority, limited weekly time.

Updated 2026-11-25 with the owner's clarifications (see docs/discussion-log.md): it must first be a real microphone (the owner's laptop mic is broken), usable for voice input and as a resident desk mic, and the interaction should be retro and fun. It is a "small tool plus small toy". Fun features are welcome but are not the core; see docs/feature-backlog.md.

The owner's converged decisions (2026-11-26) are in docs/decisions.md: read it first. Anything not listed there as decided is open.

Read README.md and docs/product-design.md, docs/hardware-research.md, docs/roadmap.md before working.

## First assignment
Act as an independent research and industrial-design collaborator, not an implementation agent yet.
1. Research mature and reproducible open-source USB microphone solutions. Audit upstream code, licenses and audio evidence. Compare alternatives, including non-S3 routes. Recommend a low-effort primary and fallback plus rough BOM.
2. Create 2–3 original flat 2D concept sheets (SVG and optionally PNG) with front/rear/side, built-in stand open/closed, and controls. Save under design/concepts/. Present tradeoffs, not a finalized design.
3. Participate in design discussion. Critically review interaction and technical assumptions; propose concrete options and a few questions for the owner.

Write research findings to docs/research/claude-review.md; summarize concept rationale in design/concepts/README.md. Use a branch/PR for first-round work if possible. Share links and explain unresolved risks. No need to build firmware or CAD or order hardware now. *(Superseded for CAD on 2026-11-26: see Phase 2 below.)*

## Constraints
Reuse mature code and modules wherever appropriate; focus on upper-layer UX and product design. No AI inference, custom driver, custom PCB or commercialization work in this phase. Wireless and battery are not part of v0.1 (keep space and a BLE-capable MCU in mind; the owner is open to them later if they turn out to be easy). Heavy or complex DSP (e.g. noise cancellation) stays out. Simple fixed effects, such as a walkie-talkie filter, are allowed as optional fun features after the core works; if an effect turns out hard or CPU-heavy, skip it rather than expand scope (owner decision, 2026-11-25). Do not import third-party assets/code without license verification. Prefer permissive licenses; separate hardware/CAD and software licensing. Do not claim hardware testing or sound quality without evidence. Avoid publishing personal details, secrets or proprietary assets. Keep discussion open and preserve owner decisions; no silent major changes. 

## Phase 2: mechanical design (approved by the owner, 2026-11-26)
The owner approved the frozen plan in docs/spec-v0.1.md and asked Claude to do the modelling and mechanical design.
- **Claude may:** model the enclosure and mechanics as parametric code (CadQuery) under `cad/`, export STL and STEP, run interference, clearance and printability checks, prepare test prints (a feel mock-up and a calibration set), and keep the parts list and measuring sheet in docs/parts-list.md.
- **Firmware (owner's go-ahead, 2026-11-26): Claude may prepare firmware source code and a bring-up guide** under `firmware/` ahead of the hardware, **clearly marked as unbuilt and untested** until the owner builds and runs it. The owner does the building, flashing and recording.
- **Autonomy (owner, 2026-11-26):** the owner leaves the order of work to Claude. Claude stops and asks when the next step needs the owner to test or decide, when a decision in docs/decisions.md or the frozen spec would change, or when Claude cannot verify something itself.
- **Still needs the owner's explicit go-ahead:** ordering or buying hardware, flashing firmware onto a device, a custom PCB, changing a decision listed in docs/decisions.md or the frozen spec, publishing outside the repository.
- **Working loop:** Claude designs and checks by numbers; the owner prints, measures real parts with calipers and holds the result; Claude revises from the measurements and photos. Claude cannot print, feel, or measure real parts, and says so; sizes from datasheets or typical values are marked as such until measured.
- **Printer:** Bambu Lab A1 mini (build volume 180 x 180 x 180 mm, 0.4 mm nozzle; PLA now, PETG to be bought; multi-colour printing possible with an AMS lite). Keep every part inside that volume and printable without supports where possible.
- **Licences** are in LICENSING.md (MIT software, CERN-OHL-P-2.0 hardware files, CC BY 4.0 documentation).
- Hardware and CAD files stay in the repository; announce nothing publicly until the owner decides.
