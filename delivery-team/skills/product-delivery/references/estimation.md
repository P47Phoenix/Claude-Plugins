# Estimation & Velocity Tracking

## Purpose

Provide consistent story estimation, track team velocity over time, enable capacity planning, and calibrate estimates against actual delivery. Estimation is a forecasting tool, not a performance metric.

---

## Story Point Estimation

### Fibonacci Scale

Use the Fibonacci sequence for relative sizing. Each number represents relative complexity, uncertainty, and effort compared to a baseline story.

| Points | Relative Size | Typical Characteristics |
|--------|--------------|------------------------|
| 1 | Trivial | Config change, copy update, well-understood fix |
| 2 | Small | Single-file change, clear requirements, no unknowns |
| 3 | Medium-small | A few files, straightforward logic, minimal integration |
| 5 | Medium | Multiple files, some integration, moderate complexity |
| 8 | Large | Cross-cutting concern, significant logic, integration testing needed |
| 13 | Very large | High uncertainty, multiple components, consider splitting |

**Rules:**
- Stories estimated at 13 should almost always be split before entering a sprint
- Stories above 13 are not estimable — they are epics, not stories
- The team picks a well-understood "3-point story" as the baseline reference
- Estimation is relative: "Is this bigger or smaller than our reference story?"

### T-Shirt Sizing Alternative

For early-stage estimation or roadmap-level planning, use T-shirt sizes mapped to point ranges:

| T-Shirt | Point Range | Use When |
|---------|------------|----------|
| XS | 1-2 | Quick wins, trivial changes |
| S | 2-3 | Small, well-understood work |
| M | 3-5 | Standard stories |
| L | 5-8 | Complex stories, may need splitting |
| XL | 8-13 | High complexity, definitely split before sprint |

T-shirt sizes are useful for backlog grooming and roadmap discussions. Convert to Fibonacci points before sprint commitment.

### Estimation Techniques

1. **Planning Poker**: Each team member independently estimates, then reveals simultaneously. Discuss outliers. Re-estimate until convergence.
2. **Affinity Mapping**: Sort stories into size buckets (columns) by comparison. Fast for large backlogs.
3. **Reference Story Comparison**: "Is this bigger or smaller than [reference story]? By how much?"

---

## Velocity Tracking

### Definition

**Velocity** = total story points completed (DONE) in a sprint. Only stories that meet the Definition of Done count. Partially completed stories carry zero velocity credit.

### Calculation

```
Sprint Velocity = SUM(story_points) for all stories with status = DONE in the sprint
Rolling Average = (V[n] + V[n-1] + V[n-2]) / 3   (last 3 sprints)
```

### Velocity Table Format

| Sprint | Committed (pts) | Completed (pts) | Velocity | Completion Rate | Notes |
|--------|----------------|-----------------|----------|----------------|-------|
| Sprint 1 | 21 | 18 | 18 | 86% | New team member onboarding |
| Sprint 2 | 20 | 20 | 20 | 100% | |
| Sprint 3 | 22 | 19 | 19 | 86% | External dependency delayed US-007 |
| **Rolling Avg** | | | **19** | **91%** | |

### Memory Integration

Store velocity data in `.delivery/memory/topics/velocity.md`:

```markdown
# Velocity History

## Rolling Average: 19 points/sprint (last 3 sprints)

| Sprint | Date | Committed | Completed | Notes |
|--------|------|-----------|-----------|-------|
| Sprint 3 | 2026-03-21 | 22 | 19 | External dependency delay |
| Sprint 2 | 2026-03-07 | 20 | 20 | |
| Sprint 1 | 2026-02-21 | 21 | 18 | Onboarding |

## Calibration Notes
- Stories estimated at 5 points: avg 1.2 correction loops
- Stories estimated at 8 points: avg 2.1 correction loops
- Stories with external dependencies: 30% more likely to carry over
```

---

## Capacity Planning

### Sprint Capacity Formula

```
Available Capacity = Rolling Velocity * (Available Days / Typical Sprint Days) * Buffer
```

Where:
- **Rolling Velocity** = average of last 3 sprints
- **Available Days** = sprint length minus PTO, holidays, ceremonies
- **Typical Sprint Days** = standard sprint length (e.g., 10 days)
- **Buffer** = 0.8 (reserve 20% for interruptions, bugs, meetings)

### Example

```
Rolling velocity: 19 points
Sprint length: 10 days
PTO this sprint: 2 person-days (1 dev out for 2 days)
Team size: 4

Available days: 10 - (2/4) = 9.5 effective days
Capacity: 19 * (9.5 / 10) * 0.8 = 14.4 -> commit to ~14 points
```

### Sprint Forecast

Based on velocity, forecast how many sprints remaining work will take:

```
Remaining Points = SUM(estimated points for all uncommitted stories)
Sprints Remaining = CEIL(Remaining Points / Rolling Velocity)
```

Include a range: optimistic (highest recent velocity), likely (rolling average), pessimistic (lowest recent velocity).

---

## Calibration Over Time

Track how estimates compare to actual effort. This improves future estimation accuracy.

### Calibration Data Points

- **Correction loops**: How many self-correction cycles did a story require?
- **Carry-overs**: Stories not completed within the sprint they were committed to
- **Actual vs estimated**: Did 5-point stories consistently take more effort than 3-point stories?
- **Surprise complexity**: Stories that revealed hidden complexity during development

### Calibration Table

| Estimated Points | Avg Correction Loops | Carry-Over Rate | Typical Pattern |
|-----------------|---------------------|-----------------|-----------------|
| 1-2 | 0.3 | 5% | Rarely surprising |
| 3 | 0.8 | 10% | Occasionally underestimated |
| 5 | 1.2 | 15% | Integration complexity often missed |
| 8 | 2.1 | 25% | Frequently underestimated — consider splitting |
| 13 | 3.0+ | 40% | Almost always should have been split |

Use calibration data to adjust future estimates: "Our 5-point stories typically need 1.2 correction loops, so budget accordingly."

---

## Anti-Patterns

| Anti-Pattern | Why It Is Harmful | What To Do Instead |
|-------------|-------------------|-------------------|
| Using velocity as a performance metric | Creates pressure to inflate estimates; destroys trust | Use velocity only for forecasting and capacity planning |
| Comparing velocity across teams | Teams estimate differently; comparison is meaningless | Each team's velocity is relative to their own baseline |
| Over-precision in estimates | "This is a 4.5-point story" — false precision | Use Fibonacci scale; the gaps are intentional |
| Counting partial credit | "We finished 80% of that 8-pointer" — not DONE | Only count stories that meet Definition of Done |
| Velocity targets set by management | Incentivizes gaming; undermines honest estimation | Let velocity emerge from consistent estimation practice |
| Ignoring velocity trends | A declining trend signals problems; a spiking trend signals inflation | Review velocity trends in retrospectives |
| Estimating in hours instead of points | Conflates effort with elapsed time; penalizes slower estimators | Points measure relative complexity, not hours |
