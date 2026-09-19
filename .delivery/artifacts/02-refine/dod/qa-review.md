# QA DoD Review: Refine (Light), Round 3

SKILL_LOADED: delivery-team:quality (loaded OK by QA). Gap: PO's last revision reports its own skill load failed (rate limit). Judged on merit; no artifact defect traced to it.

**Verdict: DONE (PASS). 0 blocking, 1 minor non-blocking (M-1).**

Method: scratch clone `/tmp/q3` of HEAD 337edb5. Pre-edit run on current tree. Post-edit state simulated (10 live sites, S1/S5 comments, guard workflow rebuilt from PRD section 12 reference body, CHANGELOG entry) as ONE commit. Repo not mutated.

## 1. Inventory
FR-1..FR-11 = 11 FRs. ACs = 28 (FR1:4, FR2:2, FR3:2, FR4:2, FR5:1, FR6:5, FR7:2, FR8:3, FR9:1, FR10:3, FR11:3). Every AC is a runnable command with expected result. PASS.

## 2. AC run results (pre = current tree, post = simulated)
| AC | Pre | Post | Verdict |
|---|---|---|---|
| FR1 live-line grep empty | 12 lines (fails, intended) | empty | PASS |
| FR1 conftest count | rc1 | `conftest.py:4` | PASS |
| FR1 telemetry line 36 | none | line 36 | PASS |
| FR1 haiku line 174 only | 174 | 174 | PASS |
| FR2 non-comment 4.x grep | 10 lines | empty | PASS |
| FR2 sed 148/189 count | 0 | 2 | PASS |
| FR3 no claude-fable | empty | empty | PASS |
| FR3 fable-5-1 in guard | rc1 | `:1` | PASS |
| FR4 pytest | 3 passed | 3 passed | PASS |
| FR4 conftest diff only claude- lines | n/a | 0 | PASS |
| FR5 non-allowlisted in 3 files | 4-7, 4-6 | empty rc1 | PASS |
| FR6 base / neg / pos / delimiters / github.event | see section 4 | all as expected; github.event=0 | PASS |
| FR7 exemption cases; no claude/curl/etc | see section 4 | as expected; rc1 | PASS |
| FR8 glob count 7 / .json inject / yaml load | 2 / n/a / ok | 7 / exit1 / rc0 | PASS |
| FR9 verification file | absent (Stage 6 by design) | 4 IDs present, loop prints nothing | PASS |
| FR10 budgets rc0; delivery-flow untouched 0; numstat 1/1; dev-notes grep | 0 | rc0, 0, 1/1, 1 (after file exists) | PASS |
| FR11 stat=2; rev-list=1; CHANGELOG count 1, removed-lines 0 | rev-list 0 | 2, 1, 1, 0 | PASS |

Pre-edit failures confirm the ACs discriminate. Origin tip is 337edb5, so rev-list is 0 before and 1 after commit.

## 3. constraints.yml
Parses (yaml.safe_load OK). 14 BCs (BC-01..BC-14), allowlist 4 IDs, matches PRD. PASS.

## 4. Guard spec cases (my own runs, guard from `steps[1].run`, 16 lines)
- Base tree: `No non-allowlisted model IDs found.` exit 0.
- exit 1: opus-4-8, fable-5, mythos-5-1, haiku-4-5, opus-5-1, sonnet-4-6, opus-5.1, opus-5-20260101, **opus-4-7, sonnet-4-5**, bare `{"model": "claude-opus-4-7"}` in .md and tracked .json/.txt/.sh.
- exit 0: fable-5-1, opus-5, sonnet-5, haiku-4-5-20251001; trailing `.` and `,` after allowed IDs; `(claude-opus-5)`.
- Trailing `.`/`,` after a disallowed ID (`claude-opus-4-7.`, `claude-opus-4-7,`) still exit 1.
- Exempt: `# ...`, `> ...`, indented `#`. Not exempt: bare line, `MODEL = "claude-sonnet-5"  # prior: claude-opus-4-7` (exit 1).
PASS.

## 5. Site map vs repo inventory and consistency
- `git grep -noE` outside `.delivery/`: 22 hits (agent_registry 6, conftest 4, smoke doc 2, telemetry 1, prompt-engineer 1, guard 8) = PRD section 1 exactly. Line numbers S1-S14 match. S16 clean.
- Counts consistent: 10 live sites (FR-1, section 5 net line), 2 provenance edits, 2 unchanged. 8 neg / 4 pos IDs consistent across FR-6, section 10, section 12, BC-02.
- Repo claims verified: cache-prefix-hash 43067c9e vs actual 0a7aa92f, no `.github` reader; no sampling params in Python; tests reference only the 4 fixture strings.
PASS with M-1.

**M-1 (minor, non-blocking): "34 SKILL.md" stamps is wrong.** PRD lines 48 and 142 say 34 stamped SKILL.md. Repo: 34 SKILL.md exist, only 25 carry `model_awareness:` (idea-brief says 25). Out-of-scope prose, no AC affected. Fix: change "34 SKILL.md" to "25 SKILL.md (of 34)" in section 4 and BACKLOG-A. Line 158 quotes BACKLOG-108 verbatim; leave.

**Advisory (no action required):** FR-11 rev-list `=1` assumes no separate unpushed `.delivery/` artifact commit. If Stage 6 commits pipeline artifacts separately first (as 337edb5 did), count is 2. Optional hardening: `git rev-list --count origin/delivery-team-agent-wrappers..HEAD -- . ':!.delivery'`.

## 6. SKILL_LOADED gap
PO skill-load failure is a process note only. Artifact stands on the evidence above.
