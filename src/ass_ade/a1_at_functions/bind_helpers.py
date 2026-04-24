"""Tier a1 — assimilated function 'bind'

Assimilated from: binder.py:109-294
"""

from __future__ import annotations


# --- assimilated symbol ---
def bind(
    manifest: CapabilityManifest,
    registry=None,
    *,
    session=None,
    tool_version: str = "",
    weights: ScoringWeights | None = None,
    metadata: dict[str, AtomMetadata] | None = None,
    now: datetime | None = None,
    scoring_spec_path: Path | None = None,
    nexus_transport=_NEXUS_SENTINEL,
) -> BindPlan:
    """Bind every blueprint in ``manifest`` to a concrete outcome.

    ``registry`` may be any object exposing ``lookup(canonical_name,
    version_pin=None) -> Atom | None`` and ``search_by_sig_fp(sig_fp,
    within=None) -> Iterable[Atom]``. When ``None`` the module's
    default registry (``ass_ade.engine.registry.default_registry``)
    is used. Tests commonly inject a lightweight mock.

    ``session`` enables oracle-backed sovereign checks. When ``None``
    the binder runs in offline mode — helpful for unit tests and
    early-development paths where the sovereign layer is not yet
    wired. Offline decisions are tagged ``offline`` in the public
    genesis log so auditors can tell them apart from production runs.

    ``nexus_transport`` wires ``_PROTOCOL.md §11`` preflight + postflight
    around the binder entry (A-11). Production callers (CLI entrypoints,
    binder orchestration) MUST thread a real
    :class:`ass_ade.engine.nexus.NexusTransport`. Passing
    ``nexus_transport=None`` explicitly opts out of Nexus binding for
    offline tests + bootstrap paths; the binder tags the plan
    ``offline`` and emits no preflight/postflight receipts. Omitting
    the argument raises :class:`ass_ade.engine.nexus.NexusTransportMissing`
    to prevent silent drift in production callsites — MAP = TERRAIN
    forbids an implicit "just skip Nexus" default.

    Failures:

    * :class:`BinderRefused` — Nexus preflight or postflight rejected
      the turn (``code`` in ``{"nexus_injection_blocked",
      "nexus_drift_stale", "hallucination_ceiling_exceeded"}``).
    * :class:`NexusUnavailable` — transport failed 3 attempts with
      exponential backoff; fail-closed per ``_PROTOCOL.md §11.5``.
    * :class:`NexusTransportMissing` — production caller forgot to
      wire ``nexus_transport=``.
    """
    if nexus_transport is _NEXUS_SENTINEL:
        raise NexusTransportMissing(
            "bind() requires an explicit nexus_transport= argument. Pass a "
            "NexusTransport for production, or nexus_transport=None to opt "
            "out (tests + bootstrap). Omitting the argument is not allowed "
            "per _PROTOCOL.md §11 (no silent Nexus bypass)."
        )

    registry = registry if registry is not None else _default_registry()
    reused: list[AtomRef] = []
    extended: list[AtomRef] = []
    refactored: list[RefactorDesc] = []
    synthesized: list[SynthDesc] = []
    fallback_atoms: dict[str, list[AtomRef]] = {}
    needs_human: list[str] = []
    per_blueprint_events: list[dict] = []

    blueprints = list(manifest.blueprints)
    now = now or datetime.now(UTC)
    constants = _scoring.load_constants(scoring_spec_path)

    # Preflight: hash the manifest shape into an envelope and call
    # Aegis-Edge + UEP-govern. On refusal, BinderRefused propagates with
    # a §11.5 code; on transport failure NexusUnavailable propagates.
    # Tests opt out with nexus_transport=None.
    preflight_result: PreflightResult | None = None
    if nexus_transport is not None:
        preflight_envelope = _preflight_envelope(manifest, session=session)
        preflight_result = _nexus_preflight(
            preflight_envelope, transport=nexus_transport
        )

    for idx, bp in enumerate(blueprints):
        classification = _classify_blueprint(
            bp,
            registry=registry,
            session=session,
            weights=weights,
            metadata=metadata,
            now=now,
            scoring_spec_path=scoring_spec_path,
        )
        key = bp.canonical_name or f"blueprint[{idx}]"
        runner = None
        if classification.ranked:
            runner = _scoring.runner_up_within_epsilon(
                classification.ranked, constants
            )
        if runner is not None:
            fallback_atoms.setdefault(key, []).append(runner.atom_ref)

        if classification.kind == "REUSE":
            w = classification.winner
            assert w is not None  # _classify_blueprint invariant for REUSE
            reused.append(AtomRef.from_atom(w))
        elif classification.kind == "EXTEND":
            w = classification.winner
            assert w is not None  # _classify_blueprint invariant for EXTEND
            extended.append(AtomRef.from_atom(w))
        elif classification.kind == "REFACTOR":
            w = classification.winner
            assert w is not None  # _classify_blueprint invariant for REFACTOR
            refactored.append(
                RefactorDesc(
                    target_ref=AtomRef.from_atom(w),
                    near_candidates=[
                        r.atom_ref for r in classification.ranked[:3]
                    ],
                    rationale=classification.rationale,
                    blueprint_idx=idx,
                )
            )
        elif classification.kind == "SYNTHESIZE":
            synthesized.append(
                SynthDesc(
                    canonical_name=bp.canonical_name
                    or f"a1.synth.blueprint_{idx}",
                    blueprint_signature=bp.signature,
                    rationale=classification.rationale,
                    seed_candidates=[
                        r.atom_ref for r in classification.ranked[:3]
                    ],
                    tier="a1",
                    blueprint_idx=idx,
                )
            )
        per_blueprint_events.append(
            _blueprint_event(bp, idx, classification, runner)
        )

    total = len(blueprints)
    synth_count = len(synthesized)
    phase_transition = _synth_saturation(
        synth_count, total, session=session
    )
    if phase_transition:
        needs_human.append(
            f"phase_transition: {synth_count}/{total} items require synthesis"
        )

    manifest_fp = _manifest_fingerprint(manifest)
    plan = BindPlan(
        reused=reused,
        extended=extended,
        refactored=refactored,
        synthesized=synthesized,
        fallback_atoms=fallback_atoms,
        phase_transition=phase_transition,
        needs_human=needs_human,
        manifest_fingerprint=manifest_fp,
    )
    plan.bindings_lock = LockFile(
        manifest_fingerprint=manifest_fp,
        entries=_collect_lock_entries(plan),
        tool_version=tool_version or _default_tool_version(),
        generated_at_iso=_deterministic_iso_from_manifest(manifest_fp),
    )
    plan.nexus_preflight = preflight_result

    # Postflight: hash the plan result, call hallucination-ceiling +
    # trust-chain-sign, seal the handle into plan.trust_receipt (not
    # the raw ceiling — §11.3 opacity). The per-blueprint decision
    # events below then travel alongside the receipt handle.
    if nexus_transport is not None:
        outbound_result = _postflight_outbound(plan, per_blueprint_events)
        plan.trust_receipt = _nexus_trust_receipt(
            outbound_result,
            transport=nexus_transport,
            session=_session_view(session),
        )

    _emit_bind_event(
        manifest,
        plan,
        per_blueprint_events,
        offline=session is None,
        nexus_offline=nexus_transport is None,
    )
    return plan

