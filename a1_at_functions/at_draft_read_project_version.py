# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/protocol/evolution.py:133
# Component id: at.source.ass_ade.read_project_version
__version__ = "0.1.0"

def read_project_version(root: Path) -> str:
    root = root.resolve()
    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        try:
            data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
            version = data.get("project", {}).get("version")
            if isinstance(version, str) and version.strip():
                return version.strip()
        except (OSError, tomllib.TOMLDecodeError):
            pass

    init_file = root / "src" / "ass_ade" / "__init__.py"
    if init_file.exists():
        match = re.search(
            r"^__version__\s*=\s*['\"]([^'\"]+)['\"]",
            init_file.read_text(encoding="utf-8"),
            flags=re.MULTILINE,
        )
        if match:
            return match.group(1)

    version_file = root / "VERSION"
    if version_file.exists():
        lines = version_file.read_text(encoding="utf-8").splitlines()
        if lines and lines[0].strip():
            return lines[0].strip()
    return INITIAL_VERSION
