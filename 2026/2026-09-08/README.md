# A cappuccino takes longer to earn in India than in Switzerland

TidyTuesday week 36: The Cappuccino Index. First edition of TidyTuesday 2026

## Finding

Among the 36 countries with at least 10 café responses, India ranks third cheapest by mean cup price but last by earning time. Switzerland ranks 35th cheapest by price but fourth shortest by earning time. In this sample, converting a menu price into minutes of reported barista pay changes the story substantially.

The original inputs contain 2,594 café responses in 87 countries. The 36-country comparison retains 2,451 responses. All records have positive, finite GBP prices and wages. Country labels normalise nonbreaking spaces; observations are not dropped or deduplicated.

## Calculation

The published index is `60 * sum(price_gbp) / sum(hourly_wage_gbp)` within each country. This equals the ratio of mean price to mean wage, multiplied by 60. It is **not** the mean of individual café ratios. `scripts/analyse.py` reproduces all 87 published indices and their sample counts. Ranks use unrounded values among the 36 included countries; presentation values are rounded.

The threshold of 10 is an editorial filter to avoid ranking countries based on one or two responses. It is not a statistical guarantee. The voluntary sample is not nationally representative; tips are excluded. The countries with the most responses are the USA (600) and UK (595). Prices in GBP are not adjusted for purchasing power. Do not interpret the line crossings as changes over time or the vertical rank gaps as differences in magnitude.

## Candidate review

| Candidate | Reference signal from another week | Strength | Limitation | Decision |
| --- | --- | --- | --- | --- |
| Rank crossings | [2024-07-16 football standings](https://github.com/nrennie/tidytuesday/tree/main/2024/2024-07-16): directly labelled ranks and focal colour against muted context | Reveals the reversal between two rankings; foregrounds a specific, verified story | Rank distances do not convey price/time differences; only four countries labelled on the poster | Selected, with exact-value explorer and full table |
| Time ledger | [2025-03-11 Pixar](https://github.com/nrennie/tidytuesday/tree/main/2025/2025-03-11): aligned horizontal comparisons and an explanatory headline | All 36 countries, linear minutes scale and sample counts | Concentration near the low end; the menu-price reversal disappears | Keep as an alternative |
| Shared clocks | [2026-04-21 health spending](https://github.com/nrennie/tidytuesday/tree/main/2026/2026-04-21): repeated country panels and a consistent encoding | Quick scan with price, wage and time together | Only eight illustrative countries; omits most of the comparison | Keep as an alternative |

The references were studied through their source code. This is an independent implementation in Matplotlib, not a port of those scripts. The shared-clocks candidate borrows the repeated-panel principle, not the health plot's geographic grid or time series. The new palette and serif-led layout belong to this collection. No design from Nicola's 2026-09-08 plot is used.

The winner is an editorial choice for this story. Selection considered correctness, how clearly the reversal appears, direct labelling, ability to inspect exact values, and legibility. The publication includes all three candidates so the tradeoffs remain reviewable.

## Files

- `data/`: original official CSV files and dataset notes.
- `sources.json`: source URLs, retrieval metadata and SHA-256 hashes.
- `summary.csv` / `summary.json`: 36-country derived summaries.
- `plots/`: three original figures, each in SVG and PNG.
- `../../scripts/analyse.py`: definitions and validation.
- `../../scripts/render.py`: complete plotting code.

Credit: James Hoffmann (original data), Filip Reierson (TidyTuesday curation), Nicola Rennie (design references from other weeks, CC BY 4.0), vibedatascience (analysis, original figures and website).
