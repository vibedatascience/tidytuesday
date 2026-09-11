import csv
import json
import math
import sys
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from analyse import summarise, validate_published, WEEK


class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.ids=set()
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if 'id' in attrs:self.ids.add(attrs['id'])
        for key in ['href','src']:
            if key in attrs:self.links.append(attrs[key])


class EditionTests(unittest.TestCase):
    def test_reproduces_every_published_country_index(self):
        all_rows=summarise(min_cafes=1)
        self.assertEqual(len(all_rows),87)
        self.assertEqual(sum(r['n'] for r in all_rows),2594)
        validate_published(all_rows)

    def test_inclusion_threshold_and_ranks(self):
        rows=summarise()
        self.assertEqual(len(rows),36)
        self.assertEqual(sum(r['n'] for r in rows),2451)
        self.assertTrue(all(r['n']>=10 for r in rows))
        for field in ['price_rank','minutes_rank']:
            self.assertEqual(sorted(r[field] for r in rows),list(range(1,37)))
        india=next(r for r in rows if r['country']=='India')
        swiss=next(r for r in rows if r['country']=='Switzerland')
        self.assertEqual((india['price_rank'],india['minutes_rank']),(3,36))
        self.assertEqual((swiss['price_rank'],swiss['minutes_rank']),(35,4))

    def test_ratio_of_sums_not_mean_individual_ratios(self):
        with (WEEK/'data/cafe.csv').open() as f:
            cafes=[r for r in csv.DictReader(f) if r['country']=='India']
        expected=60*sum(float(r['price_gbp']) for r in cafes)/sum(float(r['hourly_wage_gbp']) for r in cafes)
        naive=sum(60*float(r['price_gbp'])/float(r['hourly_wage_gbp']) for r in cafes)/len(cafes)
        value=next(r for r in summarise() if r['country']=='India')['minutes']
        self.assertAlmostEqual(value,expected)
        self.assertFalse(math.isclose(value,naive,rel_tol=.001))

    def test_published_summary_matches_computation(self):
        expected=summarise()
        for file in [WEEK/'summary.json', ROOT/'docs/2026/2026-09-08/summary.json']:
            self.assertEqual(json.loads(file.read_text()),expected)

    def test_design_references_are_other_weeks(self):
        for e in json.loads((ROOT/'editions.json').read_text()):
            self.assertEqual(len(e['references']),3)
            self.assertTrue(all(r['date']!=e['date'] for r in e['references']))
            self.assertTrue((ROOT/'docs/2026'/e['date']/(e['selected']+'.svg')).exists())

    def test_all_site_links_assets_and_fragments_resolve(self):
        for file in (ROOT/'docs').rglob('*.html'):
            parser=Links();parser.feed(file.read_text())
            for value in parser.links:
                url=urlsplit(value)
                if url.scheme or url.netloc:continue
                target=(file.parent/unquote(url.path)).resolve() if url.path else file
                if target.is_dir():target=target/'index.html'
                self.assertTrue(target.is_file(),f'{file}: {value}')
                if url.fragment and target.suffix=='.html':
                    other=Links();other.feed(target.read_text())
                    self.assertIn(url.fragment,other.ids,f'{file}: {value}')


if __name__=='__main__':unittest.main()
