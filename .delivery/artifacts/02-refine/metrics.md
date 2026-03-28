# Success Metrics: Clean Code Foundational Standards

**Feature**: Clean Code Foundational Standards
**Date**: 2026-03-27
**Author**: Data Analyst

---

## North Star Metric

### Clean Code Violation Rate

**Definition**: The percentage of code review findings classified as clean code violations out of total lines changed, measured across all PR reviews that use the `code-reviewer` or `code-simplifier` agents.

**Formula**: `(clean_code_violations / total_lines_changed) * 100`

**Source**: PR review agent output (violation counts per review) and git diff stats (lines changed).

**Target**: Below 5% within 4 sprints of adoption; below 2% within 8 sprints.

**Baseline**: No current measurement exists. First 2 sprints after launch establish the baseline.

**Cadence**: Per sprint (rolling average).

**Rationale**: This metric directly measures whether the foundational standards are reducing the incidence of clean code problems in generated and reviewed code. A declining violation rate over time proves the feature is working -- developers (human and AI-assisted) are internalizing the principles.

---

## Supporting Metrics

### 1. Adoption Rate (Default Guide)

**Definition**: Percentage of active delivery projects that have the clean code reference loaded (either default `clean-code.md` or a custom guide via `tech_stack.clean_code_guide`).

**Formula**: `(projects_with_clean_code_loaded / total_active_projects) * 100`

**Source**: Session start hook telemetry -- config check hook already validates config at session start; extend to log whether clean code guide is present and which type (default vs custom).

**Target**: 100% within 2 sprints (since loading is automatic for default, this measures that no projects have broken configs that prevent loading).

**Baseline**: 0% (feature does not exist yet).

**Cadence**: Weekly.

---

### 2. Custom Guide Adoption Rate

**Definition**: Percentage of active delivery projects using a custom coding standards file (`tech_stack.clean_code_guide` set to a non-empty path) rather than the built-in default.

**Formula**: `(projects_with_custom_guide / total_active_projects) * 100`

**Source**: Config check hook telemetry at session start.

**Target**: 20% within 6 sprints (indicates teams find value in customization without it being required).

**Baseline**: 0%.

**Cadence**: Monthly.

---

### 3. Context Window Impact (Token Budget)

**Definition**: Additional tokens consumed by loading `clean-code.md` as a percentage of the total available context window per developer/godot sub-agent invocation.

**Formula**: `(clean_code_reference_tokens / total_context_window_tokens) * 100`

**Source**: Token count of `clean-code.md` (static measurement at authoring time); sub-agent prompt template token audit.

**Target**: Below 2% of context window (approximately 2,000 tokens for a 200K context window). Must not exceed 3,000 tokens.

**Baseline**: 0 tokens (no clean code reference currently loaded).

**Cadence**: Per release (measured when the reference file is modified).

**Alert threshold**: If the file exceeds 3,000 tokens, it must be trimmed or split into tiered loading before release.

---

### 4. Developer Task Completion Rate

**Definition**: Percentage of developer/godot sub-agent tasks that complete successfully (produce accepted output) after clean code reference loading is introduced, compared to the pre-feature baseline.

**Formula**: `(successful_task_completions / total_task_invocations) * 100`

**Source**: Delivery pipeline stage completion records (Development and UAT stages).

**Target**: No regression -- must remain within 2 percentage points of baseline. Any drop greater than 2 points triggers investigation into whether the added context is causing failures.

**Baseline**: Measure current completion rate over 2 sprints before launch.

**Cadence**: Per sprint.

---

### 5. Enforcement Mode Distribution

**Definition**: Ratio of projects using `block` enforcement versus `warn` enforcement for clean code violations in code review.

**Formula**: `block_count : warn_count` (reported as percentages of total).

**Source**: Config values read at session start.

**Target**: At least 70% of projects on `block` mode after 4 sprints. A high `warn` rate may indicate the standards are too strict or producing too many false positives.

**Baseline**: 100% `block` (default behavior when no config override exists).

**Cadence**: Monthly.

---

### 6. Scaffold Command Usage

**Definition**: Number of times the `coding-standards` scaffold command is invoked to generate a starter template.

**Formula**: Count of scaffold invocations.

**Source**: Command invocation logs.

**Target**: At least 5 invocations within the first 4 sprints (indicates teams are discovering and using the customization path).

**Baseline**: 0 (command does not exist yet).

**Cadence**: Monthly.

---

## Measurement Plan

| Metric | Data Source | Collection Method | Owner |
|--------|-----------|-------------------|-------|
| Clean Code Violation Rate | PR review agent output | Parse violation counts from review output; correlate with git diff stats | Data Analyst |
| Adoption Rate (Default) | Config check hook | Extend hook to log clean code loading status | DevOps |
| Custom Guide Adoption | Config check hook | Log `tech_stack.clean_code_guide` presence and value | DevOps |
| Context Window Impact | Token counter on reference file | Static analysis at authoring/release time | Developer |
| Task Completion Rate | Pipeline stage records | Query pipeline state persistence data | Data Analyst |
| Enforcement Mode Distribution | Config check hook | Log `tech_stack.clean_code_enforcement` value | DevOps |
| Scaffold Command Usage | Command invocation log | Count invocations | Data Analyst |

## Success Criteria

The feature is considered successful when, after 4 sprints of adoption:

1. The north star metric (clean code violation rate) shows a downward trend from the established baseline
2. Adoption rate is at 100% (all projects loading some form of clean code reference)
3. Context window impact stays below 2% of available context
4. Developer task completion rate shows no regression (within 2 percentage points of baseline)
5. At least 70% of projects remain on `block` enforcement (standards are not too strict to be practical)

## Risks to Measurement

| Risk | Impact | Mitigation |
|------|--------|------------|
| No existing violation tracking infrastructure | Cannot measure north star metric without tooling | Build violation counting into PR review agent output as part of the feature itself |
| Baseline period too short | Unreliable baseline leads to false trend signals | Use 2 full sprints minimum; flag results as provisional until 4 sprints of data exist |
| Small sample size (few active projects) | Statistical noise dominates real signal | Report raw counts alongside percentages; defer trend analysis until N >= 10 reviews |
| Token count varies by model context window | 2% target is model-dependent | Report absolute token count alongside percentage; set absolute ceiling at 3,000 tokens |
