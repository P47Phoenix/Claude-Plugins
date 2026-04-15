# Retrospective — Architecture Flow Docs (FLOW-1..FLOW-6)

**Facilitator:** Aragorn · **Run:** run-2026-04-11-i0j7 · **Date:** 2026-04-11

## What went well

- Team brainstorm yielded 18 proposals; PO synthesized to 6 (33% selection rate — healthy signal-to-noise).
- Two MERGE docs (FLOW-3 hook-firing-timeline, FLOW-4 dod-self-correction) honored multi-author input rather than arbitrarily picking one contributor.
- BRE honesty preserved: FLOW-2 explicitly states delivery-team has no BRE module; gating is convention-enforced, not engine-enforced.
- All 6 docs landed within their individual line caps; 12 Mermaid diagrams total (2 per doc, consistent rhythm).

## What didn't

- `delivery-team/ARCHITECTURE.md` was already at its 250-line cap before this run — the new "Detailed flow documents" section pushed it to 261 (within authorized tolerance, but the hard cap will pinch again next time).
- `delivery-team/architecture/` is a new subdirectory; contributors won't discover it without following cross-links. README pointer mitigates but doesn't eliminate.

## Insights

- **Paired-plugin brainstorm pattern from run h9i6 worked again**: Architect leads + 2 supporting roles in parallel produces higher-quality proposals than Architect solo. Promote this pattern.
- Supplement-via-subdirectory is a viable pressure-relief valve for capped top-level architecture docs.

## Actions

- [ ] Consider raising `ARCHITECTURE.md` cap to 275 to absorb future flow-doc index growth, OR exclude the "Detailed flow documents" index section from the cap.
- [ ] Add `architecture/` directory discovery hint to new-contributor onboarding next time `CLAUDE.md` is touched.
