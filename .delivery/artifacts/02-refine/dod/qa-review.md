# QA Review -- PRD: MTG Commander Deck Builder Plugin v1.1

**Reviewer**: QA Engineer (Legolas)
**Date**: 2026-04-01
**Gate**: Gate 2 (Refine DoD)
**PRD Version**: 1.1 (revised)
**Verdict**: DONE

---

## Blocking Criteria

| Criterion | Result | Notes |
|-----------|--------|-------|
| Requirements testable | PASS | All 7 FRs (FR-01 through FR-07) and 7 NFRs have explicit, verifiable ACs. Each maps to a concrete verification: Scryfall API calls, numeric counts, file existence checks, structured PASS/FAIL verdicts, plugin-validator execution. No AC relies on subjective judgment. |
| ACs specific and measurable | PASS | 52 ACs reviewed across FR-01 through FR-07. Zero branching language. Test Case 1 now uses a single deterministic commander (K'rrik). FR-02.6 includes a disambiguation rule for dual-purpose cards (greatest structural deficit, then primary function). All numeric thresholds are explicit. |
| Previous evaluation findings addressed | PASS | All 13 findings from Round 1 evaluation and adversarial challenge verified as addressed in PRD v1.1. See disposition table below. |

---

## Previous Findings Disposition (13 of 13 addressed)

### Evaluation Round 1 Findings

| # | Finding | Severity | Status | PRD Location |
|---|---------|----------|--------|--------------|
| F1 | Test Case 1 "either...or" commander | Blocking | FIXED | Section 8, Test Case 1 -- K'rrik is sole commander |
| F2 | Dual-purpose card categorization undefined | Blocking | FIXED | FR-02.6 -- disambiguation rule added (greatest structural deficit, then primary function) |
| F3 | Success metrics lack baselines/targets | Blocking | FIXED | Section 2 -- Goals table rebuilt with Metric, Baseline, Target, Measurement columns |
| F4 | Missing price data handling | Warning | FIXED | FR-05.8 added -- null price fallback to cheapest non-foil printing, "price unavailable" flag |
| F5 | Banned commander not caught at intake | Warning | FIXED | FR-02.3a added -- banned list check at intake with halt and prompt |
| F6 | Empty Card Finder results undefined | Warning | FIXED | FR-06.9 added -- empty result set with echoed query, consuming agents note "no replacement found" |
| F7 | 100-card invariant during corrections | Warning | FIXED | FR-07.2 updated -- corrected decklist must satisfy FR-02.5, Rules Judge re-validates count |
| F8 | Synergy score threshold undefined | Observation | DEFERRED | Correctly left to Design via OQ-2. Test cases reference >= 3.0 consistently. |

### Adversarial Challenge Findings

| # | Finding | Severity | Status | PRD Location |
|---|---------|----------|--------|--------------|
| C1 | Synergy scoring untestable ("interacts meaningfully" undefined) | Must Fix | FIXED | FR-04.1 -- Synergy Interaction Taxonomy added with 6 categories (Triggers, Enables, Protects, Combos-with, Amplifies, Feeds) and 3 explicit exclusions |
| C2 | Card hallucination pre-validation | Recommended | FIXED | FR-02.9 added -- Deck Builder SHOULD validate names via Card Finder during construction |
| C3 | Scryfall batch API support | Recommended | FIXED | FR-06.8 added -- `/cards/collection` endpoint, up to 75 identifiers per request |
| C4 | Budget/synergy correction oscillation | Must Fix | FIXED | FR-07.4 updated -- budget compliance takes priority, synergy threshold relaxes to 2 interactions for budget-forced replacements, output warns |
| C5 | Insufficient test cases (no multi-color, no correction loop) | Recommended | FIXED | Test Cases 4 (Korvold, 3-color, $200) and 5 (Atraxa, 4-color, $50 stress) added |
| C6 | Partner commanders unresolved | Recommended | FIXED | FR-02.10 added (reject at intake), OQ-5 resolved as out-of-scope, v2+ deferral entry added |

---

## Observations (Non-Blocking)

1. **Synergy Interaction Taxonomy is well-structured.** The 6 categories with explicit exclusions (shared creature type, generic mana enablement, "both good cards") give the Optimization Reviewer deterministic counting rules. Design retains authority to refine or extend the taxonomy per the noted responsibility clause.

2. **Test case coverage is now strong.** 5 cases spanning mono-color, 2-color, 3-color, and 4-color identities, budgets from $50 to $200, power levels 5-8, and per-card caps. Test Case 5 specifically exercises the budget/synergy constraint negotiation and correction loop.

3. **Goals table links directly to test cases.** Baselines are 0 (GREENFIELD), targets reference the 5 dogfooding cases, and measurement methods point to specific agent outputs. G-06 (plugin validation) is independently verifiable.

---

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/02-refine/dod/qa-review.md
SUMMARY: Gate 2 QA PASS. All 3 blocking criteria met. All 13 previous findings (8 evaluation + 5 adversarial) verified as addressed in PRD v1.1. No new blocking issues.
```
