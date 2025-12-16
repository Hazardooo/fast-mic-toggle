from core import Core

app = Core()


def show_menu():
    print("""
--- fast-mic-toggle ---
1) Get a list of microphones
2) Create a fast toggle
3) Fast toggle
4) Delete config
0) Exit
""")


def get_mic_list():
    print("Your connected microphones:")
    app.get_mic_list()


def create_config():
    while True:
        raw_data = input("Specify the selected microphone indexes (e.g., '1 2') or 'b' to go back: ").strip()
        if raw_data.lower() == 'b':
            return

        try:
            default, temp = map(int, raw_data.split())
            app.new_config(default, temp)
            print("✅ Config created successfully!")
            return
        except ValueError:
            print("❌ Error: You need to enter exactly 2 integers (e.g., '1 2').")


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
