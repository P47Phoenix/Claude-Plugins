#!/usr/bin/env bash
#
# SubagentStop hook: Flag acceptance criteria that require empirical (runtime) validation.
# Fires when developer or godot sub-agents complete.
# Reads the agent's transcript, scans for empirical keywords in acceptance criteria,
# and injects a warning into Claude's context if found.
#
# Exit codes:
#   0 = success (with or without findings)
#   Non-zero = hook error (logged, non-blocking)

set -euo pipefail

# Read hook input from stdin
INPUT=$(cat)

TRANSCRIPT_PATH=$(echo "$INPUT" | jq -r '.transcript_path // empty')

if [ -z "$TRANSCRIPT_PATH" ] || [ ! -f "$TRANSCRIPT_PATH" ]; then
  # No transcript available — skip silently
  exit 0
fi

# Extract text content from transcript (user messages + assistant messages)
# Look for acceptance criteria, given/when/then, and requirement-like text
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
# Visual / Rendering
VISUAL_PATTERN='renders?|displays?|visible|appears?( on screen)?|shows?|hides?|layout|responsive|animated|animation plays'
# User Interaction
INTERACTION_PATTERN='clicks?|taps?|swipes?|drags?|scrolls?|hovers?|selects?|triggers action|input handling|gesture|touch'
# Runtime Behavior
RUNTIME_PATTERN='returns [0-9]{3}|responds with|fires|executes|processes|plays|navigates to|redirects|loads correctly|streams'
# Physics / Simulation
PHYSICS_PATTERN='collision|physics|gravity|velocity|raycast|pathfinding|navigation|AI behaves|spawns at|moves to'
# Audio / Media
AUDIO_PATTERN='sound plays|audio|music|video plays'

COMBINED_PATTERN="($VISUAL_PATTERN|$INTERACTION_PATTERN|$RUNTIME_PATTERN|$PHYSICS_PATTERN|$AUDIO_PATTERN)"

# Search for acceptance criteria sections and check for empirical keywords
# Look for text near AC markers: "acceptance criteria", "given/when/then", "AC:", "should", "must"
AC_TEXT=$(echo "$CONTENT" | grep -iE '(acceptance|criteria|given|when|then|should|must|shall|verify|validate|test that)' | head -50)

if [ -z "$AC_TEXT" ]; then
  # No acceptance criteria found — skip
  exit 0
fi

# Find empirical matches
MATCHES=$(echo "$AC_TEXT" | grep -ioE "$COMBINED_PATTERN" | sort -u)

if [ -z "$MATCHES" ]; then
  # No empirical keywords found — all criteria are structural
  exit 0
fi

# Format the matches as a bulleted list
MATCH_LIST=$(echo "$MATCHES" | while read -r match; do
  echo "  - \"$match\""
done)

# Count matches
MATCH_COUNT=$(echo "$MATCHES" | wc -l | tr -d ' ')

# Output structured warning for Claude's context
cat <<HOOK_OUTPUT
EMPIRICAL VALIDATION REQUIRED

The completed sub-agent task includes acceptance criteria with $MATCH_COUNT empirical validation keyword(s) that cannot be verified by code inspection alone:

$MATCH_LIST

These criteria require runtime verification (running the application, executing tests in the actual environment, or manual testing).

ACTION REQUIRED:
- Mark these criteria as "Requires runtime validation" in the Verification Status
- Do NOT mark them as verified by inspection
- Story status should be CODE_COMPLETE (not DONE) until runtime validation occurs
- Carry forward these items to UAT as mandatory test cases

See quality/references/empirical-validation.md for recommended validation approaches per technology.
HOOK_OUTPUT

exit 0
