## Idea Brief

**Project Type**: BUG_FIX
**Date**: 2026-04-01
**Source Issues**: #54, IA-1 (retro r4x2), IA-4 (retro r4x2)
**Bundle Rationale**: All three items address pipeline integrity gaps in delivery-flow -- the orchestrator's ability to enforce its own rules. Fixing them together ensures the pipeline that governs our work is itself governed correctly.

---

### Problem Statement

The delivery-flow pipeline has three integrity gaps where documented rules exist but are not enforced or are incomplete. These were surfaced by Issue #54 (filed against run `run-2026-03-26-f7a2`) and retrospective improvement actions from `run-2026-03-30-r4x2`.

**Evidence**:
- **Run f7a2**: Config specifies `git.branch_strategy: feature-branch` and `git.auto_branch: true`, yet all commits landed directly on `master`. No feature branch was created at Plan, no branch isolation existed during Dev, and no PR was created at UAT. The orchestrator's git-integration reference documents the expected behavior but the stage instructions do not enforce it.
- **Run r4x2**: UAT review board gave 5/5 confidence on structural-only evidence (bash was unavailable for empirical validation). The quality gates reference has no rule capping confidence when empirical validation is impossible. This overstates certainty and undermines trust in the gate.
- **Run r4x2**: A 1,157-line god object was decomposed into 4 new modules without any architect review. FEATURE routing applied Architect-skip because the change was "contained within a single service" -- but the refactoring fundamentally changed module boundaries, which is precisely the kind of structural decision an architect should weigh in on.

The common thread: the pipeline's rules are documented but lack enforcement teeth, or the rules themselves have blind spots.

---

### Bundled Work Items

| # | Item | Priority | Scope | Fix Location |
|---|------|----------|-------|-------------|
| 1 | **#54 -- Branch strategy not enforced** | P1 | Add enforcement directives at Plan (Step 8.5: create feature branch), Dev (Step 4: commit to feature branch), and UAT (Step 8: create PR). Cross-reference `git-integration.md` from stage instructions. | `delivery-flow/SKILL.md` (stage steps), `references/git-integration.md` (clarify enforcement vs. documentation) |
| 2 | **IA-1 -- Structural-only validation caps confidence** | P2 | Add a rule to Gate 7 (UAT quality gate): when empirical validation cannot be performed, review board confidence is capped at 4/5 maximum, and the DoD must document the limitation explicitly. | `references/quality-gates.md` (Gate 7 criteria) |
| 3 | **IA-4 -- Refactoring sub-type for FEATURE routing** | P2 | Add "refactoring" as a recognized FEATURE sub-type. When a FEATURE involves module decomposition, boundary changes, or architectural restructuring, route to Architect-light instead of Architect-skip. Update detection rules and Light-or-Skip decision logic. | `references/project-types.md` (FEATURE detection, Light-or-Skip logic), possibly `SKILL.md` (stage routing matrix reference) |

---

### Target Users

- **Pipeline users** (all delivery team consumers): Benefit from branch isolation that prevents incomplete work from landing on master, and from confidence scores that accurately reflect evidence quality.
- **Architects**: Gain appropriate involvement in refactoring decisions that reshape module boundaries -- exactly the structural decisions they exist to govern.
- **Product Owners / QA**: Can trust that gate scores reflect actual validation depth. A 5/5 means empirically verified, not "we looked at it and it seemed fine."

---

### Goals

1. **Branch enforcement**: When `git.branch_strategy: feature-branch` and `git.auto_branch: true` are configured, the pipeline creates a feature branch at Plan, commits to it during Dev, and creates a PR at UAT. No silent fallthrough to master.
2. **Honest confidence scoring**: Review board confidence is capped at 4/5 when empirical validation (bash execution, runtime tests) cannot be performed. The limitation is documented in the DoD artifact.
3. **Architect involvement in refactoring**: FEATURE projects involving module decomposition or boundary changes route through Architect-light, ensuring structural decisions get lightweight architect review rather than none at all.
4. **Dogfooding validation**: The fixes must be validated by running a pipeline session that exercises each fix -- this is a UAT gate, not a follow-up.

---

### Constraints

- **Markdown/YAML only**: All changes are to instruction files (`SKILL.md`, reference `.md` files). No source code, no scripts, no hooks.
- **No new files**: Modifications to existing reference documents and SKILL.md only.
- **Backward compatible**: Existing project type detection and routing for non-refactoring FEATURE projects must not change behavior.
- **Config schema unchanged**: No new config keys required. The `git.branch_strategy` and `git.auto_branch` keys already exist in config v2.3 -- the gap is enforcement, not configuration.
- **Dogfooding is a P0 UAT gate**: Per memory lesson, the pipeline must exercise these fixes before DoD submission. Structural review alone is insufficient (which is, fittingly, exactly what IA-1 addresses).

---

### Out of Scope

- Changes to hooks, Python scripts, or plugin structure
- New config schema keys or version bump
- Retrospective process changes (the retro worked correctly -- it surfaced these issues)
- Git integration features beyond enforcement of existing config (e.g., no new branch strategies)

---

*A product owner is never late, nor early. They prioritize precisely when they mean to. These three items have ripened together -- the pipeline that governs our craft must itself be governed with equal rigor.*

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/01-idea/po/idea-brief.md
SUMMARY: BUG_FIX idea brief bundling #54 (branch enforcement), IA-1 (confidence cap), IA-4 (refactoring sub-type) — 3 pipeline integrity fixes
```
