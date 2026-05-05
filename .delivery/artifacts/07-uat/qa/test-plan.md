---
title: "Wave 1 UAT Test Plan"
stage: 07-uat
author: Legolas (quality skill)
created: 2026-05-03
version: 1.0
stories: [story-1-delivery-flow-restructure, story-2-frontmatter-rollout, story-3-challenger-hook]
---

# Wave 1 UAT Test Plan

## Scope

Contributor-perspective acceptance of 3 Wave 1 stories:
- Story 1 — delivery-flow/SKILL.md restructure (cache-prefix freeze, stages.yml, frontmatter)
- Story 2 — frontmatter rollout (allowed-tools, phase_1_detector_model, alias-creator trim)
- Story 3 — challenger-tier model inheritance hook (warn-only)

Stage 6 dogfood covers unit/integration. UAT answers: **"would the next BACKLOG item ship cleanly?"**

## Pre-conditions

- Clean git tree (`git status` is empty).
- All 3 story branches merged to main.
- Files exist: `governance/cache-prefix-hash.txt`, `references/stages.yml`,
  `references/stages-schema.json`, `delivery-team/hooks/audit_agent_prompt.py`.
- Python 3.8+ stdlib-only environment available.
- `scripts/check_skill_budgets.py` and `governance/skill-budgets.json` present.

## Acceptance Scenarios

### Scenario 1 — delivery-flow loads as a skill
**Question**: Does delivery-flow/SKILL.md remain structurally intact after Story 1 edits?

- Verify file is 999 lines (post-restructure).
- Verify frontmatter contains `model: sonnet` and `extended_thinking: false`.
- Verify 5 Phase sections present (`grep -c "^## Phase" → 5`).
- Verify `## Volatile` marker appears exactly once.
- **Pass**: all 4 checks exit 0 / return expected values.

### Scenario 2 — stages.yml drives stage routing
**Question**: Can a Wave 2 executor rely on stages.yml as structured routing data?

- Verify `references/stages.yml` size > 100 bytes.
- Verify `references/stages-schema.json` parses as valid JSON (stdlib `json.load`).
- Verify stages-schema.json contains `"$schema"` key (JSON Schema identity present).
- **Pass**: size check passes; JSON parses; schema key present. (PyYAML structural
  validation deferred to Wave 2 per known limitation — file presence + schema pass
  is the Wave 1 gate.)

### Scenario 3 — CI budget gate passes after alias-creator trim
**Question**: Does `check_skill_budgets.py` exit 0 without alias-creator in known-debt?

- Run `python3 scripts/check_skill_budgets.py`.
- Verify: exit code 0.
- Verify: `alias-creator` does NOT appear in output.
- Verify: `governance/skill-budgets.json` has no `alias-creator` entry.
- **Pass**: exit 0; alias-creator absent from both output and JSON registry.

### Scenario 4 — allowed-tools whitelist declared in Tier-A + role multiplexers
**Question**: Do all 12 non-delivery-flow SKILL.md files carry `allowed-tools:` frontmatter?

- `grep -rl "^allowed-tools:" delivery-team/skills/ | wc -l` (excluding delivery-flow).
- Verify count ≥ 12.
- Verify at least one Phase-1-router file (e.g. quality/SKILL.md) also contains
  `phase_1_detector_model: haiku`.
- **Pass**: ≥ 12 files with allowed-tools; ≥ 1 router file with haiku declaration.

### Scenario 5 — Challenger hook fires warn-only on adversarial mismatch
**Question**: Does the hook emit a `[CHALLENGER-TIER-WARN]` to stderr and exit 0?

- Pipe a synthetic adversarial prompt with mismatched primary/challenger models into
  `audit_agent_prompt.py`.
- Verify: exit code 0 (no block).
- Verify: stderr contains `[CHALLENGER-TIER-WARN]`.
- Verify: hook contains no LLM calls
  (`grep -E "anthropic|openai|litellm" audit_agent_prompt.py` returns empty).
- **Pass**: exit 0; warning on stderr; no LLM imports.

### Scenario 6 — Cache-prefix hash is byte-stable across 2 reads
**Question**: Is sha256(bytes 0..2048) of SKILL.md reproducible and matches the frozen hash?

- Read `governance/cache-prefix-hash.txt` → capture stored hash.
- Recompute: `python3 -c "import hashlib,pathlib; print(hashlib.sha256(
  pathlib.Path('delivery-team/skills/delivery-flow/SKILL.md').read_bytes()[:2048]).hexdigest())"`.
- Verify: live hash == stored hash (exact string match).
- **Pass**: hashes match on both reads; no drift.

## Pass Criteria

All 6 scenarios green. A scenario is green when every Verify bullet is satisfied
without manual workarounds.

## Out of Scope

- BACKLOG-102 (caveman refactor), Wave 2+, paradigm sub-skill resolution.
- Non-delivery-team plugins (hardware-team, mtg-commander, etc.).
- End-to-end pipeline timing or throughput benchmarks.
- PyYAML structural validation of stages.yml (Wave 2 CI addition).
