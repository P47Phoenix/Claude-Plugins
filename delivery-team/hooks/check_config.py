#!/usr/bin/env python3
"""SessionStart hook: Check if delivery pipeline is configured."""
import re
from pathlib import Path

# Add hooks dir to path for shared lib
import sys
sys.path.insert(0, str(Path(__file__).parent))
from lib.hook_utils import read_hook_input, emit_response, exit_success, get_cwd


def main():
    hook_input = read_hook_input()
    cwd = get_cwd(hook_input)
    config_file = cwd / ".delivery" / "config.yml"

    if config_file.exists():
        content = config_file.read_text(encoding="utf-8")
        version = "unknown"
        date = "unknown"

        version_match = re.search(r'config_version:\s*"?([^"\s]+)"?', content)
        if version_match:
            version = version_match.group(1)

        date_match = re.search(r'wizard_completed:\s*(\S+)', content)
        if date_match:
            date = date_match.group(1)

        emit_response(message=f"Delivery pipeline configured (v{version}, {date}). Use delivery-team:delivery-flow to start the pipeline.")
    else:
        emit_response(message="No delivery pipeline config found (.delivery/config.yml missing). Run delivery-team:delivery-flow to set up the project with the setup wizard.")

    exit_success()


if __name__ == "__main__":
    main()
