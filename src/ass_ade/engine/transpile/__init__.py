"""Multi-language transpilation engine.

Closes the gap exposed by the ASS-CLAW merge, where non-Python sources
(Swift, TypeScript, Kotlin, Rust) produced JSON blueprints instead of
runnable Python. Each language transpiler converts source into Python
scaffolding with function signatures, docstrings, and preserved bodies
as comments. Tree-sitter based AST upgrade path lives in ``base.py``.

Public API
----------
- :func:`detect_language` - infer language from path/extension
- :func:`get_transpiler`  - get transpiler instance for a language
- :func:`transpile_file`  - one-shot: read, transpile, write Python
- :func:`transpile_tree`  - walk a directory and transpile every
  non-Python source into a mirror Python tree
"""

from __future__ import annotations

from ass_ade.engine.transpile.base import (
    TranspileError,
    TranspileResult,
    Transpiler,
)
from ass_ade.engine.transpile.detect import (
    LANGUAGE_EXTENSIONS,
    SUPPORTED_LANGUAGES,
    detect_language,
)
from ass_ade.engine.transpile.dispatch import (
    get_transpiler,
    transpile_file,
    transpile_source,
    transpile_tree,
)

__all__ = [
    "LANGUAGE_EXTENSIONS",
    "SUPPORTED_LANGUAGES",
    "TranspileError",
    "TranspileResult",
    "Transpiler",
    "detect_language",
    "get_transpiler",
    "transpile_file",
    "transpile_source",
    "transpile_tree",
]
