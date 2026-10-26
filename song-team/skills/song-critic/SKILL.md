---
name: song-critic
description: Song critic agent with rubric-driven judges (hook, prosody, structure, music), a listener-persona review panel, and an adversarial challenger that hunts cliche, prosody collisions, structural monotony, and resemblance to known works. Critiques cite gate-script violations; scripts decide the gate. Triggers on phrases like "critique this song", "is this lyric good", "prosody check", "listener feedback", "song review".
license: Apache License 2.0 - See repository LICENSE file
tier: B
maintainer: song-team-leads
fitness_review_due: 2027-01-24
context_budget: 300
allowed-tools: [Read, Write, Edit, Bash, Agent, Skill]
---

# song-critic

> **Status: Wave 2 lyric slice (W2-4).** `hook-judge`, `prosody-judge`, and `structure-judge` are live. `music-judge`, `listener-panel`, and `challenger` land in W3-4; their rows below point at files that exist as placeholders so the table resolves today.

## Design Principle: Critics Interpret, Scripts Decide

A gate script (`song-team/scripts/*.py`) decides PASS or FAIL. A judge never decides a gate. The judge exists because a FAIL report tells the worker *where* and *by how much*, never *why* in craft terms or *what to write instead*. The judge supplies the why and the what.

Three rules bind every judge:

1. **Evidence first.** The judge receives the gate script's `--json` output as evidence. Every row in the critique's `## Findings` table cites a `violations[].location` copied verbatim from that JSON (for example `Verse 1:1`, `hook_line`, `structure.md:sections`). The orchestrator discards a finding with no location.
2. **No override.** A judge never marks a gate passed, never softens a threshold, never tells the worker to ignore a violation. When the judge believes a heuristic (syllable count, stress guess, rhyme key) is wrong on a specific line, it records that doubt under `## Suspected false positives` with the location and the reasoning. The orchestrator surfaces the doubt to the user at escalation time; the gate still stands.
3. **Rubric informs, never gates.** When the gate PASSED and the orchestrator still dispatched a judge (quality pass, debate input, user request), the judge scores the rubric and lists craft issues with a `rubric:` prefixed location keyed to a `metrics` name. Those rows are advisory and never increment `loops_used`.

A judge reads the artifact, the gate JSON, and exactly one rubric plus one technique file. It never reads a draft history, another judge's critique, or any file outside its allowance. The main context receives only the critique artifact and the hand-back.

---

## Pipeline Context Check

Before any dispatch, check for `.song/config.yml` in the working directory.

- Present: proceed; `song-flow` owns the gate decision and the loop counter.
- Absent: announce the warning below, then proceed. The judge still needs gate JSON; run the script named in the role table by hand (`python -I song-team/scripts/<script>.py --json <artifacts>`) and paste its output as evidence.

> WARNING: No `.song/config.yml` found. This critique runs outside the song-flow pipeline. Gate thresholds come from built-in defaults, no loop counter is kept, and the critique is advisory only. Start `song-team:song-flow` for gated critique.

---

## Role Detection

Declare before every dispatch:

> `Role: [role] | Stage: [n] | Gate: [script] [status] | Rubric: references/rubrics/<file> | Technique: references/techniques/<file>`

| Role | Detect when | Gate script read as evidence | Loads (L2) | Loads (L3) |
|------|-------------|------------------------------|-----------|-----------|
| `hook-judge` | after Stage 2 (Concept); `concept.md` under review; words "hook", "title line", "chorus line" | `cliche_scan.py` on `concept.md`; `prosody_check.py --hook` | `roles/hook-judge.md`, `contracts/critique.md` | `rubrics/hook-rubric.md`, `techniques/hook-craft.md` |
| `prosody-judge` | after Stage 4 (Lyrics); `lyrics.md` under review; words "prosody", "stress", "rhyme", "singable" | every Stage 4 script: `prosody_check.py`, `rhyme_check.py`, `cliche_scan.py`, `structure_check.py` on `lyrics.md` | `roles/prosody-judge.md`, `contracts/critique.md` | `rubrics/lyric-rubric.md`, `techniques/prosody.md` |
| `structure-judge` | after Stage 3 (Structure; no critic in Wave 2, deterministic stub, dispatched from W3-2) or Stage 6 (Arrangement); `structure.md` or `arrangement.md` under review; words "form", "section order", "bars", "energy curve" | Stage 3: `structure_check.py`; Stage 6: `arrangement_check.py`, `structure_check.py --consistency` | `roles/structure-judge.md`, `contracts/critique.md` | Stage 3: `rubrics/structure-rubric.md`, `techniques/form-templates.md`; Stage 6: `rubrics/arrangement-rubric.md` (lands in W3-4), `techniques/form-templates.md` |
| `music-judge` (lands in W3-4) | after Stage 5 (Music); `chords.md` or `melody.abc` under review | `chord_tools.py`, `abc_validate.py` | `roles/music-judge.md`, `contracts/critique.md` | `rubrics/melody-rubric.md`, `techniques/melodic-contour.md` |
| `listener-panel` (lands in W3-4) | Stage 7a; review-board pattern; words "listener feedback", "would people skip" | none (advisory, never gates) | `roles/listener-panel.md`, `contracts/panel-report.md` | three `personas/*.md` selected by genre and audience |
| `challenger` (lands in W3-4) | Stage 7b always; Stage 4 when `quality.adversarial_lyrics: true`; words "challenge", "adversarial", "does this copy anything" | `challenge_gate.py` reads its output | `roles/challenger.md`, `contracts/challenge-report.md` | `shared/originality-policy.md`, `shared/blocked-targets.txt`, `shared/cliche-list.txt` |

**Ambiguity rule.** When the request names no stage and no artifact, ask which artifact is under review. Never dispatch two judges for one gate failure. When Stage 3 and Stage 6 are both plausible, the artifact decides: `structure.md` alone is Stage 3; `arrangement.md` present is Stage 6.

**Persona selection (W3-4).** `listener-panel` picks three personas by `brief.md.genre` and `audience`. The four personas shipped in this wave (`casual-radio-listener`, `lyric-first-listener`, `playlist-curator`, `musician-peer`) form the default pop and singer-songwriter panel; the remaining eight land with the panel role.

---

## Dispatch Protocol

The orchestrator (`song-flow`) normally performs these steps; a standalone invocation performs them inline.

1. **Resolve the role** from the table. Record the declaration line.
2. **Collect evidence.** Read `state.json.gates[<stage>]` when present; otherwise run the gate script(s) with `--json` and keep the full output. The evidence is the JSON, never a paraphrase of it.
3. **Check the allowance** against `song-team/references/shared/prompt-allowances.json`. Judges embed exactly: 1 role file, 1 contract, 1 rubric, 1 technique, 0 genres, 0 personas. `listener-panel` embeds 3 personas and no rubric or technique. `challenger` embeds the three `shared/` files and nothing from `rubrics/` or `techniques/`. The originality clause and the memory block are exempt.
4. **Build the prompt** from `references/agent-prompts/<role>.md`. Substitute the bracketed parts including `{project_root}`; embed the originality clause verbatim under the `<!-- originality-policy -->` marker; paste the gate JSON into the evidence block; name the artifact path to write (`{project_root}/.song/<slug>/critique-<stage>.md`; the orchestrator overwrites it on each loop).
5. **Dispatch** with the Agent tool, `subagent_type: song-critic`. The sub-agent has `Read, Glob, Grep, Write`: it reads the artifacts and writes one critique file. It never edits the artifact under review.
6. **Receive the hand-back** (`SKILL_LOADED`, `STATUS`, `ARTIFACT`, `SUMMARY`). Reject the critique and re-dispatch once when any `## Findings` row lacks a location present in the gate JSON (or a `rubric:` prefix on a PASSED gate). A second failure returns `STATUS: BLOCKED` to the orchestrator.
7. **Return** the critique path and `SUMMARY` to the caller. Do not summarise the artifact under review; the orchestrator already holds it.

Sub-agent prompts contain no draft history and no other judge's output. One dispatch, one critique, one gate.

---

## Output Contract

| Role | Contract | Artifact written |
|------|----------|------------------|
| `hook-judge`, `prosody-judge`, `structure-judge`, `music-judge` | `references/contracts/critique.md` | `.song/<slug>/critique-<stage>.md` |
| `listener-panel` | `references/contracts/panel-report.md` (W3-4) | `.song/<slug>/panel-report.md` |
| `challenger` | `references/contracts/challenge-report.md` (W3-4) | `.song/<slug>/challenge-report.md` |

`critique.md` fixes the shape: front-matter (`stage`, `gate_script`, `gate_status` only; worst status in the order `ERROR > FAIL > SKIPPED > PASS`), `## Findings` table with columns `location | violation | diagnosis | suggested revision`, `## Rubric scores` (5 criteria, 1-5), optional `## Suspected false positives`, 60 lines maximum. Rubric files under `references/rubrics/` each carry exactly five criteria with anchors at 1, 3, and 5.

---

## Hand-off

The critique feeds the worker's next loop. The orchestrator pastes it into the `## Critique to address` slot of the worker's re-dispatch prompt in this exact form:

```text
## Critique to address (if any)
Gate: <gate_script> <gate_status> (loop <n> of <cap>)
<verbatim gate JSON>

<verbatim contents of critique-<stage>.md from "## Findings" to end of file>
```

Routing of the re-dispatch by stage:

| Critique from | Re-dispatch to | Worker role |
|---------------|----------------|-------------|
| Stage 2 `hook-judge` | `lyricist` | `hook-writer` |
| Stage 3 | no critic in Wave 2 (deterministic stub); `structure-judge` for Stage 3 from W3-2 | `composer` `groove` from W3-2 |
| Stage 4 `prosody-judge` | `lyricist` | `lyric-editor` |
| Stage 5 `music-judge` | `composer` | `harmony` or `melody`, by the artifact named in `violations[].location` |
| Stage 6 `structure-judge` | `arranger` | `dynamics` for `arrangement_check.py` rows; `instrumentation` for `--consistency` rows |

`## Suspected false positives` rows travel with the critique but carry no instruction for the worker. The orchestrator shows them to the user only when `escalation.on_loop_exhaustion: ask_user` fires, alongside the last three attempts.

After the worker's revision, the orchestrator re-runs the gate script. The judge is dispatched again only on a fresh FAIL, with the fresh JSON. A judge never sees its own earlier critique.
