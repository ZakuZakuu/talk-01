# Component selection (proposal, 2026-11-26)

Status: **a proposal for the owner to confirm. Nothing has been bought, measured or tested.** Sizes are marked **[verified]** (read from a datasheet or a listing, linked), **[typical]** (a usual value for the part class) or **[unverified]**. The CAD waits for the real parts in hand.

Why now: the owner asked to fix the part choices first and then design a version that is really buildable. The paper fit check is in [`../../design/concepts/v0.6/fit.png`](../../design/concepts/v0.6/README.md).

## Owner choices that drive this (2026-11-26)

WARM palette; the dial for the modes; labels as stickers or multi-colour printing; a bigger wheel (19 mm); two switches and a cam for the wheel, the switches placed inboard; a snap-fit lid; wired USB-C, no battery in v0.1 (room kept).

## Proposed selection

| Role | Proposed | Size | Status | Why / alternatives | Check on arrival |
|---|---|---|---|---|---|
| Controller | **Seeed XIAO ESP32S3** (not the Sense version) | 21 × 17.5 mm; one source says 17.8 | footprint [verified: [CNX](https://www.cnx-software.com/2023/03/22/xiao-esp32s3-tiny-esp32-s3-wifi-4-and-ble-5-0-module-for-iot-ai-robotics/), [espboards](https://www.espboards.dev/esp32/xiao-esp32s3/)]; thickness and USB-C overhang [unverified] | native USB; the recipe in [`claude-review.md`](claude-review.md) (usb-mic, MIT, 48 kHz); BLE kept for later. Fallback XIAO RP2350/RP2040 + TinyUSB | thickness with its USB-C; edge pads or pins; 3D/DXF files on Seeed's wiki (not opened) |
| Microphone | **A/B two I2S MEMS modules**: an INMP441-class baseline and an **ICS-43434** breakout | chip 3.5 × 2.65 × 0.98 mm [verified: [TDK](https://invensense.tdk.com/products/ics-43434/)]; a typical breakout 16.7 × 12.7 × 1.8 mm [verified for the Adafruit SPH0645 board: [listing](https://www.adafruit.com/products/3421)] | chip sizes verified; module sizes [unverified] | the final chip is decided by recording, not on paper. INMP441: not recommended for new designs. ICS-43434: TDK's English page says EOL, others say active; check stock first. The SPH0645 board is shown as sold out | **which side the port is on** and where the hole is in the carrier; the module's real size |
| Wheel sensing | **two switches + printed cam** (Gray code) | small switches about 4 to 4.5 mm [typical] | [typical] | absolute, nothing special to buy (see [`mode.png`](../../design/concepts/v0.5/README.md)). Later: AS5600 + magnet for fine control | switch height and travel; the cam lobe angles once their spacing is known |
| Key | **two small switches** under the slanted key (hold, click) | about 4 mm [typical] | [typical] | one stage first; the second adds the latch | the force needed; the feel through a printed key |
| Cable | **a coiled USB-C cable**, bought, with USB-A or USB-C at the other end | plug body size [unverified] | commercial coiled USB-C cables exist, e.g. a [StarTech listing](https://www.connection.com/product/startech.com-usb-c-to-usb-c-fast-charge-sync-rugged-coiled-3a-usb-2.0-tpe-jacket-aramid-fiber-50cm-19.7in/r2ccc-50c-usb-cable/41385243) with a strain-relieved plug | the size of its plug and its strain relief decide the notch on the top edge | measure the plug; length of the coil |
| Lid | printed PETG snap-fit lid (hooks + two in-plane arms) | 2.4 mm | design only | see [`lid.png`](../../design/concepts/v0.5/README.md) | coupon first; clearance on the owner's printer |
| Printer | the owner's FDM; multi-colour (AMS-style) for labels | features of about 1 mm | to be tested | stickers as the fallback | a test print of the dial |

## What is deliberately NOT chosen

- An **EC11 encoder** (relative; needs a home switch). Kept only as an alternative.
- A **battery or wireless**: room is kept (about 43 × 28 × 11 mm); not v0.1.
- A **custom PCB**: not in this phase. Two small boards (the switches, the mic) and wires.

## The fit check, in brief

On paper everything fits in the 58 × 92 × 22 mm body, but the depth is **tight** (about 1.6 mm to spare behind the wheel stack) and the board lies behind the wheel stack, so the cable's USB-C sits near the back of the top edge. Details: [`v0.6`](../../design/concepts/v0.6/README.md).

## A "measure first" shopping list (when the owner decides; nothing is ordered)

1. One XIAO ESP32S3 (plain, not Sense).
2. Two or three I2S microphone modules: an INMP441-class one and an ICS-43434 breakout, perhaps a third.
3. A handful of small switches in two heights.
4. One coiled USB-C cable.
5. Calipers (to measure the real sizes and replace every [typical] and [unverified] above).

## Risks still open

- **Acoustics:** the port, the felt and the gap behind the lid are untested; the A/B recording (with and without the lid) is the real test. No sound claim is made.
- **Depth:** 1.6 mm spare is little; a thicker board or a taller switch breaks it. The body can grow to 24 mm if needed.
- **Mic availability:** the ICS-43434 may be end-of-life; check stock before designing a carrier for it.
- **Firmware:** audio plus HID in one USB device has no ready example ([`claude-review.md`](claude-review.md)).

## Sources

[XIAO ESP32S3 (CNX)](https://www.cnx-software.com/2023/03/22/xiao-esp32s3-tiny-esp32-s3-wifi-4-and-ble-5-0-module-for-iot-ai-robotics/) · [XIAO ESP32S3 (espboards)](https://www.espboards.dev/esp32/xiao-esp32s3/) · [TDK ICS-43434](https://invensense.tdk.com/products/ics-43434/) · [Adafruit SPH0645 breakout](https://www.adafruit.com/products/3421) · [Alps EC11 datasheet](https://www.avnet.com/opasdata/d120001/medias/docus/196/Alps-Alpine-EC11-Series-EN-Datasheet.pdf) · [AS5600 datasheet](https://www.infineon.com/assets/row/public/documents/24/49/infineon-as5600-datasheet-en.pdf) · [StarTech coiled USB-C listing](https://www.connection.com/product/startech.com-usb-c-to-usb-c-fast-charge-sync-rugged-coiled-3a-usb-2.0-tpe-jacket-aramid-fiber-50cm-19.7in/r2ccc-50c-usb-cable/41385243)
