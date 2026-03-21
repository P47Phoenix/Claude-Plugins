# Stakeholder Communication Templates

Audience-appropriate templates for product updates, decisions, and announcements.

---

## Audience Communication Guide

| Audience | Cares About | Tone | Length | Format |
|----------|------------|------|--------|--------|
| **Executive / Leadership** | Outcomes, metrics, risk, investment ROI | Strategic, confident | Short | Bullets + numbers |
| **Engineering team** | Technical decisions, scope, constraints, "why" | Direct, collaborative | Medium | Narrative + lists |
| **Design team** | User needs, research insights, design direction | User-centric | Medium | Story-driven |
| **Customer-facing teams** | What users can do, when, how to explain it | Clear, non-technical | Short | FAQ format |
| **External users / customers** | What changed, how it affects them, what to do | Empathetic, clear | Short | Benefit-focused |
| **Cross-functional stakeholders** | Status, dependencies, decisions needed | Neutral, factual | Medium | Structured update |

---

## Template 1: Executive Briefing

Use for: leadership updates, steering committee, board-level summaries.

```
## [Product / Initiative] — Executive Update
**Date:** [date]
**Prepared by:** [PO name]

### Status: [On Track / At Risk / Off Track]

### Key Outcomes This Period
- [Metric]: [result] vs. [target] ([+/- %])
- [Metric]: [result] vs. [target]

### Decisions Needed
1. [Decision] — Recommended: [option] — Deadline: [date]

### Risks & Mitigations
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| ... | Med | High | ... |

### Next Milestone
[What ships next, when, and what success looks like]
```

---

## Template 2: Sprint Review Summary

Use for: post-sprint stakeholder communication; what was shipped.

```
## Sprint [N] Review — [date]

### Sprint Goal
[Restate the sprint goal]

### Goal Achieved: Yes / Partially / No
[One sentence explanation if partial or no]

### Shipped This Sprint
| Story | Demo Link / Notes |
|-------|------------------|
| [Story title] | [link or "see recording"] |

### Metrics Impact
- [Metric changed by]: [before → after]

### What Didn't Ship (and why)
- [Story]: [reason — spilled, deprioritized, blocked]

### Next Sprint Focus
[Brief preview of sprint N+1 goal]
```

---

## Template 3: Feature Announcement (Internal)

Use for: announcing shipped features to customer-facing teams before external release.

```
## Feature Announcement: [Feature Name]

**Live Date:** [date / release version]
**Audience:** [which users / plans / regions]

### What's New
[2–3 sentence description of what changed, from the user's perspective]

### User Impact
- Before: [what users had to do / couldn't do]
- After: [what users can now do]

### How to Demo / Explain This
[Step-by-step walkthrough for support/sales to use with customers]

### Known Limitations
- [Any edge cases, known gaps, or planned follow-up work]

### FAQ
**Q: [Anticipated question]**
A: [Answer]

**Q: [Anticipated question]**
A: [Answer]

### Who to Contact
[PO name + channel for questions]
```

---

## Template 4: Roadmap Communication

Use for: quarterly roadmap reviews, stakeholder alignment sessions.

```
## [Product] Roadmap — [Quarter / Year]

**Last Updated:** [date]

### Strategic Themes This Period
1. [Theme] — [one line rationale]
2. [Theme]

### Now (This Quarter)
| Initiative | Expected Outcome | Status |
|------------|-----------------|--------|
| ... | ... | In Progress |

### Next (Next Quarter)
| Initiative | Expected Outcome | Confidence |
|------------|-----------------|------------|
| ... | ... | High / Med / Low |

### Later (6+ months)
| Initiative | Strategic Rationale |
|------------|---------------------|
| ... | ... |

### What We're NOT Doing (and why)
| Item | Reason |
|------|--------|
| ... | [Strategic trade-off / deprioritized vs. ...] |

### Open Questions / Dependencies
- [Question or dependency]: Owner: [name], Due: [date]
```

---

## Template 5: Decision Record

Use for: documenting significant product decisions for future reference and alignment.

```
## Decision Record: [Decision Title]

**Date:** [date]
**Decision Maker:** [PO / Leadership / Team]
**Status:** [Proposed / Decided / Superseded]

### Context
[What situation prompted this decision? What constraints exist?]

### Options Considered

**Option A: [Name]**
- Pros: ...
- Cons: ...

**Option B: [Name]**
- Pros: ...
- Cons: ...

### Decision
[What was decided and why]

### Implications
- [What changes as a result]
- [What is now ruled out]

### Review Date
[When will this decision be revisited, if ever]
```

---

## Template 6: Engineering Kickoff Brief

Use for: handing off a feature to engineering at the start of development.

```
## Engineering Kickoff: [Feature Name]

**Date:** [date]
**PO:** [name]
**Epic/Ticket:** [link]

### Problem We're Solving
[User problem in 2–3 sentences — the "why"]

### Success Looks Like
[Acceptance criteria at the epic level; how PO will sign off]

### User Stories in Scope
1. [Story title + link] — [X pts]
2. [Story title + link] — [X pts]

### Out of Scope (explicitly)
- [Item] — [reason]

### Design Assets
[Link to Figma / mockups / prototype]

### Technical Context
[Known constraints, API contracts, infrastructure decisions already made]

### Dependencies
| Dependency | Owner | Status | ETA |
|------------|-------|--------|-----|
| ... | ... | Blocked / In progress | ... |

### Open Questions for Engineering
1. [Question needing technical input]

### Timeline
- Start: [date]
- Target completion: [date]
- Hard deadline (if any): [date + reason]
```
