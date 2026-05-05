---
title: "Skill Token-Economy — Wave 0 Foundations"
scope: delivery-team plugin only
wave: 0
work_items: [W0-1, W0-2]
status: Draft
author: Product Owner (product-delivery skill)
created: 2026-05-03
version: 1.0
---

# Idea Brief: Skill Token-Economy — Wave 0 Foundations

## 1. Initiative Title and Scope

**Title**: Skill Token-Economy Wave 0 — Telemetry Hook + Line-Budget CI Gate (delivery-team)

**Scope**: Wave 0 only. Two work items:

| ID | Title | Effort | Risk |
|----|-------|--------|------|
| W0-1 | Skill-load telemetry hook | S | Low |
| W0-2 | Tiered SKILL.md line-budget CI gate | S | Low |

Out of scope for this run: Wave 1 through Wave 3 items, all non-delivery-team plugins.

---

## 2. Problem Statement

The delivery-team plugin is the largest in the repo. Six delivery-team SKILL.md files currently exceed their tier line budgets:

| Skill | Current lines | Tier | Budget | Overage |
|-------|--------------|------|--------|---------|
| delivery-flow | 1,089 | A | 500 | +589 |
| product-delivery | 688 | B | 300 | +388 |
| architect | 670 | B | 300 | +370 |
| presentation | 543 | B | 300 | +243 |
| ui | 493 | B | 300 | +193 |
| developer | 493 | B | 300 | +193 |

Source: `.delivery/artifacts/research/skill-token-audit-experts.md` (Repo Ground Truth, 2026-05-03)

Every skill invocation loads the full SKILL.md into the model context. Overages translate directly to excess input tokens and reduced cache hit ratios. Without measurement infrastructure (W0-1) and a budget enforcement gate (W0-2), reduction efforts from Wave 1+ have no feedback loop and gains regress. The governance expert finding: "without telemetry (W0-1) and budgets (W0-2), the gains regress within 6 months."

---

## 3. Goal

Establish the two non-negotiable foundations that make every subsequent Wave executable:

1. **W0-1** — A `PreToolUse` telemetry hook that writes one JSONL row per skill invocation to `.delivery/telemetry/skill-loads.jsonl`, capturing `{skill, model, prefix_hash, input_tokens, cache_read_tokens, cache_write_tokens}`. This is the measurement layer every Wave 1+ optimization references.

2. **W0-2** — A GitHub Actions CI gate that fails any PR where a delivery-team SKILL.md exceeds its declared tier budget (Tier-A ≤500 / Tier-B ≤300 / Tier-C ≤200). This is the regression guard that holds gains once Waves 1–3 land.

Without these two items, token savings cannot be measured, known-debt cannot be tracked, and budget violations cannot be blocked at merge time.

---

## 4. Stakeholders

| Stakeholder | Role | Interest |
|-------------|------|----------|
| User (michaelconne@gmail.com) | Decision authority | Plugin quality + cost reduction |
| delivery-team plugin contributors | Producers | Correct hook behavior; CI gates must not false-positive |
| Wave 1+ executors (downstream team) | Consumers | Need telemetry data + budget gate before executing W1-W3 items |
| Claude Code runtime | Platform | Hook must not exceed 50ms overhead per call |

---

## 5. High-Level Scope

### In Scope (Wave 0 only)

- **W0-1**: New file `delivery-team/hooks/telemetry.py`; update `delivery-team/hooks/hooks.json` to register `PreToolUse` Skill matcher; new `delivery-team/references/telemetry-schema.md` documenting the JSONL schema (v1).
- **W0-2**: New file `.github/workflows/skill-line-budget.yml`; new `scripts/check_skill_budgets.py`; add `tier:` frontmatter to all 11 delivery-team SKILL.md files; log current over-budget skills as known-debt with target wave.

### Out of Scope

- Wave 1 items (W1-1 through W1-6)
- Wave 2 items (W2-1 through W2-6)
- Wave 3 items (W3-1 through W3-3)
- Any plugin other than delivery-team (mtg-commander, hardware-team, agentic-flow-builder, prd-quality-gate-flow, research-agent, prompt-engineer)

---

## 6. Success Criteria

All criteria MUST be verified via dogfood before marking Wave 0 Done.

### W0-1 Telemetry Hook

| # | Criterion | Verification command |
|---|-----------|---------------------|
| SC-1 | Hook fires on every Skill PreToolUse and writes exactly one JSONL row | `tail -f .delivery/telemetry/skill-loads.jsonl` during a live skill invocation — row MUST appear |
| SC-2 | JSONL row contains all required fields: `skill`, `model`, `prefix_hash`, `input_tokens`, `cache_read_tokens`, `cache_write_tokens` | `python -c "import json,sys; [json.loads(l) for l in open('.delivery/telemetry/skill-loads.jsonl')]"` — MUST parse without KeyError |
| SC-3 | Schema documented as v1 in `delivery-team/references/telemetry-schema.md` | `grep 'version: 1' delivery-team/references/telemetry-schema.md` — MUST match |
| SC-4 | Sample 5-run report script renders mean tokens/run per skill | `python delivery-team/hooks/telemetry_report.py` — MUST produce non-empty table |
| SC-5 | Hook adds <50ms overhead per call | Time 10 invocations; verify mean latency delta <50ms |

### W0-2 Line-Budget CI Gate

| # | Criterion | Verification command |
|---|-----------|---------------------|
| SC-6 | Every delivery-team SKILL.md has `tier: A`, `tier: B`, or `tier: C` frontmatter | `grep -rn "^tier:" delivery-team/**/SKILL.md` — MUST return 11 matches |
| SC-7 | CI fails on a synthetic over-budget PR | Create a test branch where one SKILL.md line count exceeds tier budget; push PR; CI MUST fail with budget violation in workflow log |
| SC-8 | Current over-budget skills logged as known-debt with target wave | `grep 'known-debt' .github/workflows/skill-line-budget.yml` or script output — 6 skills MUST appear with target wave label |
| SC-9 | Permissive-language warn-only sub-check included | `python scripts/check_skill_budgets.py --warn-permissive delivery-team/skills/delivery-flow/SKILL.md` — MUST run without error; warnings may appear; MUST NOT fail |

---

## 7. Constraints

| Constraint | Source | Impact |
|------------|--------|--------|
| Pure-Python hooks — NO LLM calls inside hooks | Binding decision (memory topic, Hooks Discipline) | `telemetry.py` MUST be standalone Python; no Anthropic SDK import |
| LOTR theme applies to all delivery-team output | `.delivery/config.yml` (LOTR theme config) | Narrative framing (stage banners, logs) may use thematic language; functional code does not |
| March-to-war mode — no human checkpoints within Wave 0 | Pipeline config | Team MUST execute W0-1 and W0-2 to completion without pausing for approval between them |
| Anthropic 500-line ceiling anchor | `.delivery/artifacts/research/skill-token-audit-experts.md` (C1, Expert 4) | Tier-A budget of 500 lines is the ceiling, not a target; newly authored SKILL.md content MUST stay well below it |
| Mission-critical risk tolerance | `.delivery/config.yml` | Over-budget SKILL.md files are logged as known-debt, NOT auto-fixed in Wave 0. Wave 0 MUST NOT touch SKILL.md content beyond adding `tier:` frontmatter |
| Telemetry overhead ceiling | Binding decision (W0-1 AC) | Hook MUST add <50ms per call — verified by timing measurement |
| CI gate MUST allow known-debt exceptions | Binding decision (Ruling 3) | `Budget-Exception: <ADR-link>` in PR body MUST bypass the fail; current over-budget skills are pre-registered known-debt, not exceptions requiring ADRs yet |
| Plugin-dev skill routing is mandatory | CLAUDE.md "Key Conventions"; `.delivery/memory/topics/claude-plugins-repo.md` | W0-1 (telemetry hook) MUST be implemented via `plugin-dev:hook-development`; W0-2 (CI gate + `tier:` frontmatter changes) MUST be implemented via `plugin-dev:plugin-structure` and `plugin-dev:skill-development`; both MUST be reviewed via `plugin-dev:skill-reviewer` and validated via `plugin-dev:plugin-validator` before merge |

---

## 8. Open Questions for Downstream Stages

None. All binding decisions are resolved in `.delivery/memory/topics/skill-token-economy.md`. The following are pre-loaded for downstream Plan agents to avoid re-derivation:

**Pre-loaded constraints for Plan stage:**

- Tier budgets: Tier-A ≤500 lines / Tier-B ≤300 lines / Tier-C ≤200 lines
- Telemetry JSONL schema fields (v1): `skill` (string), `model` (string), `prefix_hash` (sha256 hex, first 8 chars of SKILL.md), `input_tokens` (int), `cache_read_tokens` (int), `cache_write_tokens` (int), `timestamp` (ISO 8601), `session_id` (string)
- CI gate enforcement mechanism: GitHub Actions workflow + `scripts/check_skill_budgets.py` reading `tier:` frontmatter from each SKILL.md; exit code 1 on budget violation unless `Budget-Exception:` present in PR body
- Hook registration: `hooks.json` matcher type `PreToolUse`, tool pattern `Skill`; hook fires BEFORE skill loads (captures what was requested, not what ran)
- Known-debt logging: the 6 over-budget skills MUST be logged in the CI script output with format `KNOWN-DEBT: <skill>/<SKILL.md> <current>/<budget> lines — target wave: W<N>`
- Permissive-language check: warn-only (not fail); regex `\bshould\b|\bcan\b|\bmay\b|\bmight\b` outside fenced code blocks

---

## 9. References

| Artifact | Path |
|----------|------|
| Master backlog (all 4 waves, 16 items) | `.delivery/backlog/BACKLOG-100-skill-token-economy-delivery-team.md` |
| 6-expert audit with repo baseline metrics | `.delivery/artifacts/research/skill-token-audit-experts.md` |
| Binding conflict rulings + per-skill model map | `.delivery/memory/topics/skill-token-economy.md` |
