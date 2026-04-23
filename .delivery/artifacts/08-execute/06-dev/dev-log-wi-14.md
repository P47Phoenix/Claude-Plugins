# WI-14 — CI Guard Wiring (Dev Log)

**Story**: WI-14 — Two new GitHub Actions workflows for marker coverage and stale-ID enforcement
**Role**: DevOps (Samwise Gamgee)
**Date**: 2026-04-22
**Skill**: delivery-team:operations
**Task Type**: ci-workflow-authoring

## Summary

Authored two new CI workflows under `.github/workflows/` to enforce the 4.7 migration contract:

1. **`skill-md-header-warn.yml`** (WARNING-ONLY) — surfaces SKILL.md files missing the `model_awareness:` frontmatter marker. Uses `continue-on-error: true` on the detection step so it reports to the job summary without blocking merge.
2. **`stale-model-id-guard.yml`** (BLOCKING) — fails the PR if any `.py` or `.md` outside `.delivery/` contains a stale 4.x dated model ID, while allowlisting canonical family IDs and provenance comments.

Both workflows mirror the structural shape of `workflow-injection-lint.yml` (name / `on:` / `permissions:` / `jobs:` top-level keys) and comply with DEFECT-004 Constraint 6 (no `${{ github.event.* }}` interpolation in any `run:` block).

## Dependencies Honored

- **WI-10 (stale-ID sweep)** — 0 active stale dated IDs; 3 provenance comments in `agentic-flow-builder/scripts/agent_registry.py` preserved. The stale-ID guard's comment-filter (`^[^:]+:[^:]+:\s*#`) exempts these three lines.
- **WI-11 (frontmatter backfill)** — all 17 SKILL.md files now carry the `model_awareness:` marker, so the header-warn workflow runs clean on current HEAD.

## File 1 — `skill-md-header-warn.yml`

**Trigger**: `pull_request` on path `**/SKILL.md`.

**Behavior**:
- Step `header-check` runs `git ls-files '*SKILL.md' ':!:.delivery/*' | xargs grep -L 'model_awareness:'` to list any SKILL.md lacking the marker.
- The step uses `continue-on-error: true`, so even a non-empty list does NOT fail the job.
- When any are missing, the step writes the list to `$GITHUB_STEP_SUMMARY` under a `### SKILL.md files missing model_awareness header` heading and sets `missing=1` in `$GITHUB_OUTPUT`.
- A subsequent `Warn if any missing` step, gated by `if: steps.header-check.outputs.missing == '1'`, emits a `::warning::` workflow command so the warning appears in the PR checks UI.
- When everything is clean, it prints a confirmation line and no warning is emitted.

**Why warning-only, not blocking**: per the WI-14 brief, the marker taxonomy is still maturing; a hard block would slow contributors while we refine the downstream paradigm policy. Blocking is reserved for stale-ID detection (File 2).

**Contents (as written)**:

```yaml
name: SKILL.md header warn

on:
  pull_request:
    paths:
      - '**/SKILL.md'

permissions:
  contents: read

jobs:
  header-warn:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check SKILL.md header coverage
        id: header-check
        continue-on-error: true
        run: |
          set -uo pipefail
          MISSING=$(git ls-files '*SKILL.md' ':!:.delivery/*' | xargs grep -L 'model_awareness:' || true)
          if [ -n "$MISSING" ]; then
            {
              echo "### SKILL.md files missing model_awareness header"
              echo ""
              echo "$MISSING" | while read -r f; do echo "- $f"; done
            } >> "$GITHUB_STEP_SUMMARY"
            echo "missing=1" >> "$GITHUB_OUTPUT"
          else
            echo "All SKILL.md files have the model_awareness header."
          fi
      - name: Warn if any missing
        if: steps.header-check.outputs.missing == '1'
        run: |
          echo "::warning::One or more SKILL.md files are missing the model_awareness header. See job summary."
```

## File 2 — `stale-model-id-guard.yml`

**Trigger**: `pull_request` on paths `**/*.py` and `**/*.md`, with `!.delivery/**` negation to exclude delivery-pipeline artifacts (which legitimately quote historical model IDs in PRDs, reviews, etc.). The exclusion is reinforced in the `git ls-files` pathspec `:!:.delivery/*` so the scan remains clean even if a file matches the path trigger.

**Calibrated regex**: `claude-(opus|sonnet|haiku)-4[-.][^7][^[:space:]"'#]*`

This pattern:
- Matches `claude-opus-4-20250514`, `claude-opus-4-5`, `claude-opus-4-5-<date>`, `claude-opus-4-6`, `claude-opus-4-6-<date>`, `claude-sonnet-4-5-20250929`, `claude-sonnet-4-<date>`, `claude-haiku-4-<date>`, `claude-haiku-4-20250514`.
- Does NOT match `claude-opus-4-7` (the `[^7]` class blocks the canonical 4.7 suffix).
- Does match `claude-sonnet-4-6` and `claude-haiku-4-5-20251001` at the regex level — these are then removed by downstream `grep -vE` allowlist filters.

**Allowlist filters (applied in order)**:
1. `grep -vE 'claude-sonnet-4-6(\b|[^0-9-])'` — exempts the canonical Sonnet family ID (and tolerates trailing word-boundary or non-dash/digit characters).
2. `grep -vE 'claude-haiku-4-5-20251001'` — exempts the canonical dated Haiku ID.
3. `grep -vE '^[^:]+:[^:]+:[[:space:]]*#'` — exempts Python/YAML comment lines (the three provenance comments in `agent_registry.py` preserved by WI-10).
4. `grep -vE '^[^:]+:[^:]+:[[:space:]]*>'` — exempts markdown blockquote lines (safety net for documentation that quotes historical IDs inside `>` blocks).

**Outcome on HEAD**: 0 blocking hits (verified locally — see dry-run results below).

**Failure message**: Human-readable `::error::` with remediation guidance (use canonical family IDs; put historical references in `#` comments or `>` blockquotes).

**Contents (as written)**:

```yaml
name: Stale model-ID guard

on:
  pull_request:
    paths:
      - '**/*.py'
      - '**/*.md'
      - '!.delivery/**'

permissions:
  contents: read

jobs:
  stale-id-guard:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Scan for stale 4.x model IDs
        run: |
          set -uo pipefail
          HITS=$(git ls-files '*.py' '*.md' ':!:.delivery/*' ':!:prd-quality-gate-flow/prd_flows.db' \
            | xargs grep -En 'claude-(opus|sonnet|haiku)-4[-.][^7][^[:space:]"'"'"'#]*' 2>/dev/null \
            | grep -vE 'claude-sonnet-4-6(\b|[^0-9-])' \
            | grep -vE 'claude-haiku-4-5-20251001' \
            | grep -vE '^[^:]+:[^:]+:[[:space:]]*#' \
            | grep -vE '^[^:]+:[^:]+:[[:space:]]*>' \
            || true)
          if [ -n "$HITS" ]; then
            echo "::error::Stale 4.x model IDs detected (Opus 4.5/4.6, Sonnet 4.5-dated, Haiku 4-dated, or retired dated Opus 4)."
            echo "$HITS"
            echo ""
            echo "Fix: replace with canonical family IDs (claude-opus-4-7, claude-sonnet-4-6, claude-haiku-4-5-20251001)."
            echo "If the reference is historical provenance, put it in a '#' comment or '>' blockquote."
            exit 1
          fi
          echo "No stale 4.x model IDs found."
```

## Local Dry-Run Results

### Dry-run 1: Header warn coverage

```
$ git ls-files '*SKILL.md' ':!:.delivery/*' | xargs grep -L 'model_awareness:'
$ echo "exit=$?"
exit=0
```

Empty output. All 17 SKILL.md files carry `model_awareness:` frontmatter (6 keystones + 11 WI-11 backfill). Header warn workflow will print "All SKILL.md files have the model_awareness header." and emit no `::warning::`.

### Dry-run 2: Stale-ID regex (unfiltered)

```
$ git ls-files '*.py' '*.md' ':!:.delivery/*' ':!:prd-quality-gate-flow/prd_flows.db' \
    | xargs grep -En 'claude-(opus|sonnet|haiku)-4[-.][^7][^[:space:]"'"'"'#]*' 2>/dev/null \
    | grep -vE 'claude-sonnet-4-6(\b|[^0-9-])' \
    | grep -vE 'claude-haiku-4-5-20251001'
agentic-flow-builder/scripts/agent_registry.py:148:                # canonical 2026-04-22 — opus-4-7 migration; prior: claude-sonnet-4-5-20250929 (retired)
agentic-flow-builder/scripts/agent_registry.py:173:                # canonical 2026-04-22 — opus-4-7 migration; prior: claude-haiku-4-20250514 (retired)
agentic-flow-builder/scripts/agent_registry.py:189:                # canonical 2026-04-22 — opus-4-7 migration; prior: claude-opus-4-20250514 (retires 2026-06-15 per F-04)
```

Three raw hits — all three are the provenance comments preserved by WI-10 (each line begins with `#`).

### Dry-run 3: Stale-ID regex (fully filtered, i.e. what the workflow actually blocks on)

```
$ git ls-files '*.py' '*.md' ':!:.delivery/*' ':!:prd-quality-gate-flow/prd_flows.db' \
    | xargs grep -En 'claude-(opus|sonnet|haiku)-4[-.][^7][^[:space:]"'"'"'#]*' 2>/dev/null \
    | grep -vE 'claude-sonnet-4-6(\b|[^0-9-])' \
    | grep -vE 'claude-haiku-4-5-20251001' \
    | grep -vE '^[^:]+:[^:]+:\s*#' \
    | grep -vE '^[^:]+:[^:]+:\s*>'
$ echo "exit=$?"
exit=1    # final grep returns 1 when nothing matches → workflow treats as 0 blocking hits
```

Empty output — the comment filter drains the three provenance lines. Workflow exits 0 and prints "No stale 4.x model IDs found."

## Constraint 6 Verification (DEFECT-004 regression guard)

Ran the exact AST-style scanner from `workflow-injection-lint.yml` against both new files:

```
$ for f in .github/workflows/skill-md-header-warn.yml .github/workflows/stale-model-id-guard.yml; do
    python3 [... the DEFECT-004 injection scanner ...] "$f"
  done
CLEAN: .github/workflows/skill-md-header-warn.yml
CLEAN: .github/workflows/stale-model-id-guard.yml
```

Neither workflow contains `${{ github.event.* }}` inside any `run:` block. Confirmed also via `grep`: the only hits for `\$\{\{\s*github\.event\.` in `.github/workflows/` are (1) an escaped error string inside `workflow-injection-lint.yml` itself, and (2) `version.yml` using it in an `env:` block (the safe pattern). No new files introduce the antipattern.

## Dogfood (from execution-PRD)

```
$ test -f .github/workflows/skill-md-header-warn.yml \
    && test -f .github/workflows/stale-model-id-guard.yml \
    && grep -qE '^on:[[:space:]]*$' .github/workflows/skill-md-header-warn.yml \
    && grep -qE '^[[:space:]]+pull_request:' .github/workflows/skill-md-header-warn.yml \
    && grep -qE '^on:[[:space:]]*$' .github/workflows/stale-model-id-guard.yml \
    && grep -qE '^[[:space:]]+pull_request:' .github/workflows/stale-model-id-guard.yml \
    && echo "DOGFOOD_OK"
DOGFOOD_OK
exit=0
```

Passed.

## Trade-Offs

| Decision | Alternative | Why chosen |
|---|---|---|
| Warning-only for header coverage | Hard-block on missing marker | Marker taxonomy is still settling (paradigm tags, routing); a hard block would slow contributors while we refine it. WI-11 already achieved 100 % coverage on HEAD, so the warning exists as a regression tripwire, not a gate. |
| Four-layer allowlist in stale-ID guard | Single "smarter" regex | A single regex that encodes all canonical IDs, comment prefixes, and blockquote prefixes is hard to read and harder to extend. Four chained `grep -vE` filters are each obvious at a glance and easy to adjust when a new canonical family ID lands. |
| `set -uo pipefail` (no `-e`) in the header-warn step | `set -euo pipefail` | With `-e`, `grep -L` returning non-zero when all files match would abort the step before we could evaluate `$MISSING`. Using `|| true` handles that, and dropping `-e` gives us defence-in-depth on the optional step. |
| Bash regex with `grep -vE` chains | Python AST scanner | For 99 % of stale-ID hits, a grep pipeline is fast, portable, and transparent. The injection-lint workflow already demonstrates the Python-embedded-in-YAML pattern; reusing it here would add no precision and cost clarity. |
| `permissions: contents: read` only | Broader GITHUB_TOKEN scopes | Both workflows are read-only scanners. Minimum-privilege aligns with the WI-14 brief and matches `workflow-injection-lint.yml`. |

## Risks and Mitigations

| Risk | Impact | Likelihood | Mitigation |
|---|---|---|---|
| A new canonical family ID (e.g. Haiku 4.7) lands and trips the stale-ID guard | PR false-positive blocks merge | Low (no 4.7 Haiku on radar) | The allowlist is trivially extended with another `grep -vE` line; document the pattern in the dev log (here) and in a follow-up to `.delivery/memory/topics/` when the event actually occurs. |
| Someone introduces a stale ID inside a markdown *code block* without leading `>` | False-negative (guard misses it) | Medium | Acceptable for v1 — code blocks are the obvious place to put legitimate historical examples, and they often need to stay quotable. If the false-negative rate climbs, a future WI can add a code-fence-aware filter. |
| `git ls-files` matches a file whose path contains a newline or backslash | `xargs` misparses the filename | Very low (project has no such filenames) | Consistent with existing `workflow-injection-lint.yml` style; escalate to `-z` / `xargs -0` if a real case appears. |
| Header-warn workflow's `grep -L` returns non-zero when *all* SKILL.md files have the marker | Step "fails" and marks the job red | Low | Handled by `|| true` in the pipeline and `continue-on-error: true` on the step. Job status only flips to warning on real misses. |

## Assumptions

- Existing `workflow-injection-lint.yml` is the canonical template for workflow structure in this repo (confirmed by reading the file).
- Provenance comments in `.py` files always begin with `#` (Python comment) after the `file:lineno:` grep prefix — verified against WI-10 output for `agent_registry.py`.
- The 3 provenance comments preserved by WI-10 are the *only* intentional in-code references to retired dated IDs outside `.delivery/`; any future ones must follow the same `#`-comment or `>`-blockquote convention documented in the failure message.
- The `.delivery/` path exclusion is handled both at the workflow-trigger level (`paths: '!.delivery/**'`) and inside the script via `git ls-files ':!:.delivery/*'`. Double-belt-and-braces is intentional.

## Follow-Up / Open Questions

- None blocking. The two files are committable as-is.
- Optional future work: add a `push` trigger on `main` for the stale-ID guard (mirrors `workflow-injection-lint.yml`). Deferred — the PR trigger is sufficient for WI-14's scope.
- Optional future work: extend the stale-ID regex to also catch historical 3.x IDs (`claude-3-opus-*`, etc.) once 4.7 migration fully settles. Out of scope here.

## Artifacts Produced

- `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/.github/workflows/skill-md-header-warn.yml` (new)
- `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/.github/workflows/stale-model-id-guard.yml` (new)
- `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/.delivery/artifacts/08-execute/06-dev/dev-log-wi-14.md` (this file)
