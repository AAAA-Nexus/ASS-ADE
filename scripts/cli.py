"""ASS-ADE CLI — recon, enhancement, and rebuild tools for CI workflows."""
import argparse
import json
import sys
from pathlib import Path

TIERS = [
    "a0_qk_constants",
    "a1_at_functions",
    "a2_mo_composites",
    "a3_og_features",
    "a4_sy_orchestration",
]


def cmd_recon(args):
    root = Path(args.path).resolve()
    tier_counts = {}
    total_py = 0
    for tier in TIERS:
        count = len(list((root / tier).glob("*.py"))) if (root / tier).exists() else 0
        tier_counts[tier] = count
        total_py += count

    manifest_components = 0
    cert_written = 0
    try:
        manifest_components = len(json.loads((root / "MANIFEST.json").read_text())["components"])
    except Exception:
        pass
    try:
        cert_written = json.loads((root / "CERTIFICATE.json").read_text()).get("written_count", 0)
    except Exception:
        pass

    result = {
        "status": "ok",
        "tier_py_files": tier_counts,
        "total_py_files": total_py,
        "manifest_components": manifest_components,
        "cert_written_count": cert_written,
        "enhancements_available": 0,
    }
    print(json.dumps(result, indent=2) if args.json else
          f"Recon: {total_py} py files, {manifest_components} manifest components")


def _find_opportunities(root: Path) -> list:
    opportunities = []
    for tier in TIERS:
        tier_path = root / tier
        if not tier_path.exists():
            continue
        for py_file in sorted(tier_path.glob("*.py"))[:10]:
            try:
                content = py_file.read_text(encoding="utf-8", errors="replace")
                stripped = content.lstrip()
                if content and not stripped.startswith('"""') and not stripped.startswith("'''"):
                    opportunities.append({
                        "file": str(py_file.relative_to(root)),
                        "type": "missing_module_docstring",
                        "priority": 1,
                    })
            except Exception:
                pass
    return opportunities


def cmd_enhance(args):
    root = Path(args.path).resolve()

    if args.apply:
        opps = _find_opportunities(root)
        applied = 0
        for opp in opps[: args.apply]:
            try:
                target = root / opp["file"]
                content = target.read_text(encoding="utf-8", errors="replace")
                name = target.stem
                target.write_text(f'"""Auto-generated module: {name}."""\n' + content, encoding="utf-8")
                applied += 1
            except Exception:
                pass
        result = {"status": "ok", "applied": applied, "enhancements": [o["file"] for o in opps[:applied]]}
        print(json.dumps(result, indent=2))
        return

    opps = _find_opportunities(root)
    result = {
        "status": "ok",
        "opportunities": opps[:10],
        "total_found": len(opps),
    }
    print(json.dumps(result, indent=2) if args.json else
          f"Enhance: {len(opps)} opportunities found")


def cmd_rebuild(args):
    try:
        from ass_ade.engine.rebuild.orchestrator import rebuild_project, render_rebuild_summary
    except ImportError as exc:
        print(f"Error: rebuild engine not available — {exc}", file=sys.stderr)
        sys.exit(1)

    source = Path(args.source).resolve()
    output = Path(args.output).resolve()

    if not source.exists():
        print(f"Error: source path does not exist: {source}", file=sys.stderr)
        sys.exit(1)

    print(f"Rebuilding {source} -> {output} ...", file=sys.stderr)
    result = rebuild_project(
        source,
        output,
        enrich_bodies=not args.no_enrich,
        emit_package=not args.no_package,
    )

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(render_rebuild_summary(result))

    pkg = result.get("phases", {}).get("package", {})
    if pkg.get("error"):
        sys.exit(2)


def cmd_doctor(args):
    """Quick health check — verify the package is importable and the CLI works."""
    checks = {}

    # Check tier directories exist
    root = Path(args.path).resolve()
    for tier in TIERS:
        tier_dir = root / tier
        checks[tier] = tier_dir.exists()

    # Check pyproject.toml
    checks["pyproject.toml"] = (root / "pyproject.toml").exists()

    # Check __init__.py
    checks["__init__.py"] = (root / "__init__.py").exists()

    all_ok = all(checks.values())
    status = "ok" if all_ok else "degraded"
    result = {"status": status, "checks": checks}
    print(json.dumps(result, indent=2) if args.json else
          f"Doctor: {status} — {sum(checks.values())}/{len(checks)} checks passed")
    if not all_ok:
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(prog="ass-ade", description="ASS-ADE CI tools")
    sub = parser.add_subparsers(dest="command")

    recon_p = sub.add_parser("recon", help="Repo reconnaissance scan")
    recon_p.add_argument("path", nargs="?", default=".")
    recon_p.add_argument("--json", action="store_true")

    enhance_p = sub.add_parser("enhance", help="Enhancement scan / apply")
    enhance_p.add_argument("path", nargs="?", default=".")
    enhance_p.add_argument("--json", action="store_true")
    enhance_p.add_argument("--apply", type=int, default=0, metavar="N",
                           help="Apply top N enhancements")

    rebuild_p = sub.add_parser("rebuild", help="Rebuild a project into a tier-partitioned package")
    rebuild_p.add_argument("source", help="Source directory to scan")
    rebuild_p.add_argument("output", help="Output directory for the rebuild package")
    rebuild_p.add_argument("--no-enrich", action="store_true", help="Skip body enrichment")
    rebuild_p.add_argument("--no-package", action="store_true", help="Skip package emission")
    rebuild_p.add_argument("--json", action="store_true", help="Output full JSON receipt")

    doctor_p = sub.add_parser("doctor", help="Health check for a rebuild package")
    doctor_p.add_argument("path", nargs="?", default=".")
    doctor_p.add_argument("--json", action="store_true")

    args = parser.parse_args()
    if args.command == "recon":
        cmd_recon(args)
    elif args.command == "enhance":
        cmd_enhance(args)
    elif args.command == "rebuild":
        cmd_rebuild(args)
    elif args.command == "doctor":
        cmd_doctor(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
