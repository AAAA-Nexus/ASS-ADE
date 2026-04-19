# Extracted from C:/!ass-ade/src/ass_ade/protocol/evolution.py:652
# Component id: at.source.ass_ade.render_branch_evolution_demo
from __future__ import annotations

__version__ = "0.1.0"

def render_branch_evolution_demo(
    *,
    root: Path,
    branches: Iterable[str],
    iterations: int,
) -> str:
    root = root.resolve()
    tracks = normalize_branch_tracks(branches)
    iterations = max(1, iterations)
    version = read_project_version(root)
    lines = [
        "# Split-Branch Evolution Workflow",
        "",
        "This demo shows how ASS-ADE can evolve along several public-safe branches,",
        "record evidence for each path, then merge the strongest line after review.",
        "",
        "## Baseline",
        "",
        "```bash",
        "ass-ade doctor",
        "python -m pytest tests/ -q --no-header",
        (
            "ass-ade protocol evolution-record baseline "
            "--summary \"Baseline before branch evolution\" "
            "--command \"ass-ade doctor\" "
            "--command \"python -m pytest tests/ -q --no-header\""
        ),
        "```",
        "",
        "## Branch Tracks",
        "",
    ]
    for track in tracks:
        short = track.split("/", 1)[-1]
        lines.extend(
            [
                f"### `{track}`",
                "",
                "```bash",
                f"git switch -c {track}",
            ]
        )
        for index in range(1, iterations + 1):
            lines.extend(
                [
                    f"ass-ade context pack \"evolution {short} iteration {index}\" --path . --json",
                    (
                        "ass-ade design "
                        f"\"{short} iteration {index}: improve the strongest measured gap\" "
                        "--path . --local-only --out "
                        f"blueprints/{short}-iteration-{index}.json"
                    ),
                    "ass-ade enhance . --local-only --json --limit 10",
                    "ass-ade rebuild . --yes --git-track",
                    "python -m pytest tests/ -q --no-header",
                    (
                        "ass-ade protocol evolution-record iteration "
                        f"--summary \"{short} iteration {index}\" "
                        f"--version {version} "
                        f"--artifact blueprints/{short}-iteration-{index}.json "
                        "--command \"ass-ade context pack\" "
                        "--command \"ass-ade design\" "
                        "--command \"ass-ade enhance\" "
                        "--command \"ass-ade rebuild . --yes --git-track\" "
                        "--command \"python -m pytest tests/ -q --no-header\""
                    ),
                ]
            )
        lines.extend(["git switch -", "```", ""])

    lines.extend(
        [
            "## Compare And Merge",
            "",
            "```bash",
            "git log --oneline --graph --all --decorate",
            "ass-ade protocol evolution-record merge-candidate --summary \"Compare branch evidence\"",
            "git switch main",
            "# Merge the branch with passing tests, fresh docs, and the strongest evidence ledger.",
            "git merge --no-ff evolve/tests-first",
            "python -m pytest tests/ -q --no-header",
            (
                "ass-ade protocol evolution-record merge "
                "--summary \"Merged selected evolution branch\" "
                "--command \"git merge --no-ff <branch>\" "
                "--command \"python -m pytest tests/ -q --no-header\""
            ),
            "```",
            "",
            "## Merge Rule",
            "",
            "A branch is merge-ready only when tests pass, public docs are current,",
            "`EVOLUTION.md` has the event trail, and any release needs a fresh certificate.",
            "",
            "## Version Rule",
            "",
            "Use `ass-ade protocol version-bump patch|minor|major` after the winning path is merged.",
            "The command updates package version surfaces and records the bump in the evolution ledger.",
        ]
    )
    return "\n".join(lines)
