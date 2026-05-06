---
title: "Wave 2 Solution Architecture — Skill Token-Economy"
wave: 2
stage: 04-architect
author: Architect (delivery-team:architect, Celebrimbor persona)
created: 2026-05-05
adrs: [ADR-tk2-001, ADR-tk2-002, ADR-tk2-003]
---

# Wave 2 Solution Architecture: Skill Token-Economy Structural Extractions

*"Let us forge something that will endure beyond the ages."*

## Overview

Wave 2 executes five structural extractions across four SKILL.md files, grouped into
three stories. The critical path runs through Story 1 (W2-1 doctrine extraction) because
it invalidates the Wave 1 cache prefix, blocks Story 1's merge until dogfood validates,
and must complete before the CI hash-check can re-baseline.

---

## Story Grouping & ADR Coverage

```mermaid
graph TD
    subgraph S5["Story 5 — Admin (W2-0 + W2-7)"]
        W20["W2-0: Re-baseline skill-budgets.json"]
        W27["W2-7: Backport BACKLOG-101 + ADR-tk1-002"]
    end

    subgraph S1["Story 1 — delivery-flow (W2-1 + W2-4) [CRITICAL PATH]"]
        W21["W2-1: Doctrine → orchestrator-doctrine.md\n(~480 lines extracted)\nADR-tk2-001"]
        W24["W2-4: Config/Commands/Manifest tables\n(~30 lines extracted)\nADR-tk2-001 §D"]
        HASH["Cache-prefix re-freeze\n(governance/cache-prefix-hash.txt)\nCI re-baseline"]
        DOG1["Dogfood gate: Phase 0–3 synthetic run\nBEFORE merge"]
        W21 --> W24
        W24 --> HASH
        HASH --> DOG1
    end

    subgraph S2["Story 2 — architect (W2-2 + W2-6)"]
        W22["W2-2: 5 contracts → output-contracts/\n(~155 lines extracted)\nADR-tk2-002"]
        W26["W2-6: Model split router\n{role, task_type, recommended_model}\nADR-tk2-002"]
        REG["Regression set: 10 inputs × 10/10\nattached to PR"]
        W22 --> REG
        W26 --> REG
    end

    subgraph S3["Story 3 — developer (W2-3)"]
        W23["W2-3: coding-standards → 2 references\n(~155 lines extracted)\nADR-tk2-003"]
        DOG3["Dogfood: write task (template NOT loaded)\ncoding-standards task (template IS loaded)"]
        W23 --> DOG3
    end

    subgraph S4["Story 4 — product-delivery (W2-5)"]
        W25["W2-5: 12 patterns → patterns/*.md\n(~380 lines extracted)\nADR-tk2-003"]
        DOG4["Dogfood: 12/12 task-type dispatch log"]
        W25 --> DOG4
    end

    S5 -->|"pre-flight gate: budgets.json accurate"| S1
    S1 -->|"cache hash stable"| S2
    S1 -->|"cache hash stable"| S3
    S1 -->|"cache hash stable"| S4
    S2 -.->|"parallel"| S3
    S3 -.->|"parallel"| S4
```

---

## Line-Count Targets (Architect Batching Simulation)

| Skill | Baseline | Primary Extract | Surplus Trim | Target | Tier | Status |
|-------|----------|-----------------|--------------|--------|------|--------|
| delivery-flow | 999 | −480 (W2-1) | −30 (W2-4) | **489** | A (≤500) | ✓ |
| architect | 673 | −155 (W2-2) | −20 (W2-6) | **498** | A (≤500) ✓ / B (≤300) deferred Wave 3 | partial |
| product-delivery | 691 | −380 (W2-5) | −11 (Stage 6) | **300** | B (≤300) | ✓ if Stage 6 trims 11 |
| developer | 495 | −155 (W2-3) | −40 (Stage 6) | **300** | B (≤300) | ✓ if Stage 6 trims 40 |

Known-debt entries for architect (~198 lines), product-delivery (+11 risk), and
developer (+40 risk) MUST be recorded in `governance/skill-budgets.json` post-merge.

---

## Critical Risk Register

| Risk | ADR | Mitigation |
|------|-----|------------|
| F-08 dispatch fusion regression (doctrine extraction removes Phase 0–4 anchors) | ADR-tk2-001 §A | Explicit anchor list; dogfood gate (Phase 0–3 synthetic run) BEFORE merge |
| Cache invalidation breaks Wave 1 hash invariant | ADR-tk2-001 §D | Deliberate re-freeze; CI re-baselines to new hash; W2-4 in same PR |
| W2-6 synthesis mis-routed to Sonnet (under-powered ADR drafting) | ADR-tk2-002 §W2-6 | 10-input regression set; >1 misroute blocks merge |
| product-delivery +11 lines, developer +40 lines post-primary-extract | ADR-tk2-003 §Math | Stage 6 Dev trims identified candidates; remainder known-debt if unresolved |
| architect Tier-B not met this wave (198-line debt) | ADR-tk2-002 §Math | skill-budgets.json known_debt entry; BACKLOG-104 Wave 3 per-role extractions |

---

## New File Inventory (22 files)

| Story | New Files |
|-------|-----------|
| S1 W2-1 | `delivery-team/references/shared/orchestrator-doctrine.md` |
| S1 W2-4 | `delivery-flow/references/{config-keys.md,commands.md,manifest.yml}` (×3) |
| S2 W2-2 | `architect/references/output-contracts/{design,adr,game,review,evaluation}.md` (×5) |
| S3 W2-3 | `developer/references/agent-prompts/coding-standards.md` + `coding-standards-template.md` (×2) |
| S4 W2-5 | `product-delivery/references/patterns/<slug>.md` (×12) |

---

## Wave 1 Retro Lessons Applied

| Lesson | Applied |
|--------|---------|
| Batching math simulation | All 3 ADRs show before→−Δ→after; known-debt explicit if over |
| F-08 anchor preservation | ADR-tk2-001 §A enumerates anchors with line-range estimates |
| Cache-prefix re-freeze contract | ADR-tk2-001 §D: procedure + historical hash recorded |
| Plugin-dev pre-load | FR-12 acknowledged in all 3 ADRs |
| Dogfood before merge | S1 dogfood gate is Architect-mandated pre-merge condition |

---

## Acceptance Verification (post-merge)

```bash
wc -l delivery-team/skills/delivery-flow/SKILL.md          # MUST: ≤500
ls delivery-team/references/shared/orchestrator-doctrine.md # MUST: exists
cat governance/cache-prefix-hash.txt                        # MUST: ≠ aea33d57...
wc -l delivery-team/skills/architect/SKILL.md              # MUST: ≤500
ls delivery-team/skills/architect/references/output-contracts/ | wc -l # MUST: 5
wc -l delivery-team/skills/developer/SKILL.md              # MUST: ≤300
wc -l delivery-team/skills/product-delivery/SKILL.md       # MUST: ≤300
ls delivery-team/skills/product-delivery/references/patterns/ | wc -l  # MUST: 12
python3 scripts/check_skill_budgets.py                     # MUST: exit 0
```
