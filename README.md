# Lumina - Monitor Brightness Controller

Lumina is an application for controlling monitor brightness with system tray interface and keyboard shortcuts.

## Features

- Control brightness of all monitors
- System tray interface with context menu
- Keyboard shortcuts (F2 - decrease brightness, F3 - increase brightness)
- Daemon mode with system tray icon
- Simple brightness setting from command line

## Installation

### System Requirements

- Python 3.7 or newer
- Windows 10/11

### Installing Dependencies

1. Clone or download the project
2. Open terminal/command prompt in the project folder
3. Install required dependencies:

```bash
pip install -r requirements.txt
```

### Alternatively - Install Individual Packages

```bash
pip install screen-brightness-control>=0.16.0
pip install pystray>=0.19.0
pip install Pillow>=9.0.0
pip install keyboard>=0.13.5
```

## Usage

### Daemon Mode (System Tray)

Run the application in daemon mode with system tray icon:

```bash
python lumina.py --daemon
```

or

```bash
lumina.bat
```

**Keyboard Shortcuts:**
- **F2** - Decrease brightness by 5%
- **F3** - Increase brightness by 5%

**System Tray Menu:**
- Current Brightness - shows current value
- Increase Brightness (+5%) - increases brightness by 5%
- Decrease Brightness (-5%) - decreases brightness by 5%
- Set Brightness... - allows entering specific value
- Exit - closes the application

### Command Mode

**Show current brightness:**
```bash
python lumina.py --get
```

**Set specific brightness:**
```bash
python lumina.py 50
```

**Set brightness to 75%:**
```bash
python lumina.py 75
```

## Parameters

- `brightness` - brightness value (0-100, default: 5)
- `--get` - show current brightness instead of setting it
- `-d, --daemon` - run in daemon mode (system tray)

## Troubleshooting

### Permission Error
If the application cannot change brightness, run it as administrator.

### Missing System Tray Icon
Make sure system tray icons are enabled in Windows settings.

### Problem with screen-brightness-control Library
On some systems, additional driver software may be required. Check the library documentation.

## Project Structure

```
lumina/
├── lumina.py          # Main application file
├── lumina.bat         # Launch script
├── requirements.txt   # Python dependencies
└── README.md          # This file
```

## License

This project is available under MIT license. 
