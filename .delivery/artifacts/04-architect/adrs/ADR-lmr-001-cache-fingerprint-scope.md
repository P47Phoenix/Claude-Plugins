# ADR-lmr-001: Cache fingerprint scope and one-time re-freeze

- **Status**: Proposed (flips to Accepted when Stage 4 DoD passes)
- **Date**: 2026-09-20
- **Run**: run-2026-05-28-o48m, BACKLOG-108 (latest-model references)
- **Owner**: Solution Architect (PRD FR-6.2, BINDING-5.5, OQ-3)
- **Series note**: `lmr` is a series label (latest-model references), not a model reference. It replaces the PRD's planned name `ADR-5-0-001-cache-fingerprint-scope.md`, as FR-6.2 allows. AC-6.2 greps for `cache-fingerprint-scope`, which this file name carries.

## Context

`governance/cache-prefix-hash.txt` holds one line. Verified in this worktree:

```
$ sha256sum delivery-team/skills/delivery-flow/SKILL.md
43067c9e07e0b988cd976432dd07d5bb3d2336c41ad08a1b0064fb2fbd0b8328  delivery-team/skills/delivery-flow/SKILL.md
$ cat governance/cache-prefix-hash.txt        # identical line (also identical on main)
43067c9e07e0b988cd976432dd07d5bb3d2336c41ad08a1b0064fb2fbd0b8328  delivery-team/skills/delivery-flow/SKILL.md
```

So the frozen fingerprint is a hash of the **whole file**, not of a prefix. Three descriptions of "the prefix" exist in the repo and they disagree. The byte arithmetic below was run for real (`wc -c`, `head -c`, `head -N | wc -c`, and a Python offset scan of the file) on 2026-09-20:

| Description | Source | Measured boundary | Hash of that region |
|---|---|---|---|
| Whole file | `governance/cache-prefix-hash.txt` (what AC-6.1 checks) | 28,616 bytes (`wc -c`), 499 lines (`wc -l`) | `43067c9e...b8328` (matches the file) |
| "bytes 0..2048" | `ADR-tk2-001` section D (`head -c 2048 ... \| sha256sum`) and the `## Volatile` comment in the SKILL.md | byte 2048 falls inside line 40 (line 40 starts at byte 2018) | `8c2ebf97...37750` (does NOT match the governance file) |
| "end of Phase 3" | the same `## Volatile` comment ("prefix boundary sits at the end of Phase 3") and the design brief for this stage | `## Phase 4` heading starts at byte 15,479 (`head -248 \| wc -c` = 15,479) | `ac03f1f2...c60d` (does NOT match) |

The brief for this stage says the 2048-byte prefix "ends at the end of Phase 3". That is false by measurement: end of Phase 3 is byte 15,479, and byte 2048 is inside Phase 0 (`## Phase 0: Setup Wizard` starts at byte 1892). The SKILL.md comment claims both at once and is internally inconsistent. This ADR does not edit that comment (it is outside the PRD's scope and every SKILL.md edit spends line budget; see Consequences) but records the discrepancy so nobody derives a design from it.

No script, workflow or hook consumes the hash file. `grep -rn cache-prefix-hash` over `*.md *.yml *.py` outside `.delivery/` finds only CHANGELOG lines. The only reader is the S7 ship step and AC-6.1.

Which S2/S3 edits move bytes? Simulated on a scratch copy of the file (nothing in the tree was touched), applying the frontmatter stamp edits and a line-neutral rewrite of the two version blocks (lines 27 to 30 and 273 to 276; the exact text is in architecture.md section 5.2):

| Region | Bytes before | Bytes after | Delta |
|---|---|---|---|
| Frontmatter (`model_awareness`, `pattern_library_version`, `last_audited`, `fitness_review_due`, lines 1 to 26) | starts changing at byte 854 | | -2 (`opus-4-7` is 8 chars, `latest` is 6; the other three values keep their length) |
| Lines 27 to 30 (block 1, inside bytes 0..2048) | 320 | 351 | +31 |
| Lines 273 to 276 (block 2, after the Phase 3 boundary) | 311 | 350 | +39 |
| Whole file | 28,616 | 28,684 | +68 (= -2 + 31 + 39) |
| `## Phase 4` heading offset | 15,479 | 15,508 | +29 (= -2 + 31; block 2 is after it) |
| `head -c 2048` hash | `8c2ebf97...` | `66bcaa25...` | changed |
| Hash up to the Phase 4 heading | `ac03f1f2...` | `97817f68...` | changed |
| Whole-file hash (simulated) | `43067c9e...` | `f5329b59...` | changed |

Line count is unchanged (499 to 499), so the Tier-A budget is not affected (see ADR-lmr-003).

Reading: the S2/S3 edits change bytes 0..2048 (first difference at byte 854), so the prefix-only fingerprint of ADR-tk2 would be re-frozen regardless. Any fingerprint scope, including "none", is invalidated by S2/S3. Re-freezing is therefore mandatory and deliberate, which is exactly the "one-time deliberate prefix change" that ADR-tk2-001 section D.5 says needs a new ADR citing cache-cost impact. This ADR is that record.

Cache-cost impact: the prompt cache is keyed on a byte-identical prefix, so a byte change at offset 854 means the first session after ship reads this skill uncached. The size of that one-time cost is **UNVERIFIED** (nothing was measured, and this ADR does not depend on it). The benefit that motivates the change: the new content contains no model version, so a future model release changes zero bytes of this file and forces no re-freeze.

## Decision

1. **Scope stays as it is: the whole of `delivery-team/skills/delivery-flow/SKILL.md`, one `sha256sum` line.** No format change, no second file. AC-6.1 is unchanged: `sha256sum delivery-team/skills/delivery-flow/SKILL.md | diff - governance/cache-prefix-hash.txt && echo MATCH`.
2. **`delivery-team/references/shared/orchestrator-doctrine.md` is OUT of scope.** It is loaded on demand from a pointer at delivery-flow line 24, not part of the always-loaded skill body, and it is not edited for cache reasons. Its S2 edit (lines 77, 79, 82) is covered by AC-2.1 (source lines gone), the guard (`--paths`) and the S7 strict run, not by the fingerprint. Putting it in scope would need a multi-line hash file and a new AC-6.1 command for a file that is not on the cache path.
3. **Re-freeze procedure (S6), run only after S3 has passed DoD and no SKILL.md edit is pending:**
   ```bash
   sha256sum delivery-team/skills/delivery-flow/SKILL.md > governance/cache-prefix-hash.txt
   sha256sum delivery-team/skills/delivery-flow/SKILL.md | diff - governance/cache-prefix-hash.txt && echo MATCH
   wc -l delivery-team/skills/delivery-flow/SKILL.md    # must print 499 or fewer
   ```
   The second command must print `MATCH`. The third protects the Tier-A budget (500).
4. **Re-check at ship (S7 step 5)**, after the final rebase and after the CHANGELOG and memory edits. If it prints anything but `MATCH`, the S7 executor re-runs step 3 and records why in the S7 report. A rebase onto a `main` that advanced and touched this file is the expected cause.
5. **Any later edit to delivery-flow/SKILL.md re-runs step 3.** No silent drift: the S7 check is the only consumer, so it is the only thing that would notice.
6. The stale `## Volatile` comment ("bytes 0..2048", "end of Phase 3") is a known documentation defect. It is logged for a later wave; fixing it costs one in-place comment rewrite in an at-cap file and is not needed for this initiative.

Byte-arithmetic rule for the S6 developer: run the commands, do not estimate. The numbers in this ADR come from commands, and the Stage 6 developer validator must re-run the three commands above and paste output (memory lesson: cache-prefix ADRs need runs-the-command validation).

## Alternatives rejected

| Alternative | Why rejected |
|---|---|
| Fingerprint `head -c 2048` only (restore ADR-tk2 wording) | Not what the governance file holds. Also weaker: it would not notice a post-S6 edit at line 273 (byte 16,806 and later), and S7 step 5 exists precisely to catch silent edits. It would also lock a boundary that falls in the middle of Phase 0 line 40, which no reader can point at. |
| Fingerprint bytes 0..end of Phase 3 (the SKILL.md comment) | Same weakness for lines 273 to 276 and beyond. The regions after Phase 3 are edited by S2 too. Choosing it would also mean deciding which of two contradictory comments is right by convention rather than by measurement. |
| Multi-file fingerprint including `orchestrator-doctrine.md` | Changes the file format and AC-6.1 for a file outside the cache path. The mirror is guarded by other ACs. |
| Drop the fingerprint | Violates BINDING-5.3 (re-fingerprint after all SKILL.md edits) and G9. |
| Add a CI check for the hash | The existing hash has no CI consumer, and a workflow gated on the hash would fail every legitimate SKILL.md edit. The ship-time local check is the accepted control. |

## Consequences

- One deliberate cache invalidation for the delivery-flow skill at first load after ship (cost UNVERIFIED). Every later model release costs zero bytes here, because the file carries no version.
- The fingerprint is stronger than the prefix it claims to protect (whole file), at the price that every legitimate edit of this file forces an S6-style re-freeze. That was already true today.
- The documentation defect in the `## Volatile` comment remains until a later wave. It is carried as a risk (architecture.md section 9, U3).
- Line budget: this ADR adds no lines to any SKILL.md. The batching claim "S2 block rewrite plus S3 stamp edits keep delivery-flow at 499" is proved with numbers in ADR-lmr-003.

## Status rationale

Proposed, not "Accepted (contingent...)". It becomes Accepted when the Stage 4 DoD validators pass; no contingency clause exists.
