# S2 DoD round 2, QA validator

Tree: commits 31ae759, 1e36eb2, 1304e2a on worktree-backlog-108-o48m. Verdict: DONE.

## Raw outputs
- wc -l: delivery-flow 499 (<=500), product-delivery 300 (<=300), prompt-engineer 520 (<=520).
- check_skill_budgets.py: `BUDGET CHECK PASSED: 17 file(s) checked, 0 known-debt, 0 exception(s).`
- AC-2.1: `0 source lines still present` (no PRESENT lines listed).
- AC-2.2: `MODEL_ID = os.environ` 1; claude-id regex 0; `canonical <YYYY` 0; `Versioned Model Reference` 0.
- AC-2.3: `0`.
- AC-2.5: cond True, cap True, `OK`. Cap line (delivery-flow 275): "`dod_validators.<stage>` is the cap: at most that many subagents per DoD checkpoint, on any model;" and a "When the orchestrating session runs the latest Opus," line. The literal word `subagents` is used deliberately (the regex accepts sub-?agent), and line 274-ish prose elsewhere uses "sub-agents"; this is the accepted exception.
- AC-2.6: `^model: sonnet` count 1.
- check_model_pins.py --paths (4 files incl. orchestrator-doctrine): hits 8 files 3, exit=1, all stamps:
  delivery-flow SKILL.md:5, :9; product-delivery SKILL.md:5, :7; prompt-engineer SKILL.md:6, :8, :415, :417.
  These are all `stamp` class (S3 owns them); no prose or pin hits. orchestrator-doctrine.md has zero hits.
- prompt-engineer line 361: "**Delegation and verification on the latest Opus:** it delegates to subagents more readily than prior models, so state the delegation scope and a spawn cap in the prompt. Explicit verification instructions cause over-verification, so do not add them. Pick an `effort` level and leave sampling alone." Delegation-scope, spawn-cap and over-verification anchors all present, no version number, no per-version effort level.

## Notes
- AC-2.3b (adversarial artifact, intent verdict) is not this validator's scope; not evaluated here.
- The pins exit=1 is expected until S3 stamps are made version-free; not an S2 defect.

## Verdict
DONE. No blocking findings.
