# Adversarial Challenge: Orchestration Discipline Bundle PRD

*"Let us forge something that will endure beyond the ages — but first, let us strike the steel and see where it cracks."*

— Celebrimbor, Master Craftsman

---

I have examined the PRD and idea brief with the care a smith reserves for a blade meant to outlast its wielder. The work is sound in its bones, but I have found seams where the hammer has not yet fallen.

## C1 — `project_type` removal: the user-config blast radius is under-examined

FR-01 through FR-05 strip `project_type` from schema and wizard. NFR-03 promises tolerant parsing. But the PRD treats `project_type` as if it lives only in the orchestrator's head. It does not.

- **Downstream consumers.** FR-05's grep is scoped only to `delivery-team/skills/delivery-flow/`. Hooks, alias surfacing, analytics dashboard, memory tiering, defect tracking — any of them may key behavior off the configured type. **The grep must run across the entire repo, and any hit outside Phase 1 detection is a defect this PRD must own.**
- **User-pinned overrides.** Users may have committed `.delivery/config.yml` with `project_type` deliberately pinned because they *wanted* a specific routing — for example, a docs-only repo that should never trigger code stages regardless of how a request is phrased. FR-02's "tolerant ignore + deprecation log" silently changes their behavior. That is not backwards compatibility; that is a behavior break wearing a compatibility costume. **The PRD must either honor a pinned `project_type` as a user-intent override (with deprecation warning), or provide an explicit escape hatch (e.g. `routing.force_type:`) and acknowledge the behavior change in NFR-03.**
- **Wizard renumbering (FR-04) is a documentation hazard.** Q1–Q10 may be referenced by number in setup-wizard.md or external write-ups. Renumbering silently breaks any doc that says "answer Q7 with…". Trivial fix, must be called out.

## C2 — "One role = one sub-agent" has legitimate exceptions the PRD denies

FR-10 states the rule absolutely: *"A single sub-agent prompt MUST NOT request that the agent 'play multiple roles.'"* Absolutism is a fine ideal and a poor specification.

- **Sequenced single-author skills.** product-delivery bundles PO, Scrum Bag, and Data Analyst into one skill that auto-detects role. Dispatching one sub-agent into product-delivery is one role, not three. The rule as written could be misread to forbid skill bundling entirely. **Clarify: the rule forbids compound *reviewer* prompts, not skill-internal role auto-detection.**
- **Tiny atomic tandems.** Evaluator-optimizer genuinely benefits from a single agent holding both halves in working memory. The PRD treats this as forbidden without discussion. **Either justify the prohibition with evidence, or carve evaluator-optimizer as a named exception.**
- **Detection heuristic (FR-12) will fire on meta-discussion.** A prompt that says *"Do not act as both reviewer and architect"* contains the smell phrase. The hook will warn on prompts that themselves enforce the rule. Architect must specify a negation-aware matcher or accept the false-positive rate.

FR-12 is correctly softened to MAY-not-MUST. But FR-10's prose should be revised to "compound *reviewer* prompts" rather than "compound role prompts."

## C3 — `enforce_pipeline_scope.py` extension: orchestrator-vs-sub-agent detection is unsolved and the PRD knows it

OQ-1 admits this. R6 admits this. Yet FR-09's acceptance criteria *require* the detection to work. This is circular: the FR cannot be accepted until OQ-1 is answered, and OQ-1 is deferred to Architect.

**The PRD must either:**
- (a) Mark FR-09 as conditional on OQ-1 with a fallback (soft-warn instead of hard-deny if origin detection is unreliable), or
- (b) Resolve OQ-1 in this PRD by selecting a mechanism (transcript stack inspection, env var on sub-agent dispatch, or tool-call metadata).

Without one of these, the PRD ships a hook contract that cannot be implemented and Plan stage will discover this only after committing.

**Worse: the allowlist forgets edge cases.** Per-stage scratch files under `.delivery/artifacts/*/state/` (if any) and stage handoff breadcrumbs need an audit before the deny rule lands.

**Worst: hooks attribute the *acting* tool, not intent.** If the orchestrator inlines a Bash heredoc that writes a file, the hook sees Bash, not Edit/Write — and the hook is registered on Edit/Write/NotebookEdit only. **The hook must also intercept Bash with redirection/heredoc patterns targeting artifact paths, or the rule is trivially bypassed by the very "simplicity shortcut" it is meant to forbid.**

## C4 — Isolated Adversarial Loop convergence: the cap is a comfort, not a guarantee

R3 dismisses non-convergence as "low likelihood" with the cap as mitigation. I challenge this directly.

- **Each loop is a fresh sub-agent with no prior context** (FR-13 step 2a). A fresh reviewer with no memory of what was already fixed will, statistically, surface a *different* set of issues each time — including issues previous reviewers waved through. There is no monotonic decrease. **Convergence is not guaranteed by the protocol; it is merely hoped for.**
- **The Architect *does* see prior loops** — it must, in order to fix things. So the artifact gets progressively patched, but the reviewer judges fresh each time. After 3 loops you may have an artifact patched against 3 disjoint critique sets, possibly internally inconsistent because each fix optimized for its own reviewer's priorities.
- **OQ-5 routes this to Plan as a test design question. It is not.** It is a protocol design question. **FR-13 should require a convergence criterion stronger than "one clean loop" — for example, two consecutive clean loops, or a severity threshold below which loops terminate.** Otherwise the cap-reached path becomes the *normal* path and "adversarially clean" becomes vanishingly rare.

## C5 — Bundling: three of four are semantically coherent; #69 is bundled by geography

- #73, #71, #70 all touch `SKILL.md` and reinforce the same delegation/isolation theme. Tightly coupled in semantics.
- #69 (isolated adversarial loops) touches `team-patterns.md`, `pipeline-stages.md`, `config-schema.md` — shared *files* with the others, but **its substantive content has no semantic dependency on the other three**.

#69 is bundled for file proximity, not coherence. Risk: if #69's protocol turns controversial at Architect (see C4), it can hold the entire bundle hostage. **NFR-08 should permit a fallback path where #69 splits into a separate immediate follow-up if Architect rejects the loop protocol.** The other three are tightly coupled in semantics; #69 is coupled only in geography.

## C6 — Dogfooding paradox (R7) is acknowledged but not resolved

R7 says the new self-write hook will block the orchestrator authoring this very PRD's successor docs. The mitigation is "this is the intended behavior."

But the hook does not exist *yet*. It will be authored *during* this run. **The PRD must specify the activation point for the hook**: enabled on commit? on merge? on stage transition? Until then, the dogfood test is unverifiable.

Also: NFR-06 says this bundle must be delivered through delivery-flow. The current run *is* delivering it. **Clarify whether dogfooding is self-referential (this run) or forward-looking (next run).** If self-referential, the PRD must accept that some discipline rules will only be enforceable retroactively in this run.

## C7 — Doc parity (FR-16) is under-specified

FR-16 lists `config-schema.md`, `CLAUDE.md`, `README.md`, `marketplace.json`. The PRD ignores:

- `delivery-flow/SKILL.md` itself (references schema version in metadata)
- The MkDocs Material site (per recent commit `185d802` — 25 pages)
- Any hook script that asserts a minimum schema version
- The setup wizard's own self-description

**The grep target list in NFR-04 must be widened, or the doc parity validator will pass while stale references survive in the published docs site.**

---

## Direct answers to the questions posed

- **Removing project_type breaks existing users?** Yes, in the pinned-override case (C1). Tolerant parsing alone is insufficient; an explicit override mechanism or behavior-change acknowledgment is required.
- **Does "one role = one sub-agent" have legitimate exceptions?** Yes — skill-internal role auto-detection and evaluator-optimizer (C2). The rule should target compound *reviewer* prompts specifically.
- **Could the hook extension block valid orchestrator writes?** Yes — incomplete allowlist plus Bash-heredoc bypass (C3). Both must be addressed.
- **Does isolated adversarial loop risk non-convergence?** Yes (C4). The protocol is designed for non-monotonic critique sets and lacks a convergence criterion stronger than a single clean pass.
- **Are the four issues compatible to bundle?** #73/#71/#70 are semantically coherent. #69 is bundled by file geography only and should have a split-out fallback (C5).
- **Backwards compat for user configs?** Tolerant parsing covers parser-level compat but not behavioral compat for users who pinned `project_type` intentionally (C1).

## Required PRD changes before Design

1. **C1**: Widen FR-05 grep to whole repo; address pinned `project_type` as intentional override; flag wizard renumbering hazard.
2. **C2**: Reword FR-10 to "compound *reviewer* prompts"; acknowledge legitimate skill-internal role bundling.
3. **C3**: Resolve OQ-1 in PRD or mark FR-09 conditional; expand allowlist; add Bash-redirection coverage to hook scope.
4. **C4**: Specify convergence criterion stronger than "one clean loop" for FR-13; reclassify R3 from Low to Medium likelihood.
5. **C5**: Permit #69 to fall out of the bundle if its protocol is rejected at Architect.
6. **C6**: Specify hook activation timing; clarify dogfood scope (this run vs next run).
7. **C7**: Widen FR-16 doc parity targets to include MkDocs site, SKILL.md metadata, and version-asserting hooks.

---

The bundle is the right work. Gandalf has named the discipline gaps correctly. But the PRD's edges are too smooth where the metal must be sharp. C1, C3, and C4 are the items I would not let leave the forge unaddressed; the rest may be carried as Design refinements with PO acknowledgment.

*Let us forge something that will endure beyond the ages.*

— Celebrimbor

Confidence: 4/5
