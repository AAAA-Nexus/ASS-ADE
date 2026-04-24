"""Tier a2 — assimilated method 'MCPServer.__init__'

Assimilated from: server.py:528-547
"""

from __future__ import annotations


# --- assimilated symbol ---
def __init__(self, working_dir: str = ".") -> None:
    self._registry = default_registry(working_dir)
    self._working_dir = working_dir
    self._initialized = False
    # Track in-flight request IDs for cancellation support
    self._cancelled: set[Any] = set()
    self._lock = threading.Lock()
    self._write_lock = threading.Lock()
    # Thread pool for dispatching long-running tool calls
    self._executor = futures.ThreadPoolExecutor(max_workers=2)
    # Track in-flight futures by request ID for cancellation
    self._futures: dict[Any, futures.Future[dict[str, Any] | None]] = {}
    # Track cancellation contexts by request ID for cooperative cancellation
    self._cancellation_contexts: dict[Any, CancellationContext] = {}
    # Phase 2/3/5: TCA, CIE, LoRA flywheel engines (lazy init)
    self._tca: Any = None
    self._cie: Any = None
    self._lora_flywheel: Any = None
    # NCB enforcement mode: "warn" (local, default) or "block" (hybrid/premium)
    self._ncb_mode: str = "warn"

