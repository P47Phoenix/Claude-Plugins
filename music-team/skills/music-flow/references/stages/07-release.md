---
loaded_by: music-flow
level: L2
last_reviewed: 2026-10-26
---

# Stage 7: Release (7p adaptation report, 7a panel, 7b challenger, 7c release, 7d memory)

Routing data: `stages.yml` keys `07p-adaptation-report`, `07a-panel`, `07b-challenger`,
`07c-release`, `07d-memory`. Loop cap: `loops.release`. Run the keys in the order listed,
filtered by the type's Stage 7 matrix cell and each key's `runs_on_cells` / `only_types`.

## Sub-flow

| Step | Key | Who | Output | Gate |
|------|-----|-----|--------|------|
| 7p | `07p-adaptation-report` | agent `adapter`, `music-adapter` (ADAPT_GENRE only) | `adaptation-report.md` | `adapt_check.py` |
| 7a | `07a-panel` | agent `song-critic`, `listener-panel` (cell F only) | `panel-report.md` | none, advisory |
| 7b | `07b-challenger` | agent `song-critic`, `challenger` (cells F and L) | `challenge-report.md` | `challenge_gate.py`, `resemblance_check.py` |
| 7c | `07c-release` | skill `music-release`, inline via `Skill` tool | `package/` | `midi_export.py` round trip |
| 7d | `07d-memory` | skill `music-memory`, inline | `retrospective.md` | Stop hook `run_id` match |

7a and 7b are independent: dispatch them as two Agent calls in one message. 7c starts only after
7b passes. 7d runs last, always, for every type with a Stage 7 cell other than `-`.

## 7p: adaptation report (ADAPT_GENRE)

`adaptation.require_report: true` (default) makes `adaptation-report.md` mandatory. Dispatch `adapter`
(Template 1) with `source_genre`, `target_genre`, and paths to source and adapted artifacts. The report
grammar is in `references/shared/artifact-formats.md`. Run `adapt_check.py`. The script lands in
Wave 7: when `music-team/scripts/adapt_check.py` is absent, mark the gate `SKIPPED (script absent)`,
log it, proceed as PASS, and tell the user the report was written but not machine-checked. When
`adaptation.require_report` is false the step is skipped. A missing report with the script present is
a FAIL; re-dispatch `adapter` up to `loops.release`.

## 7a: listener panel

Advisory. Never gates and never loops. Result is `majority: KEEP | SKIP (n of m)` in
`panel-report.md`; relay the majority and each `top_note` (<=200 characters each) to the user and
record the majority in `release-notes.md` via `music-release`.

## 7b: challenger and the release loop

1. Dispatch the challenger with a clean context (final artifacts and shared policy files only).
2. Run `challenge_gate.py {dir}/challenge-report.md`; run `resemblance_check.py {dir}/lyrics.md`
   (SKIPPED when `originality.resemblance_corpus` is empty). A `resemblance_check.py` FAIL is a
   BLOCKER on `lyrics.md`.
3. PASS or SKIPPED on all: continue to 7c.
4. BLOCKER: read each row's `location`. `chords.md` or `melody.abc` returns to Stage 5; anything
   else returns to Stage 4. `loops_used.release += 1`; reset `loops_used.lyrics` (or `.music`) to 0.
   Pass the BLOCKER rows, not the full report, to the worker as its critique. Downstream stages
   re-run as L unless `structure_check.py --consistency` invalidates their artifact, in which case F.
5. When `loops_used.release` reaches `loops.release`, apply `escalation.on_blocker`
   (`ask_user` | `accept_best` | `fail`). `accept_best` is refused when a BLOCKER cites a recognised
   existing lyric (originality clause 4): fall back to `ask_user`.
6. MAJOR and MINOR rows never block; surface counts in the release notes.

## 7c and 7d

`music-release` writes `package/` (full set for F types; `lyric-sheet.md` and `release-notes.md` only
for LYRICS_ONLY and REWRITE; `lyric-sheet.md` plus new sections for AUGMENT_LYRICS). It runs
`midi_export.py`, which is not yet built: report `SKIPPED (script absent)` and omit `song.mid`.
`music-memory` writes `retrospective.md` with front-matter `run_id` equal to `state.json.run_id` and
never includes lyric text. After 7d set `state.json.status: "complete"`.

## Per-type variations (Stage 7 cell)

| Type | Cell | Runs |
|------|------|------|
| FULL_SONG, INSTRUMENTAL, JINGLE, REVISE | F | 7a, 7b, 7c, 7d |
| ADAPT_GENRE | F | 7p, 7a, 7b, 7c, 7d |
| LYRICS_ONLY, TOPLINE, AUGMENT_LYRICS, REWRITE | L | 7b, 7c, 7d (no panel); `challenge_gate.py` always runs |
| THEORY, PARODY_ADAPT | - / refused | none |

## state.json after this stage

`stage: 7`, `loops_used.release`, `gates.release` (merged 7b result), `gate_overrides`,
`accepted_best.release`, `status: "complete"` after 7d, `updated`. Clear nothing in `.song/active`:
the pointer stays on the finished slug so a later change request can route as `REVISE`.
