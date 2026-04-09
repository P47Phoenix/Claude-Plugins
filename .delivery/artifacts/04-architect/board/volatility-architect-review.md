# Volatility Architect Review — architecture.md

STATUS: CONDITIONAL
FINDINGS: .delivery/artifacts/04-architect/board/volatility-architect-review.md
SUMMARY: Decomposition mostly honors Lowy's Golden Rule, but two components remain cut by feature rather than by axis of change.

## Gate 1 — Golden Rule citation / upholding
- No explicit citation of Lowy's Golden Rule in architecture.md (architecture.md:1-88). The design is defensible but should name the rule it obeys. Minor.

## Gate 2 — Functional-decomposition trap
- BLOCK-adjacent: "Persona Library File Structure" (architecture.md:28-50) is cut by *artifact type* (personas), not by an axis of change. What actually varies: (a) persona roster composition, (b) prompt-template wording, (c) gate-criteria evolution. These three volatilities are collapsed into one Markdown file. When gate-criteria evolve independently of roster, every edit touches the same surface.
- "team-patterns.md Augmentation" (architecture.md:56-66) is cut by *where it lives* (Pattern 3b), which is functional. The real axis: dispatch protocol volatility vs. convergence-policy volatility.

## Gate 3 — Volatility classes named
- Not named. Implicit classes detectable: config-schema volatility, persona-content volatility, dispatch-protocol volatility, judge-protocol volatility. Make them explicit in §2-§5.

## Gate 4 — One component <-> one axis
- `architecture_board` config block (architecture.md:13-26) passes — single axis (board policy).
- Judge persona structure (architecture.md:52-54) passes — judge protocol changes independently.
- MAR routing §7 (architecture.md:72-74) passes — rotation logic is its own axis. Good.
- Persona library file FAILS — three axes in one file (see Gate 2).

## Recommendation
CONDITIONAL. Split the persona library conceptually (even if one file) into roster-index vs. persona-bodies, and name the four volatility classes explicitly. No structural rewrite required.
