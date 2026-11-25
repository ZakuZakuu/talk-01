# Feature backlog

Ideas from brainstorming. **Not commitments.** Rule agreed with the owner (2026-11-25): *if it is feasible, do it; if it is hard or needs a lot of CPU, skip it.* Core comes first; fun features come after the core works, when there is spare time.

Difficulty notes are Claude's rough estimates from reading and general knowledge, not measurements.

## Core (v0.1)

| Feature | Notes |
|---|---|
| USB-C wired, works as a normal USB microphone | Primary job. Replaces the owner's broken laptop mic. |
| Voice-input lever (hold to send a configurable key; Alt for WeChat Input by default) | Key mapping must be configurable for other voice-input software. |
| Open-mic desk mode | Ordinary always-on microphone. Desk distance (30–60 cm) is the hardest audio case. |
| Built-in folding rear stand | Must aim the mic port at the mouth; isolate from desk vibration. |
| Visible mode state | A radio band-switch style selector is one candidate; to be explored in concepts. |

## Fun features (optional, after the core works)

| Idea | Source | Notes / difficulty guess | Status |
|---|---|---|---|
| **Walkie-talkie mode**: press "beep", band-limited radio voice, squelch on release | Owner | A few fixed filters plus synthesized tones; easy. Needs device-side gating (send zeros when lever is up). | Idea |
| **Other TE-FX-style effects** (robot, echo, ...) | Owner | Robot and echo: easy to medium. Pitch shift and spring reverb: medium. Skip anything CPU-heavy. | Idea |
| **Small buzzer** for local "beep" and as a status indicator | Owner | Cheap part, one GPIO. Place away from the mic and make it mutable, because the buzzer can leak into the mic and into recordings. Reserve the footprint rather than commit. | Idea |
| **Desktop pet** that raises a walkie-talkie when the lever is pressed; doubles as a promo video concept | Owner | Needs the host to know lever/mode state: either read the configured key, or expose a documented device event channel (e.g. a HID vendor report or serial port). Use an **original** character; do not use third-party mascots or brand assets without checking their terms. | Idea |
| **SDK for second-party development** | Owner | Start with a documented event/config interface. Community can add more play. | Later |
| **Bluetooth / wireless, battery** | Owner | Owner expects mostly input and chat use, where lower audio quality is fine. The chosen MCU should be BLE-capable and space reserved. Not v0.1. Windows support for Bluetooth LE audio microphones not yet researched. | Later |

## Design-level ideas (decide before CAD; see `design/inspiration.md`)

| Idea | Notes |
|---|---|
| USB-C on the top edge | Owner request; avoids a cable at the desk-contact edge. |
| Three-stage lever: light press = hold to talk; bottom-out click = latch; extra firm push = send | Owner's description. Avoids timed gestures. Inspired by the TE FX MIC lever's three sensors. Needs a slightly compliant stop (or a Hall sensor with thresholds). Release of the latch is not decided. |
| **Side-strip push-to-talk key** with a **sliding sleeve** that holds it flush (the body becomes a full rectangle; LOCK) | Owner's idea, 2026-11-25. See `design/concepts/round-6/`. The firmware must read the sleeve position, so "held down by the sleeve" is not "talking". Needs a mechanical mock first. |
| **Grip to talk**: four fingers squeeze a strip or shell to talk; a left-thumb wheel changes mode; wheel click can latch | Owner's idea, 2026-11-25. See `design/squeeze-grip.md` and `design/concepts/round-7/`. Needs a printed mock-up in a real hand; separating "holding" from "squeezing" is the central risk. |
| **Edge roller in a pocket** for the left thumb (mode, four detents; click = latch) | Owner reference, 2026-11-25. See `design/concepts/round-8/`. Needs a metal pin and a small encoder or contacts. |
| **Glowing frosted window** that shows the mode by colour | Claude's idea from a reference. One RGB LED and a diffuser; replaces a screen or a row of lamps. Untested. |
| Lever protection for bag carry (recessed shoulders, flip guard, slide cover, LOCK position) | Owner concern; options listed in the ideas file. Superseded in direction by the sleeve above. |
| Removable back cover with a hackable bay (BOOT/RESET, header, battery space, info label) | Fits the toy and SDK positioning; reserve space even in v0.1. |
| Print-your-own covers with a published cover spec | Keep the mic port outside the swappable zone. Needs a hardware/CAD licence decision. |
| Mechanical-only printed mock for feel testing | Cheap, doubles as a fidget toy. |

## One cheap early decision

Even for v0.1, decide to **expose lever and mode state to the host in a documented way**. It costs little now and enables the desktop pet, the SDK and community ideas later.
