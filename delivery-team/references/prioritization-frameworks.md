# Prioritization Frameworks

Formulas, scoring guides, and worked examples for MoSCoW, RICE, WSJF, and Kano.

---

## MoSCoW

**Best for:** Stakeholder alignment sessions, release scoping, rapid triage.

### Categories

| Category | Definition | Guideline |
|----------|-----------|-----------|
| **Must Have** | Non-negotiable — product fails without it | Max 60% of scope |
| **Should Have** | Important, but workaround exists for launch | ~20% of scope |
| **Could Have** | Nice to have — cut first if time is short | ~20% of scope |
| **Won't Have (this time)** | Explicitly out of scope for this release | Document for future |

### Rules
- If everything is "Must Have", the framework is not being applied honestly — force trade-offs
- "Won't Have" is NOT "never" — it signals backlog items for a future release
- Revisit MoSCoW at each release boundary — priorities shift

### Template

```
## MoSCoW: [Release / Sprint / Feature]

### Must Have
- [ ] [Item] — [why non-negotiable]

### Should Have
- [ ] [Item] — [workaround available: ...]

### Could Have
- [ ] [Item] — [drop if capacity < X]

### Won't Have (this release)
- [ ] [Item] — [target: next quarter / v2.0 / backlog]
```

---

## RICE

**Best for:** Data-driven prioritization across a backlog of features with different team sizes and strategies.

### Formula

```
RICE Score = (Reach × Impact × Confidence) / Effort
```

### Factor Definitions

**Reach** — How many users are affected per time period (e.g., per quarter)?
- Count of users or transactions, not a percentage
- Example: 500 users/month

**Impact** — How much does this move the needle per person?
| Score | Impact |
|-------|--------|
| 3 | Massive — major increase in metric |
| 2 | High — significant impact |
| 1 | Medium — moderate impact |
| 0.5 | Low — minimal impact |
| 0.25 | Minimal — barely noticeable |

**Confidence** — How sure are you about the estimates?
| Score | Confidence |
|-------|------------|
| 100% | High — solid data |
| 80% | Medium — some data, some assumption |
| 50% | Low — mostly guessing |

**Effort** — Total person-months required (design + engineering + QA)
- Use team's estimate; 1 person-month = 1 engineer working 1 month

### Worked Example

| Feature | Reach | Impact | Confidence | Effort | RICE Score |
|---------|-------|--------|------------|--------|------------|
| Onboarding redesign | 2000 | 2 | 80% | 2 months | (2000×2×0.8)/2 = **1600** |
| Export to CSV | 500 | 1 | 100% | 0.5 months | (500×1×1.0)/0.5 = **1000** |
| Dark mode | 3000 | 0.5 | 50% | 3 months | (3000×0.5×0.5)/3 = **250** |

**Result:** Prioritize onboarding redesign > export to CSV > dark mode.

### Template

```
## RICE Scoring: [Backlog / Feature Set]

| Item | Reach | Impact | Confidence | Effort | RICE Score | Rank |
|------|-------|--------|------------|--------|------------|------|
| ...  | ...   | ...    | ...%       | ... mo | ...        | ...  |

Assumptions:
- Time period: [quarter / month]
- Confidence adjustments: [explain any low-confidence ratings]
```

---

## WSJF (Weighted Shortest Job First)

**Best for:** SAFe environments; optimizes for flow and cost of delay.

### Formula

```
WSJF = Cost of Delay / Job Duration
```

### Cost of Delay Components (rate each 1–10)

**User-Business Value** — How valuable is this to users and the business?
**Time Criticality** — Does delaying this incur cost? (regulatory deadlines, market windows, dependencies)
**Risk Reduction / Opportunity Enablement** — Does doing this now reduce future risk or unlock future value?

```
Cost of Delay = User-Business Value + Time Criticality + RR/OE
```

**Job Duration** (Job Size) — Relative sizing (use same Fibonacci scale as story points; normalize to a scale of 1–10 if needed)

### Worked Example

| Feature | User Value | Time Critical | RR/OE | Cost of Delay | Job Size | WSJF |
|---------|-----------|--------------|-------|--------------|----------|------|
| Auth bug fix | 8 | 9 | 7 | 24 | 1 | **24.0** |
| API versioning | 5 | 7 | 8 | 20 | 3 | **6.7** |
| Reporting dashboard | 7 | 3 | 2 | 12 | 5 | **2.4** |

**Result:** Fix auth bug first (highest WSJF) even though it's small. API versioning next despite medium size — high cost of delay justifies it.

### Template

```
## WSJF Scoring: [Feature Set / PI Planning]

| Item | User Value (1-10) | Time Critical (1-10) | RR/OE (1-10) | CoD | Job Size | WSJF | Rank |
|------|-------------------|---------------------|--------------|-----|----------|------|------|
| ...  | ...               | ...                  | ...          | ... | ...      | ...  | ...  |
```

---

## Kano Model

**Best for:** Understanding which features delight users vs. which are table stakes. Guides where to invest for satisfaction vs. retention.

### Five Feature Categories

| Category | Description | User Response If Present | User Response If Absent |
|----------|-------------|--------------------------|------------------------|
| **Must-Be (Basic)** | Expected; taken for granted | Neutral | Highly dissatisfied |
| **Performance (Linear)** | More = better satisfaction | Proportionally satisfied | Proportionally dissatisfied |
| **Attractive (Delighters)** | Unexpected; creates delight | Highly satisfied | Neutral (didn't expect it) |
| **Indifferent** | Doesn't matter either way | Neutral | Neutral |
| **Reverse** | Some users actively dislike it | Dissatisfied | Satisfied |

### Kano Survey Method

For each feature, ask users two questions:
1. **Functional:** "If this feature IS present, how do you feel?" (Like / Expect / Neutral / Tolerate / Dislike)
2. **Dysfunctional:** "If this feature is NOT present, how do you feel?" (Like / Expect / Neutral / Tolerate / Dislike)

Map responses to the Kano table to classify features.

### Prioritization Using Kano

1. **Must-Be first** — without these, users churn regardless of delighters
2. **Performance features** — invest proportionally; ROI is clear
3. **Attractive features** — invest selectively; these are competitive differentiators
4. **Indifferent** — cut or defer; no satisfaction gain
5. **Reverse** — remove or make optional

### Template

```
## Kano Analysis: [Feature Set]

| Feature | Category | Reasoning | Recommendation |
|---------|----------|-----------|----------------|
| ...     | Must-Be  | ...       | Prioritize     |
| ...     | Attractive | ...     | Selective invest |
| ...     | Indifferent | ...    | Defer / cut    |

### Investment Strategy
[Based on Kano classification, where should effort go this quarter?]
```
