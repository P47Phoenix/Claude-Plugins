---
loaded_by: lyricist
level: L2
last_reviewed: 2026-10-26
---

# Augment Output Contract

Role: `augmenter`. Task: `lyric-augment`. Song type: AUGMENT_LYRICS. Artifact: `lyrics.md` holding the whole song: source sections plus the new ones. Validated by `prosody_check.py` and `rhyme_check.py` (scoped to the new sections against the source `meter_spec` and `rhyme_scheme`) and `cliche_scan.py`.

## Grammar

The file is the full `lyrics-output.md` grammar plus two additions. Both additions are `#`-prefixed lines, which every gate ignores.

1. **New-section marker.** The first line under the tag of each new section is `# <!-- new -->`. Source sections carry no marker.
2. **Augmentation block.** After the last section, one blank line, then `## Augmentation` and four `# `-prefixed lines in this order:

```markdown
[Verse 1]
<source line, verbatim>
...

[Bridge]
# <!-- new -->
<new line>
<new line>
<new line>
<new line>

## Augmentation
# Kept: Verse 1, Verse 2 (verbatim, unedited)
# Added: Bridge (4 lines), same voice, diction shifted toward <target genre> if it differs
# Meter check: <new section> lines are <n> syllables, <stress string>, the pattern of <source section>
# Rhyme check: <new section> scheme <letters> (<rhyme pairs by line>), matching the source scheme
```

## Rules

| Rule | Detail |
|------|--------|
| Verbatim source | Every original line appears unchanged, in the original order, unless the user asked for edits; edits are listed in `Added:` as `Edited: <section>:<line>` |
| Order | Sections follow `structure.md`; a new section sits where the structure places it |
| New-section fit | Line count equals its `meter_spec` entries; syllables and stress match; rhyme follows the section's `rhyme_scheme` |
| Structure | `structure.md` lists the new sections with a `meter_spec` copied from the source pattern; if it does not, report it in `SUMMARY` instead of changing the source |
| Kept / Added | `Kept:` names source sections; `Added:` names new sections with line counts; both mandatory |
| Checks | `Meter check:` and `Rhyme check:` report the self-check result in words, not script output |

## Hand-back

`SKILL_LOADED:`, `STATUS: DONE | BLOCKED`, `ARTIFACT: <dir>/lyrics.md`, `SUMMARY:` (<= 200 characters). `BLOCKED` when provenance is missing or the supplied text is recognised as a well-known lyric (clause 4); write no artifact then.
