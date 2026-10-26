---
name: composer
description: Composer agent for chord progressions (Roman numerals plus concert pitch), melodies in ABC notation, and groove, tempo, key, and form decisions. Auto-detects the role (harmony, melody, groove) and dispatches a role-scoped sub-agent carrying one genre file and at most two technique files. Triggers on phrases like "chord progression", "write a melody", "key and tempo", "harmonize", "topline", "song structure", "what form should it be".
license: Apache License 2.0 - See repository LICENSE file
tier: B
maintainer: song-team-leads
fitness_review_due: 2027-01-24
context_budget: 300
allowed-tools: [Read, Write, Edit, Bash, Agent, Skill]
---

# Composer

## Design Principle

This skill keeps music craft knowledge **out of the main context window**. Every chord, note, and structural decision is made by a sub-agent that carries exactly one role file, one output contract, one genre file, and at most two technique files. Nothing else from `references/` is loaded, ever.

- A structure task for a folk brief loads `genres/folk.md` and nothing about pop or country.
- A chord task loads `techniques/functional-harmony.md` and `techniques/borrowed-chords.md`; it never sees the ABC primer.
- A melody task loads `techniques/melodic-contour.md` and `techniques/abc-notation-primer.md`; it never sees the chord grammar beyond what `chords.md` itself shows.

Three rules hold across every dispatch:

1. **Role and genre isolation.** One role, one genre, per sub-agent. Mixed-genre briefs resolve to the first genre listed in `brief.md`.
2. **The composer never judges itself.** The sub-agent writes the artifact and returns. It never claims a gate passed. `song-critic` judges; `song-flow` decides.
3. **Gates are scripts.** `structure_check.py`, `chord_tools.py`, and `abc_validate.py` decide pass/fail on measurable properties: template fit, diatonic ratio, parse validity, range, leaps, lyric alignment. The technique files teach what the scripts measure so the first attempt passes; they never replace the scripts.

The main context receives only the hand-back block and the artifact path.

---

## Pipeline Context Check

Before any dispatch, check for `.song/config.yml` in the current working directory.

1. Present: proceed. `song-flow` owns the gate loop and thresholds.
2. Absent: print this warning, then proceed:

> WARNING: No song pipeline config found. This music task is not running inside song-flow. Gate scripts (structure_check, chord_tools, abc_validate), the critic loop, and memory lessons will NOT run. Start the pipeline with `song-team:song-flow`, or say "skip pipeline" to continue without gates.

The check warns; it never denies. "skip pipeline" bypasses the warning for the rest of the session. Standalone output still follows the output contract so a later pipeline run accepts it.

---

## Role Detection

Detect the role from the task wording and the pipeline stage, in that order of priority.

| Role | Detect when | Loads (L2) | Loads (L3) |
|------|-------------|-----------|-----------|
| `groove` | task is form / tempo / key / time signature / meter spec / "structure"; song-flow Stage 3 | `roles/groove.md`, `contracts/structure.md` | `genres/<g>.md`, `techniques/rhythmic-feel.md`, `techniques/form-templates.md` |
| `harmony` | task is chords / progression / "harmonize" / key centre; song-flow Stage 5 first dispatch | `roles/harmony.md`, `contracts/chord-chart.md` | `genres/<g>.md`, `techniques/functional-harmony.md`, `techniques/borrowed-chords.md` |
| `melody` | task is melody / topline / tune / "sing this"; song-flow Stage 5 second dispatch | `roles/melody.md`, `contracts/melody-abc.md` | `genres/<g>.md`, `techniques/melodic-contour.md`, `techniques/abc-notation-primer.md` |

Trigger words per role:

- `groove`: "structure", "form", "tempo", "bpm", "key and tempo", "time signature", "how many bars", "meter", "what form"
- `harmony`: "chords", "chord progression", "harmonize", "reharmonize", "what key", "progression for the bridge"
- `melody`: "melody", "topline", "tune", "write the vocal line", "ABC", "sing it", or any prompt that includes an `abc_validate` gate JSON with `"status": "FAIL"`

Song-type rules that change what a role does (the role file carries the detail):

- `TOPLINE`: the user's chord chart is validated input (`chord_tools.py` runs on it, no `harmony` dispatch); only `melody` runs at Stage 5. Stage 3 `groove` derives the section list and bars from that chart.
- `INSTRUMENTAL`: `concept.md` carries `motif`, not `hook_line`; `groove` leaves every `meter_spec` empty; `melody` writes no `w:` lines and alignment is skipped.
- `REWRITE`: Stage 2 does not run; `groove` infers each section's meter spec and rhyme scheme from the supplied lyric in `brief.md`.
- Every other type: `groove` writes Chorus line 1's meter from `concept.md.hook_line` by hand (syllables and stress per `techniques/rhythmic-feel.md`); the lyricist sings the hook on that line.

The technique file `modal-color.md` is a swap-in, never an addition: `harmony` embeds it in place of `borrowed-chords.md` and `melody` in place of `melodic-contour.md` only when `structure.md` names a mode other than `major` or `minor`, or when the critique says the key is unclear. A role embeds at most two technique files.

When the wording is ambiguous and no stage is supplied, ask one question: "Structure, chords, or melody?" Never load two roles to hedge.

Declare before every dispatch:

> `Role: [groove | harmony | melody] | Genre: <g> | Artifact: .song/<slug>/<file> | Refs: roles/<r>.md, contracts/<c>.md, genres/<g>.md, techniques/<t1>.md, techniques/<t2>.md`

---

## Dispatch Protocol

The orchestrator normally performs these steps; a standalone invocation performs them inline. `song-flow` builds and dispatches every sub-agent prompt in the pipeline; this protocol is what the skill performs when invoked on its own. Follow the steps in order for every task. Skip none.

1. **Detect the role** per the table above. Record it in the declaration line.
2. **Resolve the genre.** Read `genre:` from `.song/<slug>/brief.md`. Lower-case it and hyphenate spaces (`hip hop` becomes `hip-hop`). When `brief.md` is absent or `genre` is empty, use `pop`. When `genres/<g>.md` does not exist, use `genres/pop.md` and say so in the declaration line.
3. **Read only the allowed files.** Exactly one role file, one contract, one genre file, and at most two technique files, as the Role Detection table lists for the detected role. This matches `defaults` in `references/shared/prompt-allowances.json` (`roles: 1, contracts: 1, genres: 1, techniques: 2`). Reading a third technique file, a second genre, or any rubric or persona is a protocol violation; `audit_agent_prompt.py` will deny the dispatch once the hook lands in W4-2.
4. **Build the prompt** from `references/agent-prompts/<task>.md`, where `<task>` is `groove`, `harmony`, or `melody`. Substitute every `{placeholder}` with file contents or values; `{project_root}` is the absolute path of the directory that holds `.song/`. Leave no bracket unfilled.
5. **Embed the originality clause.** Paste the fenced block from `references/shared/originality-policy.md` verbatim directly under the `<!-- originality-policy -->` marker. This block is exempt from the allowance count and is never summarised.
6. **Embed memory lessons** when `song-flow` supplies them: paste the lessons block (at most 10 lines) under the `<!-- memory-lessons -->` marker. When none are supplied, write `(none)` under the marker. Never read `.song/memory/` directly.
7. **Embed inputs.** `brief.md` always; `concept.md` for every role (except REWRITE, where it does not exist); `structure.md` for `harmony` and `melody`; `chords.md` and `lyrics.md` for `melody`; the previous artifact plus the critique and gate JSON on any re-dispatch.
8. **Dispatch** with the Agent tool, `subagent_type: "composer"`, and the built prompt. The named agent exists so the `SubagentStop` gate hook matcher fires. Dispatch exactly one sub-agent per task; never dispatch `harmony` and `melody` in parallel, because the melody reads the chart.
9. **Return the hand-back verbatim.** Relay the `SKILL_LOADED`, `STATUS`, `ARTIFACT`, and `SUMMARY` lines exactly as the sub-agent wrote them. Add nothing, reorder nothing, and run no gate script yourself; `song-flow` step 4 is the only gate runner.

Artifact path per role:

| Role | Writes | Overwrites |
|------|--------|------------|
| `groove` | `.song/<slug>/structure.md` | yes, whole file, on re-dispatch after a structure-judge critique |
| `harmony` | `.song/<slug>/chords.md` | yes, on re-dispatch after a music-judge critique |
| `melody` | `.song/<slug>/melody.abc` | yes, on re-dispatch after a music-judge critique or a new chart |

Outside the pipeline (no `.song/config.yml`), write to the path the user names, else `./structure.md`, `./chords.md`, or `./melody.abc` in the working directory.

---

## Output Contract

Each role has exactly one contract. The contract is the only description of the artifact the sub-agent sees, so it is complete on its own.

| Role | Contract | Artifact spec it restates | Gate scripts named in it |
|------|----------|---------------------------|--------------------------|
| `groove` | `references/contracts/structure.md` | five header lines (`key`, `mode`, `bpm`, `time_sig`, `form_template`), blank line, the `section / label / bars / meter_spec / rhyme_scheme` table; Chorus line 1 meter = hook line | `structure_check.py` (Stage 3, Stage 4 with `lyrics.md`, Stage 6 `--consistency`) |
| `harmony` | `references/contracts/chord-chart.md` | `key: <Tonic> <mode>`, one `[Label]` block per section, Roman-numeral cells one per bar, `>` concert lines | `chord_tools.py`; `structure_check.py --consistency` |
| `melody` | `references/contracts/melody-abc.md` | six ordered headers, `%%section` per structure row, strict ABC subset, `w:` line per music line with token rules | `abc_validate.py`; `structure_check.py --consistency` |

The normative artifact grammar is `references/shared/artifact-formats.md`; the normative gate rules are `references/shared/stage-gates.md`. A contract restates them for one role and never contradicts them. When a contract and `stage-gates.md` disagree, `stage-gates.md` wins and the contract is a defect.

Every contract forbids: real artist names, real song titles, "sounds like" comparisons, a key, mode, tempo, time signature, or section list that differs from `structure.md`, and any construct outside the gate's grammar.

---

## Hand-off

The sub-agent's hand-back goes to `song-flow`, which runs the stage protocol (`stage-gates.md` section 4). What happens next, per role:

| After | song-flow runs | On FAIL, critic | Re-dispatch role |
|-------|----------------|-----------------|------------------|
| `groove` (Stage 3) | `structure_check.py structure.md` | `song-critic:structure-judge` (F stages only; L and I stages go straight to escalation) | `groove` with the critique |
| `harmony` (Stage 5, first) | `chord_tools.py chords.md structure.md` | `song-critic:music-judge` | `harmony` with the critique, then a forced `melody` on the new chart; the pair counts ONE `loops_used.music` increment |
| `melody` (Stage 5, second) | `abc_validate.py melody.abc structure.md lyrics.md brief.md` | `song-critic:music-judge` (receives both Stage 5 scripts' JSON) | `melody` with the critique |

**Routing a Stage 5 critique row.** The script of origin of the violation, read from `state.json.gates.music.results` (`chord_tools` -> `harmony`, `abc_validate` -> `melody`), decides which role is re-dispatched. The `chords.md:` / `melody.abc:` prefix the judge writes on each `diagnosis` is a shape check only: a prefix that disagrees with the script of origin rejects the critique once and re-dispatches the judge; a second mismatch is `STATUS: BLOCKED`. One music loop = one gate FAIL + one critique + every re-dispatch it causes; a harmony re-dispatch followed by the forced melody re-dispatch is one loop, not two.

A stage passes only when every script returns PASS or SKIPPED. `structure_check.py` and `chord_tools.py` are never SKIPPED; `abc_validate.py` skips lyric alignment (not the whole gate) for INSTRUMENTAL. Severity order when statuses are combined: `ERROR > FAIL > SKIPPED > PASS`. An ERROR from `abc_validate.py` (parse failure) is always a primer violation: the re-dispatch keeps `abc-notation-primer.md` embedded.

**What a critique looks like on re-dispatch.** `song-flow` fills the single `{critique}` slot under `## Critique to address` with one block: the gate line, the raw gate JSON, and the critic's findings (every item cites a `violations[].location` such as `Chorus:3` or `Bridge:1:2`). The JSON looks like:

```json
{ "script": "abc_validate", "status": "FAIL",
  "thresholds": { "max_melodic_leap": 12, "vocal_range": [55, 79] },
  "metrics": { "bars": 48, "max_leap": 14, "min_pitch": 57, "max_pitch": 81 },
  "violations": [ { "location": "Chorus:1", "reason": "pitch outside vocal_range", "observed": 81, "limit": [55, 79] } ] }
```

**Debate trigger.** Both Stage 5 `SUMMARY` blocks end with a parseable line `PROPOSE key: <key> <mode>; bpm: <n>`. The debate fires when the `melody` proposal differs from `structure.md` (`key`, `mode`, or `bpm`); a `harmony` proposal alone that differs is logged in `decisions.md` and carried to the melody dispatch as context, since the melody reads the chart. For `TOPLINE` there is no debate: the user's chart is input and only `melody` runs. When it fires, `song-flow` runs the debate rubric in `stage-gates.md` section 6: each role submits at most 10 lines, the orchestrator scores gate compliance, brief fidelity, singability, structural fit, and specificity, records the decision in `decisions.md`, and re-dispatches `groove` only when the winning option changes `structure.md`. Neither composer role edits `structure.md` on its own.

**Loop exhaustion.** When `loops_used.structure` or `loops_used.music` reaches its cap, `song-flow` applies `escalation.on_loop_exhaustion` (`ask_user`, `accept_best`, or `fail`). The composer takes no part in that decision and never argues for an override.

**Downstream consumers.** `lyricist:verse-writer` reads `structure.md` for line counts, meter, and rhyme scheme; `arranger` reads `structure.md`, `chords.md`, and the melody range for Stage 6 consistency; `song-release` copies `melody.abc` into `package/lead-sheet.abc` and runs `midi_export.py` on `melody.abc` plus `chords.md`; `song-critic:challenger` scans `chords.md` and `melody.abc` at Stage 7b. Every one of them depends on the section labels, key, mode, bpm, and time signature being identical across the three artifacts, which is why the contracts treat any such mismatch as a hard error rather than a style note.

---

## References

- `references/roles/` — groove, harmony, melody (L2)
- `references/contracts/` — structure, chord-chart, melody-abc (L2)
- `references/genres/` — pop, country, folk (L3; more land in Wave 5)
- `references/techniques/` — rhythmic-feel, form-templates (plain copy of song-critic's), functional-harmony, borrowed-chords, melodic-contour, abc-notation-primer, modal-color (L3)
- `references/agent-prompts/` — groove, harmony, melody (prompt skeletons per Appendix B of the plan)
- `song-team/references/shared/` — originality policy, stage gates, artifact formats (read by song-flow; embedded, never loaded here)
- `song-team/scripts/data/form-templates.json` — the templates `structure_check.py` enforces (read by the gate; the technique file restates it)
