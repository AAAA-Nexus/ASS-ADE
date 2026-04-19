# Extracted from C:/!ass-ade/src/ass_ade/cli.py:5063
# Component id: at.source.ass_ade.rebuild_codebase
from __future__ import annotations

__version__ = "0.1.0"

def rebuild_codebase(
    paths: List[Path] = typer.Argument(
        ...,
        help=(
            "One or more source directories to rebuild. When multiple paths are given "
            "their symbol pools are merged into one unified output (newer sources win on conflicts)."
        ),
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output directory. Required when merging multiple sources. "
             "Omit for single-source to auto-name: {source}-v{version}-{timestamp}.",
    ),
    premium: bool = typer.Option(False, help="Enable synthesis of missing blueprint components via AAAA-Nexus. Paid."),
    no_certify: bool = typer.Option(False, "--no-certify", help="Skip automatic certify step after rebuild."),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview tier plan without writing any files."),
    backup: bool = typer.Option(
        True,
        "--backup/--no-backup",
        help="Back up an existing output folder before replacing or updating it.",
    ),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt (auto-confirm)."),
    json_out: bool = typer.Option(False, "--json", help="Print result as JSON."),
    incremental: bool = typer.Option(
        False, "--incremental",
        help="Only re-process files changed since last MANIFEST.json. Skip unchanged files.",
    ),
    git_track: bool = typer.Option(
        False,
        "--git-track/--no-git-track",
        help="After a successful rebuild, stage all output files, commit, and create a tag in the output git repo.",
    ),
) -> None:
    """Rebuild any codebase into a clean tier-partitioned modular folder.

    Single-source rebuild (first time):

        ass-ade rebuild ./messy-repo --output ./clean-repo

    Merge-rebuild (multiple sources into one unified output):

        ass-ade rebuild ./source-a ./source-b ./source-c --output ./unified --yes

    Dry-run preview (no writes):

        ass-ade rebuild ./messy-repo --output ./clean-repo --dry-run

    Incremental (only changed files):

        ass-ade rebuild ./clean-repo --incremental

    ASS-ADE's heavy-hitter: point it at a spaghetti codebase, get a brand-new
    folder organized by the 5-tier monadic composition law (a0_qk_constants,
    a1_at_functions, a2_mo_composites, a3_og_features,
    a4_sy_orchestration). Every symbol classified, every gap proposed, every
    draft materialized as an ASSADE-SPEC-003 component artifact.

    Self-contained — no external ecosystem dependency required.
    """
    import time as _time
    import json as _json
    import shutil as _shutil

    from ass_ade.engine.rebuild.orchestrator import rebuild_project as _rebuild_project
    from ass_ade.engine.rebuild.orchestrator import render_rebuild_summary as _render_summary
    from ass_ade.engine.rebuild.project_parser import ingest_project as _ingest_project
    from ass_ade.engine.rebuild.project_parser import iter_source_files as _iter_source_files

    # Backward compatibility: older CLI usage accepted
    # ``ass-ade rebuild <source> <output>`` before multi-source rebuilds moved
    # output to ``--output``. Keep that form working when the second positional
    # path is absent or does not look like another source tree.
    if output is None and len(paths) == 2:
        legacy_source, legacy_output = paths
        legacy_output_resolved = legacy_output.resolve()
        second_path_is_output = not legacy_output_resolved.exists()
        if legacy_output_resolved.exists() and legacy_output_resolved.is_dir():
            second_path_is_output = not any(_iter_source_files(legacy_output_resolved))
        if second_path_is_output:
            output = legacy_output
            paths = [legacy_source]

    # ── Validate all source paths ─────────────────────────────────────────────
    if not paths:
        console.print("[red]At least one source directory is required.[/red]")
        raise typer.Exit(code=1)

    all_targets: list[Path] = []
    for _p in paths:
        _t = _p.resolve()
        if not _t.exists():
            console.print(f"[red]Source directory does not exist:[/red] {_t}")
            raise typer.Exit(code=1)
        if not _t.is_dir():
            console.print(f"[red]Source path is not a directory:[/red] {_t}")
            raise typer.Exit(code=1)
        try:
            next(_t.iterdir(), None)
        except (PermissionError, OSError) as _e:
            console.print(f"[red]Source directory is not readable:[/red] {_t}\n{_e}")
            raise typer.Exit(code=1)
        all_targets.append(_t)

    # Primary target for backward-compat single-source operations
    target = all_targets[0]
    _multi_source = len(all_targets) > 1

    if _multi_source and output is None:
        console.print(
            "[red]--output is required when merging multiple source directories.[/red]\n"
            "  Example: ass-ade rebuild src1 src2 src3 --output ./unified"
        )
        raise typer.Exit(code=1)

    dest = output.resolve() if output else target
    in_place = output is None
    # When output is omitted, dest will be replaced with a versioned sibling after the rebuild completes.
    _auto_versioned_dest = in_place

    if output and not dest.parent.exists():
        console.print(f"[red]Output parent directory does not exist:[/red] {dest.parent}")
        raise typer.Exit(code=1)
    if output and dest.parent.exists():
        import os as _os
        if not _os.access(dest.parent, _os.W_OK):
            console.print(f"[red]Output directory is not writable:[/red] {dest.parent}")
            raise typer.Exit(code=1)

    _first_rebuild = not (dest / "MANIFEST.json").exists()

    # ── Incremental: find changed files since last MANIFEST.json ─────────────
    changed_files: set[str] | None = None
    if incremental:
        manifest_path = dest / "MANIFEST.json"
        if manifest_path.exists():
            try:
                manifest = _json.loads(manifest_path.read_text(encoding="utf-8"))
                file_mtimes: dict[str, float] = manifest.get("file_mtimes", {})
                changed_files = set()
                for f in _iter_source_files(target):
                    rel = str(f.relative_to(target))
                    saved_mtime = file_mtimes.get(rel, 0)
                    current_mtime = f.stat().st_mtime
                    if current_mtime > saved_mtime:
                        changed_files.add(rel)
                if not json_out:
                    console.print(f"[dim]Incremental: {len(changed_files)} changed file(s) of "
                                  f"{sum(1 for _ in _iter_source_files(target))} total[/dim]")
            except Exception as _inc_exc:
                if not json_out:
                    console.print(f"[dim]Incremental check failed ({_inc_exc}) — running full rebuild[/dim]")
                changed_files = None
        else:
            if not json_out:
                console.print("[dim]No MANIFEST.json found — running full rebuild[/dim]")

    # ── Preview ingest: classify files into tiers for dry-run display ─────────
    _t0_ingest = _time.monotonic()
    _ingest_progress_state: list[int] = [0, 0]

    def _progress_cb(current: int, total: int) -> None:
        _ingest_progress_state[0] = current
        _ingest_progress_state[1] = total
        if not json_out:
            _draw_progress_bar("Ingest", current, total, _t0_ingest)

    if not json_out:
        _src_label_preview = (
            " + ".join(str(t) for t in all_targets)
            if _multi_source else str(target)
        )
        console.print(f"[dim]Analysing {_src_label_preview} …[/dim]")

    # For preview ingest, run on all sources and merge the summaries
    _all_preview_results = []
    for _pt in all_targets:
        _pr = _ingest_project(_pt, root_id=_pt.name, progress_callback=_progress_cb if _pt is target else None)
        _all_preview_results.append(_pr)

    if not json_out and _ingest_progress_state[1] > 0:
        _finish_progress_bar("Ingest", _ingest_progress_state[1],
                             _time.monotonic() - _t0_ingest)

    preview_result = _all_preview_results[0]
    by_tier: dict[str, int] = {}
    total_files_count = 0
    violation_count = 0
    for _pr in _all_preview_results:
        _s = _pr.get("summary", {})
        total_files_count += _s.get("files_scanned", 0)
        violation_count += len(_pr.get("gaps", []))
        for _tier, _cnt in _s.get("by_tier", {}).items():
            by_tier[_tier] = by_tier.get(_tier, 0) + _cnt
    est_seconds = max(5, total_files_count // 10)

    # ── Build tier preview lines (aligned) ───────────────────────────────────
    tier_order = [
        "a0_qk_constants", "a1_at_functions", "a2_mo_composites",
        "a3_og_features", "a4_sy_orchestration",
    ]
    _max_tier_len = max((len(t) for t in tier_order), default=20)
    tier_preview_lines = []
    for tier in tier_order:
        count = by_tier.get(tier, 0)
        if count > 0:
            tier_preview_lines.append(f"    {tier:<{_max_tier_len}}  {count:>5} files")
    for tier, count in sorted(by_tier.items()):
        if tier not in tier_order and count > 0:
            tier_preview_lines.append(f"    {tier:<{_max_tier_len}}  {count:>5} files")

    # Detect project language hint
    _lang_hints = [
        ("pyproject.toml", "Python"), ("package.json", "Node.js"),
        ("Cargo.toml", "Rust"), ("go.mod", "Go"),
    ]
    _lang = next((l for m, l in _lang_hints if (target / m).exists()), "")
    if _multi_source:
        _src_label = f"{len(all_targets)} sources merged ({total_files_count} total files)"
    else:
        _src_label = f"{target}" + (f" ({total_files_count} files, {_lang})" if _lang else f" ({total_files_count} files)")

    # Rich first-time plan vs. short follow-up diff preview
    if _first_rebuild and not dry_run:
        _src_lines = (
            "\n".join(f"            {t}" for t in all_targets) if _multi_source
            else f"  [dim]Source:[/dim]  {_src_label}"
        )
        preview_text = (
            "\n[bold]Merge-Rebuild Plan[/bold]\n" if _multi_source else "\n[bold]Rebuild Plan[/bold]\n"
        )
        if _multi_source:
            preview_text += f"  [dim]Sources ({len(all_targets)}):[/dim]\n{_src_lines}\n"
        else:
            preview_text += f"  [dim]Source:[/dim]  {_src_label}\n"
        preview_text += (
            f"  [dim]Output:[/dim]  {dest}\n\n"
            "  [bold]Tier Distribution:[/bold]\n"
            + "\n".join(tier_preview_lines or ["    (no source files classified)"])
            + f"\n\n  Gaps to fill:     {violation_count}"
            + f"\n  Estimated time:   ~{est_seconds}s"
        )
    else:
        preview_text = (
            "Dry-run preview:\n"
            + "\n".join(tier_preview_lines or ["  (no source files classified)"])
            + f"\n   {violation_count} gap(s) will be proposed as new components"
            + f"\n   Estimated time: ~{est_seconds}s"
        )

    if dry_run:
        if json_out:
            print(json.dumps({
                "dry_run": True,
                "source": str(target),
                "output": str(dest),
                "files_scanned": total_files_count,
                "by_tier": by_tier,
                "gaps": violation_count,
                "estimated_seconds": est_seconds,
            }, indent=2))
        else:
            console.print(preview_text)
        return

    # ── Confirmation prompt (unless --yes) ────────────────────────────────────
    if not yes and not json_out:
        console.print(preview_text)
        if _first_rebuild:
            # Three-option prompt for first-time rebuilds
            console.print("\n  [bold][P][/bold]roceed  [bold][E][/bold]dit plan  [bold][C][/bold]ancel\n")
            _choice = (typer.prompt("  Choice", default="P")).strip().upper()
            if _choice == "C":
                console.print("[dim]Rebuild cancelled.[/dim]")
                raise typer.Exit(code=0)
            if _choice == "E":
                _plan_path = target / ".ass-ade" / "rebuild-plan.json"
                _plan_path.parent.mkdir(parents=True, exist_ok=True)
                _plan_data = {
                    "source": str(target),
                    "output": str(dest),
                    "tier_distribution": by_tier,
                    "gaps": violation_count,
                    "estimated_seconds": est_seconds,
                }
                _plan_path.write_text(
                    json.dumps(_plan_data, indent=2), encoding="utf-8"
                )
                console.print(f"[dim]Plan saved to:[/dim] {_plan_path}")
                console.print("[dim]Edit the plan, then re-run with --yes to proceed.[/dim]")
                raise typer.Exit(code=0)
            # "P" or anything else → proceed
        else:
            confirm = typer.confirm("Proceed?", default=True)
            if not confirm:
                console.print("[dim]Rebuild cancelled.[/dim]")
                raise typer.Exit(code=0)

    # ── Recon before rebuild ──────────────────────────────────────────────────
    if not json_out:
        console.print(f"[dim]Running recon on {target} ...[/dim]")
    try:
        from ass_ade.recon import run_parallel_recon as _run_recon
        _recon_report = _run_recon(target)
        _recon_md = _recon_report.to_markdown()
        if not json_out:
            console.print(f"[dim]Recon: {_recon_report.scout['total_files']} files, "
                          f"depth {_recon_report.scout['max_depth']}, "
                          f"{_recon_report.test['test_functions']} tests, "
                          f"doc coverage {_recon_report.doc['doc_coverage']:.0%} "
                          f"({_recon_report.duration_ms:.0f} ms)[/dim]")
        if _recon_report.dependency["has_circular_deps"]:
            if not json_out:
                console.print(f"[yellow]Warning: circular imports detected — "
                              f"{_recon_report.dependency['circular_deps'][:2]}[/yellow]")
        _recon_out = target / "RECON_REPORT.md"
        try:
            _recon_out.write_text(_recon_md, encoding="utf-8")
        except OSError:
            pass
    except Exception as _recon_exc:
        if not json_out:
            console.print(f"[dim]Recon skipped: {_recon_exc}[/dim]")

    label = "Premium merge-rebuild" if (premium and _multi_source) else "Merge-rebuild" if _multi_source else ("Premium rebuild" if premium else "Rebuilding")
    if not json_out:
        if _multi_source:
            console.print(f"[bold]{label}[/bold] {len(all_targets)} sources → {dest}")
        else:
            console.print(f"[bold]{label}[/bold] {target}")
            if output:
                console.print(f"[dim]Output → {dest}[/dim]")
        console.print()

    staging_dir = dest.parent / f".{dest.name}_rebuild_staging"

    # ── Show phase progress during the rebuild ────────────────────────────────
    _rebuild_phases = ["Gap-fill", "Enrich", "Validate", "Materialize", "Audit", "Package"]
    _phase_total = len(_rebuild_phases) + 1  # +1 for ingest (already done)
    if not json_out:
        _draw_progress_bar("Rebuild", 1, _phase_total, _t0_ingest)

    _t0_rebuild = _time.monotonic()
    try:
        result = _rebuild_project(
            source_path=all_targets if _multi_source else target,
            output_dir=staging_dir,
            synthesize_gaps=premium,
        )
    except Exception as _exc:
        if json_out:
            print(json.dumps({"error": str(_exc), "source": str(target)}, indent=2))
        else:
            print(flush=True)
            console.print(f"[red]Rebuild failed:[/red] {_exc}")
        raise typer.Exit(code=1)

    if not json_out:
        _finish_progress_bar("Rebuild", _phase_total, _time.monotonic() - _t0_rebuild)

    phases = result.get("phases", {})
    mat = phases.get("materialize", {})
    rebuilt_root_str = mat.get("target_root", "")
    rebuilt_root = Path(rebuilt_root_str) if rebuilt_root_str else None

    if not rebuilt_root or not rebuilt_root.exists():
        if json_out:
            print(json.dumps({"error": "output folder not found", "source": str(target)}, indent=2))
        else:
            console.print("[yellow]Rebuild completed but output folder not found.[/yellow]")
        raise typer.Exit(code=1)

    # ── Auto-versioned output folder name ────────────────────────────────────
    # When user omits the output argument, produce a versioned sibling folder:
    #   {source_name}-v{version}-{timestamp}  (e.g. myapp-v0.1.0-20260418-174111)
    if _auto_versioned_dest:
        _rebuild_tag = mat.get("rebuild_tag", "")
        _project_version = "0.1.0"
        _version_file = rebuilt_root / "VERSION"
        if _version_file.exists():
            try:
                _project_version = _version_file.read_text(encoding="utf-8").splitlines()[0].strip()
            except Exception:
                pass
        _ts_part = _rebuild_tag.replace("_", "-") if _rebuild_tag else ""
        _versioned_name = (
            f"{target.name}-v{_project_version}-{_ts_part}"
            if _ts_part
            else f"{target.name}-v{_project_version}"
        )
        dest = target.parent / _versioned_name
        in_place = False  # treat as a new output folder now that we have a concrete name
        if not json_out:
            console.print(f"[dim]Auto-versioned output → {dest.name}[/dim]")

    _output_backup_path: Path | None = None
    if backup and dest.exists():
        _backup_ts = _time.strftime("%Y%m%d-%H%M%S")
        _output_backup_path = dest.parent / f"{dest.name}-backup-{_backup_ts}"
        _backup_suffix = 0
        while _output_backup_path.exists():
            _backup_suffix += 1
            _output_backup_path = dest.parent / f"{dest.name}-backup-{_backup_ts}-{_backup_suffix}"
        try:
            _shutil.copytree(str(dest), str(_output_backup_path), dirs_exist_ok=False)
            if not json_out:
                console.print(f"[green][OK][/green] Output backup -> {_output_backup_path}")
        except OSError as _backup_exc:
            if json_out:
                print(json.dumps({
                    "error": f"output backup failed: {_backup_exc}",
                    "source": str(target),
                    "output": str(dest),
                }, indent=2))
            else:
                console.print(f"[red]Output backup failed:[/red] {_backup_exc}")
            raise typer.Exit(code=1) from _backup_exc

    # ── Snapshot old component count for incremental diff ────────────────────
    old_count = 0
    if in_place or incremental:
        old_manifest = dest / "MANIFEST.json"
        if old_manifest.exists():
            try:
                old_count = _json.loads(old_manifest.read_text(encoding="utf-8")).get("counts", {}).get("total", 0)
            except Exception:
                pass

    # Preserve BIRTH_CERTIFICATE.md across rebuilds — it is the permanent origin record.
    _birth_cert_content: str | None = None
    _birth_cert_path = dest / "BIRTH_CERTIFICATE.md"
    if _birth_cert_path.exists():
        try:
            _birth_cert_content = _birth_cert_path.read_text(encoding="utf-8")
        except OSError:
            pass
    # Preserve README.md across rebuilds so generated docs do not overwrite the
    # showcase README when a rebuild is promoted into an existing output.
    _readme_content: bytes | None = None
    _readme_path = dest / "README.md"
    if _readme_path.exists():
        try:
            _readme_content = _readme_path.read_bytes()
        except OSError:
            pass
    _env_handoff_path: str | None = None
    _env_handoff_error: str | None = None

    if not in_place:
        _shutil.rmtree(dest, ignore_errors=True)
    _shutil.copytree(str(rebuilt_root), str(dest), dirs_exist_ok=True)

    def _rebase_rebuild_metadata(final_root: Path, staged_root: Path) -> None:
        staged_prefix = staged_root.as_posix()
        final_prefix = final_root.as_posix()

        def _rebase_value(value: Any) -> Any:
            if isinstance(value, str) and value.startswith(staged_prefix):
                return final_prefix + value[len(staged_prefix):]
            if isinstance(value, list):
                return [_rebase_value(item) for item in value]
            if isinstance(value, dict):
                return {key: _rebase_value(item) for key, item in value.items()}
            return value

        manifest_path = final_root / "MANIFEST.json"
        if manifest_path.exists():
            try:
                manifest = _json.loads(manifest_path.read_text(encoding="utf-8"))
                manifest = _rebase_value(manifest)
                manifest_path.write_text(_json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            except Exception:
                pass

        cert_path = final_root / "CERTIFICATE.json"
        if cert_path.exists():
            try:
                cert = _json.loads(cert_path.read_text(encoding="utf-8"))
                cert = _rebase_value(cert)
                cert["target_root"] = final_prefix
                cert.pop("certificate_sha256", None)
                blob = _json.dumps(cert, sort_keys=True).encode("utf-8")
                cert["certificate_sha256"] = hashlib.sha256(blob).hexdigest()
                cert_path.write_text(_json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
                phases.setdefault("certificate", {})["certificate_sha256"] = cert["certificate_sha256"]
                phases["certificate"]["certificate_path"] = cert_path.as_posix()
            except Exception:
                pass

    _rebase_rebuild_metadata(dest, rebuilt_root)

    if _birth_cert_content is not None:
        try:
            (dest / "BIRTH_CERTIFICATE.md").write_text(_birth_cert_content, encoding="utf-8")
        except OSError:
            pass
    if _readme_content is not None:
        try:
            (dest / "README.md").write_bytes(_readme_content)
        except OSError:
            pass

    # Local handoff: let users move into the rebuilt folder without retyping
    # credentials, while .gitignore keeps the file out of public artifacts.
    _env_source = target / ".env"
    _env_dest = dest / ".env"
    if _env_source.exists() and _env_source.is_file():
        try:
            if _env_source.resolve() != _env_dest.resolve():
                _shutil.copy2(str(_env_source), str(_env_dest))
            _env_handoff_path = str(_env_dest)
        except OSError as _env_exc:
            _env_handoff_error = str(_env_exc)

    # ── Save file mtimes for future incremental runs ──────────────────────────
    try:
        existing_manifest_path = dest / "MANIFEST.json"
        existing_manifest: dict = {}
        if existing_manifest_path.exists():
            existing_manifest = _json.loads(existing_manifest_path.read_text(encoding="utf-8"))
        file_mtimes_snapshot: dict[str, float] = {}
        for _st in all_targets:
            for f in _iter_source_files(_st):
                _rel_key = f"{_st.name}/{f.relative_to(_st)}" if _multi_source else str(f.relative_to(_st))
                file_mtimes_snapshot[_rel_key] = f.stat().st_mtime
        existing_manifest["file_mtimes"] = file_mtimes_snapshot
        existing_manifest_path.write_text(
            _json.dumps(existing_manifest, indent=2), encoding="utf-8"
        )
    except Exception:
        pass

    new_count = mat.get("written_count", 0)
    mode_label = "Incremental update" if (in_place or incremental) else "Rebuilt"

    cert = phases.get("certificate", {})

    if not json_out:
        console.print(f"\n[green][OK][/green] {mode_label} → [bold]{dest}[/bold]")
        if _env_handoff_path:
            console.print(f"[green][OK][/green] Local .env copied -> {dest / '.env'}")
        elif _env_handoff_error:
            console.print(f"[yellow].env handoff skipped:[/yellow] {_env_handoff_error[:160]}")

    if (in_place or incremental) and not json_out:
        delta = new_count - old_count
        if delta > 0:
            console.print(f"[green]+{delta} new components[/green] ({old_count} → {new_count})")
        elif delta < 0:
            console.print(f"[yellow]{delta} components removed[/yellow] ({old_count} → {new_count})")
        else:
            console.print(f"[dim]No component count change ({new_count} components)[/dim]")

    if not json_out:
        console.print()
        for line in _render_summary(result).splitlines():
            console.print(f"[dim]{line}[/dim]")

    if not json_out:
        console.print("[dim]Generating documentation suite…[/dim]")
    _recon_stats: "dict | None" = None
    try:
        _rr = _recon_report  # type: ignore[name-defined]
        _recon_stats = {
            "test_functions": _rr.test.get("test_functions", 0),
            "doc_coverage": _rr.doc.get("doc_coverage", 0.0),
        }
    except Exception:
        pass
    _generate_rebuild_docs(
        dest,
        target,
        recon_data=_recon_stats,
        preserve_readme=_readme_content is not None,
    )
    if not json_out:
        console.print("[green][OK][/green] Docs generated.")

    if not no_certify and not cert.get("certificate_sha256"):
        import subprocess as _sp
        rc_cert = _sp.call(
            [sys.executable, "-m", "ass_ade", "certify", str(dest)],
            env=os.environ.copy(),
        )
        cert_ok = rc_cert == 0
        if not json_out:
            if cert_ok:
                console.print("[green][OK][/green] Certified — CERTIFICATE.json written.")
            else:
                console.print("[yellow]Auto-certify failed — run 'ass-ade certify' manually.[/yellow]")
    else:
        cert_ok = bool(cert.get("certificate_sha256"))
        if cert_ok and not json_out:
            console.print("[green][OK][/green] Certified — CERTIFICATE.json written.")

    # ── Git tracking ─────────────────────────────────────────────────────────
    _git_commit_hash: str | None = None
    _git_tag_name: str | None = None
    if git_track:
        import subprocess as _git_sp
        _gt_tag = mat.get("rebuild_tag", "unknown")
        _gt_components = new_count
        _gt_pass_rate = phases.get("audit", {}).get("pass_rate", 0.0)
        _gt_pass_pct = f"{_gt_pass_rate * 100:.1f}"
        _gt_commit_msg = (
            f"evolution: rebuild {_gt_tag} — "
            f"{_gt_components} components, {_gt_pass_pct}% conformant"
        )
        _gt_tag_name = f"rebuild/{_gt_tag}"
        _gt_tag_msg = f"ASS-ADE rebuild {_gt_tag}"
        try:
            # Verify the output is inside a git repo
            _git_check = _git_sp.run(
                ["git", "-C", str(dest), "rev-parse", "--git-dir"],
                capture_output=True, text=True, timeout=10,
            )
            if _git_check.returncode == 0:
                # Stage all files in the output directory
                _git_sp.run(
                    ["git", "-C", str(dest), "add", "-A"],
                    capture_output=True, text=True, timeout=30, check=True,
                )
                # Commit
                _commit_result = _git_sp.run(
                    ["git", "-C", str(dest), "commit", "-m", _gt_commit_msg],
                    capture_output=True, text=True, timeout=30,
                )
                if _commit_result.returncode == 0:
                    _git_commit_hash = _commit_result.stdout.strip().splitlines()[0] if _commit_result.stdout else None
                    # Annotated tag
                    _git_sp.run(
                        ["git", "-C", str(dest), "tag", "-a", _gt_tag_name, "-m", _gt_tag_msg],
                        capture_output=True, text=True, timeout=15,
                    )
                    _git_tag_name = _gt_tag_name
                    if not json_out:
                        console.print(f"[green][OK][/green] Git commit: {_git_commit_hash}")
                        console.print(f"[green][OK][/green] Git tag: {_gt_tag_name}")
                elif "nothing to commit" in (_commit_result.stdout + _commit_result.stderr):
                    if not json_out:
                        console.print("[dim]Git: nothing new to commit.[/dim]")
                else:
                    if not json_out:
                        console.print(f"[yellow]Git commit failed: {_commit_result.stderr.strip()[:120]}[/yellow]")
            else:
                if not json_out:
                    console.print(f"[dim]--git-track: {dest} is not inside a git repo — skipping.[/dim]")
        except Exception as _git_exc:
            if not json_out:
                console.print(f"[dim]--git-track error (rebuild not affected): {_git_exc}[/dim]")

    # ── JSON output ───────────────────────────────────────────────────────────
    if json_out:
        print(json.dumps({
            "ok": True,
            "mode": mode_label.lower().replace(" ", "_"),
            "source": str(target),
            "output": str(dest),
            "files_scanned": total_files_count,
            "components_written": new_count,
            "by_tier": by_tier,
            "gaps": violation_count,
            "certified": cert_ok,
            "incremental_files_skipped": (
                (total_files_count - len(changed_files))
                if changed_files is not None else 0
            ),
            "git_commit": _git_commit_hash,
            "git_tag": _git_tag_name,
            "env_handoff": _env_handoff_path,
            "env_handoff_error": _env_handoff_error,
            "output_backup": str(_output_backup_path) if _output_backup_path else None,
        }, indent=2))

    # ── Clean up staging area ─────────────────────────────────────────────────
    try:
        _shutil.rmtree(str(staging_dir), ignore_errors=True)
    except Exception:
        pass
