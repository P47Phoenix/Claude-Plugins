# Challenger Review: ADR-047 Cross-Skill Shared References

**Reviewer**: Challenger (Adversarial Reviewer)
**Architecture Under Review**: Approach 5 -- Formalized Status Quo
**Date**: 2026-04-01
**Confidence in Decision**: 4 / 5

---

## Verdict

**The decision is sound but not bulletproof.** The Architect correctly identified that this is a small problem today and chose the proportionate response. However, there are gaps in the analysis that, while not fatal, should be acknowledged and tracked. The decision STANDS with caveats documented below.

---

## Challenge 1: Is the Problem Assessment Correct?

**Architect's claim**: Only 2 of 107+ refs are true sharing candidates.

**Challenge**: The number is 126 markdown reference files (not 107+), plus 13 YAML alias themes. The Architect audited 7 files in the inventory table. That is 5% of the reference corpus. The remaining 132 files were implicitly classified as "not sharing candidates" without individual assessment.

**Specific files the Architect did not evaluate that have plausible cross-skill utility**:

| File | Owner | Potential Consumer | Rationale |
|------|-------|--------------------|-----------|
| `quality/references/test-automation.md` | quality | developer | Developer writes tests. Test automation patterns could inform test task sub-agents. |
| `operations/references/ci-cd-patterns.md` | operations | developer | Developers configure CI. Overlap is likely. |
| `architect/references/c4-model.md` | architect | presentation | Stakeholder Update and Technical Deep-Dive presentations reference architecture diagrams. |
| `ui/references/accessibility.md` | ui | developer (frontend) | Frontend developers implementing accessible components need these standards. |
| `quality/references/empirical-validation.md` | quality | developer, godot | The empirical validation hook already bridges quality and developer concerns. |
| `operations/references/documentation-standards.md` | operations | presentation | Presentations are documentation artifacts. Consistent standards matter. |

**Verdict**: The Architect's count of 2 true sharing candidates is defensible *today* but represents a point-in-time snapshot, not an architectural truth. The analysis should have been more explicit: "We examined N files and found 2 true candidates. The remaining files were not individually audited but are assumed to be skill-specific based on directory ownership." The absence of a systematic audit is a minor gap, not a fatal flaw.

**Impact on decision**: LOW. Even if the true number is 5-8 sharing candidates rather than 2, the formalized convention still handles that scale. The ADR's review trigger (more than 5 cross-referenced files) is the right safety net.

---

## Challenge 2: Does the Evaluation Matrix Have Blind Spots?

**Missing criterion: Discoverability.** The matrix evaluates feasibility, simplicity, portability, maintenance, and risk. It does not evaluate discoverability -- how easily a new skill author finds and uses shared references. The Architect acknowledges discoverability as a weakness in the ADR consequences ("Discoverability depends on documentation") but does not score it in the matrix. If discoverability were weighted at 15% (taking 5% each from feasibility, simplicity, and portability), the shared/ directory approach would score higher because a directory *is* discoverable -- a convention documented in a markdown file *is not* self-evident.

**Scoring concern: Maintenance for Status Quo.** The Architect scores Status Quo maintenance at 4/5, claiming "each SKILL.md owns its own cross-references. Change is local." But when the referenced file moves or is renamed, every consuming SKILL.md must be updated manually. This is the *opposite* of local -- it is distributed coupling through hardcoded string paths. A fair score would be 3/5, matching the shared/ directory approach.

**Recalculated with corrections**: If we add Discoverability (15%, reducing feasibility/simplicity/portability by 5% each) and adjust maintenance to 3:

| Criterion | Weight | shared/ | Status Quo |
|-----------|--------|---------|------------|
| Feasibility | 20% | 5 | 5 |
| Simplicity | 20% | 3 | 5 |
| Portability | 15% | 5 | 5 |
| Maintenance | 15% | 3 | 3 |
| Risk | 15% | 3 | 4 |
| Discoverability | 15% | 4 | 2 |
| **Weighted Total** | | **3.75** | **4.10** |

**Verdict**: Status Quo still wins, but the margin narrows from 0.8 points to 0.35 points. The decision survives the stress test, but the Architect should not present a 0.8-point gap as decisive when a reasonable reweighting halves it.

**Impact on decision**: LOW. The ranking does not change. But the team should be honest about how close the alternatives actually are.

---

## Challenge 3: Is "Do Nothing + Document" a Cop-Out?

This is the hardest question. When is "formalize the status quo" wisdom versus avoidance?

**It is wisdom when:**
- The problem is genuinely small (2-3 instances) -- TRUE here
- The existing mechanism works in production -- TRUE here
- The alternatives introduce new failure modes -- TRUE (symlinks break on Windows, registry needs tooling)
- The cost of being wrong is low (easy to migrate later) -- TRUE (the ADR explicitly notes additive-compatibility)

**It would be a cop-out if:**
- The problem is growing and the Architect is ignoring the trend -- PARTIALLY TRUE. The plugin grew from 0 to 11 skills. The idea brief itself notes "maintenance cost scales with skill count." The Architect's analysis is static, not trend-aware.
- The "formalization" is just documentation with no enforcement -- PARTIALLY TRUE. The CI validation script is described in pseudocode but not implemented. If it never gets built, the "formalization" is just a markdown file that nobody reads.

**Verdict**: NOT a cop-out, but the Architect must commit to actually building the CI validation script. Without it, the "formalized" status quo is just the status quo with a new markdown file. The CI script is what makes this a real architecture decision rather than a documentation exercise.

**Recommendation**: The CI validation script (`validate_cross_refs.py`) should be a hard prerequisite for closing this spike, not a "follow-up recommendation." If it ships without the script, the formalization is incomplete.

---

## Challenge 4: Scalability

**Current state**: 11 skills, 139 reference files (126 md + 13 yml), 2 cross-references.

**What happens at 20 skills?** If the sharing ratio stays constant (~2 per 11 skills), we would expect ~4 cross-references at 20 skills. The convention handles this fine.

**What happens if the sharing ratio accelerates?** New skills are more likely to be consumers than producers. A "code-review" skill would want `clean-code.md` and `clean-code-review-checklist.md`. A "security" skill would want `security-patterns.md` from architect AND `security-scanning.md` from quality. A "docs" skill would want `documentation-standards.md` from operations. Each new composite skill could add 2-4 cross-references.

**Worst case**: 20 skills, 10 cross-referenced files, 25 total cross-reference declarations across SKILL.md files. At this scale, the convention becomes noisy (every SKILL.md has a cross-reference table) but still functional. The ADR review trigger (5 files or 3 skills referencing the same file) would fire well before this point.

**Verdict**: The scalability concern is real but mitigated by the review triggers. The Architect did the right thing by defining when to revisit. The key is that someone actually monitors these triggers -- they are not self-executing.

---

## Challenge 5: Hardcoded Path Fragility

The existing pattern uses string literals in SKILL.md files:
```
delivery-team/skills/developer/references/clean-code.md
```

**What breaks when skills are reorganized?**
- If `developer/` is renamed to `dev/`, every SKILL.md referencing developer paths breaks silently. Claude would attempt to `Read` a nonexistent file, get an error, and either skip the reference or hallucinate the content.
- If the plugin directory structure changes (e.g., skills move from `delivery-team/skills/` to `delivery-team/modules/`), all cross-references break.

**How bad is this?** In practice, skill directories have never been renamed in the history of this plugin. The risk is theoretical. But "it has never happened" is not the same as "it cannot happen." The CI validation script would catch this -- another reason it must actually be built.

**Verdict**: Fragility is real but manageable. The convention creates a contract: "these paths are stable identifiers." The team must understand that renaming a skill directory is now a breaking change that requires updating all consumers. This should be documented in the cross-skill reference guide.

---

## Challenge 6: Alternative Not Considered -- Plugin Architecture Extension

**Could Claude Code's plugin architecture support shared references natively?**

The current plugin system resolves resources relative to the skill root (`${CLAUDE_PLUGIN_ROOT}`). There is no mechanism for declaring cross-skill dependencies or shared resource pools in `plugin.json` or `marketplace.json`.

A native solution might look like:
```json
{
  "shared_resources": {
    "clean-code": "skills/developer/references/clean-code.md"
  }
}
```

Where skills could reference `${SHARED:clean-code}` in their SKILL.md files.

**Should the Architect have proposed this?** No. This would require changes to Claude Code's plugin runtime, which this team does not control. The spike constraint explicitly states "no new dependencies" and "Claude must be able to Read the file directly from a path." Proposing changes to the plugin platform is outside the spike's scope.

**However**: The Architect should have noted this as a *long-term* possibility. If the plugin platform ever supports shared resources natively, that would supersede this ADR. The ADR should acknowledge this future direction even if it cannot act on it today.

**Impact on decision**: NONE for this spike. Worth noting in the ADR's "Review Trigger" section.

---

## Summary of Findings

| Challenge | Severity | Impact on Decision |
|-----------|----------|-------------------|
| Problem assessment covers only 5% of files | Minor | None -- review triggers cover the gap |
| Missing discoverability criterion in matrix | Minor | Narrows the gap but does not change the ranking |
| CI validation script is pseudocode, not committed | **Moderate** | Must be a deliverable, not a follow-up |
| Hardcoded paths are a rename risk | Minor | Document as breaking change contract |
| Scalability at 20+ skills | Minor | Review triggers are adequate |
| Platform-native shared resources not considered | Informational | Note as future direction |

---

## Conditions for Acceptance

The Challenger accepts this architecture decision (Confidence: 4/5) with these conditions:

1. **CI validation script is a sprint deliverable**, not a follow-up. Without it, the "formalization" is just documentation.
2. **The cross-skill reference guide must explicitly state** that renaming a skill directory is a breaking change requiring consumer updates.
3. **The ADR review triggers should add**: "Claude Code plugin platform adds native shared resource support."
4. **Acknowledge the discoverability gap** -- a convention in a markdown file is less discoverable than a directory. Accept the tradeoff explicitly.

If these conditions are met, the decision is APPROVED. No escalation to the human is required.

---

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/04-architect/dod/challenger-review.md
CONFIDENCE: 4/5
DECISION: APPROVED WITH CONDITIONS
ESCALATION: NOT REQUIRED
```
