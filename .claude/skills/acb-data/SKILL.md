---
name: acb-data
description: Load and query the SkillCorner ACB 2025/26 open dataset — tracking frames, dynamic events, season aggregates. Use whenever reading, joining, filtering or aggregating this project's data, before writing any loading code, and whenever a column name, coordinate, unit or data-quality question comes up.
---

# Working with the SkillCorner ACB dataset

## Before writing code
The dataset's own docs are authoritative and written to be read directly. Read them from
the clone rather than guessing column names:

```
data/raw/opendata-basketball/docs/PRIMER.md
data/raw/opendata-basketball/docs/data_dictionary/README.md      # event catalog + joins
data/raw/opendata-basketball/docs/data_dictionary/tracking_data.md
data/raw/opendata-basketball/docs/aggregates_columns.md
data/raw/opendata-basketball/docs/KNOWN_ISSUES.md
```
Grep the data dictionary for a field before inventing one. If a field is not in the
dictionary, say so rather than assuming it exists.

## Conventions that are easy to get wrong
- Tracking: **25 fps**, one JSON object per frame, `.jsonl.gz`.
- Coordinates: **feet**, origin at **centre court**. Convert to a half-court frame by
  mirroring on the attacking direction before pooling possessions.
- **`frameIdx` is not the line number.** Dead broadcast time between periods isn't
  written to the file, so the line position drifts behind `frameIdx` as the game goes on
  (0 frames missing at Q1 start, 2,668 by Q4 on game 114243). `frameIdx` is monotonically
  non-decreasing, so filter on the field itself — `src/acb/tracking.py:load_tracking_range`
  does this correctly; don't slice by line number.
- **Raw tracking xyz and event-table locations are different coordinate frames.** Raw
  `tracking_data` xyz is fixed to the physical camera and never flips. Event-table
  `location`/`startLoc`/`endLoc`/etc. are normalized per chance so the offense always
  attacks negative x — the two are exact negations of each other whenever the physical
  attacking basket is on the positive-x side. Never plot or compare one against the
  other without transforming; keep each self-consistent (details + the derived flip
  rule in `docs/data-notes.md`).
- Events: one JSON object per game holding **one array per event family** — chances,
  possessions, shots, picks, drives, passes, touches, dribbles, free_throws, fouls,
  rebounds, turnovers, timeouts, isolations, handoffs, posts, off_ball_screens,
  closeouts, chance_players, matchups. Join on `chanceId` / `possessionId`.
- Aggregates are **player-team-season, offence only**; traded players also get a
  `team_name = "total"` row — exclude it or you double-count.

## Data-quality rules this project follows
- Merge duplicate players through `data/player_id_aliases.csv` on every load.
- Drop the `team_name = "total"` rows unless the question is season totals.
- Team scores come from `shots` + `free_throws`, never `chances.ptsScored`.
- `shots` includes **fouled misses**; box-score FGA excludes them. State which you mean.
- `passes.toReceiverId` can hold the intercepting defender — validate before trusting.
- For anything distance- or speed-sensitive, filter or weight on `isDetected` /
  `predError`. Mean error is ~1.5-1.9 ft and extrapolated points are ~3x worse; a
  "defender 3 ft away" claim is inside the noise unless detected positions are used.
- **Smooth before differentiating.** Raw frame-to-frame deltas give garbage speeds and
  acceleration. Use a Savitzky-Golay or Butterworth filter and record the parameters.

## Preferred access pattern
1. **SQL first, in DuckDB.** It reads the JSON and CSVs directly and the owner of this
   repo reads SQL faster than pandas:
   ```sql
   SELECT * FROM read_csv_auto('data/raw/opendata-basketball/data/aggregates/acb_shotsaggregates_20252026.csv') LIMIT 5;
   SELECT unnest(shots) FROM read_json_auto('data/raw/.../114243_dynamic_events.json');
   ```
   Put each question in its own file under `sql/`.
2. **Parquet for tracking.** Convert `.jsonl.gz` once into `data/interim/*.parquet`, then
   query it with DuckDB. Never re-parse the gzip in a loop.
3. Python only for geometry, smoothing, modelling and plots.

## Reproducibility
Every derived table must be rebuildable from `data/raw/` by one documented command.
Nothing in `data/interim/` is ever hand-edited, and nothing there is committed.
