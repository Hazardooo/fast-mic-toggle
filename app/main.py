from core import Core
import argparse
import sys
from time import sleep

app = Core()


def handle_create_config(default_index: int, temp_index: int) -> None:
    try:
        app.new_config(default_index, temp_index)
        print("✅ Config created successfully!")
    except Exception as e:
        print(f"❌ Error creating config: {e}")


def create_config() -> None:
    while True:
        raw_data = input("Specify mic indexes (e.g., '1 2') or 'b' to go back: ").strip()
        if raw_data.lower() == 'b':
            return

        try:
            default, temp = map(int, raw_data.split())
            handle_create_config(default, temp)
            return
        except ValueError:
            print("❌ Error: Enter exactly 2 integers (e.g., '1 2').")


def show_menu() -> None:
    print("""--- fast-mic-toggle ---
1) List microphones
2) Create toggle config
3) Fast toggle (opens Sound Settings)
4) Delete config
0) Exit
""")


def get_mic_list() -> None:
    print("Connected microphones:")
    app.get_mic_list()


def fast_toggle() -> None:
    try:
        with app.sound_session(auto_close=True):
            detected = app.mic_toggle()
            status = "with audio detection" if detected else "stopped"
            print(f"✅ Toggled successfully ({status})!")
    except Exception as e:
        print(f"❌ Error during toggle: {e}")


def delete_config() -> None:
    app.delete_config()
    print("✅ Config deleted.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="fast-mic-toggle: quick microphone switching."
    )
    parser.add_argument('option', nargs='?', type=int, help='Option 1-4')
    parser.add_argument('args', nargs='*', type=int, help='Additional args')

    if len(sys.argv) > 1:
        args = parser.parse_args()

        if args.option is None:
            parser.print_help()
            return

        match args.option:
            case 1:
                get_mic_list()
            case 2:
                if len(args.args) == 2:
                    handle_create_config(args.args[0], args.args[1])
                else:
                    print("❌ Option 2 requires 2 arguments: default_index temp_index")
            case 3:
                app.open_sound_settings()
                sleep(0.5)
                try:
                    detected = app.mic_toggle()
                    print(f"✅ Done! Audio detected: {detected}")
                except Exception as e:
                    print(f"❌ Error: {e}")
            case 4:
                delete_config()
            case _:
                print("❌ Invalid option. Use 1-4.")
        return

    while True:
        show_menu()
        user_input = input("Select option: ").strip()

        if not user_input:
            continue

        try:
            option = int(user_input)
        except ValueError:
            print("❌ Enter a valid number.")
            continue

        match option:
            case 1:
                get_mic_list()
            case 2:
                create_config()
            case 3:
                fast_toggle()
            case 4:
                delete_config()
            case 0:
                print("Exiting... 👋")
                break
            case _:
                print("❌ Invalid option. Use 0-4.")


if __name__ == "__main__":
    main()
