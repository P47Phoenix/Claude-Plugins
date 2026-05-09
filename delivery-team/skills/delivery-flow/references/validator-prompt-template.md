# Validator Prompt Template (W3-13)

Canonical, copy-paste shell for every DoD validator dispatched from the
delivery-flow orchestrator. Codifies the spec-vs-impl framing block and the
canonical artifact-path block so validators do not invent their own structure.

> **Why this exists**: Wave 1 + Wave 2 + caveman-lite (tk3) all logged the
> same recurring failure mode — validators looked in the wrong canonical path
> for inputs (path-lookup false positive) **or** treated a Stage 6 deliverable
> as a Stage 4 prerequisite (semantic-frame mistake). Both errors are
> structural, not skill-specific. They are eliminated by binding every
> validator dispatch to this template.

## Template (paste verbatim into validator dispatch)

```
You are validating a delivery-pipeline artifact as the [ROLE] on the
delivery team. STATE the framing before you read the artifact:

--- FRAMING (spec vs impl) ---
TARGET (the artifact you are validating)
- Path: [ARTIFACT_FILE_PATH]
- Stage: [N — name]
- Producer role: [PRODUCER_ROLE]
- Type: [SPEC | IMPLEMENTATION | REPORT]

CURRENT (what already exists in the working tree, NOT to be re-validated)
- Upstream artifacts: [LIST CANONICAL PATHS — see below]
- Working-tree code/config: [LIST RELEVANT REPO PATHS, IF ANY]

You are validating TARGET against TARGET-stage criteria ONLY. You are NOT
validating CURRENT (it has already been gated). If you find a defect in
CURRENT, log it as a finding on TARGET only if TARGET fails to handle it.
--- END FRAMING ---

--- INPUT ARTIFACTS (canonical paths — read with Read tool) ---
- TARGET: [ARTIFACT_FILE_PATH]
- Upstream:
  - .delivery/artifacts/01-idea/po/idea-brief.md       (Stage 1 brief)
  - .delivery/artifacts/02-refine/po/prd.md            (Stage 2 PRD)
  - .delivery/artifacts/03-design/<role>/<artifact>.md (Stage 3, if ran)
  - .delivery/artifacts/04-architect/solution/<arch>.md+ adrs/ADR-*.md
  - .delivery/artifacts/05-plan/po/stories.md          (Stage 5 backlog)
  - .delivery/artifacts/06-dev/developer/story-N-implementation.md
  - .delivery/artifacts/07-uat/<role>/<artifact>.md
- Memory: .delivery/memory/topics/<topic>.md, .delivery/memory/stages/<stage>.md
--- END INPUTS ---

Apply the role-specific criteria from
`delivery-team/skills/delivery-flow/references/quality-gates.md` § [ROLE].

Respond with ONLY this signal block (single-line STATUS, parser-stable):
STATUS: DONE | NOT_DONE | CODE_COMPLETE | PASS_WITH_NOTES
ARTIFACT: <absolute or repo-relative path to your review file>
SUMMARY: <one sentence, ≤200 characters>
FINDINGS: <if NOT_DONE: bullet list — each finding cites file:line:criterion>
```

## Binding rules

1. **STATUS line is single-line, single format** — `STATUS: <value>` (no
   `**Status**:` markdown variant). Parser-stable for the orchestrator's
   `extract_dod_status.py` helper. STATUS values stay verbatim:
   `DONE | NOT_DONE | CODE_COMPLETE | PASS_WITH_NOTES`.
2. **Spec-vs-impl framing block is mandatory** — eliminates the Wave-2
   architect false-positive (treating Stage 6 deliverable as prerequisite).
3. **Canonical paths are quoted in the dispatch** — eliminates the Wave-1 +
   Wave-2 validator path-lookup false positives. Validators do not search;
   they read the named files.
4. **One validator = one Agent invocation** — see `quality-gates.md` § "One
   validator = one Agent invocation". No fused-role prompts.
5. **Verdict-prose style** — when `config.prose_style == caveman-lite`
   (default), the ≤3-sentence verdict prose around the gate-result table
   uses caveman-lite. STATUS / FINDINGS values are verbatim. See
   ADR-tk3-001 + `references/prose-style.md`.

## When to use

- Every Stage-N DoD dispatch (Stage 1 through Stage 7).
- Every adversarial-review and review-board dispatch that emits a STATUS line.
- Stage 6 self-correction round-2 dispatches (re-validate after fix).

## See also

- `references/quality-gates.md` — role-specific criteria + DoD validator
  prompt template (this file is the canonical-path + framing extension).
- `scripts/extract_dod_status.py` — STATUS-line parser the orchestrator
  uses to grep validator outputs.
- ADR-tk3-001 — verdict-prose style binding (caveman-lite default).
