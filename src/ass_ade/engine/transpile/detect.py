"""Language detection for the transpile engine."""

from __future__ import annotations

from pathlib import Path

LANGUAGE_EXTENSIONS: dict[str, tuple[str, ...]] = {
    "python": (".py",),
    "swift": (".swift",),
    "typescript": (".ts", ".tsx"),
    "javascript": (".js", ".jsx", ".mjs", ".cjs"),
    "kotlin": (".kt", ".kts"),
    "rust": (".rs",),
}

SUPPORTED_LANGUAGES: tuple[str, ...] = tuple(LANGUAGE_EXTENSIONS.keys())

_EXT_TO_LANG: dict[str, str] = {
    ext: lang for lang, exts in LANGUAGE_EXTENSIONS.items() for ext in exts
}


def detect_language(path: str | Path) -> str | None:
    """Return the language name for ``path`` based on its extension.

    Returns ``None`` if the extension is not recognized. Callers should
    treat ``None`` as a skip signal, not an error.
    """
    ext = Path(path).suffix.lower()
    return _EXT_TO_LANG.get(ext)


def is_transpile_target(path: str | Path) -> bool:
    """Return True if ``path`` can be fed to :func:`transpile_file`."""
    return detect_language(path) is not None
