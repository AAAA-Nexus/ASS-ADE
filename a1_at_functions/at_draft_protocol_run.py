# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_protocol_run.py:7
# Component id: at.source.a1_at_functions.protocol_run
from __future__ import annotations

__version__ = "0.1.0"

def protocol_run(
    goal: str = typer.Argument(..., help="Enhancement goal for the protocol cycle."),
    config: Path | None = CONFIG_OPTION,
    path: Path = REPO_PATH_OPTION,
    markdown: bool = typer.Option(False, help="Render the protocol report as Markdown."),
) -> None:
    _, settings = _resolve_config(config)
    report = run_protocol(goal, path, settings)

    if markdown:
        console.print(render_protocol_markdown(report))
        return

    overview = Table(title="ASS-ADE Protocol Report")
    overview.add_column("Signal")
    overview.add_column("Value")
    overview.add_row("Goal", report.goal)
    overview.add_row("Profile", report.assessment.profile)
    overview.add_row("Root", report.assessment.root)
    overview.add_row("Files", str(report.assessment.total_files))
    overview.add_row("Directories", str(report.assessment.total_dirs))
    overview.add_row("Audit Checks", str(len(report.audit)))
    console.print(overview)

    design = Table(title="Design Steps")
    design.add_column("#", justify="right")
    design.add_column("Step")
    for index, step in enumerate(report.design_steps, start=1):
        design.add_row(str(index), step)
    console.print(design)

    audit = Table(title="Audit")
    audit.add_column("Status")
    audit.add_column("Check")
    audit.add_column("Detail")
    for item in report.audit:
        audit.add_row("PASS" if item.passed else "FAIL", item.name, item.detail)
    console.print(audit)

    recommendations = Table(title="Recommendations")
    recommendations.add_column("#", justify="right")
    recommendations.add_column("Recommendation")
    for index, item in enumerate(report.recommendations, start=1):
        recommendations.add_row(str(index), item)
    console.print(recommendations)

    console.print(report.summary)
