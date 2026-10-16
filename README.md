# Analytics Cup 2.0 — basketball entry (ACB 2025/26)

> **Working README.** The submitted one is capped at **1000 words and two figures/tables
> in total** — it gets written in December, from `notes/journal.md`. Keep this file for
> ourselves until then.

**Deadline: 18 December 2026.** Region: Europe (Paris final, 17 Feb 2027) — confirm at
registration. Rules, dates and judging: [`docs/competition-brief.md`](docs/competition-brief.md).

## Orientation
| File | What it's for |
|---|---|
| [`docs/competition-brief.md`](docs/competition-brief.md) | Every rule, date, prize and judging criterion |
| [`docs/data-notes.md`](docs/data-notes.md) | Dataset layout, conventions, known traps |
| [`docs/ideas.md`](docs/ideas.md) | Scored idea backlog and the current pick |
| [`notes/journal.md`](notes/journal.md) | Dated decision log — append after every session |
| [`CLAUDE.md`](CLAUDE.md) | How Claude works in this repo |

## Setup
```bash
./scripts/setup.sh                    # venv + deps, pulls game 114243 (~38 MB)
source .venv/bin/activate
./scripts/fetch_data.sh 114234 114169 # pull specific games as needed
./scripts/fetch_data.sh --all         # or all 10 games (~400 MB)
```
`fetch_data.sh` pulls the dataset over plain HTTPS (docs/CSVs via `raw.githubusercontent.com`,
the Git-LFS-tracked tracking files via `media.githubusercontent.com`) — no `git`/`git-lfs`
needed. Already validated: game 114243's events reconstruct the real 83-68 final score.

## Week one
1. **Register.** <https://pysport.org/analytics-cup/editions/analytics-cup2/register> —
   nothing else matters if this is missed. Join the Discord for rule clarifications and
   for a possible teammate (entries may be pairs).
2. **Watch the six 2026 finalist videos** (<https://pysport.org/analytics-cup/videos>).
   An hour here calibrates what a winning 60-second pitch looks like better than any
   amount of reading.
3. **Run setup, pull one game, animate one possession.** Pick a possession, watch the dots
   move, and check it against what you know a possession looks like. This is the single
   most useful first day — it turns the dataset from an abstraction into something you can
   coach against.
4. **Rebuild the box score from events.** Team score from `shots` + `free_throws`, not
   `chances.ptsScored`. If your numbers match the real final score, you understand the
   event model. If they don't, you've found your first real lesson.
5. **Query the season aggregates in SQL.** DuckDB reads the CSVs directly — start where
   you're already strong, and get a feel for the ACB's shot distribution before touching
   tracking geometry.
6. **Pick a direction by ~1 Nov.** Six weeks of building, two weeks for the README, the
   figures and the video. The write-up always takes longer than it looks.

## Rules that constrain everything
- **Only the provided SkillCorner data.** Any outside data is immediate disqualification.
- Must run **out of the box in a clean environment**, open-source tools only.
- Public repo, MIT licence, open-source in perpetuity.
- 1-minute YouTube video, voiced by you.

## Licence
MIT — see [`LICENSE.md`](LICENSE.md).
Data © SkillCorner, distributed under MIT at
<https://github.com/SkillCorner/opendata-basketball>. Not redistributed here.
