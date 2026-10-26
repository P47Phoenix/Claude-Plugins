---
loaded_by: song-critic
level: L3
last_reviewed: 2026-10-26
---

# Rubric: structure (structure-judge)

Five criteria, 1-5 each. `structure_check.py` (Stage 3), `arrangement_check.py` and
`structure_check.py --consistency` (Stage 6) decide the gate.

| Criterion | 5 means | 1 means | Gate link |
|-----------|---------|---------|-----------|
| Form logic | Section order serves the story; the hook arrives early and returns | Sections in arbitrary order | `structure_check` form rules |
| Length fit | Total bars and seconds match `target_length_sec` | Far over or under | length metrics |
| Energy arc | Verses sit below the next chorus; the peak is the last chorus or the bridge | Flat or inverted curve | `energy_curve`, `arrangement_check` |
| Section contrast | Instruments and texture change at section edges | Adjacent sections identical | instruments in/out rows |
| Cross-file consistency | Labels, key, bpm and time signature agree in every artifact | Drift between files | `--consistency` violations |

## Reading the gate JSON

- Missing or extra section: say which label differs and which file is wrong (the owning role of that file fixes it).
- Energy rows: give the section, the current value, and the direction to move; keep the range (max minus min) at least 3.
- Consistency violations: name the two files and the key that differs; the earlier stage's file is the source of truth unless the critique says otherwise.
- Never suggest editing `structure.md` from a Stage 6 critique unless a Stage 3 gate also failed.
