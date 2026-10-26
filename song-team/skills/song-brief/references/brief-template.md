---
loaded_by: song-brief
level: L2
last_reviewed: 2026-10-26
---

# brief.md Template

Path: `.song/<slug>/brief.md`. Owner: `song-brief`. Key list is defined in
`references/shared/artifact-formats.md`; this file shows the complete shape with every
key present, then one example filled from the plan's Appendix A walkthrough.

## Template (every key, in this order)

````markdown
---
theme: <required; one lower-case phrase; the only key that is never defaulted>
pov: <first person | second person | third person | brand voice | none>
audience: <short noun phrase>
genre: <lower-case, hyphenated; matches a genres/<genre>.md name where one exists>
mood: <one or two lower-case words>
language: <ISO 639-1 code, e.g. en>
target_length_sec: <integer>
must_include: [<item>, <item>]
must_avoid: [<item>, <item>]
song_type: <FULL_SONG | LYRICS_ONLY | INSTRUMENTAL | TOPLINE | REWRITE | JINGLE | REVISE>
user_asserts_original_input: <true | false>
---

## Brief

<One paragraph: what is asked, what the user supplied, the tone, and the detection
signal that chose song_type. No artist names, no quoted existing lyrics.>

## Supplied input

```text
<TOPLINE: the chord chart or ABC exactly as supplied.
 REWRITE: the lyric exactly as supplied, section tags included.
 Omit this section entirely for every other song type.>
```
````

Rules that the template does not show:

- Empty lists are written `[]`, never omitted.
- `user_asserts_original_input` is `true` only for `TOPLINE` and `REWRITE` after the user
  answers "yes"; it is `false` for every other type.
- `PARODY_ADAPT` never produces this file.
- Items containing a colon, comma, or quotation mark are double-quoted in the YAML list.

## Example: Appendix A walkthrough

Request: "Write me an upbeat indie-pop song about moving to a new city and not knowing
anyone yet." Default (full) mode, not quick mode: the wizard inferred genre `pop` (sub-tag
`indie`), mood `upbeat`, and theme, then asked the three remaining questions (audience,
length, anything-to-avoid). In quick mode it would have asked audience and length only
and defaulted the rest. Detected `FULL_SONG`. Slug derived from
theme: `moving-to-a-new-city-and-knowing-no-one` (40-character cut at a word boundary).

```markdown
---
theme: moving to a new city and knowing no one yet
pov: first person
audience: 20s-30s
genre: pop
mood: upbeat
language: en
target_length_sec: 180
must_include: []
must_avoid: [specific city names]
song_type: FULL_SONG
user_asserts_original_input: false
---

## Brief

A full song from scratch in indie-flavoured pop: the request names a genre and a mood,
asks for nothing less than a complete song, and supplies no lyric or chords of its own,
so it routes to the default FULL_SONG row. The narrator has just arrived, has a key and a
map but nobody who says their name yet; the tone is hopeful rather than lonely, and the
user asked that no real city be named.
```

## Per-type variations

| song_type | pov default | target_length_sec default | Supplied input | Notes |
|-----------|-------------|---------------------------|----------------|-------|
| FULL_SONG | first person | 180 | no | default row |
| LYRICS_ONLY | first person | 180 | no | body notes that the user has or will write the melody |
| INSTRUMENTAL | none | 180 | no | theme describes a scene or feeling, not words to sing; `must_avoid` carries `vocals` |
| TOPLINE | first person | 180 | yes: chord chart or ABC | `user_asserts_original_input: true` required |
| REWRITE | as the supplied lyric | 180 | yes: the lyric | `user_asserts_original_input: true` required; theme taken from the lyric |
| JINGLE | brand voice | 30 | no | brand name and tagline in `must_include`; competitor names in `must_avoid` |
| REVISE | copied from the finished run | copied | no | front-matter copied from the prior brief; `## Brief` holds the change request only |

## Validation (Stage 1 gate, performed by song-brief before returning)

1. `theme` present and non-empty.
2. `song_type` is one of the seven writable values above.
3. `language` is a two-letter ISO 639-1 code.
4. `target_length_sec` is an integer; for `JINGLE` it is 60 or less.
5. `user_asserts_original_input` is `true` when `song_type` is `TOPLINE` or `REWRITE`, and
   `## Supplied input` is present and non-empty for those two types.
6. No entry from `references/shared/blocked-targets.txt` appears anywhere in the file.

Any miss is fixed and the file rewritten before the hand-off; `song-flow` re-checks items
1, 2, and 3 before writing `state.json`.
