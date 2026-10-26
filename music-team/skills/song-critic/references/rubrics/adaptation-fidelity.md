---
loaded_by: song-critic
level: L3
last_reviewed: 2026-10-26
---

# Rubric: adaptation fidelity (adaptation-fidelity)

Five criteria, 1-5 each. `adapt_check.py` decides the gate; this rubric judges substance.

| Criterion | 5 means | 1 means | Evidence to cite |
|-----------|---------|---------|------------------|
| Identity kept | Hook line, section order, title image, key relationships and cadence points survive | A listed identity element is gone or altered | `## Kept` bullet vs artifact |
| Change justification | Every change is in the table with a `Why` tied to the target genre profile | Changes with no row, or a `Why` of "style" | `## Changed` row vs artifact diff |
| Meaning preserved | Each adapted section says what its source says: image, speaker, stance, outcome | A section now argues something else | source section vs adapted section |
| Genre arrival | The result is idiomatic in the target genre: feel, harmony, arrangement | Source genre still dominant | target genre `## Harmony` and `## Rhythm` |
| Singability after re-fit | Meter and rhyme deltas in `## Lyric re-fit` are real and the lines scan | Re-fit claims do not match the lines | `## Lyric re-fit` vs `lyrics.md` |

## Finding tags

| Tag | Use when |
|-----|----------|
| `KEPT-BROKEN` | An element listed under `## Kept` is not preserved in the artifacts |
| `UNJUSTIFIED` | A `## Changed` row has a `Why` the target profile and the artifact notes do not support |
| `UNLISTED CHANGE` | Source and artifact differ in an element the report does not list |
| `DRIFT` | An adapted lyric section changes meaning, not just meter or wording |

## Reading the gate JSON

- `adapt_check.py` violations (missing disposition, empty cell, unresolved genre) are structure faults: one fix row each, naming the report section.
- A clean gate with low scores is still a critique: the rubric rows are the evidence.
- Fixes go to the artifact owner (`lyric-adapter` or `music-adapter`) and the report writer, never to the source.
