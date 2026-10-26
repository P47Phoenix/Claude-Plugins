---
loaded_by: song-flow
level: L2
last_reviewed: 2026-10-26
---

# Stage protocol runbook (thin slice)

Operational restatement of `references/shared/stage-gates.md` section 4 with the exact
commands and `state.json` snippets; `stage-gates.md` is normative, this file is how.
## 0. Locate the plugin root

`PLUGIN` is `$CLAUDE_PLUGIN_ROOT` when set; otherwise the directory three levels above
this SKILL.md (`song-team/`). Resolve it to an **absolute** path once per run:

```bash
PLUGIN="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "<path to song-flow/SKILL.md>")/../.." && pwd)}"   # Git Bash
```
```powershell
$PLUGIN = if ($env:CLAUDE_PLUGIN_ROOT) { $env:CLAUDE_PLUGIN_ROOT } else { (Resolve-Path "<path to song-flow/SKILL.md>\..\..\..").Path }   # PowerShell
```

Every gate call below runs from the **project root** (the absolute directory that holds
`.song/`), which is also the value of `{project_root}` in every prompt. Gate scripts
identify artifacts **by basename** (`lyrics.md`, `structure.md`, `brief.md`), so a copy
under `attempts/` (`lyrics.md.2`) must be restored to its real name before it is gated.

## 1. Dispatch a worker (Agent tool, never the Skill tool)

1. Read the worker's `agent-prompts/<task>.md` (lyricist: `hook`, `section`, `revision`;
   song-critic: `hook-judge`, `prosody-judge`, `structure-judge`). The orchestrator builds
   the prompt itself; the worker's own Dispatch Protocol applies only when invoked standalone.
2. Substitute every `{placeholder}` with file contents. Embed exactly the files that
   prompt's table lists: lyricist roles follow the `defaults` entry of
   `references/shared/prompt-allowances.json` (1 role, 1 contract, 1 genre, 2 techniques);
   judges follow their named entries (1 rubric, 1 technique). Count before dispatching.
   Scalars: `{project_root}` = absolute project root; `{genre}`, `{song_type}` from
   `brief.md`; `{title}` = `concept.md.title` after Stage 2, else `brief.md.theme`. The
   sentence "Write only the artifact path given; read no file outside this prompt; run no
   script." is part of every template and stays.
3. Paste the fenced clause from `references/shared/originality-policy.md` under
   `<!-- originality-policy -->`. Write `(none)` under `<!-- memory-lessons -->` (W4-3).
4. Genre: `brief.md.genre`, lower-cased, spaces to `-`; `pop` when no genre file exists.
5. Call `Agent` with `subagent_type` = `lyricist` or `song-critic` and the built prompt.
6. Parse the hand-back: `SKILL_LOADED:`, `STATUS:`, `ARTIFACT:`, `SUMMARY:`. A missing
   `SKILL_LOADED` line is a warning only. `STATUS: BLOCKED` goes straight to step 5 below.

## 2. Run the gate(s)

```bash
# Stage 2
python -I "$PLUGIN/scripts/cliche_scan.py"    --json --config .song/config.yml .song/<slug>/concept.md .song/<slug>/brief.md
python -I "$PLUGIN/scripts/prosody_check.py"  --json --config .song/config.yml --hook .song/<slug>/concept.md .song/<slug>/brief.md
# Stage 3
python -I "$PLUGIN/scripts/structure_check.py" --json --config .song/config.yml .song/<slug>/structure.md
# Stage 4 (all four; the prosody-judge receives every one's JSON)
python -I "$PLUGIN/scripts/prosody_check.py"  --json --config .song/config.yml .song/<slug>/lyrics.md .song/<slug>/structure.md .song/<slug>/brief.md
python -I "$PLUGIN/scripts/rhyme_check.py"    --json --config .song/config.yml .song/<slug>/lyrics.md .song/<slug>/structure.md .song/<slug>/brief.md
python -I "$PLUGIN/scripts/cliche_scan.py"    --json --config .song/config.yml .song/<slug>/lyrics.md .song/<slug>/brief.md
python -I "$PLUGIN/scripts/structure_check.py" --json --config .song/config.yml .song/<slug>/structure.md .song/<slug>/lyrics.md
```

`challenge_gate.py` is not run in Wave 2 (W3-4). Exit codes: 0 PASS, 1 FAIL, 2 SKIPPED,
3 ERROR. Keep the full stdout JSON of every script; critic and worker receive it verbatim.
Severity order `ERROR > FAIL > SKIPPED > PASS`; ERROR is FAIL for loop purposes, and its
`violations[0].reason` is shown in the gate line.

## 3. Record the gate

```bash
python -I -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" .song/<slug>/lyrics.md
```

Top-level `status` is the worst status across the stage's scripts; top-level `metrics`
and `violations` are the merged view (script name prefixed where keys collide); `results`
keeps each script separately; `scripts` lists invocation strings (`"prosody_check --hook"`):

```json
"gates": { "lyrics": { "status": "FAIL", "metrics": { "chorus_mismatch_ratio": 0.22, "pairs_checked": 12, "per_100_words": 0.0 },
  "violations": [ { "location": "Chorus:2", "reason": "stress mismatch", "observed": 0.22, "limit": 0.15 } ],
  "artifact_sha256": "5bfd00eb...", "skipped": false,
  "scripts": ["prosody_check", "rhyme_check", "cliche_scan", "structure_check"],
  "results": { "prosody_check": { "status": "FAIL", "metrics": { "chorus_mismatch_ratio": 0.22 }, "violations": [ { "location": "Chorus:2", "reason": "stress mismatch", "observed": 0.22, "limit": 0.15 } ] },
               "rhyme_check": { "status": "PASS", "metrics": { "pairs_checked": 12 }, "violations": [] }, "cliche_scan": { "...": "..." }, "structure_check": { "...": "..." } } } }
```

`skipped: true` only when every script returned SKIPPED or PASS and at least one SKIPPED.
Then set `updated` to now (UTC, `YYYY-MM-DDTHH:MM:SSZ`) and rewrite `state.json` whole.
Release notes derive their per-script rows from `results`.

## 4. FAIL -> critic -> worker

0. Stage 4 only: when `results.structure_check.status` is FAIL or ERROR, skip the critic
   and re-dispatch `verse-writer` (`section`) with the gate JSON; this counts one loop.
1. Dispatch the critic (`subagent_type: song-critic`) with the gate JSON in
   `## Gate evidence`; artifact `.song/<slug>/critique-<stage>.md`.
2. Reject and re-dispatch once when a `## Findings` row lacks a location present in the JSON.
3. Build the worker re-dispatch (`hook` for Stage 2, `revision` for Stage 4; `section`
   once more when the lyric-editor returned BLOCKED naming a structural defect, the
   BLOCKED hand-back and that re-dispatch together counting one loop) with this exact
   block in the `## Critique to address` slot:

```text
## Critique to address (if any)
Gate: <gate_script> <gate_status> (loop <n> of <cap>)
<verbatim gate JSON, one object per script that ran>

<verbatim contents of critique-<stage>.md from "## Findings" to end of file>
```

4. Increment `loops_used.<stage>` **before** the re-dispatch, write `state.json`, dispatch, return to section 2.

## 5. Escalation (`loops_used.<stage>` == cap, still FAIL)

`cap` is `loops.<stage>` from config, or 1 in quick mode. Policy is
`escalation.on_loop_exhaustion` (quick mode: `accept_best`).

**ask_user** prints this and waits:

```text
STAGE <n> (<name>) LOOP CAP REACHED: <used>/<cap>
Last attempts (newest first):
  attempt <k>: <script> <status>  worst: <location> <reason> observed <v> limit <l>  (violations: <count>)
  attempt <k-1>: ...   attempt <k-2>: ...
Gate diff (attempt <k-1> -> <k>): <metric>: <old> -> <new> ; violations <old> -> <new>
Suspected false positives (from critique-<stage>.md): <rows or "none">
Options:
  accept   - keep attempt <k> as is; recorded as accepted_best[<stage>] = true
  override - mark the gate passed; recorded in gate_overrides[] and decisions.md (give a one-line reason)
  guidance - give one instruction; the stage counter resets to 0 once and the worker is re-dispatched
```

`override` appends `{ "stage": "<stage>", "run_id": "<run_id>", "reason": "<text>", "timestamp": "<now>" }`
to `gate_overrides[]` and `## <now> override` / `stage:` / `decision:` / `rationale:` to
`decisions.md`. `guidance` is honoured once per stage per run; a second exhaustion offers
only `accept` and `override`.

**accept_best**: among the attempts listed in `state.json.attempts[<stage>]` (one entry
per failed dispatch: `{n, sha256, violations, worst_ratio}`, file copy at
`.song/<slug>/attempts/<artifact>.<n>`) plus the artifact on disk, keep the one with the
fewest violations, then the lowest `worst_ratio`; copy it back over the artifact when it is
not the one on disk; set `accepted_best[<stage>] = true`; append `## <now> accept_best` to
`decisions.md`.

**fail**: set `status: "failed"`, write `state.json`, print `RUN FAILED at Stage <n>`, stop.

## 6. Advance

Set `stage` to the next stage the matrix runs, `updated` to now, add the `owners` entry for
the artifact just accepted, write `state.json`, print the next stage banner.
