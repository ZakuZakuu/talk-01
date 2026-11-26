# Reference: the Teenage Engineering EP-2350 "TING" teardown (read 2026-11-26)

Status: **desk research from the maker's public pages. Nothing here was measured or tested by us.** The owner relayed a second opinion that found this material; this note checks it against the pages themselves. A claim is **[verified]** if I read it on a page named below, **[inferred]** if it follows from what was read, **[not found]** if I looked and it was not there.

## 1 · What the sources are

- **Adafruit guide "Hacking the Teenage Engineering EP-2350 Ting"** ([overview](https://learn.adafruit.com/hacking-the-teenage-engineering-ep-2350-ting), [teardown](https://learn.adafruit.com/hacking-the-teenage-engineering-ep-2350-ting/teardown-and-reassembly), [pinout](https://learn.adafruit.com/hacking-the-teenage-engineering-ep-2350-ting/pinout), [reverse-engineering](https://learn.adafruit.com/hacking-the-teenage-engineering-ep-2350-ting/reverse-engineering-techniques), [CircuitPython install](https://learn.adafruit.com/hacking-the-teenage-engineering-ep-2350-ting/install-circuitpython), [code](https://learn.adafruit.com/hacking-the-teenage-engineering-ep-2350-ting/code)). It does not name a hardware revision of the unit; it names the stock firmware file `ep-2350_firmware_1_0_8.uf2`.
- **The demo code** ([`code.py`](https://github.com/adafruit/Adafruit_Learning_System_Guides/blob/main/Teenage_Engineering_EP2350_Demo/code.py)): MIT, copyright Tim Cocks for Adafruit Industries.
- **A repo that makes the TING a USB microphone** ([JR-One-Yard/ep-2350-usb-mic](https://github.com/JR-One-Yard/ep-2350-usb-mic)).
- Not readable by me: the informal.cc teardown the guide links (an empty page for my reader).

## 2 · The second opinion, checked

| Claim | Result |
|---|---|
| Main controller RP2350A | **[verified]** (pinout page) |
| Audio codec Nuvoton NAU88L21, I2C control, I2S audio | **[verified]** |
| 2 MB flash | **[verified, with a caveat]**: the guide says the flash chip is a hypothesis it could not confirm |
| Three-axis accelerometer | **[verified]** on I2C 0x18, LIS331-compatible, with a non-standard chip ID; no part number |
| Stock firmware is a custom MicroPython; CircuitPython can replace it | **[verified]**; a CircuitPython board definition exists |
| 3.5 mm analog output | **[verified]** |
| Two switches plus a potentiometer in the lever | **[verified]**: HANDLE_OUT (GPIO20), a small non-tactile switch, "moved"; HANDLE_IN (GPIO19), a tactile switch pressed when fully squeezed; a potentiometer on GPIO28 in the pivot; "an internal spring that pushes it outward" |
| The microphone is an independent two-wire analog capsule, probably electret | **[partly]**: the guide says the microphone is wired to the codec "with two very thin wires". **The capsule type, size and part number are [not found]**; "electret" is an inference |
| Codec ADC SNR 103 dBA | **[conflicting]**: Nuvoton's pages give DAC 105 dB, another Nuvoton table gives ADC 98 and DAC 100, DigiKey lists 105/103. I could not match 103 to the ADC. It is an ADC figure anyway, not a microphone figure |
| The end-stop switch click is recorded by the microphone | **[verified, in the demo code, not the guide]**: a comment says `HANDLE_IN is the travel end-stop, and its tactile click leaks a loud thump into the mic`, so the code reads the other, soft switch to gate the microphone |
| It has been turned into a USB microphone | **[verified, thin]**: the repo exists, but see §4 |
| "Early version of the product" | **[not found]**: the guide names no revision |

## 3 · What the demo code shows about the audio chain

From `code.py` (these are the **demo's settings, not the hardware's limits**): 16 kHz, 16-bit, mono; the codec's analog microphone gain set to 14 dB (the range in the comment is -1 to 36 dB); a 120 Hz high-pass on the ADC "to strip the microphone's DC offset and slow subsonic bias drift"; the volume knob is "noisy enough to jitter by a few hundred counts while nobody is touching it". The handle starts muted and un-mutes while squeezed. **Nothing says how good the microphone is**: no noise figure, no comparison with another microphone. The claim that it is "about the level of a small DJI microphone" is **[not found]**; there is no source for it.

What this tells us: an analog capsule needs **tens of dB of gain** (14 dB analog here, with a high-pass), so noise pickup on the analog wires matters; that is the cost of the analog route.

## 4 · The USB-microphone repo: a caution

- Public, **1 commit, 0 stars**, **no LICENSE file** (the licence file is a 404; with no licence the default is "all rights reserved", so **we must not copy its code**).
- The README is a how-to for a Mac or iPhone. It does **not** say the sample rate, the audio path or the USB audio method [not found]; I did not read its `adapter/` or `bin/` folders.
- Its steps **overwrite the stock firmware**; Adafruit's guide warns that CircuitPython "will erase the samples, config JSON files, and anything else" on the device; the repo gives no recovery warning beyond a link to TE's firmware download.
- It uses the lever to talk (squeeze) and a top button to mute; **no HID** is mentioned.

## 5 · What talk.01 can learn (and what it can't copy)

**Useful lessons**
1. **The lever idea is confirmed in a shipped product**: a soft "moved" switch to start, a hard "seated" switch at the end, a potentiometer for position. That is our two-switch key.
2. **The bottoming-out click is a known problem**, and TE's own demo works around it by gating on the soft switch. For talk.01: **start talking on the soft first switch, put a rubber or silicone bump at the bottom stop, mount the microphone on foam**, and keep the second (latch) switch as a quiet confirm. Firmware can also ignore the first few milliseconds after the latch.
3. **A way into the bootloader**: TING uses "double press reset while holding the handle". talk.01 needs one too: a small **BOOT/RESET access inside the hatch** with the pins.
4. **Firmware that the user can replace** (drag-and-drop UF2 on an RP2350, or CircuitPython) is attractive for an "open, hackable" device (a goal from the first discussion).
5. **Gain staging**: an analog capsule needs a high-pass and a gain stage; a digital MEMS microphone needs digital gain before the 16-bit USB conversion ([`microphone-quality.md`](microphone-quality.md)).

**Not to copy:** TE's firmware, TE's branding or exact shapes. The pinout and the architecture are facts to learn from; the stock firmware belongs to TE. The Adafruit demo is MIT and may be reused with attribution if ever needed; the USB-mic repo may not.

## 6 · Do we change route? (my view; the owner decides)

There are two separate choices: **the controller** (ESP32-S3 or RP2350) and **the microphone** (a digital MEMS chip, or an analog capsule plus a codec as in TING).

| | Digital MEMS direct (our current plan) | Analog capsule + codec (TING) |
|---|---|---|
| Parts | microphone + controller | capsule + codec + controller |
| Soldering | a module with pin wires | the codec is a 5 x 5 mm QFN-class chip: a custom PCB, or a ready codec board [ready boards: not checked] |
| Noise pickup | the microphone's output is digital, so wire noise is not a worry | analog wires carry a small signal; layout matters |
| What you can choose | modules on the market | any capsule, and gain and filters in the codec |
| Needed here | input only | TING needs the output and effects; **we do not** |
| Known quality | unknown until recorded | unknown (the capsule is not identified) |

My view: **keep ESP32-S3 + digital MEMS as the primary** (fewest parts; matches the no-custom-PCB phase), and **write the TING-style route (RP2350 + analog capsule + codec) down as a documented alternative**, because (a) it is proven in a product and documented, (b) the RP2350 gives UF2 and CircuitPython hackability, (c) a bigger or better capsule is possible later. What would change my mind: stage-1 recordings that show the digital MEMS cannot reach the wanted quality; or the owner valuing drag-and-drop firmware above ESP32 features. Note that an RP2350 with a digital I2S microphone already was our fallback; it needs no codec.

## 7 · Cost of the stage-1 microphones (the owner's Taobao prices)

INMP441 about 10 yuan, ICS-43434 about 30 to 40 yuan, T5848 over 100 yuan and hard to buy. At those prices I now agree: **buy the INMP441 and the ICS-43434 together** (about 50 yuan), because the cost is small, and the ICS-43434 is widely used in AI-voice projects, so there are examples. (I had said it was not worth buying only for a 3 to 4 dB gain; at this price it is.) Skip the T5848 for now. **Check what is on the module**: the earlier research noted that a module sold under a name may carry a different chip; read the chip marking and note which side the port is on.

## Sources

[Adafruit TING guide](https://learn.adafruit.com/hacking-the-teenage-engineering-ep-2350-ting) · [demo code](https://github.com/adafruit/Adafruit_Learning_System_Guides/blob/main/Teenage_Engineering_EP2350_Demo/code.py) · [JR-One-Yard/ep-2350-usb-mic](https://github.com/JR-One-Yard/ep-2350-usb-mic) · [NAU88L21 datasheet (Adafruit copy)](https://cdn-learn.adafruit.com/assets/assets/000/145/031/original/DS_NAU88L21_DataSheet_EN_Rev2.8.pdf?1784907999) · [NAU88L21 at DigiKey](https://www.digikey.ca/en/products/detail/nuvoton-technology-corporation/NAU88L21YG/13147653)
