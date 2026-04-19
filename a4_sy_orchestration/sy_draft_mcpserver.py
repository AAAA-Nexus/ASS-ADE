# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/mcp/server.py:441
# Component id: sy.source.ass_ade.mcpserver
__version__ = "0.1.0"

class MCPServer:
    """MCP-compatible JSON-RPC 2.0 server over stdio.

    Implements MCP 2025-11-25:
    - initialize / initialized
    - tools/list (cursor pagination)
    - tools/call (with _meta.progressToken support)
    - ping
    - notifications/cancelled
    - notifications/progress (emitted for long-running tools)
    - notifications/message (logging)

    Exposes built-in IDE tools, hero workflows, agent loop, and A2A tools.
    """

    PROTOCOL_VERSION = "2025-11-25"
    SERVER_NAME = "ass-ade"
    SERVER_VERSION = "1.0.0"

    def __init__(self, working_dir: str = ".") -> None:
        self._registry = default_registry(working_dir)
        self._working_dir = working_dir
        self._initialized = False
        # Track in-flight request IDs for cancellation support
        self._cancelled: set[Any] = set()
        self._lock = threading.Lock()
        self._write_lock = threading.Lock()
        # Thread pool for dispatching long-running tool calls
        self._executor = ThreadPoolExecutor(max_workers=2)
        # Track in-flight futures by request ID for cancellation
        self._futures: dict[Any, Future[dict[str, Any] | None]] = {}
        # Track cancellation contexts by request ID for cooperative cancellation
        self._cancellation_contexts: dict[Any, CancellationContext] = {}
        # Phase 2/3/5: TCA, CIE, LoRA flywheel engines (lazy init)
        self._tca: Any = None
        self._cie: Any = None
        self._lora_flywheel: Any = None
        # NCB enforcement mode: "warn" (local, default) or "block" (hybrid/premium)
        self._ncb_mode: str = "warn"

    # ── Phase 2/3/5: Gate hooks for MCP IDE tools ────────────────────────

    @property
    def tca(self) -> Any:
        if self._tca is None:
            from ass_ade.agent.tca import TCAEngine
            self._tca = TCAEngine({"working_dir": self._working_dir})
        return self._tca

    @property
    def cie(self) -> Any:
        if self._cie is None:
            from ass_ade.agent.cie import CIEPipeline
            self._cie = CIEPipeline()
        return self._cie

    @property
    def lora_flywheel(self) -> Any:
        if self._lora_flywheel is None:
            try:
                from ass_ade.agent.lora_flywheel import LoRAFlywheel
                from ass_ade.config import load_config
                from ass_ade.nexus.client import NexusClient
                settings = load_config()
                nexus = None
                if settings.profile in {"hybrid", "premium"} and settings.nexus_api_key:
                    nexus = NexusClient(
                        base_url=settings.nexus_base_url,
                        timeout=settings.request_timeout_s,
                        api_key=settings.nexus_api_key,
                        agent_id=settings.agent_id,
                    )
                self._lora_flywheel = LoRAFlywheel(nexus=nexus, session_id=f"mcp:{id(self)}")
            except Exception as exc:
                _LOG.debug("LoRA flywheel init skipped: %s", exc)
                return None
        return self._lora_flywheel

    def _pre_tool_hook(self, name: str, arguments: dict[str, Any]) -> tuple[bool, str]:
        """Run pre-execution gates. Returns (allow, reason).

        - write_file / edit_file: enforce NCB contract (file must have been read)
        """
        if name in ("write_file", "edit_file"):
            path = arguments.get("path") or arguments.get("file_path") or ""
            if path and not self.tca.ncb_contract(path):
                report = self.tca.check_freshness(path)
                msg = (
                    f"NCB violation: {path} was not read within the last "
                    f"{int(report.threshold_hours)}h. Call read_file first."
                )
                if self._ncb_mode == "block":
                    return False, msg
                # warn mode: log + let through
                _LOG.warning("NCB warn: %s", msg)
        return True, ""

    def _post_tool_hook(
        self,
        name: str,
        arguments: dict[str, Any],
        result: Any,
        *,
        pre_write_content: str = "",
    ) -> Any:
        """Run post-execution gates.

        - read_file  → TCA.record_read
        - write_file / edit_file → CIE pipeline gate + LoRA fix capture

        Returns the (possibly modified) result. If CIE rejects the code, the
        file on disk is rolled back via undo_edit and the result is replaced
        with a structured error.
        """
        if not result or not getattr(result, "success", False):
            return result

        if name == "read_file":
            path = arguments.get("path") or arguments.get("file_path") or ""
            if path:
                try:
                    self.tca.record_read(path)
                except Exception as exc:
                    _LOG.debug("TCA record_read failed: %s", exc)
            return result

        if name in ("write_file", "edit_file"):
            path = arguments.get("path") or arguments.get("file_path") or ""
            code = arguments.get("content") or arguments.get("new_content") or ""
            language = "python" if path.endswith(".py") else "typescript" if path.endswith((".ts", ".tsx")) else "text"
            if code and language != "text":
                try:
                    cie_result = self.cie.run(code, language=language)
                    if not cie_result.passed:
                        # Roll back the write by invoking undo_edit
                        try:
                            self._registry.execute("undo_edit", path=path)
                        except Exception:
                            pass
                        # Capture rejection as negative training signal
                        if self.lora_flywheel is not None:
                            try:
                                self.lora_flywheel.capture_rejection(
                                    candidate=code[:2000],
                                    reason="; ".join(cie_result.errors + cie_result.owasp_findings)[:200],
                                )
                            except Exception:
                                pass
                        err_msg = (
                            f"[CIE REJECTED] {path}: "
                            f"ast_valid={cie_result.ast_valid}, "
                            f"owasp_clean={cie_result.owasp_clean}, "
                            f"errors={cie_result.errors[:3]}, "
                            f"owasp={cie_result.owasp_findings[:3]}"
                        )
                        from ass_ade.tools.base import ToolResult
                        return ToolResult(error=err_msg, success=False)
                    # Passed: capture as accepted fix for LoRA training.
                    # Only capture if the content actually changed — trivial
                    # edits (e.g., formatting-only) are not training signal.
                    if self.lora_flywheel is not None and code != pre_write_content:
                        try:
                            self.lora_flywheel.capture_fix(
                                original=pre_write_content,
                                fixed=code,
                                context={"path": path, "language": language, "tool": name},
                            )
                        except Exception:
                            pass
                except Exception as exc:
                    _LOG.debug("CIE gate skipped: %s", exc)
            return result

        return result

    def run(self) -> None:
        """Run the stdio JSON-RPC loop. Reads from stdin, writes to stdout.
        
        Dispatches tool calls to a thread pool to keep stdin responsive during
        long-running operations (e.g., agent loops, Nexus API calls).
        """
        for line in sys.stdin:
            raw_bytes = len(line.encode("utf-8", errors="replace"))
            if raw_bytes > _MAX_LINE_BYTES:
                self._write({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Request too large"}})
                continue
            line = line.strip()
            if not line:
                continue

            try:
                request = json.loads(line)
            except json.JSONDecodeError:
                self._write_error(None, -32700, "Parse error")
                continue

            # Dispatch to thread pool. The worker will call _handle_sync() and write the response.
            # This keeps stdin responsive for new requests and cancellations.
            req_id = request.get("id")
            future = self._executor.submit(self._handle_worker, request)
            
            # Track the future for cancellation support
            if req_id is not None:
                with self._lock:
                    self._futures[req_id] = future

    def _handle_worker(self, request: dict[str, Any]) -> None:
        """Worker thread entry point. Calls _handle_sync and writes the response.
        
        Runs in the thread pool executor. Handles any exceptions and ensures
        the response is written with proper serialization via _write_lock.
        """
        req_id = request.get("id")
        try:
            response = self._handle_sync(request)
            if response is not None:
                self._write(response)
        except Exception:
            _LOG.exception("Request handler failed: id=%s", req_id)
            if req_id is not None:
                self._write(self._error(req_id, -32603, "Internal server error"))
        finally:
            # Clean up the future reference
            if req_id is not None:
                with self._lock:
                    self._futures.pop(req_id, None)

    def _handle_sync(self, request: dict[str, Any]) -> dict[str, Any] | None:
        """Synchronous request handler. Can be called directly from tests or from worker threads.
        
        Returns the response dict, or None for notifications.
        """
        req_id = request.get("id")
        method = request.get("method", "")
        params = request.get("params") or {}

        # Notifications (no id) — don't respond
        if req_id is None:
            if method == "notifications/initialized":
                self._initialized = True
            elif method == "notifications/cancelled":
                # MCP 2025-11-25: client may cancel an in-flight request
                cancelled_id = params.get("requestId")
                if cancelled_id is not None:
                    with self._lock:
                        # Mark as cancelled and try to cancel the future
                        self._cancelled.add(cancelled_id)
                        future = self._futures.get(cancelled_id)
                        if future is not None:
                            # Try to cancel the future if it hasn't started yet
                            future.cancel()
                        # Signal cancellation to the execution context (cooperative cancellation)
                        ctx = self._cancellation_contexts.get(cancelled_id)
                        if ctx is not None:
                            ctx.cancel()
            return None

        NON_INIT_METHODS = {"initialize", "ping", "notifications/initialized"}
        if not self._initialized and method not in NON_INIT_METHODS:
            return self._error(req_id, -32002, "Server not initialized. Send 'initialize' first.")

        if method == "initialize":
            return self._handle_initialize(req_id, params)
        elif method == "tools/list":
            return self._handle_tools_list(req_id, params)
        elif method == "tools/call":
            return self._handle_tools_call(req_id, params)
        elif method == "ping":
            return self._result(req_id, {})
        else:
            return self._error(req_id, -32601, f"Method not found: {method}")

    def _handle(self, request: dict[str, Any]) -> dict[str, Any] | None:
        """Public request handler. Delegates to _handle_sync for synchronous execution.
        
        Used by tests and any callers that expect synchronous responses.
        In production (run() method), requests are dispatched via thread pool instead.
        """
        return self._handle_sync(request)

    def _handle_initialize(
        self, req_id: Any, params: dict[str, Any]
    ) -> dict[str, Any]:
        # MCP 2025-11-25: always respond with our supported version.
        # The client's requested version (params.get("protocolVersion")) is
        # informational; we do not downgrade.
        return self._result(req_id, {
            "protocolVersion": self.PROTOCOL_VERSION,
            "capabilities": {
                "logging": {},
                "tools": {"listChanged": False},
            },
            "serverInfo": {
                "name": self.SERVER_NAME,
                "version": self.SERVER_VERSION,
            },
        })

    def _handle_tools_list(
        self, req_id: Any, params: dict[str, Any]
    ) -> dict[str, Any]:
        # MCP 2025-11-25: support cursor-based pagination.
        # All our tools fit in one page, so nextCursor is always absent.
        # We accept but ignore any incoming cursor.
        tools: list[dict[str, Any]] = []

        # Built-in IDE tools from registry — include annotations
        for schema in self._registry.schemas():
            entry: dict[str, Any] = {
                "name": schema.name,
                "description": schema.description,
                "inputSchema": schema.parameters,
            }
            if schema.name in _BUILTIN_ANNOTATIONS:
                entry["annotations"] = _BUILTIN_ANNOTATIONS[schema.name]
            tools.append(entry)

        # Workflow, agent, and A2A tools (annotations already embedded)
        tools.extend(_WORKFLOW_TOOLS)

        return self._result(req_id, {"tools": tools})

    def _handle_tools_call(
        self, req_id: Any, params: dict[str, Any]
    ) -> dict[str, Any]:
        # Check if this request was already cancelled
        with self._lock:
            if req_id in self._cancelled:
                self._cancelled.discard(req_id)
                return self._error(req_id, -32800, "Request cancelled")
            # Create a cancellation context for this request
            ctx = CancellationContext()
            self._cancellation_contexts[req_id] = ctx

        try:
            name = params.get("name", "")
            arguments = params.get("arguments") or {}

            # MCP 2025-11-25: extract progress token from _meta
            meta = params.get("_meta") or {}
            progress_token: Any = meta.get("progressToken")

            # Route workflow / agent / A2A tools
            workflow_names = {t["name"] for t in _WORKFLOW_TOOLS}
            if name in workflow_names:
                return self._handle_extended_call(req_id, name, arguments, progress_token, ctx)

            # Phase 2: pre-execution NCB gate for write/edit tools
            allow, reason = self._pre_tool_hook(name, arguments)
            if not allow:
                return self._result(req_id, {
                    "content": [{"type": "text", "text": reason}],
                    "isError": True,
                })

            # Snapshot pre-write content so LoRA gets a real bad→good sample
            pre_write_content = ""
            if name in ("write_file", "edit_file"):
                snap_path = arguments.get("path") or arguments.get("file_path")
                if snap_path:
                    try:
                        from pathlib import Path as _P
                        p = _P(snap_path)
                        if p.exists() and p.is_file() and p.stat().st_size < 512_000:
                            pre_write_content = p.read_text(encoding="utf-8", errors="replace")
                    except Exception:
                        pass

            result = self._registry.execute(name, **arguments)

            # Phase 2/3/5: post-execution gates (TCA record, CIE validate, LoRA capture)
            result = self._post_tool_hook(name, arguments, result, pre_write_content=pre_write_content)

            content: list[dict[str, str]] = []
            if result.success:
                content.append({"type": "text", "text": result.output})
            else:
                content.append({"type": "text", "text": result.error or "Unknown error"})

            return self._result(req_id, {
                "content": content,
                "isError": not result.success,
            })
        finally:
            # Clean up cancellation context
            with self._lock:
                self._cancellation_contexts.pop(req_id, None)

    def _handle_extended_call(
        self, req_id: Any, name: str, arguments: dict[str, Any],
        progress_token: Any = None,
        cancellation_context: CancellationContext | None = None,
    ) -> dict[str, Any]:
        """Handle workflow, agent, and A2A tool calls with optional progress reporting and cancellation."""
        try:
            if name == "phase0_recon":
                return self._call_phase0_recon(req_id, arguments, progress_token, cancellation_context)
            elif name == "context_pack":
                return self._call_context_pack(req_id, arguments, progress_token, cancellation_context)
            elif name == "context_memory_store":
                return self._call_context_memory_store(req_id, arguments, progress_token, cancellation_context)
            elif name == "context_memory_query":
                return self._call_context_memory_query(req_id, arguments, progress_token, cancellation_context)
            elif name == "map_terrain":
                return self._call_map_terrain(req_id, arguments, progress_token, cancellation_context)
            elif name == "trust_gate":
                return self._call_trust_gate(req_id, arguments, progress_token, cancellation_context)
            elif name == "certify_output":
                return self._call_certify_output(req_id, arguments, progress_token, cancellation_context)
            elif name == "safe_execute":
                return self._call_safe_execute(req_id, arguments, progress_token, cancellation_context)
            elif name == "ask_agent":
                return self._call_ask_agent(req_id, arguments, progress_token, cancellation_context)
            elif name == "a2a_validate":
                return self._call_a2a_validate(req_id, arguments)
            elif name == "a2a_negotiate":
                return self._call_a2a_negotiate(req_id, arguments)
            else:
                return self._error(req_id, -32602, f"Unknown extended tool: {name}")
        except Exception:
            _LOG.exception("Tool call failed: %s", name)
            return self._result(req_id, {
                "content": [{"type": "text", "text": "Tool execution failed. Check server logs for details."}],
                "isError": True,
            })

    # ── Progress helpers ──────────────────────────────────────────────────────

    def _emit_progress(
        self,
        token: Any,
        progress: float,
        total: float = 1.0,
        message: str = "",
    ) -> None:
        """Emit a notifications/progress message if a progress token was provided."""
        if token is None:
            return
        notification: dict[str, Any] = {
            "jsonrpc": "2.0",
            "method": "notifications/progress",
            "params": {
                "progressToken": token,
                "progress": progress,
                "total": total,
            },
        }
        if message:
            notification["params"]["message"] = message
        self._write(notification)

    def _emit_log(self, level: str, message: str) -> None:
        """Emit a notifications/message log entry (MCP 2025-11-25 logging capability)."""
        self._write({
            "jsonrpc": "2.0",
            "method": "notifications/message",
            "params": {"level": level, "data": message},
        })

    # ── Tool implementations ──────────────────────────────────────────────────

    def _get_nexus_client(self) -> Any:
        """Create a NexusClient from config, or raise if unavailable."""
        from ass_ade.config import load_config
        cfg = load_config()
        if cfg.profile == "local":
            raise RuntimeError("Workflow tools require hybrid or premium profile (current: local)")
        from ass_ade.nexus.client import NexusClient
        return NexusClient(
            base_url=cfg.nexus_base_url or "https://atomadic.tech",
            timeout=cfg.request_timeout_s,
            api_key=cfg.nexus_api_key,
        )

    def _call_map_terrain(
        self, req_id: Any, args: dict[str, Any], token: Any = None,
        cancellation_context: CancellationContext | None = None,
    ) -> dict[str, Any]:
        task_description = args.get("task_description", "")
        required = args.get("required_capabilities") or {}
        if not task_description:
            return self._error(req_id, -32602, "task_description is required")
        if not isinstance(required, dict):
            return self._error(req_id, -32602, "required_capabilities must be an object")

        self._emit_progress(token, 0.0, message="Mapping required capabilities...")
        
        # Cancellation checkpoint
        if cancellation_context and cancellation_context.check():
            return self._error(req_id, -32800, "Request cancelled")
        
        hosted_tools: list[str] = []
        try:
            client = self._get_nexus_client()
            with client:
                manifest = client.get_mcp_manifest()
            hosted_tools = [tool.name or "" for tool in manifest.tools]
        except Exception:
            hosted_tools = []

        self._emit_progress(token, 0.5, message="Checking local assets and hosted MCP tools...")
        from ass_ade.map_terrain import map_terrain

        result = map_terrain(
            task_description=task_description,
            required_capabilities=required,
            agent_id=args.get("agent_id", "ass-ade-local"),
            max_development_budget_usdc=float(args.get("max_development_budget_usdc", 1.0)),
            auto_invent_if_missing=bool(args.get("auto_invent_if_missing", False)),
            invention_constraints=args.get("invention_constraints") or {},
            working_dir=self._working_dir,
            hosted_tools=hosted_tools,
        )
        self._emit_progress(token, 1.0, message=f"MAP = TERRAIN verdict: {result.verdict}")
        text = json.dumps(result.model_dump(), indent=2)
        return self._result(req_id, {
            "content": [{"type": "text", "text": text}],
            "isError": result.verdict == "HALT_AND_INVENT",
        })

    def _call_phase0_recon(
        self, req_id: Any, args: dict[str, Any], token: Any = None,
        cancellation_context: CancellationContext | None = None,
    ) -> dict[str, Any]:
        task_description = args.get("task_description", "")
        if not task_description:
            return self._error(req_id, -32602, "task_description is required")

        provided_sources = args.get("provided_sources") or []
        if not isinstance(provided_sources, list):
            return self._error(req_id, -32602, "provided_sources must be an array")

        try:
            max_relevant_files = int(args.get("max_relevant_files", 20))
        except (TypeError, ValueError):
            return self._error(req_id, -32602, "max_relevant_files must be an integer")

        self._emit_progress(token, 0.0, message="Running Phase 0 codebase recon...")
        
        # Cancellation checkpoint
        if cancellation_context and cancellation_context.check():
            return self._error(req_id, -32800, "Request cancelled")
        
        from ass_ade.recon import phase0_recon

        result = phase0_recon(
            task_description=task_description,
            working_dir=self._working_dir,
            provided_sources=[str(source) for source in provided_sources],
            max_relevant_files=max_relevant_files,
        )
        self._emit_progress(token, 1.0, message=f"Phase 0 recon verdict: {result.verdict}")
        text = json.dumps(result.model_dump(), indent=2)
        return self._result(req_id, {
            "content": [{"type": "text", "text": text}],
            "isError": result.verdict == "RECON_REQUIRED",
        })

    def _call_context_pack(
        self, req_id: Any, args: dict[str, Any], token: Any = None,
        cancellation_context: CancellationContext | None = None,
    ) -> dict[str, Any]:
        task_description = args.get("task_description", "")
        if not task_description:
            return self._error(req_id, -32602, "task_description is required")

        file_paths = args.get("file_paths")
        source_urls = args.get("source_urls") or []
        if file_paths is not None and not isinstance(file_paths, list):
            return self._error(req_id, -32602, "file_paths must be an array")
        if not isinstance(source_urls, list):
            return self._error(req_id, -32602, "source_urls must be an array")

        self._emit_progress(token, 0.0, message="Building context packet...")
        
        # Cancellation checkpoint
        if cancellation_context and cancellation_context.check():
            return self._error(req_id, -32800, "Request cancelled")
        
        from ass_ade.context_memory import build_context_packet

        packet = build_context_packet(
            task_description=task_description,
            working_dir=self._working_dir,
            file_paths=[str(path) for path in file_paths] if file_paths else None,
            source_urls=[str(url) for url in source_urls],
            max_files=int(args.get("max_files", 12)),
            max_bytes_per_file=int(args.get("max_bytes_per_file", 4000)),
        )
        self._emit_progress(token, 1.0, message="Context packet ready.")
        text = json.dumps(packet.model_dump(), indent=2)
        return self._result(req_id, {
            "content": [{"type": "text", "text": text}],
            "isError": packet.recon_verdict == "RECON_REQUIRED",
        })

    def _call_context_memory_store(
        self, req_id: Any, args: dict[str, Any], token: Any = None,
        cancellation_context: CancellationContext | None = None,
    ) -> dict[str, Any]:
        text_value = args.get("text", "")
        if not text_value:
            return self._error(req_id, -32602, "text is required")
        metadata = args.get("metadata") or {}
        if not isinstance(metadata, dict):
            return self._error(req_id, -32602, "metadata must be an object")

        self._emit_progress(token, 0.0, message="Storing vector memory...")
        
        # Cancellation checkpoint
        if cancellation_context and cancellation_context.check():
            return self._error(req_id, -32800, "Request cancelled")
        
        from ass_ade.context_memory import store_vector_memory

        result = store_vector_memory(
            text=str(text_value),
            namespace=str(args.get("namespace") or "default"),
            metadata=metadata,
            working_dir=self._working_dir,
        )
        self._emit_progress(token, 1.0, message="Vector memory stored.")
        text = json.dumps(result.model_dump(), indent=2)
        return self._result(req_id, {
            "content": [{"type": "text", "text": text}],
            "isError": False,
        })

    def _call_context_memory_query(
        self, req_id: Any, args: dict[str, Any], token: Any = None,
        cancellation_context: CancellationContext | None = None,
    ) -> dict[str, Any]:
        query = args.get("query", "")
        if not query:
            return self._error(req_id, -32602, "query is required")

        self._emit_progress(token, 0.0, message="Querying vector memory...")
        
        # Cancellation checkpoint
        if cancellation_context and cancellation_context.check():
            return self._error(req_id, -32800, "Request cancelled")
        
        from ass_ade.context_memory import query_vector_memory

        result = query_vector_memory(
            query=str(query),
            namespace=str(args.get("namespace") or "default"),
            top_k=int(args.get("top_k", 5)),
            working_dir=self._working_dir,
        )
        self._emit_progress(token, 1.0, message="Vector memory query complete.")
        text = json.dumps(result.model_dump(), indent=2)
        return self._result(req_id, {
            "content": [{"type": "text", "text": text}],
            "isError": False,
        })

    def _call_trust_gate(
        self, req_id: Any, args: dict[str, Any], token: Any = None,
        cancellation_context: CancellationContext | None = None,
    ) -> dict[str, Any]:
        agent_id = args.get("agent_id", "")
        if not agent_id:
            return self._error(req_id, -32602, "agent_id is required")
        self._emit_progress(token, 0.0, message="Starting trust gate evaluation...")
        
        # Cancellation checkpoint
        if cancellation_context and cancellation_context.check():
            return self._error(req_id, -32800, "Request cancelled")
        
        from ass_ade.workflows import trust_gate
        client = self._get_nexus_client()
        self._emit_progress(token, 0.2, message="Verifying identity...")
        with client:
            self._emit_progress(token, 0.5, message="Running trust pipeline...")
            result = trust_gate(client, agent_id)
        self._emit_progress(token, 1.0, message="Trust gate complete.")
        text = json.dumps(result.model_dump(), indent=2)
        return self._result(req_id, {
            "content": [{"type": "text", "text": text}],
            "isError": result.verdict == "DENY",
        })

    def _call_certify_output(
        self, req_id: Any, args: dict[str, Any], token: Any = None,
        cancellation_context: CancellationContext | None = None,
    ) -> dict[str, Any]:
        text = args.get("text", "")
        if not text:
            return self._error(req_id, -32602, "text is required")
        self._emit_progress(token, 0.0, message="Starting output certification...")
        
        # Cancellation checkpoint
        if cancellation_context and cancellation_context.check():
            return self._error(req_id, -32800, "Request cancelled")
        
        from ass_ade.workflows import certify_output
        client = self._get_nexus_client()
        self._emit_progress(token, 0.2, message="Running hallucination oracle...")
        with client:
            self._emit_progress(token, 0.5, message="Running ethics and compliance checks...")
            result = certify_output(client, text)
        self._emit_progress(token, 1.0, message="Certification complete.")
        out = json.dumps(result.model_dump(), indent=2)
        return self._result(req_id, {
            "content": [{"type": "text", "text": out}],
            "isError": not result.passed,
        })

    def _call_safe_execute(
        self, req_id: Any, args: dict[str, Any], token: Any = None,
        cancellation_context: CancellationContext | None = None,
    ) -> dict[str, Any]:
        tool_name = args.get("tool_name", "")
        tool_input_str = args.get("tool_input", "{}")
        if not tool_name:
            return self._error(req_id, -32602, "tool_name is required")
        try:
            if isinstance(tool_input_str, str):
                tool_input = json.loads(tool_input_str)
            else:
                tool_input = tool_input_str
        except json.JSONDecodeError:
            return self._error(req_id, -32602, "tool_input must be valid JSON")
        self._emit_progress(token, 0.0, message="Starting AEGIS safe execute...")
        
        # Cancellation checkpoint
        if cancellation_context and cancellation_context.check():
            return self._error(req_id, -32800, "Request cancelled")
        
        from ass_ade.workflows import safe_execute
        client = self._get_nexus_client()
        self._emit_progress(token, 0.3, message="Running security shield and prompt scan...")
        with client:
            self._emit_progress(token, 0.6, message="Executing via AEGIS proxy...")
            result = safe_execute(client, tool_name, tool_input)
        self._emit_progress(token, 1.0, message="Safe execute complete.")
        out = json.dumps(result.model_dump(), indent=2)
        return self._result(req_id, {
            "content": [{"type": "text", "text": out}],
            "isError": not result.shield_passed,
        })

    def _call_ask_agent(
        self, req_id: Any, args: dict[str, Any], token: Any = None,
        cancellation_context: CancellationContext | None = None,
    ) -> dict[str, Any]:
        task = args.get("task", "")
        if not task:
            return self._error(req_id, -32602, "task is required")
        model = args.get("model")
        self._emit_progress(token, 0.0, message="Starting agent loop...")

        # Cancellation checkpoint
        if cancellation_context and cancellation_context.check():
            return self._error(req_id, -32800, "Request cancelled")

        from ass_ade.agent.loop import AgentLoop
        from ass_ade.config import load_config
        from ass_ade.engine.router import build_provider
        cfg = load_config()
        provider = build_provider(cfg)
        try:
            loop = AgentLoop(
                provider=provider,
                registry=self._registry,
                working_dir=self._working_dir,
                model=model,
            )
            self._emit_progress(token, 0.3, message="Agent planning...")
            text = loop.step(task)
            text = text if text else "(no response)"
            return self._result(req_id, {
                "content": [{"type": "text", "text": text}],
                "isError": False,
            })
        finally:
            provider.close()

    def _call_a2a_validate(self, req_id: Any, args: dict[str, Any]) -> dict[str, Any]:
        url = args.get("url", "")
        if not url:
            return self._error(req_id, -32602, "url is required")
        from ass_ade.nexus.validation import validate_url
        try:
            validate_url(url)
        except ValueError as e:
            return self._result(req_id, {
                "content": [{"type": "text", "text": f"Blocked: {e}"}],
                "isError": True,
            })
        from ass_ade.a2a import fetch_agent_card
        report = fetch_agent_card(url)
        issues = [
            {"severity": i.severity, "field": i.field, "message": i.message}
            for i in report.issues
        ]
        out = json.dumps({
            "valid": report.valid,
            "issues": issues,
            "card": report.card.model_dump() if report.card else None,
        }, indent=2)
        return self._result(req_id, {
            "content": [{"type": "text", "text": out}],
            "isError": not report.valid,
        })

    def _call_a2a_negotiate(self, req_id: Any, args: dict[str, Any]) -> dict[str, Any]:
        remote_url = args.get("remote_url", "")
        if not remote_url:
            return self._error(req_id, -32602, "remote_url is required")
        from ass_ade.nexus.validation import validate_url
        try:
            validate_url(remote_url)
        except ValueError as e:
            return self._result(req_id, {
                "content": [{"type": "text", "text": f"Blocked: {e}"}],
                "isError": True,
            })
        from ass_ade.a2a import fetch_agent_card, local_agent_card, negotiate
        local = local_agent_card(self._working_dir)
        report = fetch_agent_card(remote_url)
        if not report.valid or not report.card:
            messages = [issue.message for issue in report.errors]
            return self._result(req_id, {
                "content": [
                    {
                        "type": "text",
                        "text": f"Remote agent card is invalid: {messages}",
                    }
                ],
                "isError": True,
            })
        result = negotiate(local, report.card)
        out = json.dumps({
            "compatible": result.compatible,
            "shared_skills": result.shared_skills,
            "local_only": result.local_only,
            "remote_only": result.remote_only,
            "auth_compatible": result.auth_compatible,
            "notes": result.notes,
        }, indent=2)
        return self._result(req_id, {
            "content": [{"type": "text", "text": out}],
            "isError": not result.compatible,
        })

    # ── JSON-RPC helpers ──────────────────────────────────────────────────────

    @staticmethod
    def _result(req_id: Any, result: Any) -> dict[str, Any]:
        return {"jsonrpc": "2.0", "id": req_id, "result": result}

    @staticmethod
    def _error(req_id: Any, code: int, message: str) -> dict[str, Any]:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}}

    def _write(self, message: dict[str, Any]) -> None:
        data = json.dumps(message) + "\n"
        with self._write_lock:
            sys.stdout.write(data)
            sys.stdout.flush()

    def _write_error(self, req_id: Any, code: int, message: str) -> None:
        self._write(self._error(req_id, code, message))
