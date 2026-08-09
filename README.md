# Pixel Coordinator

Pixel Coordinator (also known as Lead Engineer Tool) is a lightweight, transparent overlay utility built in Python that allows you to accurately track and capture real-time mouse coordinates on any of your monitors. Perfect for developers, QA engineers, and designers who need precise pixel measurements and on-screen coordinate targeting.

## ✨ Features

- **Real-Time Tracking**: Displays live X and Y coordinates following your cursor.
- **Multi-Monitor Support**: Select exactly which monitor you want to audit.
- **Global Hotkey**: Start auditing instantly from anywhere using a customizable global hotkey (Default: `F8`).
- **Transparent Overlay**: Non-intrusive UI that dims the screen slightly for better visibility of coordinates.
- **Quick Exit**: Stop the audit simply by clicking the left mouse button or pressing `ESC`.

## 🚀 Installation & Usage

### Option 1: Standalone Executable
You can download the pre-compiled `.exe` from the [Releases](https://github.com/z3itt/pixel-coordinator/releases) page and run it directly without installing Python.

### Option 2: Running from Source
1. Clone the repository:
   ```bash
   git clone https://github.com/z3itt/pixel-coordinator.git
   cd pixel-coordinator
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python coordinator.py
   ```

## 🛠️ Building the Executable
To build the `.exe` yourself using PyInstaller, simply run:
```bash
pyinstaller coordinator.spec
```
The compiled executable will be located in the `dist/` folder.

## ⚙️ Configuration
Click the **Settings** button in the main menu to:
- Change the target monitor.
- Set a custom global hotkey for starting the audit.

## 👤 Author
Developed by [@z3itt](https://github.com/z3itt)
