from __future__ import annotations

import threading
import numpy as np
import sounddevice as sd


class AudioMonitor:
    __slots__ = ('stop_event', '_detected_event', '_stream')

    def __init__(self):
        self.stop_event: threading.Event = threading.Event()
        self._detected_event: threading.Event = threading.Event()
        self._stream: sd.InputStream | None = None

    def wait_for_signal(self, device_index: int, timeout: float, threshold: float) -> bool:
        self.stop_event.clear()
        self._detected_event.clear()
        self._stream = None

        sd_index = self._resolve_device_index(device_index)

        def callback(indata: np.ndarray, frames: int, time_info: dict, status: sd.CallbackFlags) -> None:
            if status:
                print(f"Audio status: {status}")

            volume = np.sqrt(np.mean(indata ** 2))
            if volume > threshold:
                self._detected_event.set()
                self.stop_event.set()

        try:
            self._stream = sd.InputStream(
                device=sd_index,
                channels=1,
                samplerate=44100,
                dtype=np.float32,
                blocksize=512,
                callback=callback
            )

            with self._stream:
                if self.stop_event.wait(timeout=timeout):
                    return self._detected_event.is_set()
                return False

        except Exception as e:
            print(f"❌ Error accessing microphone: {e}")
            return False
        finally:
            self._stream = None

    def stop(self) -> None:
        self.stop_event.set()
        if self._stream:
            try:
                self._stream.stop()
            except Exception:
                pass

    @staticmethod
    def _resolve_device_index(mic_index: int) -> int:
        try:
            devices = sd.query_devices()
            input_devices = [i for i, d in enumerate(devices) if d['max_input_channels'] > 0]
            for i, idx in enumerate(input_devices):
                if idx == mic_index:
                    return i
            print(f"⚠️  Device {mic_index} not found, using default input")
            return 0
        except Exception as e:
            print(f"⚠️  Error querying devices: {e}")
            return 0
