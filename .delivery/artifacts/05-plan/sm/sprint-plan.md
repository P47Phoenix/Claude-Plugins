# Sprint Plan — Flow Doc Delivery (Stage 5 Light · DOCS_ONLY)

> *Aragorn son of Arathorn: "A ranger plans the march before the march plans him. Six docs, two sprints, one road. Every story names its end; every end names its witness."*

**Planner:** Aragorn (Scrum Bag) · **Routing:** DOCS_ONLY (light) · **Capacity declaration:** 6 stories across 2 sprints (3+3). No mid-sprint scope creep. Light DoD only: Architect + Tech Writer review — no full team DoD ceremony per DOCS_ONLY routing.

**Target dir (all stories):** `delivery-team/architecture/<flow-name>.md`
**Universal AC (all stories):** (i) file exists at path · (ii) ≥1 valid Mermaid block renders · (iii) addresses the why-it-matters from source brainstorm · (iv) cross-links to `delivery-team/ARCHITECTURE.md` · (v) under stated length cap.

---

## Sprint 1 — Mandatory + Strongest Convergence (3 stories)

### FLOW-1 · Adversarial Review Trigger Flow [PO MANDATORY]
- **File:** `delivery-team/architecture/adversarial-review-triggers.md`
- **Source:** Celebrimbor #1
- **Audience:** both (user + contributor)
- **Diagrams:** 3 Mermaid — (a) flowchart: stage-entry decision tree w/ confidence 1-5 branch · (b) sequence: orchestrator→primary→evaluator→challenger→human-on-≤2 · (c) flowchart: light-mode suppression gate
- **Length cap:** 180 lines
- **Extra AC:** cites SKILL.md L626/L662/L680 + team-patterns.md L131
- **Owner:** Architect (primary) · Tech Writer (cross-link pass)

### FLOW-2 · Deterministic Gating & BRE Relationship [PO MANDATORY]
- **File:** `delivery-team/architecture/deterministic-gating.md`
- **Source:** Celebrimbor #2
- **Audience:** contributor
- **Diagrams:** 2 Mermaid — (a) flowchart: 4-layer delivery-team determinism stack · (b) side-by-side flowchart: delivery-team validator-unanimity vs. prd-quality-gate-flow BRE rule tree
- **Length cap:** 180 lines
- **Extra AC:** explicit honesty paragraph stating delivery-team has NO BRE module; cites `prd-quality-gate-flow/business_rules_engine.py` as the real thing; cites `quality-gates.md` L16 + `team-patterns.md` L131
- **Owner:** Architect (primary) · Tech Writer (honesty-framing review)

### FLOW-3 · Hook Firing Timeline [CONVERGENCE 2/3]
- **File:** `delivery-team/architecture/hook-timeline.md`
- **Source:** MERGE of Celebrimbor #7 + Sam #1
- **Audience:** contributor (plugin maintainers, hook authors, debuggers)
- **Diagrams:** 2 Mermaid — (a) sequence/swimlane (Sam): User·Session·Orchestrator·Sub-Agents·Hooks·State lanes, full FEATURE run · (b) flowchart (Celebrimbor): per-hook block/warn/pass outcomes and orchestrator reaction
- **Length cap:** 180 lines
- **Extra AC:** names all 7 hooks × 5 event types; cites both source brainstorms
- **Owner:** Architect (diagrams) · Tech Writer (merge harmonization — two voices, one doc)

**Sprint 1 review gate:** Architect reviews diagrams render + technical accuracy; Tech Writer reviews cross-links + prose clarity. Both DONE = sprint 1 closes.

---

## Sprint 2 — Remainder (3 stories)

### FLOW-4 · DoD Validation & Self-Correction State Machine
- **File:** `delivery-team/architecture/dod-self-correction.md`
- **Source:** MERGE of Celebrimbor #3 + Legolas #2
- **Audience:** both
- **Diagrams:** 2 Mermaid — (a) state diagram: validator_pending→aggregating→{all_done|mixed|all_not_done}→correcting→terminals · (b) sequence: parallel fan-out, finding aggregation, delegation meta-gate
- **Length cap:** 180 lines
- **Extra AC:** includes finding-schema contract table (Legolas); names CODE_COMPLETE terminal (Celebrimbor); cites SKILL.md L516-534, L699 + quality-gates.md L56-72
- **Owner:** Architect (state machine) · Tech Writer (contract table formatting)

### FLOW-5 · Empirical vs Analytical Validation Lifecycle
- **File:** `delivery-team/architecture/empirical-validation-lifecycle.md`
- **Source:** Legolas #1
- **Audience:** QA + Developer + Godot contributors + UAT owners
- **Diagrams:** 2 Mermaid — (a) state machine: AC lifecycle proposed→classified→code-complete-pending→empirically-validated→accepted · (b) swimlane: Developer / QA validator / UAT owner / User
- **Length cap:** 150 lines
- **Extra AC:** cites quality/SKILL.md L270-311; cross-links to `empirical-validation.md`
- **Owner:** Architect (lifecycle) · Tech Writer (cross-link to dev + godot skills)

### FLOW-6 · Sub-Agent Dispatch & Two-Channel Communication
- **File:** `delivery-team/architecture/agent-dispatch.md`
- **Source:** Celebrimbor #6
- **Audience:** contributor
- **Diagrams:** 2 Mermaid — (a) sequence: correct dispatch (scoped prompt + disk I/O + ≤200-char signal) · (b) flowchart: anti-pattern detection (direct Write block, compound-role warn)
- **Length cap:** 160 lines
- **Extra AC:** cites `audit_agent_prompt.py` + `enforce_pipeline_scope.py` hooks + `artifact-contracts.md`; names Prime Directive explicitly
- **Owner:** Architect (primary) · Tech Writer (anti-pattern framing)

**Sprint 2 review gate:** same light DoD — Architect + Tech Writer only.

---

## Closeout Criteria (both sprints)

- 6 files exist under `delivery-team/architecture/`
- All Mermaid blocks validated (syntactic render check)
- Cross-links from `delivery-team/ARCHITECTURE.md` updated (Tech Writer final pass)
- Defer list in `prioritized-flow-list.md` preserved as backlog seed

*Set out at first light; make camp when the work is done, not when the sun says so.* — Aragorn

---

STATUS: DONE
ARTIFACT: .delivery/artifacts/05-plan/sm/sprint-plan.md
SUMMARY: Aragorn — 6 stories / 2 sprints. S1: FLOW-1 adversarial-triggers (PO mandatory), FLOW-2 deterministic-gating (PO mandatory), FLOW-3 hook-timeline (2/3 convergence). S2: FLOW-4/5/6. Light DoD.
