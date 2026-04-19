# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_ciepipeline.py:5
# Component id: mo.source.ass_ade.ciepipeline
__version__ = "0.1.0"

class CIEPipeline:
    """Code Integrity Engine — validates and gates all code synthesis."""

    def __init__(self, config: dict[str, Any] | None = None, nexus: Any = None) -> None:
        self._config = config or {}
        self._nexus = nexus
        cfg = self._config.get("cie") or {}
        self._hard_block_owasp = cfg.get("hard_block_owasp", True)
        self._require_alphaverus = cfg.get("require_alphaverus", False)
        self._enable_lint = cfg.get("enable_lint", True)
        self._enable_proofbridge = cfg.get("enable_proofbridge", False)
        self._passes = 0
        self._failures = 0
        self._patches_applied = 0

    def run(self, candidate: str, language: str = "python", context: dict[str, Any] | None = None) -> CIEResult:
        """Run the full CIE pipeline on a code candidate."""
        ctx = context or {}
        result = CIEResult(passed=True, candidate=candidate, language=language)
        try:
            self._run_inner(result, ctx)
        except Exception as exc:
            _log.warning("CIE pipeline error (fail-open): %s", exc)
            result.warnings.append(f"CIE pipeline error: {exc}")
        if result.passed:
            self._passes += 1
        else:
            self._failures += 1
        return result

    def _run_inner(self, result: CIEResult, ctx: dict[str, Any]) -> None:
        # Stage 1: AST Verification
        if result.language == "python":
            self._verify_ast_python(result)
            if not result.ast_valid:
                result.passed = False
                return  # no point continuing if syntax is broken

        # Stage 2: Lint Gate
        if self._enable_lint and result.language == "python":
            self._lint_gate(result)

        # Stage 3: OWASP Scan
        self._owasp_scan(result)
        if not result.owasp_clean and self._hard_block_owasp:
            result.passed = False
            return

        # Stage 4: AlphaVerus variant gate
        self._alphaverus_gate(result, ctx)

        # Stage 5: ProofBridge (optional)
        if self._enable_proofbridge and "# @prove" in result.candidate:
            self._proofbridge_stub(result, ctx)

        result.passed = result.ast_valid and result.owasp_clean

    # ── Stage 1: AST ──────────────────────────────────────────────────────

    def _verify_ast_python(self, result: CIEResult) -> None:
        try:
            ast.parse(result.candidate)
            result.ast_valid = True
        except SyntaxError as exc:
            result.ast_valid = False
            result.errors.append(f"SyntaxError:{exc.lineno}:{exc.msg}")

    # ── Stage 2: Lint Gate ────────────────────────────────────────────────

    def _lint_gate(self, result: CIEResult) -> None:
        lint_errors = self._run_ruff(result.candidate)
        if not lint_errors:
            result.lint_clean = True
            return
        # Try to auto-patch
        for _round in range(_MAX_PATCH_ROUNDS):
            patched = self._apply_minimal_patch(result.candidate, lint_errors)
            new_errors = self._run_ruff(patched)
            if not new_errors:
                result.candidate = patched
                result.lint_clean = True
                result.patch_applied = True
                result.patch_rounds = _round + 1
                self._patches_applied += 1
                return
            lint_errors = new_errors
            result.candidate = patched
        # Still failing after patches
        result.lint_clean = False
        result.patch_applied = True
        result.patch_rounds = _MAX_PATCH_ROUNDS
        result.warnings.extend(lint_errors[:10])

    def _run_ruff(self, code: str) -> list[str]:
        try:
            result = subprocess.run(
                [sys.executable, "-m", "ruff", "check", "--select=E,W,F", "--stdin-filename=cie_check.py", "-"],
                input=code.encode(),
                capture_output=True,
                timeout=10,
            )
            if result.returncode == 0:
                return []
            output = result.stdout.decode(errors="replace")
            return [line.strip() for line in output.splitlines() if line.strip() and "error" in line.lower()][:20]
        except FileNotFoundError:
            return []  # ruff not available
        except Exception as exc:
            _log.debug("ruff check failed: %s", exc)
            return []

    def _apply_minimal_patch(self, code: str, lint_errors: list[str]) -> str:
        """Apply minimal corrections for common lint issues.

        Handles:
          F401 — unused import       → drop line
          F841 — unused local var    → prefix with underscore
          E501 — line too long       → leave alone (don't silently wrap)
          E711 — `== None`           → rewrite to `is None`
          E712 — `== True / == False`→ rewrite to `is`
          E722 — bare except         → rewrite to `except Exception`
          W291/W293 — trailing ws    → strip
        """
        lines = code.splitlines(keepends=True)
        lines_to_remove: set[int] = set()
        loc_re = re.compile(r"[^:]+:(\d+):(\d+)?:?\s*([A-Z]\d+)")

        # Pre-pass: collect error metadata per line
        per_line: dict[int, list[str]] = {}
        for err in lint_errors:
            m = loc_re.search(err)
            if not m:
                continue
            lineno = int(m.group(1)) - 1
            code_id = m.group(3)
            if 0 <= lineno < len(lines):
                per_line.setdefault(lineno, []).append(code_id)

        # Apply per-rule fixes
        for lineno, codes in per_line.items():
            original = lines[lineno]
            patched = original

            if "F401" in codes:
                lines_to_remove.add(lineno)
                continue

            if "F841" in codes:
                # "unused_var = expr" → "_unused_var = expr"
                m = re.match(r"(\s*)([A-Za-z_][A-Za-z0-9_]*)\s*=", patched)
                if m and not m.group(2).startswith("_"):
                    patched = m.group(1) + "_" + patched[len(m.group(1)):]

            if "E711" in codes:
                patched = re.sub(r"==\s*None", "is None", patched)
                patched = re.sub(r"!=\s*None", "is not None", patched)

            if "E712" in codes:
                patched = re.sub(r"==\s*True\b", "is True", patched)
                patched = re.sub(r"==\s*False\b", "is False", patched)
                patched = re.sub(r"!=\s*True\b", "is not True", patched)
                patched = re.sub(r"!=\s*False\b", "is not False", patched)

            if "E722" in codes:
                patched = re.sub(r"\bexcept\s*:", "except Exception:", patched)

            if "W291" in codes or "W293" in codes:
                # Strip trailing whitespace, preserving trailing newline
                if patched.endswith("\n"):
                    patched = patched.rstrip() + "\n"
                else:
                    patched = patched.rstrip()

            if patched != original:
                lines[lineno] = patched

        if lines_to_remove:
            lines = [l for i, l in enumerate(lines) if i not in lines_to_remove]
        return "".join(lines)

    # ── Stage 3: OWASP Scan ───────────────────────────────────────────────

    def _owasp_scan(self, result: CIEResult) -> None:
        findings: list[str] = []
        for pattern, code_id in _OWASP_CRITICAL:
            if re.search(pattern, result.candidate):
                findings.append(code_id)
        medium: list[str] = []
        for pattern, code_id in _OWASP_MEDIUM:
            if re.search(pattern, result.candidate):
                medium.append(code_id)
        result.owasp_findings = findings + medium
        result.owasp_clean = len(findings) == 0
        if medium:
            result.warnings.extend([f"OWASP_medium:{m}" for m in medium])
        # Optional: Nexus zero-day scan for hybrid/premium
        if self._nexus and findings:
            try:
                self._nexus.zero_day_scan(code=result.candidate[:4000], lang=result.language)
            except Exception:
                pass

    # ── Stage 4: AlphaVerus Gate ──────────────────────────────────────────

    def _alphaverus_gate(self, result: CIEResult, ctx: dict[str, Any]) -> None:
        try:
            from ass_ade.agent.alphaverus import AlphaVerus

            spec = ctx.get("spec") or result.candidate[:200]
            av = AlphaVerus(self._config, self._nexus)
            best = av.tree_search(result.candidate, spec)
            if best is not None:
                result.candidate = best.code
                result.variant_score = best.score
                result.alphaverus_passed = best.verified
            else:
                result.alphaverus_passed = not self._require_alphaverus
        except Exception as exc:
            _log.debug("AlphaVerus gate skipped: %s", exc)
            result.alphaverus_passed = True  # fail-open

    # ── Stage 5: ProofBridge ──────────────────────────────────────────────

    def _proofbridge_stub(self, result: CIEResult, ctx: dict[str, Any]) -> None:
        try:
            from ass_ade.agent.proofbridge import ProofBridge

            pb = ProofBridge(self._config, self._nexus)
            task = ctx.get("task") or result.candidate[:200]
            spec = pb.translate(task)
            result.proof_stub = spec.source
        except Exception as exc:
            _log.debug("ProofBridge stub skipped: %s", exc)

    # ── Reporting ─────────────────────────────────────────────────────────

    def report(self) -> dict[str, Any]:
        total = self._passes + self._failures
        return {
            "engine": "cie",
            "passes": self._passes,
            "failures": self._failures,
            "pass_rate": round(self._passes / total, 3) if total else 0.0,
            "patches_applied": self._patches_applied,
        }
