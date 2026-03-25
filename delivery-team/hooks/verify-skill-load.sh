#!/usr/bin/env bash
#
# PostToolUse hook: Verify sub-agents loaded the expected skill.
# Checks for SKILL_LOADED marker in Agent tool output.
# Warns if missing or mismatched.
#
# Exit 0 always (warning only, never blocks).

set -euo pipefail

INPUT=$(cat)

TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')

# Only check Agent tool invocations
if [ "$TOOL_NAME" != "Agent" ]; then
  exit 0
fi

TOOL_RESULT=$(echo "$INPUT" | jq -r '.tool_result // empty')

if [ -z "$TOOL_RESULT" ]; then
  exit 0
fi

# Check for SKILL_LOADED marker
if echo "$TOOL_RESULT" | head -5 | grep -q "SKILL_LOADED:"; then
  # Marker found — skill loaded successfully
  exit 0
fi

# Marker not found — warn
jq -n '{
  "continue": true,
  "suppressOutput": false,
  "systemMessage": "WARNING: Sub-agent did not confirm skill loading (no SKILL_LOADED marker in output). The agent may not have loaded its designated skill references. Consider retrying the delegation."
}'

exit 0
