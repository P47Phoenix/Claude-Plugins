#!/usr/bin/env bash
#
# PreToolUse hook: Audit Agent tool prompts for content leakage.
# Warns when orchestrator passes artifact content instead of file paths.
# Checks for code fences and excessive non-metadata content.
#
# Exit 0 = allow (with optional warning via systemMessage)
# This is a warning-only hook in v1.0.

set -euo pipefail

INPUT=$(cat)

TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')

# Only check Agent tool invocations
if [ "$TOOL_NAME" != "Agent" ]; then
  exit 0
fi

PROMPT=$(echo "$INPUT" | jq -r '.tool_input.prompt // empty')

if [ -z "$PROMPT" ]; then
  exit 0
fi

WARNINGS=""

# Check for code fences (likely pasting artifact content)
CODE_FENCE_COUNT=$(echo "$PROMPT" | grep -c '```' || true)
if [ "$CODE_FENCE_COUNT" -gt 2 ]; then
  WARNINGS="${WARNINGS}Code fences detected in agent prompt ($CODE_FENCE_COUNT found) — may indicate artifact content being pasted instead of file paths. "
fi

# Check prompt length (metadata should be < 2000 chars, content leakage makes it much longer)
PROMPT_LENGTH=${#PROMPT}
if [ "$PROMPT_LENGTH" -gt 5000 ]; then
  WARNINGS="${WARNINGS}Agent prompt is very long (${PROMPT_LENGTH} chars) — may indicate content leakage. Prefer passing file paths. "
fi

if [ -n "$WARNINGS" ]; then
  jq -n --arg warnings "$WARNINGS" '{
    "continue": true,
    "suppressOutput": false,
    "systemMessage": ("ISOLATION AUDIT WARNING: " + $warnings + "The orchestrator should pass artifact FILE PATHS, not content. See two-channel communication model.")
  }'
fi

exit 0
