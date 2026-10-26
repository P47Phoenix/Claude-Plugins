---
loaded_by: music-flow, music-release, every worker contract
level: L1
last_reviewed: 2026-10-26
---

# Artifact Formats

Every artifact lives under `.song/<slug>/`, is Markdown, plain text, ABC, JSON, or MIDI, and is written by exactly one owning role. Section tags are `[Label]` on their own line and must be identical across `structure.md`, `lyrics.md`, `chords.md`, `melody.abc` (`%%section` comments), and `arrangement.md`. Allowed labels: `Intro`, `Verse N`, `Pre-Chorus N`, `Chorus`, `Post-Chorus`, `Bridge`, `Instrumental`, `Breakdown`, `Build`, `Drop`, `Tag`, `Outro`, plus AABA `A1`, `A2`, `B`, `A3`. No artist names or quoted existing lyrics anywhere. Examples below are minimal, not complete songs.

| Artifact | Path | Owner | Validated by |
|----------|------|-------|--------------|
| Brief | `brief.md` | music-brief | Stage 1 brief validation |
| Concept | `concept.md` | hook-writer | `cliche_scan.py`, `prosody_check.py --hook` |
| Structure | `structure.md` | groove | `structure_check.py` |
| Lyrics | `lyrics.md` | verse-writer / lyric-editor | `prosody_check.py`, `rhyme_check.py`, `cliche_scan.py` |
| Chords | `chords.md` | harmony | `chord_tools.py` |
| Melody | `melody.abc` | melody | `abc_validate.py` |
| Arrangement | `arrangement.md` | dynamics | `arrangement_check.py`, `structure_check.py --consistency` |
| Production brief | `production-brief.md` | production-brief | `validate_artifacts.py` (artist-name lint) |
| Panel report | `panel-report.md` | listener-panel | advisory, not gated |
| Adaptation report | `adaptation-report.md` | lyric-adapter / music-adapter | `adapt_check.py` |
| Critique | `critiques/<stage>-<n>.md` | song-critic judges (Template 2) | none (read by the next worker dispatch) |
| Challenge report | `challenge-report.md` | challenger | `challenge_gate.py` |
| Package | `package/` | music-release | `midi_export.py` round trip |
| State | `state.json` | music-flow | hooks (`subagent_gate.py`) |
| Active pointer | `.song/active` | music-flow | hooks |
| Retrospective | `retrospective.md` | music-memory | orchestrator `run_id` check |
| Decisions | `decisions.md` | music-flow | append-only |

## brief.md

YAML front-matter keys: `theme` (required, non-empty), `pov`, `audience`, `genre`, `mood`, `language` (ISO 639-1), `target_length_sec` (integer), `must_include[]`, `must_avoid[]`, `song_type`, `user_asserts_original_input` (boolean; must be true for TOPLINE/REWRITE, and for ADAPT_GENRE/AUGMENT_LYRICS unless `public_domain` is true), `public_domain` (boolean `true|false`; second provenance flag for ADAPT_GENRE/AUGMENT_LYRICS), `public_domain_source` (free text; required when `public_domain: true`), `source_genre`, `target_genre` (genre labels, never artist or song names). Body: `## Brief` (one paragraph) and optional `## Supplied input` (fenced, user-owned).

Example front-matter (one key per line between `---` fences): `theme: moving to a new city and knowing no one yet` / `pov: first person` / `audience: 20s-30s` / `genre: pop` / `mood: upbeat` / `language: en` / `target_length_sec: 180` / `must_include: []` / `must_avoid: [specific city names]` / `song_type: FULL_SONG` / `user_asserts_original_input: false`; then `## Brief` and one paragraph.

## concept.md

YAML front-matter: `title`, `hook_line` (or `motif` for INSTRUMENTAL; exactly one of the two), `central_image`, `arc` (list of three: start, turn, end), `title_rationale`. Optional `## Notes` body.

Example: `title: Nobody Knows My Name Here` / `hook_line: Nobody knows my name here yet` / `central_image: a key that does not fit any door yet` / `arc: [arrive unseen, choose to stay, a stranger says my name]` / `title_rationale: the hook withholds its last word until the chorus lands`.

## structure.md

Header key list (`key`, `mode`, `bpm`, `time_sig`, `form_template`), then one table. `meter_spec` is `syllables/stress` per line, lines separated by `;`, stress as `S`/`u`. `rhyme_scheme` letters are scoped per section; `x` is an unconstrained line (`AxAx`).

```markdown
key: D
mode: major
bpm: 118
time_sig: 4/4
form_template: VCVCBC

| section | label | bars | meter_spec | rhyme_scheme |
|---------|-------|------|------------|--------------|
| 1 | Verse 1 | 8 | 8/uSuSuSuS; 8/uSuSuSuS; 8/uSuSuSuS; 8/uSuSuSuS | ABAB |
| 2 | Chorus | 8 | 7/SuSuSuS; 7/SuSuSuS; 7/SuSuSuS; 8/SuSuSuSu | AABB |
```

## lyrics.md

Section tags exactly matching `structure.md` labels; one lyric line per line; blank line between sections; `# ` comment lines are ignored by gates.

Example: `[Verse 1]` / `I packed the car with everything I own` / `# three more lines follow` / blank / `[Chorus]` / `Nobody knows my name here yet`.

## chords.md

Header `key: <key> <mode>`, then one `[Label]` block per section. Each line is one phrase; one bar per cell between `|`; Roman numerals; `%` repeats the previous cell; concert chords on the next line prefixed `>`.

Example: `key: D major` / blank / `[Verse 1]` / `| I | V | vi | IV |` / `> | D | A | Bm | G |`.

## melody.abc

ABC 2.1, single voice (at most one `V:` line). Headers in order: `X:1`, `T:<title>`, `M:` (equals `structure.md.time_sig`), `L:`, `Q:` (`1/4=<bpm>`), `K:` (equals `structure.md` key and mode). Sections marked by `%%section <Label>` lines. A `w:` line follows each music line when `lyrics.md` exists; tokens `-` (syllable split), `_` (extend previous syllable), `*` (skip note), `~` (join words), `|` (next bar).

```abc
X:1
T:Nobody Knows My Name Here
M:4/4
L:1/8
Q:1/4=118
K:D
%%section Verse 1
D2 F2 A2 F2 | G2 F2 E4 |
w: I packed the car with ev-ery-thing_ |
```

## arrangement.md

Header `key`, `mode`, `bpm`, `time_sig` (identical to `structure.md`), then one table in section order. `energy` is an integer 1-10; `instruments_in` / `instruments_out` are comma-separated lists or `-`.

Columns: `| section | energy | instruments_in | instruments_out | texture_note |`. Example rows: `| Verse 1 | 3 | acoustic guitar, bass | - | sparse, dry vocal |` and `| Chorus | 7 | drums, synth pad | - | wide, doubled vocal |`.

## production-brief.md

Headings `## Tempo map`, `## Vocal treatment`, `## Mix priorities`, `## Section notes`. Technical language only; no artist names, no "sounds like", no reference tracks. Example: `## Vocal treatment` / `Dry lead in verses; stereo doubles plus a 1/8 slap delay in choruses.`

## panel-report.md

One `## <persona>` block per persona with `verdict: KEEP | SKIP`, `top_note:`, `question:`; final line `majority: KEEP | SKIP (n of m)`.

Example: `## casual-radio-listener` / `verdict: KEEP` / `top_note: chorus lands on the first listen` / `question: does verse two need the second image?` / ... / `majority: KEEP (2 of 3)`.

## challenge-report.md

`## Findings` followed by the severity table with exactly these columns; severity in {BLOCKER, MAJOR, MINOR}; `location` is `<artifact>:<section>:<line>` or `<artifact>:<section>`. A header-only table is a clean pass.

Header: `| severity | location | finding | suggested fix |`. Example row: `| MINOR | lyrics.md:Bridge:2 | rhyme too predictable | use a slant rhyme on line 2 |`.

## adaptation-report.md

Written for ADAPT_GENRE at Stage 7. Front-matter: `song_type: ADAPT_GENRE`, `source_genre`, `target_genre`. Sections in order: `## Kept` (bullet list of preserved elements, e.g. hook line, section order), `## Changed` (table with header `| Element | Source | Target | Why |`, one row per change), `## Lyric re-fit` (meter and rhyme deltas per section), `## Risks` (bullets: singability, drift from the source, originality notes). Never quotes lyric text beyond the user's own supplied lines.

Example: `source_genre: folk` / `target_genre: bossa nova` / `## Kept` / `- hook line, section order` / `## Changed` / `| Element | Source | Target | Why |` / `| bpm | 96 | 120 | bossa pulse |` / `## Lyric re-fit` / `- Verse 1: 8/uSuSuSuS -> 7/SuSuSuS; rhyme ABAB kept`.

## package/

`lyric-sheet.md` (title, then `lyrics.md` body), `lead-sheet.abc` (melody with chord symbols as `"D"` annotations), `song.mid` (from `midi_export.py`), `one-pager.md` (title, genre, key, bpm, length, hook line, arc), `release-notes.md` (gates passed, loops used, overrides, panel majority). LYRICS_ONLY and REWRITE produce `lyric-sheet.md` and `release-notes.md` only.

## state.json

```json
{ "run_id": "2026-10-26T14-02-11Z-nobody-knows", "stage": 4, "song_type": "FULL_SONG", "status": "in_progress",
  "quick": false, "loops_used": { "concept": 1, "structure": 0, "lyrics": 1 },
  "gates": { "lyrics": { "status": "FAIL", "metrics": { "verse_2_mismatch_ratio": 0.22 },
             "violations": [ { "location": "Verse 2:3", "reason": "stress mismatch", "observed": 0.22, "limit": 0.15 } ],
             "artifact_sha256": "<hex>", "skipped": false } },
  "gate_overrides": [], "accepted_best": {}, "owners": { "concept.md": "hook-writer", "structure.md": "groove" },
  "started": "2026-10-26T14:02:11Z", "updated": "2026-10-26T14:31:40Z" }
```

Types: `run_id` string (ISO timestamp plus slug; unique per run and per REVISE); `stage` integer 1-7; `song_type` string; `status` one of `in_progress`, `complete`, `failed`; `quick` boolean; `loops_used` map of `concept`, `structure`, `lyrics`, `music`, `arrangement`, `release` to integer; `gates` map stage-name to `{status, metrics, violations, artifact_sha256, skipped}`; `gate_overrides` list of `{stage, run_id, reason, timestamp}`; `accepted_best` map stage-name to boolean; `owners` map artifact filename to role; `started` / `updated` ISO 8601 UTC. `gate_subagent.py` writes only `gates[]`, via temp file and atomic rename.

## .song/active

A single line containing the slug of the run in progress, nothing else (`nobody-knows-my-name-here`). Written by `music-flow` at Stage 1 and at REVISE entry; read by every hook.

## retrospective.md

Front-matter `run_id` equal to `state.json.run_id` (the orchestrator verifies this before completing), `slug`, `genre`, `song_type`, `date`; body per `music-memory/references/retrospective-template.md` (lands in W4-3; loops per stage, most-failed gate, recurring critique, overrides, three next-time notes). Never contains lyric text. Example front-matter: `run_id: 2026-10-26T14-02-11Z-nobody-knows` / `slug: nobody-knows-my-name-here` / `genre: pop` / `song_type: FULL_SONG` / `date: 2026-10-26`.

## decisions.md

Append-only; never rewrite earlier entries. Each entry: `## <ISO timestamp> <kind>` where kind is `debate`, `override`, or `accept_best`, then `stage:`, `decision:`, `rationale:`, and for debates the five rubric scores per option.

Example: `## 2026-10-26T14:40:02Z override` / `stage: lyrics` / `decision: user accepted Verse 2 at mismatch 0.19` / `rationale: heuristic false positive on "every" (two syllables in performance)`.
