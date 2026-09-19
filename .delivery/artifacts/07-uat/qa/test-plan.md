<!-- run: run-2026-09-19-models -->
# UAT Test Plan and Results - run-2026-09-19-models (FEATURE)

Scope: repo-wide model-ID migration (claude-opus-5, claude-sonnet-5, claude-haiku-4-5-20251001 kept; claude-fable-5-1 allowlisted, not adopted); positive-allowlist stale-model-id-guard.
Tree: uncommitted worktree pr88, branch delivery-team-agent-wrappers. Commands lifted from `.github/workflows/*.yml` (run blocks extracted via PyYAML into /tmp/qa/*.sh). Guard uses `git ls-files`, so untracked files are outside its view (none carry IDs).

## 1. CI reproduction (executed)

| # | Workflow / job | Command | Exit | Output |
|---|---|---|---|---|
| C1 | skill-line-budget / budget-check | `python3 scripts/check_skill_budgets.py` | 0 | BUDGET CHECK PASSED: 17 files, 0 known-debt, 0 exceptions |
| C2 | skill-line-budget / permissive scan (warn-only) | `... --warn-permissive` | 0 | Warnings only (user-feedback/persona SKILL.md 'should'/'can'); never blocks |
| C3 | lint-known-debt / lint | `python3 scripts/lint_known_debt.py` | 0 | LINT OK: JSON<->Python in sync; frontmatter complete |
| C4 | stale-model-id-guard | run block extracted via yaml, `bash` | 0 | No non-allowlisted model IDs found |
| C5 | workflow-injection-lint | run block extracted, `bash` | 0 | OK: no injection antipattern found |
| C6 | skill-md-header-warn | run block, `continue-on-error` | 0 | Warn-only: 8 SKILL.md lack `model_awareness:` (user-feedback personas x4, research-types x4); pre-existing, non-blocking |
| C7 | docs, fitness-review, release, version | inspected | n/a | Not PR-path-triggered by this change / need GH runtime (mkdocs deploy, cron, tag/release, push-to-main). No model-ID logic. Not executable locally |

Additional runtime: `py_compile` on agent_registry.py and conftest.py = OK; `pytest` in delivery-team/tests/smoke = 3 passed.

### Guard negative/boundary cases (temp git repo /tmp/qa/g, real guard script)
| Input | Expected | Actual |
|---|---|---|
| claude-opus-4-7 | FAIL | FAIL |
| claude-sonnet-5.1 | FAIL | FAIL |
| claude-opus-5-1 | FAIL | FAIL |
| claude-opus-5x | FAIL | FAIL |
| claude-haiku-4-5 (undated) | FAIL | FAIL |
| claude-fable-5-1-preview | FAIL | FAIL |
| claude-sonnet-5. (sentence end), claude-opus-5, (comma), claude-haiku-4-5-20251001 | PASS | PASS |
| `  # claude-opus-4-7 provenance` | PASS (exempt) | PASS |
| claude-3-5-sonnet in .md | out of pattern (legacy) | PASS (not detected) - known gap |
| claude-opus-4-7 in .toml / .ts | unscanned | PASS (not detected) - known gap |

Positive: 6/6 negatives blocked, 4/4 valid forms pass. Legacy `claude-3-*` and unscanned types confirmed as blind spots (by design, per ADR).

## 2. Exploratory session - Cross-Story Interaction

Charter: explore agent_registry.py defaults, smoke fixtures, telemetry-schema, docs and the guard to discover disagreement or IDs the guard cannot see. Tour: consistency / landmark. Oracle: HICCUPPS (Consistency, Claims). Time-box: 30 min.

Observations:
1. Agreement: tree-wide live IDs = claude-opus-5 (9), claude-sonnet-5 (5), claude-haiku-4-5-20251001 (1), claude-fable-5-1 (2, allowlist + doc). agent_registry.py, conftest.py, telemetry-schema.md, smoke-test-architecture.md, prompt-engineer/SKILL.md all use the same tiers as the guard ALLOW list. No mismatch.
2. Retired IDs remaining (5 distinct: haiku-4-20250514, opus-4-20250514, opus-4-7, sonnet-4-5-20250929, sonnet-4-6) occur only in 3 `# prior:` provenance comments in agent_registry.py (lines 148, 173, 189). All exempt by design. Count of non-provenance retired IDs guard-visible: 0.
3. Retired/legacy IDs on non-provenance lines in file types the guard cannot see (.toml/.ts/.js/.cfg/etc.): 0 tracked files. Legacy `claude-3-*` and `@date` forms: 0 hits.
4. `agents/*.md` frontmatter `model:` uses alias `sonnet` (14 occurrences, 3 agents); marketplace.json and .delivery/config.yml name no model. Alias, not ID: guard neither needs nor sees it. Not stale.
5. `model_awareness:` stamps (26 files: 7 `opus-4-7`, 19 `opus-4-7-frontmatter-only`) lack the `claude-` prefix so the guard cannot see them. They now read behind the live tier (deferred, BACKLOG-109). Count: 26.
6. Cosmetic: agent_registry.py:173 comment says "opus-4-7 migration" on the unchanged Haiku line (date 2026-04-22); accurate history, no action.
7. `on.paths` coverage: triggers on py/md/yml/yaml/json/txt/sh, excluding `.delivery/**`. Matches exactly the file types the scan pattern uses; every file carrying an ID (py, md) triggers it. Gap only for unscanned types (none carry IDs today). A change to the guard itself (`.yml`) also triggers it.
8. governance/cache-prefix-hash.txt is stale vs edited SKILL.md (prompt-engineer/SKILL.md changed); already DEFECT-009 / BACKLOG-110. No new instance found.

Result: no new bugs. No defect files logged (next free number would be DEFECT-010, unused).

## 3. Shared-module review <!-- retro c8f2 -->

**Shared modules identified**: 7 modified, all referenced in 2+ stages (refine, architect, plan, development, uat artifacts).

| Module Path | Stages Referencing | Modified in Dev | Test Coverage | Status |
|---|---|---|---|---|
| .github/workflows/stale-model-id-guard.yml | 02, 04, 05, 06, 07 | Yes | C4 + 10 boundary cases above; injection-lint C5 | PASS |
| agentic-flow-builder/scripts/agent_registry.py | 02, 04, 05, 06 | Yes | py_compile; guard C4; defaults grep matches ALLOW; consumers: agentic-flow-builder and prd-quality-gate-flow import it (no ID literals elsewhere) | PASS |
| delivery-team/tests/smoke/tests/conftest.py | 04, 05, 06 | Yes | pytest 3 passed; guard C4 | PASS |
| prompt-engineer/SKILL.md | 02, 05, 06 | Yes | C1/C3 budget+lint OK; guard C4; example ID only | PASS |
| delivery-team/references/telemetry-schema.md | 02, 04, 05, 06 | Yes | guard C4; ID values agree with conftest fixtures | PASS |
| delivery-team/architecture/smoke-test-architecture.md | 04, 05, 06 | Yes | guard C4; doc ID equals fixture ID | PASS |
| CHANGELOG.md | 06, 07 | Yes | Reads consistent with guard behavior and allowlist | PASS |

**Findings**: consuming contexts verified by grep; no consumer hardcodes a retired ID. Integration impact nil. Cross-story interaction covered by section 2. Note: governance/cache-prefix-hash.txt drift is pre-existing.

## 4. Verdict: GO_WITH_NOTES

All executable CI checks reproduce green on the uncommitted tree; guard boundary behavior correct; artifacts mutually consistent; zero new defects.

Residual risks (accepted, non-blocking):
- Haiku 4.5 (claude-haiku-4-5-20251001) retirement not before 2026-10-15: allowlist and agent_registry need a rollover then (edit ALLOW + one literal).
- model_awareness stamps (26 files, opus-4-7) deferred: BACKLOG-109.
- Stale governance/cache-prefix-hash.txt: DEFECT-009 / BACKLOG-110.
- Guard blind spots: unscanned file types (.toml/.ts/.js/.cfg), legacy `claude-3-*`/`@date` forms, un-prefixed stamps. Currently 0 real occurrences.
- Guard reads `git ls-files`: untracked files evade until added.
- Non-executable locally: docs, release, version, fitness-review workflows.
