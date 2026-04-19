# Features

Extracted from 151 source files.

### `hooks\post_rebuild.py`

- **function** `run`
### `hooks\post_rebuild_collect_training.py`

- **function** `run`
- **function** `_count_lines`
### `hooks\post_rebuild_context_load.py`

- **function** `_collect_components`
- **function** `_build_context_map`
- **function** `run`
### `hooks\post_rebuild_docs.py`

- **function** `run`
### `hooks\post_rebuild_eco_scan.py`

- **function** `run`
### `hooks\pre_rebuild.py`

- **function** `run`
### `hooks\pre_rebuild_validate.py`

- **function** `_validate_blueprint`
- **function** `run`
### `scripts\fix_a2a_and_pipeline.py`

- **function** `a2a_validate`
- **function** `a2a_negotiate`
- **function** `a2a_discover`
- **function** `a2a_validate`
- **function** `a2a_negotiate`
- **function** `a2a_discover`
- **function** `a2a_validate`
- **function** `a2a_negotiate`
- **function** `a2a_discover`
### `scripts\lora_train.py`

- **class** `TrainConfig`
- **function** `fetch_samples`
- **function** `train_adapter`
- **function** `_format`
- **function** `_tok`
- **function** `upload_adapter`
- **function** `_upload_hf`
- **function** `_upload_r2`
- **function** `promote_adapter`
- **function** `run_pipeline`
- **function** `_parse_args`
- **function** `main`
### `scripts\probe_endpoints.py`

- **function** `probe`
- **function** `run_all`
- **function** `section`
- **function** `_ratchet_flow`
- **function** `_rng`
- **function** `_vrf`
- **function** `_create_escrow`
- **function** `_sla_reg`
- **function** `_cs_create`
- **function** `_qt_create`
- **function** `_saga_create`
- **function** `_fence_create`
- **function** `_certify`
- **function** `_mev_protect`
- **function** `print_summary`
- **function** `main`
### `scripts\run_aaaa_nexus_mcp.py`

- **function** `_load_env_file`
- **function** `_prepare_environment`
- **function** `_probe`
- **function** `main`
### `scripts\hf_space\app.py`

- **function** `run_training`
### `scripts\lora_training\collect_training_data.py`

- **function** `_emit`
- **function** `_from_certificate`
- **function** `_from_markdown_report`
- **function** `_from_benchmarks`
- **function** `_from_cycle_report_md`
- **function** `_from_cycle_report_json`
- **function** `_from_reports_dir`
- **function** `_from_conversation_history`
- **function** `_from_lora_buffer`
- **function** `_dedup`
- **function** `collect`
- **function** `main`
### `scripts\lora_training\serve_lora.py`

- **class** `_Model`
- **function** `__init__`
- **function** `_load`
- **function** `ensure_loaded`
- **function** `generate`
- **function** `_make_handler`
- **class** `_Handler`
- **function** `log_message`
- **function** `_send_json`
- **function** `do_GET`
- **function** `do_POST`
- **function** `serve`
- **function** `main`
### `scripts\lora_training\train_lora.py`

- **function** `_load_samples`
- **function** `_format_sample`
- **function** `train`
- **function** `_tokenize`
- **function** `main`
- **function** `print_colab_instructions`
### `src\ass_ade\cli.py`

- **function** `_app_callback`
- **function** `interpreter_chat`
- **function** `memory_show`
- **function** `memory_clear`
- **function** `memory_export`
- **function** `_resolve_config`
- **function** `_redact_secrets`
- **function** `_print_json`
- **function** `_should_probe_remote`
- **function** `_require_remote_access`
- **function** `init`
- **function** `doctor`
- **function** `credits`
- **function** `plan`
- **function** `full_cycle`
- **function** `repo_summary`
- **function** `protocol_run`
- **function** `nexus_health`
- **function** `nexus_agent_card`
- **function** `nexus_mcp_manifest`
- **function** `mcp_tools`
- **function** `mcp_inspect`
- **function** `mcp_invoke`
- **function** `mcp_estimate_cost`
- **function** `mcp_mock_server`
- **function** `mcp_serve`
- **function** `nexus_overview`
- **function** `_nexus_err`
- **function** `_draw_progress_bar`
- **function** `_finish_progress_bar`
- **function** `_auto_detect_project`
- **function** `oracle_hallucination`
- **function** `oracle_trust_phase`
- **function** `oracle_entropy`
- **function** `pipeline_run`
- **function** `on_progress`
- **function** `pipeline_status`
- **function** `pipeline_history`
- **function** `oracle_trust_decay`
- **function** `ratchet_register`
- **function** `ratchet_advance`
- **function** `ratchet_status`
- **function** `trust_score`
- **function** `trust_history`
- **function** `text_summarize`
- **function** `text_keywords`
- **function** `text_sentiment`
- **function** `security_threat_score`
- **function** `security_prompt_scan`
- **function** `security_shield`
- **function** `security_pqc_sign`
- **function** `llm_chat`
- **function** `llm_stream`
- **function** `escrow_create`
- **function** `escrow_release`
- **function** `escrow_status`
- **function** `escrow_dispute`
- **function** `escrow_arbitrate`
- **function** `reputation_record`
- **function** `reputation_score`
- **function** `reputation_history`
- **function** `sla_register`
- **function** `sla_report`
- **function** `sla_status`
- **function** `sla_breach`
- **function** `discovery_search`
- **function** `discovery_recommend`
- **function** `discovery_registry`
- **function** `swarm_plan`
- **function** `swarm_relay`
- **function** `swarm_intent_classify`
- **function** `swarm_token_budget`
- **function** `swarm_contradiction`
- **function** `swarm_semantic_diff`
- **function** `compliance_check`
- **function** `compliance_eu_ai_act`
- **function** `compliance_fairness`
- **function** `compliance_drift_check`
- **function** `compliance_drift_cert`
- **function** `compliance_incident`
- **function** `defi_optimize`
- **function** `defi_risk_score`
- **function** `defi_oracle_verify`
- **function** `defi_liquidation_check`
- **function** `defi_bridge_verify`
- **function** `defi_yield_optimize`
- **function** `aegis_mcp_proxy`
- **function** `aegis_epistemic_route`
- **function** `aegis_certify_epoch`
- **function** `control_authorize`
- **function** `control_spending_authorize`
- **function** `control_spending_budget`
- **function** `control_lineage_record`
- **function** `control_lineage_trace`
- **function** `control_federation_mint`
- **function** `identity_verify`
- **function** `identity_sybil_check`
- **function** `identity_delegate_verify`
- **function** `vrf_draw`
- **function** `vrf_verify`
- **function** `bitnet_models`
- **function** `bitnet_chat`
- **function** `bitnet_stream`
- **function** `bitnet_benchmark`
- **function** `bitnet_status`
- **function** `vanguard_redteam`
- **function** `vanguard_mev_route`
- **function** `vanguard_govern_session`
- **function** `vanguard_lock_and_verify`
- **function** `mev_protect`
- **function** `mev_status`
- **function** `forge_leaderboard`
- **function** `forge_verify`
- **function** `forge_quarantine`
- **function** `forge_delta_submit`
- **function** `forge_badge`
- **function** `dev_starter`
- **function** `dev_crypto_toolkit`
- **function** `dev_routing_think`
- **function** `data_validate_json`
- **function** `data_format_convert`
- **function** `prompt_hash_command`
- **function** `prompt_validate_command`
- **function** `prompt_section_command`
- **function** `prompt_diff_command`
- **function** `prompt_propose_command`
- **function** `context_pack_command`
- **function** `context_store_command`
- **function** `context_query_command`
- **function** `a2a_local_card`
- **function** `pipeline_trust_gate`
- **function** `_progress`
- **function** `pipeline_certify`
- **function** `_progress`
- **function** `security_zero_day_scan`
- **function** `inference_token_count`
- **function** `data_convert`
- **function** `vanguard_epoch_certify`
- **function** `vanguard_wallet_session`
- **function** `pay`
- **function** `wallet`
- **function** `search`
- **function** `sam_status`
- **function** `wisdom_report`
- **function** `tca_status`
- **function** `eco_scan`
- **function** `_iter_py_eco`
- **function** `_parse_imports_eco`
- **function** `recon_command`
- **function** `_generate_rebuild_docs`
- **function** `_run_help`
- **function** `_scan_py_dir`
- **function** `_scan_dir_names`
- **function** `_scan_md_dir`
- **function** `_bullet_list`
- **function** `rebuild_codebase`
- **function** `_progress_cb`
- **function** `rollback_command`
- **function** `enhance_command`
- **function** `docs_command`
- **function** `lint_command`
- **function** `certify_command`
- **function** `design_command`
- **function** `_make_slug`
- **function** `_make_local_blueprint`
- **function** `_run_single`
- **function** `lora_train`
- **function** `lora_credit`
- **function** `lora_status`
- **function** `setup_command`
- **function** `tutorial_command`
- **function** `doStuff`
- **function** `another_function_with_too_many_lines`
- **class** `Config`
- **function** `__init__`
- **function** `read_file`
- **function** `save_data`
- **function** `compute`
- **function** `local_train`
### `src\ass_ade\config.py`

- **class** `ProviderOverride`
- **class** `AssAdeConfig`
- **function** `default_config_path`
- **function** `load_config`
- **function** `_hydrate_env_file`
- **function** `write_default_config`
### `src\ass_ade\context_memory.py`

- **class** `ContextFile`
- **class** `ContextPacket`
- **class** `VectorMemoryRecord`
- **class** `VectorMemoryStoreResult`
- **class** `VectorMemoryMatch`
- **class** `VectorMemoryQueryResult`
- **function** `_tokens`
- **function** `vector_embed`
- **function** `_memory_path`
- **function** `_safe_file`
- **function** `_read_excerpt`
- **function** `build_context_packet`
- **function** `store_vector_memory`
- **function** `_iter_memory`
- **function** `_dot`
- **function** `query_vector_memory`
### `src\ass_ade\interpreter.py`

- **function** `_load_env`
- **function** `_pick_endpoint`
- **function** `_call_llm`
- **class** `MemoryStore`
- **function** `__post_init__`
- **function** `load`
- **function** `save`
- **function** `clear`
- **function** `to_dict`
- **function** `append_history`
- **function** `recent_history`
- **function** `update_from_turn`
- **function** `greeting`
- **function** `summarize`
- **function** `_detect_tone`
- **function** `_classify_intent`
- **function** `_extract_path`
- **function** `_substitute_datetime_tokens`
- **class** `Turn`
- **class** `Atomadic`
- **function** `process`
- **function** `_dispatch`
- **function** `_execute_self_enhance`
- **function** `describe_self`
- **function** `_build_command`
- **function** `_print_dispatch`
- **function** `_run_streaming`
- **function** `_execute`
- **function** `_execute_rebuild_pipeline`
- **function** `_rollback`
- **function** `_hot_patch`
- **function** `_extract_feature_desc`
- **function** `_ask_clarification`
- **function** `_prelude`
- **function** `_postlude`
- **function** `run_interactive`
### `src\ass_ade\map_terrain.py`

- **class** `MissingCapability`
- **class** `DevelopmentPlan`
- **class** `MapTerrainResult`
- **function** `_coerce_required_names`
- **function** `_slug`
- **function** `_normalize_type`
- **function** `_load_asset_memory`
- **function** `build_capability_inventory`
- **function** `_specification`
- **function** `_verification_criteria`
- **function** `_persist_development_plan`
- **function** `map_terrain`
- **class** `InventionStub`
- **class** `ActiveTerrainVerdict`
- **function** `_write_invention_stub`
- **function** `active_terrain_gate`
### `src\ass_ade\pipeline.py`

- **class** `StepStatus`
- **class** `StepResult`
- **class** `PipelineResult`
- **function** `failed_steps`
- **function** `summary`
- **class** `StepFunction`
- **function** `__call__`
- **class** `_StepEntry`
- **class** `Pipeline`
- **function** `__init__`
- **function** `name`
- **function** `step_names`
- **function** `add`
- **function** `run`
- **function** `_persist`
- **function** `trust_gate_pipeline`
- **function** `identity_step`
- **function** `sybil_step`
- **function** `trust_step`
- **function** `reputation_step`
- **function** `gate_step`
- **function** `certify_pipeline`
- **function** `hallucination_step`
- **function** `ethics_step`
- **function** `compliance_step`
- **function** `certify_step`
### `src\ass_ade\prompt_toolkit.py`

- **class** `PromptArtifact`
- **class** `PromptHashResult`
- **class** `PromptValidateResult`
- **class** `PromptSectionResult`
- **class** `PromptDiffResult`
- **class** `PromptProposalResult`
- **function** `_resolve_under`
- **function** `load_prompt_artifact`
- **function** `prompt_hash`
- **function** `_extract_expected_hash`
- **function** `prompt_validate`
- **function** `_markdown_section`
- **function** `_xml_section`
- **function** `prompt_section`
- **function** `_redact_line`
- **function** `prompt_diff`
- **function** `prompt_propose`
### `src\ass_ade\recon.py`

- **class** `ResearchTarget`
- **class** `CodebaseRecon`
- **class** `Phase0ReconResult`
- **function** `_tokens`
- **function** `_is_technical`
- **function** `_walk_files`
- **function** `_score_file`
- **function** `_suggest_research`
- **function** `_rel`
- **function** `phase0_recon`
- **function** `_iter_files`
- **function** `_scout_agent`
- **function** `_parse_imports`
- **function** `_dependency_agent`
- **function** `_dfs`
- **function** `_bfs_depth`
- **function** `_classify_tier`
- **function** `_tier_agent`
- **function** `_count_test_functions`
- **function** `_test_agent`
- **function** `_has_docstring`
- **function** `_doc_agent`
- **class** `ReconReport`
- **function** `summary`
- **function** `to_markdown`
- **function** `to_dict`
- **function** `_build_recommendations`
- **function** `run_parallel_recon`
### `src\ass_ade\system.py`

- **class** `ToolStatus`
- **function** `detect_tool`
- **function** `collect_tool_status`
### `src\ass_ade\workflows.py`

- **class** `TrustGateStep`
- **class** `TrustGateResult`
- **class** `CertifyResult`
- **class** `SafeExecuteResult`
- **function** `trust_gate`
- **function** `certify_output`
- **function** `safe_execute`
### `src\ass_ade\a2a\__init__.py`

- **function** `_check_ssrf`
- **class** `A2ASkill`
- **class** `A2AAuthentication`
- **class** `A2AProvider`
- **class** `A2ACapabilities`
- **class** `A2AAgentCard`
- **function** `name_not_empty`
- **class** `ValidationIssue`
- **class** `ValidationReport`
- **function** `errors`
- **function** `warnings`
- **function** `validate_agent_card`
- **function** `fetch_agent_card`
- **class** `NegotiationResult`
- **function** `negotiate`
- **function** `local_agent_card`
### `src\ass_ade\agent\alphaverus.py`

- **class** `VerifiedCode`
- **function** `_ast_parses`
- **function** `_cyclomatic_complexity`
- **function** `_owasp_regex_scan`
- **function** `_tokenize`
- **function** `_semantic_distance`
- **function** `_run_pytest_if_exists`
- **function** `_score`
- **function** `_passes`
- **class** `AlphaVerus`
- **function** `__init__`
- **function** `verify`
- **function** `_mutations`
- **function** `tree_search`
- **function** `run`
- **function** `report`
### `src\ass_ade\agent\atlas.py`

- **class** `SubTask`
- **class** `Atlas`
- **function** `__init__`
- **function** `complexity_score`
- **function** `decompose`
- **function** `run`
- **function** `report`
### `src\ass_ade\agent\bas.py`

- **class** `Alert`
- **class** `BAS`
- **function** `__init__`
- **function** `_load_alert_count`
- **function** `_persist_alert`
- **function** `subscribe`
- **function** `_notify_subscribers`
- **function** `alert`
- **function** `monitor`
- **function** `monitor_all`
- **function** `flush_alerts`
- **function** `run`
- **function** `report`
### `src\ass_ade\agent\cie.py`

- **class** `CIEResult`
- **class** `CIEPipeline`
- **function** `__init__`
- **function** `run`
- **function** `_run_inner`
- **function** `_verify_ast_python`
- **function** `_lint_gate`
- **function** `_run_ruff`
- **function** `_apply_minimal_patch`
- **function** `_owasp_scan`
- **function** `_alphaverus_gate`
- **function** `_proofbridge_stub`
- **function** `report`
