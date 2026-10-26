# song-team test fixtures

Every file under this directory is original text written for the test set on 2026-10-26. No lyric line, title, brief, or corpus line quotes or paraphrases an existing song, and no real artist or song is named anywhere (the only named band, "The Harbor Lanterns", is fictional). Files are UTF-8 with LF newlines. Artifact grammars follow `song-team/references/shared/artifact-formats.md`; gate rules the fixtures satisfy or violate are the normative ones in `references/shared/stage-gates.md`.

## Layout

```text
tests/fixtures/
  README.md                  this file
  prosody-gold/gold.tsv      hand-labelled syllable and stress benchmark (240 lines)
  briefs/<TYPE>.md           one brief per routing row in song-types.md (8 files)
  briefs/expected.json       expected song_type per brief; PARODY_ADAPT is refused
  songs/FULL_SONG/           complete passing artifact set (pop, D major, 118 bpm, VCVCBC)
  songs/LYRICS_ONLY/         passing lyric-side set (folk, C major, 96 bpm, VCVCBC)
  songs/INSTRUMENTAL/        passing no-lyric set (electronic, A minor, 124 bpm, edm-build-drop)
  songs/TOPLINE/             passing set over user-supplied chords (pop, G major, 100 bpm, VCVCBC)
  songs/JINGLE/              passing 12-bar jingle (pop, G major, 130 bpm, jingle)
  songs/REWRITE/             passing lyric-edit set over a user-supplied rough draft (country, G major, 92 bpm, VCVCBC)
  negative/<case>/           one artifact set per failure mode, each with expected.json
  resemblance/               do-not-resemble corpus plus a lyric that copies three of its lines
```

## expected.json shapes

- `songs/<TYPE>/expected.json`: `{"<script>": "PASS|SKIPPED", ...}` for every gate script that applies to that song type (plus `song_type`). Each script is run from inside the song directory with its documented artifact arguments.
- `negative/<case>/expected.json` and `resemblance/expected.json`: `{"expectations": [{"script", "args", "status", "location_contains"?}, ...]}`. `args` are file names relative to the case directory (flags such as `--hook` or `--config` appear in `args` verbatim); `status` is the expected `status` field and exit code class; `location_contains` is a substring that must appear in at least one `violations[].location`. A case may list several scripts.
- `briefs/expected.json`: `{"<TYPE>": {"song_type": "<TYPE>", "refused"?: true}}`.

## Brief fixtures

Each `briefs/<TYPE>.md` starts with a complete `brief.md` front-matter block (so `gate_common.parse_frontmatter` reads it as a real brief), followed by `## Request` holding the one-sentence user request that should trigger that routing row, then `## Brief` and, for TOPLINE and REWRITE, `## Supplied input` with the user-owned chords or lyric and `user_asserts_original_input: true`. `REVISE.md` assumes an existing `.song/nobody-knows-my-name-here/state.json` with `status: complete`. `PARODY_ADAPT.md` has no front-matter because the refusal produces no brief.

## Prosody gold set (`prosody-gold/gold.tsv`)

Tab-separated, three columns: `line`, `syllables` (integer), `stress` (one character per syllable in word order, `S` stressed, `u` unstressed). Lines starting with `#` are comments (provenance and column names). Lines are 3-12 syllables and mix mono- and polysyllabic words. Targets for a heuristic: at least 90 percent line-level syllable accuracy and at least 85 percent stress accuracy.

Labelling rules:

1. **Syllables** are counted as in careful (dictionary) speech, not sung or compressed speech: `every` 3, `ordinary` 4, `camera` 3, `library` 3, `interesting` 4. Silent final `e` does not count (`home`, `time`, `love` are 1). `-ed` counts only after `t` or `d` (`walked` 1, `wanted` 2, `needed` 2). Consonant plus `-le` counts one (`little` 2, `kettle` 2). `-tion`, `-sion`, `-ious` are one syllable each (`station` 2, `decision` 3, `serious` 3, `ambitious` 3). `fire`, `hour`, `flour`, `wires`, `tired`, `oil` are 1; `tower`, `flowers`, `power` are 2. Contractions (`I'm`, `don't`, `you're`, `won't`, `I'd`) are 1; `doesn't`, `couldn't` are 2; `whatever's` is 3. Hyphenated compounds count each part (`shop-bought` 2).
2. **Content words** (nouns, main verbs, adjectives, adverbs, numerals and the quantifiers `all`, `half`, `every`, `most`, ordinals, indefinite compounds such as `nobody`, `someone`, `everything`, `somewhere`, and the standalone possessives `mine`, `yours`) take `S` on their primary-stress syllable and `u` on every other syllable: `numbers` Su, `again` uS, `imagination` uuuSu, `cathedral` uSu, `seventeen` uuS. Monosyllabic content words are `S`. Verb particles are content (`left the light on` ends S; `comes out` is SS).
3. **Function words** are `u` on every syllable: articles, prepositions (including two-syllable ones used as prepositions such as `over the reservoir` uu, `under` uu; but `over` as an adverb in `started over` is Su), personal, relative, and demonstrative pronouns, possessive determiners (`my`, `your`), conjunctions, auxiliaries and modals (`is`, `was`, `have been`, `will`, `would`, `could`, `won't`, `doesn't`), `to`, `of`, `not`, the determiners `a`, `the`, `this`, `no`, `some`, `each`, and wh-words (`how`, `where`, `when`, `what`, `who`).
4. Capitalisation and punctuation never affect the labels. Where the dictionary gives second-syllable stress (`hello` uS, `hotel` uS, `TV` uS, `belongs` uS), the gold set follows the dictionary even though the plugin heuristic will put stress on the first syllable; these are the deliberate stress-accuracy traps along with the syllable traps in rule 1.

## Song sets

`songs/FULL_SONG/` is the Appendix A walkthrough song ("Nobody Knows My Name Here"): `brief.md`, `concept.md`, `structure.md`, `lyrics.md`, `chords.md`, `melody.abc`, `arrangement.md`, `production-brief.md`, `panel-report.md`, `challenge-report.md`. Sections are `Verse 1, Pre-Chorus 1, Chorus, Verse 2, Pre-Chorus 2, Chorus, Bridge, Chorus` with the energy curve 3, 5, 7, 4, 6, 8, 5, 9. The `meter_spec` of every section is the real per-line syllable count and stress string of the lyric under the rules above, so `prosody_check.py` sees a mismatch ratio of 0 against a perfect labeller. Every lettered rhyme pair is a full rhyme whose final spelled vowel group plus trailing consonants are identical (`street`/`feet`, `town`/`down`, `door`/`floor`, `rain`/`again`, `nine`/`mine`, `wall`/`call`, `old`/`told`), with one deliberate exception: the hook word `yet` against `met`. A key builder that treats a word-initial `y` as a vowel gets `yet` versus `et`; the pair still passes as a tolerated slant rhyme (identical final consonant cluster `t`) under the default `slant_rhyme_allowed: true`, so `expected.json` says PASS either way. The ABC melody carries a `w:` line per music line, uses one melisma (`yet_` over two notes in every Chorus) and one skipped note (`*` at the end of every Chorus), stays within MIDI 62-74, and never leaps more than 12 semitones. The chord chart is fully diatonic and every section ends on a V-I or IV-I cadence. `challenge-report.md` has exactly one MINOR row and no BLOCKER. The first chorus line is labelled 8 syllables (`No-bo-dy knows my name here yet`), not the 9 the plan's walkthrough quotes for the longer working title.

`songs/LYRICS_ONLY/` is a second original song ("Half the Island Looks Away", folk, C major) with only the lyric-side artifacts and a header-only challenge table.

The four W3-1 sets below cover the remaining routing rows. Each holds exactly the artifacts its row in `song-types.md` produces, and every set's `expected.json` lists only the scripts whose SONG_ARGS inputs exist in that directory (`test_fixtures.py` drops absent arguments, so a script is listed only when its required inputs are present). `structure_check --consistency` is run over every present artifact of every set.

| set | song | artifacts | notes |
|-----|------|-----------|-------|
| `INSTRUMENTAL` | "Signal Lanterns", electronic, A minor, 124 bpm, `edm-build-drop` (Intro 8, Build 8, Drop 16, Breakdown 8, Build 8, Drop 16, Outro 8) | brief, concept (`motif:`, no `hook_line`), structure (empty `meter_spec` and `rhyme_scheme`), chords, melody.abc (no `w:` lines), arrangement, production-brief, challenge-report (one MINOR) | energy 2, 5, 8, 3, 6, 9, 4: the Drops play the chorus role under `chorus_rising` (8 then 9, peak in the final Drop, Outro below it, no verses). `abc_validate` reports `alignment_skipped`. Chart is fully diatonic in natural minor (`i ii iv v VI VII III`, the dominant is minor `v`) and every section ends `v-i` or `iv-i`. `cliche_scan` and `prosody_check --hook` are not in `expected.json` because SONG_ARGS scans `lyrics.md`, which does not exist; both pass on `concept.md` (`--hook` returns SKIPPED `instrumental motif`). Melody range MIDI 57-76, largest leap 8 |
| `TOPLINE` | "A Lot to Ask", pop, G major, 100 bpm, VCVCBC | brief with a `## Supplied input` chord block and `user_asserts_original_input: true`, concept, structure, lyrics, chords (the supplied numerals verbatim plus `>` concert lines), melody.abc with `w:` alignment, challenge-report (one MINOR); no arrangement or production brief (Stage 6 skipped) | The supplied chart covers the whole form so Stage 3 infers VCVCBC from it; every section ends `V-I`. Prosody ratio 0 in every section, eleven full-rhyme pairs, 48 aligned bars, range MIDI 62-76, largest leap 7 |
| `JINGLE` | "Flat to Fixed in Fifteen" for the fictional shop Pedal Patch (the `briefs/JINGLE.md` brand), pop, G major, 130 bpm, `jingle` | brief, concept, structure, lyrics, chords, melody.abc with `w:`, arrangement (3 rows), production-brief, challenge-report (header-only) | Chorus 4, Verse 1 4, Chorus 4 = 12 bars (cap 16); energy 6, 5, 8 so the final chorus peaks and the verse sits below it. The Chorus spec labels the final `that` of "Roll it in and that is that" as stressed where the heuristic reads it as a function word, giving a tolerated mismatch ratio of 0.0769 (limit 0.15); every other line matches exactly. One line per bar; range MIDI 62-74, largest leap 5 |
| `REWRITE` | "The Colour Under the Colour", country, G major, 92 bpm, VCVCBC | brief with the user's rough draft under `## Supplied input` and `user_asserts_original_input: true`, structure (meter inferred from the draft's shape), lyrics (the edited second draft), challenge-report (one MINOR); no concept (Stage 2 skipped) | The draft is original but deliberately rough: run against the same `structure.md` it fails `prosody_check` (Verse 1 ratio 0.75, eleven syllable-mismatch lines) and `rhyme_check` (`fast`/`July`), and carries one near-stock line ("time flies by so fast") that the edit removes. The edited `lyrics.md` scores ratio 0 in every section, nine full-rhyme pairs, no cliche hits, and keeps the required phrase |

In all three chord charts `chord_tools` reports only "possible parallel fifths" advisories (adjacent root-position triads a step apart, normal for pop loops), never a cadence warning. `midi_export` round-trips all three melodies (3 tracks, bar counts 72 / 48 / 12).

## Negative cases

| case | files | expectation |
|------|-------|-------------|
| `malformed-abc` | `melody.abc`, `structure.md` | `abc_validate` ERROR (bad `X:`, unknown header, unbalanced bar) |
| `mismatched-tags` | `lyrics.md`, `structure.md` | `structure_check` FAIL and `prosody_check` ERROR (`[Verse 2]` absent from structure) |
| `empty-lyrics` | `lyrics.md`, `structure.md` | `cliche_scan` ERROR (no text), `structure_check` FAIL (0 lines vs 2 meter lines) |
| `wrong-key-chords` | `chords.md`, `structure.md` | `chord_tools` FAIL (diatonic ratio 1/16 in C major) |
| `non-english` | `brief.md` (`language: es`), `lyrics.md`, `structure.md` | `prosody_check` and `rhyme_check` SKIPPED |
| `w-mismatch` | `melody.abc`, `lyrics.md`, `structure.md` | `abc_validate` FAIL at `Verse 1:1` (bar 1 has 4 notes but 3 `w:` tokens) |
| `prosody-fail` | `lyrics.md`, `structure.md` | `prosody_check` FAIL (Verse 1 spec is trochaic, lyric is iambic; Chorus is clean) |
| `rhyme-fail` | `lyrics.md`, `structure.md` | `rhyme_check` FAIL (AABB with `street`/`rain`) |
| `cliche-heavy` | `lyrics.md` | `cliche_scan` FAIL (16 non-overlapping list hits in 66 words, 24.24 per 100; nested phrases count once) |
| `flat-energy` | `arrangement.md` | `arrangement_check` FAIL (every energy 5, so no verse is below its following chorus) |
| `challenge-blocker` | `challenge-report.md` | `challenge_gate` FAIL (one BLOCKER row) |
| `challenge-malformed` | `challenge-report.md` | `challenge_gate` ERROR (prose, no table) |
| `hook-too-long` | `concept.md` | `prosody_check --hook` FAIL (16-syllable hook line) |
| `scheme-length` | `lyrics.md`, `structure.md` | `rhyme_check` ERROR at `Verse 1` (3 lyric lines against the 4-letter scheme AABB) |
| `unknown-template` | `structure.md` | `structure_check` ERROR at `form_template` (`waltz-xyz` is not in form-templates.json) |
| `short-lyric` | `lyrics.md`, `config.yml`, `corpus.txt` | `resemblance_check --config config.yml` ERROR (4-word lyric has no 5-gram; corpus present so it does not SKIP) |

## Resemblance

`resemblance/corpus-a.txt` is 40 lines of throwaway original lyric text standing in for a user-supplied do-not-resemble corpus. `overlapping-lyrics.md` copies three consecutive corpus lines verbatim into Verse 1 (word 5-gram overlap well above the 0.05 default). `config.yml` lists the corpus by a path relative to the config file's directory (relative corpus entries resolve against the `--config` directory, else against the first lyric's directory, never the working directory); with it `resemblance_check.py` must FAIL, and without any config it must return SKIPPED. 5-grams never cross a `[Section]` boundary, so the three copied lines must sit inside one section to count.
