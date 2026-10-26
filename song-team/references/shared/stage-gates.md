---
loaded_by: song-flow
level: L1
last_reviewed: 2026-10-26
---

# Stage Gates (normative)

This file is the single normative source for every gate rule. Scripts in `song-team/scripts/` implement it; `tests/unit/` assert it. A rule here wins over any restatement in a technique or rubric file.

## 1. Stage table

| # | Stage | Owner role(s) | Critic | Produces (`.song/<slug>/`) | Gate script(s) | Threshold keys (`quality.*` unless noted) |
|---|-------|---------------|--------|----------------------------|----------------|-------------------------------------------|
| 1 | Brief | `song-brief` (inline) | - | `brief.md`; `.song/config.yml` if absent | brief validation: `theme` non-empty, `song_type` detected, `language` set | - |
| 2 | Concept | `lyricist:hook-writer` | `hook-judge` | `concept.md` | `cliche_scan.py`; `prosody_check.py --hook` | `cliche_max_per_100_words`, `hook_max_syllables` |
| 3 | Structure | `composer:groove` | `structure-judge` | `structure.md` | `structure_check.py` | form template (`techniques/form-templates.md`, lands in W2-4) |
| 4 | Lyrics | `lyricist:verse-writer` then `lyricist:lyric-editor` | `prosody-judge` | `lyrics.md` | `prosody_check.py`, `rhyme_check.py`, `cliche_scan.py` | `prosody_tolerance`, `slant_rhyme_allowed`, `cliche_max_per_100_words` |
| 5 | Music | `composer:harmony` then `composer:melody` | `music-judge` | `chords.md`, `melody.abc` | `chord_tools.py`, `abc_validate.py` | `diatonic_min_ratio`, `max_melodic_leap`, `vocal_range` |
| 6 | Arrangement | `arranger` (instrumentation, dynamics, production-brief) | `structure-judge` | `arrangement.md`, `production-brief.md` | `arrangement_check.py`, `structure_check.py --consistency` | `energy_curve`, `vocal_range` |
| 7 | Release | `song-critic:listener-panel`, `song-critic:challenger`, `song-release` | - | `panel-report.md`, `challenge-report.md`, `package/` | `challenge_gate.py`; `resemblance_check.py` when corpus configured | `originality.ngram_max_overlap` |

A stage with several scripts passes only when every script returns PASS or SKIPPED. The listener panel (7a) is advisory and never gates.

## 2. Common script contract (`gate_common.py`)

```text
usage: <script>.py [--config .song/config.yml] [--json] [--genre <g>] <artifact paths...>
exit codes: 0 PASS | 1 FAIL | 2 SKIPPED (gate not applicable, e.g. non-English) | 3 ERROR (unparseable input)
--json stdout schema:
{ "script": "<name>", "status": "PASS|FAIL|SKIPPED|ERROR",
  "thresholds": { "<key>": <value from config or flag> },
  "metrics": { "<name>": <number> },
  "violations": [ { "location": "<section>:<line>", "reason": "<text>", "observed": <v>, "limit": <v> } ] }
```

Artifact grammars are normative in `artifact-formats.md`; rules here reference them by field name.

Every script: accepts `--help`; is stdlib-only and `python -I` safe; normalizes every path with `pathlib.PurePath(p).as_posix()` before matching; names itself in `script` without `.py`; emits `violations: []` on PASS and SKIPPED; on ERROR puts the parse failure in `violations[0].reason` with `location` of the offending line where known. Exit code and `status` always agree.

**Threshold precedence:** explicit flag (`--<key>`) > `quality.genre_overrides.<genre>.<key>` (genre from `--genre`, else `brief.md`) > `quality.<key>` > built-in default (the values in `config-schema.md`). `thresholds` reports the resolved value and tests assert it.

## 3. Script rules (normative)

| Script | Inputs | Rule | Stages |
|--------|--------|------|--------|
| `prosody_check.py` | `lyrics.md`, `structure.md`, `brief.md` (language; a `--language <code>` flag takes precedence) | **Syllables:** `scripts/data/syllable-exceptions.txt` first (performance counts, optional stress pattern); else vowel groups `[aeiouy]+` (`y` vocalic only between a consonant and a non-vowel), trailing silent `e` after a consonant does not count, `-le` after a consonant counts one, `-ed` after a non-t/d consonant is silent, `-es` counts only after s/x/z/c/g/ch/sh, hiatus pairs (ia/io/iu/eo/ua/uo) split, minimum one. **Stress (per word):** monosyllables are `u` when in `scripts/data/function-words.txt`, else `S`; polysyllables take, in order: the exception table's pattern; a stress-fixing suffix (-tion/-sion/-cian/-ic/-ity/-ical/-logy/-ette/-eer/-self ...); a neutral inflection (-s, -ed, -ing, -er, -ly, -ness, -ful, -less, -ment ...) stripped back to a table or prefix base; an unstressed Latin prefix (un-, re-, de-, be-, ex-, com-, con-, pre-, pro-, dis-, trans- ...) before an open syllable; else first-syllable stress. A stranded line-final preposition (on, in, at, by, for, with, through, off) is `S`. **Ratio (per section):** denominator = count of `S` positions in the section `meter_spec` (min 1); numerator, summed over lines i = spec-`S` positions that the lyric line i does not stress + abs(spec syllables - observed syllables), plus every syllable of a lyric line with no meter line, plus every `S` of a meter line with no lyric line. An empty `meter_spec` leaves the section unconstrained (ratio 0). **FAIL** if any section ratio > `prosody_tolerance` (ratio == tolerance passes); `metrics.<section>_mismatch_ratio` per section, `metrics.syllable_mismatch_lines`; one violation per failing section, `location: "<section>:<line>"` of the worst line. **`--hook`:** input is `concept.md`; count syllables of `hook_line`; **FAIL** if count > `hook_max_syllables` (count == limit passes); `metrics.hook_syllables`; **SKIPPED** (`instrumental motif`) when `concept.md` has `motif` and no `hook_line`; ERROR when it has neither. **SKIPPED** when the resolved language (`--language`, else `brief.md.language`) is not `en` (either mode). ERROR when a lyric section tag is absent from `structure.md`, or a threshold in config is not a number | 2, 4 |
| `rhyme_check.py` | `lyrics.md`, `structure.md` | Rhyme key of a line = last word, lower-cased, punctuation stripped, from its final vowel group to the end (`y` is vocalic when final or after a consonant; a trailing silent `e` after a consonant stays in the consonant tail, so time/lime key as `Ime`). `scripts/data/rhyme-exceptions.txt` (`word<TAB>key`: through, you, do, who, two, to, love, of, come, some, one, done, none, gone ...) is consulted first. The final vowel group is then normalised to a class: ee/ea/ie/ei-after-c/final-e -> `E`; ay/ai/ei/ey/eigh -> `A`; oo/ue/ew/final-ou/final-u -> `U`; igh/final-y-in-a-monosyllable/final-ie/final-i -> `I`; oa/ow/oe/final-o -> `O`; a lone vowel before consonant+silent-e takes its long class (name -> `Ame`); final `y` after an earlier vowel group -> `E` (lonely); silent `gh` is dropped from the tail (bought -> `out`). **Full rhyme:** identical keys (see/be, day/weigh, blue/through, high/sky, love/of). **Slant rhyme:** identical vowel class only, or identical non-empty final consonant cluster with a different vowel class (go/see is not a rhyme). Scheme letters in `rhyme_scheme` are scoped per section (an `A` in Verse 1 is unrelated to an `A` in Verse 2); `x` or `X` marks an unconstrained line; an empty scheme leaves the section unconstrained. Within a section every pair of lines sharing a letter must full-rhyme, or slant-rhyme when `slant_rhyme_allowed: true`. **FAIL** on any unmatched pair; the violation `location` is the later line; `metrics.pairs_checked`, `metrics.slant_pairs` (tolerated slant pairs). ERROR if a section's line count differs from its (non-empty) scheme length, or `slant_rhyme_allowed` is not a boolean. **SKIPPED** when `language != en` | 4 |
| `structure_check.py` | `structure.md` [+ `lyrics.md`, `chords.md`, `melody.abc`, `arrangement.md`] | Section labels and their order must match the named `form_template` (its allowed label sequence, with optional repeats as the template defines); each section's `bars` within the template min/max; when `lyrics.md` is given, lyric line count per section must equal the number of meter spec lines for that section. **FAIL** on any diff. **`--consistency`:** across all present artifacts, `key`, `mode`, `bpm`, `time_sig` must be identical (`structure.md` fields; `K:`/`Q:`/`M:` in ABC; the chord chart key line; arrangement header), the melody pitch range must lie within `vocal_range`, and the ordered section lists must be identical (`[Label]` tags in Markdown artifacts, `%%section <Label>` lines in `melody.abc`). **FAIL** on any diff, one violation per differing field with `observed` and `limit` (expected). Never SKIPPED. ERROR on a missing `form_template` or unknown template name | 3, 6, REVISE |
| `arrangement_check.py` | `arrangement.md` | Reads `energy` per section in order. Let `C1..Cn` be the chorus energies in order, `G` the global maximum. **`chorus_rising`** (default) PASSES iff all of: (a) `Ci >= Ci-1` for every `i > 1`; (b) `G` occurs in the final chorus or in the bridge (ties count); (c) the final section's energy `< G` unless the final section is the last chorus; (d) every verse energy `<` the energy of the next chorus after it (a verse with no following chorus is unconstrained). **`strict_rising`** PASSES iff the sequence is non-decreasing up to the first occurrence of `G` and non-increasing after it. **`free`:** always PASS with `metrics` reported. Sections labeled `Drop` count as choruses and `B` (AABA) counts as the bridge; when no chorus-role section exists, `chorus_rising` evaluates as `strict_rising` and reports `metrics.no_chorus: 1`. ERROR if no section has `energy` or any `energy` is outside 1..10 | 6 |
| `chord_tools.py` | `chords.md`, key from `structure.md` | Parse every Roman-numeral cell (`I..vii`, qualities `dim`/`aug`/`7`/`maj7`/`m7`/`sus2`/`sus4`, slash bass, `bVII`/`#iv` accidentals, `%` repeats previous cell). Diatonic = root and quality belong to the key's mode. `metrics.diatonic_ratio` = diatonic chords / all chords (repeats count). **FAIL** if ratio < `diatonic_min_ratio`. Emits concert-pitch spellings per cell. **Warnings (not FAIL)** go in `metrics.warnings` count and a `violations`-shaped list under `"warnings"`: parallel fifths between adjacent root-position triads; a section whose last two cells form no cadence (V-I, IV-I, V-vi, bVII-I). ERROR on an unparseable cell | 5 |
| `abc_validate.py` | `melody.abc` [+ `lyrics.md`] | Must parse as ABC 2.1 with headers `X:`, `T:`, `M:`, `L:`, `Q:`, `K:` and at most one `V:` line. `K:` and `M:` must equal `structure.md` `key`/`mode` and `time_sig`. Sections are delimited by `%%section <Label>` lines whose labels must match `structure.md`. No interval between consecutive note heads > `max_melodic_leap` semitones; every pitch within `vocal_range` inclusive. **Lyric alignment** runs when `lyrics.md` exists and `song_type != INSTRUMENTAL`: ABC 2.1 `w:` token rules apply: `-` splits a word into syllable tokens; `_` extends the previous syllable over the next note (no new token); `*` skips one note; `~` joins two words into one token; `\|` advances to the next bar. After applying them, per bar: syllable tokens + `_` extensions + `*` skips must equal the number of non-rest note heads; and the de-hyphenated `w:` text per section (tokens joined, `~` restored to a space) must equal the `lyrics.md` section text ignoring case and punctuation. **FAIL** on any violation with `location: "<section>:<bar>"`. ERROR on parse failure | 5 |
| `midi_export.py` | `melody.abc`, `chords.md` | Writes a type-1 MIDI file: track 0 tempo (from `Q:`) and time signature (from `M:`); track 1 melody notes with ABC durations scaled by `L:`; track 2 block triads from the concert chords, one per bar, channel 1. Round-trip test parses the header (`MThd`, format 1, 3 tracks) and both `MTrk` lengths. Not a gate: exit 0 on success, 3 on parse failure | 7 |
| `cliche_scan.py` | `concept.md` or `lyrics.md` | Case-insensitive whole-phrase matches (word-boundary, punctuation-insensitive) against non-comment lines of `cliche-list.txt`; `metrics.hits`, `metrics.words`, `metrics.per_100_words` = hits * 100 / words. **FAIL** if `per_100_words` > `cliche_max_per_100_words`; one violation per hit with the phrase and line. On `concept.md` only the values of `hook_line`, `central_image`, and `title` are scanned (YAML keys excluded from `metrics.words`); on `lyrics.md` all non-comment, non-tag lines (lines starting with `#` and `[Label]` tags are not counted as words). ERROR on empty text | 2, 4, challenger |
| `resemblance_check.py` | lyric text + `originality.resemblance_corpus` | Tokenize to lower-case words; build word 5-gram sets. `metrics.overlap_ratio` = matching 5-grams / total 5-grams in the lyric. **FAIL** if ratio > `ngram_max_overlap`. **SKIPPED** when the corpus list is empty or every listed path is absent (absence is reported in `metrics.missing_files`) | 7b |
| `challenge_gate.py` | `challenge-report.md` | Locate the first Markdown table whose header row is `severity | location | finding | suggested fix` (case-insensitive, trimmed). `metrics.blocker`, `metrics.major`, `metrics.minor` count rows. **FAIL** if `blocker > 0`, one violation per BLOCKER row. ERROR if the table is missing, a row has a severity outside {BLOCKER, MAJOR, MINOR}, or a row has fewer than four cells. An empty table (header only) PASSES | 7b |
| `validate_artifacts.py` | `lyrics.md`, `chords.md`, `melody.abc`, `structure.md`, `arrangement.md`, `production-brief.md` | Runs the matching lint for the file written; `production-brief.md` **FAILs** on any `blocked-targets.txt` whole-phrase hit or the strings "sounds like" / "reference track". Advisory `PostToolUse` hook: always exit 0, findings in `violations`. Lands in W4-2 | hook |
| `check_reference_caps.py` | `song-team/**/references/**` | Every reference file <= 150 lines; files under `genres/` <= 100; every `.md` reference begins with the 3-line frontmatter; duplicate pairs listed in `CROSS-SKILL-REFERENCES.md` (lands in W5-3) byte-identical. Exit 1 on any finding, listing path and count. CI lint, not a stage gate | CI |

## 4. Stage execution protocol

1. Orchestrator reads `.song/config.yml` (created in Stage 1 if absent) and `.song/<slug>/state.json`.
2. Build the sub-agent prompt from the worker's `agent-prompts/<task>.md`, embedding only files permitted by `prompt-allowances.json`; dispatch with `subagent_type` set to the matching `agents/*.md` definition.
3. Sub-agent writes the artifact to `.song/<slug>/<artifact>` and returns the hand-back (`SKILL_LOADED:`, `STATUS`, `ARTIFACT`, `SUMMARY`).
4. **Gate decision (single runner).** Read `state.json.gates[<stage>]`. If the `SubagentStop` hook populated it in this dispatch and its `artifact_sha256` equals the sha256 of the artifact on disk, reuse it; otherwise run the gate script(s) via `gate_common.py` and write the result. This is the only gate decision point. On FAIL: dispatch the stage critic with the script JSON as evidence, then re-dispatch the worker with the critique and increment `loops_used.<stage>`. On SKIPPED: proceed as PASS and log `skipped: true` under the gate entry.
5. When `loops_used.<stage>` reaches `loops.<stage>`, apply `escalation.on_loop_exhaustion`: `ask_user` shows the last three attempts and the gate diff, user picks accept, override (recorded in `gate_overrides[]` and `decisions.md`), or guidance (resets the counter once); `accept_best` keeps the attempt with the best gate metrics (fewest violations, then lowest worst ratio) and records `accepted_best[<stage>] = true`; `fail` writes `status: "failed"` and stops.
6. Update `state.json` (`stage`, `updated`, `owners`) and proceed to the next stage the routing matrix allows.

Light (L) stages run steps 1-4 once with no critic loop: on FAIL they apply step 5 immediately. Input (I) stages run only the gate on the user-supplied artifact.

## 5. Release loop semantics

A Stage 7b BLOCKER returns to Stage 4, or to Stage 5 when the BLOCKER row's `location` names `chords.md` or `melody.abc`. Each return increments `loops_used.release` and resets `loops_used.lyrics` (or `.music`) to zero; downstream stages re-run as L unless `structure_check.py --consistency` invalidates their artifact. When `loops_used.release` reaches `loops.release`, `escalation.on_blocker` applies with the same three policies as step 5. `resemblance_check.py` FAIL is treated as a BLOCKER on `lyrics.md`.

## 6. Debate rubric (orchestrator as judge)

Used when `harmony` and `melody` disagree on key or tempo, or when two hook candidates tie. Each advocate submits <= 10 lines. The orchestrator scores both on five criteria, 1-5 each, and records the scores and rationale in `decisions.md`:

| Criterion | 5 means |
|-----------|---------|
| Gate compliance | The option already passes, or is nearest to passing, every applicable gate script |
| Brief fidelity | Matches `brief.md` genre, mood, audience, and length most closely |
| Singability | Range within `vocal_range` with tessitura in the middle third; no leap > `max_melodic_leap` |
| Structural fit | Requires no change to `structure.md`; fewer downstream invalidations |
| Specificity | The argument cites concrete bars, lines, or metrics rather than taste |

Highest total wins; on a tie, the option with the higher gate-compliance score; on a further tie, the owning role's option (`state.json.owners`). The decision is final for the run unless the user overrides.
