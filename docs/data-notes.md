# The basketball dataset — facts, conventions, traps

Official repo: <https://github.com/SkillCorner/opendata-basketball> (MIT, ~66 stars)
Read `docs/PRIMER.md` and `docs/data_dictionary/` in that repo before writing code.
SkillCorner says explicitly: those docs are written to be read by both analysts *and*
LLMs — point Claude at them instead of hunting for tutorials (there are none).

## What you get
**Liga Endesa ACB 2025/26.** Broadcast optical tracking: computer vision on the TV feed,
no in-venue hardware.

1. **10 full games** — tracking + Dynamic Events + game metadata.
2. **Season aggregates** — 293 of 327 games, player-season roll-ups of shots, drives and
   picks, pivoted by zone / contest level / shot type / coverage. **Offence only.**

The 10 sample games:

| gameId | Date | Home | Away | Score |
|---|---|---|---|---|
| 114243 | 2025-10-11 | BAXI Manresa | Coviran Granada | 83-68 |
| 114234 | 2025-10-18 | Casademont Zaragoza | Leche Rio Breogan | 84-88 |
| 114169 | 2025-12-14 | CB UCAM Murcia | Joventut Badalona | 80-77 |
| 114099 | 2026-01-31 | Basquet Girona | San Pablo Burgos | 77-71 |
| 114086 | 2026-02-08 | Dreamland Gran Canaria | Bitci Baskonia | 75-97 |
| 178442 | 2026-03-21 | MoraBanc Andorra | Bilbao Basket | 98-102 |
| 179612 | 2026-04-12 | Malaga | Valencia BC | 89-96 |
| 184439 | 2026-04-19 | Real Madrid | Lenovo Tenerife | 90-95 |
| 188630 | 2026-05-03 | BC Barcelona | Dreamland Gran Canaria | 91-69 |
| 191313 | 2026-05-29 | Leche Rio Breogan | Casademont Zaragoza | 94-95 |

## File layout
```
data/aggregates/acb_{shots,drives,picks}aggregates_20252026.csv
data/player_id_aliases.csv
data/matches.json
data/matches/{gameId}/{gameId}_game_data.json          # rosters + match info
data/matches/{gameId}/{gameId}_dynamic_events.json     # all event families, one object
data/matches/{gameId}/{gameId}_tracking_data.jsonl.gz  # 25 fps, 30-46 MB/game (Git LFS)
```

## Conventions
- **Tracking**: 25 fps, one JSON object per video frame, player + ball positions.
- **Coordinates**: origin at **centre of the court**, units **feet**.
- **Event families** in `dynamic_events.json`: chances, possessions, shots, picks,
  drives, passes, touches, dribbles, free_throws, fouls, rebounds, turnovers, timeouts,
  isolations, handoffs, posts, off_ball_screens, closeouts, chance_players, matchups.
  Every record carries `id`, `gameId`, `season`, `period` and its `chanceId` /
  `possessionId` — it's a relational bundle, joinable in one pass.
- Events carry **tracking-derived context a hand-scored feed does not have**: defender
  identity and distance, coverage type, exact location. That context is the whole edge.

## Traps (from the repo's README / KNOWN_ISSUES)
- ~76-83% of player positions per game are **directly detected**; the rest extrapolated.
  Mean `predError` ~1.5-1.9 ft (p95 ~4.9-6.3 ft); extrapolated-only ~4.4-5.2 ft.
  → Filter or weight by `isDetected` / `predError` for anything distance-sensitive.
- Raw tracking needs **smoothing before computing speed or acceleration**.
- A few players have **two `player_id` values** — merge via `player_id_aliases.csv`.
- Compute team scores from `shots` + `free_throws`, **not** `chances.ptsScored`.
- `shots` **includes fouled misses**, which box scores do not count as attempts.
- Picks aggregates count **direct picks only**.
- `passes.toReceiverId` sometimes holds the **intercepting defender**, not the receiver.
- Aggregates are **offence-only** and cannot be reproduced from the 10 games.

## Sample-size reality check
10 games ≈ 1,300-1,600 shot attempts total across 20 team-games. That is enough for a
careful descriptive or mechanistic study, and **not** enough to train a deep model from
scratch. Projects that fit something interpretable on the 10 tracking games and then
sanity-check or extrapolate it against the 293-game aggregates get volume *and* depth —
few entrants will bother to bridge the two layers.

## Trap found 2026-10-16: event-table locations are NOT in the same frame as raw tracking xyz
The primer says locations across "`tracking_data` and every event table" share one
convention (offense attacks negative x). In practice, confirmed by comparing the same
player at the same frame: **raw `tracking_data` xyz is fixed to the physical camera/
court and never flips. Event-table `location`/`startLoc`/`endLoc`/`touchLoc` etc. are
normalized per chance so the offense always attacks negative x** — the two are the
negation of each other whenever the offense's physical attacking basket is on the
positive-x side at that point in the game.

The flip is fully determined by period and which team is on offense (FIBA swaps ends at
halftime, so periods 1-2 share one physical layout and 3-4 the other):
```
flip_needed = is_home_team_on_offense XOR (period <= 2)
```
(derived empirically on game 114243's `closeouts`; re-verify on another game before
trusting it blindly — see which team's raw tracking sits on which side in period 1).

**Practically: don't mix the two.** Plot raw `tracking_data` positions against other raw
`tracking_data` positions (self-consistent), or event-table locations against other
event-table locations (self-consistent) — never both in the same scene without
transforming one to match the other. A zoom window, a spacing/gravity metric, or a
closeout animation built from event `location` fields but raw `xyz` dots (or vice versa)
will silently put things on the wrong half of the court.

## Trap found 2026-10-16: tracking_data frameIdx is not the line number
Dead broadcast time between periods isn't written to `tracking_data.jsonl.gz` at all, so
line position drifts behind `frameIdx` as the game goes on (measured on game 114243: 0
frames missing at the start of Q1, 592 by Q2, 1,206 by Q3, 2,668 by Q4). `frameIdx` *is*
monotonically non-decreasing throughout, so a forward scan filtering on the `frameIdx`
field is correct; slicing by line number is not. `src/acb/tracking.py:load_tracking_range`
does this correctly — use it rather than re-deriving the slice.
