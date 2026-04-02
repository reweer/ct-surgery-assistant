import sounddevice as sd
import json
import os

def setup_audio():
    print("--- CT Surgery Assistant: Audio Setup ---")
    devices = sd.query_devices()
    
    input_devices = []
    print("Available Input Devices:")
    for i, dev in enumerate(devices):
        if dev['max_input_channels'] > 0:
            default_mark = "*" if i == sd.default.device[0] else " "
            print(f"{default_mark} [{i}] {dev['name']}")
            input_devices.append(i)

    if not input_devices:
        print("❌ No input devices found!")
        return

    try:
        choice = input("Select device index to use (or press Enter for default): ").strip()
        
        if choice == "":
            selected_index = sd.default.device[0]
        else:
            selected_index = int(choice)
            if selected_index not in input_devices:
                print(f"❌ Invalid index. Please choose from {input_devices}")
                return

        config = {"device_index": selected_index}
        
        with open("config.json", "w") as f:
            json.dump(config, f, indent=4)
            
        print(f"✅ Configuration saved! Using: {devices[selected_index]['name']}")
        print("You can now run 'python3 src/main.py'")

    except ValueError:
        print("❌ Please enter a valid number.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    setup_audio()
