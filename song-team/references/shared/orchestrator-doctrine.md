---
loaded_by: song-flow
level: L1
last_reviewed: 2026-10-26
---

# Song Flow Orchestrator Doctrine

> Full elaboration of the eight design principles that `song-flow` operates under.
> `SKILL.md` carries one-line invariants; this file carries the rationale, the
> anti-pattern catalog, and the guardrails. Adapted from the delivery-team
> orchestrator doctrine for a creative pipeline whose gates are scripts.

## What the orchestrator is

`song-flow` is a coordinator. It reads config and state, builds sub-agent prompts,
dispatches workers, runs or reuses gate results, applies loop and escalation policy,
and advances the routing matrix. Its only write paths are `.song/active`,
`.song/<slug>/state.json`, `.song/<slug>/decisions.md`, `.song/<slug>/attempts/` (gate-time
copies for `accept_best`), and `.song/memory/**`. **Transitional (Wave 2 thin slice):**
two stand-ins are also written by the orchestrator until their roles land:
`package/` (W4-3) and `retrospective.md`
(W4-3). Every other file under `.song/<slug>/` is written by a dispatched sub-agent.

The orchestrator reasons from six shared files (doctrine, `stage-gates.md`,
`song-types.md`, `config-schema.md`, `artifact-formats.md`, `originality-policy.md`). It
opens other reference files and `form-templates.json` only to paste them into a prompt or
to verify a hook meter line, and keeps nothing else in its working context.

## The eight principles

1. **The orchestrator never writes the song.** Not a title, not a hook line, not a
   chord cell, not an ABC note, not a texture note. "It is only one line" is the most
   common violation. Dispatch the worker role; the orchestrator records the result.

2. **Context isolation by role and genre.** A sub-agent sees exactly one role file,
   one contract, one genre file, and the technique files its allowance permits
   (`prompt-allowances.json`). A lyricist working a country ballad never sees the
   hip-hop genre file, and never sees composer material. Pass artifact paths, not
   pasted artifact text, between stages unless the contract requires the content.

3. **Evaluator-optimizer at every creative stage.** Every F stage is a loop: worker
   produces, gate script measures, critic interprets the script output against its
   rubric, worker revises. The critic is a different sub-agent from the worker and
   receives the gate JSON as evidence. Loop caps come from `loops.<stage>`; exhaustion
   follows `escalation.on_loop_exhaustion`.

4. **Adversarial re-verification before release.** Stage 7b dispatches a challenger
   with a clean context that never saw drafts or critiques. It attacks cliche density,
   prosody collisions, structural monotony, and resemblance to known works, and writes
   a parseable severity table. `challenge_gate.py` decides; the challenger does not.

5. **Deterministic gates.** Pass and fail are decided by scripts on measurable
   properties. Sub-agents interpret and improve. They never self-certify and never
   override a gate; a judge may only note a suspected heuristic false positive in its
   critique. Only the user overrides, at an escalation point, and every override is
   written to `state.json.gate_overrides[]` and `decisions.md`.

6. **One gate runner.** Stage protocol step 4 is the only place a gate result decides
   a loop. The `SubagentStop` hook may pre-populate `state.json.gates[<stage>]` with
   an `artifact_sha256`; the orchestrator reuses it on hash match and re-runs the
   script otherwise. Hooks are advisory and never block a stage independently.

7. **Everything on disk.** Each stage writes its artifact to `.song/<slug>/` before
   the gate runs. `state.json` is updated after every dispatch so a session can resume
   at the current stage, the retrospective can read what happened, and memory can learn.

8. **Budgeted SKILL.md files.** Tier A/B/C budgets from `governance/skill-budgets.json`
   apply (A=500, B=300, C=200). Depth lives in `references/`, and every reference file
   is capped at 150 lines (genre files 100) by `check_reference_caps.py`.

## Anti-patterns

| Anti-pattern | Why it breaks the pipeline | Do instead |
|--------------|----------------------------|------------|
| Writing a "quick" hook line or chord chart inline | Violates principle 1; no gate, no critic, no ownership | Dispatch `lyricist:hook-writer` or `composer:harmony` |
| One prompt asking a sub-agent to be writer and judge | Collapses the evaluator-optimizer loop; self-certification | One role = one sub-agent; critic is a separate dispatch |
| Pasting the previous critique into the challenger prompt | Destroys the clean-context guarantee of principle 4 | Challenger receives only final artifacts and shared policy files |
| Treating an L (light) stage as skipped | L still produces an artifact and runs its gate | Single dispatch, gate runs, no critic loop |
| Treating a `SKIPPED` gate as `FAIL` | Non-English lyrics would never pass Stage 4 | Proceed as PASS and log the skip in `state.json` |
| Letting a judge "approve" a failed gate | Violates principle 5 | Only the user overrides; record it |
| Re-running the gate script when the hook hash matches | Wastes a dispatch cycle and can double-count loops | Reuse the hook result on hash match |
| Loading the whole `references/shared/` tree into the orchestrator | Context bloat; the orchestrator reasons from six files | Open any other reference only to paste it into a prompt; keep nothing else in context |
| Embedding a style target such as "sounds like <artist>" | Originality policy violation; `audit_agent_prompt.py` denies | Describe genre, era, tempo, texture in technical language |
| Advancing past Stage 7 without `retrospective.md` | Memory never learns; Stop hook blocks | Run `song-memory` as the post-pipeline protocol |

## Guardrails the orchestrator enforces

- **Allowance manifest.** Before dispatch, count the `references/` files embedded for the
  role against `prompt-allowances.json`. The `<!-- originality-policy -->` and
  `<!-- memory-lessons -->` blocks are exempt. Over-allowance is a prompt bug, not a
  reason to trim the policy clause.
- **Originality clause.** Every creative prompt embeds `originality-policy.md` verbatim
  under the `<!-- originality-policy -->` marker. `PARODY_ADAPT` is refused before any
  `.song/<slug>/` directory exists.
- **Routing is single-sourced.** The F/L/I/- matrix in `song-types.md` is the only
  routing table. `routing.force_type` pins it with a banner; `REVISE` is detected only.
- **Loop accounting.** `loops_used.<stage>` increments once per worker re-dispatch after
  a FAIL. A release-loop return to Stage 4 or 5 increments `loops_used.release` and
  resets the re-entered stage's counter to zero.
- **Decision ownership.** `state.json.owners[<artifact>]` names the one role that owns
  each artifact. Debates end with a written decision in `decisions.md`, judged by the
  orchestrator against the rubric in `stage-gates.md`.
- **Quick mode.** When `quick: true` or the brief says "quick song", every loop cap is 1,
  `on_loop_exhaustion` is `accept_best`, and the wizard asks at most two questions.
- **Standalone workers warn, never deny.** A worker skill invoked outside `song-flow`
  is told that gates will not run; it is not blocked.
- **Hand-back shape.** Every sub-agent reply begins `SKILL_LOADED:` then `STATUS`,
  `ARTIFACT`, `SUMMARY` (Appendix B of the plan). A missing marker is a warning in
  Wave 5 telemetry, not a gate failure.

## Resume protocol

On trigger, read `.song/active`; if it names a slug whose `state.json.status` is
`in_progress`, resume at `state.json.stage` and re-run that stage's gate before
dispatching anything. If the brief is a change request against a finished run, route
as `REVISE` with a new `run_id` (while REVISE is wave-blocked, stop before `song-brief`
runs so the finished run is never overwritten). A Restart passes `reuse_slug: <slug>` to
`song-brief`. Never silently start a second run while one is active.
