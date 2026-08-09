import tkinter as tk
from tkinter import ttk, messagebox
import screeninfo
from pynput import keyboard # Industry standard for global listeners
import threading
import sys
import os
import ctypes

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class CoordinateApp:
    def __init__(self):
        # Prevent Windows from grouping it with other Python apps to show the correct taskbar icon
        try:
            myappid = 'mycompany.myproduct.subproduct.version'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception:
            pass

        self.root = tk.Tk()
        self.root.title("Pixel Coordinator v1.0")
        
        try:
            self.root.iconbitmap(resource_path('app.ico'))
        except Exception as e:
            print("Could not load icon:", e)
        
        # Persistent State
        self.config = {
            "monitor": 0,
            "hotkey": "f8",  # Lowercase is standard for pynput
            "running": True
        }
        
        self.overlay = None
        self._setup_main_ui()
        self._init_global_hotkey()
        
        self.root.protocol("WM_DELETE_WINDOW", self._on_exit)

    def _setup_main_ui(self):
        frame = ttk.Frame(self.root, padding="20")
        frame.pack()
        ttk.Label(frame, text="Coordinate Auditor", font=("Arial", 10, "bold")).pack(pady=5)
        ttk.Button(frame, text="Start Tracking (Manual)", command=self.start_audit, width=25).pack(pady=5)
        ttk.Button(frame, text="Settings", command=self.open_settings, width=25).pack(pady=5)
        ttk.Button(frame, text="@z3itt", width=25).pack(pady=5)
        self.status_label = ttk.Label(frame, text=f"Hotkey active: [{self.config['hotkey'].upper()}]", foreground="green")
        self.status_label.pack(pady=5)

    def _init_global_hotkey(self):
        """Initializes a background thread to listen for the global hotkey."""
        def on_press(key):
            try:
                # Format key name to string
                k = key.char if hasattr(key, 'char') else key.name
                if k.lower() == self.config['hotkey'].lower():
                    # Thread-safe GUI call
                    self.root.after(0, self.start_audit)
            except AttributeError:
                pass

        self.listener = keyboard.Listener(on_press=on_press)
        self.listener.start()

    def open_settings(self):
        SettingsDialog(self.root, self.config, self.update_hotkey_label)

    def update_hotkey_label(self):
        self.status_label.config(text=f"Hotkey active: [{self.config['hotkey'].upper()}]")

    def start_audit(self):
        if self.overlay: return # Prevent multiple instances (Idempotency)
        
        monitors = screeninfo.get_monitors()
        target = monitors[self.config['monitor']]
        
        self.overlay = tk.Toplevel()
        self.overlay.geometry(f"{target.width}x{target.height}+{target.x}+{target.y}")
        self.overlay.overrideredirect(True)
        self.overlay.attributes("-alpha", 0.3, "-topmost", True)
        self.overlay.config(cursor="crosshair")
        
        canvas = tk.Canvas(self.overlay, bg="black", highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        
        label = canvas.create_text(0, 0, fill="yellow", font=("Consolas", 14, "bold"), anchor="sw")

        def update_pos(e):
            abs_x, abs_y = target.x + e.x, target.y + e.y
            canvas.coords(label, e.x, e.y - 15)
            canvas.itemconfig(label, text=f" {abs_x}, {abs_y} ")

        self.overlay.bind("<Motion>", update_pos)
        self.overlay.bind("<Button-1>", lambda e: self.stop_audit())
        self.overlay.bind("<Escape>", lambda e: self.stop_audit())

    def stop_audit(self):
        if self.overlay:
            self.overlay.destroy()
            self.overlay = None

    def _on_exit(self):
        self.config['running'] = False
        self.listener.stop()
        self.root.destroy()

class SettingsDialog(tk.Toplevel):
    def __init__(self, parent, config, callback):
        super().__init__(parent)
        self.title("Configuration")
        self.config = config
        self.callback = callback
        self.grab_set()
        
        container = ttk.Frame(self, padding=20)
        container.pack()

        # Monitor Selection
        ttk.Label(container, text="Monitor:").grid(row=0, column=0, pady=5, sticky="w")
        self.mon_combo = ttk.Combobox(container, values=[f"Display {i}" for i in range(len(screeninfo.get_monitors()))])
        self.mon_combo.current(self.config['monitor'])
        self.mon_combo.grid(row=0, column=1, pady=5)

        # Hotkey Input
        ttk.Label(container, text="Hotkey:").grid(row=1, column=0, pady=5, sticky="w")
        self.hk_entry = ttk.Entry(container)
        self.hk_entry.insert(0, self.config['hotkey'])
        self.hk_entry.grid(row=1, column=1, pady=5)

        ttk.Button(container, text="Save Changes", command=self.save).grid(row=2, column=0, columnspan=2, pady=10)

    def save(self):
        self.config['monitor'] = self.mon_combo.current()
        self.config['hotkey'] = self.hk_entry.get().lower()
        self.callback()
        self.destroy()

if __name__ == "__main__":
    app = CoordinateApp()
    app.root.mainloop()