# Defect Patterns

**Entries**: 2 | **Last updated**: 2026-04-03

- **Agent validation gap (LLM inference vs deterministic check)**: When correctness is binary (legal/illegal, valid/invalid), agent prompts must mandate programmatic API validation — not LLM knowledge. LLM card knowledge is unreliable for exhaustive checks across large datasets (100+ items). Root cause: agent guide did not mandate batch API validation. (severity: Critical, validated: 1, last: run-2026-04-02-k3r9)
- **Single-source data gap**: When a capability is scoped to one data source (pricing, availability, etc.), the output must disclose the limitation to the user. PRD team knowing about a scope limit is not sufficient — the user must know. Price divergence between sources can exceed 50%. (severity: Major, validated: 1, last: run-2026-04-02-k3r9)
