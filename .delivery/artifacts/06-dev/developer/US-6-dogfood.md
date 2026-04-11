# US-6 Dogfood Report -- Volatility Paradigm Skill Design Validation

**Author:** Gimli (Developer)
**Date:** 2026-04-08
**Type:** Design validation (not a live decomposition run)

---

## 1. Context Isolation Proof

**Paradigm skill loads (4 files):**

| # | File | Lines |
|---|------|-------|
| 1 | `paradigms/volatility/SKILL.md` | 66 |
| 2 | `paradigms/volatility/references/volatility-decomposition.md` | 260 |
| 3 | `references/architecture-patterns.md` (shared_ref) | 180 |
| 4 | `references/c4-model.md` (shared_ref) | 269 |
| 5 | `references/domain-discovery.md` (shared_ref) | 261 |
|   | **Total** | **1,036 lines** |

**Monolithic architect loads (worst case: all 27 refs + SKILL.md):**

| Item | Lines |
|------|-------|
| `architect/SKILL.md` | 667 |
| 27 reference files | 4,941 |
| **Total** | **5,608 lines** |

**Estimated reduction:** ~82% fewer lines loaded for a volatility decomposition task. No DDD, game architecture, compliance, security, incident response, privacy, or transformation refs bleed in. Context isolation holds.

---

## 2. Content Completeness

| Criterion | Present? | Location |
|-----------|----------|----------|
| Golden Rule (section 0) | YES | SKILL.md lines 17-21 AND reference lines 7-44 |
| Phase 1: Business Process Walkthrough | YES | Reference lines 92-100 |
| Phase 2: Identify Commonalities/Volatilities | YES | Reference lines 104-116 |
| Phase 3: Define Components by What They Handle | YES | Reference lines 118-127 |
| Phase 4: Validate with Real Use Cases | YES | Reference lines 130-137 |
| Phase 5: Project Planning | YES | Reference lines 140-162 |
| IDesign hierarchy (M/E/A/U) | YES | SKILL.md lines 25-37 |
| Volatility axis identification | YES | SKILL.md lines 39-49 |
| Anti-patterns | YES | Reference lines 220-228 |
| Practical checklist | YES | Reference lines 252-260 |
| Decomposition Hygiene sidebar | **NO** | Missing -- DDD paradigm has it, volatility does not |
| `domain-discovery-volatility.md` | **NO** | AC-1.4 requires it; only `volatility-decomposition.md` exists |

**Gaps found: 2**

1. **Decomposition Hygiene sidebar** (forbidden vocabulary list) was added to the DDD paradigm refs but not to volatility. The a1f3 lesson about forbidden implementation vocabulary at the decomposition stage applies equally here.
2. **`domain-discovery-volatility.md`** required by AC-1.4 is missing. The SKILL.md frontmatter points to the shared `domain-discovery.md` instead. This may be intentional (reuse shared ref), but the AC explicitly calls for a volatility-specific extract.

---

## 3. Router Test

Trace for `architecture.decomposition: volatility` in config:

1. Router checks ADR-002 priority chain level 1 (explicit user intent) -- no match.
2. Level 2: reads `architecture.decomposition` from config -- finds `volatility`.
3. Router looks up `paradigms/volatility/SKILL.md` -- file exists.
4. Spawns `Agent` with: volatility SKILL.md + shared_refs (`architecture-patterns.md`, `c4-model.md`, `domain-discovery.md`) + task context.
5. Non-decomposition tasks (`review`, `document`, etc.) bypass routing -- documented in SKILL.md line 202.

**Result:** Router logic traces correctly. AC-6.5 (ADR-002 priority chain level 2) would be satisfied.

---

## 4. Backwards Compatibility Test

Scenario: architect invoked WITHOUT `architecture.decomposition` in config.

1. Priority chain level 1: no explicit user intent detected.
2. Level 2: config key absent or set to `auto`.
3. Level 3: decision matrix fallback evaluates `domain_complexity`, `change_rate`, `team_size`, `deploy_independence` to recommend a paradigm.
4. If `paradigms/` directory does not exist: falls back to inline logic with monolithic refs (SKILL.md line 206). No breakage.
5. Redirect stubs at original paths (`references/volatility-decomposition.md`) point to new location with human-readable message.

**Result:** Backwards compatibility holds. Pre-migration and no-config states both fall back gracefully.

---

## Summary

| Aspect | Verdict |
|--------|---------|
| Context isolation | PASS -- 82% reduction, no cross-paradigm bleed |
| Content completeness | PARTIAL -- 2 gaps (hygiene sidebar, domain-discovery-volatility.md) |
| Router wiring | PASS -- ADR-002 priority chain traces correctly |
| Backwards compat | PASS -- fallback to inline logic documented and functional |
