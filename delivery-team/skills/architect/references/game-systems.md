# Game Systems Architecture

Reference for core game system design patterns, decision criteria, and implementation guidance.

---

## Entity-Component-System (ECS)

ECS separates identity (entity = integer ID), data (component = plain struct), and behavior (system = function iterating over component sets). This separation enables cache-friendly memory layouts and parallelizable systems.

**When to use ECS vs alternatives:**

- **Pure ECS (Bevy, Flecs, Unity DOTS):** Best when you have thousands of similar entities (bullets, particles, NPCs) and need data-oriented performance. The upfront complexity pays off at scale.
- **Component-based (Unity MonoBehaviour, Godot Node):** Better for content-heavy games with fewer unique entities. Easier for designers to compose behaviors in the editor. Accept the overhead.
- **Inheritance hierarchies:** Almost never the right choice for game entities. Use only for truly hierarchical concepts (UI widget trees, menu systems). The "diamond of death" in game entity hierarchies is real and arrives faster than expected.

**Data-oriented design principles:**
- Store components in contiguous arrays (Structure of Arrays, not Array of Structures).
- Systems should iterate linearly over component arrays. Random access patterns destroy cache performance.
- Avoid pointers between components. Use entity IDs as indirect references and resolve them per-frame.
- Archetype storage (entities with the same component set stored together) gives the best query performance. Sparse sets give better add/remove component performance.

**Anti-patterns:**
- God components (a `GameData` component with 40 fields). Split into focused components.
- Systems that query single entities by ID repeatedly. This is OOP in disguise.
- Storing references to other entities as direct pointers. Entities can be destroyed; dangling references crash.

---

## Game Loop Architecture

**Fixed timestep (e.g., 60 updates/sec):**
- Physics, netcode, and gameplay logic get deterministic, reproducible results.
- Accumulator pattern: each frame, add `deltaTime` to an accumulator; consume it in fixed-size chunks.
- If the game falls behind, you simulate multiple fixed steps per frame (spiral of death risk -- cap max steps per frame).

**Variable timestep:**
- Rendering always runs at native framerate. Smooth visual output.
- Multiply all movement by `deltaTime`. Sounds simple, breaks subtly: floating-point drift, frame-rate-dependent physics, inconsistent collision at low FPS.
- Never use for physics or competitive gameplay.

**Semi-fixed (the standard):**
- Fixed update for gameplay/physics (e.g., 60Hz). Variable render with interpolation between the last two fixed states.
- Interpolation formula: `renderState = previousState * (1 - alpha) + currentState * alpha` where `alpha = accumulator / fixedTimestep`.
- This is what most shipped games use. Unity, Unreal, and Godot all support this pattern natively.

**Frame independence checklist:**
- All gameplay values expressed in units-per-second, not units-per-frame.
- Input buffering decoupled from frame rate.
- Animation playback uses time, not frame count.
- Timers use accumulated time, not frame counters.

---

## Combat System Patterns

**Turn-based:**
- Action queue: each turn, collect actions from all actors, sort by initiative/speed, execute in order.
- Turn order systems: round-robin (simple), initiative-based (D&D-style roll), speed-based cooldown (FFX -- each action has a recovery time, fastest actor goes next).
- Key design: separate action declaration from action resolution. This enables preview, undo, and AI evaluation.

**Real-time:**
- Hitbox/hurtbox separation: attack colliders (hitboxes) are distinct from vulnerability colliders (hurtboxes). Never use the same collider for both.
- Invincibility frames (i-frames): after taking damage, briefly disable the hurtbox. Track with a cooldown timer, not a frame counter.
- Hit detection: use overlap tests on fixed update, not continuous collision. Buffer hit events and process them in a damage resolution phase.

**Damage calculation pipeline:**
```
Raw damage (base + scaling)
  -> Apply attacker modifiers (buffs, critical multiplier, charge level)
  -> Apply defender modifiers (armor, resistances, vulnerability)
  -> Apply global modifiers (difficulty scaling, zone effects)
  -> Clamp to [0, max]
  -> Apply to health
  -> Trigger reactive effects (thorns, lifesteal, on-hit procs)
```

**Status effect architecture:**
- Effects as data: type, duration, tick rate, magnitude, stacking rule (refresh, stack count, stack duration, independent).
- Process effects in a dedicated system each tick. Do not scatter effect logic across combat code.
- Stack policies must be explicit: does applying Poison twice refresh duration, add a stack, or create an independent instance?
- Cleanse/immunity: tag effects by category (debuff, DoT, CC) so cleanse mechanics can target categories.

---

## Inventory and Item Systems

**Storage models:**
- Slot-based: fixed grid (Resident Evil), fixed slots (equipment slots), limited count. Simple UI, forces player choices.
- Weight-based: unlimited slots, weight cap. More flexible but requires careful weight balancing.
- Hybrid: slot grid with weight limits (Escape from Tarkov). Most complex but most expressive.

**Item data architecture:**
- Items are data records, not objects with behavior. Store item definitions in a database (JSON, SQLite, ScriptableObjects, Godot Resources).
- Item instances reference a definition ID plus instance-specific data (durability, enchantments, stack count).
- Component items: attachments and modifiers are separate item records that reference a parent. A weapon is a base item + scope item + magazine item.

**Serialization for save/load:**
- Save item definition IDs, not full item data. Reconstruct from the database on load.
- Save only instance-specific mutations (durability, custom name, socket contents).
- Version your item database. When definitions change between patches, write migration logic.

**Anti-patterns:**
- Item as a class hierarchy (Weapon extends Item extends Object). Use composition.
- Storing full item data in save files. Bloated saves, impossible to patch item balance.
- Unique item IDs as sequential integers. Use GUIDs or content-addressable hashes.

---

## Progression Systems

**XP curves:**
- Linear: `xp_to_next = base + (level * increment)`. Predictable, can feel grindy at high levels.
- Polynomial: `xp_to_next = base * level^exponent`. Gentle early curve, steeper later. Exponent of 2-3 is typical.
- Exponential: `xp_to_next = base * multiplier^level`. Dramatic scaling. Requires exponential reward scaling to match, or players stall.
- Always define the curve as a formula or table, never hardcode per-level values.

**Skill trees:**
- DAG structure (directed acyclic graph). Nodes are skills/perks, edges are prerequisites.
- Validate prerequisite chains at unlock time. Also validate on load (patches may restructure the tree).
- Respec: store allocated points separately from unlocked nodes. Respec clears nodes, refunds points.
- Avoid deep linear chains. Players should face meaningful choices within 2-3 points of investment.

**Prestige/rebirth:**
- Reset primary progression, grant permanent bonuses (multipliers, unlocks, cosmetics).
- Track prestige count and total lifetime progress separately.
- Each prestige cycle should be noticeably faster than the last, or players disengage.

---

## Economy Design

**Currency flow:**
- Faucets (sources): quest rewards, enemy drops, crafting, trading.
- Sinks (drains): vendor purchases, repair costs, consumables, taxes, upgrade costs.
- If faucets > sinks over time, inflation occurs. Monitor average currency held per player over time.

**Dual currency:**
- Soft currency: earned through gameplay. Abundant, low value per unit.
- Hard currency: purchased with real money or earned sparingly. Used for convenience, cosmetics, or time-skipping.
- Never gate core progression behind hard currency unless the game is explicitly designed for it.

**Marketplace architecture (player trading):**
- Order book: buy orders and sell orders matched by price. Prevents price manipulation better than auction systems.
- Transaction tax: percentage removed from each trade. Primary inflation sink.
- Price history tracking: store rolling averages for economic monitoring and player-facing price charts.
- Bot detection: flag accounts with inhuman trading patterns (perfect timing, impossible volumes).

---

## Game State Management

**State machine selection:**
- Simple FSM: flat set of states with transitions. Good for entity states under ~8 states (idle, walk, run, jump, fall, attack, hurt, dead).
- Hierarchical state machine (HFSM): states contain sub-states. "Combat" state contains "melee" and "ranged" sub-states. Reduces transition explosion.
- State stack: push/pop states. Perfect for pause menus, dialog overlays, inventory screens layered over gameplay.
- Blackboard: shared key-value store. Best for AI where multiple systems need to read/write shared context.

**State separation:**
- Scene/level state: which level is loaded, level completion flags, environmental state.
- Entity state: per-entity FSM, health, position, inventory.
- UI state: which menus are open, scroll positions, selected items.
- Keep these in separate systems. Never store UI state on game entities.

---

## Save/Load Architecture

**Serialization format selection:**
- JSON: human-readable, easy to debug, large file sizes. Good for development and mod-friendly games.
- Binary: compact, fast, not human-readable. Good for production saves with large state.
- Protobuf/FlatBuffers: schema-defined, versioned, cross-platform. Best for games with frequent updates and cloud saves.

**Versioning and migration:**
- Every save file includes a version number. On load, check version and run migration functions sequentially (v1->v2, v2->v3, etc.).
- Never delete fields from the save schema. Mark them deprecated and ignore on load.
- Test save compatibility as part of CI. Keep sample saves from each version.

**What to save vs reconstruct:**
- Save: player state, inventory, quest progress, world mutations (destroyed objects, opened doors), settings.
- Reconstruct: level geometry, enemy base stats, item definitions, UI layout, audio state.
- Rule of thumb: save the delta from the default state, not the full state.

**Autosave:** trigger on meaningful state changes (entering a new area, completing a quest), not on a timer. Timer-based autosaves can capture undesirable states (mid-fall, mid-combat).

---

## Event/Message Bus

- Typed events: define event types as structs/classes. Listeners subscribe to specific types. Avoids string-based event names.
- Event pooling: reuse event objects to avoid GC pressure. Reset fields instead of allocating.
- Priority ordering: listeners declare priority. Higher priority listeners can consume events to prevent further propagation.
- Deferred dispatch: queue events during system iteration, dispatch after the current system completes. Prevents mutation during iteration.
- Scope events: global bus for cross-system communication, local buses for entity-internal communication. Do not route everything through a single global bus.

---

## AI Architecture

**Behavior trees:**
- Selector (OR): try children left-to-right, succeed on first success. Use for "try attack, else try flee, else idle."
- Sequence (AND): run children left-to-right, fail on first failure. Use for "check ammo AND aim AND fire."
- Decorators: invert result, repeat, cooldown timer, conditional gate.
- Leaf nodes: actions (move, attack, play animation) and conditions (is target visible, is health low).
- Tick behavior trees on a lower frequency than the game loop (e.g., 10Hz) to save CPU.

**Utility AI:**
- Score each available action by evaluating response curves (linear, quadratic, logistic) against relevant inputs (health, distance, ammo, threat level).
- Select the highest-scoring action, or use weighted random selection among top candidates for variety.
- Best for NPCs that need to appear to "think" and weigh trade-offs (The Sims, strategy game units).

**GOAP (Goal-Oriented Action Planning):**
- Define world state as a set of boolean/numeric properties. Define actions with preconditions and effects.
- Planner searches backwards from goal state to find a sequence of actions. A* on the action graph.
- Expensive to plan every frame. Cache plans and replan only when the world state invalidates the current plan.
- Best for complex NPCs with many interacting systems (F.E.A.R., Shadow of Mordor).

**Steering behaviors:**
- Seek/flee: accelerate toward/away from target.
- Arrive: seek with deceleration radius. Prevents oscillation around the target.
- Flocking: separation + alignment + cohesion. Weight each component. Add obstacle avoidance.
- Combine steering outputs as weighted vectors. Clamp the result to max acceleration.
- Layer steering on top of pathfinding: pathfinding gives waypoints, steering handles smooth movement between them.
