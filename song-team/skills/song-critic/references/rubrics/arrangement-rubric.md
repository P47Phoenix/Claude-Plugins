---
loaded_by: structure-judge
level: L3
last_reviewed: 2026-10-26
---

# Arrangement Rubric (Stage 6)

Five criteria, each scored 1-5. Anchors are given for 1, 3, and 5; score 2 and 4 when the arrangement sits between anchors. The rubric informs the critique and sets revision priority. `arrangement_check.py` and `structure_check.py --consistency` decide the gate; scores never alter `gate_status`. Metrics referenced: `arrangement_check` `sections`, `global_max`, `chorus_count`, `no_chorus`; `structure_check` `artifacts_compared`, `melody_min_pitch`, `melody_max_pitch`.

## 1. Energy curve

- **1**: the curve fails `energy_curve` (a later chorus lower than an earlier one, the peak in a verse, a verse at or above the following chorus), or every section shares one value.
- **3**: the curve passes; choruses step up by one each time and the bridge sits at the same value as a verse, so the final lift is small.
- **5**: choruses rise with the largest step into the final chorus; the bridge drops at least two below the preceding chorus to make room; the outro (if any) falls away; `global_max` sits on the last chorus.

## 2. Section contrast

- **1**: `instruments_in` and `instruments_out` are `-` at most boundaries; the listener cannot tell sections apart by texture.
- **3**: every chorus adds something; verses change nothing after Verse 1; the bridge removes nothing.
- **5**: every section boundary changes at least one instrument in or out; Verse 2 differs from Verse 1 by one element; the bridge strips to two or three voices; each chorus adds one element the previous chorus lacked.

## 3. Hook support

- **1**: the chorus texture buries the vocal (the `texture_note` names more than three new elements at once) or the hook line gets no doubling, harmony, or space.
- **3**: the chorus is wider than the verse, but each chorus is treated identically.
- **5**: the hook line is the clearest moment in each chorus (doubles, a harmony line, or a drop-out before it); the final chorus adds the gang or harmony vocal; the first chorus leaves room for the second to grow.

## 4. Consistency with earlier stages

- **1**: `--consistency` reports a differing `key`, `mode`, `bpm`, `time_sig`, or section list; or the arrangement asks for a vocal moment outside `melody_min_pitch`..`melody_max_pitch`.
- **3**: fields agree; the texture notes ignore what the melody does (a "wide, doubled" chorus under a melody that sits in the bottom of the range).
- **5**: fields agree; instrument choices follow the chord chart's register (bass under a low melody, pad above a high one); the `texture_note` for each section names the melodic peak or the lyric turn it supports.

## 5. Texture-note consistency

- **1**: `texture_note` cells are empty or `-` in most rows, or a note contradicts its own row (a "stripped" note on a section whose `instruments_in` adds three parts).
- **3**: every row has a note, but the notes describe instruments already listed in the row without saying what the texture does for the section.
- **5**: every `texture_note` names one job (space, width, drive, lift) in technical terms, agrees with the row's energy and instrument changes, and no two adjacent sections carry the same note.

## Scoring notes

- Score `arrangement.md` only, as written; the melody and chords are closed. `production-brief.md` is never read here; the challenger owns it at Stage 7b.
- Criteria 1 and 4 reflect the gate; a 4 or 5 on a FAIL is a `## Suspected false positives` candidate (name the section row).
- Criterion 5 at 1 is a craft finding at `rubric:sections` for the `dynamics` role even when the gate passed.
- Total 10 or below on a PASS gate: recommend one optional quality loop before Stage 7; the orchestrator decides.
