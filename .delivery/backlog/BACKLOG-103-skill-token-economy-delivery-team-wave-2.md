# BACKLOG-103: Skill Token-Economy Wave 2 — delivery-team plugin (structural extractions)

**Status**: Open
**Priority**: P1 (immediate sequel to BACKLOG-101; foundations + frontmatter discipline now in place)
**Size**: L (8 items spanning 4 sprints; biggest extraction is delivery-flow doctrine 999→≤500)
**Created**: 2026-05-05
**Owner**: PO → delivery-flow pipeline (full team)
**Predecessors**:
- BACKLOG-100 (Wave 0 — telemetry + CI gate; merged d0e0928 → main)
- BACKLOG-101 (Wave 1 — cache freeze + frontmatter rollout + challenger hook; merged b412a40 → main)

## Source

- **Audit**: `.delivery/artifacts/research/skill-token-audit-experts.md` Wave 2 cluster (#2, #9, #10, #12, #13, #14)
- **Binding decisions**: `.delivery/memory/topics/skill-token-economy.md` (5 conflict rulings — unchanged)
- **Wave 1 retro**: `.delivery/artifacts/post-pipeline/retro/retrospective.md` (4 carry-forward action items)
- **Current known-debt baseline** (`governance/skill-budgets.json` — note registry stale; W2-0 re-baselines):
  - delivery-flow: **999/500** (over by 499 — registry says 1089 but actual is 999 post-Wave-1; -499 is the real Wave 2 target)
  - product-delivery: 688/300 (over by 388)
  - architect: 670/300 (over by 370)
  - presentation: 543/300 (over by 243)
  - developer: 493/300 (over by 193)
  - ui: 493/300 (over by 193)
  - operations: 417/300 (over by 117)
  - quality: 415/300 (over by 115)
  - user-feedback: 397/300 (over by 97)
  - godot: 234/200 (over by 34)

## Goal

Extract bulky inline content from the heaviest delivery-team SKILL.md files into `references/` so each lands within its tier budget. Wave 2 focuses on the highest-leverage extractions; remaining smaller-budget files (presentation, ui, operations, quality, user-feedback, godot) get their dedicated wave (BACKLOG-104+) since their reductions follow distinct patterns (paradigm sub-skills, role multiplexer Phase-1/2 routing, etc.).

## In-scope work items (8)

### W2-0. Re-baseline `governance/skill-budgets.json` known-debt registry (admin)
- **MUST**: Update `known_debt` array in `governance/skill-budgets.json` to reflect actual current line counts (delivery-flow 999 not 1089) and re-target wave assignments (Wave 1 target was misassigned at audit time; reassign to W2 or W3 per actual extraction plan).
- **Files**: `governance/skill-budgets.json`, `scripts/check_skill_budgets.py` (sync hard-coded list if present)
- **AC**: `python3 scripts/check_skill_budgets.py --known-debt-report` shows accurate line counts; target_wave field reflects Wave 2 plan
- **Effort**: S | **Risk**: Low (admin)

### W2-1. Externalize shared orchestrator doctrine (the big delivery-flow reducer)
- **MUST**: Move shared orchestrator doctrine (Prime Directive, Core Principles, One Role = One Sub-Agent, Two-Channel Communication, Theme-Gated Reporting protocol details, Common Anti-Patterns enumeration, Stage-Definitions per-stage detail blocks, Memory and Self-Learning detail) from `delivery-team/skills/delivery-flow/SKILL.md` to `delivery-team/references/shared/orchestrator-doctrine.md`. Keep in SKILL.md: routing skeleton (Phase 0 setup, Phase 1 detect, Phase 2 memory, Phase 3 routing, Phase 4 protocol skeleton — 10 steps), Stage Routing Matrix table, references manifest pointer.
- **Files**: `delivery-team/skills/delivery-flow/SKILL.md`, new `delivery-team/references/shared/orchestrator-doctrine.md`, ADR for cache-prefix re-freeze
- **AC**:
  - [ ] delivery-flow/SKILL.md ≤ 500 lines (Tier-A compliant)
  - [ ] orchestrator-doctrine.md exists with all extracted content
  - [ ] Cache-prefix hash (governance/cache-prefix-hash.txt) UPDATED — this is a deliberate prefix change requiring ADR-tk2-001
  - [ ] Dogfood: run a synthetic delivery-flow invocation; verify Phase 0/1/2/3 still routable from skeleton SKILL.md
  - [ ] CI hash check passes after hash file update
- **Effort**: L | **Risk**: High — load-bearing prefix; F-08 dispatch fusion regression risk if doctrine extraction loses semantic anchors. Mitigation: Architect dogfood-validates the skeleton against a multi-stage pipeline run BEFORE merge.

### W2-2. Extract architect output contracts to references
- **MUST**: Move 5 output contracts (Design Output, ADR Output, Game Architecture Output, Review Output, Technology Evaluation Output) from `delivery-team/skills/architect/SKILL.md` lines ~385–537 to `delivery-team/skills/architect/references/output-contracts/{design,adr,game,review,evaluation}.md`. SKILL.md keeps a routing table mapping task_type → contract file.
- **Files**: `delivery-team/skills/architect/SKILL.md`, new `delivery-team/skills/architect/references/output-contracts/*.md` (×5)
- **AC**:
  - [ ] All 5 contracts extracted; SKILL.md cites them via routing table
  - [ ] architect/SKILL.md → ≤300 lines (Tier-B compliant) OR remaining items added to W2-6/Wave-3 sequence
  - [ ] Dogfood: dispatch architect for one ADR-authoring task; verify it loads only the matched contract
- **Effort**: M | **Risk**: Low (mechanical extraction)

### W2-3. Extract developer coding-standards template
- **MUST**: Move developer/SKILL.md `coding-standards` task implementation (lines ~162–318, ~155 lines) to `delivery-team/skills/developer/references/agent-prompts/coding-standards.md` + `delivery-team/skills/developer/references/coding-standards-template.md`. SKILL.md keeps a one-line dispatch pointer.
- **Files**: `delivery-team/skills/developer/SKILL.md`, 2 new references files
- **AC**:
  - [ ] Coding-standards template extracted; sub-agent prompt extracted
  - [ ] developer/SKILL.md → ≤300 lines (Tier-B compliant)
  - [ ] Dogfood: dispatch developer for a `write` task (non-coding-standards); verify the template is NOT loaded
  - [ ] Dogfood: dispatch developer for `coding-standards` task; verify template IS loaded
- **Effort**: M | **Risk**: Low

### W2-4. Move config/commands/manifest tables to references
- **MUST**: Move from delivery-flow/SKILL.md to `delivery-team/skills/delivery-flow/references/`:
  - 35-row Config Settings Applied table → `references/config-keys.md`
  - 18-row User Commands table → `references/commands.md`
  - 19-row References manifest table → `references/manifest.yml`
- **Files**: `delivery-team/skills/delivery-flow/SKILL.md`, 3 new references files
- **AC**:
  - [ ] All 3 tables extracted; SKILL.md keeps one-line pointers
  - [ ] Setup wizard still finds config keys (verify via `setup` command dry-run)
  - [ ] Cache-prefix hash UPDATED (delivery-flow prefix region affected)
  - [ ] Telemetry confirms ≥2,500 token savings on delivery-flow load
- **Effort**: M | **Risk**: Low (tables are reference data; pointer pattern proven in Wave 1 stages.yml extraction)

### W2-5. product-delivery 12 patterns split
- **MUST**: Each of the 12 `### Pattern N:` blocks in `product-delivery/SKILL.md` (lines ~140–511) MUST live in `delivery-team/skills/product-delivery/references/patterns/<pattern-slug>.md`. The Phase 1 routing table maps task_type → pattern file; Phase 2 sub-agent loads only the matched pattern.
- **Files**: `delivery-team/skills/product-delivery/SKILL.md`, 12 new pattern files
- **AC**:
  - [ ] 12 pattern files exist with stable filenames
  - [ ] Routing table picks correct pattern in 12/12 dogfood task-type cases
  - [ ] product-delivery/SKILL.md → ≤300 lines (Tier-B compliant)
- **Effort**: M | **Risk**: Low

### W2-6. Architect model split (Opus for synthesis only)
- **MUST**: Architect classification phases (Prior Art Analysis, paradigm pick, decomposition strategy pick, Compliance/Privacy/IR checklist roles) MUST run on Sonnet; only design synthesis (ADR drafting, transformation TO-BE) MUST escalate to Opus. Implementation: extend the architect skill router to return `{role, task_type, recommended_model}`; orchestrator dispatches design sub-agent with returned model.
- **Files**: `delivery-team/skills/architect/SKILL.md`, sub-skill manifests under `architect/skills/paradigms/` (volatility, ddd)
- **AC**:
  - [ ] Phase-to-model map documented in architect/SKILL.md
  - [ ] Regression set: 10 known inputs classified identically pre/post on Sonnet
  - [ ] Cost telemetry shows ≥3× reduction on classification turns
- **Effort**: M | **Risk**: Med (wrong classification cascades; mitigated by regression set)

### W2-7. Wave 1 retro carry-forward backports (admin)
- **MUST**: Apply the 2 stale-content corrections identified at Wave 1 retro:
  - BACKLOG-101 W1-7 line target: -1 → -2 (math correction for alias-creator batching)
  - BACKLOG-101 W1-3/W1-5 hook filename: `agent_audit.py` → `audit_agent_prompt.py` (correct existing-file name)
  - ADR-tk1-002 same backports
- **Files**: `.delivery/backlog/BACKLOG-101-skill-token-economy-delivery-team-wave-1.md`, `.delivery/artifacts/04-architect/adrs/ADR-tk1-002-model-tools-rollout.md`
- **AC**:
  - [ ] BACKLOG-101 + ADR-tk1-002 reflect corrected math + filename
  - [ ] Edit-history note appended to each (do not silently rewrite history)
- **Effort**: S | **Risk**: Low (administrative cleanup; non-load-bearing — these documents are historical records)

## Out of scope (next BACKLOG entries)

- **Smaller-budget Tier-B/C extractions** (presentation, ui, operations, quality, user-feedback, godot): BACKLOG-104+ for Wave 3
- **Wave 3 governance** (frontmatter `maintainer:` + `fitness_review_due:` + retro KPI): BACKLOG-105+
- **Paradigm sub-skill pattern** (research-agent, user-feedback, presentation per audit): BACKLOG-105+ Wave 3
- **CLAUDE.md refactor** (169→≤150 lines): Wave 3
- **BACKLOG-102 caveman-lite prose discipline**: still queued; sequencing under user direction (parallel with W2 OR after)
- All other plugins (mtg-commander, hardware-team, etc.)

## Sequencing

```
W2-0 ──> W2-1 (cache prefix re-freeze) ─┬──> W2-4 (config tables — also touches prefix)
                                        │
                                        └──> W2-2 (architect contracts)
                                        │
                                        └──> W2-3 (developer coding-standards)
                                        │
                                        └──> W2-5 (product-delivery patterns)

W2-6 (architect model split) ── independent; can run in parallel after W2-2

W2-7 (admin backports) ── parallel with anything; trivial
```

W2-0 first (admin re-baseline; cleans the gate). W2-1 next (the big delivery-flow doctrine extraction with explicit cache-prefix re-freeze ADR-tk2-001). After W2-1, the remaining W2-2/3/4/5 can dispatch in parallel within Stage 6 (no file overlap among them; W2-4 also touches delivery-flow but only the post-prefix region). W2-6 is a frontmatter+sub-skill change independent of the others. W2-7 is administrative cleanup.

## Acceptance Criteria (initiative-level)

1. After Wave 2 lands, `python3 scripts/check_skill_budgets.py` returns exit 0 (no Budget-Exception needed for these 4 files)
2. delivery-flow/SKILL.md ≤500 (Tier-A compliant)
3. architect/SKILL.md, product-delivery/SKILL.md, developer/SKILL.md ≤300 (Tier-B compliant)
4. No regression in delivery-flow first-try DoD pass rate (currently averaging ~70-80% across stages per memory/index.md; Wave 2 should not degrade)
5. Telemetry-measured per-pipeline-run token reduction ≥30% on delivery-flow invocations vs Wave 1 baseline (telemetry hook captures this)
6. Defects/story rate ≤0.4 (stop-rule from BACKLOG-100)

## Pipeline-run preferences

- **Project type**: FEATURE-execution-of-pre-planned-waves (binding-decisions-in-memory pattern, third invocation)
- **Routing**: 1 light · 2 light · 3 SKIP · 4 light · 5 light · 6 full · 7 full (same as Wave 0/1)
- **Theme**: lotr (continued)
- **Models**: Sonnet primaries, Haiku DoD validators (per binding); Opus opt-in only for design synthesis (W2-6 makes this enforceable)
- **Story consolidation**: per memory `topics/project-types.md` Wave 1 lesson, group WIs by file scope. Likely groups:
  - Story 1: delivery-flow doctrine + tables (W2-1 + W2-4)
  - Story 2: architect contracts + model split (W2-2 + W2-6)
  - Story 3: developer coding-standards (W2-3)
  - Story 4: product-delivery patterns (W2-5)
  - Story 5 admin: W2-0 + W2-7 (single Gimli pass; trivial)
  - 5 stories vs 8 WIs → ~40% Stage 6 dispatch savings

## Memory lessons to inject (from chunks)

1. **BACKLOG discovery discipline** (gate-patterns NEW): all file references in BACKLOG-103 above ran through `wc -l`/`find`/`ls` BEFORE finalization
2. **Architect batching math simulation** (architect/refine NEW): for any extraction reducing lines, ADR MUST show before → −Δ → after with after ≤ budget
3. **PRD validation TARGET vs CURRENT** (refine NEW): Stage 2 prompts will explicitly distinguish
4. **Pipeline artifact path canonical** (gate-patterns NEW): validators cite `.delivery/artifacts/<NN>-<stage>/`
5. **Story consolidation by file scope** (project-types NEW): apply to Stage 6 dispatch grouping
6. **Hot lesson #1 runs the command** (5x validated)

## Carry-forward actions integrated

| # | Action | Resolution |
|---|--------|------------|
| 1 | Backport ADR-tk1-002 + BACKLOG-101 W1-7 -1→-2 | W2-7 |
| 2 | Backport BACKLOG-101 W1-3/W1-5 filename | W2-7 |
| 3 | Author BACKLOG-103 (this file) | DONE |
| 4 | File issue: plugin-dev:skill-development invocation pattern | Carryover (not in this BACKLOG; one-off post-pipeline task) |

## Stop-rule

If defects/story rate >0.4 across any 3-PR window OR delivery-flow first-try DoD drops below 60%, pause Wave 3 (BACKLOG-104+) until root-cause retro completes.

## Pre-flight gate

BACKLOG-101 (Wave 1) MUST be merged on main before this pipeline starts. **Status: SATISFIED** — main is at b412a40 (Wave 1 merged 2026-05-05, trunk-based).

## Risk register

| Risk | Severity | Mitigation |
|------|----------|------------|
| Doctrine extraction loses semantic anchors causing F-08 dispatch fusion regression on Opus 4.7 | High | Architect dogfood-validates skeleton with multi-stage pipeline run before merge; ADR-tk2-001 documents which doctrine pieces stay inline as load-bearing gates |
| Cache-prefix re-freeze breaks Wave 1's hash invariant | Med | W2-1 explicit ADR + governance/cache-prefix-hash.txt update; CI gate validates new hash |
| product-delivery 12-pattern split misroutes a task type | Low | Routing table tested with 12/12 inputs in dogfood |
| Architect model split misroutes a synthesis task to Sonnet (under-powered) | Med | Regression set: 10 known synthesis inputs classified identically pre/post |
| W2-7 backport silently rewrites history | Low | Backports MUST include "Edit-history note" footer; no silent rewriting |
