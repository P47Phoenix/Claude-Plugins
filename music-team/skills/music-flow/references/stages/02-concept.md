---
loaded_by: music-flow
level: L2
last_reviewed: 2026-10-26
---

# Stage 2: Concept

Routing data: `stages.yml` key `02-concept`. Loop cap: `loops.concept`.

## Purpose

Turn the brief into a title, a hook, a central image, and a three-beat arc. The hook is the
unit later stages are measured against (syllable cap, cliche density).

## Dispatch

| Item | Value |
|------|-------|
| Worker | agent `lyricist`, role `hook-writer`, task `hook-concept` (Template 1) |
| Critic | agent `song-critic`, role `hook-judge` (Template 3) |
| Inputs | `brief.md` |
| Output | `concept.md` (grammar in `references/shared/artifact-formats.md`) |
| Owner | `hook-writer` |

## Gates

Both scripts run; the stage passes only if each returns PASS or SKIPPED.

```text
cliche_scan.py {dir}/concept.md                 # scans title, hook_line, central_image
prosody_check.py --hook {dir}/concept.md        # hook_line syllables <= quality.hook_max_syllables
```

`prosody_check.py --hook` returns SKIPPED for INSTRUMENTAL (a `motif` instead of `hook_line`) and
for non-English briefs. SKIPPED proceeds as PASS and is logged under `gates.concept.skipped: true`.

## Loop

1. Dispatch worker. Run gates. PASS or SKIPPED: advance.
2. FAIL: dispatch `hook-judge` with the gate JSON, then re-dispatch `hook-writer` with the critique
   path; `loops_used.concept += 1`.
3. When `loops_used.concept` reaches `loops.concept`, apply `escalation.on_loop_exhaustion`
   (`ask_user` | `accept_best` | `fail`). Two hook candidates that tie after a critique go to the
   debate rubric in `references/shared/stage-gates.md` section 6; record the result in `decisions.md`.

## Per-type variations

| Type | Cell | Behaviour |
|------|------|-----------|
| FULL_SONG, LYRICS_ONLY, TOPLINE, JINGLE | F | As above. JINGLE: hook is the tagline; length cap from `target_length_sec` |
| INSTRUMENTAL | L | Single dispatch, no critic loop. Worker writes a `motif` description instead of `hook_line`; on gate FAIL apply escalation immediately |
| ADAPT_GENRE, AUGMENT_LYRICS | I | No dispatch and no `concept.md`: the concept is the user's supplied source in `brief.md` `## Supplied input`. Log `stage 2: input, no artifact` in `state.json` and advance |
| REWRITE, THEORY | - | Skipped |
| REVISE | per request | Run as F only when the request touches `concept.md` (title, hook, image) |

## state.json after this stage

`stage`, `loops_used.concept`, `gates.concept` (`status`, `metrics`, `violations`, `artifact_sha256`,
`skipped`), `owners["concept.md"]`, `updated`.
