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

> **Status: Wave 3 music slice (W3-4).** All six roles are live: `hook-judge`, `prosody-judge`, `structure-judge` (Stages 3 and 6), `music-judge`, `listener-panel`, and `challenger`. Twelve listener personas ship under `references/personas/`.

## Design Principle: Critics Interpret, Scripts Decide

A gate script (`song-team/scripts/*.py`) decides PASS or FAIL. A judge never decides a gate. The judge exists because a FAIL report tells the worker *where* and *by how much*, never *why* in craft terms or *what to write instead*. The judge supplies the why and the what.

Three rules bind every judge:

1. **Evidence first.** The judge receives the gate script's `--json` output as evidence. Every row in the critique's `## Findings` table cites a `violations[].location` copied verbatim from that JSON (for example `Verse 1:1`, `hook_line`, `structure.md:sections`, `Chorus:1:4`). The orchestrator discards a finding with no location.
2. **No override.** A judge never marks a gate passed, never softens a threshold, never tells the worker to ignore a violation. When the judge believes a heuristic (syllable count, stress guess, rhyme key, diatonic test) is wrong on a specific line, it records that doubt under `## Suspected false positives` with the location and the reasoning. The orchestrator surfaces the doubt to the user at escalation time; the gate still stands.
3. **Rubric informs, never gates.** When the gate PASSED and the orchestrator still dispatched a judge (quality pass, debate input, user request), the judge scores the rubric and lists craft issues with a `rubric:` prefixed location keyed to a `metrics` name. Those rows are advisory and never increment `loops_used`.

A judge reads the artifact, the gate JSON, and exactly one rubric plus one technique file. It never reads a draft history, another judge's critique, or any file outside its allowance. The main context receives only the critique artifact and the hand-back.

Two roles are not judges. The **listener-panel** hears the finished song as listeners and reports verdicts; it has no gate JSON and never loops a worker. The **challenger** sees nothing but the final artifacts and the originality files, and its report is the only critic output a script (`challenge_gate.py`) reads.

---

## Pipeline Context Check

Before any dispatch, check for `.song/config.yml` in the working directory.

- Present: proceed; `song-flow` owns the gate decision and the loop counter.
- Absent: announce the warning below, then proceed. A judge still needs gate JSON; run the script named in the role table by hand (`python -I song-team/scripts/<script>.py --json <artifacts>`) and paste its output as evidence. The panel and the challenger need no JSON; the challenger's report is then checked by hand with `python -I song-team/scripts/challenge_gate.py --json .song/<slug>/challenge-report.md`.

> WARNING: No `.song/config.yml` found. This critique runs outside the song-flow pipeline. Gate thresholds come from built-in defaults, no loop counter is kept, and the critique is advisory only. Start `song-team:song-flow` for gated critique.

---

## Role Detection

Declare before every dispatch:

> `Role: [role] | Stage: [n] | Gate: [script] [status] | Rubric: references/rubrics/<file> | Technique: references/techniques/<file>`

(`listener-panel` declares `Gate: none (advisory) | Personas: <a>, <b>, <c>`; `challenger` declares `Gate: challenge_gate pending | Shared: originality-policy, blocked-targets, cliche-list`.)

| Role | Detect when | Gate script read as evidence | Loads (L2) | Loads (L3) |
|------|-------------|------------------------------|-----------|-----------|
| `hook-judge` | after Stage 2 (Concept); `concept.md` under review; words "hook", "title line", "chorus line" | `cliche_scan.py` on `concept.md`; `prosody_check.py --hook` | `roles/hook-judge.md`, `contracts/critique.md` | `rubrics/hook-rubric.md`, `techniques/hook-craft.md` |
| `prosody-judge` | after Stage 4 (Lyrics); `lyrics.md` under review; words "prosody", "stress", "rhyme", "singable" | every Stage 4 script: `prosody_check.py`, `rhyme_check.py`, `cliche_scan.py`, `structure_check.py` on `lyrics.md` | `roles/prosody-judge.md`, `contracts/critique.md` | `rubrics/lyric-rubric.md`, `techniques/prosody.md` |
| `structure-judge` | after Stage 3 (Structure) or Stage 6 (Arrangement); `structure.md` or `arrangement.md` under review; words "form", "section order", "bars", "energy curve" | Stage 3: `structure_check.py`; Stage 6: `arrangement_check.py`, `structure_check.py --consistency` | `roles/structure-judge.md`, `contracts/critique.md` | Stage 3: `rubrics/structure-rubric.md`, `techniques/form-templates.md`; Stage 6: `rubrics/arrangement-rubric.md`, `techniques/form-templates.md` |
| `music-judge` | after Stage 5 (Music); `chords.md` or `melody.abc` under review; words "chords", "melody", "range", "leap", "diatonic" | `chord_tools.py`, `abc_validate.py` (both, always) | `roles/music-judge.md`, `contracts/critique.md` | `rubrics/melody-rubric.md`, `techniques/melodic-contour.md` |
| `listener-panel` | Stage 7a; review-board pattern; words "listener feedback", "would people skip", "panel" | none (advisory, never gates) | `roles/listener-panel.md`, `contracts/panel-report.md` | `listener_panel_size` (default 3) `personas/*.md` chosen from the selection table in `roles/listener-panel.md` |
| `challenger` | Stage 7b always; Stage 4 when `quality.adversarial_lyrics: true`; words "challenge", "adversarial", "does this copy anything" | none in; `challenge_gate.py` reads its output | `roles/challenger.md`, `contracts/challenge-report.md` | `shared/originality-policy.md`, `shared/blocked-targets.txt`, `shared/cliche-list.txt` |

**Ambiguity rule.** When the request names no stage and no artifact, ask which artifact is under review. Never dispatch two judges for one gate failure. When Stage 3 and Stage 6 are both plausible, the artifact decides: `structure.md` alone is Stage 3; `arrangement.md` present is Stage 6. Stage 5 always dispatches one `music-judge` with both scripts' JSON, even when only one of them failed.

**Persona selection.** `roles/listener-panel.md` holds the table: a genre row gives three default seats; `audience` keywords and `song_type` (`JINGLE`, `INSTRUMENTAL`) replace seat 3 (or seat 2 when the replacement already sits). A persona never sits twice. The chosen names are recorded in `state.json.owners["panel-report.md"]`.

---

## Dispatch Protocol

The orchestrator (`song-flow`) normally performs these steps; a standalone invocation performs them inline.

1. **Resolve the role** from the table. Record the declaration line.
2. **Collect evidence** (judges only). Read `state.json.gates[<stage>]` when present; otherwise run the gate script(s) with `--json` and keep the full output. The evidence is the JSON, never a paraphrase of it. For Stage 5 keep the `warnings` list; the judge treats it as advisory.
3. **Check the allowance** against `song-team/references/shared/prompt-allowances.json`. Judges embed exactly: 1 role file, 1 contract, 1 rubric, 1 technique, 0 genres, 0 personas. `listener-panel` embeds `listener_panel_size` personas (the manifest caps embedded personas at 3) and no rubric or technique. `challenger` embeds the three `shared/` files and nothing from `rubrics/`, `techniques/`, or `personas/`. The originality clause and the memory block are exempt.
4. **Build the prompt** from `references/agent-prompts/<role>.md`. Substitute the bracketed parts including `{project_root}`; embed the originality clause verbatim under the `<!-- originality-policy -->` marker; paste the gate JSON into the evidence block; name the artifact path to write (`{project_root}/.song/<slug>/critique-<stage>.md`, `panel-report.md`, or `challenge-report.md`; the orchestrator overwrites it on each loop).
5. **Dispatch** with the Agent tool, `subagent_type: song-critic`. The sub-agent has `Read, Glob, Grep, Write`: it reads the artifacts and writes one report file. It never edits the artifact under review.
6. **Receive the hand-back** (`SKILL_LOADED`, `STATUS`, `ARTIFACT`, `SUMMARY`). Reject and re-dispatch once when the shape check fails (below). A second failure returns `STATUS: BLOCKED` to the orchestrator.
7. **Return** the report path and `SUMMARY` to the caller. Do not summarise the artifact under review; the orchestrator already holds it.

Sub-agent prompts contain no draft history and no other judge's output. One dispatch, one report, one gate.

### Shape checks on the hand-back

- Judges: every `## Findings` row's `location` appears in the gate JSON (or carries a `rubric:` prefix on a PASSED gate); five rubric rows; <= 60 lines.
- `listener-panel`: one `## <persona>` block per embedded persona, in order, each with `verdict`, `top_note`, `question`; `majority` line with `n` and `m` matching the blocks; <= 40 lines.
- `challenger`: `challenge_gate.py --json` returns PASS or FAIL (an ERROR is a shape failure); every `location` begins with an artifact name; no `blocked-targets.txt` entry anywhere in the report.

### listener-panel (Stage 7a)

ONE dispatch carries exactly `quality.listener_panel_size` persona files (default 3) chosen from the selection table in `roles/listener-panel.md` by `brief.md.genre`, then adjusted by `audience` and `song_type`. The prompt embeds every final artifact present (`concept.md`, `structure.md`, `lyrics.md`, `chords.md`, `melody.abc`, `arrangement.md`) and `brief.md`; no gate JSON, no rubric, no technique. The panel is advisory: its `majority` line never gates, never loops a worker, and never blocks Stage 7b. A `SKIP` majority is shown to the user with the release notes; the user decides whether to invoke REVISE.

### challenger (Stage 7b, and Stage 4 when `quality.adversarial_lyrics: true`)

A clean-context dispatch. The prompt contains ONLY: the originality clause, `roles/challenger.md`, `contracts/challenge-report.md`, the three shared files (`originality-policy.md`, `blocked-targets.txt`, `cliche-list.txt`), `brief.md`, and the final artifacts as present: `lyrics.md`, `concept.md`, `chords.md`, `melody.abc`, `production-brief.md`. NEVER a critique, an earlier draft, an `attempts/` copy, a panel report, or a lessons block; the `<!-- memory-lessons -->` block is omitted for this role. At Stage 4 the artifacts are `lyrics.md`, `concept.md`, and `brief.md` only. The report is read by `challenge_gate.py`; a BLOCKER row's `location` names the artifact so the orchestrator routes the return (Stage 4 for `lyrics.md`, `concept.md`, `production-brief.md`; Stage 5 for `chords.md`, `melody.abc`). The challenger reports a line it recognises as an existing well-known lyric, or any named artist, song, or brand used as a style target, as a BLOCKER, citing the location and never quoting or naming the work.

---

## Output Contract

| Role | Contract | Artifact written |
|------|----------|------------------|
| `hook-judge`, `prosody-judge`, `structure-judge`, `music-judge` | `references/contracts/critique.md` | `.song/<slug>/critique-<stage>.md` |
| `listener-panel` | `references/contracts/panel-report.md` | `.song/<slug>/panel-report.md` |
| `challenger` | `references/contracts/challenge-report.md` | `.song/<slug>/challenge-report.md` |

`critique.md` fixes the shape: front-matter (`stage`, `gate_script`, `gate_status` only; worst status in the order `ERROR > FAIL > SKIPPED > PASS`), `## Findings` table with columns `location | violation | diagnosis | suggested revision`, `## Rubric scores` (5 criteria, 1-5), optional `## Suspected false positives`, 60 lines maximum. Rubric files under `references/rubrics/` each carry exactly five criteria with anchors at 1, 3, and 5.

`panel-report.md`: one `## <persona>` block per seat (`verdict: KEEP | SKIP`, `top_note:`, `question:`), then `majority: KEEP | SKIP (n of m)`; 40 lines maximum.

`challenge-report.md`: `## Findings` and the table `| severity | location | finding | suggested fix |` with severity in {BLOCKER, MAJOR, MINOR}; a header-only table is a clean pass; 60 lines maximum.

---

## Hand-off

A judge's critique feeds the worker's next loop. The orchestrator pastes it into the `## Critique to address` slot of the worker's re-dispatch prompt in this exact form:

```text
## Critique to address (if any)
Gate: <gate_script> <gate_status> (loop <n> of <cap>)
<verbatim gate JSON>

<verbatim contents of critique-<stage>.md from "## Findings" to end of file>
```

Routing by stage:

| Critique from | Re-dispatch to | Worker role |
|---------------|----------------|-------------|
| Stage 2 `hook-judge` | `lyricist` | `hook-writer` |
| Stage 3 `structure-judge` | `composer` | `groove` |
| Stage 4 `prosody-judge` | `lyricist` | `lyric-editor` |
| Stage 4 `challenger` (`adversarial_lyrics`) | `lyricist` | `lyric-editor`, with the BLOCKER rows in the critique slot; counts against `loops.lyrics` |
| Stage 5 `music-judge` | `composer` | `harmony` when the row's diagnosis opens `chords.md:` (a `chord_tools` location); `melody` when it opens `melody.abc:` (an `abc_validate` location). Rows for both artifacts produce two re-dispatches, harmony first |
| Stage 6 `structure-judge` (arrangement rubric) | `arranger` | `dynamics` for `arrangement_check.py` rows; `instrumentation` for `--consistency` rows; `production-brief` for `rubric:sections` rows that cite `production-brief.md` |
| Stage 7a `listener-panel` | nobody | shown to the user and recorded in `release-notes.md` (`panel majority`); no re-dispatch, no loop increment |
| Stage 7b `challenger` | release loop (`stage-gates.md` section 5) | `challenge_gate.py` FAIL returns to Stage 4 (`lyricist:lyric-editor`) or to Stage 5 (`composer:harmony` or `melody`) by the artifact named in the BLOCKER `location`; increments `loops_used.release`; MAJOR and MINOR rows travel to the user with the release notes and trigger nothing |

`## Suspected false positives` rows travel with the critique but carry no instruction for the worker. The orchestrator shows them to the user only when `escalation.on_loop_exhaustion: ask_user` fires, alongside the last three attempts.

After the worker's revision, the orchestrator re-runs the gate script. The judge is dispatched again only on a fresh FAIL, with the fresh JSON. A judge never sees its own earlier critique. After a release-loop return, the challenger is dispatched again from a clean context against the revised final artifacts; it never sees its own earlier report.
