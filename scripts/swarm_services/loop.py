from __future__ import annotations

import signal
import sys
import time
from pathlib import Path

from .config import SwarmServiceConfig
from .pulse import automation_dir, one_tick, write_automation_pulse
from .state import DaemonState


def run_forever(cfg: SwarmServiceConfig) -> int:
    """Block until SIGINT/SIGTERM; one tick per interval."""
    dpath = automation_dir(cfg) / "daemon_state.json"
    st = DaemonState.load(dpath)
    stop = [False]

    def _h(signum, frame) -> None:  # type: ignore[no-untyped-def]
        stop[0] = True

    if sys.platform != "win32":
        signal.signal(signal.SIGTERM, _h)
    signal.signal(signal.SIGINT, _h)

    print(
        f"swarm-services: repo={cfg.repo_root}\n"
        f"  plan=.ato-plans/{cfg.plan_rel_dir}\n"
        f"  interval={cfg.tick_interval_sec}s (SWARM_TICK_SEC)\n"
        f"  Ctrl+C to stop.",
        flush=True,
    )
    while not stop[0]:
        try:
            st, summary = one_tick(cfg, st)
            write_automation_pulse(cfg, st, summary)
            st.save(dpath)
            print(f"{summary}", flush=True)
        except Exception as e:
            print(f"swarm-services tick error: {type(e).__name__}: {e}", file=sys.stderr, flush=True)
        t = 0.0
        while t < cfg.tick_interval_sec and not stop[0]:
            time.sleep(min(1.0, cfg.tick_interval_sec - t))
            t += 1.0
    print("swarm-services: shutdown OK", flush=True)
    return 0
