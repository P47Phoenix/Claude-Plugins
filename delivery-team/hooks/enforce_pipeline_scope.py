"""PreToolUse hook: enforce delivery pipeline scope on Edit/Write/NotebookEdit.

Reads .delivery/config.yml for pipeline.scope, scope_include, scope_exclude.
Checks .delivery/state.md for an active pipeline.
Warns via systemMessage if the file is in scope but no pipeline is active.
Passes through silently on any error (graceful degradation).

In addition (v2.7+, ADR-001), this hook performs **layered origin detection**
to distinguish orchestrator-originated writes to `.delivery/artifacts/**` from
sub-agent-originated writes to the same paths. Activation is gated on BOTH
`schema_version >= 2.7` AND `pipeline.enforce_self_write_block: true`. When
either gate is off, the hook remains warning-only (NFR-05 wins over strictness
when the mechanism itself is uncertain).

Layered detection order (first signal that resolves wins):

  Layer 1 — Environment variable (primary, deterministic):
      CLAUDE_AGENT_ID or DELIVERY_FLOW_AGENT_CONTEXT set => sub-agent => allow.
      The orchestrator is expected to inject one of these on every Agent
      tool dispatch. Absence => candidate orchestrator-origin.

  Layer 2 — Hook input metadata (secondary):
      Inspect the harness hook payload for a `parent_tool_use_id` (or similar
      sub-agent frame indicator). Positive identification => allow.
      Inconclusive => fall through.

  Layer 3 — Soft-deny fallback (safety):
      If neither signal resolves AND the write targets a non-allowlisted path
      under `.delivery/artifacts/**`, emit a loud systemMessage warning naming
      the Delegation Prime Directive and the target path. Do NOT hard-deny.

KNOWN GAPS (mirrored in references/quality-gates.md):
  - Bash write-redirection is NOT matched by this hook's registered tool
    matchers (Edit|Write|NotebookEdit). Orchestrator-origin writes via Bash
    with `>`, `>>`, `tee`, `cat <<EOF`, `dd of=`, or `cp`/`mv` into artifact
    paths will bypass this check. Closing the gap requires registering on
    the Bash tool AND pattern-matching the command string.
  - Layer 2 metadata shape is harness-version-dependent. The detector is
    conservative: unknown keys fall through to Layer 3 (warn-only), never
    to a hard-deny.
  - A missing env-var injection at any orchestrator dispatch site collapses
    Layer 1, leaving Layer 2 load-bearing. Centralizing sub-agent dispatch
    (one injection site) is the architectural mitigation.

No external dependencies -- stdlib only, YAML parsed with regex.
"""
import fnmatch
import os
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
# Artifact origin detection (ADR-001)
# ---------------------------------------------------------------------------
# Paths under `.delivery/` that are ALWAYS allowed regardless of origin.
# These are legitimately orchestrator-owned routing/bookkeeping files.
# A single source of truth so the allowlist cannot drift.
ARTIFACT_ALLOWLIST: tuple[str, ...] = (
    ".delivery/state.md",
    ".delivery/state.tmp.md",
    ".delivery/config.yml",
)

# Directory prefixes under `.delivery/` that are always allowed.
ARTIFACT_ALLOWLIST_DIRS: tuple[str, ...] = (
    ".delivery/memory/",
    ".delivery/state-archive/",
    ".delivery/defects/",
    ".delivery/features/",
    ".delivery/aliases/",
)

# Filenames under `.delivery/artifacts/**` that the orchestrator is
# permitted to write directly (routing metadata, not domain content).
ARTIFACT_ROUTING_BASENAMES: tuple[str, ...] = (
    "stage-summary.md",
    "state.md",
    "state.tmp.md",
)

# Env vars that, if set, indicate this tool call originates from a
# dispatched sub-agent rather than the top-level orchestrator.
SUBAGENT_ENV_VARS: tuple[str, ...] = (
    "CLAUDE_AGENT_ID",
    "DELIVERY_FLOW_AGENT_CONTEXT",
)


def _is_artifact_path(rel_path: str) -> bool:
    """Return True if *rel_path* lives under `.delivery/artifacts/`."""
    return rel_path.startswith(".delivery/artifacts/") or rel_path.startswith("./.delivery/artifacts/")


def _is_allowlisted(rel_path: str) -> bool:
    """Return True if the path is always permitted, regardless of origin."""
    norm = rel_path.lstrip("./") if rel_path.startswith("./") else rel_path
    if norm in ARTIFACT_ALLOWLIST:
        return True
    for prefix in ARTIFACT_ALLOWLIST_DIRS:
        if norm.startswith(prefix):
            return True
    # Routing metadata files inside `.delivery/artifacts/**` are allowed
    # for orchestrator writes.
    if _is_artifact_path(norm):
        basename = Path(norm).name
        if basename in ARTIFACT_ROUTING_BASENAMES:
            return True
    return False


def _detect_subagent_origin(hook_input: dict) -> bool:
    """Return True if this tool call can be positively identified as sub-agent.

    Layered detection per ADR-001:
      Layer 1 — env var (CLAUDE_AGENT_ID or DELIVERY_FLOW_AGENT_CONTEXT)
      Layer 2 — hook input metadata (parent_tool_use_id or similar)

    If neither signal resolves, return False and let the caller fall through
    to Layer 3 (soft-deny warn-only).
    """
    # Layer 1: environment variable.
    for var in SUBAGENT_ENV_VARS:
        if os.environ.get(var):
            return True

    # Layer 2: hook input metadata. Conservative — any positive signal wins,
    # unknown shape falls through.
    try:
        if isinstance(hook_input, dict):
            if hook_input.get("parent_tool_use_id"):
                return True
            # Some harness versions nest under 'context' or 'frame'.
            ctx = hook_input.get("context") or {}
            if isinstance(ctx, dict) and ctx.get("parent_tool_use_id"):
                return True
            frame = hook_input.get("frame") or {}
            if isinstance(frame, dict) and frame.get("is_subagent"):
                return True
    except Exception:
        pass

    return False


def _activation_gated(config_text: str) -> bool:
    """Return True if enforcement is activated (schema >= 2.7 AND flag on)."""
    version = _parse_yaml_string("config_version", config_text) or ""
    version = version.strip().strip('"').strip("'")
    # Compare as tuples; reject anything below 2.7.
    try:
        parts = [int(p) for p in version.split(".")[:2]]
        if len(parts) < 2 or (parts[0], parts[1]) < (2, 7):
            return False
    except ValueError:
        return False
    flag = _parse_yaml_string("pipeline.enforce_self_write_block", config_text)
    if not flag:
        return False
    return flag.strip().lower() in ("true", "yes", "on", "1")


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

    # Compute rel_path once; both the origin check and the scope check need it.
    try:
        rel_path_early = str(Path(file_path).resolve().relative_to(cwd.resolve()))
    except (ValueError, OSError):
        rel_path_early = ""

    # ------------------------------------------------------------------
    # Origin detection (ADR-001): only active when schema v2.7+ AND flag.
    # Applies to non-allowlisted paths under `.delivery/artifacts/**`.
    # Soft-deny only — warning systemMessage, never a hard deny.
    # ------------------------------------------------------------------
    if (
        rel_path_early
        and _is_artifact_path(rel_path_early)
        and not _is_allowlisted(rel_path_early)
        and _activation_gated(config_text)
    ):
        if not _detect_subagent_origin(hook_input):
            # Layer 3: soft-deny. Warn loudly, do not block.
            emit_response(
                continue_=True,
                message=(
                    "[delivery-team] DELEGATION PRIME DIRECTIVE: the orchestrator "
                    f"appears to be writing directly to '{rel_path_early}'. Domain "
                    "artifacts (PRDs, designs, architecture, code, test plans, reviews) "
                    "MUST be produced by delegated sub-agents via the Agent tool, not "
                    "written by the orchestrator. If you are a sub-agent, ensure the "
                    "orchestrator injected CLAUDE_AGENT_ID or DELIVERY_FLOW_AGENT_CONTEXT "
                    "on dispatch. See delivery-flow SKILL.md Phase 4 Step 4.5."
                ),
            )
            sys.exit(0)

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
