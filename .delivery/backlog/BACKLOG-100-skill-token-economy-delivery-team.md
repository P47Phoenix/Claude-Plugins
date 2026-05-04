# BACKLOG-100: Skill Token-Economy Initiative — delivery-team plugin

**Status**: Open
**Priority**: P1 (initiative — multiple work items in waves)
**Size**: L (4 waves, ~17 items, scoped to delivery-team plugin)
**Created**: 2026-05-03
**Owner**: PO → delivery-flow pipeline (full team)

## Source

- **Audit**: `.delivery/artifacts/research/skill-token-audit-experts.md` (6 expert interviews + debate moderator + PO synthesis)
- **Binding decisions**: `.delivery/memory/topics/skill-token-economy.md` (5 conflict rulings + per-skill model map)

## Goal

Reduce token/context usage in delivery-team plugin skills WITHOUT degrading quality. delivery-team is the largest plugin (11 skills) and the highest-impact target. Other plugins (mtg-commander, hardware-team, agentic-flow-builder, prd-quality-gate-flow, research-agent, prompt-engineer) follow in subsequent BACKLOG entries — one plugin at a time per user directive.

## In-scope skills (delivery-team only)

`delivery-flow`, `product-delivery`, `developer`, `godot`, `architect`, `quality`, `operations`, `ui`, `user-feedback`, `alias-creator`, `presentation`

## Out-of-scope (this backlog)

- mtg-commander/SKILL.md prompt extraction → next BACKLOG (W1-7 in audit)
- hardware-team Phase boundary split → next BACKLOG
- All other plugins → subsequent BACKLOGs

## Wave 0 — Foundations (must land first)

### W0-1. Skill-load telemetry hook
- **MUST**: PreToolUse hook on `Skill` matcher SHALL emit `{skill, model, prefix_hash, input_tokens, cache_read_tokens, cache_write_tokens}` to `.delivery/telemetry/skill-loads.jsonl` for every skill invocation.
- **Files**: `delivery-team/hooks/hooks.json`, `delivery-team/hooks/telemetry.py` (new), `delivery-team/references/telemetry-schema.md` (new)
- **AC**:
  - [ ] Hook fires on every Skill PreToolUse and writes one JSONL row
  - [ ] Schema documented and versioned (v1)
  - [ ] Sample 5-run report script renders mean tokens/run per skill
  - [ ] Hook adds <50 ms overhead per call
- **Effort**: S | **Risk**: Low

### W0-2. Tiered SKILL.md line-budget CI gate
- **MUST**: A GitHub Actions workflow SHALL fail any PR where Tier-A SKILL.md > 500 lines, Tier-B > 300, or Tier-C > 200; tiering SHALL be declared in the SKILL.md frontmatter `tier:` field.
- **Files**: `.github/workflows/skill-line-budget.yml` (new), `scripts/check_skill_budgets.py` (new), all `delivery-team/**/SKILL.md` (add `tier:` frontmatter)
- **AC**:
  - [ ] Every delivery-team SKILL.md has `tier:` frontmatter
  - [ ] CI fails on a synthetic over-budget PR (proven in test PR)
  - [ ] Current over-budget skills (delivery-flow 1089, product-delivery 688, architect 670, presentation 543, ui 493, developer 493) logged as known-debt with target wave
  - [ ] Permissive-language warn-only sub-check included (regex `\bshould\b|\bcan\b|\bmay\b|\bmight\b` outside fenced blocks)
- **Effort**: S | **Risk**: Low | **Blocks**: every Wave 1+ extraction

## Wave 1 — Quick Wins (sprint 1, all Effort S)

### W1-1. Cache-prefix freeze + relocate volatile content
- **MUST**: First ~2k tokens of `delivery-team/skills/delivery-flow/SKILL.md` SHALL be byte-stable across runs; dates/run-IDs/dynamic config SHALL appear after a `## Volatile` marker near EOF; future prefix changes SHALL require an ADR.
- **Files**: `delivery-team/skills/delivery-flow/SKILL.md`, `docs/adr/ADR-NNNN-cache-prefix-freeze.md` (new)
- **AC**:
  - [ ] Telemetry (W0-1) shows cache_read/input ratio ≥0.85 on second run
  - [ ] ADR merged
  - [ ] CI hash check fails when prefix mutates without ADR bump
- **Effort**: S | **Risk**: Med (load-bearing prefix) | **Blocked by**: W0-1, W0-2

### W1-2. Stage definitions to YAML manifest
- **MUST**: 7 stage definitions in `delivery-flow/SKILL.md` lines ~612–743 SHALL move to `delivery-team/skills/delivery-flow/references/stages.yml`; SKILL.md SHALL load on demand only.
- **Files**: `delivery-team/skills/delivery-flow/SKILL.md`, `delivery-team/skills/delivery-flow/references/stages.yml` (new), `references/stages.schema.json` (new)
- **AC**:
  - [ ] stages.yml validates against JSON schema
  - [ ] Pipeline routes all 7 stages correctly in dogfood run
  - [ ] Telemetry confirms ≥2,000 token drop on cold load
- **Effort**: S | **Risk**: Low | **Blocked by**: W0-2

### W1-3. Haiku for routing/dispatch sub-agents
- **MUST**: Sub-agents whose sole job is classification, dispatch, or paradigm routing SHALL declare `model: haiku`; orchestrators SHALL NOT invoke them under Sonnet/Opus.
- **Files**: Phase 1 detector agents in `product-delivery/SKILL.md`, `architect/SKILL.md`, `quality/SKILL.md`, `operations/SKILL.md`, `ui/SKILL.md`; `delivery-team/hooks/agent_audit.py` (extend to warn on tier mismatch)
- **AC**:
  - [ ] All routing agents have `model: haiku` declared
  - [ ] Hook warns if a routing agent runs under non-Haiku model
  - [ ] Dogfood: correct routing on 10/10 sample inputs across 5 multiplexer skills
- **Effort**: S | **Risk**: Low | **Blocked by**: W0-1

### W1-4. Selective `allowed-tools` + description prune
- **MUST**: Tier-A and MCP-loading skills SHALL declare `allowed-tools: [Read, Edit, Write, Bash, Skill, ToolSearch]` (extend with justification only); every skill description >500 chars SHALL be pruned to ≤500.
- **Files**: All `delivery-team/**/SKILL.md` frontmatter, `.claude-plugin/marketplace.json` (delivery-team description)
- **AC**:
  - [ ] Every Tier-A delivery-team skill has `allowed-tools` set
  - [ ] No description in marketplace.json for delivery-team exceeds 500 chars
  - [ ] Session-start payload measured ≥10 KB smaller post-change (telemetry from W0-1)
- **Effort**: S | **Risk**: Low | **Blocked by**: W0-1

### W1-5. Adversarial challenger model-tier inheritance + extended thinking off
- **MUST**: Adversarial challenger sub-agents SHALL inherit primary's `model:` value at dispatch; extended thinking SHALL default OFF unless orchestrator opts in per-stage.
- **Files**: `delivery-team/skills/delivery-flow/SKILL.md` (adversarial-review section), `delivery-team/hooks/agent_audit.py` (extend to enforce)
- **AC**:
  - [ ] Hook enforces challenger.model == primary.model (decision: hard-block vs warn-only — open question, default warn-only sprint 1)
  - [ ] Extended-thinking flag defaults OFF in all delivery-team agent frontmatter
  - [ ] Dogfood adversarial round still surfaces ≥1 substantive critique
- **Effort**: S | **Risk**: High (silent quality loss if violated; anti-pattern session 0876a59e) | **Blocked by**: W0-1

### W1-6. Sonnet default for orchestrator + pure-Python hooks
- **MUST**: `delivery-flow` SHALL declare `model: sonnet` as default (Opus opt-in per-stage); every `delivery-team/hooks/*.py` SHALL run as standalone Python with no LLM call inside.
- **Files**: `delivery-team/skills/delivery-flow/SKILL.md` frontmatter, all 7 `delivery-team/hooks/*.py`
- **AC**:
  - [ ] No delivery-team hook contains a model invocation
  - [ ] Dogfood pipeline runs end-to-end on Sonnet default
  - [ ] Cost telemetry shows ≥3× reduction per run (open question: 5-run shadow A/B before flip vs immediate — default A/B)
- **Effort**: S | **Risk**: Low | **Blocked by**: W0-1

## Wave 2 — Structural Extractions (sprints 2–3, Effort M)

### W2-1. Externalize shared orchestrator doctrine
- **MUST**: Prime Directive, One Role = One Sub-Agent, Two-Channel Communication, debate/consensus/adversarial-review patterns SHALL live in `delivery-team/references/shared/orchestrator-doctrine.md`; `delivery-flow/SKILL.md` SHALL reference by path.
- **Files**: `delivery-team/references/shared/orchestrator-doctrine.md` (new), `delivery-team/skills/delivery-flow/SKILL.md`
- **AC**:
  - [ ] Doctrine file created
  - [ ] delivery-flow references it
  - [ ] ADR amendment confirms post-extraction prefix re-frozen (per W1-1 rule)
  - [ ] Dogfood debate + adversarial run unchanged in behavior
- **Effort**: M | **Risk**: Med (load-bearing under Opus 4.7 — F-08 dispatch fusion regression; reference doctrine MUST stay strong) | **Blocked by**: W1-1

### W2-2. Architect output contracts to references
- **MUST**: `architect/SKILL.md` lines ~385–537 (5 output templates: Design, ADR, Game Architecture, Review, Technology Evaluation) SHALL move to `delivery-team/skills/architect/references/output-contracts/{design,adr,game,review,evaluation}.md`; SKILL.md SHALL keep a routing table only.
- **Files**: `delivery-team/skills/architect/SKILL.md`, `delivery-team/skills/architect/references/output-contracts/*.md` (new x5)
- **AC**:
  - [ ] All 5 output contracts extracted
  - [ ] Architect Tier-B budget (≤300) satisfied
  - [ ] Dogfood architect run produces equivalent ADR/design artifacts
- **Effort**: M | **Risk**: Low | **Blocked by**: W0-2

### W2-3. Developer coding-standards template extraction
- **MUST**: `developer/SKILL.md` lines ~162–318 (`coding-standards` task implementation, ~155 lines) SHALL move to `delivery-team/skills/developer/references/agent-prompts/coding-standards.md` + `references/coding-standards-template.md`.
- **Files**: `delivery-team/skills/developer/SKILL.md`, `delivery-team/skills/developer/references/agent-prompts/coding-standards.md` (new), `delivery-team/skills/developer/references/coding-standards-template.md` (new)
- **AC**:
  - [ ] Template + sub-agent prompt extracted
  - [ ] 14-language matrix unaffected in dogfood
  - [ ] Tier-B budget satisfied (developer ≤300)
- **Effort**: M | **Risk**: Low | **Blocked by**: W0-2

### W2-4. Config / commands / manifest tables to references
- **MUST**: Verbose tables in `delivery-flow/SKILL.md` (Config Settings ~lines 168–210, User Commands ~lines 1037–1062, References ~lines 1067–1089) SHALL move to `delivery-team/skills/delivery-flow/references/{config-keys.md, commands.md, manifest.yml}`; SKILL.md SHALL keep one-line pointers.
- **Files**: `delivery-team/skills/delivery-flow/SKILL.md`, `delivery-team/skills/delivery-flow/references/{config-keys.md,commands.md,manifest.yml}` (new)
- **AC**:
  - [ ] All three tables extracted
  - [ ] Setup wizard still finds config keys
  - [ ] Telemetry confirms ≥2,500 token savings
- **Effort**: M | **Risk**: Low | **Blocked by**: W0-2

### W2-5. product-delivery 12 patterns split
- **MUST**: Each of the 12 `### Pattern N:` blocks in `product-delivery/SKILL.md` (lines ~140–511) SHALL live in `delivery-team/skills/product-delivery/references/patterns/<pattern-slug>.md`; routing table SHALL load only the matched pattern.
- **Files**: `delivery-team/skills/product-delivery/SKILL.md`, `delivery-team/skills/product-delivery/references/patterns/*.md` (new x12)
- **AC**:
  - [ ] 12 pattern files exist with stable filenames
  - [ ] Router selects correct pattern in 12/12 dogfood cases
  - [ ] Tier-B budget satisfied
- **Effort**: M | **Risk**: Low | **Blocked by**: W0-2

### W2-6. Architect model split (Opus synthesis only)
- **MUST**: Architect classification phases (Prior Art Analysis, paradigm pick, decomposition strategy pick, Compliance/Privacy/IR checklist roles) SHALL run on Sonnet; only design synthesis (ADR drafting, transformation TO-BE) SHALL escalate to Opus.
- **Files**: `delivery-team/skills/architect/SKILL.md`, sub-skill manifests under `architect/skills/paradigms/`
- **AC**:
  - [ ] Phase-to-model map documented in architect/SKILL.md
  - [ ] Regression set: 10 known inputs classified identically pre/post on Sonnet
  - [ ] Cost telemetry confirms reduction
- **Effort**: M | **Risk**: Med (wrong classification cascades) | **Blocked by**: W1-6

## Wave 3 — Slow-burn (this quarter)

### W3-1. Phase-1/2 routing pattern for >2-role multiplexers
- **MUST**: `architect`, `operations`, `ui` SHALL adopt `product-delivery`'s Phase 1 detect / Phase 2 spawn-with-only-relevant-references pattern.
- **Files**: `delivery-team/skills/architect/SKILL.md`, `delivery-team/skills/operations/SKILL.md`, `delivery-team/skills/ui/SKILL.md`
- **AC**:
  - [ ] Router pattern documented and applied
  - [ ] 10/10 dogfood routes correct per skill
  - [ ] Tier-B budget satisfied (≤300 each)
- **Effort**: M | **Risk**: Med (router misroute is silent failure) | **Blocked by**: W2-2

### W3-2. Governance frontmatter + retro KPI + quarterly fitness review
- **MUST**: Every delivery-team SKILL.md SHALL declare `tier`, `maintainer`, `last_fitness_review`, `context_budget` frontmatter. Retro template SHALL include `context_tokens_per_pipeline_run` 5-run rolling-mean KPI; >15% growth opens defect. Quarterly: highest (lines × invocations) skill gets refactor sprint targeting ≥30% reduction.
- **Files**: All `delivery-team/**/SKILL.md`, `delivery-team/skills/delivery-flow/references/retro-template.md`
- **AC**:
  - [ ] Frontmatter present on every delivery-team SKILL.md
  - [ ] Retro template updated; one retro run uses it
  - [ ] Quarterly review calendared
- **Effort**: M | **Risk**: Low | **Blocked by**: W0-1 (telemetry source)

### W3-3. Paradigm sub-skill pattern for ≥3 mutually-exclusive variants
- **MUST**: `user-feedback` (≥20 personas in 4 categories), `presentation` (9 types) SHALL adopt the `architect/skills/paradigms/` sub-skill pattern with `disable-model-invocation: true` on sub-skills.
- **Files**: `delivery-team/skills/user-feedback/skills/personas/*` (new structure), `delivery-team/skills/presentation/skills/types/*` (new structure)
- **AC**:
  - [ ] Sub-skill structure created for at least one of the two
  - [ ] Router selects correctly across 5 dogfood runs
  - [ ] No regression in existing persona/type behavior
- **Effort**: L | **Risk**: Med (`disable-model-invocation` misuse breaks discoverability) | **Blocked by**: W3-1

## Acceptance Criteria (initiative-level)

1. Every Wave 0+1 item lands with telemetry showing actual token savings (W0-1 measures it)
2. Wave 2+3 items land with no regression in delivery-flow dogfood runs (5-run baseline)
3. delivery-flow Tier-A budget (500 lines) achieved
4. Defect rate on this initiative ≤0.4 across any 3-PR window (per stop-rule in `topics/skill-token-economy.md`)
5. Final state: every delivery-team SKILL.md within tier budget, telemetry running, governance frontmatter present, retro KPI publishing

## Open questions (per-wave team decisions)

These are NOT blockers — the team decides per-wave during execution:

1. **Sonnet orchestrator flip (W1-6)**: 5-run shadow A/B before default flip, OR immediate flip with telemetry watch? Team default: shadow A/B (mission-critical risk tolerance per config.yml).
2. **Challenger-tier hook enforcement (W1-5)**: hard-block dispatch on tier mismatch, OR warn-only sprint 1? Team default: warn-only sprint 1, escalate to hard-block sprint 2 if violated.

## Sequencing summary

```
W0-1 ────┬──> W1-1 ──> W2-1 ────────────┐
W0-2 ────┴──> W1-2,3,4,5,6 ──> W2-2..6 ─┴──> W3-1 ──> W3-3
                                              │
                                              └─> W3-2
```

Wave 0 must land first (foundations). Wave 1 items 2–6 can run in parallel after W0-2. W2-1 must wait for W1-1 (cache prefix). W2-2..6 can run in parallel after W0-2. W3-1 needs W2-2.

## Rationale

The 6-expert audit converged on four themes: (1) externalize inline payload, (2) decompose orchestrators by phase, (3) adopt product-delivery's Phase 1/2 routing pattern repo-wide, (4) move shared orchestrator doctrine to a single reference. Model-tuning expert added per-skill model recommendations (Sonnet default, Haiku for routing, Opus for synthesis-only). Governance expert closed the loop: without telemetry (W0-1) and budgets (W0-2), the gains regress within 6 months.

The 5 conflict rulings (`.delivery/memory/topics/skill-token-economy.md`) resolve real tensions — particularly cache-prefix freeze vs doctrine externalization (sequenced, not conflicting) and `disable-model-invocation` breadth (sub-skills only, not blanket).

delivery-team is the largest plugin and benefits from highest leverage. mtg-commander, hardware-team, and remaining plugins follow in subsequent BACKLOG entries — one plugin at a time per user directive.
