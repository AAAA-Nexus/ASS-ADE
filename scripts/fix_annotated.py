"""Fix Annotated[..., CONFIG_OPTION/ALLOW_REMOTE_OPTION] usage to plain assignment style."""
import re

with open("src/ass_ade/cli.py", encoding="utf-8") as f:
    content = f.read()

# Replace: config: Annotated[Path | None, CONFIG_OPTION] = None,
# With:    config: Path | None = CONFIG_OPTION,
content = re.sub(
    r'(\s+)config: Annotated\[Path \| None, CONFIG_OPTION\] = None,',
    r'\1config: Path | None = CONFIG_OPTION,',
    content
)

# Replace: allow_remote: Annotated[bool, ALLOW_REMOTE_OPTION] = False,
# With:    allow_remote: bool = ALLOW_REMOTE_OPTION,
content = re.sub(
    r'(\s+)allow_remote: Annotated\[bool, ALLOW_REMOTE_OPTION\] = False,',
    r'\1allow_remote: bool = ALLOW_REMOTE_OPTION,',
    content
)

# Replace: json_out: Annotated[Path | None, ...] patterns with explicit Option
# (Only do safe replacements that match exact patterns)
content = re.sub(
    r'(\s+)json_out: Annotated\[Path \| None, typer\.Option\(None, help="Write result JSON to this path\."\)\] = None,',
    r'\1json_out: Path | None = typer.Option(None, help="Write result JSON to this path."),',
    content
)

with open("src/ass_ade/cli.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Done")

import py_compile
try:
    py_compile.compile("src/ass_ade/cli.py", doraise=True)
    print("Syntax OK")
except py_compile.PyCompileError as e:
    print(f"Syntax error: {e}")
