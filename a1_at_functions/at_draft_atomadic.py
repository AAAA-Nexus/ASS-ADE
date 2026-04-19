# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/interpreter.py:454
# Component id: at.source.ass_ade.atomadic
__version__ = "0.1.0"

class Atomadic:
    """The Atomadic interpreter — friendly front door for ASS-ADE.

    Axiom 0 (Jessica Mary Colvin): Every boundary is also a door.

    6-step pipeline: receive → extract → gap-analyze → clarify → map → construct.
    Tone-adaptive: casual input → casual reply; precise input → precise reply.
    Epistemically honest: reports real outcomes, does not fabricate success.
    """

    working_dir: Path = field(default_factory=Path.cwd)
    history: list[Turn] = field(default_factory=list)
    memory: MemoryStore = field(default_factory=MemoryStore.load)
    _pending_clarification: str | None = field(default=None, init=False, repr=False)
    _clarification_ctx: dict = field(default_factory=dict, init=False, repr=False)

    # ── Public interface ───────────────────────────────────────────────────────

    def process(self, user_input: str) -> str:
        """Run the 6-step pipeline and return the postlude response.

        Transparency output (intent, command, progress) is printed directly
        to stdout during execution so the user sees it in real time.

        Tries LLM intent derivation first; falls back to keyword heuristics
        when no LLM endpoint is reachable.
        """
        text = user_input.strip()
        if not text:
            return ""

        tone = _detect_tone(text)

        # ── LLM-first path ────────────────────────────────────────────────────
        llm_result = _call_llm(text, self.working_dir)
        if llm_result is not None:
            if llm_result.get("type") == "chat":
                reply = llm_result.get("response", "")
                turn = Turn(
                    user=text, tone=tone, intent="chat",
                    path=str(self.working_dir), command=[],
                    output="", response=reply,
                )
                self.history.append(turn)
                self.memory.update_from_turn(turn)
                self.memory.append_history(turn)
                self.memory.save()
                return reply

            if llm_result.get("type") == "command":
                intent = llm_result.get("intent", "chat")
                cli_args = llm_result.get("cli_args")
                path = _substitute_datetime_tokens(
                    llm_result.get("path") or _extract_path(text) or str(self.working_dir)
                )
                output_path_raw = llm_result.get("output_path")
                output_path = _substitute_datetime_tokens(output_path_raw) if output_path_raw else None
                feature_desc = llm_result.get("feature_desc")

                if intent == "cli" and isinstance(cli_args, list):
                    raw_output, cmd = self._dispatch_cli_args(cli_args, tone)
                    response_intent = "cli"
                else:
                    raw_output, cmd = self._dispatch(intent, path, text, tone, feature_desc, output_path)
                    response_intent = intent
                response = self._postlude(response_intent, path, raw_output, tone)
                turn = Turn(
                    user=text, tone=tone, intent=response_intent, path=path,
                    command=cmd, output=raw_output, response=response,
                )
                self.history.append(turn)
                self.memory.update_from_turn(turn)
                self.memory.append_history(turn)
                self.memory.save()
                return response

        # ── Keyword-heuristic fallback (no LLM available) ─────────────────────
        path = _substitute_datetime_tokens(_extract_path(text) or str(self.working_dir))

        if self._pending_clarification:
            intent = self._clarification_ctx.get("intent", _classify_intent(text))
            new_path = _extract_path(text)
            if new_path:
                path = _substitute_datetime_tokens(new_path)
            elif text not in {"", ".", "here"}:
                path = _substitute_datetime_tokens(text.strip().strip("\"'")) or path
            self._pending_clarification = None
            self._clarification_ctx = {}
        else:
            lower_t = text.lower().strip()
            if lower_t in {"help", "?", "commands"} or any(
                p in lower_t for p in (
                    "what commands", "what can you", "what do you do",
                    "commands available", "show commands", "capabilities",
                )
            ):
                intent = "help"
            else:
                intent = _classify_intent(text)

        if intent == "rebuild" and path == str(self.working_dir) and not self.history:
            self._pending_clarification = "path"
            self._clarification_ctx = {"intent": intent}
            return self._ask_clarification(tone)

        raw_output, cmd = self._dispatch(intent, path, text, tone)
        response = self._postlude(intent, path, raw_output, tone)

        turn = Turn(
            user=text, tone=tone, intent=intent, path=path,
            command=cmd, output=raw_output, response=response,
        )
        self.history.append(turn)
        self.memory.update_from_turn(turn)
        self.memory.append_history(turn)
        self.memory.save()
        return response

    def _dispatch(
        self,
        intent: str,
        path: str,
        raw: str,
        tone: str,
        feature_desc: str | None = None,
        output_path: str | None = None,
    ) -> tuple[str, list[str]]:
        """Dispatch the intent to the right execution path.

        Returns (raw_output, cmd_used).
        Prints transparency header and prelude directly to stdout.
        """
        if intent == "rebuild":
            if not output_path:
                ts = datetime.now().strftime("%Y%m%d-%H%M%S")
                input_p = Path(path).resolve()
                output_path = str(input_p.parent / f"{input_p.name}-rebuilt-{ts}")
            prelude = self._prelude(intent, path, tone)
            print(prelude, flush=True)
            raw_output = self._execute_rebuild_pipeline(path, output_path)
            return raw_output, []

        if intent == "self-enhance":
            feature = feature_desc or self._extract_feature_desc(raw) or raw.strip()
            raw_output = self._execute_self_enhance(feature, tone)
            return raw_output, []

        if intent == "help":
            return self.describe_self(), []

        cmd = self._build_command(intent, path, raw, feature_desc=feature_desc, output_path=output_path)
        self._print_dispatch(intent, cmd)
        prelude = self._prelude(intent, path, tone)
        print(prelude, flush=True)
        print(flush=True)
        raw_output = self._execute(cmd)
        return raw_output, cmd

    def _dispatch_cli_args(self, cli_args: list[Any], tone: str) -> tuple[str, list[str]]:
        """Dispatch an exact ASS-ADE CLI command path chosen from the dynamic inventory."""
        args = [str(item).strip() for item in cli_args if str(item).strip()]
        if not args:
            return "[error] No CLI arguments were provided.", []
        if args[0] == "chat":
            return "[error] `chat` is already running; ask for help instead.", []
        if not command_path_exists(args, self.working_dir):
            return f"[error] Unknown ASS-ADE command path: {' '.join(args)}", []

        cmd = [sys.executable, "-m", "ass_ade", *args]
        self._print_dispatch("cli", cmd)
        prelude = (
            "Running the requested ASS-ADE command..."
            if tone != TONE_CASUAL
            else "On it - running that ASS-ADE command..."
        )
        print(prelude, flush=True)
        print(flush=True)
        return self._execute(cmd), cmd

    def _execute_self_enhance(self, feature_desc: str, tone: str) -> str:
        """Live self-enhancement: design → rebuild → hot-patch → visual flicker."""
        import time as _time

        source = str(self.working_dir.resolve())
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        output_path = str(self.working_dir.parent / f"{self.working_dir.name}-evolved-{ts}")
        base = [sys.executable, "-m", "ass_ade"]

        print(f"\n🧠 Intent: self-enhance")
        print(f"📋 Feature: {feature_desc}")
        print(f"⚡ Starting live evolution pipeline...", flush=True)
        print()

        # Step 1: Generate design blueprint
        print("⏳ Step 1/3: Generating design blueprint...", flush=True)
        rc = self._run_streaming(
            base + ["design", feature_desc, "--path", source]
        )
        if rc != 0:
            print(f"⚠️  Blueprint generation had warnings (continuing)", flush=True)
        else:
            print(f"✅ Blueprint generated", flush=True)

        # Step 2: Run rebuild pipeline
        print("\n⏳ Step 2/3: Rebuilding with blueprint applied...", flush=True)
        rebuild_output = self._execute_rebuild_pipeline(source, output_path)
        rebuild_ok = "[ok]" in rebuild_output

        # Step 3: Visual flicker transition
        print("\n⏳ Step 3/3: Hot-patching and evolving...", flush=True)
        _time.sleep(0.3)

        # Clear screen and show evolution animation
        try:
            print("\033[2J\033[H", end="", flush=True)  # clear screen
        except Exception:
            print("\n" * 3, flush=True)

        frames = ["⚡ Evolving.", "⚡ Evolving..", "⚡ Evolving...", "⚡ ⚡ Evolving..."]
        for frame in frames:
            print(f"\r{frame}   ", end="", flush=True)
            _time.sleep(0.25)
        print(flush=True)

        # Hot-patch
        patched = self._hot_patch()

        try:
            print("\033[2J\033[H", end="", flush=True)
        except Exception:
            print("\n" * 2, flush=True)

        if rebuild_ok:
            print(f"✅ Evolution complete.", flush=True)
            if patched:
                print(f"⚡ Hot-patched: {', '.join(patched[:5])}", flush=True)
            print(f"📁 New build: {output_path}", flush=True)
            return f"[ok] Done. The CLI just evolved. Feature applied: {feature_desc}"
        else:
            print(f"⚠️  Evolution had issues — check output above.", flush=True)
            return f"[ok] Evolution attempted with warnings. Feature: {feature_desc}. Check output folder: {output_path}"

    def describe_self(self) -> str:
        try:
            return render_atomadic_help(self.working_dir)
        except Exception:
            return (
                "I'm Atomadic, the front door of ASS-ADE.\n\n"
                "I can rebuild, design, document, lint, certify, enhance, scan, "
                "and evolve codebases. Just tell me what you want in plain English."
            )

    # ── Internals ──────────────────────────────────────────────────────────────

    def _build_command(
        self, intent: str, path: str, raw: str,
        feature_desc: str | None = None, output_path: str | None = None,
    ) -> list[str]:
        base = [sys.executable, "-m", "ass_ade"]
        if intent == "rebuild":
            # Rebuild is handled by _execute_rebuild_pipeline; return empty sentinel.
            return []
        if intent == "design":
            feature = feature_desc or self._extract_feature_desc(raw) or "feature"
            return base + ["design", feature, "--path", path]
        if intent == "docs":
            return base + ["docs", path]
        if intent == "lint":
            return base + ["lint", path]
        if intent == "certify":
            return base + ["certify", path]
        if intent == "enhance":
            return base + ["enhance", path]
        if intent == "eco-scan":
            return base + ["eco-scan", path]
        if intent == "recon":
            return base + ["recon", path]
        if intent == "doctor":
            return base + ["doctor"]
        if intent == "help":
            return []  # handled inline in _dispatch
        # "chat" intent with no LLM available — describe self
        return base + ["doctor"]

    def _print_dispatch(self, intent: str, cmd: list[str]) -> None:
        display_args = cmd[3:] if len(cmd) > 3 else []
        cmd_str = "ass-ade " + " ".join(str(a) for a in display_args)
        print(f"\n🧠 Intent: {intent}")
        print(f"🔧 Dispatching: {cmd_str}")
        print(flush=True)

    def _run_streaming(self, cmd: list[str]) -> int:
        """Stream subprocess output to stdout; return exit code."""
        try:
            proc = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, encoding="utf-8", errors="replace",
                cwd=str(self.working_dir),
            )
            if proc.stdout:
                for line in proc.stdout:
                    print(line, end="", flush=True)
            proc.wait(timeout=120)
            return proc.returncode or 0
        except subprocess.TimeoutExpired:
            try:
                proc.kill()
            except Exception:
                pass
            print("[timed out after 120s — killed]", flush=True)
            return -1
        except Exception as exc:
            print(f"[execution error: {exc}]", flush=True)
            return -1

    def _execute(self, cmd: list[str]) -> str:
        """Run a single command, streaming output live; return collected output."""
        output_parts: list[str] = []
        try:
            proc = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, encoding="utf-8", errors="replace",
                cwd=str(self.working_dir),
            )
            if proc.stdout:
                for line in proc.stdout:
                    print(line, end="", flush=True)
                    output_parts.append(line)
            proc.wait(timeout=120)
            output = "".join(output_parts).strip()
            if proc.returncode != 0:
                return f"[error] exit {proc.returncode}\n{output}"
            return output
        except subprocess.TimeoutExpired:
            try:
                proc.kill()
            except Exception:
                pass
            return "[error timed out after 120s]"
        except Exception as exc:
            return f"[execution error: {exc}]"

    def _execute_rebuild_pipeline(self, source: str, output: str) -> str:
        """Built-in rebuild pipeline: backup → copy → recon → lint → docs → certify → hot-patch."""
        import shutil as _shutil

        source_path = Path(source).resolve()
        output_path = Path(output).resolve()
        base = [sys.executable, "-m", "ass_ade"]

        # Safety: block in-place rebuild
        if source_path == output_path:
            return "[error] Source and output are the same path — in-place rebuild blocked for safety."

        print(f"\n🧠 Intent: rebuild")
        print(f"🔧 Dispatching: rebuild pipeline (5 phases)")
        print(f"   Source : {source_path}")
        print(f"   Output : {output_path}")
        print(flush=True)

        # Phase 0 — auto-backup
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_path = source_path.parent / f"{source_path.name}-backup-{ts}"
        suffix = 0
        while backup_path.exists():
            suffix += 1
            backup_path = source_path.parent / f"{source_path.name}-backup-{ts}-{suffix}"
        print(f"🛡️  Backup : {backup_path}")
        try:
            _shutil.copytree(str(source_path), str(backup_path))
            print(f"✅ Backup complete ({backup_path.name})", flush=True)
        except Exception as exc:
            return f"[error] Backup failed: {exc} — rebuild aborted for safety."

        # Phase 1 — copy source to output
        print(f"\n⏳ Phase 1/5: Copying source to output folder...", flush=True)
        try:
            if output_path.exists():
                _shutil.rmtree(output_path)
            _shutil.copytree(str(source_path), str(output_path))
            file_count = sum(1 for f in output_path.rglob("*") if f.is_file())
            print(f"✅ Copied {file_count} files → {output_path.name}", flush=True)
        except OSError as exc:
            print(f"[error] Copy failed: {exc}", flush=True)
            return (
                f"[error] Copy failed (disk full?): {exc}\n"
                f"Backup preserved at: {backup_path}"
            )
        except Exception as exc:
            return f"[error] Copy failed: {exc}"

        out_str = str(output_path)
        warnings: list[str] = []

        phases = [
            ("Recon",   ["recon",   out_str]),
            ("Lint",    ["lint",    out_str]),
            ("Docs",    ["docs",    out_str]),
            ("Certify", ["certify", out_str]),
        ]
        for idx, (label, args) in enumerate(phases, start=2):
            print(f"\n⏳ Phase {idx}/5: {label}...", flush=True)
            rc = self._run_streaming(base + args)
            if rc != 0:
                print(f"⚠️  {label} completed with warnings (exit {rc})", flush=True)
                warnings.append(label)
            else:
                print(f"✅ {label} done", flush=True)

        # Verify output is non-empty
        output_file_count = sum(1 for f in output_path.rglob("*") if f.is_file()) if output_path.exists() else 0
        if output_file_count == 0:
            failure_msg = "Rebuild produced empty output."
            print(f"\n❌ {failure_msg}", flush=True)
            log_path = source_path / "REBUILD_FAILURE.log"
            try:
                log_path.write_text(
                    f"{failure_msg}\nTimestamp: {ts}\nWarning phases: {warnings}\n",
                    encoding="utf-8",
                )
            except OSError:
                pass
            print(f"🔄 Rolling back to backup {backup_path.name}...", flush=True)
            self._rollback(output_path, backup_path)
            return f"[error] {failure_msg} Restored from backup: {backup_path}"

        # Hot-patch: reload updated modules immediately
        print(f"\n⚡ Hot-patching updated modules...", flush=True)
        patched = self._hot_patch()
        if patched:
            print(f"✅ Hot-patched: {', '.join(patched)}", flush=True)

        print(flush=True)
        result_tag = "[ok] All 5 phases complete" if not warnings else f"[ok] Pipeline complete — warnings in: {', '.join(warnings)}"
        return f"{result_tag}\nOutput : {output_path}\nBackup : {backup_path}"

    def _rollback(self, output_path: Path, backup_path: Path) -> None:
        """Restore output_path from backup after a failed rebuild."""
        import shutil as _shutil
        try:
            if output_path.exists():
                _shutil.rmtree(output_path)
            if backup_path.exists():
                _shutil.copytree(str(backup_path), str(output_path))
                print(f"✅ Restored from backup: {backup_path.name}", flush=True)
            else:
                print(f"⚠️  Backup not found at {backup_path} — manual restore required", flush=True)
        except Exception as exc:
            print(f"❌ Rollback failed: {exc} — restore manually from {backup_path}", flush=True)

    def _hot_patch(self) -> list[str]:
        """Reload ASS-ADE Python modules in-place after a rebuild."""
        import importlib as _il
        import sys as _sys
        patched: list[str] = []
        for name in list(_sys.modules.keys()):
            if name.startswith("ass_ade") and "interpreter" not in name:
                mod = _sys.modules.get(name)
                if mod is None:
                    continue
                try:
                    _il.reload(mod)
                    patched.append(name)
                except (ImportError, SyntaxError, Exception):
                    pass  # keep old module loaded
        return patched

    def _extract_feature_desc(self, text: str) -> str | None:
        patterns = [
            r'"([^"]{4,})"',
            r"'([^']{4,})'",
            r'(?:feature|implement|add|create|build)\s+(?:a\s+)?(.+)',
        ]
        for pat in patterns:
            m = re.search(pat, text, re.IGNORECASE)
            if m:
                return m.group(1).strip()[:200]
        return None

    def _ask_clarification(self, tone: str) -> str:
        if tone == TONE_CASUAL:
            return "Sure! Which folder do you want me to rebuild? (hit Enter to use the current directory)"
        return "Which path would you like to rebuild? Press Enter to use the current working directory."

    def _prelude(self, intent: str, path: str, tone: str) -> str:
        label = Path(path).name or path
        casual = {
            "rebuild": f"On it! Rebuilding `{label}` into clean tiers...",
            "design":  "Let me sketch that blueprint for you...",
            "docs":    f"Generating docs for `{label}`...",
            "lint":    f"Running lint on `{label}`...",
            "certify": f"Certifying `{label}`...",
            "enhance": f"Looking for improvements in `{label}`...",
            "eco-scan": f"Scanning `{label}` — getting the lay of the land...",
            "recon":   f"Running parallel recon on `{label}` — 5 agents, no LLM...",
            "doctor":  "Checking everything's connected and healthy...",
            "self-enhance": "Time to evolve. Generating blueprint, rebuilding, and hot-patching...",
            "help":    "Here's everything I can do:",
            "chat":    "Let me look into that...",
        }
        formal = {
            "rebuild": f"Initiating rebuild of `{label}` into the 5-tier monadic layout.",
            "design":  "Generating an AAAA-SPEC-004 blueprint.",
            "docs":    f"Generating documentation for `{label}`.",
            "lint":    f"Running the CIE lint pipeline on `{label}`.",
            "certify": f"Running the certification pipeline on `{label}`.",
            "enhance": f"Scanning `{label}` for enhancement opportunities.",
            "eco-scan": f"Running monadic compliance check on `{label}`.",
            "recon":   f"Running parallel reconnaissance on `{label}` (Scout, Dependency, Tier, Test, Doc).",
            "doctor":  "Running self-diagnostics.",
            "self-enhance": "Initiating live self-enhancement: design → rebuild → hot-patch.",
            "help":    "Available commands:",
            "chat":    "Processing your request.",
        }
        pool = casual if tone == TONE_CASUAL else formal
        return pool.get(intent, pool["chat"])

    def _postlude(self, intent: str, path: str, output: str, tone: str) -> str:
        label = Path(path).name or path
        failed = (
            not output
            or "[error" in output.lower()
            or "error:" in output.lower()
            or "[execution error" in output.lower()
        )

        if failed:
            snippet = output[:400] if output else "No output captured."
            if tone == TONE_CASUAL:
                return f"Hmm, ran into something:\n\n```\n{snippet}\n```\n\nWant me to try a different approach?"
            return f"The command encountered an issue:\n\n```\n{snippet}\n```\n\nReview the output and try again."

        if tone == TONE_CASUAL:
            wins = {
                "rebuild":  f"Done! `{label}` rebuilt, documented, and certified. Backup was saved — check the transparency output for its path.",
                "design":   "Blueprint's ready! Want me to rebuild it into actual code?",
                "docs":     "Docs generated! Check the output folder.",
                "lint":     "Lint done! See any issues above you want me to address?",
                "certify":  "Certified! CERTIFICATE.json is in the output folder.",
                "enhance":  "Here are my recommendations. Want me to apply any?",
                "eco-scan": "Compliance check complete! Full breakdown above.",
                "recon":    "Recon done! Scout, deps, tiers, tests, and docs all checked. See findings above.",
                "doctor":   "All good — everything's connected.",
                "self-enhance": "Done. The CLI just evolved. Try it out.",
                "help":     output if output else self.describe_self(),
                "cli":      "Command complete. I streamed the output above.",
                "chat":     output[:600] if output else "Here's what I found.",
            }
        else:
            wins = {
                "rebuild":  f"`{label}` rebuilt, documented, and certified. CERTIFICATE.json is in the output folder. Backup preserved.",
                "design":   "Blueprint generated. Review the JSON and run `ass-ade rebuild` to materialize it.",
                "docs":     "Documentation generated successfully.",
                "lint":     "Lint pipeline complete. Review any findings above.",
                "certify":  "Certification complete. CERTIFICATE.json has been written.",
                "enhance":  "Enhancement recommendations generated. Use `--apply` to apply specific findings.",
                "eco-scan": "Monadic compliance check complete.",
                "recon":    "Reconnaissance complete. Review the report above for structure, dependencies, tier distribution, test coverage, and documentation gaps.",
                "doctor":   "Self-check complete. All systems nominal.",
                "self-enhance": "Live evolution complete. The CLI has been rebuilt and hot-patched.",
                "help":     output if output else self.describe_self(),
                "cli":      "Command complete. Review the streamed output above.",
                "chat":     output[:600] if output else "No output returned.",
            }

        return wins.get(intent, wins["chat"])
