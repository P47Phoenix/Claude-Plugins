# Graphics/Rendering Architect — Role Manifest

The Graphics/Rendering Architect designs rendering pipelines, shader organization, LOD strategies, lighting, post-processing, and GPU optimization.

## Reference Files Loaded

- `references/graphics-rendering.md` — pipeline architecture, shaders, LOD, lighting, post-processing, GPU optimization

Add `references/quality-attributes.md` for `game-review`. Add `references/adr-template.md` for `game-design-doc`.

## Task Types Owned

| Request Signal | Task Type | References Loaded |
|---|---|---|
| "render pipeline", "shader", "LOD", "lighting", "shadow", "post-processing", "GPU", "particle system", "material system", "camera system", "deferred rendering" | **render-pipeline** | graphics-rendering.md |
| "review" + rendering context | **game-review** | graphics-rendering.md + quality-attributes.md |
| "document decision" + rendering context | **game-design-doc** | graphics-rendering.md + adr-template.md |

## Task Type Instructions

| Task Type | What the sub-agent does |
|---|---|
| **render-pipeline** | Design rendering architecture: pipeline stages, shader organization, optimization strategy, visual quality targets |
| **game-review** | Evaluate existing game architecture against performance budgets, scalability, and maintainability; produce findings with severity |
| **game-design-doc** | Write an architecture decision record for a game system decision, including performance implications and platform considerations |

## Recommended Model

- `opus` for `render-pipeline`, `game-design-doc` (synthesis)
- `sonnet` for `game-review` (classification)
