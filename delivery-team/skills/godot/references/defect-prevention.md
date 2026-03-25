# Godot Defect Prevention Checklist

Pre-completion checklist derived from real defect data (12 defects across 14 stories = 0.86 defects/story). Apply before marking any Godot story as "done."

For @onready lifecycle, scene instancing, and engine API patterns, see `validation.md` (bug patterns #1-#5 and pre-write checklist). This file covers the additional defect categories not covered there.

## Control Node Input Blocking (17% of defects)

Before completing any story that creates or modifies Control-derived nodes (ColorRect, Label, Panel) near an Area2D:

- [ ] Every visual-only Control node has `mouse_filter = 2` (MOUSE_FILTER_IGNORE)
- [ ] In .tscn files, check all ColorRect/Label/Panel nodes for explicit `mouse_filter` property
- [ ] Movement overlays, attack range overlays, health bars, selection indicators — ALL need MOUSE_FILTER_IGNORE
- [ ] Interactive Controls (Button, TextEdit, LineEdit) should NOT have MOUSE_FILTER_IGNORE — they need input

**Detection command:**
```bash
# Find .tscn files with Control-derived nodes missing mouse_filter
# Excludes interactive controls (Button, TextEdit, LineEdit) that need input
find . -name "*.tscn" -exec grep -ln "type=\"ColorRect\"\|type=\"Label\"\|type=\"Panel\"" {} \; | while read file; do
  grep -n "type=\"ColorRect\"\|type=\"Label\"\|type=\"Panel\"" "$file" | while read line; do
    node_name=$(echo "$line" | grep -o 'name="[^"]*"')
    if ! grep -A10 "$node_name" "$file" | grep -q "mouse_filter"; then
      echo "MISSING mouse_filter: $file: $line"
    fi
  done
done
```

## Integration Wiring (17% of defects)

Before completing stories that reference other stories' functionality:

- [ ] If Story A creates a UI panel and Story B creates the trigger, verify the signal chain is wired end-to-end
- [ ] List all EventBus signals the story emits AND connects — verify both ends exist
- [ ] If a signal is emitted in one story and consumed in another, both stories must be tested together
- [ ] Signal ownership must be clear: each signal should have ONE emitter (documented in EventBus comments)

**Pattern to enforce:**
```gdscript
## EventBus signal ownership comments
## combat_started: Emitted by CombatPanel on attack confirm. Listened by CombatManager.
## unit_selected: Emitted by Unit.select(). Listened by MovementController, AttackRange.
```

## Input Handler Priority (8% of defects)

- [ ] If multiple nodes use _unhandled_input for the same event (left-click), define priority order
- [ ] Movement handler should skip tiles occupied by enemy units
- [ ] Attack handler should take priority over movement for occupied tiles
- [ ] Use get_viewport().set_input_as_handled() to prevent event propagation

## Node Lifecycle Safety (8% of defects)

- [ ] Before queue_free(), store any data you'll need after (tile_pos, stats, player_id)
- [ ] Don't pass node references in signals if the node might be freed before listeners process
- [ ] Use is_instance_valid() before accessing nodes that might have been freed

## Convention Enforcement (8% of defects)

- [ ] All cross-system communication uses EventBus signals (no get_node("../Sibling"))
- [ ] No direct method calls between systems (combat <-> movement <-> UI)
- [ ] Check CLAUDE.md conventions are followed

## Type Safety

- [ ] Never use `:=` type inference in production code -- always explicitly type variables: `var x: int = 5` not `var x := 5`
- [ ] Enable strict type warnings in Project Settings > Debug > GDScript:
  - UNSAFE_METHOD_ACCESS = Error
  - UNSAFE_PROPERTY_ACCESS = Error
  - UNSAFE_CAST = Error
- [ ] When renaming a method or property, search ALL .gd files for the old name before committing

**Detection command:**
```bash
# Find all := usage (should be zero in production code)
grep -rn ":=" --include="*.gd" src/ | grep -v "test"
```

## Array/Enum Consistency

- [ ] Every array indexed by an enum must have exactly as many elements as the enum has values
- [ ] Use `enum.size()` or `EnumName.values().size()` to validate array length at runtime
- [ ] When adding a value to an enum, search for all arrays indexed by that enum and add corresponding entries

**Detection command:**
```bash
# Find all enum declarations and their value counts
grep -rn "^enum " --include="*.gd" src/
```

## Defect Metrics

Track defect rate per sprint to measure improvement. Record defects in `.delivery/defects/` with sprint, story ID, category, and root cause.

| Sprint | Stories | Defects | Rate | Notes |
|--------|---------|---------|------|-------|
| 1-4 (baseline) | 14 | 12 | 0.86 | Initial audit |
| Target | - | - | <0.3 | After checklist adoption |

To record a defect, add an entry to `.delivery/defects/sprint-N.md`:
```markdown
### DEF-NNN: [Short description]
- **Severity**: CRITICAL / HIGH / MEDIUM / LOW
- **Category**: [From checklist categories above]
- **Story**: Sprint N, Story "[title]"
- **Root cause**: [Why this happened]
- **Detected by**: Code inspection / Headless validation / Manual playtest
- **Prevention**: [How to prevent in future]
- **Plugin PR**: none / PR #N to Claude-Plugins (if pattern is systemic)
```
