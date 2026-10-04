# RP2350 Zero Macro Pad

This project is the software for a small, low profile macro keypad based on a RP2350. It uses:
* [circuit python](https://circuitpython.org)
    * The board file can be found [here](https://circuitpython.org/board/waveshare_rp2350_zero/)
    * The Neo Pixel lib can be found [here](https://circuitpython.org/libraries)
* the [kmk](https://github.com/KMKfw/kmk_firmware/tree/main?tab=License-1-ov-file) library (firmware for computer keyboards)
* 3D printed hardware publish on [printables](https://www.printables.com/model/1866058-low-profile-macro-pad)

## Structure
This repo contains:
* main.py --> main circuit python file
* layers.py --> handling the different macro layers (sets of macros)
* README.md --> this read me files
* watchdog_module.py --> watchdog to prevent stalling
* WebApp --> folder with a wep app to configure the keys
    * KeySetting.html --> wep app to configure the keys
    * README_Web.md --> read me file for the web app

All these files are small enough to copy them on the RP2350.

## Getting started
* Copy the [circuit python software](https://circuitpython.org/board/waveshare_rp2350_zero/) to your RP2350 Zero
    * [Installing CircuitPython](https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython)
* Download the [kmk](https://github.com/KMKfw/kmk_firmware/tree/main/kmk) files and copy the `kmk` folder to the RP2350 Zero
* Download the [adafruit-circuitpython-bundle](https://circuitpython.org/libraries) that fits your *.uf2 file version and copy the "neopixel.mpy" file to the `lib` folder on the RP2350 Zero
* Copy the files from this repo (at least: `main.py`, `layers.py`, `watchdog_module.py`) to the RP2350 Zero
* Configure the keys with the web app
* Build the hardware published on [printables](https://www.printables.com/model/1866058-low-profile-macro-pad)