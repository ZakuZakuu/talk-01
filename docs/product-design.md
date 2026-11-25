# Product brief — v0.1 concept

## User need
Daily voice typing and AI conversations should feel like picking up a small radio, not holding a keyboard modifier. The same device should handle occasional clean spoken-word recording (podcast, narration, calls) and travel easily. It is a low-priority hobby, not a startup or a deadline-driven project.

## Agreed direction
- Wired USB-C only, bus powered; portable, no separate receiver or stand.
- Retro pager/telegraph/radio instrument feel. Reference: Teenage Engineering EP-2350 FX MIC for tactile proportions and side lever; CM-15 for foldable support. Original industrial design, no copied branding, artwork or exact geometry.
- Rear hinged kickstand sits flush when stored; stable on a desk, with cable clearance and pickup facing the user.
- Physical lever with satisfying travel and feedback. A few purposeful controls; avoid feature clutter, RGB and unnecessary screens.
- Standard microphone mode plus configurable voice-input controls. Windows first; avoid custom drivers where possible.
- Audio should sound natural and be suitable for simple spoken-word recording; no studio-grade requirement.
- Prototype with available modules and home 3D printing, then consider custom PCB.

## Interaction proposal (not finalized)
| Gesture / control | Intended behavior |
|---|---|
| Hold side lever | Hold mapped keyboard key (default Alt for WeChat Input) |
| Release | Release modifier, end dictation |
| Double tap | Optional Enter / send; must avoid inadvertent dictation or sending |
| Mode switch or auxiliary button | Continuous recording vs voice-input mode; mute behavior TBD |
| Status indicator | Clear active/muted state; must reflect actual audio gating if provided |
| Optional gain control | Only if useful and easy to implement |

Key mapping should be configurable and stored on device eventually. HID key-down/up and recovery on mode change, reconnect and timeout need testing. A short-vs-long press threshold may introduce latency; compare separate send button vs double tap. No automatic message sending by default until behavior is validated. Voice-input software handles transcription, not the microphone.

## Design targets (not requirements)
Pocket-sized, roughly 90 × 55 × 20 mm, about 100 g or less if feasible. Warm off-white / gray and orange accents are one possible palette, not a locked choice. USB connector on side or other position that clears the deployed stand. Printed shell, separate mechanical parts where useful. Electronics envelope and microphone port geometry must be measured before detailed CAD.

## Non-goals
Wireless, battery, embedded AI, standalone recorder, advanced DSP, custom driver, polished companion app, immediate PCB production or commercialization. Revisit only after daily usability.

## Future possibilities
If prototype works well, consider sharing build files and evaluating demand. Commercial use requires separate review of licensing, original industrial design, compliance, reliability and sourcing.
