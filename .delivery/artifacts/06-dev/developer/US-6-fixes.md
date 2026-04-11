# US-6 Dogfood Fixes — Developer Log

**Date:** 2026-04-08
**Author:** Gimli (delivery-team:developer)
**Story:** US-6

## Fixes Applied

### Gap 1: Decomposition Hygiene sidebar for volatility paradigm

**File:** `delivery-team/skills/architect/paradigms/volatility/references/volatility-decomposition.md`
**Problem:** DDD paradigm had a Decomposition Hygiene sidebar (added in run a1f3) but the volatility paradigm did not. Golden Rule §0 guards against functional decomposition but not against implementation-detail contamination (naming components after AWS/infra tokens).
**Fix:** Added a Decomposition Hygiene callout after §0. Lists forbidden vocabulary (Lambda, ECR, ECS, SQS, etc.) and explains the distinction: §0 guards against verbs, the sidebar guards against infrastructure nouns.

### Gap 2: Volatility-specific domain discovery reference

**File (new):** `delivery-team/skills/architect/paradigms/volatility/references/domain-discovery-volatility.md`
**Problem:** Shared `domain-discovery.md` had volatility questions but the volatility paradigm had no local quick-reference. DDD paradigm benefits from co-located references; volatility paradigm did not.
**Fix:** Extracted the four-step volatility interview (16 questions) plus the five-axis checklist into a focused 50-line reference under the volatility paradigm directory. Points back to the shared file for full protocol.

## Verification

- [x] Sidebar matches DDD pattern (shield emoji, forbidden vocabulary list, stage guidance)
- [x] New file under 60 lines (50 lines)
- [x] No implementation-detail vocabulary leaked into decomposition guidance
