"""Tier a1 — pure system action helpers for OS-level interactions."""

from __future__ import annotations

import subprocess
import sys
import webbrowser
from datetime import datetime, timezone
from pathlib import Path


def open_browser(url: str, fullscreen: bool = True) -> bool:
    """Open *url* in the default browser. Requests fullscreen on Windows if asked.

    Returns True if the open call dispatched without error.
    """
    try:
        webbrowser.open(url, new=2)
    except Exception:
        return False
    if fullscreen:
        _request_fullscreen()
    return True


def play_audio(url: str) -> bool:
    """Open an audio/video URL (e.g. YouTube) in the default browser.

    Returns True if dispatched without error.
    """
    return open_browser(url, fullscreen=False)


def get_system_time() -> datetime:
    """Return the current UTC datetime."""
    return datetime.now(timezone.utc)


def send_desktop_notification(title: str, body: str) -> bool:
    """Send a desktop notification.

    Tries plyer first, then a PowerShell balloon on Windows.
    Returns True if the notification was dispatched without error.
    """
    return _try_plyer(title, body) or _try_powershell(title, body)


# ── internals ──────────────────────────────────────────────────────────────────


def _request_fullscreen() -> None:
    """Best-effort: send F11 to the foreground browser window after a short delay."""
    if sys.platform != "win32":
        return
    script = (
        "Start-Sleep -Milliseconds 1800; "
        "$ws = New-Object -ComObject WScript.Shell; "
        "$ws.SendKeys('{F11}')"
    )
    try:
        subprocess.Popen(
            ["powershell", "-WindowStyle", "Hidden", "-Command", script],
            creationflags=0x08000000,  # CREATE_NO_WINDOW
        )
    except Exception:
        pass


def _try_plyer(title: str, body: str) -> bool:
    try:
        from plyer import notification  # type: ignore[import]
        notification.notify(title=title, message=body, timeout=10)
        return True
    except Exception:
        return False


def _try_powershell(title: str, body: str) -> bool:
    """Windows PowerShell system-tray balloon notification."""
    if sys.platform != "win32":
        return False
    safe_title = title.replace("'", "''").replace('"', '`"')
    safe_body = body.replace("'", "''").replace('"', '`"')
    script = (
        "Add-Type -AssemblyName System.Windows.Forms; "
        "$n = New-Object System.Windows.Forms.NotifyIcon; "
        "$n.Icon = [System.Drawing.SystemIcons]::Information; "
        "$n.BalloonTipIcon = [System.Windows.Forms.ToolTipIcon]::Info; "
        f"$n.BalloonTipTitle = '{safe_title}'; "
        f"$n.BalloonTipText = '{safe_body}'; "
        "$n.Visible = $true; "
        "$n.ShowBalloonTip(8000); "
        "Start-Sleep 9; $n.Dispose()"
    )
    try:
        subprocess.Popen(
            ["powershell", "-WindowStyle", "Hidden", "-Command", script],
            creationflags=0x08000000,  # CREATE_NO_WINDOW
        )
        return True
    except Exception:
        return False


def wake_page_path() -> Path:
    """Return the absolute path to assets/wake.html relative to this package root."""
    return Path(__file__).resolve().parents[4] / "assets" / "wake.html"
