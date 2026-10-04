# MacroPad Editor

## TLDR

- Open `index.html` in **Chrome or Edge**.
- Click **Connect CIRCUITPY** and pick the pad's drive.
- Click a key, press your shortcut (recording starts automatically), and add delays with the Delay buttons.
- Set LED colour and brightness per layer.
- Click **Save to device**. The pad reloads by itself.
- Other browsers: use **Download** and copy `macros.json` to the drive manually.

## Files

| File                                       | Where           | Purpose                                           |
| ------------------------------------------ | --------------- | ------------------------------------------------- |
| `index.html`                               | your PC         | The editor (no server or install needed)          |
| `macros.json`                              | CIRCUITPY drive | Shortcuts and LED settings, written by the editor |
| `layers.py`                                | CIRCUITPY drive | Reads `macros.json` and builds the layers         |
| `main.py`, `watchdog_module.py`, `boot.py` | CIRCUITPY drive | Unchanged firmware                                |

## Using the editor

1. **Connect:** click *Connect CIRCUITPY* and select the drive. An existing `macros.json` is loaded.
2. **Pick a key:** click a tile in the 3×3 grid. Recording starts right away.
3. **Record:** press the shortcut on your keyboard. Each press is appended to the sequence.
4. **Modifiers (Win, Ctrl, Alt, Shift):** the OS often grabs Win+… combos. Click the modifier buttons, then press the last key. For Win+Alt+P, click *Win*, click *Alt*, press *P*. *Capture all keys* (fullscreen) is a best-effort alternative.
5. **Delays:** click a preset (20 to 500 ms) or type a custom value and click *Add delay*.
6. **Fix mistakes:** *Undo last* removes the last step and *Clear* empties the sequence. You can also edit the sequence field by hand.
7. **LED:** each layer has its own colour and brightness. The key backlight brightness is shared by all layers.
8. **Save:** click *Save to device*.

## Sequence syntax

| Sequence                            | Meaning                                       |
| ----------------------------------- | --------------------------------------------- |
| `T G M`                             | Tap T, then G, then M                         |
| `LCTL+LALT+C`                       | One chord (Ctrl+Alt+C)                        |
| `LCTL+A wait100 LCTL+C wait100 ESC` | Chord, 100 ms pause, chord, 100 ms pause, Esc |

- A single chord is a normal key press. Anything longer is a macro.
- Names are KMK keycodes (`LCTL`, `LGUI`, `SCLN`, `N1`, ...). They refer to US key positions, so `Ö` on a German layout is `SCLN`.

## Browser support

| Feature                   | Chrome / Edge (desktop) | Firefox / Safari / phones           |
| ------------------------- | ----------------------- | ----------------------------------- |
| Editing and recording     | Yes                     | Recording needs a physical keyboard |
| Connect and save to drive | Yes                     | No, use Download and Upload         |

## Troubleshooting

- **A key does nothing:** the keycode name is probably misspelled. The pad disables that key silently, so check the sequence for red chips.
- **Changes don't appear:** wait a second after saving. If nothing happens, press reset or replug the pad.
- **The pad boots with empty layers:** `macros.json` is missing or broken. Re-save it from the editor.
- **A shortcut won't record:** use the modifier buttons or type the sequence by hand.
- **The page looks outdated:** hard reload with Ctrl+Shift+R.