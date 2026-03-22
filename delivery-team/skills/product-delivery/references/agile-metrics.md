# Agile Metrics

Reference guide for measuring team performance, flow, and delivery health.
Metrics exist to inform decisions, not to judge people.

---

## Velocity

**Calculation:** Sum of story points (or count of items) completed in a sprint.
Use a rolling average of the last 3-5 sprints for planning.

**Normalization:** Velocity is team-specific and cannot be compared across teams.
Different teams estimate differently, work on different problem domains, and have
different definitions of done. Comparing velocities creates perverse incentives
to inflate estimates.

**What velocity predicts:** How much work this team can likely complete next sprint,
assuming stable composition and similar work types.

**What velocity does not predict:** Individual productivity, code quality, or
business value delivered. A team can have rising velocity while delivering
decreasing value. Stop using velocity when the team treats it as a target.

---

## Burn-Down Chart

**Components:** X-axis is time (days in sprint). Y-axis is remaining work. The ideal
line runs diagonally from total committed work to zero. The actual line shows real
remaining work each day.

**Reading the chart:**
- Actual above ideal: behind schedule. Investigate impediments.
- Actual below ideal: ahead or over-estimated.
- Flat sections: work in progress but nothing completing. Check for blockers.
- Upward jumps: scope added mid-sprint.

**Limitations:** Burn-downs hide scope changes. Use burn-up charts when scope
volatility is a concern.

---

## Burn-Up Chart

**Components:** X-axis is time. Two lines: total scope and completed work. The gap
between them is remaining work.

**Scope creep visibility:** When the scope line rises during a sprint, scope is being
added. This is the primary advantage over burn-down charts.

**Forecasting:** Extend the completion trend line to see when it intersects the
scope line. If scope is also rising, the intersection moves outward -- making the
"never done" risk visible.

---

## Cycle Time

**Definition:** The elapsed time from when work actively starts (moves to In Progress)
to when it is done (meets Definition of Done).

**Distribution analysis:** Cycle time is not normally distributed. Use percentiles:
- 50th percentile: half of items finish faster than this.
- 85th percentile: most items finish by this time. Use for commitments.
- 95th percentile: nearly all items. Use for contractual deadlines.

**Percentile-based forecasting:** "Based on historical data, there is an 85% chance
this item will be done within 8 days." This is more honest and useful than single-
point estimates.

---

## Lead Time

**Definition:** The elapsed time from when work is requested (enters the backlog or
is formally requested) to when it is delivered to the customer.

**Lead time vs cycle time:** Lead time includes queue time (waiting in the backlog).
Cycle time is a subset of lead time. Lead time is the customer-facing metric --
customers do not care when you started working, they care when they asked and when
they received.

**Reducing lead time:** Reducing cycle time helps, but often the largest component of
lead time is queue time. Prioritization discipline and WIP limits have more impact
than working faster.

---

## Throughput

**Definition:** The number of items completed per unit of time (per week or per
sprint).

**Stability:** Throughput measured in item count (not story points) tends to be more
stable over time than velocity, because it removes estimation variance. Teams that
right-size work items to similar sizes get the most value from throughput tracking.

**Forecasting with throughput:** Monte Carlo simulations using historical throughput
data produce probabilistic forecasts: "Given our throughput distribution, there is
an 80% chance we complete these 20 items within 6 sprints."

---

## Work In Progress (WIP)

**WIP limits:** Set explicit limits on how many items can be in each workflow state.
Start with a limit equal to the number of team members minus one, then adjust.

**Little's Law:** Average Lead Time = Average WIP / Average Throughput. This is a
mathematical relationship, not a guideline. Reducing WIP directly reduces lead time,
assuming throughput stays constant.

**Why WIP limits work:** They force the team to finish work before starting new work,
reduce context switching, surface bottlenecks faster, and create pull-based flow.

---

## Cumulative Flow Diagram (CFD)

**Structure:** X-axis is time. Y-axis is item count. Stacked bands represent each
workflow state (To Do, In Progress, In Review, Done). The width of each band at any
point shows the WIP in that state.

**Bottleneck detection:** A widening band indicates accumulation -- that state is a
bottleneck. A narrowing band indicates drain. Flat bands at the top (Done) indicate
no delivery.

**Flow efficiency from CFD:** The ratio of the active-work band width to the total
width (all non-Done bands) approximates flow efficiency.

---

## Flow Efficiency

**Calculation:** (Active working time / Total elapsed time) * 100.

**Typical benchmarks:** Most teams operate at 15-40% flow efficiency. World-class
teams reach 40-60%. Below 15% indicates severe wait-time problems.

**Improvement levers:** Reduce handoffs, reduce approval queues, co-locate expertise,
limit WIP, automate repetitive steps.

---

## Escape Rate

**Calculation:** (Defects found after release / Total items released) * 100.

**Interpretation:** Measures the effectiveness of the team's quality practices. Track
over time. A rising escape rate signals that quality practices (testing, code review,
definition of done) need attention.

**Segmentation:** Break escape rate down by severity. A 10% escape rate of cosmetic
issues is different from a 10% escape rate of data-loss bugs.

---

## Predictability (Commitment Reliability)

**Calculation:** (Items completed / Items committed at sprint planning) * 100.

**Target range:** 80-100% indicates healthy planning. Consistently below 70%
suggests systemic over-commitment, scope creep, or external disruptions. Above
100% consistently suggests under-commitment or sandbagging.

**Improving predictability:** Right-size stories, use historical data for capacity,
account for known absences, and protect sprint scope.

---

## Anti-Patterns

**Vanity metrics:** Metrics that look good but do not inform decisions (lines of
code, commits, hours worked). If a metric does not change behavior, it is vanity.

**Velocity as productivity measure:** Using velocity to evaluate individuals or
compare teams destroys its planning utility. Teams inflate estimates to game it.

**Comparing teams:** Cross-team metric comparison is valid only for system-level
flow metrics (lead time, escape rate) with identical measurement definitions.

**Metric fixation:** Goodhart's Law -- when a measure becomes a target, it ceases
to be a good measure. Rotate attention and pair primary metrics with counter-metrics.
