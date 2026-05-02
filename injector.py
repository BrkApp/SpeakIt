"""Text injection — copies text to clipboard then simulates Ctrl+V."""

import time

import pyperclip
import pyautogui


def inject_text(text: str) -> None:
    """Inject *text* into the currently focused input field.

    The strategy is simple and universal:
    1. Save the current clipboard content.
    2. Copy the transcribed text to the clipboard.
    3. Simulate Ctrl+V to paste.
    4. Restore the original clipboard content.
    """
    if not text:
        return

    # Save previous clipboard
    try:
        previous = pyperclip.paste()
    except pyperclip.PyperclipException:
        previous = ""

    pyperclip.copy(text)
    time.sleep(0.05)  # small delay so the clipboard is ready

    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.1)

    # Restore previous clipboard content
    try:
        pyperclip.copy(previous)
    except pyperclip.PyperclipException:
        pass
