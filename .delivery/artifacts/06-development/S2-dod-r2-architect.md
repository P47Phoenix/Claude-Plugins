# S2 DoD round 2: Architect validator (fresh)

Scope: `git diff 18b8e30..HEAD` for prompt-engineer/SKILL.md, delivery-flow/SKILL.md, orchestrator-doctrine.md. Fetched 2026-09-20.

## Verdict: DONE

## Checks (live doc quotes)

1. prompt-engineer ~351 adaptive shape + output_config.effort: PASS.
   - thinking-steering-and-cost: "Effort is set at `output_config.effort`, not inside the `thinking` object"; examples use `thinking={"type": "adaptive"}`.
   - Opus 5 migration guide: "`thinking: {type: "enabled", budget_tokens: N}` is no longer supported on Claude Opus 4.7 or later models and returns a 400 error."
   - Effort page: valid levels low/medium/high/xhigh/max; "Not every model that supports `max` supports `xhigh`." (matches ~355 wording); API default `high`; "If you carried effort settings over from an earlier model, run a fresh effort sweep" (matches "do not copy per-model level").
2. ~359 sampling 400 on 4.7+: PASS. Migration guide: "Setting `temperature`, `top_p`, or `top_k` to any non-default value on Claude Opus 4.7 or later models, including Claude Opus 5, returns a 400 error."
3. ~361 delegation and over-verification: PASS.
   - Opus 5 prompting: "Claude Opus 5 delegates to subagents more readily than prior models"; advice to give explicit scope or "set deterministic caps".
   - "instructions like these cause over-verification on Claude Opus 5" (explicit verification instructions, remove them).
4. delivery-flow cap wording: PASS, not contradicted. "`dod_validators.<stage>` is the cap ... on any model" is model-independent; docs say cap delegation for cost. Orchestrator-doctrine text ("delegates more readily", fusion and over-spawning) is consistent, and the old wrong "dispatches fewer" claim (PRD FR-2.1, refuted) is gone. Frontmatter `model: sonnet` untouched; the phrasing is conditional ("When the orchestrating session runs the latest Opus"), per FR-2.6.
5. Version-free prose (FR-2.1/2.3): PASS. No "Opus 4.7", "F-08" or per-version effort level in the three files. Pattern 4.1 is a config read (FR-2.2). Heading is "latest Opus" (FR-2.3). Line 88 rewritten.

## Non-blocking notes for S3 (not S2 defects)
- Residual "4.7" strings: prompt-engineer lines 351 and 359 ("Claude 4.7 and later") are doc-accurate API thresholds, but AC-3.1b (zero version markers in every SKILL.md) may match them via BARE_RE. Consider rewording, for example "on current models" or "since the 4.7 generation" allowlisted, when S3 runs the guard.
- Stamp lines (`model_awareness: opus-4-7`, `pattern_library_version: 4-7-1`, lines 6/8/415/417 and delivery-flow 5/9) are still present: S3 FR-3.2 scope. Line ~410 describes the `latest` stamp already.
