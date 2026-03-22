# Dashboard Design

Principles and patterns for building dashboards that inform decisions rather than
decorate walls. A dashboard is a communication tool, not a data dump.

---

## Dashboard Hierarchy

Different audiences need different views at different cadences.

**Strategic (executive, quarterly/monthly):** 3-5 KPIs with trend lines. North Star,
revenue, retention, satisfaction. Business health understandable in 30 seconds.

**Tactical (team, weekly):** 5-10 metrics for the team's domain. Velocity, cycle
time, feature adoption, funnel rates. Guides weekly planning.

**Operational (daily/real-time):** System health, error rates, deployment status,
queue depth. Optimized for speed of comprehension during incidents.

---

## Chart Type Selection Guide

Choose the chart type that matches the analytical question.

- **Time series** -- line chart. Limit to 5-7 lines. Y-axis at zero for rates.
- **Comparison** -- bar chart. Horizontal for long labels. Sort by value.
- **Composition** -- stacked bar. Pie/donut only for 2-4 segments.
- **Distribution** -- histogram or box plot. Show percentiles, not just averages.
- **Correlation** -- scatter plot. Add trend line. Label outliers.
- **Funnel** -- funnel chart. Show absolute numbers and conversion percentages.
- **Geographic** -- map. Choropleth for rates, dot maps for counts.

---

## Layout Principles

How you arrange charts determines how effectively the dashboard communicates.

**Most important top-left.** Z-pattern scanning: primary metric in top-left.

**Consistent grid.** 12-column grid. Equal-importance metrics get equal-sized charts.

**Whitespace.** If you need 15 charts, you need 2-3 dashboards, not a denser layout.

**Grouping.** Related metrics together via proximity and headers. Grouping reflects
the audience's mental model.

**Progressive disclosure.** Summary first, drill-down on demand.

---

## Real-Time vs Batch Dashboards

**Batch (hourly/daily):** Simpler, cheaper, adequate for most analytical use cases.
Data 1-24 hours old is acceptable when decisions are made weekly.

**Real-time (seconds to minutes):** For operational monitoring: error rates, latency,
deployment health. Requires streaming infrastructure, costs 5-10x more than batch.

**Decision test:** "Will anyone decide differently in the next hour based on this
data?" If no, batch is sufficient. Most teams need real-time for system health and
batch for business metrics.

---

## Alert Threshold Design

Dashboards should actively notify when attention is needed.

**Static thresholds:** Set upper and lower bounds based on historical data. Error
rate above 5%, conversion rate below 2%, latency above 500ms. Simple to implement,
but requires manual tuning as baselines shift.

**Anomaly detection:** Statistical methods that adapt to trends and seasonality.
Flag values outside N standard deviations of the expected range. More robust than
static thresholds for metrics with natural variance.

**Burn rate alerts:** For SLO-based monitoring. Alert when the error budget is being
consumed faster than the allowed rate. A 1-hour burn rate alert fires if the current
error rate would exhaust the monthly budget in 1 hour. A 6-hour burn rate alert
catches slower degradation.

**Alert fatigue prevention:** Every alert must have a defined response action. If
the response is "ignore it," remove the alert. Consolidate related alerts. Require
alert review quarterly -- remove alerts that have not triggered or have been
consistently ignored. Target fewer than 5 actionable alerts per dashboard.

---

## Annotation Patterns

Context transforms data from numbers into narrative.

**Incident markers:** Vertical lines/regions marking outages. Prevents investigating
dips with known causes.

**Deployment markers:** Vertical lines at releases. Include version identifiers.

**Holiday/seasonal markers:** Flag low-traffic periods to prevent false alarms.

**Contextual notes:** Brief text for one-time events (campaign launch, pricing
change). Store annotations in structured format for cross-dashboard reuse.

---

## Dashboard Anti-Patterns

Common mistakes that reduce dashboard effectiveness to zero.

**Too many charts:** More than 8-10 charts means nothing gets attention. Split it.

**3D charts:** Never. They distort perception and misrepresent proportions.

**Dual y-axes:** Viewers assume same scale. Use two stacked charts instead.

**Pie charts with many slices:** Beyond 4-5 slices, use horizontal bar chart.

**No context:** "Conversion: 3.2%" is meaningless. Add target (4.0%), prior period
(2.8%), and trend direction.

**Misleading axes:** Always start bar chart y-axes at zero.

---

## Drill-Down Patterns

Moving from summary to detail without losing context.

**Summary to detail:** Click a KPI to see components, then underlying data. Preserve
parent context in breadcrumbs.

**Filter by segment:** Consistent filter controls that slice all charts by platform,
user type, geography, time period simultaneously.

**Time range selection:** Default to the most relevant range (7 days operational,
90 days strategic). Show the selected range prominently.

---

## Audience-Specific Dashboards

Build for the viewer, not for the data.

**Executive:** 3-5 KPIs, sparklines, status indicators. Answers "Is the business
healthy?" in 30 seconds. No jargon.

**Team:** Metrics the team controls. Answers "What should we focus on this week?"

**Individual:** Personal metrics (review turnaround, learning goals). Opt-in only.
Never use for performance evaluation -- they become surveillance tools.

---

## Dashboard Maintenance

Dashboards are products that require ongoing care.

**Review cadence:** Quarterly. For each chart: "Has anyone decided based on this
last quarter?" If no, remove it.

**Ownership:** Every dashboard has one owner. Orphaned dashboards decay into
misleading artifacts.

**Retirement:** Retire when the audience, data source, or metrics no longer exist.
Archive rather than delete.

**Documentation:** Brief description on the dashboard itself: audience, questions
answered, update frequency.
