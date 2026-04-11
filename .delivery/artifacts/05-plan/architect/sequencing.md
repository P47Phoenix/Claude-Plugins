# Implementation Sequencing: MTG Commander Adversarial Review

**Stage:** 05-Plan | **Role:** Architect (Celebrimbor) | **Plugin:** mtg-commander
**Pipeline:** run-2026-04-11-e6f3

---

## Dependency Graph

```
US-1 (Challengers) --+--> US-2 (Loop Protocol)
                     +--> US-5 (DEFECT-001)
                     +--> US-6 (DEFECT-002)
                     +--> US-7 (Guardrail Section)
                     +--> US-8 (Reference Guides)

US-3 (Config) ----------> US-4 (Price Rules)
                     +--> US-8 (Reference Guides)

US-7 (Guardrail) -------> US-9 (Dogfood Verification)
```

## Critical Path

```
US-1 (3) -> US-2 (3) -> US-8 (1) -> US-9 (0) = 7 pts, 3 sprints
```

US-1 is the single bottleneck. All functional stories depend on challenger templates existing.

---

## Sequencing Rationale

### Sprint 1: Two Independent Pillars

US-1 and US-3 share zero coupling. US-1 adds challenger agent sections to SKILL.md. US-3 adds config loading protocol + schema reference doc. Both modify SKILL.md but in different sections (no merge conflict risk).

### Sprint 2: Dependent Chains Converge

US-2 wires US-1's challengers into a loop protocol. US-5 specializes US-1's Rules Challenger with deterministic validation. US-4 consumes US-3's config for `max_card_price`. All three are independent of each other.

### Sprint 3: Integration + Hardening

US-6, US-7, US-8 all augment existing sections. US-9 is pure verification (zero cost). Sequenced last because US-8 aggregates changes from US-4, US-5, US-6 into reference guides.

---

## File Contention Map

| File | Stories | Conflict Risk |
|------|---------|---------------|
| `mtg-commander/SKILL.md` | US-1,2,3,4,7 | Low -- different sections |
| `references/price-evaluator-guide.md` | US-4, US-6, US-8 | None -- sequential sprints |
| `references/rules-judge-guide.md` | US-5, US-8 | None -- sequential sprints |
| `references/config-reference.md` | US-3 (creates), US-8 (reviews) | None |

---

## Architectural Guardrails for Development

1. **Section isolation:** Each challenger gets its own H3 in SKILL.md. Do not inline challenger prompts into primary agent sections.
2. **Config is read-only at runtime:** Values read once at pipeline start. No mid-pipeline reloads.
3. **Additive only:** Existing pipeline sections (intake, correction cycle, output format) augmented, never rewritten. Core agent prompts preserved per constraints.yml invariant.
4. **Version field mandatory:** `references/config-reference.md` must document `version: 1` and forward-compat contract (unknown keys warned, not rejected).
