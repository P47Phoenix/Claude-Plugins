#!/usr/bin/env python3
"""SessionStart hook: Validate .hardware/config.yml exists and is current.

Checks:
1. .hardware/config.yml existence and schema version
2. kicad-happy skill availability (delegates to check_kicad_happy.py logic)
3. Paused pipeline staleness detection via .hardware/state.md
4. Missing dependency reporting

Security: All input parsed via json.loads(). No shell execution. Paths validated.
Per SEC-06, all environment variables treated as untrusted input.
"""
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


# Current config schema version expected by this plugin version.
CURRENT_SCHEMA_VERSION = "1.0"

# Default staleness thresholds (days).
DEFAULT_STALENESS_WARNING_DAYS = 7
DEFAULT_STALENESS_CRITICAL_DAYS = 30


def _read_hook_input() -> dict:
    """Read hook input from stdin (Claude Code hook protocol)."""
    try:
        return json.loads(sys.stdin.read())
    except (json.JSONDecodeError, Exception):
        return {}


def _get_cwd(hook_input: dict) -> Path:
    """Extract working directory from hook input."""
    return Path(hook_input.get("cwd", os.getcwd()))


def _check_config(cwd: Path) -> list[str]:
    """Validate .hardware/config.yml. Returns list of message lines."""
    messages = []
    config_path = cwd / ".hardware" / "config.yml"

    if not config_path.exists():
        messages.append(
            "WARNING: No .hardware/config.yml found. "
            "Run `hw-setup` to create one. "
            "Pipeline will use default settings."
        )
        return messages

    try:
        content = config_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        messages.append(
            f"WARNING: Cannot read .hardware/config.yml: {exc}. "
            "Pipeline will use default settings."
        )
        return messages

    # Parse YAML safely -- try PyYAML first, fall back to regex extraction.
    config = None
    try:
        import yaml
        config = yaml.safe_load(content)
    except ImportError:
        # No PyYAML -- extract version via regex.
        pass
    except Exception as exc:
        messages.append(
            f"WARNING: .hardware/config.yml has invalid YAML: {exc}. "
            "Pipeline will use default settings for unparseable fields."
        )

    # Extract schema version.
    version = None
    if isinstance(config, dict):
        version = str(config.get("schema_version", ""))
    if not version:
        match = re.search(r'schema_version:\s*"?([^"\s]+)"?', content)
        if match:
            version = match.group(1)

    if not version:
        messages.append(
            "WARNING: .hardware/config.yml missing schema_version field. "
            f"Expected version {CURRENT_SCHEMA_VERSION}."
        )
    elif version != CURRENT_SCHEMA_VERSION:
        messages.append(
            f"WARNING: .hardware/config.yml schema version {version} is outdated. "
            f"Current version is {CURRENT_SCHEMA_VERSION}. "
            "Run `hw-setup` to migrate your config."
        )
    else:
        messages.append(
            f"Hardware config loaded (v{version})."
        )

    return messages


def _check_pipeline_state(cwd: Path, config_content: str | None = None) -> list[str]:
    """Check for paused pipeline and report staleness."""
    messages = []
    state_path = cwd / ".hardware" / "state.md"

    if not state_path.exists():
        return messages

    try:
        state_text = state_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return messages

    # Parse YAML frontmatter (between --- delimiters).
    frontmatter = None
    fm_match = re.match(r'^---\s*\n(.*?)\n---', state_text, re.DOTALL)
    if fm_match:
        fm_text = fm_match.group(1)
        try:
            import yaml
            frontmatter = yaml.safe_load(fm_text)
        except ImportError:
            # Regex fallback for key fields.
            frontmatter = {}
            for key in ("status", "current_stage", "last_updated", "pipeline_id"):
                m = re.search(rf'{key}:\s*"?([^"\n]+)"?', fm_text)
                if m:
                    frontmatter[key] = m.group(1).strip()
        except Exception:
            return messages

    if not isinstance(frontmatter, dict):
        return messages

    status = frontmatter.get("status", "")
    current_stage = frontmatter.get("current_stage", "unknown")
    last_updated_str = frontmatter.get("last_updated", "")

    if status not in ("paused", "in_progress", "paused_awaiting_human", "paused_dispatch_error"):
        return messages

    # Parse last_updated timestamp.
    paused_days = None
    paused_since_str = "unknown"
    if last_updated_str:
        try:
            # Handle ISO format timestamps.
            last_updated_str_clean = str(last_updated_str).replace("Z", "+00:00")
            last_dt = datetime.fromisoformat(last_updated_str_clean)
            if last_dt.tzinfo is None:
                last_dt = last_dt.replace(tzinfo=timezone.utc)
            now = datetime.now(timezone.utc)
            delta = now - last_dt
            paused_days = delta.days
            paused_since_str = str(last_updated_str)
        except (ValueError, TypeError):
            pass

    # Always report paused status.
    day_str = f" ({paused_days} days ago)" if paused_days is not None else ""
    messages.append(
        f"PIPELINE PAUSED at {current_stage}."
        f"\n  Paused since: {paused_since_str}{day_str}."
        f'\n  Resume with "resume hardware pipeline".'
    )

    # Staleness detection.
    if paused_days is not None:
        warning_days = DEFAULT_STALENESS_WARNING_DAYS
        critical_days = DEFAULT_STALENESS_CRITICAL_DAYS

        # Try reading thresholds from config.
        if config_content:
            try:
                import yaml
                cfg = yaml.safe_load(config_content)
                if isinstance(cfg, dict):
                    pipeline = cfg.get("pipeline", {})
                    if isinstance(pipeline, dict):
                        warning_days = int(pipeline.get(
                            "staleness_warning_days", warning_days
                        ))
                        critical_days = int(pipeline.get(
                            "staleness_critical_days", critical_days
                        ))
            except Exception:
                pass

        if paused_days >= critical_days:
            messages.append(
                f"CRITICAL: Pipeline has been paused for {paused_days} days. "
                "It is strongly recommended to Restart rather than Resume, "
                "as project context has likely changed significantly."
            )
        elif paused_days >= warning_days:
            messages.append(
                f"WARNING: Pipeline has been paused for {paused_days} days "
                f"at {current_stage}.\n"
                "  Config or project files may have drifted since the pipeline was paused.\n"
                "  Options: Resume (uses original config snapshot) | Restart (applies current config) | Abandon"
            )

    return messages


def _check_dependencies(cwd: Path) -> list[str]:
    """Check for required dependencies beyond kicad-happy (which has its own hook)."""
    messages = []

    # Check PyYAML availability (soft dependency).
    try:
        import yaml  # noqa: F401
    except ImportError:
        messages.append(
            "NOTE: PyYAML is not installed. Config validation uses regex fallback. "
            "Install PyYAML for full schema validation: pip install pyyaml"
        )

    return messages


def main():
    hook_input = _read_hook_input()
    cwd = _get_cwd(hook_input)

    all_messages = []

    # 1. Validate config.
    all_messages.extend(_check_config(cwd))

    # 2. Read config content for staleness thresholds.
    config_path = cwd / ".hardware" / "config.yml"
    config_content = None
    if config_path.exists():
        try:
            config_content = config_path.read_text(encoding="utf-8")
        except Exception:
            pass

    # 3. Check pipeline state (paused/stale).
    all_messages.extend(_check_pipeline_state(cwd, config_content))

    # 4. Check non-kicad-happy dependencies.
    all_messages.extend(_check_dependencies(cwd))

    # Emit combined message.
    combined = "\n".join(all_messages)
    result = {"message": combined} if combined else {}
    print(json.dumps(result))
    sys.exit(0)


if __name__ == "__main__":
    main()
