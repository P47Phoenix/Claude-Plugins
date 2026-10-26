---
loaded_by: adapter
level: L2
last_reviewed: 2026-10-26
---

# Cross-Role Tasks

How the two adapter roles combine. One role is one `Agent` call; the orchestrator (`music-flow`) or this
skill (standalone) sequences them. A role never calls the other.

## Combination patterns

| Supplied input | Sequence | Artifacts |
|---|---|---|
| Lyric only | `lyric-adapter` (`lyric-adapt`), then `adaptation-report` | `lyrics.md`, `adaptation-report.md` |
| Chords and/or melody only | `music-adapter` (`music-adapt`), optionally `arrangement-adapt`, then `adaptation-report` | `chords.md` (+ `melody.abc`), `arrangement.md`, `adaptation-report.md` |
| Lyric and chords/melody | `lyric-adapter`, then `music-adapter` (`music-adapt`), then `music-adapter` (`arrangement-adapt`), then `adaptation-report` | all of the above |

In the pipeline these map to stages 4, 5, 6 and 7p of `stages.yml` (`type_variants.ADAPT_GENRE`). Standalone,
run the same order yourself and stop after the last role the input needs.

## Order and why

1. **Lyric first.** The lyric is fitted to the meter in `structure.md`; the chords and melody are then fitted
   to the adapted lyric, not the other way round.
2. **Music second.** `music-adapt` reads the adapted `lyrics.md` and `structure.md`. It may not edit them.
3. **Arrangement third.** `arrangement-adapt` reads `chords.md`, `melody.abc` (if any) and `structure.md`.
4. **Report last.** `adaptation-report` reads the notes blocks of the artifacts that exist. A missing block is a
   `BLOCKED` finding for that artifact's role, not something to invent.

## Hand-offs

| From | To | Passed as |
|---|---|---|
| lyric-adapter | music-adapter | path to `lyrics.md`; its `# Risks:` lines about stressed beats |
| music-adapter (`music-adapt`) | music-adapter (`arrangement-adapt`) | paths to `chords.md`, `melody.abc` |
| every role | `adaptation-report` | paths to the artifacts; the notes blocks are the source of truth |

Pass paths, never artifact text. The `adaptation-report` role reads the files itself.

## Conflicts

- **Meter conflict.** If the music-adapter needs a different time signature, bpm or key than `structure.md`, it
  returns `BLOCKED` with `FINDINGS`; the orchestrator re-runs Stage 3 and then the lyric stage as needed.
- **Hook conflict.** If a lyric fit and a melody contour disagree on where the hook sits, the lyric hook wins;
  the music-adapter re-times the melody and logs it under Risks.
- **Change budget.** `adaptation.max_changed_elements` applies to the final report. Each role keeps its own
  Changed lines grouped by element family so the consolidation fits without losing a hook-level change.
- **Provenance.** One check per run, in Phase 1 of the skill; roles do not re-ask.

## Standalone report-only requests

"What would change if this were <genre>": run the role matching the input with task `adaptation-report` and a
note that no artifact was adapted. The report then lists the changes that *would* be made under Changed, marks
Kept as the identity elements found, and states under Risks that the report is a plan, not an adaptation.
