#!/usr/bin/env bash
#
# SubagentStop hook: Flag acceptance criteria that require empirical (runtime) validation.
# Fires when developer or godot sub-agents complete.
# Reads the agent's transcript, scans for empirical keywords in acceptance criteria,
# and outputs a systemMessage for Claude's context if found.
#
# Exit codes:
#   0 = success (with or without findings — stdout shown in transcript)
#   2 = blocking error (stderr fed back to Claude)
#   Other = non-blocking error (logged only)

set -euo pipefail

# Read hook input from stdin
INPUT=$(cat)

TRANSCRIPT_PATH=$(echo "$INPUT" | jq -r '.transcript_path // empty')

if [ -z "$TRANSCRIPT_PATH" ] || [ ! -f "$TRANSCRIPT_PATH" ]; then
  # No transcript available — skip silently
  exit 0
fi

# Extract text content from transcript (user messages + assistant messages)
CONTENT=$(jq -r '
  .[] |
  select(.role == "user" or .role == "assistant") |
  if .content | type == "string" then .content
  elif .content | type == "array" then
    [.content[] | select(.type == "text") | .text] | join("\n")
  else empty
  end
' "$TRANSCRIPT_PATH" 2>/dev/null || echo "")

if [ -z "$CONTENT" ]; then
  exit 0
fi

# Empirical validation keyword patterns (from empirical-validation.md registry)
VISUAL_PATTERN='renders?|displays?|visible|appears?( on screen)?|shows?|hides?|layout|responsive|animated|animation plays'
INTERACTION_PATTERN='clicks?|taps?|swipes?|drags?|scrolls?|hovers?|selects?|triggers action|input handling|gesture|touch'
RUNTIME_PATTERN='returns [0-9]{3}|responds with|fires|executes|processes|plays|navigates to|redirects|loads correctly|streams'
PHYSICS_PATTERN='collision|physics|gravity|velocity|raycast|pathfinding|navigation|AI behaves|spawns at|moves to'
AUDIO_PATTERN='sound plays|audio|music|video plays'

COMBINED_PATTERN="($VISUAL_PATTERN|$INTERACTION_PATTERN|$RUNTIME_PATTERN|$PHYSICS_PATTERN|$AUDIO_PATTERN)"

# Search for acceptance criteria sections
AC_TEXT=$(echo "$CONTENT" | grep -iE '(acceptance|criteria|given|when|then|should|must|shall|verify|validate|test that)' | head -50 || true)

if [ -z "$AC_TEXT" ]; then
  exit 0
fi

# Find empirical matches
MATCHES=$(echo "$AC_TEXT" | grep -ioE "$COMBINED_PATTERN" | sort -u || true)

if [ -z "$MATCHES" ]; then
  exit 0
fi

# Format matches as a JSON-safe string
MATCH_LIST=$(echo "$MATCHES" | while read -r match; do
  echo "  - \"$match\""
done)

MATCH_COUNT=$(echo "$MATCHES" | wc -l | tr -d ' ')

# Output structured JSON per hook output format
# systemMessage is injected into Claude's context
jq -n \
  --arg count "$MATCH_COUNT" \
  --arg matches "$MATCH_LIST" \
  '{
    "continue": true,
    "suppressOutput": false,
    "systemMessage": ("EMPIRICAL VALIDATION REQUIRED: This sub-agent task includes " + $count + " acceptance criteria keyword(s) requiring runtime verification:\n" + $matches + "\n\nACTION: Mark these as \"Requires runtime validation\" in Verification Status. Story status should be CODE_COMPLETE (not DONE). Carry forward to UAT. See quality/references/empirical-validation.md for recommended validation approaches.")
  }'

exit 0
