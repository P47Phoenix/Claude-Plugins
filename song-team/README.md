# song-team

> **Status: scaffold (Wave 0).** The plugin is registered in the marketplace; skills land wave by wave. Design source of truth until Wave 5: `docs/plans/song-team-plan.md`.

A song-creation agent plugin: one orchestrator (`song-flow`) drives a 7-stage pipeline (Brief, Concept, Structure, Lyrics, Music, Arrangement, Release) through role-scoped worker skills (`lyricist`, `composer`, `arranger`), a rubric-driven critic with listener personas and an adversarial challenger (`song-critic`), and deterministic gate scripts under `scripts/`.

## Originality policy (summary)

The pipeline never reproduces or closely imitates an identifiable existing song or artist. Genre and era are fine as targets; named artists and song titles are not. Parody and "in the style of <artist>" requests are refused with an offer to write an original on the same theme. The resemblance-corpus check is opt-in; the challenger role is the default originality control. See `references/shared/originality-policy.md`.
