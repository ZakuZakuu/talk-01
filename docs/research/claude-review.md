# Claude review — USB microphone routes (desk research)

Date: 2026-11-25 · Status: **desk research only. Nothing was built, flashed, listened to or measured.**
Scope: the "Independent technical research" item of [roadmap.md](../roadmap.md), under the constraints in [CLAUDE.md](../../CLAUDE.md).

> **中文摘要**
> 1. 现成的、可复现的"USB 麦克风"开源方案有，但**没有一个同时带 HID 按键**；音频加 HID 的复合设备需要我们自己合并描述符。
> 2. 证据比我上一轮聊天时的直觉更偏向 **ESP32-S3**：唯一有 48 kHz 实测记录的现成方案是 S3 + I2S（`usb-mic`，MIT）。我之前"倾向 RP2040"的判断**证据不足**，现已改为：主选 S3，备选 RP2040/RP2350。
> 3. RP2040 路线的现成项目（Mico、ANAVI）采样率都是 **16 kHz**，适合语音识别，不适合"自然录音"；能否做到 48 kHz 是待验证项。
> 4. INMP441 已被 TDK 标为不推荐用于新设计，DigiKey 标 Obsolete。它只适合当"先跑通"的基线。
> 5. 授权上最大的坑：Mico 的硬件是 **CC BY-NC-SA**（非商用），ANAVI 全项目是 **CC BY-SA**（相同方式共享）。只当参考，不复制硬件文件。
> 6. 所有音质数据都是作者自测，仓库里没有 WAV 样本，**不能当作音质证据**。

## 1. How to read this document

Evidence tags used below:

- **[read]** — I cloned the upstream repository (shallow) and read the file named.
- **[web]** — taken from a web search result or web page, not independently confirmed.
- **[inferred]** — my reasoning from the above; may be wrong.
- Anything with no tag is an opinion.

Not done: no build, no flash, no listening, no GitHub issue review (issue API is outside this session's scope), no check of the Espressif documentation pages beyond search snippets. Prices are indicative only.

## 2. Candidate audit

Commit dates are the HEAD of a depth-1 clone made on 2026-11-25.

| Candidate | HEAD | License (as found) | What it really is | Audio evidence | HID? | Verdict |
|---|---|---|---|---|---|---|
| [mmajjedi/usb-mic](https://github.com/mmajjedi/usb-mic) | `c09a07f` 2026-11-07 | MIT [read: `LICENSE`] | ESP32-S3 + INMP441, ESP-IDF. 73-line `main/usb_mic.c`. 48 kHz / mono / 16-bit [read: `sdkconfig.defaults`] | Self-measured iPhone comparison table in README; **no WAV files in repo** [read] | No | **Best starting recipe.** Most complete reproducible 48 kHz example found. |
| [espressif/usb_device_uac](https://github.com/espressif/esp-iot-solution/tree/master/components/usb/usb_device_uac) | v1.3.2, 2026-08-18 | Apache-2.0 [read: `license.txt`] | Vendor UAC device component on top of `espressif/tinyusb` 0.19.0~3 | Vendor component; changelog lists fixes for mic dropouts and Windows enumeration | Not out of the box; custom descriptors possible via `USB_DEVICE_UAC_AS_PART` [read: `Kconfig.uac`] | **Primary software base.** HID must be added by us. |
| [hathach/tinyusb](https://github.com/hathach/tinyusb) | `1384420` 2026-11-25 | MIT [read] | The USB stack used by both Espressif and Pico SDK | n/a | `hid_composite` example exists; no audio + HID example [read: `examples/device`] | **Foundation for the fallback route.** |
| [sameclub/dotmic](https://github.com/sameclub/dotmic) | `fdfa3e6` 2026-10-08 | MIT repo [read], but `lib/DotMicAudio` descriptors carry an Espressif Apache-2.0 header [read] | Push-to-talk USB mic on one specific handheld (S3AI Game, ESP32-S3), UAC1 + CDC, with a spectrum display | None (README states previews are layout checks, not captures) | No | **Interaction reference only.** Tied to specific hardware and pinned toolchain. |
| [AnaviTechnology/anavi-dev-mic](https://github.com/AnaviTechnology/anavi-dev-mic) | `f742ae0` 2024-10-23 | **CC BY-SA 4.0** for the whole project [read: README] | XIAO RP2040 + PDM MEMS mic, KiCad design, shipped via Crowd Supply | Product, but 16 kHz [web: CNX Software] | No | **Reference only.** Share-alike would bind anything copied. No firmware in this repo [read]. |
| [mkvenkit/mico](https://github.com/mkvenkit/mico) | `4c48a1c` 2022-01-06 | Software MIT; **hardware CC BY-NC-SA 4.0**, commercial builds need permission [read: README] | RP2040 + PDM mic. Firmware = lightly modified Microphone Library for Pico (Apache-2.0 [read]) | 16 kHz example config, `CFG_TUD_HID 0` [read: `tusb_config.h`] | No | **Do not reuse the PCB.** Confirms the flag in `hardware-research.md`. |

### 2.1 Notes per candidate

**usb-mic (ESP32-S3 + INMP441)**
- Dependency lock: IDF 5.5.5, `usb_device_uac` 1.3.2, `espressif/tinyusb` 0.19.0~3 [read: `dependencies.lock`]. These are exactly the versions to pin.
- Firmware does: 32-bit I2S read → fixed shift (`GAIN_SHIFT 13`) → 90 Hz 2nd-order high-pass → 16-bit mono. Mute is implemented by sending zero samples [read]. That is a good, honest pattern for our mute LED: it reflects what is actually sent.
- Hardware: 100 Ω series + 100 µF to ground on the mic supply, to remove USB noise. This is a cheap fix worth keeping [read: README].
- README's own numbers: voice-to-noise ~38 dB (with both fixes) versus ~36 dB for the phone mic; noise floor −63 dB vs −68 dB [read]. Single author, single room, one phone, no published recordings. **This is encouraging but is not audio evidence we can rely on.**
- Code observations, from reading only [inferred]: `i2s_channel_read(..., portMAX_DELAY)` runs inside the USB audio callback, and filter state is shared with that callback. This may be fine, but it is the first place to look if dropouts appear in the 30-minute test.
- README and walkthrough both say one build cannot be compatible with Windows and Linux (Android counts as Linux) at the same time, and this repo is set to Windows + iPhone/macOS [read: `docs/walkthrough.md`]. Fine for a Windows-first v0.1; relevant for any future "works everywhere" or SDK claim.

**Espressif `usb_device_uac`**
- Active: changelog has v1.3.2 (2026-08-18) "fix chronic mic-stream dropouts" and v1.2.3 (2026-03-05) "fix Windows multi-channel UAC enumeration (Code 10)" [read: `CHANGELOG.md`]. Good sign of maintenance, but also shows that exactly the failure modes we care about have occurred before.
- The code uses `UAC2_ENTITY_*` identifiers [read: `usb_device_uac.c`], so it likely presents as USB Audio Class 2.0 [inferred]. Windows 10 1703 and later ship an in-box USB Audio 2.0 driver (`usbaudio2.sys`) [web: Microsoft Learn], so no driver install should be needed, but this must be confirmed by enumeration on the owner's actual PC.
- Not supported: dynamic sample-rate change; Windows and Linux simultaneously [read: README].
- HID: no ready path. The Kconfig option `USB_DEVICE_UAC_AS_PART` says that you then write your own `tusb_config.h` and `usb_descriptors.c` [read]. That is where a HID keyboard interface would be added. **Unproven; this is the main integration risk of the primary route.**

**TinyUSB**
- Its docs state support for USB Audio Class 1.0 and 2.0 [read: `docs/reference/class/audio.rst`]. Relevant examples: `audio_test` (1-channel UAC2 mic), `audio_test_multi_rate` (UAC1 at full speed), `cdc_uac2` (audio + CDC composite), `hid_composite` (HID composite), `uac2_headset` [read]. No example combines audio with HID, but `cdc_uac2` shows that audio inside a composite is a normal pattern [inferred].

**DotMic**
- Useful as a behavior reference: "hold to talk, release to mute", with the stream staying connected but submitting zero samples when the key is not held [read: README]. Very close to what the lever might do if we ever gate audio.
- UAC1 mono 48 kHz 16-bit with a CDC port [read: README], built on Arduino-ESP32 with a custom `DotMicAudio` library and a pinned platform/core [read: `platformio.ini`]. A web search found an open request for a USB Audio class in the official Arduino-ESP32 core (issue #12053) [web], which fits why DotMic needs its own library. **Avoid the Arduino route for us**; it looks fragile and version-locked.
- Mixed licensing inside an MIT repo (Espressif Apache-2.0 headers; vendored MIT board files). Whoever reuses code must keep those notices.

**ANAVI Dev Mic / Mico (RP2040)**
- Both use PDM MEMS microphones and the open-source Microphone Library for Pico, with TinyUSB for output [read; web]. ANAVI's published sample rate is 16 kHz [web]; Mico's example is configured for 16 kHz [read].
- ANAVI's schematic contains both an ST MP23DB01HP and a SPH0641LU4H-1 symbol [read]; the press coverage names only the ST part [web]. Which is populated is unverified.
- Can the RP2040 route reach 48 kHz? **Unknown.** The library is configurable but I did not find a 48 kHz USB example.

## 3. Route comparison

| | A. ESP32-S3 + I2S MEMS, ESP-IDF + `usb_device_uac` | B. ESP32-S3, Arduino-ESP32 (DotMic style) | C. RP2040/RP2350 + TinyUSB (PDM or I2S via PIO) | D. USB audio chip + separate HID MCU + hub |
|---|---|---|---|---|
| Existing reproducible recipe | **Yes**, 48 kHz (usb-mic) | Partial, hardware-specific | Yes, but 16 kHz and PDM | None found |
| Audio + HID in one device | Needs custom descriptors | Needs patched/custom USB stack | Needs merging TinyUSB examples | Trivial per chip, but needs a hub |
| Stack maturity | Vendor component, active | Community, pinned versions | **Most mature stack (TinyUSB)** | Fixed-function chips |
| Licenses | MIT + Apache-2.0 | MIT + Apache-2.0 | MIT / BSD / Apache-2.0 | n/a |
| Size / cost | XIAO-class 21 × 17.5 mm board [web] | same | XIAO RP2350, 21 × 17.5–17.8 mm [web] | Largest: extra hub |
| Unneeded hardware | Wi-Fi/BT unused | same | none | n/a |
| Main risk | HID integration; Windows/Linux exclusivity | Toolchain fragility | 48 kHz capture and clock handling unproven | Size, cable, complexity |

Route D was not researched further; the hub alone makes it a poor fit for a 90 × 55 × 20 mm handheld, and it leaves little room for the "hackable" goal.

## 4. Recommendation

This **revises** my earlier chat suggestion. I had leaned towards RP2040 because TinyUSB is the more mature stack. The audit does not support that on audio: every RP2040 example is 16 kHz, while the S3 route has a documented 48 kHz recipe.

**Primary: Route A** — ESP32-S3 (native USB) + I2S digital MEMS mic + ESP-IDF 5.5 + `usb_device_uac` 1.3.2, starting from `usb-mic` (MIT). Add a HID keyboard interface via custom descriptors.
- Why: the only complete, current, permissively licensed recipe at 48 kHz; vendor-maintained USB audio component.
- What is unproven: audio and HID in one descriptor set; 30-minute stability on Windows.

**Fallback: Route C** — XIAO RP2350 (or RP2040) + TinyUSB, merging `audio_test_multi_rate`/`cdc_uac2` with `hid_composite`, capturing the mic through PIO.
- Why fallback: strongest USB stack and likely the easiest audio + HID composite, but I found no 48 kHz precedent.
- Switch to it if HID cannot be added cleanly to the Espressif component, or if the S3 route shows dropouts.

**Decision gate (suggested, owner to confirm):** one evening with the S3 board and `usb-mic` unmodified → confirm it enumerates on the owner's Windows PC and records a clean 30 minutes → then try adding HID. Only then decide whether to stay on A.

## 5. Microphone part

- INMP441: TDK lists it as NR/ND (not recommended for new designs); DigiKey lists the part as obsolete [web]. Cheap modules sold under this name are easy to buy, but I cannot tell what die is on any given module [inferred]. Use it as a **baseline to get the pipeline working**, not as a final choice.
- ICS-43434: sources conflict (one TDK page says EOL, another says production) [web]. Check before designing it in.
- Modern replacements: TDK's own comparison table points to the T5838 for some older I2S parts but names no direct replacement for INMP441 [web]. The T5838 is PDM and I did not verify it. ANAVI's shipped design uses an ST PDM part [web].
- Interface matters: I2S and PDM are not interchangeable. The S3 route as documented uses I2S; PDM would need a different capture path.
- Practical suggestion: buy two or three candidate modules (one INMP441 baseline, one or two currently active I2S/PDM parts after reading their datasheets) and A/B them with the test in `hardware-research.md`. Acoustic port design and handling-noise isolation will probably matter more than the part number.

## 6. Rough prototype BOM

Indicative, unverified. Owner already has FDM printer and basic supplies; **no purchase is authorized by this document**.

| Item | Note | Cost basis |
|---|---|---|
| ESP32-S3 board with native USB, compact | XIAO ESP32S3 (launch price US$7.49; current retail listings vary by retailer and currency [web]); usb-mic README also names an S3 Super Mini [read] | indicative |
| I2S digital MEMS mic module | INMP441 baseline + 1–2 alternatives | unverified |
| 100 Ω resistor + 100 µF capacitor | Supply filter from usb-mic | negligible |
| Lever switch (micro/snap-action or tactile) | Choose by feel; the lever is the product | unverified |
| Status LED + resistor | LED must reflect firmware state | negligible |
| Slide switch | Candidate for mute/lock | unverified |
| Hinge pin (e.g. metal pin), screws, foam for mic port | Mechanical | unverified |

Likely well inside the CNY 200 target from `hardware-research.md`, but that is my estimate, not a quote.

## 7. Licensing plan (proposal; owner decides)

- Our software: MIT (as already intended). Dependencies seen so far: MIT (TinyUSB, usb-mic, DotMic), Apache-2.0 (Espressif component, Microphone Library for Pico). Apache-2.0 notices must be preserved if code is vendored.
- Do **not** copy ANAVI (CC BY-SA 4.0) or Mico (CC BY-NC-SA 4.0) hardware files into this repository. Using them as inspiration for ideas is fine.
- Hardware and CAD: separate license decision before any design files are published. Options to discuss: a permissive hardware license, or a Creative Commons license for the enclosure only.
- TE-inspired design: keep identity original. See [`discussion-log.md`](../discussion-log.md) for the specific elements to avoid copying.

## 8. Unknowns that need real hardware

1. Does the S3 build from `usb-mic` enumerate as a standard input device on the owner's Windows PC, and does it survive sleep and reconnect?
2. Can a HID keyboard interface be added to the Espressif UAC component's custom-descriptor path without breaking enumeration?
3. 30-minute recording: dropouts, clock drift, noise?
4. Audio against the phone or a known mic, per the test plan in `hardware-research.md`. Unprocessed WAVs only.
5. Handling and lever noise with the mic mounted in a shell; effect of foam and mic port geometry.
6. Whether the RP2040/RP2350 route can capture and stream at 48 kHz.
7. Key-up reliability (no stuck modifiers) across unplug, sleep and mode changes.

## 9. Open questions for the owner

See the end of [`discussion-log.md`](../discussion-log.md).

## Sources

- [mmajjedi/usb-mic](https://github.com/mmajjedi/usb-mic) · [espressif/esp-iot-solution — usb_device_uac](https://github.com/espressif/esp-iot-solution/tree/master/components/usb/usb_device_uac) · [hathach/tinyusb](https://github.com/hathach/tinyusb) · [sameclub/dotmic](https://github.com/sameclub/dotmic) · [AnaviTechnology/anavi-dev-mic](https://github.com/AnaviTechnology/anavi-dev-mic) · [mkvenkit/mico](https://github.com/mkvenkit/mico)
- [ANAVI Dev Mic coverage (CNX Software)](https://www.cnx-software.com/2024/08/20/anavi-dev-mic-digital-omnidirectional-microphone-raspberry-pi-rp2040-mcu/)
- [USB Audio 2.0 drivers (Microsoft Learn)](https://learn.microsoft.com/windows-hardware/drivers/audio/usb-2-0-audio-drivers)
- [TDK INMP441 product page](https://invensense.tdk.com/digital/inmp441) · [DigiKey INMP441ACEZ-R7](https://www.digikey.com/en/products/detail/tdk-invensense/INMP441ACEZ-R7/2606606) · [TDK ICS-43434](https://invensense.tdk.com/products/ics-43434/)
- [arduino-esp32 issue #12053 (USB Audio class request)](https://github.com/espressif/arduino-esp32/issues/12053)
- [XIAO ESP32S3 (CNX Software)](https://www.cnx-software.com/2023/03/22/xiao-esp32s3-tiny-esp32-s3-wifi-4-and-ble-5-0-module-for-iot-ai-robotics/) · [XIAO RP2350 (CNX Software)](https://www.cnx-software.com/2024/08/09/xiao-rp2350-tiny-usb-c-board-raspberry-pi-rp2350-mcu/)
- [Teenage Engineering EP-2350 FX MIC (Thomann)](https://www.thomannmusic.com/teenage_engineering_ep_2350_fx_mic.htm) · [Synth Anatomy](https://synthanatomy.com/2026/08/teenage-engineering-ep-2350-fx-mic-the-mic-with-built-in-sample-playback.html)
