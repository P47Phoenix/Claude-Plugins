# Graphics and Rendering Architecture

Reference for render pipeline design, shader systems, lighting, post-processing, and GPU optimization patterns.

---

## Render Pipeline Architecture

**Forward rendering:**
- Each object is drawn once per light that affects it (single-pass) or once with all lights evaluated in one pass (single-pass forward).
- Transparent objects work naturally: render back-to-front with alpha blending.
- Light count limitation: evaluating many lights per fragment is expensive. Practical limit ~8-16 dynamic lights without clustering.
- Best for: mobile, VR (simpler pipeline, lower latency), stylized games with few lights.

**Deferred rendering:**
- Geometry pass: render all objects to a G-buffer (albedo, normal, depth, roughness/metallic).
- Lighting pass: for each light, render a volume (sphere for point lights, cone for spot lights) and evaluate lighting using G-buffer data.
- Decouples lighting cost from scene complexity. Hundreds of lights are feasible.
- Limitations: no transparency in the G-buffer (transparent objects require a separate forward pass). High memory bandwidth for G-buffer reads. MSAA is impractical; use TAA or FXAA.

**Forward+ (clustered forward):**
- Divide the screen (or view frustum) into tiles or 3D clusters. Assign lights to clusters in a compute shader pre-pass.
- During the forward pass, each fragment looks up its cluster and evaluates only the lights assigned to it.
- Best of both worlds: supports transparency, handles many lights, lower bandwidth than deferred.
- Increasing adoption: Unreal, Unity URP/HDRP, and custom engines use variants of this.

**Tile-based deferred (mobile):**
- Mobile GPUs have tile-based architectures. On-chip tile memory is fast; main memory access is slow.
- Keep the G-buffer in tile memory. Perform lighting in-tile before writing to main memory. Saves bandwidth.
- Design the pipeline to minimize render target switches (each switch flushes tiles to main memory).

---

## Shader Architecture

**Uber shaders:**
- One shader file with `#ifdef` branches for every feature combination. Compiler strips unused branches per variant.
- Pros: all shader logic in one place, easy to maintain consistency.
- Cons: combinatorial explosion of variants (10 toggles = 1024 variants). Compile times can become prohibitive.
- Mitigation: identify which toggles actually co-occur. Prune impossible combinations. Use multi-compile only for runtime-varying features; shader_feature for material-fixed features.

**Shader variants / permutations:**
- Pre-compile all needed permutations at build time. Runtime selects the correct variant by keyword set.
- Cache compiled variants on disk. First-launch compilation causes stutters (the "shader compilation stutter" problem).
- Warm the shader cache by pre-rendering representative scenes during loading.

**Modular shader graphs (node-based):**
- Visual node editors (Unity Shader Graph, Unreal Material Editor, Godot Visual Shader).
- Enable artist-created materials without writing code. Generate optimized shader code from the graph.
- Architect consideration: define a standard set of master graphs/templates. Artists create instances, not new graphs from scratch.

**Compute shaders:**
- General-purpose GPU computation. Use for: particle simulation, post-processing, culling, physics, procedural generation.
- Dispatch in thread groups. Size thread groups to match GPU wavefront size (32 for NVIDIA, 64 for AMD).
- Synchronization between compute and graphics: use barriers and resource transitions. Incorrect synchronization causes visual corruption.

---

## Level-of-Detail Strategies

**Discrete LOD:**
- Artist creates 3-4 mesh versions: LOD0 (full detail), LOD1 (50% triangles), LOD2 (25%), LOD3 (10% or billboard).
- Switch based on screen-space size (percentage of screen occupied), not raw distance. Accounts for FOV and resolution.
- Hysteresis: switch to lower LOD at distance D, switch back to higher LOD at D * 0.8. Prevents flickering at boundary.

**Cross-fade / dithered transitions:**
- During transition, render both LODs with dithered opacity (screen-door pattern). Fades over 0.5-1 second.
- Costs double draw calls during transition. Limit the number of simultaneously transitioning objects.

**HLOD (Hierarchical LOD):**
- Merge clusters of distant objects into single combined meshes at build time.
- An entire building block at distance becomes one mesh with one draw call instead of hundreds.
- Streaming integration: load HLODs first, replace with individual objects as the player approaches.

**Impostor LOD:**
- Pre-render the 3D object from multiple angles to a texture atlas. Display as a billboard that selects the closest angle.
- Octahedral impostors: 8x8 grid of views covering a hemisphere. Interpolate between nearest views.
- Best for: vegetation at medium distance, distant architectural detail.

---

## Lighting Systems

**Baked lightmaps:**
- Pre-compute global illumination and store as textures mapped to static geometry. Zero runtime cost for indirect light.
- Limitations: static only (no dynamic time-of-day), large texture memory, long bake times.
- UV2 requirement: lightmap UVs must not overlap. Auto-unwrap tools exist but review results for quality.

**Real-time dynamic lights:**
- Full flexibility: moving lights, time-of-day, destructible environments.
- Cost: each light requires shadow map rendering (rendering the scene from the light's perspective).
- Budget: limit real-time shadow-casting lights to 1-4 in view. Additional lights can be shadow-less (cheaper, no self-shadowing).

**Hybrid (the standard for modern games):**
- Bake ambient/indirect lighting. Render direct lights dynamically.
- Light probes: spherical harmonics samples placed in the world. Dynamic objects sample nearby probes for indirect lighting approximation.
- Reflection probes: capture environment reflections at key points. Objects sample the nearest probe for specular reflections. Use box or sphere projection to correct parallax.

**Global illumination approaches:**
- Light Propagation Volumes (LPV): inject light into a 3D grid, propagate iteratively. Low quality but real-time. Largely superseded.
- Voxel Cone Tracing (VXGI): voxelize the scene, trace cones through the voxel grid for diffuse and specular GI. Medium quality, moderate cost.
- Screen-space GI (SSGI): trace rays in screen space. Cheap but misses off-screen contributions.
- Lumen (Unreal 5): hybrid software ray tracing using signed distance fields and screen-space traces. High quality, significant cost. Represents the current state-of-the-art for real-time GI.

---

## Shadow Techniques

**Shadow maps:**
- Render the scene from the light's perspective into a depth texture. During the main pass, project each fragment into the shadow map to determine visibility.
- Resolution is the primary quality factor. Low resolution = aliased shadow edges.

**Cascaded shadow maps (CSM):**
- Split the view frustum into 3-4 depth ranges (cascades). Each cascade gets its own shadow map with appropriate resolution.
- Near cascades: small area, high texel density, sharp shadows. Far cascades: large area, lower density, softer shadows.
- Cascade split distances: logarithmic distribution works well. Tune per-project for visual quality.

**Shadow atlas:**
- Pack multiple lights' shadow maps into one large texture. Allocate atlas tiles based on light importance and screen coverage.
- Reduces render target switches. Standard approach for many-light scenarios.

**Contact-hardening shadows (PCSS):**
- Shadows are sharp near the contact point, soft farther from the caster. Physically motivated.
- Two-pass: blocker search (find average blocker distance) then PCF with a kernel size proportional to blocker distance.

**Shadow caching:**
- Static lights casting shadows on static geometry: render the shadow map once, reuse until the light or geometry changes.
- Cache invalidation: track which objects have moved. Re-render only affected shadow map regions.

---

## Post-Processing Pipeline

**Typical execution order:**
```
Scene render (HDR)
  -> Screen-space ambient occlusion (SSAO/GTAO/HBAO)
  -> Screen-space reflections (SSR)
  -> Volumetric lighting/fog
  -> Motion vectors (per-object + camera)
  -> Tone mapping (HDR -> LDR)
  -> Color grading (LUT application)
  -> Bloom (threshold -> downsample chain -> upsample blend)
  -> Depth of field
  -> Motion blur
  -> Temporal anti-aliasing (TAA)
  -> Film grain, vignette, chromatic aberration
  -> UI overlay (rendered in LDR, after all post-processing)
```

**Temporal anti-aliasing (TAA):**
- Jitter the projection matrix sub-pixel each frame. Blend current frame with history buffer using motion vectors.
- Ghosting: moving objects leave trails in the history buffer. Mitigate with neighborhood clamping (clamp history color to the min/max of the current frame's 3x3 neighborhood).
- Sharpening pass after TAA to counteract the inherent blurring.

**Bloom:**
- Threshold: extract pixels above a brightness threshold. Downsample through a chain of half-resolution buffers (5-6 levels). Upsample and blend back.
- Use a smooth threshold curve (knee) to avoid hard cutoffs that cause flickering.
- Bloom is additive energy. Excessive bloom washes out the image. Subtle bloom adds atmosphere.

**Screen-space ambient occlusion:**
- SSAO (original): sample depth buffer in a hemisphere around each pixel. Occluded samples darken the pixel. Noisy, requires blur pass.
- GTAO (Ground Truth AO): more physically accurate, integrates visibility over the hemisphere using horizon angles. Better quality per sample.
- HBAO (Horizon-Based AO): traces rays along the depth buffer. Good balance of quality and performance.
- Half-resolution AO with bilateral upsample: reduces cost by 4x with minimal quality loss.

**Color grading and tone mapping:**
- Tone mapping converts HDR to LDR. ACES is the industry standard (filmic curve, pleasing highlight rolloff). Reinhard is simpler but washes highlights.
- Color grading via 3D LUT (lookup table): a 32x32x32 or 64x64x64 color cube. Apply color transformations by looking up the input color in the LUT. Artists author LUTs in external tools.

---

## GPU Optimization Patterns

**Draw call batching:**
- Static batching: combine meshes that share a material into a single mesh at build time. Zero runtime cost, increased memory.
- Dynamic batching: combine small meshes at runtime. CPU overhead for combining. Only worth it for very small meshes (<300 vertices).
- GPU instancing: draw many copies of the same mesh in one draw call with per-instance data (transform, color). Best for vegetation, debris, crowds.
- SRP Batcher (Unity-specific): does not reduce draw calls but minimizes GPU state changes between draws with the same shader. Faster than traditional batching for varied materials.

**Culling:**
- Frustum culling: discard objects entirely outside the camera frustum. Cheap, always enabled.
- Occlusion culling: discard objects hidden behind other objects. Hardware occlusion queries (GPU readback, 1-frame latency), software rasterization (CPU-based, no latency), hierarchical Z-buffer (HZB, test bounding boxes against downsampled depth buffer).
- GPU-driven culling: perform frustum and occlusion tests in a compute shader. Output an indirect draw buffer. Eliminates CPU bottleneck for large scenes.

**GPU-driven rendering:**
- Indirect draws: GPU fills a draw argument buffer. CPU issues a single indirect draw call. The GPU decides what to draw.
- Meshlet rendering: split meshes into small clusters (meshlets, ~64 triangles each). Cull meshlets individually in a compute shader. Enables per-cluster LOD and occlusion culling.
- Nanite (Unreal 5): extreme meshlet-based approach. Virtualized geometry with continuous LOD at the cluster level. Eliminates traditional LOD authoring.

---

## Particle System Architecture

**CPU vs GPU particles:**
- CPU: simulated on CPU, uploaded to GPU for rendering. Flexible (access game state, physics), limited count (~10K before CPU bottleneck).
- GPU: simulated in compute shaders. Millions of particles feasible. Limited interaction with game state (must pass data via buffers).
- Use CPU particles for gameplay-interactive effects (damage numbers, ability indicators). Use GPU particles for visual-only effects (weather, ambient dust, fire).

**Particle pooling:**
- Pre-allocate a fixed particle buffer. Dead particles are recycled, not deallocated. Avoids allocation spikes.
- Ring buffer emission: new particles overwrite the oldest dead particles.

**LOD for particles:**
- Reduce spawn rate at distance. Increase particle size to compensate for fewer particles.
- Beyond a threshold distance, disable the emitter entirely.
- Performance-critical: particle overdraw (many overlapping transparent particles) is a major fillrate cost.

---

## Material System Design

**PBR pipeline:**
- Metallic/roughness workflow: albedo (base color), metallic (0 or 1, with transitions), roughness (0 = mirror, 1 = diffuse). Industry standard (glTF, Unity, Godot).
- Specular/glossiness workflow: diffuse, specular color, glossiness. Used in some legacy pipelines. Not recommended for new projects.
- Energy conservation is built into PBR BRDFs. Increasing roughness reduces specular intensity while increasing diffuse spread.

**Material layering:**
- Blend multiple material layers based on masks (vertex color, height maps, procedural noise).
- Terrain: blend 4+ ground materials per terrain tile using splat maps. Limit to 4 layers per draw call for performance (one RGBA splat texture).
- Decals: project a material layer onto underlying surfaces. Deferred decals modify G-buffer values. Forward decals require mesh-projected geometry.

**Virtual texturing:**
- Stream texture pages (tiles) on demand based on what the camera sees. Only the visible mipmap levels of visible textures are in memory.
- Feedback buffer: render at low resolution to determine which texture pages are needed. Load those pages asynchronously.
- Eliminates texture memory limits at the cost of streaming complexity and potential pop-in.

**Material instancing:**
- Shared material: one material definition, one set of properties. All users look identical.
- Material instance: references a parent material, overrides specific properties (color, texture). Shares the compiled shader.
- Per-instance properties (via instancing buffers): per-object overrides without creating material instances. Best for color variation on instanced meshes.

---

## Camera System Architecture

**Virtual camera stack:**
- Multiple virtual cameras with priorities. The highest-priority active camera controls the view.
- Blending: when the active camera changes, interpolate position/rotation/FOV over a transition duration. Cut (instant), lerp (linear), ease-in-out (smooth).
- Each virtual camera defines a behavior (follow target, orbit, rail, fixed), not a position.

**Camera behaviors:**
- Follow: track a target with offset and damping. Damping prevents jerky movement. Higher damping = more sluggish camera.
- Orbit: rotate around a target at fixed distance. Input-controlled azimuth and elevation with clamping.
- Rail: camera position constrained to a spline or path. Closest point on the path to the target determines camera position.
- Free-look: player controls camera direction directly (FPS-style). Position follows the character.

**Cinemachine-style composition:**
- Dead zone: area where the target can move without the camera moving. Reduces micro-adjustments.
- Soft zone: area where the camera gradually moves to keep the target within it. Creates smooth following.
- Screen position target: place the target at a specific screen position (rule of thirds, lower-center for platformers).
- Damping: separate horizontal and vertical damping values. Vertical damping often higher (less jarring for jumps).

**Camera shake:**
- Perlin noise on position and rotation axes. Multiple layers at different frequencies for organic feel.
- Shake profile: amplitude decay over time (exponential or linear). Trigger shake on impact events with intensity parameter.
- Never shake the actual camera transform. Apply shake as an additive offset that does not affect game logic.

---

## UI Rendering Architecture

**Immediate mode (ImGui-style):**
- UI defined procedurally each frame: `if (Button("Start")) { StartGame(); }`. No persistent UI objects.
- Best for: debug UIs, developer tools, prototyping. Low overhead, zero state management.
- Not suitable for: complex animated UIs, accessibility features, rich styling.

**Retained mode:**
- UI defined as a persistent scene graph of nodes (panels, buttons, labels). Layout computed on change, not every frame.
- Supports styling (CSS-like), animation, data binding, accessibility (screen readers, keyboard navigation).
- Standard for production game UIs.

**Render integration:**
- Screen-space overlay: rendered after all post-processing, directly to the backbuffer. Always on top. Standard for HUD and menus.
- World-space UI: rendered as geometry in the 3D scene. Affected by depth, lighting, post-processing. Used for in-world labels, health bars above enemies, diegetic UI (screens within the game world).

**UI batching and atlasing:**
- Combine UI textures into atlas sheets. Batch UI elements that share the same atlas into single draw calls.
- Breaking batches: Z-order interleaving of different atlases, different shaders, or clipping rects. Minimize batch breaks by ordering UI layers carefully.
- Text rendering: signed distance field (SDF) fonts scale cleanly to any size. Pre-generate the SDF font atlas.

**Resolution independence:**
- Design UI at a reference resolution (e.g., 1920x1080). Scale uniformly to the actual resolution.
- Anchor-based layout: elements anchored to screen edges, corners, or center. Anchors define stretch and position behavior on different aspect ratios.
- Safe areas: account for notches, rounded corners, overscan on TVs. Inset critical UI elements from screen edges.
