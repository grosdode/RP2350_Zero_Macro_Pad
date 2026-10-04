# Shortcut sets (layers) for the MacroPad.
# The shortcuts and LED colours live in /macros.json and are edited with the
# web editor (index.html). Do not edit them here.
# Full keycode reference: http://kmkfw.io/docs/keycodes

import json

from kmk.extensions.rgb import hsv_to_rgb
from kmk.keys import KC, Key
from kmk.modules.macros import Delay, Tap

MACROS_FILE = "/macros.json"

# Fallbacks used when macros.json has no colour for a layer.
# (hue 0-255, brightness 0-255)
DEFAULT_COLORS = [
    (85, 180),  # green
    (170, 180),  # blue
    (0, 180),  # red
    (128, 180),  # cyan
    (21, 180),  # orange
    (200, 180),  # purple
    (42, 180),  # yellow
    (225, 180),  # magenta / pink
]
DEFAULT_STRIP_BRIGHTNESS = 20


# --- Sequence parser --------------------------------------------------------
# "T G M"                  -> tap T, then G, then M
# "LCTL+LALT+C"            -> one chord
# "LCTL+A wait20 LCTL+C"   -> chord, 20 ms delay, chord
# A single chord becomes a plain key; anything longer becomes a KC.MACRO.


def _chord(token):
    names = token.split("+")
    key = getattr(KC, names[-1])
    if key is None:
        raise ValueError(names[-1])
    for mod in reversed(names[:-1]):
        mod_key = getattr(KC, mod)
        if mod_key is None:
            raise ValueError(mod)
        key = mod_key(key)
    return key


def _build_key(seq):
    tokens = seq.split()
    if not tokens:
        return KC.NO
    if len(tokens) == 1 and not tokens[0].startswith("wait"):
        return _chord(tokens[0])
    steps = []
    for t in tokens:
        if t.startswith("wait"):
            steps.append(Delay(int(t[4:])))
        else:
            steps.append(Tap(_chord(t)))
    return KC.MACRO(*steps)


def _clamp(value, default):
    try:
        return max(0, min(255, int(value)))
    except Exception:
        return default


def _load_config():
    # Never crash on a bad file: a typo in the editor must not make the pad
    # reboot-loop under the watchdog.
    layers = []
    colors = []
    strip = DEFAULT_STRIP_BRIGHTNESS
    try:
        with open(MACROS_FILE) as f:
            data = json.load(f)
        strip = _clamp(data.get("strip_brightness"), DEFAULT_STRIP_BRIGHTNESS)
        for i, layer in enumerate(data["layers"]):
            keys = []
            for k in layer.get("keys", [])[:9]:
                try:
                    keys.append(_build_key(k.get("seq", "")))
                except Exception:
                    keys.append(KC.NO)  # unknown keycode -> key disabled
            dh, dv = DEFAULT_COLORS[i % len(DEFAULT_COLORS)]
            layers.append(keys)
            colors.append((_clamp(layer.get("hue"), dh), _clamp(layer.get("brightness"), dv)))
    except Exception:
        pass
    if not layers:
        layers = [[]]
        colors = [DEFAULT_COLORS[0]]
    return layers, colors, strip


_RAW_LAYERS, LAYER_COLORS, STRIP_BRIGHTNESS = _load_config()


# Filled in by main.py after the RGB extension is created.
_rgb = None
# Filled in by main.py after the SK6805 strip is created.
_strip = None


def bind_rgb(rgb):
    global _rgb
    _rgb = rgb


def bind_strip(strip):
    global _strip
    _strip = strip
    _apply_strip_color(0)


def _apply_strip_color(layer_index):
    if _strip is None:
        return
    hue = LAYER_COLORS[layer_index % len(LAYER_COLORS)][0]
    layer_keys = LAYERS[layer_index] if layer_index < len(LAYERS) else ()
    lit = hsv_to_rgb(hue, 255, STRIP_BRIGHTNESS)
    off = (0, 0, 0)
    # Strip indices 0..8 map to the 9 physical grid keys. A slot is "undefined"
    # if the layer list is shorter, or if it holds KC.NO / KC.TRNS.
    for i in range(len(_strip)):
        if i < len(layer_keys):
            key = layer_keys[i]
            defined = key is not None and key is not KC.NO and key is not KC.TRNS
        else:
            defined = False
        _strip[i] = lit if defined else off
    _strip.show()


def apply_layer_color(layer_index):
    hue, val = LAYER_COLORS[layer_index % len(LAYER_COLORS)]
    if _rgb is not None:
        # KMK's set_hsv_fill writes the pixel buffer but does NOT push to hardware
        # when animation_mode is STATIC_STANDBY, so keep KMK's state in sync and
        # force a show() ourselves.
        _rgb.hue = hue
        _rgb.sat = 255
        _rgb.val = val
        _rgb.set_hsv_fill(hue, 255, val)
        _rgb.show()
    _apply_strip_color(layer_index)


def _cycle(key, keyboard, *args, **kwargs):
    keyboard.active_layers[0] = (keyboard.active_layers[0] + 1) % len(keyboard.keymap)
    apply_layer_color(keyboard.active_layers[0])
    return keyboard


# Encoder-button key: advances to the next shortcut set and updates the LED.
CYCLE = Key(on_press=_cycle)


def _finalize(grid_keys):
    # Pad to 9 grid slots with KC.NO (unused -> LED off), then encoder push = CYCLE.
    keys = list(grid_keys[:9])
    keys += [KC.NO] * (9 - len(keys))
    keys.append(CYCLE)
    return keys


LAYERS = [_finalize(layer) for layer in _RAW_LAYERS]


# Encoder rotation map: one tuple (CCW, CW, press) per layer.
# The "press" slot is None because the push switch is wired as a regular key
# on GP8 (see main.py), so CYCLE is triggered via the keymap instead.
ENCODER_MAP = [((KC.VOLD, KC.VOLU, None),) for _ in LAYERS]
