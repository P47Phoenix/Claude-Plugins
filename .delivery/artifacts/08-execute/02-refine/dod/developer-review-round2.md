# Developer DoD Review — Round 2 (Refine, Light Mode)

**Validator:** Gimli (blunt, developer role)
**Artifact:** `.delivery/artifacts/08-execute/02-refine/po/execution-prd.md`
**Round:** 2 of max 3
**Scope:** Re-verify G-1 (blocking). Spot-confirm G-2..G-6 (non-blocking). Confirm no new blockers.
**Language:** Bash (dogfood commands) | Task: review | Reference: references/languages/bash.md | Clean Code: default

---

> *"And my code! The last command pretended `yq` was a birthright. This round I ran the new one. It fell on the axe of `test -f`, not on `command not found`. That is the difference between a dwarf's tool and a wizard's excuse."*
> — Gimli

---

## Executive Verdict

**G-1 FIXED.** The revised WI-14 dogfood command is pure `grep -qE` + `test -f`. Ran it. Exit code was **1**, with output of **nothing** — the exact failure mode the spec wanted: "file not found, not command not found." No `yq` anywhere in the command. The two workflow files do not yet exist (correct — this is the Refine stage, not the implementation run), so `test -f` exits non-zero on the first file, and the short-circuit chain returns 1. That is a *semantic* failure, not a *dependency* failure. G-1 is dead. Good.

**G-2..G-6 all applied.** Spot-checked every one against the revised file. Each maps cleanly to a numbered §9 Revision Log entry and an in-place edit in the corresponding WI or AC. No phantom claims.

**No new blockers introduced.** 14 stories still present. Wave distribution 3/3/3/5 = 14, matches roadmap. DAG still acyclic (read all 14 `Depends on:` lines; no back-edges, no cycles). §3 carry-items still bound to specific WI+AC. §7 six verification commands still parse and execute (three currently return AS-IS state, which is correct — they're end-state gates for the impl-run, not the Refine run).

**VERDICT: DONE.**

---

## Gate A — G-1 Fix Verification (BLOCKING gate, the whole point of round 2)

### The new command (from WI-14 Dogfood block, lines 381–382)

```bash
test -f .github/workflows/skill-md-header-warn.yml \
  && test -f .github/workflows/stale-model-id-guard.yml \
  && grep -qE '^on:[[:space:]]*$' .github/workflows/skill-md-header-warn.yml \
  && grep -qE '^[[:space:]]+pull_request:' .github/workflows/skill-md-header-warn.yml \
  && grep -qE '^on:[[:space:]]*$' .github/workflows/stale-model-id-guard.yml \
  && grep -qE '^[[:space:]]+pull_request:' .github/workflows/stale-model-id-guard.yml
```

### Actual execution (bash, from repo root)

| Observation | Value |
|---|---|
| Exit code | **1** |
| stderr | (empty) |
| stdout | (empty) |
| `command -v yq` | exit 1 (not installed — the original blocker) |
| `command -v grep` | exit 0 (installed; aliased `grep --color=auto`) |
| Failure mode | First `test -f` returns 1 (file does not yet exist). Short-circuit ends. No `command not found`. No exit 127. |

### Ruling

| Check | Pass? |
|---|---|
| Command contains zero references to `yq` | YES |
| Command uses only `test -f` and `grep -qE` | YES |
| `grep` is a POSIX/standard shell built-in/coreutil (no install required) | YES |
| Failure on missing workflow file is "file not found" (exit 1), not "command not found" (exit 127) | YES |
| AC-1 intent preserved: both workflow files exist check | YES (`test -f ... && test -f ...`) |
| AC-1/AC-2 intent preserved: `pull_request:` trigger present in both | YES (two `grep -qE '^[[:space:]]+pull_request:'`) |

**G-1 is FIXED.** No round 3 needed on this finding.

---

## Gate B — G-2..G-6 Non-Blocker Application Check (spot-verified)

| Finding | Claim in §9 Revision Log | Actual edit verified at | Applied? |
|---|---|---|---|
| **G-2** | WI-11 `**/SKILL.md` shell-glob replaced with `find … -name SKILL.md -not -path …` idiom | WI-11 AC-3 (line 293), AC-6 (line 296), "So that" narrative (line 288). Only surviving `**/SKILL.md` occurrence in the whole PRD is inside the §9 Revision Log entry itself, which quotes the old broken pattern for audit. | YES |
| **G-3** | WI-09 `awk` vacuous-pass trap replaced with `test "$(grep -cE …)" -ge "6"` | WI-09 dogfood line 248: `test "$(grep -cE '^- +(Weakness\|Referent\|Alternative)' ...)" -ge "6"`. Zero `awk` occurrences in the entire file. | YES |
| **G-4** | WI-12 AC-1a format binding added (markdown table, `Theme` column, ≥3 rows) | WI-12 AC-1a at line 318. Binds `alias-theme-sample.md` to a table format and pins the existing `grep -cE '^\| *(Theme\|theme) '` as the mechanical check. | YES |
| **G-5** | WI-05 AC-7 broadens single-line retarget of `research-agent/references/prompt-library.md:10` to close §7.4 | WI-05 AC-7 at line 143. Out-of-Scope block at line 148 carries the explicit single-line exception. | YES |
| **G-6** | WI-03 `grep -cE` swapped for `grep -qE` | WI-03 dogfood at line 94: `grep -qE '^(verdict\|Verdict): *(unknown-fields-accepted\|strict) *$' ...`. No `grep -cE` in WI-03. | YES |

All five non-blockers applied cleanly. None regressed into a new blocker. Revision Log (§9) is present, enumerated G-1..G-6, each with an "applied 2026-04-22" stamp and a one-line edit summary.

---

## Gate C — No-New-Blockers Spot Check

### 14 stories still present

```
grep -cE "^### Story WI-[0-9]+" → 14  ✓
```

### Wave distribution matches transformation-plan §6.2

| Wave | Count | WIs |
|---|---|---|
| 1 | 3 | WI-01, WI-02, WI-03 |
| 2 | 3 | WI-04, WI-05, WI-06 |
| 3 | 3 | WI-07, WI-08, WI-09 |
| 4 | 5 | WI-10, WI-11, WI-12, WI-13, WI-14 |
| **Total** | **14** | |

Matches roadmap. No silent re-waving.

### DAG acyclicity

Read all 14 `Depends on:` lines. Checked for back-edges:

| WI | Depends on | Wave | Dependency wave |
|---|---|---|---|
| WI-01 | — | 1 | — |
| WI-02 | — | 1 | — |
| WI-03 | — | 1 | — |
| WI-04 | 01, 02, 03 | 2 | 1, 1, 1 |
| WI-05 | 01, 02, 03 | 2 | 1, 1, 1 |
| WI-06 | 01, 02 | 2 | 1, 1 |
| WI-07 | 05 | 3 | 2 |
| WI-08 | 05 | 3 | 2 |
| WI-09 | 02 | 3 | 1 |
| WI-10 | 02 | 4 | 1 |
| WI-11 | 04, 05, 06, 07, 08, 09 | 4 | 2, 2, 2, 3, 3, 3 |
| WI-12 | 02 | 4 | 1 |
| WI-13 | 02 | 4 | 1 |
| WI-14 | 10, 11 | 4 | 4 (parallelisable — see WI-14 line 367) |

All dependencies point backward (lower-wave or earlier-same-wave parallelisable peers). Acyclic. Intra-wave-4 dep WI-14 → WI-10/WI-11 is explicit in the parallelisable clause and §5 Wave 4 gate ordering. No cycle.

### Carry-items (§3) still bound

| Carry-item | Bound to | Verified? |
|---|---|---|
| MID-04 | WI-10 AC-5 (AC-01.5) | YES (line 270, line 392) |
| Keystone AC unevenness | WI-07 AC-1, WI-08 AC-1, WI-09 AC-2 | YES (lines 192, 217, 242, 393) |
| AC-03B.2 hardening | WI-06 AC-2, WI-06 AC-3 | YES (lines 165–169, 394) |
| Label drift | WI-11 AC-2, WI-11 AC-6 | YES (lines 292, 296, 395) |

No carry-item regressed into new work.

### §7 six verification commands still parse and execute

All six commands were executed against the current repo state. They all **parse** (shell accepts them) and **execute** (return exit codes, not syntax errors). Present end-state values are expected AS-IS values for a Refine run that has not yet implemented the waves:

| # | Command | AS-IS exit / output | Interpretation |
|---|---|---|---|
| 7.1 M-01 | `! grep -rEn 'claude-(opus-4-20250514\|sonnet-4-5-20250929\|haiku-4-20250514)' ...` | 3 hits in `agent_registry.py` lines 148, 172, 187 | Expected — WI-10 has not yet run. Target: 0 hits post-WI-10. Command parses. |
| 7.2 DX-M4 | `find ... \| xargs grep -L 'model_awareness:' \| wc -l` | `17` | Expected — WI-04..WI-11 have not yet run. Target: 0 post-WI-11. Command parses. |
| 7.3 two-tier stamp | `test "$(...grep -l '^model_awareness: opus-4-7$' ... \| wc -l)" = "6" && test "... opus-4-7-frontmatter-only$ ... = "11"` | exit 1 | Expected — stamps not yet applied. Target: exit 0 post-WI-11. Command parses. |
| 7.4 DX-M3 | `grep -rn '<thinking>' ... \| grep -v 'prompt-engineer/SKILL.md' \| wc -l` | `1` | Expected — WI-05 AC-7 retarget has not yet run. Target: 0 post-WI-05. Command parses. |
| 7.5 dual-write | local-file count vs gh-issue count | local: 0 | Expected — WI-13 has not yet run. Target: both ≥6 and equal post-WI-13. Command parses. |
| 7.6 CI guards | `test -f skill-md-header-warn.yml && test -f stale-model-id-guard.yml && test -f workflow-injection-lint.yml` | exit 1 (only `workflow-injection-lint.yml` exists) | Expected — WI-14 has not yet run. Target: exit 0 post-WI-14. Command parses. |

**The DoD gate is "the verification commands parse and execute" — not "the end-state values are already met."** All six pass that gate.

### Spot check: no phantom edits or accidental scope expansion

| Spot check | Result |
|---|---|
| WI-13 dual-write section §4 still enumerates the six required topics + three time-permitting topics | YES (lines 405–414) |
| No WI-13 count drift (count still ≥6, not renegotiated) | YES (line 356 dogfood, line 468 §7.5) |
| No new REQ/AC/ADR anchor introductions — all story PRD-anchors still cite existing upstream artifacts | YES |
| `STATUS: DONE` signal at bottom of PRD (line 511) — PO self-signed | YES |

No new blockers. No regressions.

---

## Findings Table

| # | Finding | Severity | Applied? | Blocking? |
|---|---|---|---|---|
| G-1 | `yq` dependency removed from WI-14 dogfood; pure `grep -qE`/`test -f` now | **BLOCKING (round 1)** | FIXED | No (closed) |
| G-2 | WI-11 shell-glob replaced with portable `find ... \| xargs grep` idiom | non-blocking | YES | No |
| G-3 | WI-09 `awk` vacuous-pass trap eliminated | non-blocking | YES | No |
| G-4 | WI-12 AC-1a format binding added (markdown table + pin) | non-blocking | YES | No |
| G-5 | WI-05 AC-7 broadens to close §7.4 `<thinking>` retarget | non-blocking | YES | No |
| G-6 | WI-03 `grep -cE` → `grep -qE` | cosmetic | YES | No |

Zero blocking findings remain. Zero new blockers introduced.

---

## Signal

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/08-execute/02-refine/dod/developer-review-round2.md
SUMMARY: And my code! G-1 dies clean on `test -f` not `command not found`. G-2..G-6 all applied. Fourteen stories stand. Ship it.
```
