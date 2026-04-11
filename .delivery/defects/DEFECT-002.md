# DEFECT-002: Price Evaluator uses only Scryfall/TCGPlayer pricing — Card Kingdom prices diverge significantly

**Pipeline**: run-2026-04-02-k3r9
**Test Case**: TC-2 (Karlov Orzhov Lifegain)
**Severity**: Major (budget compliance)
**Category**: Incomplete pricing validation

## Description
TC-2 reports $97.37 total (under $100 budget) using Scryfall's `prices.usd` field (TCGPlayer market price). However, the same deck costs over $150 on Card Kingdom — a 50%+ price divergence. Users who buy from Card Kingdom will exceed their stated budget.

## Evidence
- Price Evaluator reports: $97.37 (TCGPlayer market via Scryfall)
- Card Kingdom total for same deck: $150+ (user-reported)
- The user's original spec lists Card Kingdom as an alternative pricing source

## Root Cause
The PRD (FR-05) and architecture (ADR-002) scoped v1 to Scryfall-only pricing (which reflects TCGPlayer market prices). Card Kingdom pricing is not checked. The user's original spec explicitly lists Card Kingdom as an expected pricing source:

> | Card Kingdom | https://www.cardkingdom.com | Price Evaluator |

## Impact
Budget compliance is only valid for TCGPlayer. Users purchasing from Card Kingdom, local game stores, or other vendors may significantly exceed their stated budget. The "budget compliant" success criterion is vendor-specific, not absolute.

## Suggested Fix
1. **Short-term (v1 patch)**: Add a disclaimer to Price Evaluator output: "Prices reflect TCGPlayer market values via Scryfall. Card Kingdom and other vendors may differ significantly."
2. **Long-term (v2)**: Add multi-source pricing as planned in PRD v2 scope — check Card Kingdom and/or aggregate pricing from Moxfield/Archidekt

## Classification
This was a known v1 scope limitation (single-source pricing) that surfaced as a user experience gap during UAT. Not a code bug — it's a PRD scope gap that needs a UX mitigation in v1.

**Status: CLOSED** — fixed in run-2026-04-11-e6f3 (commit TBD). Price Challenger fetches CK independently, divergence >30% escalated.
