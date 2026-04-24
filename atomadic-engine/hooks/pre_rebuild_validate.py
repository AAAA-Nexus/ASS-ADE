"""Pre-rebuild hook: validate blueprints before materializing.

Reads all AAAA-SPEC-004 blueprint JSON files in the target directory (or a
blueprints/ sub-folder) and checks that they are well-formed before allowing
the rebuild to proceed. Returns ok=False and halts the rebuild if any blueprint
has a critical schema error.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_REQUIRED_FIELDS = {"schema", "version", "feature", "components", "entry_point"}
_REQUIRED_COMPONENT_FIELDS = {"id", "tier", "role"}
_VALID_TIERS = {"qk", "at", "mo", "og", "sy"}


def _validate_blueprint(path: Path) -> list[str]:
    """Return a list of error strings for a blueprint file (empty = valid)."""
    errors: list[str] = []
    try:
        bp = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        return [f"cannot parse: {exc}"]

    missing = _REQUIRED_FIELDS - set(bp.keys())
    if missing:
        errors.append(f"missing top-level fields: {sorted(missing)}")

    components = bp.get("components", [])
    if not isinstance(components, list):
        errors.append("'components' must be a list")
        return errors

    entry = bp.get("entry_point", "")
    entry_ids = {c.get("id", "") for c in components if isinstance(c, dict)}

    if entry and entry not in entry_ids:
        errors.append(f"entry_point '{entry}' not found in components")

    for i, c in enumerate(components):
        if not isinstance(c, dict):
            errors.append(f"component[{i}] is not an object")
            continue
        comp_missing = _REQUIRED_COMPONENT_FIELDS - set(c.keys())
        if comp_missing:
            errors.append(f"component[{i}] missing fields: {sorted(comp_missing)}")
        tier = c.get("tier", "")
        if tier and tier not in _VALID_TIERS:
            errors.append(f"component[{i}] has invalid tier '{tier}' (must be one of {sorted(_VALID_TIERS)})")
        deps = c.get("dependencies", [])
        if not isinstance(deps, list):
            errors.append(f"component[{i}] 'dependencies' must be a list")

    return errors


def run(path: str) -> dict:
    """Validate blueprints before rebuild.

    Args:
        path: The codebase path that is about to be rebuilt.

    Returns:
        dict with keys:
            ok (bool): False if any blueprint has critical errors (blocks rebuild).
            blueprint_count (int): Number of blueprint files found.
            valid_count (int): Number of blueprints that passed validation.
            invalid_count (int): Number of blueprints with errors.
            findings (list[dict]): Per-file validation results.
            path_exists (bool): Whether the target path exists.
    """
    target = Path(path)
    if not target.exists():
        return {
            "ok": False,
            "blueprint_count": 0,
            "valid_count": 0,
            "invalid_count": 0,
            "findings": [],
            "path_exists": False,
            "error": f"path does not exist: {path}",
        }

    # Search target and target/blueprints/ for *.blueprint.json or blueprint*.json
    search_dirs = [target]
    bp_subdir = target / "blueprints"
    if bp_subdir.exists():
        search_dirs.append(bp_subdir)

    blueprint_files: list[Path] = []
    for d in search_dirs:
        blueprint_files.extend(d.glob("*.blueprint.json"))
        blueprint_files.extend(d.glob("blueprint*.json"))
        blueprint_files.extend(d.glob("**/blueprints/*.json"))

    # Deduplicate
    seen: set[Path] = set()
    unique_blueprints: list[Path] = []
    for f in blueprint_files:
        resolved = f.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique_blueprints.append(f)

    if not unique_blueprints:
        # No blueprints found — that's fine, proceed with rebuild.
        return {
            "ok": True,
            "blueprint_count": 0,
            "valid_count": 0,
            "invalid_count": 0,
            "findings": [],
            "path_exists": True,
        }

    findings: list[dict] = []
    invalid_count = 0

    for bp_file in sorted(unique_blueprints):
        errors = _validate_blueprint(bp_file)
        findings.append({
            "file": str(bp_file),
            "valid": len(errors) == 0,
            "errors": errors,
        })
        if errors:
            invalid_count += 1

    valid_count = len(unique_blueprints) - invalid_count

    return {
        "ok": invalid_count == 0,
        "blueprint_count": len(unique_blueprints),
        "valid_count": valid_count,
        "invalid_count": invalid_count,
        "findings": findings,
        "path_exists": True,
    }


if __name__ == "__main__":
    target_path = sys.argv[1] if len(sys.argv) > 1 else "."
    result = run(target_path)
    print(json.dumps(result, indent=2))
    # Non-zero exit when blueprints are invalid.
    if not result.get("ok"):
        invalid = result.get("invalid_count", 0)
        print(f"[pre_rebuild_validate] {invalid} blueprint(s) failed validation. Fix errors before rebuilding.", file=sys.stderr)
        sys.exit(1)
