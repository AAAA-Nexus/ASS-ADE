"""Small local system-action helpers for awareness-driven operator moments."""

from __future__ import annotations

import ctypes
import os
import subprocess
import sys
import webbrowser
from datetime import datetime
from pathlib import Path
from typing import Any

_CHROME_CANDIDATES_WIN = (
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
)
_CHROME_CANDIDATES_UNIX = (
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
)


def find_chrome_executable() -> str | None:
    """Return a Chrome/Chromium executable path when one is installed."""
    candidates = _CHROME_CANDIDATES_WIN if sys.platform == "win32" else _CHROME_CANDIDATES_UNIX
    for raw_path in candidates:
        path = Path(raw_path)
        if path.exists():
            return str(path)
    if sys.platform != "win32":
        try:
            result = subprocess.run(
                ["which", "google-chrome"],
                capture_output=True,
                text=True,
                timeout=5,
                check=False,
            )
        except (OSError, subprocess.SubprocessError):
            return None
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    return None


def open_browser(url: str, *, fullscreen: bool = True, app_mode: bool = True) -> bool:
    """Open a URL or file URL in Chrome when available, else the default browser."""
    chrome = find_chrome_executable()
    if chrome is None:
        return webbrowser.open(url)

    args = [chrome]
    if fullscreen:
        args.append("--start-fullscreen")
    if app_mode:
        args.append(f"--app={url}")
    else:
        args.append(url)
    args.append("--autoplay-policy=no-user-gesture-required")
    try:
        subprocess.Popen(args, close_fds=True)
    except OSError:
        return webbrowser.open(url)
    return True


def open_path(path: Path, *, fullscreen: bool = True) -> bool:
    """Open a local file path in a browser."""
    return open_browser(path.resolve().as_uri(), fullscreen=fullscreen)


def get_system_time() -> dict[str, Any]:
    """Return current local system time as simple JSON-ready fields."""
    now = datetime.now()
    return {
        "iso": now.isoformat(timespec="seconds"),
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "hour": now.hour,
        "minute": now.minute,
        "day_of_week": now.strftime("%A"),
        "is_morning": 5 <= now.hour < 12,
        "is_weekend": now.weekday() >= 5,
    }


class _LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_ulong)]


def get_user_activity_status(active_threshold_seconds: int = 300) -> dict[str, Any]:
    """Return idle-time information without installing any background process."""
    if sys.platform != "win32":
        return {
            "idle_seconds": 0.0,
            "idle_minutes": 0.0,
            "is_active": True,
            "active_threshold_seconds": active_threshold_seconds,
            "platform": sys.platform,
            "note": "last-input detection is Windows-only; non-Windows reports active",
        }

    try:
        lii = _LASTINPUTINFO()
        lii.cbSize = ctypes.sizeof(_LASTINPUTINFO)
        ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii))  # type: ignore[attr-defined]
        millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime  # type: ignore[attr-defined]
        idle_seconds = max(0.0, millis / 1000.0)
    except Exception:
        idle_seconds = 0.0

    return {
        "idle_seconds": idle_seconds,
        "idle_minutes": idle_seconds / 60.0,
        "is_active": idle_seconds < active_threshold_seconds,
        "active_threshold_seconds": active_threshold_seconds,
        "platform": "win32",
    }


def send_desktop_notification(title: str, body: str) -> bool:
    """Dispatch a best-effort local desktop notification."""
    safe_title = title.replace('"', "'").replace("\n", " ")[:64]
    safe_body = body.replace('"', "'").replace("\n", " ")[:256]
    if sys.platform == "win32":
        ps = (
            "Add-Type -AssemblyName System.Windows.Forms; "
            "$n = New-Object System.Windows.Forms.NotifyIcon; "
            "$n.Icon = [System.Drawing.SystemIcons]::Information; "
            f'$n.BalloonTipTitle = "{safe_title}"; '
            f'$n.BalloonTipText = "{safe_body}"; '
            "$n.Visible = $true; "
            "$n.ShowBalloonTip(8000); "
            "Start-Sleep -Seconds 9; "
            "$n.Visible = $false"
        )
        try:
            subprocess.Popen(
                ["powershell", "-NonInteractive", "-Command", ps],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except OSError:
            return False
        return True

    try:
        subprocess.Popen(["notify-send", safe_title, safe_body])
    except OSError:
        return False
    return True

