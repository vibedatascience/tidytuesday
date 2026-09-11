# Cross-continent links between twinned cities

![Cross-continent links between twinned cities](20260512.png)

[Python code](20260512.py) · [Source dataset](https://github.com/rfordatascience/tidytuesday/tree/main/data/2026/2026-05-12)

Collapse reciprocal/duplicate city links to unique undirected pairs; remove self-links and missing continent mappings. A cross-continent edge appears in both symmetric cells, and a within-continent edge once on the diagonal. Colours use log1p counts, labels exact counts.

Data: Wikidata / Twin Cities Explorer. Chart: vibedatascience.

Inputs (original CSV files, losslessly gzip-compressed): [cities.csv.gz](data/cities.csv.gz) · [links.csv.gz](data/links.csv.gz)
