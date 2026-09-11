# Where seabirds were recorded at sea

![Where seabirds were recorded at sea](20260414.png)

[Python code](20260414.py) · [Source dataset](https://github.com/rfordatascience/tidytuesday/tree/main/data/2026/2026-04-14)

Join bird-record counts to unique ship record IDs. Convert unsigned west longitudes to degrees east across the dateline. Show survey positions, not abundance; circle area uses sqrt(record count). No coastlines or remote images are used.

Data: At-Sea Observations of Seabirds, New Zealand. Chart: vibedatascience.

Inputs (original CSV files, losslessly gzip-compressed): [birds.csv.gz](data/birds.csv.gz) · [ships.csv.gz](data/ships.csv.gz)
