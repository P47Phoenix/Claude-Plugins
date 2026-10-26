---
theme: a slow song about waiting for a late ferry
pov: first person
audience: adults
genre: bossa nova
mood: wistful
language: en
target_length_sec: 180
must_include: []
must_avoid: []
song_type: ADAPT_GENRE
user_asserts_original_input: true
source_genre: folk
target_genre: bossa nova
---

## Request

Turn my slow folk ballad about the late ferry into a bossa nova. It is my own lyric and my own chords; keep the words as close as the new groove allows.

## Brief

The user supplies their own lyric and chords and asks to convert them to a target genre ("turn my ... into", a genre label), so the ADAPT_GENRE row applies. Provenance is satisfied by `user_asserts_original_input: true`. The target is a genre label, not a named artist or song. Stage 3 infers meter from the source and Stages 4-6 run through the `adapter` skill; Stage 7 needs `adaptation-report.md`.

## Supplied input

```text
key: G minor, 3/4, 72 bpm

[Verse 1]
The ferry is late and the harbor is grey
I count the gulls as they drift away
My coat is damp and my coffee is cold
The timetable lied but the tide is old

[Chorus]
Wait for the horn and wait for the light
Everyone gets across tonight

| Gm | Cm | D7 | Gm |
```
