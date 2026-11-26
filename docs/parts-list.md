# Parts list and measuring sheet

## What to buy first, and what can wait (2026-11-26, updated after the owner's questions)

The enclosure prints and the electronics bench test do **not** depend on each other, so you can order now.

**Buy now, for the bench test:**
| What | Exactly which | Notes |
|---|---|---|
| Controller | **Seeed XIAO ESP32S3, the plain one** (not "Sense", not "Plus") | the plain board is what the plans and the CAD assume. The **Plus** has 16 MB flash and 9 extra castellated GPIO pads on the edge but a **different pinout** and a battery ADC path; nothing we need; its length is quoted as 17.8 mm by one source and 17.5 mm by another. **Sense** adds a camera and microphone board: bigger, not wanted. It comes with loose pin headers: **solder them on** to use it on a breadboard |
| Microphone 1 | **INMP441 standalone I2S microphone module**, 6 pins (VDD, GND, SD, WS, SCK, L/R), **2 pieces of the SAME listing** | **with pins already soldered** if offered (it saves time on the bench). **No speaker amplifier on the board.** Round or square does not matter; the pin rows (3 on each side or all 6 on one side) do not matter either |
| Microphone 2 | **ICS-43434 standalone I2S microphone module**, 6 pins, **2 pieces of the same listing** | same rules. **Do not buy the boards with MAX98357**: that chip is a small **speaker amplifier** (I2S in, a speaker out); those boards are for voice assistants that talk back; talk.01 has **no speaker**, so a board with it only adds size and noise. Look for a **small bare microphone board with the chip and 6 pins**, as you found |
| Switches | **6 × 6 × 4.3 mm tact switch, 4 pins, through-hole** ("轻触开关 6x6x4.3"), about 20 | no particular brand or model is needed yet: they are for the bench and for measuring; a quiet type comes later |
| Cable, wires, breadboard | **your own**: a USB cable that carries **data** (not charge-only), Dupont wires, a breadboard | any brand. Jumpers: male-to-male if the boards have male pins soldered on |

**Why two of the same listing:** the bracket and the hole will be designed for **one exact board**, and cheap boards vary from seller to seller. Buy two of one listing, send me the product page's size and a **photo of both sides with a ruler** when they arrive; I design the bracket for that board.

**What to check when the microphone boards arrive:** a small round hole in the board near the chip is the **sound hole**; the sound comes in from the side with the hole, the chip is on the other side. Photograph both sides. For the ICS-43434 look at the chip's marking if it can be read.

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
