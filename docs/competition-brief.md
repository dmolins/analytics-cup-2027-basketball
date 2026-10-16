# Analytics Cup 2.0 — competition brief

Source: <https://pysport.org/analytics-cup/editions/analytics-cup2> (scraped 2026-10-11).
Treat this file as the single source of truth in-repo; re-check the site + Discord for amendments.

## What it is
Hackathon-style open-data competition by **SkillCorner x PySport**. Second edition
("2.0") adds a basketball dataset and splits into Europe and USA competitions.
Status as of 2026-10-11: **open**.

## Key dates
| Date | Milestone |
|---|---|
| 9 Sep 2026 | Challenge opened, registration live |
| **18 Dec 2026** | **Submission deadline** |
| 8 Jan 2027 | Finalists announced |
| 17 Feb 2027 | Europe Final — Paris, France |
| 24 Feb 2027 | USA Final — Boston, Massachusetts |

Register: <https://pysport.org/analytics-cup/editions/analytics-cup2/register> (HubSpot form)
Submit: <https://submissions.analytics-cup.org> (must be registered first)

## Format
- **No fixed tracks** (unlike 2026, which had Analyst vs Research). Any original
  analysis, research, methodology, visualisation or practical tool.
- Pick **one region** (Europe *or* USA — not both). Region is independent of your sport.
- Pick a dataset: Football or Basketball. You may submit one entry per sport, both in
  the same region.
- Entries by **1 or 2 people**. Sign-ups are individual; submission is per entry.
- Finalists must present **in person**. No remote talks. Travel not reimbursed.

## Suggested theme — Basketball: Shot Quality
> "What makes one shot better than another? Use tracking and contextual data to explore
> how player positioning, defensive pressure, movement, spacing and game context
> influence shot selection and shot quality."

Following the theme is **optional** — an original question using the dataset is allowed
and explicitly welcomed.

## Judging criteria (equal weight, 20% each)
1. **Relevance** — meaningful sporting question / real-world problem for analysts, coaches, the community.
2. **Methodology** — technically sound, transparent, appropriate for the question.
3. **Originality** — fresh idea, approach or application.
4. **Communication** — clearly presented, effective evidence and visualisation.
5. **Open-source potential** — others can reproduce, reuse, develop it further.

Reviewed by a panel from sports, data and open-source analytics (SkillCorner, PySport,
elite football and basketball organisations).

## Submission requirements (these shape the whole project)
- **YouTube video, max 1 minute**, presented and voiced by you (or your teammate).
- **Public GitHub repo** with *all* resources, files and code (data excluded), under an
  open-source licence (MIT / Apache-2.0 / similar), incl. `LICENSE.md`.
  **Must work out of the box.**
- **`README.md` of at most 1000 words, with a maximum of TWO figures or tables in
  total** (any combination), supplementing the pitch. Must document how to reproduce
  results, including running in a clean environment.
- Substantial **new work created for this competition**. Pre-existing libraries fine if
  licensed and disclosed. No resubmitting or lightly adapting old projects.
- **Only the provided SkillCorner dataset** (and/or data from prior Analytics Cups).
  Using any extra data — video, extra matches, extra tracking — is **immediate
  disqualification**.
- Reproducible **without proprietary software** (no Excel, Tableau, Power BI).
- Must remain open-source in perpetuity. SkillCorner retains dataset rights and may use
  submissions promotionally.

Disqualification also for: late submission, code that doesn't run out of the box,
plagiarism, false registration info.

## Prizes
- 6 finalists per region invited to present in Paris / Boston.
- Each selected submission: **€500 (EU) / $500 (USA)**, one per submission regardless of
  team size.
- Each **regional winner**: **€1,500 / $1,500 open-source grant**, released on completing
  an agreed deliverable (Python package, or a functional PR to an existing package).

Finalists may get extra ACB / A-League data under EULA between 8 Jan and the final, to
extend the project.

## Prior art to study (2026 edition, football)
Winner: Amar Shah — *Simulated Annealing For Positional Optimization*
(now a module in [DataballPy](https://databallpy.readthedocs.io/)) —
<https://github.com/amarshah1999/analytics_cup_research>
Finalists: Hadi Sotudeh (Positional Player Scouting), Zach Cochran (Off-Ball Run Decision
Making), Emaly Vatne (Worst-Case Running Demands), Oscar Bartolome Pato (Dynamic Skills
Finder), Antoine Verdon (SkPy Analytics Platform).
All six 1-min/finalist videos: <https://pysport.org/analytics-cup/videos>

## Suggested open-source toolkit (from the official resources page)
Data: [kloppy](https://kloppy.pysport.org/), [databallpy](https://databallpy.readthedocs.io/),
[floodlight](https://floodlight.readthedocs.io/)
Viz: [mplbasketball](https://github.com/mlsedigital/mplbasketball),
[skillcornerviz](https://github.com/SkillCorner/skillcornerviz), mplsoccer
Methods: [unravelsports](https://unravelsports.readthedocs.io/) (GNNs on tracking data),
[ML-KULeuven](https://github.com/ML-KULeuven/), [Hyunsung Kim](https://github.com/hyunsungkim-ds/)
