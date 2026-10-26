---
loaded_by: music-flow
level: L2
last_reviewed: 2026-10-26
---

# Stage 3: Structure

Routing data: `stages.yml` key `03-structure`. Loop cap: `loops.structure`.

## Purpose

Fix the song's skeleton: key, mode, bpm, time signature, form template, section bars, and the
per-section `meter_spec` and `rhyme_scheme` that Stage 4 gates measure against.

## Dispatch

| Item | Value |
|------|-------|
| Worker | agent `composer`, role `groove`, task `structure` (Template 1) |
| Critic | agent `song-critic`, role `structure-judge` (Template 3, Stage 3 rubric) |
| Inputs | `brief.md`, `concept.md` (absent for REWRITE, THEORY) |
| Output | `structure.md` |
| Owner | `groove` |

## Gate

```text
structure_check.py {dir}/structure.md
```

Checks section labels and order against the named `form_template`, and bars within the template
range. Never SKIPPED. ERROR on a missing or unknown template: stop the stage and report; ERROR is
not a loop trigger.

## Loop

FAIL: dispatch `structure-judge` with the gate JSON, re-dispatch `groove` with the critique,
`loops_used.structure += 1`. At `loops.structure`, apply `escalation.on_loop_exhaustion`.

## Per-type variations

| Type | Cell | Behaviour |
|------|------|-----------|
| FULL_SONG, INSTRUMENTAL, JINGLE | F | Standard. JINGLE uses form template `jingle` and a hard length cap. INSTRUMENTAL has empty `meter_spec` and `rhyme_scheme` columns |
| LYRICS_ONLY, REWRITE | L | Single dispatch, gate runs, no critic loop; FAIL applies escalation immediately. LYRICS_ONLY still needs the meter spec for Stage 4. REWRITE: `groove` infers `meter_spec` from the supplied lyric under `brief.md` `## Supplied input` |
| TOPLINE | I | The user supplied chords. `groove` still runs once to derive form and meter spec from the supplied progression (the artifact is validated, not invented); treat as L for loop purposes |
| ADAPT_GENRE, AUGMENT_LYRICS | I | `groove` infers `structure.md` from the supplied source (one dispatch, no critic loop); the gate validates it. Meter is the source's, not the target genre's. `source_genre` form fidelity is preserved here; genre change happens in Stages 4-6 |
| THEORY | - | Skipped |
| REVISE | per request | F only when the request touches form, bars, tempo, key, time signature, or meter; then run `structure_check.py --consistency {present}` and re-run invalidated downstream stages per `references/shared/song-types.md` |

An `I` cell here means the artifact originates from user-supplied input but still needs a
well-formed `structure.md` for downstream gates. The single `groove` dispatch is a transcription
of the source's shape, run as L, and the gate must pass.

## state.json after this stage

`stage`, `loops_used.structure`, `gates.structure`, `owners["structure.md"]`, `updated`.
