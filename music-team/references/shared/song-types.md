---
loaded_by: music-flow, music-brief
level: L1
last_reviewed: 2026-10-26
---

# Song Type Detection and Routing

> **Runtime detection is mandatory.** Song type is a per-run routing decision made in
> Stage 1 by `music-brief` from the brief text, and logged in `brief.md.song_type` and
> `state.json.song_type`. `routing.force_type` in `.song/config.yml` is the only
> supported pin: detection still runs and is logged, routing uses the pin, and a banner
> announces the override on every run. `REVISE` is detected only and cannot be forced.
>
> **This file is the single routing source.** `music-flow` and `music-brief` both derive
> from the matrix below; there is no second routing table anywhere in the plugin.
> `skills/music-brief/references/routing-matrix.md` (lands in W2-1) is a pointer to this file.

## Detection matrix

Classify every brief into exactly one type before Stage 2. When several match, the
first matching row in this order wins: PARODY_ADAPT, REVISE, THEORY, ADAPT_GENRE,
AUGMENT_LYRICS, REWRITE, TOPLINE, INSTRUMENTAL, JINGLE, LYRICS_ONLY, FULL_SONG.

### FULL_SONG

- **Signals**: default when nothing else matches; "write a song", "full song", "song from scratch", "compose a song"
- **Confidence boosters**: asks for melody, chords, or production; names a genre and mood
- **Confidence reducers**: any signal from the rows below

### LYRICS_ONLY

- **Signals**: "just lyrics", "words only", "lyrics for", "write the words", no chords, melody, or production mentioned
- **Confidence boosters**: user says they have a melody or will compose themselves
- **Confidence reducers**: "chords", "melody", "beat", "arrangement", "production"

### INSTRUMENTAL

- **Signals**: "instrumental", "no vocals", "beat", "theme music", "background music", "score cue"
- **Confidence boosters**: no theme stated as words to be sung; describes a scene or mood only
- **Confidence reducers**: "lyrics", "chorus lyrics", "sing"

### TOPLINE

- **Signals**: user supplies chords or a track; "write over this", "topline", "melody and words for these chords", "I have the progression"
- **Confidence boosters**: a chord chart or ABC is pasted or a file path is given
- **Confidence reducers**: nothing supplied
- **Requires**: `user_asserts_original_input: true` in `brief.md` (wizard asks once)

### THEORY

- **Signals**: "explain", "analyze this progression", "what mode is", "reharmonize", "what chords fit", "why does this cadence"; no song deliverable requested
- **Confidence boosters**: a progression, scale, or cadence is quoted; the request is a question
- **Confidence reducers**: a full song, lyric, or topline deliverable is requested (then fall through to the other rows)
- **Requires**: nothing

### ADAPT_GENRE

- **Signals**: "turn my <x> into <genre>", "convert to <genre>", "adapt this to <genre>", "make it bossa nova / blues / ..."; a lyric and/or chords supplied AND a target genre
- **Confidence boosters**: a lyric or chord chart is pasted; the target is a genre label
- **Confidence reducers**: no supplied source (then `FULL_SONG` in that genre); a named artist or song as target (routes to `PARODY_ADAPT` first)
- **Requires**: `user_asserts_original_input: true` OR `public_domain: true` (with `public_domain_source`) in `brief.md`; otherwise reply inline with the sentence under "PARODY_ADAPT refusal" and create no artifact. `target_genre` must be a genre label; `blocked-targets.txt` is checked against the target string

### AUGMENT_LYRICS

- **Signals**: "add a verse", "write a bridge for my song", "extend", "one more chorus", "more verses in the same voice", "pre-chorus for this"; a lyric supplied
- **Confidence boosters**: a lyric is pasted or a file path is given; a section to add is named
- **Confidence reducers**: only "fix", "tighten", or "polish" with no new material (then `REWRITE`)
- **Requires**: same provenance as `ADAPT_GENRE`; `target_genre` optional and defaults to the source's

### REWRITE

- **Signals**: user supplies an original lyric; "fix", "tighten", "second draft", "rewrite my lyric", "polish these words"
- **Confidence boosters**: a lyric is pasted or a file path is given
- **Confidence reducers**: the supplied text is a well-known existing lyric (then clause 4 of the originality policy applies and the challenger blocks)
- **Requires**: `user_asserts_original_input: true`; the originality check runs on the input first

### JINGLE

- **Signals**: "jingle", "ad", "advert", "commercial", "30 seconds", "15 seconds", a brand or product name present
- **Confidence boosters**: a tagline or slogan is given; `target_length_sec <= 60`
- **Confidence reducers**: "album", "three minutes", "verse two"

### REVISE

- **Signals**: an existing `.song/<slug>/state.json` with `status: complete` plus a change request: "make the chorus punchier", "slower bridge", "change the key", "swap verse two"
- **Confidence boosters**: `.song/active` names the slug; the request names a section or artifact
- **Confidence reducers**: no prior run exists (then classify by the other rows)

### PARODY_ADAPT

- **Signals**: "parody", "to the tune of", "in the style of <named song or artist>", "like <artist>'s song", a `blocked-targets.txt` entry used as the target
- **Not a signal**: "in the style of <genre>" (for example "in the style of 80s synth-pop") routes to `FULL_SONG`
- **Outcome**: refused; see below

## Routing matrix

Legend: **F** full stage with loops · **L** light (single dispatch, gate still runs, no critic loop) · **I** input (artifact supplied by user, validated not generated) · **-** skipped.

| Type | Signals | 1 Brief | 2 Concept | 3 Structure | 4 Lyrics | 5 Music | 6 Arrangement | 7 Release | Notes |
|------|---------|---|---|---|---|---|---|---|-------|
| `FULL_SONG` | default | F | F | F | F | F | F | F | |
| `LYRICS_ONLY` | "just lyrics", "words only", no chords/melody mentioned | F | F | L | F | - | - | L | Stage 3 still produces the meter spec that Stage 4 gates need; Release packages lyric sheet only |
| `INSTRUMENTAL` | "instrumental", "no vocals", "beat", "theme music" | F | L | F | - | F | F | F | Concept produces a *motif* description instead of a hook; `abc_validate.py` skips lyric alignment |
| `TOPLINE` | user supplies chords or a track; "write over this", "topline" | F | F | I | F | L | - | L | Stage 3 derives form and meter spec from the supplied chords; Stage 5 runs melody role only, harmony is validated input |
| `THEORY` | "explain", "analyze this progression", "what mode is", "reharmonize", "what chords fit"; no song deliverable | F | - | - | - | - | - | - | Single dispatch to `composer` role `theorist`; answer returned inline; no `.song/<slug>/` directory unless the user asks to save |
| `ADAPT_GENRE` | "turn my <x> into <genre>", "convert to <genre>", supplied lyric/chords + target genre | F | I | I | L | I | I | F | Stage 3 infers meter from the source; Stages 4-6 run through the `adapter` skill (`lyric-adapter`, `music-adapter`) with `source_genre` and `target_genre` profiles; Stage 7 requires `adaptation-report.md` (kept vs changed) |
| `AUGMENT_LYRICS` | "add a verse", "write a bridge for my song", "extend", "one more chorus" with a supplied lyric | F | I | I | L | - | - | L | Stage 4 runs `lyricist` role `augmenter` only; new sections match the source `meter_spec`/rhyme scheme (`prosody_check` + `rhyme_check` gate them); original lines kept verbatim unless edits are requested |
| `REWRITE` | user supplies an original lyric; "fix", "tighten", "second draft" | F | - | L | F | - | - | L | Stage 3 infers the meter spec from the input lyric; Stage 4 runs lyric-editor only; originality check runs on the input first |
| `JINGLE` | "jingle", "ad", "30 seconds", brand name present | F | F | F | F | F | L | F | Hard length cap; form template `jingle` |
| `REVISE` | existing `.song/<slug>/state.json` and "make the chorus punchier", "slower bridge", "change the key" | - | per request | per request | per request | per request | per request | F | Re-enters at the earliest stage the request touches; downstream stages re-run as L unless their artifact is invalidated by `structure_check.py --consistency` |
| `PARODY_ADAPT` | "parody", "to the tune of", "in the style of <named song or artist>" | refused | | | | | | | One-sentence refusal plus an offer to write an original on the same theme; no `.song/<slug>/` directory is created. See `originality-policy.md`. "In the style of <genre>" is fine and routes to `FULL_SONG` |

## Quick mode

`quick: true` in config, or the phrase "quick song", caps every stage loop at 1, sets `on_loop_exhaustion: accept_best`, and limits the wizard to the questions the brief leaves unanswered (max 2). Time-to-first-song is then bounded by one dispatch per stage. Quick mode changes loop depth only; it never changes which stages the matrix runs.

## REVISE re-entry rules

1. A REVISE run gets a new `run_id`; `state.json.stage` is set to the re-entry stage and `loops_used` is reset for that stage and every downstream stage. `.song/active` is rewritten to the slug.
2. Re-entry stage is the earliest stage the request touches, by artifact: `concept.md` -> 2; `structure.md` (form, bars, tempo, key, time sig, meter) -> 3; `lyrics.md` -> 4; `chords.md` or `melody.abc` -> 5; `arrangement.md` or `production-brief.md` -> 6; a request touching only release packaging -> 7.
3. The re-entered stage runs as F, scoped to the sections the request names (the worker prompt lists them; other sections are supplied as read-only context).
4. After the re-entered stage passes, `structure_check.py --consistency` runs over all present artifacts. Each downstream stage whose artifact appears in a violation re-runs as F; every other downstream stage re-runs as L. Stage 7 always runs as F.
5. Examples: "make the chorus punchier" -> Stage 4 (chorus only) then 5, 6 as L and 7 as F; "change the key" -> Stage 3 (key field) then 5 as F (consistency invalidates `chords.md` and `melody.abc`), 6 as F if the arrangement header disagrees, 7 as F.
6. If no finished run exists, the request is not REVISE; classify by the remaining rows.

## PARODY_ADAPT refusal

`music-brief` (also for `ADAPT_GENRE`/`AUGMENT_LYRICS` without a provenance flag) replies inline with exactly one sentence of explanation and one offer, then stops:

> I cannot write a parody of, or a song to the tune of or in the exact style of, a named existing song or artist; I would be glad to write an original song on the same theme and in the same genre instead.

No `.song/<slug>/` directory is created, `.song/active` is not written, and no stage runs. If the user accepts the offer, the next brief is classified afresh from the top of the matrix.
