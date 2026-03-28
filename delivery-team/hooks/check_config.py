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

        message = f"Delivery pipeline configured (v{version}, {date}). Use delivery-team:delivery-flow to start the pipeline."

        # Validate custom clean code guide path (FR-16, FR-17)
        clean_code_guide_match = re.search(r'clean_code_guide:\s*(\S+)', content)
        if clean_code_guide_match:
            guide_path = clean_code_guide_match.group(1).strip('"').strip("'")
            if guide_path:
                full_path = cwd / guide_path
                if full_path.exists():
                    message += f"\nCustom clean code guide: {guide_path}"
                    token_estimate = len(full_path.read_text(encoding="utf-8")) // 4
                    if token_estimate > 4000:
                        message += f"\nWARNING: Custom clean code guide is large (~{token_estimate} tokens): {guide_path}"
                        message += "\n  The built-in guide targets <=2000 tokens to preserve context for code generation."
                        message += "\n  Large guides may reduce available context for complex tasks."
                else:
                    message += f"\nWARNING: Custom clean code guide not found: {guide_path}"
                    message += "\n  The file at this path does not exist or is not readable."
                    message += "\n  Fix: Either create the file, update the path in .delivery/config.yml under tech_stack.clean_code_guide, or remove the key to use the built-in default."
                    message += "\n  Falling back to built-in clean-code.md for this session."

        # Validate clean code enforcement value
        enforcement_match = re.search(r'clean_code_enforcement:\s*(\S+)', content)
        if enforcement_match:
            enforcement = enforcement_match.group(1).strip('"').strip("'")
            if enforcement not in ('block', 'warn'):
                message += f"\nWARNING: Invalid clean_code_enforcement value: '{enforcement}'"
                message += "\n  Valid values: block, warn"
                message += "\n  Defaulting to: block"

        emit_response(message=message)
    else:
        emit_response(message="No delivery pipeline config found (.delivery/config.yml missing). Run delivery-team:delivery-flow to set up the project with the setup wizard.")

    exit_success()


if __name__ == "__main__":
    main()
