---
name: submission-check
description: Audit this project against every Analytics Cup 2.0 submission rule before submitting — clean-environment reproducibility, licence, README word and figure limits, no-extra-data rule, video length. Use when preparing or reviewing a submission, or when asked whether the entry is compliant.
---

# Submission compliance audit

Rules live in `docs/competition-brief.md`. Any disagreement, the official site wins —
re-check it, because the organisers may amend the rules.

Work through this list and report each item as PASS / FAIL / CAN'T VERIFY with the
evidence. Do not mark anything PASS you did not actually check.

## Hard disqualifiers — check these first
1. **No external data.** Grep the repo for any URL, API call, scraped file, manual CSV or
   hard-coded number that did not come from the provided SkillCorner dataset.
   Any outside data, including video, is immediate disqualification.
2. **Runs out of the box in a clean environment.** Create a throwaway venv from a fresh
   clone, follow only the README, and run the documented command. If it needs a step the
   README omits, that is a FAIL.
3. **No proprietary software** anywhere in the pipeline.
4. **Submitted before 18 Dec 2026**, via <https://submissions.analytics-cup.org>,
   registered first.
5. **New work for this competition**, with third-party libraries disclosed and licensed.

## Repository
6. Public GitHub repo containing all code and resources except the data.
7. `LICENSE.md` present, MIT / Apache-2.0 / similar permissive.
8. Dependencies pinned; the documented install path actually resolves.
9. No data files, no secrets, no absolute paths from the author's machine committed.
10. Data acquisition documented: where the dataset comes from and how to place it.

## README — the tightest constraint
11. **At most 1000 words.** Count it: `pandoc`-free check with
    `tr -s '[:space:]' '\n' < README.md | grep -c .` or a small Python word count, and
    report the number.
12. **At most two figures or tables IN TOTAL**, any combination. Count image embeds and
    markdown tables together. Three is a FAIL.
13. Reproduction instructions sufficient for a clean environment.
14. States the question, the method, the result and the limitations. With 10 games of
    tracking, the sample-size limitation must be stated explicitly — judges will notice
    its absence faster than they will punish its presence.

## Video
15. **At most 60 seconds**, on YouTube, voiced and presented by the author or teammate.
    Check the actual duration, not the intent.

## Judging-criteria self-score
Score the entry 1-5 on each, with one line of justification and the single cheapest
improvement available for each: Relevance, Methodology, Originality, Communication,
Open-source potential.

End with the three highest-value fixes, ordered by effort-to-impact.
