# BACKLOG-101: Skill Token-Economy Wave 1 — delivery-team plugin

**Status**: Open
**Priority**: P1 (immediate sequel to BACKLOG-100; Wave 0 foundations now in place)
**Size**: M (7 items, all Effort S, single sprint achievable)
**Created**: 2026-05-04
**Owner**: PO → delivery-flow pipeline (full team)
**Predecessor**: BACKLOG-100 (Wave 0 — telemetry hook + CI gate; GO at run-2026-05-03-tk0e)

## Source

- **Audit**: `.delivery/artifacts/research/skill-token-audit-experts.md` (6-expert audit)
- **Binding decisions**: `.delivery/memory/topics/skill-token-economy.md` (5 conflict rulings + per-skill model map + tiered line budgets)
- **Wave 0 retro**: `.delivery/artifacts/post-pipeline/retro/retrospective.md` (run-2026-05-03-tk0e action items)

## Goal

Execute the Wave 1 quick-wins from the audit backlog. With telemetry (W0-1) and budget gate (W0-2) now in place, every Wave 1 item produces measurable token savings (validated by telemetry deltas) without regression risk (gated by CI).

## In-scope work items (7)

### W1-1. Cache-prefix freeze for `delivery-flow/SKILL.md`
- **MUST**: First ~2k tokens of `delivery-team/skills/delivery-flow/SKILL.md` SHALL be byte-stable across runs; volatile content (dates, run-IDs, dynamic config echoes) SHALL appear after a `## Volatile` marker near EOF; future prefix changes SHALL require an ADR.
- **Files**: `delivery-team/skills/delivery-flow/SKILL.md`, new ADR
- **AC**: telemetry shows `cache_read/input ratio` ≥0.85 on second run; CI hash check fails when prefix mutates without ADR bump
- **Effort**: S | **Risk**: Med (load-bearing prefix)

### W1-2. Stage definitions to YAML manifest
- **MUST**: 7 stage definitions in `delivery-flow/SKILL.md` lines ~612–743 SHALL move to `delivery-team/skills/delivery-flow/references/stages.yml`; SKILL.md SHALL load on demand only.
- **Files**: `delivery-team/skills/delivery-flow/SKILL.md`, new `references/stages.yml` + JSON schema
- **AC**: stages.yml validates against schema; pipeline routes all 7 stages correctly in dogfood; telemetry confirms ≥2,000 token drop on cold load; delivery-flow SKILL.md drops below Tier-A 500 (or known-debt entry updated)
- **Effort**: S | **Risk**: Low

### W1-3. Haiku for routing/dispatch sub-agents
- **MUST**: Sub-agents whose sole job is classification, dispatch, or paradigm routing SHALL declare `model: haiku` in their agent frontmatter.
- **Files**: Phase 1 detector agents in product-delivery, architect, quality, operations, ui SKILL.md; `delivery-team/hooks/agent_audit.py` extension to warn on tier mismatch
- **AC**: All routing agents declare `model: haiku`; hook warns if a routing agent runs under non-Haiku model; dogfood: 10/10 routing decisions correct on Haiku
- **Effort**: S | **Risk**: Low

### W1-4. Selective allowed-tools + top-level description prune
- **MUST**: Tier-A and MCP-loading skills SHALL declare `allowed-tools: [Read, Edit, Write, Bash, Skill, ToolSearch]` (extend with justification only); every skill description >500 chars in marketplace.json SHALL be pruned to ≤500.
- **Files**: All `delivery-team/**/SKILL.md` frontmatter; `.claude-plugin/marketplace.json`
- **AC**: Every Tier-A delivery-team skill has `allowed-tools` set; no description exceeds 500 chars; session-start payload measured ≥10 KB smaller (telemetry diff)
- **Effort**: S | **Risk**: Low

### W1-5. Adversarial challenger model-tier inheritance + extended thinking OFF
- **MUST**: Adversarial challenger sub-agents SHALL inherit the primary's `model:` value at dispatch; extended thinking SHALL default OFF unless orchestrator opts in per-stage.
- **Files**: `delivery-team/skills/delivery-flow/SKILL.md` (adversarial-review section); `delivery-team/hooks/agent_audit.py` extension
- **AC**: Hook enforces challenger.model == primary.model (default warn-only sprint 1; escalate to hard-block sprint 2 if violated); extended-thinking flag defaults OFF in all delivery-team agent frontmatter; dogfood adversarial round still surfaces ≥1 substantive critique
- **Effort**: S | **Risk**: High (silent quality loss if violated; anti-pattern session 0876a59e)

### W1-6. Sonnet default for orchestrator + pure-Python hooks audit
- **MUST**: `delivery-flow` SHALL declare `model: sonnet` as default (Opus opt-in per-stage); every `delivery-team/hooks/*.py` SHALL be audited for and confirmed to contain NO LLM calls.
- **Files**: `delivery-team/skills/delivery-flow/SKILL.md` frontmatter; all 7 `delivery-team/hooks/*.py`
- **AC**: No delivery-team hook contains a model invocation (`grep -E "anthropic|openai|litellm"` in hooks/ returns empty); dogfood pipeline runs end-to-end on Sonnet default; cost telemetry shows ≥3× reduction per run vs Opus baseline
- **Effort**: S | **Risk**: Low (Sonnet validated for orchestration in prior runs)
- **Open team decision**: 5-run shadow A/B before flip OR immediate flip with telemetry watch (default: shadow A/B per mission-critical risk tolerance)

### W1-7. alias-creator -1 line known-debt fix (carry-in from Wave 0 retro)
- **MUST**: `delivery-team/skills/alias-creator/SKILL.md` SHALL be reduced by exactly 1 line to restore Tier-C compliance (≤200 lines).
- **Files**: `delivery-team/skills/alias-creator/SKILL.md`
- **AC**: `wc -l delivery-team/skills/alias-creator/SKILL.md` returns ≤200; CI gate passes without `Budget-Exception:` for this file; `governance/skill-budgets.json` known-debt entry for alias-creator removed
- **Effort**: S | **Risk**: Low

## Out of scope (next BACKLOG entries)

- Wave 2+ structural extractions (BACKLOG-102+)
- mtg-commander 4 agent prompts extraction (next plugin's BACKLOG)
- All other plugins
- CLAUDE.md refactor (Wave 3 — `tk0e-claude-md-refactor` known-debt)

## Sequencing

```
W1-1 ──┬──> (no inter-WI dependencies — all 7 mechanically independent)
W1-2 ──┤
W1-3 ──┤
W1-4 ──┤    All 7 dispatchable in parallel within Stage 6 Dev
W1-5 ──┤
W1-6 ──┤
W1-7 ──┘
```

## Acceptance Criteria (initiative-level)

1. Every WI lands with telemetry showing actual token/cost savings (W0-1 measures it; capture before/after)
2. CI gate passes after each WI (W0-2 enforces; no regressions)
3. delivery-flow SKILL.md drops below Tier-A 500 budget (was 1089) — measured by `wc -l`
4. alias-creator restored to Tier-C compliance (≤200)
5. No degradation in delivery-flow first-try DoD pass rate (currently ≥80% across stages per memory/index.md)
6. Defects/story rate ≤0.4 (stop-rule from BACKLOG-100)

## Pipeline-run preferences

- **Project type**: FEATURE-execution-of-pre-planned-waves (binding-decisions-in-memory pattern)
- **Routing**: 1 light · 2 light · 3 SKIP · 4 light · 5 light · 6 full · 7 full (same pattern as Wave 0; brief is the audit)
- **Theme**: lotr (continued — works well per Wave 0 retro)
- **Models**: Sonnet for primaries, Haiku for DoD validators (per binding)
- **Validators**: per-stage minimum + Tech Writer cross-doc consistency check now standard at UAT (Wave 0 retro action item)
- **Lessons to inject** (from `memory/`):
  - Hot lesson #1: Developer DoD runs the command (3 validations now)
  - Stage-1 idea: plugin-dev skill routing in PO upfront context (NEW)
  - Stage-2 refine: PRDs from upstream prose MUST run discovery commands (NEW)
  - Stage-7 UAT: cross-doc consistency check (NEW)
  - Mandatory-rollout side-effect: simulate line delta before mass edits (NEW)

## Carry-forward action items from Wave 0 retro

| # | Action | Status |
|---|--------|--------|
| 2 | Wire pre-merge git hook for skill-budget local check | Pending — incorporate into W1-7 dogfood |
| 3 | Add cross-doc consistency check to default UAT TW gate criteria template | Pending — apply at Wave 1 UAT |
| 4 | File issue: plugin-dev:skill-development to recommend invocation pattern | Pending — separate one-off task |

## Stop-rule (carryover from BACKLOG-100)

If defects/story rate exceeds 0.4 across any 3-PR window, pause Wave 2 (BACKLOG-102+) until root-cause retro completes.

## Pre-flight gate

Wave 0 (BACKLOG-100) MUST be merged before Wave 1 pipeline starts. Rationale: per memory `topics/project-types.md` "per-wave commit cadence is defensible for mechanically-independent WI batches" — keeping Wave 0 and Wave 1 as separable PRs preserves audit-trail readability and independent revert capability. Wave 1 modifies many of the same SKILL.md files Wave 0 added `tier:` frontmatter to; compounding the diffs would obscure both reviews.
