# Working agreement for this repo

## Context
Entry for the **SkillCorner x PySport Analytics Cup 2.0**, basketball track
(ACB 2025/26 broadcast tracking data). Hard deadline **18 Dec 2026**.
Full rules, dates and judging criteria: `docs/competition-brief.md`.
Dataset conventions and known traps: `docs/data-notes.md`.
Idea backlog and the current pick: `docs/ideas.md`.
Running decision log: `notes/journal.md`.

## Who I am
A basketball coach. I know the game deeply and I have read basketball analytics, but I
have never done an analytics job. Strong SQL, light Python. The goal of this project is
as much **learning** as winning.

So:
- **Teach while you build.** When you introduce a method, say in two or three sentences
  what it does, what it assumes, and how it could mislead me. Name the technique so I can
  go read about it.
- **Don't hand me a black box.** I need to be able to defend every number in a 1-minute
  video and a 1000-word README. If I can't explain it, it doesn't ship.
- **Prefer SQL where SQL fits.** Use DuckDB over the event JSON and the aggregate CSVs so
  I can read and modify the logic myself. Reserve Python for tracking geometry, smoothing
  and plots.
- **Ask me basketball questions.** If a definition needs a coaching judgement (what counts
  as beaten, what counts as a good closeout), ask instead of guessing. That judgement is
  the edge of this project.
- Short, concrete explanations. No filler, no restating my own question back to me.

## Non-negotiable competition constraints
- **No data outside the provided SkillCorner dataset.** No scraping, no extra games, no
  video, no box scores from elsewhere. This is immediate disqualification — flag it if
  anything we do drifts toward it.
- Everything must run **in a clean environment, out of the box**, with open-source tools
  only. No Excel, no Tableau. Pin dependencies.
- Code is public and MIT-licensed. Write it as if a stranger will reuse it, because the
  grant depends on exactly that.
- The final README is capped at **1000 words and two figures/tables total**. Every chart
  we make is a candidate for one of two slots — keep `outputs/figures/` curated and tell
  me when a figure is good enough to be one of the two.

## Repo conventions
```
data/raw/        # gitignored. The cloned SkillCorner repo lives here.
data/interim/    # gitignored. Parquet/DuckDB built by scripts, always reproducible.
src/acb/         # importable library code. Anything used twice goes here.
notebooks/       # exploration only. Numbered. Never the source of a final number.
sql/             # DuckDB queries, one file per question.
outputs/figures/ # curated plots
docs/            # the brief, data notes, ideas
notes/journal.md # dated decision log — append, never rewrite
```
- Every number that reaches the README must come from a script in `src/` or `sql/`, run
  end to end from raw data. Notebook-only results don't count.
- Any derived table in `data/interim/` must be rebuildable with one documented command.
- Use the `research-log` skill after any session that produced a finding or killed an
  idea. The journal is what makes the README writable in December.

## Visualisation
Load the `dataviz` skill before writing chart code, and the local `court-viz` skill for
anything drawn on a court. Court coordinates are **feet, origin at centre court**.
