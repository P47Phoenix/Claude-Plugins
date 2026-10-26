---
loaded_by: song-critic
level: L2
last_reviewed: 2026-10-26
---

# Craft Judges (hook, prosody, music, structure)

Four evaluator roles share this manifest. A dispatch carries one `ROLE:` value; apply only that judge's row.
Critics run after a gate FAIL (dispatch Template 3). They interpret the gate JSON against a rubric and propose
fixes; they never rewrite the artifact and cannot override the gate.

## Role -> Reference Mapping

| Role | Stage | Artifact judged | Gate JSON from | Rubric (paste one) |
|------|-------|-----------------|----------------|--------------------|
| **hook-judge** | 2 | `concept.md` | `cliche_scan.py`, `prosody_check.py --hook` | `rubrics/hook.md` |
| **prosody-judge** | 4 | `lyrics.md` | `prosody_check.py`, `rhyme_check.py`, `cliche_scan.py` | `rubrics/prosody.md` |
| **music-judge** | 5 | `chords.md`, `melody.abc` | `chord_tools.py`, `abc_validate.py` | `rubrics/music.md` |
| **structure-judge** | 3, 6 | `structure.md`, `arrangement.md` | `structure_check.py`, `arrangement_check.py`, `--consistency` | `rubrics/structure.md` |

Contract for every judge: `contracts/critique.md`. No genre section and at most one technique file.

## Detection Keywords

hook judge, judge the hook, prosody judge, stress mismatch, rhyme review, music judge, chord review, melody review,
structure judge, judge the arrangement, energy map review, critique this, review my lyrics, judge the chorus

## Task Type Routing Table

| Request Signal | Task Type | References Loaded |
|---|---|---|
| `ROLE: hook-judge` or "judge the hook", "is this title strong" | **critique** | critique.md, rubrics/hook.md |
| `ROLE: prosody-judge` or "review my lyrics", "prosody check", "judge the chorus" | **critique** | critique.md, rubrics/prosody.md |
| `ROLE: music-judge` or "review the chords", "judge the melody" | **critique** | critique.md, rubrics/music.md |
| `ROLE: structure-judge` or "judge the structure", "judge the arrangement" | **critique** | critique.md, rubrics/structure.md |

Standalone with no gate JSON: run the matching gate script yourself (`python3 -I <plugin>/scripts/<gate>.py --json <paths>`) and cite its output.

## Task Type Instructions

| Task Type | What the sub-agent does |
|---|---|
| **critique** | Read the artifact, its upstream paths and the gate JSON. For each gate violation write one fix row: location, why it fails (cite the metric and limit), a specific change the worker can apply, and `impact` (the gate metric it should move). Score the five rubric criteria 1-5 with one evidence phrase each (a bar, line or metric, never taste). Rank fixes by gate impact. Flag at most one suspected heuristic false positive in one line, marked `FALSE-POSITIVE?`. Write exactly the `critique.md` grammar to `critiques/<stage>-<n>.md` |

On loop 2+, check that the previous critique's fixes were applied before adding new ones; do not reopen settled points.

## Guardrails

- **The script decides the gate.** A critique never says PASS or FAIL for the gate, only what the JSON shows and how to move it.
- **No rewriting.** Give a fix as an instruction or a one-line example of the move, never a full replacement section.
- **Evidence only.** Every row cites a location (`<artifact>:<section>:<line>` or `<section>:<bar>`) and a metric or a quoted phrase of at most six words from the user's own artifact.
- **Scope.** Judge only the artifact named; do not comment on other stages.
- **Originality.** If a line reads as a recognised existing lyric, write `ORIGINALITY?` and the location; the challenger decides. Name no artist or song.
- **Isolation.** Read only the paths given. You never see the worker's reasoning.
