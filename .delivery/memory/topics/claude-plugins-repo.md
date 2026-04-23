# Claude-Plugins Repo — Project-Specific Memory

## Keystone Files (migrations start here)

- **`prompt-engineer/SKILL.md` (~440 LOC)** is the prompt-pattern keystone. Drift here propagates to every downstream skill author who reads it as a reference. Future prompt-pattern migrations should start here and let the citation graph pull the rest. (validated: 1, last: run-2026-04-20-o4v7)

- **`delivery-team/skills/delivery-flow/SKILL.md` (~1100 LOC)** is the sub-agent dispatch keystone. The DISP-01 section (lines 328-345 as of rev run-2026-04-20) defines the dispatch contract. Any model-migration touching sub-agent defaults (e.g., Opus 4.7's "fewer subagents by default") must update this first and baseline downstream dispatch annotations against it. (validated: 1, last: run-2026-04-20-o4v7)

- **`delivery-team/skills/product-delivery/SKILL.md` (~685 LOC)** is the third keystone — flagship PO/SM/Analyst skill with heavy role-prompt content. (validated: 1, last: run-2026-04-20-o4v7)

## Repo Surface Facts

- **Zero `import anthropic` / `from anthropic` anywhere in the repo.** Migration plans that assume an SDK-wiring edit path are out of scope; every model-ID reference is a direct string in prose markdown. (validated: 1, last: run-2026-04-20-o4v7)

- **Model-ID references are rare in skill-authored content.** As of run-2026-04-20: 3 total model-ID hits in 1 file. Plugin migration is primarily prose/prompt work, not config work. (validated: 1, last: run-2026-04-20-o4v7)

- **Alias theme YAMLs** live at `delivery-team/skills/delivery-flow/references/aliases/` (13 files). Tone-strengthening on a regressing theme is bounded by the theme file scope. Dogfooding a theme is inherently qualitative — budget human judgement time. (validated: 1, last: run-2026-04-20-o4v7)

## Config Facts

- **`.delivery/config.yml` `parallel_validators: true` is a boolean, not a count.** Easy to mis-read. The expected validator count comes from `dod_validators.<stage>` list length. Future config readers should assume any type-shaped assumption is wrong until grep-verified. (validated: 1, last: run-2026-04-20-o4v7)

- **`.delivery/config.yml` `pipeline.checkpoints: []`** (PO override "march to war"). Stages do not pause for human checkpoints; advance automatically after DoD passes. (validated: 1, last: run-2026-04-20-o4v7)

## Convention Hooks

- **CLAUDE.md's plugin-dev skill routing is load-bearing.** Any run that edits skills/hooks/plugin-structure MUST load the corresponding `plugin-dev:*` skill first (hook-development, skill-development, plugin-structure, skill-reviewer, plugin-validator). (validated: 1, last: run-2026-04-20-o4v7)
