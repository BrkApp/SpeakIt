"""SpeakIt — Windows voice dictation app.

Listens for Ctrl+Space, records audio, transcribes with Whisper,
and injects the text into the active input field.
"""

import sys
import os
import threading
import datetime

import keyboard
from PIL import Image
import pystray

import config
from audio import AudioRecorder
from transcriber import Transcriber
from injector import inject_text
from notifier import notify

# ---------------------------------------------------------------------------
# Globals
# ---------------------------------------------------------------------------

recorder = AudioRecorder()
transcriber = Transcriber()
tray_icon: pystray.Icon | None = None
_recording_lock = threading.Lock()

# ---------------------------------------------------------------------------
# Asset helpers
# ---------------------------------------------------------------------------

def _asset_path(filename: str) -> str:
    """Return absolute path to an asset file, works both for dev and PyInstaller."""
    if getattr(sys, "frozen", False):
        base = sys._MEIPASS  # type: ignore[attr-defined]
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "assets", filename)


def _load_icon(name: str) -> Image.Image:
    path = _asset_path(name)
    if os.path.exists(path):
        return Image.open(path)
    # Generate a simple coloured circle fallback
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    color = (220, 50, 50, 255) if "recording" in name else (80, 130, 200, 255)
    draw.ellipse([4, 4, 60, 60], fill=color)
    return img


icon_idle: Image.Image | None = None
icon_recording: Image.Image | None = None

# ---------------------------------------------------------------------------
# Transcription log
# ---------------------------------------------------------------------------

def _log_transcription(text: str) -> None:
    if not config.ENABLE_LOG:
        return
    try:
        with open(config.LOG_FILE, "a", encoding="utf-8") as f:
            ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{ts}] {text}\n")
    except OSError:
        pass

# ---------------------------------------------------------------------------
# Hotkey handler
# ---------------------------------------------------------------------------

def _on_hotkey() -> None:
    """Toggle recording on each Ctrl+Space press."""
    with _recording_lock:
        if not recorder.is_recording:
            _start_recording()
        else:
            _stop_and_transcribe()


def _start_recording() -> None:
    recorder.start()
    if tray_icon and icon_recording:
        tray_icon.icon = icon_recording
    print("[recording…]")


def _stop_and_transcribe() -> None:
    audio = recorder.stop()
    if tray_icon and icon_idle:
        tray_icon.icon = icon_idle

    if audio is None or len(audio) == 0:
        print("[no audio captured]")
        return

    print("[transcribing…]")
    try:
        text = transcriber.transcribe(audio)
    except Exception as exc:
        notify("SpeakIt — Erreur", str(exc))
        print(f"Transcription error: {exc}")
        return

    if not text:
        notify("SpeakIt", "Aucun texte détecté.")
        return

    word_count = len(text.split())
    inject_text(text)
    _log_transcription(text)
    notify("SpeakIt", f"✓ Transcrit : {word_count} mots")
    print(f"[injected] {text}")

# ---------------------------------------------------------------------------
# System tray
# ---------------------------------------------------------------------------

def _quit_app(icon: pystray.Icon, _item: pystray.MenuItem) -> None:
    """Clean shutdown."""
    recorder.cleanup()
    keyboard.unhook_all()
    icon.stop()


def _build_tray() -> pystray.Icon:
    menu = pystray.Menu(
        pystray.MenuItem("SpeakIt — Dictée vocale", lambda *_: None, enabled=False),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem(f"Raccourci : {config.HOTKEY}", lambda *_: None, enabled=False),
        pystray.MenuItem(f"Modèle : {config.WHISPER_MODEL}", lambda *_: None, enabled=False),
        pystray.MenuItem(f"Langue : {config.WHISPER_LANGUAGE}", lambda *_: None, enabled=False),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Quitter", _quit_app),
    )
    icon = pystray.Icon("SpeakIt", icon_idle, "SpeakIt — Dictée vocale", menu)
    return icon

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    global tray_icon, icon_idle, icon_recording

    print("SpeakIt — Démarrage…")

    # Load icons
    icon_idle = _load_icon("icon_idle.png")
    icon_recording = _load_icon("icon_recording.png")

    # Load Whisper model once
    transcriber.load_model()

    # Register global hotkey
    keyboard.add_hotkey(config.HOTKEY, _on_hotkey, suppress=True)
    print(f"Hotkey {config.HOTKEY} enregistré.")

    # Build and run system tray (blocks on this thread)
    tray_icon = _build_tray()
    print("SpeakIt prêt — en attente dans le system tray.")
    tray_icon.run()


if __name__ == "__main__":
    main()
