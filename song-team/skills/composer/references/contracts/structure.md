---
loaded_by: groove
level: L2
last_reviewed: 2026-10-26
---

# Output Contract: structure.md (form, meter spec, key, tempo)

Normative grammar: `references/shared/artifact-formats.md` section `structure.md`. Normative gate rules: `references/shared/stage-gates.md` (`structure_check.py`, and the Stage 4 readers `prosody_check.py` and `rhyme_check.py`). This contract restates them for the `groove` role.

## File

Path: `.song/<slug>/structure.md` (the prompt states the exact path). UTF-8, LF line endings, Markdown. No front-matter fences, no headings, **no comment lines**: the header parser reads the top of the file verbatim and stops at the first line that is not `key: value`.

## Structure

1. Exactly five header lines, in this order:
   `key: <Tonic>` (`A`-`G` plus optional `#`/`b`; `D`, `Bb`, `F#`) / `mode: <mode>` (`major`, `minor`, `dorian`, `mixolydian`, `lydian`, `phrygian`, `locrian`; lower-case) / `bpm: <integer>` / `time_sig: <n>/<d>` (`4/4`, `3/4`, `6/8`) / `form_template: <name>` (one of `VCVCBC`, `AABA`, `verse-refrain`, `jingle`, `edm-build-drop`, `through-composed`; case-sensitive).
2. One blank line.
3. One table with exactly this header row and separator:
   `| section | label | bars | meter_spec | rhyme_scheme |`
   `|---------|-------|------|------------|--------------|`
4. One row per section in performance order. `section` is the 1-based index. `label` is one of the allowed labels (`Intro`, `Verse N`, `Pre-Chorus N`, `Chorus`, `Post-Chorus`, `Bridge`, `Instrumental`, `Breakdown`, `Build`, `Drop`, `Tag`, `Outro`, `A1`, `A2`, `B`, `A3`; `N` a single digit) and must satisfy the template's label sequence. `bars` is a positive integer inside the template's range for that group.
5. `meter_spec`: `;`-separated entries, one per lyric line, each `N/pattern` where `N` is the syllable count and `pattern` is exactly `N` characters of `S` (stressed) and `u` (unstressed). Empty for sections with no lyric (Intro, Instrumental, Outro, every section of an INSTRUMENTAL song).
6. `rhyme_scheme`: one upper-case letter or `x` per meter entry, scoped to the section (`ABAB`, `AABB`, `AxAx`, `AA`); empty when `meter_spec` is empty. Length equals the entry count, always.
7. **Chorus line 1 = the hook.** In every `Chorus` row the first meter entry is the syllable count and stress pattern of `concept.md.hook_line`, counted by the rules in `techniques/rhythmic-feel.md`. The lyricist sings the hook verbatim on that line and the Stage 4 prosody gate measures it against this entry.
8. Repeated sections (three `Chorus` rows) carry identical `meter_spec` and `rhyme_scheme` unless the brief asks for a varied final chorus.

## Example (original; VCVCBC, hook line `Nobody knows my name here yet` = `8/SuuSuSSS`)

```markdown
key: D
mode: major
bpm: 118
time_sig: 4/4
form_template: VCVCBC

| section | label | bars | meter_spec | rhyme_scheme |
|---------|-------|------|------------|--------------|
| 1 | Verse 1 | 8 | 8/uSuSuSuS; 8/uSuSuSuS; 8/uSuSuSuS; 8/uSuSuSuS | ABAB |
| 2 | Chorus | 8 | 8/SuuSuSSS; 8/uSuSuSuS; 8/uSuSuSuS; 8/uSuSuSuS | AABB |
| 3 | Verse 2 | 8 | 8/uSuSuSuS; 8/uSuSuSuS; 8/uSuSuSuS; 8/uSuSuSuS | ABAB |
| 4 | Chorus | 8 | 8/SuuSuSSS; 8/uSuSuSuS; 8/uSuSuSuS; 8/uSuSuSuS | AABB |
| 5 | Bridge | 8 | 8/uSuSuSuS; 8/uSuSuSuS | AA |
| 6 | Chorus | 8 | 8/SuuSuSSS; 8/uSuSuSuS; 8/uSuSuSuS; 8/uSuSuSuS | AABB |
```

Running time: 48 bars x 4 beats x 60 / 118 = 98 seconds; a 180-second brief wants an Intro, pre-choruses, and a final chorus repeat.

## Forbidden content

- Real artist names, song titles, or "feels like" comparisons anywhere.
- Comment lines, headings, prose, or blank lines between the header lines; a sixth header key.
- A label outside the allowed set or outside the template's sequence; `bars` outside the group range; `jingle` totals above 16.
- A `meter_spec` entry whose pattern length differs from `N`; a `rhyme_scheme` whose length differs from the entry count.
- A `bpm` outside the template's tempo band; a `time_sig` other than `4/4`, `3/4`, `6/8`.

## Gates run against this file

| Script | Invocation | PASS when |
|--------|------------|-----------|
| `structure_check.py` (Stage 3) | `structure_check.py --json structure.md` | label sequence matches `form_template`; each `bars` inside range; total within cap; `form_template` known |
| `structure_check.py` (Stage 4) | `structure_check.py --json structure.md lyrics.md` | lyric line count per section equals meter entry count |
| `prosody_check.py`, `rhyme_check.py` (Stage 4) | read `meter_spec` and `rhyme_scheme` | ERROR there when a scheme length differs from its line count |
| `structure_check.py --consistency` (Stage 6) | compares `key`, `mode`, `bpm`, `time_sig`, section lists across `chords.md`, `melody.abc`, `arrangement.md` | every field identical |

`structure_check.py` is never SKIPPED. ERROR (not FAIL) on a missing or unknown `form_template`.

## Max length

40 lines.
