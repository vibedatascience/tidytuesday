"""Generate the gallery and pilot edition from validated summaries and metadata."""
import html
import json
from pathlib import Path
from analyse import ROOT

DOCS = ROOT / 'docs'
REPO = 'https://github.com/vibedatascience/tidytuesday'
esc = html.escape


def shell(title, description, content, prefix='', script=''):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · TidyTuesday 2026</title><meta name="description" content="{esc(description)}">
<meta name="theme-color" content="#f4f0e7"><link rel="stylesheet" href="{prefix}assets/site.css">
<link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml"></head>
<body><a class="skip" href="#main">Skip to content</a><div class="wrap">
<header class="top"><a class="brand" href="{prefix}index.html"><span>t</span>TidyTuesday 2026.</a>
<nav aria-label="Main navigation"><a href="{prefix}index.html#collection">Collection</a><a href="{REPO}">GitHub ↗</a></nav></header>
{content}
<footer class="footer"><span>vibedatascience / 2026</span><span>Original TidyTuesday visualisations.</span><a href="{REPO}">Data &amp; code ↗</a></footer>
</div>{script}</body></html>'''


def index(editions):
    cards=[]
    for e in sorted(editions,key=lambda e:e['date'],reverse=True):
        url=f"2026/{e['date']}/"
        cards.append(f'''<article class="issue"><div class="issue-copy"><span class="eyebrow">Week {e['week']:02d} / {esc(e['date'])}</span>
<h2>{esc(e['title'])}</h2><p>{esc(e['summary'])}</p><a class="link-button" href="{url}">Explore the story <span aria-hidden="true">↗</span></a>
<div class="issue-meta">{''.join('<span class="pill">'+esc(t)+'</span>' for t in e['tags'])}</div></div>
<a class="issue-cover" href="{url}" aria-label="Open {esc(e['title'])}"><img src="{url}{e['selected']}.svg" width="1800" height="2160" alt="Country rankings cross between coffee price and minutes of barista pay."></a></article>''')
    body=f'''<main id="main"><section class="hero"><div><p class="eyebrow">A visual journal / TidyTuesday 2026</p><h1>TidyTuesday<br><em>2026.</em></h1></div>
<div class="intro"><p>Original data visualisations by vibedatascience, using the weekly TidyTuesday datasets.</p><p class="small">Explore the charts, source data and code for each week.</p></div></section>
<section id="collection" aria-labelledby="collection-title"><div class="rule"><h2 class="eyebrow" id="collection-title">The collection</h2><span class="small">{len(editions):02d} published {'edition' if len(editions)==1 else 'editions'} / 2026</span></div>{''.join(cards)}</section>
<section class="note"><h2>About this collection</h2><p>Each week includes an analysis of the data and a comparison of several chart designs. The selected plot is published with the alternatives, methods, source data and reproducible code.</p></section></main>'''
    (DOCS/'index.html').write_text(shell('Original data visualisations','A personal collection of original TidyTuesday visualisations by vibedatascience.',body))


def pilot(edition):
    path=DOCS/'2026'/'2026-09-08'
    rows=json.loads((path/'summary.json').read_text())
    india=next(r for r in rows if r['country']=='India')
    table_rows=''.join(f"<tr><td>{esc(r['country'])}</td><td>£{r['price']:.2f}</td><td>£{r['wage']:.2f}</td><td>{r['minutes']:.1f}</td><td>{r['n']}</td></tr>" for r in rows)
    options=''.join(f'<option value="{esc(r["country"])}" {"selected" if r["country"]=="India" else ""}>{esc(r["country"])}</option>' for r in sorted(rows,key=lambda r:r['country']))
    candidates=[('01-rank-crossings','01 / Selected','Rank crossings','Best for the story: the reversal between menu price and earning time is visible at a glance. Ranks show order; the table gives the actual amounts.'),('02-time-ledger','02 / Alternative','Time ledger','Best for comparing exact magnitudes. A single linear scale shows the gap across all 36 countries, but loses the price-versus-pay reversal.'),('03-shared-clocks','03 / Alternative','Shared clocks','Best for a quick read. Eight country panels pair the price with the time; easier to scan, but less complete than the full comparison.')]
    alternatives=''.join(f'''<article class="candidate"><a href="{slug}.svg" aria-label="Open full-size {title}"><img src="{slug}.svg" loading="lazy" width="1800" height="2160" alt="{title}: {esc(desc)}"></a><p class="eyebrow">{label}</p><h3>{title}</h3><p>{esc(desc)}</p><a class="download" href="{slug}.png" download>Download PNG ↓</a></article>''' for slug,label,title,desc in candidates)
    refs=''.join(f'<li><a href="{esc(r["url"])}">{esc(r["title"])} · {r["date"]}</a><br>{esc(r["signal"])}</li>' for r in edition['references'])
    body=f'''<main id="main"><header class="article-head"><p class="eyebrow">Edition 01 / Week 36 / 08 September 2026</p>
<h1>A cappuccino takes longer to earn<br>in India than in Switzerland.</h1><p class="dek">In the sampled cafés, a cappuccino costs £1.96 on average in India and £5.41 in Switzerland. Relative to reported barista pay, it takes 172 minutes to earn in India and 14 minutes in Switzerland.</p>
<div class="article-meta"><span>The Cappuccino Index</span><span>36 countries with ≥10 cafés</span><a href="#data">Explore the numbers ↓</a><a href="#studies">Three ways of seeing it ↓</a></div></header>
<div class="story"><figure class="poster"><a href="01-rank-crossings.svg" aria-label="Open the full-size rank comparison"><picture><source media="(max-width: 700px)" srcset="01-rank-crossings-mobile.svg"><img src="01-rank-crossings.svg" width="1800" height="2160" alt="Ranks among 36 countries: India moves from third cheapest cup to longest earning time; Switzerland from 35th cheapest to fourth shortest earning time. Australia has the shortest earning time."></picture></a><figcaption><span>Follow a country from left to right.</span><a href="01-rank-crossings.png" download>Download PNG ↓</a><a href="01-rank-crossings.svg">Full-size SVG ↗</a></figcaption></figure>
<aside class="side" aria-label="Read the chart"><p class="eyebrow">Behind the crossing lines</p><h2>Comparing price<br>with hourly pay.</h2><p>At the sampled cafés, an average cup in India costs about £1.96. In Switzerland, it costs £5.41. Relative to the reported barista wages, the Indian cup takes much longer to earn.</p><p>Every line is a country. The left side ranks mean prices in pounds; the right ranks minutes of pay. Higher up means cheaper or quicker. The lines connect two measures—not change over time.</p>
<label for="country">Look closer at a country</label><select id="country">{options}</select><div class="country-detail" aria-live="polite"><h3 id="country-name">India</h3><div class="metric"><div><span>MEAN CUP PRICE</span><strong id="cup-price">£1.96</strong><span id="price-rank">Price rank 3 of 36</span></div><div><span>TIME TO EARN IT</span><strong id="work-time">172.2 min</strong><span id="time-rank">Time rank 36 of 36</span></div></div><p id="country-note">11 cafés · Mean hourly pay £0.68, excluding tips.</p></div>
<p class="small">These are voluntary café responses, not a representative country survey. The ≥10 café threshold removes the smallest samples; it does not make the remaining estimates representative.</p><a href="#method">How this was calculated ↓</a></aside></div>
<section class="section" id="studies"><div class="section-title"><h2>Three chart designs.</h2><p>Compare the alternatives.</p></div><div class="candidates">{alternatives}</div></section>
<section class="section" id="data"><div class="section-title"><h2>Country-level data.</h2><a href="summary.csv" download>Download summary CSV ↓</a></div><p class="small">All 36 countries shown in the chart. Prices and wages are means in GBP; the index uses their ratio.</p>
<div class="table-controls"><label for="country-search">Find a country</label><input id="country-search" type="search" placeholder="e.g. Australia"><label for="sort">Sort by</label><select id="sort"><option value="minutes">Shortest earning time</option><option value="price">Lowest cup price</option><option value="n">Most café responses</option><option value="country">Country name</option></select></div>
<div class="table-scroll" tabindex="0" role="region" aria-label="Country data; scroll horizontally on small screens"><table><caption class="small">Mean cup price, mean hourly pay, earning time and sample size</caption><thead><tr><th scope="col">Country</th><th scope="col">Cup price</th><th scope="col">Hourly pay</th><th scope="col">Minutes / cup</th><th scope="col">Cafés</th></tr></thead><tbody id="countries">{table_rows}</tbody></table></div><p id="table-status" role="status">36 of 36 countries</p></section>
<section class="section" id="method"><div class="section-title"><h2>Sources &amp; decisions.</h2><a href="{REPO}/blob/main/scripts/render.py">Read the plotting code ↗</a></div><div class="method"><div><h3>What the index measures</h3><p><code>Minutes = 60 × sum(cup prices) ÷ sum(hourly wages)</code></p><p>This reproduces the published Cappuccino Index. It is a ratio of country-level sums, not the average of individual cafés’ price-to-wage ratios. All 36 results were checked against the published values.</p><p>The full dataset has 2,594 cafés across 87 countries. This edition uses the 36 countries with at least 10 responses. The input prices and wages were positive and complete. Tips are excluded, which matters when comparing pay.</p><p>Ranks use unrounded values; display values are rounded. GBP conversion makes menu prices comparable in one currency, but is not a purchasing-power adjustment. No national estimates or confidence intervals are claimed.</p><p>Data: <a href="https://github.com/rfordatascience/tidytuesday/tree/main/data/2026/2026-09-08">TidyTuesday, 8 September 2026</a>, curated by Filip Reierson from <a href="https://www.youtube.com/watch?v=WtlE3BW9Nqs">James Hoffmann’s Cappuccino Index</a>.</p></div>
<div><h3>Design references, from other weeks</h3><p>Nicola Rennie’s earlier work provided useful design signals. These charts use new code, a new palette, and this week’s data.</p><ul>{refs}</ul><p>The rank comparison is our editorial choice for this story. The alternatives remain available so you can judge that choice. References: Nicola Rennie, <a href="https://github.com/nrennie/tidytuesday">nrennie/tidytuesday</a> (<a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>).</p></div></div></section></main>'''
    data=json.dumps(rows).replace('<','\\u003c')
    script=f'<script id="country-data" type="application/json">{data}</script><script src="../../assets/edition.js"></script>'
    (path/'index.html').write_text(shell(edition['title'],edition['summary'],body,'../../',script))


def main():
    editions=json.loads((ROOT/'editions.json').read_text())
    for e in editions:
        assert all(r['date'] != e['date'] for r in e['references']), 'Use references from other weeks'
    index(editions)
    pilot(next(e for e in editions if e['date']=='2026-09-08'))
    (DOCS/'.nojekyll').touch()
    print('Built gallery and edition pages.')


if __name__ == '__main__':main()
