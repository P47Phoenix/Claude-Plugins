# PO DoD Review — Stage 7 UAT

**Validator**: Gandalf the Grey, Product Owner
**Stage**: 07 — UAT
**Bundle**: Orchestration Discipline (issues #73, #71, #70, #69)
**Date**: 2026-04-05

> *"A pipeline is judged not by the speed of its passage, but by the truth of what it leaves behind. Let us see whether the road has been walked rightly."*

---

## Verdict

**STATUS: DONE**

The bundle delivers all 13 stories, satisfies all 16 functional requirements, and the four source GitHub issues (#73, #71, #70, #69) can be closed by this change. Business value — a delivery-flow orchestrator that no longer lies about its own discipline — is realized.

---

## 1. Story coverage (OD-01 through OD-13)

| Story | Title (abbrev) | Evidence in OD-all.md | Status |
|---|---|---|---|
| OD-01 | Phase 0 stop pinning `project_type` (SKILL.md) | OD-01 entry — Phase 0 directive replaced; `routing.force_type` override surfaced | DONE |
| OD-02 | Phase 1 always-runs note (SKILL.md) | OD-02 entry — Phase 1 header rewritten | DONE |
| OD-03 | Delegation Prime Directive strengthened | OD-03 entry — Core Principle 1 expanded, 5 anti-patterns, permitted write paths enumerated | DONE |
| OD-04 | "One Role = One Sub-Agent" rule block | OD-04 entry — rule with worked examples (3 / 4 / N call cases) | DONE |
| OD-05 | Step 4.5 rejected justifications | OD-05 entry — explicit rejection list added | DONE |
| OD-06 | Common Orchestrator Anti-Patterns section | OD-06 entry — 8 anti-patterns (PRD asked for 6 minimum; exceeds) | DONE |
| OD-07 | Config table updates (SKILL.md) | OD-07 entry — `routing.force_type`, `pipeline.enforce_self_write_block` rows added | DONE |
| OD-08 | Schema v2.6 → v2.7 (config-schema.md + JSON) | OD-08 entry — version bumped, deprecated section added, JSON regenerated via generator | DONE |
| OD-09 | Setup wizard renumber (Round 3 corrected to 9 questions) | OD-09 + Round 3 D2-01/D2-02 — Q8 demoted to pre-question, final 9 contiguous Q1..Q9 | DONE |
| OD-10 | `audit_agent_prompt.py` compound-role detector (MAY) | OD-10 + Round 2 M-05 — three detectors plus negation guard | DONE (optional shipped) |
| OD-11 | `project-types.md` reframed for runtime detection | OD-11 entry — top block added, ADR-002 referenced | DONE |
| OD-12 | `team-patterns.md` dispatch rules + Pattern 2b Isolated Adversarial Loop | OD-12 entry — every pattern has dispatch rule; Pattern 2b with taxonomy + 3 convergence rules + pseudocode | DONE |
| OD-13 | Cross-cutting: quality-gates.md, pipeline-stages.md, hook extension, doc parity | OD-13 entry — Delegation Meta-Gate, Known Hook Limitations, Stage 4 rewritten, hook layered detection, CLAUDE.md/README.md/marketplace.json updated | DONE |

**13/13 stories delivered.**

---

## 2. Functional Requirements (16 FRs)

| FR | Requirement | Coverage | Status |
|---|---|---|---|
| FR-01 | Remove `project_type` from active schema, bump v2.7 | OD-08 (config-schema.md, deprecated section, version history row) | MET |
| FR-02 | Tolerant parsing + `routing.force_type` opt-in | OD-07/OD-08 docs; activation gating in OD-13 hook honors v2.6 tolerance | MET |
| FR-03 | Phase 1 every invocation | OD-01, OD-02 SKILL.md edits | MET |
| FR-04 | Wizard drops Q1, renumbers | OD-09 + Round 3 — 9 contiguous questions verified | MET |
| FR-05 | Routing docs reframed | OD-11 project-types.md block; SKILL.md Phase 1 note | MET |
| FR-06 | Delegation Prime Directive top-of-file | OD-03 SKILL.md Core Principle 1 | MET |
| FR-07 | Step 4.5 rejects "simple" | OD-05 rejected-justifications subsection | MET |
| FR-08 | Common Anti-Patterns section (>= 6) | OD-06 — 8 patterns shipped | MET (exceeds) |
| FR-09 | `enforce_pipeline_scope.py` blocks orchestrator self-writes (layered detection, allowlist, activation gate) | OD-13 — Layer 1 env var, Layer 2 metadata, Layer 3 soft-deny; allowlist; v2.7 + flag gating; gaps documented | MET (Bash redirection gap documented per ADR-001 and surfaced in quality-gates.md Known Hook Limitations — acceptable per PRD) |
| FR-10 | "One Role = One Sub-Agent" rule in SKILL.md | OD-04 prominent rule block with worked examples | MET |
| FR-11 | Dispatch rule in team-patterns.md, quality-gates.md, pipeline-stages.md | OD-12 + OD-13 — all three docs reinforced | MET |
| FR-12 | Compound-role detector (MAY) | OD-10 + M-05 negation guard | MET (optional shipped) |
| FR-13 | Isolated Adversarial Loop pattern with taxonomy + 3 convergence rules | OD-12 Pattern 2b complete | MET |
| FR-14 | Stage 4 references the loop pattern + cap | OD-13 pipeline-stages.md Stage 4 rewrite | MET |
| FR-15 | `max_self_correction` documented for Architect loops | OD-08 schema v2.7 docs | MET |
| FR-16 | Schema bump + doc parity (CLAUDE.md, README.md, marketplace.json, docs/**) | OD-13 + Round 2 M-04 + Round 3 (count fix across root docs) | MET |

**16/16 functional requirements satisfied.**

---

## 3. GitHub issues — closeable by this change

| Issue | Title | FRs delivered | Closeable? |
|---|---|---|---|
| #73 | Remove `project_type` from config; detect every run | FR-01..FR-05; legacy tolerance + `routing.force_type` opt-in shipped | YES — close on merge |
| #71 | Orchestrator bypasses delegation when "simple" | FR-06..FR-09; Prime Directive + Step 4.5 + 8 anti-patterns + layered hook + meta-gate | YES — close on merge |
| #70 | One sub-agent per reviewer role | FR-10..FR-12; rule block + dispatch rules in 3 docs + non-blocking detector with negation guard | YES — close on merge |
| #69 | Architect adversarial loops with isolated context | FR-13..FR-15; Pattern 2b with taxonomy + 3 convergence rules + Stage 4 reference + cap documented | YES — close on merge |

All four issues can be closed by this PR. PO directs that the merge commit / PR description carry `Closes #73, #71, #70, #69` so GitHub auto-closes them.

---

## 4. Business value delivered

1. **Truthful project typing per run.** Operators (P1) no longer suffer mistyped routing from a frozen wizard guess. Phase 1 detects every run; intentional pinning is a discoverable namespaced act under `routing.`.
2. **Delegation as enforced behavior, not aspiration.** Plugin contributors (P2) can trust DoD verdicts come from independent sub-agents. The Delegation Prime Directive is enforced by SKILL.md prose, the Step 4.5 rejection clause, the 8 anti-patterns, the layered hook, AND the new Delegation Meta-Gate in `quality-gates.md`. Defense-in-depth.
3. **Context isolation restored across all collaboration patterns.** Reviewers cannot be silently collapsed; the dispatch rule leads every pattern in `team-patterns.md`, and `audit_agent_prompt.py` warns on compound prompts (with negation handling so anti-pattern guidance text is not falsely flagged).
4. **Anchoring defeated at Architect.** The Isolated Adversarial Loop with two-clean / no-new-classes / hard-cap convergence ensures a single lucky pass cannot masquerade as proven convergence. Future Architect sub-agents (P4) inherit a real protocol, not a single-shot shortcut.
5. **Atomic merge, no churn.** All four fixes ship in one PR; no contradictory edits across `SKILL.md`, `pipeline-stages.md`, `team-patterns.md`, `quality-gates.md`, `config-schema.md`. NFR-08 satisfied.
6. **Backwards compatibility honored.** Legacy v2.6 configs load without error; the activation gate (`schema_version >= 2.7` AND `enforce_self_write_block: true`) means upgrading repos are not surprised by hard denials. NFR-03 + NFR-05 satisfied.
7. **Documentation parity end-to-end.** Round 2 (M-04) and Round 3 swept `docs/**`, both READMEs, CLAUDE.md, marketplace.json (bumped to 2.18.0). NFR-04 satisfied.
8. **Dogfood evidence.** This very pipeline run produced PO/PRD/stories/dev/QA/UAT artifacts via dispatched sub-agents (Gandalf PO, architect, Gimli developer, Legolas QA, Bilbo tech-writer). NFR-06 satisfied; the activation gate's forward-looking semantics (per FR-09 / R7) means this run was not blocked while authoring v2.7's own successor docs.

---

## 5. PO observations and follow-ups (non-blocking)

- **Bash-redirection bypass** in `enforce_pipeline_scope.py` is a known, documented gap. PO accepts deferral because (a) it requires a `hooks.json` Bash matcher addition outside this bundle's edit map, (b) the Delegation Meta-Gate in `quality-gates.md` provides a manual check that catches the bypass at DoD time, and (c) the gap is surfaced in both the hook docstring and `quality-gates.md` "Known Hook Limitations". **Action**: log a follow-up issue post-merge to close this gap in a future bundle.
- **Centralized sub-agent dispatch wrapper** for `CLAUDE_AGENT_ID` / `DELIVERY_FLOW_AGENT_CONTEXT` injection is also flagged as a known follow-up by Gimli. PO accepts deferral — it is an orchestrator-runtime concern, not a docs/hook concern, and Layer 3 soft-deny is the intended safety net until then. **Action**: log follow-up issue.
- **Wizard count history (R1 -> R2 -> R3 churn).** Three passes were required to land on 9 contiguous questions because Q8 needed demotion to a pre-question, not removal. Retrospective lesson: count-and-renumber stories deserve explicit "verify by grep" acceptance criteria from the Plan stage. Lesson, not a defect.

---

## 6. DoD signal

**STATUS: DONE**

All 13 stories delivered. All 16 FRs met. All 4 GitHub issues closeable. Business value realized. Backwards compatibility preserved. Documentation in parity. Dogfood demonstrated. Two known gaps documented and routed to follow-up issues.

> *"The road goes ever on — and this stretch of it has been walked with the discipline that was promised. Ride on."*
>
> — Gandalf, PO
