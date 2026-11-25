# Grip to talk: research and analysis

Date: 2026-11-25 · Status: **desk research and reasoning. Nothing built or measured. Numbers marked "unverified" must be checked.**

## The idea (owner)

Are we locked into TE's "key on the left"? Alternative: the **left hand holds the device, the four fingers squeeze to talk, and the left thumb rolls a wheel to change mode.**

## A correction first

Earlier I described the TE FX MIC lever as thumb-pressed, following the conversation. The retailer copy actually says you **squeeze** the lever to shape the effects (see [`inspiration.md`](inspiration.md)). I could not confirm which fingers use it. So "the key on the left, pressed by the thumb" was an assumption inherited from the discussion, not a verified fact about TE. A finger-grip is therefore not a departure from the reference; it may be closer to it.

## What I found

### Squeeze as an input exists, and the hard part is known
- **Google Pixel 2 "Active Edge"** is a force-sensitive surface along the sides, supported by **strain gauge elements stuck to the inner chassis walls**. Google's paper says one of the main design problems is a **gesture design that tells intentional squeezes from innocuous handling** ([Google Research](https://research.google/pubs/pub48144/)).
- It has a **sensitivity slider with nine levels**, from light to firm squeeze, to avoid triggering by simply holding the phone. A user report says even the highest level **did not fully stop** accidental triggers ([Android Central](https://www.androidcentral.com/how-use-customize-disable-active-edge-google-pixel)). Later Pixels dropped the feature.
- Takeaway: a squeeze can be sensed, but for a device you hold all day, **separating "holding" from "squeezing" is the central problem**, and it is worse for **hold-to-talk** (a sustained squeeze) than for a quick squeeze gesture.

### Grip-to-talk has real prior art
- **Astatic's grip-to-talk lever** on its Model 552 microphone is a lever-operated leaf switch; squeezing it turns on the microphone and a control circuit. The manual says the mic ships **non-locking**, and a **lock** needs a mechanical change ([Astatic 552 manual](https://manualmachine.com/astatic/552/26834871-user-guide/)). That is the same logic as our "hold to talk, latch to keep it on".
- Two-way-radio accessory makers fight **accidental PTT** with **dual PTT buttons** ([L3Harris](https://www.l3harris.com/all-capabilities/xg-75pxg-75pe-two-way-portable-radio-microphones-and-audio)), aftermarket **PTT guards**, and large glove-friendly buttons usable by either hand ([MSA](https://se.msasafety.com/Huvudskydd/Brand/Kommunikationssystem/Push-to-Talk-mikrofoner-och-monofoner/p/000010000900001000)). These are vendor claims, not independent tests.

### Ergonomics (numbers: check before relying)
- For a **power grip**, a cylindrical or oval handle of about **40 mm**, within **30 to 50 mm**, is recommended; non-slip, compressible material helps; handles should be longer than about 100 mm ([CCOHS](https://www.ccohs.ca/oshanswers/ergonomics/handtools/tooldesign.html)). That guidance is for tools, not microphones.
- **Hand breadth** in the tables I saw is about **75 to 91 mm** (5th to 95th percentile, women and men); I did not verify the population ([example table](https://pmc.ncbi.nlm.nih.gov/articles/PMC9225906/table/tab3)). So a squeeze strip of **70 to 80 mm** covers four fingers for most adults, and the device should be **about 90 mm or taller** to hold it.

**What this means for our shapes:**
- Our slab is about **20 mm thick**. That is thinner than a comfortable power-grip diameter. A 20 mm slab squeezes like a **pinch**, not a grip. A thicker body (**30 to 40 mm**) will feel better to squeeze, but is bulkier in a pocket. This is a real trade-off between *pocketable* and *squeezable*, and round 7 explores both ends (A thin, B and C thick).

### Sensing options (hobby level)
- **Mechanical strip + Hall sensor** (the round-6 idea moved to the right edge): the strip moves a few millimetres; a Hall sensor and magnet give an analogue reading, so the **thresholds are software-adjustable** (like Pixel's nine levels) and a **spring preload screw** adjusts the base force mechanically. My preferred first try.
- **Force-sensitive resistor (FSR)** behind a rigid plate: a 12.7 mm round Interlink 402 reads roughly 1 N to 100 N ([Adafruit](https://learn.adafruit.com/force-sensitive-resistor-fsr/overview)). Cheap, but needs a force spreader; its feel is "hard, no travel".
- **Strain gauges** like Pixel's: accurate but tricky to mount and read for a hobby build.

## Risks I see

1. **Accidental talk.** People grip firmly when walking or carrying. A threshold above the normal holding force needs a **spring preload / dead zone**, and the firmware should be able to adjust it. The **LOCK sleeve** stays (and in a bag, the squeeze part must be locked or recessed).
2. **Fatigue.** Sustaining a squeeze for a long dictation tires the hand. The **latch** stage and the wheel's **click** (below) are the answer.
3. **Handling noise.** A squeezing hand next to the microphone is a noise source; the mic should be at the head, **mechanically decoupled** from the grip.
4. **Desk use.** When the device stands on its stand, nobody is gripping it. So there needs to be another way to talk: **click the thumb wheel to latch**, or treat the stand pose as an always-on **OPEN** mode.
5. **Handedness.** A left-hand design; the user mirrors the print for a right hand (all shapes here can be mirrored).
6. **Hand fit.** Only a printed mock in a real hand can answer it.

## Interaction map options (to discuss; nothing decided)

| Input | Option 1 | Option 2 |
|---|---|---|
| Squeeze (four fingers) | hold = talk | hold = talk; a firmer squeeze = send |
| Wheel (left thumb) | roll = mode (DICT, TALK, OPEN, LOCK) | same |
| Wheel click | click = **latch** (hands-free; also the desk way to talk) | click = send |
| Sleeve | LOCK (squeeze part held flush); may also be the power switch | same |

My reading: **Option 1** keeps "squeeze" simple (one stage), avoids a firmer-squeeze stage that fatigue would make hard to control, and gives the thumb something useful. The three-stage lever from earlier fits the side-strip idea better than a four-finger squeeze.

## Suggested first test (cheap)

Print a **mock-up with no electronics**: a body with a squeeze strip on a hinge and a pen spring, plus a **preload screw**. Hold it in a real left hand, walk around, put it in a bag, and see: Is the strip's default force comfortable? Do you ever hold it hard enough to trigger? Does a thicker body feel better? This answers the questions the sketches cannot.
