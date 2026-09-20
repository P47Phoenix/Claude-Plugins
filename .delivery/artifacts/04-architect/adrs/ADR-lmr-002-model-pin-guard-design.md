# ADR-lmr-002: Model-pin guard design (single script, no exemptions, local gate)

- **Status**: Proposed (flips to Accepted when Stage 4 DoD passes)
- **Date**: 2026-09-20
- **Run**: run-2026-05-28-o48m, BACKLOG-108
- **Owner**: Solution Architect (PRD S1, FR-1.1 to FR-1.6, BINDING-0.3, BINDING-5.1, BINDING-5.2)

## Context

The current guard `.github/workflows/stale-model-id-guard.yml` is a `pull_request`-only, paths-filtered workflow with an inline shell regex, a positive allowlist of three IDs, and `#` and `>` exemptions (verified by reading the file). It fails on the wrong thing (unlisted IDs rather than pins), needs an edit on every release, and never runs on the ship path, because ship is a direct push to `main` with no PR (BINDING-5.1). CI runners have no `claude` CLI (memory: feedback_claude_code_local_only), so the guard is a static scan.

The PRD already decided the shape (Decisions Already Made: one script, five constants, scope via `git ls-files`, no exemptions, marker banned, push trigger plus local strict run). This ADR records the design rationale, the boundary cases the design must hold, and what the implementer must not change. It builds on the PRD; it does not reopen it.

## Decision

**D1. One definition point.** `scripts/check_model_pins.py` (stdlib only, same style as `scripts/check_skill_budgets.py`) defines `PIN_RE`, `STAMP_RE`, `PROSE_RE`, `BARE_RE`, `COUNT_RE` as module-level string constants and a `files()` generator. It scans only under `if __name__ == "__main__":`, so `importlib` can load it for AC-1.2a with no side effect. The values are copied verbatim from PRD FR-1.2 (`COUNT_RE` included). The workflow, hook, ship gate and AC snippets all call this script; no other file contains a pattern.

**D2. Rule order and classification** (must match the canonical command in PRD section 1, line for line):
1. A line matching `PIN_RE` (case-insensitive) is category `pin`.
2. Else a line matching `STAMP_RE` (case-insensitive) is `stamp`.
3. Else, for `.md` files only: blank `COUNT_RE` matches with a single space, then a match of `PROSE_RE` (case-sensitive) or `BARE_RE` (case-insensitive) is `prose`.
4. One category per line; a file is counted once per hit line.

**D3. Scope** = `git ls-files --cached --others --exclude-standard`, filtered to existing regular files (`os.path.isfile`), extensions `.py .md .yml .yaml .txt .sh`, excluding `CHANGELOG.md` and everything under `.delivery/`. It is the same file set as the canonical count, so the ship gate and the count cannot disagree. Untracked files count before `git add`. Nested git worktrees (this repo keeps some under `.claude/worktrees/`) appear as non-files and are skipped by `isfile`. `.json` is out of scope by design, because baselines record the observed model ID and the fixture file holds strings that are pins.

**D4. No exemptions of any kind.** No comment, blockquote, heading or code-fence exemption; no per-line marker. The string `model-pin-ok` is not honoured anywhere (AC-1.6a, AC-1.6b). A legitimate hit is reworded (PRD wording rule). Counts and durations are handled by `COUNT_RE` blanking only.

**D5. CLI contract**: no args scans the scope; `--paths <file>...` scans the named files with the same extension, `CHANGELOG.md` and `.delivery/` filters (a named file outside the repository is scanned); `--list` prints `category file:line` per hit before the summary; `--help` exits 0; the last stdout line is `guard-scope hits <N> files <M>`; exit status 1 when N is above 0, else 0. Output is sorted by file then line so it is deterministic.

**D6. Fixtures** live in `scripts/model_pin_fixtures.json` (JSON is outside the scan). Five keys and provenance rules as in AC-1.2a. AC-1.2a runs every fixture through both engines (`re` and `grep -E`/`sed -E`), so the patterns must stay in the portable subset (no lookaheads, no `(?`, no POSIX classes, no `#` or single quote in a value).

**D7. Workflow** `stale-model-id-guard.yml` is rewritten to: `on: push (branches: main), pull_request, workflow_dispatch`, no `paths:` filter; one job that checks out and runs `python3 scripts/check_model_pins.py`. It contains no ID, no pattern and no `${{ github.event.* }}` inside `run:` (keeps `workflow-injection-lint.yml` green). It adds no `pip install` (NFR-8) and no `claude` invocation (AC-1.3). Honest limit: on `push` the workflow detects after the push; it cannot block it.

**D8. Local gates** (blocking gate = the local run):
- **Pre-commit hook** (`.githooks/pre-commit`, opt-in via `core.hooksPath`): staged-file mode, advisory by default, blocking when `MODEL_PIN_STRICT=1`. The hook runs under `set -euo pipefail`, so the call is written to tolerate zero staged files, deleted paths, and a non-zero exit. Reference implementation (the developer may adapt style, not behaviour):
  ```bash
  staged="$(git diff --cached --name-only --diff-filter=ACMR)"
  if [ -n "$staged" ] && [ -f scripts/check_model_pins.py ]; then
    echo "pre-commit: model-pin guard (staged files)..."
    pin_rc=0
    printf '%s\n' "$staged" | tr '\n' '\0' | xargs -0 python3 scripts/check_model_pins.py --paths || pin_rc=$?
    if [ "$pin_rc" -ne 0 ]; then
      if [ "${MODEL_PIN_STRICT:-0}" = "1" ]; then echo "pre-commit: MODEL PIN VIOLATION - commit blocked." >&2; exit 1; fi
      echo "pre-commit: model-pin hits above are advisory (set MODEL_PIN_STRICT=1 to block)." >&2
    fi
  fi
  ```
  Placement: after the existing budget and known-debt checks, before the final `budget + lint OK.` line. Missing `python3` or script warns and skips, like the existing checks. The `[ -n "$staged" ]` test replaces GNU-only `xargs -r`, so it behaves the same on BSD. Known limit: `--paths` reads the working-tree file, not the index, so a partly staged file is judged by its full working copy (stricter, never looser).
- **Ship gate** (S7, mandatory, strict): `python3 scripts/check_model_pins.py` must print `guard-scope hits 0 files 0` with `exit=0` before the push, and its `--list` line count must equal the canonical command's hit count (R12 equivalence).
- **Recommended addition, needs PO confirmation at Plan (not silently added to the PRD)**: an opt-in `.githooks/pre-push` that runs the script strictly, so the ship-time control is mechanical for anyone who installed the hooks. Without it the S7 report line `check_model_pins.py exit=0` is the sole control (Architect DoD round-2 F5).

**D9. Self-scan and documentation rule.** The script, the workflow and every `.md` written by S1 (governance notes, docstring examples, README text) must themselves pass the guard, so they contain no version examples; docstrings and docs use synthetic IDs (`claude-opus-fixture`). Checked: the five constants do not match their own source text (`PIN_RE` needs a digit or `-latest` directly after the `claude-` run, and the source has `[` there). S5 additions (`tests/test_model_capture.py`, smoke README) are inside the scan scope and must derive model strings from the fixture or use synthetic IDs, never literals.

## Alternatives rejected

| Alternative | Why rejected |
|---|---|
| Keep the positive allowlist of approved IDs | Needs an edit on every release, which is the defect being removed. It also stores IDs in the guard (NFR-11). |
| Patterns inline in the workflow YAML | Two definition points (workflow and local), no local ship gate, and the YAML would contain pins as pattern text. |
| `pull_request`-only trigger | Never runs on a direct push to `main` (BINDING-5.1). |
| Comment, blockquote and fence exemptions | They let a pin hide under `# claude-opus-5 setup` or `> claude-opus-4-7 was retired`. Revision 3 had that hole (F3/F4). History belongs in `CHANGELOG.md`. |
| Per-line marker such as `model-pin-ok` | Asymmetric: allowlisted in the script but banned at ship, so it could not be used and CI could not enforce the ban. Removed in Revision 5. |
| Scope `git ls-files` (tracked only) | A new file would be scanned only after staging, and the count would differ from the ship gate. |
| Semantic or AST detection of "model reference" | Adds a parser dependency, cannot cover Markdown prose, and the repo needs a tripwire, not a proof. |
| Scan `.json` too | Baselines legitimately record the concrete observed model; fixtures need pin strings. |
| Fail on any digit next to any family word ("Opus 4 agents") | The COUNT_RE filter exists because those are real sentences. |

## Consequences

- Guard scan wall clock is well under NFR-13 (the PRD measured 0.5 s for the canonical command).
- **Accepted loopholes**, recorded (the guard is a tripwire, not a proof): string concatenation of an ID; a pin inside a `.json` file; a version in words; a real version phrased in a COUNT_RE form ("Opus 4 agents"); and, from the QA round-2 probes, separator variants such as `claude_opus_4_7`, `OPUS_4_7`, `claude opus 5`, `claude.opus.5`, tab or NBSP between family and digit. The architect recommends leaving the patterns as the PRD wrote them (FR-1.2 says the developer copies them verbatim); PO decides at Plan whether to add `_` and `.` to the separator class and the underscore forms to the fixtures.
- **Accepted false-positive classes** (remedy: reword): hyphen-digit tool names such as `claude-plugins-v2`, and bare decimals with major 4 to 9 after a context word ("on 6.8 kernels", "with 4.7 V rail", "the 4.7 uF cap"). Hardware-team prose is the likeliest source. Risk R4 is therefore Medium for `hardware-team/`, not Low; the S1 dispatch runs the guard over the whole tree and reports any such hit before S1 closes (the tree scan today shows none in `hardware-team/`, which is why the PRD count is 91 hits in 31 files).
- S1 to S3 WIP commits touching unmigrated files would fail a strict hook, which is why the hook is advisory by default. From S1 until S4 the tree holds hits by design; the workflow on a pushed branch is expected red until S4 lands, which is why the ship squashes S1 to S7 into one push (BINDING-2.1).
- The hook is opt-in, so a contributor without `core.hooksPath` gets no local signal. The ship gate does not depend on it.

## Status rationale

Proposed until Stage 4 DoD passes; then Accepted. No contingency clauses.
