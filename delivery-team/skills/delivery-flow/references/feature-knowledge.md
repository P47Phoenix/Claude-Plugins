# Feature Knowledge System

The delivery pipeline's persistent memory for what features exist, how they interact, and what they assume. Prevents the "Feature X breaks Feature Y" scenario by making feature contracts visible and queryable.

## Feature Knowledge Cards (FKCs)

Every delivered feature gets a card in `.delivery/features/<feature-slug>.md`.

### Card Template

```markdown
---
feature: <feature-slug>
display_name: "<Human Readable Name>"
status: active          # active | deprecated | modified
created_sprint: <N>
last_updated: YYYY-MM-DD
last_updated_sprint: <N>
owners: [<who built/maintains this>]
---

# Feature: <Display Name>

## Summary
[2-3 sentences: what this feature does and why it exists]

## Provides (what this feature exposes to others)
- **[Interface/Behavior name]**: [description, data types, contract]
  - Consumers: [list of features that use this]
  - Contract: [what this promises -- data shape, response format, guarantees]

## Consumes (what this feature depends on)
- **[Feature Name].[Interface]**: [what it uses and what it assumes]
  - Assumption: [explicit statement of what must be true]

## Assumptions (things that must remain true for this feature to work)
1. [Assumption]: [what happens if this is violated]
2. [Assumption]: [what happens if this is violated]

## Data Profile
- **Storage**: [tables, collections, file formats used]
- **Data shapes**: [key data types, any heterogeneous/schemaless data]
- **Volume**: [expected records, growth rate]
- **Access pattern**: [read-heavy, write-heavy, mixed]

## Operations
- **Config keys**: [list of config keys this feature uses, with valid ranges]
- **Migrations**: [database migrations required, ordering dependencies]
- **Resource pattern**: [CPU/memory/IO profile under load]
- **Deployment dependencies**: [what must be deployed first]

## Known Fragilities
- **[Interaction]**: [what broke, when, what to watch for]
  - Boundary test: [test that verifies this interaction]

## Decision Log
- [Decision]: [why, link to ADR or Decision Trail if exists]

## Related Features
- [feature-slug]: [nature of relationship]
```

### Card Creation Protocol

**When to create**: After Stage 6 (Development) DoD passes for a NEW feature. The pipeline auto-generates a draft from PRD + architecture + dev notes.

**What's auto-generated**:
- Summary from PRD problem statement
- Provides from architecture component interfaces
- Consumes from architecture dependency declarations
- Data Profile from architect data-design artifacts
- Operations from DevOps deployment plan

**What the developer fills in** (15 min max):
- Assumptions (the invisible contracts)
- Known Fragilities (what they discovered during implementation)
- Decision Log (sub-ADR choices they made)

**When to update**: Pipeline prompts "Has this feature's knowledge card been updated?" as part of Development DoD when modifying an EXISTING feature.

### Card Storage
- `.delivery/features/` directory -- one file per feature
- Cards are committed to the repo (shared with team)
- Naming: `<feature-slug>.md` (kebab-case)

---

## Impact Analysis Gate

Runs automatically at the Architect stage (between Design and Development). Queries FKCs to warn about conflicts.

### How It Works

1. **Feature Surface Scan**: Parse the new feature's PRD and architecture for entity references -- data tables, APIs, config keys, modules touched.

2. **FKC Query**: For each surface identified, search existing FKCs:
   - Which features PROVIDE interfaces touching this surface?
   - Which features CONSUME from this surface?
   - What assumptions exist about this surface?

3. **Assumption Conflict Detection**: Compare the new feature's design against existing assumptions:
   - New feature assumes X, existing feature assumes NOT X -- CONFLICT
   - New feature modifies data shape that existing feature assumes is stable -- WARNING
   - New feature adds load to resource that existing feature has a performance budget for -- CHECK

4. **Risk Scoring**:
   - CRITICAL: direct assumption conflict (will break)
   - HIGH: touches surface with known fragility history
   - MEDIUM: touches shared resource with no boundary test
   - LOW: related features exist but no conflict detected

5. **Output**: Impact analysis report added to pipeline artifacts:
   ```markdown
   ## Impact Analysis: [New Feature]

   ### Surfaces Touched
   - [surface]: used by [features]

   ### Conflicts Found
   | Severity | Existing Feature | Conflict | Resolution Required |
   |----------|-----------------|----------|-------------------|

   ### Boundary Tests Required
   - [test]: verifies [interaction] between [features]

   ### Recommendations
   1. [actionable recommendation]
   ```

6. **Gate Behavior**:
   - CRITICAL conflicts: BLOCK -- must resolve before proceeding
   - HIGH/MEDIUM: WARN -- architect must acknowledge and document mitigation
   - LOW: INFO -- noted in artifacts, no action required

### Integration with Pipeline

Stage 4 (Architect) sub-flow, BEFORE the main design work:
1. Run Impact Analysis Gate
2. Present findings to architect
3. If CRITICAL -- resolve before designing
4. If HIGH/MEDIUM -- design with awareness, add boundary tests to QA plan
5. Record impact analysis in `.delivery/artifacts/<run>/impact-analysis.md`

---

## Generated Feature Interaction Map

Derived from FKC declarations -- NOT hand-maintained.

### Generation Protocol
1. Scan all `.delivery/features/*.md` files
2. Extract all `Provides` and `Consumes` declarations
3. Build interaction list:
   ```
   [Provider Feature] --[interface]--> [Consumer Feature]
   ```
4. Write to `.delivery/features/interaction-map.md`
5. Regenerate after every pipeline run that creates/modifies an FKC

### Format
```markdown
# Feature Interaction Map
**Generated**: YYYY-MM-DD (do not edit -- regenerated from FKCs)

## Interactions

| Provider | Interface | Consumer | Risk | Last Verified |
|----------|----------|----------|------|--------------|
| custom-fields | getFieldValue(Any) | reporting-engine | HIGH | Sprint 7 |
| auth | getUserSession() | custom-fields | LOW | Sprint 3 |

## Orphaned Providers (no consumers)
- [feature]: [interface] -- no known consumers

## High-Risk Interactions (known fragilities)
- [provider] --> [consumer]: [fragility description]
```

---

## Decision Trail

Expanded decision recording beyond ADRs. Auto-created by pipeline, human fills in "why."

### Decision Types
- **Architecture Decision (ADR)**: formal, in `.delivery/artifacts/04a-adrs/`
- **Product Decision (PDR)**: scope, priority, trade-off -- why we built X instead of Y
- **Implementation Decision (IDR)**: sub-ADR code choices -- why this data format, why this algorithm
- **Experiment Result (EXR)**: A/B test outcomes, research findings that informed design

### Auto-Creation
At each pipeline stage gate, the pipeline asks: "Were any significant decisions made?" If yes:
- Auto-create a stub in `.delivery/decisions/DEC-NNN-<slug>.md`
- Populate: date, sprint, stage, feature(s) affected
- Developer/architect fills in: decision, rationale, alternatives considered, revisit condition

### Decision File Format
```markdown
---
id: DEC-NNN
type: adr | pdr | idr | exr
date: YYYY-MM-DD
sprint: N
stage: architect
features_affected: [custom-fields, reporting-engine]
status: active       # active | revisit | superseded
revisit_when: "team grows beyond 5 people"
supersedes: DEC-MMM  # if applicable
---

# DEC-NNN: [Short Title]

## Context
[What situation prompted this decision]

## Decision
[What was decided]

## Rationale
[Why -- the key arguments]

## Alternatives Considered
- [Alternative]: [why rejected]

## Consequences
[What becomes easier/harder as a result]
```

### Cross-Referencing
Every decision tags `features_affected`. FKCs include a "Decision Log" section that auto-links to relevant decisions.

---

## Staleness Detection

Prevents documentation rot by flagging FKCs that drift from code changes.

### Detection Rules
1. **Code-change trigger**: After Stage 6 (Development), check if the story modified files in a module that has an FKC. If yes and the FKC's `last_updated` is more than 2 sprints old, flag: "Feature [X]'s knowledge card may be stale -- it hasn't been updated since Sprint [N] but code was modified."

2. **Time-based trigger**: At pipeline start (Phase 0), scan all FKCs. Flag any with `last_updated` > 90 days.

3. **Interaction staleness**: If an FKC's "Consumers" list doesn't include a feature that the interaction map shows as a consumer, flag the discrepancy.

### Enforcement
- Staleness warnings appear at the start of each pipeline run (Phase 0, after memory retrieval)
- Development DoD includes: "If modifying an existing feature, its FKC must be reviewed and updated"
- `stale-features` command lists all FKCs that need attention
