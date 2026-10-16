---
name: court-viz
description: Draw basketball courts, shot maps, player positions, spacing diagrams and possession animations for this project. Use before writing any plot that puts something on a court, and alongside the dataviz skill for charts generally.
---

# Court visualisation for this project

Load the global `dataviz` skill too — this skill only covers what is court-specific.

## Court geometry
- Data is in **feet, origin at centre court**. Do not rescale to a 0-94 frame without
  saying so in the code; half the bugs in court plots are a silent coordinate flip.
- FIBA court (ACB), not NBA: 28 x 15 m ≈ **91.9 x 49.2 ft**, three-point arc 6.75 m
  ≈ 22.15 ft (6.60 m ≈ 21.65 ft in the corners), no NBA restricted-area arc.
  Using an NBA court outline on ACB data is a visible, credibility-costing error —
  check `mplbasketball`'s court options for a FIBA layout, or draw the lines yourself
  from FIBA dimensions.
- Pool possessions by mirroring to a single attacking half before any shot map.

## Defaults
- `mplbasketball` for the court; matplotlib for everything else. Static SVG or PNG.
- Court lines are **background**: thin, low-contrast grey. The data is the only thing
  that gets colour.
- Hexbin or smoothed density over raw scatter once there are more than ~300 shots; raw
  scatter is fine and more honest below that.
- Diverging colour only for genuinely signed quantities (above/below expectation), with
  zero pinned to the neutral midpoint. Sequential otherwise.
- Always put **n** on the figure. With 10 games, sample size is the first thing a judge
  will ask about, so answer it before they ask.
- Label the orientation and the units once per figure. A reader must know which way the
  offence attacks.

## Animations
Possession animations are the fastest way to validate that an event definition matches
what actually happened on court. Build them early and watch them — a definition that
looks right in a table and wrong in an animation is wrong.
Render at 25 fps or decimate to 10 fps for size; keep clips under 15 seconds.

## The two-figure rule
The final README allows **two figures or tables in total**. Treat `outputs/figures/` as a
shortlist, and when a figure is strong enough to be one of the two, say so and explain
what it costs to include it.
