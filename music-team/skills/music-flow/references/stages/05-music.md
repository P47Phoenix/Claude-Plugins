---
loaded_by: music-flow
level: L2
last_reviewed: 2026-10-26
---

# Stage 5: Music

Routing data: `stages.yml` key `05-music`. Loop cap: `loops.music`.

## Purpose

Produce the harmony (`chords.md`, Roman numerals plus concert pitch) and a single-voice melody
(`melody.abc`) that sit inside `structure.md` and the vocal range.

## Dispatch

| Item | Value |
|------|-------|
| Worker chain | agent `composer`: `harmony` (task `chords-melody`), then `melody` (Template 2) |
| Critic | agent `song-critic`, role `music-judge` (Template 3) |
| Inputs | `brief.md`, `structure.md`, `lyrics.md` (absent for INSTRUMENTAL) |
| Outputs | `chords.md`, `melody.abc` |
| Owners | `harmony` for `chords.md`, `melody` for `melody.abc` |

## Gates (both; PASS or SKIPPED each)

```text
chord_tools.py {dir}/chords.md {dir}/structure.md
abc_validate.py {dir}/melody.abc {dir}/structure.md {dir}/lyrics.md
```

Both scripts are not yet built (see `references/shared/stage-gates.md` section 7). Until they land
the orchestrator reports each as `SKIPPED (script absent)`, proceeds as PASS, and sets
`gates.music.skipped: true` with the reason in `state.json.notes`. Absent script is never FAIL.
INSTRUMENTAL runs `abc_validate.py` without `lyrics.md` (lyric alignment skipped).

## Loop

FAIL: dispatch `music-judge` with the gate JSON, re-dispatch `harmony` when `chord_tools.py` failed
and `melody` when only `abc_validate.py` failed (both when both failed); `loops_used.music += 1`.
A key or tempo disagreement between `harmony` and `melody` goes to the debate rubric in
`references/shared/stage-gates.md` section 6, decided by the orchestrator and logged in `decisions.md`.
At `loops.music` apply `escalation.on_loop_exhaustion`. A 7b BLOCKER naming `chords.md` or
`melody.abc` re-enters here and resets `loops_used.music` to 0.

## Per-type variations

| Type | Cell | Agent / role | Behaviour |
|------|------|--------------|-----------|
| FULL_SONG, INSTRUMENTAL, JINGLE | F | `composer` harmony then melody | Standard. INSTRUMENTAL: melody is the motif line, no `w:` lines |
| TOPLINE | L | `composer` `melody` only | Single dispatch; harmony is validated input, no `harmony` dispatch. The prompt points the `melody` role at the supplied progression in `brief.md` `## Supplied input`; its contract transcribes that progression into `chords.md` unchanged, then writes `melody.abc`. `chord_tools.py` validates `chords.md` as input |
| ADAPT_GENRE | I | agent `adapter`, role `music-adapter` | Source chords/melody are the input; one adapter dispatch re-voices them for `target_genre` (two genre files), gates validate the result. No critic loop. Needs `agents/adapter.md` (Wave 7) |
| LYRICS_ONLY, AUGMENT_LYRICS, REWRITE, THEORY | - | none | Skipped |
| REVISE | per request | `composer` harmony and/or melody | F scoped to the sections named when the request touches chords or melody; a key change re-runs this stage as F via `--consistency` |

## state.json after this stage

`stage`, `loops_used.music`, `gates.music`, `owners["chords.md"]`, `owners["melody.abc"]`, `updated`.
