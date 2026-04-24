#!/usr/bin/env python3
"""Compatibility wrapper for ``tools/assimilate_multi_source.py``.

This filename remains because older operator notes call it directly. New logic
belongs in the source-agnostic multi-source driver.
"""

from __future__ import annotations

try:
    from tools import assimilate_multi_source as _driver
except ModuleNotFoundError:
    import assimilate_multi_source as _driver  # type: ignore[no-redef]

_dedupe_roots = _driver._dedupe_roots
_env_source_roots = _driver._env_source_roots
_root_ids = _driver._root_ids
_slug = _driver._slug
main = _driver.main

if __name__ == "__main__":
    raise SystemExit(main())
