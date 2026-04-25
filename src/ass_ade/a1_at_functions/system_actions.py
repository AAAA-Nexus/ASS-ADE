"""Tier a1 — pure system-action helpers for ambient awareness (time, presence, desktop)."""

from __future__ import annotations

import subprocess
import sys
import webbrowser
from datetime import datetime
from pathlib import Path
from typing import Any


def get_system_time() -> dict[str, Any]:
    """Return current local time metadata."""
    now = datetime.now()
    return {
        "timestamp": now.isoformat(timespec="seconds"),
        "hour": now.hour,
        "minute": now.minute,
        "day_of_week": now.strftime("%A"),
        "date": now.date().isoformat(),
    }


def get_user_activity_status(threshold_seconds: int = 300) -> dict[str, Any]:
    """Return a best-effort user activity snapshot.

    On Windows we check the last input time via ctypes.  On other platforms
    (or on failure) we return ``is_active=True`` so the wakeup flow is never
    silently blocked.
    """
    idle_seconds = _idle_seconds_windows()
    if idle_seconds is None:
        return {"is_active": True, "idle_minutes": 0.0, "source": "unknown"}
    is_active = idle_seconds < threshold_seconds
    return {
        "is_active": is_active,
        "idle_minutes": round(idle_seconds / 60, 1),
        "source": "win32_last_input",
    }


def open_path(path: Path, *, fullscreen: bool = False) -> bool:
    """Open a local file path in the default application.

    Returns True if the open command was dispatched without error.
    """
    try:
        url = path.as_uri()
        webbrowser.open(url)
        return True
    except Exception:
        pass
    try:
        if sys.platform == "win32":
            subprocess.Popen(["start", "", str(path)], shell=True)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", str(path)])
        else:
            subprocess.Popen(["xdg-open", str(path)])
        return True
    except Exception:
        return False


def send_desktop_notification(title: str, body: str) -> bool:
    """Send a desktop notification if a supported notifier is available.

    Returns True if a notification was dispatched, False otherwise (non-fatal).
    """
    try:
        if sys.platform == "win32":
            _notify_windows(title, body)
            return True
        elif sys.platform == "darwin":
            subprocess.run(
                ["osascript", "-e", f'display notification "{body}" with title "{title}"'],
                check=False,
                timeout=5,
            )
            return True
        else:
            subprocess.run(["notify-send", title, body], check=False, timeout=5)
            return True
    except Exception:
        return False


# ── private helpers ────────────────────────────────────────────────────────────

def _idle_seconds_windows() -> float | None:
    """Return seconds since last user input on Windows, or None on failure."""
    if sys.platform != "win32":
        return None
    try:
        import ctypes

        class _LASTINPUTINFO(ctypes.Structure):
            _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]

        lii = _LASTINPUTINFO()
        lii.cbSize = ctypes.sizeof(lii)
        if ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii)):
            tick_now = ctypes.windll.kernel32.GetTickCount()
            idle_ms = tick_now - lii.dwTime
            return max(0.0, idle_ms / 1000.0)
    except Exception:
        pass
    return None


def _notify_windows(title: str, body: str) -> None:
    """Fire a Windows toast via PowerShell (no extra dependencies)."""
    script = (
        f"[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, "
        f"ContentType = WindowsRuntime] | Out-Null; "
        f"$t = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent("
        f"[Windows.UI.Notifications.ToastTemplateType]::ToastText02); "
        f"$t.SelectSingleNode('//text[@id=1]').InnerText = '{title}'; "
        f"$t.SelectSingleNode('//text[@id=2]').InnerText = '{body}'; "
        f"$n = [Windows.UI.Notifications.ToastNotification]::new($t); "
        f"[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier('Atomadic').Show($n)"
    )
    subprocess.run(
        ["powershell", "-NonInteractive", "-Command", script],
        check=False,
        timeout=10,
        capture_output=True,
    )
