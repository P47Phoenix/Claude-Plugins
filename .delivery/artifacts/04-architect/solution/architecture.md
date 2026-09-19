# Architecture: model ID refresh + positive-allowlist guard

Stage 4 | LIGHT | FEATURE | Role: solution | Model: opus
SKILL_LOADED: delivery-team:architect

## 1. Domain Discovery

PO interview not run at LIGHT depth. PRD section 3 (9 answered questions) and `constraints.yml` (BC-01..BC-14) substituted for it. Risk: PRD answers not stress-tested live; mitigated by FR-9 live-doc gate (BC-13). No gaps found that need human escalation.

## 2. Prior Art Analysis

PRD is user-provided spec. Read in full. Elements classified:

| Spec element | Class | Rationale |
|---|---|---|
| Allowlist = 4 exact IDs, whole-token | Decision Already Made | BC-02 |
| Token regex, delimiter rule, `#`/`>` line-start exemption | Decision Already Made | FR-6/FR-7; QA prototype |
| Scan surface 7 globs, excludes `.delivery/`, prd_flows.db, guard file | Decision Already Made | FR-8 |
| One atomic commit, no dual-allow | Decision Already Made | BC-03 |
| Fable allowlisted, not adopted | Decision Already Made | BC-07 |
| cache-prefix-hash not re-frozen | Decision Already Made | BC-10 |
| Exact script text | Open Question | PRD says "adopt or improve" |
| Allowlist maintenance mechanics, rollout/rollback | Open Question | Designed below |

No deviation from any decision. No technical blocker found.

## 3. Guard design

Runs as `steps[1]` of job `stale-id-guard`. Static: `git ls-files | xargs grep | grep | sed | grep`. No network, no `claude` CLI (BC-01), GNU grep (BC-05), no `github.event` (BC-06).

Pipeline (verified script at `/tmp/arch-g.sh`, same body as PRD section 12):

1. **File set**: `git ls-files '*.py' '*.md' '*.yml' '*.yaml' '*.json' '*.txt' '*.sh'` minus pathspecs `.delivery/*`, `prd-quality-gate-flow/prd_flows.db`, `.github/workflows/stale-model-id-guard.yml`. Tracked files only, so untracked scratch never trips CI.
2. **Find**: `grep -EnH "$TOK"`. `TOK` matches `claude-<family>-<digit>...` where family in opus|sonnet|haiku|fable|mythos; tail cannot end `.`/`,`/`-`.
3. **Provenance exempt**: drop lines matching `^file:N:\s*[#>]`. Only line-start comment or blockquote. Mid-line trailing `# prior:` on code NOT exempt (BC-04).
4. **Strip allowed**: `sed -E "s/claude-($ALLOW)($D)/<OK>\2/g"`. `$D` = end of line, char outside `[-A-Za-z0-9.]`, or `.` then non-alnum. So `claude-opus-5-20260101` and `claude-opus-5.1` are NOT stripped (delimiter fails).
5. **Re-grep**: any leftover `claude-<family>-<digit>` = violation, print, exit 1.

Single-source allowlist: `ALLOW='fable-5-1|opus-5|sonnet-5|haiku-4-5-20251001'` (prefix-less tails; `claude-` supplied by sed). Nothing else in the workflow names an ID except the human-facing error text, which must be phrased generically (say "see ALLOW in this file") so one edit rolls over. Comment block in the workflow describing the set is also in the excluded file; keep it to one line.

### Verified this run

Reference script on the CURRENT (un-migrated) tree exits 1 and lists exactly the 10 live sites (agent_registry.py:149,190; smoke-test-architecture.md:115,116; telemetry-schema.md:36; conftest.py:105,117,129,151; prompt-engineer/SKILL.md:368). Provenance `#` lines in agent_registry.py (148,173,189) are exempt. So post-migration the set is empty and guard passes. Scan set is 515 tracked files (324 tracked under `.delivery/` are excluded).

## 4. Failure modes / false positives

| Case | Behaviour | Handling |
|---|---|---|
| Historic ID in prose (non-comment line) | FAIL | Move to own `#`/`>` line. Intended. |
| Trailing comment on code line | FAIL | Intended (BC-04); put provenance on own line |
| JSON containing retired ID | FAIL (no comments in JSON) | Intended (Q7) |
| Alias `claude-haiku-4-5` | FAIL | Intended (Q6); one spelling |
| ID split across lines / string concat | Not detected | Accepted; static grep limit |
| ID with trailing `.` or `,` in prose | PASS if allowed token | `$D` rule |
| CHANGELOG.md history with old IDs | Would FAIL if not `#`/`>` | Currently zero hits; new Unreleased entry must use only allowed IDs or a blockquote for retired ones. Dev must run guard on final tree |
| Guard's own ALLOW/comment | Excluded by pathspec | Risk: an ID typo in the guard is unscanned; covered by FR-6 injection ACs |
| ADR/architecture docs under `.delivery/` | Excluded | none |
| Other `.github/workflows/*.yml` naming IDs | Scanned | none today (zero hits) |
| `xargs` with empty list | grep runs on stdin edge | not reachable; 515 files |
| Very long file lists | xargs batches; `-H` keeps prefix so `^file:N:` parse holds for single-file batches | -H is mandatory |

Filename containing `:` would break the prefix parse; none tracked, accepted.

## 5. Rollover on next model release

One place: the `ALLOW=` line in `stale-model-id-guard.yml`. Procedure: (1) change the four tails or add one, (2) edit the sites (grep tells you: guard fails on every old literal, which doubles as the to-do list), (3) update `on.paths` only if globs change (no), (4) one atomic commit. Adding a family not in `TOK` (e.g. a new brand) requires editing `TOK` too; `mythos` and `fable` are pre-seeded. Haiku 4-5 retirement (not before 2026-10-15, QA F-6) is the next expected rollover. Keep provenance breadcrumb `# prior:` per gate-patterns lesson: comments and guard allowlist are a named pair, edit one, review the other.

## 6. Interaction with smoke fixtures and telemetry

- `conftest.py` (4 sites) and `smoke-test-architecture.md` (2) and `telemetry-schema.md` (1) are fixtures/examples. No test asserts the literal (PRD Q2). They are scanned, so a future fixture with a non-allowlisted ID fails CI: desired, fixtures stay honest.
- Fixture edits are a separate hunk from harness logic (BINDING-4.5, FR-4); since it is one commit, keep them as distinct hunks and verify by FR-4 diff AC.
- Telemetry schema: doc example only; field definitions untouched. Runtime telemetry emits whatever model the harness reports; the guard does not see runtime data.
- Baseline `pytest delivery-team/tests/smoke/tests -q` = 3 passed must hold.

## 7. cache-prefix-hash status

`governance/cache-prefix-hash.txt` is already stale (PRD section 7: recorded `43067c9e...` vs current `0a7aa92f...`). This change does not touch `delivery-flow/SKILL.md`, so it neither causes nor fixes the drift. No CI reads the file. Deferred to BACKLOG-B. Because this ADR does not alter any cached-prefix file, the "Dev runs-the-command" memory rule reduces to: Dev runs FR-10 AC2 (`git diff --name-only` shows no delivery-flow/SKILL.md) as proof.

## 8. Rollout order and rollback

Constraint: BC-03 no dual-allow; CI runs on PR head, and every pushed commit is evaluated.

Options: (A) staged (literals first, guard second) or (B) guard first. Both intermediate states are red or mixed:
- Guard first: new guard runs against old literals, FAIL.
- Literals first: old guard (deny-regex, allows 4-6/4-7 only) sees `claude-opus-5`; regex `4[-.][^7]` does not match `-5`, so it would PASS, but nothing enforces the new set and the old allowlist is still live. That is the mixed state BC-03 forbids.

Decision: **single commit** carrying all ten literal edits, the two provenance-comment edits, the guard rewrite and the CHANGELOG entry (FR-11). Every commit on the branch is then either pre-change (old guard + old literals, green) or post-change (new guard + new literals, green). Only one commit is ahead of origin (`git rev-list --count origin/delivery-team-agent-wrappers..HEAD` = 1 before push; the earlier `chore: delivery pipeline artifacts` commit is already in origin or excluded via `.delivery/`). Dev may split working edits locally but must squash before push.

Pre-push checks (Dev runs, records in dev-notes): guard script on final tree exits 0; injection matrix from FR-6/7/8; `pytest` 3 passed; `check_skill_budgets.py` 0; skill-development loaded for prompt-engineer edit.

Merge gate: `model-id-verification.md` exists with all four IDs (FR-9). If live docs contradict, change ALLOW and sites in a new atomic commit before merge (no dual-allow).

Rollback: `git revert <shipping commit>` restores old literals AND old guard together (atomicity makes revert whole). No data, config schema or runtime state involved. If only the guard misbehaves in CI (false positive), forward-fix `ALLOW`/`TOK` in the workflow file; do not relax by adding retired IDs to ALLOW.

## 9. Risks

| Risk | Mitigation |
|---|---|
| Cached model table wrong | FR-9 live re-fetch blocks merge |
| Dated Haiku not in live docs | Keep per user; record discrepancy |
| Guard regex regression | 8 negative + 4 positive + delimiter + provenance ACs on scratch clone |
| Guard file excluded from scan | Accepted; only file with legit allowlist |
| CHANGELOG entry trips guard | Dev runs guard after CHANGELOG edit |

## 10. Hand-off (downstream_ready: true)

Developer: implement per PRD section 5 and this design; `steps[1]` must be the scan step (FR-6 runner extracts by index); error message generic; one commit. QA: FR-6 negative matrix plus one extra case: `claude-opus-5-` (trailing hyphen) and `CLAUDE-OPUS-4-8` (uppercase; not matched, accepted). ADR: `adrs/ADR-models-001-guard-allowlist.md`.
