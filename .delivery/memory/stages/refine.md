# Refine Stage — Memory

## Lessons Learned

- PRD citation discipline is the load-bearing property of any migration PRD. Every Anthropic-docs claim should cite a live URL; adversarial reviewer must independently re-fetch every load-bearing URL. 29-citation PRD with 0 fabricated quotes held under Challenger spot-check of 8. (validated: 1, last: run-2026-04-20-o4v7)

- Developer DoD catches command-validity bugs that no reasoning-only validator finds. On a PRD that names executable commands (grep patterns, paths, config keys), Gimli found 3 real bugs (regex missed a match, wrong alias path, `parallel_validators` treated as count when actually boolean). PO/Architect/QA all ACCEPTed — they reasoned, didn't run. Developer DoD is non-optional on plans-with-commands. (validated: 1, last: run-2026-04-20-o4v7)

- Two-loop Evaluator-Optimizer is worth the cost on multi-requirement PRDs. Loop 1: QA REVISE (11 defects). PO rev 1. Loop 2: QA ACCEPT, 0 regressions. Single-loop would have shipped with the 11 defects. (validated: 1, last: run-2026-04-20-o4v7)

- Two-loop Adversarial converges with measurable signal. confidence 3 → rev 1 → confidence 4. The rev added a 2-hostname gate to WebFetch AC that single-loop would have missed. For PRDs with ≥10 findings, the second loop usually lifts confidence by hardening an AC loop-1 surfaced but didn't close. (validated: 1, last: run-2026-04-20-o4v7)
