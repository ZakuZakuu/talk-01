# Inspiration and design ideas — input for round 2

Date: 2026-11-25 · Status: **research notes and ideas for discussion. Nothing here is decided.**
Sources are web search results and two teardown articles; I did not handle any of these products. Anything I could not confirm is marked.

## 1. What I found

### Teenage Engineering EP-2350 FX MIC — the lever is a three-stage control
A teardown on [Hackaday](https://hackaday.com/2026/08/20/teardown-shows-low-fi-microphone-is-surprisingly-sophisticated/) and the [Adafruit Learn guide](https://learn.adafruit.com/hacking-the-teenage-engineering-ep-2350-ting/teardown-and-reassembly) (both credit Sam Holland of informal.cc for the original teardown) describe it:

- A **spring-loaded side lever with three sensors**: one switch that detects "touched at all" (the device wakes from sleep as soon as the lever moves), a **potentiometer on the pivot** that reads how far it is pressed, and a **third switch that clicks when the lever is pushed all the way in**.
- Pressing wakes the device, travel adjusts the effect in proportion, and bottoming out gives a distinct click that also acts as an input.
- Construction: **one PCB** with a cutout for two AAA cells; a back panel held by **5 small Phillips screws**; the capsule connected by two thin wires; the 3.5 mm cable on a press-fit connector; no glue.

Takeaway for us: a lever can be much more than a switch. The half-press / full-press idea maps directly onto our open interaction questions (see §2).

I could **not** find where the slanted-lever idea came from; none of the sources say. Push-to-talk bars on handheld radios and handsets are the obvious family, but that is my inference.

### What is the TE FX MIC's reference device? (owner question)
- **Retailer and press descriptions** call it a handheld mic in an **80s CB-radio style** and "a tiny radio mic", and say it could be mistaken for a kids' toy or a CB radio ([Yanko Design](https://www.yankodesign.com/2025/11/05/teenage-engineerings-latest-microphone-is-the-most-unserious-yet-brilliant-piece-of-music-tech-weve-seen/amp/), [Product Hunt](https://www.producthunt.com/posts/ep-2350-fx-mic)). **Teenage Engineering's own statement of the inspiration was not found.** The lineage below is my inference.
- The look matches a **CB or two-way-radio hand microphone**: a rectangular body, a perforated front, a **coiled cable**, and a big spring-loaded **push-to-talk (PTT) bar on the side**. It is *not* a walkie-talkie (no radio inside) and not a telegraph.
- **PTT** means press to transmit, release to listen (a half-duplex radio habit, see [Handie-Talkie](https://en.wikipedia.org/wiki/Handie-Talkie) for the walkie-talkie ancestry). A **telegraph key** is a different thing: a lever tapped to send Morse. They share only the "spring lever with a click" feel.
- **Correction (2026-11-25):** earlier chat replies assumed the lever is pressed by the thumb. The retailer copy says you **squeeze** it, and I could not confirm which fingers use it. See [`squeeze-grip.md`](squeeze-grip.md).
- **What the TE lever does** is described differently by different sources: "squeeze the lever to shape the vocal FX" (retailers), "press the orange talk button and you are off" ([Synth Anatomy](https://synthanatomy.com/2026/08/teenage-engineering-ep-2350-fx-mic-the-mic-with-built-in-sample-playback.html)), and a wake-on-touch plus travel-proportional control ([Hackaday teardown](https://hackaday.com/2026/08/20/teardown-shows-low-fi-microphone-is-surprisingly-sophisticated/)). I did not confirm that it gates the audio like a real PTT.
- Naming is confusing: the earlier **EP-2350 Ting** is the CB-styled model; the **FX MIC** is described as its redesigned successor ([Gearnews](https://gearnews.com/teenage-engineering-ep-2350-fx-mic/)).
- Idea for us: a **coiled cable** is part of that retro cue. A commercial coiled USB-C cable could be an easy, cheap signature detail.

### CMF (Nothing) Speaker S / M — swappable panels with official 3D files
[Digital Trends](https://digitaltrends.com/home-theater/cmfs-first-bluetooth-speakers-s-and-m-come-with-swappable-panels-and-3d-printable-parts/) and [Android Headlines](https://androidheadlines.com/2026/10/cmf-by-nothing-launches-speaker-s-m-specs-price.html) report (October 2026):

- Front panel and volume knob are swappable; a **switch at the back releases them**.
- CMF is releasing **official 3D design files** so people can print their own parts. One review notes that **panel fit affects the sound**, so it must be secured correctly.
- Precedent: in 2024 Nothing published documentation for printing CMF Phone 1 back covers ([9to5Google](https://9to5google.com/2024/07/15/nothing-cmf-phone-1-accessories-3d-print/)).
- **Not confirmed:** the official file page was not in the results, so I do not know the file formats or the licence. Do not reuse their files; only the idea applies.

### Teenage Engineering covers — I did not find an official swappable faceplate
- Community items exist: a [Pocket Operator case with a swappable button plate](https://www.printables.com/model/1190768-teenage-engineering-pocket-operator-case), a [TPU battery cover](https://makerworld.com/models/102322), custom EP-133 battery panels sold on Etsy.
- iFixit's [OP-Z back cover guide](https://www.ifixit.com/Guide/Teenage+Engineering+OP-Z+Back+Cover+Replacement/128284) mentions that the back cover's **rubber feet unlock by turning 90°**. That is a nice detail: feet that double as latches.

### Braun T3 (1958) — one expressive control on a plain box
Museum and design pages ([Microsoft Buxton Collection](https://microsoft.com/buxtoncollection/detail.aspx?id=179), [Core77 history](https://www.core77.com/posts/24768/A-History-of-Braun-Design-Part-3-Audio-Products)) describe an almost featureless box interrupted by a dial and speaker apertures. One less reliable blog says the dial sits on the **side because the thumb reaches it while the hand holds the device**; treat that as interpretation. Buxton's notes say it inspired the first iPod generations. Relevance: it supports a single thumb-reachable dial as the expressive control.

### Philips Pocket Memo — dictation hardware settled on a thumb slider
The [DPM7000](https://www.dictation.philips.com/products/mobile-dictation/pocketmemo-voice-recorder-dpm7000/) uses a four-position slide switch (record, stop, play, rewind) that Philips describes as ergonomic for one-thumb use. Relevance: a thumb slider is the established control for dictation; it is a candidate for the stand-by / lock / hold position.

### CB hand microphones
My search found no design history of palm-mic push-to-talk ergonomics (only trucking and CB product pages), so I draw no conclusion from it.

## 2. Ideas, with what each one solves

Effort is a rough guess for a hobby build. "Round 2" means I would show it as an option in the next sketches.

| # | Idea | Source | Solves | Effort | Notes |
|---|---|---|---|---|---|
| 1 | **USB-C on the top edge** (or top corner), with a back notch so the cable can leave backwards when standing | Owner | A bottom cable collides with the desk; a top cable can run behind the stand toward the laptop | Low | Fits the board: small dev boards have USB-C on a short end. Cable noise travels into the mic, so keep the port away from the mic hole and use a strain-relief groove. |
| 2 | **Left-hand thumb ergonomics.** Right hand stays on the mouse, so the left hand holds the device and the **left thumb** reaches the left edge. A **thumb dial at a corner** for mode, lever lower on the same edge | Owner | Natural one-hand use | Low | Thumb wheels and side dials are an old pattern (T3-style). Needs a full-size paper/print mock to check reach. |
| 3 | **Two-stage lever**: first stage = hold-to-talk; pushing through to a bottom-out click = latch (hands-free) or send | Claude, from the TE lever | The double-tap timing problem and long dictation, without a timer: the gesture is physical, not timed | Medium | Two microswitches, or a Hall sensor and magnet. Firmware must handle releases carefully. |
| 4 | **Lever lock** so it cannot be pressed in a bag: (a) recessed shoulders around the lever; (b) a **flip-up guard** like an aircraft/military switch guard; (c) a slide cover; (d) a **LOCK position on the mode dial** that disables the lever and mutes | Owner (problem), Claude (options) | Accidental presses, wear | (a) low, (b)(c) medium, (d) low | (a)+(d) are cheapest. (b) is the most retro and fun. A guard that must be opened every time is annoying: it should flip fully out of the way. |
| 5 | **Removable back cover = hackable bay.** Under it: BOOT/RESET access, a small header, battery space, device info and a QR label | Owner, Claude | Updating firmware, SDK tinkering, later battery, hiding specs | Medium | TE uses a screwed back panel; CMF uses a release switch. FDM snap fits fatigue, so use screws, magnets or a twist lock. |
| 6 | **Print-your-own covers**: publish a "cover spec" (dimensions, tolerances, keep-out zones, fastener) so anyone can print front plates or knob caps | Owner | The toy and hackable positioning | Medium | **Keep the mic port out of the swappable zone** or define an acoustic gasket and alignment, because fit affects sound. Hardware/CAD licence needs deciding first. |
| 7 | **Twist-lock rubber feet** that hold the back cover | Claude, from OP-Z | A clever fastener that doubles as feet | Medium | Check printability. |
| 8 | **Mechanical-only mock** (lever, dial, guard, stand, no electronics) printed first | Claude | Judging the feel before wiring anything; it is also a fidget toy | Low | Matches "it should work as an EDC toy even without function". |
| 9 | **Lever position controls effect amount** (for the walkie mode), like the TE lever | Claude | Extra fun on an already existing sensor | Low if #3 uses a Hall sensor | Optional; part of the fun backlog. |

## 3. Questions for the owner

1. Which lever protection appeals most: recessed shoulders only, a flip-up guard, a slide cover, or just the LOCK position on the dial?
2. Is it acceptable that the back cover is secured with screws (simple, strong), or do you want a tool-free release?
3. Where should the thumb dial sit: upper-left corner (above the lever) or somewhere else?
4. Do you want round 2 to look more like **A** (cream slab) or **C** (radio) as the base, or one hybrid?
