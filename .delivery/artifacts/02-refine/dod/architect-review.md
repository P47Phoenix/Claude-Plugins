# Architect DoD Review -- PRD: MTG Commander Deck Builder Plugin v1.1

**Reviewer**: Architect (Celebrimbor)
**Date**: 2026-04-01
**Artifact**: `.delivery/artifacts/02-refine/po/prd.md` (v1.1)
**Status**: DONE

---

## Gate 2 Architect Criteria

### 1. Technically Feasible, No Blockers

- [x] **Technically feasible, no blockers** [blocking]

| Feasibility Area | Assessment |
|-----------------|------------|
| FR-01 (Plugin Structure) | Feasible. Standard plugin skeleton (`mtg-commander/`, SKILL.md, LICENSE.txt, subdirectories). Follows established repo conventions exactly. No novel structural patterns. |
| FR-02 (Deck Builder Agent) | Feasible. 7-question intake with Scryfall validation is straightforward. Commander validation via `/cards/named` (exact match) is a single API call. Category disambiguation rule is deterministic. Partner rejection (FR-02.10) is a simple keyword check on oracle text. |
| FR-03 (Rules Judge Agent) | Feasible. All validation rules map directly to Scryfall API fields: `legalities.commander`, `color_identity`, `name`. Banned list is a static reference file lookup. Synergy rationale validation (FR-03.7) against oracle text is the most complex check but is bounded -- it validates claims against card text, not open-ended reasoning. |
| FR-04 (Optimization Reviewer) | Feasible. Synergy Interaction Taxonomy (6 categories) is well-defined with explicit exclusions. Structural minimums are static thresholds. Synergy scoring formula is arithmetic (total connections / non-land cards). Mana curve distribution is a count-and-bucket operation. |
| FR-05 (Price Evaluator) | Feasible. Scryfall returns USD pricing per printing. Cheapest-printing selection requires iterating printings. Null-price handling (FR-05.8) is specified. Budget math is summation and comparison. |
| FR-06 (Card Finder Utility) | Feasible. Python script using `urllib` against Scryfall REST API. Rate limiting (50ms delay) is a `time.sleep(0.05)`. Batch endpoint (`/cards/collection`, 75 per request) is documented Scryfall functionality. Retry with exponential backoff is standard pattern. |
| FR-07 (Orchestration) | Feasible. Sequential agent pipeline with correction loops reuses existing `pipeline.max_self_correction` config. Budget-over-synergy priority rule (FR-07.4) is a clear precedence -- no ambiguity. 100-card invariant during corrections is enforceable by the Rules Judge re-validating count each cycle. |
| Scryfall API dependency | No blocker. Scryfall is free, well-documented, stable, and requires no API key. Rate limit (10 req/sec) is generous for deck-building volumes. `api.scryfall.com` WebFetch permission is a user config step. |

**No technical blockers identified.** The plugin is a SKILL.md orchestrator + 4 agent definitions + 1 Python script (Card Finder) + 6 reference files. All agent logic is prompt-driven with Scryfall as the sole external dependency.

### 2. NFRs Realistic

- [x] **NFRs realistic** [blocking]

| NFR | Assessment |
|-----|-----------|
| NFR-01 (Scryfall rate limiting) | Realistic. 50ms minimum delay is trivial (`time.sleep`). Batch endpoint reduces call volume for full-deck operations. |
| NFR-02 (No external Python dependencies) | Realistic. `urllib`, `json`, `time` are stdlib. Scryfall returns JSON over HTTPS -- no parsing libraries needed beyond stdlib. |
| NFR-03 (Card name accuracy) | Realistic. Rules Judge validates every name against Scryfall. Deck Builder pre-validates during construction (FR-02.9). Two-layer defense is sound. Zero-tolerance gate is enforceable because Scryfall `/cards/named?exact=` returns 404 for non-existent names. |
| NFR-04 (Plugin validation) | Realistic. Plugin structure follows established conventions. Zero errors/warnings is achievable with correct structure. |
| NFR-05 (Internet required) | Realistic. Documented constraint, not a technical challenge. |
| NFR-06 (Scryfall error resilience) | Realistic. Exponential backoff with max 3 retries is a standard pattern. `urllib` handles HTTP status codes natively. |
| NFR-07 (Session completion) | Realistic with caveat. A full pipeline run with correction cycles involves multiple Scryfall API calls (100+ cards validated, priced, searched). With batch endpoints and 50ms delays, API time is bounded (~5-10 seconds for a full deck validation). Agent reasoning time dominates. Single-session completion is achievable for the 3-cycle correction limit. |

**All NFRs are achievable within the stated scope.**

---

## Open Questions (Architect-Relevant)

OQ-3 and OQ-4 are flagged for the Architect stage. Brief pre-assessment:

- **OQ-3** (`/cards/search` vs `/cards/named` for name validation): `/cards/named?exact=` is the correct choice for validation -- returns 200 or 404, no ambiguity. `/cards/search` is for discovery queries (Card Finder's replacement suggestions). Both endpoints will be needed for different purposes.
- **OQ-4** (Double-faced / split / adventure cards): Scryfall handles these with `card_faces` array and `//` in names. Card Finder should accept either the full name or the front face name. Design should specify the canonical name format used in decklists.

These are solvable in the Architect stage with no feasibility risk.

---

## Verdict

**DONE.** The PRD is technically feasible with zero blockers. All components map to proven patterns: SKILL.md orchestration, prompt-driven agents, Python stdlib HTTP client, static reference files. Scryfall API is a reliable, free, well-documented external dependency. All 7 NFRs are realistic and achievable. Two open questions (OQ-3, OQ-4) are tractable and deferred to Architect stage.

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/02-refine/dod/architect-review.md
SUMMARY: Gate 2 DONE. All FRs feasible (SKILL.md + agents + 1 Python script + reference files). Scryfall API is sole external dependency, no blockers. All 7 NFRs realistic. OQ-3 and OQ-4 tractable for Architect stage.
```
