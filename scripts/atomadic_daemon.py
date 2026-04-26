"""Atomadic Discord Bot watchdog daemon.

Keeps atomadic_discord_bot.py alive permanently. On crash: exponential backoff,
then restart. On clean exit (code 0): stop.

Usage:
    python scripts/atomadic_daemon.py
    atomadic discord start --daemon

Logs to .ass-ade/logs/daemon.log with rotation (5 MB × 3 files).
"""

from __future__ import annotations

import logging
import logging.handlers
import signal
import subprocess
import sys
import time
from pathlib import Path

BOT_SCRIPT = Path(__file__).parent / "atomadic_discord_bot.py"
SEED_ROOT = BOT_SCRIPT.parent.parent
LOG_DIR = SEED_ROOT / ".ass-ade" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

_handler = logging.handlers.RotatingFileHandler(
    LOG_DIR / "daemon.log", maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
)
_handler.setFormatter(logging.Formatter("%(asctime)s [daemon] %(levelname)s %(message)s"))
_stream = logging.StreamHandler()
_stream.setFormatter(logging.Formatter("%(asctime)s [daemon] %(message)s"))
logging.basicConfig(level=logging.INFO, handlers=[_handler, _stream])
log = logging.getLogger("atomadic.daemon")

# Backoff config
_INITIAL_BACKOFF = 2
_MAX_BACKOFF = 120
# If the process lives longer than this before dying, reset the backoff counter.
_STABLE_THRESHOLD = 30

_shutdown = False


def _handle_signal(sig: int, _frame: object) -> None:
    global _shutdown
    log.info("Signal %d received — daemon shutting down gracefully", sig)
    _shutdown = True


def run() -> None:
    global _shutdown
    signal.signal(signal.SIGTERM, _handle_signal)
    signal.signal(signal.SIGINT, _handle_signal)

    log.info("Atomadic daemon started. Watching: %s", BOT_SCRIPT)
    backoff = _INITIAL_BACKOFF
    restarts = 0
    proc: subprocess.Popen | None = None

    while not _shutdown:
        log.info("Launching bot (attempt %d)…", restarts + 1)
        t0 = time.monotonic()
        try:
            proc = subprocess.Popen(
                [sys.executable, str(BOT_SCRIPT)],
                cwd=str(SEED_ROOT),
            )
            proc.wait()
        except KeyboardInterrupt:
            _shutdown = True
            if proc and proc.poll() is None:
                proc.terminate()
            break

        exit_code = proc.returncode if proc else -1
        elapsed = time.monotonic() - t0
        restarts += 1

        if exit_code == 0:
            log.info("Bot exited cleanly (code 0) after %.0fs — daemon stopping.", elapsed)
            break

        if elapsed >= _STABLE_THRESHOLD:
            log.info("Bot ran %.0fs before exit %d — treating as stable, resetting backoff.", elapsed, exit_code)
            backoff = _INITIAL_BACKOFF
        else:
            log.warning("Bot crashed after %.1fs (exit %d). Backoff: %ds.", elapsed, exit_code, backoff)

        if _shutdown:
            break

        log.info("Restart #%d in %ds…", restarts + 1, backoff)
        for _ in range(backoff):
            if _shutdown:
                break
            time.sleep(1)
        backoff = min(backoff * 2, _MAX_BACKOFF)

    log.info("Daemon exited after %d restart(s).", restarts)


if __name__ == "__main__":
    run()
