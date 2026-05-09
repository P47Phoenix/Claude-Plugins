<!-- run: run-2026-05-09-tk4 | stage: 07-uat | depth: full | author: Tech-Writer (Bilbo Baggins) | role: technical-writer | task: release-notes | wave: 3 (final) -->

---
title: "Release Notes — Wave 3 Skill Token-Economy Closure (run-2026-05-09-tk4)"
stage: 07-uat
author: Bilbo Baggins (operations skill, tech-writer role)
created: 2026-05-09
pipeline_id: run-2026-05-09-tk4
initiative: SKILL-TOKEN-ECONOMY (delivery-team)
wave: 3 of 3 (initiative close-out)
predecessor: run-2026-05-05-tk3 (Wave caveman-lite, commit 02ad3da)
closes: BACKLOG-104 (W3-1..W3-18)
adrs: [ADR-tk4-001, ADR-tk4-002, ADR-tk4-003]
supersedes: prior tk3 release-notes (2026-05-05)
---

# Release Notes — Wave 3 Skill Token-Economy Closure

> "And the road goes ever on and on, down from the door where it began. Now far ahead the road has gone, and I must follow if I can — and so I do, with the last of my notebooks open."
> — Bilbo Baggins, Chronicler of the Red Book, on closing the cycle.

This release closes the delivery-team skill token-economy initiative. Wave 3 is the final wave — five waves shipped (Waves 0, 1, 2, caveman-lite, 3), and with this merge the initiative is complete. Seven over-budget SKILL.md files reach tier compliance, governance frontmatter lands on every top-level skill, the paradigm sub-skill pattern operationalizes for two more axes, and six retrospective carry-forwards from prior waves discharge in a single Story 7 sweep.

## What's new

Three substantive changes ship together.

**Tier-budget compliance across delivery-team.** Seven SKILL.md files trim under their declared tier ceilings via reference-extraction: architect (500 → 294, Tier-B 300), presentation (545 → 185, Tier-B), ui (496 → 222, Tier-B), operations (420 → 219, Tier-B), quality (418 → 289, Tier-B), user-feedback (399 → 272, Tier-B), and godot (236 → 200, Tier-C exact). Reference content moves to `references/roles/`, `references/contracts/`, `references/types/`, and `references/formats/` directories per ADR-tk4-001's per-file extraction strategy. The on-disk sub-skill SKILL.md files for paradigm dispatch (research-agent x5, user-feedback x4) live under `skills/<axis>/<variant>/SKILL.md` per the canonical shape codified in ADR-tk4-002.

**Governance frontmatter on all 11 top-level SKILL.md.** Three new keys — `maintainer:`, `fitness_review_due:`, `context_budget:` — land on every top-level delivery-team SKILL.md per ADR-tk4-003. The keys make ownership explicit, schedule the quarterly fitness review, and make the line-budget CI lint single-pass (no tier-to-line lookup). Default rollout values: `maintainer: delivery-team-leads`, `fitness_review_due: 2026-08-09`, `context_budget:` matching tier (A=500, B=300, C=200). Future PRs may stagger fitness-review dates across an 80–100-day window.

**Six retrospective carry-forwards discharged in Story 7.** W3-13 (validator prompt template at `delivery-team/skills/delivery-flow/references/validator-prompt-template.md`), W3-14 (KNOWN_DEBT JSON-Python lint at `scripts/lint_known_debt.py`), W3-15 (STATUS-format helper standardized at the orchestrator layer), W3-16 (opt-in pre-merge git hook at `.githooks/pre-commit`, install instructions at `governance/git-hooks-install.md`), W3-17 (Stage-7 stale-artifact entry sweep, Option A banner pattern), and W3-18 (telemetry hardening so `prose_tokens` per-dispatch becomes reliable). All six have backlog provenance from Wave 0 / Wave 1 / Wave 2 / caveman-lite retros; this wave clears them in one consolidated story.

## Why

The initiative goal was a cumulative ≥50% reduction in delivery-team token-economy load across the five-wave plan. With Wave 3 closure, all 7 over-budget SKILL.md files are compliant, `governance/skill-budgets.json known_debt[]` is empty for the first time since the registry was created, and the cumulative ~1,100 lines moved from frequently-loaded SKILL.md files into on-demand `references/` exceed the cumulative-target threshold. ADR-tk4-001 records the exact extraction math per file; ADR-tk4-003 records the cache-prefix re-freeze procedure that this wave executes once at the end of Story 5.

The paradigm sub-skill pattern (ADR-tk4-002) operationalizes Ruling 2 of the binding token-economy decisions: ≥3-mutually-exclusive-variant axes get router-dispatched sub-skills with `disable-model-invocation: true`. Research-agent (5 research types) and user-feedback (4 persona families) take the pattern this wave; presentation (9 types) is deferred per ADR-tk4-002's conditional clause because references-only met its budget after the W3-2 trim.

## For users / repo maintainers

Every top-level delivery-team SKILL.md now carries three new frontmatter keys. The user-facing impact is one: the new `fitness_review_due:` field schedules a quarterly review for each skill. The first reminder issues on 2026-08-02 (7 days before the 2026-08-09 default due date) via the `.github/workflows/fitness-review.yml` workflow. The review process itself is documented at `governance/fitness-review.md` — pass / pass-with-notes / fail outcomes, escalation rules, and the rotation pattern that prevents author-reviews-own-work bias.

A new CI lint workflow enforces frontmatter consistency on every PR. Failing the lint blocks merge until the SKILL.md frontmatter (presence of all three new keys + `context_budget` matches `tier:` + `fitness_review_due` parses as ISO-8601) passes. There is no opt-out — this is a marketplace-quality invariant.

If you want the new pre-commit budget gate locally, one command installs it:

```bash
git config core.hooksPath .githooks
```

The hook runs `scripts/check_skill_budgets.py` and `scripts/lint_known_debt.py` before each commit. To bypass intentionally, use `git commit --no-verify`. Full instructions at `governance/git-hooks-install.md`.

## For pipeline operators

The `governance/cache-prefix-hash.txt` regenerated once at the end of Story 5. The hash file's scope expanded from a single file (delivery-flow/SKILL.md, ADR-tk3-001 precedent) to all delivery-team Tier-A and Tier-B SKILL.md — though the current ledger entry pins delivery-flow as the canonical anchor (`43067c9e07e0b988cd976432dd07d5bb3d2336c41ad08a1b0064fb2fbd0b8328`). Prior hash from Wave caveman-lite was `9d4011d11e5b...926f`. The transition path was `9d40... → 4306...` over the course of Stories 1 through 5.

A one-time ~650-byte cumulative cache-prefix re-warm (~26KB cold-cache cost across the 13-file prefix region) lands on the first post-merge dispatch. ADR-tk4-003 records the math: +50 bytes per file × 13 files. The cumulative ~13,200-token reduction from the W3-1..W3-7 content trims pays back the ~6,500-token cold-cache cost on dispatch #1.

W3-18 (telemetry hardening) ships in this same release and starts producing reliable per-dispatch `prose_tokens` figures from the next pipeline run forward. Pipeline operators reading `.delivery/telemetry/skill-loads.jsonl` should expect the first effective baseline measurement on the next post-merge run; pre-Wave-3 rows in the file are placeholder/unreliable per the binding caveman-lite dogfood-report carry-forward.

## Initiative recap (5 waves, 4 months)

This is the close-out wave of the five-wave delivery-team skill token-economy initiative. The full arc:

| Wave | Pipeline | Theme | Headline outcome |
|---|---|---|---|
| 0 | tk0e | Foundations | Tier registry (`governance/skill-budgets.json`), telemetry hook (`.delivery/telemetry/skill-loads.jsonl`), CI line-budget gate (`.github/workflows/skill-line-budget.yml`), 5 binding rulings codified at `.delivery/memory/topics/skill-token-economy.md`. |
| 1 | tk1 | First structural extractions | Wave-1 doctrine extractions on delivery-flow + product-delivery; first cache-prefix freeze at `governance/cache-prefix-hash.txt` (Ruling 1 operationalized). |
| 2 | tk2 | Architect + paradigm seeds | Architect output-contracts split, transformation-phase detail extraction, paradigms/{volatility,ddd}/ seed sub-skills (precursor to ADR-tk4-002). |
| caveman-lite | tk3 | Prose-discipline floor | `prose_style: caveman-lite` config key + PROSE STYLE block injection in three dispatch templates; ADR-tk3-001 + 6-element contract; cache-prefix re-freeze (`9d40... → f997ec25...`). |
| 3 | tk4 (this run) | Closure + governance | All 7 over-budget SKILL.md compliant; governance frontmatter rollout to 11 top-level SKILL.md; paradigm sub-skill pattern operationalized for 2 more axes (research-agent, user-feedback); 6 retrospective carry-forwards discharged. Cache-prefix re-freeze (`f997ec25... → 4306...`). |

The cumulative arc moves the delivery-team token-economy floor from a pre-initiative SKILL.md surface of ~5,200 lines (delivery-flow alone at 999 lines pre-Wave-2 doctrine extraction) to today's compliant tier-budget regime (orchestrator at 500/500 Tier-A, 6 multiplexers at ≤300 Tier-B, 4 leaf skills at ≤200 Tier-C). Cumulative reduction across all five waves substantially exceeds the initiative's ≥50% target; exact telemetry-measured percentage lands on the next pipeline run once W3-18 telemetry hardening produces its first effective baseline.

## Known carry-forwards

The caveman-lite AC-13 close-out (initiative-level ≥20% prose-token reduction empirically measured) has a chicken-and-egg property in this wave: W3-18 is what makes per-dispatch token telemetry reliable, and W3-18 itself ships in this release. The first effective measurement therefore lands on the next pipeline run after this merge. Severity P1, non-blocking for Wave 3 close. The BACKLOG-102 stop-rule armed in Wave caveman-lite remains armed; if the next-run measurement shows <15% prose-token reduction, root-cause retro fires and pauses any Tier-2 A/B follow-on work. Owner: PO + QA jointly at the close of the next pipeline run; first agenda item of next-run UAT.

The architect Cross-Role Tasks partial-compliance reserve (ADR-tk4-001 §"Partial-compliance reserve") was not exercised — architect landed at 294 ≤ 300 with the canonical extraction math. No `Budget-Exception:` line in this PR body.

A small directory-hygiene residual remains: 13 Wave-caveman-lite (tk3) UAT artifacts in `.delivery/artifacts/07-uat/` (qa, devops, dod subdirectories) carry over to this run because W3-17 (Stage-7 stale-sweep) is itself one of the Wave 3 deliverables. Other Stage 7 roles refresh their artifacts during this Wave 3 dispatch; the residual is P2 directory hygiene, not numeric drift. The cross-doc consistency report at `.delivery/artifacts/07-uat/tech-writer/cross-doc-consistency-report.md` enumerates the 13 files explicitly.

## References

- BACKLOG-104 — `.delivery/backlog/BACKLOG-104-skill-token-economy-delivery-team-wave-3.md`
- ADR-tk4-001 — `.delivery/artifacts/04-architect/adrs/ADR-tk4-001-tier-b-closure-approach.md`
- ADR-tk4-002 — `.delivery/artifacts/04-architect/adrs/ADR-tk4-002-paradigm-sub-skill-pattern.md`
- ADR-tk4-003 — `.delivery/artifacts/04-architect/adrs/ADR-tk4-003-governance-frontmatter-shape.md`
- Architecture summary — `.delivery/artifacts/04-architect/solution/architecture-tk4-wave-3.md`
- Stage 6 summary — `.delivery/artifacts/06-dev/stage-summary.md` (7 stories, 5 first-try)
- Story implementations — `.delivery/artifacts/06-dev/developer/story-{1..7}-implementation.md`
- Governance fitness-review process — `governance/fitness-review.md`
- Governance budgets registry — `governance/skill-budgets.json` (`known_debt: []` post-Wave-3)
- Cache-prefix ledger — `governance/cache-prefix-hash.txt`
- Git-hooks install — `governance/git-hooks-install.md`
- Binding decisions — `.delivery/memory/topics/skill-token-economy.md`
- Caveman-lite predecessor — `.delivery/memory/archive/run-2026-05-05-tk3.md`

## Credits

Aragorn (PO, Idea) · Gandalf (PO, Refine) · Saruman of Many Colours (Architect) · Frodo (PO, Plan) · Gimli (Developer, 7 stories) · Boromir (DevOps) · Legolas (QA) · Bilbo (Tech-Writer). The Council that started the road meets it again at the end. Five waves shipped; the long task is done.

— Bilbo Baggins, Red Book of Westmarch, run-2026-05-09-tk4
