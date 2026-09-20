# ADR-lmr-003: Central tier alias, stamp convention, and line-neutral edit math

- **Status**: Accepted (Stage 4 DoD passed 2026-09-20: architect, developer, devops, security, qa all DONE)
- **Date**: 2026-09-20
- **Run**: run-2026-05-28-o48m, BACKLOG-108
- **Owner**: Solution Architect (PRD FR-3.2, FR-3.3, FR-4.1, FR-4.6, FR-2.5, FR-2.6, convention items 1 to 4, OQ-11)

## Context

Model versions are encoded in four places (PRD section 1). The user's binding decision is to name the latest version of a model family and never pin. Two mechanisms carry that in code and metadata: a tier-label alias for code, and version-free SKILL.md stamps.

Verified facts this design rests on:
- Claude Code CLI aliases: https://code.claude.com/docs/en/model-config, fetched 2026-09-20: `opus` "Uses the latest Opus model for complex reasoning tasks", `sonnet` "Uses the latest Sonnet model for daily coding tasks", `haiku` "Uses the fast and efficient Haiku model for simple tasks" (no word "latest" for haiku: OQ-6 stays open). "Aliases point to the recommended version for your provider and update over time." `ANTHROPIC_DEFAULT_OPUS_MODEL` sets the model used for `opus`.
- The Claude API has no evergreen alias for current models (PRD section 8, quotes from platform.claude.com model-ids-and-versions; not re-fetched by this stage).
- Local `claude --help` (CLI 2.1.278) lists `--model`, `--effort`, `--max-budget-usd`, `--bare` (run 2026-09-20).
- The only consumer of a stamp value is `.github/workflows/skill-md-header-warn.yml`, which greps for the presence of `model_awareness:` (read from the file). `grep -rn "model_awareness\|pattern_library_version"` over `*.py *.yml *.sh *.json` outside `.delivery/` finds no other reader. So stamp values can change freely; only presence matters.
- No repo code sends `config.model` to the API (`flow_orchestrator.py:663` is a placeholder comment; `grep` found no `anthropic` import, PRD FR-4.5).

## Decision

**A1. `MODEL_TIER_ALIAS` in `agentic-flow-builder/scripts/agent_registry.py`** is exactly one top-level dict, `{"heavy": "opus", "mid": "sonnet", "light": "haiku"}`, defined once (AST-checked by AC-4.1). The three default-agent entries (currently lines 149, 174, 190) become `"config": {"model": MODEL_TIER_ALIAS["mid"]}` and so on. The three `# canonical ... (retired)` provenance comments (lines 148, 173, 189) are replaced by one identical line each: `# tier alias resolved via MODEL_TIER_ALIAS; earlier versioned IDs are recorded in CHANGELOG.md`. Place the dict above the class that uses it (module level, after imports) so a reader sees the vocabulary first. **`fable` is intentionally NOT a value of this dict (revision 2, loop-2 F4).** The live sub-agents page lists the accepted `model:` values as `sonnet`, `opus`, `haiku`, `fable`, a full model ID, or `inherit`, so `fable` is a valid CLI alias. `MODEL_TIER_ALIAS` maps the three cost tiers (`heavy`, `mid`, `light`) to the three aliases that have a tier meaning here; `fable` has no tier in this registry and no default agent uses it, so it is excluded by decision, not by oversight. Widening is one dict entry plus the AC-4.6 alternation (A3), made when an agent first needs it. `inherit` is not a tier alias and is likewise out of the closed set.

**A2. The value is a Claude Code CLI alias, not an API model ID.** `config.model` holds `opus` and would be rejected by the API. Therefore `flow_orchestrator.py:663` is reworded (FR-4.5): the API call reads one configured model ID; `config.model` is a CLI tier alias. Convention: code that must call the Claude API reads one environment or config value and never a literal.

**A1a. Scope of the single definition point (revision 1, F6).** "One Python definition" (NFR-12) covers `agentic-flow-builder/scripts/agent_registry.py` ONLY. `prd-quality-gate-flow/stage_definitions.py` holds a second, differently spelled tier vocabulary (`"model": "claude-sonnet"` at lines 51, 87, 154, 185 and `"claude-haiku"` at 119, 220, 247; also `prd-quality-gate-flow/README.md` line 306). Those labels contain no digit, so `PIN_RE` does not match them and S4 does not touch them: out of scope, guard-neutral, by decision. Nobody should read NFR-12 as repo-wide. If those files ever call the CLI, they should adopt the `opus|sonnet|haiku` vocabulary in a separate change.

**A3. Frontmatter aliases** (`model:` in 4 files, `phase_1_detector_model:` in 5) cannot import Python. They are held to the vocabulary `opus|sonnet|haiku` by AC-4.6 instead of a single location. NFR-12 counts exactly one Python definition plus these nine lines. **The vocabulary is a deliberately closed set (F7).** The live CLI reference lists a fourth documented alias, `fable` (`claude --help` for `--model` prints `'fable', 'opus', or 'sonnet'` and the full-name example `claude-fable-5`; the guard's `PROSE_RE` already knows Fable and Mythos). `model: fable` in a frontmatter would fail AC-4.6 today, on purpose: no skill uses it. Widening the vocabulary is one edit to the AC-4.6 alternation (one place), made when a skill first needs it.

**A4. Stamp convention** in the 25 stamped SKILL.md (26 `model_awareness` lines, 26 `pattern_library_version` lines): `model_awareness: latest`, `pattern_library_version: rev-1`, `last_audited: 2026-09-20` (the date of the S3 DoD pass, per FR-3.3; use the actual date), `fitness_review_due:` reset in the 11 files that carry it, STAGGERED (revision 3, loop-3 F15): `governance/fitness-review.md` line 34 says the field is staggered across an 80 to 100 day window so reminder issues distribute, and `fitness-review.yml` opens one reminder per due date, so 11 identical dates would fire 11 reminders in one week. Rule: sort the 11 files by path; file i (0 to 10) gets `S3_date + 20 + 7*i` days, which stays after today and within 90 days (AC-3.3a still passes). Computed this revision for `S3_date = 2026-09-20`: first `2026-10-10`, last `2026-12-19` (exactly +90). The S3 developer recomputes from the actual S3 date. Every edit replaces the VALUE on an existing line. No line is added or removed. The 9 unstamped SKILL.md stay unstamped.

**A5. `delivery-flow/SKILL.md` frontmatter `model: sonnet` is unchanged** (OQ-11 confirmed; AC-2.6). Re-tiering the orchestrator is a cost and behaviour decision nobody has made, and the new guidance is conditional ("when the orchestrating session runs the latest Opus") and holds for any model.

**A6. Stamp semantics** (documented in the prompt-engineer stamp-doc block): `latest` means "written for whichever model is latest at `last_audited`". The date is the anchor; the quarterly fitness review (`fitness_review_due`) is the trigger to re-verify version-free guidance (risk R7).

**A6b. Stated limit of the uniform stamp (revision 3, loop-3 F7).** Under NARROW (BINDING-6.1) only 3 SKILL.md get a prose review, but all 25 stamped files get `latest` and `last_audited`. Before this change 19 of the 26 `model_awareness` lines read `opus-4-7-frontmatter-only`, a falsifiable marker that the file had NOT been prose-reviewed; the PRD-fixed value `latest` deletes it. Memory records the opposite rule twice (`.delivery/memory/archive/retrospective-run-2026-04-20-o4v7.md` line 79: "a false claim wearing a truthful sleeve"; `run-2026-04-22-4x7e.md` line 46: "mechanical uniform stamping would lie cheaply"). The value stays (PRD fixes it), but the design keeps it honest: (1) for every stamped file NOT in the prose ledger (22 by the loop-3 count, 25 minus the 3 reviewed; S3 computes the exact set) `last_audited` records the MECHANICAL STAMP DATE only, not a review, and `latest` on those files certifies nothing about their prose; (2) S3 writes `06-development/stamp-only-ledger.tsv` listing each of those paths with the label `stamp-only, not prose-reviewed` (row count = stamped files minus prose-ledger files, checked by S3); (3) the residual is raised to the PO as Plan decision P21 (owner PO). The falsifiable distinction is thus kept in a ledger rather than in the frontmatter value.

**A6a. `model_awareness` semantics and the value `latest` (revision 2, loop-2 F5).** Every reader and definer of the key, from `git grep -n model_awareness` outside `.delivery/`: (1) `.github/workflows/skill-md-header-warn.yml` lines 21 to 35 test PRESENCE only (`grep -L 'model_awareness:'`), so `latest` passes; (2) `prompt-engineer/SKILL.md:420` DEFINES the key as "the model generation the skill was authored or last re-audited against", which contradicts a `latest` stamp (a generation name is version-shaped, `latest` is a moving reference); (3) `delivery-team/skills/delivery-flow/SKILL.md:491` says the key "may change on model migration", which stays true and needs no edit (delivery-flow is at 499 of 500 lines and this line is not a version claim). Decision: UPDATE (2). It is inside the S2(b) prompt-engineer dispatch and unbudgeted (no tier key); the edit is one line replaced by one line, so line delta is 0. Proposed text, replacing line 420, keeping the bullet form:
```
- `model_awareness` — `latest`: the skill is written for whichever model is the latest at `last_audited`. It names no generation; the date is the anchor.
```
and line 421 (`last_audited`) reads "ISO-8601 date of the most recent review against the latest model at that date." Line 420 is in the FR-2.1 rewrite list (architecture.md section 4, S2); line 421 is an added edit inside the same file and the same dispatch, and neither new text contains a version, so the guard stays at 0 hits. Sources for the wording: this decision (A6) and PRD FR-3.2. No requirement changes: FR-3.2 already fixes the value `latest`; this only removes a contradicting definition.

## Line-budget batching math (required proof)

Rule: the 25 stamp edits and the 3-file prose edits add zero lines. Numbers are from commands run 2026-09-20, `wc -l` before, and a scratch-copy simulation of the edits after (regex value replacement for stamps; the prose blocks in architecture.md section 4, S2, "Exact delivery-flow rewrite"). Nothing in the working tree was modified.

Budget-checked files (`python3 scripts/check_skill_budgets.py` on the current tree: `BUDGET CHECK PASSED: 17 file(s) checked, 0 known-debt, 0 exception(s).`, exit 0):

| File (tier) | Budget | `wc -l` before | + stamp edits (value-only) | + prose rewrite | `wc -l` after | Headroom after | `--check --tier` on simulated file |
|---|---|---|---|---|---|---|---|
| `delivery-team/skills/delivery-flow/SKILL.md` (A) | 500 | 499 | +0 | 4 lines to 4 lines (lines 27 to 30) and 4 to 4 (lines 273 to 276): +0 | 499 | 1 | PASSED, exit 0 |
| `delivery-team/skills/product-delivery/SKILL.md` (B) | 300 | 300 | +0 | none (no version mention; ledger only, PRD FR-3.1) | 300 | 0 | PASSED, exit 0 |
| `delivery-team/skills/developer/SKILL.md` (B) | 300 | 299 | +0 | none | 299 | 1 | PASSED, exit 0 |
| `delivery-team/skills/godot/SKILL.md` (C) | 200 | 200 | +0 | none | 200 | 0 | PASSED, exit 0 |
| `delivery-team/skills/alias-creator/SKILL.md` (C) | 200 | 199 | +0 | none | 199 | 1 | PASSED, exit 0 |

Math for the one file that gets prose edits and is at cap: `499 -> +0 (stamps, in place) -> +0 (block 1: 4 lines replaced by 4 lines) -> +0 (block 2: 4 lines replaced by 4 lines) -> 499 <= 500`. The rewrite must keep each block at exactly four lines; the S2 developer verifies `wc -l` after the edit and before handing back.

All 25 stamped files, `wc -l` before and after the simulated stamp edits (delta 0 for every one, total 9,056 to 9,056):

| File | Lines | File | Lines |
|---|---|---|---|
| `agentic-flow-builder/skills/flow-builder/SKILL.md` | 562 | `hardware-team/skills/hardware-flow/SKILL.md` | 1023 |
| `delivery-team/skills/alias-creator/SKILL.md` | 199 | `hardware-team/skills/hw-product-owner/SKILL.md` | 310 |
| `delivery-team/skills/architect/SKILL.md` | 294 | `hardware-team/skills/manufacturing-engineer/SKILL.md` | 401 |
| `delivery-team/skills/architect/paradigms/ddd/SKILL.md` | 86 | `hardware-team/skills/pcb-layout-engineer/SKILL.md` | 329 |
| `delivery-team/skills/architect/paradigms/volatility/SKILL.md` | 72 | `hardware-team/skills/test-engineer/SKILL.md` | 405 |
| `delivery-team/skills/delivery-flow/SKILL.md` | 499 | `mtg-commander/SKILL.md` | 1184 |
| `delivery-team/skills/developer/SKILL.md` | 299 | `prompt-engineer/SKILL.md` | 520 |
| `delivery-team/skills/godot/SKILL.md` | 200 | `research-agent/SKILL.md` | 488 |
| `delivery-team/skills/operations/SKILL.md` | 219 | `hardware-team/SKILL.md` | 53 |
| `delivery-team/skills/presentation/SKILL.md` | 185 | `hardware-team/skills/compliance-engineer/SKILL.md` | 292 |
| `delivery-team/skills/product-delivery/SKILL.md` | 300 | `hardware-team/skills/electrical-engineer/SKILL.md` | 353 |
| `delivery-team/skills/quality/SKILL.md` | 289 | | |
| `delivery-team/skills/ui/SKILL.md` | 222 | | |
| `delivery-team/skills/user-feedback/SKILL.md` | 272 | | |

Files that are not budget-checked (the checker covers the 17 `delivery-team` skills that carry `tier:`; the `hardware-team`, `mtg-commander`, `research-agent`, `agentic-flow-builder` and `prompt-engineer` files have no tier key) still hold at delta 0 because the edit is value-only. Frontmatter presence counts from the simulation: 25 of 25 have `model_awareness`, `pattern_library_version` and `last_audited`; 11 have `fitness_review_due`; so every AC-3.3a target line exists and no line has to be inserted.

`prompt-engineer/SKILL.md` (520 lines, no tier key) is the only file where the prose review changes structure (the versioned-model-reference block becomes a config-read pattern and a family heading). It has no budget cap, so line growth is not constrained, but the reviewer keeps it net-neutral or negative to avoid drift.

Rollout check (memory lesson: any ADR adding lines to ALL files must verify at-cap files): this decision adds zero lines to any file, so no at-cap file needs headroom. The at-cap files are delivery-flow (1 spare), product-delivery (0), godot (0), alias-creator (1), developer (1). None is edited beyond in-place values, except delivery-flow's two 4-line blocks.

## Alternatives rejected

| Alternative | Why rejected |
|---|---|
| Delete the stamp lines (no stamps) | Removes lines (helps budgets) but the header-warn workflow reads `model_awareness:` presence and would warn on all 25; it also discards the `last_audited` anchor the quarterly review relies on. The PRD decided to keep version-free stamps. |
| Stamp value `opus` or another alias | It re-introduces a per-family value into 25 files and would still need edits when a new family appears; `latest` is family-neutral. |
| Add stamps to the 9 unstamped files | A `latest` stamp with no audit date certifies nothing; edit with no purpose (PRD FR-3.2). |
| Full API model ID in `MODEL_TIER_ALIAS` | Puts a version string in code (the defect being removed) and needs an edit per release. |
| Tier dict read from environment | Adds a runtime dependency for labels that nothing uses today; the alias is a label for the CLI. Revisit only when a real API caller exists. |
| Put the alias vocabulary in a shared YAML read by both Python and the frontmatter | Frontmatter is parsed by Claude Code, not by this repo; there is no consumer that could read a shared file. AC-4.6 pins the vocabulary instead. |
| Re-tier delivery-flow to `model: opus` | Cost and behaviour decision, out of scope (FR-2.6). |

## Consequences

- One Python definition point plus nine frontmatter lines; the guard cannot enforce a single location for the nine, so AC-4.6 must keep printing `violations 0`.
- Registry rows already persisted in a user's local SQLite database keep whatever `config.model` they were inserted with: `_load_default_agents` returns early when a `general` agent already exists (verified in `agent_registry.py`, lines 135 to 139). No database is tracked in the repo (`git ls-files` shows none), so nothing in the repo is stale, but a developer with an old local database still holds the retired ID in that row. Nothing reads `config.model` today, so it is harmless; logged as risk P9 in architecture.md section 7.
- The alias may resolve differently per provider (`sonnet` differs on every non-Anthropic provider per the PRD table); the scheme claims only "latest for your provider" (R9).
- Guidance written as "latest Opus" can go stale silently (R7); the mitigation is the date anchor plus the quarterly review, and `fitness_review_due` is reset in this initiative.

## Status rationale

Accepted (Stage 4 DoD passed 2026-09-20).
