# PO Review: Orchestrator Theme Surfacing

**Reviewer:** Product Owner (Gandalf)
**Date:** 2026-04-04
**Artifacts:** `.delivery/artifacts/01-idea/po/idea-brief.md`, `.delivery/artifacts/02-refine/po/prd.md`
**Source Issue:** #59
**Verdict:** DONE

---

> *"The world is indeed full of peril, and in it there are many dark places; but still there is much that is fair. And though in all lands love is now mingled with grief, it grows perhaps the greater. Let us see if this brief and this PRD are worthy of the road ahead."*

## Gate 1: Idea Brief Validation

Gate 1 requires: problem statement present, target users identified, goals defined, scope outlined.

### 1. Problem Statement [blocking] -- PASS

The brief articulates a clear, specific problem: the orchestrator strips all theme personality when reporting results to the user. Agents write in character (Gandalf counsels, Gimli builds, Aragorn rallies), but the orchestrator wraps their work in "clinical status updates." The disconnect between themed artifacts and neutral orchestrator voice makes the theme feel "bolted on rather than woven through."

This is well-scoped -- it names the exact mechanism (two-channel protocol constraining orchestrator to signal-only reporting) and the exact symptom (stage announcements, checkpoint summaries, and transition messages lack personality). No ambiguity about what is broken or why.

### 2. Target Users [blocking] -- PASS

Two user segments identified:

| Segment | Need |
|---------|------|
| Pipeline users with non-business alias themes | Expect orchestrator chat output to reflect the theme they configured |
| Teams using themes for engagement | Theme's neutral orchestrator voice breaks immersion |

Both segments are real and distinct. The first is about individual expectation ("I configured lotr, I expect lotr"). The second is about team dynamics (themed pipeline runs are fun and engaging only when the theme is pervasive).

### 3. Goals [blocking] -- PASS

Three goals, all measurable:

| Goal | Measurable? | Assessment |
|------|-------------|------------|
| Orchestrator surfaces theme in stage headers, checkpoints, transitions | Yes -- character names and voice present in output | Clear pass/fail |
| Checkpoint summaries quote agent artifact lines | Yes -- at least one quoted line per checkpoint | Countable |
| Business theme unchanged | Yes -- identical output to current behavior | Diffable |

Goals are SMART-adjacent: specific (which output slots), measurable (character names present, quotes counted, diffs clean), and bounded (only when non-business theme active).

### 4. Scope [blocking] -- PASS

The brief defines both what is in scope and what is out:

**In scope:** Theme-gated reporting protocol (stage headers, checkpoint quotes, transition messages), orchestrator neutrality preservation (internal routing stays personality-free), business theme guard.

**Out of scope:** Config schema changes, agent invocation template changes, two-channel architecture changes, theme-aware validators, new themes, changes to other skills.

The scope is narrow and achievable: single file change (`delivery-flow/SKILL.md`), no config changes, no new dependencies. The constraints section reinforces this with five explicit boundaries.

**Gate 1 Verdict: PASS.** All four elements present and well-articulated.

---

## Gate 2: PRD Validation

Gate 2 requires: business value clear, stories valuable, scope appropriate.

### 1. Business Value Clear [blocking] -- PASS

The PRD traces to Issue #59 and articulates a clear value proposition: users who configure a non-business theme expect the theme to be pervasive. Currently, the orchestrator -- the user's primary interface -- speaks in neutral voice while agents write in character behind the scenes. The feature closes this gap.

**Goals table (Section 1)** provides 4 goals with measurable targets, baselines, and measurement methods:

| Goal | Target | Measurement |
|------|--------|-------------|
| G-01: Theme in orchestrator output | Stage headers, checkpoints, transitions carry themed voice | Dogfooding with `lotr` theme |
| G-02: Agent voice quoted at checkpoints | At least 1 quoted line at each of 4 human checkpoints | Visual inspection |
| G-03: Business theme unchanged | Zero output differences | Diff test before/after |
| G-04: Two-channel preserved | Zero artifact content in downstream agent prompts | Code review |

All goals are measurable and have clear baselines ("currently personality-free", "current behavior"). G-03 and G-04 are preservation goals -- they ensure the feature does not break existing guarantees. This is mature product thinking for an enhancement.

**Personas (Section 2):** Three personas map to distinct user segments:

| Persona | Need | Relevant Goals |
|---------|------|----------------|
| Aria (solo dev, `lotr` theme) | Full themed experience in real-time chat | G-01, G-02 |
| Dev team lead (`star-wars` for engagement) | Checkpoint summaries as mission briefings | G-01, G-02 |
| Enterprise user (`business` theme) | No regressions | G-03 |

Every persona maps to goals. No persona is orphaned. The enterprise user persona ensures backward compatibility is a first-class concern, not an afterthought.

### 2. Stories Are Valuable [blocking] -- PASS

Five user stories (Section 7), all following proper format:

| Story | Value Proposition | Assessment |
|-------|-------------------|------------|
| US-01: Themed Stage Experience | Theme woven through pipeline, not buried in files | Clear user value, maps to FR-01 |
| US-02: Agent Voice at Checkpoints | Taste of personality without opening artifact files | Clear user value, maps to FR-02 |
| US-03: Themed Transitions | Pipeline feels like narrative journey, not checklist | Clear user value, maps to FR-03 |
| US-04: Business Theme Unchanged | No regressions from un-opted feature | Defensive value, maps to FR-04, FR-05 |
| US-05: Partial Theme Graceful Degradation | Pipeline never crashes from missing theme entry | Resilience value, maps to FR-01.4, NFR-02 |

Each story articulates a distinct "so that" clause. US-04 and US-05 are defensive stories -- they protect existing users and edge cases. No story is duplicative. All stories trace to functional requirements.

**FR coverage is thorough:**
- 5 functional requirements with 15 acceptance criteria across 2 groups (A: theme-gated reporting, B: neutrality preservation)
- Every AC uses Given/When/Then format with clear pass/fail conditions
- FR-04 and FR-05 are preservation requirements ensuring internal routing, state files, agent templates, and signal block formats remain unchanged
- FR-01.4 handles the partial theme edge case (role not in theme's `roles` map) with neutral fallback

### 3. Scope Appropriate [blocking] -- PASS

**Not too large:**
- Single file change: `delivery-team/skills/delivery-flow/SKILL.md` only
- No config schema changes -- `aliases.theme` already exists
- No new files, no new dependencies
- 5 FRs, 3 NFRs -- appropriately sized for a single-file enhancement
- 6 explicit out-of-scope items with rationale (Section 6)

**Not too small:**
- 15 acceptance criteria cover the feature comprehensively
- 3 NFRs address performance, resilience, and maintainability
- Risk analysis (Section 9) identifies 4 risks with mitigations
- Implementation notes (Section 10) provide actionable guidance for Design/Architect stages
- Dependencies section (Section 8) confirms all prerequisites exist

**Scope boundaries well-defined:**
- Section 6 draws clear in/out lines. Agent invocation templates, two-channel architecture, validator prompts, new themes, and other skills are all explicitly out of scope.
- The single-file constraint is repeated in the brief, PRD summary, and scope section -- no ambiguity about the change boundary.
- Implementation notes correctly defer structural decisions (where in SKILL.md to add the protocol) to Design/Architect.

---

## Additional Observations

**Strengths:**

1. **Brief-to-PRD traceability is seamless.** The PRD elaborates every element from the brief without introducing scope creep. Goals, constraints, and scope boundaries align perfectly between the two artifacts.

2. **Two-channel preservation is treated as a hard constraint, not a nice-to-have.** FR-02.2 explicitly scopes quote reading to user-facing output only. FR-04.3 confirms agent prompts contain only paths. The PRD understands that violating the two-channel rule would be an architectural regression, not just a style issue.

3. **Partial theme fallback (FR-01.4, NFR-02)** handles an edge case that would be easy to overlook. Custom themes that only cover some roles should degrade gracefully, not crash. This is the kind of defensive requirement that prevents support tickets.

4. **The quote extraction constraint (FR-02.1: max 280 characters, FR-02.4: omit if no themed language found)** shows thoughtful design. Quoting neutral prose would be worse than quoting nothing. The 280-character limit prevents checkpoint summaries from becoming walls of text.

5. **Success metrics (Section 5)** include pipeline completion rate monitoring. This acknowledges the risk that theme surfacing could introduce parsing issues or confuse routing. Measuring failure rates pre/post is responsible.

**Items to watch (not blocking):**

1. **FR-03.2 asks themed transitions to preserve routing signals within the themed message.** Design should specify exactly which tokens are required (stage number, stage name, continuation directive) and whether they must appear as structured markers or can be woven into prose. If the orchestrator relies on parsing its own transition messages, themed prose could break self-parsing.

2. **NFR-03 claims "new themes require zero SKILL.md changes."** This is true because Phase 0 already loads theme data dynamically, but it is worth verifying during development that the theme surfacing instructions in SKILL.md are truly theme-agnostic and do not reference specific theme names (except as examples).

---

## Verdict

**Gate 1 (Idea Brief):** All four elements present and well-articulated. Problem is specific, users are identified, goals are measurable, scope is narrow and bounded.

**Gate 2 (PRD):** All three criteria pass:

1. **Business value clear**: 4 goals with measurable targets traced to 3 personas. Preservation goals (G-03, G-04) ensure no regressions. Every FR maps to a persona and a goal.
2. **Stories valuable**: 5 user stories with distinct value propositions. Defensive stories (US-04, US-05) protect existing users and edge cases. All stories trace to FRs with Given/When/Then acceptance criteria.
3. **Scope appropriate**: Single-file change, no new dependencies, 5 FRs with 15 ACs, 3 NFRs, 4 risks mitigated, 6 explicit out-of-scope items. Well-bounded for a FEATURE project type.

*"You shall pass."*

**DONE**

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/02-refine/dod/po-review.md
SUMMARY: Idea brief and PRD both pass -- problem specific, goals measurable, stories valuable, scope well-bounded to single SKILL.md change.
```
