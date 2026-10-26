---
loaded_by: any
level: L1
last_reviewed: 2026-10-26
---

# Glossary

Terms used across music-team skills, references, scripts, and artifacts. Where a term has a gate, the gate script is named.

## Lyric craft

| Term | Meaning |
|------|---------|
| Prosody | The fit between the natural spoken stress of the words and the musical stress of the line. Good prosody puts stressed syllables on strong beats. Gated by `prosody_check.py`. |
| Meter spec | The per-line target in `structure.md`: syllable count plus a stress pattern, written `8/uSuSuSuS` (count / pattern), lines separated by `;`. |
| Stress pattern | A string of `S` (stressed) and `u` (unstressed) positions, one per syllable, that a lyric line should match. |
| Syllable count | Vowel-group count per word with an exception table; the heuristic is English-only. |
| Function word | Articles, prepositions, pronouns, auxiliaries, conjunctions: unstressed by default in the stress heuristic (300-word stoplist). |
| Content word | Noun, verb, adjective, adverb: stressed on its first syllable by default unless in the exception table. |
| Rhyme (full) | Identical final vowel group plus all following consonants (`light` / `night`). |
| Slant rhyme | Identical final vowel group only (`light` / `time`) or identical final consonant cluster with a different vowel (`light` / `late`). Tolerated when `slant_rhyme_allowed: true`. |
| Rhyme scheme | Letters per line within a section (`ABAB`); letters are scoped per section; `x` marks an unconstrained line (`AxAx`). Gated by `rhyme_check.py`. |
| Hook | The most memorable, repeated lyric and melodic phrase, usually the chorus title line. Length gated by `prosody_check.py --hook` against `hook_max_syllables`. |
| Hook line | The single lyric line in `concept.md` that carries the title. |
| Motif | For INSTRUMENTAL runs, the short melodic or rhythmic idea that replaces the hook line in `concept.md`. |
| Central image | One concrete, sensory image that the whole lyric returns to. |
| Arc | The three-beat emotional shape of the lyric: start, turn, end. |
| Point of view (POV) | Who is speaking and to whom: first person, second person, third person, direct address. |
| Cliche | A stock phrase on `cliche-list.txt`; density gated by `cliche_scan.py` per 100 words. |
| Specificity | Preferring a particular detail over a general statement; the main antidote to cliche. |
| Lyric sheet | The packaged, section-tagged lyric (`package/lyric-sheet.md`). |

## Music

| Term | Meaning |
|------|---------|
| Topline | The vocal melody and lyric written over an existing chord progression or track. Also the `TOPLINE` song type. |
| Tessitura | The pitch region where most of a melody sits (not its extremes); should lie in the middle third of `vocal_range`. |
| Vocal range | Lowest to highest allowed melody pitch, MIDI note numbers (`[55, 79]` = G3 to G5). Gated by `abc_validate.py`. |
| Melodic leap | The interval in semitones between two consecutive note heads; capped by `max_melodic_leap`. |
| Melodic contour | The shape of a melody over time: rising, falling, arch, wave, static. |
| Melisma | One syllable sung across several notes; written in ABC `w:` lines with `_` extensions. |
| Diatonic | A chord whose root and quality belong to the key and mode. Ratio gated by `chord_tools.py` against `diatonic_min_ratio`. |
| Borrowed chord | A chord taken from the parallel mode (for example `bVII` or `iv` in major); non-diatonic by definition. |
| Roman numeral | Chord written relative to the key: upper case major (`I`, `IV`, `V`), lower case minor (`ii`, `vi`), `dim` and `7` qualities, accidentals (`bVII`). |
| Concert pitch | The literal chord or note names (`D`, `A`, `Bm`) that the Roman numerals resolve to in the chosen key. |
| Cadence | A harmonic arrival at a phrase end: authentic (V-I), plagal (IV-I), deceptive (V-vi), or backdoor (bVII-I). `chord_tools.py` warns when a section ends without one. |
| Parallel fifths | Two voices moving in the same direction a fifth apart between adjacent root-position triads; `chord_tools.py` warns, does not fail. |
| Key / mode | Tonal center and scale (`D` / `major`, `A` / `minor`, `D` / `mixolydian`). Must agree across artifacts (consistency check). |
| Time signature | Beats per bar and beat unit (`4/4`, `6/8`); ABC `M:` must match `structure.md`. |
| Tempo (bpm) | Beats per minute; ABC `Q:1/4=118` must match `structure.md.bpm`. |
| Groove | The rhythmic feel (straight, swung, shuffle, half-time) chosen by the `groove` role with tempo and form. |
| ABC notation | Plain-text music notation (ABC 2.1). `melody.abc` uses the strict subset defined in `abc-notation-primer.md` (lands in W3-2). |
| `w:` line | An ABC lyric line aligned to the preceding music line. Tokens: `-` splits syllables, `_` extends a syllable, `*` skips a note, `~` joins words, `\|` advances a bar. |
| Lead sheet | Melody plus chord symbols (`package/lead-sheet.abc`). |
| MIDI | Binary note data exported by `midi_export.py` (`package/song.mid`, type 1, three tracks). |

## Form and arrangement

| Term | Meaning |
|------|---------|
| Form template | A named allowed sequence of sections with bar ranges, in `techniques/form-templates.md` (lands in W2-4). Gated by `structure_check.py`. |
| VCVCBC | Verse, Chorus, Verse, Chorus, Bridge, Chorus; pre-choruses and a final chorus repeat are allowed expansions. |
| AABA | Two A sections, a contrasting B (the "middle eight"), a return to A; common in standards and ballads. |
| Verse-refrain | Verses that each end in the same refrain line instead of a separate chorus; common in folk and country. |
| Jingle | A 15-60 second form: hook first, one short verse at most, hook again; brand or tagline in the hook. |
| EDM build-drop | Intro, Build (rising tension), Drop (peak energy), Breakdown, Build, Drop, Outro; the drop plays the chorus role. |
| Through-composed | No repeated sections; each section is new material; used for narrative or theater pieces. |
| Section | A tagged block (`[Verse 1]`, `[Chorus]`) shared by every artifact. |
| Energy | An integer 1-10 per section in `arrangement.md` describing perceived intensity. |
| Energy curve | The energy sequence across sections. Rules `chorus_rising`, `strict_rising`, `free` are defined in `stage-gates.md`; gated by `arrangement_check.py`. `Drop` sections count as choruses and `B` (AABA) as the bridge; with no chorus-role section, `chorus_rising` evaluates as `strict_rising` and reports `metrics.no_chorus: 1`. |
| Instrumentation | Which instruments enter and leave per section (`instruments_in`, `instruments_out`). |
| Texture | How dense or sparse the layers are at a moment (`texture_note`). |
| Production brief | Technical notes for a producer: tempo map, vocal treatment, mix priorities; never names an artist. |

## Pipeline

| Term | Meaning |
|------|---------|
| Song type | The routing class detected in Stage 1: `FULL_SONG`, `LYRICS_ONLY`, `INSTRUMENTAL`, `TOPLINE`, `REWRITE`, `JINGLE`, `REVISE`, `PARODY_ADAPT` (refused). Source: `song-types.md`. |
| F / L / I / - | Stage depth in the routing matrix: Full (loops), Light (one dispatch, gate runs), Input (user artifact validated), skipped. |
| Quick mode | `quick: true` or "quick song": every loop cap 1, `accept_best`, at most two wizard questions. |
| Stage | One of the seven pipeline steps: Brief, Concept, Structure, Lyrics, Music, Arrangement, Release. |
| Gate | A deterministic script decision (PASS / FAIL / SKIPPED / ERROR) made once per stage in protocol step 4. |
| Threshold | A config value a gate compares against; precedence flag > genre override > `quality.*` > default. |
| Loop | One worker re-dispatch after a FAIL, with the critic's critique; counted in `loops_used`. |
| Escalation | What happens at a loop cap: `ask_user`, `accept_best`, or `fail`. |
| Release loop | A Stage 7b BLOCKER sending the run back to Stage 4 or 5; capped by `loops.release`. |
| Evaluator-optimizer | The worker / critic / worker loop run at every F stage. |
| Critic (judge) | A song-critic role (`hook-judge`, `prosody-judge`, `structure-judge`, `music-judge`) that interprets gate output against a rubric; never decides the gate. |
| Rubric | Five criteria scored 1-5 that inform a critique; the script decides the gate. |
| Challenger | A clean-context adversarial role at Stage 7b that writes the severity table; the default originality control. |
| Listener panel | Three persona sub-agents (review board) at Stage 7a; advisory majority verdict, not a gate. |
| Persona | A listener profile file in `song-critic/references/personas/` (lands in W2-4/W3-4; what they notice, what makes them skip). |
| Debate | Two advocates plus the orchestrator as judge, scored by the rubric in `stage-gates.md`, recorded in `decisions.md`. |
| Consensus | `structure_check.py --consistency` agreement of key, mode, bpm, time sig, range, and section list across artifacts. |
| Decision ownership | Each artifact has one owning role in `state.json.owners`. |
| Override | A user decision to accept a failed gate; recorded in `gate_overrides[]` and `decisions.md`. |
| L0 - L3 | Progressive disclosure levels: L0 marketplace metadata, L1 SKILL.md and shared references, L2 role file plus contract, L3 genre / technique / persona / rubric files per allowance. |
| Allowance manifest | `prompt-allowances.json`: how many files from each reference directory a role's prompt may embed. |
| Exempt block | The `<!-- originality-policy -->` and `<!-- memory-lessons -->` prompt blocks, not counted by the manifest. |
| Hand-back | The sub-agent reply shape: `SKILL_LOADED:`, `STATUS`, `ARTIFACT`, `SUMMARY`. |
| Slug | The kebab-case directory name for a run under `.song/`; the current one is in `.song/active`. |
| run_id | Unique id per run (and per REVISE), matched between `state.json` and `retrospective.md` by the Stop hook. |
| Retrospective | The `music-memory` post-pipeline write-up; process observations only, never lyric text. |
| Lessons block | Up to ten lines from the last five same-genre memory files, injected into Stage 2 and 4 prompts. |
| Resemblance corpus | Opt-in user-supplied lyric files the song must not overlap (5-gram ratio); `resemblance_check.py`. |
| Blocked target | An artist name or song title in `blocked-targets.txt` that may not be used as a style target. |
