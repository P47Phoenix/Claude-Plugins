#!/usr/bin/env bash
#
# SessionStart hook: Check if delivery pipeline is configured for this project.
# Announces when .delivery/config.md is missing so the user knows setup hasn't run.
#
# Exit 0 always (informational, never blocks session start).

set -euo pipefail

INPUT=$(cat)
CWD=$(echo "$INPUT" | jq -r '.cwd // empty')

if [ -z "$CWD" ]; then
  exit 0
fi

CONFIG_FILE="$CWD/.delivery/config.md"

if [ -f "$CONFIG_FILE" ]; then
  # Config exists — extract version and date
  VERSION=$(head -20 "$CONFIG_FILE" | grep -oP 'config_version:\s*"\K[^"]+' || echo "unknown")
  DATE=$(head -20 "$CONFIG_FILE" | grep -oP 'wizard_completed:\s*\K\S+' || echo "unknown")

  jq -n \
    --arg version "$VERSION" \
    --arg date "$DATE" \
    '{
      "continue": true,
      "suppressOutput": false,
      "systemMessage": ("Delivery pipeline configured (v" + $version + ", " + $date + "). Use delivery-team:delivery-flow to start the pipeline.")
    }'
else
  jq -n '{
    "continue": true,
    "suppressOutput": false,
    "systemMessage": "No delivery pipeline config found (.delivery/config.md missing). Run delivery-team:delivery-flow to set up the project with the setup wizard. All implementation work should go through the delivery pipeline for QA review and defect prevention."
  }'
fi

exit 0
