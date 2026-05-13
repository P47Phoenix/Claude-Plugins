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

## Pre-Initiative History

Documented backfill of changes before the skill-token-economy initiative (pre-2026-05-03). Reconstructed from `git log` and tag history; entries grouped by version-tag anchors where available, otherwise by feature theme. Earlier history (pre-v2.22) is in `git log` and not enumerated here.

The repository was first scaffolded 2025-11-15 (commit `ecc3452`). The pre-initiative span covers 152 commits across roughly six months, anchored by 23 marketplace version tags from `v2.8.0` (2026-03-26) through `v2.24.0` (2026-05-05). Tag dates are commit-date UTC.

### v2.24.0 — 2026-05-05 — Opus 4.7 migration

**Changed**
- Opus 4.7 migration run-2026-04-22-4x7e completed (PR #86, merge `aa5c2cd`): four migration waves (`1170c4f`, `e1b80c1`, `0d489a2`, `57a09e7`) covering baseline + spike, keystone annotations, audits + adversarial dogfood, and final sweeps with CI + backlog updates.
- Post-pipeline housekeeping: memory rebuild (`8ca5684`), hardware-team frontmatter stamps (`dd82907`), state-archive cleanup, and scaffolding pruning with binding-decision preservation (`1923e9f`).

### v2.23.0 — 2026-04-18

**Added**
- `hardware-team/` plugin with 8-stage hardware delivery pipeline (`ff3ac93`) — 7 roles (PO, EE, PCB Layout, Manufacturing, Compliance, Test), 5 gates, 11 kicad-happy integrations, 6 hooks across 3 event types.

### v2.22.0 → v2.22.2 — 2026-04-11 to 2026-04-15

**Added**
- mtg-commander adversarial Challenger agents, configurable loops, price goal escalation (`b63ebc5`, v2.22.0).
- Per-plugin `ARCHITECTURE.md` with Mermaid diagrams across 6 plugins / 14 diagrams (`0080722`); detailed delivery-team flow documents — 6 flows, 12 diagrams (`52f0671`).

**Fixed**
- Defect sweep DEFECT-003 (wizard/migration), `--skip-declarations` flag, CI injection regression guard (`3aee2f9`).
- DEFECT-005: Mermaid diagram syntax errors — `\n` literals in labels and `classDiagram` type keywords (`f2ca2c7`).

**Changed**
- Documentation harmonization across repo: mtg-commander discoverability, constraints quickstart, troubleshooting (`f67e8b6`); user-facing docs caught up through `g8h5` defect sweep (`e0dab2d`).

### v2.20.0 → v2.21.0 — 2026-04-09 to 2026-04-11

**Added**
- architect Transformation Planning sub-workflow: AS-IS behavioral/structural → TO-BE → Roadmap, paired PO + Architect with Architecture Board review (`ed8b5f0`, v2.20.0).

**Changed**
- architect paradigm-as-skill restructure with router and context isolation (BACKLOG-005, `fe6e214`, v2.21.0) — paradigm sub-skills moved under `skills/paradigms/` so only the selected paradigm loads.

### v2.19.1 — 2026-04-09 — Orchestration discipline bundle

**Added**
- delivery-flow configurable Architecture Board review pattern (BACKLOG-003, `dc34e9d`): multi-persona review with MAR iteration-2 cross-persona routing.
- delivery-flow paired constraints primitive: model-first schema + decomposition guidance depth (`165b44f`).
- delivery-flow `DESIGN` project type for design-only sessions (#72, #75, `4b507a2`).
- delivery-flow orchestration discipline bundle — config schema v2.7 (#69-#74, `9f991ee`).

**Fixed**
- CI command injection in version bump workflow (DEFECT-004, `f3fea27`) — regression guarded by `workflow-injection-lint.yml`.

### v2.16.0 → v2.17.2 — 2026-04-04 to 2026-04-06

**Added**
- presentation skill v1.1 enhancements: 5 new types, PPTX output, narrative intelligence, light mode (#43-#46, `1747b86`, v2.16.0).
- delivery-flow theme-gated reporting protocol for orchestrator chat output (#59, `828119d`, v2.17.0).
- MkDocs Material documentation site with 25 pages (#48, `185d802`).

**Fixed**
- Multiple delivery-flow patch fixes: duplicated stage definitions, artifact paths, DoD template (#60-#62, `c6f10fb`); stale hook migration and post-install wizard validation (#67-#68, `20f4aea`); `sys.exit` → exceptions in `generate_pptx.py`, map-type schema parsing (#65-#66, `35ffd58`).

### v2.13.0 → v2.15.2 — 2026-04-02 to 2026-04-04 — mtg-commander era

**Added**
- `mtg-commander/` plugin with multi-agent pipeline (`d80702f`, v2.14.0): synergy-first 100-card Commander deck builder with Scryfall integration. Card Kingdom pricing via Archidekt API followed (`f012b7d`, v2.15.0).
- Cross-skill shared references convention and CI validation (#47, `d098fff`, v2.13.0).

**Fixed**
- mtg-commander follow-ups: `validate-deck` command for color identity violations (#56, `c4df423`); TCGPlayer pricing source disclaimer (#57, `8008586`); architect Prior Art Analysis step to respect user-provided specs (#55, `4f27f76`); Agent Invocation Templates with alias injection (#58, `80d1cc8`).

### v2.8.0 → v2.12.1 — 2026-03-26 to 2026-04-02 — presentation, deterministic rules engine, clean code

**Added**
- presentation skill with team-collaborative 6-step flow (`3d2270d`, v2.8.0).
- Deterministic rules engine for delivery-flow pipeline (`834b532`, v2.11.0) — rule-based gate decisions for auditable, consistent outcomes.
- Stage health hardening across Design, Plan, UAT, and Dev gates (`268fb83`, v2.12.0).
- Clean code foundational standards for developer and godot skills (`3d28694`), with delivery-artifact extensions (`6b16350`).

**Changed**
- `PRDFlowBuilder` god object decomposed and entry points consolidated (`402f21e`).
- delivery-flow branch strategy, confidence cap, and refactoring routing enforced (`94ccccc`).
- Config bumped to v2.2 with presentation keys (`30b666b`).

**Fixed**
- Pipeline stall bug #49: delivery artifacts and retrospective handling (`7eee3c7`); anti-stall directives in orchestrator (`5ff09f6`); alias theme loading wired into orchestrator (`5816d4f`).

### Pre-v2.8.0 Foundation — 2025-11-15 to 2026-03-26

The repository's first ~3 months built the marketplace and the bulk of the delivery-team plugin. Highlights from `git log --reverse`:

**Added — plugins**
- Initial marketplace scaffold (`ecc3452`, 2025-11-15).
- `agentic-flow-builder/` — ReAcTree hierarchical workflow system (`361ec7c`).
- `prompt-engineer/` skill (`c839fcb`); `prd-quality-gate-flow/` PRD workflow with 7 gates and SQLite persistence (`f6264ed`); `research-agent/` with academic methodology (`414a42a`).
- `delivery-team/` plugin evolved from `product-owner-agent` (`15cf62a` → rename `b2b03d7` → skills-subfolder restructure `f7539b0`, `fc0aa13`).

**Added — delivery-team skills**
- developer skill with language context isolation (`2a256c5`); later expanded with Nx monorepo, FP patterns, and 4 functional languages (`c3ce548`).
- godot skill + R + OOP patterns (`b5ecf33`); Godot validation hooks (`c71d630`); defect prevention checklist (`44a859f`).
- delivery-team expanded to 7 skills covering full lifecycle: architect, operations, product-delivery, quality, ui (`3630bc2`).
- delivery-flow pipeline orchestrator with team collaboration patterns (`d8ed71f`); setup wizard with state detection (`8e4b6f9`); tiered chunked memory (`ece5a4e`).
- user-feedback skill with simulated persona-based testing (`30217bd`).
- Architecture decomposition strategies with config-driven selection (`7a40242`); Lowy IDesign volatility rewrite (`8ce9dea`); Evans/Fowler strategic DDD rewrite (`c3a3dd3`).

**Added — process infrastructure**
- Empirical validation detection across delivery pipeline (`2b33cae`, closes #1).
- Defect tracking with self-improvement feedback loop and issue/PR templates (`c51b893`, `c05aad6`).
- 3-layer pipeline-bypass enforcement (`13ae5f4`, fixes #6, #7); setup-config enforcement hook (`305afc0`, fixes #10).
- Exploratory testing, enforced retrospectives, Scrum Bag rename (`14fe710`); milestone playtesting protocols (`d8412d8`, `dc7e9ef`).
- Config schema reference with versioning + extension protocol (`6066851`).

**Fixed**
- hooks.json format and hook output corrected per Claude Code hooks API (`b4c66ec`); setup wizard not triggering when config missing (`1faaac9`); mouse_filter bug pattern + QA heuristics (`9c3b1cc`).

**Removed**
- `skill-creator/` and `plugin-creator/` plugins superseded by `plugin-dev` and removed (`106d6a1`).

_Coverage note: alias-creator and several smaller skill additions landed in this window but their introducing commits were not individually isolated from message lines alone. See `git log --reverse v2.8.0` for the complete sequence._
