run: run-2026-05-28-o48m
story: S2 (keystone prose), BACKLOG-108
role: qa (DoD validator; skill delivery-team:qa unknown, role applied directly)
commits: 31ae759, 1e36eb2 on 18b8e30. base_sha f4fea7db = `main` (same sha, so main: and base-sha evaluate the same)

## Verdict
S2_QA: DONE
blocking: 0

## AC results (raw output run by me)

| AC | Expected | Actual | Result |
|---|---|---|---|
| AC-2.1 (vs `main` and vs base-sha) | `0 source lines still present` | `main 0 source lines still present` / `f4fea7d 0 source lines still present` (no PRESENT lines) | PASS |
| AC-2.2 | 1 / 0 / 0 / 0 | `MODEL_ID = os.environ` 1; claude-id regex 0; `canonical <YYYY` 0; `Versioned Model Reference` 0 | PASS |
| AC-2.3 hedge scan | `0` | `0` | PASS |
| AC-2.5 | `OK` (cond, cap) | `True True 8 OK`; 8 added lines | PASS |
| AC-2.6 | 1 | `1` | PASS |
| PA-10 wc | 499 | delivery-flow 499, prompt-engineer 520, product-delivery 300 | PASS |
| PA-10 blocks | block 1 and 2 stay 4 lines | lines 27-30 = 4, lines 273-276 = 4 (viewed) | PASS |
| PA-10 rewritten lines differ | yes | AC-2.1 counter check, 0 present | PASS |
| PA-10 product-delivery net 0 | 300/300, unchanged | not in numstat | PASS |
| Budgets | exit 0 | `BUDGET CHECK PASSED: 17 file(s) checked, 0 known-debt, 0 exception(s).` rc=0 | PASS |
| FR-3.1 / AC-3.1b (these files only) | no pin or prose hits | guard `--list --paths` on 3 files + doctrine: 8 hits, all `stamp` (below); 0 `pin`, 0 `prose` | PASS for S2 scope |

Guard per-file output (rc=1 because stamps remain; S3 removes them):
```
stamp delivery-team/skills/delivery-flow/SKILL.md:5
stamp delivery-team/skills/delivery-flow/SKILL.md:9
stamp delivery-team/skills/product-delivery/SKILL.md:5
stamp delivery-team/skills/product-delivery/SKILL.md:7
stamp prompt-engineer/SKILL.md:6
stamp prompt-engineer/SKILL.md:8
stamp prompt-engineer/SKILL.md:415
stamp prompt-engineer/SKILL.md:417
files-scanned 4
guard-scope hits 8 files 3
```
orchestrator-doctrine.md: 0 hits. The guard-scope `hits 0` clause in AC-2.1 cannot be met until S3 (stamps); PRD text for S2 says prose/pin only, so I treat stamps as S3 debt, not S2 failure.

Numstat `git diff --numstat 18b8e30..HEAD` (all net zero):
```
6  6  delivery-team/references/shared/orchestrator-doctrine.md   (31ae759)
8  8  delivery-team/skills/delivery-flow/SKILL.md                 (31ae759)
18 18 prompt-engineer/SKILL.md                                    (1e36eb2)
```
product-delivery/SKILL.md: no diff (deliberate; FR-2.1 verdict is a ledger item for S3).

## Vacuity attempt
- AC-2.5 reads only `+` lines of `git diff -U0 main`. Base already had `dod_validators` at lines 275 and 455, but those lines are not added lines, so they cannot satisfy the AC. Added lines 27-30 carry "The latest Opus delegates ... more readily", line 273 carries "When the orchestrating session runs the latest Opus" (cond), line 275 carries `dod_validators.<stage>` + "cap" + "at most" + "subagents" (cap). Real edit satisfies it; no vacuous pass.
- Cap sentence is real prose: bound is dod_validators length, "on any model", matched by MUST NOT exceed line 276.
- AC-2.1 counter logic: 0 present against both refs; not satisfied by moved duplicates (untouched duplicates would show PRESENT).
- AC-2.2 `MODEL_ID = os.environ` count 1 is the real line in the snippet, not a comment elsewhere (grep count exactly 1, no id literal).

## Cache state (for S6 record)
- `sha256sum delivery-flow/SKILL.md` = `5489c4d6a27c...02c13`; `governance/cache-prefix-hash.txt` = `43067c9e07e0...b8328`. MISMATCH, EXPECTED until S6 re-freeze. Not a defect.
- Telemetry prefix `head -c 2048 | sha256sum` = `6c9664d99a42...a0055`; pre-s2-hashes.txt = `8c2ebf9705bc...37750`. DIFFERENT. S2 changed the first 2048 bytes (block 1 at lines 27-30 sits inside that window). Before value for S6 record is the pre-s2 file value; after is the new value. Expected, fine.

## Warnings
1. `prompt-engineer/SKILL.md:415,417` still carry `model_awareness: opus-4-7` and `pattern_library_version: 4-7-1` as stamp-doc example lines (not among the named 25). They are guard `stamp` hits. S3 must clear them, or they fail AC-3.1b.
2. PA-27 (dispatch prompt grep for `plugin-dev:skill-development`) and AC-2.3b (adversarial artifact, intent verdict line) are not exercised in this review; a separate reviewer artifact must supply them.
3. prompt-engineer at 520 lines passes budget (it is not the 500 cap tier); no headroom concern for S2.

## Evidence files
scratch scripts in /tmp/tmp.uJtTkXgGuW (ac21.py, ac23.py, ac25.py); no repo file other than this one written; no commits.
