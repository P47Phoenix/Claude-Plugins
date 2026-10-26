---
loaded_by: music-flow
level: L2
last_reviewed: 2026-10-26
---

# Stage 4: Lyrics

Routing data: `stages.yml` key `04-lyrics`. Loop cap: `loops.lyrics`.

## Purpose

Write (or adapt, or extend, or edit) the lyric so it fits the `meter_spec` and `rhyme_scheme` in
`structure.md` and carries the Stage 2 hook.

## Dispatch

| Item | Value |
|------|-------|
| Worker chain | agent `lyricist`: `verse-writer` (task `section-lyrics`), then `lyric-editor` (Template 2) |
| Critic | agent `song-critic`, role `prosody-judge` (Template 3) |
| Inputs | `brief.md`, `concept.md`, `structure.md` |
| Output | `lyrics.md` |
| Owner | `verse-writer` / `lyric-editor` (record the last writer) |

## Gates (all three; PASS or SKIPPED each)

```text
prosody_check.py {dir}/lyrics.md {dir}/structure.md {dir}/brief.md
rhyme_check.py   {dir}/lyrics.md {dir}/structure.md
cliche_scan.py   {dir}/lyrics.md
```

Non-English `brief.md.language` makes `prosody_check.py` and `rhyme_check.py` return SKIPPED: proceed
as PASS, log `skipped: true`. Thresholds come from config (`prosody_tolerance`, `slant_rhyme_allowed`,
`cliche_max_per_100_words`).

When `quality.adversarial_lyrics: true`, after the gates pass dispatch the challenger (Template 1,
role `challenger`) on `lyrics.md` and run `challenge_gate.py`; a BLOCKER counts as a gate FAIL here.

## Loop

FAIL: dispatch `prosody-judge` with the combined gate JSON, re-dispatch the chain from `lyric-editor`
(`verse-writer` again only if the critique names missing sections); `loops_used.lyrics += 1`. At
`loops.lyrics`, apply `escalation.on_loop_exhaustion`. Re-entry from a 7b BLOCKER resets
`loops_used.lyrics` to 0.

## Per-type variations

| Type | Cell | Agent / role | Behaviour |
|------|------|--------------|-----------|
| FULL_SONG, LYRICS_ONLY, TOPLINE, JINGLE | F | `lyricist` verse-writer then lyric-editor | Standard loop |
| REWRITE | F | `lyricist` `lyric-editor` only | Originality check runs on the supplied input first (`cliche_scan.py` on the `## Supplied input` lyric; a recognised well-known lyric means stop and relay the refusal sentence). Original lines kept unless the brief asks to change them |
| ADAPT_GENRE | L | agent `adapter`, role `lyric-adapter` | Single dispatch, gates run, no critic loop. Prompt carries `source_genre` and `target_genre` (two genre files). Meter re-fit goes against `structure.md` from Stage 3. Requires `agents/adapter.md` (Wave 7); absent means `MISSING_AGENT` |
| AUGMENT_LYRICS | L | `lyricist` role `augmenter` | Single dispatch. New sections must match the source `meter_spec` and `rhyme_scheme`; gates scoped to the new sections plus `cliche_scan.py`. Original lines stay verbatim unless edits are requested. Prompt lists the sections to add; the rest is read-only context |
| INSTRUMENTAL, THEORY | - | none | Skipped |
| REVISE | per request | `lyricist` `lyric-editor` | F scoped to the sections named; other sections are read-only context; then `structure_check.py --consistency` |

On a gate FAIL at an `L` cell, apply escalation immediately (no critic dispatch, no re-dispatch loop),
except that `ask_user` may let the user supply guidance for one more attempt.

## state.json after this stage

`stage`, `loops_used.lyrics`, `gates.lyrics` (merged result of the three scripts: worst status wins,
`metrics` and `violations` concatenated), `owners["lyrics.md"]`, `accepted_best.lyrics` if used.
