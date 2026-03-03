from __future__ import annotations

from contextlib import contextmanager
from typing import Generator

from config import ConfigRepository, MicConfig
from audio_device import AudioDeviceController
from audio_monitor import AudioMonitor
from mic_toggle import MicToggleService
from system import SystemIntegration


class Core:
    __slots__ = ('_config', '_devices', '_monitor', '_toggle_service', '_system')

    def __init__(self):
        self._config: ConfigRepository = ConfigRepository()
        self._devices: AudioDeviceController = AudioDeviceController()
        self._monitor: AudioMonitor = AudioMonitor()
        self._system: SystemIntegration = SystemIntegration()

        self._toggle_service: MicToggleService = MicToggleService(
            config_repo=self._config,
            device_ctrl=self._devices,
            monitor=self._monitor
        )

    @contextmanager
    def sound_session(self, auto_close: bool = True) -> Generator[None, None, None]:
        self._system.open_sound_settings()
        try:
            yield
        finally:
            if auto_close:
                self._system.close_sound_settings()

    # Остальные методы без изменений...
    def get_mic_list(self) -> dict:
        return self._devices.list_recording_devices()

    def set_mic(self, mic_index: int) -> None:
        self._devices.set_default_communication_device(mic_index)

    def mic_toggle(self, timeout: float = 5.0, threshold: float = 0.01) -> bool:
        return self._toggle_service.toggle_until_signal(timeout, threshold)

    def stop_toggle(self) -> None:
        self._toggle_service.stop()

    def get_config(self) -> None:
        self._toggle_service.load_config()

    def new_config(self, default: int, temp: int) -> None:
        self._config.save(default, temp)

    def delete_config(self) -> None:
        self._config.delete()

    def open_sound_settings(self) -> None:
        self._system.open_sound_settings()

    def close_sound_settings(self) -> None:
        self._system.close_sound_settings()
