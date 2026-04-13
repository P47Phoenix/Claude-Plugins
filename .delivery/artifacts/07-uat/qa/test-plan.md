# UAT Test Plan: hardware-team Plugin

**Author:** QA Engineer (Legolas)
**Pipeline:** run-2026-04-12-hw01 | **Type:** GREENFIELD
**Date:** 2026-04-12
**PRD Version:** 1.1 | **Test Strategy Version:** aligned to PRD 1.1
**Status:** Active

---

> "A keen eye reveals what haste would miss. Every gate shall be tested, every skill shall be verified, every FR shall be traced. That bug still only counts as one."

---

## 1. Test Plan Overview

### 1.1 Purpose

This UAT test plan verifies that the hardware-team plugin -- a Claude Code plugin orchestrating 8-stage hardware development pipelines by consuming kicad-happy skills as building blocks -- meets all 22 PRD functional requirements and 10 non-functional requirements. The plugin is a GREENFIELD delivery that introduces 7 sub-skills, 6 hooks, 5 validation gates, 2 collaboration patterns, and an 8-stage pipeline orchestrator with rework loop support.

### 1.2 Scope

| Area | Items Under Test | Count |
|------|------------------|-------|
| Plugin installation | marketplace.json registration, SKILL.md loading, directory structure | 1 plugin |
| Skill discoverability | 7 sub-skills (hardware-flow, hw-product-owner, electrical-engineer, pcb-layout-engineer, manufacturing-engineer, compliance-engineer, test-engineer) | 7 skills |
| Hook execution | SessionStart config check, SessionStart kicad-happy check, PreToolUse pipeline bypass, PostToolUse KiCad DRC (P2), PostToolUse BOM drift (P2), Agent prompt audit | 6 hooks |
| Config validation | validate_config.py, schema validation, defaults | 1 script |
| Pipeline orchestrator | 8 stages, routing matrix, rework loops (8 paths), state persistence | 8 stages |
| Validation gates | Schematic Review, DRC, BOM, DFM, Compliance (all against reference fixture) | 5 gates |
| kicad-happy integration | Cross-plugin Skill tool invocation for all 11 kicad-happy skills | 11 skills |
| Collaboration patterns | Design Review Board (P1), BOM Reconciliation (P2) | 2 patterns |
| Security controls | Path sanitization, YAML safe_load enforcement | 2 controls |
| FR traceability | All 22 PRD functional requirements | 22 FRs |

### 1.3 Out of Scope

- Phase 2 stories: US-105 (state persistence), US-106 (memory), US-502 (BOM reconciliation), US-504 (DRC hook), US-505 (BOM drift hook)
- FR-021 (dynamic pipeline adaptation -- P2 deferred)
- FR-016 (BOM Reconciliation -- P2)
- FR-018 (PostToolUse DRC hook -- P2)
- FR-019 (PostToolUse BOM drift -- P2)
- Modifying kicad-happy skills themselves
- Physical hardware testing or lab automation
- Phase 2 roles: Mechanical Engineer, Firmware Engineer

---

## 2. Entry Criteria

| # | Criterion | Verification Method |
|---|-----------|---------------------|
| EC-1 | Plugin skeleton (US-101) structurally complete | `ls -R hardware-team/` confirms SKILL.md, skills/, references/, hooks/, scripts/, LICENSE.txt |
| EC-2 | All P1 stories developer-complete and self-tested | Developer sign-off on all Epic 1-5 P1 stories |
| EC-3 | kicad-happy plugin v1.2.0+ installed | Verify 11 skills loadable at `~/.claude/plugins/cache/kicad-happy/` |
| EC-4 | Reference test fixture (US-400) complete | MANIFEST.md present with >= 18 seeded defects documented |
| EC-5 | marketplace.json updated with hardware-team entry | `grep "hardware-team" .claude-plugin/marketplace.json` returns match |
| EC-6 | Python 3.x available (stdlib only) | `python --version` succeeds |
| EC-7 | All hook scripts compile | `python -m py_compile hardware-team/hooks/*.py` exits 0 |

---

## 3. Exit Criteria

| # | Criterion | Target |
|---|-----------|--------|
| XC-1 | All P1 FR test cases pass | 100% pass rate (21/21 P1 FRs) |
| XC-2 | All P1 NFR verifications pass | 100% pass rate |
| XC-3 | All 5 validation gates tested against reference fixture | 5/5 gates executed with documented results |
| XC-4 | Schematic Review Gate category detection rate | >= 6/7 categories (>80%) |
| XC-5 | Zero critical defects open | 0 critical defects |
| XC-6 | FR traceability matrix complete | 21/22 FRs mapped (FR-021 deferred to P2) |
| XC-7 | Cross-plugin kicad-happy invocation verified | 11/11 skills dispatched successfully |
| XC-8 | Rework termination conditions verified | Per-path (3) and total (10) limits tested |

---

## 4. Test Areas

### 4.1 Plugin Installation Verification

**Objective:** Confirm the hardware-team plugin follows CLAUDE.md conventions, is structurally sound, and is discoverable.

**Coverage:**
- Directory structure: SKILL.md, skills/ (7 sub-dirs), references/, hooks/, scripts/, LICENSE.txt
- SKILL.md three-level context loading (metadata, skill instructions, on-demand resources)
- marketplace.json registration: unique ID, display name, description, 7 skill paths, kicad-happy dependency noted
- No ID conflicts with existing plugins (delivery-team, kicad-happy, etc.)

**Test cases:** TC-001 through TC-005
**FR mapping:** FR-001

---

### 4.2 Skill Discoverability

**Objective:** Confirm all 7 sub-skills load correctly with SKILL_LOADED signal and maintain context isolation.

**Coverage per skill:**
- hardware-flow: orchestrator loads, contains 8-stage definition, Prime Directive guardrail
- hw-product-owner: loads only HW PO references (hw-requirements.md, feasibility-analysis.md, make-vs-buy.md)
- electrical-engineer: loads only EE references (5 files), Sonnet+ tier, firmware interface docs output
- pcb-layout-engineer: loads only Layout references (3 files), Sonnet+ tier
- manufacturing-engineer: loads only MfgE references (4 files)
- compliance-engineer: loads only CompE references (4 files)
- test-engineer: loads only TestE references (4 files)

**Test cases:** TC-010 through TC-023
**FR mapping:** FR-008

---

### 4.3 Hook Execution

**Objective:** Confirm all hooks fire on correct events and produce expected output.

**Coverage:**
- hooks.json defines all hooks with correct event types (SessionStart, PreToolUse, PostToolUse)
- SessionStart config check: fires with valid/invalid/missing .hardware/config.yml
- SessionStart kicad-happy check: reports N/11 skills available, lists missing skills
- PreToolUse pipeline bypass: warns when role skill invoked outside pipeline context
- PostToolUse KiCad DRC: triggers on .kicad_sch edits (P2 -- hook definition only tested)
- PostToolUse BOM drift: detects schematic-BOM divergence (P2 -- hook definition only tested)

**Test cases:** TC-030 through TC-042
**FR mapping:** FR-017, FR-018 (P2), FR-019 (P2)

---

### 4.4 Config Validation

**Objective:** Confirm validate_config.py handles all config states correctly.

**Coverage:**
- Valid config: passes validation, all fields read correctly
- Missing config: defaults used, warning emitted
- Invalid config: warns on bad fields, uses defaults for those fields
- Outdated schema version: migration guidance displayed
- Schema contents: version, target_fab, compliance_regions, bom_budget, dependencies.kicad_happy_version, max_rework_iterations (default 3), max_total_reworks (default 10), staleness thresholds
- Forward compatibility: v1.0 config works with v1.1+ schema

**Test cases:** TC-050 through TC-058
**FR mapping:** FR-004

---

### 4.5 Pipeline Orchestrator

**Objective:** Confirm the 8-stage pipeline routes correctly with gate enforcement, rework loops, and sub-agent dispatch.

**Coverage:**
- 8 stages: Concept, Schematic, Layout, Prototype, DFM/DFA, Compliance, Pilot Run, Production Release
- Stage classification: AI-execution (stages 1-3, 5-6) vs human-execution (stages 4, 7, 8)
- Sequential progression with gate validation between stages
- Sub-agent dispatch via Agent tool (NOT inlined) for every stage
- Dispatch failure: retry-then-pause with error classification (TIMEOUT, CONTEXT_OVERFLOW, MODEL_ERROR, UNKNOWN)
- Gate enforcement: ALL validators DONE to advance; ANY NOT_DONE blocks with feedback
- Human Confirmation Gate for physical stages
- 8 rework paths: Prototype->Schematic, Prototype->Layout, DFM/DFA->Layout, DFM/DFA->Schematic, Compliance->Schematic, Compliance->Layout, Pilot Run->DFM/DFA, Pilot Run->Schematic
- Rework termination: per-path limit (3), total limit (10), human escalation
- Rework history: trigger reason, source, target, resolution, iteration count, total count

**Test cases:** TC-060 through TC-090
**FR mapping:** FR-002, FR-003, FR-007, FR-020

---

### 4.6 Validation Gates (Against Reference Fixture)

**Objective:** Confirm all 5 gates detect their target defect categories using the reference test fixture as ground truth.

**Coverage:**
- Reference fixture validated first (TC-400 through TC-406)
- Schematic Review Gate: iterative multi-reviewer, forced-find prompting, deduplication, 7 categories, >= 6/7 detection
- DRC Gate: consumes kicad-happy:kicad, detects 4 DFM violation types, DONE/NOT_DONE logic
- BOM Gate: lifecycle check (NRND/obsolete block), budget check, single-source warning, offline testable
- DFM Gate: fab-specific rules via kicad-happy:jlcpcb/pcbway, 4 seeded violations detected
- Compliance Gate: per-region checklists (FCC, CE), evidence linking, missing evidence blocks

**Test cases:** TC-140 through TC-163 (gates), TC-400 through TC-406 (fixture)
**FR mapping:** FR-010, FR-011, FR-012, FR-013, FR-014, FR-022

---

### 4.7 kicad-happy Integration

**Objective:** Confirm all 11 kicad-happy skills are consumable via cross-plugin Skill tool invocation.

**Coverage:**
- 11 skill dispatch: kicad, spice, digikey, mouser, lcsc, element14, jlcpcb, pcbway, bom, emc, kidoc
- Role-to-skill mapping: EE->kicad/spice/digikey/mouser/lcsc/element14, Layout->kicad, MfgE->jlcpcb/pcbway/bom, CompE->emc/kidoc
- SKILL_LOADED signal verification for each
- Failure modes: not installed (clear error + install instructions), version mismatch (warning), dispatch timeout, context overflow
- Non-reimplementation verification: no role SKILL.md parses .kicad_sch, queries APIs, or implements EMC checks directly
- Integration layer documentation: all 11 skills with dispatch pattern, expected I/O

**Test cases:** TC-100 through TC-120
**FR mapping:** FR-009

---

### 4.8 Security Controls

**Objective:** Confirm path sanitization and safe YAML loading throughout the plugin.

**Coverage:**
- All YAML loading uses yaml.safe_load() (never yaml.load() with unsafe Loader)
- Path construction prevents traversal (no ../ exploitation)
- Config file paths validated before access
- Hook scripts do not execute arbitrary user input
- No shell injection vectors in Python scripts

**Test cases:** TC-130 through TC-135
**FR mapping:** Cross-cutting security (NFR alignment)

---

## 5. FR Traceability Matrix

| FR ID | Requirement Summary | Priority | Test Case(s) | P1/P2 |
|-------|---------------------|----------|--------------|-------|
| FR-001 | Standard plugin structure | P1 | TC-001 through TC-005 | P1 |
| FR-002 | 8-stage pipeline with execution mode classification | P1 | TC-060 through TC-065 | P1 |
| FR-003 | Gate DoD validation (ALL validators must DONE) | P1 | TC-070 through TC-074 | P1 |
| FR-004 | Config-driven pipeline (.hardware/config.yml) | P1 | TC-050 through TC-058 | P1 |
| FR-005 | State persistence and resume | P2 | TC-080 through TC-082 | P2 |
| FR-006 | Self-learning memory | P2 | TC-083, TC-084 | P2 |
| FR-007 | Rework loops with termination | P1 | TC-085 through TC-090 | P1 |
| FR-008 | 6 role skills with context isolation + EE firmware docs | P1 | TC-010 through TC-023 | P1 |
| FR-009 | kicad-happy integration via cross-plugin invocation | P1 | TC-100 through TC-120 | P1 |
| FR-010 | Schematic Review Gate | P1 | TC-140 through TC-144 | P1 |
| FR-011 | DRC Gate | P1 | TC-145 through TC-148 | P1 |
| FR-012 | BOM Gate | P1 | TC-150 through TC-153 | P1 |
| FR-013 | DFM Gate | P1 | TC-155 through TC-158 | P1 |
| FR-014 | Compliance Gate | P1 | TC-160 through TC-163 | P1 |
| FR-015 | Design Review Board | P1 | TC-170 through TC-173 | P1 |
| FR-016 | BOM Reconciliation | P2 | TC-175, TC-176 | P2 |
| FR-017 | SessionStart hook (config + kicad-happy check) | P1 | TC-030 through TC-036 | P1 |
| FR-018 | PostToolUse DRC hook | P2 | TC-037, TC-038 | P2 |
| FR-019 | PostToolUse BOM drift hook | P2 | TC-039, TC-040 | P2 |
| FR-020 | Sub-agent dispatch via Agent tool (NOT inlined) | P1 | TC-066, TC-067 | P1 |
| FR-021 | Dynamic pipeline adaptation | P2 | N/A | P2 deferred |
| FR-022 | Reference test fixture with seeded defects | P1 | TC-400 through TC-406 | P1 |

**Coverage:** 21/22 FRs have mapped test cases. FR-021 is explicitly P2 deferred. 100% P1 FR coverage.

---

## 6. NFR Verification Plan

| NFR ID | Requirement | Verification Method | Pass Criterion |
|--------|-------------|---------------------|----------------|
| NFR-001 | No external Python dependencies | `grep -r "^import\|^from" hardware-team/scripts/ hardware-team/hooks/` | 0 non-stdlib imports |
| NFR-002 | Context isolation per role | Load each of 6 roles, audit reference files loaded | 0 cross-role references loaded |
| NFR-003 | kicad-happy consumed, never duplicated | Code review per reimplementation checklist (Section 4.7) | 0 reimplemented capabilities |
| NFR-004 | Pipeline completes 8 stages in single session | End-to-end run on reference project | All 8 stages complete |
| NFR-005 | Gate messages comprehensible | Review output: what/where/why/how present | All 4 elements in every gate message |
| NFR-006 | Forward-compatible config schema | Test v1.0 config against v1.1+ schema | Old config uses defaults, no errors |
| NFR-007 | Model tier documented per role | Audit 6 role SKILL.md files | Each specifies minimum tier |
| NFR-008 | Memory retrieval <2s | Benchmark with 100+ entries | p95 < 2s (P2 -- deferred) |
| NFR-009 | Plugin passes plugin-validator | Run `plugin-dev:plugin-validator` | 0 validation errors |
| NFR-010 | Rework history auditable | Inspect .hardware/state.md after rework | 100% events logged with all fields |

---

## 7. Test Execution Schedule

| Phase | Test Area | Priority | Dependencies |
|-------|-----------|----------|--------------|
| Phase 1 | Plugin installation (TC-001 through TC-005) | P0 | EC-1, EC-5 |
| Phase 1 | Reference fixture validation (TC-400 through TC-406) | P0 | EC-4 |
| Phase 2 | Skill discoverability + context isolation (TC-010 through TC-023) | P0 | Phase 1 pass |
| Phase 2 | Hook execution (TC-030 through TC-042) | P1 | Phase 1 pass |
| Phase 2 | Config validation (TC-050 through TC-058) | P1 | Phase 1 pass |
| Phase 3 | kicad-happy integration (TC-100 through TC-120) | P0 | EC-3, Phase 2 pass |
| Phase 3 | Security controls (TC-130 through TC-135) | P1 | Phase 2 pass |
| Phase 4 | Pipeline orchestrator (TC-060 through TC-090) | P0 | Phase 3 pass |
| Phase 5 | Validation gates against fixture (TC-140 through TC-163) | P0 | Phase 3, Phase 4 pass |
| Phase 5 | Design Review Board (TC-170 through TC-173) | P1 | Phase 4 pass |

---

## 8. Risk-Based Test Prioritization

| Priority | Test Area | Rationale |
|----------|-----------|-----------|
| P0 (Critical) | Cross-plugin kicad-happy invocation (TC-100 through TC-115) | Foundation dependency -- if this fails, nothing works |
| P0 (Critical) | Gate enforcement (TC-070, TC-071) | Core quality mechanism -- gates must block |
| P0 (Critical) | Reference fixture completeness (TC-400 through TC-406) | All gate testing depends on fixture integrity |
| P0 (Critical) | Plugin structure (TC-001 through TC-005) | Everything depends on correct structure |
| P1 (High) | Pipeline stage routing (TC-060 through TC-067) | Core orchestration flow |
| P1 (High) | Rework termination (TC-089, TC-090) | Prevents infinite loops |
| P1 (High) | Context isolation (TC-010 through TC-023) | Architecture integrity |
| P2 (Medium) | Config validation (TC-050 through TC-058) | Graceful degradation on bad config |
| P2 (Medium) | SessionStart hooks (TC-030 through TC-036) | Early warning system |
| P3 (Low) | State persistence (TC-080 through TC-082) | P2 story |
| P3 (Low) | Memory system (TC-083, TC-084) | P2 story |

---

## 9. Dogfooding Evidence

This GREENFIELD pipeline run IS the dogfooding evidence. The delivery-flow pipeline exercised the plugin architecture through all 7 delivery stages:

1. **Idea** -- Hardware-team plugin concept defined
2. **Refine** -- PRD v1.1 produced with 22 FRs, 5 blocking adversarial challenges resolved
3. **Design** -- Architecture v1.4 with 8-stage pipeline, 6 roles, 5 gates
4. **Architect** -- ADRs for pipeline topology, namespace, integration strategy
5. **Plan** -- Test strategy, sprint plan, dependency map
6. **Development** -- Plugin skeleton, skills, hooks, scripts, reference fixture
7. **UAT** -- This test plan and companion test cases (current stage)

The pipeline itself validates: sub-agent dispatch (FR-020), role context isolation (FR-008), gate enforcement (FR-003), and the collaboration patterns the hardware-team plugin mirrors.

---

## 10. Minimum Regression Suite

When time is limited after changes, the minimum regression suite covers:

1. Plugin structure validation (TC-001) -- structural integrity
2. Pipeline happy path (TC-060 through TC-065) -- core flow
3. One gate test (TC-140 Schematic Review against fixture) -- gate mechanism
4. Context isolation spot check (2 roles: EE + MfgE) -- isolation integrity
5. Cross-plugin dispatch (kicad-happy:kicad) -- integration health
6. Config load with defaults (TC-052) -- config mechanism
7. SessionStart hook (TC-030, TC-033) -- hook mechanism

---

## 11. Test Environment

| Requirement | Detail |
|-------------|--------|
| Claude Code | Current version with Agent tool and Skill tool |
| kicad-happy | v1.2.0+ at `~/.claude/plugins/cache/kicad-happy/kicad-happy/1.2.0/` (all 11 skills) |
| Python | 3.x (standard library only) |
| KiCad | Optional -- for fixture file validation only |
| Reference fixture | `hardware-team/references/test-fixtures/` fully populated |
| Filesystem | Write access for `.hardware/` directory creation |

---

## 12. Defect Handling

- **P0** = blocks merge. Route to dev immediately; cannot ship.
- **P1** = ship-blocker unless explicit waiver from PO + Architect.
- **P2/P3** = log to `.delivery/defects/` and surface in retrospective; ship allowed.
- All defects reference the failing TC ID and the specific FR/AC violated.

---

*Test plan authored by Legolas. My eyes see far and they see every defect. That bug still only counts as one.*
