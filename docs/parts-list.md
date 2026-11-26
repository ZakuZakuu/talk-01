# Parts list and measuring sheet

## What to buy first, and what can wait (2026-11-26, updated after the owner's questions)

The enclosure prints and the electronics bench test do **not** depend on each other, so you can order now.

**Buy now, for the bench test:**
| What | Exactly which | Notes |
|---|---|---|
| Controller | **Either the Seeed XIAO ESP32S3 (plain, not "Sense", not "Plus") or, the owner's cheaper choice, an ESP32-S3 Super Mini** (see below) | the plain board is what the plans and the CAD assume. The **Plus** has 16 MB flash and 9 extra castellated GPIO pads on the edge but a **different pinout** and a battery ADC path; nothing we need; its length is quoted as 17.8 mm by one source and 17.5 mm by another. **Sense** adds a camera and microphone board: bigger, not wanted. It comes with loose pin headers: **solder them on** to use it on a breadboard |
| Microphone 1 (optional) | **INMP441 standalone I2S microphone module**, 6 pins (VDD, GND, SD, WS, SCK, L/R), **1 piece, only if wanted** (the round Ø13.8 mm one the owner found) | **the pins come loose in the bag on the round boards: do NOT solder them yet** (see below: which side the sound hole is on decides how to solder). **No speaker amplifier on the board.** Round or square does not matter; the pin rows (3 on each side or all 6 on one side) do not matter either |
| Microphone | **ICS-43434 standalone I2S microphone module**, 6 pins, **1 piece** (the round Ø13 mm one the owner found) | same rules. **Do not buy the boards with MAX98357**: that chip is a small **speaker amplifier** (I2S in, a speaker out); those boards are for voice assistants that talk back; talk.01 has **no speaker**, so a board with it only adds size and noise. Look for a **small bare microphone board with the chip and 6 pins**, as you found |
| Switches | **6 × 6 × 4.3 mm tact switch, 4 pins, through-hole** ("轻触开关 6x6x4.3"), about 20 | no particular brand or model is needed yet: they are for the bench and for measuring; a quiet type comes later |
| Cable, wires, breadboard | **your own**: a USB cable that carries **data** (not charge-only), Dupont wires, a breadboard | any brand. Jumpers: male-to-male if the boards have male pins soldered on |

**Which controller board (owner's question, 2026-11-26: must it be the XIAO? about 50 yuan against about 20 for a Super Mini):**
- **The chip must be an ESP32-S3** (or S2) **with a native USB port**; the USB audio and keyboard functions need it. The open-source recipe we start from says so, and names "DevKitC-1 (dual USB-C) for easy development; Super Mini or XIAO ESP32-S3 for a compact build" ([usb-mic README](https://github.com/mmajjedi/usb-mic); it names no tested board).
- **Not usable:** ESP32-H2 (only the fixed-function USB Serial/JTAG controller, no OTG: [Espressif](https://docs.espressif.com/projects/esp-faq/en/latest/software-framework/peripherals/usb.html)), ESP32-C3 and the plain ESP32 (the recipe says they cannot run the USB microphone firmware), and boards without a USB connector (Waveshare's ESP32-S3-Tiny has none).
- **A big ESP32-S3 dev board (N8R8, usually two USB-C ports)** works for the bench (use the port marked "USB", not "UART") but is too big for the enclosure.
- **ESP32-S3 Super Mini** works on paper and is the cheaper choice. **The boards sold under that name differ between sellers** (one listing says 22.5 × 18 mm; the number of exposed pins and even the chip variant are quoted differently), so **check the listing**: the chip says ESP32-S3; a USB-C connector; BOOT and RESET buttons; the size given or a photo with a ruler. Its pins are flexible: the recipe's GPIO 4, 5, 6 are only defaults.
- **XIAO** costs more but has an official, fixed pinout and size and a CAD file, so anyone can rebuild from our files. **Proposal:** the Super Mini for the bench and the first build; if it works, the shell is designed around the board the owner actually has; for a public release, list the XIAO as the reference board.

**The reference boards (found by the owner on Taobao, 2026-11-26).** The design uses **these two round boards** (from the seller's pictures, to be measured when they arrive). The 16.7 × 12.7 mm rectangle used in the first fit check was only a stand-in from another maker's product page.

| Board | Seen in the listing | What it tells |
|---|---|---|
| **ICS-43434 module** | round, **13 mm across**; two rows of 3 through-hole pads (a square pad marks pin 1); the chip on the same face, its top marking reads something like "762 2QW"; a **"PS" solder-bridge** marking for the left/right channel (the description: bridge the right and middle pad = left channel, the default); pins WS, L/R, SCK, SD | the shape and size of the bracket; the pin order must be read from the board's own print |
| **INMP441 module** | round, **13.8 mm across** with two notches; pads of **Ø1.3 mm** in two rows of 3; the seller's drawing gives 7.4 mm, 2.3 mm and 1.2 mm (unclear which is which, to be measured); three-pin yellow header strips come **loose in the bag, not soldered**; the chip's top marking reads something like "MA29 H11P" | the same shape and size class as the 43434 board: **one bracket can serve both** |

The chip markings do **not** tell me which die is on each board (they are not the maker's markings I know); that is fine for a baseline, and it matches the earlier warning that a module sold as "INMP441" may carry another chip.

**How many (owner's decision, 2026-11-26: as few as possible, no spares "just in case"; there is no hurry, a broken part can be bought again):**
- **The minimum that works: one XIAO ESP32S3 and one ICS-43434 module.** The seller says it replaces the INMP441 directly; both are I2S digital microphones with the same wires (VDD, GND, SD, WS, SCK, L/R), so the same wiring and firmware are expected to work.
- **What is given up** by skipping the INMP441: (1) the open-source recipe we start from was tested with an INMP441, so if the first test does not work, I cannot tell a chip difference from a fault in our wiring or code; that risk is small, since the chips are pin-compatible; (2) the cheap baseline for the "is the dearer chip really better?" listening test, which would then have to wait. If the owner wants both back later, an INMP441 costs about 10 yuan.
- The ICS-43434 is better on **paper** (65 dBA against 61 dBA signal-to-noise, from the maker's datasheets). These cheap boards' chips are not identified, so it is a datasheet claim and **not yet heard**.
- A few tact switches cost cents; they are the one place where a handful is worth buying.

**What to check when the microphone boards arrive, BEFORE soldering:** these chips have the sound port on the underside, so there should be a small round hole in the board under the chip: the **sound hole**. The sound comes in from the board's other face (the side without the chip). **Photograph both sides.** Do not let a breadboard or a pin header cover the sound hole. I will say how to solder the pins (or wires) once you tell me which face has the hole. The pad order differs between makers: read it from each board's own silkscreen.

**Not needed now:** the coiled USB-C cable (use your own cable for the bench; the coiled one is for the real build and for measuring the plug), silicone wire (the soft stranded wire for inside the enclosure), and the mechanical parts (10 to 18) and the PETG and stickers (19 to 21): wait for the bench test and the cap print, then the CAD will name the exact sizes.

The plan for the bench test is in [`bench-test-plan.md`](bench-test-plan.md).

## A · Electronics (stage 1)

| # | Item | Qty | What to look for (and search words) | Notes |
|---|---|---|---|---|
| 1 | **Seeed XIAO ESP32S3** | 1 (2 if you like a spare) | the plain board, **not "Sense", not "Plus"**; with or without header pins (you can solder wires directly). "Seeed XIAO ESP32S3" | native USB; 21 × 17.5 mm ([CNX](https://www.cnx-software.com/2023/03/22/xiao-esp32s3-tiny-esp32-s3-wifi-4-and-ble-5-0-module-for-iot-ai-robotics/)) |
| 2 | **INMP441 I2S microphone module** | 2 | "INMP441 全向麦克风模块 I2S"; the common small board with 6 pins (VDD, GND, SD, WS, SCK, L/R) | about 10 yuan; **the chip is "not recommended for new designs"**, fine as the baseline |
| 3 | **ICS-43434 I2S microphone module** | 1 (2 if cheap) | "ICS-43434 I2S 数字麦克风模块"; ask the seller for a photo showing the chip marking | about 30 to 40 yuan; TDK's English page marks the chip EOL, so keep a spare |
| 4 | **Tact switch 6 × 6 mm, 4.3 mm high** | 20 | "轻触开关 6x6x4.3"; also a few in 5 mm | the common type, for the fit test |
| 5 | **Silent tact switch 6 × 6 mm** | 10 | "静音轻触开关 6x6"; low-force | for the bottom (latch) switch |
| 6 | **Small tact switch 4.5 × 4.5 mm** (optional) | 10 | "4.5x4.5 轻触开关" | if the 6 × 6 is too big behind the wheel |
| 7 | **Coiled USB-C cable** | 2 | "螺旋 USB-C 数据线 卷线"; **data capable**, not charge-only; one USB-C to USB-C and one USB-C to USB-A; stretched length 1 to 1.5 m | the plug's overmould decides the top notch: **measure it** |
| 8 | Dupont wires, breadboard, 2.54 mm pin headers | 1 set | "杜邦线 母对母 公对母", "面包板 400孔", "排针 2.54mm" | for the bench test |
| 9 | Silicone wire 30 AWG and heat shrink | 1 set | "硅胶线 30AWG 多色", "热缩管" | for the wiring inside |

## B · Mechanics and acoustics

| # | Item | Qty | What to look for | Notes |
|---|---|---|---|---|
| 10 | **Thin foam double-sided tape** | 1 roll each of 1 mm and 2 mm | "EVA 泡棉双面胶 1mm" / "2mm" | the microphone's soft mount |
| 11 | Adhesive felt sheet | 1 | "背胶毛毡 0.5mm" or 1 mm | behind the lid |
| 12 | Small foam windscreen | 1 pack | "领夹麦克风 海绵套 小号" | for the pickup hole |
| 13 | **Silicone bumper pads** | 20 | "硅胶脚垫 圆形 φ6x2" or smaller | the soft stop for the key's bottom |
| 14 | **Small compression springs, an assorted set** | 1 set | "压缩弹簧 套装 外径4 5 6mm 线径0.3 0.4"; free length 8 to 12 mm | the key's return; the wheel's detent |
| 15 | **Steel balls Ø2 mm** | 10 | "钢珠 2mm" | the detent ball (a test) |
| 16 | **Steel dowel pins Ø2 × 20 mm** | 10 | "不锈钢 圆柱销 2x20" | the key's hinge pin |
| 17 | **M2 screws assortment** (M2 × 4, 6, 8) and **M2 heat-set inserts** | 1 set | "M2 螺丝套装", "M2 热熔铜螺母 外径3.2 长3mm" | board posts and the hatch |
| 17b | **M2 self-tapping screws**, **countersunk (flat) head**, cross recess, the same as the owner's robots: **8 mm** long mainly, some 6 and 10 mm | 30 | "M2 自攻螺丝 十字 圆头 平头" assorted; if the owner's robot screws are M2, the same ones will do | the body is closed with these; look at the pack's label and tell me the size and head |
| 18 | Spare 1.75 mm filament pieces | (from a spool) | any | the wheel's axle in the mock-up |

## C · Printing

| # | Item | Qty | What to look for | Notes |
|---|---|---|---|---|
| 19 | **PETG filament** 1.75 mm | 1 spool | any good PETG, light or warm grey | the lid; the A1 mini lists PETG as supported ([Tom's Hardware](https://www.tomshardware.com/uk/reviews/bambu-lab-a1-mini)); PETG on an AMS lite is **not** checked |
| 20 | PLA 1.75 mm: warm light grey/beige, dark grey, orange | 1 spool each | "PLA 1.75 暖灰/米色", "深灰", "橙色" | the WARM palette; orange is the key |
| 21 | Printable sticker paper (A4, white or clear) | 1 pack | "激光/喷墨 不干胶贴纸 A4", or "水转印纸" | dial icons if you do not print them in colour |

## D · Tools

| # | Item | Qty | Notes |
|---|---|---|---|
| 22 | **Digital caliper**, 150 mm, 0.01 mm | 1 (if you have none) | "数显游标卡尺 150mm" |
| 23 | Multimeter, flush cutters, tweezers | if missing | |

## The measuring sheet (fill in when the parts arrive; photos with a ruler help)

| Part | Measure | Value |
|---|---|---|
| XIAO ESP32S3 | length × width × thickness (with and without pin headers); how far the USB-C sticks out of the board edge; its height above the board | |
| INMP441 module | length × width × thickness; **which side the microphone port is on**; the port hole's diameter and its distance from two edges; pin pitch | |
| ICS-43434 module | the same; also read the chip marking | |
| Tact switch 6 × 6 | body length × width × height; the button's height above the body; how far it travels | |
| Silent tact switch | the same, and how it feels (click or soft) | |
| 4.5 × 4.5 switch | the same | |
| Coiled cable | the **plug overmould** length × width × height; the strain relief length; the coil's outer diameter; the stretched and the relaxed length | |
| Silicone pad | diameter × height | |
| Spring | outer diameter, free length, wire diameter | |
| Dowel pin, balls | diameter, length | |

Send the numbers (a table or a photo of your notes). Anything unmeasured stays marked *typical* in the CAD.

## First prints (no electronics; the files are in [`../cad/`](../cad/README.md))
- the **feel mock-up**: body, three key blocks (3, 5, 7 mm), the wheel;
- the **calibration set**: clearance pockets, ridge gaps, line widths, and a snap-fit test lid and frame.
