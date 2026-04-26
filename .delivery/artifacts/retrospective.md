# Retrospective: run-2026-04-20-o4v7

**Pipeline:** Opus 4.6 → 4.7 Plugin Migration Plan (DESIGN, transformation-planning sub-workflow)
**Scrum Master:** Aragorn — *"I do not know what strength is in my backlog, but I swear to you I will not let the sprint fall."*
**Date:** 2026-04-20 | **Stages:** Idea → Refine → Design (light) → Architect | **Status:** completed, plan-only terminus held

---

## Summary

- 4 stages executed, Plan/Dev/UAT correctly skipped (DESIGN-type routing).
- Artifacts: Idea brief (159 lines), PRD rev 2 (577 lines, 29 cited findings, 8 REQs), scope-baseline (191 lines), DX design (338 lines), transformation-plan rev 1 (610 lines, 4 waves, 14 WIs), 6 ADRs (395 lines), ~20 reviews/validations.
- First-try DoD passes: 2/4 stages (Idea, Design). Refine + Architect each needed one revision cycle.
- Defects caught pre-gate: **3 command-validity bugs in Stage 2 Developer DoD** + **one ADR-status process smell (ADR-006)** + **one measurement-infrastructure gap (WI-06)** in Stage 4 adversarial loop.
- One rate-limit interruption on Stage 3 (artifact wrote successfully; only the STATUS signal block was truncated — non-fatal).

---

## What Went Well

1. **PRD citation discipline held under adversarial pressure.** Every Anthropic-docs claim in PRD rev 2 cited a live URL; Challenger spot-checked 8 load-bearing quotes and all matched verbatim. No fabricated quotes, no stale doc references. This is the single most load-bearing property of a migration plan and it held.

2. **Developer DoD caught 3 real command-validity bugs in Stage 2.** Gimli actually *ran* the grep regex, the alias path lookup, and the `parallel_validators` config read against the live repo. QA DoD, PO DoD, and Architect DoD all ACCEPTed — they reasoned about the commands. Only the validator that executed them found the defects. Dogfooding is not a slogan; it is the only validator class that catches this failure mode.

3. **Architect-revision pattern converged cleanly in one round.** All 5 DoD validators returned DONE after rev 1. Reviewers surfaced 10 findings (F-C-01…F-C-10) graded low-to-medium; Architect absorbed the fixable ones, documented the rest as impl-run caveats, and no second revision was needed. The pattern "reviewers find tactical issues → Architect amends → DoD converges" worked exactly as designed.

4. **Scope terminus held under real temptation.** The PO hypothesis could have silently pulled in task-budget wiring, memory-tool adoption, prompt-caching work, or SDK-wiring during Refine — each is genuinely valuable and genuinely 4.7-adjacent. Instead they were logged as `BACKLOG-47-*.md` items (REQ-07, ADR-004). The plan ships as a plan; implementation is a separate engagement.

5. **Dogfood-before-edit primitive was applied consistently.** WI-06, WI-09, WI-12 are all "no edit unless the dogfood shows regression." The default action is "don't touch" — exactly right for a tuning engagement on a large prose surface.

---

## What Did Not Go Well

1. **Refine needed 2 PO revisions + 2 E-O loops + 2 Adversarial loops — significant API spend for a DESIGN-light stage.** The underlying cause was legitimate (Challenger loop-2 hardened AC-03B to add the 2-hostname gate, which was the correct outcome), but the stage consumed more capacity than a light routing would predict. One rate-limit interruption on Stage 3 is consistent with this pressure.

2. **ADR-006 shipped as "Accepted (contingent on an un-executed spike)."** The Challenger correctly flagged this as a process smell (F-C-01). An ADR whose viability depends on a research spike that has not run should not be stamped Accepted in the same artifact that schedules the check. The fallback (Option B HTML comments) is documented, but the status line is louder than the contingency clause.

3. **WI-06's "≥2 WebFetch calls AND ≥2 distinct hostnames" gate shipped with "measured via transcript" as the implicit tool** — i.e., an eyeball spot-check. No script, no hook instrumentation. The plan correctly insists elsewhere on dogfood-with-evidence and then softened on its most important measurement gate. The Architect-revision pass did not fully close this; it remains a documented impl-run caveat.

4. **11 of 17 SKILL.md files get `model_awareness: opus-4-7` stamped without prose review (WI-11).** The plan is honest about this via a `last_audited` note, but the stamp is a claim that will outlive the note. If a reader six months on greps for "4.7-ready" files, 11/17 hits are unverified. Noted but not fully resolved.

5. **Stage 3 DX design artifact wrote successfully but the signal block got truncated by a rate-limit interruption.** The artifact was recovered from the write, but the orchestrator had to re-synthesize the STATUS signal. Non-fatal but a reminder that signal blocks are load-bearing and should be emitted early, not last.

---

## Process Observations

### Which collaboration pattern caught the most real defects?

**Developer DoD caught the most grep-invisible, runtime-shaped defects** (3 command-validity bugs in Stage 2 that every reasoning-only validator missed). Its edge was not cleverness — it was *actually running the commands*. For any plan that names a specific grep / path / config key, Developer DoD is the only validator class that closes the "the command looks right to a reader but does not actually work" gap.

**Adversarial review caught the most structural / framing defects** (ADR-006 contingent-acceptance status smell, WI-06 measurement gap, ADR-005 missing worked example, WI-13 wave-placement inefficiency). A fresh-context Challenger reading the plan end-to-end sees structural issues that iterative authors miss — this is where adversarial review earns its cost.

**Evaluator-Optimizer caught the most AC-precision defects** (Refine loop-2 QA hardened AC-03B from "hostname" to "≥2 distinct hostnames" — closing the reason-instead-of-fetch regression window). E-O is the right pattern for tightening a spec; adversarial is the right pattern for interrogating it.

**No pattern felt redundant** on this DESIGN engagement. Each caught a class of defect the others did not. Cutting any of the three would have shipped a weaker plan.

### Developer DoD catching 3 command-validity bugs — what does this say?

It says: **for any plan that names executable commands in acceptance criteria, Developer DoD is non-optional.** Reasoning validators share the author's mental model — they read the command and reason "this would do X," and that reasoning is correct *conditional on the command parsing as the author expected*. Reading does not catch parse errors, path errors, or type errors. Running does. On migration / audit / inventory work, this is the highest-ROI validator on the board. A future DESIGN-with-commands run should treat skipping Developer DoD as a regression, not an optimization.

### Two-loop adversarial convergence (confidence 3 → 4) vs. one-shot — worth it?

**Yes, for this scope.** Loop 1 surfaced the AC-03B hostname weakness — the change from "≥1 WebFetch" to "≥2 WebFetch AND ≥2 hostnames" is the difference between catching the F-07 regression and not catching it. Loop 2 then lifted confidence 3 → 4 by re-reviewing with the hardened AC. One-shot would have shipped with the weak gate.

**Caveat:** this judgement is scope-dependent. For a single-file FEATURE, one-shot is usually enough. For a 610-line plan with 14 WIs and 29 findings, the second loop paid its cost.

---

## Lessons for Future DESIGN / Transformation-Planning Runs (portable — goes to memory)

1. **Citation spot-check is the load-bearing property of any migration plan.** If the plan cites external docs, the adversarial reviewer must independently re-fetch every load-bearing URL. A plan with 29 citations and one fabricated quote is worse than a plan with 5 verified citations.

2. **Developer DoD is non-optional on plans that name executable commands.** Reading-only validators share the author's parsing assumptions and miss command-validity bugs by construction. If the plan says `grep -L "model_awareness:" **/SKILL.md`, someone has to *run it* before DoD passes.

3. **ADR status ≠ ADR contingency.** An ADR whose acceptance depends on an un-executed spike must be stamped "Proposed," not "Accepted (contingent)." The status line is louder than the contingency clause, and readers in 6 months will grep for `Status: Accepted` and stop there.

4. **Stamp-based DX markers must be falsifiable.** `model_awareness: opus-4-7` on a file that was not prose-reviewed is a false claim wearing a truthful sleeve. Either weaken the stamp (`opus-4-7-frontmatter-only`) or earn the full stamp with a prose skim. Do not optimize for zero-cost backfill at the cost of marker trust.

5. **Pattern-library anchors must decouple from heading text.** If Plan cites `[Pattern 4.2](#pattern-4-2)` and the heading is later renamed, the citation breaks silently. Use explicit `<a id="...">` anchors for any cross-document citation authored before the target exists.

6. **Two-loop adversarial is worth it for plans with ≥10 findings.** One-shot is enough for single-file FEATUREs. For multi-wave plans, the second loop almost always lifts confidence by tightening an AC that loop-1 surfaced but did not harden.

7. **Scope terminus held by logging, not by saying no.** The PRD did not reject task-budget / memory-tool / caching work — it logged each as `BACKLOG-47-*.md`. This is the mechanism that makes "plan-only" hold without feeling restrictive.

---

## Lessons Specific to THIS Repo (Claude-Plugins — project chunk)

1. **`prompt-engineer/SKILL.md` is a keystone file.** Drift there propagates to every downstream skill author who reads it as a reference. Future prompt-pattern migrations should start here and let the citation graph pull the rest.

2. **`delivery-team/skills/delivery-flow/SKILL.md` DISP-01 section (lines 328–345) is the sub-agent dispatch contract.** Any model-migration engagement that changes sub-agent defaults (Opus 4.7's "fewer subagents spawned by default") must update this section first and baseline all downstream dispatch annotations against it.

3. **The alias-creator theme YAMLs live at `delivery-team/skills/delivery-flow/references/aliases/`** (13 files). Tone-strengthening on a regressing theme is bounded by the theme file's own scope — but tone dogfooding is inherently qualitative, so budget human judgement time into any theme-touching wave.

4. **`.delivery/config.yml` `parallel_validators: true` is a boolean, not a count.** The Stage 2 Developer DoD bug confirmed this is easy to mis-read. Future readers/editors of the config should assume any type-shaped assumption is wrong until `grep`-verified.

5. **Zero `import anthropic` / `from anthropic` anywhere in the repo.** Migration plans that assume an SDK-wiring edit path are categorically out of scope; every model-ID reference is a direct string in prose. Confirmed by grep in Stage 4 adversarial review.

6. **CLAUDE.md's plugin-dev skill routing is load-bearing during implementation.** Any impl run that edits skills/hooks/plugin-structure MUST load the corresponding `plugin-dev:*` skill first. The transformation plan embeds this; future plans should as well.

---

## Action Items (impl-engagement TODO, not orchestrator work)

These are hints for the implementation run that inherits this plan, not work for this pipeline:

- **A1.** Downgrade ADR-006 status to "Proposed" and make WI-03 an explicit Wave-1 gate (Challenger F-C-01).
- **A2.** Add a transcript-parsing script to WI-06 (a few lines of Python counting WebFetch/WebSearch calls), not a manual eyeball (F-C-02).
- **A3.** Either weaken the 11 WI-11 backfill stamps to `opus-4-7-frontmatter-only` or add a 30-min-per-file prose skim before stamping (F-C-08).
- **A4.** Add a worked example to ADR-005 for plugin-local pattern handling (e.g., `mtg-commander` Challenger-specific voicing), pre-empting the next migration's ambiguity (F-C-06).
- **A5.** Add explicit HTML anchors in WI-05's pattern-library edit so WI-04/07/08 citations decouple from heading text (F-C-04).
- **A6.** Consider moving WI-13a (pre-declared backlog) to Wave 1 alongside WI-02 to uphold the plan's own declare-scope-first discipline (F-C-07).

None of these block the plan shipping. They are the mortar-cracks, not the stone-cracks.

---

*"The fellowship holds. The plan holds. The keystones are the right six. What we ship into implementation is a map, not a monument — and it was drawn honestly, with the cracks marked."*

— Aragorn

---

**End of retrospective.**
