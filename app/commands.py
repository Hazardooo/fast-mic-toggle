from __future__ import annotations
from typing import Protocol


class AudioService(Protocol):
    def get_mic_list(self) -> dict: ...

    def set_mic(self, mic_index: int) -> None: ...

    def mic_toggle(self, timeout: float = 5.0, threshold: float = 0.01) -> bool: ...

    def stop_toggle(self) -> None: ...

    def new_config(self, default: int, temp: int) -> None: ...

    def delete_config(self) -> None: ...

    def open_sound_settings(self) -> None: ...

    def close_sound_settings(self) -> None: ...

    def sound_session(self, auto_close: bool = True): ...


class CommandExecutor:
    def __init__(self, service: AudioService):
        self._service = service

    def list_mics(self) -> None:
        print("Connected microphones:")
        self._service.get_mic_list()

    def create_config(self, indices: tuple[int, ...]) -> None:
        if len(indices) != 2:
            print("❌ Requires 2 arguments: default_index temp_index")
            return
        self._service.new_config(indices[0], indices[1])
        print("✅ Config created!")

    def toggle(self) -> None:
        try:
            with self._service.sound_session(auto_close=True):
                detected = self._service.mic_toggle()
                status = "with audio detection" if detected else "stopped"
                print(f"✅ Toggled successfully ({status})!")
        except Exception as e:
            print(f"❌ Error: {e}")

    def delete_config(self) -> None:
        self._service.delete_config()
        print("✅ Config deleted.")
