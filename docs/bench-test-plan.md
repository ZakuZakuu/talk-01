# Bench test plan (draft, 2026-11-26)

Status: **a plan only. No firmware has been written or flashed; flashing needs the owner's go-ahead (`CLAUDE.md`).** Purpose: find out, before the enclosure is finished, whether the electronics do what talk.01 needs. This is the biggest technical risk of the project.

## What has to be proven (in this order)
1. **The board starts and appears on the computer** (the XIAO ESP32S3 shows up over USB-C; a first program runs).
2. **It is a USB microphone**: the computer lists it as an audio input and records from a **digital microphone module** (INMP441 first), 48 kHz, mono, 16-bit, with the recipe in [`research/claude-review.md`](research/claude-review.md) (the MIT-licensed `usb-mic` project).
3. **It is also a USB keyboard at the same time**: pressing a button holds the configured key (Alt by default) and releasing lets go. **No ready example of audio plus keyboard in one device was found**, so this is the open risk.
4. **The second microphone module** (ICS-43434) in the same setup, to compare.
5. **Recording tests**: the test table in [`research/microphone-quality.md`](research/microphone-quality.md) (silence, 10 cm, 30 cm, key noise, 30 minutes), against the phone.

## What it needs
The parts bought first in [`parts-list.md`](parts-list.md): the XIAO ESP32S3, the two microphone modules, a breadboard, wires, header pins, a coiled USB-C cable (also to measure its plug), a few tact switches, a computer with USB-C.

## What is not known yet
- the exact pin wiring (to be taken from Seeed's pinout when the firmware starts, not from memory);
- whether the audio plus keyboard combination works on Windows without a custom driver (the earlier research says Windows 10 1703 and later has a class driver for USB audio class 2);
- which of the two microphone modules sounds better, and whether the difference matters.

## Who does what
Claude writes the test firmware and the wiring notes (after the owner's go-ahead); the owner solders, flashes and records, and reports (photos, recordings, what the computer shows).
