---
loaded_by: song-critic
level: L3
last_reviewed: 2026-10-26
---

# Rubric: prosody (prosody-judge)

Five criteria, 1-5 each. `prosody_check.py`, `rhyme_check.py` and `cliche_scan.py` decide the gate.

| Criterion | 5 means | 1 means | Gate link |
|-----------|---------|---------|-----------|
| Stress alignment | Stressed syllables land on strong beats in every line | Many lines fight the meter | `prosody_tolerance`, mismatch ratio per section |
| Rhyme craft | Scheme matches `rhyme_scheme`; slant rhymes sound deliberate | Forced or missing rhymes | `rhyme_check` violations |
| Line length | Syllable counts match `meter_spec` within the tolerance | Lines vary wildly | `prosody_check` syllable counts |
| Freshness | Concrete, specific images; no stock phrases | Cliche runs | `cliche_max_per_100_words` |
| Section contrast | Verses advance; the chorus repeats and lifts | Sections read the same | none |

## Reading the gate JSON

- Each violation row has `location` (`Verse 2:3`), `observed` and `limit`. Turn every row into one fix: name the line, the offending stress or rhyme, and the move (reorder words, swap a synonym with the right stress, change the end word).
- Prefer fixes that touch one line. Ask for a section rewrite only when more than half its lines fail.
- Slant-rhyme allowance (`slant_rhyme_allowed`): if true, do not demand a perfect rhyme; if false, name the near-miss pair.
- Non-English lyrics: the gate may be SKIPPED; critique craft only and say the gate did not run.
- Suspected false positive (a word the dictionary scans differently in performance): one `FALSE-POSITIVE?` line, still list the fix.
