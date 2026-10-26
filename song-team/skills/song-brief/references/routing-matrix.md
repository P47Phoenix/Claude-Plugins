---
loaded_by: song-brief
level: L2
last_reviewed: 2026-10-26
---

# Routing Matrix (pointer)

**The single routing source is `references/shared/song-types.md`.** This file is a
pointer plus a compact copy of its signal table for L2 loading; it adds no rows, no
signals, and no precedence of its own. When the two disagree, `song-types.md` wins and
this file is the one to fix.

## Precedence

When several rows match, the first matching row in this order wins:
`PARODY_ADAPT`, `REVISE`, `REWRITE`, `TOPLINE`, `INSTRUMENTAL`, `JINGLE`, `LYRICS_ONLY`,
`FULL_SONG`.

## Signal table (copied from song-types.md)

| Order | Type | Signals | Not a signal / reducers | Requires |
|-------|------|---------|-------------------------|----------|
| 1 | `PARODY_ADAPT` | "parody", "to the tune of", "in the style of <named song or artist>", "like <artist>'s song", a `blocked-targets.txt` entry as target | "in the style of <genre>" routes to `FULL_SONG` | refused inline; no `.song/<slug>/`, no `.song/active` |
| 2 | `REVISE` | existing `.song/<slug>/state.json` with `status: complete` plus a change request ("make the chorus punchier", "slower bridge", "change the key", "swap verse two") | no prior finished run: classify by the remaining rows | detected only; never forced |
| 3 | `REWRITE` | user supplies an original lyric; "fix", "tighten", "second draft", "rewrite my lyric", "polish these words" | supplied text is a well-known existing lyric (challenger blocks) | `user_asserts_original_input: true` |
| 4 | `TOPLINE` | user supplies chords or a track; "write over this", "topline", "melody and words for these chords", "I have the progression" | nothing supplied | `user_asserts_original_input: true` |
| 5 | `INSTRUMENTAL` | "instrumental", "no vocals", "beat", "theme music", "background music", "score cue" | "lyrics", "chorus lyrics", "sing" | - |
| 6 | `JINGLE` | "jingle", "ad", "advert", "commercial", "30 seconds", "15 seconds", a brand or product name | "album", "three minutes", "verse two" | `target_length_sec <= 60` |
| 7 | `LYRICS_ONLY` | "just lyrics", "words only", "lyrics for", "write the words"; no chords, melody, or production mentioned | "chords", "melody", "beat", "arrangement", "production" | - |
| 8 | `FULL_SONG` | default; "write a song", "full song", "song from scratch", "compose a song"; asks for melody, chords, or production | any signal from rows 1-7 | - |

## Stage routing (what song-flow does with the result)

Legend: F full · L light · I input · - skipped.

| Type | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|------|---|---|---|---|---|---|---|
| `FULL_SONG` | F | F | F | F | F | F | F |
| `LYRICS_ONLY` | F | F | L | F | - | - | L |
| `INSTRUMENTAL` | F | L | F | - | F | F | F |
| `TOPLINE` | F | F | I | F | L | - | L |
| `REWRITE` | F | - | L | F | - | - | L |
| `JINGLE` | F | F | F | F | F | L | F |
| `REVISE` | - | per request | per request | per request | per request | per request | F |
| `PARODY_ADAPT` | refused | | | | | | |

Refusal sentence, REVISE re-entry rules, and quick-mode semantics: see `song-types.md`.
