---
title: "Skill Token-Economy — Wave 1 Quick-Wins"
scope: delivery-team plugin only
wave: 1
work_items: [W1-1, W1-2, W1-3, W1-4, W1-5, W1-6, W1-7]
predecessor_run: run-2026-05-03-tk0e
predecessor_pr: 87 (d0e0928)
status: Draft
author: Product Owner (product-delivery skill)
created: 2026-05-03
version: 1.0
---

# Idea Brief: Skill Token-Economy — Wave 1 Quick-Wins

## 1. Scope

Execute all 7 Wave 1 quick-wins from BACKLOG-101. Wave 0 (BACKLOG-100) merged clean (PR #87, d0e0928, GO). Telemetry (W0-1) and CI gate (W0-2) are in place; every Wave 1 item produces measurable token savings validated by telemetry and gated by CI.

## 2. In-Scope Work Items

| ID | Title | Files | Risk | D/P[^1] |
|----|-------|-------|------|---------|
| W1-1 | Cache-prefix freeze for delivery-flow/SKILL.md | SKILL.md + new ADR | Med | P (ADR = D) |
| W1-2 | Stage definitions to YAML manifest | SKILL.md + new stages.yml + JSON schema | Low | **D** (stages.yml created in Stage 6) |
| W1-3 | Haiku for routing/dispatch sub-agents | product-delivery, architect, quality, operations, ui SKILL.md + audit_agent_prompt.py | Low | P (modify existing hook) |
| W1-4 | Selective allowed-tools + description prune | All delivery-team SKILL.md frontmatter + marketplace.json | Low | P |
| W1-5 | Adversarial challenger tier-inheritance + extended thinking OFF | delivery-flow SKILL.md (adversarial-review) + audit_agent_prompt.py | High | P (modify existing hook) |
| W1-6 | Sonnet default for orchestrator + pure-Python hooks audit | delivery-flow SKILL.md frontmatter + all 7 hooks/*.py | Low | P |
| W1-7 | alias-creator -1 line known-debt fix (carry-in from Wave 0) | alias-creator/SKILL.md | Low | P |

[^1]: D = Deliverable (created during pipeline); P = Prerequisite (already exists or derived from existing artifact). W1-2 `stages.yml` does not exist yet — it is produced by Stage 6 Dev, not consumed as input. W1-3 and W1-5 hook target is the **existing** file `delivery-team/hooks/audit_agent_prompt.py` (MODIFY, not create). BACKLOG-101 cites `agent_audit.py` — that filename is wrong; actual file is `audit_agent_prompt.py`. Downstream stages MUST use the actual filename. BACKLOG-101 correction logged for post-pipeline retro action.

All 7 items are mechanically independent and dispatchable in parallel within Stage 6 Dev. See BACKLOG-101 §Sequencing.

## 3. Out of Scope

- Wave 2+ structural extractions (BACKLOG-102+)
- mtg-commander agent-prompt extractions (next plugin BACKLOG)
- All other plugins (hardware-team, agentic-flow-builder, etc.)
- CLAUDE.md refactor (Wave 3 — `tk0e-claude-md-refactor` known-debt)

## 4. Carry-Forward from Wave 0 Retro

| # | Action | Owner | Where applied |
|---|--------|-------|---------------|
| 2 | Wire pre-merge git hook for skill-budget local check | Gimli | W1-7 dogfood |
| 3 | Add cross-doc consistency check to UAT TW gate template | Bilbo | Wave 1 UAT |
| 4 | File issue: plugin-dev:skill-development invocation pattern | Gandalf | Separate one-off |

Note: Action #1 (Author BACKLOG-101) is closed — BACKLOG-101 exists and is the input to this run.

## 5. Plugin-Dev Skill Routing (binding per CLAUDE.md + memory/stages/idea.md)

Pre-loaded for Dev stage agents — do not re-derive:

| WI | Hook changes? | SKILL.md frontmatter changes? | New files? | Required skills |
|----|--------------|-------------------------------|------------|-----------------|
| W1-1 | No | Yes (delivery-flow) | Yes (ADR) | plugin-dev:skill-development |
| W1-2 | No | Yes (delivery-flow) | Yes (stages.yml + schema) | plugin-dev:skill-development |
| W1-3 | Yes — modify existing `audit_agent_prompt.py` | Yes (5 SKILL.md) | No | plugin-dev:hook-development + plugin-dev:skill-development |
| W1-4 | No | Yes (all delivery-team) | No | plugin-dev:skill-development |
| W1-5 | Yes — modify existing `audit_agent_prompt.py` | Yes (delivery-flow) | No | plugin-dev:hook-development + plugin-dev:skill-development |
| W1-6 | No (audit only) | Yes (delivery-flow) | No | plugin-dev:skill-development |
| W1-7 | No | Yes (alias-creator) | No | plugin-dev:skill-development |

Post-completion: `plugin-dev:skill-reviewer` on all modified SKILL.md; `plugin-dev:plugin-validator` before PR.

## 6. Known-Debt Status

**Cleared this wave (W1-7)**:
- `delivery-team/skills/alias-creator/SKILL.md`: 201→≤200 lines, restoring Tier-C compliance; `known_debt` entry removed from `governance/skill-budgets.json`

**Remains after Wave 1**:
- `CLAUDE.md`: 169 lines vs binding 150-line cap — deferred to Wave 3 (`tk0e-claude-md-refactor`; logged in run-2026-05-03-tk0e retro)
- All Tier-B Wave-2 `target_wave` entries in `governance/skill-budgets.json` (presentation 543, ui 493, operations 417, quality 415, user-feedback 397) remain open until Wave 2

## 7. Success Criteria (runnable verification)

Reference: BACKLOG-101 §Acceptance Criteria.

| # | Criterion | Verification command |
|---|-----------|---------------------|
| SC-1 | delivery-flow SKILL.md under Tier-A 500-line budget | `wc -l delivery-team/skills/delivery-flow/SKILL.md` — MUST return ≤500 |
| SC-2 | alias-creator restored to Tier-C compliance | `wc -l delivery-team/skills/alias-creator/SKILL.md` — MUST return ≤200 |
| SC-3 | No delivery-team hook contains LLM calls | `grep -rE "anthropic\|openai\|litellm" delivery-team/hooks/` — MUST return empty |
| SC-4 | No marketplace.json description exceeds 500 chars | `python -c "import json; d=json.load(open('.claude-plugin/marketplace.json')); [print(p['id'],len(p['description'])) for p in d['plugins'] if len(p.get('description',''))>500]"` — MUST return empty |
| SC-5 | CI gate passes after all WIs land (no Budget-Exception needed for alias-creator) | `python scripts/check_skill_budgets.py` — MUST exit 0 without alias-creator warning |

## 8. References

| Artifact | Path |
|----------|------|
| Wave 1 canonical spec (7 WIs + full ACs) | `.delivery/backlog/BACKLOG-101-skill-token-economy-delivery-team-wave-1.md` |
| Wave 0 run archive + carry-forward actions | `.delivery/memory/archive/run-2026-05-03-tk0e.md` |
| Binding decisions (5 rulings + model map) | `.delivery/memory/topics/skill-token-economy.md` |
| Stage 1 routing lesson (plugin-dev constraint) | `.delivery/memory/stages/idea.md` |
| Current known-debt registry | `governance/skill-budgets.json` |
