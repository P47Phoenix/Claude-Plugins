---
title: "Skill Token-Economy — Wave 1 PRD"
work_items: [W1-1, W1-2, W1-3, W1-4, W1-5, W1-6, W1-7]
sprint: single-iteration, 7-WI ceiling
stage: 02-refine
author: Product Owner (product-delivery skill)
source: idea-brief v1.0 (run-2026-05-04-tk1) + BACKLOG-101
created: 2026-05-04
version: 1.0
---

# PRD: Skill Token-Economy — Wave 1 Quick-Wins

## 1. Problem Statement

Wave 0 (PR #87, d0e0928) delivered telemetry and CI budget enforcement. Wave 1 executes 7
targeted quick-wins — cache stabilization, stage-definition externalization, model-tier
assignments, tool allow-lists, and known-debt clearance — projected to reduce delivery-flow
cold-load tokens ≥2,000 and cut per-run cost ≥3× vs the Opus baseline. All 7 items are
mechanically independent and dispatchable in parallel within Stage 6 Dev.

---

## 2. Goals & Success Metrics

| Metric | Target | Baseline |
|--------|--------|----------|
| delivery-flow SKILL.md line count | ≤ 500 | 1090 (confirmed `wc -l`) |
| alias-creator SKILL.md line count | ≤ 200 | 201 (confirmed `wc -l`) |
| Cold-load token delta for delivery-flow | ≥ 2,000 token drop | N/A — Wave 0 baseline |
| Per-run cost vs Opus baseline | ≥ 3× reduction | N/A — Wave 0 baseline |
| Cache read/input ratio (2nd run) | ≥ 0.85 | Prefix not frozen |
| Routing agents declaring `model: haiku` | 10/10 correct decisions | 0 declared |
| Delivery-team skills with `allowed-tools` | All Tier-A + Tier-B | 0 set |
| marketplace.json descriptions ≤ 500 chars | All plugins | delivery-team: 913 chars (FAILS) |

---

## 3. User Personas

| Persona | Description |
|---------|-------------|
| **Primary** — delivery-team plugin contributor | Engineers modifying delivery-team SKILL.md; CI gate enforces gains |
| **Secondary** — Wave 2+ executor | Inherits frozen cache prefix, YAML stage manifest, and model map before Wave 2 begins |

---

## 4. Functional Requirements

| ID | Requirement | Priority | WI |
|----|-------------|----------|----|
| FR-01 | First ~2,000 tokens of `delivery-flow/SKILL.md` MUST be byte-stable across runs; volatile content MUST appear after `## Volatile` marker near EOF | Must Have | W1-1 |
| FR-02 | A new ADR MUST be committed requiring future delivery-flow prefix changes to cite cache-cost impact | Must Have | W1-1 |
| FR-03 | 7 stage definitions (SKILL.md lines ~612–743) MUST move to `delivery-flow/references/stages.yml`; SKILL.md MUST retain a routing pointer only | Must Have | W1-2 |
| FR-04 | `stages.yml` MUST validate against a committed companion JSON schema | Must Have | W1-2 |
| FR-05 | Routing/dispatch/paradigm sub-agents in product-delivery, architect, quality, operations, ui SKILL.md MUST declare `model: haiku` | Must Have | W1-3 |
| FR-06 | `delivery-team/hooks/audit_agent_prompt.py` MUST be extended to warn when a routing agent runs under a non-Haiku model (filename binding — NOT `agent_audit.py`) | Must Have | W1-3 |
| FR-07 | All `delivery-team/**/SKILL.md` frontmatter MUST declare `allowed-tools: [Read, Edit, Write, Bash, Skill, ToolSearch]`; extensions MUST include inline justification | Must Have | W1-4 |
| FR-08 | Every `.claude-plugin/marketplace.json` description > 500 chars MUST be pruned to ≤ 500 (delivery-team: 913 → ≤ 500) | Must Have | W1-4 |
| FR-09 | Adversarial challenger sub-agents in delivery-flow MUST inherit primary agent's `model:` at dispatch; adversarial-review section MUST be updated | Must Have | W1-5 |
| FR-10 | Extended thinking MUST default OFF in all delivery-team agent frontmatter; opt-in per-stage only | Must Have | W1-5 |
| FR-11 | `audit_agent_prompt.py` MUST enforce challenger.model == primary.model (warn-only Sprint 1) | Must Have | W1-5 |
| FR-12 | `delivery-flow/SKILL.md` frontmatter MUST declare `model: sonnet`; Opus MUST be opt-in per-stage | Must Have | W1-6 |
| FR-13 | All 7 `delivery-team/hooks/*.py` MUST be audited and confirmed to contain NO LLM calls | Must Have | W1-6 |
| FR-14 | `alias-creator/SKILL.md` MUST be reduced by exactly 1 line to ≤ 200; `governance/skill-budgets.json` known-debt entry MUST be removed | Must Have | W1-7 |
| FR-15 | Pre-rollout `wc -l` simulation MUST be recorded before any mass-edit touching ≥3 SKILL.md files (W1-3/4/5/6); output MUST be attached to PR | Must Have | W1-3/4/5/6 |
| FR-16 | Dev MUST load `plugin-dev:skill-development` before modifying any SKILL.md; `plugin-dev:hook-development` before modifying hooks/*.py | Must Have | All WIs |

---

## 5. Non-Functional Requirements

| ID | Requirement | Verification |
|----|-------------|--------------|
| NFR-01 | Hook overhead MUST remain < 50 ms (unchanged from Wave 0) | `python3 delivery-team/hooks/telemetry.py --dry-run` ×10; mean < 50 ms |
| NFR-02 | Telemetry schema MUST remain v1; no new fields without schema bump | `grep 'version: 1' delivery-team/references/telemetry-schema.md` matches |
| NFR-03 | CI gate MUST pass after all 7 WIs; no `Budget-Exception:` needed for alias-creator | `python scripts/check_skill_budgets.py` exits 0 without alias-creator warning |
| NFR-04 | Tier budget values MUST remain exactly 500/300/200 | `grep -n 'TIER_LIMITS\|500\|300\|200' scripts/check_skill_budgets.py` shows only these three |
| NFR-05 | No SKILL.md MUST be content-reduced beyond W1-7's -1-line target; reduction is Wave 2 | `git diff --stat HEAD -- 'delivery-team/**/SKILL.md'` delta ≤ 0 except alias-creator (-1) and delivery-flow (W1-2) |
| NFR-06 | W1-3/W1-5 changes to `audit_agent_prompt.py` MUST NOT introduce LLM calls | `grep -E "anthropic|openai|litellm" delivery-team/hooks/audit_agent_prompt.py` returns empty |

---

## 6. Out of Scope

- Wave 2+ structural extractions (BACKLOG-102+); mtg-commander agent-prompt extractions
- All non-delivery-team plugins (hardware-team, agentic-flow-builder, research-agent, etc.)
- CLAUDE.md refactor (Wave 3 — `tk0e-claude-md-refactor` known-debt); telemetry dashboards

---

## 7. Dependencies & Risks

| Item | Type | Detail | Mitigation |
|------|------|--------|------------|
| W1-1 cache-prefix self-modification | Risk | Modifying delivery-flow/SKILL.md affects FUTURE invocations only; current pipeline run loads pre-modification prefix | ADR required; verify on second run via telemetry cache_read/input ≥ 0.85 |
| W1-3/4/5/6 mandatory-rollout side-effect | Risk (HIGH) | 4 WIs touch multiple SKILL.md files simultaneously; mass-edit errors trigger CI failures | FR-15 pre-rollout `wc -l` simulation MUST be recorded before edits begin |
| W1-5 adversarial quality loss | Risk (HIGH) | Capability asymmetry kills adversarial property; anti-pattern session 0876a59e (14 undetected violations) | Warn-only Sprint 1; re-run failing validators at Sonnet before reopening loop |
| W1-6 Sonnet flip approach | Open team decision | 5-run shadow A/B vs immediate flip with telemetry watch | Default: shadow A/B per mission-critical risk tolerance (BACKLOG-101 §W1-6) |
| W1-2 stages.yml not on disk | Dependency | `stages.yml` is a Stage 6 Dev deliverable (D), not a prerequisite | Dev creates it; no upstream artifact to read |
| audit_agent_prompt.py filename | Binding correction | BACKLOG-101 cites `agent_audit.py` — WRONG; confirmed `audit_agent_prompt.py` via `ls delivery-team/hooks/` | All Dev agents MUST use `audit_agent_prompt.py` |
| delivery-team marketplace description | Known violation | 913 chars; exceeds 500-char cap (discovery confirmed) | FR-08 addresses it; verified by AC-10 |

---

## 8. Acceptance Criteria

Sprint ceiling: 7-WI, single-iteration. No new items. No mid-sprint replan.
### Mandatory artifact list

| WI | Artifact | Must exist at Done |
|----|----------|--------------------|
| W1-1 | `delivery-flow/SKILL.md` with `## Volatile` marker; volatile content after marker | Yes |
| W1-1 | ADR file in `delivery-flow/references/` (e.g. `adr-cache-prefix-freeze.md`) | Yes |
| W1-2 | `delivery-flow/references/stages.yml` (7 entries) + companion JSON schema | Yes |
| W1-3 | 5 SKILL.md files updated with `model: haiku` routing agents | Yes |
| W1-3 | `audit_agent_prompt.py` extended with routing-tier mismatch warn | Yes |
| W1-4 | All 13 `delivery-team/**/SKILL.md` with `allowed-tools:` frontmatter | Yes |
| W1-4 | `.claude-plugin/marketplace.json` delivery-team description ≤ 500 chars | Yes |
| W1-5 | `delivery-flow/SKILL.md` adversarial-review section enforcing challenger.model == primary.model | Yes |
| W1-5 | `audit_agent_prompt.py` extended with challenger.model == primary.model warn | Yes |
| W1-6 | `delivery-flow/SKILL.md` frontmatter with `model: sonnet` | Yes |
| W1-6 | Audit log confirming 0 LLM calls in all 7 hooks/*.py | Yes |
| W1-7 | `alias-creator/SKILL.md` ≤ 200 lines | Yes |
| W1-7 | `governance/skill-budgets.json` — alias-creator known-debt entry removed | Yes |

### Runnable ACs by WI

**W1-1**
```bash
grep -n '## Volatile' delivery-team/skills/delivery-flow/SKILL.md          # MUST: ≥1 match
find delivery-team/skills/delivery-flow/references -name 'adr-cache*' | wc -l  # MUST: ≥1
```

**W1-2**
```bash
python3 -c "import json,yaml,jsonschema; schema=json.load(open('delivery-team/skills/delivery-flow/references/stages-schema.json')); data=yaml.safe_load(open('delivery-team/skills/delivery-flow/references/stages.yml')); jsonschema.validate(data,schema); assert len(data.get('stages',[]))==7; print('PASS')"
# MUST: print PASS
python3 -c "import json; rows=[json.loads(l) for l in open('.delivery/telemetry/skill-loads.jsonl')]; b=[r for r in rows if r.get('tag')=='pre-w1-2']; a=[r for r in rows if r.get('tag')=='post-w1-2']; drop=b[-1]['input_tokens']-a[-1]['input_tokens']; assert drop>=2000,drop; print(f'PASS drop={drop}')"
# MUST: print PASS
```

**W1-3**
```bash
for f in delivery-team/skills/product-delivery/SKILL.md delivery-team/skills/architect/SKILL.md delivery-team/skills/quality/SKILL.md delivery-team/skills/operations/SKILL.md delivery-team/skills/ui/SKILL.md; do grep -n 'model: haiku' "$f" || echo "MISSING $f"; done
# MUST: every file shows ≥1 match; MUST: no MISSING lines
grep -n 'routing\|haiku\|tier.mismatch' delivery-team/hooks/audit_agent_prompt.py  # MUST: ≥1 match
```

**W1-4**
```bash
find delivery-team -name 'SKILL.md' -exec grep -qL 'allowed-tools' {} \; -print  # MUST: no output
python3 -c "import json; d=json.load(open('.claude-plugin/marketplace.json')); bad=[(p.get('name'),len(p.get('description',''))) for p in d['plugins'] if len(p.get('description',''))>500]; assert not bad,bad; print('PASS')"
# MUST: print PASS
```

**W1-5**
```bash
grep -n 'challenger.*model\|inherit.*model' delivery-team/skills/delivery-flow/SKILL.md  # MUST: ≥1 match
grep -n 'challenger.*model\|primary.*model' delivery-team/hooks/audit_agent_prompt.py    # MUST: ≥1 match
grep -rn 'extended.thinking' delivery-team/skills/delivery-flow/SKILL.md                 # MUST: default OFF shown
```

**W1-6**
```bash
grep -n '^model:' delivery-team/skills/delivery-flow/SKILL.md | head -1  # MUST: "model: sonnet"
grep -rE 'anthropic|openai|litellm' delivery-team/hooks/                 # MUST: no matches
```

**W1-7**
```bash
wc -l delivery-team/skills/alias-creator/SKILL.md                  # MUST: ≤ 200
python3 scripts/check_skill_budgets.py                              # MUST: exit 0; no alias-creator warning
grep -n 'alias-creator' governance/skill-budgets.json               # MUST: no known_debt entry
```

---

## 9. Open Questions

**None.** Binding decisions resolved in `.delivery/memory/topics/skill-token-economy.md`.

## 10. Verification Plan (dogfood — Stage 6 Dev MUST produce per WI)

| WI | Required dogfood evidence (MUST appear in PR body or linked gist) |
|----|-------------------------------------------------------------------|
| W1-1 | Telemetry row showing cache_read/input ≥ 0.85 on second delivery-flow invocation post-merge |
| W1-2 | Pipeline dogfood: all 7 stages route correctly; telemetry diff showing ≥2,000 token drop |
| W1-3 | 10-sample dispatch log showing routing decisions under `model: haiku`; 10/10 correct role selections |
| W1-4 | `find delivery-team -name SKILL.md -exec grep -L allowed-tools {} \;` empty; all descriptions ≤ 500 (paste output) |
| W1-5 | Adversarial round output excerpt: ≥1 substantive critique produced; `grep challenger audit_agent_prompt.py` shows enforcement |
| W1-6 | End-to-end pipeline run on Sonnet default; telemetry diff ≥3× cost reduction vs Opus baseline; grep hooks/ clean |
| W1-7 | `wc -l alias-creator/SKILL.md` ≤ 200 (paste); `check_skill_budgets.py` exit 0 without alias-creator warning |

**Pre-rollout gate** (FR-15 — MUST run before W1-3/W1-4/W1-5/W1-6 mass edits):
```bash
find delivery-team -name 'SKILL.md' | xargs wc -l | sort -rn
# Record as pre-rollout baseline; attach to PR; re-run post-edit and diff
```
