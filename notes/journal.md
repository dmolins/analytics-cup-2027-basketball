# Decision log

Append-only. One entry per working session that produced something: a finding, a killed
idea, a definition, a surprise in the data. Date everything — the final README is written
from this file.

Template:

```
## YYYY-MM-DD — short title
**Question:** what I was trying to find out
**Did:** what I actually ran
**Found:** the result, with the number
**Means:** my read of it as a coach
**Next:** the single next step
```

---

## 2026-10-11 — project opened
**Question:** what is this competition and what can be done with the data?
**Did:** scraped the Analytics Cup 2.0 rules, dates and judging criteria into
`docs/competition-brief.md`; read the SkillCorner basketball open-data README into
`docs/data-notes.md`; drafted seven candidate ideas in `docs/ideas.md`.
**Found:** deadline is 18 Dec 2026 (68 days). Basketball theme is Shot Quality but it is
optional. Season aggregates are offence-only, while the 10 tracking games carry defensive
context — defender identity, distance, coverage type.
**Means:** defensive-side work is structurally under-served in this dataset, which is
where a coach's read is worth most.
**Next:** register for the Europe edition, install the toolchain, pull the data, and
animate one real possession end to end.

## 2026-10-11 — direction set
**Question:** region, team size, idea.
**Did:** confirmed with David.
**Found:** Europe region (Paris final, 17 Feb 2027), solo entry, author David Molins.
Chosen idea: **A — Advantage ledger** (create/keep/lose a defensive advantage, then
finish it), over closeout quality (B) and action-chain-to-shot-quality (C, kept as
fallback).
**Means:** this is the highest-ceiling, highest-risk idea on the list, so the first two
weeks are the definitions, not the metric. If "advantage created" doesn't hold up against
10+ animated possessions by ~10 Nov, fall back to C rather than keep forcing A.
**Next:** run scripts/setup.sh, pull one game's tracking data, animate a few possessions
to start sanity-checking what "advantage" should mean in the tracking data.

## 2026-10-11 — environment up, first data validated
**Question:** does the toolchain actually work, and does the event data reconstruct a
real game correctly?
**Did:** `brew install uv`/`git-lfs` tried to compile cmake/openssl from source (no bottle
CDN reachable from this machine) and would have taken a very long time, so switched to
plain `python3 -m venv` + `pip install -e ".[dev]"` (PyPI is reachable) and wrote
`scripts/fetch_data.sh`, which pulls the dataset over plain HTTPS — LFS tracking files
via `media.githubusercontent.com` — with no `git`/`git-lfs` dependency at all. Ran it for
game 114243 (BAXI Manresa 83-68 Coviran Granada, 2025-10-11). Rebuilt the final score from
`shots` (made shots, 2/3 pts) + `free_throws` (made FTs, 1 pt).
**Found:** venv has duckdb, pandas, numpy, scipy, sklearn, matplotlib, mplbasketball, all
importing cleanly. Tracking file is a real 33.7 MB gzip (146,870 frames, 25 fps, ~98 min
incl. stoppages), confirmed not an LFS pointer. One tracking frame: `homePlayers` /
`awayPlayers` carry `xyz`, `speed`, `predError`, `isDetected`, `jersey`, `playerId`; one
sample player had `predError` ≈ 4.55 ft with `isDetected=0` — a real example of the
~1.5-1.9 ft mean / extrapolated-worse error the docs warn about. Game 114243 has 58
`closeouts` events, 135 `picks`, 58 `drives`, 11 `isolations` — plenty of signal for the
advantage-ledger idea. **Rebuilt score: 83-68 — exact match** to the real result.
**Means:** the event model is trustworthy; `offTeamId`/`outcome`/`three` on `shots` and
`offTeamId`/`outcome` on `free_throws` are exactly the fields to join on. The toolchain
being venv+pip+curl rather than uv+git-lfs is now the standing setup for this machine —
`scripts/setup.sh` and `scripts/fetch_data.sh` reflect that.
**Next:** decompress + eyeball an actual possession (ideally one with a `closeouts` or
`drives` event) by plotting positions over a few seconds, to start sanity-checking what
"advantage created" should look like geometrically.

## 2026-10-16 — first closeout animation, two real data bugs caught
**Question:** what does one closeout actually look like? Build a short animation to find
out, and start sanity-checking the advantage-ledger premise visually.
**Did:** wrote `src/acb/tracking.py` (frame loading) and `scripts/animate_closeout.py`
(FIBA court via mplbasketball, highlights ball handler + defender, live distance label,
phase annotation). Picked the closeout with the biggest gap closed among direct shots:
`closeout-114243-2-8`, Travis Munnings (Granada) vs. Hugo Benitez (Manresa, #22), Q2.
**Found:** two real bugs, both now fixed and documented in `docs/data-notes.md` +
the `acb-data` skill:
1. `tracking_data.jsonl.gz`'s `frameIdx` is **not** the line number — dead time between
   periods isn't written to the file, so line position drifts behind frameIdx (0 frames
   missing at Q1 start, 2,668 by Q4). First version of the loader sliced by line number
   and silently animated the wrong ~4s of the game (still real tracking data, just the
   wrong event). Fixed by filtering on the `frameIdx` field itself.
2. Event-table `location`/`startLoc`/`endLoc` fields are **not** in the same coordinate
   frame as raw `tracking_data` xyz — event fields are normalized so offense always
   attacks negative x, raw tracking is fixed to the physical camera. They're exact
   negations of each other whenever the physical attacking basket is on the positive-x
   side. Confirmed empirically across 4 closeouts in different periods; derived the
   exact flip rule (`is_home_offense XOR period<=2`). This had been silently sending
   player dots off-canvas in the first correct-frameIdx version of the animation.
**Means:** after both fixes, the animation tells a clean, correct story — defender-to-
ball-handler distance goes 23.0 -> 10.8 -> 1.9 -> 4.3 -> 7.5 ft across the clip, matching
the event record's own checkpoints (start 20.4, touch 14.1, end 2.8) — Benitez sprints
out from the top of the arc, closes to a tight contest, Munnings still gets the three off
but misses it. The event model and the geometry agree with each other and with basic
basketball sense. Both bugs would have been invisible in a results table (distances,
counts, correlations) — only a literal picture of the players caught them. That's a vote
for building more of these before trusting any tracking-geometry metric, not just for
closeouts.
**Next:** build 3-5 more closeout animations (varied outcomes: good contest + miss, late
closeout + make, help-and-recover) to start writing down, in basketball language, what
actually separates a good closeout from a bad one — the working definition the
advantage-ledger idea needs.
