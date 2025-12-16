# Fast Mic Toggle

### A tool for automatically restoring malfunctioning microphones in Windows by quickly toggling audio devices.

---

## 💡 Problem Description

Some sound cards or USB microphones in Windows have a specific issue: after system startup or waking from sleep, the device appears as active but **does not transmit sound** (becomes "silent") until you manually switch it to another device and back.

**Fast Mic Toggle** solves this problem by performing the necessary switch automatically using a simple script and saving the settings in the Windows registry.

---

## ✨ How It Works

The application performs a quick, automated operation:

* Reads the saved microphone indexes (Primary and Temporary).
* Temporarily (≈1 second) sets the Temporary microphone as the default communication device.
* Restores your Primary microphone as the default communication device.

This quick toggle triggers an internal "reset" of the audio driver, after which your Primary microphone works properly in applications like Discord or Zoom.

---

## 🚀 Installation

### 1️⃣ As a Standalone Application (.exe)

If you downloaded the application as a ready-made `.exe` file:

1. Download and extract the archive.
2. Run `fast-mic-toggle.exe`.

**Important:** The executable (`fast-mic-toggle.exe`) will not work without the `_internal` folder, which contains all required DLL dependencies.

### 2️⃣ As a Python Package (For Developers)

```bash
pip install -r requirements.txt
cd ./app/
python main.py
```

---

## ⚙️ Usage (Setup)

The application runs in a console menu mode:

```
--- fast-mic-toggle ---
1) Get a list of microphones
2) Create a fast toggle
3) Fast toggle
4) Delete config
0) Exit
```

### Step 1: Get the list of microphones (Option 1)

Run the application and select option `1` to see all available recording devices and their system indexes:

```
Select an option: 1
Your connected microphones:
{'Index': 5, ..., 'Name': 'Line (Xonar U7 MKII)', ...}
{'Index': 7, ..., 'Name': 'Microphone (Xonar U7 MKII)', ...}
```

* Identify your **Primary microphone**: the one you want to fix (e.g., 7).
* Identify a **Temporary microphone**: any other recording index used for toggling (e.g., 5).

### Step 2: Create a configuration (Option 2)

Select option `2` to save the indexes. The configuration will be stored in the Windows registry at:
`HKEY_CURRENT_USER\Software\fast-mic-toggle`.

Enter two indexes separated by a space:

* **Primary microphone** (the one to fix)
* **Temporary microphone** (used for toggling)

Example:

```
Select an option: 2
Specify the selected microphone indexes (e.g., '1 2') or 'b' to go back: 7 5
✅ Config created successfully!
```

### Step 3: Fast toggle (Option 3)

Once configured, you can perform the toggle at any time by selecting option `3`:

```
Select an option: 3
✅ Microphone toggled successfully!
```

Your **Primary microphone** (Index 7) should now be fully functional.

**Important:** Before toggling, make sure all applications that might be using the microphone (Discord, Zoom, games) are closed. Active communication apps may not handle device switching correctly.

---

## Delete configuration (Option 4)

If you no longer need the tool, you can remove the saved indexes from the registry:

```
Select an option: 4
✅ Config deleted.
```

---

## 💻 Windows Autostart Integration

To fully automate the fix, you can set up `fast-mic-toggle.exe` to run at system startup:

1. Make sure you have configured the settings (Step 2).
2. Create a shortcut for `fast-mic-toggle.exe`.
3. Open the shortcut properties.
4. In the "Target" field, after the full path to your `.exe`, add the number `3` (so the application runs only the "Fast toggle" option and exits). Example:
   `"C:\Path\To\fast-mic-toggle.exe" 3`
5. Place this shortcut in the Windows Startup folder (`shell:startup`).

---

## 🗑️ Uninstallation

Simply delete the `fast-mic-toggle` folder. Optionally, use menu option `4` to clear the registry.

