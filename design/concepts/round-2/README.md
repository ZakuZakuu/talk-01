# Round 2 — three coherent directions

> **Owner feedback on this round:** all three were "a bit short of something" and did not catch the eye; the owner wants bolder, more distinctive designs. See [`../round-3/README.md`](../round-3/README.md) and [`../../design-principles.md`](../../design-principles.md). The baseline items (top USB-C, three-stage lever) still stand; the full-back cover does not (the owner wants a small hatch, and a small U stand or a cover that doubles as the stand).

Date: 2026-11-25 · Status: **sketches for discussion. Tentative dimensions, nothing built or measured.**

Round 1 explored shapes. Round 2 starts from the owner's feedback and from [`../../inspiration.md`](../../inspiration.md). The rule for this round: **each concept has exactly one organising idea, and every other part either serves it or is deliberately left out.** This is not a mix of every idea on the list.

| Sheet | The one idea | Files |
|---|---|---|
| **D · Dial** | A thumb wheel is the whole interface. Quiet body, shoulders protect the lever, `LOCK` is a wheel position | [`D-dial.svg`](D-dial.svg) · [`png`](D-dial.png) |
| **E · Armed** | Safety-switch language: a guard flips over the lever, and the guard is the master switch (SAFE / ARMED) | [`E-armed.svg`](E-armed.svg) · [`png`](E-armed.png) |
| **F · Handset** | Form follows the left thumb: a flared body with a scooped groove holding the slider and the lever | [`F-handset.svg`](F-handset.svg) · [`png`](F-handset.png) |

> **中文摘要**
> 这一轮每个方案只讲一个核心想法，其余部件要么为它服务、要么明确舍弃。D 是"一个拇指拨盘就是整台界面"，E 是"护罩即总开关（SAFE/ARMED）"，F 是"外形顺着左手拇指长出来"。三者共用一小套基础设计（顶部 USB-C、左边缘三段式拉杆、可换背板加开发舱、四分之一转锁扣脚），下表说明每个想法放在了哪里、为什么没放在别处。

## Shared baseline (identical in all three)

These are the owner's decisions and the cheapest, most reusable ideas. They are drawn the same way in every sheet so that the sheets differ only where the concepts differ.

- **USB-C on the top edge**, away from the mic hole (see the *Top edge* view in each sheet).
- **Lever on the left edge**, pressed with the left thumb (the right hand stays on the mouse). The lever has **three stages** (below).
- **Swappable back plate with a hackable bay** under it: BOOT/RESET access, a small header, space for batteries later, an info label. The stand is part of the back plate.
- **Quarter-turn feet** that hold the back plate (an idea from the TE OP-Z back cover).
- **Three modes**: DICT / TALK / OPEN, plus a LOCK state. *How* the mode is chosen is what differs between D, E and F.

### The three-stage lever

This follows the owner's description. Travel is about 3 mm (a guess).

| Stage | Physical action | Meaning (to be settled per mode) |
|---|---|---|
| Rest | not touched | idle |
| 1 · Hold | light press | hold-to-talk (key down while held) |
| 2 · Click | press to the bottom, a distinct click | **latch**: hands-free, stays active after release |
| 3 · Push | extra firm push past the click | **send**: ends dictation and sends Enter |

- Stage 2 needs only a bottom-out switch. Stage 3 needs the stop to be slightly compliant (for example a small spring behind the bottom stop), so a firm push moves the lever a further fraction of a millimetre. A Hall sensor and magnet can read the lever position continuously, so that all stages can come from one sensor and tuned thresholds.
- The feel is the whole point, so this needs a mechanical mock before any electronics.
- Open question: in a latched state, how is it released? Probably another light press. This is not decided.

## What each concept keeps and leaves out

| Idea | D · Dial | E · Armed | F · Handset |
|---|---|---|---|
| Thumb wheel for mode | **Yes, the hero** | No (a slider; mode changes rarely) | No |
| Lever guard / lock | Shoulders + a `LOCK` wheel position | **Flip guard = master switch** | Groove shoulders + a `LOCK` slider position |
| Ergonomic shaped body | No (plain slab) | No (plain slab) | **Yes, the hero** |
| Mode selector | Wheel | Front slider | Slider in the groove |
| Stand | Flat slab | Single bar with a carabiner hole | U-frame bail, also a carry loop |
| Fidget element | Wheel | Guard flip | Slider and groove |
| Grille | Sunburst slots | Pyramid vent | Rosette of holes |
| Palette | Stone grey + orange | Olive + orange | Bakelite brown + cream |
| Left-hand only? | Mirror-able | Mirror-able | **Left-hand shape**; mirror for right |

Optional extras that apply to any of them but are **not drawn**, to keep the sheets honest: a small buzzer; a magnet in the stand so the firmware knows "stand open = desk profile, stand closed = handheld profile" (a gain change, no DSP); a walkie-talkie mode.

## Considered and dropped

**One lid that is guard, stand and master switch.** The idea: a front cover that flips over the top, folds flat onto the back as a handset position, and swings out as the kickstand. It does not work with a single hinge: a lid hinged on the top edge ends up sticking *up* after 180°, not lying on the back. Making it work needs a 360° offset hinge (a laptop-convertible style hinge), which is hard to make strong in FDM. Dropped, but the reasoning is recorded here in case a stronger hinge idea appears.

## Notes per concept

### D · Dial
- **Why it might work:** the most TE/Braun-like: a quiet body with one expressive part, and the wheel is exactly where the left thumb rests. It is also the best fidget toy of the three.
- **Left out on purpose:** lid or guard, slider, lamp row, extra buttons.
- **Risks:** the wheel is the most complex mechanism (click detent plus a rotary switch or encoder, seen through a window). It can be bumped in a bag, so it needs firm detents and friction. Wheel and lever share one edge, so thumb travel needs a full-size print to check.

### E · Armed
- **Why it might work:** it answers the "keys get pressed in a bag" worry most directly, and it makes the state obvious: guard up means live. Field-gear styling is distinctive and quite different from the reference.
- **Left out on purpose:** wheel, groove, lid. The mode slider is deliberately plain.
- **Risks:** a printed hinge will fatigue (use a metal pin). Reading the guard state needs a magnet or Hall sensor. It adds one action before every use, so it must flip fully out of the way of the thumb. A single narrow stand bar can rock sideways. The look is serious, less playful than D or F.

### F · Handset
- **Why it might work:** best ergonomics: the groove cradles the thumb; the wide base stands stably; it feels like a retro handset. The slider echoes dictation recorders.
- **Left out on purpose:** wheel, guard, lid, symmetry.
- **Risks:** a left-hand shape (a mirrored print is needed for right-handed users). A tapered, curved body is harder to pack and to print. A slider is less fun than a wheel, so the fun is in the shape. The bail is the only stand.

## Geometry checks (same assumptions as round 1)

- Lean angles drawn: D 30°, E 30°, F 28° (the port faces about 30° above horizontal against an estimated 40° to the mouth, so a second, more reclined position would aim better).
- In every sketch the centre of mass (uniform body) falls 13–15 mm behind the bottom-rear pivot, so the body rests on its stand. Real electronics will move this; recheck with real parts.

## My opinion (not a decision)

- If one concept had to be tested first: **D**. It concentrates the fun in one mechanism, and that mechanism (a thumb wheel) is the thing most worth feeling in the hand.
- **F's groove is worth testing as a pure shape**, independent of the rest: a printed block held in the left hand answers whether the scoop helps.
- **E's guard is the best answer to "bag safety"**, but also the least playful; I would borrow only the *idea* (a lock state that is physically obvious), and the `LOCK` position in D or F already covers that.
- I deliberately did not combine them. If a hybrid is wanted later, pick one hero and drop one thing for each thing added.

## Suggested first physical step (optional)

Print three **mechanical-only mocks**, no electronics: a wheel block (D), a groove block (F), and a guard flap (E). Hold each in the left hand. This costs little and answers the feel questions that sketches cannot.

## Questions for the owner

1. Gut feeling: which of D, E, F attracts you? Why?
2. Is the three-stage mapping right: light press = talk, click = latch, firm push = send? Or should "send" and "latch" be the other way around?
3. Do you want to keep the walkie-talkie voice effect on the list even though nothing here draws it?
4. Palettes: stone grey, olive, bakelite brown. Any strong yes or no?

## Regenerating

[`../src/make_round2.py`](../src/make_round2.py) generates these sheets (Python standard library only). Edit the dimensions inside each concept function and run:

```bash
python3 design/concepts/src/make_round2.py design/concepts/round-2
```
