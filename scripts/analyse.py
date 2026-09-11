"""Derive country summaries, preserving the published ratio-of-sums definition."""
import csv
import math
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEEK = ROOT / '2026' / '2026-09-08'


def summarise(min_cafes=10):
    groups = defaultdict(list)
    with (WEEK / 'data/cafe.csv').open() as source:
        for row in csv.DictReader(source):
            price, wage = float(row['price_gbp']), float(row['hourly_wage_gbp'])
            if not (math.isfinite(price) and math.isfinite(wage) and price > 0 and wage > 0):
                raise ValueError('Non-positive or non-finite input: review before publishing')
            groups[row['country'].replace('\xa0', ' ')].append((price, wage))
    result = []
    for country, pairs in groups.items():
        if len(pairs) < min_cafes:
            continue
        price = sum(p for p, w in pairs) / len(pairs)
        wage = sum(w for p, w in pairs) / len(pairs)
        result.append(dict(country=country, n=len(pairs), price=price, wage=wage,
                           minutes=60 * price / wage))
    for field in ['price', 'minutes']:
        for rank, row in enumerate(sorted(result, key=lambda r: (r[field], r['country'])), 1):
            row[field + '_rank'] = rank
    return sorted(result, key=lambda r: r['minutes'])


def validate_published(rows):
    with (WEEK / 'data/cappuccino_index.csv').open() as source:
        published = {r['country'].replace('\xa0', ' '): r for r in csv.DictReader(source)}
    for row in rows:
        other = published[row['country']]
        assert math.isclose(row['minutes'], float(other['index']), rel_tol=1e-10), row['country']
        assert row['n'] == int(other['n']), row['country']


if __name__ == '__main__':
    rows = summarise()
    validate_published(rows)
    print(f'Validated {len(rows)} countries with at least 10 cafés against published index.')
