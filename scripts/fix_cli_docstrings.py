"""Fix escaped triple-quote docstrings and backslash dollar amounts in cli.py."""
import re

with open("src/ass_ade/cli.py", encoding="utf-8") as f:
    content = f.read()

original_len = len(content)

# Fix \""" -> """ (escaped triple quotes in docstrings)
content = content.replace('\\"\\"\\"', '"""')

# Also handle the pattern where backslash precedes each quote character individually
# e.g. \"\"\"text\"\"\" -> """text"""
content = re.sub(r'\\"\\"\\"(.*?)\\"\\"\\"', r'"""\1"""', content, flags=re.DOTALL)

# Fix \. followed by digits in docstrings (e.g. \.040 -> $0.040)
content = re.sub(r'\\\.(\d)', r'$0.\1', content)

with open("src/ass_ade/cli.py", "w", encoding="utf-8") as f:
    f.write(content)

print(f"Fixed file ({original_len} -> {len(content)} chars)")

import py_compile
try:
    py_compile.compile("src/ass_ade/cli.py", doraise=True)
    print("Syntax OK")
except py_compile.PyCompileError as e:
    print(f"Syntax error: {e}")
    # Show the problematic line
    lines = content.splitlines()
    import re as re2
    m = re2.search(r'line (\d+)', str(e))
    if m:
        lineno = int(m.group(1))
        for i in range(max(0, lineno-3), min(len(lines), lineno+3)):
            print(f"  {i+1}: {lines[i]!r}")
