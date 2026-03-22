#!/usr/bin/env bash
#
# PostToolUse hook: Validate GDScript files after Write/Edit.
# Runs godot --headless --check-only on .gd files if godot is available.
# Silently skips non-.gd files and missing godot binary.
#
# Exit codes:
#   0 = success or not applicable (non-.gd file, godot not found)
#   2 = parse error found (stderr fed back to Claude)

set -euo pipefail

INPUT=$(cat)

# Extract the file path from tool input
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

if [ -z "$FILE_PATH" ]; then
  exit 0
fi

# Only process .gd files
if [[ "$FILE_PATH" != *.gd ]]; then
  exit 0
fi

# Check if the file exists
if [ ! -f "$FILE_PATH" ]; then
  exit 0
fi

# Check if godot is available
if ! command -v godot &>/dev/null; then
  # Godot not on PATH — skip silently
  exit 0
fi

# Run parse validation (requires Godot 4.2+)
PARSE_OUTPUT=$(godot --headless --check-only --script "$FILE_PATH" 2>&1 || true)

# Check for errors in output
if echo "$PARSE_OUTPUT" | grep -qi "error\|SCRIPT ERROR\|Parse Error"; then
  # Parse error found — feed back to Claude via stderr
  echo "{\"decision\": \"block\", \"reason\": \"GDScript parse error in $FILE_PATH:\\n$(echo "$PARSE_OUTPUT" | head -20 | sed 's/"/\\"/g')\"}" >&2
  exit 2
fi

# No errors — proceed silently
exit 0
