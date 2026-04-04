# Dev Notes: Story-01 — Prior Art Analysis in Architect Skill

**Pipeline**: run-2026-04-04-w7m3
**Developer**: Gimli
**Date**: 2026-04-04
**Issue**: #55

> "Three cuts, three clean joints. That module was built by dwarf-craft. It will hold."

---

## Changes Made

**File modified**: `/home/meconnelly/.claude/plugins/marketplaces/mec-claude-agent-skills/delivery-team/skills/architect/SKILL.md`

### T1 — Prior Art Analysis Section (lines 34-80)

Added a new `## Prior Art Analysis` section between Phase 1 (Role Detection) and Phase 2 (Sub-Agent Invocation). The section includes:

1. **Condition gate**: Executes ONLY when user-provided specs exist. When absent, notes "No prior specifications provided" and proceeds to Phase 2 (backward-compatible).
2. **Step 1: Read and Summarize** — Mandatory full read of all user-provided specs with written summary.
3. **Step 2: Classify Each Element** — Structured table with two classifications: "Decision Already Made" and "Open Question". Includes concrete examples showing both categories.
4. **Step 3: Build On the Existing Design** — Three mandatory actions: validate feasibility, fill gaps, map to implementation.
5. **Step 4: Deviation Protocol** — Alternatives to settled decisions ONLY permitted with specific, documented technical blockers. Burden of proof on the Architect. Concrete example provided.
6. **Output requirement** — Summary and classification table MUST appear in the architecture artifact under a "Prior Art Analysis" section.

Uses MUST language throughout for mandatory steps.

### T2 — Sub-Agent Prompt Template Update (line 116)

Added to the `## Context` section of the Sub-Agent Prompt Template:
```
- Prior Art Analysis results (if applicable): spec summary, decisions-already-made, open questions
```

This ensures sub-agents receive the prior art context when spawned.

### T3 — Software Architecture Guardrail (line 497)

Added to Software Architecture Guardrails:
```
- **Respect user-provided specifications** — when a user provides an existing design or specification, the Architect must build on it. Proposing alternatives to settled design decisions is only permitted when a specific, documented technical blocker makes the original decision infeasible. The burden of proof is on the Architect to justify any deviation.
```

---

## AC Traceability

| AC | Status | Evidence |
|----|--------|----------|
| AC-01 | MET | Prior Art Analysis section exists at lines 34-80, positioned before Phase 2 |
| AC-02 | MET | Step 1 requires reading and summarizing ALL user-provided specs; output section is mandatory |
| AC-03 | MET | Step 2 requires structured classification table with "Decision Already Made" / "Open Question" |
| AC-04 | MET | Step 3 requires building ON existing design; Step 2 prohibits alternatives for "Decision Already Made" |
| AC-05 | MET | Step 4 Deviation Protocol requires specific, documented technical blockers with concrete example |
| AC-06 | MET | Condition gate: "If no user-provided specs exist, note and skip to Phase 2" |
| AC-07 | PENDING | Requires dogfooding validation (T4) |

---

## Backward Compatibility

All new instructions are conditional on user-provided spec presence. The condition gate at the top of the section explicitly handles the absence case with a skip-to-Phase-2 path. Existing pipelines without user specs will see no behavioral change.

---

## Notes

- No reference files were modified — Prior Art Analysis is an orchestration concern that lives in SKILL.md
- The classification table example uses realistic scenarios to reduce ambiguity for the AI agent
- The Deviation Protocol uses concrete PostgreSQL example to set the bar for what constitutes a valid technical blocker
- Seventeen commits I have made today. How many has the QA engineer found fault with? ... Do not answer that.
