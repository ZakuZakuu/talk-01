# Discussion log

A running record of owner direction and open questions, so decisions are not lost or silently changed. Newest entry first. Entries record what the owner said; they are not specifications. Nothing here overrides the owner.

## 2026-11-25 — first discussion with Claude

### Owner direction

**Why this exists (stated later the same day)**
- The owner's laptop microphone is broken (very quiet), and is also unclear in voice chats with friends. So the device is first of all **a real microphone**: voice input by holding the lever, **and** a resident desk / external microphone for calls and ordinary use.
- The interaction must be **fun and retro** (big lever or big button, walkie-talkie feel), not a plain mic. Both matter: it is a proper microphone, and the interaction has to be enjoyable.
- Connectors, battery, standalone use and Bluetooth/wireless are **undecided**. A wired first version is acceptable. Wireless is welcome *if it is easy*; the repository's earlier "no wireless" line is not a hard owner rule. The owner asks for Claude's opinion.
- Owner wants a **walkie-talkie effect mode**: press makes a "beep", voice sounds radio-like (band-limited, hissy), a short "squelch" on release. It would be a fun mode; **dictation and open-mic are the two practical modes**. Copying the idea of TE FX MIC's built-in effects is welcome. **Conflict to resolve:** `CLAUDE.md` says "no complex DSP in this phase". Claude's view: a few fixed filters are simple DSP, but this is the owner's call, so the constraint was **not** changed at first. **Resolved later the same day:** the owner said `CLAUDE.md` can be changed since nothing is settled, and the constraint was updated to allow simple fixed effects as optional fun features.
- Owner prefers the fun ideas to be recorded as optional features, **not core**. Rule: feasible → do it; hard or CPU-heavy → skip. A small buzzer is fine if it is easy; the other party hearing the beep is enough, hearing it locally is optional. A desktop-pet promo idea was recorded in [`feature-backlog.md`](feature-backlog.md).
- Bluetooth: owner expects it would mostly be used for input and chat, not for recording, so lower audio quality is acceptable there; a wired desk version is preferred for desktop use. Not for v1.0, only reserve space and keep a BLE-capable MCU.
- Typical desk use: laptop on a desk, device on the owner's **left**, roughly 30–60 cm away; a stand that brings it closer (e.g. next to the keyboard, about 30 cm) is welcome.

- The immediate use case is **voice input while "web coding" with an AI assistant**, so the device is mostly used at a desk with a laptop.

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

**Feedback on the first concept sketches (2026-11-25)**
- The owner prefers **A (Pager)** and **C (Radio)**, portrait, over **B (Telegraph)**, which is parked, not deleted. B may be influenced by the reference product; the owner is open to either.
- **USB-C should be on the top**, not the right edge, since the device sits on a desk.
- Wants more **small clever details**: look at retro devices, Teenage Engineering and Nothing for ideas.
- **Removable cover plates** (battery or hidden info underneath, users can 3D print their own) are considered a key idea for a toy / hackable device.
- The device will be carried in a bag, so the **lever needs protection** (slide cover or fold-over guard) against being pressed or damaged.
- **Ergonomics**: right hand is on the mouse, so the **left hand holds** it and the **left thumb** presses the left-edge lever. A small round **thumb dial at a corner** for mode switching, with a nice feel, is suggested.
- The prototype should also work as an **EDC fidget toy** even without function; make it playful.
- All of these are brainstorm points, not commitments.
- Research and Claude's ideas: [`../design/inspiration.md`](../design/inspiration.md).

**Three-stage lever and round 2 brief (2026-11-25)**
- The owner likes the three-stage lever and described the stages: light press = hold to talk; pressing to the bottom = **latch**; an extra bit of force at the bottom = **send**. Mechanics can be sorted out later; the feel matters most.
- Round 2 brief: new, more novel directions, **not a random mash-up**. Each concept should have clear tradeoffs and be self-consistent. No strong preference yet; the aim is a good final product. Result: [`../design/concepts/round-2/README.md`](../design/concepts/round-2/README.md).

**Feedback on round 2 (2026-11-25)**
- No colour stands out and none is disliked: "all fine". Colour is not the issue.
- Overall the three designs "fall short" and do not catch the eye compared with Teenage Engineering, Nothing and Braun-style products. Quality bar: **on par with TE is the aim; slightly worse with room to improve is acceptable**.
- TE looks minimal at a glance but is intricate up close; the owner wants that. The FX MIC's slanted side button is very eye-catching.
- Wants **bolder, more radical** options and for Claude to research the designers' philosophy and interviews and learn from them.
- The owner is not a designer and can only tell by feel what suits their taste. So: show many options and let the owner react.
- **The back cover should not be the whole back.** The stand should be a **small U shape**, or the **cover and stand combined**.
- Research and the resulting checklist: [`../design/design-principles.md`](../design/design-principles.md). Round 3: [`../design/concepts/round-3/README.md`](../design/concepts/round-3/README.md).

**Feedback on round 3 and the new brief (2026-11-25)**
- Round 3 was **too aggressive**: flip, tilt and layers went too far. The owner still values the creativity.
- **Cut** is the preferred shape. The owner still wants a device that **starts from a walkie-talkie**, because it is something you talk into; the favourite reference remains the TE FX MIC.
- The **coiled cable** is an important point. The shape does not have to be a rectangle; Cut or MP3-player-like shapes are fine.
- Core function: **push to talk**. Body: **a small walkie-talkie-like handheld**.
- Inspiration may range widely: walkie-talkie, push-to-talk, telegraph, **cassette players, CD players, game consoles, phones, Walkman, cameras, old Macs, Game Boy**, up to about the year 2000. Combine them with TE's flat graphic language.
- Results: [`../design/concepts/round-4/README.md`](../design/concepts/round-4/README.md) and [`../design/brainstorm-retro.md`](../design/brainstorm-retro.md).

**Feedback on round 4 (2026-11-25)**
- Cut was only the closest; the owner did **not** want it refined, but wanted **more varied** designs.
- Round 4 felt **too modern and technical**, not "retro tech". Starting from walkie-talkies, it should feel properly old.
- **Diagonal slots are out.** Preferred grilles: **horizontal lines, vertical slots, or dot-matrix perforations**. TE colours whole panels differently; the owner likes that.
- The owner was dissatisfied just from the images and had not read the rest. Claude should **find many more reference photos of old devices** and design from them. Visual quality is judged first.
- Results: [`../design/concepts/round-5/README.md`](../design/concepts/round-5/README.md).

**Feedback on round 5 and the side-strip idea (2026-11-25)**
- Round 5 was much better and "very distinctive". The **first design (TPS)** resonated most, especially its **separate long strip on the left**.
- **Idea:** make the **whole left side the push-to-talk key**: spring it up (possibly with a cut top corner or an inset design); press to talk, press further to send; then a **sliding sleeve or similar holds it down** so the body is a full rectangle again. This protects the key in a bag. It can also be **only part** of the side that pops up, with a sleeve holding the rest.
- **Ergonomics (left hand):** thumb presses; can other fingers use keys, or a lever under the thumb pad? Design from the **few key interactions**: hold to talk, switch mode, mode switching, at most power.
- **Back:** a **small U stand** and a **small openable hatch** with pins so users can write programs.
- **Materials and colour:** the round parts will be **matte 3D prints**. Palette: retro **beige with bright colours such as teal**; multicolour, like the old Mac, Windows and Chrome logos.
- The owner sent four reference photos (cream-teal-lavender micro-cassette deck render, stacked compo stereo with screws and orange translucent keys, translucent-blue-record turntable, cream-teal boombox). Not stored in the repo.
- Results: [`../design/concepts/round-6/README.md`](../design/concepts/round-6/README.md).

**New direction: grip to talk (2026-11-25, late)**
- The owner asked whether the design is "locked into TE's key on the left", and proposed: **the left hand holds the device, the four fingers squeeze to talk, and the left thumb rolls a wheel to change mode.** Asked for several designs and overnight research; the owner went to sleep.
- Results: research [`../design/squeeze-grip.md`](../design/squeeze-grip.md) and six designs [`../design/concepts/round-7/README.md`](../design/concepts/round-7/README.md).
- Claude corrected an earlier assumption: the TE lever is described as **squeezed**, not thumb-pressed.

**More references and the wheel direction (2026-11-25, morning)**
- Two new references: a real yellow walkie-talkie (too industrial and military; the owner still prefers TE) and a dark gadget with a glowing screwed window, a seven-dimple speaker and a ribbed roller sunk in a corner pocket.
- **Wheel:** the first reference's twisted top knob is "the wrong direction". The owner wants a **roller sunk into the edge**, not necessarily in a corner (the sunk-in feel is the point). The owner's interaction: **thumb switches; the other side presses to talk** (Claude read "the right hand" as the right-hand side, where the fingers are).
- Results: [`../design/concepts/round-8/README.md`](../design/concepts/round-8/README.md).

### Claude's notes from the discussion

- TE's recognisable elements are the **perforated dot-matrix grille, the single saturated lever and the two-tone split body** (observed from one marketing render). Our concepts should not reproduce that combination. Our real differentiators are the **built-in rear stand** and **USB audio + keyboard in one cable**; the stand could be made a visual feature rather than a hidden mechanism.
- Because short taps are common, lever press and release should send the key **immediately**, with no gesture-detection delay. Gestures that need a timing window (such as double-tap) should be designed carefully or moved to a separate control.
- Technical research: see [`research/claude-review.md`](research/claude-review.md).

### Open questions for the owner (no hurry)

1. **Holding style** — walkie-talkie to the mouth, held at chest height, or mostly on the desk on its stand? This decides mic port position and which side the lever sits.
2. ~~Using it with speakers~~ — withdrawn. Claude misread a voice-input sentence; the owner never asked for speaker output. If a built-in speaker is wanted, say so.
3. **Mode switch** — see the proposal in Claude's reply on 2026-11-25: three lever behaviours (dictate / talk / open). Does that match what you imagine?
4. **Power and wireless** — wired USB-C only for v0.1 with room reserved for a later battery, or should the first shell already include batteries? (Claude's recommendation is in the chat reply; not yet decided.)
5. **Hardware license** — any preference for the enclosure and PCB files later? (No rush; only needed before design files are published.)
6. **Concept direction** — any pager, telegraph, radio or other objects you love the look of? Photos would help set proportion and details.
