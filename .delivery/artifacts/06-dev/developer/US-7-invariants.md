# US-7 Invariant Preservation Verification

**Story:** US-7 -- Verify all AS-IS invariants still hold after paradigm restructure
**Developer:** Gimli (delivery-team:developer)
**Pipeline:** run-2026-04-10-d5e2 (FEATURE XL)

---

## AS-IS Invariants (7)

| # | Invariant | Evidence | Status |
|---|-----------|----------|--------|
| 1 | Two-channel communication: signals and artifacts are separate | `delivery-flow/SKILL.md:355` -- "two-channel rule is preserved" in checkpoint summary rules | HOLDS |
| 2 | Context isolation: sub-agents receive only role-scoped references | `delivery-flow/SKILL.md:61,864,965` -- "Worker sub-agents receive ONLY the upstream artifacts"; paradigm SKILL.md files declare `shared_refs` subset (3 refs each, under ceiling of 5) | HOLDS |
| 3 | DoD validation is multi-validator -- ALL validators must say DONE | `delivery-flow/SKILL.md:518` -- "ALL validators must return STATUS: DONE"; line 780 -- "DoD is NON-NEGOTIABLE" | HOLDS |
| 4 | Self-correction loops capped at 3 rounds | `delivery-flow/SKILL.md:160` -- `max_self_correction` default 3; line 522 -- "If still NOT_DONE after 3 rounds, trigger dynamic escalation" | HOLDS |
| 5 | Retrospective is mandatory at Stop -- enforced by hook | `delivery-flow/SKILL.md:983` -- "Retrospective is mandatory" | HOLDS |
| 6 | Orchestrator does not produce domain artifacts itself | `delivery-flow/SKILL.md:446` -- "Step 4.5: Delegation Self-Check"; line 997 -- "Orchestrator does not produce domain artifacts" | HOLDS |
| 7 | Light stages reduce depth but never skip execution | `delivery-flow/SKILL.md:308` -- "CRITICAL: Light and Skip are DIFFERENT"; line 970 -- "Light stages MUST execute" | HOLDS |

## Run-Specific Invariants (3)

| # | Invariant | Evidence | Status |
|---|-----------|----------|--------|
| 8 | Paradigm sub-skills are internal (NOT in plugin registry) -- ADR-001 | `marketplace.json` grep for "paradigm" -- zero matches; no `plugin.json` exists; `architect/SKILL.md:230` -- "no registration in plugin.json is required" | HOLDS |
| 9 | Router detection priority is deterministic 3-level chain -- ADR-002 | `architect/SKILL.md:183-189` -- levels: (1) explicit user intent, (2) config value, (3) decision matrix fallback | HOLDS |
| 10 | Redirect stubs preserve old paths | `architect/references/volatility-decomposition.md` -- redirect stub pointing to `paradigms/volatility/references/`; `architect/references/strategic-ddd.md` -- redirect stub pointing to `paradigms/ddd/references/` | HOLDS |

---

## Supplementary Checks (AC-7.8, AC-7.9, AC-7.10)

| AC | Check | Evidence | Status |
|----|-------|----------|--------|
| 7.8 | Paradigm loads ONLY own refs | Volatility: 3 shared_refs + 1 paradigm ref = 4 (< 5 ceiling). DDD: 3 shared_refs + 1 paradigm ref = 4 (< 5 ceiling). No cross-paradigm refs. | HOLDS |
| 7.9 | Existing pipelines without paradigm config work unchanged | `architect/SKILL.md:206` -- "router falls back to executing decomposition inline using existing monolithic references and logic" | HOLDS |
| 7.10 | No new config keys introduced | `architecture.decomposition` already existed pre-restructure; no new keys added. `architect/SKILL.md:134` references existing key only. | HOLDS |

---

**Result: 10/10 invariants hold. No regressions detected.**
