---
title: "Sprint Plan — Skill Token-Economy Wave 1"
sprint: Wave-1
stage: 05-plan
author: Scrum Master (product-delivery skill)
sources: [prd.md v1.0, ADR-tk1-001, ADR-tk1-002, ADR-tk1-003, architecture-tk1-wave1.md]
created: 2026-05-04
version: 1.0
---

# Sprint Plan: Skill Token-Economy Wave 1

## 1. Sprint Goal

Ship Wave 1's cache-prefix freeze, stage extraction, model-tier assignments, and token-budget debt clearance — achieving ≥2,000-token cold-load reduction and ≥3× per-run cost savings.

---

## 2. Sprint Dates

**Sprint Wave-1** — single iteration, no mid-sprint replan, 7-WI ceiling.

---

## 3. Capacity Declaration

| Parameter | Value |
|-----------|-------|
| Team size | 1 (solo) — `config: team.size: 1` |
| Effective capacity ceiling | 80% — full attention on committed 7 WIs |
| Buffer | 20% — unplanned defects and dogfood re-runs only |
| Replan trigger | None — sprint ceiling is absolute per PRD §8 |

---

## 4. Committed Stories

| WI | Story Title | Estimate | Dependencies | Commit Group |
|----|-------------|----------|--------------|--------------|
| W1-1 | Cache-prefix freeze + Volatile marker | M | Wave 0 infra | A |
| W1-2 | stages.yml extraction + JSON schema | M | W1-1 (same file; group after A) | B |
| W1-3 | Haiku model frontmatter on 5 SKILL.md files | S | Wave 0 tier frontmatter | C |
| W1-4 | allowed-tools whitelist on 13 SKILL.md + marketplace prune | M | W1-7 must be batched | C |
| W1-5 | Challenger model-tier hook + adversarial section update | S | Wave 0 infra | D |
| W1-6 | delivery-flow model:sonnet + hooks LLM audit | S | W1-1 (Group A must land first) | E |
| W1-7 | alias-creator -1 line + known-debt entry removal | S | must batch with W1-4 | C |

**Estimates**: S = ~1 hr focused work; M = ~2–3 hrs including verification; L = not present.

---

## 5. Commit Sequencing Groups

Each group is one atomic commit on the feature branch. Order is enforced.

| Group | WIs | Key constraint | Plugin-dev skill(s) required |
|-------|-----|---------------|------------------------------|
| A | W1-1 | MUST be first — fixes frozen prefix boundary; establishes `cache-prefix-hash.txt` | `skill-development` |
| B | W1-2 | After A; independent of C/D/E — stage region (L613–746) distinct from frozen prefix | `skill-development` |
| C | W1-3+W1-4+W1-7 | BATCHED (hard) — alias-creator at 201L; W1-7 **-2 lines** + W1-4 +1 line (allowed-tools) = net -1 → final 200 ✓; FR-15 pre-rollout `wc -l` MANDATORY before edits. (ADR-tk1-002 originally said -1; real-math correction is -2 — backport to ADR-tk1-002 + BACKLOG-101 deferred to retro) | `skill-development`, `hook-development`, `plugin-structure` |
| D | W1-5 | After A; independent of B/C — adversarial section not in frozen prefix region | `hook-development`, `skill-development` |
| E | W1-6 | MUST follow A — frontmatter edit in frozen prefix; commit MUST update `cache-prefix-hash.txt` with `Cache-Prefix-Change: ADR-tk1-002` | `skill-development` |

**Group C artifact list**: 5 SKILL.md (`product-delivery`, `architect`, `quality`, `operations`, `ui`) +
all 13 delivery-team SKILL.md (allowed-tools, allowlist-over-deny pattern) +
`alias-creator/SKILL.md` (-1 line) + `governance/skill-budgets.json` (debt entry removed) +
`.claude-plugin/marketplace.json` (description 913→≤500, ADR-tk1-002 prescribed text) +
`audit_agent_prompt.py` (routing-tier mismatch warn, pure Python, no LLM calls).

---

## 6. Commitment Rationale

**Why these 7**: All items are mechanically scoped, have pre-confirmed artifact lists, and carry
runnable acceptance criteria from PRD §8. Combined they deliver the full cache-stability and
cost-reduction gains defined in the Wave 1 mission. Sequencing constraints are fully resolved by
the ADRs; no open decisions remain.

**What is NOT included**:
- BACKLOG-102+ Wave 2+ structural extractions (delivery-flow deep content reduction)
- CLAUDE.md refactor (`tk0e-claude-md-refactor` known-debt — Wave 3)
- mtg-commander agent-prompt extractions
- hardware-team, agentic-flow-builder, research-agent, prd-quality-gate-flow plugins
- Telemetry dashboards (Wave 2 concern)
- Shadow A/B testing for Sonnet flip (resolved: immediate flip with telemetry watch, ADR-tk1-002)

---

## 7. Risks to Sprint Goal

| # | Risk | Severity |
|---|------|----------|
| a | Cache-prefix self-modification breaks downstream pipelines | High |
| b | Mandatory-rollout side-effect across 13 SKILL.md (Group C mass edit) | High |
| c | `audit_agent_prompt.py` extensions cause false-positive warnings on existing dispatches | Medium |
| d | Marketplace description prune loses skill trigger phrases | Medium |

---

## 8. Risk Mitigations

**(a) Cache-prefix self-modification**
All commits land on a dedicated feature branch. After Group A lands, a second delivery-flow
invocation is run via dogfood before merge to main; telemetry cache_read/input ≥0.85 is the
pass gate. Group E must update `cache-prefix-hash.txt` in its own commit or CI blocks the PR.
Revert path: single-line frontmatter edit + hash restore.

**(b) Mandatory-rollout side-effect**
FR-15 pre-rollout `wc -l` simulation is mandatory before Group C begins. Current confirmed
baseline: only alias-creator is at a budget edge (201 lines). Corrected math:
`alias-creator: 201 → -2 (W1-7) → 199 → +1 (W1-4 allowed-tools) → 200 ✓`
W1-7 MUST trim **2 lines** (not 1; ADR-tk1-002 had -1 — correction deferred to retro as backport to
ADR-tk1-002 + BACKLOG-101). Post-edit re-scan is diffed against baseline and attached to PR. No other
file is within 1 line of its ceiling (per ADR-tk1-002 baseline).

**(c) audit_agent_prompt.py false positives**
Both W1-3 and W1-5 extensions are additive; no existing logic removed. W1-3 detects role fields
containing `router|detector|dispatch|classify`; W1-5 detects `adversarial|challenger|critic|reviewer`.
Existing non-routing dispatches carry neither tag set. Verify with
`grep -rE 'anthropic|openai|litellm' delivery-team/hooks/` post-edit (must return empty).

**(d) Marketplace description prune loses trigger phrases**
ADR-tk1-002 §W1-4 prescribes a specific ~280-char replacement that retains all trigger phrases
and skill count. Developer uses the ADR-prescribed text verbatim and verifies with the PRD §8
AC-W1-4 one-liner before marking Done.

---

## 9. Dogfood Plan

Per BACKLOG-100 W0-1 directive: every Wave 1 item MUST be validated by running a delivery-flow
pipeline iteration end-to-end. Evidence MUST appear in the PR body or a linked gist.

| WI | Required dogfood evidence | Produced after |
|----|--------------------------|----------------|
| W1-1 | Telemetry row: `cache_read/input ≥ 0.85` on second delivery-flow invocation | Group A lands |
| W1-2 | Full 7-stage pipeline run; telemetry diff showing ≥2,000 token drop vs pre-W1-2 baseline | Group B lands |
| W1-3 | 10-sample dispatch log: `model: haiku` routing; 10/10 correct role selections | Group C lands |
| W1-4 | `find delivery-team -name SKILL.md -exec grep -L allowed-tools {} \;` empty (paste); all descriptions ≤500 (paste AC output) | Group C lands |
| W1-5 | Adversarial round excerpt: ≥1 substantive critique; `grep challenger audit_agent_prompt.py` output shown | Group D lands |
| W1-6 | End-to-end pipeline run on Sonnet default; telemetry diff ≥3× cost reduction vs Opus baseline; hooks grep clean | Group E lands |
| W1-7 | `wc -l alias-creator/SKILL.md` ≤200 (paste); `check_skill_budgets.py` exit 0 without alias-creator warning | Group C lands |

**Batch dogfood gate after Group C**: Dispatch a 1-stage synthetic delivery-flow run with
telemetry enabled and `model: haiku` routing active. Verify `.delivery/telemetry/skill-loads.jsonl`
captures haiku model invocation for routing decisions. This single run validates W1-3, W1-4, and
W1-7 simultaneously and satisfies the BACKLOG-100 W0-1 dogfood directive for all three items.

---

## 10. Definition of Done (Sprint-Level)

- [ ] All 7 WIs landed on feature branch; PR passes CI (budget gate + schema validation + cache hash check)
- [ ] `alias-creator/SKILL.md` confirmed ≤200 lines (`wc -l` output in PR body) — W1-7 MUST remove **2 lines** (corrected from -1; see §8b)
- [ ] All 13 delivery-team SKILL.md files carry `allowed-tools:` frontmatter (AC find command returns no output)
- [ ] `delivery-flow/SKILL.md` frontmatter declares `model: sonnet`, `extended_thinking: false`; `## Volatile` marker present near EOF
- [ ] `stages.yml` validates against `stages-schema.json`; 7-stage count assertion prints PASS
- [ ] `audit_agent_prompt.py` extended with routing-tier and challenger-tier checks; zero false positives on existing non-routing dispatches confirmed by grep
- [ ] Telemetry JSONL captures haiku-tier dispatch on at least one dogfood run (batch dogfood gate passed)
- [ ] All plugin-dev skill routing followed: `plugin-dev:skill-development` for SKILL.md edits (Groups A–E); `plugin-dev:hook-development` for hook edits (Groups C, D); `plugin-dev:plugin-structure` for marketplace.json (Group C)
- [ ] Retrospective completed; defects found during dogfood logged to backlog; changelog/release notes draft committed
- [ ] No new items entered sprint; 7-WI ceiling maintained

---

## 11. Retro Actions (carry-forward)

| # | Action | Owner | When |
|---|--------|-------|------|
| R-1 | Backport W1-7 line-count correction: ADR-tk1-002 + BACKLOG-101 both say `-1 line`; real-math is `-2 lines`. Update both artifacts to reflect corrected target. | Dev | Sprint retro |
