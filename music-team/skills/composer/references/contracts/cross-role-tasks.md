---
loaded_by: composer
level: L2
last_reviewed: 2026-10-26
---

# Cross-Role Tasks

Composer roles never share a prompt: one role is one `Agent` call. A task that needs two roles is a sequence of calls, each with its own manifest and contract, run by the orchestrator (`music-flow`) in pipeline mode or by this skill in standalone mode. The earlier role's artifact path is passed to the later role as an input file; its contents are not pasted.

## Combination patterns

| Task | Sequence | Hand-off | Notes |
|------|----------|----------|-------|
| Full music stage (Stage 5) | `harmony` then `melody` | `chords.md` path to melody | Gates run once after the last role: `chord_tools.py`, then `abc_validate.py` |
| New song skeleton | `groove` then `harmony` then `melody` | `structure.md` to both | Stage 3, then Stage 5; lyrics are written between them |
| TOPLINE | `groove` (derive form from supplied chords), then `melody` only | supplied progression in `brief.md` `## Supplied input` | `melody` transcribes the progression into `chords.md` unchanged, then writes `melody.abc`; no `harmony` dispatch |
| Key change (REVISE) | `groove` updates `key`/`mode`, then `harmony`, then `melody` | new `structure.md` | Run `structure_check.py --consistency`; downstream stages re-run per `song-types.md` |
| Tempo or meter change | `groove` then `melody` | new `bpm` or `time_sig` | Harmony only if the meter change alters bars per section |
| Theory question that becomes a song task | `theorist` answer, then (on user request) `harmony` | user-confirmed progression | The theorist never writes the chart; the user confirms first |
| Reharmonize a finished section | `theorist` options, user picks, `harmony` (task `reharmonize-revise`), then `melody` check | chosen option text | Re-run `abc_validate.py`: new chords may need melody notes revised |

## Shared facts every role keeps identical

| Fact | Source of truth | Copied by |
|------|-----------------|-----------|
| key and mode | `structure.md` | `chords.md` header, `melody.abc` `K:` |
| bpm | `structure.md` | `melody.abc` `Q:1/4=<bpm>` |
| time signature | `structure.md` | `melody.abc` `M:` |
| section labels and order | `structure.md` | `chords.md` tags, `melody.abc` `%%section` |
| vocal range | `brief.md` or config `quality.vocal_range` | `melody` pitch choices |
| syllable stresses | `lyrics.md` and `structure.md` `meter_spec` | `melody` strong-beat placement |

A role that finds one of these facts wrong in its input does not fix the other role's artifact. It returns `STATUS: BLOCKED` with a `FINDINGS:` bullet naming the file and field.

## Disagreements

Key or tempo disagreement between `harmony` and `melody` goes to the orchestrator's debate rubric (`references/shared/stage-gates.md` section 6); each role states its position in the artifact notes and the orchestrator decides and logs it in `decisions.md`.

## Hand-off notes (pipeline summary field)

A role writes into `SUMMARY` only facts the next role needs, in one sentence of at most 200 characters: key and mode, whether any non-diatonic chord was used, the melody's range, whether a melisma was used.

## Boundaries with other skills

| Need | Goes to |
|------|---------|
| Lyric text, hook, rhyme | `lyricist` |
| Instrumentation, energy curve, production | `arranger` |
| Re-voicing a whole song for another genre | `adapter` (role `music-adapter`) |
| Judging a gate failure | `song-critic` (role `music-judge`) |
