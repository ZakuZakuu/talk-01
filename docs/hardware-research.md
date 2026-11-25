# Hardware research — candidate routes, not final selection

## Selection priorities
1. Working and reproducible open-source implementation, preferably tested in real hardware.
2. Natural voice for ordinary podcast/narration, reasonable cost and low noise.
3. Fast development-board build; little bespoke circuit work.
4. Standard USB audio plus programmable HID, Windows first.
5. Permissive licensing (MIT/BSD/Apache-2.0 preferred); audit hardware, firmware and dependencies separately.

## Candidate sources
These links are leads from preliminary discussion, not independently reproduced or audited. Claude should check current upstream source, exact licenses, build instructions, known issues, sample recordings, and component availability before recommending reuse.

| Candidate | Why investigate | Key uncertainty |
|---|---|---|
| [mmajjedi/usb-mic](https://github.com/mmajjedi/usb-mic) | ESP32-S3 + INMP441, reported 48 kHz mono USB audio; development-board reference | Real audio quality, power noise, exact license and composite HID integration |
| [Espressif USB UAC](https://github.com/espressif/esp-iot-solution/tree/master/components/usb/usb_device_uac) | Vendor-supported audio component | Windows compatibility, descriptor/endpoint constraints and HID coexistence |
| [TinyUSB](https://github.com/hathach/tinyusb) | USB Audio and HID stack/examples | Concrete composite-device example on selected MCU; validate build and host enumeration |
| [ANAVI Dev Mic](https://github.com/AnaviTechnology/anavi-dev-mic) | Productized RP2040 open hardware, KiCad reference | Sample-rate constraints and reciprocal hardware license obligations |
| [DotMic](https://github.com/sameclub/dotmic) | Handheld microphone / push-to-talk interaction reference | Maturity, exact license, audio quality and HID support |
| [Mico](https://github.com/mkvenkit/mico) | RP2040 PCB and firmware reference | Reported noncommercial hardware terms: do not incorporate unless permission and terms verified |

Also evaluate an alternative: use an existing well-tested USB audio module plus separate HID MCU and USB hub if single-MCU integration is too costly. Compare size, cost, reliability and one-cable feasibility. Do not assume S3 is mandatory.

## Provisional prototype
ESP32-S3 board with exposed native USB (not just USB-UART), INMP441 or better validated compatible module, basic switch/LED. Existing ESP32-C3 can test interactions but its fixed USB Serial/JTAG is not a general-purpose UAC/HID device. Existing basic electronic supplies and 3D printer are available; no need to rebuy them. S3 is a suggested purchase, not final architecture. No purchases or PCB fabrication authorized by this document.

Baseline INMP441 is a low-cost test option, not necessarily final sound quality. Investigate higher-SNR digital MEMS modules and established electret/USB audio solutions when evidence warrants. PDM and I2S are not interchangeable; check supported interface and sample clocks. Prefer 48 kHz mono, 16-bit sufficient, 24-bit optional; sample format alone does not establish quality. Preserve clean audio path.

## Acceptance tests
- Windows enumerates as standard audio input and HID; reconnect/sleep recovery.
- Record identical speech at ~10 cm and ~30 cm versus a phone or known microphone, same room and matched loudness; save unprocessed WAV. Listen for intelligibility, natural timbre, hum, clipping, plosives and hand/lever noise. Compare room noise and level; do not claim calibrated SNR from casual tests.
- 30-minute recording with no audible dropouts; repeated key down/up, no stuck modifiers or unintended send.
- Stand stability, cable clearance, easy handheld use; test mechanical isolation before cosmetic polishing.
- Target electronics prototype under CNY 200 if reasonable (estimate, not verified BOM).

## Decision gate
Recommend one primary route, one fallback, exact module/board and minimal BOM only after source and license checks. Identify evidence versus assumptions. No custom PCB until audio and composite USB are demonstrated on actual hardware.
