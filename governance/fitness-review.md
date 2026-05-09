# Skill Fitness Review Process

Quarterly health check for every top-level SKILL.md across the marketplace.
Prevents drift between the line-budget regime, maintainer ownership, and the
lived-in shape of each skill after waves of token-economy edits.

Companion artifacts:
- `governance/skill-budgets.json` — line-budget tiers + known-debt registry
- `governance/cache-prefix-hash.txt` — cache-prefix re-freeze ledger
- `.github/workflows/fitness-review.yml` — automated reminder workflow
- Per-skill `fitness_review_due:` frontmatter (added in Story 5 / W3-9)

---

## Purpose

Each SKILL.md ships with a `fitness_review_due:` ISO-8601 date in its
frontmatter. The fitness review is the operational answer to that date —
the process that examines the skill, decides whether it still earns its
budget, and resets the due date for the next cycle.

Goals:
1. Catch budget drift early (file approaching its tier ceiling without a
   contributing PR).
2. Surface stale content (references that no longer match SKILL.md, dead
   trigger phrases, deprecated patterns).
3. Verify the maintainer field is still accurate (people change teams).
4. Confirm telemetry KPIs (`context_tokens_per_pipeline_run`) are not
   regressing for skills that participate in delivery-flow.

## Cadence

Quarterly per skill. The exact due date is recorded in each SKILL.md
`fitness_review_due:` field, staggered across an 80–100-day window so the
load distributes (FR-5.4 from PRD). The reminder workflow opens a tracking
issue 7 days before each due date.

A skill that fails fitness 2 quarters in a row triggers escalation (see
Escalation section below).

## Scope

All top-level SKILL.md files in the repository. Currently:
- 11 `delivery-team/skills/*/SKILL.md`
- 2 grandfathered `delivery-team/skills/architect/paradigms/{volatility,ddd}/SKILL.md`
- Top-level SKILL.md for: `agentic-flow-builder`, `prompt-engineer`,
  `prd-quality-gate-flow`, `research-agent`, `mtg-commander`, `hardware-team`,
  and any future plugin added to `.claude-plugin/marketplace.json`
- Paradigm sub-skills under `.../skills/<axis>/<variant>/SKILL.md` (added in
  Story 4 / W3-8) inherit the parent's review date by default

Out of scope: reference files under `references/`, scripts under `scripts/`,
hook implementations under `hooks/`. These ride on the parent skill's review.

## Procedure

For each skill that comes due:

1. **Assign a reviewer** — rotate from the skill's `maintainer:` group; the
   reviewer must NOT be the most recent committer on the skill (avoid
   author-reviews-own-work bias).
2. **Run the budget check** — `python3 scripts/check_skill_budgets.py`; the
   skill must exit 0 OR have a justified `Budget-Exception:` entry in
   `governance/skill-budgets.json known_debt[]` with a `target_wave:`.
3. **Inspect frontmatter** — verify `tier:` matches `context_budget:`,
   `maintainer:` is a real owning group, `fitness_review_due:` is the
   current cycle (will be advanced at the end of this review).
4. **Spot-check trigger phrases** — sample 3 user prompts from
   `.delivery/telemetry/skill-loads.jsonl` (or recent transcripts); confirm
   the skill triggers for the queries it advertises and does NOT trigger for
   queries it disclaims.
5. **References freshness** — `grep -l references/ <skill>/SKILL.md`; confirm
   every referenced file still exists and matches the description in
   SKILL.md.
6. **KPI check** — for delivery-team skills, look at the most recent retro
   `context_tokens_per_pipeline_run` rolling mean. Flag any skill
   contributing >20% of the per-run total as "review for further extraction."
7. **Record outcome** — append a row to the review log (next section).

## Outputs

- **Review log**: `governance/fitness-review-log.md` (created on first
  review). Append-only table: date | skill | reviewer | result | notes.
  Result values: PASS / PASS_WITH_NOTES / FAIL.
- **Corrective backlog items**: any FAIL or PASS_WITH_NOTES with action items
  becomes a `BACKLOG-XXX` entry under `.delivery/backlog/`. Actions get
  routed through the next available delivery-flow wave.
- **Frontmatter update**: on PASS, advance `fitness_review_due:` by 90 days
  (committed in the same PR as the log entry).

## Escalation

A skill that fails fitness review 2 cycles in a row escalates:
- The skill's `maintainer:` group is paged via the next pipeline retro.
- The Architect role evaluates whether the skill should be (a) restructured,
  (b) merged into another skill, or (c) deprecated and removed from
  `.claude-plugin/marketplace.json`.
- A FEATURE-or-CLEANUP backlog item lands the recommended treatment.

A skill that has gone >180 days past its `fitness_review_due:` date without
a review escalates immediately (the workflow will open a P1 issue, not a
reminder).
