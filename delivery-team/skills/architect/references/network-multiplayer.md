# Network and Multiplayer Architecture

Reference for multiplayer networking patterns, synchronization, lag compensation, and infrastructure design.

---

## Network Architecture Patterns

**Client-server authoritative:**
- Server owns the canonical game state. Clients send inputs, server simulates, server sends results.
- Clients display a predicted/interpolated view. Server resolves disagreements.
- Best for: competitive games, games with more than ~8 players, any game where cheating matters.
- Cost: requires dedicated servers or a hosted service. Adds development complexity for prediction and reconciliation.

**Peer-to-peer:**
- Each peer runs a full simulation. Peers exchange inputs or state directly.
- NAT traversal is the first hard problem (STUN, TURN, ICE). Expect 10-20% of players to be unreachable without a relay.
- No inherent authority: any peer can cheat. Suitable only for cooperative or low-stakes competitive games.
- Best for: fighting games (2 players, low bandwidth), cooperative games with trusted players, LAN play.

**Hybrid:**
- Authoritative game server for state, P2P channels for voice chat or non-critical data.
- Reduces server bandwidth while maintaining authority where it matters.
- Common pattern: relay critical game state through the server, allow direct P2P for voice and non-gameplay social features.

**Decision matrix:**

| Factor | Client-Server | P2P | Hybrid |
|--------|:---:|:---:|:---:|
| Anti-cheat | Strong | Weak | Strong |
| Player count | High | Low (2-8) | Medium-High |
| Server cost | High | None | Medium |
| Latency | Higher (round trip to server) | Lower (direct) | Varies |
| NAT issues | Server has public IP | Major problem | Partial |

---

## State Synchronization

**Snapshot interpolation:**
- Server sends full world state snapshots at a fixed rate (e.g., 20Hz). Clients buffer two snapshots and interpolate between them.
- Interpolation delay = snapshot interval (50ms at 20Hz). Adds perceived latency but produces smooth visuals.
- Extrapolation for late snapshots: risky, causes visual errors. Prefer brief freezing over bad extrapolation.

**Delta compression:**
- Send only fields that changed since the last acknowledged snapshot. Reduces bandwidth dramatically.
- Track per-client acknowledged baseline. Each client may have a different baseline depending on packet loss.
- XOR-based delta: XOR current and baseline, then compress. Unchanged fields become zero bytes, which compress well.

**Interest management:**
- Each client receives only entities relevant to them. Relevance criteria: distance, line of sight, team, game mode.
- Area of interest (AOI): spatial partitioning of the world. Only send entities in the client's AOI region plus a margin.
- Priority-based: when bandwidth is tight, prioritize nearby and fast-moving entities. Deprioritize distant, slow-moving ones.
- Send rate scaling: high-priority entities update every tick. Low-priority entities update every Nth tick.

**Entity relevancy and dormancy:**
- Dormant entities consume zero bandwidth. Wake them when they enter a client's AOI.
- Track dormancy state per-client-per-entity. An entity dormant for client A may be active for client B.

---

## Rollback Netcode

**Core loop:**
1. Receive remote inputs. If an input arrives for a past frame, roll back game state to that frame.
2. Re-apply all inputs (local and remote) from the rollback frame to the current frame (resimulation).
3. If the predicted state matches the corrected state, no visual disruption. If it differs, smooth the correction.

**Input prediction:** assume the remote player repeats their last known input. Correct when the actual input arrives. Works well for continuous inputs (movement); poor for discrete inputs (shooting, jumping).

**State save/restore:** every frame, save a snapshot of the game state to a ring buffer. On rollback, restore the snapshot at the rollback frame. Snapshot must be lightweight -- only gameplay-critical state (positions, velocities, health), not visual state.

**Visual smoothing:** after correction, do not snap entities to corrected positions. Lerp visual representation toward the corrected position over several frames. Separate simulation position from render position.

**When rollback is appropriate:**
- Fighting games: 2 players, small game state, frame-perfect input requirements. Rollback is standard.
- Fast-paced action (shooters, racing): rollback works for movement prediction. Hit detection is typically handled by server rewind instead.
- When rollback is not appropriate: MMOs (too many entities to snapshot), turn-based (no need), RTS with many units (state too large).

**GGPO-style implementation:**
- Fixed frame length. Inputs are tagged with frame numbers. Synchronize game start frame.
- Input delay of 1-2 frames to absorb jitter and reduce rollback frequency.
- Maximum rollback window: cap at 7-8 frames. Beyond that, corrections are too jarring. If latency exceeds the window, add input delay.

---

## Lag Compensation

**Client-side prediction:**
- Client applies local input immediately without waiting for server confirmation. Player sees instant response.
- When server confirms, compare predicted state with authoritative state. If they match, discard the prediction. If they differ, correct.
- Only predict the local player's state. Never predict other players' actions (use interpolation for them).

**Server reconciliation:**
- Server processes input with timestamp. Sends back the authoritative state for that timestamp.
- Client replays all unacknowledged inputs on top of the server state to produce the current predicted state.
- This is the standard model for all modern FPS games (Quake, Overwatch, Valorant).

**Hit detection with server rewind:**
- When a client fires, the server rewinds other players' positions to where they were at the client's perceived time.
- Perceived time = current server time - client RTT/2 - interpolation delay.
- Rewind uses the server's position history buffer. Look up positions at the rewound timestamp.
- Fairness trade-off: the shooter sees accurate hits, but the target can be hit after they think they are behind cover. Cap the maximum rewind window (e.g., 200ms) to limit this effect.

**Interpolation buffer:**
- Display remote entities at a position slightly in the past (typically 100ms behind real-time).
- Buffer length = 2-3x the snapshot interval. Absorbs jitter and packet loss.
- Longer buffer = smoother display but more perceived latency. Shorter buffer = more responsive but choppy on bad connections.

**Latency budgets:**
- Total perceived latency = input delay + client processing + network RTT + server processing + interpolation delay.
- Target: under 100ms total for action games. Under 200ms for most genres. Above 300ms, most real-time games feel unplayable.

---

## Matchmaking Architecture

**Skill-based matchmaking (SBMM):**
- Elo: simple rating adjusted after each match. Good for 1v1. Poorly handles team games.
- Glicko-2: adds rating deviation (confidence) and volatility. New players have wide deviation, converge over time.
- TrueSkill/TrueSkill 2: designed for team games. Models individual skill within team outcomes. Handles parties and uneven teams.
- Placement matches: start new players with high uncertainty. 5-10 matches to converge on approximate skill.

**Queue systems:**
- Expand search criteria over time: start with tight skill/region match, widen every N seconds.
- Backfill: allow joining in-progress games to replace disconnected players. Reduce penalty for backfilled players.
- Party matching: match parties against parties of similar size. Solo queue vs team queue separation prevents frustration.

**Region-based matching:**
- Prefer low-latency matches. Player selects preferred region or auto-detect via ping measurement.
- Cross-region matchmaking as fallback when queue times exceed threshold. Warn players about expected latency.

---

## Session and Lobby Architecture

**Lobby state machine:**
```
Creating -> Waiting (players join/leave)
  -> Ready Check (all players confirm)
  -> Loading (all clients load the level)
  -> Playing (game in progress)
  -> Results (post-game summary)
  -> Disbanded
```

**Host migration (P2P / listen server):**
- When the host disconnects, another player is promoted to host. Requires serializing and transferring the full game state.
- Pre-select a migration candidate (second-lowest latency peer). Keep them informed of state changes to minimize migration time.
- Migration interrupts gameplay for 2-5 seconds. Acceptable for casual games, unacceptable for competitive.

**Join-in-progress:**
- New player receives a full state snapshot on join. Late joiners start with current world state, not from the beginning.
- Balance considerations: give late joiners catch-up mechanics or accept the disadvantage.

---

## Network Message Serialization

**Bit packing:**
- Write values using only the bits needed. A boolean is 1 bit, not 8. A health value 0-100 is 7 bits, not 32.
- Write a bit packing stream that tracks bit offset within a byte buffer. Reduces bandwidth 2-4x vs naive serialization.

**Variable-length encoding:**
- Small integers (0-127) use 1 byte, larger values use more. Protobuf varint encoding is the standard approach.
- Good for fields that are usually small but occasionally large (entity counts, delta values).

**Bandwidth budgets:**
- Typical: 5-15 KB/s per player upstream, 10-30 KB/s downstream (server to client).
- 64-player server at 20 KB/s per player = ~1.3 MB/s total downstream. Plan infrastructure accordingly.

**Message reliability:**
- Unreliable: fire-and-forget. Use for position updates, state snapshots -- stale data is worse than missing data.
- Reliable ordered: guaranteed delivery in order. Use for chat, important events (player death, objective capture).
- Reliable unordered: guaranteed delivery, may arrive out of sequence. Use for asset loading commands, configuration.

---

## Anti-Cheat Architecture

**Server authority is the foundation.** Client-side anti-cheat without server authority is security theater.

**Input validation:**
- Rate limit inputs: no more than N inputs per second. Reject excess.
- Range checks: movement speed cannot exceed max speed. Position deltas validated against physics constraints.
- Sequence validation: cannot fire without ammo, cannot jump while already airborne (unless double-jump is a mechanic).

**Anomaly detection:**
- Statistical analysis over time: flag players with inhuman accuracy, impossible reaction times, movement patterns that violate physics.
- Do not auto-ban on anomaly detection. Flag for review. False positives destroy player trust.
- Speed hack detection: compare client-reported time progression against server clock. Divergence indicates time manipulation.

**Replay validation:**
- Record inputs and random seeds. Replay the match deterministically. Compare outcomes with reported results.
- Expensive but definitive. Use for high-stakes matches (ranked, tournaments).

---

## Dedicated Server vs Listen Server

**Dedicated servers:**
- Run on cloud infrastructure. No player has host advantage. Consistent performance.
- Cost: monthly hosting fees scale with concurrent players. Containerized servers (Docker/Kubernetes) enable auto-scaling.
- Fleet management: orchestrate server allocation per region. Spin up servers in response to matchmaking demand. Drain and terminate idle servers.

**Listen servers:**
- One player's machine acts as server. Zero infrastructure cost. Higher latency for non-host players. Host advantage.
- Acceptable for: casual co-op, LAN play, small-scale games.

**Cloud scaling patterns:**
- Game server per pod/container. Orchestrator assigns players to servers with capacity.
- Scale based on queue depth, not CPU utilization. Games need servers before players are waiting, not after.
- Reserve capacity for peak hours. Pre-warm servers in advance of predictable demand (patch day, events, weekends).

---

## Real-Time vs Turn-Based Multiplayer

**Lockstep simulation:**
- All clients run the same deterministic simulation. Only inputs are shared, not state.
- Requires deterministic math (fixed-point, no floating-point non-determinism across platforms).
- Bandwidth is minimal (just inputs). But any desync is catastrophic -- add checksum validation to detect desync early.
- Best for: RTS (many units, sharing state would be expensive), simulation games.

**Async turn-based:**
- Store game state on a server. Players take turns at their own pace (hours or days between turns).
- Push notifications when it is a player's turn. Allow multiple concurrent games per player.
- Simple networking: REST API calls to submit turns and fetch state. No persistent connection needed.

---

## Transport Protocols

**UDP:**
- Low latency, no head-of-line blocking. Packets may be lost, duplicated, or reordered.
- Build reliability, ordering, and fragmentation on top as needed. Most game networking libraries do this (ENet, GameNetworkingSockets, LiteNetLib).
- Standard choice for real-time multiplayer.

**TCP:**
- Reliable, ordered delivery. Head-of-line blocking means one lost packet stalls all subsequent packets.
- Acceptable for: turn-based games, lobby/chat, login/authentication, downloading assets.
- Never use raw TCP for real-time game state in competitive contexts.

**WebSocket:**
- TCP-based, works in browsers. Required for web-based multiplayer games.
- Higher latency than UDP. Acceptable for casual real-time games, turn-based, and social games.
- WebTransport (emerging): UDP-like semantics in the browser. Watch for adoption.

**QUIC:**
- Reliable UDP with multiplexed streams. No head-of-line blocking between streams (unlike TCP).
- Independent streams for independent data: one stream for chat, one for state, one for voice. Loss on one stream does not stall others.
- Growing adoption. Good fit when you need both reliable and unreliable channels without managing two separate connections.
