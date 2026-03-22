# Godot Defect Prevention Checklist

Pre-completion checklist derived from real defect data (12 defects across 14 stories = 0.86 defects/story). Apply before marking any Godot story as "done."

## Control Node Input Blocking (17% of defects)

Before completing any story that creates or modifies Control-derived nodes (ColorRect, Label, Panel, Button) near an Area2D:

- [ ] Every visual-only Control node has `mouse_filter = 2` (MOUSE_FILTER_IGNORE)
- [ ] In .tscn files, check all ColorRect/Label/Panel nodes for explicit `mouse_filter` property
- [ ] Movement overlays, attack range overlays, health bars, selection indicators — ALL need MOUSE_FILTER_IGNORE

**Detection command:**
```bash
grep -rn "type=\"ColorRect\"\|type=\"Label\"\|type=\"Panel\"" src/scenes/ | while read line; do
  file=$(echo "$line" | cut -d: -f1)
  if ! grep -A5 "$(echo "$line" | grep -o 'name="[^"]*"')" "$file" | grep -q "mouse_filter"; then
    echo "MISSING mouse_filter: $line"
  fi
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

## @onready Lifecycle (8% of defects)

- [ ] No method that accesses @onready vars is called before add_child()
- [ ] Factory/spawner pattern: instantiate -> add_child -> configure (not instantiate -> configure -> add_child)
- [ ] If a method MUST be called pre-tree, it must not access any @onready var or $NodePath

## Scene Instancing (8% of defects)

- [ ] All .tscn parent= paths are relative (never include root node name)
- [ ] Test: instance the scene into a different parent — do paths still resolve?

## Engine API Calls (8% of defects)

- [ ] Camera2D: make_current() or current=true in _ready()
- [ ] CanvasLayer: layer property set to avoid z-order conflicts
- [ ] TileMapLayer: TileSet assigned with create_tile() called for each atlas position

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

## Defect Metrics

Track defect rate per sprint to measure improvement:

| Sprint | Stories | Defects | Rate |
|--------|---------|---------|------|
| 1-4 (baseline) | 14 | 12 | 0.86 |
| Target | - | - | <0.3 |
