# US-6 Developer Log

**Story:** Decomposition Hygiene sidebars in strategic-ddd.md (Phases 1–4)
**Alias:** Gimli

## Files touched
- `delivery-team/skills/architect/references/strategic-ddd.md`

## Insertion strategy
**Option A** — Phases 1–4 are distinct top-level sections. Inserted a dedicated blockquote sidebar at the start of each phase, phase-tailored.

## Line ranges (post-edit)
- Phase 1 sidebar: lines 24–29
- Phase 2 sidebar: lines 64–68
- Phase 3 sidebar: lines 106–111
- Phase 4 sidebar: lines 141–151

## Content coverage
- AC-6.1 (all 4 phases): core rule restated in every sidebar; forbidden vocabulary enumerated from ADR-003 in Phase 1 (Lambda, ECR, ECS, SQS, DynamoDB, S3, EC2, Kubernetes, Docker, Python, Node, TypeScript, Go, Rust, Java, Express, FastAPI, Django, PostgreSQL, MySQL, MongoDB). Phases 2–4 reinforce with phase-specific framings.
- AC-6.2 (bounded-context integrity): Phase 3 states language ownership + no bleed + ACL integration. Phase 4 enumerates the three integrity rules (language ownership, ACL, domain-term context maps) plus the "decomposing by microservice" anti-pattern with a worked Ordering / Fulfillment / Customer Communications example.

## Preservation
No existing content rewritten. All inserts are additive blockquotes placed immediately after each `## Phase N` heading.

## Verification
- `grep "Decomposition Hygiene"` → 4 hits (Phases 1, 2, 3, 4). OK.
- `grep "bounded context"` → existing hits intact + new Phase 3/4 hits. OK.
- Total new lines: ~38 (within 30–60 budget).

## Status
DONE.
