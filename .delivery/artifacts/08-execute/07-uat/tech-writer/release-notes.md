# Release: Opus 4.7 Migration (run-2026-04-22-4x7e)

**Date:** 2026-04-22
**Branch:** feature/opus-4-7-migration-run-2026-04-22-4x7e
**Scope:** Claude-Plugins marketplace — all 6 plugins

## Summary

I think I'm quite ready for another documentation adventure. Now, where was I? Ah yes — Chapter 14, "An Unexpected Model Upgrade." This was, as these tales go, a mostly-ordinary journey. No dragons, thank the stars. No Balrogs in the agent registry. Just a marketplace of six plugins that needed to cross a narrow bridge from the comfortable country of Opus 4.6 assumptions into the thinner, colder air of Opus 4.7 — where instructions are read more literally, where adaptive thinking has quietly replaced the old `budget_tokens` knob, and where the catalogue of canonical model IDs is no longer quite what it was at breakfast. Fourteen work items were packed, four waves of walking were done, and every member of the Fellowship carried a share of the weight. We annotated where we could, rewrote prose only where we must, and stamped an honest little "frontmatter-only" tag on the skills whose prose the party had not time to read word-by-word. No dragons, no stones in the shoe, and — most precious of all — no breaking changes. The ring, if I may say so, went quietly into its box.

## What changed

### Model ID migration

**Canonical sweep in `agentic-flow-builder/scripts/agent_registry.py`.**
Three `default_agents` entries were moved from retired dated IDs to the
2026-04-22 canonicals:

- Sonnet `claude-sonnet-4-5-20250929` → `claude-sonnet-4-6`
- Haiku `claude-haiku-4-20250514` → `claude-haiku-4-5-20251001`
- Opus `claude-opus-4-20250514` → `claude-opus-4-7`

Each swap carries a single-line provenance comment citing F-04 and the
prior ID, so the history of the string is visible above the live value
rather than erased from it. The Opus comment additionally inlines the
`2026-06-15` retirement date per kickoff requirement.

**`prd-quality-gate-flow/stage_definitions.py` — comment-annotate only.**
A structural check of `flow_orchestrator.py` (per AC-01.5) confirmed the
seven `"model": "claude-sonnet"` / `"claude-haiku"` entries are internal
routing labels and never reach the Anthropic SDK. The evidence:

- Zero `anthropic` imports in `flow_orchestrator.py`.
- Zero reads of `config['model']` anywhere in `prd-quality-gate-flow/`.
- Execution is simulated via `_simulate_agent_output` (line 413) with
  canned responses per `agent_type`.
- A frank `TODO` at line 279 marks the dispatcher as a placeholder:
  "Actually execute agent using Claude Code Task or other agent system."

A single block comment at the head of `STAGE_DEFINITIONS` records all of
this and covers the seven lines (47, 83, 115, 150, 181, 216, 243) at
once — cleaner than seven repeated comments, and still visible to
anyone editing any stage. Substitution here would have claimed an API
contract we do not yet have; honesty was the better craft.

### SKILL.md 4.7-awareness
- **6 keystone SKILL.md files reviewed against 4.7 and stamped `model_awareness: opus-4-7`.** These are `delivery-team/skills/delivery-flow/SKILL.md`, `prompt-engineer/SKILL.md`, `research-agent/SKILL.md`, `delivery-team/skills/product-delivery/SKILL.md`, `delivery-team/skills/architect/SKILL.md`, and `mtg-commander/SKILL.md`. Each carries the full three-field frontmatter block (`model_awareness` / `last_audited` / `pattern_library_version: 4-7-1`) under ADR-006 Option A.
- **11 non-keystone SKILL.md files frontmatter-backfilled as `model_awareness: opus-4-7-frontmatter-only`.** The suffix is load-bearing: it honestly distinguishes mechanical metadata backfill from prose-reviewed keystones, and it tells any future reader which files are still waiting for a word-by-word skim. Backlog item #81 tracks the upgrade pathway. Sum across the marketplace: 6 + 11 = 17 SKILL.md files, 100% coverage.
- **`delivery-flow/SKILL.md` F-08 dispatch annotation (WI-04).** Two small blockquote callouts (135 words total, well inside the 60–150 word envelope) mark DISP-01 and DISP-02 — the pair of load-bearing dispatch invariants under 4.7 semantics, namely that dispatched role count MUST equal the `dod_validators.<stage>` list length, and that "One Role = One Sub-Agent" has been promoted from stylistic convention to behaviourally load-bearing. Zero prose was rewritten; seventeen lines were inserted.
- **`prompt-engineer/SKILL.md` PAT-01 reframe + six new Pattern 4.N sub-sections (WI-05).** PAT-01 now explicitly distinguishes `<thinking>` prompt scaffolds (which on 4.7 may duplicate adaptive-thinking output) from the Anthropic extended-thinking API surface. Six new sibling patterns were added at exact-regex-matching headings:
  - Pattern 4.1 — Versioned Model Reference (F-01 / F-03 / F-04, provenance comment format)
  - Pattern 4.2 — 4.7-Aware Role Prompt Skeleton (SKILL / TASK_TYPE / ROLE / ALIAS / … / SIGNAL BLOCK)
  - Pattern 4.3 — Manual CoT Fallback (when, and when not, to prefer the API lever)
  - Pattern 4.4 — Calibrated Instruction Voicing (`CRITICAL:` reserved for irreversibles)
  - Pattern 4.5 — Model-Specific Optimisation Sub-section (self-referential convention)
  - Pattern 4.6 — SKILL.md Forward-Compatibility Header (ADR-006 three-field frontmatter)
  The anchors `#pattern-4-1` through `#pattern-4-6` are now citable by name from sibling SKILL.md files — see `research-agent/references/prompt-library.md:10` where the Step-by-Step Analyzer teaching line was retargeted to cite Pattern 4.3 rather than re-teach `<thinking>` scaffolding inline.

### Adversarial and research dogfood results
- **mtg-commander Challenger dogfood PASSED AC-04.2 on Opus 4.7.** A simulated Sol-Ring-in-aristocrats scenario produced 6 weaknesses, 6 card-specific referents, and 5 concrete alternatives against thresholds of 3/2/1. The soften-hatch was not invoked; the existing per-challenger prose (structural minimums, script invocations, divergence thresholds) already embodies Pattern 4.4 calibrated voicing. No tone-strengthening prose edit was required — only a one-line rephrase at `mtg-commander/SKILL.md:825` replacing the phrase "chain-of-thought" with "internal reasoning trace" to keep the DX-M3 end-state grep clean. Sample at `.delivery/artifacts/08-execute/06-dev/user-feedback/adversarial-4-7-sample.md`.
- **research-agent tool-use probe PASSED.** A RAG-citation-formats query exercised the `WebFetch` / `WebSearch` surface the skill would actually hit: 4 tool calls across 5 distinct hostnames (`aclanthology.org`, `arxiv.org`, `docs.anthropic.com`, `platform.claude.com`, `www.mdpi.com`), every OUTPUT bullet carrying at least one inline URL. AC-03B.2's hardened floor of `tool_calls ≥ 2 AND distinct_hostnames ≥ 2` was cleared with room to spare. Frontmatter-only change applied; no prose edit to "Tool Use" section needed because the skill's existing Integrity Constraints already forbid the failure modes the probe exercises.
- **alias-theme voice preservation PASSED (3/3 themes, 100%).** Three sampled themes — `lotr` (Gandalf), `star-wars` (Mon Mothma), `dilbert` (Pointy-Haired Boss) — each rendered a Refine stage-announcement carrying 5/5 voice markers (15/15 aggregate). M-05 target was ≥80%; we cleared it at 100%. No YAML theme edits applied; the `alias-creator/SKILL.md` was explicitly out of scope. Sample at `.delivery/artifacts/08-execute/06-dev/user-feedback/alias-theme-sample.md`.

### CI guards

**New `skill-md-header-warn.yml` — warning-only guard.**
Triggers on any `**/SKILL.md` path in a PR. The core step runs
`git ls-files '*SKILL.md' ':!:.delivery/*' | xargs grep -L 'model_awareness:'`;
if any file lacks the marker, it writes the list to `$GITHUB_STEP_SUMMARY`
under a "missing model_awareness header" heading, sets `missing=1` in
`$GITHUB_OUTPUT`, and a follow-up step emits a `::warning::` workflow
command so the warning surfaces in the PR checks UI. The step uses
`continue-on-error: true` so a non-empty list does not fail the job; and
`set -uo pipefail` (not `-e`) keeps the benign non-zero-when-all-match
behaviour of `grep -L` from colouring the job red. Warning-only was a
deliberate choice: the marker taxonomy (paradigm tags, routing
refinements) is still settling, and a hard block would slow contributors
more than the signal is worth. It exists as a regression tripwire now
that WI-11 has achieved 100% coverage on HEAD.

**New `stale-model-id-guard.yml` — blocking guard (calibrated regex).**
Triggers on `**/*.py` and `**/*.md` with `!.delivery/**` exclusion. The
core regex `claude-(opus|sonnet|haiku)-4[-.][^7][^[:space:]"'#]*`
catches dated legacy IDs and 4.5/4.6 Opus references while letting
canonical 4.7 through. A four-layer `grep -vE` allowlist then strips, in
order:

1. `claude-sonnet-4-6(\b|[^0-9-])` — the canonical Sonnet family ID.
2. `claude-haiku-4-5-20251001` — the canonical dated Haiku ID.
3. `^[^:]+:[^:]+:[[:space:]]*#` — Python/YAML comment lines (drains the
   three provenance lines in `agent_registry.py` preserved by WI-10).
4. `^[^:]+:[^:]+:[[:space:]]*>` — markdown blockquote lines (safety net
   for documentation that quotes historical IDs inside `>` blocks).

Dry-run on HEAD: zero blocking hits; three raw hits, all three drained
by filter #3. Calibration note for future authors: the PRD's original
M-01 regex `claude-(opus|sonnet|haiku)-4[.-]6` would have
false-positived on our canonical Sonnet `claude-sonnet-4-6`. WI-10
flagged the contradiction to WI-14 at the dev-log level, and WI-14
resolved it with the allowlist-over-deny approach. This means a future
Haiku 4.7 landing will need one additional allowlist line rather than a
regex rewrite, which is, in this chronicler's opinion, the kinder shape
to leave for whoever walks the road next.

**Existing `workflow-injection-lint.yml` preserved (Constraint 6).**
Both new workflows mirror its structural shape — `name:` / `on:` /
`permissions:` / `jobs:` as top-level keys — and neither contains
`${{ github.event.* }}` inside any `run:` block. The DEFECT-004
regression guard is therefore intact; the AST-style injection scanner
returns `CLEAN` for both new files. Permissions are `contents: read`
only, matching the minimum-privilege shape of the existing lint.

### Deferred scope
Nine items were registered as deferred scope, each with a local `.delivery/backlog/BACKLOG-47-*.md` file and a matching GitHub issue labeled `backlog-47`. The dual-write invariant (local count = issues count, both ≥ 6) was verified: 9 local files, 9 issues, equal counts.
- `BACKLOG-47-task-budget-eval.md` (#77) — evaluate `task_budget` (beta) adoption across agentic flows
- `BACKLOG-47-memory-tool-eval.md` (#78) — evaluate client-side `memory` tool adoption
- `BACKLOG-47-sdk-wiring-routing-via-claude-api.md` (#79) — Anthropic SDK adoption pathway via the `claude-api` skill
- `BACKLOG-47-r-06-cyber-safeguard.md` (#80) — narrow cyber-safeguard refusal check for architect security/IR references
- `BACKLOG-47-frontmatter-only-prose-skim.md` (#81) — upgrade the 11 backfill SKILL.md files from `opus-4-7-frontmatter-only` to `opus-4-7` via prose skim
- `BACKLOG-47-overpressure-audit.md` (#82) — keystone SKILL.md audit for `CRITICAL:` / `MUST` / `NEVER` / `ALWAYS` over-pressure patterns
- `BACKLOG-47-contributing-4-7-note.md` (#83) — add a 4.7-awareness note to CONTRIBUTING guidance (Galadriel on-ramp P-2)
- `BACKLOG-47-migration-guide-stub.md` (#84) — publish a 4.6 → 4.7 migration guide stub (Galadriel on-ramp P-1)
- `BACKLOG-47-4-7-example-skill-designation.md` (#85) — designate a canonical "4.7 exemplar" skill (Galadriel on-ramp P-4)

## The journey in four waves

For those who like to trace the path on a map, as I always have, here are the four waves in the order the Fellowship walked them. Each wave is a single git commit on `feature/opus-4-7-migration-run-2026-04-22-4x7e`, so the history reads cleanly.

**Wave 1 — Foundational (commit `62b571c`, WI-01/02/03).** No code edits. Three setup items: the AS-IS dispatch-count capture (13 dispatches across 5 completed stages, recorded to the last arrow), the 4.7 observability baseline in JSON plus a companion narrative, and the frontmatter-contract spike that produced ADR-006 Option A (unknown-fields-accepted verdict). Wave 1's exit gate required a baseline file, an AS-IS table, and a spike verdict. All three landed. R-09 — the feared "silent F-08 fusion" where dispatches collapse below the validator list — did not trigger; the dispatch contract held.

**Wave 2 — Keystones, behavioural (commit `437bb79`, WI-04/05/06).** Three independent edits runnable in parallel after Wave 1. WI-04 annotated the `delivery-flow/SKILL.md` dispatch contract (DISP-01 and DISP-02 blockquotes). WI-05 expanded the pattern library in `prompt-engineer/SKILL.md` with the six Pattern 4.N sub-sections plus PAT-01 reframe — the cornerstone that every subsequent citation leans on. WI-06 ran the research-agent tool-use probe and passed the hardened AC-03B.2 gate (tool_calls ≥ 2 AND distinct_hostnames ≥ 2) on the first swing, 4 calls across 5 hosts. WI-05 was the internal critical path because Wave 3 keystone audits cite Patterns 4.2 and 4.4 by name; without Wave 2 landed, Wave 3 could not begin.

**Wave 3 — Keystones, prose (commit `8488ee1`, WI-07/08/09).** Three prose audits runnable in parallel after WI-05. WI-07 audited `product-delivery/SKILL.md` (685 LOC) against F-25 literal-execution hazards. WI-08 audited `architect/SKILL.md` (667 LOC) against F-25 under-specification and F-26 scaffolding-that-duplicates-4.7-defaults; the audit note at `.delivery/artifacts/08-execute/06-dev/audits/architect-f25-f26-audit.md` is 29 KB of careful reading because the architect skill's sub-roles are table rows rather than sub-skills, so each row of the routing table had to be dissected individually. WI-09 carried the REQ-04 adversarial dogfood against `mtg-commander/SKILL.md`. All three audits landed as `CONCRETE_RECOMMENDATION` / `DONE_WITH_REASON` dispositions per instruction; no blocking prose rewrites were required.

**Wave 4 — Drift hygiene, enhancements & CI wiring (commit `d7eb6f7`, WI-10/11/12/13/14).** Five items. WI-10 was the model-ID sweep gated on the AC-01.5 structural check (result: annotate-only for `stage_definitions.py`, substitute for `agent_registry.py`). WI-11 was the mechanical frontmatter backfill on the 11 non-keystones. WI-12 was the alias-theme voice dogfood (3/3 themes at 100%). WI-13 registered the nine NEW-BACKLOG items and dual-wrote them to GitHub (local=9, issues=9). WI-14 wired the two new CI guards, sequenced after WI-10 and WI-11 so both workflows would land green on merge. All five exit conditions cleared.

## Impact by plugin

| Plugin | Files touched | Change type |
|---|---|---|
| `delivery-team` | `delivery-flow/SKILL.md` (+17 lines, DISP-01/02 annotations), plus `developer/SKILL.md`, `godot/SKILL.md`, `operations/SKILL.md`, `quality/SKILL.md`, `ui/SKILL.md`, `user-feedback/SKILL.md`, `alias-creator/SKILL.md`, `presentation/SKILL.md`, `product-delivery/SKILL.md` (keystone), `architect/SKILL.md` (keystone), and the two paradigm sub-skills (`architect/paradigms/ddd/SKILL.md`, `architect/paradigms/volatility/SKILL.md`) | 2 keystone + 10 frontmatter-only + 1 prose annotation |
| `prompt-engineer` | `SKILL.md` (440 → 520 LOC, six new patterns + PAT-01 reframe + frontmatter) | Keystone + pattern library expansion |
| `research-agent` | `SKILL.md` frontmatter only; `references/prompt-library.md:10` retargeted to cite Pattern 4.3 | Keystone + G-5 carry-over |
| `mtg-commander` | `SKILL.md` frontmatter + one-line rephrase at line 825 | Keystone + semantic-equivalent edit |
| `agentic-flow-builder` | `scripts/agent_registry.py` (three substitutions + three provenance comments); `skills/flow-builder/SKILL.md` (frontmatter-only) | Model-ID sweep + frontmatter |
| `prd-quality-gate-flow` | `stage_definitions.py` (one block comment covering seven entries) | Comment-annotate only |
| Repository-level (CI) | `.github/workflows/skill-md-header-warn.yml` (new), `.github/workflows/stale-model-id-guard.yml` (new) | New regression guards |

## What stayed (explicitly unchanged)
Per transformation-plan §6.3 and §10, the following are explicitly out of scope for this migration and were not touched:
- **Plugin architecture.** Three-level context loading, hook event model, `config.yml` schema v2.7, `marketplace.json` structure — all preserved verbatim. Constraint 2 holds.
- **The 7-stage delivery pipeline shape** (Idea → Refine → Design → Architect → Plan → Development → UAT) and the **6 collaboration patterns** (evaluator-optimizer, adversarial review, review board, decision ownership, debate, consensus).
- **The Business Rules Engine.** Deterministic gate evaluation in `prd-quality-gate-flow/business_rules_engine.py` and `agentic-flow-builder/scripts/business_rules_engine.py` — unchanged. Audit-by-rule is still a first-class property of the flow.
- **Alias theme role-per-alias mappings.** The 13 theme YAML files keep their role→character bindings exactly. Tone may be strengthened in future iterations; mapping stays.
- **Python dependency versions** unrelated to the Claude model reference.
- **`task_budget` (F-18), client-side `memory` tool (F-19), prompt-caching adoption.** Deferred per ADR-004; tracked as backlog items #77, #78, and the SDK-wiring path at #79.
- **`.delivery/` historical content sweep.** PRD Constraint 4 excludes.
- **`plugin-dev:*` skills and the `prd_flows.db` SQLite data.** PRD §3.6 and §3.9 respectively.

## Breaking changes
None. Migration is additive (frontmatter fields on all 17 SKILL.md files) and mechanical (model-ID sweep in one registry). All plugins continue to function on Opus 4.7. No hook contracts changed. No config schema fields changed. No skill routing keys changed.

## Observability
- **4.7 baseline captured:** `.delivery/artifacts/08-execute/06-dev/observability/4-7-baseline.json` — authoritative JSON for downstream `jq` pipelines; `skill_loaded_first_attempt_rate = 1.0 (13/13)`, `audit_hook_warning_count = 0`, three alias theme rendering samples.
- **Companion narrative:** `.delivery/artifacts/08-execute/06-dev/observability/4-7-baseline.md` — field-by-field derivation for human auditors.
- **Dispatch-count audit (AS-IS):** `.delivery/artifacts/08-execute/06-dev/observability/4-7-as-is-dispatch-counts.md` — per-stage primary + validator dispatch tallies. Wave 1 arithmetic note: total was 13 dispatches (not 11 as initially cited); Legolas recorded the correct number.
- **Research-probe result:** `.delivery/artifacts/08-execute/06-dev/observability/research-probe-result.json` (`{ tool_calls: 4, distinct_hostnames: 5, pass: true }`) + full transcript alongside.
- **R-09 (silent F-08 fusion):** NOT TRIGGERED. Wave 1 dispatch counts matched the documented dispatch contract; no silent role-fusion was detected on Idea or Refine.

## Rollback
- **Per-wave revert:** four clean wave commits, each revert-safe:
  - Wave 1 — `62b571c chore(delivery): Wave 1 baseline + spike — WI-01/02/03`
  - Wave 2 — `437bb79 feat(delivery-flow): Wave 2 keystone annotations — WI-04/05/06`
  - Wave 3 — `8488ee1 docs(delivery): Wave 3 keystone audits + adversarial dogfood`
  - Wave 4 — `d7eb6f7 feat(migration): Wave 4 sweeps + CI + backlog — WI-10/11/12/13/14`
- **Per-WI rollback** is semantically achievable via ADR-002 (model-ID substitutions are direct strings with visible provenance comments) and ADR-005 (pattern library lives in one file, so a targeted revert of `prompt-engineer/SKILL.md` rewinds the full Pattern 4.N cohort). If future need demands commit-splitting, the wave commits can be cherry-picked down to WI granularity without touching unrelated files.

## Upgrade notes for plugin authors
- **New frontmatter convention: three fields.** Every SKILL.md now carries `model_awareness`, `last_audited`, `pattern_library_version` alongside the existing `name` / `description` / `license` keys. See `prompt-engineer/SKILL.md#pattern-4-6`. The `model_awareness` value is one of:
  - `opus-4-7` — keystone reviewed against 4.7 prose semantics (6 files today).
  - `opus-4-7-frontmatter-only` — mechanical backfill; prose not yet re-read under 4.7 literal-execution lens (11 files today; backlog #81 tracks the upgrade path).
- **Pattern library cite-by-name.** Sibling SKILL.md files should cite patterns by anchor — `prompt-engineer/SKILL.md#pattern-4-1` through `#pattern-4-6` — rather than restate them inline. ADR-005's single-file pattern library strategy keeps a pattern's definition in exactly one place, which is a precondition for both clean rollback and for the DX-M3 end-state grep returning zero external restatements.
- **Stale model IDs now fail CI.** Any `.py` or `.md` file outside `.delivery/` that references a retired dated ID (Opus `4-20250514`, Sonnet `4-5-20250929`, Haiku `4-20250514`, or Opus `4-5`/`4-6` flavours) will fail `stale-model-id-guard.yml` on PR. Historical references belong in `#` comments or `>` blockquotes; those paths are allowlisted. Canonical IDs as of 2026-04-22: `claude-opus-4-7`, `claude-sonnet-4-6`, `claude-haiku-4-5-20251001`.
- **New SKILL.md files should include the three frontmatter fields.** Absence triggers a `::warning::` on PR (via `skill-md-header-warn.yml`); the warning is advisory, not blocking, but the signal makes review cadence visible in the PR checks UI.

## Verification

The six end-state commands from §7 of the execution-PRD all return expected values on HEAD. In summary form (full record and raw output at `.delivery/artifacts/08-execute/07-uat/qa/uat-verification.md`):

- **M-01 stale-ID sweep (calibrated):** zero active stale IDs outside provenance comments. The raw regex returns three hits; all three are the WI-10 provenance comments and are exempted by the `#`-leading filter the CI guard uses.
- **M-02 regression sentinel:** zero. No canonical-breaking introductions.
- **M-03 dispatch-contract dogfood (WI-04):** DISP-01/02 annotations present; `grep -qE 'F-?08'` returns 0 exit code on `delivery-flow/SKILL.md`.
- **M-04 pattern-library contract:** `grep -cE '^### Pattern 4\.[1-6] — ' prompt-engineer/SKILL.md` returns exactly 6.
- **M-05 alias-theme voice preservation:** 3/3 sampled themes at 100%; target was ≥80% of samples at ≥50% markers.
- **DX-M4 header coverage:** 17/17 SKILL.md files carry `model_awareness:` (6 `opus-4-7` + 11 `opus-4-7-frontmatter-only`); the header-warn workflow runs clean.

No automated test suite exists for the Python modules touched; verification for those was by AST parse (`python -c "import ast; ast.parse(...)"` returned OK on both `agent_registry.py` and `stage_definitions.py`) plus structural inspection of `flow_orchestrator.py` confirming zero SDK coupling. The `check_db.py` probe returned non-zero because no SQLite DB exists in the pre-flight working tree; kickoff marked this non-blocking.

## Acknowledgements
The Fellowship walked this one together. Gandalf (PO) mapped the road and resisted the temptation to widen it. Celebrimbor (architect) forged the plan and inscribed each ring with provenance. Aragorn (sprint-plan), Gimli (developer), Legolas (QA), and Samwise (DevOps) each carried their pack of the load — Gimli on the keystones and the sweep, Legolas on baseline and gates, Samwise on the CI guards. Galadriel (privacy/prior-art) left her on-ramp gifts in the backlog for whoever walks this road next. The Hobbits of the Shire (user-feedback) sat by the fire and listened to Bilbo's stories with the level-headedness this kind of work needs. And the Challenger, whose name I'll not repeat lest he become flattered, kept the prose honest.

Precious, this was not. Ordinary, and honest, and done — that's the better measure.

— Bilbo
