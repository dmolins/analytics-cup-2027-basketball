# Idea backlog

> **Current pick (2026-10-11): A — Advantage ledger.** David's instinct as a coach.
> Highest risk/reward on this list — the definitions *are* the project, so weeks 1-2 are
> about nailing "created / kept / lost" against real animated possessions before any
> metric gets built. Idea C (action chains) stays as the fallback if the definitions
> don't converge by ~10 Nov.

Scored 1-5 against the five judging criteria (Relevance, Methodology-feasibility,
Originality, Communication, Open-source potential). Feasibility here means "can one
person with 10 games of tracking actually land this by 18 Dec".

**Decide by one test:** can you pitch it to a head coach in 60 seconds and have them
want the output? That is literally the submission format (1-min video, 1000-word README,
two figures). If it takes three minutes to explain, it is the wrong project.

---

## The strategic read

The organisers named **Shot Quality** as the basketball theme, so a large share of
entries will be "xFG model from tracking features". That is the crowded lane, and it is
also the lane where a first-time analyst competes directly against people who have built
xG/xFG models for years. Two better-positioned shapes:

1. **Stay in the theme but change the unit of analysis.** Not "how good is this shot" but
   "what *produced* this shot" — the action chain, the advantage, the defensive mistake.
   Still answers the theme, judged as original.
2. **Use the coaching edge.** You know what coaches actually argue about on Monday
   morning. The dataset has event families almost nobody in public analytics has touched
   — `closeouts`, `off_ball_screens`, `matchups`, `handoffs`, `posts`, `isolations`.
   A metric that a coach recognises as *their* concept, formalised from tracking, scores
   on Relevance and Originality at once.

Your weakness is methodology depth. Counter it by choosing something **interpretable**
(geometry, timing, counting, simple models with clear assumptions) and **validating it
visibly** — not by reaching for a neural net.

---

## A. Advantage ledger (coach-native, theme-adjacent)
Spanish basketball talks about *ventaja*: an advantage is created, kept or lost, then
finished. Nobody has a public tracking metric for it.

Define, from tracking + events: an **advantage is created** when the ball-handler's
primary defender is beaten (distance/angle thresholds) or two defenders commit to one
player; **kept** when the next pass arrives before the defence re-forms (rotation
latency); **lost** when the defence recovers to a set shell. Then measure what each
chance's shot quality looks like as a function of advantage state at release.

Output: per-team and per-player "advantage created / kept / finished" rates, plus the
EV cost of killing an advantage.
*Relevance 5 · Feasibility 3 · Originality 5 · Communication 4 · OSS 4*
Risk: definitions are the whole project. Spend the first week only on the definition and
eyeball it against video-free animations of real possessions.

## B. Closeout quality (defensive, under-studied, data is ready-made)
There is a `closeouts` event family with defender identity and distance. Coaches teach
closeouts every single day and have no numbers for them.

Measure: defender distance and closing speed at the catch vs. at the release, whether
the closeout conceded a drive-by, and the resulting points per chance. Build a
"closeout grade" and a per-player defensive profile (too slow / too hot / out of control).
*Relevance 5 · Feasibility 4 · Originality 5 · Communication 5 · OSS 4*
Why it's strong: the aggregates are offence-only, so **defensive work is automatically
differentiated**, and the 10 games carry defensive context. Easiest big win here.

## C. Which actions manufacture good shots
Chain `picks` / `off_ball_screens` / `handoffs` / `drives` / `isolations` → `shots`
through `chanceId`. For each action type and each defensive coverage (the data has
coverage type), what is the shot quality distribution that follows?

Output: an action-by-coverage matrix a coach can use for game prep — "against drop
coverage, their PnR produces X; against switch, Y".
*Relevance 5 · Feasibility 5 · Originality 3 · Communication 5 · OSS 4*
Lowest-risk project in the list. Good fallback if A or B stalls. Needs an original
twist to avoid being a dashboard anyone could make.

## D. Spacing and gravity
Court geometry per frame: convex hull of the four off-ball attackers, nearest-defender
distance distribution, how far help defenders sit off their assignment. Who bends the
defence, and does their gravity actually raise teammates' shot quality?
*Relevance 4 · Feasibility 4 · Originality 3 · Communication 5 · OSS 5*
Very visual, very explainable; the gravity idea exists in NBA work, so lean on the
*ACB* angle and on a clean reusable spacing library.

## E. Rotation latency / help-side timing
How long does the defence take to re-form after the ball moves? Per team, per player,
per situation. "Late by 0.4 s" is a number coaches will instantly use.
*Relevance 5 · Feasibility 3 · Originality 5 · Communication 4 · OSS 4*
Hardest geometry of the list; strong if you pull it off. Overlaps with A.

## F. Shot diet tool on the 293-game aggregates
An interactive, open-source profiling tool over the season aggregates: each player's shot
mix by zone / contest / coverage vs. league baseline, with similarity search.
*Relevance 4 · Feasibility 5 · Originality 2 · Communication 5 · OSS 5*
Fast and safe, but closest to "a dashboard". Best used as a **companion** to A/B/C —
it gives your tracking finding season-scale context, which is the bridge almost no one
will build.

## G. Rebounding position: crash vs. retreat
Positions at release → rebound outcome + transition exposure. Quantify the trade-off a
coach makes every possession.
*Relevance 4 · Feasibility 3 · Originality 4 · Communication 4 · OSS 3*
Rebound events exist but the tracking around them is where the error is worst (bodies
overlap, broadcast cuts). Validate feasibility on one game before committing.

---

## Shortlist recommendation
Spend week 1 on **B (closeouts)** and **A (advantage)** in parallel as throwaway
exploration, then commit to one by ~1 Nov. Keep **C** as the safety net — it can be
rescued into a submission in a week if needed. Carry **F** as the season-scale validation
layer for whichever you pick.

## Log decisions in `notes/journal.md`
Every killed idea is README material: "we tried X, it failed because Y" is exactly the
transparency the Methodology criterion rewards.
