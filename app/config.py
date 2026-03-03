from __future__ import annotations

from dataclasses import dataclass
import winreg as reg


@dataclass(frozen=True, slots=True)
class MicConfig:
    name: str
    value: str | None = None


class ConfigRepository:
    __slots__ = ('_root_key', '_sub_key_path')

    def __init__(self, root_key: int = reg.HKEY_CURRENT_USER,
                 sub_key_path: str = r"Software\fast-mic-toggle"):
        self._root_key: int = root_key
        self._sub_key_path: str = sub_key_path

    def load(self) -> tuple[MicConfig, MicConfig]:
        with reg.OpenKey(self._root_key, self._sub_key_path, 0, reg.KEY_READ) as key:
            default_val, _ = reg.QueryValueEx(key, "default_microphone")
            temp_val, _ = reg.QueryValueEx(key, "temporary_microphone")

            return (
                MicConfig("default_microphone", str(default_val)),
                MicConfig("temporary_microphone", str(temp_val))
            )

    def save(self, default: int, temp: int) -> None:
        with reg.CreateKeyEx(self._root_key, self._sub_key_path, 0, reg.KEY_WRITE) as key:
            reg.SetValueEx(key, "default_microphone", 0, reg.REG_SZ, str(default))
            reg.SetValueEx(key, "temporary_microphone", 0, reg.REG_SZ, str(temp))
            print("✅ Config saved")

    def delete(self) -> None:
        try:
            reg.DeleteKey(self._root_key, self._sub_key_path)
        except FileNotFoundError:
            pass
