"""
Deduplicate cli.py by keeping only the first occurrence of each Typer command function.

Strategy:
1. Parse the file into "chunks" (sections of code between blank lines or decorator boundaries)
2. Track (app_name, command_name) pairs seen
3. Keep first occurrence, discard duplicates
4. Also fix corrupt console.print(table) lines
"""
import re
import sys

INPUT = "src/ass_ade/cli.py"
OUTPUT = "src/ass_ade/cli.py"

# Read the file
with open(INPUT, encoding="utf-8", errors="replace") as f:
    lines = f.readlines()

print(f"Input: {len(lines)} lines")

# Fix known corrupt patterns in individual lines FIRST
fixed_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    # Fix corrupt console.print(table) lines - strip trailing garbage
    # Pattern: console.print(table)GARBAGE where GARBAGE is not just whitespace/newline
    stripped = line.rstrip('\n\r')
    if re.match(r'^\s+console\.print\(table\)\S', stripped):
        fixed_lines.append('    console.print(table)\n')
        i += 1
        continue
    # Fix corrupt ]Error reading... line (appears after _print_json(result))
    if stripped.startswith(']Error reading workflow:'):
        # This is a stray fragment - skip it
        i += 1
        continue
    fixed_lines.append(line)
    i += 1

lines = fixed_lines
print(f"After line-level fixes: {len(lines)} lines")

# Now split into "function blocks"
# A block starts at a decorator (@xxx_app.command(...)) and ends before the next decorator
# or before a section comment (# ===... or # ---...)

COMMAND_RE = re.compile(r'^@(\w+)\.command\("([^"]+)"\)')
SECTION_RE = re.compile(r'^# [=─-]{5,}')
DEF_RE = re.compile(r'^def ')

# Parse into segments
# Each segment is a list of lines that belong together
segments = []
current_segment = []
current_key = None  # (app_name, command_name) for command segments, None for others

for line in lines:
    m = COMMAND_RE.match(line)
    if m:
        # Start of a new command segment
        if current_segment:
            segments.append((current_key, current_segment))
        current_key = (m.group(1), m.group(2))
        current_segment = [line]
    else:
        current_segment.append(line)

if current_segment:
    segments.append((current_key, current_segment))

print(f"Total segments: {len(segments)}")
command_segments = [(k, s) for k, s in segments if k is not None]
print(f"Command segments: {len(command_segments)}")

# Count duplicates
from collections import Counter
key_counts = Counter(k for k, s in command_segments)
dupes = {k: v for k, v in key_counts.items() if v > 1}
print(f"Duplicate commands: {len(dupes)}")
for k, v in sorted(dupes.items(), key=lambda x: -x[1])[:15]:
    print(f"  {v}x  {k[0]}.{k[1]}")

# Deduplicate: keep first occurrence of each key
seen_keys = set()
deduped_segments = []
skipped = 0

for key, segment in segments:
    if key is None:
        deduped_segments.append(segment)
    elif key not in seen_keys:
        seen_keys.add(key)
        deduped_segments.append(segment)
    else:
        skipped += 1

print(f"Skipped {skipped} duplicate command definitions")

# Reassemble
output_lines = []
for segment in deduped_segments:
    output_lines.extend(segment)

print(f"Output: {len(output_lines)} lines")

# Write output
with open(OUTPUT, "w", encoding="utf-8") as f:
    f.writelines(output_lines)

print("Done. Verifying syntax...")
import py_compile, os
try:
    py_compile.compile(OUTPUT, doraise=True)
    print("✓ Syntax OK")
except py_compile.PyCompileError as e:
    print(f"✗ Syntax error: {e}")
    sys.exit(1)
