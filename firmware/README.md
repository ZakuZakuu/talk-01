# firmware/: bench-test firmware for talk.01

Licence: MIT for the code written for this project; the vendored files under `stage2-composite/main/tusb/` keep their own licences (MIT or Apache-2.0), see [`NOTICE.md`](NOTICE.md) and [`../LICENSING.md`](../LICENSING.md).

> **Status: written 2026-11-26, before the hardware arrived, WITHOUT a compiler or a board. It has not been built, flashed or run.** Expect to fix small things the first time. The owner builds, flashes and tests; Claude fixes what the build or the test shows. Nothing here has been heard or measured.

## The plan, in two stages

| Stage | What | Where |
|---|---|---|
| **1. A microphone** | the open-source `usb-mic` project **unchanged** (MIT, [mmajjedi/usb-mic](https://github.com/mmajjedi/usb-mic)): the board becomes a USB microphone. This proves the board, the microphone module and the wiring | not copied here: clone it |
| **2. A microphone and a keyboard** | one USB device that is both: the BOOT button is the push-to-talk key (Left Alt held while pressed). **No ready example of this was found**; it is the open risk | [`stage2-composite/`](stage2-composite/) |

Do **stage 1 first**. If stage 1 works, stage 2 is a small step; if stage 2 does not build or behave, stage 1 still tells you the hardware is fine.

## Why stage 2 needs its own USB descriptors

The `usb_device_uac` component builds a USB device with **one audio function and nothing else**, and has no switch for adding a keyboard. It has one escape hatch, `CONFIG_USB_DEVICE_UAC_AS_PART`: with it on, the project supplies `tusb_config.h` and `usb_descriptors.c` itself. Stage 2 does that: it copies the component's descriptor files (`stage2-composite/main/tusb/`), adds a HID keyboard interface, and the application sends key reports from the button task. Details: [`../docs/research/uac-hid-composite.md`](../docs/research/uac-hid-composite.md).

## What you need
- the ESP32-S3 Super Mini and the ICS-43434 board (the owner's orders), a breadboard and Dupont wires, a USB cable that carries data;
- **ESP-IDF 5.5** on your computer (the version the upstream project's lock file names is 5.5.5): follow Espressif's own guide for the ESP32-S3: <https://docs.espressif.com/projects/esp-idf/en/v5.5.5/esp32s3/get-started/index.html>. The installer and its steps differ by system; I cannot check them from here.

## Wiring (a first guess; check your board's pin labels)

| Microphone board pin | Super Mini |
|---|---|
| VDD | 3V3 (the upstream project adds 100 ohm in series and 100 uF from VDD to GND; optional but cheap) |
| GND | GND |
| SCK | GPIO4 |
| WS | GPIO5 |
| SD | GPIO6 |
| L/R | GND (or the board's "PS" pad bridged as its seller says: left channel is wanted) |

These GPIOs are the upstream defaults. **If your board does not bring GPIO4, 5, 6 out, use three others** (any free GPIO works on the S3) and change `PIN_SCK`, `PIN_WS`, `PIN_SD` at the top of `main.c`. The pad order differs between makers: read it from the board's own silkscreen. Keep the I2S wires short (the upstream advice: under 15 cm). **Do not solder the microphone board's pins before you know which face has the sound hole** (see [`../docs/parts-list.md`](../docs/parts-list.md)).

## Build and flash (the usual ESP-IDF steps)

```bash
cd firmware/stage2-composite
idf.py set-target esp32s3
idf.py build
idf.py -p <port> flash monitor
```

The port is a serial port name (on Windows something like `COM5`). **Use the board's native USB port.** If the computer does not see the board for flashing, the usual way on S3 boards is: hold BOOT, tap RESET, release BOOT (check your board's silkscreen). After flashing, replug the board.

## What to look for and report

1. **Does it build?** If not: paste the first error to Claude (the whole message).
2. **Does the computer list a new audio input** ("talk.01 microphone" or similar) and a new keyboard?
3. **Record 30 seconds of silence and 30 seconds of speaking** in any recorder; tell me what you hear (hiss, hum, clicks, too quiet, distorted). The serial monitor prints `level: rms ... dBFS` every 2 seconds: write down the value in silence and while talking.
4. **Press and hold the BOOT button**: the monitor should print `key DOWN sent`; in WeChat Input (hold Alt for voice) the voice input should start; release: `key UP sent`, it stops.
5. If it is **too quiet or distorted**, change `GAIN_SHIFT` in `main.c` (12 is louder, 14 is quieter), rebuild, flash.
6. **Plug it into a different USB port, and unplug and replug while recording**; tell me if the recording stops or the audio breaks.

## Known weak points (from reading, not from running)
- Calling `tud_hid_keyboard_report` from another task than TinyUSB's own is common in examples but TinyUSB is not strictly thread-safe; if reports are lost, the fix is to queue them to TinyUSB's task.
- The component's `tud_mount_cb` and friends are compiled out in AS_PART mode, so `main.c` supplies simple ones that only log; the component's own "active" flags are then not cleared on unmount. If audio does not restart after a replug, this is the first suspect.
- The USB VID/PID in `talk01_usb.h` is a placeholder for bench tests only.
- The HID endpoint polling interval (10 ms) and the descriptor lengths were written by hand from the TinyUSB macros: a wrong total length shows up as the host not enumerating the device.
