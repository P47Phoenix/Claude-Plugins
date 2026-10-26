---
loaded_by: song-critic
level: L2
last_reviewed: 2026-10-26
---

# Output Contract: panel-report.md

Artifact: `panel-report.md` at the song directory root, written at Stage 7a. Advisory: no script gates it.
Grammar source of truth: `references/shared/artifact-formats.md`, section `panel-report.md`.

## Grammar

```markdown
## casual-radio-listener
verdict: KEEP
top_note: the chorus lands on the first listen
question: does verse two need the second image?

## songwriter-peer
verdict: SKIP
top_note: the bridge repeats the verse shape
question: what changes emotionally in the bridge?

## genre-devotee
verdict: KEEP
top_note: the groove sits right for the genre
question: is the turnaround too busy?

majority: KEEP (2 of 3)
```

## Rules

1. **One block per persona**, `## <persona-name>` equal to the persona file's `name`, in the order the personas were pasted.
2. **Keys** `verdict`, `top_note`, `question`, each on its own line, in that order. `verdict` is `KEEP` or `SKIP`.
3. **`top_note`** one sentence, 200 characters or fewer, naming a section or moment. **`question`** one open question for the writer.
4. **Last line** `majority: KEEP | SKIP (n of m)`: n votes for the winning verdict out of m personas; a tie is SKIP.
5. No lyric text beyond six words in any field; no artist or song names; no PASS or FAIL wording.
6. **Panel size above 3** (`quality.listener_panel_size`): each persona is a separate dispatch writing its own block to `panel-report.<persona>.md`; the orchestrator merges them and writes the majority line.

## Hand-back

```text
SKILL_LOADED: <paths>
STATUS: DONE | BLOCKED
ARTIFACT: <path of panel-report.md>
SUMMARY: <one sentence, 200 characters or fewer; the majority and the strongest note>
```
