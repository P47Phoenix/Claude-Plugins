# Changelog

All notable changes to this repository are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

_No unreleased changes at this time._

## Initiative — Skill Token-Economy (delivery-team plugin)

This initiative landed across 5 waves from 2026-05-03 to 2026-05-09. All 5 binding rulings established at audit close are preserved through the full sequence.

### Wave 3 — 2026-05-09 (BACKLOG-104, commit 2609272)

**Added**
- Governance frontmatter (`maintainer` / `fitness_review_due` / `context_budget`) on all 11 top-level delivery-team SKILL.md.
- 9 paradigm sub-skills (research-agent x5 research types + user-feedback x4 persona families) per ADR-tk4-002.
- `governance/fitness-review.md` + `.github/workflows/fitness-review.yml` (monthly cron, quarterly cadence).
- `scripts/lint_known_debt.py` + `.github/workflows/lint-known-debt.yml` (W3-14).
- `scripts/extract_dod_status.py` (W3-15).
- `scripts/sweep_stale_artifacts.py` (W3-17 Stage-7 stale-sweep).
- `.githooks/pre-commit` (W3-16 local budget check).
- `delivery-team/skills/delivery-flow/references/validator-prompt-template.md` (W3-13).
- W3-18 telemetry hardening + `.delivery/telemetry/stop-rule-tk4.txt`.
- `context_tokens_per_pipeline_run` KPI in retrospective template (W3-10).

**Changed**
- `architect/SKILL.md` 500 -> 291 lines (description 1732 -> 496 chars; Ruling 2 compliance).
- `presentation/SKILL.md` 545 -> 182 lines.
- `ui/SKILL.md` 496 -> 219 lines.
- `operations/SKILL.md` 420 -> 216 lines.
- `quality/SKILL.md` 418 -> 286 lines.
- `user-feedback/SKILL.md` 399 -> 269 lines.
- `godot/SKILL.md` 236 -> 197 lines (Tier-C; +3 frontmatter -> 200 exact).
- `CLAUDE.md` 168 -> 110 lines (now 112 post-frontmatter additions).
- `governance/cache-prefix-hash.txt` regenerated (`f997` -> `4306`).
- `governance/skill-budgets.json` `known_debt` re-baselined empty.

**Fixed**
- DEFECT-006 (caveman-lite tk3 stale-artifact carry-over): closed via W3-17 Stage-7 stale-sweep.

### Wave caveman-lite — 2026-05-05 (BACKLOG-102, commit baa49b9)

**Added**
- `prose_style` top-level config key (default `caveman-lite`, opt-out `standard`).
- `delivery-team/skills/delivery-flow/references/prose-style.md` (canonical directive).
- PROSE STYLE block injection in 3 dispatch templates per ADR-tk3-001.
- DoD validator verdict-prose treatment.
- config-schema v2.8 -> v2.9 + migration entry.
- ADR-tk3-001 documenting cache-prefix re-freeze procedure.

**Changed**
- `delivery-flow/SKILL.md` Phase 0 +1 / Step 4 +2 lines (held 500/500 ceiling via mid-implementation extraction).
- `governance/cache-prefix-hash.txt` regenerated (`9d40` -> `f997`).

**Known**
- AC-13 telemetry close-out deferred to Wave 3's first dispatches (chicken-and-egg with W3-18 telemetry hardening).

### Wave 2 — 2026-05-05 (commit c2e7d5a)

**Added**
- Orchestrator doctrine extraction: `delivery-team/skills/delivery-flow/references/orchestrator-doctrine.md`.
- Architect output contracts split into `architect/references/contracts/`.
- Developer coding-standards reference extracted.
- product-delivery 12 patterns split into `product-delivery/references/patterns/`.

**Changed**
- `delivery-flow/SKILL.md` 1090 -> 497 lines.
- Cache-prefix re-frozen and governance registry synced.
- Wave 1 retrospective carry-forward items backported.

### Wave 1 — 2026-05-04 (BACKLOG-101, commit b412a40)

**Added**
- Cache-prefix freeze + `governance/cache-prefix-hash.txt` + governance registry.
- Skill frontmatter rollout (`allowed-tools`, `model: haiku` for routing skills).
- Challenger hook (`audit_agent_prompt.py` compound-role audit).
- Stage YAML manifest (`delivery-flow/references/stages.yml`).

**Changed**
- `alias-creator/SKILL.md` trimmed (-2 lines, graduated from `known_debt`).
- Multiple SKILL.md frontmatter additions per Wave 1 scope.

### Wave 0 — 2026-05-03 (BACKLOG-100, commit d0e0928, PR #87)

**Added**
- Telemetry hook (`.delivery/telemetry/skill-loads.jsonl`) - PreToolUse Skill matcher.
- Line-budget CI gate (`scripts/check_skill_budgets.py` + `.github/workflows/skill-line-budget.yml`).
- Tier frontmatter (A / B / C) on 13 SKILL.md.
- `governance/skill-budgets.json` `known_debt` mechanism.

### Initiative Outcomes

- 5 of 5 waves SHIPPED 2026-05-09; INITIATIVE COMPLETE.
- Cumulative structural reduction: 5807 -> 3090 lines across all SKILL.md (46.79%).
- All 5 binding rulings preserved through 5 invocations.
- Cumulative defects: 2 (DEFECT-006 closed at Wave 3; DEFECT-007 = this CHANGELOG gap, closed at the same commit).
- Defects/story 3-PR rolling: 0.111 (well under the 0.4 stop-rule).

## Prior history

Pre-initiative changes are not enumerated here. See `git log` for the full record prior to 2026-05-03; recent marketplace versions are tagged from `v2.17.2` through `v2.27.0`.
