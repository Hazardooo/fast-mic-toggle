from __future__ import annotations

from pyaudiodevice.audio_common import AudioCommon


class AudioDeviceController:
    __slots__ = ('_common',)

    def __init__(self):
        self._common: AudioCommon = AudioCommon()

    def list_recording_devices(self) -> dict:
        devices = self._common.get_audio_device_list()
        recording_devices = {}
        for idx, device in devices.items():
            if device.get('Type') == 'Recording':
                recording_devices[idx] = device
                print(device)
        return recording_devices

    def set_default_communication_device(self, device_index: int) -> None:
        self._common.set_default_communication_device_by_index(device_index)
