---
name: arranger
description: Arranger agent for instrumentation, section dynamics and energy curves, and artist-free production briefs. Auto-detects the role (instrumentation, dynamics, production-brief) and dispatches a role-scoped sub-agent. Triggers on phrases like "arrangement", "instrumentation", "production notes", "build the drop", "string arrangement".
license: Apache License 2.0 - See repository LICENSE file
tier: B
maintainer: song-team-leads
fitness_review_due: 2027-01-24
context_budget: 300
allowed-tools: [Read, Write, Edit, Bash, Agent, Skill]
---

# Arranger

## Design Principle

This skill keeps craft knowledge **out of the main context window**. Every arrangement decision is made by a sub-agent that carries exactly one role file, one output contract, one genre file, and at most two technique files. Nothing else from `references/` is loaded, ever.

- An instrumentation task for a folk brief loads `genres/folk.md` and nothing about pop or country.
- A dynamics task loads `techniques/energy-curve.md`; it never sees `reference-track-language.md`.
- A production-brief task loads `techniques/reference-track-language.md` so the brief describes sound without naming anyone.

Four rules hold across every dispatch:

1. **Role and genre isolation.** One role, one genre, per sub-agent. Mixed-genre briefs resolve to the first genre listed in `brief.md`.
2. **The arranger never judges itself.** The sub-agent writes the artifact and returns. It never claims a gate passed. `song-critic` judges; `song-flow` decides.
3. **Gates are scripts.** `arrangement_check.py` decides the energy curve and `structure_check.py --consistency` decides agreement with Stages 3 and 5 on measurable properties. The technique files teach what the scripts measure so the first attempt passes; they never replace the scripts.
4. **No names, ever.** Arrangement and production text describe sound in technical terms (tempo, texture, dynamics, space, tone). An artist name, a song title, "sounds like", or "reference track" in any artifact is a defect, not a style choice.

The main context receives only the hand-back block and the artifact path.

---

## Pipeline Context Check

Before any dispatch, check for `.song/config.yml` in the current working directory.

1. Present: proceed. `song-flow` owns the gate loop and thresholds.
2. Absent: print this warning, then proceed:

> WARNING: No song pipeline config found. This arrangement task is not running inside song-flow. Gate scripts (arrangement_check, structure_check --consistency), the critic loop, and memory lessons will NOT run. Start the pipeline with `song-team:song-flow`, or say "skip pipeline" to continue without gates.

The check warns; it never denies. "skip pipeline" bypasses the warning for the rest of the session. Standalone output still follows the output contract so a later pipeline run accepts it.

---

## Role Detection

Detect the role from the task wording and the pipeline stage, in that order of priority.

| Role | Detect when | Loads (L2) | Loads (L3) |
|------|-------------|-----------|-----------|
| `instrumentation` | task is instruments / palette / who plays what / entries and exits; song-flow Stage 6 first dispatch | `roles/instrumentation.md`, `contracts/arrangement-map.md` | `genres/<g>.md`, `techniques/section-contrast.md` |
| `dynamics` | task is energy curve / build / drop / "the chorus needs to lift"; song-flow Stage 6 second dispatch, or any dispatch carrying an `arrangement_check` FAIL | `roles/dynamics.md`, `contracts/arrangement-map.md` | `genres/<g>.md`, `techniques/energy-curve.md` |
| `production-brief` | task is notes for a producer, DAW, mix, vocal chain, tempo map; song-flow Stage 6 third dispatch | `roles/production-brief.md`, `contracts/production-brief.md` | `genres/<g>.md`, `techniques/reference-track-language.md` |

Trigger words per role:

- `instrumentation`: "instrumentation", "instruments", "palette", "string arrangement", "what plays where", "arrangement map"
- `dynamics`: "energy", "energy curve", "build", "build the drop", "lift", "dynamics", "the bridge is too loud", or any prompt that includes a gate JSON with `"script": "arrangement_check"`
- `production-brief`: "production notes", "production brief", "for the producer", "mix notes", "vocal chain", "tempo map", "DAW"

When the wording is ambiguous and no stage is supplied, ask one question: "Instrument map, energy curve, or production brief?" Never load two roles to hedge.

The technique files `vocal-production.md` and `section-contrast.md` are swap-ins for `production-brief` and `dynamics` respectively, never additions: a role embeds at most two technique files. Swap one in only when the critique names vocal layering or section sameness as the failure and the role's default pair does not address it.

Declare before every dispatch:

> `Role: [instrumentation | dynamics | production-brief] | Genre: <g> | Artifact: .song/<slug>/<file> | Refs: roles/<r>.md, contracts/<c>.md, genres/<g>.md, techniques/<t1>.md[, techniques/<t2>.md]`

---

## Dispatch Protocol

The orchestrator normally performs these steps; a standalone invocation performs them inline. `song-flow` builds and dispatches every sub-agent prompt in the pipeline; this protocol is what the skill performs when invoked on its own. Follow the steps in order for every task. Skip none.

1. **Detect the role** per the table above. Record it in the declaration line.
2. **Resolve the genre.** Read `genre:` from `.song/<slug>/brief.md`. Lower-case it and hyphenate spaces (`hip hop` becomes `hip-hop`). When `brief.md` is absent or `genre` is empty, use `pop`. When `genres/<g>.md` does not exist, use `genres/pop.md` and say so in the declaration line.
3. **Read only the allowed files.** Exactly one role file, one contract, one genre file, and at most two technique files, as the Role Detection table lists for the detected role. This matches `defaults` in `references/shared/prompt-allowances.json` (`roles: 1, contracts: 1, genres: 1, techniques: 2`). Reading a third technique file, a second genre, or any rubric or persona is a protocol violation; `audit_agent_prompt.py` will deny the dispatch once the hook lands in W4-2.
4. **Build the prompt** from `references/agent-prompts/<task>.md`, where `<task>` is `arrangement` (for `instrumentation` and `dynamics`) or `production-brief`. Substitute every `{placeholder}` with file contents or values, including `{project_root}` (the absolute path of the directory that holds `.song/`). Leave no bracket unfilled.
5. **Embed the originality clause.** Paste the fenced block from `references/shared/originality-policy.md` verbatim directly under the `<!-- originality-policy -->` marker. This block is exempt from the allowance count and is never summarised.
6. **Embed memory lessons** when `song-flow` supplies them: paste the lessons block (at most 10 lines) under the `<!-- memory-lessons -->` marker. When none are supplied, write `(none)` under the marker. Never read `.song/memory/` directly.
7. **Embed inputs.** `brief.md` and `structure.md` always; `chords.md` and `melody.abc` for `instrumentation` (range and harmonic rhythm decide the palette); the current `arrangement.md` for `dynamics` and `production-brief`; `lyrics.md` for `production-brief` when it exists; the critique and gate JSON on any re-dispatch.
8. **Dispatch** with the Agent tool, `subagent_type: "arranger"`, and the built prompt. The named agent exists so the `SubagentStop` gate hook matcher fires. Dispatch exactly one sub-agent per task; never dispatch two roles in parallel for the same artifact.
9. **Return the hand-back verbatim.** Relay the `SKILL_LOADED`, `STATUS`, `ARTIFACT`, and `SUMMARY` lines exactly as the sub-agent wrote them. Add nothing, reorder nothing, and run no gate script yourself; `song-flow` step 4 is the only gate runner.

### Stage 6 order: who writes what in `arrangement.md`

Stage 6 runs three dispatches in a fixed order: `instrumentation` -> `dynamics` -> `production-brief`. The first two **both** write `arrangement.md`; the split is by column, not by file:

| Dispatch | Writes in `arrangement.md` | Leaves alone |
|----------|----------------------------|--------------|
| 1 `instrumentation` | the header (`key`, `mode`, `bpm`, `time_sig` copied from `structure.md`), the `section` column in `structure.md` order, `instruments_in`, `instruments_out`, `texture_note`, and a **provisional** `energy` value per row (its best estimate, flagged by a `# energy: provisional` comment line above the table) | nothing exists yet |
| 2 `dynamics` | the `energy` column only, finalised against the `quality.energy_curve` rule; deletes the provisional comment | every other cell byte-for-byte |
| 3 `production-brief` | `production-brief.md` | `arrangement.md` entirely |

The gates run once, after dispatch 2, on the finalised file. `song-flow` verifies the `# energy: provisional` comment is present after dispatch 1 and absent after dispatch 2 (a mismatch re-dispatches that role once), hashes `arrangement.md` for `state.json.gates.arrangement.artifact_sha256` only after dispatch 2, and sets `owners["arrangement.md"] = "dynamics"`. A `dynamics` sub-agent that finds no `arrangement.md` (an L stage, a standalone call, or a lost file) writes the whole table itself; its role file covers both cases.

**Light stage (JINGLE, REVISE re-runs).** The routing matrix runs Stage 6 as L: a single dispatch, gate still runs, no critic loop. In L mode `song-flow` dispatches `dynamics` once with `agent-prompts/arrangement.md` to produce the complete `arrangement.md` (all columns, energy final), then `production-brief` once. `instrumentation` is not dispatched separately in L mode.

Artifact path per role:

| Role | Writes | Overwrites |
|------|--------|------------|
| `instrumentation` | `.song/<slug>/arrangement.md` | yes, on the first Stage 6 pass only |
| `dynamics` | `.song/<slug>/arrangement.md` | yes; `energy` column only when a table exists, whole table otherwise |
| `production-brief` | `.song/<slug>/production-brief.md` | yes, on re-dispatch after a critique or lint finding |

Outside the pipeline (no `.song/config.yml`), write to the path the user names, else `./arrangement.md` or `./production-brief.md` in the working directory.

---

## Output Contract

Each role has exactly one contract. The contract is the only description of the artifact the sub-agent sees, so it is complete on its own.

| Role | Contract | Artifact spec it restates | Gate scripts named in it |
|------|----------|---------------------------|--------------------------|
| `instrumentation` | `references/contracts/arrangement-map.md` | `arrangement.md`: header identical to `structure.md`; table `section, energy, instruments_in, instruments_out, texture_note`; section list identical to `structure.md`; energy integers 1-10 | `arrangement_check.py`, `structure_check.py --consistency` |
| `dynamics` | `references/contracts/arrangement-map.md` | the same file; the `energy` column must satisfy `chorus_rising` (or the configured curve) | `arrangement_check.py`, `structure_check.py --consistency` |
| `production-brief` | `references/contracts/production-brief.md` | `production-brief.md`: headings `## Tempo map`, `## Vocal treatment`, `## Mix priorities`, `## Section notes`; technical language only | `validate_artifacts.py` (lint, lands W4-2); challenger at Stage 7b |

The normative artifact grammar is `references/shared/artifact-formats.md`; the normative gate rules are `references/shared/stage-gates.md`. A contract restates them for one role and never contradicts them. When a contract and `stage-gates.md` disagree, `stage-gates.md` wins and the contract is a defect.

Every contract forbids: real artist names, real song titles, band or producer names, any entry on `references/shared/blocked-targets.txt`, the strings "sounds like" and "reference track", and quoted existing lyrics.

---

## Hand-off

The sub-agent's hand-back goes to `song-flow`, which runs the stage protocol (`stage-gates.md` section 4). What happens next, per role:

| After | song-flow runs | On FAIL, critic | Re-dispatch role |
|-------|----------------|-----------------|------------------|
| `instrumentation` (Stage 6, dispatch 1) | nothing yet; proceeds straight to `dynamics` | - | - |
| `dynamics` (Stage 6, dispatch 2) | `arrangement_check.py arrangement.md`; `structure_check.py --consistency structure.md lyrics.md chords.md melody.abc arrangement.md` | `song-critic:structure-judge` with `rubrics/arrangement-rubric.md` | `dynamics` with the critique; `instrumentation` only when the critique names the palette or a section-list diff |
| `production-brief` (Stage 6, dispatch 3) | no gate script; `validate_artifacts.py` (W4-2) lints it as an advisory `PostToolUse` hook and reports any blocked-targets hit, "sounds like", or "reference track" | `song-critic:challenger` reports a name or comparison as a BLOCKER at Stage 7b | `production-brief` with the finding, as an L re-dispatch counted against `loops.release` (never `.arrangement`) |

A stage passes only when every script returns PASS or SKIPPED. Neither Stage 6 script is ever SKIPPED. Severity order when statuses are combined: `ERROR > FAIL > SKIPPED > PASS`.

**What a critique looks like on re-dispatch.** `song-flow` fills the single `{critique}` slot under `## Critique to address` with one block: the gate line, the raw gate JSON, and the critic's findings (every item cites a `violations[].location` such as `Verse 2` or `Chorus:3`). The JSON looks like:

```json
{ "script": "arrangement_check", "status": "FAIL",
  "thresholds": { "energy_curve": "chorus_rising" },
  "metrics": { "sections": 8, "global_max": 9, "chorus_count": 3 },
  "violations": [ { "location": "Verse 2", "reason": "(d) verse energy is not below the next chorus", "observed": 7, "limit": 7 } ] }
```

The `dynamics` role changes only the `energy` cells it must, keeps every other cell byte-identical, and reports a before/after energy list in `SUMMARY` so the critic reads the diff rather than the whole table. A `structure_check --consistency` violation on `arrangement.md` (header field or section list) is a copy error: the fix is to copy the header and section labels from `structure.md` again, never to edit `structure.md`.

**Loop exhaustion.** When `loops_used.arrangement` reaches `loops.arrangement`, `song-flow` applies `escalation.on_loop_exhaustion` (`ask_user`, `accept_best`, or `fail`). The arranger takes no part in that decision and never argues for an override.

**Downstream consumers.** `song-critic:listener-panel` reads `arrangement.md` (never `production-brief.md`) at Stage 7a; `song-critic:challenger` scans `production-brief.md` (never `arrangement.md`) at Stage 7b for names and comparisons; `song-release` copies the energy column into `package/one-pager.md` and reads `instruments_in` when `midi_export.py` picks program numbers. Every one of them depends on the `section` column matching `structure.md` exactly, which is why the contracts treat a label mismatch as a hard error rather than a style note.

---

## References

- `references/roles/` — instrumentation, dynamics, production-brief (L2)
- `references/contracts/` — arrangement-map, production-brief (L2)
- `references/genres/` — pop, country, folk (L3; more land in Wave 5)
- `references/techniques/` — section-contrast, energy-curve, reference-track-language, vocal-production (L3)
- `references/agent-prompts/` — arrangement, production-brief (prompt skeletons per Appendix B of the plan)
- `song-team/references/shared/` — originality policy, stage gates, artifact formats, blocked targets (read by song-flow; embedded, never loaded here)
