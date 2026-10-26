---
loaded_by: adapter
level: L2
last_reviewed: 2026-10-26
---

# Output Contract: arrangement-adapt

Artifact: `arrangement.md`. The grammar is the normal arrangement grammar in
`music-team/references/shared/artifact-formats.md`, followed by one `## Adaptation notes` block.
`production-brief.md` is not required for ADAPT_GENRE.

## Arrangement body

- Header lines `key`, `mode`, `bpm`, `time_sig`, identical to `structure.md`.
- One table with columns `| section | energy | instruments_in | instruments_out | texture_note |`,
  one row per `structure.md` section, in section order, `section` equal to the structure label.
- `energy` is an integer 1-10. At least one verse-type section sits below the chorus that follows it
  (`arrangement_check.py` rejects a flat curve); the quietest and loudest sections of the source stay the
  quietest and loudest.
- `instruments_in` / `instruments_out` are comma-separated lists or `-`; every instrument leaving was entered earlier.
- `texture_note` is technical language only: density, register, reverb, vocal treatment. No artist names, no
  "sounds like", no reference tracks.
- Instruments come from the target profile `## Arrangement` core and optional lists.

## Adaptation notes block

After the table, one blank line, then the literal heading and `# `-prefixed lines:

```text
## Adaptation notes
# Kept: <comma-separated preserved elements: energy shape, section order, sparse opening, ...>
# Changed: <element>: <source> -> <target> (<why>)
# Risks: <one risk per line>
```

Rules: exactly one `# Kept:` line; one `# Changed:` line per element family (instrumentation, percussion,
tempo and feel, texture); every Changed entry has element, source, target and why; at most
`adaptation.max_changed_elements` Changed lines; no artist, band or song names.

## Example

```markdown
| section | energy | instruments_in | instruments_out | texture_note |
|---------|--------|----------------|-----------------|--------------|
| Verse 1 | 3 | nylon-string guitar, upright bass | - | soft close vocal, rim click only |
| Chorus | 5 | brushed snare, shaker | - | vocal opens slightly |

## Adaptation notes
# Kept: sparse opening, modest dynamic range
# Changed: guitar: strummed acoustic -> nylon-string syncopated pattern (core groove of the target)
# Risks: brushes can crowd the guitar pattern
```

## Hand-back

```text
SKILL_LOADED: <every references/ path pasted>
STATUS: DONE | BLOCKED
ARTIFACT: <dir>/arrangement.md
SUMMARY: one sentence, max 200 characters
```
