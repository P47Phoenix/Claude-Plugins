# Adversarial Challenge: Hardware Delivery Team PRD

**Challenger:** QA Engineer (Adversarial Review)
**Pipeline:** run-2026-04-12-hw01
**Stage:** 02-refine
**Target Artifact:** `.delivery/artifacts/02-refine/po/prd.md`
**Date:** 2026-04-12

---

## Challenge 1: Cross-Plugin Skill Invocation Is an Unverified Platform Capability

**Assumption challenged:** The entire PRD rests on Assumption #1: "The kicad-happy/ plugin skills are consumable as sub-agents from other plugins (cross-plugin skill invocation is supported by the Claude Code plugin system)."

**Why it matters:** This is the architectural foundation of Epic 3 (Integration Layer), which is P1 and has 4 downstream stories. The PRD itself marks dependency D-002 as "Pending -- assumed but not verified." If cross-plugin skill invocation is NOT supported, the integration layer architecture changes fundamentally (the PRD's own words). Every role story (Epic 2) that says "CONSUMES kicad-happy:X" becomes undeliverable as specified. This is not a small risk -- it is the single point of failure for approximately 40% of the PRD's functional requirements (FR-009 through FR-014 all depend on it).

The PRD acknowledges this risk (R-005) but defers resolution to "Architect stage." This is too late. If the Architect discovers cross-plugin invocation is unsupported, the entire PRD needs rewriting -- not just the architecture. The acceptance criteria, the metrics (M1 kicad-happy Utilization Rate), and the success metrics all assume this capability exists.

**Concrete fix:** Before this PRD exits Refine, someone must verify cross-plugin skill invocation with a simple test: from a delivery-team skill context, attempt to invoke a kicad-happy skill via the Agent tool. Document the result. If it fails, the PRD must define the fallback architecture NOW (e.g., inline reference loading, monorepo skill copying, or skill-as-prompt-template pattern) and adjust all acceptance criteria accordingly.

**Severity:** BLOCKING

---

## Challenge 2: kicad-happy Does Not Exist in This Repository

**Assumption challenged:** The PRD references "kicad-happy/" skills throughout (11 skills, Epic 3 entirely dedicated to integration). However, there is no `kicad-happy/` directory in this repository and no `kicad-happy` entry in `.claude-plugin/marketplace.json`.

**Why it matters:** The kicad-happy skills ARE visible in the current session's skill list (they appear as loadable skills like `kicad-happy:digikey`, `kicad-happy:kicad`, etc.), which means they are installed via some external mechanism -- likely a separate repository or a user-level skill installation. The PRD correctly flags this as D-001 ("At-Risk: skills are loaded in session but no files found under kicad-happy/ in this repo") but does not resolve it.

This creates three problems:
1. **Deployment coupling**: hardware-team cannot be installed independently. Users must ALSO have kicad-happy installed, but the PRD does not specify how.
2. **Version coupling**: If kicad-happy updates its skill interface (different expected inputs/outputs), hardware-team breaks silently with no version pinning or compatibility check.
3. **Testing impossibility**: The metrics document (M1) defines "kicad-happy Skill Utilization Rate" but the test fixture requires kicad-happy to be installed. CI/CD cannot verify this metric without a reproducible installation path.

**Concrete fix:** Add a new story (suggest Epic 1 or Epic 3) for "kicad-happy Dependency Documentation" that: (a) documents the installation mechanism for kicad-happy, (b) adds kicad-happy version compatibility to `.hardware/config.yml` schema, (c) adds a SessionStart hook that verifies kicad-happy skill availability and reports missing skills with installation instructions.

**Severity:** BLOCKING

---

## Challenge 3: The 8-Stage Pipeline May Be Over-Decomposed for the Plugin Context

**Assumption challenged:** FR-002 specifies 8 stages: Concept, Schematic, Layout, Prototype, DFM/DFA, Compliance, Pilot Run, Production Release.

**Why it matters:** In a Claude Code plugin context, the "Prototype" stage is fundamentally different from the others. Stages 1-3 and 5-6 are analysis/documentation stages that Claude can execute as an AI agent (review schematics, validate DFM rules, check compliance). But "Prototype" requires physical fabrication -- ordering boards, soldering, powering on, measuring. "Pilot Run" requires manufacturing a batch. "Production Release" requires shipping to a CM. Claude cannot do any of these.

The PRD is ambiguous about what these physical stages actually DO within the plugin. Story 1.2 says the Prototype stage exists but its acceptance criteria only say "each stage has a defined purpose, key activities list, and required role(s)" without clarifying what the AI does during a physical stage. If these stages are just "generate documentation for the human to execute physically," they could be merged or represented as gate outputs rather than full pipeline stages.

Having 8 stages when 3 of them (Prototype, Pilot Run, Production Release) are essentially "generate a checklist and wait for human" inflates the pipeline complexity and the config/state management overhead without proportional value.

**Concrete fix:** Clarify in the PRD what the AI agent concretely does during Prototype, Pilot Run, and Production Release stages. If the answer is "generates documentation/checklists," consider: (a) merging Pilot Run into Production Release, (b) making Prototype a gate output of Layout (generate prototype ordering package) rather than a full stage, or (c) explicitly documenting that these stages are "human execution stages" with a different orchestration pattern (gate-in, human-action, gate-out).

**Severity:** ADVISORY

---

## Challenge 4: Missing Role -- Where Is the Firmware-Hardware Interface in Phase 1?

**Assumption challenged:** The PRD defers Firmware Engineer to Phase 2 (Epic 6) but claims the 6 Phase 1 roles are sufficient for initial release.

**Why it matters:** Persona 3 (Priya) is specifically a firmware/hardware bridge engineer whose primary pain point is "receives schematics without interface documentation." But there is no role in Phase 1 that produces firmware interface documentation. The HW Product Owner handles requirements but not pin-level interface specs. The Electrical Engineer handles schematic design but not firmware bring-up documentation. The Test Engineer handles test strategy but not firmware validation.

This means Phase 1 delivers a pipeline that serves Personas 1, 2, 4, and 5 but explicitly CANNOT serve Persona 3 -- who is listed as a Primary Persona. A primary persona with zero Phase 1 coverage is a prioritization mismatch.

**Concrete fix:** Either (a) add "firmware interface documentation" as an output of the Electrical Engineer role during the Schematic stage (not a new role, just a new artifact -- pin assignment table, power domain map, communication bus interface spec), or (b) downgrade Priya from Primary to Secondary persona and acknowledge that firmware-hardware interface is Phase 2 only. Option (a) is preferred because the EE already has the schematic context needed to produce this artifact.

**Severity:** ADVISORY

---

## Challenge 5: Acceptance Criteria Are Not Testable Without a Reference Test Fixture

**Assumption challenged:** Multiple acceptance criteria assume runtime conditions that cannot be verified without a real KiCad project and installed kicad-happy skills.

**Why it matters:** Examples of untestable acceptance criteria:
- Story 1.4: "Given the config specifies `target_fab: jlcpcb`, when DFM validation runs, then it uses JLCPCB's specific design rules (consuming kicad-happy:jlcpcb)" -- requires kicad-happy:jlcpcb to be installed AND a real KiCad project with DFM-relevant features.
- Story 4.1: "when review categories are checked, then the following categories are covered: power integrity, signal integrity, component derating..." -- requires a reference schematic with seeded defects in all 7 categories.
- Story 4.3: "when total BOM cost exceeds the budget, then the gate returns NOT_DONE" -- requires live pricing data from distributor APIs.

The metrics document (M2) acknowledges this by requiring "a reference KiCad schematic with exactly 10 seeded defects across all 7 review categories" stored in `hardware-team/references/test-fixtures/`. But creating this reference schematic is not a story in any epic. It is assumed to exist but never scheduled for creation.

**Concrete fix:** Add a story (suggest Epic 4, before Story 4.1) for "Reference Test Fixture Creation" that creates: (a) a reference KiCad project with seeded defects, (b) a reference BOM with known issues (obsolete parts, budget violations, single-source risks), (c) a reference layout with DFM violations. Without this test fixture, the acceptance criteria for all 5 validation gates (Epic 4) and the North Star metric are unmeasurable.

**Severity:** BLOCKING

---

## Challenge 6: "0 Reimplemented Capabilities" Counter-Metric Is Unenforceable

**Assumption challenged:** NFR-003 states "kicad-happy skills consumed, never duplicated -- 0 reimplemented kicad-happy capabilities." M1 includes a counter-metric: "Zero reimplemented kicad-happy capabilities. Verify via code review."

**Why it matters:** "Reimplementation" is a judgment call, not a binary check. If the Electrical Engineer role's SKILL.md contains guidance like "check capacitor derating by comparing rated voltage to operating voltage," is that reimplementing kicad-happy:kicad's schematic review, or is it role-specific domain knowledge? If the Manufacturing Engineer role evaluates trace width minimums from a SKILL.md reference table, is that reimplementing kicad-happy:jlcpcb's DFM rules?

The boundary between "role knowledge that guides skill invocation" and "reimplemented capability" is undefined. Without a clear definition, this metric will either always pass (by defining everything as "guidance, not reimplementation") or always fail (by defining any domain logic as reimplementation).

**Concrete fix:** Define "reimplementation" operationally: "A capability is reimplemented if a hardware-team role performs an action that would produce the same output as invoking a kicad-happy skill, without invoking that skill." Add examples of what IS and IS NOT reimplementation to the integration layer architecture document (Story 3.1).

**Severity:** ADVISORY

---

## Challenge 7: Scope Creep Risk from "Config-Driven Flexibility"

**Assumption challenged:** FR-021 (P2) says "Pipeline auto-detects project type (1-layer prototype vs. 8-layer production, hobby vs. certified) and adapts stage depth." M4 targets "3+ project types supported."

**Why it matters:** "Adapts stage depth" is unbounded complexity. For each of the 3+ project types, the pipeline must: (a) decide which stages to skip/minimize, (b) adjust gate strictness per stage, (c) modify role emphasis, (d) change BOM budget thresholds, (e) select different compliance regions. That is 5 configuration dimensions across 3+ project types across 8 stages -- potentially 120+ configuration decision points.

The delivery-flow plugin achieved this through config v2.7 after 21 prior versions. The hardware-team is attempting it from v1.0. The PRD puts config-driven flexibility at P2 but the acceptance criteria for P1 stories (like Story 1.4) already depend on config-driven behavior ("Given the config specifies target_fab: jlcpcb").

**Concrete fix:** Separate "config reads static settings" (P1, already needed) from "config adapts pipeline behavior per project type" (P2, the risky part). Ensure that P1 acceptance criteria for Story 1.4 only require reading config values, NOT dynamically adapting pipeline structure. The pipeline structure adaptation should be a clean Phase 2 addition, not entangled with P1 config stories.

**Severity:** ADVISORY

---

## Challenge 8: Rework Loops Lack Termination Conditions

**Assumption challenged:** Story 1.7 defines 6 rework paths and says "pipeline is a DAG with controlled backward edges." But there is no termination condition.

**Why it matters:** What happens when Prototype fails, triggers rework to Schematic, Schematic re-runs, passes its gate, Layout re-runs, passes its gate, Prototype runs again... and fails again? The PRD defines rework paths but not rework limits. A pipeline could theoretically loop infinitely: Prototype -> Schematic -> Layout -> Prototype -> Schematic -> ...

In physical hardware development, this loop terminates because humans run out of patience or budget. In an AI pipeline running autonomously, there is no such natural brake. The pipeline will consume context window and session time in infinite rework loops.

**Concrete fix:** Add a rework loop limit to the config schema (e.g., `max_rework_iterations: 3` per path, `max_total_reworks: 10` per pipeline run). When the limit is hit, escalate to human with the rework history. Add this as an acceptance criterion to Story 1.7: "Given a rework path has been triggered N times (configurable, default 3), when it triggers again, then the pipeline escalates to the human instead of looping."

**Severity:** BLOCKING

---

## Challenge 9: The Metrics Document Has Targets Without Meaningful Baselines

**Assumption challenged:** The metrics document sets targets (e.g., "80% Pipeline Completion Rate within first 3 months") against baselines of 0% across the board.

**Why it matters:** Per the memory lesson "Adversarial target adjustment: challenger can productively adjust targets based on thin baseline data" -- with EVERY metric at baseline 0%, the targets are arbitrary. The 80% Pipeline Completion Rate target means "8 out of 10 pipeline runs complete all configured stages." But what does a pipeline "failure" look like? If 3 of those 10 runs fail because kicad-happy is unavailable (infrastructure, not quality), the metric reads 70% and appears to miss target -- but the pipeline itself is fine.

The North Star metric does not distinguish between:
- Pipeline logic failures (bug in orchestrator)
- Infrastructure failures (missing skills, session timeout)
- Domain failures (legitimately unfixable design issues)
- User abandonment (user stops pipeline mid-run)

All of these count as "not completing all configured stages."

**Concrete fix:** Amend the North Star metric definition to exclude infrastructure failures and user abandonment from the denominator. Define: "A pipeline run counts toward the completion rate only if all required skills are available at pipeline start (infrastructure check passes) and the user does not explicitly abandon the run." Add a root cause categorization to pipeline failure logging.

**Severity:** ADVISORY

---

## Challenge 10: No Story for the Integration Layer's Fallback Architecture

**Assumption challenged:** Risk R-005 says "if [cross-plugin invocation is] unsupported, fall back to inline skill reference loading." But there is no story, acceptance criteria, or design guidance for this fallback.

**Why it matters:** The fallback architecture ("inline skill reference loading") is fundamentally different from the primary architecture ("cross-plugin skill invocation via Agent tool"). Inline loading means the hardware role loads kicad-happy's SKILL.md content directly into its own context, which: (a) violates context isolation (NFR-002), (b) increases context window consumption per role, (c) requires knowing the file paths of kicad-happy SKILL.md files (which are not in this repo), and (d) changes every acceptance criterion that says "CONSUMES kicad-happy:X."

A fallback that contradicts 4 of the PRD's own non-functional requirements is not a viable fallback -- it is a fundamentally different product.

**Concrete fix:** Either (a) resolve the cross-plugin invocation question NOW (before exiting Refine) and remove the fallback from the risk register if it works, or (b) design the fallback as a first-class architecture option with its own acceptance criteria, acknowledging the NFR trade-offs. Do not leave "fall back to inline skill reference loading" as a hand-wave in a risk mitigation column.

**Severity:** BLOCKING

---

## Overall Confidence Rating

**Confidence: 2 out of 5**

**Rationale:** The PRD is well-structured, thorough in its scope definition, and clearly modeled on the proven delivery-team architecture. The personas are realistic, the user stories are detailed, and the metrics are more rigorously defined than most PRDs. However, the PRD has a critical structural dependency -- cross-plugin skill invocation -- that is unverified and potentially unsupported. Five of the twelve out-of-scope items exist specifically to manage scope, which is disciplined. But the five BLOCKING challenges (cross-plugin invocation verification, kicad-happy dependency management, test fixture creation, rework loop termination, and fallback architecture resolution) represent gaps that cannot be deferred to the Architect stage without risking a fundamental rewrite.

Per memory lesson "Trust challenger confidence ratings when data is sparse": the data on cross-plugin skill invocation is sparse (zero evidence it works), and this single unknown cascades through 40% of the PRD. Until Challenges 1, 2, 5, 8, and 10 are addressed, this PRD should not advance past Refine.

---

## Summary: Challenge Severity Index

| # | Challenge | Severity |
|---|-----------|----------|
| C1 | Cross-plugin skill invocation unverified | BLOCKING |
| C2 | kicad-happy not in repository | BLOCKING |
| C3 | 8-stage pipeline over-decomposed for AI context | ADVISORY |
| C4 | Firmware-hardware interface missing in Phase 1 | ADVISORY |
| C5 | Acceptance criteria untestable without reference fixture | BLOCKING |
| C6 | "0 reimplemented" counter-metric unenforceable | ADVISORY |
| C7 | Config-driven flexibility scope creep risk | ADVISORY |
| C8 | Rework loops lack termination conditions | BLOCKING |
| C9 | Metrics targets without meaningful baselines | ADVISORY |
| C10 | Fallback architecture undefined | BLOCKING |

**BLOCKING count:** 5
**ADVISORY count:** 5

---

## Recommendation

Address the 5 BLOCKING items before gate evaluation. The 5 ADVISORY items can be resolved during Design/Architect stages. Specifically:

1. **Verify cross-plugin invocation** with a live test (C1) -- this is a 15-minute experiment that de-risks the entire PRD
2. **Document kicad-happy installation** and add dependency verification (C2)
3. **Add reference test fixture story** to Epic 4 (C5)
4. **Add rework loop termination** to Story 1.7 acceptance criteria (C8)
5. **Resolve fallback architecture** or remove it from risk mitigations (C10)
