# Analytics Patterns

Core patterns for product analytics instrumentation, analysis, and data quality.
Good analytics is intentional: track what informs decisions, not everything possible.

---

## Event Taxonomy

Consistent naming is the foundation of usable analytics.

**Naming convention: object_action.** Noun + past-tense verb: page_viewed,
button_clicked, order_completed, search_performed.

**Property standards:** Base properties on every event: timestamp, user_id (or
anonymous_id), session_id, platform, app_version. Feature-specific properties added
per event (page_viewed carries page_name and referrer).

**Versioning events:** When schema changes, increment a schema_version property.
Never silently change semantics -- a button_clicked that starts including auto-
triggered clicks breaks every downstream analysis.

**Governance:** Maintain a central event dictionary. Every new event requires a
purpose statement: "This event measures X for decision Y."

---

## Instrumentation Plans

Systematic approach to deciding what to track and how.

**What to track:** Start from decisions, not features. "What decisions will this
data inform?" Work backward from business questions to events.

**Where to track:** Client-side for UI interactions. Server-side for business logic
events (more reliable -- immune to ad blockers and network issues).

**Implementation checklist:**
1. Define events in the tracking plan.
2. Review with analytics and product stakeholders.
3. Implement with unit tests verifying event payloads.
4. Validate in staging: volume, property completeness, value distributions.
5. Monitor post-launch: alerts for missing events or schema violations.

---

## Funnel Analysis

Measuring conversion through a sequence of steps.

**Define funnel stages:** Sequential events in the user journey. Example:
product_viewed -> add_to_cart -> checkout_started -> payment_submitted -> confirmed.

**Conversion rates:** Step-by-step and overall (first to last). The largest absolute
drop-off is the biggest opportunity.

**Segmented analysis:** Compare funnels by device, user type, traffic source. A 60%
mobile checkout drop-off vs 20% desktop points to a mobile UX issue.

---

## Cohort Analysis

Grouping users by shared characteristics to track behavior over time.

**Time-based cohorts:** Group users by their signup week or month. Track a metric
(retention, revenue, feature usage) over subsequent periods. Comparing cohorts
reveals whether the product is improving for new users over time.

**Behavioral cohorts:** Group users by actions taken (completed onboarding, used
feature X in first week, invited a teammate). Compare outcomes between cohorts
to identify which behaviors predict long-term retention.

**Retention curves:** Plot the percentage of each cohort that remains active over
time. A flattening curve indicates a retained core. A curve that never flattens
indicates the product has not found retention-worthy value.

**Comparing cohorts:** Overlay retention curves for different cohorts. If recent
cohorts retain better, product changes are working. If a behavioral cohort retains
dramatically better, that behavior is a candidate for an activation metric.

---

## Segmentation

Dividing users into meaningful groups for targeted analysis and action.

**Demographic:** Age, location, language, company size. Useful for market analysis
but often less predictive of in-product behavior than behavioral segments.

**Behavioral:** Actions taken in the product. Power users vs casual users, feature
adopters vs non-adopters. Most actionable for product decisions.

**RFM analysis:** Recency (last activity), Frequency (activity count), Monetary
(revenue contribution). Score users on each dimension. High-RFM users are your
champions; low-RFM users are at risk.

**Segment-based reporting:** Every top-level metric should be breakable by key
segments. "DAU increased 10%" is less useful than "DAU increased 15% in the
enterprise segment and decreased 5% in SMB."

---

## Data Pipeline Patterns

Moving data from collection to consumption reliably.

**Event collection:** Client SDKs buffer and batch-send events. Server-side events
go directly to the pipeline.

**Processing:** Validate against schemas, enrich with derived properties (session
attribution, geo-IP), deduplicate using event IDs.

**Storage:** Raw events in a data lake (flexibility). Aggregated data in a warehouse
(performance). Pre-computed metrics in a serving layer (dashboards).

**Batch vs streaming:** Batch (hourly/daily) is simpler and cheaper. Streaming is
necessary for alerting and real-time dashboards. Most teams need both.

---

## Data Quality Checks

Bad data is worse than no data -- it drives confident wrong decisions.

- **Completeness:** Are expected events arriving? Monitor event volume over time.
  A sudden drop indicates an instrumentation regression.
- **Uniqueness:** Are events duplicated? Check for duplicate event IDs within
  time windows.
- **Timeliness:** Are events arriving within expected latency? Late-arriving events
  can skew real-time dashboards.
- **Consistency:** Do related events tell coherent stories? An order_completed event
  without a preceding checkout_started event indicates a gap.
- **Validity:** Are property values within expected ranges? Negative order values,
  timestamps in the future, or enum values not in the schema all indicate bugs.
- **Automated monitoring:** Run quality checks on every batch load. Alert on
  threshold breaches. Quarantine suspect data rather than loading it silently.

---

## Attribution Modeling

Assigning credit for conversions to touchpoints in the user journey.

- **First-touch:** 100% credit to the first interaction. Favors awareness channels.
- **Last-touch:** 100% credit to the last interaction before conversion. Favors
  closing channels. Simple but misleading.
- **Linear:** Equal credit to all touchpoints. Simple and fair but assumes all
  touches are equally influential.
- **Time-decay:** More credit to recent touchpoints. Reasonable default when you
  lack the data for a custom model.
- **Data-driven:** Machine-learned attribution based on actual conversion paths.
  Requires significant data volume. Most accurate but least transparent.

**Practical guidance:** Start with last-touch (simple, universally available). Add
first-touch for comparison. If the two tell very different stories, invest in
time-decay or data-driven modeling.

---

## User Journey Analysis

Understanding the paths users take through the product.

**Path analysis:** Visualize the most common sequences of events after a starting
point. Identify unexpected paths -- users finding workarounds indicate UX failures.

**Friction point identification:** Where do users pause, retry, or abandon? Long
gaps between events in a flow indicate confusion. Repeated events (form_submitted
multiple times) indicate errors. Back-and-forth navigation indicates lost users.

---

## Common Analytics Anti-Patterns

- **Vanity metrics:** Total signups, page views only go up. Replace with active
  usage, retention, engagement.
- **Survivorship bias:** Analyzing only current users ignores those who left.
- **Correlation as causation:** Users of feature X retain better -- but did X cause
  retention, or do engaged users find X? Use experiments to distinguish.
- **P-hacking:** Testing segments until one shows significance. With 20 segments at
  p<0.05, expect one false positive by chance.
