---
verdict: DONE
stage: 4-architect
run: run-2026-05-28-o48m
backlog: BACKLOG-108
role: security (DoD validator, fresh reviewer)
architecture_rev: 3
blocking_issues: []
blocking_count: 0
warning_count: 7
---

# Security DoD review: Stage 4 Architect, BACKLOG-108

Scope: architecture.md rev 3, ADR-lmr-001..005, PRD. Design review only; nothing executed. Threat model in design is accidental drift, not adversary. I judged against that, and noted where an adversary would change the answer.

## Verdict: DONE (0 blocking, 7 warnings)

## Checklist

| Check | Result | Evidence |
|---|---|---|
| Workflow injection | PASS | ADR-lmr-002 D7: no `${{ github.event.* }}` in `run:`, only runs `python3 scripts/check_model_pins.py`, no pip, no `claude`. Triggers push main / pull_request / dispatch; no `pull_request_target`, so fork PRs get no secrets. |
| Least-privilege `permissions:` | GAP (W1) | D7 and architecture section 4 S1 never state a `permissions:` block. |
| Secrets in fixtures / sidecars / baseline | MOSTLY PASS (W2) | Baseline stores 4 pin env vars, model names, session_id, sha256 (arch section 4 S5). Committed raw streams are "trimmed `system/init`: type, subtype, model, session_id" (ADR-lmr-004 sec 5). No key fields. Real-shape fixture has no stated scrub rule. |
| Paid `claude -p` controls | PASS (W4) | Two-layer cap: `--max-budget-usd 3.00` plus post-check (arch P12, FR-5.4); sequential samples; abort init on non-zero exit (F9); `--effort` only for `opus`. Run output goes out of tree. No `--bare`, so host hooks/plugins/CLAUDE.md load (OQ-12, `host_context` recorded); accepted, local only. |
| Guard script safety | PASS with W3, W5 | Stdlib only, no shell, regexes are module constants. See W3 and W5. |
| Ship gate integrity / RR-1 | ACCEPTABLE | Stated plainly as detect-not-prevent (arch section 3, U14, ADR-lmr-005 item 8). Layers: clean tree, out-of-tree teed log, pre-push (opt-in), S7b fresh clone by different dispatch. No overclaim. |
| Manifest tamper / forgery | ACCEPTED LIMIT (W6) | Orchestrator writes manifests; ids pasted from Agent result; transcript check is supporting only and skippable when dir absent (ADR-lmr-005 item 6). Recovered-form manifests REQUIRE transcript files (item 4a). Honestly stated. |
| Producer/validator separation | PASS | Distinct dispatch ids, red-first at `validator_start`, AST stub check, `run_smoke.py` in producer path list, trailers cross-checked to manifest (ADR-lmr-004 sec 6, ADR-lmr-005 items 6-7). Order-provable, not identity-provable; stated. |

## Blocking issues

None.

## Non-blocking warnings

**W1. New guard workflow has no stated `permissions:` block.** Evidence: ADR-lmr-002 D7 lists triggers and steps only. Without it the job inherits repo default token scope, which may be read-write. Fix: S1 AC asserts the workflow declares top-level `permissions: contents: read` (nothing else), checkout with `persist-credentials: false`, and third-party actions pinned (or first-party only). Same for the new `push` trigger added to `skill-line-budget.yml` (P16). Add to the S1 dispatch prompt.

**W2. Real-shape fixture and provenance sidecar have no scrub or secret-scan step.** Evidence: ADR-lmr-004 sec 5 trims the five committed baseline streams, but the fixture `stream_real_shape.jsonl` is a real capture; without `--bare` the init event and assistant text can carry `cwd`, home paths, MCP server names, plugin names, host CLAUDE.md or memory text. Repo is public (P47Phoenix). Fix: validator dispatch scrubs paths and host text, and a plan AC greps fixture, sidecar, baseline and streams for `sk-ant-`, `ANTHROPIC_API_KEY=`, `/home/`, `/var/home/`, tokens, emails before commit. Also note `model_pin_env` values could be a Bedrock/Vertex ARN with an account id; record set/unset instead of value if it is not a bare model name.

**W3. Guard `git ls-files` output handling.** Evidence: D3 says filter with `os.path.isfile`; no `-z` stated. Without `-z`, git quotes non-ASCII or odd names (`core.quotepath`), `isfile` returns false, and the file is silently skipped, which is a scan evasion and a count mismatch with the canonical command. Fix: use `git ls-files -z --cached --others --exclude-standard`, `subprocess.run([...], shell=False, check=True)`, fail closed (exit 2) if git returns non-zero. Also skip or flag symlinks (`os.path.islink`) so a link cannot pull an out-of-tree file in.

**W4. Predictable temp paths in shared `/tmp`.** Evidence: ship log `${TMPDIR:-/tmp}/ship-gate-<sha12>.log` and `${TMPDIR:-/tmp}/smoke-out`. On a multi-user host a pre-placed symlink redirects writes, and the evidence log is the integrity artifact. Fix: `mktemp -d` with 0700 and log the resulting path. Low on a single-user workstation.

**W5. ReDoS review of PIN_RE, STAMP_RE, PROSE_RE, BARE_RE, COUNT_RE.** Read from PRD lines 32-36. No nested quantifiers, no overlapping alternation under `*`; worst case is `claude-[a-z0-9.-]*` backtracking, linear per start and only at `claude-` occurrences (quadratic on a pathological one-line file of repeated `claude-`). NFR-13 measured 0.5 s. Not exploitable in practice. Optional hardening: skip or truncate lines over about 10k chars and files over a size cap, with a printed note. Note COUNT_RE only blanks text for the prose/bare tests, not PIN_RE, so it cannot hide a real pin ID.

**W6. Manifest and transcript forgery (accepted limit).** An executor that writes the manifest can also paste fake ids; the transcript check is skipped when the directory is missing (ADR-lmr-005 item 6) and the layout is observed on one CLI only. Fine for accidental drift; not a control against a hostile orchestrator. Suggest the S7b dispatch always runs the transcript check on all manifests and prints the skip note loudly, so a silent skip is visible in the report.

**W7. `pre-push` hook and pre-commit hook are inert by default** (P23, `core.hooksPath` = `.git/hooks`), and `--no-verify` bypasses. Design already logs `hooksPath=` and does not rely on them. Also `MODEL_PIN_STRICT` is read from the environment; harmless (it only tightens), but hooks must not `eval` staged filenames. Use `git diff --cached --name-only -z` with `xargs -0`.

## Residuals R-1..R-6, security view

| ID | Acceptable? | Note |
|---|---|---|
| R-1 uniform `latest` stamp on 22 unreviewed files | Yes | Integrity of a claim, not a vulnerability; mitigated by `stamp-only-ledger.tsv`. |
| R-2 version words in non-.md files pass guard | Yes | No hit today; low. |
| R-3 / RR-1 direct push to main detect-not-prevent | Yes for stated threat model | Revisit trigger must include any second pusher, any CI secret, or any workflow gaining write scope. Then branch protection is required. |
| R-4 `Makefile` and `.githooks/pre-commit` outside scan | Yes | Both executable, both clean today; minor supply-chain blind spot, low. |
| R-5 `02-refine` dropped from AC-DISP | Yes | Honest alternative to a forged manifest; better security posture than inventing ids. |
| R-6 F12/F13 argued not reproduced | Yes | Process and doc facts, no security impact. |

## Recommendation

Advance. Carry W1, W2, W3 into the Plan stage as explicit S1/S5 ACs; they are cheap and close the only real gaps (token scope, fixture leakage, silent path skip).
