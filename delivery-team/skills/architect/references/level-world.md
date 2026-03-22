# Level and World Architecture

Reference for world structure, spatial systems, procedural generation, and environment design patterns.

---

## World Structure Patterns

**Open world (seamless streaming):**
- The entire world exists as one continuous space. No loading screens between areas.
- Requires streaming architecture, aggressive LOD, and strict memory budgets.
- Best for: exploration-driven games, sandbox games, large-scale RPGs.
- Risk: empty world syndrome. Open worlds need dense, hand-placed or procedurally meaningful content.

**Hub-and-spoke:**
- Central hub area connects to discrete levels/zones via portals, doors, or travel systems.
- Each spoke can be independently loaded, designed, and tested. Hub provides narrative cohesion.
- Best for: action games with mission structure, Souls-like interconnected worlds, platformers.
- Allows varied visual themes per spoke without streaming complexity.

**Linear:**
- Levels played in fixed sequence. Each level loads completely, replacing the previous.
- Simplest memory model. Entire level fits in memory. Full art/design control over pacing.
- Best for: narrative-driven games, FPS campaigns, puzzle games.

**Metroidvania (interconnected with gating):**
- One large interconnected map. Areas gated by abilities or items acquired elsewhere.
- Requires a global map state tracking which gates are open. Backtracking is a core mechanic.
- Map connectivity is the design artifact: design the gate/key graph first, then build the world geometry.
- Best for: 2D exploration games, ability-progression platformers.

**Decision criteria:** Choose based on content density budget, team size, and whether traversal itself is gameplay. Open worlds need 10-100x more content than linear games for comparable density.

---

## Spatial Partitioning

**Quadtree (2D) / Octree (3D):**
- Recursive subdivision of space into 4 (quad) or 8 (oct) children. Nodes split when entity count exceeds a threshold.
- Query: traverse from root, prune branches outside the query region. O(log n) for point and range queries.
- Best for non-uniform entity distributions. Adapts depth to density.
- Rebuild cost matters: for static geometry, build once. For dynamic entities, rebuild per frame or use loose trees (expanded node bounds to reduce re-insertions).

**BSP trees:**
- Binary space partition using arbitrary splitting planes. Classic for indoor environments and visibility determination.
- Compile-time structure. Not suitable for dynamic content.
- Used in Doom, Quake-era engines for rendering order and collision.

**Uniform grid:**
- Divide space into fixed-size cells. Entities stored in the cell they occupy.
- O(1) insertion and lookup by position. Range queries check neighboring cells.
- Best for uniformly distributed entities. Wastes memory in sparse areas, bottlenecks in dense areas.
- Cell size should match typical query radius. Too small = many cells checked. Too large = too many entities per cell.

**Spatial hashing:**
- Hash entity position to a flat array of buckets. Equivalent to a uniform grid without allocating empty cells.
- Memory-efficient for sparse worlds. Same query characteristics as uniform grid.
- Hash function: `hash(x, y) = (x * 73856093 ^ y * 19349663) % tableSize`. Use prime multipliers to reduce collisions.

**Selection criteria:** uniform grid or spatial hash for physics broad-phase (uniform entity distribution). Quadtree/octree for frustum culling and interest management (clustered distribution). BSP only for static indoor geometry.

---

## Level Streaming and Loading Zones

**Chunk-based streaming:**
- World divided into fixed-size chunks. Load chunks within a radius of the player. Unload chunks beyond a larger radius (hysteresis prevents thrashing at boundaries).
- Load radius > unload radius. The gap is the hysteresis zone.
- Chunks have three states: unloaded, loading (async), loaded. Never access a loading chunk's data.

**Portal-based transitions:**
- Trigger volumes at zone boundaries initiate loads. Hide loading behind corridors, elevators, narrow passages.
- "L-shaped" corridors are the classic trick: player cannot see both zones simultaneously.
- Pre-load the destination zone when the player enters the trigger area, not when they reach the door.

**Seamless world streaming:**
- No explicit zones. Stream assets based on camera position and movement direction.
- Predictive loading: analyze player velocity to prioritize loading in the direction of travel.
- Asset priority tiers: terrain and collision first, then major structures, then props and decorations.

**Memory budgeting:**
- Define a hard memory ceiling per platform. Divide among: always-loaded (UI, player, core systems), streaming budget (level content), transient (particles, audio, temp buffers).
- Profile actual memory per chunk during development. Flag chunks that exceed budget.
- Streaming pool: pre-allocate a fixed memory pool for streaming. When full, unload lowest-priority content before loading new content.

**Background loading:**
- All asset loading must be asynchronous. Synchronous loads cause frame hitches.
- Loading thread reads from disk and decompresses. Main thread integrates loaded assets (GPU upload, scene graph insertion) during a fixed time slice per frame (e.g., 2ms budget).

---

## Procedural Generation Patterns

**Wave Function Collapse (WFC):**
- Tile-based constraint solver. Each cell starts in superposition (all tiles possible). Collapse the cell with lowest entropy (fewest possibilities), then propagate constraints to neighbors.
- Constraint definition: adjacency rules (which tiles can neighbor which, per edge/face).
- Deterministic given a seed. Fast for 2D grids. 3D WFC is feasible but expensive.
- Best for: dungeon rooms, city blocks, tiled interior layouts.
- Trap: over-constrained inputs produce generation failures. Under-constrained inputs produce noise. Curate the tile set carefully.

**Cellular automata:**
- Initialize grid randomly. Apply rules iteratively (e.g., cell becomes wall if 5+ of 8 neighbors are walls).
- Classic 4-5 rule: birth if 5+ neighbors, survive if 4+ neighbors. Produces organic cave shapes in 4-6 iterations.
- Post-process: flood fill to find connected regions. Keep the largest, fill the rest. Ensures traversability.
- Best for: caves, organic terrain, natural-looking formations.

**L-systems:**
- String rewriting rules applied iteratively. Interpret the resulting string as drawing commands (forward, rotate, push/pop state).
- Best for: vegetation, tree branching, coral, river networks, road networks.
- Stochastic L-systems: multiple rules per symbol with probability weights. Creates natural variation.

**Noise-based terrain:**
- Perlin/Simplex noise: smooth, coherent random values. Use as heightmap base.
- Fractal Brownian Motion (fBM): layer multiple noise octaves at different frequencies and amplitudes. More octaves = more detail.
- Domain warping: feed noise output back as input coordinates. Creates swirling, organic terrain features.
- Biome assignment: use separate noise layers for temperature and moisture. Map (temp, moisture) pairs to biome types. Apply biome-specific terrain modifiers.

**Seed management:**
- Store world seed, not generated content. Regenerate deterministically from seed on load.
- Use separate RNG streams per system (terrain, enemies, loot) derived from the world seed. Changing one system does not cascade changes to others.
- For testing: log seeds that produce interesting results. Build a seed library for QA.

**Hybrid approaches:**
- Hand-craft key areas (boss rooms, story locations). Procedurally generate connecting areas.
- Use procedural generation for layout, then apply hand-authored decoration rules.
- Pre-generate and curate: generate many instances, select the best, ship as "hand-crafted" content.

---

## Navigation Mesh Architecture

**NavMesh generation:**
- Bake-time: voxelize world geometry, build heightfield, identify walkable surfaces, simplify into convex polygons. Standard in Unity, Unreal, Godot.
- Runtime generation: needed for procedural or destructible worlds. Use a tiled NavMesh approach -- only rebake affected tiles.

**Dynamic obstacles:**
- NavMesh cutting: carve holes in the NavMesh at obstacle positions. Expensive if obstacles move frequently.
- Alternative: use local avoidance (RVO / ORCA) to steer around dynamic obstacles without modifying the NavMesh.
- Reserve NavMesh cutting for semi-static obstacles (placed barricades, opened doors). Use avoidance for moving entities.

**Pathfinding layers:**
- Separate NavMeshes for different movement types: ground, flying (3D volume or high-altitude NavMesh), swimming (water volume).
- Agents query the NavMesh matching their movement type. Multi-mode agents switch NavMeshes on transition.

**Hierarchical pathfinding:**
- Partition NavMesh into regions. Build a high-level graph of region connectivity.
- First: A* on the region graph (fast, coarse path). Then: detailed A* within each region along the path.
- Reduces pathfinding cost dramatically for long paths in large worlds.

**Off-mesh links:**
- Manual connections between disconnected NavMesh surfaces: jump points, ladders, teleporters, drop-downs.
- Define as directed edges (one-way drop) or bidirectional (ladder). Tag with agent capability requirements.

**Crowd simulation:**
- RVO (Reciprocal Velocity Obstacles): each agent computes velocities that avoid collisions with nearby agents.
- Limit neighbor queries to a small radius. RVO with 100+ neighbors is expensive.
- Flow fields: for very large crowds (hundreds+), compute a vector field from goal to all positions. Agents follow the field. Amortize the cost over multiple frames.

---

## Tile and Chunk-Based World Systems

- Tilemap: 2D grid of tile indices referencing a tile palette. Multiple layers for ground, objects, decorations.
- Chunk storage: serialize chunks independently. Load/unload as units. Chunk size balances granularity vs overhead (16x16, 32x32 are common for 2D; 16x16x16 for voxel).
- Infinite world: generate chunks on demand. Use the chunk coordinate as input to the world seed for deterministic generation.
- Chunk generation queue: prioritize chunks near the player. Generate on a background thread. Use a ring buffer of loaded chunks centered on the player.

---

## Level-of-Detail for World Geometry

- **Discrete LOD:** artist creates 3-4 mesh versions at decreasing polygon counts. Switch based on distance to camera. Transition can pop visually.
- **Cross-fade / dithering:** render both LODs simultaneously with screen-door transparency during transition. Eliminates popping at the cost of brief overdraw.
- **HLOD (Hierarchical LOD):** merge distant objects into single combined meshes. An entire building becomes one draw call at distance. Reduces draw call count dramatically.
- **Impostors:** render 3D object to a billboard texture. Display the billboard at extreme distances. Update the billboard only when the viewing angle changes significantly.

---

## Environment Systems

**Day/night cycle:**
- Central time system: a float representing time-of-day (0.0-24.0), advanced at a configurable rate.
- Lighting: lerp sun direction, color, and intensity along the time curve. Use gradient textures or keyframed values for sky color.
- NPC schedules: define behaviors keyed to time ranges. NPCs query the time system and transition states accordingly.
- Do not tie game logic to real-time clock unless the design explicitly requires it.

**Weather system:**
- State machine: clear -> cloudy -> rain -> storm -> clear. Transitions have minimum and random duration.
- Each weather state defines: particle effect parameters, ambient lighting modification, audio ambience, gameplay effects (visibility reduction, movement speed).
- Transition smoothly: cross-fade particle intensity and lighting values over the transition duration.

**Destructible environments:**
- Health per destructible object. Damage reduces health. At zero, swap the intact mesh for a debris prefab.
- Debris: pre-fractured mesh pieces with physics enabled. Despawn after a timer or distance threshold to manage object count.
- NavMesh update: mark destroyed objects for NavMesh re-bake if they were blocking navigation.

---

## Spawn Systems

- **Spawn points:** tagged positions in the world. Filter by entity type, difficulty, spawn conditions.
- **Wave spawning:** define waves as lists of (entity type, count, delay). Track active entity count. Trigger next wave when count drops below threshold or timer expires.
- **Population density:** define maximum entity count per region. Spawner checks region population before spawning. Prevents overcrowding.
- **Respawn:** timer-based (fixed cooldown) or condition-based (player leaves area, time-of-day change). Store last-death timestamp per spawn point.
- **Director-style dynamic spawning:** monitor player metrics (health, ammo, idle time) and adjust spawn intensity. Left 4 Dead's AI Director is the canonical example.

---

## Level Design Flow Patterns

**Intensity curves:**
- Alternate high-intensity sections (combat, puzzle) with low-intensity sections (exploration, story, safe areas).
- The pattern is tension-release-tension-release, with overall escalation toward the climax.
- Map this curve before building geometry. Each section of the level corresponds to a point on the curve.

**Gating mechanisms:**
- Ability gates: require a specific ability to pass (double jump, grapple hook). Core to metroidvania design.
- Key/lock: literal or metaphorical. Find the key in area A to unlock area B. Creates directed exploration.
- Story gates: narrative triggers that open new areas. Risk: feels arbitrary if not well-motivated.

**Player guidance:**
- Lighting: bright areas attract attention. Light the critical path more than dead ends.
- Environmental cues: contrasting colors on interactive objects, worn paths, NPC gaze direction.
- Breadcrumbing: place collectibles along the intended path. Players follow rewards.
- Weenies (Disney term): tall, visible landmarks that orient the player and pull them forward.

**Pacing tools:**
- Lock-behind: seal the entrance after the player enters an arena. Forces commitment to the encounter.
- Safe rooms: explicitly marked spaces where enemies cannot enter. Provides psychological relief.
- Shortcuts: connect late areas back to early areas. Reward exploration and reduce backtracking tedium.
