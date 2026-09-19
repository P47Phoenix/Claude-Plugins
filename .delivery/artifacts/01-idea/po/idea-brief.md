# Idea Brief: Update model literals to the latest model set

Stage: 1 (Idea, LIGHT) | Type: FEATURE | PO: Gandalf | Branch: delivery-team-agent-wrappers (PR #88 worktree)
Supersedes: previous run's brief at this path. Retargets BACKLOG-108 (see last section).

> A product owner is never late, nor early. They prioritize precisely when they mean to.

## Request

User: "models should be updated to the latest models". Scope chosen: **all model literals in the repo** (outside `.delivery/` history).

Latest set (user's environment; IDs cross-checked against the claude-api skill's model table, cached 2026-06-24):

| Tier | Target ID | Verified | Note |
|---|---|---|---|
| Frontier | `claude-fable-5-1` | yes (skill table) | Added by user scope correction. Different API behavior from Opus family (see Constraints). |
| Heavy | `claude-opus-5` | yes | Replaces `claude-opus-4-7` (and BACKLOG-108's `claude-opus-4-8` target) |
| Mid | `claude-sonnet-5` | yes | Replaces `claude-sonnet-4-6` |
| Light | `claude-haiku-4-5-20251001` | repo already uses it; skill table lists alias `claude-haiku-4-5` | Unchanged per user. Dated form remains the repo convention. |

Verification caveat: the skill's table is a cache dated 2026-06-24; Refine should re-confirm against the live models page before the allowlist is frozen.

## Discovery (commands run, non-`.delivery/`)

`grep -rnoE 'claude-(opus|sonnet|haiku)-[0-9]...'` over the tree (fable not yet present anywhere; zero `claude-fable` hits expected and to be confirmed).

| File | Lines | Literal(s) | Live or provenance |
|---|---|---|---|
| `agentic-flow-builder/scripts/agent_registry.py` | 148, 149 | `claude-sonnet-4-5-20250929` (comment), `claude-sonnet-4-6` (live config) | 149 live |
| | 173, 174 | `claude-haiku-4-20250514` (comment), `claude-haiku-4-5-20251001` (live) | 174 live, unchanged |
| | 189, 190 | `claude-opus-4-20250514` (comment), `claude-opus-4-7` (live) | 190 live |
| `delivery-team/tests/smoke/tests/conftest.py` | 105, 117, 129, 151 | `claude-opus-4-7` (fixture strings) | live fixtures |
| `prompt-engineer/SKILL.md` | 368 | `claude-opus-4-7` (`MODEL_ID` code literal) | live |
| `delivery-team/references/telemetry-schema.md` | 36 | `claude-sonnet-4-6` | doc example |
| `delivery-team/architecture/smoke-test-architecture.md` | 115, 116 | `claude-opus-4-7`, `claude-sonnet-4-6` | doc examples |
| `.github/workflows/stale-model-id-guard.yml` | 23-25, 30-31, 39 | allowlist of opus-4-7 / sonnet-4-6 / haiku-4-5-20251001 | guard config |

Totals: 22 literal hits across 6 files plus the guard. Regex in the guard (`claude-(opus|sonnet|haiku)-4[-.][^7]...`) only flags 4.x IDs, so `claude-opus-5` / `claude-sonnet-5` / `claude-fable-5-1` currently pass silently and, conversely, `claude-opus-4-7` and `claude-sonnet-4-6` are allowlisted, so the guard would not object to leaving old IDs in place.

## Survey (counts only; no decisions)

- `model_awareness:` stamps in SKILL.md: 26 lines across 25 files (7 x `opus-4-7`, 19 x `opus-4-7-frontmatter-only` per grep count; BACKLOG-108 recorded 18, includes a possible second stamp in `prompt-engineer/SKILL.md` at `:6` and `:415`).
- `model:` frontmatter: 15 files (11 in `delivery-team/agents/*.md`, 2 paradigm SKILL.md, `delivery-flow/SKILL.md`, `prompt-engineer/SKILL.md`); values are family aliases only: 14 x `model: sonnet`, 1 x `model: opus`. No versioned IDs, so these do not go stale by ID.
- Prose naming versions ("Opus 4.7", "Sonnet 4.x"): 11 lines in 5 files: `CHANGELOG.md` (history, x2), `orchestrator-doctrine.md:77`, `delivery-flow/SKILL.md:27,273`, `prompt-engineer/SKILL.md` (88, 347, 356, 397, 408), guard message text. Several are behavior claims tied to 4.7 (F-08 fusion, `xhigh` default) rather than mere labels.
- Hooks/scripts naming models: `prd-quality-gate-flow/stage_definitions.py` (`claude-sonnet`, `claude-haiku` family aliases, version-agnostic, exempt per BINDING-1.4), `.claude-plugin/marketplace.json` (prose mention only). No hook in `hooks/` pins a versioned ID.
- `governance/cache-prefix-hash.txt` holds a sha256 of `delivery-team/skills/delivery-flow/SKILL.md`; it must be re-frozen after any edit to that file.

## Goals

1. Every live model ID literal in scope points at the latest set: `claude-opus-5` (heavy), `claude-sonnet-5` (mid), `claude-haiku-4-5-20251001` (light, unchanged), with `claude-fable-5-1` handled per the Fable questions below.
2. The CI guard is inverted to a positive allowlist of the final set, so stale IDs fail and future rollovers are one-line changes (allowlist-over-deny, per memory lesson).
3. Smoke tests and telemetry fixtures keep passing with the new IDs.
4. Provenance is preserved: retired IDs survive only in `#` comments or `>` blockquotes.

## In scope

- The 6 files above with live literals, plus rewriting `stale-model-id-guard.yml`.
- Doc examples that quote IDs (`telemetry-schema.md`, `smoke-test-architecture.md`).
- `governance/cache-prefix-hash.txt` re-freeze if `delivery-flow/SKILL.md` changes.
- CHANGELOG entry.

## Out of scope (proposed; Refine confirms)

- `model_awareness:` stamp values and `pattern_library_version` / `last_audited` (25 files). Proposed default: not touched in this run, because a stamp asserts a full prose audit against a model and a bulk rewrite without the audit would be dishonest (BACKLOG-108 explicitly funded the audit; this request does not). Open question 1.
- Prose behavior claims about 4.7 (F-08, `xhigh`) in SKILL.md files. Rewriting them requires doc-verified Opus 5 behavior; propose deferring to a separate audit item, but fix any sentence that becomes factually wrong because an ID literal changed.
- Family-alias `model:` frontmatter (`opus` / `sonnet`) and `prd-quality-gate-flow` aliases: version-agnostic, no change.
- `.delivery/` history, `CHANGELOG.md` historical entries.
- Wiring Fable into any role (unless Refine decides yes; see questions).

## Constraints

- **CI is static grep only.** No `claude` CLI in workflows (memory: feedback_claude_code_local_only). Guard must stay a `git ls-files | grep` job.
- **Guard mechanics.** Positive allowlist; provenance-comment exemption (`#` lines and `>` blockquotes) retained; no dual-allow window (BINDING-2.1 carried over); ship as one atomic change so the guard never sees a mixed state. The guard's path filter covers `**/*.py` and `**/*.md` only, so YAML/JSON literals are not scanned; Refine should decide whether to widen it.
- **Smoke harness.** `delivery-team/tests/smoke/tests/conftest.py` fixture strings and the telemetry schema example must stay mutually consistent, and existing smoke tests must pass. Fixture edits should be made separately from harness logic edits (BINDING-4.5).
- **Governance.** SKILL.md line budgets (`scripts/check_skill_budgets.py`) must still pass; `cache-prefix-hash.txt` must match final `delivery-flow/SKILL.md`; edits to skills go through `plugin-dev:skill-development` per CLAUDE.md.
- **Fable API differences** (from claude-api skill, to be re-verified): thinking always on (explicit `budget_tokens`/`disabled` returns 400), forced `tool_choice` returns 400, no sampling params, no prefill, `refusal` stop reason needs handling with fallbacks, 30-day retention required (no ZDR), no Priority Tier, pricing $10/$50 per MTok vs Opus 5 at $5/$25. Any code path that sends requests to a Fable ID needs these handled; nothing in this repo currently calls the API directly except the registry's config values, so risk is mainly downstream consumers.
- **Sonnet 5 / Opus 5 differences**: `budget_tokens`, sampling params and prefill rejected; Opus 5 thinking on by default. Repo Python does not appear to send these, to be confirmed in Refine by grep.

## Open questions for Refine

1. Stamps: leave `model_awareness` values at `opus-4-7` (now inaccurate), bump uniformly, or drop the field? If bumped, does a full prose audit come with it (BACKLOG-108 answer: yes)? Recommend separate follow-up backlog item.
2. Do the `claude-opus-4-7` strings in `conftest.py` and `smoke-test-architecture.md` need to change, or are they opaque telemetry fixtures? Recommend change to keep fixtures and real-world IDs aligned, unless a test asserts on the literal.
3. Guard design: flag any `claude-(opus|sonnet|haiku|fable)-` ID not on the allowlist (recommended, covers 4.x, 5.x, future), or keep a deny regex for `claude-opus-4-x` / `claude-sonnet-4-x`? Should `claude-fable-5-1` be allowed alongside the others? Should `claude-opus-4-8` / `claude-fable-5` / `claude-mythos-*` be explicitly rejected or just unlisted?
4. **Fable roles**: which call sites or roles, if any, should use `claude-fable-5-1` versus Opus 5 / Sonnet 5? Candidates only, not decided: a new top "frontier" tier in `agent_registry.py` default agents, the orchestrator or architect agent, adversarial review, or none (allowlist only, no usage). Cost at 2x Opus and the API constraints above are the trade-off.
5. Should the registry gain a fourth default agent for Fable, or should the existing `claude-opus` agent map to Opus 5 only?
6. Haiku: keep the dated `claude-haiku-4-5-20251001` (repo convention, user said unchanged) even though the current docs alias is `claude-haiku-4-5`. Confirm the guard allowlist accepts the dated form.
7. Widen the guard's scanned paths (`*.yml`, `*.json`, `*.txt`) so future literals in those types are caught?
8. Ship mode: PR onto this branch (#88 is open) versus BACKLOG-108's direct ff-merge; and whether `.delivery/` history is exempt (yes, by existing pathspec).
9. Live-doc verification: who re-checks the four IDs against Anthropic's models page before the allowlist merges?

## BACKLOG-108 disposition

BACKLOG-108 (untracked, main checkout, IN PROGRESS) targets `claude-opus-4-8`, which is now behind the user's latest model (`claude-opus-5`) and was never shipped. Proposal: **supersede and retarget**, not run in parallel.

- Carry forward: positive-allowlist guard, no dual-allow window, provenance-comment exemption, atomic ship, static-grep-only CI, smoke fixture edits separate from harness edits, `cache-prefix-hash` re-freeze, family-alias exemption for `prd-quality-gate-flow`.
- Retarget: heavy ID `claude-opus-4-8` -> `claude-opus-5`; mid `claude-sonnet-4-6` -> `claude-sonnet-5`; add `claude-fable-5-1` decision.
- Drop or split out: BACKLOG-108 S3 (full prose sweep of 34 SKILL.md, 9 new stamps) and S5 (smoke harness metrics extension, `--effort xhigh`, 5-sample baseline against a live model) as separate items, since the user's request is literal-scoped and S5 needs a live `claude` run that CI cannot do.
- Memory topic `opus-4-8-migration.md` is authoritative for BACKLOG-108 only; mark its Section 1 lineup table as superseded by this run and record the new lineup as a new topic during the memory update. Exists in the main checkout, not in this worktree.

## Success signal

`git grep` for retired IDs (`claude-opus-4-7`, `claude-sonnet-4-6`, and any 4.x) returns only comment/blockquote provenance; the rewritten guard passes on the change and fails on an injected stale ID; smoke tests, `check_skill_budgets.py`, and the cache-prefix hash check all pass.

## Next

Refine: resolve open questions 1-4 first (stamps, fixtures, guard shape, Fable roles); the rest have recommended defaults.
