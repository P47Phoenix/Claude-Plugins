# Test Strategy — BACKLOG-005 Paradigm-as-Skill Restructure
**Role:** Legolas (QA)
**Stage:** 05-plan
**Pipeline:** run-2026-04-10-d5e2 (FEATURE XL)

## Approach
Mix of **static** (file-exists, grep, schema-check) and **empirical** (dogfood measurement, invariant audit). Static tests gate each story's DoD. Empirical tests gate US-6 (dogfood) and US-7 (invariant verification).

## Traceability Matrix

| FR | Story | Test ID | Type | Oracle |
|---|---|---|---|---|
| FR-1 | US-1 | T-1.1 | file-exists | `paradigms/volatility/SKILL.md` exists |
| FR-1 | US-1 | T-1.2 | grep | SKILL.md frontmatter contains `paradigm_id: volatility` |
| FR-1 | US-1 | T-1.3 | file-exists | `paradigms/volatility/references/volatility-decomposition.md` exists (moved) |
| FR-1 | US-1 | T-1.4 | file-exists | `paradigms/volatility/references/domain-discovery-volatility.md` exists |
| FR-1 | US-1 | T-1.5 | count | Paradigm references directory contains <=5 files (ceiling) |
| FR-2 | US-2 | T-2.1 | file-exists | `paradigms/ddd/SKILL.md` exists |
| FR-2 | US-2 | T-2.2 | grep | SKILL.md frontmatter contains `paradigm_id: ddd` |
| FR-2 | US-2 | T-2.3 | file-exists | `paradigms/ddd/references/strategic-ddd.md` exists (moved) |
| FR-2 | US-2 | T-2.4 | file-exists | `paradigms/ddd/references/domain-discovery-ddd.md` exists |
| FR-2 | US-2 | T-2.5 | count | Paradigm references directory contains <=5 files (ceiling) |
| FR-3 | US-3 | T-3.1 | grep | `architect/SKILL.md` contains router logic dispatching to `paradigms/volatility/` |
| FR-3 | US-3 | T-3.2 | grep | `architect/SKILL.md` contains router logic dispatching to `paradigms/ddd/` |
| FR-3 | US-3 | T-3.3 | grep | Router references ADR-002 priority chain: user intent > config > decision matrix |
| FR-3 | US-3 | T-3.4 | grep | Non-decomposition task types listed as bypass (review, document, evaluate, model) |
| FR-3 | US-3 | T-3.5 | grep | Fallback clause: if `paradigms/` does not exist, use inline logic |
| FR-3 | US-3 | T-3.6 | grep-absent | `plugin.json` does NOT contain `paradigm` entries (ADR-001 internal-only) |
| FR-4 | US-4 | T-4.1 | file-exists | `delivery-flow/references/design-sprint.md` exists |
| FR-4 | US-4 | T-4.2 | grep | Contains "PO defines problem scope" + "Architect detects paradigm" + "handoff to Plan" |
| FR-4 | US-4 | T-4.3 | grep | Documents trigger: Design and Architect stages |
| FR-5 | US-5 | T-5.1 | file-exists | `architect/references/volatility-decomposition.md` exists (redirect stub) |
| FR-5 | US-5 | T-5.2 | file-exists | `architect/references/strategic-ddd.md` exists (redirect stub) |
| FR-5 | US-5 | T-5.3 | grep | Volatility stub contains path `paradigms/volatility/references/volatility-decomposition.md` |
| FR-5 | US-5 | T-5.4 | grep | DDD stub contains path `paradigms/ddd/references/strategic-ddd.md` |
| FR-5 | US-5 | T-5.5 | line-count | Each stub is <=3 lines (single redirect, not content) |
| FR-6 | US-6 | **T-6.1 (empirical)** | invocation | Architect invoked with `decomposition: volatility` completes without error |
| FR-6 | US-6 | **T-6.2 (empirical)** | context-isolation | Paradigm sub-agent prompt contains volatility refs ONLY — grep for DDD/event-storming/game-architecture terms returns 0 hits in loaded refs |
| FR-6 | US-6 | **T-6.3 (empirical)** | output-contract | Decomposition artifact lands at expected `.delivery/artifacts/04-architect/` path |
| FR-6 | US-6 | **T-6.4 (empirical)** | token-measurement | Document paradigm prompt ref count (<5) vs monolithic ref count (27+) |
| FR-6 | US-6 | T-6.5 | grep | Router selected volatility via config (ADR-002 level 2) — logged in output |
| FR-7 | US-7 | T-7.1 | invariant-audit | Two-channel: orchestrator dispatches `architect` by name, not paradigm directly |
| FR-7 | US-7 | T-7.2 | invariant-audit | Context isolation: paradigm sub-agent refs are paradigm-scoped (proven by T-6.2) |
| FR-7 | US-7 | T-7.3 | invariant-audit | DoD multi-validator: output contract unchanged; DoD sees same artifact paths |
| FR-7 | US-7 | T-7.4 | invariant-audit | Orchestrator does not produce domain artifacts — delegation chain intact |
| FR-7 | US-7 | T-7.5 | grep | Self-correction cap: `3` still present in relevant SKILL.md sections |
| FR-7 | US-7 | T-7.6 | grep | Retrospective hook unchanged in hooks.json |
| FR-7 | US-7 | T-7.7 | grep | Light stage logic preserved — no skip semantics introduced |
| FR-7 | US-7 | T-7.8 | grep-absent | No cross-paradigm bleeding: volatility SKILL.md does not reference `strategic-ddd.md`; ddd SKILL.md does not reference `volatility-decomposition.md` |
| FR-7 | US-7 | T-7.9 | backwards-compat | Architect invoked WITHOUT paradigm config works (fallback to inline logic) |
| FR-7 | US-7 | T-7.10 | config-check | No new keys in `.delivery/config.yml`; `architecture.decomposition` pre-exists |

## Forbidden-Vocabulary Oracle
Applies to any NEW decomposition artifact produced during dogfood (US-6). Vocabulary from `constraints.yml.forbidden_vocabulary`:
- "event-storming skill"
- "functional decomposition skill"
- "new config key"
- "schema v2.8"

Oracle: case-insensitive whole-word grep on dogfood output. Zero hits required.

## Empirical vs Static Summary
- **Static:** T-1.*, T-2.*, T-3.*, T-4.*, T-5.*, T-6.5, T-7.5..T-7.10 — runnable immediately after code lands.
- **Empirical:** T-6.1..T-6.4, T-7.1..T-7.4 — require live invocation; gate US-6 and US-7 DoD.

## Risks
- **R-QA-1** Context isolation measurement (T-6.2) depends on observability of sub-agent prompt contents. Mitigation: count loaded reference files as proxy.
- **R-QA-2** Backwards compatibility test (T-7.9) requires invoking architect without paradigm config. Mitigation: use a clean config or `decomposition: auto` to trigger fallback path.
- **R-QA-3** Redirect stub tests (T-5.3, T-5.4) may false-pass if stubs contain additional content. Mitigation: T-5.5 line-count cap ensures stubs are minimal.
