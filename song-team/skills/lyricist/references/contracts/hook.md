---
loaded_by: hook-writer
level: L2
last_reviewed: 2026-10-26
---

# Output Contract: concept.md (hook)

Normative grammar: `references/shared/artifact-formats.md` section `concept.md`. Normative gate rules: `references/shared/stage-gates.md`. This contract restates both for the `hook-writer` role.

## File

Path: `.song/<slug>/concept.md` (the prompt states the exact path). UTF-8, LF line endings, Markdown.

## Required front-matter

A YAML block between two `---` fences, one key per line, in this order:

| Key | Type | Rule |
|-----|------|------|
| `title` | string | 1 to 8 words. Derived from the hook line. No colon. |
| `hook_line` | string | The chorus landing line. Syllable count <= `hook_max_syllables` (default 12; genre file states any override). Plain text, no quotes around it, no trailing punctuation other than `?` or `!`. |
| `central_image` | string | One physical, concrete thing. 3 to 12 words. No abstraction as the head noun. |
| `arc` | list of 3 strings | `[start, turn, end]`, each 2 to 6 words, each a state. Beat two contradicts or complicates beat one. |
| `title_rationale` | string | One sentence stating why this title and how it relates to the hook. |

`hook_line` is required for every `song_type` except `INSTRUMENTAL`, which uses `motif` instead and never both. This role is never dispatched for `INSTRUMENTAL`.

## Optional body

`## Notes`: at most six lines. What the verses collect, what the pre-chorus turns, what the chorus answers. No lyric lines beyond the hook; verses are the `verse-writer`'s job.

## Example (original)

```markdown
---
title: Platform Nine
hook_line: I learn the tram stop, platform nine
central_image: a paper ticket folded into a coat pocket
arc: [arrive with a map, choose one stop to know, the vendor says my name]
title_rationale: the platform number is the one fact the narrator owns before anyone owns their name
---

## Notes

Verses collect small proofs of being new. The pre-chorus makes staying a choice. The chorus answers with the ticket and the platform.
```

## Forbidden content

- Real artist names, real song titles, real band names, anywhere in the file.
- Quoted or closely paraphrased lines from existing songs.
- "sounds like", "in the style of <name>", "like that song".
- Any item from `brief.md` `must_avoid[]`.
- Any whole phrase from `references/shared/cliche-list.txt` in `title`, `hook_line`, or `central_image`.
- Placeholder text (`TBD`, `[insert]`, `lorem`).
- A `hook_line` that names the theme instead of delivering it ("this is a song about leaving").

## Gates run against this file

| Script | Invocation | PASS when |
|--------|------------|-----------|
| `cliche_scan.py` | `cliche_scan.py --json concept.md` | hits * 100 / words over `title` + `hook_line` + `central_image` <= `cliche_max_per_100_words` (default 2). With ~20 words scanned, any hit fails; target zero. |
| `prosody_check.py --hook` | `prosody_check.py --hook --json concept.md brief.md` | syllables of `hook_line` <= `hook_max_syllables` (equal passes); SKIPPED when `brief.md.language` is not `en`. |

Syllables are counted by the heuristic in `techniques/prosody.md`: vowel groups, silent trailing `e` dropped, `-ed` silent after most consonants, performance counts from the exception table (`every` = 3, `fire` = 1, `hour` = 1, `poem` = 2, `flower` = 2). Count the hook line yourself with those rules and write the count in `SUMMARY`.

## Max length

40 lines including front-matter and notes.
