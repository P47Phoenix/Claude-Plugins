## Idea Brief

**Project Type**: BUG_FIX
**Date**: 2026-03-25
**GitHub Issues**: #40
**Applies To**: delivery-team hooks, project-level enforcement

### Problem Statement

The project-level enforcement hook in `.claude/settings.json` is a prompt-based hook that instructs Claude to "check .delivery/config.yml for pipeline.scope" — but prompt hooks cannot read files. They evaluate based on text instructions and tool input only. The hook describes filesystem checks it is structurally incapable of performing.

This means the enforcement is entirely illusory. The hook cannot read `pipeline.scope` from config. It cannot evaluate `scope_include` or `scope_exclude` patterns against actual config values. It cannot detect an active pipeline by reading `.delivery/state.md`. When a user changes their config, the hook behavior does not change because the scope rules are hardcoded in the prompt text, not read from the config file.

A guard who cannot read the law he enforces is no guard at all.

### Target Users

- **Any delivery-flow user**: Everyone with a `.delivery/config.yml` expects the enforcement hook to respect their configured scope settings. It does not.
- **Users with custom scope configs**: Anyone who has set `pipeline.scope: custom` or modified `scope_exclude` patterns is getting zero benefit from those settings — the hook ignores them entirely.

### Goals

1. The enforcement hook reads `pipeline.scope`, `scope_include`, and `scope_exclude` from `.delivery/config.yml` at invocation time — not from hardcoded prompt text
2. The hook detects active pipeline status by reading `.delivery/state.md`
3. Missing config or missing state file results in graceful pass-through (no enforcement, no crash)
4. The hook uses the shared `hooks/lib/hook_utils.py` library for stdin/stdout handling, consistent with other Python command hooks in this repo

### Constraints

- Must be a Python command hook, not a prompt hook — this is the entire point of the fix
- Must be cross-platform (pathlib, no shell-isms)
- Must use the existing hook_utils.py shared library for hook I/O
- Hook timeout budget remains 10 seconds (same as current prompt hook)
- Must not break the existing `.claude/settings.json` structure beyond replacing the hook entry

### Initial Scope

- New script: `delivery-team/hooks/enforce_pipeline_scope.py` that reads config and state files, evaluates scope rules, and returns allow/warn via hook protocol
- Update `.claude/settings.json` to replace the prompt hook with a command hook pointing to the new script
- Handle all three scope modes: `code-only` (default), `all`, and `custom`

### Out of Scope

- Changes to the config schema itself — we are reading existing config keys, not adding new ones
- Changes to other hooks (PreToolUse/Skill, PostToolUse/Write, SubagentStop) — those are working correctly
- New scope modes beyond the three already defined
- UI or messaging changes to the warning output beyond what is needed for accurate enforcement
