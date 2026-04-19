# Extracted from C:/!ass-ade/src/ass_ade/cli.py:6872
# Component id: at.source.ass_ade.tutorial_command
from __future__ import annotations

__version__ = "0.1.0"

def tutorial_command() -> None:
    """Interactive 2-minute demo — rebuild, enhance, docs, and certify a sample project.

    Creates a small messy demo project in a temp directory and walks you
    through the full ASS-ADE workflow: rebuild → enhance → docs → certify.
    Uses the free LLM tier — costs nothing.
    """
    import json as _json
    import shutil as _shutil
    import tempfile as _tmp

    console.print("\n[bold cyan]ASS-ADE Tutorial[/bold cyan]")
    console.print("[dim]2-minute interactive demo. Press Ctrl+C at any time to stop.[/dim]\n")

    # --- Create a messy demo project ---
    tmpdir = Path(_tmp.mkdtemp(prefix="ass-ade-demo-"))
    console.print(f"[dim]Demo project at: {tmpdir}[/dim]\n")

    (tmpdir / "main.py").write_text("""\
# messy demo app
import os, sys, json, pickle

def doStuff(x, y, z):
    # does stuff
    try:
        data = pickle.loads(x)  # unsafe
        result = eval(y)  # unsafe
        return data, result
    except:
        pass

def another_function_with_too_many_lines():
    a = 1; b = 2; c = 3; d = 4; e = 5
    f = 6; g = 7; h = 8; i = 9; j = 10
    k = 11; l = 12; m = 13; n = 14; o = 15
    p = 16; q = 17; r = 18; s = 19; t = 20
    return a+b+c+d+e+f+g+h+i+j+k+l+m+n+o+p+q+r+s+t

class Config:
    def __init__(self):
        self.secret = "hardcoded_secret_12345"
        self.db = "sqlite:///local.db"
""", encoding="utf-8")

    (tmpdir / "utils.py").write_text("""\
import os

def read_file(path):
    # TODO: add error handling
    return open(path).read()

def save_data(obj, filename):
    import pickle
    with open(filename, 'wb') as f:
        pickle.dump(obj, f)

def compute(n):
    # FIXME: this is slow
    return sum(range(n))
""", encoding="utf-8")

    (tmpdir / "README.md").write_text("# Demo App\n\nA messy codebase.\n", encoding="utf-8")

    console.print("[bold]Step 1: Scan for enhancement opportunities[/bold]")
    console.print(f"[dim]$ ass-ade enhance {tmpdir} --local-only[/dim]")
    typer.confirm("Run this step?", default=True, abort=True)

    import subprocess as _sp
    r1 = _sp.run(
        [sys.executable, "-m", "ass_ade", "enhance", str(tmpdir), "--local-only"],
        capture_output=False,
    )
    console.print()

    console.print("[bold]Step 2: Generate documentation[/bold]")
    console.print(f"[dim]$ ass-ade docs {tmpdir} --local-only[/dim]")
    typer.confirm("Run this step?", default=True, abort=True)

    r2 = _sp.run(
        [sys.executable, "-m", "ass_ade", "docs", str(tmpdir), "--local-only"],
        capture_output=False,
    )
    console.print()

    console.print("[bold]Step 3: Certify the codebase[/bold]")
    console.print(f"[dim]$ ass-ade certify {tmpdir}[/dim]")
    typer.confirm("Run this step?", default=True, abort=True)

    r3 = _sp.run(
        [sys.executable, "-m", "ass_ade", "certify", str(tmpdir)],
        capture_output=False,
    )
    console.print()

    console.print("[bold]Step 4: Run the lint pipeline[/bold]")
    console.print(f"[dim]$ ass-ade lint {tmpdir}[/dim]")
    typer.confirm("Run this step?", default=True, abort=True)

    r4 = _sp.run(
        [sys.executable, "-m", "ass_ade", "lint", str(tmpdir)],
        capture_output=False,
    )
    console.print()

    # --- Summary ---
    console.print("[bold green]Tutorial complete![/bold green]")
    console.print(f"\nDemo files are at: [bold]{tmpdir}[/bold]")
    console.print()
    console.print(
        "[bold]Now point ASS-ADE at your own repo:[/bold]\n"
        "  [cyan]ass-ade enhance ./your-project[/cyan]               # find improvements\n"
        "  [cyan]ass-ade rebuild ./your-project ./clean-output[/cyan] # full monadic rebuild\n"
        "  [cyan]ass-ade docs ./your-project[/cyan]                   # generate docs\n"
        "  [cyan]ass-ade certify ./your-project[/cyan]                # sign the codebase\n"
    )
    keep = typer.confirm("Keep the demo files?", default=False)
    if not keep:
        _shutil.rmtree(tmpdir, ignore_errors=True)
