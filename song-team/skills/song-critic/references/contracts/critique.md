---
loaded_by: hook-judge, prosody-judge, structure-judge, music-judge
level: L2
last_reviewed: 2026-10-26
---

# Output Contract: critique

Written to `.song/<slug>/critique-<stage>.md`. Maximum 60 lines including front-matter. Plain Markdown; no code fences inside the body except where a suggested revision needs line breaks.

## Front-matter (required, exactly these keys)

```yaml
---
stage: 4
gate_script: prosody_check, rhyme_check
gate_status: FAIL
---
```

`stage` is the integer stage number. `gate_script` lists every script whose JSON was supplied, names without `.py`, comma-separated. `gate_status` is the worst status across them in the order `ERROR > FAIL > SKIPPED > PASS` (SKIPPED proceeds as PASS but is reported as SKIPPED).

## `## Findings` (required)

A table with exactly these columns:

```markdown
| location | violation | diagnosis | suggested revision |
|----------|-----------|-----------|--------------------|
| Verse 1:1 | stress mismatch (0.94 > 0.15) | "beneath" puts the beat on "be-" | "under the streetlight glow" lands S on under, street, glow |
```

Rules per row:

- `location` is copied verbatim from a `violations[].location` in the gate JSON. No invented locations, no ranges, no "throughout".
- When `gate_status` is PASS and the rubric still finds a craft issue, `location` is `rubric:<metrics key>` (for example `rubric:hook_syllables`, `rubric:chorus_mismatch_ratio`). Such rows are advisory.
- `violation` restates `reason` with `observed` and `limit` in parentheses.
- `diagnosis` names the exact word, bar, or label at fault, in one sentence.
- `suggested revision` is a concrete replacement the worker pastes or applies, not advice ("tighten this").
- One row per gate violation; a cliche scan with many hits on one line collapses to one row per location listing each phrase.
- Order rows: chorus and hook first, then by section order, then by line.

An empty table (header only) is valid only when `gate_status` is PASS.

## `## Rubric scores` (required)

Five rows, one per criterion of the loaded rubric, in rubric order:

```markdown
| criterion | score | one-line reason |
|-----------|-------|-----------------|
| Singability | 2 | three lines in the chorus stress the article |
```

Scores are integers 1-5. Scores inform the orchestrator's priority and the retrospective; they never alter `gate_status`.

## `## Suspected false positives` (optional)

Same `location` rule as Findings. Each row: `| location | why the heuristic is suspect |`. This section is a doubt, never an override; the gate script's verdict stands and the orchestrator shows these rows to the user only at escalation.

## Forbidden content

- Any existing artist, band, or song title, including as a comparison.
- Quoting more of the artifact than the lines cited in Findings.
- Instructions to change a stage that is already closed (meter after Stage 3 when judging Stage 4, and so on).
- Any wording that tells the worker a violation is safe to skip.

## Gate scripts run against this output

None. The orchestrator validates the shape: front-matter keys present, every Findings `location` present in the supplied gate JSON (or `rubric:` prefixed on PASS), five rubric rows, <= 60 lines. A failed shape check triggers one re-dispatch.
