from __future__ import annotations

from time import sleep

from config import ConfigRepository, MicConfig
from audio_device import AudioDeviceController
from audio_monitor import AudioMonitor


class MicToggleService:
    __slots__ = ('_config_repo', '_device_ctrl', '_monitor', '_default', '_temp')

    def __init__(
            self,
            config_repo: ConfigRepository,
            device_ctrl: AudioDeviceController,
            monitor: AudioMonitor
    ):
        self._config_repo: ConfigRepository = config_repo
        self._device_ctrl: AudioDeviceController = device_ctrl
        self._monitor: AudioMonitor = monitor
        self._default: MicConfig | None = None
        self._temp: MicConfig | None = None

    def load_config(self) -> None:
        self._default, self._temp = self._config_repo.load()

    def toggle_until_signal(self, timeout: float = 5.0, threshold: float = 0.01) -> bool:
        if not self._default or not self._temp:
            self.load_config()
        default_idx = int(self._default.value) if self._default.value else 0
        temp_idx = int(self._temp.value) if self._temp.value else 0
        cycle = 0
        while not self._monitor.stop_event.is_set():
            cycle += 1
            print(f"\n--- Cycle {cycle} ---")
            print(f"➡️  TEMP (index: {temp_idx})...")
            self._device_ctrl.set_default_communication_device(temp_idx)
            sleep(0.1)
            print(f"➡️  DEFAULT (index: {default_idx})...")
            self._device_ctrl.set_default_communication_device(default_idx)
            sleep(0.1)
            print(f"🎤 Listening on DEFAULT mic...")
            detected = self._monitor.wait_for_signal(default_idx, timeout, threshold)
            if detected:
                print(f"✅ Audio detected after {cycle} cycle(s)!")
                return True
            else:
                print(f"⏱️  No signal, retrying...")

        return False

    def stop(self) -> None:
        self._monitor.stop()
