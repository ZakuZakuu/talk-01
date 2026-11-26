// SPDX-License-Identifier: MIT
// talk.01 bench firmware: the USB layout shared by usb_descriptors.c and main.c.
// UNBUILT AND UNTESTED: see ../../README.md.
#pragma once

// With CONFIG_USB_DEVICE_UAC_AS_PART=y the component does not define the interface numbers; we do.
// One microphone (audio control + one streaming interface) and one HID keyboard.
enum {
    ITF_NUM_AUDIO_CONTROL = 0,
    ITF_NUM_AUDIO_STREAMING_MIC,     // 1: the number handed to uac_device_init() as mic_itf_num
    ITF_NUM_HID,                     // 2: the keyboard
    ITF_NUM_TOTAL                    // 3
};

// A placeholder USB identity for bench tests ONLY. Espressif's own VID with a test PID is not a product identity;
// a proper VID/PID has to be settled before anything is given to anyone else.
#define TALK01_USB_VID   0x303A
#define TALK01_USB_PID   0x4011
