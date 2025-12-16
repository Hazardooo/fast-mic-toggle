from core import Core

app = Core()


def main():
    print("\n--- fast-mic-toggle ---")

    while True:
        print("""
1) Get a list of microphones
2) Create a fast toggle
3) Fast toggle
4) Delete config
0) Exit""")

        user_input = input("\nSelect an option: ").strip()

        if not user_input:
            continue

        try:
            answer = int(user_input)

            match answer:
                case 1:
                    app.get_mic_list()

                case 2:
                    while True:
                        try:
                            raw_data = input("Specify the selected microphone indexes (e.g., '1 2') or 'b' to back: ")
                            if raw_data.lower() == 'b':
                                break

                            default, temp = map(int, raw_data.split())
                            app.new_config(default, temp)
                            print("Config created successfully!")
                            break
                        except ValueError:
                            print("Error: You need to enter exactly 2 integers (e.g., '1 2').")

                case 3:
                    app.mic_toggle()

                case 4:
                    app.delete_config()
                    print("Config deleted.")

                case 0:
                    print("Exiting...")
                    break

                case _:
                    print("Invalid option. Please choose between 0 and 4.")

        except ValueError:
            print("Error: Please enter a valid number.")
        except Exception as e:
            print(f"An unexpected error has occurred: {e}")


if __name__ == "__main__":
    main()
