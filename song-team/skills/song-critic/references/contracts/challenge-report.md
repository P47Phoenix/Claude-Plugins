---
loaded_by: challenger
level: L2
last_reviewed: 2026-10-26
---

# Output Contract: challenge-report

Written to `.song/<slug>/challenge-report.md` by the `challenger` role. Normative grammar: `song-team/references/shared/artifact-formats.md`, section `challenge-report.md`. Maximum 60 lines. `challenge_gate.py` parses the first table whose header is `severity | location | finding | suggested fix` and FAILS on any BLOCKER row; a header-only table PASSES.

## Shape (required, in this order)

1. Title line: `# Challenge report: <title>`.
2. `## Findings` followed by the severity table with exactly these columns:

```markdown
| severity | location | finding | suggested fix |
|----------|----------|---------|---------------|
| BLOCKER | lyrics.md:Chorus:1 | recognised as an existing well-known lyric line | replace with an original image on the same stress pattern; keep the end rhyme |
| MAJOR | lyrics.md:Verse 2 | three cliche-list phrases in eight lines | swap two for images from the brief's setting |
| MINOR | chords.md:Bridge | familiar pattern, not attributable | move the vi to a IV on bar 5 for a fresh lift |
```

3. Optional `## Notes`: at most one paragraph stating what was checked and found clean. No table, no severities.

Rules per row:

- `severity` is exactly `BLOCKER`, `MAJOR`, or `MINOR`; any other word makes the gate ERROR.
- `location` is `<artifact>:<section>:<line>` for a lyric line (`lyrics.md:Verse 1:3`), `<artifact>:<section>:<bar>` for melody (`melody.abc:Chorus:2`), `<artifact>:<section>` for a chord block or arrangement row, `concept.md:hook_line` or `concept.md:title` for the concept, `production-brief.md:<heading>` for the production brief. The artifact name is mandatory: the orchestrator reads it to route a BLOCKER to Stage 4 (`lyrics.md`, `concept.md`), Stage 5 (`chords.md`, `melody.abc`), or Stage 6 (`production-brief.md`: an L re-dispatch of `arranger:production-brief`, counted against `loops.release`).
- `finding` is one clause, no more than 15 words, and never quotes the matched work.
- `suggested fix` is a craft direction the worker applies, not replacement words for a BLOCKER row (writing the words would be the challenger drafting).
- Every cell is present; a row with fewer than four cells makes the gate ERROR.
- Order rows BLOCKER first, then MAJOR, then MINOR; within a severity, chorus and hook first, then section order.
- One row per location. Several cliche hits in one section collapse to one row.

## Severity definitions

**BLOCKER** (release stops; routed back to Stage 4, 5, or 6):

- A line the challenger recognises as an existing well-known lyric (originality clause 4).
- A named artist, song title, or brand used as a style target anywhere, or the phrases `sounds like`, `reference track`, `in the style of` (clauses 1 and 3), including any `blocked-targets.txt` entry.
- Resemblance to a known work the challenger can name without quoting it: a melody phrase, a chord-plus-rhythm pattern, or a form that belongs to one specific work.
- Lyrics or chords built on supplied input without `user_asserts_original_input: true` (clause 5).

**MAJOR** (reported; the user decides whether to loop): cliche density (three or more list phrases in one section, or any on the hook line); a prosody collision on a chorus line; structural monotony (three or more sections sharing rhythm, chords, and texture); a hook line that does not appear in the chorus.

**MINOR** (reported; no action expected): a predictable rhyme pair, one isolated cliche, a vague image, a bridge that restates the chorus, or a familiar pattern the challenger cannot attribute.

## Forbidden content

- Any quoted, titled, or attributed existing work, even to explain a BLOCKER. The location is the evidence.
- Replacement lyric lines or chord cells in a BLOCKER row.
- Gate names, thresholds, scores, loop counts, or references to any critique or draft.
- A row without an artifact name in `location`.

## Gate scripts run against this output

`challenge_gate.py --json challenge-report.md`: `metrics.blocker`, `metrics.major`, `metrics.minor`; FAIL when `blocker > 0` with one violation per BLOCKER row; ERROR on a missing table, a bad severity, or a short row. At Stage 7b a FAIL enters the release loop (`stage-gates.md` section 5); at Stage 4 (`quality.adversarial_lyrics: true`) a FAIL re-dispatches `lyric-editor` with the BLOCKER rows and counts against `loops.lyrics`.
