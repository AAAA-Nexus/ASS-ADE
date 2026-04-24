"""Tier a1 — assimilated function 'materialize_plan'

Assimilated from: rebuild/schema_materializer.py:622-1046
"""

from __future__ import annotations


# --- assimilated symbol ---
def materialize_plan(
    plan: dict[str, Any],
    *,
    out_dir: Path,
    rebuild_tag: str | None = None,
    prev_manifest_path: Path | None = None,
    registry_candidates: list[Atom] | None = None,
    allowed_source_root: Path | str | None = None,
    provenance_meta: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Write each source module (whole file) to its dominant tier directory.

    Instead of extracting individual function bodies into separate files
    (which strips imports and class context), we copy the WHOLE source file
    to the appropriate tier folder.  Multiple components from the same source
    file are deduplicated: the file is written once to the tier where most of
    its symbols land.

    JSON component-spec artifacts are still written per component for metadata
    and audit purposes.

    Args:
        plan:               Gap-fill plan from ``gap_filler.build_gap_fill_plan``.
        out_dir:            Parent directory for the timestamped rebuild folder.
        rebuild_tag:        Optional timestamp tag; auto-generated when omitted.
        prev_manifest_path: MANIFEST.json from a previous build for version continuity.
        allowed_source_root: If set, every non-empty ``source_symbol.path`` on
            proposals must resolve under this directory (MAP = TERRAIN: no
            mixed-tree materialization for single-root rebuilds). Typically the
            sole ingest path from ``rebuild_project``.
        provenance_meta:    Extra fields persisted to ``PROVENANCE.json`` next
            to the manifest (declared input paths, single-root policy, etc.).
    """
    tag = rebuild_tag or dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    target_root = out_dir / tag
    _assert_under_root(target_root, out_dir)
    target_root.mkdir(parents=True, exist_ok=True)

    if allowed_source_root is not None:
        allowed_root = Path(allowed_source_root).resolve()
        assert_proposals_under_source_root(plan, allowed_root)
        for proposal in plan.get("proposed_components") or []:
            src_sym = proposal.get("source_symbol") or {}
            raw = (src_sym.get("path") or "").strip()
            if not raw:
                continue
            src_sym = dict(src_sym)
            src_sym["path"] = str(_resolve_source_symbol_path(raw, allowed_root))
            proposal["source_symbol"] = src_sym

    resolve_plan_canonical_names(
        plan.get("proposed_components") or [],
        registry_candidates=registry_candidates,
    )

    prev_versions = load_prev_versions(prev_manifest_path)

    # ── Step 0: Determine dominant tier per source file ───────────────────────
    # Count how many components from each source file land in each tier.
    # The file goes to the tier that claims the most of its symbols.
    file_tier_votes: dict[str, dict[str, int]] = {}
    for proposal in plan.get("proposed_components") or []:
        src_sym = proposal.get("source_symbol") or {}
        src_path = src_sym.get("path") or ""
        if src_path:
            tier = proposal.get("tier") or "a1_at_functions"
            votes = file_tier_votes.setdefault(src_path, {})
            votes[tier] = votes.get(tier, 0) + 1

    file_to_tier: dict[str, str] = {
        src: _dominant_tier(votes)
        for src, votes in file_tier_votes.items()
        if votes
    }

    # ── Step 0b: Pick canonical (CNA-style) filename per source file ──────────
    # The destination filename is derived from the dominant proposal's
    # canonical id (e.g. "at.source.aaaa-nexus.sha256_hex") so every output
    # file is a swappable, registry-addressable atom — not a copy of the
    # original source filename. This is the naming convention from the
    # ASS-CLAW master plan (`a1.crypto.hash.sha256_hex.py`-style).
    file_canonical_name: dict[str, str] = {}
    file_proposal_counts: dict[str, dict[str, int]] = {}
    for proposal in plan.get("proposed_components") or []:
        src_sym = proposal.get("source_symbol") or {}
        src_path = src_sym.get("path") or ""
        if not src_path:
            continue
        cid = proposal.get("id") or ""
        if not cid:
            continue
        counts = file_proposal_counts.setdefault(src_path, {})
        counts[cid] = counts.get(cid, 0) + 1
    for src_path_str, id_counts in file_proposal_counts.items():
        # Most-common canonical id wins; ties broken alphabetically for determinism.
        winner = sorted(id_counts.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
        # Resolve the winner through CNA via its proposal so the archived
        # source module shares the canonical name of its dominant atom.
        winner_proposal = next(
            (p for p in (plan.get("proposed_components") or [])
             if (p.get("canonical_name") or p.get("id")) == winner),
            None,
        )
        if winner_proposal:
            winner_canonical = winner_proposal.get("canonical_name") or canonical_name_for(
                winner_proposal,
                fallback_tier=winner_proposal.get("tier") or "a1_at_functions",
                registry_candidates=registry_candidates,
            )
            file_canonical_name[src_path_str] = filename_stem_for(winner_canonical)
        else:
            file_canonical_name[src_path_str] = _slug(winner)

    # ── Step 1: Copy whole source modules (one per source file) ───────────────
    # Each unique source file is written exactly once to its dominant tier dir
    # under its canonical name (CNA convention). Conflicts get a numeric suffix.
    written_modules: dict[str, str] = {}  # source_path_str → written dest path
    # Source modules are archived outside the canonical tier dirs so they
    # never collide with per-atom .py files. Tier dirs hold ONLY canonical
    # atoms (one .py + one .json per id). Whole-file references live here:
    sources_root = target_root / "_source_modules"
    for src_path_str, tier in sorted(file_to_tier.items()):
        src_path = Path(src_path_str)
        if not src_path.exists():
            continue
        archive_dir = sources_root / tier
        archive_dir.mkdir(parents=True, exist_ok=True)

        canonical_stem = file_canonical_name.get(src_path_str) or src_path.stem
        dest_name = f"{canonical_stem}{src_path.suffix}"
        dest_file = archive_dir / dest_name
        # Resolve name conflicts with a numeric suffix (e.g. ...__2.py).
        counter = 1
        while dest_file.exists():
            dest_file = archive_dir / f"{canonical_stem}__{counter}{src_path.suffix}"
            counter += 1

        _assert_under_root(dest_file, out_dir)
        try:
            content = src_path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        dest_file.write_text(content, encoding="utf-8")
        written_modules[src_path_str] = dest_file.as_posix()

    # ── Step 2: Per-atom emission — one .py + one .json sidecar per canonical id ─
    # Every atom gets a canonical-stem filename derived from its dotted id
    # (e.g. `at.crypto.sha256_hex` → `crypto_sha256_hex.py` + `.json`).
    # No `_draft_` prefixes, no `source_*` prefixes — same id → same filename
    # everywhere → true swappable lego pieces.
    #
    # Body emission rules:
    #   - If the atom came from a real source file we copied in Step 1, its
    #     .py is that copied module (sibling). The JSON sidecar's `body_path`
    #     points there; many atoms share one .py.
    #   - If the atom is synthetic / draft (no copied source), we extract its
    #     embedded body string into its own `<stem>.py` file. No stubs.
    #
    # JSON sidecars are slim: metadata + `body_path`. The body lives in .py.
    written: list[dict[str, Any]] = []
    by_tier: dict[str, int] = {}
    tier_module_versions: dict[str, list[dict[str, Any]]] = {}
    seen_canonical: dict[str, dict[str, str]] = {}  # cid -> {py_rel, json_rel, tier}
    # Semantic dedupe: same body_hash → same atom, no matter what 5 different
    # repos called the function. The first canonical id to claim a body wins;
    # later duplicates collapse onto it (their fulfills_blueprints + aliases
    # get merged into the canonical entry). This is what makes a 2 M-line
    # codebase shrink: identical implementations stop being rewritten.
    seen_body_hash: dict[str, str] = {}  # body_hash -> canonical cid that owns it

    for proposal in plan.get("proposed_components") or []:
        tier = proposal.get("tier") or "a1_at_functions"
        tier_dir = target_root / tier
        tier_dir.mkdir(parents=True, exist_ok=True)

        # ── Canonical name via CNA — single source of truth ────────────────
        # Same intent + signature + language → same name, regardless of what
        # the original repo called the function. This is the entire reason
        # 5 repos with `sha256Hex`, `compute_sha256`, `hash_sha` collapse to
        # one `a1.crypto.hash.sha256_hex` atom.
        canonical = proposal.get("canonical_name") or canonical_name_for(
            proposal,
            fallback_tier=tier,
            registry_candidates=registry_candidates,
        )
        artifact = _make_component_artifact(proposal)
        artifact["id"] = canonical
        cid = canonical
        body = proposal.get("body") or ""
        src_sym = proposal.get("source_symbol") or {}
        lang = (src_sym.get("language") or "python").lower()

        # Dedupe: same canonical id only emitted once. Subsequent duplicates
        # reuse the first emission's paths (their fulfills_blueprints get
        # appended to the manifest entry below).
        if cid in seen_canonical:
            for w in written:
                if w["id"] == cid:
                    for fb in artifact["fulfills_blueprints"]:
                        if fb not in w["fulfills_blueprints"]:
                            w["fulfills_blueprints"].append(fb)
                    break
            continue

        stem = filename_stem_for(cid)

        # ── Body file: ALWAYS one .py per canonical atom (true swappability) ──
        # Prefer the proposal's body. If empty, try to slice the symbol's
        # line range out of the original source. Never share .py across atoms.
        src_path_str = src_sym.get("path") or ""
        if not body and src_path_str:
            try:
                src_text = Path(src_path_str).read_text(encoding="utf-8", errors="replace")
                lo = src_sym.get("line_start") or src_sym.get("start_line")
                hi = src_sym.get("line_end") or src_sym.get("end_line")
                if lo and hi and hi >= lo:
                    body = "".join(src_text.splitlines(keepends=True)[lo - 1 : hi])
            except OSError:
                body = ""

        # ── Semantic dedupe: identical bodies collapse to one atom ──────────
        # If we've already emitted this exact body under a different name,
        # the new id becomes an alias of the canonical one. No new files
        # written; the canonical atom records the alias. This is how the
        # rebuilder shrinks: 100 copy-pasted helpers across a repo collapse
        # to a single canonical atom that everyone imports.
        body_hash_now = content_hash(body) if body else ""
        if body_hash_now and body_hash_now in seen_body_hash:
            canonical_cid = seen_body_hash[body_hash_now]
            for w in written:
                if w["id"] == canonical_cid:
                    aliases = w.setdefault("aliases", [])
                    if cid not in aliases and cid != canonical_cid:
                        aliases.append(cid)
                    for fb in artifact["fulfills_blueprints"]:
                        if fb not in w["fulfills_blueprints"]:
                            w["fulfills_blueprints"].append(fb)
                    break
            seen_canonical[cid] = seen_canonical.get(canonical_cid, {})
            continue

        py_file = tier_dir / f"{stem}.py"
        counter = 1
        while py_file.exists():
            py_file = tier_dir / f"{stem}__{counter}.py"
            counter += 1
        _assert_under_root(py_file, out_dir)
        payload = _python_payload_for_body(
            cid=cid,
            lang=lang,
            source_path=src_path_str,
            body=body,
        )
        if not payload.endswith("\n"):
            payload += "\n"
        py_file.write_text(payload, encoding="utf-8")
        body_abs = py_file
        emitted_body_hash = content_hash(payload)

        body_rel = body_abs.relative_to(target_root).as_posix()

        # ── JSON sidecar: slim metadata, no embedded body ──
        json_file = tier_dir / f"{stem}.json"
        counter = 1
        while json_file.exists():
            json_file = tier_dir / f"{stem}__{counter}.json"
            counter += 1
        _assert_under_root(json_file, out_dir)

        version, change_type = assign_version(cid, body, lang, prev_versions)
        artifact["version"] = version
        artifact["body_hash"] = emitted_body_hash
        artifact["body_path"] = body_rel
        artifact.pop("body", None)  # body lives in .py now — no duplication
        if change_type == "major":
            artifact["compat_warning"] = "public API removed or renamed — review before shipping"

        json_file.write_text(
            json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )

        seen_canonical[cid] = {
            "py_rel": body_rel,
            "json_rel": json_file.relative_to(target_root).as_posix(),
            "tier": tier,
        }
        if artifact["body_hash"]:
            seen_body_hash.setdefault(artifact["body_hash"], cid)

        tier_module_versions.setdefault(tier, []).append({
            "id": cid,
            "name": artifact["name"],
            "version": version,
            "change_type": change_type,
        })

        written.append({
            "body_hash": artifact["body_hash"],
            "body_path": body_rel,
            "change_type": change_type,
            "fulfills_blueprints": artifact["fulfills_blueprints"],
            "id": cid,
            "kind": artifact["kind"],
            "name": artifact["name"],
            "path": json_file.as_posix(),
            "source_file": body_abs.as_posix(),
            "tier": tier,
            "version": version,
        })
        by_tier[tier] = by_tier.get(tier, 0) + 1

    # ── Step 3: Write per-tier VERSION.json ───────────────────────────────────
    tier_versions: dict[str, str] = {}
    for tier, modules in tier_module_versions.items():
        tier_dir = target_root / tier
        write_tier_version_file(tier_dir, tier, modules)
        tier_versions[tier] = _aggregate_version([m["version"] for m in modules])

    write_project_version_file(target_root, tier_versions, tag)

    manifest_path = target_root / "MANIFEST.json"
    _assert_under_root(manifest_path, out_dir)
    manifest = {
        "schema": COMPONENT_SCHEMA,
        "rebuild_tag": tag,
        "materialized_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "source_plan_digest": plan.get("content_digest"),
        "counts": {"total": len(written), "by_tier": by_tier},
        "tier_versions": tier_versions,
        "source_module_map": {k: v for k, v in written_modules.items()},
        "components": written,
    }
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    prov_path = target_root / "PROVENANCE.json"
    _assert_under_root(prov_path, out_dir)
    prov_body: dict[str, Any] = {
        "schema": "ASSADE-SPEC-PROVENANCE-1",
        "materialized_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "allowed_source_root": (
            str(Path(allowed_source_root).resolve())
            if allowed_source_root is not None
            else None
        ),
        "provenance": provenance_meta or {},
        "unique_source_modules_archived": len(written_modules),
    }
    prov_path.write_text(
        json.dumps(prov_body, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    # ── Step 4: BLUEPRINT.json — the reconstruction seed ──────────────────────
    # Engine + BLUEPRINT.json = full deterministic reconstruction. Every atom
    # is listed by canonical id, tier, body_hash, language, and the source
    # signature it was derived from. Drop this file alongside `ass-ade` and
    # run `ass-ade rebuild --from-blueprint BLUEPRINT.json` to regenerate
    # the entire output, byte-identical (modulo timestamps), with sovereign
    # constants resolved fresh through the oracle.
    blueprint_path = target_root / "BLUEPRINT.json"
    _assert_under_root(blueprint_path, out_dir)
    blueprint = {
        "blueprint_schema": "ASSADE-SPEC-BLUEPRINT-1",
        "rebuild_tag": tag,
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "source_plan_digest": plan.get("content_digest"),
        "counts": {"total": len(written), "by_tier": by_tier},
        "tier_versions": tier_versions,
        # Atoms in stable canonical-id order — the registry view of this
        # build. Each row is a swappable contract: same id + same body_hash
        # = byte-identical atom across rebuilds, registries, and languages.
        "atoms": sorted(
            [
                {
                    "id": w["id"],
                    "tier": w["tier"],
                    "name": w["name"],
                    "kind": w["kind"],
                    "version": w["version"],
                    "body_hash": w["body_hash"],
                    "fulfills_blueprints": w.get("fulfills_blueprints", []),
                    # Source-relative path inside this output (post-rename),
                    # so consumers can locate the atom body without parsing
                    # MANIFEST.json again.
                    "module_path": (
                        Path(w["source_file"]).relative_to(target_root).as_posix()
                        if w.get("source_file") and Path(w["source_file"]).is_relative_to(target_root)
                        else None
                    ),
                }
                for w in written
            ],
            key=lambda r: (r["tier"], r["id"]),
        ),
        # Reconstruction recipe — exactly what an external runner needs.
        "reconstruction": {
            "engine": "ass-ade>=0.1",
            "command": "ass-ade rebuild --from-blueprint BLUEPRINT.json --output ./out",
            "requires": ["scripts/leak_patterns/symbols.txt", ".ass-ade/specs/cna-seed.yaml"],
            "ships_with": ["agents/", "scripts/leak_patterns/", ".ass-ade/specs/"],
        },
    }
    blueprint_path.write_text(
        json.dumps(blueprint, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    pointer = out_dir / "latest.txt"
    _assert_under_root(pointer, out_dir)
    pointer.write_text(target_root.as_posix() + "\n", encoding="utf-8")

    return {
        "rebuild_tag": tag,
        "target_root": target_root.as_posix(),
        "manifest_path": manifest_path.as_posix(),
        "provenance_path": prov_path.as_posix(),
        "blueprint_path": blueprint_path.as_posix(),
        "pointer": pointer.as_posix(),
        "written_count": len(written),
        "by_tier": by_tier,
        "tier_versions": tier_versions,
        "written_modules": list(written_modules.values()),
        # Full src→dest map for import_rewriter (E2 — predictive import resolution)
        "written_modules_map": {src: dest for src, dest in written_modules.items()},
    }

