# One USB device that is a microphone and a keyboard (research, 2026-11-26)

Status: **read from the maker's sources; nothing built or run.** It answers the open risk named in [`claude-review.md`](claude-review.md): no ready example of USB audio plus keyboard was found. The firmware that follows from it is [`../../firmware/`](../../firmware/README.md).

## What was read (all on GitHub, espressif/esp-iot-solution, `components/usb/usb_device_uac`, version 1.3.2)
- **The component builds a USB device with one audio function and nothing else.** `uac_device_init()` starts TinyUSB itself (`tusb_init()`, then a TinyUSB task), unless `skip_tinyusb_init` is set. Its configuration descriptor is a fixed array: a configuration header plus one audio descriptor. **No option, callback or Kconfig switch adds another interface.** The example (`examples/usb/device/usb_uac`) uses only the four audio callbacks.
- **One escape hatch: `CONFIG_USB_DEVICE_UAC_AS_PART`** ("Using customer tinyusb configs and descriptors"). With it on, the project must provide `tusb_config.h` and `usb_descriptors.c`; the component then takes the interface numbers from `uac_device_config_t` (`spk_itf_num`, `mic_itf_num`) and no longer provides `tud_mount_cb`, `tud_umount_cb`, `tud_suspend_cb`, `tud_resume_cb`.
- The audio descriptor macros (`TUD_AUDIO_DESCRIPTOR`, `TUD_AUDIO_MIC_DESCRIPTOR`) and the audio TinyUSB configuration live in files the component adds to the TinyUSB library's include path only when AS_PART is **off**; so with AS_PART on, the project has to carry its own copies of those files.
- The microphone data path is a pull: the component calls the application's `input_cb` every `MIC_INTERVAL_MS` and expects it to fill the buffer.
- TinyUSB's HID keyboard needs `CFG_TUD_HID`, a report descriptor (`TUD_HID_REPORT_DESC_KEYBOARD`), an interface descriptor (`TUD_HID_DESCRIPTOR`) and three callbacks; neither `CFG_TUD_HID` nor `CFG_TUD_CDC` is set in the component's configuration.
- Licences: the component's C files and the two audio config headers are Apache-2.0; the descriptor files and `tusb_config.h` carry MIT headers from TinyUSB authors.

## What the firmware does about it
`firmware/stage2-composite` turns AS_PART on, vendors the component's descriptor and config files, adds the HID interface (interface 2, endpoint 0x83) after the audio interfaces (0 and 1, endpoint 0x82), and sends key reports from a button task. The owner builds and tests it.

## Risks that remain (none tested)
1. The hand-written total length and the interface and endpoint numbers: a mistake shows as the host failing to enumerate the device.
2. The component's own state, which it clears in the callbacks that are now ours: audio after an unplug and replug.
3. TinyUSB calls from a second task.
4. Whether Windows enumerates a device that is both an audio-class-2 function and a HID function without a driver (the earlier research says Windows 10 1703 and later has an in-box driver for audio class 2; not tested here).
5. The upstream `usb-mic` project lists no tested board, and names Windows, macOS, Linux, Android and USB-C iPhones as detecting its device "on their own"; no test notes were found.
