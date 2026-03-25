#!/usr/bin/env bash
#
# SessionStart hook: Check if delivery pipeline is configured for this project.
# Announces when .delivery/config.yml is missing so the user knows setup hasn't run.
#
# Exit 0 always (informational, never blocks session start).

set -euo pipefail

INPUT=$(cat)
CWD=$(echo "$INPUT" | jq -r '.cwd // empty')

if [ -z "$CWD" ]; then
  exit 0
fi

CONFIG_FILE="$CWD/.delivery/config.yml"

if [ -f "$CONFIG_FILE" ]; then
  # Config exists — extract version and date
  VERSION=$(grep -oP 'config_version:\s*"\K[^"]+' "$CONFIG_FILE" || echo "unknown")
  DATE=$(grep -oP 'wizard_completed:\s*\K\S+' "$CONFIG_FILE" || echo "unknown")

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
    "systemMessage": "No delivery pipeline config found (.delivery/config.yml missing). Run delivery-team:delivery-flow to set up the project with the setup wizard. All implementation work should go through the delivery pipeline for QA review and defect prevention."
  }'
fi

exit 0
