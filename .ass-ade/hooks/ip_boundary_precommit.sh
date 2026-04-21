#!/usr/bin/env bash
# T-E1a pre-commit hook: run IP-boundary linter over staged files.
#
# Blocks a commit that introduces any forbidden name or numeric constant
# into the public surface as defined in
# .ass-ade/lints/ip_boundary.yaml.
#
# Plan: autopoietic-ai-research-enhance-assade-r2-20260420-0212 (task T-E1a).

set -euo pipefail

REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
CONFIG="$REPO_ROOT/.ass-ade/lints/ip_boundary.yaml"

if [ ! -f "$CONFIG" ]; then
  echo "[ip-boundary] config missing: $CONFIG" >&2
  exit 0   # fail-open when lint infra itself is missing; CI catches it
fi

STAGED=$(git diff --cached --name-only --diff-filter=ACM || true)
if [ -z "$STAGED" ]; then
  exit 0
fi

PY=${PYTHON:-python3}

"$PY" - "$CONFIG" <<'PYEOF' "$@"
import os
import re
import subprocess
import sys
from pathlib import Path

config_path = Path(sys.argv[1])
repo_root = Path(
    subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
)

sys.path.insert(0, str(repo_root / "!ass-ade" / "src"))
sys.path.insert(0, str(repo_root / "src"))

try:
    from ass_ade.a1_at_functions.ip_boundary_linter import (
        lint_text,
        load_config_from_yaml_text,
        Severity,
    )
except Exception as exc:  # pragma: no cover
    print(f"[ip-boundary] linter import failed: {exc}", file=sys.stderr)
    sys.exit(0)

config = load_config_from_yaml_text(config_path.read_text(encoding="utf-8"))
allow_paths = config.get("allow_paths", [])

def is_allowed(p: str) -> bool:
    for pat in allow_paths:
        rx = re.escape(pat).replace(r"\*\*", ".*").replace(r"\*", "[^/]*")
        if re.match("^" + rx + "$", p):
            return True
    return False

staged = subprocess.check_output(
    ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"], text=True
).splitlines()

hits = 0
crit = 0
for rel in staged:
    if not rel or is_allowed(rel):
        continue
    full = repo_root / rel
    if not full.is_file():
        continue
    try:
        text = full.read_text(encoding="utf-8", errors="replace")
    except OSError:
        continue
    findings = lint_text(text, config, source_path=rel)
    for f in findings:
        print(
            f"[ip-boundary] {f.severity.value} {rel}:{f.line}:{f.column} "
            f"rule={f.rule} match={f.match!r}",
            file=sys.stderr,
        )
        hits += 1
        if f.severity == Severity.CRITICAL:
            crit += 1

if hits:
    print(f"[ip-boundary] {hits} finding(s), {crit} CRITICAL", file=sys.stderr)
    sys.exit(1 if crit > 0 else 0)
PYEOF
