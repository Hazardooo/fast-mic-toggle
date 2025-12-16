from core import Core
import argparse
import sys

app = Core()


def handle_create_config(default_index: int, temp_index: int):
    try:
        app.new_config(default_index, temp_index)
        print("✅ Config created successfully!")
    except Exception as e:
        print(f"❌ Error creating config: {e}")


def create_config():
    while True:
        raw_data = input("Specify the selected microphone indexes (e.g., '1 2') or 'b' to go back: ").strip()
        if raw_data.lower() == 'b':
            return

        try:
            default, temp = map(int, raw_data.split())

            handle_create_config(default, temp)
            return
        except ValueError:
            print("❌ Error: You need to enter exactly 2 integers (e.g., '1 2').")


def show_menu():
    print("""--- fast-mic-toggle ---
1) Get a list of microphones
2) Create a fast toggle
3) Fast toggle
4) Delete config
0) Exit
""")


def get_mic_list():
    print("Your connected microphones:")
    app.get_mic_list()


def fast_toggle():
    try:
        app.mic_toggle()
        print("✅ Microphone toggled successfully!")
    except Exception as e:
        print(f"❌ Error during toggle: {e}")


def delete_config():
    app.delete_config()
    print("✅ Config deleted.")


def main():
    parser = argparse.ArgumentParser(
        description="fast-mic-toggle: quick microphone switching. "
                    "Use without arguments to start the interactive menu."
    )

    parser.add_argument(
        'option',
        nargs='?',
        type=int,
        help='Select an option (1-4). Option 2 requires two additional arguments.'
    )

    parser.add_argument(
        'args',
        nargs='*',
        type=int,
        help='Additional numeric arguments (e.g., microphone indices for Option 2).'
    )

    if len(sys.argv) > 1:
        args = parser.parse_args()

        if args.option is None:
            print("❌ Specify the option number (1, 2, 3, or 4).")
            parser.print_help()
            return

        option = args.option

        print(f"--- Executing option {option} ---")

        match option:
            case 1:
                get_mic_list()
            case 2:
                if len(args.args) == 2:
                    default, temp = args.args[0], args.args[1]
                    handle_create_config(default, temp)
                else:
                    print(
                        "❌ Option 2 (Create config) requires exactly 2 numeric arguments (Default Index, Temp Index).")
            case 3:
                fast_toggle()
            case 4:
                delete_config()
            case _:
                print("❌ Invalid option. Choose between 1 and 4.")

        return

    while True:
        show_menu()
        user_input = input("Select an option: ").strip()

        if not user_input:
            continue

        try:
            option = int(user_input)
        except ValueError:
            print("❌ Please enter a valid number.")
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
                print("❌ Invalid option. Please choose between 0 and 4.")


if __name__ == "__main__":
    main()
