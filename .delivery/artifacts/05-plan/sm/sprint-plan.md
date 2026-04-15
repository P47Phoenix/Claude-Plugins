# Sprint Plan — DOCS_ONLY Documentation Refresh

**Author:** Aragorn, son of Arathorn (Scrum Bag, `lotr-full` alias)
**Stage:** 05-Plan · Project type: DOCS_ONLY · Tier: markdown
**Input:** `tech-writer/doc-stories.md` (Bilbo) · 8 stories · 8 pts

> "A day may come when the courage of men fails... but it is not this day. This day we ship markdown."

---

## Capacity Check

- **Sprint ceiling:** 4 pts · **Hard cap:** 5 pts
- **Total plan:** 8 pts
- **Sprint count:** 2 (4 + 4) — fits exactly under ceiling, zero headroom burned
- **Tier:** markdown — small estimates, no code, no schema, no tests beyond grep + JSON-load

## Dependency Graph

```
US-3 (CLAUDE.md)  ──────────────── independent
US-6 (marketplace.json) ───────── independent
US-1 (mtg-commander README) ──┐
                              ├──► US-2 (same file section)
                              └──► US-4 (links into it)
US-5 (delivery-team README) ──┬──► US-7 (cross-link audit)
US-4 (root README) ──────────┘
                              └──► US-8 (troubleshooting block appends)
```

Critical path: **US-1 → US-4 → US-7** (new plugin README must exist before root README links to it; cross-link audit runs last).

## Sprint 1 — Foundation (4 pts)

Goal: Close the mtg-commander discoverability gap at the plugin level + correct CLAUDE.md drift + verify marketplace registry. Everything self-contained; no cross-file dependencies leave the sprint unfinished.

| ID | Title | Pts | Rationale |
|----|-------|-----|-----------|
| US-1 | Create `mtg-commander/README.md` | 2 | Highest-severity convergent gap (Bilbo #1 + Galadriel #1). Biggest single user-value delivery. |
| US-2 | `.mtg-commander.yml.example` + walkthrough | 1 | Directly follows US-1 (same file's Configuration section). Bundling reduces re-read cost. |
| US-3 | CLAUDE.md refresh | 1 | Independent; touches a different file; parallelizable. Agent-facing drift fix. |
| US-6 | marketplace.json verification | 0.5 | Independent, quick. Bundled with S1 to lock registry truth before S2 README edits consume it. |

**Sprint 1 total:** 4.5 pts — **exceeds 4-pt ceiling by 0.5**.

**Mitigation:** US-6 is a 0.5-pt verification story; if on-disk matches registry (high likelihood per Bilbo §2 — "matches top-level directories exactly"), actual work collapses to ~15 min and stays inside ceiling. If a real mismatch surfaces, promote US-6 to Sprint 2 and reclaim capacity.
**Decision:** keep US-6 in S1, monitor at mid-sprint checkpoint.

## Sprint 2 — Surface + Integrate (4 pts)

Goal: Root-level discoverability (README) + delivery-team advanced-capabilities surfacing + cross-link integrity + lightweight troubleshooting. Consumes S1 outputs (links to mtg-commander/README.md).

| ID | Title | Pts | Rationale |
|----|-------|-----|-----------|
| US-4 | README.md roster + recent additions | 1 | Links to US-1 artifact; must run after S1. |
| US-5 | delivery-team/README.md Advanced section | 1 | Independent of S1; surfaces constraints / board / transformation / paradigms. |
| US-8 | Troubleshooting inline blocks | 1 | Appends to US-5's file + root README; runs after US-4 and US-5 land. |
| US-7 | Cross-link audit | 0.5 | Runs last — validates all new links across touched files. |

**Sprint 2 total:** 3.5 pts — comfortably under ceiling, absorbs any US-6 spillover from S1.

## Adversarial Self-Check

- **Q: Is this actually 2 sprints of effort or 1 bloated sprint?** A: 8 pts at markdown tier ≈ 8 hours of focused authoring. Two sprints is honest pacing with review time; one sprint would skip the US-7 cross-link verification pass.
- **Q: Are we smuggling a feature in?** A: No. Every story is content creation/refresh on existing files. `.mtg-commander.yml.example` is a config example, not a new primitive — schema already shipped in SKILL.md.
- **Q: Sprint 1 is 4.5 — are we kidding ourselves?** A: US-6 is genuinely a 15-minute verification if the registry matches disk (Bilbo confirmed it does in §2). The 0.5-pt estimate is a buffer, not realistic work. Acceptable.
- **Q: Does the plan honor "light means reduced depth, not skip"?** A: Yes. Deferred `docs/user-guide/*` pages are not "skipped light stages" — they are explicitly deferred to a named follow-on cycle in the story doc. Current cycle still executes in full at its chosen scope.
- **Q: Will out-of-scope vocabulary leak?** A: US-3 and US-5 AC explicitly forbid impl-detail language (no "sub-skill refactor," describe as "paradigm selection"). Tech Writer owns wording; QA grep strategy catches regressions.

## Exit Criteria

- All 8 stories meet their AC
- QA test strategy (Legolas) passes end-to-end
- No new broken links introduced (US-7 gate)
- Total work delivered: 8 files touched (2 new, 6 edits), 0 code changes, 0 schema changes.

> "By all the signs, we are come to the end of this stretch of road. Two sprints and we sup in Rivendell."
