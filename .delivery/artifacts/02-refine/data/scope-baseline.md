# Repo-Scope Metrics Baseline — Claude-Plugins

**Artifact**: Scope Baseline (Elrond / Data Analyst)
**Stage**: 2 / Refine
**Date**: 2026-04-20
**Alias**: Elrond — *"I was there three thousand sprints ago, when the metrics last failed."*

---

> *"The trends are clear to those who have watched long enough. You bring evidence before the council. Let it be examined."*

This document is the quantitative baseline. No interpretation, no recommendation. The Product Owner will read the numbers and decide what they mean.

**Measurement scope**: all files tracked in the repo root, excluding `.delivery/`, `.git/`, `node_modules/`, `__pycache__/`, and the generated `site/` directory. Line counts are raw `wc -l` output. Match counts are literal-string / regex occurrences (match count, not line count — one line may contain several matches).

---

## Section 1 — Plugin Inventory

Plain counts. "Sub-skills" = `SKILL.md` files found under a plugin's `skills/` directory (includes nested paradigm sub-skills). "Hook scripts" = Python/shell files under `hooks/` (includes `lib/` helpers and `__init__.py`; excludes `__pycache__`). "SKILL.md lines" = sum of `wc -l` across every `SKILL.md` under the plugin. "References lines" = sum of `wc -l` across every file under any `references/` directory within the plugin.

| Plugin | MD files | Py files | Sh files | Sub-skills (SKILL.md) | Hook scripts | hooks.json hook entries | SKILL.md total lines | References total lines |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `delivery-team/` | 166 | 19 | 0 | 13 | 8 | 7 | 5,738 | 34,870 |
| `agentic-flow-builder/` | 3 | 5 | 0 | 1 | 0 | 0 | 559 | 440 |
| `prompt-engineer/` | 3 | 0 | 0 | 0 (top-level only) | 0 | 0 | 440 | 0 |
| `prd-quality-gate-flow/` | 5 | 10 | 0 | 0 | 0 | 0 | 0 (no SKILL.md) | 0 |
| `research-agent/` | 7 | 0 | 0 | 0 (top-level only) | 0 | 0 | 471 | 822 |
| `mtg-commander/` | 14 | 1 | 0 | 0 (top-level only) | 0 | 0 | 1,181 | 2,531 |
| **Totals** | **198** | **35** | **0** | **14** | **8** | **7** | **8,389** | **38,663** |

Notes:
- `delivery-team/` has no top-level `SKILL.md`; each of its 11 surface skills lives under `skills/<name>/SKILL.md`. Two additional sub-skills live under `skills/architect/paradigms/{volatility,ddd}/SKILL.md` (total 13).
- `prd-quality-gate-flow/` has no `SKILL.md` — it is a Python-script plugin with 5 docs (`README.md`, `ARCHITECTURE.md`, `QUICKSTART.md`, `IMPLEMENTATION_SUMMARY.md`, `DEMONSTRATION_RESULTS.md`).
- `mtg-commander/` has a top-level `SKILL.md` plus `references/` rather than sub-skills.
- `delivery-team/` holds 86% of all plugin markdown (166 / 198) and 90% of all reference-doc lines (34,870 / 38,663).

---

## Section 2 — Model ID References Across the Repo

All counts below exclude `.delivery/`, `.git/`, `node_modules/`, `__pycache__/`, and `site/`. "Match count" counts regex matches (a file may contain several). "Files touched" counts distinct files.

| Pattern | Match count | Files touched | Sample file paths (up to 3) |
|---|---:|---:|---|
| `claude-opus-4-7` | 0 | 0 | — |
| `claude-opus-4-6` | 0 | 0 | — |
| `claude-opus-4-5` | 0 | 0 | — |
| `claude-opus-4` (wildcard) | 1 | 1 | `agentic-flow-builder/scripts/agent_registry.py` (line 187: `"model": "claude-opus-4-20250514"`) |
| `claude-sonnet-4-6` | 0 | 0 | — |
| `claude-sonnet-4-5` | 1 | 1 | `agentic-flow-builder/scripts/agent_registry.py` (line 148: `"model": "claude-sonnet-4-5-20250929"`) |
| `claude-haiku-4-5` | 0 | 0 | — |
| `claude-3-5` / `claude-3-7` | 0 | 0 | — |
| `claude-3` (generic) | 0 | 0 | — |
| `anthropic.messages.create` | 0 | 0 | — |
| `@anthropic-ai/sdk` / `from anthropic import` | 0 | 0 | — |

**Short-alias model references** (not in the original pattern list, added for completeness — these are logical names like `"claude-sonnet"` without a version suffix):

| Pattern | Match count | Files touched | Sample file paths |
|---|---:|---:|---|
| `claude-sonnet` (any form) | 19 | 4 | `prd-quality-gate-flow/prd_flows.db` (12, SQLite binary — logical strings `"claude-sonnet"` stored in rows); `prd-quality-gate-flow/stage_definitions.py` (4); `agentic-flow-builder/scripts/agent_registry.py` (2); `prd-quality-gate-flow/README.md` (1) |
| `claude-haiku` (any form) | 14 | 3 | `prd-quality-gate-flow/prd_flows.db` (9); `prd-quality-gate-flow/stage_definitions.py` (3); `agentic-flow-builder/scripts/agent_registry.py` (2) |
| `claude-opus` (any form) | 2 | 1 | `agentic-flow-builder/scripts/agent_registry.py` (2) |

**Hard-coded versioned model IDs (canonical inventory for the PO)**:

| File | Line | String |
|---|---:|---|
| `agentic-flow-builder/scripts/agent_registry.py` | 148 | `"model": "claude-sonnet-4-5-20250929"` |
| `agentic-flow-builder/scripts/agent_registry.py` | 172 | `"model": "claude-haiku-4-20250514"` |
| `agentic-flow-builder/scripts/agent_registry.py` | 187 | `"model": "claude-opus-4-20250514"` |

`prd-quality-gate-flow/stage_definitions.py` (7 references) and `prd-quality-gate-flow/README.md` (1 reference) use **short aliases** only (`"claude-sonnet"`, `"claude-haiku"`) — no version suffix. The `prd_flows.db` SQLite file contains stored copies of the same short aliases from previous runs (21 row-level occurrences).

No plugin SKILL.md file contains any Claude model ID.

---

## Section 3 — Prompt-Pattern Signals

Case-insensitive substring counts across the repo, excluding `.delivery/`, `.git/`, `node_modules/`, `__pycache__/`, `site/`. "Match count" is regex matches (one file may contain several). Top-3 files shown by per-file match count.

| Pattern | Match count | Files touched | Top-3 files (by match count) |
|---|---:|---:|---|
| `extended thinking` / `extended_thinking` / `thinking budget` | 0 | 0 | — |
| `prompt cach` (catches prompt cache / caching) | 0 | 0 | — |
| `cache_control` | 0 | 0 | — |
| `chain of thought` / `chain-of-thought` / `think step-by-step` | 8 | 5 | `prompt-engineer/SKILL.md` (3); `prompt-engineer/ARCHITECTURE.md` (2); `prompt-engineer/README.md` (1); `mtg-commander/ARCHITECTURE.md` (1); `mtg-commander/SKILL.md` (1) |
| `tool_choice` / `tool choice` | 0 | 0 | — |
| `parallel tool` / `parallel_tool` | 0 | 0 | — |
| `system prompt` in `SKILL.md` files | 2 | 1 | `prompt-engineer/SKILL.md` (2) |
| `sub-agent` / `subagent` | 314 | 61 | `delivery-team/skills/delivery-flow/SKILL.md` (30); `delivery-team/skills/developer/SKILL.md` (26); `delivery-team/skills/architect/SKILL.md` (18) |
| `SKILL_LOADED` | 35 | 15 | `delivery-team/skills/delivery-flow/references/team-patterns.md` (9); `delivery-team/architecture/sub-agent-dispatch.md` (5); `delivery-team/skills/delivery-flow/references/pipeline-stages.md` (3) |

Zero-match patterns are reported explicitly because their absence is itself a signal: no `extended_thinking`, no `cache_control`, no `tool_choice`, no `parallel_tool`, and no explicit `prompt caching` references exist anywhere in the source plugins.

---

## Section 4 — Skill Size Distribution

Every `SKILL.md` in the repo, sorted descending by total line count. `Frontmatter` = lines from the first `---` to the second `---` inclusive (YAML block at the top). `Body` = total − frontmatter.

| File path | Total lines | Frontmatter lines | Body lines |
|---|---:|---:|---:|
| `mtg-commander/SKILL.md` | 1,181 | 10 | 1,171 |
| `delivery-team/skills/delivery-flow/SKILL.md` | 1,072 | 5 | 1,067 |
| `delivery-team/skills/product-delivery/SKILL.md` | 685 | 5 | 680 |
| `delivery-team/skills/architect/SKILL.md` | 667 | 5 | 662 |
| `agentic-flow-builder/skills/flow-builder/SKILL.md` | 559 | 5 | 554 |
| `delivery-team/skills/presentation/SKILL.md` | 540 | 5 | 535 |
| `delivery-team/skills/ui/SKILL.md` | 490 | 5 | 485 |
| `delivery-team/skills/developer/SKILL.md` | 490 | 5 | 485 |
| `research-agent/SKILL.md` | 471 | 5 | 466 |
| `prompt-engineer/SKILL.md` | 440 | 6 | 434 |
| `delivery-team/skills/operations/SKILL.md` | 414 | 5 | 409 |
| `delivery-team/skills/quality/SKILL.md` | 412 | 5 | 407 |
| `delivery-team/skills/user-feedback/SKILL.md` | 394 | 5 | 389 |
| `delivery-team/skills/godot/SKILL.md` | 231 | 5 | 226 |
| `delivery-team/skills/alias-creator/SKILL.md` | 197 | 5 | 192 |
| `delivery-team/skills/architect/paradigms/ddd/SKILL.md` | 80 | 11 | 69 |
| `delivery-team/skills/architect/paradigms/volatility/SKILL.md` | 66 | 11 | 55 |
| **Total (17 SKILL.md files)** | **8,389** | **102** | **8,287** |

Distribution: 4 skills > 650 lines (`mtg-commander`, `delivery-flow`, `product-delivery`, `architect`). 7 skills in the 400–600 band. 4 skills in the 200–400 band. 2 paradigm sub-skills < 100 lines. Median skill body = 466 lines (`research-agent/SKILL.md`).

---

## Section 5 — Hook Inventory

Only one `hooks.json` exists in the repo: `delivery-team/hooks/hooks.json`. No other plugin ships hooks.

| Plugin | hooks.json path | Hook entries | Event types used | Hook scripts referenced (Python) |
|---|---|---:|---|---|
| `delivery-team` | `delivery-team/hooks/hooks.json` | 7 | SessionStart, Stop, PreToolUse (×2), PostToolUse (×2), SubagentStop | `hooks/check_config.py`, `hooks/audit_agent_prompt.py`, `hooks/validate_gdscript.py`, `hooks/verify_skill_load.py`, `hooks/flag_empirical_validation.py` |

**Breakdown of the 7 hook entries in `delivery-team/hooks/hooks.json`**:

| # | Event | Matcher | Type | Script / prompt reference |
|---:|---|---|---|---|
| 1 | SessionStart | `*` | command | `check_config.py` |
| 2 | Stop | `*` | prompt | inline prompt (retrospective enforcement) |
| 3 | PreToolUse | `Skill` | prompt | inline prompt (pipeline bypass detection) |
| 4 | PreToolUse | `Agent` | command | `audit_agent_prompt.py` |
| 5 | PostToolUse | `Write\|Edit` | command | `validate_gdscript.py` |
| 6 | PostToolUse | `Agent` | command | `verify_skill_load.py` |
| 7 | SubagentStop | `developer\|godot` | command | `flag_empirical_validation.py` |

**Python files under `delivery-team/hooks/`** (8 total, excluding `__pycache__`):

| Path | Role |
|---|---|
| `hooks/check_config.py` | SessionStart command (script) |
| `hooks/audit_agent_prompt.py` | PreToolUse Agent command (script) |
| `hooks/validate_gdscript.py` | PostToolUse Write\|Edit command (script) |
| `hooks/verify_skill_load.py` | PostToolUse Agent command (script) |
| `hooks/flag_empirical_validation.py` | SubagentStop command (script) |
| `hooks/enforce_pipeline_scope.py` | Present in repo, not referenced by `hooks.json` |
| `hooks/lib/__init__.py` | Shared library init |
| `hooks/lib/hook_utils.py` | Shared library helpers |

Two inline LLM-facing prompts in `hooks.json`: the Stop hook (retrospective enforcement) and the PreToolUse/Skill hook (pipeline bypass detection). Both are free-text prompt bodies inside the JSON, not separate files.

---

## Section 6 — Orchestrator-Style Pattern Indicators (delivery-team only)

Scope: everything under `delivery-team/`. Counts are regex match counts (files where the pattern appears listed in parentheses).

| Indicator | Match count | Files |
|---|---:|---:|
| `Agent Invocation Template` | 8 | 3 (`skills/delivery-flow/SKILL.md` (6); `skills/delivery-flow/references/pipeline-stages.md` (1); `skills/delivery-flow/references/team-patterns.md` (1)) |
| `ALIAS` / `alias-theme` / `alias theme` | 30 | 9 (`skills/alias-creator/SKILL.md` (3); `README.md` (2); `skills/delivery-flow/SKILL.md` (6); `skills/delivery-flow/references/pipeline-stages.md` (6); `skills/delivery-flow/references/team-patterns.md` (9); `ARCHITECTURE.md` (1); `CROSS-SKILL-REFERENCES.md` (1); `skills/alias-creator/references/theme-format.md` (1); `skills/delivery-flow/references/config-schema.md` (1)) |
| `DoD validator` | 45 | 18 (top files: `skills/delivery-flow/references/quality-gates.md` (10); `skills/delivery-flow/SKILL.md` (11); `skills/delivery-flow/references/pipeline-stages.md` (2); see full list below) |
| `SKILL_LOADED` | 29 | 11 (top files: `skills/delivery-flow/references/team-patterns.md` (9); `architecture/sub-agent-dispatch.md` (5); `skills/delivery-flow/references/pipeline-stages.md` (3); `architecture/hook-firing-timeline.md` (3); `hooks/verify_skill_load.py` (3)) |
| `Agent tool` / `Task tool` | 33 | 9 (top files: `architecture/sub-agent-dispatch.md` (7); `skills/delivery-flow/SKILL.md` (5); `skills/delivery-flow/references/team-patterns.md` (8); `skills/delivery-flow/references/pipeline-stages.md` (4); `hooks/audit_agent_prompt.py` (4)) |

**`DoD validator` — full file list** (18 files, counts shown):
`skills/delivery-flow/references/quality-gates.md` (10); `skills/delivery-flow/SKILL.md` (11); `ARCHITECTURE.md` (2); `architecture/sub-agent-dispatch.md` (2); `architecture/deterministic-gating.md` (3); `skills/quality/SKILL.md` (1); `skills/delivery-flow/references/troubleshooting.md` (1); `skills/delivery-flow/references/constraints-model-guide.md` (2); `skills/delivery-flow/references/design-sprint.md` (2); `skills/quality/references/empirical-validation.md` (1); `skills/delivery-flow/references/artifact-contracts.md` (1); `skills/delivery-flow/references/pipeline-stages.md` (2); `skills/delivery-flow/references/team-patterns.md` (1); `skills/delivery-flow/references/templates/README.md` (1); `skills/delivery-flow/references/rules/stage-routing.json` (1); `skills/delivery-flow/references/templates/constraints-architect.yml` (2); `skills/delivery-flow/references/setup-wizard.md` (1); `skills/delivery-flow/references/project-types.md` (1).

Concentration observation (purely quantitative): the five delivery-flow files — `SKILL.md`, `references/team-patterns.md`, `references/pipeline-stages.md`, `references/quality-gates.md`, and `architecture/sub-agent-dispatch.md` — appear in the top-3 for every indicator measured in this section.

---

## Section 7 — Data Snapshot Summary

The Claude-Plugins repo comprises six plugins totaling 198 markdown files, 35 Python files, zero shell scripts, 17 `SKILL.md` files spanning 8,389 lines (8,287 body + 102 frontmatter), 14 sub-skills (13 under `delivery-team/skills/` plus 1 under `agentic-flow-builder/skills/`), one `hooks.json` file defining 7 hook entries across 5 event types (SessionStart, Stop, PreToolUse, PostToolUse, SubagentStop) and backed by 8 Python files under `delivery-team/hooks/`, and 38,663 lines of reference documentation (90% of which — 34,870 lines — sits inside `delivery-team/references/`); the model-ID surface area is three hard-coded versioned Claude model strings (`claude-sonnet-4-5-20250929`, `claude-haiku-4-20250514`, `claude-opus-4-20250514`) all colocated in `agentic-flow-builder/scripts/agent_registry.py` plus 8 short-alias references (`"claude-sonnet"`, `"claude-haiku"`) in `prd-quality-gate-flow/stage_definitions.py` and its README, with 21 further short-alias occurrences stored as data inside the `prd_flows.db` SQLite file, and zero model IDs in any `SKILL.md` or hook file; the prompt-pattern signal surface is dominated by sub-agent/orchestrator vocabulary (314 matches across 61 files, concentrated in `delivery-flow/SKILL.md`, `developer/SKILL.md`, `architect/SKILL.md`) and `SKILL_LOADED` signals (35 matches across 15 files), while modern prompt-engineering primitives — `extended_thinking`, `prompt cach*`, `cache_control`, `tool_choice`, `parallel_tool` — return zero matches across the entire repo, and `chain of thought` language appears 8 times across 5 files (all in `prompt-engineer/` and `mtg-commander/`).

---

**End of Scope Baseline.** Numbers are numbers. The council will deliberate.
