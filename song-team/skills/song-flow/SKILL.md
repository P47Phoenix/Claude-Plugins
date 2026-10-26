---
name: song-flow
description: Song-creation pipeline orchestrator that coordinates the song team through 7 stages (Brief, Concept, Structure, Lyrics, Music, Arrangement, Release) with song-type auto-detection, deterministic script gates, evaluator-optimizer loops, listener panel, adversarial challenger, and self-learning memory. Triggers on phrases like "write a song", "song pipeline", "make me a song", "compose a song", "full song", "song from scratch", "revise the song".
license: Apache License 2.0 - See repository LICENSE file
tier: A
maintainer: song-team-leads
fitness_review_due: 2027-01-24
context_budget: 500
allowed-tools: [Read, Write, Edit, Bash, Agent, Skill]
---

# song-flow

## Design Principle

The orchestrator coordinates; sub-agents write the song. Eight invariants, elaborated with
rationale and an anti-pattern catalog in `song-team/references/shared/orchestrator-doctrine.md`:

1. **Never write the song.** No title, hook line, lyric line, chord, or note is written in the main context. Dispatch a worker; record its result.
2. **Context isolation by role and genre.** One role file, one contract, one genre file, at most two techniques per sub-agent, per `references/shared/prompt-allowances.json`.
3. **Evaluator-optimizer at every F stage.** Worker produces, script measures, critic interprets, worker revises, up to `loops.<stage>`.
4. **Adversarial re-verification before release.** A clean-context challenger attacks the final artifacts (lands in W3-4; see the banner below).
5. **Deterministic gates.** Scripts decide PASS/FAIL. Sub-agents never self-certify. Only the user overrides, and the override is recorded.
6. **One gate runner.** The stage protocol step 4 is the only place a gate result decides a loop.
7. **Everything on disk.** Every artifact lives under `.song/<slug>/`; `state.json` is rewritten after every dispatch.
8. **Budgeted files.** This file is Tier A (500 lines). Depth lives in `references/`.

The orchestrator's only write paths are `.song/active`, `.song/<slug>/state.json`,
`.song/<slug>/decisions.md`, `.song/<slug>/attempts/` (copies, for accept_best), and, in
this wave only, the two stand-ins named in the banner below (`package/`, `retrospective.md`).

> **Thin slice (Wave 3).** This revision runs **`LYRICS_ONLY` end to end**: Stages 1, 2,
> 3-light (`composer:groove`, one dispatch), 4, and 7-light (lyric sheet plus release notes).
> **Every other song type** (`FULL_SONG`, `INSTRUMENTAL`, `TOPLINE`, `REWRITE`, `JINGLE`,
> `REVISE`) runs Stage 1, writes `state.json` with `status: "blocked_wave"`, prints
> `> This song type (<TYPE>) lands in Wave 4 (Stages 5-6 in W4-1, full orchestrator). Stage 1 brief is saved at .song/<slug>/brief.md; nothing else runs.`
> and stops. `PARODY_ADAPT` is refused inside `song-brief` and never reaches this file.
> **Stages 5 (Music) and 6 (Arrangement) land in W4-1**; the composer's `harmony` and
> `melody` roles and the arranger exist but this file does not yet dispatch them.
> Not in this wave: hooks (`hooks/` is empty; every gate runs from step 4), `song-memory`
> lessons (the block is `(none)`), the listener panel, the challenger, `song-release`.
> Two stand-ins are therefore performed by the orchestrator and are flagged inline:
> the **package** (Stage 7, replaced by `song-release` in W4-3) and a **minimal
> retrospective** (post-pipeline, replaced by `song-memory` in W4-3).

The orchestrator **reasons from six shared files** loaded when triggered:
`orchestrator-doctrine.md`, `stage-gates.md`, `song-types.md`, `config-schema.md`,
`artifact-formats.md`, `originality-policy.md`, all under `song-team/references/shared/`,
plus this skill's `references/stage-protocol.md` and `references/package-thin-slice.md`
at the stage that needs them. It opens any other reference file (role, contract, genre,
technique, rubric, prompt template) **only to paste it into a prompt**, and keeps nothing
else in its working context.

---

## Phase 0: Setup and Resume

Run this phase on every trigger, before any dispatch.

**Plugin root.** `PLUGIN` = `$CLAUDE_PLUGIN_ROOT` when set; otherwise the directory three
levels above this SKILL.md (`song-team/`), always as an absolute path (shell examples in
`references/stage-protocol.md` section 0). Every gate command is
`python -I "$PLUGIN/scripts/<gate>.py" --json --config .song/config.yml <artifacts>` run
from the **project root** (the absolute directory that holds `.song/`; it also fills
`{project_root}` in every prompt).

**1. Active-run check.** Read `.song/active`. When it names a slug and
`.song/<slug>/state.json` exists, read `status`:

| `status` | Action |
|----------|--------|
| `in_progress` | Announce `> Existing run found: <run_id>, <song_type>, at Stage <stage>, updated <updated>.` Verify every artifact named in `owners` exists on disk; name any that is missing. Offer **Resume** / **Restart** / **Abandon**. |
| `blocked_wave` | Announce the Wave 4 message again and offer **Restart** (a fresh brief) / **Abandon**. |
| `failed` | Announce `> Failed run found at Stage <stage> (<policy> policy).` Offer **Resume** (re-enter that stage with the counter reset to 0) / **Restart** / **Abandon**. |
| `complete` | Not a blocker for a new song. When the new request is a **change request** (the `REVISE` signals in `song-types.md`: "make the chorus punchier", "slower bridge", "swap verse two"), print the blocked-type banner with `<TYPE>` = `REVISE` and **stop here, before `song-brief` is invoked**, so the finished run is never overwritten (`state.json` and `.song/active` untouched). Otherwise proceed to a new run. |

- **Resume**: keep `run_id`; set `stage` from the file; **re-run that stage's gate** on the
  artifact on disk before dispatching anything (protocol step 4); PASS skips to the next stage.
- **Restart**: move `.song/<slug>/state.json` to `.song/<slug>/state-archive/state-<timestamp>.json`
  (keep at most 5, delete the oldest); artifacts stay; start at Stage 1 with a new `run_id`,
  invoking `song-brief` with `reuse_slug: <slug>` so it writes into the same directory
  instead of appending `-2`.
- **Abandon**: delete `.song/active`; set `status: "failed"` with `updated` now; stop. No stage runs.

Never start a second run while one is `in_progress`. A missing `.song/active` or a slug
with no `state.json` means no active run: proceed.

**2. Config.** `.song/config.yml` is created by `song-brief` in Stage 1 when absent, so
Phase 0 reads it only when it exists. Validate the keys this wave consumes: `quick`,
`loops.concept`, `loops.structure`, `loops.lyrics`, `escalation.on_loop_exhaustion`,
`routing.force_type`. A missing key takes the default from
`references/shared/config-schema.md`; a non-numeric loop cap or an unknown policy value is
announced and replaced by its default for this run (the file is never edited).

**3. Quick-mode detection.** Quick mode is on when `quick: true` in config **or** the
request contains the phrase "quick song". Effects for the whole run, in memory only:

- every `loops.<stage>` cap is treated as **1** (`release` included);
- `escalation.on_loop_exhaustion` is treated as **`accept_best`**;
- the `song-brief` wizard asks at most **2** questions (song-brief enforces this itself from the same signals);
- `state.json.quick` is recorded as `true`.

Print the quick-mode banner from `## Declarations` when it is on.

---

## Stage execution protocol

The thin slice runs this protocol at Stages 2 and 4 in full and at Stage 3 as a light
stage (F for the types W4-1 unblocks). `references/stage-protocol.md` carries the exact commands, JSON snippets, and the
`ask_user` dialogue text; `stage-gates.md` section 4 is the normative source.

**Step 1: Read state.** Load `.song/config.yml` and `.song/<slug>/state.json`. Resolve
the cap for this stage (`loops.<stage>`, or 1 in quick mode) and the escalation policy.

**Step 2: Build and dispatch the worker.** The orchestrator dispatches the sub-agent
itself with the **Agent tool** (never the Skill tool, which would run the worker inline
and put craft files into this context):

1. Open the worker's prompt template: `song-team/skills/lyricist/references/agent-prompts/<hook|section|revision>.md`,
   `song-team/skills/composer/references/agent-prompts/groove.md` (`harmony.md` and `melody.md` from W4-1),
   or `song-team/skills/song-critic/references/agent-prompts/<hook-judge|prosody-judge|structure-judge>.md`.
   The orchestrator builds and dispatches every sub-agent prompt itself; a worker
   SKILL.md's Dispatch Protocol is what that worker performs when invoked standalone.
2. Fill every `{placeholder}` with the file contents the template's table names and
   nothing else. Count embedded `references/` files against `prompt-allowances.json`:
   lyricist and composer roles use its `defaults` entry (1 role, 1 contract, 1 genre, 2 techniques);
   judges use their named entries (`hook-judge`, `prosody-judge`, `structure-judge`: 1
   rubric, 1 technique). Over-allowance is a prompt bug; fix the prompt, never trim the policy.
   Scalar placeholders: `{project_root}` = the absolute project root; `{genre}` and
   `{song_type}` from `brief.md`; `{title}` = `concept.md.title` once Stage 2 has passed,
   `brief.md.theme` before that. Every template carries the sentence "Write only the
   artifact path given; read no file outside this prompt; run no script."; keep it.
3. Paste the fenced clause of `originality-policy.md` verbatim under `<!-- originality-policy -->`.
4. Write `(none)` under `<!-- memory-lessons -->` (lessons arrive with W4-3).
5. Resolve the genre: `brief.md.genre` lower-cased with spaces as `-`; `pop` when no
   `genres/<g>.md` exists for the worker (say so in the declaration).
6. Call `Agent` with `subagent_type: "lyricist"`, `"composer"`, or `"song-critic"` and the built prompt.
   One role per dispatch; never two roles in one prompt; never two workers on one artifact in parallel.

**Step 3: Receive the hand-back.** Parse `SKILL_LOADED:`, `STATUS:`, `ARTIFACT:`,
`SUMMARY:`. A missing `SKILL_LOADED:` line is a warning, not a failure. `STATUS: BLOCKED`
skips the gate and goes to Step 5 with the `SUMMARY` as the reason. Confirm the artifact
exists at the path the stage expects; a missing artifact is treated as BLOCKED.

**Step 4: Gate decision (single runner).** No hook populates `state.json.gates` in this
wave, so always run the stage's script(s) from the project root:

```bash
python -I "$PLUGIN/scripts/<gate>.py" --json --config .song/config.yml .song/<slug>/<artifact> [...]
```

Parse the JSON of every script. The stage status is the worst status in the severity
order `ERROR > FAIL > SKIPPED > PASS` (ERROR counts as FAIL for loop purposes). Compute the
artifact hash and write `state.json.gates[<stage>]`: the top-level `status`, `metrics`,
`violations` are the merged worst-status view; `results` keeps each script separately
(keyed by script name); `scripts` lists the invocation strings, `"prosody_check --hook"`
for hook mode:

```bash
python -I -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" .song/<slug>/<artifact>
```

```json
"gates": { "<stage>": { "status": "PASS|FAIL|SKIPPED|ERROR", "metrics": {}, "violations": [],
  "artifact_sha256": "<hex>", "skipped": false, "scripts": ["cliche_scan", "prosody_check --hook"],
  "results": { "cliche_scan": { "status": "PASS", "metrics": {}, "violations": [] },
               "prosody_check --hook": { "status": "PASS", "metrics": {}, "violations": [] } } } }
```

Print one gate line per script (see `## Declarations`). Then:

- **PASS**, or **SKIPPED** (non-English `language`): set `skipped: true` when any script
  skipped, log it, and proceed as PASS to Step 6.
- **FAIL** at an F stage: dispatch the stage's critic (`subagent_type: song-critic`) with
  every script's JSON in `## Gate evidence`; it writes `.song/<slug>/critique-<stage>.md`.
  Reject and re-dispatch the critic once when a `## Findings` row cites a location absent
  from the JSON. Then copy the failing artifact to `.song/<slug>/attempts/<artifact>.<n>`,
  increment `loops_used.<stage>`, write `state.json`, and re-dispatch the worker with the
  song-critic hand-off block pasted into `## Critique to address`:

```text
## Critique to address (if any)
Gate: <gate_script> <gate_status> (loop <n> of <cap>)
<verbatim gate JSON, one object per script that ran>

<verbatim contents of critique-<stage>.md from "## Findings" to end of file>
```

  Return to Step 3. **Loop accounting:** `loops_used.<stage>` counts worker re-dispatches
  after a FAIL; the first dispatch is loop 0. A cap of 0 escalates on the first FAIL.
- **FAIL** at an L stage: no critic, no re-dispatch; go to Step 5 at once.

**Step 5: Escalation.** When the stage is still FAIL and `loops_used.<stage>` equals the
cap (or the worker returned BLOCKED), apply `escalation.on_loop_exhaustion`:

| Policy | Behaviour |
|--------|-----------|
| `ask_user` | Print the last three attempts (status, worst violation, violation count), the gate diff between the last two, and any `## Suspected false positives` rows from the critique. Options: **accept** (keep the last attempt; `accepted_best[<stage>] = true`), **override** (gate marked passed; append `{stage, run_id, reason, timestamp}` to `gate_overrides[]` and an `override` entry to `decisions.md`), **guidance** (one user instruction added to the next worker prompt under `## Critique to address`; `loops_used.<stage>` resets to 0 once per stage per run). Exact dialogue text: `references/stage-protocol.md` section 5. |
| `accept_best` | Among the attempts in `attempts/` plus the one on disk, keep the one with the fewest violations, then the lowest worst ratio (`max` of `*_mismatch_ratio`, else `per_100_words`); restore it if it is not the file on disk; set `accepted_best[<stage>] = true`; append an `accept_best` entry to `decisions.md`; proceed. |
| `fail` | Set `status: "failed"`, `updated` now; write `state.json`; print `RUN FAILED at Stage <n> (<name>): loop cap <cap> reached under policy fail.`; stop. |

Quick mode always resolves to `accept_best` here. A gate that passed is never escalated.

**Step 6: Advance.** Set `stage` to the next stage the routing matrix allows for the
song type, `updated` to now (UTC `YYYY-MM-DDTHH:MM:SSZ`), add `owners[<artifact>]`, write
`state.json` whole (never a partial edit), print the next stage banner.

---

## Stage 1: Brief

Stage 1 runs **inline**: invoke `song-team:song-brief` with the **Skill tool** (it is an
intake wizard, not a creative worker, so inline is correct here). It creates
`.song/config.yml` when absent, detects the song type, runs the wizard (at most 2 questions
in quick mode), refuses `PARODY_ADAPT`, and writes `.song/<slug>/brief.md`. It returns the
brief path, its declaration line, and the asked-versus-inferred list.

Then, and only then, the orchestrator:

1. Reads `song_type`, `genre`, `language` from `brief.md`; the slug is the directory name.
2. Writes `.song/active` containing the slug and nothing else (single line).
3. Creates `.song/<slug>/state.json` with the full key set from `artifact-formats.md`:

```json
{ "run_id": "<started with ':' replaced by '-'>-<slug>", "stage": 1, "song_type": "LYRICS_ONLY",
  "status": "in_progress", "quick": false,
  "loops_used": { "concept": 0, "structure": 0, "lyrics": 0, "music": 0, "arrangement": 0, "release": 0 },
  "gates": {}, "gate_overrides": [], "accepted_best": {}, "attempts": {},
  "owners": { "brief.md": "song-brief" },
  "started": "2026-10-26T14:02:11Z", "updated": "2026-10-26T14:02:11Z" }
```

   `run_id` example: started `2026-10-26T14:02:11Z` and slug `half-the-island-looks-away`
   give `2026-10-26T14-02-11Z-half-the-island-looks-away`. `attempts` is an additive key
   (map of stage to a list of `{n, sha256, violations, worst_ratio}`) used by `accept_best`.
4. Prints the type banner and, when `routing.force_type` is set, the override banner.
5. Routes: `LYRICS_ONLY` continues to Stage 2. Any other type: set `status: "blocked_wave"`,
   `updated` now, write `state.json`, print the Wave 4 message from the thin-slice banner,
   and stop. (`song-brief` already refused `PARODY_ADAPT` before any directory existed.)

`force_type` pins routing only; detection still runs inside `song-brief` and both values
appear in the banner. A `force_type` naming `REVISE` is ignored with a one-line warning.

---

## Stage 2: Concept

| Item | Value |
|------|-------|
| Worker | `lyricist:hook-writer`, template `agent-prompts/hook.md`, `subagent_type: lyricist` |
| Artifact | `.song/<slug>/concept.md` (`title`, `hook_line`, `central_image`, `arc`, `title_rationale`) |
| Gates | `cliche_scan.py concept.md brief.md`; `prosody_check.py --hook concept.md brief.md` |
| Critic | `song-critic:hook-judge`, template `agent-prompts/hook-judge.md`, writes `critique-2.md` |
| Re-dispatch | `hook-writer` again (`hook.md`) with the critique block; `{title}` is the previous `concept.md` title |
| Cap | `loops.concept` (default 3; quick 1) |
| Owner | `owners["concept.md"] = "hook-writer"` |

On the first dispatch `{title or brief theme}` is `brief.md.theme` and `{critique}` is
`(none)`. The stage passes when both scripts return PASS or SKIPPED.

---

## Stage 3: Structure

| Item | Value |
|------|-------|
| Worker | `composer:groove`, template `song-team/skills/composer/references/agent-prompts/groove.md`, `subagent_type: composer` |
| Depth | **F** for `FULL_SONG`, `INSTRUMENTAL`, `JINGLE`; **L** for `LYRICS_ONLY`, `REWRITE`; **I** for `TOPLINE` (one dispatch derives the section list and bars from the user's chord chart in `brief.md`; the gate validates that derived structure, no critic) |
| Inputs | `brief.md`; `concept.md` (absent for `REWRITE`; carries `motif` for `INSTRUMENTAL`) |
| Artifact | `.song/<slug>/structure.md`: five header lines (`key`, `mode`, `bpm`, `time_sig`, `form_template`), blank line, the section table |
| Gate | `structure_check.py structure.md` |
| Critic | `song-critic:structure-judge`, template `agent-prompts/structure-judge.md`, writes `critique-3.md` (F stages only) |
| Re-dispatch | `groove` again (`groove.md`) with the critique block; the role rewrites the file whole |
| Cap | `loops.structure` (default 2; quick 1) |
| Owner | `owners["structure.md"] = "groove"` |

Rules specific to this stage:

- **Hook line.** The groove role writes Chorus line 1's `meter_spec` entry as the syllable
  count and stress pattern of `concept.md.hook_line`, counted by hand per
  `composer/references/techniques/rhythmic-feel.md` (the rules `prosody_check.py` applies).
  The orchestrator verifies the entry before recording the gate, with the one-liner
  `python -I -c "import sys; sys.path.insert(0, r'<PLUGIN>/scripts'); import prosody_check as p; h='<hook_line>'; print(len(p.stress_pattern(h)), p.stress_pattern(h))"`
  (`<n> <pattern>`); a mismatch is pasted into `## Critique to address` as
  `Gate hook_meter MISMATCH: structure.md Chorus line 1 <entry>, hook line <n>/<pattern>` and
  counts one loop (L stages: escalate per Step 5). Never edit `structure.md` in the main context.
- `concept.md` is mandatory for every type except `REWRITE`; when it is missing, return to
  Stage 2 rather than dispatching.
- At an L or I stage a FAIL skips the critic and goes to Step 5 at once (`stage-gates.md` section 4).
- `brief.md.user_asserts_original_input` must be `true` for `REWRITE` and `TOPLINE`;
  otherwise stop and relay the `song-brief` policy sentence.

---

## Stage 4: Lyrics

| Item | Value |
|------|-------|
| First dispatch | `lyricist:verse-writer`, template `agent-prompts/section.md`, `subagent_type: lyricist` |
| Artifact | `.song/<slug>/lyrics.md`; `[Label]` tags identical to `structure.md`, one line per meter line |
| Gates (all four) | `prosody_check.py lyrics.md structure.md brief.md`; `rhyme_check.py lyrics.md structure.md brief.md`; `cliche_scan.py lyrics.md brief.md`; `structure_check.py structure.md lyrics.md` (line counts per section) |
| Critic | `song-critic:prosody-judge`, template `agent-prompts/prosody-judge.md`, writes `critique-4.md`; receives every Stage 4 script's JSON |
| Re-dispatch | `lyricist:lyric-editor`, template `agent-prompts/revision.md`, with the previous `lyrics.md`, the critique block, and the loop text `loop <n> of <cap>` |
| Cap | `loops.lyrics` (default 4; quick 1) |
| Owner | `owners["lyrics.md"] = "verse-writer"` on the first pass, `"lyric-editor"` after any accepted revision |

Rules specific to this stage:

- `structure.md` and `concept.md` are mandatory inputs; when either is missing, go back to
  the stage that owns it rather than dispatching.
- The stage passes only when all four scripts return PASS or SKIPPED. `structure_check.py`
  is never SKIPPED; `prosody_check.py` and `rhyme_check.py` SKIP for non-English lyrics.
- **Hook line.** `verse-writer` must use `concept.md.hook_line` verbatim as Chorus line 1
  (the groove role derived the Chorus meter line 1 from it). If `lyric-editor` changes that line,
  song-flow updates `concept.md.hook_line` to the new text, re-runs both Stage 2 gates
  (recorded under `gates.concept`), and appends a `## <now> hook_line` entry to `decisions.md`.
- A `structure_check.py` **FAIL or ERROR** (tag or line-count problem) skips the critic:
  re-dispatch `verse-writer` (`section.md`) straight away with the gate JSON in
  `## Critique to address`; it counts one loop.
- A `rhyme_check.py` or `prosody_check.py` **ERROR** (tag mismatch, scheme length mismatch)
  still dispatches `lyric-editor` with the ERROR JSON; when the editor returns BLOCKED
  naming a structural defect, re-dispatch `verse-writer` (`section.md`) once before
  escalating. The BLOCKED hand-back plus that one re-dispatch together count one loop.
- Never edit `lyrics.md` in the main context, not even to fix one tag.

---

## Stage 7: Release (light, LYRICS_ONLY)

The challenger (7b) lands in W3-4 and `song-release` in W4-3. For the thin slice the
orchestrator assembles the package itself. **This is allowed**: assembling a package copies
finished artifacts and tabulates `state.json`; it writes no new creative content. Formats
are in `references/package-thin-slice.md`.

1. `challenge_gate.py` is **not run** in Wave 2 (the challenger lands in W3-4): print
   `Gate challenge_gate: not run (W3-4)`, write **no** `gates.release` entry, and let the
   release-notes row read `not run (W3-4)`.
2. Write `package/lyric-sheet.md`: `# <concept.md title>`, blank line, then the `lyrics.md`
   body byte-for-byte minus `# ` comment lines.
3. Write `package/release-notes.md`: front-matter (`run_id`, `slug`, `song_type`, `quick`),
   a gates table (one row per `results` key of every `state.json.gates` entry), a loops
   table (every stage in `loops_used` against its effective cap), and the overrides /
   accept_best list (or `(none)`).
4. Set `stage: 7`, `status: "complete"`, `updated` now, `owners["package/"] = "song-flow (thin slice)"`;
   write `state.json`. Leave `.song/active` in place (REVISE reads it in W4-4).

**Post-pipeline (stand-in for `song-memory`, replaced in W4-3).** Write
`.song/<slug>/retrospective.md` so the future Stop hook (`run_id` match) is satisfied:

```markdown
---
run_id: <state.json.run_id>
slug: <slug>
genre: <brief.md.genre>
song_type: LYRICS_ONLY
date: <YYYY-MM-DD>
---
# Retrospective (thin slice)
| stage | loops_used | cap | gate |
|-------|------------|-----|------|
| concept | <loops_used.concept> | <effective cap> | <gates.concept.status> |
| ... one row per key of loops_used, in that order ... |
Overrides: (none). Accept_best: (none).
```

`cap` is the **effective** cap (`loops.<stage>` from config, or 1 in quick mode), never a
hard-coded number; stages with no gate entry show `-`. No lyric text ever enters this file. W4-3 replaces it with the full template and the
`.song/memory/<date>-<slug>.md` lessons file. Then print the completion banner.

---

## Declarations

Print these lines verbatim (placeholders filled) so a transcript reads like a log:

| When | Line |
|------|------|
| After Stage 1 | `> Song type: <TYPE> \| Matched row: <signal> \| Pin: <none \| force_type> \| Quick: <true \| false> \| Slug: <slug> \| Run: <run_id>` |
| `force_type` set | `> ROUTING OVERRIDE: routing.force_type: <TYPE> is set in .song/config.yml; detected <DETECTED>, routing as <TYPE>.` |
| Quick mode on | `> QUICK MODE: every loop cap = 1, on_loop_exhaustion = accept_best, wizard <= 2 questions (source: <config \| phrase>).` |
| Blocked type | `> This song type (<TYPE>) lands in Wave 4 (Stages 5-6 in W4-1, full orchestrator). Stage 1 brief is saved at .song/<slug>/brief.md; nothing else runs.` |
| Stage start | `## Stage <n>: <name> (<F \| L \| I>) — worker <role> — cap <cap>` |
| Each dispatch | `> Dispatch: <role> \| subagent_type <lyricist \| composer \| song-critic> \| genre <g> \| refs <n> files \| artifact <path>` |
| Each gate | `Gate <script>: PASS \| FAIL \| SKIPPED \| ERROR (<metric>=<value>, ...; violations <count>)` |
| Each loop | `> Loop <n>/<cap> at Stage <n>: critic <role> -> worker <role>` |
| Escalation | `> ESCALATION at Stage <n>: policy <ask_user \| accept_best \| fail>` then the policy's text |
| Resume | `> Existing run found: <run_id>, <song_type>, at Stage <stage>, updated <updated>.` |
| Complete | `> COMPLETE: <slug> \| package/lyric-sheet.md, package/release-notes.md \| loops concept <n> structure <n> lyrics <n> \| overrides <count>` |

Metrics in the gate line: `cliche_scan` -> `per_100_words`; `prosody_check --hook` ->
`hook_syllables`; `prosody_check` -> the worst `*_mismatch_ratio`; `rhyme_check` ->
`pairs_checked`, `slant_pairs`; `structure_check` -> `sections`, `total_bars`;
`challenge_gate` -> `blocker`, `major`, `minor`.

---

## Guardrails

- **Never write lyrics, hook, title, structure, chords, or notes inline.** "It is only one
  line" is the most common violation. The package copy and the retrospective are the two
  documented exceptions in this wave; each is flagged where it occurs and each is scheduled
  for removal. Verifying the hook meter one-liner at Stage 3 is a check, not a write.
- **One gate runner.** Step 4 is the only place a script result decides a loop. No hook
  runs in this wave; when W4-2 adds `gate_subagent.py`, Step 4 reuses its result on hash
  match and re-runs the script otherwise.
- **No hooks in this wave.** `hooks/` stays empty. `audit_agent_prompt.py` is not present,
  so the allowance count and the originality clause are the orchestrator's responsibility
  at Step 2.
- **Agent tool for workers, Skill tool for song-brief only.** Invoking `lyricist`,
  `composer`, or `song-critic` through the Skill tool loads craft files into the main
  context and runs the worker inline: a principle 2 violation.
- **Standalone worker invocation warns, never denies.** A worker triggered outside this
  pipeline prints its own warning and proceeds; its output is not gated.
- **Routing is single-sourced** in `references/shared/song-types.md`. This file names no
  second matrix; the thin-slice banner is a wave gate, not a routing rule.
- **Critique format is fixed.** The `## Critique to address` block is pasted exactly as
  `song-critic` specifies; the gate JSON is never summarised.
- **state.json is rewritten whole** after every dispatch, gate, loop, escalation, and
  stage advance, with `updated` refreshed each time. Never a partial edit.
- **PARODY_ADAPT** never reaches this file; if a brief slips through with that type, stop,
  delete nothing, and relay the `song-brief` refusal sentence.
- **Memory lessons are `(none)`** until W4-3; never read `.song/memory/` here.

## References

- `references/stage-protocol.md` — commands, `state.json` snippets, sha256 one-liner, `ask_user` dialogue (L2)
- `references/package-thin-slice.md` — `lyric-sheet.md` and `release-notes.md` formats; superseded in W4-3 (L2)
- `song-team/references/shared/` — doctrine, stage gates, song types, config schema, artifact formats, originality policy (L1)
- `song-team/skills/lyricist/references/agent-prompts/`, `song-team/skills/composer/references/agent-prompts/`, `song-team/skills/song-critic/references/agent-prompts/` — prompt templates filled at Step 2
