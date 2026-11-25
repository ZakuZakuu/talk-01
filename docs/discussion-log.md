# Discussion log

A running record of owner direction and open questions, so decisions are not lost or silently changed. Newest entry first. Entries record what the owner said; they are not specifications. Nothing here overrides the owner.

## 2026-11-25 — first discussion with Claude

### Owner direction

**Positioning**
- This is a **toy-like object that is a little useful**, not a strictly practical product. The reference attitude is Teenage Engineering: products that are not necessary but create desire. The owner likes the design language but finds TE products expensive and functionally mismatched.
- Closest inspiration: TE **EP-2350 FX MIC** (grey perforated grille on top, off-white lower panel, orange side lever, small side buttons). Inspiration, not copying; we should improve on it and bring our own identity.
- Keep it **open and hackable**: an SDK for second-party development is a nice later idea; users might connect it to other gear such as speakers.
- The mic is an **input peripheral** for voice-input software. Alt for WeChat Input is the owner's current daily workflow; other voice-input software (e.g. Typeless) should also work, so **the key mapping must be configurable**.
- Voice effects like TE's are not excluded as a *future* idea. They are outside this phase's scope (see `CLAUDE.md` constraints).
- Open-sourcing or selling are "later". For now: hobby pace, no seriousness required, no deadlines.

**Interaction**
- Holding Alt works well in daily use; **no concern** about it. (Claude's initial worry about Alt-key side effects is withdrawn.)
- Typical use is **short press, speak, release** ("say it when it comes to mind"); long holds are acceptable but not the main pattern. Long hands-free dictation helpers are a possible small interaction idea to explore later.
- **Double-tap to send** was a passing thought, not a decision.
- A mode switch (for example a "desk-resident microphone" mode and other modes) is wanted in some form; details later.

**Design**
- Owner is unsure whether the preferred style is Bauhaus or Braun. Claude's reading: functional minimalism in the Dieter Rams / Braun lineage, with a playful, saturated-accent attitude closer to TE. Terminology is not important now.

**Resources**
- FDM 3D printer available; owner is a model-maker and is comfortable with surface finishing and painting.
- An ESP32-C3 is on hand. Per `hardware-research.md` it cannot act as the USB audio + HID device, so it is only for interaction experiments.

### Claude's notes from the discussion

- TE's recognisable elements are the **perforated dot-matrix grille, the single saturated lever and the two-tone split body** (observed from one marketing render). Our concepts should not reproduce that combination. Our real differentiators are the **built-in rear stand** and **USB audio + keyboard in one cable**; the stand could be made a visual feature rather than a hidden mechanism.
- Because short taps are common, lever press and release should send the key **immediately**, with no gesture-detection delay. Gestures that need a timing window (such as double-tap) should be designed carefully or moved to a separate control.
- Technical research: see [`research/claude-review.md`](research/claude-review.md).

### Open questions for the owner (no hurry)

1. **Holding style** — walkie-talkie to the mouth, held at chest height, or mostly on the desk on its stand? This decides mic port position and which side the lever sits.
2. **Using it with speakers** — a USB microphone cannot drive a speaker by itself. What did you picture: a line-out jack on the device, a USB-C host/dongle setup, or just "works with a speaker that has a USB port"? This could change the electronics a lot, so we should decide whether it is in or out of v0.1.
3. **Mode switch** — what should the modes be, in your head? (For example: voice-input / always-on desk mic / muted.)
4. **Hardware license** — any preference for the enclosure and PCB files later? (No rush; only needed before design files are published.)
5. **Concept direction** — any pager, telegraph, radio or other objects you love the look of? Photos would help set proportion and details.
