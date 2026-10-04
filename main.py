# MacroPad firmware entry point (CircuitPython + KMK on RP2350).
# Copy this file plus layers.py and the kmk/ folder onto the CIRCUITPY drive.

import board
import neopixel
from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.rgb import RGB
from kmk.kmk_keyboard import KMKKeyboard
from kmk.modules.encoder import EncoderHandler
from kmk.modules.layers import Layers
from kmk.modules.macros import Macros
from kmk.scanners.keypad import KeysScanner
from watchdog_module import Watchdog

# Instantiate Macros() and MediaKeys() BEFORE importing layers: doing so
# registers KC.MACRO / KC.MPLY / KC.VOLU / etc, which layers.py references
# at import time.
_layers_module = Layers()
_macros_module = Macros()
_media_keys_ext = MediaKeys()
_watchdog_module = Watchdog(timeout=5)

import layers as user_layers  # noqa: E402  (must come after Macros() init)

# --- Pin assignments -------------------------------------------------------
# 9 keys + encoder push switch, wired switch -> GPIO -> GND (active low).
KEY_PINS = [
    board.GP27,
    board.GP28,
    board.GP29,
    board.GP26,
    board.GP15,
    board.GP14,
    board.GP13,
    board.GP12,
    board.GP11,
    board.GP8,  # encoder push switch (index 9 matches CYCLE in layers.py)
]

ENCODER_A_PIN = board.GP10
ENCODER_B_PIN = board.GP9

# Change to your board's onboard RGB pin. Common values:
#   Adafruit boards:            board.NEOPIXEL
#   Waveshare RP2350-Zero:      board.NEOPIXEL  (alias for GP16)
#   Many generic RP2350 boards: board.GP23
RGB_PIN = board.NEOPIXEL

# External per-key strip: 9x SK6805-EC2018 daisy-chained on GP6.
STRIP_PIN = board.GP6
STRIP_NUM_PIXELS = 9


# --- Keyboard --------------------------------------------------------------
keyboard = KMKKeyboard()
keyboard.modules.append(_layers_module)
keyboard.modules.append(_macros_module)
keyboard.modules.append(_watchdog_module)

keyboard.matrix = KeysScanner(
    pins=KEY_PINS,
    value_when_pressed=False,  # pressed = pin pulled to GND
    pull=True,  # enable internal pull-up
)

encoder = EncoderHandler()
encoder.pins = ((ENCODER_A_PIN, ENCODER_B_PIN, None),)
keyboard.modules.append(encoder)

rgb = RGB(
    pixel_pin=RGB_PIN,
    num_pixels=1,
    # Waveshare RP2350-Zero onboard LED is wired RGB, not GRB.
    rgb_order=(0, 1, 2),
    hue_default=user_layers.LAYER_COLORS[0][0],
    val_default=user_layers.LAYER_COLORS[0][1],
)
keyboard.extensions.append(rgb)
keyboard.extensions.append(_media_keys_ext)

strip = neopixel.NeoPixel(
    STRIP_PIN,
    STRIP_NUM_PIXELS,
    auto_write=False,
)


# --- Wire up user layers ---------------------------------------------------
user_layers.bind_rgb(rgb)
user_layers.bind_strip(strip)
keyboard.keymap = user_layers.LAYERS
encoder.map = user_layers.ENCODER_MAP


if __name__ == "__main__":
    keyboard.go()
