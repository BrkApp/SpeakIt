"""Windows toast notifications."""

import threading


def notify(title: str, message: str) -> None:
    """Show a Windows toast notification (non-blocking)."""
    threading.Thread(target=_show, args=(title, message), daemon=True).start()


def _show(title: str, message: str) -> None:
    try:
        from winotify import Notification

        toast = Notification(
            app_id="SpeakIt",
            title=title,
            msg=message,
            duration="short",
        )
        toast.show()
    except Exception:
        # Fallback: print to console if notifications fail
        print(f"[{title}] {message}")
