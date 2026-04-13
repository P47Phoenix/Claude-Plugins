# Project Type Patterns

**Entries**: 1 | **Last updated**: 2026-04-03

## GREENFIELD

- GREENFIELD pipelines benefit from all 7 stages at full depth. No stage felt unnecessary. Idea established scope, Refine tightened ACs, Design mapped FRs, Architect resolved open questions, Plan caught sizing issues, Dev delivered clean, UAT found real defects. (validated: 2, last: run-2026-04-12-hw01)
- Cross-plugin skill invocation should be verified at Refine (not deferred to Architect) when the entire architecture depends on it. hw01 adversarial challenger caught this at confidence 2/5. A 15-minute live test resolved it and prevented PRD rewrite. (validated: 1, last: run-2026-04-12-hw01)
- Plugin GREENFIELD projects produce primarily markdown + Python scripts. Calibrate estimates accordingly — markdown-heavy work is one tier lower than code. Sprint capacity planning confirmed this in hw01 (85% markdown, 15% Python). (validated: 1, last: run-2026-04-12-hw01)
