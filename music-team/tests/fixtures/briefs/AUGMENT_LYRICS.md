---
theme: a lighthouse keeper's last winter
pov: first person
audience: adults
genre: folk
mood: reflective
language: en
target_length_sec: 200
must_include: []
must_avoid: []
song_type: AUGMENT_LYRICS
user_asserts_original_input: false
public_domain: true
public_domain_source: traditional folk verse, anonymous, collected before 1900
---

## Request

Write a bridge for my song and add one more verse in the same voice. The two verses below are a public-domain traditional text I am building on.

## Brief

A lyric is supplied and the user asks for new material ("write a bridge", "one more verse", "in the same voice"), so the AUGMENT_LYRICS row applies. Provenance is satisfied by `public_domain: true` with a `public_domain_source`, a second path alongside `user_asserts_original_input`. Stage 4 runs `lyricist` role `augmenter` only; the new sections match the source meter and rhyme and the supplied lines are kept verbatim.

## Supplied input

```text
[Verse 1]
The lamp is trimmed and the oil is low
The winter wind has a long way to go
I climb the stair with a steady hand
And watch for ships that will not land

[Verse 2]
The glass is clear and the night is wide
The sea lies still on the turning tide
I keep the light for the ones at sea
And the sea keeps no light for me
```
