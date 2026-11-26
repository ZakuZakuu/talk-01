# Microphone quality: what matters for talk.01 (analysis, 2026-11-26)

Status: **analysis from datasheets and arithmetic. Nothing has been recorded or measured.** Figures are marked **[verified]** (read in a datasheet or the maker's page, linked), **[unverified]** (quoted by someone, not checked), or **[calc]** (my arithmetic, with the stated assumptions). The owner relayed a second opinion (from another assistant) and asked Claude to analyse it; this note records the result.

## 1 · Three kinds of route (the owner asked what the differences are)

| Route | What it is | Fits talk.01? |
|---|---|---|
| **A. A digital MEMS chip on a small module** (I2S or PDM) | the microphone and its converter in one 3.5 × 2.65 mm part; wires straight to the controller | **Yes, this is our route.** XIAO ESP32S3 reads it directly; no analog circuit |
| **B. An analog electret capsule** (the kind in lavalier microphones) | a small capsule with an analog output | **Needs an extra converter chip** (the ESP32's own ADC is not good for audio) and its own circuit: more parts, not fewer |
| **C. A finished product** (a wireless clip-on, a USB microphone) | a whole system with its own processing | **Not a part. A reference** to listen against, not something to build in |

The **DJI Mic Mini** belongs to C. It is a wireless transmitter and receiver pair (DJI's specs: a 2.4 GHz link, GFSK 2 Mbps; omni; 20 Hz to 20 kHz; equivalent noise 24 dBA; 120 dB SPL maximum) [verified: [DJI specs](https://www.dji.com/mic-mini/specs); the result mixed pages of the Mic Mini and Mic Mini 2, so check the model]. Its "equivalent noise" is a **whole-system** figure, which may include processing. You cannot reuse its capsule or its circuit. Its use to us: **something good to listen against** if the owner has or can borrow one.

## 2 · What the other opinion gets right, and where it needs care

**Right**
- A "voice recognition" label on a module says little about the chip; sample rate and bit depth do not make a noisy capsule good.
- The four figures to look at are right: SNR, frequency response, AOP (maximum level), directivity.
- 73 dBA against 61 dBA is 12 dB, a factor of about 16 in noise power [calc, correct]. 40 cm to 10 cm is about +12 dB of direct sound in the free field [calc, correct].
- Make the pickup replaceable; keep the first shield and mount minimal and listen first; keep the 24 mm body; use the owner's phone as the reference; the test table is a good one.

**Needs care**
- The numbers in its chart are partly verified: INMP441 61 dBA [TDK, in the earlier note]; ICS-43434 64 or 65 dBA depending on the revision [verified: [datasheet v1.2](https://cdn.sparkfun.com/assets/a/9/c/9/1/DS-000069-ICS-43434-v1.2.pdf)]; **T5848 68 dBA in high-quality mode** (65 in low-power) [verified: [TDK](https://invensense.tdk.com/products/digital/t5848/)]; **IM72D128 72 dBA** (71.5 in one datasheet) [verified: [Infineon](https://www.infineon.com/content/dam/infineon/row/public/documents/24/45/infineon-mems-im72d128v01-productbrief-en.pdf)]; IM69D130 69 and IM73D122 73 [unverified by me]; DJI "70" is 94 minus its stated 24 dBA equivalent noise [calc, a system figure, not a chip figure].
- **SNR is the right first number, but it is not the one that decides the result here.** See §3.
- It says the ESP32-S3 converts PDM to PCM in hardware. The ESP-IDF documentation says so for **one I2S port (I2S0)**, and an older page says that path is **16-bit** [verified: [ESP-IDF I2S](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/peripherals/i2s.html)]; how good that built-in filter is, is **unknown** to me.
- "Buy the baseline, the high-end part and a finished microphone" is a good aim, but the high-end part is the one that is hard to get as a module (§4).
- A **lavalier assembly** sounds like the lazy way out but is route B: it needs a converter, and an ordinary USB sound-card chip cannot send our key presses (we need our own controller anyway).

## 3 · Does a better chip actually change the recording? (my calculation, with assumptions)

Self-noise in dBA SPL is 94 minus the SNR [calc]: INMP441 about 33; ICS-43434 about 29 to 30; **T5848 about 26**; **IM72D128 about 22**; DJI system about 24.

Assumptions (typical values, **not measured in the owner's room**): normal speech about 60 dB SPL at 1 m, so about 80 dB SPL at 10 cm and about 70 at 30 cm; a quiet home room 25 to 35 dBA.

| Room noise | Total noise with INMP441 | with T5848 | with IM72D128 | Gain from the best chip |
|---|---|---|---|---|
| 35 dBA | 37.1 dBA | 35.5 | 35.2 | **about 2 dB** |
| 30 dBA | 34.8 | 31.5 | 30.6 | about 4 dB |
| 25 dBA | 33.6 | 28.5 | 26.8 | **about 7 dB** |

[calc: powers added, A-weighted figures, one number each.] So **a better chip pays off in a very quiet room**; in an ordinary room the room itself is the noise, and the gain is a couple of dB. This is why the owner's reading, "if the cheap module is enough, no need to upgrade", is right, and why the cheap module should be tried first.

**What I think will matter more than the chip** (judgement, to be tested):
1. **Mechanical noise**: the key's click, the hand's rustle and a hard 3D-printed body all reach the microphone. A soft mount (thin foam tape under the mic board) and a decoupled key are worth more than several dB of SNR.
2. **The port and the hole**: a hole with a gap in front can resonate; the felt, the gap and the hole size change the tone. Test with and without the lid.
3. **Pops and wind at 10 cm**: a small foam cover (the lavalier foam sleeves are cheap) or a thin mesh.
4. **Power and clock noise** from the controller and USB: a clean 3.3 V (an LDO), short wires, the mic away from the controller board.
5. **Gain staging** [calc from datasheets]: the T5848 in high-quality mode has a sensitivity of -37 dBFS at 94 dB SPL, so speech at 10 cm is about -51 dBFS. If the USB stream is **16-bit** (as in the usb-mic recipe), its own noise floor is about -98 dBFS, which is no longer small beside the T5848's -105 dBFS (A-weighted). So: **apply digital gain in 24 bits, then convert to 16 bits**, or find out whether the USB audio stack can send 24-bit. This is a firmware question to settle early.

## 4 · The candidates, and how I would stage them

| Candidate | Interface | SNR | AOP | Size | Availability / risk |
|---|---|---|---|---|---|
| INMP441 module | I2S | 61 dBA | (not checked here) | module | cheap; TDK: not recommended for new designs. **The baseline** |
| ICS-43434 breakout | I2S | 64 to 65 | 120 dB SPL [verified] | chip 3.5 × 2.65 × 0.98 | TDK's English page says EOL. **Only 3 to 4 dB better than the baseline: not worth buying just for this** |
| **TDK T5848** | **I2S, 24-bit** | **68 (HQ)** | **133 dB SPL (HQ)** [verified] | chip 3.5 × 2.65 × 0.98 (the same package as the ICS-43434) [verified] | a bare chip (LCSC lists it); the datasheet v1.0 (2024) is marked pre-production; **no cheap module found**; the 2.0 to 3.3 MHz clock suits 48 kHz x 64 = 3.072 MHz [calc, to check in the datasheet] |
| Infineon IM72D128 | PDM | 72 | 128 dB SPL [verified] | small LLGA | PDM goes through the ESP32's one hardware port (16-bit?); a bare chip; IP57 |
| A finished microphone (a phone, a DJI Mic Mini, any USB microphone) | n/a | n/a | n/a | n/a | a **reference** to listen against |

**Why T5848 before IM72D128:** it is I2S, so the **same firmware path** as the baseline; 24-bit; the same package size as the ICS-43434; so the carrier and the code stay almost the same when we swap. IM72D128 is a tick better on paper, but it needs the PDM path whose quality I cannot judge.

**The catch:** a bare 3.5 × 2.65 mm bottom-port chip needs a **tiny carrier PCB** (the chip and a few passives) and reflow or hot-air soldering. `CLAUDE.md` says **no custom PCB in this phase**, so this needs the owner's decision (§6). I have **not** found a cheap ready module for it; the maker's evaluation board was quoted at about 37 US dollars by the other opinion, which I did not verify.

**My staging (a proposal):**
1. **Stage 1:** INMP441-class module in the real body, with thin foam and a small windscreen; record with the test table below. Many answers (mechanics, tone, level) come from this alone.
2. **Stage 2, only if the noise floor is audible at the target distance in a quiet room:** a T5848 on a tiny carrier (needs the owner's go-ahead), through the same replaceable bracket.
3. **Reference throughout:** the phone, and a DJI Mic Mini or another known USB microphone if one can be borrowed.

## 5 · A replaceable pickup (a good idea, with a bonus)

Make the microphone sit on a **small printed bracket** behind the hole. Because the lid is removable and the hole (38 mm) is **larger than the module** (16.7 mm wide), the module can be **installed and swapped from the front, with the lid off**, on a small connector (say four to six wires), without printing a new body. The outside stays the same; only the bracket and the foam change.

## 6 · Questions for the owner

1. **Do you accept stage 1 as the plan** (cheap module first, listen, then decide)?
2. **A tiny carrier PCB for a bare microphone chip** (the T5848): is that allowed later, though `CLAUDE.md` says no custom PCB in this phase? Can you solder very small chips (reflow, hot air)?
3. Do you have, or can you borrow, a **DJI Mic Mini** or another USB microphone to listen against?
4. **Battery space:** the other opinion suggested a general expansion space instead of a dedicated battery bay. I agree: the same volume, named "expansion".

## 7 · Test plan (adopting the other opinion's table, with two additions)

Same distance, same voice, noise cancellation and auto gain off where possible, loudness matched before listening.

| Test | Look for |
|---|---|
| Quiet room, normal talk | natural and clear |
| Five seconds of silence | audible floor |
| 10 cm close talk | pops, clipping |
| 30 cm on the desk | full and clear |
| Operate the key while talking | how much mechanical noise is recorded |
| Thirty minutes | dropouts, clicks |
| **Added:** with and without the lid and the foam | what the hole and the felt do to the tone |
| **Added:** hold it, then put it on the stand | handling noise and desk noise |

## Sources

[ICS-43434 datasheet v1.2](https://cdn.sparkfun.com/assets/a/9/c/9/1/DS-000069-ICS-43434-v1.2.pdf) · [TDK ICS-43434](https://invensense.tdk.com/products/ics-43434/) · [TDK T5848](https://invensense.tdk.com/products/digital/t5848/) · [T5848 datasheet](https://invensense.tdk.com/wp-content/uploads/2024/04/DS-000479-T5848-Datasheet-v1.0.pdf) · [Infineon IM72D128 product brief](https://www.infineon.com/content/dam/infineon/row/public/documents/24/45/infineon-mems-im72d128v01-productbrief-en.pdf) · [Infineon IM73D122](https://infineon.com/cms/en/product/sensor/mems-microphones/mems-microphones-for-consumer/im73d122) · [ESP-IDF I2S (ESP32-S3)](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/peripherals/i2s.html) · [DJI Mic Mini specs](https://www.dji.com/mic-mini/specs)
