---
loaded_by: arranger
level: L2
last_reviewed: 2026-10-26
---

# Cross-Role Task Patterns

The arranger has one dispatched role (`instrumentation`) with three task types. Requests often span
more than one. One task type = one Agent call; chain them, never merge two `ROLE:` lines in one prompt.

## Patterns

| Request | Chain | Hand-over |
|---------|-------|-----------|
| "Arrange this song" (full Stage 6) | `instrumentation` -> `dynamics` -> `production-brief` | Draft `arrangement.md`, then the same file edited in place, then `production-brief.md` |
| "Pick the instruments" only | `instrumentation` | Draft with provisional energy values; flag that `dynamics` has not run |
| "Make the chorus hit harder" | `dynamics` | Edit `energy` and `texture_note` in place; prior instrument columns stay |
| "Write mix notes for the arrangement" | `production-brief` | Reads the finished `arrangement.md` read-only |
| "Export MIDI" | none (script) | `midi_export.py` on `chords.md` and `melody.abc`; no sub-agent |
| REVISE touching arrangement | `dynamics` (energy) or `instrumentation` (table shape), then `production-brief` if sections changed | Only the named rows change |

## Hand-over rules

1. Each task writes or edits exactly one artifact. `dynamics` is the only task allowed to edit the file
   another task created.
2. The next task reads the previous artifact by path. Do not paste artifact text into the prompt.
3. Gates run once, after the last task of the chain: `arrangement_check.py` and
   `structure_check.py --consistency`.
4. A gate violation is routed back to the owner of the failing column: energy values to `dynamics`,
   instrument cells and row shape to `instrumentation`, lint hits in the brief to `production-brief`.

## Conflicts

| Conflict | Resolution |
|----------|------------|
| Energy curve fights the genre arc | The gate wins; adjust `energy`, then explain the departure in `texture_note` |
| `structure.md` header disagrees with the arrangement header | Fix the arrangement header; the arranger never edits `structure.md` |
| Brief mentions an instrument absent from the table | The table wins; correct the brief |
| User asks for a named-artist sound | Originality policy clause 2 and 3: decline the reference, offer the technical description (tempo, instruments, texture) instead |

## Dependencies on other skills

- Upstream: `music-brief` (genre, mood, length), `composer` (`chords.md`, `melody.abc`), the groove role
  (`structure.md`).
- Downstream: `song-critic` (`structure-judge` rubric), `music-release` (package, `midi_export.py`).
