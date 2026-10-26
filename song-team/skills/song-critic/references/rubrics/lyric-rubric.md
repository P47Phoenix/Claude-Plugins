---
loaded_by: prosody-judge
level: L3
last_reviewed: 2026-10-26
---

# Lyric Rubric

Five criteria, each scored 1-5. Anchors are given for 1, 3, and 5; score 2 and 4 when the lyric sits between anchors. The rubric informs the critique and sets revision priority. `prosody_check.py`, `rhyme_check.py`, and `cliche_scan.py` decide the gate; scores never alter `gate_status`.

## 1. Prosody fit

- **1**: stressed syllables land on articles, prepositions, or weak syllables in most lines; syllable counts drift from `meter_spec` by two or more.
- **3**: most lines fit the spec; one or two lines per section need a stress swap or a syllable trimmed.
- **5**: every line's natural speech stress matches the spec's `S` positions; syllable counts match exactly; the chorus is the cleanest section.

## 2. Rhyme craft

- **1**: scheme broken in more than one pair, or every rhyme is an identity rhyme or a forced inversion ("the night so dark").
- **3**: scheme satisfied; rhymes are predictable (fire/desire, heart/apart) but not forced.
- **5**: scheme satisfied with at least one fresh pair per section; word order stays natural; slant rhymes, where used, sit on the less important line.

## 3. Imagery and specificity

- **1**: abstractions throughout; no object, place, or action a listener pictures.
- **3**: one concrete image per section; verses tell rather than show in places.
- **5**: each verse carries a specific, sensory detail that advances the arc; the `central_image` from `concept.md` recurs with variation.

## 4. Narrative arc

- **1**: verses are interchangeable; nothing changes between verse 1 and verse 2; the bridge restates the chorus.
- **3**: verse 2 adds information; the bridge shifts angle but the ending is unresolved by accident.
- **5**: the song moves through `arc: [start, turn, end]` from `concept.md`; verse 2 earns the chorus differently; the bridge turns and the last chorus lands with new weight.

## 5. Voice and point of view

- **1**: pov drifts (I/you/they) without purpose; register clashes with `mood` or `audience`.
- **3**: pov stable; diction mostly consistent; one or two lines sound like a different speaker.
- **5**: one consistent speaker whose diction fits `brief.md` `pov`, `mood`, and `audience`; address (to whom the song speaks) is clear and stable.

## Scoring notes

- Score the lyric as written, not as it would read after revision.
- Prosody fit and rhyme craft reflect the gate; when they score 4 or 5 on a FAIL, say so under `## Suspected false positives` with the location.
- Total 10 or below on a PASS gate: recommend one optional quality loop; the orchestrator decides.
