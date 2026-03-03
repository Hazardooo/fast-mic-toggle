from __future__ import annotations

import subprocess
import time
from contextlib import contextmanager
from typing import Generator


class SystemIntegration:
    """Отвечает только за интеграцию с системой"""

    @staticmethod
    def open_sound_settings() -> None:
        """Открывает системные настройки звука Windows"""
        try:
            subprocess.Popen(
                ["start", "ms-settings:sound"],
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print("🔊 Opening Windows Sound Settings...")
            time.sleep(0.3)  # Даём время на открытие
        except Exception as e:
            print(f"⚠️  Could not open sound settings: {e}")

    @staticmethod
    def close_sound_settings() -> None:
        """Закрывает системные настройки звука Windows"""
        try:
            # Пробуем разные способы закрытия
            # Способ 1: Закрыть конкретное окно настроек
            subprocess.run(
                ["powershell", "-Command",
                 "(Get-Process | Where-Object {$_.MainWindowTitle -like '*Звук*' -or $_.MainWindowTitle -like '*Sound*'}).CloseMainWindow()"],
                capture_output=True,
                timeout=2
            )

            # Способ 2: Принудительно убить процесс SystemSettings (если висит)
            subprocess.Popen(
                ["taskkill", "/F", "/IM", "SystemSettings.exe"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            print("🔇 Closing Windows Sound Settings...")
        except Exception as e:
            print(f"⚠️  Could not close sound settings: {e}")

    @classmethod
    @contextmanager
    def sound_settings_session(cls, auto_close: bool = True) -> Generator[None, None, None]:
        """
        Контекстный менеджер для автоматического открытия/закрытия настроек звука.
        
        Usage:
            with SystemIntegration.sound_settings_session():
                # работа со звуком
                pass
        """
        cls.open_sound_settings()
        try:
            yield
        finally:
            if auto_close:
                cls.close_sound_settings()