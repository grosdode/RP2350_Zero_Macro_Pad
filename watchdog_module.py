# Hardware watchdog for KMK on RP2350.
# If the main loop stalls for `timeout` seconds, the MCU resets.

from kmk.modules import Module
from microcontroller import watchdog
from watchdog import WatchDogMode


class Watchdog(Module):
    def __init__(self, timeout=5):
        self.timeout = timeout
        self._wdt = watchdog

    def during_bootup(self, keyboard):
        self._wdt.timeout = self.timeout
        self._wdt.mode = WatchDogMode.RESET
        self._wdt.feed()

    def before_matrix_scan(self, keyboard):
        self._wdt.feed()

    def after_matrix_scan(self, keyboard):
        return

    def before_hid_send(self, keyboard):
        return

    def after_hid_send(self, keyboard):
        self._wdt.feed()

    def on_powersave_enable(self, keyboard):
        # Give up watchdog protection while we intentionally sleep.
        try:
            self._wdt.deinit()
        except Exception:
            pass

    def on_powersave_disable(self, keyboard):
        self._wdt.timeout = self.timeout
        self._wdt.mode = WatchDogMode.RESET
        self._wdt.feed()

    def deinit(self, keyboard):
        try:
            self._wdt.deinit()
        except Exception:
            pass
