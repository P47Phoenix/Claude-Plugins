# ADR-lmr-001: Cache fingerprint scope and one-time re-freeze

- **Status**: Accepted (Stage 4 DoD passed 2026-09-20: architect, developer, devops, security, qa all DONE)
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

So the frozen fingerprint is a hash of the **whole file**, not of a prefix. Four descriptions of "the prefix" exist in the repo and they disagree (revision 1 added row 4, found by adversarial review F1). The byte arithmetic below was run for real (`wc -c`, `head -c`, `head -N | wc -c`, and a Python offset scan of the file) on 2026-09-20:

| Description | Source | Measured boundary | Hash of that region |
|---|---|---|---|
| Whole file | `governance/cache-prefix-hash.txt` (what AC-6.1 checks) | 28,616 bytes (`wc -c`), 499 lines (`wc -l`) | `43067c9e...b8328` (matches the file) |
| "bytes 0..2048" | `ADR-tk2-001` section D (`head -c 2048 ... \| sha256sum`) and the `## Volatile` comment in the SKILL.md | byte 2048 falls inside line 40 (line 40 starts at byte 2018) | `8c2ebf97...37750` (does NOT match the governance file) |
| "end of Phase 3" | the same `## Volatile` comment ("prefix boundary sits at the end of Phase 3") and the design brief for this stage | `## Phase 4` heading starts at byte 15,479 (`head -248 \| wc -c` = 15,479) | `ac03f1f2...c60d` (does NOT match) |
| "first 2048 bytes", executable | `delivery-team/hooks/telemetry.py` line 21 `PREFIX_READ_BYTES = 2048`; `_compute_prefix_hash` returns `sha256(SKILL.md[:2048])[:8]`; documented in `delivery-team/references/telemetry-schema.md` line 23 and ADR-tk0e-001 | same boundary as row 2 (byte 2048, inside line 40) | `8c2ebf97` (8 hex chars) for delivery-flow today; written to every telemetry row as `prefix_hash` |

What is true, after revision 1: the phrase "2048-byte prefix ends at the end of Phase 3" is false by measurement (end of Phase 3 is byte 15,479; byte 2048 is inside Phase 0, whose heading starts at byte 1892), and the `## Volatile` comment in SKILL.md is internally inconsistent because it claims both boundaries. But the bytes-0..2048 notion itself is NOT a stale comment: it is an executable definition (row 4, `telemetry.py`), the only executable "prefix" in the repo. The whole-file governance hash (row 1) and the 2048-byte telemetry hash (row 4) are two live, independent fingerprints with different scopes. This ADR does not edit the SKILL.md comment (outside PRD scope; every SKILL.md edit spends line budget) but records the discrepancy so nobody derives a design from it.

No script, workflow or hook consumes `governance/cache-prefix-hash.txt`. Re-run in revision 1 over all file types outside `.delivery/`: `grep -rIln 'cache-prefix-hash\|prefix_hash\|PREFIX_READ' .` lists `CHANGELOG.md`, `delivery-team/artifacts/06-dev/...` (two stale docs), `delivery-team/hooks/telemetry.py`, `delivery-team/references/telemetry-schema.md`, `delivery-team/skills/delivery-flow/SKILL.md` and `governance/fitness-review.md`. Only `telemetry.py` is code. The only reader of the governance hash is the S7 ship step and AC-6.1. The only code that hashes SKILL.md bytes is `telemetry.py`; `grep -rn prefix_hash delivery-team/tests` prints nothing, so no test pins any value and no downstream reader (dashboard, script) of `prefix_hash` exists in the repo.

Which S2/S3 edits move bytes? Simulated on a scratch copy of the file (nothing in the tree was touched), applying the frontmatter stamp edits and a line-neutral rewrite of the two version blocks (lines 27 to 30 and 273 to 276; the exact text is in architecture.md section 4, S2, "Exact delivery-flow rewrite"):

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

**Telemetry `prefix_hash` blast radius (run, not estimated).** `telemetry.py` resolves only skills under `delivery-team/skills/` (`SKILL_ROOT`), 17 tracked SKILL.md files, of which 13 carry stamps. A scratch simulation of the S3 stamp edits alone (value replacement of `model_awareness`, `pattern_library_version`, `last_audited` on the 25 stamped files; nothing in the tree touched) shows the first stamp line starts at byte 927 or earlier in every file (25 of 25 below 2048) and `sha256(file[:2048])[:8]` changes for 25 of 25. So, at ship, the telemetry `prefix_hash` changes for all 13 stamped `delivery-team` skills, not only delivery-flow. This is expected, needs no code change and breaks nothing (no consumer), but a telemetry reader that groups rows by `prefix_hash` sees a new group per skill from the ship date. The same fact means the prompt-cache prefix of each of those 13 skills changes, so the one-time uncached-first-read cost applies to 13 skills, not one (size still UNVERIFIED).

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
4. **Re-check at ship (ship-gate Block B step 7, ADR-lmr-005 item 8; revision 4 corrected the reference from "S7 step 5")**, after the final rebase and after the CHANGELOG and memory edits. If it prints anything but `MATCH`, the S7 executor re-runs step 3 and records why in the S7 report. A rebase onto a `main` that advanced and touched this file is the expected cause.
5. **Any later edit to delivery-flow/SKILL.md re-runs step 3.** No silent drift: the S7 check is the only consumer, so it is the only thing that would notice.
6. The stale `## Volatile` comment ("bytes 0..2048", "end of Phase 3") is a known documentation defect. It is logged for a later wave; fixing it costs one in-place comment rewrite in an at-cap file and is not needed for this initiative.
7. **S6 must also account for the telemetry hash (revision 1, F1).** Beside the governance re-freeze, the S6 report records before and after values of the 2048-byte hash for delivery-flow: `head -c 2048 delivery-team/skills/delivery-flow/SKILL.md | sha256sum | cut -c1-8` (before `8c2ebf97`, simulated after `66bcaa25`; the real after-value is recorded at S6) and states that all 13 stamped `delivery-team` skills will show a new telemetry `prefix_hash` at ship. The governance fingerprint stays whole-file; `telemetry.py` and its schema doc are NOT changed by this initiative (a change would alter the telemetry contract, ADR-tk0e-001, and no requirement asks for it). If a later wave wants one shared boundary, it must update the `PREFIX_READ_BYTES` constant, the schema doc and the SKILL.md comment together; that is a separate decision.

Byte-arithmetic rule for the S6 developer: run the commands, do not estimate. The numbers in this ADR come from commands, and the Stage 6 developer validator must re-run the three commands above and paste output (memory lesson: cache-prefix ADRs need runs-the-command validation).

## Alternatives rejected

| Alternative | Why rejected |
|---|---|
| Fingerprint `head -c 2048` only (restore ADR-tk2 wording) | Not what the governance file holds. Also weaker: it would not notice a post-S6 edit at line 273 (byte 16,806 and later), and ship-gate step 7 exists precisely to catch silent edits. It would also lock a boundary that falls in the middle of Phase 0 line 40, which no reader can point at. |
| Fingerprint bytes 0..end of Phase 3 (the SKILL.md comment) | Same weakness for lines 273 to 276 and beyond. The regions after Phase 3 are edited by S2 too. Choosing it would also mean deciding which of two contradictory comments is right by convention rather than by measurement. |
| Multi-file fingerprint including `orchestrator-doctrine.md` | Changes the file format and AC-6.1 for a file outside the cache path. The mirror is guarded by other ACs. |
| Drop the fingerprint | Violates BINDING-5.3 (re-fingerprint after all SKILL.md edits) and G9. |
| Add a CI check for the hash | The existing hash has no CI consumer, and a workflow gated on the hash would fail every legitimate SKILL.md edit. The ship-time local check is the accepted control. |

## Consequences

- One deliberate cache invalidation at first load after ship: delivery-flow (governance hash and prompt cache) plus the other 12 stamped `delivery-team` skills (telemetry `prefix_hash` and prompt cache), cost UNVERIFIED. Every later model release costs zero bytes in these files, because they carry no version.
- The fingerprint is stronger than the prefix it claims to protect (whole file), at the price that every legitimate edit of this file forces an S6-style re-freeze. That was already true today.
- The documentation defect in the `## Volatile` comment remains until a later wave. It is carried as risk P10 (architecture.md section 7).
- Line budget: this ADR adds no lines to any SKILL.md. The batching claim "S2 block rewrite plus S3 stamp edits keep delivery-flow at 499" is proved with numbers in ADR-lmr-003.

## Status rationale

Accepted (Stage 4 DoD passed 2026-09-20), not "Accepted (contingent...)"; no contingency clause exists.
