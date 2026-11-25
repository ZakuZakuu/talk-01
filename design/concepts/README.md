# Concept sketches — first round

Date: 2026-11-25 · Status: **flat 2D sketches for discussion. Not CAD, not a final design.** Every dimension is a guess; no electronics envelope has been measured yet.

| Sheet | Idea | Files |
|---|---|---|
| **A · Pager** | Portrait slab, thumb paddle, slider mode switch, slit grille, full-back flip stand | [`A-pager.svg`](A-pager.svg) · [`png`](A-pager.png) |
| **B · Telegraph** | Landscape body, key bar on top, preset mode keys, vertical-slot grille, full-width flap stand | [`B-telegraph.svg`](B-telegraph.svg) · [`png`](B-telegraph.png) |
| **C · Radio** | Portrait body, rotary band dial, slide-latch lever, ring grille, bail stand / carry loop | [`C-radio.svg`](C-radio.svg) · [`png`](C-radio.png) |

Each sheet shows: front, rear (stand closed), side (stand closed), side (stand open, on a desk, with the direction of the mic port and the direction to the mouth), numbered controls, and the tradeoffs.

> **中文摘要**
> 三张是供讨论的草图，不是定稿。三个方向的核心差别在于"拉杆 + 模式选择 + 支架"这三个交互件：A 是拇指拨片 + 滑块 + 整块翻板；B 是电报键杆 + 预设按键 + 全宽翻脚；C 是旋转波段拨盘 + 滑动锁定拉杆 + U 形提手支架。它们的各个部件可以混搭（见下面"模块化挑选"）。所有尺寸都是猜的，先看形态和手感再说。

## Shared assumptions (apply to all three)

These come from the owner discussion in [`../../docs/discussion-log.md`](../../docs/discussion-log.md) and the research in [`../../docs/research/claude-review.md`](../../docs/research/claude-review.md).

- **Mic first.** It must work as a plain USB microphone and as a voice-input device. Fun is the second priority.
- **Three modes**: DICT (lever = configurable key), TALK (lever = walkie-style push-to-talk), OPEN (always-on desk mic). The mode must be **visible** on the device.
- **Wired USB-C only for v0.1.** Battery and wireless are not drawn; the bodies keep room for them.
- **USB-C on the right edge** (in the front view), because the owner's device usually sits to the *left* of the laptop and the cable runs to the right.
- **Lever on the left edge** (front view), pressed with the thumb of the right hand, walkie-talkie style. The layout is mirror-able; handedness is an open question.
- **Optional buzzer** holes, kept as far from the mic as the body allows (a buzzer can leak into the mic).
- **Desk use**: the owner sits at a laptop, device 30–60 cm away at the left, or closer next to the keyboard. The mouth is roughly 40° above the mic in that setup (a rough estimate).
- **Grille and mic port**: the mic port is a single small hole. Slits, slots and rings are the visible grille; their acoustic effect is untested.
- Palette is a suggestion: A warm cream + orange, B charcoal-olive + cream + orange, C sand + teal. Colours can be swapped independently of shape.

## What the sketches show beyond looks

These are simple geometry checks done by the sketch script, assuming a uniform-density body. They are **sanity checks, not measurements.**

1. **The stand angle decides where the mic points.** At 28–30° lean the port faces about 30° above horizontal, but the mouth is estimated at ~40° up. Close enough for an omnidirectional MEMS mic, but a second, more reclined stand position would aim better. C mentions a second detent.
2. **Short, thick bodies need a steeper recline.** For a body that leans back on a rear stand to stay put, the centre of mass must stay behind the bottom-rear pivot: tan(lean) > depth / height. For B (24 / 48) that means more than ~27°, so it is drawn at 40°. A and C are tall and thin and are comfortable at ~30°. Real mass (board, key bar, any battery) will move the centre of mass, so rerun this check once there are real parts.
3. **Stand length and footprint.** The stand legs in the sketches reach roughly 40–60 mm behind the body at the desk. That is a lot of desk next to a keyboard; shorter stands lean the body more.

## Comparison

| | **A · Pager** | **B · Telegraph** | **C · Radio** |
|---|---|---|---|
| Handheld (walkie style) | Best | Awkward (held like a bar) | Good |
| Desk presence | Plain, tidy | Best, very toy-like | Good, radio-like |
| Lever | Thumb paddle, left edge | Key bar on top | Slide lever, left edge, with a latch for hands-free |
| Mode selector | 3-position slider + 3 lamps | 3 preset keys with lamps | Rotary dial, clicks, visible pointer |
| Stand | Flat slab | Full-width flap | U-frame bail, doubles as a carry loop |
| Parts / tuning effort | Low | Medium | Highest |
| Distance from the EP-2350 FX MIC | Closest (left lever, portrait) | Farthest | Medium (round dial is distinctive; side lever is similar) |
| Main risk | Looks too much like the reference unless the paddle is reshaped | Handling, stand footprint, bar noise | Complexity: three mechanisms to tune |

## Pick modules, not whole concepts

The sheets are different on purpose, but the parts mix freely. Each row is an independent choice:

| Part | Options drawn |
|---|---|
| Body | Portrait slab (A, C) · landscape bar (B) |
| Talk lever | Thumb paddle (A) · key bar (B) · slide-latch (C) |
| Mode selector | 3-position slider (A) · preset keys (B) · rotary dial (C) |
| Stand | Flat slab (A) · flap (B) · bail (C) |
| Grille | Horizontal slits (A) · vertical slots (B) · segmented rings (C) |
| Palette | Cream + orange (A) · charcoal + cream (B) · sand + teal (C) |

My opinion, not a decision: for a device that is mostly on the desk and sometimes handheld, a **portrait body** (A or C) is safer; the **paddle** is the simplest lever to build and test first; the **rotary dial** and the **latch** are the most fun but add the most tuning, so they make a good "second step"; **preset keys with lamps** are the clearest way to show mode if a dial feels too fiddly. If you want a pure desk toy, B is the most distinctive.

## Differences from the reference

The EP-2350 FX MIC (from one promotional render) combines a perforated dot-matrix grille, a two-tone body and a single saturated side lever. These sketches deliberately use other grille patterns (slits, vertical slots, segmented rings), single-body colourways, and different lever types, but A's left-edge paddle and C's left-edge lever are placed where a thumb naturally goes and are therefore closest. Please judge whether that is far enough.

## Unresolved risks

- No electronics or mechanism has been measured, so none of the thicknesses (20–24 mm) is validated.
- Switch travel, detent feel, hinge strength (FDM) and print tolerances are unknown.
- Acoustics are untested: port position, grille effect, lever noise, and desk vibration through the feet.
- Lever/handling noise matters more for TALK and DICT than for OPEN; B's long key bar is the biggest concern.
- The latch in C adds firmware states and needs careful key-release handling.

## Questions for the owner

1. Which parts above do you like, mix and match? (A body with C's dial? B's keys on a portrait body?)
2. Lever side: right-hand thumb (as drawn), or should it be mirrored?
3. How important is carrying it handheld versus leaving it on the desk?
4. Colourways: keep warm cream + orange, or try something else?

## Regenerating

The sheets are generated by [`src/make_concepts.py`](src/make_concepts.py) (Python standard library only). Edit the dimensions at the top of each concept function and run:

```bash
python3 design/concepts/src/make_concepts.py design/concepts
```

PNG previews were rendered from the SVGs with a headless browser at 2× scale.
