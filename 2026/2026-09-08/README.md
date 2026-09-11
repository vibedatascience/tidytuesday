# The Cappuccino Index

![Country rankings by cappuccino price and minutes of barista pay](20260908.png)

[Plotting code](20260908.py) · [TidyTuesday data](https://github.com/rfordatascience/tidytuesday/tree/main/data/2026/2026-09-08)

The chart compares mean cup-price ranks with earning-time ranks for the 36 countries with at least 10 café responses. Minutes per cup = `60 × sum(prices) / sum(hourly wages)`. The script checks all 87 country indices against the published data before plotting.

The data are voluntary café responses, not representative national estimates. Tips are excluded. Rank gaps show order, not differences in magnitude.

Data: James Hoffmann; curated for TidyTuesday by Filip Reierson. Design inspiration: Nicola Rennie's [2024-07-16 football rankings](https://github.com/nrennie/tidytuesday/tree/main/2024/2024-07-16), using direct labels and selective colour ([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)). Original chart and code by vibedatascience.
