# TidyTuesday 2026

Original TidyTuesday data visualisations by **vibedatascience**.

**Website:** https://vibedatascience.github.io/tidytuesday/

Each edition explores several visual directions, then selects the strongest for its particular story. Nicola Rennie's work from **other weeks** is a design reference library: useful signals about comparison, annotation, typography and visual emphasis. The plots and implementation here are original.

## First edition

[2026-09-08 — The Cappuccino Index](https://vibedatascience.github.io/tidytuesday/2026/2026-09-08/): **A cappuccino takes longer to earn in India than in Switzerland**

Three candidates: rank crossings (selected), a ranked time ledger, and shared-scale country panels. The page includes all three, a country explorer, a searchable table, downloadable SVG/PNG charts, and the calculation and source notes. See [the editorial review](2026/2026-09-08/README.md).

This is the first published edition, not a completed 2026 archive. New editions appear in the gallery when added to `editions.json` and published. There is no unattended plot-generation service or weekly agent running.

## Reproduce

Python 3.9 or later:

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/render.py
.venv/bin/python scripts/build_site.py
.venv/bin/python -m unittest discover -s tests -v
python3 -m http.server 8766 --directory docs
```

Open http://localhost:8766. Input CSV files are versioned, so rebuilding never silently switches to a different upstream dataset. The website has no frontend framework, remote script dependency, API token, or analytics.

GitHub Pages publishes the committed `docs/` directory from `main`. Run the reproduction commands and checks before pushing changes. GitHub Actions is currently disabled at the account level, so builds and tests are local; publication does not automatically generate new plots. An optional build-and-deploy workflow is included for later use. To use it after Actions is enabled, change the Pages source to GitHub Actions. Pull requests will then run the same build and tests without publishing.

## Workflow for the next week

1. Create `2026/YYYY-MM-DD/` with the official data, source URLs, and dataset notes. Record the date and hashes of downloaded files.
2. Explore distributions, sample sizes, missingness, definitions and outliers before writing a headline. Identify several possible stories. Use direct, factual headlines that state the finding or name the comparison. Avoid puns, slogans, teaser questions and clever contrasts; this is an explicit user preference.
3. Find at least three useful precedents in [nrennie/tidytuesday](https://github.com/nrennie/tidytuesday) from dates **other than this week's dataset**. Her [catalogue](https://raw.githubusercontent.com/nrennie/tidytuesday/main/data/all_weeks.csv) contains titles, packages and source paths. Read the relevant source; package names alone do not establish the visual style. Document the exact useful signal and why it transfers.
4. Produce three materially different candidates. Use independent code, accurate scales, a coherent personal palette, clear labels and relevant source/inspiration credits.
5. Compare accuracy, insight, readability, visual hierarchy, accessibility and completeness. Record a reasoned editorial choice; do not invent popularity scores or call a subjective choice objectively best.
6. Build an edition page with the selected graphic, readable numbers, methods, code and downloads. Review real rendered outputs on desktop and mobile. Verify any interactions and links.
7. Add the published edition to `editions.json`. The gallery builder lists entries newest first. Extend the renderer and edition builder for the new dataset; the pilot's layout is not a universal chart template.
8. Run the checks, publish, and verify the live page.

User feedback should shape subsequent editions. The goal is a recognisable body of work, with chart forms chosen for the data rather than forcing every week into the same layout.

## Sources and credit

- Datasets: [TidyTuesday / Data Science Learning Community](https://github.com/rfordatascience/tidytuesday), with individual original sources credited per edition.
- First edition: James Hoffmann's Cappuccino Index; curated for TidyTuesday by Filip Reierson. Upstream dataset notes are retained in `2026/2026-09-08/data/readme.md`.
- Design references: Nicola Rennie, [nrennie/tidytuesday](https://github.com/nrennie/tidytuesday), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). No Nicola Rennie plot images are republished here.
