import screen_brightness_control as sbc
import argparse
import sys
import threading
import time
from pystray import Icon, Menu, MenuItem
from PIL import Image
import keyboard
import os

class MonitorBrightnessController:
    def set_brightness(self, brightness):
        """Set the brightness of external monitors (skip laptop screen)."""
        try:
            brightness_values = sbc.get_brightness()
            if isinstance(brightness_values, list) and len(brightness_values) > 1:
                # Keep laptop screen brightness unchanged, set external monitors
                new_brightness_list = [brightness_values[0]] + [brightness] * (len(brightness_values) - 1)
                sbc.set_brightness(new_brightness_list)
            else:
                sbc.set_brightness(brightness)
        except Exception as e:
            # Fallback: try to set brightness directly
            sbc.set_brightness(brightness)

    def get_brightness(self):
        """Get the average brightness of external monitors (skip laptop screen)."""
        try:
            brightness_values = sbc.get_brightness()
            if isinstance(brightness_values, list) and len(brightness_values) > 1:
                # Skip first value (laptop screen) and average the rest
                external_monitors = brightness_values[1:]
                return sum(external_monitors) // len(external_monitors)
            elif isinstance(brightness_values, list):
                return brightness_values[0]  # Single monitor
            return brightness_values  # Single value
        except Exception as e:
            # Fallback: try to get brightness directly
            return sbc.get_brightness()

    def increase_brightness(self, step=5):
        """Increase brightness by step percentage."""
        current = self.get_brightness()
        new_brightness = min(100, current + step)
        self.set_brightness(new_brightness)
        return new_brightness

    def decrease_brightness(self, step=5):
        """Decrease brightness by step percentage."""
        current = self.get_brightness()
        new_brightness = max(0, current - step)
        self.set_brightness(new_brightness)
        return new_brightness

class SystemTrayApp:
    def __init__(self, controller):
        self.controller = controller
        self.icon = None
        self.setup_icon()
        self.setup_hotkeys()

    def setup_icon(self):
        # Creating simple icon (white square on black background)
        img = Image.new('RGB', (64, 64), color='black')
        for i in range(16, 48):
            for j in range(16, 48):
                img.putpixel((i, j), (255, 255, 255))

        brightness = self.controller.get_brightness()

        self.menu = Menu(
            MenuItem(f"Current Brightness: {brightness}%", self.show_current_brightness),
            MenuItem("Increase Brightness (+5%)", self.increase_brightness),
            MenuItem("Decrease Brightness (-5%)", self.decrease_brightness),
            Menu.SEPARATOR,
            MenuItem("Exit", self.stop)
        )

        self.icon = Icon("Lumina", img, "Lumina - Brightness Controller", self.menu)
        
        # Update menu with initial brightness
        self.update_menu()

    def setup_hotkeys(self):
        keyboard.add_hotkey('shift+ctrl+f2', self.decrease_brightness)
        keyboard.add_hotkey('shift+ctrl+f3', self.increase_brightness)

    def update_menu(self):
        """Update menu with current brightness."""
        try:
            brightness = self.controller.get_brightness()
            # Create new menu with updated brightness
            new_menu = Menu(
                MenuItem(f"Current Brightness: {brightness}%", self.show_current_brightness),
                MenuItem("Increase Brightness (+5%)", self.increase_brightness),
                MenuItem("Decrease Brightness (-5%)", self.decrease_brightness),
                Menu.SEPARATOR,
                MenuItem("Exit", self.stop)
            )
            # Update the icon's menu
            self.icon.menu = new_menu
            self.menu = new_menu
        except Exception as e:
            # If update fails, keep original menu
            pass

    def show_current_brightness(self):
        brightness = self.controller.get_brightness()
        self.icon.notify(f"Current brightness: {brightness}%", "Lumina")

    def increase_brightness(self):
        new_brightness = self.controller.increase_brightness(5)
        self.icon.notify(f"Increased brightness: {new_brightness}%", "Lumina")
        self.update_menu()

    def decrease_brightness(self):
        new_brightness = self.controller.decrease_brightness(5)
        self.icon.notify(f"Decreased brightness: {new_brightness}%", "Lumina")
        self.update_menu()



    def stop(self):
        self.icon.stop()
        keyboard.unhook_all()

    def run(self):
        self.icon.run()

def main():
    parser = argparse.ArgumentParser(description='Monitor brightness controller')
    parser.add_argument('brightness', nargs='?', type=int, default=5, 
                       help='Brightness (0-100, default: 5)')
    parser.add_argument('--get', action='store_true', 
                       help='Show current brightness instead of setting it')
    parser.add_argument('-d', '--daemon', action='store_true',
                       help='Run in daemon mode (system tray)')
    
    args = parser.parse_args()
    
    controller = MonitorBrightnessController()
    
    if args.daemon:
        # Run in daemon mode without console window
        print("Starting Lumina in daemon mode...")
        print("Keyboard shortcuts:")
        print("  Shift+Ctrl+F2 - Decrease brightness by 5%")
        print("  Shift+Ctrl+F3 - Increase brightness by 5%")
        print("System tray icon provides additional options.")
        
        app = SystemTrayApp(controller)
        app.run()
    elif args.get:
        current_brightness = controller.get_brightness()
        print(f"Current brightness: {current_brightness}%")
    else:
        if not 0 <= args.brightness <= 100:
            print("Error: Brightness must be between 0-100")
            sys.exit(1)
        
        controller.set_brightness(args.brightness)
        print(f"Brightness set to: {args.brightness}%")

if __name__ == "__main__":
    main()
