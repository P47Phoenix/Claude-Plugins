---
loaded_by: structure-judge
level: L3
last_reviewed: 2026-10-26
---

# Structure Rubric (Stage 3)

Five criteria, each scored 1-5. Anchors are given for 1, 3, and 5; score 2 and 4 when the form sits between anchors. The rubric informs the critique and sets revision priority. `structure_check.py` decides the gate; scores never alter `gate_status`. The Stage 6 arrangement rubric is a separate file (`arrangement-rubric.md`).

## 1. Template compliance

- **1**: label sequence diverges from `form_template` at the first required section, or a section's bars fall outside the template range.
- **3**: sequence matches; one optional section is placed oddly (post-chorus before chorus) or bars sit at an extreme of the range.
- **5**: sequence and bar counts match the template exactly as `techniques/form-templates.md` describes; optional sections are used only where the brief justifies them.

## 2. Length fit

- **1**: computed duration (total bars x beats x 60 / bpm) differs from `brief.md.target_length_sec` by more than 40 percent.
- **3**: within 20 percent.
- **5**: within 10 percent, and the chorus first arrives before 60 seconds for `FULL_SONG` pop, country, and jingle types.

## 3. Meter spec quality

- **1**: `meter_spec` empty for lyric sections, or stress patterns impossible to sing at `bpm` (every syllable stressed, or 12+ syllables in a 4/4 bar at a fast tempo).
- **3**: specs present and singable; chorus and verse specs are identical, giving the lyricist no contrast.
- **5**: verse specs run longer and lighter (`uSuS...`), chorus specs shorter and front-stressed (`SuSu...`); line counts match the bar counts (one line per two bars at moderate tempo).

## 4. Rhyme scheme fit

- **1**: scheme length differs from the meter line count, or every section uses the same scheme.
- **3**: schemes valid; verses and chorus share one scheme.
- **5**: schemes valid, scoped per section, with `x` used deliberately on lines meant to carry image over rhyme; chorus scheme is tighter than the verse scheme.

## 5. Tempo and key sanity

- **1**: `bpm` outside the template's tempo band and the genre's band; `time_sig` contradicts the feel the brief asks for.
- **3**: inside the template band; `key` is the default C with no reason recorded.
- **5**: `bpm` inside both bands and near the genre's centre; `time_sig` fits the mood; key and mode are chosen for the stated vocal range or mood.

## Scoring notes

- Score the structure as written.
- Criterion 1 reflects the gate; a 4 or 5 on a FAIL is a `## Suspected false positives` candidate (name the label the regex rejected).
- Total 10 or below on a PASS gate: recommend one optional quality loop before Stage 4; the orchestrator decides.
