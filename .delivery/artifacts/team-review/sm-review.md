# Scrum Master Process & Health Review

**Reviewer**: Aragorn (Scrum Master)
**Date**: 2026-04-04
**Scope**: Delivery pipeline runs 1-13, memory system, hooks, config, process health
**Runs reviewed**: 13 total (archive files for runs c8f2 through w7m3)

---

## Executive Summary

The fellowship has marched far -- 13 pipeline runs, a memory system that learns, and a team that files its own bugs. But even Minas Tirith has crumbling walls that need tending. This review surfaces five critical findings, three moderate concerns, and several opportunities. The pipeline is healthy and improving, but specific areas need attention before technical debt compounds.

---

## 1. Critical Findings

### 1.1 Dead Hook: `enforce_pipeline_scope.py` is Not Registered

**Severity**: Critical
**Evidence**: The file `delivery-team/hooks/enforce_pipeline_scope.py` exists (213 lines of working code) but is NOT registered in `hooks.json`. There is no `PreToolUse` hook with matcher `Write|Edit` that calls this script.

The hooks.json `PostToolUse` entry for `Write|Edit` calls `validate_gdscript.py`, not `enforce_pipeline_scope.py`. The `PreToolUse` section only has `Skill` and `Agent` matchers -- no `Write|Edit` matcher exists.

**Impact**: The entire pipeline scope enforcement system -- which should warn when source code is edited outside an active pipeline -- is inert. The config key `enforcement.source_code_hook: true` gives a false sense of protection. Every edit in the last 13 runs has bypassed this guardrail without detection.

**Action**: Register the hook in `hooks.json` under `PreToolUse` with matcher `Write|Edit`, or remove the dead code and the config key that references it.

### 1.2 Missing Memory File: `topics/team-decisions.md`

**Severity**: Critical
**Evidence**: `memory/index.md` (line 34) references `topics/team-decisions.md` with instruction "Read before Architect or Plan stages." The file does not exist. No file named `team-decisions.md` exists anywhere in `.delivery/memory/`.

**Impact**: Every Architect and Plan stage for all 13 runs has skipped loading team decisions because the file is missing. The index promises context that is never delivered. Given that Plan is already the weakest stage (57-80% first-try pass rate), missing context here directly contributes to failures.

**Action**: Create `topics/team-decisions.md` and populate it with the architectural decisions documented across runs (ADR-001 from c8f2, DD1-DD4 from k4m9, ADR-047 from p8n5, etc.).

### 1.3 Pipeline Bypass Detection Hook Has a Coverage Gap

**Severity**: High
**Evidence**: The `PreToolUse` Skill hook in `hooks.json` checks for `.delivery/config.yml` existence as a proxy for "active pipeline." But it does not check `state.md` for `status: in_progress`. A project with a config file but no active pipeline (status: completed or no state file) would pass the check.

The hook correctly catches the case where no config exists at all, but the more common scenario -- config exists from a previous run, developer skill invoked for a quick fix outside the pipeline -- is not caught.

**Impact**: The bypass detection gives a false positive ("config exists, must be in pipeline") when the real question is "is a pipeline currently running?" This undermines the preference documented in `human-preferences.md`: "ALL implementation must go through delivery-flow pipeline."

**Action**: The hook should check for `state.md` with `status: in_progress`, not just config file existence. The `enforce_pipeline_scope.py` script already has the correct logic (`_has_active_pipeline`) -- but that script is dead (Finding 1.1).

### 1.4 Installed-vs-Source Sync Gap: Recurring 3 Times, Not Systemically Fixed

**Severity**: High
**Evidence**:
- Run j8f2 (lesson L-1): "Second recurrence of installed-vs-source confusion"
- Run w7m3 (lesson): "Developer should proactively diff source vs installed plugin files BEFORE DoD submission"
- `stages/development.md` entry 4: "Two consecutive runs (j8f2, w7m3) required correction rounds for the same class of issue"
- `stages/uat.md` entries 5-6: Both directions of the gap documented

The lesson has been written down three times but the fix is behavioral ("add as pre-DoD step"). There is no automated check. The Dev DoD validators catch it reactively, but the lesson says the validator should be a safety net, not the primary mechanism.

**Impact**: Each occurrence burns a self-correction round. Two correction rounds across j8f2 and w7m3 represent wasted cycles on a known, documented problem.

**Action**: Create a hook or script that diffs installed vs source plugin files and runs automatically before Dev DoD submission. The lesson has been learned; it needs to be encoded.

### 1.5 Config Drift: `project_type: FEATURE` is a Lie

**Severity**: High
**Evidence**: `.delivery/config.yml` line 2 sets `project_type: FEATURE`, but runs 1-13 include GREENFIELD (k3r9), BUG_FIX (b4e1, m7v3, j8f2, w7m3), SPIKE (p8n5), DOCS_ONLY (d8m1), and FEATURE (c8f2, k4m9, h3k7, r4x2, p5v8, t2k6). The config type is overridden at runtime for every non-FEATURE run.

This is not harmful because Phase 1 detects the type from user input, but it means the config is misleading. The `wizard_completed: 2026-03-29` date suggests the wizard was run once and never updated, despite 7 different project types being used since.

**Action**: Either set `project_type: auto` to reflect actual usage, or accept that this config key is advisory only and document that behavior.

---

## 2. Stage Health Analysis

### Stage Health Trends (Runs 1-13)

| Stage | Index Rate (Last 5) | Full History | Trend | Assessment |
|-------|---------------------|-------------|-------|------------|
| Idea | 100% | 100% (13/13) | Stable | No action needed |
| Refine | 100% | ~90% | Stable | Healthy (adversarial review adding value) |
| Design | 100% | ~70% | Improving | Gate-patterns memory injection fixed this -- validated |
| Architect | 100% | ~90% | Stable | Healthy |
| Plan | 80% | 57-80% | Improving | Was systemic weak point; pre-loaded constraints helping |
| Development | 60% | ~75% | Dipped | Installed-vs-source sync gap is the recurring cause |
| UAT | 100% | ~85% | Improving | Dogfooding enforcement resolved prior failures |

**Key observation**: Design and Plan were the weakest stages in runs 1-9. Memory injection (gate-patterns before Design, pre-loaded constraints in Plan) has measurably improved both. The memory system is working for these stages. Development has now become the weakest stage due to the recurring sync gap issue.

---

## 3. Retro Action Item Tracking

### Action Items from Earlier Runs -- Status

| Run | Action Item | Status | Evidence |
|-----|------------|--------|----------|
| c8f2 (run 1) | FR traceability before Design DoD | Addressed | Design stage lesson, validated 1x |
| c8f2 (run 1) | Regenerate derived artifacts after source changes | Partially | Lesson exists but p5v8 hit same issue (stale config-schema.json) |
| c8f2 (run 1) | Issues #50-53 logged | #50 fixed (j8f2), #51-53 addressed (r4x2) | All resolved |
| b4e1 (run 2) | TC-4 full pipeline run deferred | Addressed | h3k7 served as full pipeline dogfooding |
| k4m9 (run 3) | Alias theme loading fix | Addressed | Spike completed, then j8f2 fixed residual bug |
| h3k7 (run 4) | Gate-patterns memory injection -- validate over 2 runs | Validated | r4x2 confirmed (100% first-try), k3r9 maintained |
| h3k7 (run 4) | Markdown estimates calibration | Documented | plan.md lesson exists, no recurrence |
| r4x2 (run 5) | Session loss as delivery metric | Not addressed | No tracking mechanism added |
| r4x2 (run 5) | Structural-only validation caps confidence | Documented | uat.md lesson exists |
| r4x2 (run 5) | FEATURE routing for refactoring sub-type | Not addressed | No routing change made |
| k3r9 (run 8) | Pre-loaded constraints for Plan agents | Addressed | Runs 10-13 show improvement (80% vs prior 57%) |
| k3r9 (run 8) | Agent validation must be API-driven | Documented | defect-patterns.md entry exists |

### Unaddressed Action Items

1. **Session loss tracking** (from r4x2): "Session loss is a delivery metric" -- no mechanism tracks this. Only r4x2 and k3r9 recorded session counts.
2. **FEATURE routing for refactoring** (from r4x2, L-5): "FEATURE routing should consider refactoring sub-type for Architect stage" -- no routing change made to the matrix.
3. **Stale derived artifacts** keep recurring: c8f2 first logged it, p5v8 hit it again with config-schema.json. The lesson exists but the behavior has not been automated.

---

## 4. Memory System Effectiveness

### What is Working

- **Gate-patterns injection**: The single strongest improvement lever. Run r4x2 achieved the first-ever 100% first-try rate (6/6 stages) after gate-patterns were loaded pre-stage. Subsequent runs maintained the improvement.
- **Stage chunk files**: 4 stage files (design, plan, development, uat) with 18 total entries. Entries have validation counts showing they are being re-confirmed across runs.
- **Topic files**: 4 of 5 referenced topics exist with useful, current content.
- **Index file**: Well-structured routing table with stage health metrics updated after each run.

### What is Not Working

- **`team-decisions.md` is missing** (Finding 1.2): Referenced in index, never created. Zero decisions loaded in 13 runs.
- **`stages/idea.md` does not exist**: Idea has a 100% pass rate so this may not matter, but it means lessons from Idea (e.g., phantom file references from k4m9) are only captured in gate-patterns, not in a stage-specific chunk.
- **`stages/refine.md` does not exist**: Refine lessons are only in gate-patterns. No stage-specific file despite adversarial review insights across multiple runs.
- **`stages/architect.md` does not exist**: Architect lessons live only in gate-patterns.
- **No Idea/Refine/Architect stage chunks**: The index only lists Design, Plan, Development, UAT. Three stages have no dedicated chunk files. Lessons from those stages are scattered across topic files only.
- **`project-types.md` has only 1 entry**: Despite running GREENFIELD, FEATURE, BUG_FIX, SPIKE, and DOCS_ONLY across 13 runs, only GREENFIELD has a lesson. BUG_FIX routing lessons (from b4e1, m7v3, j8f2, w7m3) are not captured here. SPIKE routing lessons (from p8n5) are not captured. DOCS_ONLY lessons (from d8m1) are not captured.

### Memory Staleness

- `design.md`: Last updated 2026-03-29 (6 days ago, only 2 entries). Design has run 4+ times since -- entries should have grown.
- `human-preferences.md`: Last updated 2026-03-29 (10 entries, comprehensive). Current but could benefit from the installed-vs-source lesson being added.
- `defect-patterns.md`: Last updated 2026-04-03 (2 entries). Only captures defects from k3r9. No entries from c8f2 (4 issues logged) or other runs.

---

## 5. Velocity and Efficiency Trends

### Last 4 Runs (10-13): Runs w7m3, p5v8, t2k6, d8m1

| Run | Type | Stages | DoD First-Try | SP | Sessions | Efficiency |
|-----|------|--------|---------------|-----|----------|------------|
| w7m3 | BUG_FIX | 4 | 75% (3/4) | ~2 | 1 | Good (1 correction round in Dev) |
| p5v8 | FEATURE | 7 | 57% (4/7) | 24 | ? | Moderate (Plan, Dev, UAT all needed R2+) |
| t2k6 | FEATURE | 5 | 100% (5/5) | ? | 1 | Excellent (first-try across all stages) |
| d8m1 | DOCS_ONLY | 4 | 100% (4/4) | ? | 1 | Excellent (aggressive skip routing) |

**Patterns in runs 10-13**:

1. **Small-scope runs are highly efficient**: t2k6 (single-file FEATURE) and d8m1 (DOCS_ONLY) both achieved 100% first-try. BUG_FIX routing (w7m3) was near-perfect at 75%.
2. **Large FEATURE runs still struggle**: p5v8 (8 stories, 4 sprints, 24 SP) hit issues at Plan, Dev, and UAT. Three of four correction rounds were in derived artifact handling -- the same class of issue from run c8f2.
3. **Autonomous execution works for BUG_FIX**: j8f2 completed with zero human checkpoints. This validates the routing depth.
4. **Five runs on the same day (2026-04-04)**: w7m3, p5v8, t2k6, d8m1, j8f2 all ran on April 4th. High throughput but raises the question of whether retro quality suffers under volume.

### Velocity Trend

- Runs 1-5: Average ~2 self-correction rounds per run
- Runs 6-9: Average ~1 self-correction round per run
- Runs 10-13: Average ~0.75 self-correction rounds per run (excluding p5v8)

The pipeline is getting faster. Memory injection is the primary driver.

---

## 6. Hook Effectiveness

### Retro Enforcement Hook (Stop event)

**Mechanism**: Prompt-based hook checks if pipeline work occurred and whether post-pipeline protocol completed.

**Assessment**: The hook design is sound -- it checks for stage references, .delivery/ artifacts, and pipeline context. However, it is a prompt-based hook, meaning it relies on LLM judgment to determine if pipeline work occurred. This introduces variance.

**Evidence of effectiveness**: All 13 runs have retro archives. No run is missing a retrospective file. Either the hook is working, or the team is disciplined enough that the hook is never triggered. Either way, the outcome is good.

**Risk**: The 15-second timeout may be tight for complex session analysis. If the prompt times out, the hook silently fails (the Stop hook does not block on timeout).

### Pipeline Bypass Detection Hook (PreToolUse Skill)

**Mechanism**: Prompt-based hook checks if developer/godot/quality skills are invoked outside an active pipeline.

**Assessment**: Partially effective. Checks for `.delivery/config.yml` existence, not for active pipeline state (`state.md` with `status: in_progress`). See Finding 1.3 for the gap.

### Source Code Enforcement Hook (`enforce_pipeline_scope.py`)

**Assessment**: Completely inert. Not registered in hooks.json. See Finding 1.1.

### Agent Prompt Audit Hook

**Assessment**: Working. Checks for code fences (>2) and prompt length (>5000 chars) as proxies for content leakage. Simple but effective guardrails for the two-channel communication model.

### GDScript Validation Hook

**Assessment**: Working but untested in pipeline context. No GAME_DEV runs have occurred in the 13-run history. The hook exists and is registered, but has had zero real-world activations.

### Skill Load Verification Hook

**Assessment**: Registered and running. No evidence of failures in run archives, suggesting skills are loading correctly.

### Empirical Validation Hook (SubagentStop)

**Assessment**: Registered for developer|godot agents. Purpose is to flag when acceptance criteria require runtime validation. Runs k3r9 (empirical items deferred) and r4x2 (5 empirical items) show this is relevant. No archive mentions the hook firing or being useful, which may mean findings come through other channels.

---

## 7. Process Overhead Assessment

### Ceremony That Adds Value

- **Adversarial review**: Consistently catches real issues (BRE coupling in k4m9, builder.conn in r4x2, sprint overloading in r4x2). Keep.
- **Multi-perspective DoD**: The team DoD model catches issues single reviewers miss. PO catches dogfooding gaps, Architect catches stale artifacts, QA catches traceability gaps, SM catches capacity issues. Keep.
- **Memory injection**: Measurably improves first-try pass rates. Keep and expand.
- **Stage routing by project type**: BUG_FIX 4-stage routing, SPIKE 3-stage routing, DOCS_ONLY 4-stage routing are all well-calibrated. Skip and light stages save real time.

### Ceremony That May Be Overhead

- **Full Design stage for small FEATURE runs**: t2k6 skipped Design and Architect for a single-file change. The routing correctly allowed this, but the decision was manual. Consider encoding single-module FEATURE skip rules.
- **Tech Writer validator for plugin repos**: False negatives documented in j8f2 and m7v3. The validator greps wrong file scope (source vs installed). Two runs spent correction rounds on this. The validator needs scoping guidance specific to this repo.
- **Config version checking at session start**: Every session reads config, checks version, checks staleness. For a single-developer project with `wizard_completed: 2026-03-29`, this is low-value ceremony after the first few runs.

---

## 8. Recommendations (Prioritized)

### P0 -- Fix Before Next Run

1. **Register `enforce_pipeline_scope.py` in `hooks.json`** or delete the dead code. A guardrail that exists but does not fire is worse than no guardrail -- it creates false confidence.
2. **Create `topics/team-decisions.md`** with consolidated decisions from all 13 runs. The index promises this file; it must exist.

### P1 -- Fix Within Next 3 Runs

3. **Fix pipeline bypass detection** to check `state.md` status, not just config existence.
4. **Automate installed-vs-source diff** as a pre-DoD hook or script. Three occurrences of the same manual error is enough.
5. **Populate `project-types.md`** with lessons for BUG_FIX, SPIKE, and DOCS_ONLY routing. Five project types have been exercised; only one has a lesson entry.
6. **Create stage chunk files** for Idea, Refine, and Architect. Lessons for these stages are scattered across topic files with no stage-specific home.

### P2 -- Improve Within Next Sprint

7. **Set `project_type: auto`** in config.yml or document that it is advisory-only.
8. **Add session count tracking** to all run archives (only 3 of 13 currently track it).
9. **Consider FEATURE sub-type routing** for refactoring (from r4x2 L-5, still unaddressed).
10. **Update `design.md`** -- it has not grown since 2026-03-29 despite Design running in p5v8.

---

## 9. What the Fellowship is Doing Well

I do not know what strength is in my backlog, but I swear to you -- this team has earned recognition:

1. **Self-improvement culture**: The team files its own bugs (#50-53 from c8f2, #54 from m7v3, #55 from w7m3, #58 from j8f2, #59 from w7m3). Issues logged during runs are worked in subsequent runs. This is rare and valuable.
2. **Memory system ROI**: Gate-patterns injection took Design from ~50% to 100% first-try pass rate. Plan improved from 57% to 80%. The learning loop works.
3. **Project type routing is well-calibrated**: BUG_FIX, SPIKE, and DOCS_ONLY routing are all efficient. No run has complained about missing a skipped stage.
4. **Retro discipline**: 13/13 runs have retrospective archives. No gaps.
5. **Defect density is low**: 2 defects across 13 runs (both in k3r9, both fixed in-pipeline). The pipeline catches issues before they ship.
6. **Dogfooding enforcement works**: After c8f2 established it as a P0 gate, no subsequent run has shipped without dogfooding.

---

*"The road goes ever on -- but we sharpen our swords as we walk."*

**Next review**: After run 20 or when 3+ P1 items are resolved, whichever comes first.
