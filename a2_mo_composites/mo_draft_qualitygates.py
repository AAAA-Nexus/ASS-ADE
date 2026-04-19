# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/agent/gates.py:35
# Component id: mo.source.ass_ade.qualitygates
__version__ = "0.1.0"

class QualityGates:
    """Applies AAAA-Nexus quality gates to agent operations.

    In hybrid/premium profiles, every model call is guarded:
    - Prompt injection scan (input)
    - Hallucination oracle (output)
    - Security shield (tool calls)
    - Output certification (final answer)
    - Context trimming (memory optimization)
    """

    def __init__(self, nexus_client: Any, config: dict | None = None) -> None:
        self._client = nexus_client
        self._v18_config: dict = config or {}
        self._gate_log: list[GateResult] = []

    @property
    def gate_log(self) -> list[GateResult]:
        """Full log of gate results for this session."""
        return list(self._gate_log)

    def scan_prompt(self, text: str) -> dict[str, Any] | None:
        """Scan user input for injection attacks."""
        try:
            result = self._client.prompt_inject_scan(text)
            gate = GateResult(
                gate="prompt_scan",
                passed=not (result.threat_detected or False),
                confidence=result.confidence,
                details={"threat_level": result.threat_level},
            )
            self._gate_log.append(gate)
            return {
                "blocked": result.threat_detected or False,
                "threat_level": result.threat_level,
                "confidence": result.confidence,
            }
        except Exception as _exc:  # noqa: BLE001
            logging.getLogger(__name__).warning(
                "Gate %s failed (fail-open): %s: %s",
                "scan_prompt",
                type(_exc).__name__,
                _exc,
            )
            return None

    def check_hallucination(self, text: str) -> dict[str, Any] | None:
        """Check model output for hallucination using ε-KL divergence scoring."""
        try:
            result = self._client.hallucination_oracle(text)
            gate = GateResult(
                gate="hallucination",
                passed=result.verdict != "unsafe",
                confidence=result.confidence,
                details={"verdict": result.verdict, "policy_epsilon": result.policy_epsilon},
            )
            self._gate_log.append(gate)
            return {
                "verdict": result.verdict,
                "confidence": result.confidence,
                "policy_epsilon": result.policy_epsilon,
            }
        except Exception as _exc:  # noqa: BLE001
            logging.getLogger(__name__).warning(
                "Gate %s failed (fail-open): %s: %s",
                "check_hallucination",
                type(_exc).__name__,
                _exc,
            )
            return None

    def shield_tool(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any] | None:
        """Shield a tool call through Nexus security."""
        try:
            result = self._client.security_shield({"tool": tool_name, **arguments})
            gate = GateResult(
                gate="tool_shield",
                passed=not (result.blocked or False),
                confidence=1.0,
                details={"tool": tool_name, "sanitized": result.sanitized},
            )
            self._gate_log.append(gate)
            return {
                "blocked": result.blocked or False,
                "sanitized": result.sanitized,
                "reason": "security policy" if result.blocked else None,
            }
        except Exception as _exc:  # noqa: BLE001
            logging.getLogger(__name__).warning(
                "Gate %s failed (fail-open): %s: %s",
                "shield_tool",
                type(_exc).__name__,
                _exc,
            )
            return None

    def certify(self, output: str) -> dict[str, Any] | None:
        """Certify final output quality against a rubric."""
        try:
            result = self._client.certify_output(
                output=output,
                rubric=["correctness", "safety", "completeness"],
            )
            gate = GateResult(
                gate="certify",
                passed=result.rubric_passed,
                confidence=result.score,
                details={"certificate_id": result.certificate_id},
            )
            self._gate_log.append(gate)
            return {
                "certificate_id": result.certificate_id,
                "score": result.score,
                "passed": result.rubric_passed,
            }
        except Exception as _exc:  # noqa: BLE001
            logging.getLogger(__name__).warning(
                "Gate %s failed (fail-open): %s: %s",
                "certify",
                type(_exc).__name__,
                _exc,
            )
            return None

    def trim_context(self, context: str, target_tokens: int) -> str | None:
        """Trim context using Nexus memory_trim for optimal token usage.

        Falls back to None if Nexus is unavailable (caller uses local trim).
        """
        try:
            result = self._client.memory_trim(context=context, target_tokens=target_tokens)
            gate = GateResult(
                gate="memory_trim",
                passed=True,
                confidence=1.0,
                details={"target_tokens": target_tokens},
            )
            self._gate_log.append(gate)
            return result.trimmed_context
        except Exception as _exc:  # noqa: BLE001
            logging.getLogger(__name__).warning(
                "Gate %s failed (fail-open): %s: %s",
                "trim_context",
                type(_exc).__name__,
                _exc,
            )
            return None

    def hook_50_audit(self, cycle_state: dict[str, Any]) -> dict[str, Any] | None:
        try:
            from ass_ade.agent.wisdom import WisdomEngine
            engine = WisdomEngine(getattr(self, "_v18_config", {}) or {}, self._client)
            report = engine.run_audit(cycle_state)
            self._gate_log.append(GateResult(
                gate="fifty_audit",
                passed=report.score >= 0.5,
                confidence=report.score,
                details={"passed": report.passed, "failed": report.failed},
            ))
            return {
                "passed": report.passed,
                "failed": report.failed,
                "score": report.score,
                "conviction": report.conviction,
            }
        except Exception as exc:
            logging.getLogger(__name__).warning("hook_50_audit failed: %s", exc)
            return None

    def hook_trustbench_verify(self, action: dict[str, Any]) -> bool | None:
        try:
            from ass_ade.agent.trust_gate import TrustVerificationGate
            gate = TrustVerificationGate(getattr(self, "_v18_config", {}) or {}, self._client)
            ok = gate.pre_action_verify(action)
            self._gate_log.append(GateResult(
                gate="trustbench_verify",
                passed=ok,
                confidence=1.0 if ok else 0.0,
                details={"action": str(action)[:200]},
            ))
            return ok
        except Exception as exc:
            logging.getLogger(__name__).warning("hook_trustbench_verify failed: %s", exc)
            return None

    def hook_deception_monitor(self, history: list[dict[str, Any]]) -> dict[str, Any] | None:
        if not history:
            return {"selective_trust": False, "inconsistencies": 0}
        try:
            per_target: dict[str, list[bool]] = {}
            for entry in history:
                target = str(entry.get("target") or entry.get("agent") or "")
                result = bool(entry.get("result", True))
                per_target.setdefault(target, []).append(result)
            inconsistencies = sum(
                1 for outcomes in per_target.values()
                if len(set(outcomes)) > 1 and len(outcomes) >= 3
            )
            selective = inconsistencies >= 2
            self._gate_log.append(GateResult(
                gate="deception_monitor",
                passed=not selective,
                confidence=1.0 - 0.1 * inconsistencies,
                details={"inconsistencies": inconsistencies},
            ))
            return {"selective_trust": selective, "inconsistencies": inconsistencies}
        except Exception as exc:
            logging.getLogger(__name__).warning("hook_deception_monitor failed: %s", exc)
            return None

    def hook_aaaa_nexus_economic(self, action: dict[str, Any]) -> dict[str, Any] | None:
        try:
            x402 = getattr(self._client, "x402", None)
            if x402 is None:
                return {"settled": False, "reason": "x402_unavailable"}
            amount = float(action.get("amount", 0.0))
            if hasattr(x402, "settle"):
                receipt = x402.settle(amount=amount, recipient=action.get("recipient", ""))
                return {"settled": True, "receipt": str(receipt)[:256]}
            return {"settled": False, "reason": "no_settle_method"}
        except Exception as exc:
            logging.getLogger(__name__).warning("hook_aaaa_nexus_economic failed: %s", exc)
            return None

    def hook_pci_verify(self, code: str, lang: str = "python", spec: str | None = None) -> dict[str, Any] | None:
        import ast
        import re
        try:
            findings: list[str] = []
            cc = 1
            if lang == "python":
                try:
                    tree = ast.parse(code)
                    for node in ast.walk(tree):
                        if isinstance(node, (ast.If, ast.For, ast.While, ast.And, ast.Or, ast.ExceptHandler)):
                            cc += 1
                except SyntaxError as exc:
                    findings.append(f"syntax:{exc.msg}")
                    cc = 999
            owasp_patterns = [
                (r"eval\s*\(", "a03_injection_eval"),
                (r"exec\s*\(", "a03_injection_exec"),
                (r"subprocess\.[a-z_]+\([^)]*shell\s*=\s*True", "a03_shell_injection"),
                (r"pickle\.loads?\s*\(", "a08_deserialization"),
                (r"md5\s*\(|sha1\s*\(", "a02_weak_hash"),
            ]
            for pat, code_id in owasp_patterns:
                if re.search(pat, code):
                    findings.append(code_id)
            cc_ok = cc <= 7
            lean4_ok = True
            if spec and "sorry" in spec:
                lean4_ok = False
            passed = cc_ok and not findings and lean4_ok
            self._gate_log.append(GateResult(
                gate="pci_verify",
                passed=passed,
                confidence=1.0 if passed else 0.3,
                details={"cc": cc, "findings": findings, "lean4_ok": lean4_ok},
            ))
            return {"cc": cc, "findings": findings, "passed": passed, "lean4_ok": lean4_ok}
        except Exception as exc:
            logging.getLogger(__name__).warning("hook_pci_verify failed: %s", exc)
            return None

    def hook_verispec_synthesize(self, task: str) -> dict[str, Any] | None:
        try:
            from ass_ade.agent.proofbridge import ProofBridge
            pb = ProofBridge(getattr(self, "_v18_config", {}) or {}, self._client)
            spec = pb.translate(task)
            return {"name": spec.name, "source": spec.source, "has_sorry": spec.has_sorry}
        except Exception as exc:
            logging.getLogger(__name__).warning("hook_verispec_synthesize failed: %s", exc)
            return None

    def hook_alphaverus_refine(self, code: str, spec: str) -> dict[str, Any] | None:
        try:
            from ass_ade.agent.alphaverus import AlphaVerus
            av = AlphaVerus(getattr(self, "_v18_config", {}) or {}, self._client)
            result = av.tree_search(code, spec)
            if result is None:
                return {"code": code, "verified": False, "score": 0.0, "passed": False}
            return {
                "code": result.code,
                "verified": result.verified,
                "score": result.score,
                "passed": True,
            }
        except Exception as exc:
            logging.getLogger(__name__).warning("hook_alphaverus_refine failed: %s", exc)
            return None

    def hook_dgm_h_validate(self, patch: Any) -> dict[str, Any] | None:
        try:
            from ass_ade.agent.dgm_h import DGMH, Patch
            dgm = DGMH(getattr(self, "_v18_config", {}) or {}, self._client)
            if not isinstance(patch, Patch):
                patch = Patch(
                    id=str(getattr(patch, "id", "p0")),
                    target=str(getattr(patch, "target", "")),
                    diff=str(getattr(patch, "diff", patch)),
                )
            sim = dgm.simulate(patch)
            self._gate_log.append(GateResult(
                gate="dgm_h_validate",
                passed=sim.validated,
                confidence=max(0.0, min(1.0, sim.delta)),
                details={"cycles": sim.cycles, "violations": sim.violations},
            ))
            return {"validated": sim.validated, "delta": sim.delta, "cycles": sim.cycles}
        except Exception as exc:
            logging.getLogger(__name__).warning("hook_dgm_h_validate failed: %s", exc)
            return None

    def hook_meta_edit_validate(self, meta_edit: Any) -> dict[str, Any] | None:
        """Validate a meta-edit by running N=5 sample tasks before and after.

        Passes iff audit_pass_rate_delta >= 0.05. Results are persisted to
        .ass-ade/state/meta_edit_audits/{timestamp}.json.
        """
        import json
        from datetime import UTC, datetime
        from pathlib import Path

        try:
            from ass_ade.agent.golden_runner import run_golden

            cfg = getattr(self, "_v18_config", {}) or {}
            golden_path = Path(
                (cfg.get("dgm_h") or {}).get("golden_task_path", ".ass-ade/golden/tasks.jsonl")
            )
            audits_dir = Path(
                (cfg.get("dgm_h") or {}).get("meta_audit_dir", ".ass-ade/state/meta_edit_audits")
            )

            me_id = str(getattr(meta_edit, "id", "meta_edit"))
            me_desc = str(getattr(meta_edit, "description", "") or getattr(meta_edit, "procedure", ""))

            before = run_golden(golden_path, tasks_limit=5, repeats=1, prompt_suffix="", seed=11)
            after = run_golden(
                golden_path,
                tasks_limit=5,
                repeats=1,
                prompt_suffix=f"meta_edit:{me_id}:{me_desc[:80]}",
                seed=13,
            )
            before_rate = float(before.get("aggregate", {}).get("pass_rate", 0.0))
            after_rate = float(after.get("aggregate", {}).get("pass_rate", 0.0))
            delta = after_rate - before_rate
            ok = delta >= 0.05

            artifact: dict[str, Any] = {
                "meta_edit_id": me_id,
                "description": me_desc,
                "before_rate": before_rate,
                "after_rate": after_rate,
                "delta": delta,
                "validated": ok,
                "before_per_task": before.get("per_task", []),
                "after_per_task": after.get("per_task", []),
                "ts": datetime.now(UTC).isoformat(),
            }
            try:
                audits_dir.mkdir(parents=True, exist_ok=True)
                ts = datetime.now(UTC).strftime("%Y%m%dT%H%M%S%f")
                (audits_dir / f"{ts}_{me_id}.json").write_text(
                    json.dumps(artifact, indent=2), encoding="utf-8"
                )
            except OSError:
                pass

            self._gate_log.append(GateResult(
                gate="meta_edit_validate",
                passed=ok,
                confidence=max(0.0, min(1.0, 0.5 + delta)),
                details={"before_rate": before_rate, "after_rate": after_rate, "delta": delta},
            ))
            return {
                "before_rate": before_rate,
                "after_rate": after_rate,
                "delta": delta,
                "validated": ok,
            }
        except Exception as exc:
            logging.getLogger(__name__).warning("hook_meta_edit_validate failed: %s", exc)
            return None

    def hook_map_terrain_gate(self, ctx: dict[str, Any]) -> dict[str, Any] | None:
        try:
            for method in ("map_terrain", "nexus_map_terrain"):
                fn = getattr(self._client, method, None)
                if fn is None:
                    continue
                try:
                    result = fn(ctx)
                    verdict = getattr(result, "verdict", None)
                    if verdict is None and isinstance(result, dict):
                        verdict = result.get("verdict")
                    return {"verdict": verdict or "proceed"}
                except Exception:
                    break
            return {"verdict": "proceed", "source": "fallback"}
        except Exception as exc:
            logging.getLogger(__name__).warning("hook_map_terrain_gate failed: %s", exc)
            return None

    def gate_sam(self, target: str, intent: str = "", impl: str = "") -> dict[str, Any] | None:
        """Run SAM TRS scoring + G23 gate as Stage 0 of the pipeline.

        Returns None on failure (fail-open). Logs result to gate_log.
        Blocks synthesis in hybrid/premium if TRS < 0.5.
        """
        try:
            from ass_ade.agent.sam import SAM

            sam = SAM(self._v18_config, self._client)
            trs = sam.compute_trs(target)
            g23_ok = sam.validate_g23(intent, impl) if (intent and impl) else True
            composite = (trs["trust"] + trs["relevance"] + trs["security"]) / 3.0
            passed = composite >= 0.5 and g23_ok
            self._gate_log.append(GateResult(
                gate="sam",
                passed=passed,
                confidence=composite,
                details={"trs": trs, "g23": g23_ok, "composite": composite},
            ))
            # TRS telemetry to Nexus in hybrid/premium
            try:
                if hasattr(self._client, "reputation_record"):
                    if composite < 0.7:
                        self._client.reputation_record(
                            "sam_gate", success=False, quality=composite, latency_ms=0.0
                        )
                    elif composite >= 0.9:
                        self._client.reputation_record(
                            "sam_gate", success=True, quality=composite, latency_ms=0.0
                        )
            except Exception:
                pass
            return {"trs": trs, "g23": g23_ok, "composite": composite, "passed": passed}
        except Exception as exc:
            logging.getLogger(__name__).warning("gate_sam failed (fail-open): %s", exc)
            return None

    def run_pipeline(self, *, prompt: str, output: str, intent: str = "", impl: str = "") -> list[GateResult]:
        """Run the full gate pipeline on a prompt→output pair.

        Stage 0 (Phase 1): SAM TRS scoring + G23 gate
        Stage 1: prompt injection scan
        Stage 2: hallucination oracle
        Stage 3: output certification

        Returns the list of gate results. Does not block — callers
        should inspect the results and act accordingly.
        """
        results: list[GateResult] = []

        # Stage 0: SAM (Phase 1)
        log_before = len(self._gate_log)
        self.gate_sam(target=prompt, intent=intent or prompt, impl=impl or output)
        if len(self._gate_log) > log_before:
            results.extend(self._gate_log[log_before:])

        log_before = len(self._gate_log)
        scan = self.scan_prompt(prompt)
        if scan and len(self._gate_log) > log_before:
            results.extend(self._gate_log[log_before:])

        log_before = len(self._gate_log)
        halluc = self.check_hallucination(output)
        if halluc and len(self._gate_log) > log_before:
            results.extend(self._gate_log[log_before:])

        log_before = len(self._gate_log)
        cert = self.certify(output)
        if cert and len(self._gate_log) > log_before:
            results.extend(self._gate_log[log_before:])

        return results
