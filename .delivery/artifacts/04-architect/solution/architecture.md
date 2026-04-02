# Architecture Decision: Cross-Skill Shared References

**Spike**: #47 — Cross-skill shared references mechanism for delivery-team
**Architect**: Celebrimbor (Solution Architect)
**Date**: 2026-04-01
**Status**: PROPOSED

---

## 1. Structural Survey — What Exists Today

Before forging anything new, I examined the existing metalwork. Two cross-skill reference patterns already operate in production:

### Pattern A: Godot -> Developer (cross-skill file read)

In `godot/SKILL.md` line 58:
```
Otherwise, read `delivery-team/skills/developer/references/clean-code.md`
(shared with the developer skill -- do NOT copy this file into the Godot skill directory)
```

**How it works**: The SKILL.md instructs Claude to `Read` a file from another skill's directory. The path `delivery-team/skills/developer/references/clean-code.md` is resolved by Claude Code relative to the plugin installation root (`~/.claude/plugins/marketplaces/mec-claude-agent-skills/`). Claude uses the `Read` tool with this path, and the file exists at that location. This works because Claude can read any file on the filesystem — path resolution is not constrained to the skill's own directory.

**Verified**: The file exists at the installed location: `delivery-team/skills/developer/references/clean-code.md` contains the clean code guide.

### Pattern B: Alias Creator -> Delivery Flow (cross-skill directory reference)

In `alias-creator/SKILL.md` line 15:
```
Built-in themes are in `delivery-flow/references/aliases/`.
```

**How it works**: Same mechanism — a relative path from the plugin root referencing another skill's references directory. The 13 `.yml` theme files exist at `delivery-team/skills/delivery-flow/references/aliases/`.

**Key insight**: Both patterns use the same resolution mechanism. Claude resolves paths relative to the plugin installation root. This is not documented as a formal feature — it works because Claude's `Read` tool accepts any accessible filesystem path.

### Reference Loading Patterns Across All Skills

Every skill follows the same architecture: SKILL.md contains path strings like `references/test-strategy.md`. When Claude loads the SKILL.md, it reads these paths using the `Read` tool. The paths are resolved relative to the SKILL.md's parent directory (the skill root). Cross-skill paths use a longer relative path from the plugin root.

**Sub-agent context passing**: Skills spawn sub-agents via the `Agent` tool. The sub-agent prompt contains the **pasted contents** of reference files (not file paths). The parent agent reads the file, then includes the content in the sub-agent prompt string. This means path resolution happens in the parent agent, not the sub-agent.

---

## 2. Sharing Candidates Inventory

From the idea brief and structural analysis:

| File | Owner Skill | Sharing Candidate? | Justification |
|---|---|---|---|
| `developer/references/clean-code.md` | developer | **TRUE DUPLICATE** | Already cross-referenced by godot. Any code-producing skill benefits. |
| `developer/references/clean-code-review-checklist.md` | developer | **PARTIAL OVERLAP** | Useful for quality skill's code review tasks. Currently developer-only. |
| `delivery-flow/references/aliases/*.yml` | delivery-flow | **TRUE SHARED** | Already cross-referenced by alias-creator. Ownership is delivery-flow, consumption is alias-creator. |
| `architect/references/security-patterns.md` | architect | **INTENTIONALLY DISTINCT** | Architect's security patterns focus on architectural decisions. Quality's `security-scanning.md` focuses on scanning techniques. Different audiences, different concerns. |
| `architect/references/quality-attributes.md` | architect | **INTENTIONALLY DISTINCT** | Non-functional requirements from an architecture perspective vs. quality metrics from a QA perspective. |
| `godot/references/defect-prevention.md` | godot | **PARTIAL OVERLAP** | Game-specific defect patterns. Could be useful for developer skill on GAME_DEV projects, but content is Godot-specific, not general. |
| `delivery-flow/references/quality-gates.md` | delivery-flow | **ORCHESTRATOR-OWNED** | Consumed during DoD validation. The delivery-flow orchestrator reads it and passes relevant criteria to sub-agents. Not a sharing problem — it is orchestrator infrastructure. |

**Conclusion**: There are exactly **2 true sharing candidates** today (clean-code.md and alias themes), plus **1 partial overlap** (clean-code-review-checklist.md). The remaining cases are intentionally distinct content serving different roles. This is a small, well-bounded problem.

---

## 3. Evaluation Matrix

| Criterion | 1. `shared/` Directory | 2. Symlinks | 3. Orchestrator Passes Paths | 4. Reference Registry | 5. Status Quo + Convention |
|---|---|---|---|---|---|
| **Feasibility** | HIGH -- mkdir + move files. Claude reads from any path. | MEDIUM -- works on Linux/Mac. Windows requires admin or developer mode. | HIGH -- delivery-flow already passes context to sub-agents. | LOW -- no tooling exists to resolve a registry. Claude cannot auto-resolve declared references. | HIGH -- already working in production (2 cross-references). |
| **Simplicity** | MEDIUM -- new directory, update 2-3 SKILL.md paths, document convention. | LOW -- symlink creation, tracking, potential confusion when Claude reads the link vs target. | MEDIUM -- orchestrator SKILL.md changes, path lists per stage. Only works for orchestrated flows. | LOW -- new JSON schema, resolution logic, no implementation exists. | **HIGH** -- zero changes. Document what exists. |
| **Portability** | HIGH -- directories and file paths work everywhere. | **LOW** -- Windows symlinks require elevated privileges or developer mode. Git symlinks need `core.symlinks=true`. Known fragile. | HIGH -- text paths in prompts. No OS dependency. | HIGH -- JSON is portable. But the resolution tooling would need to be. | HIGH -- no OS-specific features used. |
| **Maintenance** | MEDIUM -- shared files have no clear owner. Who reviews PRs to `shared/`? Shared ownership is diffuse ownership. | LOW -- symlinks break on file moves/renames. Must recreate on every structural change. | MEDIUM -- orchestrator must be updated when shared refs change. Centralized but coupled. | HIGH burden -- registry must stay in sync with actual files. No automated validation. | **LOW burden** -- each SKILL.md owns its own cross-references. Change is local. |
| **Risk** | MEDIUM -- introduces a new directory convention. All skills must know about it. May incentivize over-sharing (files migrate to shared/ prematurely). | **HIGH** -- Windows breakage, git confusion, Claude may resolve symlink targets inconsistently. | MEDIUM -- only works within delivery-flow pipeline. Direct skill invocation (e.g., `/developer`) bypasses orchestrator, loses shared refs. | HIGH -- over-engineering for 2-3 shared files. Registry becomes stale. | LOW -- the current pattern works. Risk is discoverability for new skill authors. |

### Scoring Summary (5 = best)

| Criterion | Weight | shared/ | Symlinks | Orchestrator | Registry | Status Quo |
|---|---|---|---|---|---|---|
| Feasibility | 25% | 5 | 3 | 4 | 2 | 5 |
| Simplicity | 25% | 3 | 2 | 3 | 2 | 5 |
| Portability | 20% | 5 | 1 | 5 | 4 | 5 |
| Maintenance | 15% | 3 | 2 | 3 | 2 | 4 |
| Risk | 15% | 3 | 1 | 3 | 2 | 4 |
| **Weighted Total** | | **3.9** | **1.9** | **3.6** | **2.3** | **4.7** |

---

## 4. Recommendation

**Approach 5: Status Quo + Convention (formalized)**

The evidence is clear. Let us not forge a new ring when the existing craft serves well.

### Rationale

1. **The problem is smaller than it appears.** Of 107+ reference files, exactly 2 are true sharing candidates. This does not justify new infrastructure.

2. **The existing pattern works.** Godot has been cross-referencing developer's clean-code.md since the skill was created. Alias-creator cross-references delivery-flow's alias themes. Both work in production across platforms.

3. **Claude's file resolution is the enabling mechanism.** Claude can `Read` any file path on the filesystem. Cross-skill references are just longer relative paths. No special infrastructure is needed to enable this — it is already a capability of the runtime.

4. **A `shared/` directory creates shared ownership problems.** When `clean-code.md` lives in `developer/references/`, the developer skill owns it. If it moves to `shared/`, who owns it? Shared ownership is diffuse ownership, and diffuse ownership leads to stale content.

5. **The orchestrator approach (3) only works within the pipeline.** When a user directly invokes `/developer` or `/godot` outside of delivery-flow, the orchestrator is not running. Shared references must work regardless of invocation path.

6. **Symlinks (2) are a non-starter.** Windows fragility alone disqualifies this approach for a cross-platform plugin.

7. **A registry (4) is premature abstraction.** Building tooling to resolve 2-3 shared files is engineering for a problem we do not have.

### What "Formalized" Means

The status quo works, but it is undocumented and undiscoverable. Formalization means:

- **Document the convention** in a reference file that all skill authors can find
- **Add a cross-reference section** to each SKILL.md that uses cross-skill references
- **Establish naming/path conventions** so cross-references are predictable
- **Validate in CI** that cross-referenced files actually exist (no phantom references)

---

## 5. ADR — Architecture Decision Record

### ADR-047: Cross-Skill Shared References Convention

**Status**: Proposed
**Date**: 2026-04-01
**Deciders**: Celebrimbor (Architect), delivery team

#### Context

The delivery-team plugin has 11 skills with 107+ reference files. Two cross-skill references exist today:
- `godot/SKILL.md` reads `developer/references/clean-code.md`
- `alias-creator/SKILL.md` reads `delivery-flow/references/aliases/*.yml`

Both use the same mechanism: Claude's `Read` tool resolves paths relative to the plugin installation root. This works but is undocumented — new skill authors must discover the pattern from existing SKILL.md files.

A spike was conducted (#47) evaluating 5 approaches: shared directory, symlinks, orchestrator-passed paths, reference registry, and formalized status quo.

#### Decision

**Formalize the existing cross-skill reference convention without introducing new infrastructure.**

The convention is:
1. Files remain in their owner skill's `references/` directory
2. Cross-skill references use paths relative to the plugin root: `delivery-team/skills/<skill>/references/<file>.md`
3. Each SKILL.md that uses cross-skill references declares them in a `## Cross-Skill References` section
4. A developer guide documents how to add cross-skill references
5. CI validation ensures cross-referenced paths resolve to existing files

#### Consequences

**Positive**:
- Zero migration effort — no files move, no paths change
- Clear ownership — the file lives where it is maintained
- Works on all platforms — no symlinks, no OS-specific features
- Works in all invocation contexts — direct skill invocation, pipeline orchestration, sub-agent spawning
- Low maintenance — no registry to keep in sync, no tooling to maintain

**Negative**:
- Cross-skill references are string paths in SKILL.md files, not enforced by tooling (mitigated by CI validation)
- Discoverability depends on documentation (mitigated by the developer guide and SKILL.md sections)
- If sharing needs grow beyond 5-10 files, this convention may need revisiting (trigger: more than 3 skills referencing the same file)

**Neutral**:
- Does not prevent a future `shared/` directory if the problem grows — this decision is additive-compatible

#### Supersedes

None (first decision on this topic).

#### Review Trigger

Revisit this decision when any of:
- More than 5 files are cross-referenced between skills
- More than 3 skills reference the same single file
- A new skill author reports difficulty discovering cross-reference patterns

---

## 6. Prototype Design

The prototype should prove two things:
1. The convention is discoverable (a new skill author can find and follow it)
2. Cross-references can be validated (phantom references are caught)

### 6.1 Developer Guide: `delivery-team/CROSS-SKILL-REFERENCES.md`

Create a guide at the plugin root that documents:

```markdown
# Cross-Skill Reference Convention

## How It Works

Skills can reference files from other skills using paths relative to the
plugin root. Claude resolves these paths using the Read tool.

## Path Format

  delivery-team/skills/<owner-skill>/references/<file>.md

Example: The godot skill references the developer skill's clean code guide:

  delivery-team/skills/developer/references/clean-code.md

## Rules

1. The file stays in the owner skill's references/ directory
2. The owner skill maintains the file -- consumers do not modify it
3. Every SKILL.md that cross-references another skill's file MUST
   declare it in a "Cross-Skill References" section (see format below)
4. Before adding a cross-reference, verify the file exists at the path

## SKILL.md Declaration Format

Add this section to any SKILL.md that uses cross-skill references:

  ## Cross-Skill References

  | File | Owner Skill | Purpose |
  |------|-------------|---------|
  | `delivery-team/skills/developer/references/clean-code.md` | developer | Clean code standards (loaded on every task) |

## Current Cross-References

| Consumer Skill | Referenced File | Owner Skill |
|----------------|----------------|-------------|
| godot | developer/references/clean-code.md | developer |
| alias-creator | delivery-flow/references/aliases/*.yml | delivery-flow |

## When NOT to Cross-Reference

- If the content serves a different audience (architect's security-patterns.md
  vs quality's security-scanning.md) -- these are intentionally distinct
- If you need a modified version -- copy and adapt, then document why
  it diverged from the original
```

### 6.2 SKILL.md Updates (2 skills)

**godot/SKILL.md** -- Add a `## Cross-Skill References` section:

```markdown
## Cross-Skill References

| File | Owner Skill | Purpose |
|------|-------------|---------|
| `delivery-team/skills/developer/references/clean-code.md` | developer | Foundational clean code standards. Loaded on every godot task unless overridden by `tech_stack.clean_code_guide` in `.delivery/config.yml`. |
```

**alias-creator/SKILL.md** -- Add a `## Cross-Skill References` section:

```markdown
## Cross-Skill References

| File | Owner Skill | Purpose |
|------|-------------|---------|
| `delivery-team/skills/delivery-flow/references/aliases/*.yml` | delivery-flow | Built-in alias theme definitions. 13 themes (lotr, star-wars, marvel, etc.). Read-only from alias-creator's perspective. |
```

### 6.3 Validation Script: `delivery-team/scripts/validate_cross_refs.py`

A simple Python script that:
1. Scans all `SKILL.md` files for the `## Cross-Skill References` table
2. Extracts file paths from the table
3. Verifies each path resolves to an existing file (relative to repo root)
4. Reports phantom references as errors

```python
# Pseudocode -- Developer implements
# Input: delivery-team/skills/*/SKILL.md
# Parse: extract paths from Cross-Skill References tables
# Validate: os.path.exists(path) for each
# Output: PASS/FAIL with list of phantom references
```

This script can be integrated into CI or run manually during plugin-dev validation.

### 6.4 Prototype Test Plan

Test with the two existing cross-references to prove the convention works:

#### Test 1: Godot -> Developer clean-code.md

1. Load the godot skill (`/godot`)
2. Ask it to write a simple GDScript function
3. Verify the sub-agent prompt includes clean code standards content
4. Verify the clean code content came from `developer/references/clean-code.md` (not a copy)

#### Test 2: Alias Creator -> Delivery Flow aliases

1. Load the alias-creator skill
2. Ask it to list available themes
3. Verify it reads from `delivery-flow/references/aliases/`
4. Verify all 13 theme files are discovered

#### Test 3: Phantom Reference Detection

1. Add a fake cross-reference to a test SKILL.md: `delivery-team/skills/fake/references/nonexistent.md`
2. Run `validate_cross_refs.py`
3. Verify it reports the phantom reference as an error
4. Remove the fake reference

#### Test 4: Cross-Platform Path Resolution

1. Verify the paths use forward slashes (POSIX-compatible)
2. Confirm Claude's Read tool resolves forward-slash paths on all platforms (it does -- Claude normalizes paths internally)
3. No symlinks, no OS-specific features -- purely text-based path references

---

## 7. Follow-Up Recommendations

If this spike's recommendation is accepted:

1. **Feature work**: Create `CROSS-SKILL-REFERENCES.md`, update 2 SKILL.md files, write validation script. Estimated: 1-2 story points.

2. **Future consideration**: If a third skill needs `clean-code.md`, that is fine under this convention -- just add the cross-reference declaration. If a fourth and fifth follow, re-evaluate whether a `shared/` directory is warranted (per the review trigger in the ADR).

3. **Do not pre-build**: The `shared/` directory, reference registry, and orchestrator approaches are all viable future options. They should be built when the problem demands them, not before. Let us forge something that will endure beyond the ages -- and the most enduring designs are the simplest ones that serve the actual need.

---

*"I could build you a Silmaril of shared reference architecture -- a registry of registries, a web of symbolic links, a cathedral of indirection. But the wise smith knows that the finest work is the one that needs no ornament. Two cross-references do not require a framework. They require a map."*

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/04-architect/solution/architecture.md
SUMMARY: Recommends formalized status quo (Approach 5). 2 of 107+ refs are true sharing candidates. Existing cross-skill Read pattern works. ADR + prototype design included.
```
