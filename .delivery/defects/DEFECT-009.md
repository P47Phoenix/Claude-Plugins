<!-- run: run-2026-09-18-pr88 -->
# DEFECT-009: stale SKILL.md line anchors in docs (pre-existing)
- Severity: Trivial (P4); Found by: QA exploratory session
- `delivery-team/architecture/sub-agent-dispatch.md:51` cites "SKILL.md line 699"; delivery-flow SKILL.md is 497 lines. Also `governance/cache-prefix-hash.txt` records a stale whole-file hash (2048-byte prefix hash itself unchanged by PR #88).
- Not a regression from PR #88. Fix: replace line anchor with a section anchor; refresh hash file per governance doc.
