# PRD: Refresh model literals to the latest model set + positive-allowlist guard

Stage: 2 (Refine, LIGHT) | Type: FEATURE | PO: Gandalf | Branch: delivery-team-agent-wrappers (PR #88 worktree)
Supersedes: prior-run PRD at this path. Inputs: `.delivery/artifacts/01-idea/po/idea-brief.md`, `stage-summary.md`, `dod/architect-review.md`, `dod/po-review.md`.

> A wizard's decisions arrive precisely when they mean to. Nine questions asked; nine answered below.

## 1. Problem and goal

Hard-coded model IDs in the repo point at `claude-opus-4-7` and `claude-sonnet-4-6`. The user's latest set is `claude-fable-5-1`, `claude-opus-5`, `claude-sonnet-5`, `claude-haiku-4-5-20251001`. The CI guard (`.github/workflows/stale-model-id-guard.yml`) is a deny-regex on 4.x IDs that allowlists the old IDs, so it cannot catch new-generation drift and actively protects the stale IDs.

Goal: every live literal maps to the latest set by role tier, and the guard becomes a positive allowlist of that set, shipped as one atomic change.

**Hit-count correction (idea brief wording was wrong).** `grep -rnoE 'claude-(opus|sonnet|haiku)-[0-9]'` outside `.delivery/` finds **14 hits across 5 source files** (`agent_registry.py` 6, `conftest.py` 4, `smoke-test-architecture.md` 2, `telemetry-schema.md` 1, `prompt-engineer/SKILL.md` 1) **plus 8 hits inside the guard workflow** (lines 23, 24, 25, 30, 31, and three on line 39) = 22 hits in 6 files. "22 hits across 6 files plus the guard" double-counted the guard.

## 2. Verification of model IDs

Source: claude-api skill "Current Models" table (cached 2026-06-24), read this run. Live page for reviewer re-fetch: https://platform.claude.com/docs/en/about-claude/models/overview

| ID | In skill table | Notes |
|---|---|---|
| `claude-fable-5-1` | yes | 1M ctx, $10/$50 per MTok, thinking always on, forced `tool_choice` 400, no sampling params/prefill, `refusal` stop reason, 30-day retention, no Priority Tier |
| `claude-opus-5` | yes | 1M ctx, $5/$25 |
| `claude-sonnet-5` | yes | 1M ctx, $2/$10 |
| `claude-haiku-4-5` (alias) | yes | The skill lists the alias only. The repo's dated `claude-haiku-4-5-20251001` is unchanged per user and is not contradicted by the table; the dated form is a repo convention that the live page must confirm (FR-9). |

Honest marker: this is verified against a 2026-06-24 cache, not a live fetch. FR-9 makes the live re-fetch a merge gate. Repo Python does not send `budget_tokens`, `temperature`, `top_p`, prefill or `tool_choice` (grep across `*.py` outside `.delivery/`: only unrelated `top_pos`/`Inches(top)` in `generate_pptx.py`), so the Opus 5 / Sonnet 5 request-surface changes do not affect this repo.

## 3. Decisions on the 9 open questions

| # | Question | Decision | Rationale |
|---|---|---|---|
| 1 | `model_awareness` stamps | **OUT of scope.** Left at current values. Follow-up BACKLOG (section 8). | A stamp asserts a full prose audit against a model. Bulk-bumping without the audit is dishonest, and this request is literal-scoped. |
| 2 | Fixtures in `conftest.py` and `smoke-test-architecture.md` | **Change** to new IDs by role tier. | No test asserts the literal (grep of `delivery-team/tests` shows the four fixture strings only). Aligning fixtures with real IDs keeps docs and telemetry examples honest. Fixture edits land in a commit or hunk separate from harness logic (BINDING-4.5); no harness logic is edited. |
| 3 | Guard shape | **Positive allowlist**, exactly four IDs. Any `claude-(opus\|sonnet\|haiku\|fable\|mythos)-<digit>...` token not exactly on the list fails. `claude-opus-4-8`, `claude-fable-5`, `claude-mythos-*`, `claude-haiku-4-5` (undated alias), and any suffixed variant are simply unlisted and therefore rejected. `claude-fable-5-1` IS on the allowlist. | Allowlist-over-deny (memory lesson). One-line rollover. No explicit deny list to maintain. |
| 4 | Fable roles | **Not adopted in any role.** Allowlist only. | Costs 2x Opus 5 ($10/$50 vs $5/$25). API constraints (forced `tool_choice` 400, thinking always on, no ZDR, no Priority Tier, `refusal` handling) need code paths this repo does not have. No role in the repo has a demonstrated need beyond Opus 5. Guard permits the ID so a future PR can adopt it by editing sites only. |
| 5 | Fourth registry agent for Fable | **No.** Registry keeps three default agents; the `claude-opus` agent maps to `claude-opus-5`. | Follows Q4; adding an unused agent is dead config with a cost trap. |
| 6 | Haiku form | **Keep dated `claude-haiku-4-5-20251001`.** Allowlist contains the dated form only; the undated alias `claude-haiku-4-5` fails the guard. | User said unchanged; repo convention; one canonical spelling keeps the guard exact. |
| 7 | Widen guard scan paths | **Yes.** Scan `*.py *.md *.yml *.yaml *.json *.txt *.sh`, with the guard workflow file itself pathspec-excluded (it necessarily contains the allowlist), plus existing `.delivery/` and `prd_flows.db` exclusions. The `on.paths` filter widens to match. | Grep today finds zero versioned IDs in those types, so widening is free now and prevents silent future drift. JSON has no comments, so a bare stale ID in JSON must fail; that is intended. |
| 8 | Ship mode | **Commit onto PR #88's branch (`delivery-team-agent-wrappers`), one atomic commit** for literals + guard (BINDING-2.1: no dual-allow window, no mixed state). Not BACKLOG-108's direct ff-merge. `.delivery/` history exempt via existing pathspec. | PR #88 is open and reviewed by CI; ff-merge bypasses the guard's own check. |
| 9 | Live-doc verification | **QA at Stage 2 DoD / Stage 6 re-fetches** the live models page and records the result in `.delivery/artifacts/06-development/qa/model-id-verification.md`. Allowlist merge is blocked until that file exists and confirms all four IDs. | Every external claim cites a live URL; reviewer re-fetches load-bearing ones. |

## 4. Scope

In scope: the per-site edits in section 5; rewrite of `stale-model-id-guard.yml`; CHANGELOG entry (new `Unreleased` section, history entries untouched).

Out of scope (each has an explicit reason):
- `model_awareness:` stamps in 34 SKILL.md and their `pattern_library_version` / `last_audited` (Q1).
- Prose naming "Opus 4.7" / F-08 / `xhigh` behavior claims (`delivery-flow/SKILL.md:27,273`, `orchestrator-doctrine.md:77`, `prompt-engineer/SKILL.md` prose at 88, 347, 356, 397, 408). These are behavior claims needing doc-verified Opus 5 behavior; deferred to the audit BACKLOG. Only ID literals change here.
- Family-alias `model: opus|sonnet` frontmatter and `prd-quality-gate-flow/stage_definitions.py` aliases (version-agnostic, BINDING-1.4).
- `.delivery/` history and `CHANGELOG.md` historical entries.
- `governance/cache-prefix-hash.txt`: see section 7.
- Any use of `claude-fable-5-1` in a role (Q4).

## 5. Per-site mapping

| # | file:line | Current | New | Reason |
|---|---|---|---|---|
| S1 | `agentic-flow-builder/scripts/agent_registry.py:148` | comment: `canonical 2026-04-22 — opus-4-7 migration; prior: claude-sonnet-4-5-20250929 (retired)` | comment rewritten: `canonical 2026-09-19 — model refresh; prior: claude-sonnet-4-6, claude-sonnet-4-5-20250929 (retired)` | Provenance line; `#` exempt; records the retired ID. |
| S2 | `agent_registry.py:149` | `claude-sonnet-4-6` | `claude-sonnet-5` | Sonnet tier stays Sonnet. |
| S3 | `agent_registry.py:173` | comment naming `claude-haiku-4-20250514 (retired)` | unchanged | Haiku unchanged; provenance still accurate. |
| S4 | `agent_registry.py:174` | `claude-haiku-4-5-20251001` | unchanged | Light tier, user said unchanged. |
| S5 | `agent_registry.py:189` | comment `... prior: claude-opus-4-20250514 (retires 2026-06-15 per F-04)` | comment rewritten: `canonical 2026-09-19 — model refresh; prior: claude-opus-4-7, claude-opus-4-20250514 (retired)` | Provenance; `#` exempt. |
| S6 | `agent_registry.py:190` | `claude-opus-4-7` | `claude-opus-5` | Opus tier stays Opus. |
| S7-S10 | `delivery-team/tests/smoke/tests/conftest.py:105,117,129,151` | `claude-opus-4-7` (x4) | `claude-opus-5` (x4) | Opus-tier fixtures; no test asserts the literal. |
| S11 | `delivery-team/references/telemetry-schema.md:36` | `claude-sonnet-4-6` | `claude-sonnet-5` | Doc example, sonnet tier. |
| S12 | `delivery-team/architecture/smoke-test-architecture.md:115` | `claude-opus-4-7` | `claude-opus-5` | Doc example, opus tier. |
| S13 | `smoke-test-architecture.md:116` | `claude-sonnet-4-6` | `claude-sonnet-5` | Doc example, sonnet tier. |
| S14 | `prompt-engineer/SKILL.md:368` | `MODEL_ID = "claude-opus-4-7"  # canonical 2026-04-22` | `MODEL_ID = "claude-opus-5"  # canonical 2026-09-19` | Live code literal in a Pattern 4.1 example; the provenance-date comment convention is the pattern's own teaching, so the date is bumped with the ID. Line count neutral (budget unaffected). |
| S15 | `.github/workflows/stale-model-id-guard.yml` (23-25, 30-31, 39) | deny-regex + old allowlist | rewritten per FR-6..FR-8 | Guard redesign. |
| S16 | `.claude-plugin/marketplace.json`, `hooks/*`, `prd-quality-gate-flow/stage_definitions.py` | family names only | unchanged | No versioned literal (verified by grep, zero hits). |

Net: 9 live-literal edits (S2, S6, S7-S10, S11, S12, S13; S14 makes 10 with the code literal), 2 provenance-comment edits (S1, S5), 2 unchanged (S3, S4), plus the guard.

## 6. Functional requirements

All commands run from the repo root; `grep` is GNU grep (`/usr/bin/grep`).

**FR-1 Live literals migrated.** All ten live sites in section 5 use the new IDs.
- AC: `git grep -nE 'claude-(opus-4-7|sonnet-4-6)' -- ':!.delivery' ':!CHANGELOG.md'` prints only lines whose content begins (after optional whitespace) with `#` or `>`; the live-line check `git grep -nE 'claude-(opus-4-7|sonnet-4-6)' -- ':!.delivery' | /usr/bin/grep -vE '^[^:]+:[0-9]+:[[:space:]]*[#>]'` prints nothing.
- AC: `git grep -c 'claude-opus-5' -- delivery-team/tests/smoke/tests/conftest.py` prints `...conftest.py:4`.
- AC: `git grep -nE '"model": "claude-sonnet-5"' -- delivery-team/references/telemetry-schema.md` prints line 36.
- AC: `git grep -nE 'claude-haiku-4-5-20251001' -- agentic-flow-builder/scripts/agent_registry.py` still prints exactly line 174.

**FR-2 Provenance preserved.** Retired IDs survive only in `#` comments or `>` blockquotes.
- AC: `git grep -nE 'claude-(opus|sonnet|haiku)-4-' -- ':!.delivery' ':!.github/workflows/stale-model-id-guard.yml' | /usr/bin/grep -vE '^[^:]+:[0-9]+:[[:space:]]*[#>]' | /usr/bin/grep -v 'claude-haiku-4-5-20251001'` prints nothing.
- AC: `sed -n '148p;189p' agentic-flow-builder/scripts/agent_registry.py` piped to `/usr/bin/grep -cE '^[[:space:]]*#.*claude-(sonnet-4-6|opus-4-7)'` prints `2` (run after the S1/S5 edits).

**FR-3 Fable not adopted.** No role uses Fable; guard permits it.
- AC: `git grep -n 'claude-fable' -- ':!.delivery' ':!.github/workflows/stale-model-id-guard.yml' ':!CHANGELOG.md'` prints nothing.
- AC: `git grep -c 'fable-5-1' -- .github/workflows/stale-model-id-guard.yml` prints `.github/workflows/stale-model-id-guard.yml:1` (or higher). The guard's `ALLOW` variable holds prefix-less tails (`fable-5-1|opus-5|sonnet-5|haiku-4-5-20251001`, see section 12) and the strip regex supplies the `claude-` prefix, so the AC greps the tail; the four-ID list in FR-6 and section 10 names the same set with prefixes.

**FR-4 Smoke tests pass.** Baseline this run: 3 passed.
- AC: `python -m pytest delivery-team/tests/smoke/tests -q` exits 0 with `3 passed` (or more, never fewer).
- AC: fixture edits and harness-logic edits are separate hunks: `git diff -U0 -- delivery-team/tests/smoke/tests/conftest.py | /usr/bin/grep -E '^[+-]' | /usr/bin/grep -vE '^(\+\+\+|---)' | /usr/bin/grep -vc 'claude-'` prints `0`.

**FR-5 Doc examples consistent.** `telemetry-schema.md`, `smoke-test-architecture.md`, and `conftest.py` use only allowlisted IDs.
- AC: `git grep -ohE 'claude-(opus|sonnet|haiku|fable)-[0-9][^ "'"'"',]*' -- delivery-team/references/telemetry-schema.md delivery-team/architecture/smoke-test-architecture.md delivery-team/tests/smoke/tests/conftest.py | sort -u` piped to `/usr/bin/grep -vxE 'claude-(opus-5|sonnet-5)'` prints nothing (grep exits 1).

**FR-6 Guard is a positive allowlist.** Allowed set (exact, whole-token match): `claude-fable-5-1`, `claude-opus-5`, `claude-sonnet-5`, `claude-haiku-4-5-20251001`. Detection token: `claude-(opus|sonnet|haiku|fable|mythos)-[0-9][-A-Za-z0-9.]*[-A-Za-z0-9]` (plus a bare `claude-<family>-<digit>` alternative for one-char tails). The token cannot end in `.` or `,`, so prose like "use claude-haiku-4-5-20251001." still yields the allowed token. Mechanics (contract): `git ls-files` to `xargs grep -EnH` token, drop `#`/`>` lines, `sed` strip each allowed ID only when followed by end of line, a char outside `[-A-Za-z0-9.]`, or `.` then a non-alnum, then re-`grep` for any remaining `claude-<family>-<digit>`; non-empty output exits 1. A suffixed variant (`claude-opus-5-20260101`) or dotted variant (`claude-opus-5.1`) is a different token and fails. The allowlist lives in one shell variable (`ALLOW=`) so a rollover edits one line. The scan is step index 1 (`steps[1]`, after checkout) of job `stale-id-guard`.

Runner used by all guard ACs (from a scratch clone of the committed head, so the worktree is never dirtied): `git clone -q . /tmp/scratch && cd /tmp/scratch && python3 -c "import yaml;print(yaml.safe_load(open('.github/workflows/stale-model-id-guard.yml'))['jobs']['stale-id-guard']['steps'][1]['run'])" > /tmp/g.sh` then `bash /tmp/g.sh; echo $?`. Inject with `printf '%s\n' 'MODEL = "claude-opus-4-8"' >> README.md` and reset with `git checkout -q README.md`.
- AC (positive): in the scratch clone, `bash /tmp/g.sh; echo $?` prints `No non-allowlisted model IDs found.` and `0`.
- AC (negative, injection): append `MODEL = "<ID>"` to `README.md`; `bash /tmp/g.sh; echo $?` prints `README.md:<line>:MODEL = "<ID>"` and `1` for each `<ID>` in `claude-opus-4-8`, `claude-fable-5`, `claude-mythos-5-1`, `claude-haiku-4-5`, `claude-opus-5-1`, `claude-sonnet-4-6`, `claude-opus-5.1`, `claude-opus-5-20260101`. Repeat once with a `.json`-content line in a tracked `.md` (`{"model": "claude-opus-4-7"}`); exit 1.
- AC (positive IDs): the same injection with each of `claude-fable-5-1`, `claude-opus-5`, `claude-sonnet-5`, `claude-haiku-4-5-20251001` exits `0`.
- AC (delimiters): appending the prose lines `Use claude-haiku-4-5-20251001.` and `Use claude-opus-5, claude-sonnet-5, and claude-haiku-4-5-20251001.` exits `0` (trailing `.` and `,` after an allowed ID are not swallowed). Appending `Use claude-opus-5.1` exits `1`.
- AC: the workflow `run:` block contains no `${{ github.event.* }}` interpolation (`/usr/bin/grep -c 'github.event' .github/workflows/stale-model-id-guard.yml` prints `0`).

**FR-7 Provenance exemption and static-only.** Lines whose content starts with `#` or `>` after the `file:line:` prefix are exempt. Only line-start `#`/`>` is exempt: a trailing mid-line comment on a code line, e.g. `MODEL = "claude-sonnet-5"  # prior: claude-opus-4-7`, is NOT exempt and exits 1. Provenance must therefore live on its own comment line. The guard is static `git ls-files | grep` only: no `claude` CLI, no network, no `curl`, no `pip`.
- AC (uses the FR-6 runner): appending `# prior: claude-opus-4-8 (retired)` exits `0`; appending `> prior: claude-opus-4-8` exits `0`; appending the same text as a bare line (`prior: claude-opus-4-8`) exits `1`; appending `MODEL = "claude-sonnet-5"  # prior: claude-opus-4-7` exits `1`.
- AC: `/usr/bin/grep -nE '\bclaude\b +(-|--)|curl|wget|pip install|npx' .github/workflows/stale-model-id-guard.yml` prints nothing (grep exits 1).

**FR-8 Scan surface widened and self-exempt.** Pathspec: `*.py *.md *.yml *.yaml *.json *.txt *.sh`, excluding `.delivery/`, `prd-quality-gate-flow/prd_flows.db`, and `.github/workflows/stale-model-id-guard.yml`. The workflow `on.paths` list matches (and keeps `!.delivery/**`). Globs stay single-quoted (`'**/*.ext'`), the existing workflow style.
- AC: `/usr/bin/grep -cE "'\*\*/\*\.(py|md|yml|yaml|json|txt|sh)'" .github/workflows/stale-model-id-guard.yml` prints `7`.
- AC (FR-6 runner): a tracked `.json` file containing bare `{"model": "claude-opus-4-7"}` (`echo '{"model": "claude-opus-4-7"}' > scratch.json && git add scratch.json && bash /tmp/g.sh; echo $?`) prints `scratch.json:1:...` and `1`.
- AC: `python3 -c "import yaml; yaml.safe_load(open('.github/workflows/stale-model-id-guard.yml'))"; echo $?` prints `0`.

**FR-9 Live verification gate.** Before merge, QA re-fetches https://platform.claude.com/docs/en/about-claude/models/overview and records per-ID confirmation (including whether the dated Haiku form is accepted by the API), the fetch date, and any discrepancy.
- AC: `test -s .delivery/artifacts/06-development/qa/model-id-verification.md` exits 0 and the file contains all four IDs: `for i in claude-fable-5-1 claude-opus-5 claude-sonnet-5 claude-haiku-4-5-20251001; do /usr/bin/grep -q "$i" .delivery/artifacts/06-development/qa/model-id-verification.md || echo MISSING $i; done` prints nothing.
- Failure rule: if the live page contradicts any ID, the allowlist is changed to the live value before merge; no dual-allow.

**FR-10 Governance gates hold.**
- AC: `python scripts/check_skill_budgets.py` exits 0 (baseline this run: 0). S14 must be line-count neutral: `git diff --numstat -- prompt-engineer/SKILL.md` shows equal add/delete counts.
- AC: `git diff --name-only | /usr/bin/grep -c 'delivery-team/skills/delivery-flow/SKILL.md' || true` prints `0` (grep exits 1 on zero matches, hence `|| true`; this change must not touch it; see section 7).
- AC: `/usr/bin/grep -c 'plugin-dev:skill-development' .delivery/artifacts/06-development/dev/dev-notes.md` prints `1` or higher (developer records the skill load in dev-notes at Stage 6; file created then, like FR-9's).

**FR-11 Atomic ship and changelog.** One commit contains all literal edits and the guard rewrite; no intermediate commit has the guard allowlist and the literals disagreeing. Let `C` be the shipping commit (`HEAD` after commit).
- AC: `git show --stat --format= HEAD | /usr/bin/grep -cE 'stale-model-id-guard.yml|agent_registry.py'` prints `2`; and `git rev-list --count origin/delivery-team-agent-wrappers..HEAD` prints `1` (run before push, with origin at the pre-change tip).
- AC: the FR-6 positive AC passes on `HEAD` (guard and literals agree in the single commit).
- AC: `/usr/bin/grep -nE 'claude-opus-5|claude-sonnet-5|stale-model-id-guard' CHANGELOG.md` prints at least `1` under `-c`. Earlier entries unchanged: the only removed line is the `[Unreleased]` placeholder, checked by `git diff CHANGELOG.md | /usr/bin/grep -E '^-[^-]' | /usr/bin/grep -vc 'No unreleased changes'` printing `0`.

## 7. Handling notes

- **`governance/cache-prefix-hash.txt`: not affected, and already stale.** It records `43067c9e...` for `delivery-flow/SKILL.md`; the file's sha256 today is `0a7aa92f...`. It drifted before this work (`CHANGELOG.md:39` shows the last regeneration). This change does not edit `delivery-flow/SKILL.md` (it has no ID literal; its "Opus 4.7" prose is out of scope), so no re-freeze belongs here. Re-freezing now would launder unrelated drift into this PR. Logged as follow-up BACKLOG-B (section 8). No CI workflow currently reads the file (grep of `.github/` shows none).
- **`telemetry-schema.md`**: literal is a doc example only; one-line edit (S11). Schema field definitions are untouched.
- **`prompt-engineer/SKILL.md`**: only the `MODEL_ID` line changes; surrounding Pattern 4.1 prose ("When in doubt on 4.7", line 356 region) is behavior guidance and stays for the audit BACKLOG.
- **`agent_registry.py` comments** keep the arrow of history: each retired ID stays in a `#` comment, which the guard exempts. No functional code besides the two `config.model` values changes.
- **`conftest.py`**: only the four string values change; no fixture structure or harness logic.

## 8. Follow-up BACKLOG items (created by PO at Stage 8, not edited now)

- **BACKLOG-A: model_awareness stamp + prose audit.** Audit the 34 SKILL.md stamps (`opus-4-7` / `opus-4-7-frontmatter-only`) and the "Opus 4.7"/F-08/`xhigh` prose against doc-verified Opus 5 / Sonnet 5 behavior; bump stamps only with the audit. Absorbs BACKLOG-108 S3.
- **BACKLOG-B: cache-prefix-hash drift.** Reconcile `governance/cache-prefix-hash.txt` with `delivery-flow/SKILL.md` and decide whether a CI check should read it.
- **BACKLOG-C: smoke-harness metrics / live baseline.** Local-only (claude CLI). Absorbs BACKLOG-108 S5.
- **BACKLOG-D (conditional): Fable adoption.** Only if a role shows a measured need; requires refusal/fallback handling and 30-day-retention acknowledgement.

## 9. BACKLOG-108 disposition: supersede and retarget

File is untracked in the main checkout; not edited here. Proposed replacement text for its header (apply at Stage 8 by whoever owns that checkout):

```
Status: SUPERSEDED by run "model literals refresh" (PR #88 branch), 2026-09-19.
Retarget: heavy claude-opus-4-8 -> claude-opus-5; mid claude-sonnet-4-6 -> claude-sonnet-5;
light claude-haiku-4-5-20251001 unchanged; claude-fable-5-1 allowlisted, not adopted.
Carried forward: positive-allowlist guard, no dual-allow window, '#'/'>' provenance exemption,
atomic ship, static-grep-only CI, fixture edits separate from harness logic,
family-alias exemption for prd-quality-gate-flow.
Split out: S3 (34-file prose sweep + stamps) -> BACKLOG-A; S5 (metrics/xhigh/live baseline) -> BACKLOG-C.
cache-prefix re-freeze: dropped (drift is pre-existing) -> BACKLOG-B.
Memory topic opus-4-8-migration.md Section 1 lineup table: superseded; record new lineup as a new topic.
```

## 10. Success metrics

- FR-1..FR-11 acceptance commands all pass on the branch head.
- Guard negative test: 8 of 8 injected stale/unlisted IDs fail; 4 of 4 allowlisted IDs pass.
- Zero live `claude-opus-4-7` / `claude-sonnet-4-6` literals outside `.delivery/` and CHANGELOG history.

## 11. Assumptions and open items

- Assumption: the claude-api skill's cache is accurate for the four IDs until FR-9 re-fetches (owner: QA; blocks merge, not design).
- Open (owner: QA, FR-9): whether the live docs also publish a dated Haiku 4.5 snapshot ID; if the page shows only the alias, PO decision Q6 is to keep the dated form anyway (user instruction) and record the discrepancy.
- Resolved by QA prototype (`/tmp/qa-guard-proto/guard.sh`, reproduced in Verification): strip-then-regrep mechanics satisfy FR-6/FR-7 with GNU grep + sed only. Architect may adopt or improve; the FR-6/FR-7 contract is binding, exact script is not.
- Known rollover item (QA F-6): live docs list Haiku 4.5 retirement not sooner than 2026-10-15. The allowlist pins that ID; rollover is a one-line `ALLOW=` edit plus the four Haiku sites. Not blocking.
- `downstream_ready: true`.

## 12. Verification (self-correction rounds 1 and 2, run 2026-09-19)

Method: scratch clone `/tmp/pr88s` of this worktree with the proposed guard workflow written and literals migrated, committed as 1 commit on top of origin tip. Nothing in the real worktree source changed. Actual outputs:

```
$ python3 -c "import yaml;yaml.safe_load(open('.delivery/artifacts/02-refine/po/constraints.yml'))"   # 14 constraints load; BC-04 quoted
$ python3 -c "import yaml;print(yaml.safe_load(open('.github/workflows/stale-model-id-guard.yml'))['jobs']['stale-id-guard']['steps'][1]['run'])" > /tmp/g.sh   # 16 lines
$ bash /tmp/g.sh; echo $?
No non-allowlisted model IDs found.
0
exit 1: claude-opus-4-8, claude-fable-5, claude-mythos-5-1, claude-haiku-4-5, claude-opus-5-1,
        claude-sonnet-4-6, claude-opus-5.1, claude-opus-5-20260101 (8/8), {"model": "claude-opus-4-7"} in .md and in tracked .json
        sample: README.md:79:MODEL = "claude-opus-4-8"  -> exit 1
exit 0: claude-fable-5-1, claude-opus-5, claude-sonnet-5, claude-haiku-4-5-20251001 (4/4),
        "Use claude-haiku-4-5-20251001.", "Use claude-opus-5, claude-sonnet-5, and claude-haiku-4-5-20251001.",
        "# prior: claude-opus-4-8 (retired)", "> prior: claude-opus-4-8"
exit 1: MODEL = "claude-sonnet-5"  # prior: claude-opus-4-7   (trailing comment NOT exempt)
$ grep -c 'github.event' <workflow>                      -> 0   (also 0 on current real file)
$ grep -nE '\bclaude\b +(-|--)|curl|wget|pip install|npx' <workflow>   -> (no output, rc=1)
$ grep -cE "'\*\*/\*\.(py|md|yml|yaml|json|txt|sh)'" <workflow>       -> 7
$ python3 -c "import yaml;yaml.safe_load(open('<workflow>'))"; echo $?   -> 0
$ git show --stat --format= HEAD | grep -cE 'stale-model-id-guard.yml|agent_registry.py'   -> 2
$ git rev-list --count origin/delivery-team-agent-wrappers..HEAD          -> 1
```

Reference guard body (adoptable, as run above): `ALLOW='fable-5-1|opus-5|sonnet-5|haiku-4-5-20251001'; TOK='claude-(opus|sonnet|haiku|fable|mythos)-[0-9][-A-Za-z0-9.]*[-A-Za-z0-9]|claude-(opus|sonnet|haiku|fable|mythos)-[0-9]'; D='$|[^-A-Za-z0-9.]|\.($|[^-A-Za-z0-9])'`, then `git ls-files <7 globs + 3 excludes> | xargs grep -EnH "$TOK" | grep -vE '^[^:]+:[0-9]+:[[:space:]]*[#>]' | sed -E "s/claude-($ALLOW)($D)/<OK>\3/g" | grep -E 'claude-(opus|sonnet|haiku|fable|mythos)-[0-9]' || true`.

Defects addressed: F-4 (YAML quoted, loads), F-1 (token, delimiter rule, new ACs), F-2 (runner extraction command, garbled wording removed), F-3 (FR-11 parseable commands), F-5 (`|| true`), F-6 (section 11).

Round 2 (scratch clone `/tmp/cl`, literals and CHANGELOG edits simulated; guard file from `/tmp/pr88s`). Actual outputs:

```
$ git diff CHANGELOG.md | /usr/bin/grep -E '^-[^-]' | /usr/bin/grep -vc 'No unreleased changes'   -> 0   (placeholder replaced by a Changed entry)
$ /usr/bin/grep -cE 'claude-opus-5|claude-sonnet-5|stale-model-id-guard' CHANGELOG.md            -> 1
$ /usr/bin/grep -c 'fable-5-1' /tmp/pr88s/.github/workflows/stale-model-id-guard.yml              -> 1
$ /usr/bin/grep -c 'claude-fable-5-1' <same>                                                      -> 0   (why the old AC failed)
$ sed -n '148p;189p' agent_registry.py | /usr/bin/grep -cE '^[[:space:]]*#.*claude-(sonnet-4-6|opus-4-7)'   -> 2 (after edits; 0 before)
$ git grep -ohE 'claude-(opus|sonnet|haiku|fable)-[0-9][^ "'"'"',]*' -- <3 files> | sort -u | /usr/bin/grep -vxE 'claude-(opus-5|sonnet-5)'; echo $?   -> (empty) 1 (after edits)
```

Not runnable until Stage 6 (files absent now, by design): FR-9 verification file, FR-10 dev-notes grep. Both are gates with defined paths and expected results.

Defects addressed round 2: FR-3 AC2 (grep tail), FR-10 AC3 (dev-notes grep), FR-11 CHANGELOG (`-vc` form), section 10 count (8 of 8). Also tightened FR-2 AC2, FR-5, FR-11 `C` to `HEAD`.
