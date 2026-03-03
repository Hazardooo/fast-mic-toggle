from __future__ import annotations
from enum import Enum


class MenuOption(Enum):
    LIST = "1"
    CONFIG = "2"
    TOGGLE = "3"
    DELETE = "4"
    EXIT = "0"


class InteractiveMenu:
    @staticmethod
    def show() -> None:
        print("""--- fast-mic-toggle ---
1) List microphones
2) Create toggle config
3) Fast toggle
4) Delete config
0) Exit
""")

    @staticmethod
    def get_input() -> MenuOption | None:
        user_input = input("Select option: ").strip()
        try:
            return MenuOption(user_input)
        except ValueError:
            print("❌ Invalid option")
            return None

    @staticmethod
    def get_mic_indices() -> tuple[int, ...] | None:
        raw = input("Specify mic indexes (e.g., '1 2') or 'b' to go back: ").strip()
        if raw.lower() == 'b':
            return None
        try:
            return tuple(map(int, raw.split()))
        except ValueError:
            print("❌ Enter exactly 2 integers")
            return None
