<!-- run: run-2026-05-09-tk4 | stage: 07-uat | depth: full | author: Tech-Writer (Bilbo Baggins) | role: technical-writer | task: user-guide | wave: 3 (final) -->

---
title: "Contributor Guide — Wave 3 Governance Frontmatter and Workflows (run-2026-05-09-tk4)"
stage: 07-uat
author: Bilbo Baggins (operations skill, tech-writer role)
created: 2026-05-09
pipeline_id: run-2026-05-09-tk4
audience: future delivery-team contributors and skill maintainers
prerequisite_knowledge: familiarity with `delivery-team/skills/<name>/SKILL.md` frontmatter, `governance/` registry files, and the delivery-flow pipeline
supersedes: prior tk3 user-guide (2026-05-05)
---

# Contributor Guide — Wave 3 Governance Frontmatter and Workflows

## New SKILL.md frontmatter keys

Every top-level delivery-team SKILL.md (11 files) now carries three governance keys appended to the existing frontmatter:

| Key | Type | Purpose | Example |
|---|---|---|---|
| `maintainer:` | string (github-handle or team-id) | Names the owning party accountable for fitness review and budget compliance. | `delivery-team-leads` |
| `fitness_review_due:` | ISO-8601 date (YYYY-MM-DD) | Schedules the next quarterly fitness review for this skill. | `2026-08-09` |
| `context_budget:` | integer (line cap) | Explicit line cap, redundant with `tier:` but lint-friendly. Must match tier (A=500, B=300, C=200). | `300` |

The keys land in frontmatter immediately after `tier:`. Edit them in place when you change ownership, advance a review cycle, or correct a tier mismatch. The CI lint workflow (PR-time) blocks merge on any missing key, malformed date, or context_budget-vs-tier mismatch.

## Pre-commit hook (opt-in)

A pre-commit hook at `.githooks/pre-commit` runs the same checks as the PR-time CI gate, but locally before the commit ever leaves the working tree. One command installs:

```bash
git config core.hooksPath .githooks
```

The hook runs `python3 scripts/check_skill_budgets.py` and `python3 scripts/lint_known_debt.py`. Either non-zero exit blocks the commit. Bypass intentionally with `git commit --no-verify` — use sparingly; the CI gate still fires on PR. For a legitimate budget exception, also include `Budget-Exception: known-debt-tk0e` in the PR body per ADR-tk0e-002.

Uninstall the hook with `git config --unset core.hooksPath`. Full instructions and verification steps live at `governance/git-hooks-install.md`.

## Fitness-review workflow

The quarterly fitness review process is the operational answer to the `fitness_review_due:` date in each SKILL.md. The cron-driven `.github/workflows/fitness-review.yml` workflow opens a tracking issue 7 days before each due date. The full process is documented at `governance/fitness-review.md`; the short version:

1. Reviewer is assigned from the skill's `maintainer:` group, rotated to avoid the most recent committer (no author-reviews-own-work).
2. Reviewer runs `python3 scripts/check_skill_budgets.py` (must exit 0 or have a justified `known_debt[]` entry).
3. Reviewer inspects frontmatter (`tier:` matches `context_budget:`; `maintainer:` is a real owning group; trigger phrases in `description:` still match recent telemetry).
4. Reviewer spot-checks `references/` freshness and per-run KPI contribution (`context_tokens_per_pipeline_run`).
5. Outcome (PASS / PASS_WITH_NOTES / FAIL) appended to `governance/fitness-review-log.md`. PASS advances `fitness_review_due:` by 90 days in the same PR.

Two consecutive FAIL outcomes escalate: the maintainer group is paged, the Architect role evaluates restructure / merge / deprecate, and a CLEANUP backlog item lands the recommended treatment. A skill >180 days past its due date escalates immediately as a P1 issue.

## Validator prompt template

A canonical validator prompt template lives at `delivery-team/skills/delivery-flow/references/validator-prompt-template.md`. Story-7 W3-13 created it; subsequent FRESH-dispatch DoD validator prompts MUST reference this template rather than reconstructing prompt scaffolding inline. The template encodes the producer-validator separation rule, the FRESH-dispatch context isolation contract, and the standard verdict-line format (STATUS / ARTIFACT / SUMMARY).

When you author a new validator gate, point your dispatch at the template by file:line; do not duplicate the scaffolding text. The template is single-source-of-truth; edits ripple to every gate that references it.

## Canonical PROSE STYLE directive

The caveman-lite PROSE STYLE block remains at `delivery-team/skills/delivery-flow/references/prose-style.md` — single source of truth carried over from Wave caveman-lite (predecessor `run-2026-05-05-tk3`). Wave 3 did not modify the directive itself; the three dispatch templates in `references/pipeline-stages.md` (Primary, Supporting, DoD Validator) continue to inject the verbatim block under the `--- PROSE STYLE ---` delimiter. ADR-tk3-001 owns the contract.

If the block text needs to change in a future wave, edit `prose-style.md` only. Do not edit inlined copies elsewhere; there are none by design.

## Where to look when something behaves oddly

| Symptom | First place to look |
|---|---|
| CI lint fails on missing frontmatter key | `grep -L "fitness_review_due:" delivery-team/skills/*/SKILL.md` — names the file missing the key |
| Pre-commit hook blocks but CI passes | `python3 scripts/check_skill_budgets.py` locally — verify same Python version + working-tree-clean state as CI |
| Cache-prefix hash mismatch warning | `governance/cache-prefix-hash.txt` vs `sha256sum delivery-team/skills/delivery-flow/SKILL.md`; regenerate via `python3 scripts/regenerate_cache_prefix_hash.py` if a content edit landed without re-freeze |
| Fitness-review issue did not open on schedule | `.github/workflows/fitness-review.yml` cron schedule + recent run logs; `fitness_review_due:` date arithmetic |
| Paradigm sub-skill not discovered by router | Confirm sub-skill SKILL.md has `disable-model-invocation: true` (mandatory per ADR-tk4-002) and parent skill's Phase 1 router knows the variant |
| `known_debt[]` non-empty after a clean wave | `python3 scripts/lint_known_debt.py` — surfaces JSON-Python registry drift; usually a `governance/skill-budgets.json` edit that did not propagate to the lint script |

## Related authoritative documents

- ADR-tk4-001 — Tier-B/C closure approach (per-file extraction strategy + partial-compliance reserve).
- ADR-tk4-002 — Paradigm sub-skill pattern contract (canonical directory shape + frontmatter contract for sub-skills).
- ADR-tk4-003 — Governance frontmatter + cumulative cache-prefix re-freeze (the contract this guide operationalizes).
- BACKLOG-104 — Wave 3 initiative-level ACs and stop-rule.
- `plugin-dev:skill-development` — authoring conventions for any SKILL.md edit.
- `plugin-dev:skill-reviewer` — post-edit review pattern (load before opening PR).
