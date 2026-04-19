# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testpipelinerun.py:187
# Component id: og.source.ass_ade.test_pipeline_history_lists_workflows
__version__ = "0.1.0"

    def test_pipeline_history_lists_workflows(self, tmp_path: Path) -> None:
        """Pipeline history should list recent workflows."""
        workflow_dir = tmp_path / ".ass-ade" / "workflows"
        workflow_dir.mkdir(parents=True, exist_ok=True)
        
        # Create several workflow files
        for i in range(3):
            workflow_data = {
                "name": f"test-workflow-{i}",
                "passed": i % 2 == 0,
                "duration_ms": 500 + i * 100,
            }
            workflow_file = workflow_dir / f"workflow-{i:03d}.json"
            workflow_file.write_text(json.dumps(workflow_data), encoding="utf-8")
        
        with patch("pathlib.Path.cwd", return_value=tmp_path):
            result = runner.invoke(
                app,
                ["pipeline", "history", "--limit", "5"],
            )
        
        # History should display a table with workflows
        assert result.exit_code == 0, f"History failed:\n{result.stdout}"
        # Should show table or list of workflows
        assert "test-workflow" in result.stdout or "History" in result.stdout or "Workflow" in result.stdout
