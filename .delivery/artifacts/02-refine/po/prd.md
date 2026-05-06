---
title: "Skill Token-Economy — Wave 2 PRD"
work_items: [W2-0, W2-1, W2-2, W2-3, W2-4, W2-5, W2-6, W2-7]
sprint: 5-story ceiling (8 WIs consolidated by file scope)
stage: 02-refine
author: Product Owner (product-delivery skill)
source: idea-brief run-2026-05-05-tk2 + BACKLOG-103
created: 2026-05-05
version: 1.0
---

# PRD: Skill Token-Economy — Wave 2 Structural Extractions

## 1. Problem Statement

Wave 0 (d0e0928) and Wave 1 (b412a40) established telemetry, CI gates, cache-prefix freeze,
stage YAML, model-tier rules, and allowed-tools. Wave 2 executes the high-leverage structural
extractions — delivery-flow doctrine, architect contracts, developer coding-standards,
config/commands tables, product-delivery patterns, and architect model split — targeting
Tier-A (≤500) and Tier-B (≤300) compliance for the four heaviest SKILL.md files.

---

## 2. Goals & Success Metrics

| Metric | Baseline (post-Wave-1) | Target |
|--------|------------------------|--------|
| delivery-flow/SKILL.md | 999 lines | ≤ 500 (Tier-A) |
| architect/SKILL.md | 673 lines | ≤ 500 this wave (−175 → ~498; Tier-A met; Tier-B ≤300 deferred Wave 3 BACKLOG-104) |
| product-delivery/SKILL.md | 691 lines | ≤ 300 (Tier-B) |
| developer/SKILL.md | 495 lines | ≤ 300 (Tier-B) |
| Per-pipeline token reduction (delivery-flow load) | Wave 1 baseline | ≥ 30% |
| `check_skill_budgets.py` | Known-debt warnings | Exit 0 |
| Cache-prefix hash | Stale post-W2-1 | ADR-tk2-001 + CI re-baselined |

---

## 3. User Personas

Same as Wave 1: (1) delivery-team plugin contributor — benefits from reduced cold-load;
(2) Wave 3+ executor — inherits re-frozen cache prefix and extracted references.

---

## 4. Functional Requirements

| ID | Requirement | WI |
|----|-------------|----|
| FR-01 | `governance/skill-budgets.json` known-debt MUST reflect actual post-Wave-1 counts (delivery-flow 999, not 1089); `check_skill_budgets.py --known-debt-report` MUST show accurate counts | W2-0 |
| FR-02 | **Doctrine MOVE** (W2-1): Prime Directive prose, Core Principles, One Role = One Sub-Agent prose, Two-Channel prose, Theme-Gated Reporting detail, Common Anti-Patterns, Stage 1–7 verbose detail blocks, Memory/Self-Learning detail MUST MOVE to `delivery-team/references/shared/orchestrator-doctrine.md` | W2-1 |
| FR-03 | **Doctrine STAY** (F-08 anchors): Phase 0 setup wizard (9 questions), Phase 1 project-type detect block, Phase 2 memory load block, Phase 3 routing block, Phase 4 protocol skeleton (Steps 1–10), Stage Routing Matrix table, One Role = One Sub-Agent invariant (1-line), Two-Channel constraint (1-line) MUST STAY inline in `delivery-flow/SKILL.md` | W2-1 |
| FR-04 | ADR-tk2-001 MUST be committed enumerating inline anchors vs extracted content, citing F-08 risk, and documenting explicit batching math: **999 → −Δ_W2-1 (~480) → −Δ_W2-4 (~30) → ≤ 489 lines** | W2-1 |
| FR-05 | `governance/cache-prefix-hash.txt` MUST be updated post-doctrine extraction; CI hash-check MUST pass on the new hash (ADR-tk2-001 governs this) | W2-1 |
| FR-06 | Five architect output contracts (Design, ADR, Game Architecture, Review, Technology Evaluation) MUST MOVE to `architect/references/output-contracts/{design,adr,game,review,evaluation}.md`; SKILL.md MUST retain task_type → contract routing table | W2-2 |
| FR-07 | Architect skill router MUST return `{role, task_type, recommended_model}`; classification phases MUST dispatch on Sonnet; design synthesis (ADR drafting, TO-BE) MUST dispatch on Opus; phase-to-model map MUST be documented in SKILL.md | W2-6 |
| FR-08 | Developer coding-standards (~155 lines) MUST MOVE to `developer/references/agent-prompts/coding-standards.md` + `developer/references/coding-standards-template.md`; SKILL.md MUST retain one-line dispatch pointer | W2-3 |
| FR-09 | Three tables MUST MOVE from `delivery-flow/SKILL.md`: Config Settings (35 rows) → `references/config-keys.md`; User Commands (18 rows) → `references/commands.md`; References Manifest (19 rows) → `references/manifest.yml`; SKILL.md MUST retain one-line pointers | W2-4 |
| FR-10 | All 12 `### Pattern N:` blocks in `product-delivery/SKILL.md` MUST MOVE to `product-delivery/references/patterns/<slug>.md` (12 files); Phase 1 routing table MUST map task_type → pattern file; Phase 2 MUST load only matched pattern | W2-5 |
| FR-11 | BACKLOG-101 and ADR-tk1-002 MUST receive: W1-7 math correction (−1 → −2), W1-3/W1-5 filename correction (`agent_audit.py` → `audit_agent_prompt.py`), and Edit-history note footer (no silent rewriting) | W2-7 |
| FR-12 | W2-1/2/3/4/5/6 MUST pre-load `plugin-dev:skill-development` before any SKILL.md or references file is created/modified; W2-0 and W2-7 (admin-only) do NOT require plugin-dev dispatch | All |
| FR-13 | All WI-level ADRs (especially ADR-tk2-001) MUST include explicit batching math: before → −Δ → after for each SKILL.md line-count target; silent assertions MUST be rejected | W2-1 |

---

## 5. Non-Functional Requirements

| ID | Requirement | Verification |
|----|-------------|--------------|
| NFR-01 | delivery-flow ≤ 500 (Tier-A). Math: 999 → −Δ_W2-1 (~480) → −Δ_W2-4 (~30) → **≤ 489** | `wc -l delivery-team/skills/delivery-flow/SKILL.md` ≤ 500 |
| NFR-02 | architect/SKILL.md MUST be reduced to ≤500 lines this wave (partial Tier-B progress); full ≤300 Tier-B compliance is deferred to Wave 3 BACKLOG-104 (per-role + per-task-type extractions). Math: 673 → −Δ_W2-2 (~155) → −Δ_W2-6 (~20) → **~498** (Tier-A 500-line ceiling met; Tier-B 300 deferred) | `wc -l delivery-team/skills/architect/SKILL.md` ≤ 500 |
| NFR-03 | product-delivery ≤ 300 (Tier-B). Math: 691 → −Δ_W2-5 (~380) → **~311** — Stage 6 MUST trim ~12 more lines | `wc -l delivery-team/skills/product-delivery/SKILL.md` ≤ 300 |
| NFR-04 | developer ≤ 300 (Tier-B). Math: 495 → −Δ_W2-3 (~155) → **~340** — Stage 6 MUST trim ~41 more lines | `wc -l delivery-team/skills/developer/SKILL.md` ≤ 300 |
| NFR-05 | F-08 anchors (Phase 0/1/2/3/4, Stage Routing Matrix) MUST remain inline; verified by Architect dogfood synthetic run | Route correctness on Idea + Architect + Dev dispatch before merge |
| NFR-06 | `governance/cache-prefix-hash.txt` MUST be updated; CI MUST pass on new hash | `cat governance/cache-prefix-hash.txt` non-empty; CI green |
| NFR-07 | Per-pipeline token reduction ≥ 30% on delivery-flow load vs Wave 1 baseline | Telemetry diff post-merge |

---

## 6. Out of Scope

Wave 3+ (presentation, ui, operations, quality, user-feedback, godot), CLAUDE.md refactor,
BACKLOG-102, paradigm sub-skill pattern, governance frontmatter, mtg-commander, hardware-team,
all other plugins, plugin-dev invocation-pattern issue (carryover post-pipeline).
Full architect Tier-B compliance (≤300) — deferred to Wave 3 BACKLOG-104 per honest batching math (Wave 2 reduces to ~498).

---

## 7. Dependencies & Risks

| Item | Severity | Mitigation |
|------|----------|------------|
| W2-1 F-08 dispatch fusion regression: doctrine extraction loses routing semantic anchors on Opus 4.7 | HIGH | FR-03 enumerates inline-anchor list; Architect dogfood-validates skeleton on synthetic multi-stage run BEFORE merge; correctness beats line count — restore anchors if routing misfires |
| W2-1 cache invalidation: deliberate prefix change breaks Wave 1 hash invariant | MED | FR-05 mandates `cache-prefix-hash.txt` update + CI re-baseline as W2-1 merge checklist item |
| W2-6 architect synthesis under-power: misroutes ADR/TO-BE synthesis to Sonnet | MED | Regression set: 10 synthesis inputs classified identically pre/post; >1 misroute blocks merge |
| NFR-03/04 surplus lines: product-delivery ~11 over, developer ~40 over after primary extraction | LOW | Stage 6 Dev MUST identify and cut surplus lines (header/boilerplate candidates) before dispatch |
| W2-4 touches delivery-flow post-prefix region | Dep | Sequence W2-4 after W2-1 or in same PR to avoid double hash-update |
| architect Tier-B compliance not fully achieved this wave | KNOWN DEBT | tracked in skill-budgets.json post-Wave-2 known_debt entry; targeted in BACKLOG-104 (Wave 3 per-role + per-task-type extractions) |

---

## 8. Acceptance Criteria

Sprint ceiling: 5 stories. Story grouping: S1=W2-1+W2-4, S2=W2-2+W2-6, S3=W2-3, S4=W2-5, S5=W2-0+W2-7.

**W2-0**
```bash
python3 scripts/check_skill_budgets.py --known-debt-report  # shows delivery-flow=999; no stale entries
```

**W2-1 — doctrine extraction + cache re-freeze**
```bash
wc -l delivery-team/skills/delivery-flow/SKILL.md                                    # MUST: ≤ 500
ls delivery-team/references/shared/orchestrator-doctrine.md                          # MUST: exists
grep -c "Phase 0\|setup wizard" delivery-team/skills/delivery-flow/SKILL.md          # MUST: ≥ 1
grep -c "Stage Routing Matrix" delivery-team/skills/delivery-flow/SKILL.md           # MUST: ≥ 1
grep -c "Phase 4\|protocol skeleton" delivery-team/skills/delivery-flow/SKILL.md    # MUST: ≥ 1
ls delivery-team/skills/delivery-flow/references/adrs/ADR-tk2-001*.md               # MUST: ≥ 1
grep -c "999\|−Δ\|489\|≤500" delivery-team/skills/delivery-flow/references/adrs/ADR-tk2-001*.md  # MUST: ≥ 1
cat governance/cache-prefix-hash.txt                                                 # MUST: new hash value; CI green
```

**W2-2**
```bash
ls delivery-team/skills/architect/references/output-contracts/  # MUST: 5 files
wc -l delivery-team/skills/architect/SKILL.md                   # MUST: ≤ 500 (Tier-B ≤300 deferred to Wave 3 BACKLOG-104)
grep -c "output-contracts\|task_type" delivery-team/skills/architect/SKILL.md  # MUST: ≥ 1
# MUST: skill-budgets.json known_debt entry for architect retained with target_wave=3
```

**W2-3**
```bash
ls delivery-team/skills/developer/references/agent-prompts/coding-standards.md  # MUST: exists
ls delivery-team/skills/developer/references/coding-standards-template.md       # MUST: exists
wc -l delivery-team/skills/developer/SKILL.md                                   # MUST: ≤ 300
```

**W2-4**
```bash
ls delivery-team/skills/delivery-flow/references/config-keys.md \
   delivery-team/skills/delivery-flow/references/commands.md \
   delivery-team/skills/delivery-flow/references/manifest.yml   # MUST: all 3 exist
grep -c "config-keys\|commands\|manifest" delivery-team/skills/delivery-flow/SKILL.md  # MUST: ≥ 3
```

**W2-5**
```bash
ls delivery-team/skills/product-delivery/references/patterns/ | wc -l          # MUST: 12
wc -l delivery-team/skills/product-delivery/SKILL.md                           # MUST: ≤ 300
grep -c "task_type\|pattern" delivery-team/skills/product-delivery/SKILL.md    # MUST: ≥ 12
```

**W2-6**
```bash
grep -c "recommended_model\|Sonnet\|Opus" delivery-team/skills/architect/SKILL.md  # MUST: ≥ 3
# Regression set (10 synthesis inputs, 10/10 classified correctly) MUST be attached to PR
```

**W2-7**
```bash
grep -c "Edit-history" .delivery/backlog/BACKLOG-101-skill-token-economy-delivery-team-wave-1.md  # MUST: ≥ 1
grep -c "Edit-history" .delivery/artifacts/04-architect/adrs/ADR-tk1-002-model-tools-rollout.md  # MUST: ≥ 1
grep -c "audit_agent_prompt" .delivery/backlog/BACKLOG-101-skill-token-economy-delivery-team-wave-1.md  # MUST: ≥ 1
```

**Initiative gate**
```bash
python3 scripts/check_skill_budgets.py  # MUST: exit 0
wc -l delivery-team/skills/{delivery-flow,architect,product-delivery,developer}/SKILL.md
# MUST: 500 / 500 / 300 / 300 or under  (architect Tier-B ≤300 deferred to Wave 3 BACKLOG-104)
```

---

## 9. Open Questions

**None.** All decisions bound in `.delivery/memory/topics/skill-token-economy.md` + BACKLOG-103.

---

## 10. Verification Plan

W2-1 is HIGH RISK and requires pre-merge dogfood: Architect MUST run a synthetic pipeline
(Idea + Architect + Dev dispatch minimum) against the skeleton delivery-flow/SKILL.md and
confirm Phase 0/1/2/3 routing is correct. Routing misfire → restore anchors inline;
doctrine file grows to compensate.

| Story | Dogfood evidence MUST appear in PR body |
|-------|-----------------------------------------|
| S1: W2-1+W2-4 | Synthetic pipeline run log: Phase 0–3 route correctly; telemetry diff ≥30% token drop; CI green with new cache hash |
| S2: W2-2+W2-6 | ADR-authoring dispatch log: only `adr.md` contract loaded; regression set 10/10 attached |
| S3: W2-3 | `write` task: template NOT loaded (log); `coding-standards` task: template IS loaded (log); `wc -l` ≤ 300 pasted |
| S4: W2-5 | Routing-table 12/12 task-type dispatch log; `wc -l` ≤ 300 pasted |
| S5: W2-0+W2-7 | `--known-debt-report` output pasted; Edit-history notes visible in diff |
