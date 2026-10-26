---
loaded_by: listener-panel
level: L2
last_reviewed: 2026-10-26
---

# Output Contract: panel-report

Written to `.song/<slug>/panel-report.md` by the `listener-panel` role. Normative grammar: `song-team/references/shared/artifact-formats.md`, section `panel-report.md`. Maximum 40 lines. Plain Markdown; no tables, no code fences. Advisory only: no script gates this file, and the orchestrator never loops a worker on it.

## Shape (required, in this order)

1. Title line: `# Listener panel: <title>` (exactly as `concept.md.title`).
2. One block per seated persona, in seat order, each exactly:

```markdown
## <persona-file-name>
verdict: KEEP | SKIP
top_note: <one sentence naming a section and a line or bar>
question: <one question the writers could act on>
```

3. A blank line, then the final line: `majority: KEEP | SKIP (n of m)` where `m` equals the number of persona blocks and `n` counts the blocks that share the majority verdict. On a tie (even `m`) write `majority: SPLIT (n of m)`.

Rules per block:

- The heading is the persona file name without `.md` (`casual-radio-listener`), never a display name.
- `verdict` is one of the two words, upper-case, no qualifier.
- `top_note` names the one moment that decided the verdict: `<Section> line <n>` for lyric moments, `<Section> bar <n>` for musical ones, `<Section>` alone for arrangement moments. One sentence, no more than 25 words.
- `question` is a single sentence ending in `?`. It asks; it does not instruct ("could the bridge land on a rhyme?" not "make the bridge rhyme").
- Each block is written in that persona's register and from its verdict rules; a KEEP from a persona whose file says SKIP on that condition is a shape failure.

## Forbidden content

- Any existing artist, band, performer, or song title, including as praise.
- More than one quoted lyric line per block.
- Rubric scores, gate names, thresholds, loop counts, or the words PASS / FAIL.
- A recommendation to re-run a stage or to release. The panel informs; it does not decide.
- A block for a persona not embedded in the prompt, or fewer blocks than personas embedded.

## Gate scripts run against this output

None. The orchestrator validates the shape: title line, one block per embedded persona with the three keys in order, verdict words valid, majority line present with `n` and `m` matching the blocks, <= 40 lines. A failed shape check triggers one re-dispatch; a second failure records `panel-report.md` as absent in the release notes and continues to Stage 7b.
