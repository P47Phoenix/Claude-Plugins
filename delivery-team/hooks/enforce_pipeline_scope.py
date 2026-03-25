"""PreToolUse hook: enforce delivery pipeline scope on Edit/Write/NotebookEdit.

Reads .delivery/config.yml for pipeline.scope, scope_include, scope_exclude.
Checks .delivery/state.md for an active pipeline.
Warns via systemMessage if the file is in scope but no pipeline is active.
Passes through silently on any error (graceful degradation).

No external dependencies -- stdlib only, YAML parsed with regex.
"""
import fnmatch
import re
import sys
from pathlib import Path

# Bootstrap: add the lib directory so hook_utils is importable.
sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

from hook_utils import (  # noqa: E402
    emit_response,
    get_cwd,
    get_tool_input,
    read_hook_input,
)

# ---------------------------------------------------------------------------
# Known source-code extensions for the "code-only" scope mode.
# ---------------------------------------------------------------------------
CODE_EXTENSIONS: set[str] = {
    ".py", ".ts", ".js", ".go", ".rs", ".cs", ".java", ".gd",
    ".scala", ".hs", ".ex", ".fs", ".tsx", ".jsx", ".vue", ".svelte", ".sh",
}

# Default exclusion patterns (used when config has none).
DEFAULT_EXCLUDES: list[str] = [
    ".delivery/", ".git/", "node_modules/", "__pycache__/",
]


# ---------------------------------------------------------------------------
# Lightweight YAML helpers (stdlib only -- no pyyaml)
# ---------------------------------------------------------------------------

def _parse_yaml_string(key: str, text: str) -> str | None:
    """Return the scalar value for a top-level or dotted key like 'pipeline.scope'."""
    parts = key.split(".")
    if len(parts) == 2:
        section, field = parts
        # Find the section header, then look for the field inside it.
        pattern = rf"^{re.escape(section)}:\s*\n((?:[ \t]+\S.*\n)*)"
        m = re.search(pattern, text, re.MULTILINE)
        if not m:
            return None
        block = m.group(1)
        val_match = re.search(rf"^\s+{re.escape(field)}:\s*(.+)", block, re.MULTILINE)
        if val_match:
            return val_match.group(1).strip().strip('"').strip("'")
        return None
    # Single-level key.
    m = re.search(rf"^{re.escape(key)}:\s*(.+)", text, re.MULTILINE)
    if m:
        return m.group(1).strip().strip('"').strip("'")
    return None


def _parse_yaml_list(key: str, text: str) -> list[str]:
    """Return a list value for a key inside a section, e.g. 'pipeline.scope_include'.

    Supports both inline ``[a, b]`` and block-style YAML lists.
    """
    parts = key.split(".")
    if len(parts) != 2:
        return []
    section, field = parts

    pattern = rf"^{re.escape(section)}:\s*\n((?:[ \t]+\S.*\n)*)"
    m = re.search(pattern, text, re.MULTILINE)
    if not m:
        return []
    block = m.group(1)

    val_match = re.search(rf"^\s+{re.escape(field)}:\s*(.*)", block, re.MULTILINE)
    if not val_match:
        return []

    raw = val_match.group(1).strip()

    # Inline list: [".delivery/", ".git/"]
    if raw.startswith("["):
        items = re.findall(r'"([^"]+)"|\'([^\']+)\'|([^,\[\]\s]+)', raw)
        return [next(g for g in groups if g) for groups in items]

    # Block list (lines starting with "- ").
    result: list[str] = []
    remaining = block[val_match.end() - m.start(1):]
    for line in remaining.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            result.append(stripped[2:].strip().strip('"').strip("'"))
        elif stripped and not stripped.startswith("#"):
            break
    return result


# ---------------------------------------------------------------------------
# Scope evaluation
# ---------------------------------------------------------------------------

def _is_excluded(rel_path: str, excludes: list[str]) -> bool:
    """Return True if *rel_path* matches any exclusion pattern."""
    for pattern in excludes:
        # Directory prefix pattern (e.g. ".delivery/")
        if pattern.endswith("/") and (rel_path.startswith(pattern) or ("/" + pattern) in ("/" + rel_path)):
            return True
        # Glob / suffix pattern (e.g. "*.lock")
        if fnmatch.fnmatch(rel_path, pattern):
            return True
    return False


def _is_in_scope(rel_path: str, scope: str, includes: list[str], excludes: list[str]) -> bool:
    """Determine if *rel_path* falls within the configured enforcement scope."""
    if scope == "code-only":
        ext = Path(rel_path).suffix.lower()
        return ext in CODE_EXTENSIONS

    if scope == "all":
        return not _is_excluded(rel_path, excludes)

    if scope == "custom":
        return any(fnmatch.fnmatch(rel_path, pat) for pat in includes)

    # Unknown scope value -- pass through.
    return False


def _has_active_pipeline(cwd: Path) -> bool:
    """Return True if .delivery/state.md indicates an active pipeline."""
    state_file = cwd / ".delivery" / "state.md"
    if not state_file.exists():
        return False
    try:
        content = state_file.read_text(encoding="utf-8")
        # Look for status: in_progress (or similar active markers).
        if re.search(r"status:\s*in[_-]progress", content, re.IGNORECASE):
            return True
        return False
    except OSError:
        return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    hook_input = read_hook_input()
    if not hook_input:
        sys.exit(0)

    cwd = get_cwd(hook_input)
    tool_input = get_tool_input(hook_input)

    # Determine target file path from tool_input.
    file_path = tool_input.get("file_path", "")
    if not file_path:
        sys.exit(0)

    # Read config.
    config_file = cwd / ".delivery" / "config.yml"
    if not config_file.exists():
        sys.exit(0)

    try:
        config_text = config_file.read_text(encoding="utf-8")
    except OSError:
        sys.exit(0)

    config_text = config_text.rstrip() + "\n"  # Ensure trailing newline for regex matching

    scope = _parse_yaml_string("pipeline.scope", config_text)
    if not scope:
        sys.exit(0)

    includes = _parse_yaml_list("pipeline.scope_include", config_text)
    excludes = _parse_yaml_list("pipeline.scope_exclude", config_text) or DEFAULT_EXCLUDES

    # Make the file path relative to cwd for pattern matching.
    try:
        rel_path = str(Path(file_path).resolve().relative_to(cwd.resolve()))
    except (ValueError, OSError):
        # Path is outside the project -- not our concern.
        sys.exit(0)

    if not _is_in_scope(rel_path, scope, includes, excludes):
        sys.exit(0)

    if _has_active_pipeline(cwd):
        sys.exit(0)

    # In scope, no active pipeline -- warn.
    emit_response(
        continue_=True,
        message=(
            f"[delivery-team] The file '{rel_path}' is within the delivery pipeline scope "
            f"(pipeline.scope: {scope}) but no active pipeline was detected. "
            "Consider running `/delivery-flow` to ensure changes go through "
            "the full delivery process."
        ),
    )


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # Graceful degradation: never crash, never block.
        sys.exit(0)
