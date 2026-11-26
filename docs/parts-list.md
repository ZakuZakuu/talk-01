# Parts list and measuring sheet

## What to buy first, and what can wait (2026-11-26)

The enclosure prints and the electronics bench test do **not** depend on each other, so you can order now.
1. **Buy now, for the bench test** (items 1, 2, 3, 7, 8, 9 below, plus 22 the caliper if you have none): the XIAO ESP32S3, the two microphone modules, the coiled USB-C cables, the Dupont wires, breadboard and pin headers, silicone wire. A few tact switches (4, 5) are worth adding: they cost cents and are needed for measuring.
2. **Buy a little later, once the bench test works and the cap print is tried:** the mechanical bits (10 to 18) and the PETG and stickers (19 to 21). By then the CAD will name the exact sizes.
The plan for the bench test is in [`bench-test-plan.md`](bench-test-plan.md).

For the owner to buy item by item (nothing is ordered by Claude). Updated 2026-11-26. **Why a measuring sheet:** the CAD uses typical sizes until the real parts are measured. Quantities are generous: the parts are cheap and variants differ. Search words are suggestions for Taobao; check each listing's photos.

## A · Electronics (stage 1)

| # | Item | Qty | What to look for (and search words) | Notes |
|---|---|---|---|---|
| 1 | **Seeed XIAO ESP32S3** | 1 (2 if you like a spare) | the plain board, **not "Sense"**; with or without header pins (you can solder wires directly). "Seeed XIAO ESP32S3" | native USB; 21 × 17.5 mm ([CNX](https://www.cnx-software.com/2023/03/22/xiao-esp32s3-tiny-esp32-s3-wifi-4-and-ble-5-0-module-for-iot-ai-robotics/)) |
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
