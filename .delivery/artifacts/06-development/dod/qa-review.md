# QA DoD Review: Stories 1-2 (PR #88 CI fixes)

**Status**: DONE (all 16 ACs PASS; 2 non-blocking notes)
Env: GNU grep 3.12 at /usr/bin/grep (default `grep` on PATH is ugrep 7.8.4; guard rerun with GNU). All commands run by QA.

## Story 1
| AC | Expected | Actual | Result |
|---|---|---|---|
| 1.1 | no BUDGET VIOLATION, exit 0 | "BUDGET CHECK PASSED: 17 file(s), 0 known-debt, 0 exception(s)", exit 0 | PASS |
| 1.2 | <=497 | 497 | PASS |
| 1.3 | ok | ok | PASS |
| 1.4 | SKILL.md >=2; manifest ==1 | 2; 1 | PASS |
| 1.5 | each string >=1; verbatim | developer 1, presentation 1, alias-creator 1, orchestrator 2, Agent Invocation Template 1, role-agent-first 2. Text diff vs HEAD SKILL.md: only whitespace rewrap (one line joined, "fall back ... Agent Invocation Template (see ...") | PASS |
| 1.6 | "prefer" hit in Steps 4, 5 | line 335 (Step 4), line 368 (Step 5) | PASS |
| 1.7 | no new KNOWN_DEBT; skill-budgets.json diff empty | 0 lines diff (origin/main...HEAD and worktree); 0 known-debt | PASS |
| 1.8 | lint, header-warn exit 0 / no new warnings | `lint_known_debt.py` exit 0 "LINT OK". header-warn logic: 9 files missing model_awareness, all pre-existing (user-feedback personas x4, research-types x5); delivery-flow SKILL.md and new ref not in list. No new warnings | PASS |

TCs:
- TC-1.3 (lines 1-332 vs HEAD): identical.
- Prefer+fallback semantics (diff vs HEAD): Step 4 pointer keeps "prefer matching `delivery-<role>` agent via Agent tool, else fall back to inline Agent Invocation Template". Step 5 keeps "Role-agent-first rule as Step 4: prefer `delivery-<role>` agents". Removed text all present in the ref file (Step 4 role list, required fields, orchestrator hand-off, Step 5 sentence). PROSE STYLE block untouched. PASS.
- TC-1.5: `delivery-orchestrator` discoverable at SKILL.md:336. PASS.
- TC-1.6: only manifest comment at line 2 (no numeric claim). Dev updated SKILL.md "22 files" to 24 and manifest "22 entries" to 24 (22 + new ref + self entry was already counted; consistent with manifest edit). Not an AC; QA did not recount entries.
- Budget margin: 497/500, margin 3 (meets target).
- New-ref side effect: HEAD has role-agent-dispatch.md untracked; guard file-list uses `git ls-files` so it is scanned only once tracked. Manual scan of it: no 4.x model IDs.

## Story 2
| AC | Expected | Actual | Result |
|---|---|---|---|
| 2.1 | pre-edit 1 hit at :116; post-edit none | pre-edit (HEAD blob): line 116 `claude-sonnet-4-5`; post-edit HITS empty | PASS |
| 2.2 | line 116 exact text with 4-6 | `    {"model": "claude-sonnet-4-6", "dispatches": 5, "input_tokens": 4345, "output_tokens": 2589}` | PASS |
| 2.3 | HITS empty, "No stale" | HITS=[] (full pipeline, GNU grep) | PASS |
| 2.4 | 1 ins, 1 del | 1 file changed, 1 insertion(+), 1 deletion(-) | PASS |
| 2.5 | guard workflow diff empty | 0 lines | PASS |

## Story 3 (text only)
- AC-3.1: proposed text present in stories.md (Story 3 block); no PR edit made by QA. PASS.
- AC-3.2: checkboxes must be ticked only after run; QA ran budget, guard, lint, header-warn, diff. "all 4 required checks green on PR" cannot be ticked until CI runs (mark PARTIAL). PASS (rule stated).
- AC-3.3: `git diff origin/main...HEAD --stat -- '*/SKILL.md'` = 8 files (7 roles + delivery-flow), 99+/266-, net -167 (about -170). Consistent. PASS.

## Notes (non-blocking)
1. `manifest.yml` line 49 fails `yaml.safe_load` ("mapping values are not allowed here": unquoted `Git integration: ...`). Pre-existing at HEAD, not from this change. TC-1.7 fails as literally written; no CI job parses it. Suggest a separate fix (quote the purpose value), out of scope.
2. Default `grep` here is ugrep; the guard was rerun with /usr/bin/grep. CI uses GNU, so result stands.
3. Untracked new ref file must be `git add`ed so CI (and guard) sees it.
