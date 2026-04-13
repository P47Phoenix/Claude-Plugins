#!/usr/bin/env python3
"""SessionStart hook: Check kicad-happy skill availability and version compatibility."""
import json
import os
import re
import sys
from pathlib import Path


# The 11 kicad-happy skills consumed by hardware-team roles.
REQUIRED_SKILLS = [
    "kicad", "spice", "digikey", "mouser", "lcsc",
    "element14", "jlcpcb", "pcbway", "bom", "emc", "kidoc",
]

TOTAL_SKILLS = len(REQUIRED_SKILLS)


def _find_kicad_happy_path() -> Path | None:
    """Locate the kicad-happy plugin cache directory."""
    home = Path.home()
    cache_root = home / ".claude" / "plugins" / "cache" / "kicad-happy"
    if not cache_root.exists():
        return None

    # Scan for version directories: cache/kicad-happy/kicad-happy/<version>/
    plugin_dir = cache_root / "kicad-happy"
    if not plugin_dir.exists():
        return None

    # Find the latest version directory
    version_dirs = sorted(
        [d for d in plugin_dir.iterdir() if d.is_dir()],
        key=lambda d: d.name,
        reverse=True,
    )
    if version_dirs:
        return version_dirs[0]
    return None


def _extract_version(install_path: Path) -> str | None:
    """Extract the version string from the install path directory name."""
    return install_path.name if install_path else None


def _check_skill_available(install_path: Path, skill_name: str) -> bool:
    """Check if a specific kicad-happy skill directory and SKILL.md exist."""
    # Skills may be at top level or in a skills/ subdirectory
    candidates = [
        install_path / skill_name / "SKILL.md",
        install_path / "skills" / skill_name / "SKILL.md",
    ]
    return any(c.exists() for c in candidates)


def _get_required_version(cwd: str) -> str | None:
    """Read the required kicad-happy version from .hardware/config.yml."""
    config_path = Path(cwd) / ".hardware" / "config.yml"
    if not config_path.exists():
        return None
    try:
        content = config_path.read_text(encoding="utf-8")
        match = re.search(r'kicad_happy_version:\s*"?([^"\s]+)"?', content)
        if match:
            return match.group(1)
    except Exception:
        pass
    return None


def _version_satisfies(installed: str, required: str) -> bool:
    """Check if installed version satisfies the required version constraint.

    Supports simple >=X.Y.Z constraints.
    """
    if not installed or not required:
        return True  # Cannot check, assume OK

    # Strip >= prefix from requirement
    req = required.lstrip(">= ")

    try:
        inst_parts = [int(x) for x in installed.split(".")]
        req_parts = [int(x) for x in req.split(".")]

        # Pad to equal length
        max_len = max(len(inst_parts), len(req_parts))
        inst_parts.extend([0] * (max_len - len(inst_parts)))
        req_parts.extend([0] * (max_len - len(req_parts)))

        return inst_parts >= req_parts
    except (ValueError, AttributeError):
        return True  # Cannot parse, assume OK


def main():
    # Read hook input from stdin (Claude Code hook protocol)
    try:
        hook_input = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, Exception):
        hook_input = {}

    cwd = hook_input.get("cwd", os.getcwd())

    install_path = _find_kicad_happy_path()

    if install_path is None:
        # kicad-happy is not installed at all
        result = {
            "message": (
                "WARNING: Required dependency kicad-happy is not installed. "
                "Install it via the Claude Code plugin system. "
                "Hardware pipeline will operate with degraded capability -- "
                "role skills that depend on kicad-happy will report SKILL_UNAVAILABLE."
            )
        }
        print(json.dumps(result))
        sys.exit(0)

    # Check each skill
    available = []
    missing = []
    for skill in REQUIRED_SKILLS:
        if _check_skill_available(install_path, skill):
            available.append(skill)
        else:
            missing.append(skill)

    available_count = len(available)

    # Build message
    if available_count == TOTAL_SKILLS:
        message = f"kicad-happy: {TOTAL_SKILLS}/{TOTAL_SKILLS} skills available"
    elif available_count > 0:
        missing_list = ", ".join(missing)
        message = (
            f"kicad-happy: {available_count}/{TOTAL_SKILLS} skills available. "
            f"Missing: [{missing_list}]. "
            f"Install kicad-happy via Claude Code plugin system."
        )
    else:
        message = (
            f"WARNING: kicad-happy is installed but no skills found at {install_path}. "
            f"The plugin installation may be corrupted. "
            f"Reinstall kicad-happy via the Claude Code plugin system."
        )

    # Version compatibility check
    installed_version = _extract_version(install_path)
    required_version = _get_required_version(cwd)

    if installed_version and required_version:
        if not _version_satisfies(installed_version, required_version):
            message += (
                f"\nkicad-happy version {installed_version} installed; "
                f"hardware-team requires {required_version}."
            )

    result = {"message": message}
    print(json.dumps(result))
    sys.exit(0)


if __name__ == "__main__":
    main()
