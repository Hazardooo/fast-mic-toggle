from time import sleep

from pyaudiodevice.audio_common import AudioCommon
import winreg as reg

root_key = reg.HKEY_CURRENT_USER
sub_key_path = r"Software\fast-mic-toggle"


class Core:
    def __init__(self):
        self._common = AudioCommon()
        self._default = {"name": "default_microphone", "value": None}
        self._temp = {"name": "temporary_microphone", "value": None}

    def get_mic_list(self):
        devices = self._common.get_audio_device_list()
        for device in devices:
            if devices[device]['Type'] == 'Recording':
                print(devices[device])

    def set_mic(self, mic_index):
        self._common.set_default_communication_device_by_index(mic_index)

    def mic_toggle(self):
        self.get_config()
        self.set_mic(self._temp["value"])
        sleep(5)
        self.set_mic(self._default["value"])

    def get_config(self):
        with reg.OpenKey(root_key, sub_key_path, 0, reg.KEY_READ) as key:
            self._default["value"], _ = reg.QueryValueEx(key, self._default["name"])
            self._temp["value"], _ = reg.QueryValueEx(key, self._temp["name"])

    def new_config(self, default, temp):
        with reg.CreateKeyEx(root_key, sub_key_path, 0, reg.KEY_WRITE) as key:
            print(f"Registry key '{sub_key_path}' created or opened successfully.")
            reg.SetValueEx(key, self._default["name"], 0, reg.REG_SZ, str(default))
            reg.SetValueEx(key, self._temp["name"], 0, reg.REG_SZ, str(temp))

    def delete_config(self):
        reg.DeleteKey(root_key, sub_key_path)
