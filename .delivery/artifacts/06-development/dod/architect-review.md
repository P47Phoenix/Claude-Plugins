# Architect DoD Review - Development (ADR-models-001)

Verdict: PASS. No must-fix. Four notes.

## Criteria
| # | Criterion | Result | Evidence |
|---|---|---|---|
| 1 | Positive allowlist | PASS | Guard sed-strips ALLOW IDs, fails on any leftover `claude-(family)-<digit>` token |
| 2 | Single ALLOW var, prefix-less tails | PASS | `ALLOW='fable-5-1\|opus-5\|sonnet-5\|haiku-4-5-20251001'` |
| 3 | Static grep only, GNU grep, no `claude` CLI | PASS | git ls-files + xargs grep/sed only |
| 4 | No dual-allow window | PASS | Only 4 current IDs; no 4-7/4-6/4-8 in ALLOW |
| 5 | Provenance exemption (`#`/`>` line start) | PASS | grep -vE on `file:line:` prefix; BACKLOG-108 record uses `>` |
| 6 | Exclusions | PASS | `.delivery/*`, prd_flows.db, guard file; 7 file types |
| 7 | Rollover = edit ALLOW only | PASS | Arch s.rollover documents; TOK edit only for new family (fable/mythos pre-seeded) |
| 8 | Atomic single commit readiness | PASS | Guard + literals in the same working tree; my rerun of the guard pipeline on the tree gives zero hits |
| 9 | FR-9 verification file exists and gates | PASS | qa/model-id-verification.md: live fetch 2026-09-19, 4 IDs confirmed, AC-22 run PASS; allowlist matches |
| 10 | cache-prefix-hash honestly deferred | PASS | us-1.md states no cache-prefix files touched (BC-10); BACKLOG-110 OPEN records drift |
| 11 | BACKLOG-108 superseded record coherent | PASS | Retarget opus-5/sonnet-5/haiku unchanged/fable allowlisted-not-adopted; split-outs map to 109/110/111/112, all exist |

## Blind spots (honest, none correctness gaps)
- Unscanned types: .toml/.cfg/.ini/.ts/.js/.tsx. Current tree: no ID hits in them (only .py hits, which are scanned). Arch doc failure-mode table does not list this. NOTE: add one line to architecture.md s.4 or BACKLOG.
- Legacy/dot forms (`claude-3-5-sonnet`, `claude-3-opus`): not matched by TOK (family must follow `claude-`). Zero hits in tree. Undocumented. NOTE.
- Bedrock/Vertex `@date` and `-v1:0` suffix forms: token matched up to `@`; stale ones caught, allowed ones with `@` pass delimiter. Haiku `claude-haiku-4-5@20251001` fails by design (not in ALLOW); documented only in QA note. NOTE.
- Bare aliases (`model: opus|sonnet` in agents/*.md frontmatter, 15 occurrences): intentionally out of scope, family aliases exempt (carried in BACKLOG-108 record). Not a version pin. Acceptable.
- Paths trigger: PR touching only unlisted types (.toml, .ts, ...) skips the guard. Same set as scanned files, so consistent; no false-green on scanned content. Acceptable. Undocumented; NOTE.
- Guard file self-excluded: documented risk, covered by FR-6 ACs.
- Split-line/concat IDs: documented, accepted.

## Must-fix
None.
