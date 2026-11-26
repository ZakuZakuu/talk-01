# Third-party material in firmware/

| File | Origin | Licence |
|---|---|---|
| `stage2-composite/main/tusb/uac_config.h`, `tusb_config_uac.h` | espressif/esp-iot-solution, `components/usb/usb_device_uac/tusb_uac/` (usb_device_uac 1.3.2), vendored unchanged | **Apache-2.0** (text in [`../LICENSES/Apache-2.0.txt`](../LICENSES/Apache-2.0.txt)) |
| `stage2-composite/main/tusb/uac_descriptors.h` | the same directory; originally Copyright (c) 2020 Jerzy Kasenbreg; vendored unchanged | **MIT** (header kept in the file) |
| `stage2-composite/main/tusb/tusb_config.h`, `usb_descriptors.c` | `components/usb/usb_device_uac/tusb/`; originally Copyright (c) 2019 Ha Thach (tinyusb.org) and 2020 Jerzy Kasenbreg; **modified** for talk.01 (the HID keyboard added; the changes are noted at the top of each file) | **MIT** (header kept in the file) |
| `stage2-composite/main/main.c` (the I2S reading, the 90 Hz high-pass and the gain shift) | adapted from [mmajjedi/usb-mic](https://github.com/mmajjedi/usb-mic) `main/usb_mic.c`, Copyright (c) 2026 Mahdi | **MIT** |
| everything else in `firmware/` | written for this project | MIT |

The vendored files were obtained by fetching the upstream files from GitHub; they are **not byte-verified** against a clone. Before a release they should be re-fetched from a tagged upstream version and compared.
