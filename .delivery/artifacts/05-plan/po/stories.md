# Stories: model ID refresh + positive-allowlist guard

SKILL_LOADED: delivery-team:product-delivery
Stage 5 Plan (LIGHT) | FEATURE | PO: Gandalf | Branch: delivery-team-agent-wrappers | Base tip: 337edb5
Inputs: PRD (`02-refine/po/prd.md`), constraints.yml, architecture.md, ADR-models-001, `04-architect/dod/developer-review.md`. Overwrites previous run.

Role: Product Owner | Task: user_story | Refs: user-stories.md, backlog-management.md

Light depth = reduced depth, not skipped. Consolidated by file scope. ADR-models-001 + BC-03 mandate atomic ship, so guard + literals + fixtures = ONE dev unit (US-1). Independent scopes split out: FR-9 verification file (US-2), CHANGELOG + dev-notes (US-3), backlog/supersede text (US-4).

All commands from repo root. GNU grep = `/usr/bin/grep`. Guard tests run in scratch clone, never dirty worktree.

## Corrections applied (PRD not edited)

| # | PRD text | Problem | Corrected in stories |
|---|---|---|---|
| C1 | PRD s12 reference sed uses `\3` | D group nested; whole delimiter is `\2` (dev-review Note A) | Guard script in US-1 uses `\2`: `sed -E "s/claude-($ALLOW)($D)/<OK>\2/g"` |
| C2 | FR-11 AC `git rev-list --count origin/delivery-team-agent-wrappers..HEAD` prints `1` | Branch already pushed at 337edb5; origin..HEAD = 0 before ship (dev-review Note B) | AC-26 uses pinned base: `git rev-list --count 337edb5..HEAD -- ':!.delivery'` prints `1` (counts only commits touching non-`.delivery` paths, so pipeline-artifact commits do not break it). Also `git rev-list --count 337edb5..HEAD` prints `1` if no `.delivery/` commit interleaves. After push, `origin/...` form prints 0 again; not used. |
| C3 | Idea/PRD "34 stamps" | Actual: 25 SKILL.md files carry the stamp (26 stamp lines, one file has two) | BACKLOG-A (US-4) says "25 SKILL.md files" |

## Dependency order

US-2 (verification gate) -> US-3 (CHANGELOG + dev-notes) -> US-1 (edits + guard, then single shipping commit including CHANGELOG) -> US-4 (Stage 8 backlog text, independent, no ordering vs code).
US-1 commit is blocked until `model-id-verification.md` exists and confirms all four IDs (FR-9 failure rule: contradiction -> change allowlist to live value, no dual-allow).

---

## US-1 (Must): Atomic literal migration + positive-allowlist guard

As a repo maintainer, I want every live model literal on the latest set and the CI guard to be a positive allowlist shipped in one commit, so that new-generation drift fails CI and stale IDs are no longer protected.

File scope: `agentic-flow-builder/scripts/agent_registry.py` (S1,S2,S5,S6; S3,S4 untouched), `delivery-team/tests/smoke/tests/conftest.py` (S7-S10, values only), `delivery-team/references/telemetry-schema.md:36` (S11), `delivery-team/architecture/smoke-test-architecture.md:115,116` (S12,S13), `prompt-engineer/SKILL.md:368` (S14, line-neutral), `.github/workflows/stale-model-id-guard.yml` (S15). Load `plugin-dev:skill-development` before touching prompt-engineer/SKILL.md; record in dev-notes (US-3).
Depends on: US-2, US-3. Commit: single, `HEAD` = C.

Edits: sonnet-4-6 -> `claude-sonnet-5` (S2,S11,S13); opus-4-7 -> `claude-opus-5` (S6,S7-S10,S12,S14; S14 date comment 2026-04-22 -> 2026-09-19); S1/S5 provenance comments rewritten per PRD s5 on own `#` lines; fable not used; haiku line 174 untouched. conftest.py: string values only, no harness logic.

Guard contract: `ALLOW='fable-5-1|opus-5|sonnet-5|haiku-4-5-20251001'`; `TOK='claude-(opus|sonnet|haiku|fable|mythos)-[0-9][-A-Za-z0-9.]*[-A-Za-z0-9]|claude-(opus|sonnet|haiku|fable|mythos)-[0-9]'`; `D='$|[^-A-Za-z0-9.]|\.($|[^-A-Za-z0-9])'`; pipeline `git ls-files '*.py' '*.md' '*.yml' '*.yaml' '*.json' '*.txt' '*.sh' <3 excludes> | xargs grep -EnH "$TOK" | grep -vE '^[^:]+:[0-9]+:[[:space:]]*[#>]' | sed -E "s/claude-($ALLOW)($D)/<OK>\2/g" | grep -E 'claude-(opus|sonnet|haiku|fable|mythos)-[0-9]' || true`; non-empty -> exit 1, else print `No non-allowlisted model IDs found.` Scan is `steps[1]` of job `stale-id-guard`; `git ls-files` globs are `'*.ext'` (F-1: `'**/*.ext'` misses root files like README.md in git pathspec, giving a false pass; verified count 0 vs 1); `'**/*.ext'` is used ONLY in workflow `on.paths` (7 entries, so AC-19 stays `7`); `on.paths` widened, keeps `!.delivery/**`. No `github.event`, no claude CLI/network.

Runner (used by all guard ACs):
```
git clone -q . /tmp/scratch && cd /tmp/scratch && python3 -c "import yaml;print(yaml.safe_load(open('.github/workflows/stale-model-id-guard.yml'))['jobs']['stale-id-guard']['steps'][1]['run'])" > /tmp/g.sh
bash /tmp/g.sh; echo $?
# inject: printf '%s\n' 'MODEL = "<ID>"' >> README.md ; reset: git checkout -q README.md
```
Run scratch clone from committed HEAD (after commit) for final pass.

### Acceptance criteria (ACs mapped, ID = AC-NN)

| AC | FR | Command | Expected |
|---|---|---|---|
| AC-01 | FR-1 | `git grep -nE 'claude-(opus-4-7\|sonnet-4-6)' -- ':!.delivery' \| /usr/bin/grep -vE '^[^:]+:[0-9]+:[[:space:]]*[#>]'` | no output |
| AC-02 | FR-1 | `git grep -c 'claude-opus-5' -- delivery-team/tests/smoke/tests/conftest.py` | `delivery-team/tests/smoke/tests/conftest.py:4` |
| AC-03 | FR-1 | `git grep -nE '"model": "claude-sonnet-5"' -- delivery-team/references/telemetry-schema.md` | prints line 36 |
| AC-04 | FR-1 | `git grep -nE 'claude-haiku-4-5-20251001' -- agentic-flow-builder/scripts/agent_registry.py` | exactly line 174 |
| AC-05 | FR-2 | `git grep -nE 'claude-(opus\|sonnet\|haiku)-4-' -- ':!.delivery' ':!.github/workflows/stale-model-id-guard.yml' \| /usr/bin/grep -vE '^[^:]+:[0-9]+:[[:space:]]*[#>]' \| /usr/bin/grep -v 'claude-haiku-4-5-20251001'` | no output |
| AC-06 | FR-2 | `sed -n '148p;189p' agentic-flow-builder/scripts/agent_registry.py \| /usr/bin/grep -cE '^[[:space:]]*#.*claude-(sonnet-4-6\|opus-4-7)'` | `2` |
| AC-07 | FR-3 | `git grep -n 'claude-fable' -- ':!.delivery' ':!.github/workflows/stale-model-id-guard.yml' ':!CHANGELOG.md'` | no output |
| AC-08 | FR-3 | `git grep -c 'fable-5-1' -- .github/workflows/stale-model-id-guard.yml` | `.github/workflows/stale-model-id-guard.yml:1` or higher |
| AC-09 | FR-4 | `python -m pytest delivery-team/tests/smoke/tests -q` | exit 0, `3 passed` (never fewer) |
| AC-10 | FR-4 | `git diff -U0 -- delivery-team/tests/smoke/tests/conftest.py \| /usr/bin/grep -E '^[+-]' \| /usr/bin/grep -vE '^(\+\+\+\|---)' \| /usr/bin/grep -vc 'claude-'` | `0` (run pre-commit; post-commit use `git show HEAD -- <file>` in place of `git diff`) |
| AC-11 | FR-5 | `git grep -ohE 'claude-(opus\|sonnet\|haiku\|fable)-[0-9][^ "'"'"',]*' -- delivery-team/references/telemetry-schema.md delivery-team/architecture/smoke-test-architecture.md delivery-team/tests/smoke/tests/conftest.py \| sort -u \| /usr/bin/grep -vxE 'claude-(opus-5\|sonnet-5)'` | no output, grep exit 1 |
| AC-12 | FR-6 | runner: `bash /tmp/g.sh; echo $?` on clean clone | `No non-allowlisted model IDs found.` then `0` |
| AC-13 | FR-6 | inject each of 8 IDs (matrix T-N1..N8) plus `{"model": "claude-opus-4-7"}` line in `.md` | each prints `README.md:<line>:...` and `1` |
| AC-14 | FR-6 | inject each of 4 allowed IDs (T-P1..P4) | each exit `0` |
| AC-15 | FR-6 | append `Use claude-haiku-4-5-20251001.` and `Use claude-opus-5, claude-sonnet-5, and claude-haiku-4-5-20251001.` -> exit `0`; append `Use claude-opus-5.1` -> exit `1` | as stated |
| AC-16 | FR-6 | `/usr/bin/grep -c 'github.event' .github/workflows/stale-model-id-guard.yml` | `0` |
| AC-17 | FR-7 | inject `# prior: claude-opus-4-8 (retired)` and `> prior: claude-opus-4-8` -> `0`; bare `prior: claude-opus-4-8` and `MODEL = "claude-sonnet-5"  # prior: claude-opus-4-7` -> `1` | as stated |
| AC-18 | FR-7 | `/usr/bin/grep -nE '\bclaude\b +(-\|--)\|curl\|wget\|pip install\|npx' .github/workflows/stale-model-id-guard.yml` | no output, exit 1 |
| AC-19 | FR-8 | `/usr/bin/grep -cE "'\*\*/\*\.(py\|md\|yml\|yaml\|json\|txt\|sh)'" .github/workflows/stale-model-id-guard.yml` | `7` |
| AC-20 | FR-8 | `echo '{"model": "claude-opus-4-7"}' > scratch.json && git add scratch.json && bash /tmp/g.sh; echo $?` (scratch clone) | `scratch.json:1:...` and `1` |
| AC-21 | FR-8 | `python3 -c "import yaml; yaml.safe_load(open('.github/workflows/stale-model-id-guard.yml'))"; echo $?` | `0` |
| AC-23 | FR-10 | `python scripts/check_skill_budgets.py; echo $?` and `git diff --numstat -- prompt-engineer/SKILL.md` | exit `0`; add count == delete count (`1 1`). Post-commit (working tree empty): `git diff --numstat 337edb5..HEAD -- prompt-engineer/SKILL.md` -> `1 1` |
| AC-24 | FR-10 | `git diff --name-only 337edb5..HEAD \| /usr/bin/grep -c 'delivery-team/skills/delivery-flow/SKILL.md' \|\| true` (post-commit form; bare `git diff` is empty after commit = vacuous pass) | `0` |
| AC-26 | FR-11 | `git show --stat --format= HEAD \| /usr/bin/grep -cE 'stale-model-id-guard.yml\|agent_registry.py'` -> `2`; CORRECTED: `git rev-list --count 337edb5..HEAD -- ':!.delivery'` -> `1` (replaces origin..HEAD form, see C2) | `2` and `1` |
| AC-27 | FR-11 | AC-12 runner on scratch clone of `HEAD` | `No non-allowlisted model IDs found.` `0` |

Note on sed: all guard runs use the `\2` script (C1). Do not copy `\3`.

### Test cases (guard matrix, scratch clone, inject one line per case)

| ID | Appended line | Exit |
|---|---|---|
| T-N1..N8 | `MODEL = "<ID>"` for `claude-opus-4-8`, `claude-fable-5`, `claude-mythos-5-1`, `claude-haiku-4-5`, `claude-opus-5-1`, `claude-sonnet-4-6`, `claude-opus-5.1`, `claude-opus-5-20260101` | 1 (8/8) |
| T-N9 | `{"model": "claude-opus-4-7"}` in tracked `.md` | 1 |
| T-P1..P4 | `MODEL = "<ID>"` for `claude-fable-5-1`, `claude-opus-5`, `claude-sonnet-5`, `claude-haiku-4-5-20251001` | 0 (4/4) |
| T-D1 | `Use claude-haiku-4-5-20251001.` | 0 |
| T-D2 | `Use claude-opus-5, claude-sonnet-5, and claude-haiku-4-5-20251001.` | 0 |
| T-D3 | `Use claude-opus-5.1` | 1 |
| T-E1 | `# prior: claude-opus-4-8 (retired)` | 0 |
| T-E2 | `> prior: claude-opus-4-8` | 0 |
| T-E3 | `prior: claude-opus-4-8` (bare) | 1 |
| T-E4 | `MODEL = "claude-sonnet-5"  # prior: claude-opus-4-7` | 1 |
| T-W1 | tracked `scratch.json` with stale ID | 1 |
| T-R1 | inject stale ID into ROOT `README.md` (and root `CHANGELOG.md`) with the `'*.ext'` ls-files globs | 1 (guards F-1 root-file false pass) |
| T-X1 | guard-only on old literals (pre-migration) | 1 (proves halves fail alone; atomicity) |

Rollback: `git revert` of shipping commit restores old guard + literals together.

---

## US-2 (Must): Live model-ID verification gate

As a reviewer, I want QA to re-fetch the live models page and record per-ID confirmation, so that the allowlist is not built on a 2026-06-24 cache.

File scope: `.delivery/artifacts/06-development/qa/model-id-verification.md` (new, no repo source). Depends on: none; blocks US-1 commit.
Content: fetch date, source URL https://platform.claude.com/docs/en/about-claude/models/overview, per-ID confirmation for all four, whether dated Haiku form is accepted by API, discrepancies. If live page contradicts an ID: allowlist changed to live value before merge, no dual-allow. If only Haiku alias appears: keep dated form (user instruction), record discrepancy.

| AC | FR | Command | Expected |
|---|---|---|---|
| AC-22 | FR-9 | `test -s .delivery/artifacts/06-development/qa/model-id-verification.md; echo $?` then `for i in claude-fable-5-1 claude-opus-5 claude-sonnet-5 claude-haiku-4-5-20251001; do /usr/bin/grep -q "$i" .delivery/artifacts/06-development/qa/model-id-verification.md \|\| echo MISSING $i; done` | `0`, then no output |

Test cases: T-V1 file absent -> `test -s` exit 1 (gate blocks); T-V2 one ID omitted -> prints `MISSING <id>`.

---

## US-3 (Must): CHANGELOG entry + dev-notes

As a release reader, I want an Unreleased changelog entry and dev-notes recording the skill load, so that the change is traceable and governance-compliant.

File scope: `CHANGELOG.md` (replace `[Unreleased]` placeholder line with a Changed entry naming `claude-opus-5`, `claude-sonnet-5`, `stale-model-id-guard`; history untouched). Entry wording must NOT contain retired IDs (`claude-opus-4-7`, `claude-sonnet-4-6`) on a non-`#`/`>` line: guard scans `*.md` and AC-01 covers CHANGELOG.md; use opus/sonnet tier wording or a `>` blockquote for retired IDs, `.delivery/artifacts/06-development/dev/dev-notes.md` (new; must mention `plugin-dev:skill-development` load). CHANGELOG edit is staged into US-1's single shipping commit. Depends on: none; must precede US-1 commit.

| AC | FR | Command | Expected |
|---|---|---|---|
| AC-25 | FR-10 | `/usr/bin/grep -c 'plugin-dev:skill-development' .delivery/artifacts/06-development/dev/dev-notes.md` | `1` or higher |
| AC-28 | FR-11 | `/usr/bin/grep -cE 'claude-opus-5\|claude-sonnet-5\|stale-model-id-guard' CHANGELOG.md` and `git diff 337edb5..HEAD -- CHANGELOG.md \| /usr/bin/grep -E '^-[^-]' \| /usr/bin/grep -vc 'No unreleased changes'` | first `>= 1`; second `0` (second is the post-commit form; pre-commit `git diff CHANGELOG.md` equivalent) |

Test cases: T-C1 historical entry edited -> second command prints `>=1` (fail); T-C2 dev-notes missing -> grep error/`0` (fail); T-C3 (F-3, not a PRD AC) `git grep -nE 'claude-(opus-4-7|sonnet-4-6)' -- CHANGELOG.md | /usr/bin/grep -vE '^[^:]+:[0-9]+:[[:space:]]*[#>]'` -> no output.

---

## US-4 (Should): Supersede BACKLOG-108 + follow-up backlog items

As PO, I want the superseded item retargeted and four follow-ups logged, so that deferred scope is not lost. Stage 8 work; no source edits, no PRD ACs.

File scope: proposed header text (PRD s9) for untracked BACKLOG-108 in main checkout (applied by its owner); new item files under `.delivery/backlog/`:
- `.delivery/backlog/BACKLOG-109-model-awareness-stamp-audit.md` (BACKLOG-A): `model_awareness` stamp + prose audit. Count is **25 SKILL.md files** (26 stamp lines; not 34); absorbs BACKLOG-108 S3.
- `.delivery/backlog/BACKLOG-110-cache-prefix-hash-drift.md` (BACKLOG-B): `governance/cache-prefix-hash.txt` drift (recorded `43067c9e...` vs SKILL.md sha256 `0a7aa92f...`; no CI reads it).
- `.delivery/backlog/BACKLOG-111-smoke-harness-live-baseline.md` (BACKLOG-C): smoke-harness metrics / live baseline (local-only, claude CLI); absorbs BACKLOG-108 S5.
- `.delivery/backlog/BACKLOG-112-fable-adoption-conditional.md` (BACKLOG-D, conditional): Fable adoption only on measured need.
Depends on: none.

| AC | Command | Expected |
|---|---|---|
| US4-a | `for f in .delivery/backlog/BACKLOG-109-*.md .delivery/backlog/BACKLOG-110-*.md .delivery/backlog/BACKLOG-111-*.md .delivery/backlog/BACKLOG-112-*.md; do test -s "$f" \|\| echo MISSING $f; done` | no output |
| US4-b | `/usr/bin/grep -cE '\b25\b' .delivery/backlog/BACKLOG-109-*.md` | `1` or higher |
| US4-c | `/usr/bin/grep -c '25 SKILL.md files' .delivery/backlog/BACKLOG-109-*.md` | `1` or higher |

Test cases: T-B1 BACKLOG-109 states 25 (`\b25\b` count >= 1, US4-b); it may mention "not 34" as correction, so no `34` absence check; T-B2 supersede header contains `Status: SUPERSEDED` and retarget lines opus-4-8->opus-5, sonnet-4-6->sonnet-5; T-B3 a missing file prints `MISSING <path>` (US4-a fails).

---

## Coverage table

| FR | ACs | Story |
|---|---|---|
| FR-1 | AC-01, 02, 03, 04 | US-1 |
| FR-2 | AC-05, 06 | US-1 |
| FR-3 | AC-07, 08 | US-1 |
| FR-4 | AC-09, 10 | US-1 |
| FR-5 | AC-11 | US-1 |
| FR-6 | AC-12, 13, 14, 15, 16 | US-1 |
| FR-7 | AC-17, 18 | US-1 |
| FR-8 | AC-19, 20, 21 | US-1 |
| FR-9 | AC-22 | US-2 |
| FR-10 | AC-23, 24 (US-1); AC-25 (US-3) | US-1, US-3 |
| FR-11 | AC-26, 27 (US-1); AC-28 (US-3) | US-1, US-3 |

Count check: FR-1 4 + FR-2 2 + FR-3 2 + FR-4 2 + FR-5 1 + FR-6 5 + FR-7 2 + FR-8 3 + FR-9 1 + FR-10 3 + FR-11 3 = **28 ACs**, all mapped (AC-01..AC-28, none orphaned). 11/11 FRs covered. US-4 carries scope items (BACKLOG-108 supersede, BACKLOG-A..D) with no PRD AC.

## Open items

- QA FR-9 live fetch is merge gate (owner QA).
- Haiku 4-5 retirement not before 2026-10-15: rollover = one `ALLOW=` line + four Haiku sites; not blocking.
- `downstream_ready: true`.

## Verification note (self-correction round 1)

Run in worktree at base 337edb5 (nothing shipped yet, so post-commit forms are exercised on an empty range):
- F-1: `git ls-files '**/*.md' | grep -c '^README.md$'` -> `0` (bug reproduced); `git ls-files '*.md' | grep -c '^README.md$'` -> `1` (fix). AC-19 counts only `on.paths` `'**/*.ext'` lines: stays 7.
- F-2: `git diff --name-only 337edb5..HEAD | grep -c delivery-flow/SKILL.md || true` -> `0`; `git diff --numstat 337edb5..HEAD -- prompt-engineer/SKILL.md` -> empty pre-ship (becomes `1 1` after ship); CHANGELOG second command -> `0` pre-ship; `git rev-list --count 337edb5..HEAD -- ':!.delivery'` -> `0` pre-ship (becomes `1`).
- F-4/F-5: `.delivery/backlog/` exists, BACKLOG-109..112 unused (108 untracked in main); `grep -c 'model_awareness:'` over SKILL.md files -> 25 files with the stamp.
- AC count unchanged: 28 (F-3 check is test case T-C3, not a new AC).
