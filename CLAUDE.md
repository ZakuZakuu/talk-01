# Claude Code collaboration guide

## Context
talk.01 is a public open-source personal hobby project. Owner wants a compact, satisfying handheld USB microphone for frequent voice typing/AI conversations and occasional normal recording, with a built-in folding rear stand. Inspired by retro pager and radio instruments and Teenage Engineering's tactile design language; original product identity. Owner can assemble electronics and 3D-print parts. Low priority, limited weekly time.

Updated 2026-11-25 with the owner's clarifications (see docs/discussion-log.md): it must first be a real microphone (the owner's laptop mic is broken), usable for voice input and as a resident desk mic, and the interaction should be retro and fun. It is a "small tool plus small toy". Fun features are welcome but are not the core; see docs/feature-backlog.md.

Read README.md and docs/product-design.md, docs/hardware-research.md, docs/roadmap.md before working.

## First assignment
Act as an independent research and industrial-design collaborator, not an implementation agent yet.
1. Research mature and reproducible open-source USB microphone solutions. Audit upstream code, licenses and audio evidence. Compare alternatives, including non-S3 routes. Recommend a low-effort primary and fallback plus rough BOM.
2. Create 2–3 original flat 2D concept sheets (SVG and optionally PNG) with front/rear/side, built-in stand open/closed, and controls. Save under design/concepts/. Present tradeoffs, not a finalized design.
3. Participate in design discussion. Critically review interaction and technical assumptions; propose concrete options and a few questions for the owner.

Write research findings to docs/research/claude-review.md; summarize concept rationale in design/concepts/README.md. Use a branch/PR for first-round work if possible. Share links and explain unresolved risks. No need to build firmware or CAD or order hardware now.

## Constraints
Reuse mature code and modules wherever appropriate; focus on upper-layer UX and product design. No AI inference, custom driver, custom PCB or commercialization work in this phase. Wireless and battery are not part of v0.1 (keep space and a BLE-capable MCU in mind; the owner is open to them later if they turn out to be easy). Heavy or complex DSP (e.g. noise cancellation) stays out. Simple fixed effects, such as a walkie-talkie filter, are allowed as optional fun features after the core works; if an effect turns out hard or CPU-heavy, skip it rather than expand scope (owner decision, 2026-11-25). Do not import third-party assets/code without license verification. Prefer permissive licenses; separate hardware/CAD and software licensing. Do not claim hardware testing or sound quality without evidence. Avoid publishing personal details, secrets or proprietary assets. Keep discussion open and preserve owner decisions; no silent major changes. 
