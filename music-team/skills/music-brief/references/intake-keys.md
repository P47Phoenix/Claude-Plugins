---
loaded_by: music-brief
level: L2
last_reviewed: 2026-10-26
---

# Intake Keys per Song Type

Source of truth for key meanings is `references/shared/artifact-formats.md` (`brief.md`). This file
says which keys each song type needs, so the wizard asks only what is missing. Detection rules and
priority order live in `references/shared/song-types.md`; this file never restates them.

## Key glossary

| Key | Type | Ask as |
|-----|------|--------|
| `theme` | string, required, non-empty | "What is the song about?" |
| `genre` | genre label | "What genre?" (fallback `routing.default_genre`) |
| `mood` | string | "What mood?" |
| `pov` | string | infer: first person unless stated |
| `audience` | string | "Who is it for?" |
| `target_length_sec` | integer | "About how long?" (default 180; JINGLE 15-60) |
| `language` | ISO 639-1 | infer from the request; default `routing.default_language` |
| `must_include[]`, `must_avoid[]` | lists | "Anything it must include or avoid?" (last question) |
| `user_asserts_original_input` | boolean | provenance question, below |
| `public_domain`, `public_domain_source` | boolean, free text | provenance question, below |
| `source_genre`, `target_genre` | genre labels | never an artist or song name |
| `## Supplied input` | fenced body | the user's pasted lyric or chords, stored verbatim |

## Required keys per type

`R` required (ask if missing), `I` infer silently when missing, `-` not used. `theme` is required
for every type that writes a brief.

| Type | theme | genre | mood | audience | length | provenance | source/target genre | Supplied input |
|------|-------|-------|------|----------|--------|------------|---------------------|----------------|
| FULL_SONG | R | R | R | I | I | - | - | - |
| LYRICS_ONLY | R | R | R | I | I | - | - | - |
| INSTRUMENTAL | R (scene or mood) | R | R | I | I | - | - | - |
| JINGLE | R (brand/product) | R | R | I | R (<=60) | - | - | - |
| TOPLINE | R | R | I | I | I | R original | - | R (chords) |
| REWRITE | I (from lyric) | I | I | I | I | R original | - | R (lyric) |
| ADAPT_GENRE | I (from source) | I (= target) | I | I | I | R original or public domain | R both | R (lyric and/or chords) |
| AUGMENT_LYRICS | I (from source) | I (= source) | I | I | I | R original or public domain | target optional | R (lyric) |
| THEORY | - | - | - | - | - | - | - | quoted progression, inline |
| REVISE | - | - | - | - | - | - | - | none; reads existing brief |
| PARODY_ADAPT | refused: ask nothing, write nothing | | | | | | | |

`I` means: derive from the request or supplied input; record the inferred value; do not ask.
`genre` for ADAPT_GENRE is set to `target_genre`; for AUGMENT_LYRICS to `source_genre` unless
`target_genre` is given.

## Provenance question (ADAPT_GENRE, AUGMENT_LYRICS, and the TOPLINE / REWRITE flag)

Ask once, in one turn: "Is this your own original work, or is it in the public domain?"

| Answer | Record in `brief.md` |
|--------|----------------------|
| Own work | `user_asserts_original_input: true`, `public_domain: false` |
| Public domain | `public_domain: true`, `public_domain_source: <where it is documented>`, `user_asserts_original_input: false` |
| Neither, unsure, or a published song | Refuse with the sentence from `song-types.md`; write nothing |
| Already stated in the request ("my song", "my lyric") | Do not re-ask; record `user_asserts_original_input: true` |

TOPLINE and REWRITE accept only "own work" (the public-domain flag is not defined for them).
A bare assertion does not override clause 4: a recognised well-known lyric is still blocked later by
the challenger.

## Wizard order and budget

Ask in this order, skipping anything already known: provenance (when required), genre, mood,
theme, audience, length, anything to avoid. Maximum 3 questions per turn. Quick mode (`quick: true`
or "quick song") asks at most 2 questions in total, taking the first unanswered ones in order, and
infers the rest.

## Target-genre check (ADAPT_GENRE)

`target_genre` must be a genre label (`bossa nova`, `blues`, `country`). If the value names an
artist, band, or song, or matches an entry in `references/shared/blocked-targets.txt`, treat the
request as `PARODY_ADAPT` and refuse. "In the style of 80s synth-pop" is a genre and is fine.

## Declaration line

Always end with: `Type: <T> | Genre: <g> | Provenance: <original | public-domain | n/a> | Brief: <path | none>`.
