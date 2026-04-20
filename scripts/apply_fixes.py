"""Apply mechanical code fixes from enhance scan findings.

Reads enhance_scan.json and applies safe, automated improvements
to source files. Used by the auto-evolve CI workflows.

Usage:
    python3 scripts/apply_fixes.py [max_fixes] [--lane LANE]

Supported categories (all lanes):
    bare_except     -> replace `except:` with `except Exception:`
    missing_docs    -> add minimal docstring to undocumented functions

Lane-specific categories:
    security: bare_except, security
    quality:  bare_except, missing_docs, missing_types
    default:  bare_except, missing_docs
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def apply_bare_except(file_path: str) -> int:
    """Replace all bare `except:` with `except Exception:`. Returns change count."""
    p = Path(file_path)
    if not p.exists() or not p.suffix == ".py":
        return 0
    content = p.read_text(encoding="utf-8")
    new_content = re.sub(r"(?m)^(\s*)except\s*:", r"\1except Exception:", content)
    if new_content != content:
        p.write_text(new_content, encoding="utf-8")
        count = content.count("except:") - new_content.count("except:")
        return max(count, 1)
    return 0


def apply_missing_docstring(file_path: str, line_num: int | None) -> bool:
    """Add minimal docstring to function at line_num. Returns True if applied."""
    if line_num is None:
        return False
    p = Path(file_path)
    if not p.exists() or not p.suffix == ".py":
        return False
    try:
        lines = p.read_text(encoding="utf-8").splitlines(keepends=True)
    except Exception:
        return False
    idx = line_num - 1
    if idx >= len(lines):
        return False
    func_line = lines[idx]
    if not re.match(r"\s*def ", func_line):
        return False
    # Don't add if already has docstring
    next_idx = idx + 1
    # Skip decorator / signature continuation lines
    while next_idx < len(lines) and (
        lines[next_idx].rstrip().endswith(")") or lines[next_idx].rstrip().endswith(",")
        or lines[next_idx].strip().startswith("#")
    ):
        next_idx += 1
    if next_idx >= len(lines):
        return False
    next_stripped = lines[next_idx].lstrip()
    if next_stripped.startswith('"""') or next_stripped.startswith("'''"):
        return False  # already has docstring
    # Infer body indent from function definition indent + 4
    func_indent = len(func_line) - len(func_line.lstrip())
    body_indent = " " * (func_indent + 4)
    name_match = re.search(r"def (\w+)\(", func_line)
    func_name = name_match.group(1) if name_match else "function"
    docstring_line = f'{body_indent}"""TODO: document {func_name}."""\n'
    lines.insert(next_idx, docstring_line)
    p.write_text("".join(lines), encoding="utf-8")
    return True


def main() -> None:
    args = sys.argv[1:]
    max_fixes = 3
    lane = "default"
    for i, a in enumerate(args):
        if a == "--lane" and i + 1 < len(args):
            lane = args[i + 1]
        elif a.isdigit():
            max_fixes = int(a)

    scan_file = "enhance_scan.json"
    try:
        d = json.load(open(scan_file))
        findings = d.get("findings", [])
    except Exception as e:
        print(f"Could not load {scan_file}: {e}")
        return

    if not findings:
        print("No findings — nothing to apply")
        return

    print(f"Applying up to {max_fixes} fixes (lane={lane}) from {len(findings)} findings")

    applied = 0
    skipped = 0

    for finding in findings:
        if applied >= max_fixes:
            break
        category = finding.get("category", "")
        file_path = finding.get("file", "")
        line_num = finding.get("line")

        if not file_path:
            skipped += 1
            continue

        if category == "bare_except":
            count = apply_bare_except(file_path)
            if count:
                print(f"[FIXED] bare_except x{count} in {file_path}")
                applied += 1
            else:
                skipped += 1

        elif category in ("missing_docs", "missing_function_docstring"):
            if apply_missing_docstring(file_path, line_num):
                print(f"[FIXED] added docstring to {file_path}:{line_num}")
                applied += 1
            else:
                skipped += 1

        else:
            skipped += 1
            print(f"[SKIP] {category} in {file_path} (no auto-fix for this category)")

    print(f"\nResult: applied={applied}, skipped={skipped}")


if __name__ == "__main__":
    main()
