# Clean Code Review Checklist

Condensed pass/fail criteria for code review. Severity: **BLOCK** = merge blocker, **WARN** = should fix, non-blocking.

## Meaningful Names
- [ ] [BLOCK] Every variable, function, and class name reveals intent without needing a comment
- [ ] [BLOCK] No single-letter names outside loop counters or lambda parameters
- [ ] [WARN] No misleading abbreviations or encodings (e.g., Hungarian notation)

## Functions
- [ ] [BLOCK] Each function does exactly one thing (single level of abstraction)
- [ ] [BLOCK] No function exceeds 30 lines (excluding signature and closing)
- [ ] [WARN] No more than 3 parameters; 4+ requires justification or refactor
- [ ] [WARN] No flag (boolean) parameters that split function behavior

## Comments
- [ ] [BLOCK] No commented-out code checked in
- [ ] [WARN] No comments that restate what the code does; comments explain *why*
- [ ] [WARN] All TODOs include a tracking reference or owner

## Formatting
- [ ] [BLOCK] File follows project formatting rules (indentation, line length, spacing)
- [ ] [WARN] Related code is grouped; unrelated code is separated by blank lines
- [ ] [WARN] Vertical ordering: caller above callee, public above private

## Error Handling
- [ ] [BLOCK] No swallowed exceptions (empty catch/except blocks)
- [ ] [BLOCK] No returning null where an error or empty collection is appropriate
- [ ] [WARN] Error messages include context (what failed, why, what to do)

## Boundaries
- [ ] [BLOCK] External dependencies are wrapped behind an interface or adapter
- [ ] [WARN] No direct use of third-party types in core domain signatures

## Unit Tests
- [ ] [BLOCK] Each test tests exactly one behavior (single assertion concept)
- [ ] [BLOCK] Tests have no interdependencies or shared mutable state
- [ ] [WARN] Test names describe the scenario and expected outcome
- [ ] [WARN] No production logic in test code (no conditional assertions)

## Classes
- [ ] [BLOCK] Each class has a single reason to change (high cohesion)
- [ ] [WARN] Class exposes no internal state unnecessarily (minimal public surface)
- [ ] [WARN] Inheritance depth does not exceed 3 levels; prefer composition

## Emergent Design
- [ ] [WARN] No premature abstractions (abstraction justified by 2+ concrete uses)
- [ ] [WARN] No duplication across the changeset (DRY within the PR scope)
- [ ] [WARN] Simplest solution chosen; no speculative generality

## Code Smells
- [ ] [BLOCK] No dead code (unreachable branches, unused imports, unused variables)
- [ ] [BLOCK] No magic numbers or strings; use named constants
- [ ] [WARN] No feature envy (method uses another class's data more than its own)
- [ ] [WARN] No data clumps (3+ fields always passed together without a grouping type)
