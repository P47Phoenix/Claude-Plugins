# Architect DoD Review: Idea brief (model literal migration)

SKILL_LOADED: delivery-team:architect | Role: Solution | Task: review | Model: sonnet

Verdict: feasible. No blockers. 3 PASS, 0 FAIL, 4 advisory notes.

## Criteria

| # | Criterion | Result |
|---|---|---|
| 1 | Literal-site inventory complete | PASS |
| 2 | Fixture change (conftest.py) safe | PASS |
| 3 | Static-grep positive allowlist expressible, incl. fable-5-1/opus-5/sonnet-5/haiku-4-5-20251001 | PASS |

### 1. Inventory
Own grep `claude-(opus|sonnet|haiku|fable|mythos)-[0-9]...` over whole tree (excl .git, .delivery), all file types: hits only in the 6 files + guard yml the brief lists. Line numbers match exactly (agent_registry 148/149/173/174/189/190; conftest 105/117/129/151; prompt-engineer 368; telemetry-schema 36; smoke-test-architecture 115/116). Zero `claude-fable`, zero `.json/.yml/.sh` literals besides guard. No hook or test pins a versioned ID. `model:` frontmatter: 14 sonnet + 1 opus, aliases only. Confirmed.
Note: `agent_registry.py` comments at 148/173/189 also say "opus-4-7 migration" (no `claude-` prefix, not caught by any ID regex). Reword them when editing so provenance stays accurate.

### 2. Fixtures
`python3 -m pytest -q` in delivery-team/tests/smoke: 3 passed (pytest 9.0.3 available). Grep of tests/ shows no assertion on the `opus-4-7` literal; conftest strings are only fixture data. Changing to `claude-opus-5` is safe. Keep telemetry-schema.md:36 and smoke-test-architecture.md:115-116 in sync (docs only).

### 3. Guard
Feasible in pure `git ls-files | grep`. Sketch: extract all `claude-(opus|sonnet|haiku|fable|mythos)-[0-9][-0-9a-z.]*` matches, drop lines whose text (after `file:line:`) starts with `#` or `>`, then drop allowed IDs with `grep -vE` on an exact-token allowlist:
`claude-(fable-5-1|opus-5|sonnet-5|haiku-4-5-20251001)([^0-9a-z.-]|$)`.
The trailing boundary is required so `claude-opus-5-1`, `claude-sonnet-5-20250101`, `claude-fable-5` (prefix of fable-5-1) are NOT accepted by prefix. Existing guard's `[^7]` trick and `\b` are brittle; replace.

## Advisory notes (not FAIL)
- A. Line-level exemption: a line with both an allowed and a stale ID passes only if the stale is in a comment line; do the allowlist check per-match (`grep -o`, then filter tokens), not per-line, else `"claude-opus-5" ... claude-opus-4-7` on one line slips through. Use `grep -Eno` then filter.
- B. Inline trailing comments (`code  # prior: claude-x`) are NOT exempt under a line-start rule. Current repo has none (registry provenance is on own `#` lines), so fine; document it.
- C. Prose false positives: 11 non-comment prose lines mention "Opus 4.7" (space/dot form, no `claude-` prefix), so the ID regex ignores them. Good; but CHANGELOG.md historical lines containing full IDs would need `>` or exclusion. Currently none found with full IDs.
- D. Widening scan paths to `*.yml/*.json/*.txt` would self-match the guard file's own allowlist and `.github/workflows` text; exclude the guard file (or keep the allowlist in a `#`-free helper file excluded by pathspec). Also `governance/cache-prefix-hash.txt` needs re-freeze only if delivery-flow/SKILL.md changes; this migration need not touch it (stamps out of scope), so likely no re-freeze.
- E. Live-model-ID verification (brief's caveat, skill table cached 2026-06-24) remains a Refine action; feasibility does not depend on it.
