# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_load_project_metadata.py:5
# Component id: at.source.ass_ade.load_project_metadata
__version__ = "0.1.0"

def load_project_metadata(root: Path) -> dict[str, Any]:
    result: dict[str, Any] = {
        "source": None,
        "name": None,
        "version": None,
        "description": None,
        "dependencies": [],
        "entry_points": [],
        "license": None,
        "language_hint": None,
    }

    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        result["source"] = "pyproject.toml"
        result["language_hint"] = "python"
        try:
            try:
                import tomllib
            except ImportError:
                import tomli as tomllib  # type: ignore[no-reattr]
            data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
            project = data.get("project", {})
            result["name"] = project.get("name")
            result["version"] = project.get("version")
            result["description"] = project.get("description")
            result["license"] = project.get("license")
            result["dependencies"] = project.get("dependencies", [])
            scripts = project.get("scripts", {})
            result["entry_points"] = list(scripts.keys())
            return result
        except Exception:
            pass
        # regex fallback
        try:
            raw = pyproject.read_text(encoding="utf-8")
            for field in ("name", "version", "description"):
                m = re.search(rf'^{field}\s*=\s*"([^"]+)"', raw, re.MULTILINE)
                if m:
                    result[field] = m.group(1)
        except Exception:
            pass
        return result

    for filename in ("setup.py", "setup.cfg"):
        candidate = root / filename
        if candidate.exists():
            result["source"] = filename
            result["language_hint"] = "python"
            try:
                raw = candidate.read_text(encoding="utf-8")
                for field in ("name", "version"):
                    m = re.search(rf'{field}\s*=\s*["\']([^"\']+)["\']', raw)
                    if m:
                        result[field] = m.group(1)
            except Exception:
                pass
            return result

    package_json = root / "package.json"
    if package_json.exists():
        result["source"] = "package.json"
        result["language_hint"] = "javascript"
        try:
            import json
            data = json.loads(package_json.read_text(encoding="utf-8"))
            result["name"] = data.get("name")
            result["version"] = data.get("version")
            result["description"] = data.get("description")
            deps = list(data.get("dependencies", {}).keys())
            deps += list(data.get("devDependencies", {}).keys())
            result["dependencies"] = deps
            result["entry_points"] = list(data.get("scripts", {}).keys())
            result["license"] = data.get("license")
        except Exception:
            pass
        return result

    cargo = root / "Cargo.toml"
    if cargo.exists():
        result["source"] = "Cargo.toml"
        result["language_hint"] = "rust"
        try:
            try:
                import tomllib
            except ImportError:
                import tomli as tomllib  # type: ignore[no-reattr]
            data = tomllib.loads(cargo.read_text(encoding="utf-8"))
            pkg = data.get("package", {})
            result["name"] = pkg.get("name")
            result["version"] = pkg.get("version")
            result["description"] = pkg.get("description")
        except Exception:
            pass
        return result

    go_mod = root / "go.mod"
    if go_mod.exists():
        result["source"] = "go.mod"
        result["language_hint"] = "go"
        try:
            raw = go_mod.read_text(encoding="utf-8")
            m = re.search(r"^module\s+(\S+)", raw, re.MULTILINE)
            if m:
                result["name"] = m.group(1)
            m = re.search(r"^go\s+(\S+)", raw, re.MULTILINE)
            if m:
                result["version"] = m.group(1)
        except Exception:
            pass
        return result

    return result
