# Gate 2 Evaluation, Round 2: BACKLOG-108 Opus 4.8 Migration PRD (Revision 1)

Evaluator: QA Engineer (evaluator only). Artifact: `.delivery/artifacts/02-refine/po/prd.md` (Revision 1). Binding decisions in `.delivery/memory/topics/opus-4-8-migration.md` treated as authoritative. Framing: ACs judged for well-formedness and runnability, not for passing today.

**Verdict: REVISE** (2 blocking defects, 2 warnings; all are narrow and mechanical to fix)

## 1. Gate 2 per-criterion results

| # | Criterion | Sev | Result | Note |
|---|-----------|-----|--------|------|
| 1 | Every FR has AC with testable condition | blocking | PASS | All FRs mapped; process-only FR-2.4, FR-4.4, FR-7.3 tagged inspection with named evidence. Exception: AC-1.2c conflicts with FR-4.1 (D2-1) |
| 2 | NFRs quantified | blocking | PASS | NFR-1..9 numeric with commands; NFR-5 depends on AC-1.2c (D2-1) |
| 3 | Out-of-scope present | blocking | PASS | Sec 10 |
| 4 | Success metrics numeric + method | blocking | PASS | Gates G1..G10, one closing story each |
| 5 | No blocking open questions | blocking | PASS | OQ-1..4 with owner, due, non-blocking rationale |
| 6 | Personas specific | warning | PASS | 3 personas with goal/pain/context |
| 7 | Dependencies w/ status | warning | PASS | Sec 7 |
| 8 | Risks L/I/mitigation | warning | PASS | R1-R5 |
| 9 | Assumptions explicit | suggestion | PASS | 4 assumptions |
| 10 | Discovery numbers accurate (added from round-1 D-11) | blocking | FAIL | "9 hits in 6 files" and "today's AC-1b value is 9" do not reproduce (D2-2) |

## 2. Round-1 defect resolution

| Defect | Status | Evidence |
|--------|--------|----------|
| D-1 FR->AC coverage | RESOLVED | ACs present for all FRs incl. new 5.5, 5.6, 7.4 |
| D-2 NFRs | RESOLVED | NFR-1..9 |
| D-3 Gate ownership | RESOLVED | G1->S1, G-LIT->S4, G6->S3, G8->S7, G9->S6, G10->S7; preconditions separated |
| D-4 AC-DISP | RESOLVED | FR-7.4 defines manifest format; AC-DISP is count + distinct-role python check |
| D-5 Weak ACs | RESOLVED | AC-1.1 per-ID grep, AC-1.2b, AC-3.3a anchored (`opus-4-8-frontmatter-only` fails), CHANGELOG exclusion, walk.py excludes `.claude`/`.delivery`/`.git*` |
| D-6 Open questions | RESOLVED | Sec 9 |
| D-7 Missing sections | RESOLVED | Secs 2, 7 |
| D-8 AC-5 vs schema | RESOLVED | FR-5.5 adds `model`/`effort`; FR-5.1 adds metrics; verified baseline JSON lacks these today, so schema extension is correctly framed |
| D-9 False positives | RESOLVED | AC-2.3 scoped; ran: prints 0 hits outside research-agent |
| D-10 constraints.yml | RESOLVED | `validate_constraints.py` output: "ok: ... is valid against constraints schema", rc=0; entities and invariants present |
| D-11 Discovery numbers | UNRESOLVED (partial) | Stamp numbers now correct (see sec 3). Literal counts still wrong (D2-2) |
| D-12 Body-delta | RESOLVED | AC-3.1 is a machine check over 34 files; parses and is runnable |
| D-13 BINDING-4.4 | RESOLVED | FR-5.6 |

## 3. Command-execution results (worktree root)

| Command / claim | PRD says | Actual | Match |
|---|---|---|---|
| SKILL.md count (walk.py) | 34 | 34 | YES |
| Stamp lines / files | 26 lines in 25 files | 26 / 25 | YES |
| Stamp values | 7 `opus-4-7`, 19 `frontmatter-only` | 7 / 19 | YES |
| prompt-engineer stamp lines | 2 (lines 6, 415) | 2; line 6 `model_awareness: opus-4-7` frontmatter, line 415 column 0 inside yaml fence | YES |
| Unstamped files | 9 | 34 - 25 = 9 | YES |
| `claude-opus-4-7` hits (walk.py, py/md/yml/yaml/txt) | 9 in 6 files (baseline of AC-1b "today's value is 9") | **7 in 4 files** via walk.py (registry:190, arch doc:115, conftest x4, prompt-engineer:368). walk.py skips `.github` (starts with `.git`), so guard yml (2 hits: L23, L39) is not scanned. Guard included = 9 hits in **5** files | NO (D2-2) |
| AC-1.3 claude-CLI grep / `smoke-` count | 0 / 0 | 0 / 0 | YES |
| AC-2.3 hedge scan | 0 | 0 | YES |
| AC-3.1b `frontmatter-only` file count | 0 target | 19 today | well-formed |
| AC-6 `check_skill_budgets.py` | exit 0 | BUDGET CHECK PASSED, 17 files | YES |
| AC-6.1 sha256 diff | MATCH | MATCH | YES |
| AC-5.3 `--effort` in `run_smoke.py --help` | >= 1 after S5 | 0 today; flag absent, `--cost-cap` present | well-formed (S5 adds) |
| AC-5.4 `cost_usd.hard_max` | 3.0 | 3.0 today | YES |
| NFR-3 `wall_clock_seconds.hard_max` | 1800.0 | 1800.0 | YES |
| AC-5.5 baseline keys | needs `model`, `effort` | absent today (keys: schema_version, scenario, sample_status, n_samples, last_captured_*, metrics, deferred_reason) | well-formed (FR-5.5 adds) |
| AC-5.2 pytest availability | pytest | pytest 9.0.3 present; `test_meta.py` exists | YES |
| CHANGELOG `BACKLOG-108` / memory `## Run outcome` | >= 1 after S7 | 0 / 0 today | well-formed |
| `validate_constraints.py` | passes | valid, rc=0 | YES |
| Heredoc/python ACs (walk.py, AC-3.1, AC-3.3a, AC-2.3, AC-1b) | runnable | all execute/parse under python3 stdlib | YES |

## 4. New defects and required fixes

**D2-1 (blocking) AC-1.2c / NFR-5 contradict FR-4.1 (secs 3 S1, S4).** FR-4.1 requires the provenance comment on the same line as the code: `"config": {"model": "claude-opus-4-8"}  # prior: claude-opus-4-7 (retired ...)`. Line 190 of `agent_registry.py` is a code line, so the comment is trailing. The guard's existing provenance exemption only drops lines where `#` is the first non-space character after the `file:lineno:` prefix (see guard L27-L31, `grep -vE '^[^:]+:[^:]+:[[:space:]]*#'`). So the migrated tree contains a line with `claude-opus-4-7` that STALE_RE flags, and AC-1.2c ("0 matches of STALE_RE", NFR-5 "0 false positives") cannot reach 0. AC-1b handles this with an explicit exemption string but AC-1.2c does not. Required fix, pick one and state it: (a) require STALE_RE / guard to exempt lines containing `# prior: claude-opus-4-7 (retired 2026-05-28, BACKLOG-108)`, and add that to FR-1.2 plus AC-1.2a (fixture line with trailing provenance comment MUST NOT be rejected); or (b) make FR-4.1 place the comment on its own preceding line, and update AC-4.1 and AC-1b accordingly.

**D2-2 (blocking) Discovery numbers still wrong (sec 1, AC-1b, D-11 revision claim).** Reproduced count: 7 hits in 4 files through the walk.py reproducer the PRD prescribes; adding the guard yml gives 9 hits in 5 files, not 6. The table has 5 rows = 5 files, and the "(five source sites plus the guard yml = six files...)" sentence contradicts it. The AC-1b line "Today's value is 9" is false because walk.py excludes `.github` (name starts with `.git`), so today's value is 7. Required fix: state 9 hits in 5 files (guard yml included) for the repo-wide census, state that AC-1b baseline via walk.py is 7 (guard yml covered separately by AC-1.2b), delete the "six files" sentences, and note in section 3 that walk.py skips `.github`.

**D2-3 (warning) AC-1.2a portability.** The regex extracted from the guard is applied with Python `re`, but the existing guard uses POSIX classes (`[^[:space:]...]`) and shell quote-splicing (`'"'"'`) inside the pattern. Python `re` treats `[[:space:]]` as a literal character set (silent semantic difference), and a `STALE_RE='...'` single-quoted value cannot contain a single quote. Required fix: add to the FR-1.2 contract that STALE_RE contains no POSIX classes and no single quotes (use `\s` or `[ \t]`, compatible with `grep -P` and Python), or have AC-1.2a run `grep -E "$STALE_RE"` on the fixture via subprocess.

**D2-4 (warning) Diff-based ACs assume worktree branch state.** AC-3.1 and AC-2.1 use `git diff main` including untracked handling note ("untracked new files count as changed") but a plain `git diff main` ignores untracked files; no new SKILL.md files are planned so this is benign. Required fix (optional): delete the parenthetical or state that no SKILL.md is created (avoids a false reassurance).

## 5. Summary

Twelve of thirteen round-1 defects resolved; new FRs 5.5, 5.6, 7.4 and their ACs are well-formed, measurable and runnable. Blocking: D2-1 (AC-1.2c unsatisfiable given FR-4.1 trailing comment) and D2-2 (literal counts and AC-1b baseline do not reproduce; D-11 only partly closed). Fix both and D2-3, then round 3 is a quick re-verify.
