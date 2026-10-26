---
loaded_by: song-critic
level: L3
last_reviewed: 2026-10-26
---

# Rubric: hook (hook-judge)

Five criteria, 1-5 each. Scores inform the critique; `cliche_scan.py` and `prosody_check.py --hook` decide the gate.

| Criterion | 5 means | 1 means | Gate link |
|-----------|---------|---------|-----------|
| Memorability | The hook line stands alone and is repeatable after one read | Needs the verses to make sense | `hook_max_syllables` |
| Image specificity | One concrete object, place or action carries the theme | Abstract feeling words only | `cliche_scan` hits |
| Singable shape | Stressed first and last word, natural speech rhythm | Awkward stress or tongue-twisting cluster | `prosody_check --hook` |
| Title fit | Title is the hook or its key phrase | Title unrelated to the hook | none |
| Brief fidelity | Honours `must_include`, `must_avoid`, POV and language | Ignores a brief constraint | none |

## Reading the gate JSON

- `metrics.per_100_words` above the limit: name the phrase and propose a concrete image from the brief to replace it.
- A hook over the syllable limit: say which words to cut first (modifiers before nouns) and keep the final stressed word.
- Hook score below 3 on Memorability: ask for one candidate with a withheld or twisted last word.
- `INSTRUMENTAL`: judge the `motif` description for contour and repetition instead of words.
