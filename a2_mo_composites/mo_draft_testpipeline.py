# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_pipeline.py:49
# Component id: mo.source.ass_ade.testpipeline
__version__ = "0.1.0"

class TestPipeline:
    def test_empty_pipeline_fails(self) -> None:
        pipe = Pipeline("empty")
        result = pipe.run()
        assert not result.passed
        assert len(result.steps) == 0

    def test_single_passing_step(self) -> None:
        pipe = Pipeline("single")
        pipe.add("step1", pass_step)
        result = pipe.run()
        assert result.passed
        assert len(result.steps) == 1
        assert result.steps[0].status == StepStatus.PASSED

    def test_single_failing_step(self) -> None:
        pipe = Pipeline("fail")
        pipe.add("step1", fail_step)
        result = pipe.run()
        assert not result.passed
        assert result.steps[0].status == StepStatus.FAILED
        assert result.steps[0].error == "something broke"

    def test_context_flows_through_steps(self) -> None:
        pipe = Pipeline("context")
        pipe.add("count1", counting_step)
        pipe.add("count2", counting_step)
        result = pipe.run()
        assert result.passed
        assert result.context["count"] == 2

    def test_initial_context_is_available(self) -> None:
        pipe = Pipeline("initial")
        pipe.add("reader", context_reader)
        result = pipe.run({"message": "hello"})
        assert result.passed
        assert result.context["reader"]["read_message"] == "hello"

    def test_chaining_add(self) -> None:
        pipe = Pipeline("chain")
        returned = pipe.add("s1", pass_step).add("s2", pass_step)
        assert returned is pipe
        assert len(pipe.step_names) == 2
