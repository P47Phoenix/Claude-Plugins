# Metrics Definition: Hardware Delivery Team Plugin

**Product:** hardware-team plugin
**Version:** 1.0
**Author:** Data Analyst (Elrond)
**Pipeline:** run-2026-04-12-hw01
**Last Updated:** 2026-04-12

---

> "I was there three thousand sprints ago, when the metrics last failed. Let these definitions endure longer than the last."

---

## North Star Metric

**Metric:** Pipeline Completion Rate
**Definition:** The percentage of hardware-team pipeline runs that successfully produce artifacts across all configured stages without manual intervention to bypass a broken gate or missing skill.
**Formula:** `(pipeline_runs_completing_all_configured_stages / pipeline_runs_started) * 100`
**Target:** 80% completion rate within first 3 months of deployment (Sprint 5-8 window).
**Baseline:** 0% -- no structured hardware pipeline exists today. Hardware development is ad-hoc.
**Data Source:** `.hardware/state.md` -- parse stage completion records from pipeline state files.
**Collection Frequency:** Per pipeline run, aggregated monthly.
**Leading Indicator:** Stage gate pass rate at stages 1-4 (early stages passing predicts full run completion).
**Lagging Indicator:** This metric itself is lagging -- it measures outcomes already occurred.
**Note:** A run counts as "complete" if all stages configured for that project type finish (e.g., a hobby project configured to skip Compliance and Pilot Run is "complete" at 6/6 configured stages, not 6/8 total stages).

---

## Supporting Metrics

### M1: kicad-happy Skill Utilization Rate

| Field | Value |
|-------|-------|
| **Definition** | The percentage of the 11 kicad-happy skills that are successfully mapped in the integration layer and invoked at least once during a full pipeline run. |
| **Formula** | `(kicad_happy_skills_successfully_invoked / 11) * 100` |
| **Target** | 100% mapping (11/11 in integration layer); 80%+ invocation per certified-product pipeline run (9+ skills invoked). |
| **Baseline** | 0% orchestrated utilization. Skills are used ad-hoc, one at a time, with no pipeline coordination. |
| **Collection Frequency** | Static mapping verified at plugin release. Runtime invocation measured per pipeline run. |

**Measurement Method:**
1. **Static check (mapping):** Inspect the integration layer reference file. Count kicad-happy skills with explicit dispatch patterns. Target: 11/11 mapped.
2. **Runtime check (invocation):** After a pipeline run, inspect `.hardware/state.md` for skill invocation records. Each invocation is logged with: skill name, invoking role, stage, timestamp, success/failure.

**Data Source:** Integration layer mapping file (static); `.hardware/state.md` invocation log (runtime).

**Leading Indicator:** Integration layer mapping completeness predicts runtime invocation success.
**Lagging Indicator:** Runtime invocation failures that trace back to missing or broken mappings.

**Counter-Metric:** Zero reimplemented kicad-happy capabilities. Verify via code review: search for duplicated search patterns, API call logic, or analysis algorithms in `hardware-team/` that already exist in `kicad-happy/`.

---

### M2: Defect Detection Rate (Schematic Review Gate)

| Field | Value |
|-------|-------|
| **Definition** | The percentage of reviewable defect categories where the Schematic Review Gate identifies at least one seeded defect, measured against a reference schematic with known defects. |
| **Formula** | `(defect_categories_with_at_least_one_detection / total_defect_categories_seeded) * 100` |
| **Target** | >80% category detection rate (6 out of 7 categories minimum). |
| **Baseline** | Unknown -- no structured schematic review gate exists. Issue #76 documented 30+ real defects caught by iterative review agents, but no systematic detection rate was measured against a controlled benchmark. |
| **Collection Frequency** | Measured at plugin release (M4 milestone) and after each gate algorithm change. |

**Measurement Method:**
1. Create a reference KiCad schematic (`.kicad_sch`) with exactly 10 seeded defects across all 7 review categories:
   - Power integrity (e.g., missing bulk capacitor on voltage regulator)
   - Signal integrity (e.g., unterminated high-speed trace)
   - Component derating (e.g., capacitor rated at exactly operating voltage)
   - Missing pull-ups/pull-downs (e.g., floating I2C lines)
   - Decoupling strategy (e.g., missing decoupling cap on IC power pin)
   - Voltage level compatibility (e.g., 5V signal to 3.3V input without level shifter)
   - Thermal considerations (e.g., high-power component without thermal relief)
2. Run the Schematic Review Gate against the reference schematic.
3. Collect all findings. Map each finding to its defect category.
4. Score: category detected if at least one defect in that category was found.

**Data Source:** Gate output artifact (findings list with category, severity, location). Reference schematic stored in `hardware-team/references/test-fixtures/`.

**Leading Indicator:** Number of review passes configured (more passes = higher detection). Forced-find prompting enabled = higher detection.
**Lagging Indicator:** Post-prototype defects that trace back to categories the gate should have caught.

**Counter-Metric:** False positive rate. Target: <30%. Formula: `(findings_not_matching_actual_defects / total_findings) * 100`. High detection achieved by flagging everything is valueless.

---

### M3: Role Context Isolation Compliance

| Field | Value |
|-------|-------|
| **Definition** | The percentage of role skill invocations where zero cross-role reference files are loaded. |
| **Formula** | `(invocations_with_zero_cross_role_refs / total_role_invocations) * 100` |
| **Target** | 100% isolation compliance across all 6 role skills. |
| **Baseline** | N/A -- new plugin, no prior invocations exist. |
| **Collection Frequency** | Static audit at plugin release. Runtime audit per pipeline run. |

**Measurement Method:**
1. **Static audit:** For each of the 6 role SKILL.md files, extract the reference loading directives. Verify no role references another role's files:
   - HW Product Owner: loads only HW PO references
   - Electrical Engineer: loads only EE references
   - PCB Layout Engineer: loads only Layout references
   - Manufacturing Engineer: loads only MfgE references
   - Compliance Engineer: loads only CompE references
   - Test Engineer: loads only TestE references
2. **Runtime audit:** After a pipeline run, inspect sub-agent invocation logs in `.hardware/state.md`. For each role invocation, verify loaded references match ONLY the expected set. Any cross-role reference file is a violation.

**Data Source:** SKILL.md files (static); sub-agent invocation logs in `.hardware/state.md` (runtime).

**Leading Indicator:** Static audit passes (correctly defined SKILL.md files predict runtime isolation).
**Lagging Indicator:** Context window overflow or confused/hybrid role outputs indicate isolation failure.

---

### M4: Config-Driven Flexibility Score

| Field | Value |
|-------|-------|
| **Definition** | The number of distinct project type configurations that produce a correctly adapted pipeline run without code changes. |
| **Formula** | Count of distinct `.hardware/config.yml` configurations that produce complete pipeline runs with adapted stage depth, gate strictness, and role emphasis. |
| **Target** | 3+ project types supported. |
| **Baseline** | 0 -- no config-driven pipeline exists. |
| **Collection Frequency** | Measured at M7 milestone. Re-measured when config schema evolves. |

**Measurement Method:**
1. Create 3 distinct `.hardware/config.yml` files:
   - **1-layer prototype** (hobby/maker): Compliance and Pilot Run minimized/skipped; BOM budget relaxed.
   - **4-layer IoT device** (startup): Full pipeline, standard gate strictness, JLCPCB target fab.
   - **8-layer certified product** (regulated): Full pipeline, strict gates, FCC+CE compliance, second-source required.
2. Run the pipeline with each config.
3. Verify per run:
   - Stage depth adapts (prototype skips Compliance/Pilot; certified enforces full Compliance).
   - Gate strictness matches config.
   - Target fab rules are applied correctly.
   - BOM budget threshold matches config value.
4. Score: 1 point per project type passing all checks.

**Data Source:** `.hardware/config.yml` files (input); `.hardware/state.md` stage execution records (output).

**Leading Indicator:** Config schema completeness (does the schema have fields for all differentiating parameters?).
**Lagging Indicator:** User-reported config failures ("my config was ignored").

---

### M5: Rework Loop Effectiveness

| Field | Value |
|-------|-------|
| **Definition** | The percentage of the 6 defined rework paths that correctly return the pipeline to the target stage, re-execute, and re-validate all downstream gates. |
| **Formula** | `(rework_paths_executed_correctly / 6) * 100` |
| **Target** | 100% (6/6 paths function correctly). |
| **Baseline** | 0% -- no rework support exists. |
| **Collection Frequency** | Measured at M7 milestone. Re-measured after pipeline architecture changes. |

**Measurement Method:**
For each of the 6 rework paths, create a test scenario and verify:

| Rework Path | Trigger Scenario |
|-------------|-----------------|
| Prototype -> Schematic | Prototype failure traces to schematic error |
| Prototype -> Layout | Prototype failure traces to layout error |
| DFM/DFA -> Layout | DFM violation requires layout change |
| DFM/DFA -> Schematic | DFM violation requires schematic change |
| Compliance -> Schematic | Compliance failure requires design change |
| Pilot Run -> DFM/DFA | Pilot yield issue requires DFM revision |

**Verification per path:**
- Pipeline returns to the correct target stage
- Target stage has access to original artifacts AND rework reason
- All downstream gates from the target are re-validated (not skipped)
- Rework history is logged with: trigger reason, source stage, target stage, timestamp, resolution

**Data Source:** `.hardware/state.md` rework history section.

**Leading Indicator:** Rework path definitions exist in orchestrator SKILL.md.
**Lagging Indicator:** Pipeline runs that get stuck because a rework path fails silently.

---

### M6: Gate Quality Score

| Field | Value |
|-------|-------|
| **Definition** | The percentage of gate findings (across all 5 gates) that include all 4 required fields: location, severity, description, and remediation guidance. |
| **Formula** | `(findings_with_all_4_fields / total_findings) * 100` |
| **Target** | 100% of findings include all 4 required fields. |
| **Baseline** | 0% -- no gates exist, no findings exist. |
| **Collection Frequency** | Measured at M4 milestone. Re-measured per gate algorithm change. |

**Measurement Method:**
1. Run all 5 gates (Schematic Review, DRC, BOM, DFM, Compliance) against a reference KiCad project that triggers findings in each gate.
2. Collect all findings.
3. For each finding, verify presence and non-empty values for:
   - **Location:** Component, net, sheet, layer, or coordinates
   - **Severity:** Critical, Major, or Minor
   - **Description:** What the issue is, in hardware engineer language
   - **Remediation:** Specific fix guidance
4. Score: finding passes if all 4 fields present and non-empty.

**Data Source:** Gate output artifacts in `.hardware/artifacts/`.

**Leading Indicator:** Gate prompt templates include explicit output format requirements.
**Lagging Indicator:** User complaints about unhelpful gate messages.

**Counter-Metric:** Gate false positive rate (see M2). Quality scores are meaningless if findings are fabricated.

---

### M7: Pipeline Stage Artifact Production

| Field | Value |
|-------|-------|
| **Definition** | The percentage of pipeline stages that produce at least one well-formed artifact upon completion. |
| **Formula** | `(stages_with_at_least_one_artifact / 8) * 100` |
| **Target** | 100% -- every stage produces at least one artifact. |
| **Baseline** | 0% -- no pipeline stages exist. |
| **Collection Frequency** | Per pipeline run. |

**Measurement Method:**
1. Run a full pipeline on a reference KiCad project.
2. After each stage, verify at least one artifact file exists in `.hardware/artifacts/<stage-name>/`.
3. Verify each artifact is non-empty and follows the expected format.

**Data Source:** `.hardware/artifacts/` directory structure; `.hardware/state.md` artifact path records.

**Leading Indicator:** Stage SKILL.md files define expected output artifacts.
**Lagging Indicator:** Downstream stages failing because upstream artifacts are missing.

---

## Metric Summary Table

| ID | Metric | Type | Target | Baseline | Source | Cadence |
|----|--------|------|--------|----------|--------|---------|
| NS | Pipeline Completion Rate | Lagging | 80% | 0% | `.hardware/state.md` | Monthly |
| M1 | kicad-happy Utilization | Leading + Lagging | 100% mapped, 80%+ invoked | 0% | Integration layer + state | Per run |
| M2 | Defect Detection Rate | Lagging | >80% categories | Unknown | Gate output vs. seeded defects | Per release |
| M3 | Context Isolation Compliance | Leading | 100% | N/A | SKILL.md audit + invocation logs | Per run |
| M4 | Config-Driven Flexibility | Lagging | 3+ project types | 0 | Config files + state | Per release |
| M5 | Rework Loop Effectiveness | Lagging | 100% (6/6 paths) | 0% | `.hardware/state.md` rework log | Per release |
| M6 | Gate Quality Score | Leading | 100% fields present | 0% | Gate output artifacts | Per release |
| M7 | Stage Artifact Production | Leading | 100% (8/8 stages) | 0% | `.hardware/artifacts/` | Per run |

---

## Metric Dependencies and Relationships

> "The trends are clear to those who have watched long enough. These metrics do not stand alone -- they form a causal chain."

```
M3 (Isolation) --> M7 (Artifacts) --> M6 (Gate Quality) --> M2 (Detection Rate)
                                                         \
M1 (Utilization) --> M6 (Gate Quality) -----------> NS (Pipeline Completion)
                                                         /
M4 (Config Flex) --> M5 (Rework Loops) -----------------
```

- **M3 enables M7:** Correct role isolation produces correct artifacts.
- **M7 enables M6:** Gates can only evaluate quality if stage artifacts exist.
- **M6 enables M2:** Well-formed gate findings are prerequisite for measuring detection rate.
- **M1 enables M6:** Gates consuming kicad-happy skills need those skills to be available.
- **M4 enables M5:** Config-driven flexibility includes rework path configuration.
- **All flow to NS:** Pipeline completion depends on all upstream metrics being healthy.

---

## Collection Infrastructure

All metrics are measurable within the Claude Code plugin ecosystem using file-based artifacts. No external analytics platforms, databases, or instrumentation SDKs are required.

| Infrastructure | Purpose | Location |
|---------------|---------|----------|
| Pipeline state file | Stage completions, gate results, skill invocations, rework events | `.hardware/state.md` |
| Artifact store | Stage output artifacts including gate findings | `.hardware/artifacts/<stage-name>/` |
| Project config | Pipeline parameterization per project type | `.hardware/config.yml` |
| Skill definitions | Role reference loading directives for isolation audit | `hardware-team/skills/*/SKILL.md` |
| Test fixtures | Reference KiCad projects with seeded defects for benchmarks | `hardware-team/references/test-fixtures/` |

---

## Traceability: PRD Success Metrics to Metric Definitions

| PRD Success Metric | This Document | Coverage |
|-------------------|---------------|----------|
| Pipeline coverage (8 stages, all artifacts) | NS + M7 | Pipeline Completion Rate measures end-to-end; M7 measures per-stage artifact production |
| kicad-happy utilization (11/11, 0 reimplemented) | M1 | Static mapping + runtime invocation + counter-metric for reimplementation |
| Defect detection rate (>80% categories) | M2 | 7-category benchmark with seeded defects + false positive counter-metric |
| Role context isolation (zero bleed) | M3 | Static SKILL.md audit + runtime invocation log verification |
| Config-driven flexibility (3+ project types) | M4 | 3 project type configs with verification checks |
| Rework loop effectiveness (6 paths) | M5 | Per-path test scenarios with 4-point verification |
| Gate quality (actionable findings) | M6 | 4-field completeness check on all gate findings |

---

## Open Questions

| # | Question | Impact |
|---|----------|--------|
| MQ-001 | Should the false positive rate counter-metric (M2) be measured against the same seeded-defect reference schematic, or against real-world schematics contributed by early users? | Medium -- seeded defects may not represent real-world distributions. |
| MQ-002 | Does a failed kicad-happy invocation (skill unavailable) count as an attempt for M1? | Low -- affects denominator. Current assumption: only successful invocations count toward utilization. |
| MQ-003 | How should Pipeline Completion Rate (NS) handle intentionally abbreviated runs (hobby project skipping Compliance)? | High -- resolved by defining "complete" as all configured stages, not all 8 stages. |

---

> "I have counseled this council before: define your metrics precisely, or the data will betray you. These definitions shall endure -- provided you collect the baselines before you set the targets."

---
