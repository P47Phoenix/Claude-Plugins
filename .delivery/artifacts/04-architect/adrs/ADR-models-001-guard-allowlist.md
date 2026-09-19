# ADR-models-001: Stale-model-ID guard as positive allowlist

Status: Accepted (binary rule: Accepted, no conditional status)
Date: 2026-09-19 | Deciders: Architect (solution), PO | Stage 4
Supersedes: the 2026-04-22 deny-regex guard design (allowlisted 4-7/4-6/4-5 dated, denied other 4.x). Prior ADR-002 breadcrumb pattern retained.

## Context

Guard denies stale 4.x IDs but allowlists the old canonical ones, so it protects `claude-opus-4-7` / `claude-sonnet-4-6` and misses new-generation drift. Latest set: `claude-fable-5-1`, `claude-opus-5`, `claude-sonnet-5`, `claude-haiku-4-5-20251001`. Constraints: static grep only (BC-01), no dual-allow (BC-03), provenance exemption kept (BC-04), one-line rollover, GNU grep (BC-05).

## Decision

Positive allowlist held in one shell variable `ALLOW` (prefix-less tails). Pipeline: find any `claude-(opus|sonnet|haiku|fable|mythos)-<digit>` token, drop line-start `#`/`>` lines, `sed`-strip allowed IDs when followed by a valid delimiter, re-grep for leftovers; any leftover fails. Scan 7 file types, exclude `.delivery/`, `prd_flows.db` and the guard file. Ship atomically with all literals. Verified on current tree: flags exactly the 10 live stale sites, exempts `#` provenance.

## Alternatives considered

| Option | Pros | Cons | Verdict |
|---|---|---|---|
| A. Positive allowlist (chosen) | Catches any unlisted or future ID incl. suffixed/dotted; rollover is one line; matches gate-patterns lesson (allowlist-over-deny) | Must edit on every release (intended forcing function); new family name needs `TOK` edit | Chosen |
| B. Deny-list of retired IDs | Tiny regex; no per-release edit for new IDs | Never catches unknown drift (`opus-4-8`, `fable-5`); list grows forever; current design's failure | Rejected |
| C. Pinned model-registry file (e.g. `governance/models.json`) read by guard and code | Single source for code and CI; could drive literals | Large scope: code must read the file; guard becomes coupled to a parser or needs jq; Python literals, docs and SKILL.md examples still hardcoded; violates literal-scoped request and adds a new artifact class | Rejected now; revisit with BACKLOG-A |
| D. Dual-allow window (old + new IDs allowed temporarily) | Staged rollout, smaller commits | Mixed state; the old IDs stay protected; forbidden by BC-03 | Rejected (constraint) |
| E. Guard first, literals later (or reverse) as two commits | Smaller diffs | Intermediate commit red or mixed | Rejected; single commit |

## Consequences

- One edit place: `ALLOW=`. Guard failures double as the list of sites to migrate.
- Historic IDs must sit on their own `#`/`>` line; trailing comments and JSON cannot carry them.
- Guard file is unscanned; its correctness rests on the FR-6/7/8 injection ACs.
- Undated `claude-haiku-4-5` alias rejected on purpose.
- Fable permitted, not adopted (BC-07).
- Provenance exemption travels with this ADR: changing `#`/`>` handling requires revising this ADR (ADR-revision pattern, not a silent edit).
- cache-prefix-hash unaffected (BC-10); stale drift deferred to BACKLOG-B. Because no cached-prefix file changes, Dev evidence is FR-10 AC2 plus the guard run.

## Rollback

`git revert` of the single shipping commit restores old guard and literals together.

## Verification

Run this stage: reference guard on current tree exits 1 with the 10 expected hits; provenance lines exempt. Remaining ACs (injection matrix, delimiter, YAML load) execute at Stage 6 per PRD FR-6..FR-8.
