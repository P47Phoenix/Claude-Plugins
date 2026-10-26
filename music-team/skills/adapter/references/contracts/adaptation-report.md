---
loaded_by: adapter
level: L2
last_reviewed: 2026-10-26
---

# Output Contract: adaptation-report

Artifact: `adaptation-report.md`, written at Stage 7p. The grammar is the one in
`music-team/references/shared/artifact-formats.md` (section `adaptation-report.md`), reproduced here as the
rule set `adapt_check.py` enforces. Consolidate; do not re-adapt. Read the `## Adaptation notes` blocks of
`lyrics.md`, `chords.md` and `arrangement.md` and the `## Supplied input` of `brief.md`; change no artifact.

## Grammar

```markdown
---
song_type: ADAPT_GENRE
source_genre: <genre label or alias with a profile>
target_genre: <genre label or alias with a profile>
---

## Kept
- <preserved element>

## Changed

| Element | Source | Target | Why |
|---------|--------|--------|-----|
| <element> | <source value> | <target value> | <reason> |

## Lyric re-fit
- <section>: <meter and rhyme delta>

## Risks
- <risk>
```

Section order is fixed: Kept, Changed, Lyric re-fit, Risks.

## Rules

1. **Front-matter.** `song_type` is `ADAPT_GENRE`. `source_genre` and `target_genre` equal the brief's keys and each
   resolves to `references/shared/genres/<slug>.md` by its `genre:` or an alias. Never an artist or song.
2. **Kept.** One bullet per preserved identity element; merge the `# Kept:` lines of every artifact; at least one bullet.
3. **Changed.** Exactly the four columns above. One row per element family, merged across artifacts (for example
   `time_sig` from the arrangement and the chords is one row). Every cell non-empty, including `Why`. At most
   `adaptation.max_changed_elements` rows (default 12): when there are more, merge related rows, then drop the least
   audible change, never a change that affects the hook, key or meaning.
4. **Lyric re-fit.** One bullet per lyric section, naming its meter delta (syllables per line, stress shape) and
   its rhyme delta (scheme kept or changed). Name every `structure.md` section at least once across Kept,
   Changed and Lyric re-fit; `adapt_check.py` warns about a section it never finds. Non-empty.
5. **Risks.** One bullet per risk: singability, drift from the source, originality notes. Non-empty. If nothing risky
   remains, write one bullet that says what was checked.
6. **Text.** Quote only lines the user supplied, and only to identify a change. No lyric text beyond that, no artist,
   band or song names.
7. **Consistency.** A `Changed` row must match what the artifact notes say; if the notes and the artifact disagree,
   report it under Risks instead of silently choosing.

## Self-check before hand-back

```bash
python -I music-team/scripts/adapt_check.py <dir>/adaptation-report.md <dir>/structure.md
```

Fix every FAIL the script lists (empty cell, missing section, too many rows). Report the final status in `SUMMARY`.
The orchestrator runs the gate again; your run does not replace it.

## Hand-back

```text
SKILL_LOADED: <every references/ path pasted>
STATUS: DONE | BLOCKED
ARTIFACT: <dir>/adaptation-report.md
SUMMARY: one sentence, max 200 characters
```

`BLOCKED` adds `FINDINGS:` bullets (for example "chords.md has no Adaptation notes block").
