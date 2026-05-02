"""PyInstaller build script for SpeakIt."""

import PyInstaller.__main__

PyInstaller.__main__.run([
    "main.py",
    "--onefile",
    "--windowed",
    "--name=SpeakIt",
    "--icon=assets/icon_idle.png",
    "--add-data=assets;assets",
    "--hidden-import=faster_whisper",
    "--hidden-import=sounddevice",
    "--hidden-import=keyboard",
    "--hidden-import=pyperclip",
    "--hidden-import=pyautogui",
    "--hidden-import=pystray",
    "--hidden-import=winotify",
])
