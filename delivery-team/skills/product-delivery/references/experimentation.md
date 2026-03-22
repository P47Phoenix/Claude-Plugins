# Experimentation

A systematic approach to product experimentation. Experiments replace opinions with
evidence. The goal is learning, not winning.

---

## Hypothesis Template

Every experiment starts with a falsifiable hypothesis. Use this structure:

"If we [make this specific change], then [this metric will change by this amount],
because [this is the rationale based on user behavior or data]."

**Example:** "If we reduce the signup form from 5 fields to 3, then completion rate
will increase by 15%, because 40% of users abandon at field 4."

**Requirements:** Change must be specific. Metric must be instrumented. Effect size
must be stated -- "will improve" is a wish, not a hypothesis. Rationale grounded
in data or research.

---

## A/B Test Design

The standard controlled experiment for product changes.

**Control vs treatment:** Control sees existing experience. Treatment sees the
change. Both randomly assigned from the same population.

**Random assignment:** Deterministic hash of user_id + experiment_id ensures random,
consistent, reproducible assignment. Use server-side assignment when possible.

**Independence:** Each user in only one variant. Cross-contamination across sessions
or devices invalidates results.

**Duration:** At least 1-2 full business cycles (2-4 weeks). Do not stop early
unless using a valid sequential testing method.

---

## A/B/n Tests

Testing multiple treatments simultaneously.

**Multiple treatments:** Test several variants simultaneously rather than
sequentially to save time.

**Correction for multiple comparisons:** False positive probability increases with
N variants. Apply Bonferroni (strict) or Benjamini-Hochberg (less conservative).

**Traffic allocation:** Equal split among all variants including control. Each must
receive enough traffic for the required sample size.

---

## Sample Size Calculation

Determine the required sample size before starting the experiment.

**Inputs:**
- **Baseline conversion rate:** Current metric value (e.g., 5% signup rate).
- **Minimum detectable effect (MDE):** Smallest change worth detecting. Smaller
  MDEs require larger samples.
- **Statistical power:** Standard 80%, use 90% for high-stakes experiments.
- **Significance level:** Standard 5% (two-tailed).

**Practical guidance:** For a 5% baseline with 10% relative MDE, 80% power, 5%
significance: approximately 30,000 users per variant. If traffic is insufficient,
increase MDE or use a more sensitive metric. Do not skip this step -- under-powered
experiments waste time.

---

## Statistical Significance

Interpreting experiment results correctly.

**P-value:** Probability of observing this result assuming no real effect. p=0.03
means 3% chance by random chance. It does not mean 97% chance the treatment works.

**Confidence intervals:** Report alongside p-values -- they convey both significance
and magnitude. A 95% CI means 95% of repeated experiments would contain the true
effect.

**Practical vs statistical significance:** A 0.1% improvement can be statistically
significant with enough data but not worth the engineering cost. Evaluate whether
the effect size matters for the business.

---

## Bayesian vs Frequentist Approaches

Two valid paradigms for experiment analysis with different trade-offs.

**Frequentist:** Fixed sample size. P-values and confidence intervals. Cannot peek
without inflating false positives. Well-understood, widely supported.

**Bayesian:** Probability that treatment is better, given observed data. Allows
early stopping with valid inference. Reports credible intervals.

**When to use Bayesian:** Quick decisions needed, low traffic, or stakeholders find
"85% probability B is better" more intuitive than "p = 0.04."

**When to use frequentist:** Regulatory requirements, simple framework preferred,
or limited Bayesian tooling support.

---

## Guardrail Metrics

Metrics that must not regress, even if the primary metric improves.

**Common guardrails:** Revenue per user, error rate, latency, support contact rate,
unsubscribe rate.

**Decision framework:** If the treatment improves the primary metric but degrades a
guardrail beyond threshold, do not ship. Investigate whether the impact is causal
and whether the treatment can be modified.

---

## Experiment Lifecycle

A repeatable process from idea to organizational learning.

1. **Hypothesis:** Specific, falsifiable, with expected effect size.
2. **Design:** Sample size, primary metric, guardrails, analysis method.
3. **Implement:** Feature flags, QA both variants, verify instrumentation in staging.
4. **Run:** Small ramp (5-10%) first, then full allocation. Monitor guardrails
   daily; do not analyze primary metric until sample size is reached.
5. **Analyze:** Compare variants, check guardrails, segment by key dimensions.
6. **Decide:** Ship, iterate, or abandon. Document rationale.
7. **Document:** Record everything in the experiment registry.

---

## Common Pitfalls

**Peeking at results:** Inflates false positive rate from 5% to 20-30%. Commit to
fixed sample size or use sequential testing designed for continuous monitoring.

**Stopping early:** Biases effect estimates upward. Early significant results are
disproportionately likely to be overestimates.

**Selection bias:** Non-random assignment invalidates results. Verify with a sample
ratio mismatch (SRM) check -- if 50/50 shows 52/48, the assignment is broken.

**Novelty effect:** Users engage more with new designs simply because they are new.
Run 2+ weeks for novelty to wear off.

**Seasonality:** Run for full weekly cycles to avoid confounding day-of-week effects.

---

## Feature Flag Integration

Feature flags are the delivery mechanism for experiments.

**Experiment assignment:** Feature flag system assigns users and records assignment,
replacing custom experiment code.

**Gradual rollout:** Ramp the winner from 50% to 100% over 2-3 days post-experiment.

**Kill switch:** Every variant must be instantly disableable without a code deploy.

---

## Organizational Experiment Culture

Building a team and company that learns through experimentation.

**Learning over winning:** Negative and null results are valuable -- they prevent
investing in ideas that do not work. Celebrate learning, not just wins.

**Sharing results:** Publish all results (positive, negative, null) organization-
wide. A weekly digest prevents teams from re-running concluded experiments.

**Experiment registry:** Central database of all experiments. Without it, teams
repeat failures and lose successful insights.

**Velocity target:** Set a throughput goal (e.g., 10 experiments per team per
quarter) to normalize experimentation as a default practice.
