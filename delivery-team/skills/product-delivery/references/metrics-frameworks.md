# Metrics Frameworks

Structured approaches to defining, organizing, and managing product metrics.
A good metrics framework connects daily measurements to strategic outcomes.

---

## HEART Framework

Google's framework for user-centered metrics. Each dimension uses a Goals, Signals,
Metrics (GSM) process to move from abstract intent to concrete measurement.

**Happiness:** Subjective satisfaction. Signal: surveys, app store ratings. Metric:
NPS, CSAT, rating per release. Trigger surveys at meaningful moments, not randomly.

**Engagement:** Depth and frequency of interaction. Signal: sessions, actions. Metric:
DAU/MAU ratio, actions per session, feature adoption. Tie to value-producing actions.

**Adoption:** New user or feature uptake. Signal: first-time usage, onboarding
completion. Metric: % using feature X within 7 days, onboarding completion rate.

**Retention:** Users returning over time. Signal: return visits, renewals. Metric:
Day-1/7/30 retention, cohort curves. Strongest signal of product-market fit.

**Task Success:** Efficiency of specific tasks. Signal: completion, errors, time.
Metric: task completion rate, error rate, time to complete key workflows.

---

## AARRR Pirate Metrics

A lifecycle funnel framework for growth-stage products.

**Acquisition:** How users find the product. Metrics: visitors by channel, CPA,
channel conversion. Focus on channels that bring retaining users, not just volume.

**Activation:** First experience quality. Metrics: signup completion, time to first
value, onboarding rate. Identify the "aha moment" correlated with retention.

**Retention:** Do users come back? Metrics: Day-N retention, churn rate. The most
important stage -- growth without retention is a leaky bucket.

**Revenue:** Do users pay? Metrics: paid conversion, ARPU, LTV, LTV:CAC ratio.

**Referral:** Do users invite others? Metrics: viral coefficient (invites * convert
rate), NPS. Coefficient above 1.0 means organic growth.

---

## North Star Metric

A single metric that captures the core value your product delivers to users.

**How to identify:** "What single measure best captures that a user got value?"
Reflects value delivery, not revenue. Airbnb: nights booked. Slack: messages sent.

**Characteristics:** Leads to revenue (but is not revenue itself), reflects customer
value, is measurable, is actionable, and is a leading indicator.

**Supporting metrics:** Decomposes into 3-5 input metrics teams directly influence.
For "nights booked": search conversion, listing quality, host response rate.

**Pitfalls:** Revenue as North Star optimizes for extraction. Vanity metrics (total
users) provide no signal. Should change rarely -- quarterly changes mean it is not
truly north.

---

## OKR-to-Metrics Mapping

Connecting Objectives and Key Results to instrumented metrics.

**Alignment chain:** Company Objective -> Team Key Result -> Metric -> Events.
Example: Objective "Preferred tool for data teams" -> KR "Weekly active teams
500 to 800" -> Metric: teams with 2+ active users in 7 days -> Event: user_logged_in.

**Verification:** Each KR must have: (1) unambiguous metric definition, (2) reliable
pipeline, (3) dashboard, (4) review cadence. Common failure: OKRs set without
instrumented metrics, discovered at quarter-end.

---

## Leading vs Lagging Indicators

**Lagging:** Outcomes already occurred (revenue, churn, NPS). Too late to change.

**Leading:** Predict future outcomes. Feature adoption in week 1 predicts month-3
retention. Support ticket volume predicts churn.

**Early warning:** Establish correlations between leading and lagging using
historical data. Monitor leading indicators weekly. When one degrades, intervene
before the lagging indicator reflects damage.

**Caution:** Validate causal links with experiments before building strategy on them.

---

## Input vs Output Metrics

**Input metrics:** Activities and behaviors you can directly control. Number of
experiments run, features shipped, sales calls made, support response time.

**Output metrics:** Results you want to achieve but cannot directly manipulate.
Revenue, retention, NPS, market share.

**Linking them:** Map each output metric to the input metrics believed to drive it.
"We believe that reducing onboarding time (input) will increase Day-30 retention
(output)." Track both. If input metrics improve but output metrics do not, the
hypothesis is wrong.

---

## Counter-Metrics and Guardrail Metrics

Preventing optimization of one metric from damaging others.

**Definition:** For every optimized metric, define counter-metrics that must not
regress. Optimizing conversion? Guardrail: support tickets. Optimizing load time?
Guardrail: feature completeness.

**In experiments:** Every A/B test defines guardrails alongside the primary metric.
Do not ship a variant that degrades a guardrail without deliberate discussion.

**Organizational guardrails:** Revenue teams: satisfaction. Growth teams: revenue.
Product teams: performance.

---

## Metric Hierarchy

Organizing metrics across organizational levels.

**Company level:** 3-5 KPIs visible to leadership. North Star metric plus
supporting financial and customer metrics. Updated monthly or quarterly.

**Team level:** 5-8 metrics specific to the team's domain. Feature adoption,
funnel conversion, cycle time. Updated weekly.

**Feature level:** Metrics tied to a specific feature or experiment. Task completion
rate, engagement with a new UI component. Updated daily or in real-time. These
metrics have a limited lifespan -- they are retired when the feature stabilizes.

**Rolling up vs drilling down:** Higher-level metrics should be decomposable into
lower-level ones. If company-level retention drops, teams should be able to drill
into their segment-specific retention to identify the source.

---

## Metric Lifecycle

Metrics are not permanent. They have a lifecycle that must be managed.

1. **Define:** Write an unambiguous definition including calculation formula,
   data source, filters, and time window. Two people reading the definition should
   produce the same number.
2. **Instrument:** Implement the tracking events and processing logic. Validate
   against known data or manual counts.
3. **Validate:** Compare the metric output to expected values. Check edge cases:
   what happens with zero values, null properties, duplicate events?
4. **Baseline:** Collect 4-8 weeks of data before setting targets. The baseline
   reveals natural variance and seasonality.
5. **Target:** Set targets based on baseline data and strategic goals. Targets
   should be ambitious but grounded in historical performance.
6. **Monitor:** Display on dashboards, review at regular cadence, alert on
   anomalies.
7. **Retire:** When a metric no longer informs decisions, remove it. Dead metrics
   on dashboards create noise and erode trust in the metrics that matter.

---

## Common Pitfalls

**Ambiguous definitions:** "Active user" means different things to different teams.
Define precisely: "A user who performed at least one value action in a 7-day
rolling window, excluding automated actions."

**Changing definitions:** If you change how a metric is calculated, restate the
baseline. Comparing old-definition data to new-definition data produces misleading
trends. Mark the change point visibly on charts.

**Gaming metrics:** When a metric becomes a target, people optimize for the metric
rather than the underlying goal. Pair every target metric with a counter-metric.
Rotate which metrics receive attention. Watch for sudden jumps that lack a clear
causal explanation.
