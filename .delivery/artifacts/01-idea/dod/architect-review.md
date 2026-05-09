<!-- run: run-2026-05-09-tk4 | stage: 1 (Idea, LIGHT) | dod-round: 1 | reviewer: solution-architect (FRESH dispatch) -->

# Architect DoD Review — Wave 3 Idea-Brief (run-2026-05-09-tk4)

**Reviewer**: Solution Architect (DoD validator, Stage 1 round 1, FRESH dispatch)
**Date**: 2026-05-09
**Pipeline**: run-2026-05-09-tk4
**Artifact**: `.delivery/artifacts/01-idea/po/idea-brief.md`
**Mode**: light (round 1)

## STATUS: DONE

## Findings

- **Criterion 1 — Brief acknowledges this work modifies SKILL files → Stage 6 Dev MUST load `plugin-dev:skill-development`: PASS.** §4 lines 42-43 binding-conventions block explicitly names `plugin-dev:skill-development` MUST be acknowledged at the developer dispatch, plus `plugin-dev:skill-reviewer` post-completion and `plugin-dev:plugin-validator` before PR. §6 Stage 6 routing row repeats: "`plugin-dev:skill-development` acknowledged". Memory lesson honored.

- **Criterion 2 — Ruling 1 cache-prefix invariant acknowledged; any SKILL.md Phase 0 edit identified: PASS.** §5 is a dedicated Cache-Prefix Invariant section. It identifies W3-9 governance frontmatter rollout as the Phase-0-touching surface ("MAY touch Phase 0"), assigns ownership to `ADR-tk4-001` for cumulative re-freeze, mandates `governance/cache-prefix-hash.txt` update at end of Story 5 (one-time, not per-story), and references the caveman-lite Hot Lesson #1 extension on Dev runs-the-command discipline at Architect DoD. Cross-reference confirmed against binding-decisions Ruling 1 (`topics/skill-token-economy.md:10-14`).

- **Criterion 3 — All 7 over-budget surfaces accurately identified per `governance/skill-budgets.json`: PASS.** Cross-checked the brief's §7 Story table against the known_debt array:

  | Known-debt entry | Story assignment | Match |
  |---|---|---|
  | architect/SKILL.md (B, 500) | Story 1 (W3-1) | OK |
  | presentation/SKILL.md (B, 545) | Story 2 (W3-2..4) | OK |
  | ui/SKILL.md (B, 496) | Story 2 (W3-2..4) | OK |
  | operations/SKILL.md (B, 420) | Story 2 (W3-2..4) | OK |
  | quality/SKILL.md (B, 418) | Story 3 (W3-5..7) | OK |
  | user-feedback/SKILL.md (B, 399) | Story 3 (W3-5..7) | OK |
  | godot/SKILL.md (C, 236) | Story 3 (W3-5..7) | OK |

  All 7 entries mapped 1:1, no misses, no extras. AC §8.1 cites the exact close criterion (`scripts/check_skill_budgets.py` exits 0 with empty `known_debt` array). §3 Goal sentence reproduces the count ("ALL 7 remaining over-budget SKILL.md files"). BACKLOG-104 known-debt list matches.

- **Criterion 4 — Stop-rule continuity preserved (defects/story >0.4 across 3-PR window — same threshold): PASS.** §9 line 99 reproduces the canonical threshold verbatim: "defects/story rate >0.4 across any 3-PR window pauses subsequent waves." Matches `topics/skill-token-economy.md:129` and prior-wave continuity. Window arithmetic shown (tk2 = 0 defects, tk3 = 1 P1 non-blocking → 0.33 < 0.4, not triggered, Wave 3 may proceed). PO empowered to halt at any Story boundary if next defect lands. Engagement-local AC-13 telemetry stop-rule (§8 lines 93-95) is additive, not a substitute — orthogonal to prose discipline gating Story 5 only.

- **Criterion 5 — Does not pre-decide ADR-tk4-001/002/003 contracts: PASS.** §6 lines 62 names all three ADRs by ID and intent only:
  - ADR-tk4-001 = cumulative cache-prefix re-freeze (mandatory if Phase 0 touched)
  - ADR-tk4-002 = W3-1 architect partial-compliance ruling (if 200-line residual infeasible)
  - ADR-tk4-003 = W3-8 paradigm sub-skill dispatch shape (highest novelty)
  
  No contract shape, no extraction pattern, no exact frontmatter keys, no paradigm dispatch contract pre-specified. §10 explicitly defers three architectural choices to Stage 4 (W3-1 partial-compliance threshold, W3-8 paradigm dispatch shape per axis, W3-15 STATUS-format standardize-vs-helper). §7 Story 4 sequencing note ("After Story 1 ships ADR-pattern") signals dependency without specifying the pattern. §3 names the W3-9 frontmatter keys (`maintainer:` + `fitness_review_due:` + `context_budget:`) — but these are the BACKLOG-104 acceptance-gate keys carried verbatim from the source brief, NOT new architect decisions. Architect Stage 4 retains contract-shape authority.

## Verdict

The brief consolidates BACKLOG-104 faithfully without re-authoring, honors all five binding rulings (especially the cache-prefix invariant via the dedicated §5 ADR-tk4-001 ownership statement), correctly maps all 7 known-debt surfaces to Stories 1–3, and hands the three open architectural choices to Stage 4 rather than pre-deciding them. No blocking architect-lens concerns; vote DONE on round 1.
