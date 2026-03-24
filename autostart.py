"""Auto-start management — add/remove SpeakIt from Windows startup."""

import os
import sys
import winreg

APP_NAME = "SpeakIt"
REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"


def _get_exe_path() -> str:
    """Return the path to the current executable (supports both .py and .exe)."""
    if getattr(sys, "frozen", False):
        return sys.executable
    return f'"{sys.executable}" "{os.path.abspath(sys.argv[0])}"'


def is_autostart_enabled() -> bool:
    """Check if SpeakIt is registered in Windows startup."""
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_READ) as key:
            winreg.QueryValueEx(key, APP_NAME)
            return True
    except FileNotFoundError:
        return False
    except OSError:
        return False


def enable_autostart() -> bool:
    """Register SpeakIt to start automatically with Windows."""
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, _get_exe_path())
        return True
    except OSError:
        return False


def disable_autostart() -> bool:
    """Remove SpeakIt from Windows startup."""
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_SET_VALUE) as key:
            winreg.DeleteValue(key, APP_NAME)
        return True
    except FileNotFoundError:
        return True  # already removed
    except OSError:
        return False


def toggle_autostart() -> bool:
    """Toggle auto-start and return the new state (True = enabled)."""
    if is_autostart_enabled():
        disable_autostart()
        return False
    else:
        enable_autostart()
        return True
