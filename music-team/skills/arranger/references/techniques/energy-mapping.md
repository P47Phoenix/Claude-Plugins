---
loaded_by: arranger
level: L3
last_reviewed: 2026-10-26
---

# Technique: Energy Mapping

Energy is one integer per section, 1-10, describing the whole band: loudness, density, rhythmic
activity, and vocal intensity together. It is relative to this song, not to other songs.

## The scale

| Energy | Typical picture |
|--------|-----------------|
| 1-2 | One or two sounds, sparse, room to breathe (intro, a stripped ending) |
| 3-4 | Rhythm section implied, single vocal, dry (first verse, post-peak verse) |
| 5-6 | Full rhythm section, one added layer, lift in rhythmic activity (pre-chorus, bridge) |
| 7-8 | Everything the genre calls "core", doubled vocal, wide image (chorus) |
| 9-10 | Every layer in, top register active, crowd or stacked vocals (final chorus, last drop) |

Use the full range the song needs; a 4-to-6 map reads as flat even when the labels differ.

## Curve shapes

| Curve | Shape | Gate setting |
|-------|-------|--------------|
| Rising choruses (default) | Each chorus at or above the previous; verses sit under the next chorus; peak in the final chorus or the bridge | `chorus_rising` |
| Single arch | Climb to one peak, then descend; suits ballads and short forms | `strict_rising` |
| Free | Any shape; no curve rule, metrics only | `free` |

## Procedure

1. List sections in order with their roles: verse, pre-chorus, chorus, bridge, drop, outro.
2. Pick the floor (usually verse 1) and the ceiling (final chorus or bridge). Keep at least 3 points
   between them; 5-6 is typical for pop, rock, and electronic.
3. Place each chorus: first at ceiling minus 2 or 3, each later one 1 higher.
4. Place each verse 2 or 3 below the chorus it leads to. A second verse may sit one point above the first
   because the band keeps part of the chorus lift.
5. Place pre-choruses at the midpoint between the verse and the chorus they join. Place the bridge by
   intent: a low point (6 below the final chorus) for a reset, or the peak for a late climax.
6. Check the last section: it should be below the peak unless it is the final chorus.

## Pitfalls

- Equal energy everywhere with different instrument lists: the ear hears one level.
- A louder verse than the chorus it feeds: the chorus loses its arrival.
- Peak too early: after the highest point there is nowhere left to go; place it in the last third.
- Using the top of the scale on the first chorus: reserve 9-10 for the end.
- Treating energy as volume only: a sparse, high, fast section can outrank a loud, slow one.
