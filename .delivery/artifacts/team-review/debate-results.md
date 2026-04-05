# Team Review Debate Results

**Date**: 2026-04-04
**Facilitator**: Debate Agent
**Participants**: Gandalf (PO), Celebrimbor (Architect), Legolas (QA), Gimli (Developer), Bilbo (Tech Writer), Aragorn (SM)
**Input**: ~96 combined findings from 6 individual reviews

---

## Debate Proceedings

### Round 1: Consolidation

The team identified significant overlap across reviews. The following clusters were merged:

1. **Dead hook enforce_pipeline_scope.py** -- cited by Celebrimbor, Legolas, Gimli, Aragorn (4 reviewers). Single issue.
2. **Artifact path divergence** (flat vs namespaced) -- cited by Celebrimbor, Legolas, Gimli (3 reviewers). Single issue.
3. **Config version mismatch** (config.yml says 2.3, schema says 2.6) -- cited by Gandalf, Bilbo (2 reviewers). Single issue.
4. **DoD validator prompt template issues** -- cited by Celebrimbor, Legolas (2 reviewers). Single issue.
5. **Docs site missing config keys** -- cited by Gimli, Bilbo (2 reviewers). Single issue.

### Round 2: Challenges and Pushback

**enforce_pipeline_scope.py is dead code -- CONFIRMED.**
The script exists at `delivery-team/hooks/enforce_pipeline_scope.py` but hooks.json has no entry that invokes it. The PreToolUse Skill matcher uses an inline prompt instead. The file is truly orphaned. Aragorn's additional point that the inline prompt checks the wrong thing (config.yml existence rather than active pipeline state) is a separate but related issue -- the prompt-based hook partially covers the intent but with weaker logic.

**Config version mismatch -- CONFIRMED.**
config.yml line 1: `config_version: "2.3"`. config-schema.md line 15: default is `"2.6"`. The migration protocol in config-schema.md says the pipeline should auto-detect and upgrade, but this has not happened. The check_config.py SessionStart hook either is not triggering migration or migration is not implemented.

**Retro location inconsistency -- CONFIRMED but LOW IMPACT.**
Retros exist in both `artifacts/retro/` (subdirectory) and `artifacts/retro-*.md` (flat). This is messy but does not break functionality. The team agreed this is cleanup work, not blocking.

**"Scrum Bag" terminology -- CHALLENGED by Gandalf.**
"Scrum Bag" is intentional -- it is a tongue-in-cheek alias used by the delivery team's alias system (the LOTR theme maps SM to humorous names). This is BY DESIGN, not a terminology conflict. Bilbo's finding is invalid.

**Missing memory file topics/team-decisions.md -- CONFIRMED.**
The memory index references `topics/team-decisions.md` but the file does not exist. The topics directory has 4 files (defect-patterns, gate-patterns, human-preferences, project-types) but not team-decisions.

**project-types.md has 1 entry despite 5 types -- CONFIRMED but EXPECTED.**
Only 1 pipeline run (GREENFIELD) has completed end-to-end. The memory system is append-only -- entries appear as pipelines run. This is not a defect. Aragorn's finding is invalid for the current state.

**5 of 13 runs missing retro -- NEEDS INVESTIGATION.**
Gandalf cited this but the Stop hook should enforce it. Possible explanations: (a) early runs predated the hook, (b) sessions crashed/were killed, (c) the prompt-based hook approved incorrectly. This is a real enforcement gap but the root cause is uncertain.

**Persona name collision -- CHALLENGED by Legolas.**
Bilbo flagged this as critical, but QA found no functional impact -- persona names are scoped to their invocation context and never collide at runtime. Downgraded.

**SKILL.md duplicates pipeline-stages.md with drift -- CONFIRMED.**
Celebrimbor identified ~400 lines of accumulated drift. This is a maintenance burden and source of contradictions. The team agreed SKILL.md should be the authority and pipeline-stages.md should be the detailed reference, with no duplication.

**audit_agent_prompt.py ignores config key -- CONFIRMED but LOW IMPACT.**
The script runs but does not read `pipeline.isolation_audit` from config. It always warns. This means the config key is cosmetic. Low impact since warn-mode is the safe default.

### Round 3: Priority Assignment (Gandalf deciding)

Gandalf's rationale: "Fix the things that make the system lie to us first. Dead enforcement code and version mismatches mean we think we have safety nets that don't exist. Then fix the documentation drift that causes team confusion. Cosmetic issues go to backlog."

---

## Final Prioritized Issue List

### Fix Now (P0)

| # | Issue | Severity | Cited By | Resolution |
|---|-------|----------|----------|------------|
| 1 | **Dead hook: enforce_pipeline_scope.py not in hooks.json** -- Script exists but is never invoked; the inline prompt-based hook partially covers intent but checks config existence, not active pipeline state | P0 | Celebrimbor, Legolas, Gimli, Aragorn | Either wire the script into hooks.json as a command hook (replacing the inline prompt) or delete the dead script and strengthen the inline prompt to check for active pipeline state |
| 2 | **Config version mismatch: config.yml says 2.3, schema is 2.6** -- Migration protocol exists in config-schema.md but is not executing; check_config.py SessionStart hook does not trigger auto-upgrade | P0 | Gandalf, Bilbo | Fix check_config.py to detect version drift and apply migration defaults, then upgrade config.yml to 2.6 |
| 3 | **Artifact path divergence: SKILL.md uses flat paths, pipeline-stages.md uses namespaced** -- Team members get contradictory instructions on where to write artifacts | P0 | Celebrimbor, Legolas, Gimli | Standardize on namespaced paths (artifacts/{stage}/); update SKILL.md to match pipeline-stages.md |

### Fix Next Sprint (P1)

| # | Issue | Severity | Cited By | Resolution |
|---|-------|----------|----------|------------|
| 4 | **SKILL.md duplicates pipeline-stages.md with ~400 lines of accumulated drift** -- Two sources of truth for pipeline behavior cause contradictions | P1 | Celebrimbor | Refactor SKILL.md to reference pipeline-stages.md for stage details; remove duplicated content |
| 5 | **DoD validator prompt template violates two-channel isolation rule** -- One of three templates leaks cross-context information | P1 | Celebrimbor, Legolas | Audit all three DoD prompt templates; fix the violating one to use proper context isolation |
| 6 | **Missing memory file: topics/team-decisions.md referenced in index but does not exist** -- Memory retrieval for Architect/Plan stages will fail silently | P1 | Aragorn | Create the file with initial structure, or remove the index entry if the topic is not yet needed |
| 7 | **Docs site missing 12-13 config keys (presentation, personas, aliases sections)** -- Users configuring these features have no reference documentation | P1 | Gimli, Bilbo | Add missing config keys to docs site config reference |
| 8 | **Retro enforcement gap: 5 of 13 runs have no retrospective artifact** -- Stop hook either predates some runs or is not reliably blocking | P1 | Gandalf | Investigate which runs are missing retros and why; if pre-hook runs, document as known; if post-hook, fix the prompt logic |
| 9 | **Retro action item backlog: 10+ open TODOs with ~20% closure rate** -- Action items accumulate without follow-through, undermining the retro process | P1 | Gandalf | Triage the backlog: close stale items, merge duplicates, schedule remaining items into sprints |

### Backlog (P2)

| # | Issue | Severity | Cited By | Resolution |
|---|-------|----------|----------|------------|
| 10 | **Retro file location inconsistency (artifacts/retro/ vs artifacts/retro-*.md)** -- Both flat files and subdirectory exist with retro artifacts | P2 | Gandalf | Consolidate all retros into artifacts/retro/ subdirectory; update templates |
| 11 | **audit_agent_prompt.py ignores pipeline.isolation_audit config key** -- Always warns regardless of config setting | P2 | Legolas | Read config key and respect warn/block/off modes |
| 12 | **generate_pptx.py: sys.exit() in library function + dead accent_color param** -- sys.exit() prevents clean error handling when called as library; accent_color is accepted but unused | P2 | Gimli | Replace sys.exit() with raised exception; remove or implement accent_color |
| 13 | **config-schema.json type errors: map types rendered as string/enum** -- JSON Schema does not accurately represent the YAML schema for nested map types | P2 | Legolas | Fix type definitions in config-schema.json to use object types where appropriate |
| 14 | **CLAUDE.md says config schema is v2.3** -- Stale reference in project-level documentation | P2 | Bilbo | Update CLAUDE.md to reference current schema version |

### Won't Fix

| # | Issue | Rationale |
|---|-------|-----------|
| W1 | **"Scrum Bag" vs "Scrum Master" terminology conflict** (Bilbo) | By design -- "Scrum Bag" is an intentional humorous alias in the LOTR theme. The product-delivery skill correctly uses "Scrum Bag" as a role name. |
| W2 | **project-types.md has only 1 entry despite 5 types** (Aragorn) | Expected state -- memory is append-only and only 1 type (GREENFIELD) has completed a full pipeline run. Entries will appear organically. |
| W3 | **Persona name collision across 3 files** (Bilbo) | No functional impact -- persona names are scoped to invocation context and never collide at runtime. Cosmetic only. |

---

**Total consolidated issues**: 14 actionable + 3 won't-fix = 17 findings from ~96 raw inputs
**Reduction**: 82% consolidation rate

**Gandalf's closing note**: "The dead hook and version mismatch are the scariest findings -- we thought we had guardrails that were not actually running. Those get fixed before anything else ships."
