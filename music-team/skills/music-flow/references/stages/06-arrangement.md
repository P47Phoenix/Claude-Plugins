---
loaded_by: music-flow
level: L2
last_reviewed: 2026-10-26
---

# Stage 6: Arrangement

Routing data: `stages.yml` key `06-arrangement`. Loop cap: `loops.arrangement`.

## Purpose

Map instrumentation and energy per section, then write a producer-facing brief in technical
language only (tempo map, vocal treatment, mix priorities, section notes).

## Dispatch

| Item | Value |
|------|-------|
| Worker chain | agent `arranger`: `instrumentation` (task `arrangement`), then `dynamics`, then `production-brief` (Template 2, three sequential calls) |
| Critic | agent `song-critic`, role `structure-judge` (Template 3, Stage 6 arrangement rubric) |
| Inputs | `brief.md`, `structure.md`, `chords.md`, `melody.abc` |
| Outputs | `arrangement.md`, `production-brief.md` |
| Owners | `dynamics` for `arrangement.md`, `production-brief` for `production-brief.md` |

## Gates (both; PASS or SKIPPED each)

```text
arrangement_check.py --structure {dir}/structure.md {dir}/arrangement.md
structure_check.py --consistency {present}
```

`{present}` is every artifact of the run that exists: `structure.md` plus any of `lyrics.md`,
`chords.md`, `melody.abc`, `arrangement.md`. `--structure` makes `arrangement_check.py` also FAIL on
section-list mismatch; a flat energy map (range below `quality.min_energy_range`, default 3) or a
"sounds like" / blocked-target hit is a FAIL too, and a malformed table is ERROR (exit 3).
`production-brief.md` additionally gets `validate_artifacts.py` as an advisory hook (blocked-targets
and "sounds like" lint); treat any reported hit as a FAIL of this stage.

## Loop

FAIL: dispatch `structure-judge` with the gate JSON, re-dispatch the role whose artifact the
violation names (`dynamics` for energy curve, `instrumentation` for table shape, `production-brief`
for lint hits); `loops_used.arrangement += 1`. A `--consistency` violation naming `key`, `mode`,
`bpm`, or `time_sig` is fixed in the artifact that disagrees with `structure.md`, never by editing
`structure.md` here. At `loops.arrangement` apply `escalation.on_loop_exhaustion`.

## Per-type variations

| Type | Cell | Agent / role | Behaviour |
|------|------|--------------|-----------|
| FULL_SONG, INSTRUMENTAL | F | `arranger` | Standard. INSTRUMENTAL energy curve is built from the motif, no vocal-treatment section beyond "none" |
| JINGLE | L | `arranger` | Single chain, gates run, no critic loop; length cap from `target_length_sec` |
| ADAPT_GENRE | I | agent `adapter`, role `music-adapter` | Source arrangement notes (if any) are the input; one adapter dispatch re-targets instrumentation and energy for `target_genre`; gates validate. No critic loop |
| LYRICS_ONLY, AUGMENT_LYRICS, REWRITE, TOPLINE, THEORY | - | none | Skipped |
| REVISE | per request | `arranger` | F when the request touches `arrangement.md` or `production-brief.md`; otherwise L when `--consistency` flags the arrangement header |

## state.json after this stage

`stage`, `loops_used.arrangement`, `gates.arrangement`, `owners["arrangement.md"]`,
`owners["production-brief.md"]`, `updated`.
