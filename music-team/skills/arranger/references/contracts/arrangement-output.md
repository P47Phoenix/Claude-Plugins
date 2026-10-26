---
loaded_by: arranger
level: L2
last_reviewed: 2026-10-26
---

# Output Contract: arrangement.md

Owner: `dynamics` (the `instrumentation` task writes the first draft). Validated by
`arrangement_check.py` and `structure_check.py --consistency`. Grammar source of truth:
`references/shared/artifact-formats.md`.

## File shape

A header of four `key: value` lines, a blank line, then one pipe table with exactly these columns:

```text
key: D
mode: major
bpm: 118
time_sig: 4/4

| section | energy | instruments_in | instruments_out | texture_note |
|---------|--------|----------------|-----------------|--------------|
| Verse 1 | 3 | acoustic guitar, bass | - | sparse, dry vocal |
| Chorus | 7 | drums, synth pad | - | wide, doubled vocal |
```

## Rules

| Item | Rule |
|------|------|
| Header | `key`, `mode`, `bpm`, `time_sig` identical to `structure.md` (consistency gate) |
| Rows | One per section of `structure.md`, same labels, same order, repeats included |
| `energy` | Integer 1-10 per section; relative loudness, density, and intensity of the whole band |
| Energy map | Range (max minus min) at least 3; choruses never fall below the previous chorus; every verse is below the next chorus; the peak is the final chorus or the bridge |
| `instruments_in` | Comma-separated list of what enters at the section start; never empty. `-` only after the first section |
| `instruments_out` | Comma-separated list of what leaves; `-` when nothing leaves; never empty |
| `texture_note` | One short phrase: density, register, stereo width, vocal layering, or rhythmic feel. Technical words only |
| Forbidden text | "sounds like", "reference track", any artist, band, album, or song name (`blocked-targets.txt`) |

## Per-section content

Each row answers four questions: what plays (cumulative instruments after in/out), how full it is
(`energy`), how wide or dry it sounds (`texture_note`), and how the vocal is treated (single, double,
stacked, stripped; state it in `texture_note` when it changes).

## Song-type variations

| Type | Variation |
|------|-----------|
| FULL_SONG | Standard |
| INSTRUMENTAL | Energy curve built from the motif; the lead instrument replaces the vocal in `texture_note` |
| JINGLE | Few sections; the min energy range still applies; stay inside `target_length_sec` |
| REVISE | Edit only the rows the change request names; keep the rest byte-identical |

## Hand-back

`ARTIFACT:` the path of `arrangement.md`. `SUMMARY:` one sentence naming the peak section and the
energy range, 200 characters or fewer. Run `arrangement_check.py` before replying; report BLOCKED with
`FINDINGS:` when a violation cannot be fixed without changing `structure.md`.
