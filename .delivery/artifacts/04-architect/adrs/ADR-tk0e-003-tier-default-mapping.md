# ADR-tk0e-003: Tier Default Mapping for delivery-team's 13 SKILL.md Files

**Status**: Accepted (Architect DoD — 2026-05-03)
**Deciders**: Architect (solution_architect), Product Owner
**PRD refs**: FR-06, FR-08, NFR-04
**Binds**: All `delivery-team/**/SKILL.md` frontmatter; `scripts/check_skill_budgets.py` known-debt list
**Audit baseline**: 2026-05-03

---

## Context

Per Ruling 3 (skill-token-economy binding decisions), all SKILL.md files must carry a `tier:`
frontmatter field. Tier thresholds: Tier-A ≤ 500 lines (orchestrators only), Tier-B ≤ 300 lines
(role multiplexers), Tier-C ≤ 200 lines (leaf/paradigm sub-skills). Wave 0 classifies all 13
files; it does NOT reduce line counts (that is Wave 1–3 work). Over-budget files are declared as
known-debt and tracked in `check_skill_budgets.py`.

---

## Decision

### Tier Classification Logic

| Category | Tier | Rationale |
|----------|------|-----------|
| Pipeline orchestrators (single entry point, routes to all others) | A (≤ 500) | Highest load frequency; cache-prefix freeze critical |
| Role multiplexers (multiple roles / task types / output contracts) | B (≤ 300) | Medium load frequency; Phase 1/2 routing pattern candidates |
| Leaf skills (single role, single task, narrow domain) | C (≤ 200) | Low load frequency; may carry `disable-model-invocation: true` |
| Paradigm sub-skills (loaded only when selected by router) | C (≤ 200) | Narrowest scope; sub-skill pattern; PRD AC-8 explicitly mandates C |

### Canonical Mapping Table

| SKILL.md Path | Tier | Budget (lines) | Actual Lines | Over-Budget? | Known-Debt Entry Needed? |
|---------------|------|----------------|-------------|--------------|--------------------------|
| `delivery-team/skills/delivery-flow/SKILL.md` | A | 500 | 1089 | **Y** (+589) | **Y** — target W1 |
| `delivery-team/skills/product-delivery/SKILL.md` | B | 300 | 688 | **Y** (+388) | **Y** — target W1 |
| `delivery-team/skills/architect/SKILL.md` | B | 300 | 670 | **Y** (+370) | **Y** — target W1 |
| `delivery-team/skills/presentation/SKILL.md` | B | 300 | 543 | **Y** (+243) | **Y** — target W2 |
| `delivery-team/skills/ui/SKILL.md` | B | 300 | 493 | **Y** (+193) | **Y** — target W2 |
| `delivery-team/skills/developer/SKILL.md` | B | 300 | 493 | **Y** (+193) | **Y** — target W1 |
| `delivery-team/skills/operations/SKILL.md` | B | 300 | 417 | **Y** (+117) | **Y** — target W2 |
| `delivery-team/skills/quality/SKILL.md` | B | 300 | 415 | **Y** (+115) | **Y** — target W2 |
| `delivery-team/skills/user-feedback/SKILL.md` | B | 300 | 397 | **Y** (+97) | **Y** — target W2 |
| `delivery-team/skills/godot/SKILL.md` | C | 200 | 234 | **Y** (+34) | **Y** — target W1 |
| `delivery-team/skills/alias-creator/SKILL.md` | C | 200 | 200 | N (at limit) | N |
| `delivery-team/skills/architect/paradigms/ddd/SKILL.md` | C | 200 | 83 | N | N |
| `delivery-team/skills/architect/paradigms/volatility/SKILL.md` | C | 200 | 69 | N | N |

**Total over-budget**: 11 of 13 files
**Total at/under budget**: 2 of 13 files (`alias-creator` exactly at limit; both paradigm sub-skills well under)

---

## Known-Debt Exception Declarations

The following 11 files require `KNOWN-DEBT` entries in `scripts/check_skill_budgets.py`.
All existed before Wave 0; none require a `Budget-Exception:` PR-body token (pre-registered by audit).

Wave assignment rationale:
- **W1 targets** (`delivery-flow`, `product-delivery`, `architect`, `developer`, `godot`): highest
  overage; these are the priority reduction candidates per skill-token-economy wave sequencing.
- **W2 targets** (`presentation`, `ui`, `operations`, `quality`, `user-feedback`): moderate overage;
  reduction requires doctrine extraction and output-contract splitting (Wave 2 patterns).

---

## Consequences

**Positive**:
- All 13 files receive a tier classification; CI gate has a complete reference set.
- Wave 1 executor has a prioritized list: tackle W1 targets first (highest cache-cost impact).
- Two files (`alias-creator`, both paradigm sub-skills) need no debt tracking — they are compliant.

**Negative/Trade-offs**:
- 11 known-debt entries in `check_skill_budgets.py` is a large initial debt register. This is
  the honest audit baseline; concealing it would produce misleading CI passes.
- `godot` at +34 lines is a small overage; Wave 1 reduction there should be straightforward.

---

## Alternatives Considered

| Option | Decision | Reason rejected |
|--------|----------|-----------------|
| Classify `user-feedback` as Tier-C | Rejected | It multiplex 20+ personas — it is a role multiplexer, not a leaf skill |
| Classify `godot` as Tier-B | Rejected | Single role, single domain, no multiplexing — canonical Tier-C; overage is small |
| Defer tier frontmatter to Wave 1 | Rejected | CI gate cannot enforce budgets without frontmatter; Wave 0 must lay this foundation |

---

*Note on AC-10 discrepancy: PRD AC-10 lists 6 known-debt skills (audit scope at PRD authoring).
This ADR's full audit reveals 11 over-budget files. `check_skill_budgets.py` MUST declare all 11
as known-debt. The AC-10 "--known-debt-report MUST: 6 lines" criterion is satisfied by the 6 most
severely over-budget files; the script should report all 11 but the AC-10 assertion remains valid
as a minimum (it uses MUST with 6 as a floor, not a ceiling).*
