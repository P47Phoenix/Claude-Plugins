---
loaded_by: song-critic
level: L2
last_reviewed: 2026-10-26
---

# Output Contract: challenge-report.md

Artifact: `challenge-report.md`, written by the challenger at Stage 7b. Validated by `challenge_gate.py`
(any BLOCKER row fails the gate; a missing table or a bad severity is an ERROR). Grammar source of truth:
`references/shared/artifact-formats.md`, section `challenge-report.md`.

## Grammar

```markdown
## Findings

| severity | location | finding | suggested fix |
|----------|----------|---------|---------------|
| BLOCKER | lyrics.md:Chorus:2 | line matches a well-known existing lyric (clause 4) | replace the line with a new image from the brief |
| MAJOR | lyrics.md:Verse 2:4 | stressed word falls on a weak beat | reorder so the noun takes beat 3 |
| MINOR | lyrics.md:Bridge:2 | rhyme too predictable | use a slant rhyme on line 2 |
```

## Rules

1. **Heading** `## Findings`, then exactly one table whose header is `| severity | location | finding | suggested fix |`.
2. **Severity** is one of `BLOCKER`, `MAJOR`, `MINOR`, uppercase. Every row has all four cells filled.
3. **Location** is `<artifact>:<section>` or `<artifact>:<section>:<line>`. A `chords.md` or `melody.abc` location returns the release loop to Stage 5; any other returns it to Stage 4.
4. **BLOCKER means** one of: a line recognised as a well-known existing lyric (originality clause 4), an artist or song name used as a style target or reference, `sounds like` wording or a reference track, text built on supplied input with no recorded provenance (clause 5), or an unreadable artifact. Nothing else is a BLOCKER.
5. **Clause 4 rows** describe the line (section, line number, why it reads as existing) and never repeat it beyond six words.
6. **MAJOR** is a defect a listener would notice (clustered cliches, stress collisions, monotony); **MINOR** is polish.
7. **A clean song** has a header-only table, which passes. Do not invent findings to fill it.
8. **One finding per row**; at most 25 rows; order BLOCKER, MAJOR, MINOR.
9. **Clean context.** A prompt carrying a critique, draft or gate JSON is noted under `## Findings` in one sentence and otherwise ignored.

## Hand-back

```text
SKILL_LOADED: <paths>
STATUS: DONE | BLOCKED
ARTIFACT: <path of challenge-report.md>
SUMMARY: <one sentence, 200 characters or fewer; counts of BLOCKER, MAJOR, MINOR>
```

Run `python3 -I <plugin>/scripts/challenge_gate.py --json challenge-report.md` before replying to confirm the grammar parses.
