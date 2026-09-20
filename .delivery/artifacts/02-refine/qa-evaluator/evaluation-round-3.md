# Gate 2 Evaluation, Round 3 (FINAL): BACKLOG-108 Opus 5 Migration PRD (Revision 2)

Evaluator: QA Engineer (evaluator only). Artifact: `.delivery/artifacts/02-refine/po/prd.md` (Revision 2). Framing: ACs judged for well-formedness, specificity, testability and runnability, not for passing today. Binding retarget to `claude-opus-5` not re-debated.

**Verdict: REVISE** (1 blocking defect, D3-1, one-line mechanical fix; 1 warning). All four round-2 defects verified resolved except that the D2-1 fix (AC-1.2c reachable at 0) is defeated by a second, unrelated stale literal the new broad STALE_RE catches.

## 1. Gate 2 per-criterion results

| # | Criterion | Sev | Result | Note |
|---|-----------|-----|--------|------|
| 1 | Every FR has AC with testable condition | blocking | PASS | FR-2.5 (AC-2.5), FR-5.7 (AC-5.7, inspection with named evidence), FR-7.5 (AC-7.5) well-formed. All FRs mapped |
| 2 | NFRs quantified | blocking | FAIL (via D3-1) | NFR-1..9 numeric, but NFR-5 (guard false positives = 0) is not reachable after S4 as scoped |
| 3 | Out-of-scope present | blocking | PASS | Sec 10 |
| 4 | Success metrics numeric + method | blocking | FAIL (via D3-1) | G-LIT closing AC-1.2c cannot reach 0 as scoped; other gates fine (G1..G10, one closing story each) |
| 5 | No blocking open questions | blocking | PASS | OQ-1..8 each with owner, due, non-blocking rationale; OQ-7/OQ-8 UNVERIFIED items are gated by FR-5.7 / explicit runner effort |
| 6 | Personas specific | warning | PASS | 3 personas |
| 7 | Dependencies w/ status | warning | PASS | Sec 7 |
| 8 | Risks L/I/mitigation | warning | PASS | R1-R7; R1/R6/R7 well-formed (L, I, mitigation, tied to OQ/FR) |
| 9 | Assumptions explicit | suggestion | PASS | 5 assumptions |
| 10 | Discovery numbers accurate | blocking | PASS | All reproduce exactly (sec 3) |

## 2. Round-2 defect resolution

| Defect | Status | Evidence |
|--------|--------|----------|
| D2-1 AC-1.2c vs FR-4.1 trailing comment | RESOLVED (design) | FR-4.1 puts provenance comment on its own line above registry line; guard `#`-first-char exemption covers it; AC-4.1 checks placement; AC-1.2a fixture confirms the comment line is not a hit. BUT see D3-1: AC-1.2c still cannot print 0 for a different reason |
| D2-2 Literal counts reproduce | RESOLVED | Canonical command run: `claude-opus-4-7 hits 9 files 5` with exact file:line list; `claude-opus-4-8 hits 0 files 0`; 7 hits in 4 files excluding guard yml. Identical to PRD text and table |
| D2-3 AC-1.2a portability | RESOLVED | Contract forbids POSIX classes/single quotes/lookaheads; suggested STALE_RE/ALLOW_RE executed in Python `re` against the 5 fixtures: all behave as asserted (4-7 hit, 4-8 hit, opus-5 pass, sonnet-4-6 pass, `#` provenance line pass) |
| D2-4 git diff assumption | RESOLVED | AC-3.1 now states no SKILL.md is created; parenthetical removed |

## 3. Command-execution results (worktree root)

| Command / claim | PRD says | Actual | Match |
|---|---|---|---|
| Canonical literal count (4-7) | 9 hits, 5 files: guard [23,39], agent_registry [190], smoke-test-architecture [115], conftest [105,117,129,151], prompt-engineer [368] | identical | YES |
| Canonical literal count (4-8) | 0 / 0 | 0 / 0 | YES |
| SKILL.md count | 34 | 34 | YES |
| Stamp census | 26 lines / 25 files; 7 `opus-4-7` + 19 `frontmatter-only` | `26 25 {'...frontmatter-only': 19, 'opus-4-7': 7}` | YES |
| `validate_constraints.py` on constraints.yml | valid | `ok: ... valid against constraints schema`, rc=0 | YES |
| `check_skill_budgets.py` | exit 0 | PASSED, 17 files, exit=0 | YES |
| AC-6.1 sha256 diff | MATCH | MATCH | YES |
| AC-1.3 (claude CLI grep, `smoke-` count) | 0 / 0 | 0 / 0 | YES |
| AC-2.3 hedge scan | 0 | 0 | YES |
| `run_smoke.py` has `--effort` | absent today | grep returns nothing | YES (S5 adds) |
| AC-1.2a logic with suggested regexes | OK | all 5 fixture assertions hold | YES |
| AC-1.2c logic with suggested regexes on today's tree | expected non-zero before S1/S4, 0 after | 8 hits today: 7x `claude-opus-4-7` (all fixed by S4) plus 1x `claude-sonnet-4-5` at `delivery-team/architecture/smoke-test-architecture.md:116` | NO (D3-1) |
| Renamed files | old names gone, new exist | `BACKLOG-108-opus-5-migration.md`, `opus-5-migration.md` present; no opus-4-8 named files in `.delivery/backlog` or `.delivery/memory/topics` | YES |
| Heredoc python ACs (walk.py, AC-1b, census, AC-1.2a/c) | runnable | all execute under python3 stdlib | YES |

Note: `bash -n` on multi-line AC snippets was not runnable under this session's worktree-isolation shell filter; the bash ACs are single-line grep/test/sha256sum/diff commands and were executed directly where they have a today-value (AC-6.1, AC-1.3, AC-6).

## 4. Retarget-consistency findings

- Leftover `4-8`/`4.8` in PRD: 27 lines, all intentional: rename provenance, rejected-ID rules (FR-1.2, AC-1.2a fixture, AC-1b, G1, G-LIT), doc-citation rows describing 4.8 as legacy or the cache-min correction, OQ-2 comparison, and the Revision 2 changelog. None assume 4.8 behaviour as the target. No stale target references found.
- ACs/gates: stamps, guard allowlist, registry, conftest, baseline `model: claude-opus-5`, `model_usage.claude-opus-5.`, ADR-5-0-001 all consistent. AC-3.3a arithmetic (35 = 34 frontmatter + prompt-engineer example line 415) consistent with census and G2.
- Changelog matches body: ADR rename, FR-2.5/5.7/7.5, OQ-5..8, R6/R7, assumption 5, renames all present in the body. D2 fix table matches actual text.
- Memory file: Section 6 re-verification log present; its OPEN-1..4 map to PRD OQ-5..8 (numbering differs, non-blocking; PRD does not cite `OPEN-n`). constraints.yml, backlog file, state.md, index.md: no stale 4.8 targets (only the deliberate rejected-ID entries).
- Historical `.delivery/artifacts/01-idea/**` still cite old names: disclosed as immutable stage records (FR-7.5 note, changelog). Accepted.
- New FR/AC/risk well-formedness: FR-2.5/AC-2.5 (regex over added diff lines, prints OK) testable; FR-5.x ACs have specific commands and MUST-print values; R1/R6/R7 and OQ-2/5-8 have owner/due/why-non-blocking. Observation: R7 says the guard "will flag any `claude-sonnet-5`" which is true for the suggested STALE_RE.
- Regression check rounds 1-2: no regressions; D-1..D-13 fixes intact.

## 5. New defects and required fixes

**D3-1 (blocking) AC-1.2c / NFR-5 / G-LIT unreachable after S4 (sec 3 S1 FR-1.2; S4 FR-4.3).** With the PRD's suggested STALE_RE, which matches any `claude-(opus|sonnet|haiku)-<digit>...`, and ALLOW_RE, AC-1.2c also flags `claude-sonnet-4-5` at `delivery-team/architecture/smoke-test-architecture.md:116` (`{"model": "claude-sonnet-4-5", ...}` in the same code fence as line 115). FR-4.3 and AC-4.3 only change line 115 and only check `claude-opus-4-7`. After S1+S4 as written, AC-1.2c prints 1, not 0, so NFR-5 and the G-LIT closing AC fail through no fault of the developer. Executed evidence: today's tree yields 7x opus-4-7 + 1x sonnet-4-5.
Required fix (pick one, state it): (a) extend FR-4.3 to also replace `claude-sonnet-4-5` on line 116 with `claude-sonnet-4-6`, and extend AC-4.3 to `grep -c "claude-sonnet-4-5" ... MUST print 0`; or (b) narrow the guard contract so STALE_RE does not flag that fixture string (less preferred; the existing guard also treated non-4-6 Sonnet as stale). Option (a) is one line of PRD text. Also add a discovery sentence to sec 1 noting the guard's STALE_RE catches other stale IDs than the two counted literals, so the AC-1.2c pre-migration value is 8 (7 opus-4-7 in py/md plus 1 sonnet-4-5), not 7.

**D3-2 (warning) Minor.** AC-1.2c pre-migration expectation is described only as "non-zero"; give the exact today-value (8 with the suggested regexes) so a green run is meaningful, mirroring AC-1b. Optional.

## 6. Summary

Round-2 defects D2-1..D2-4 resolved in design; canonical counts, census, constraints validation, budgets and hash all reproduce exactly. Retarget is internally consistent. One residual blocking defect (D3-1): the broad guard contract catches a `claude-sonnet-4-5` string in `smoke-test-architecture.md:116` that no story rewrites, so AC-1.2c/NFR-5/G-LIT cannot reach 0. Fix is one FR/AC line. This is the final allowed round; if the PRD is not revised, PO must decide by explicit escalation to the human checkpoint rather than an unrecorded pass.
