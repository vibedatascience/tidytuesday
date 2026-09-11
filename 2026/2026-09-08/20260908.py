"""TidyTuesday 2026-09-08: cappuccino prices and barista pay.

Run this script to validate the source data and reproduce 20260908.png.
Design reference: nrennie/tidytuesday, 2024-07-16 (football rankings).
"""
import csv
import math
from collections import defaultdict
from pathlib import Path

WEEK = Path(__file__).resolve().parent


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



import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.path import Path as MPath
from matplotlib.patches import PathPatch

PAPER = '#f4f0e7'
INK = '#202827'
MUTED = '#72756c'
LINE = '#d3d1c6'
BLUE = '#314daa'
RUST = '#bb4e35'
GOLD = '#897037'
TEAL = '#277b77'
COLORS = {'India': RUST, 'Switzerland': BLUE, 'Australia': TEAL, 'Philippines': GOLD}
plt.rcParams.update({'font.family': 'DejaVu Sans', 'text.color': INK,
                     'axes.labelcolor': INK, 'xtick.color': MUTED, 'ytick.color': MUTED,
                     'svg.fonttype': 'path', 'svg.hashsalt': 'tidytuesday-2026',
                     'savefig.facecolor': PAPER})


def canvas(title, subtitle, height=12):
    fig = plt.figure(figsize=(10, height), facecolor=PAPER)
    fig.text(.075, .958, 'VIBEDATASCIENCE     /     TIDYTUESDAY 2026', size=9, weight='bold', color=BLUE)
    fig.text(.925, .958, 'NO. 36', ha='right', size=9, color=MUTED)
    fig.text(.075, .91, title, size=34, fontfamily='DejaVu Serif', va='top', linespacing=1.06)
    fig.text(.075, .804, subtitle, size=10, va='top', linespacing=1.6)
    fig.text(.075, .032, 'Data: James Hoffmann · TidyTuesday, 08 Sep 2026. Tips excluded. Voluntary café sample.\nOriginal graphic: vibedatascience. Design references and methodology in the repository.',
             size=7, linespacing=1.6, color=MUTED)
    return fig


def save(fig):
    fig.savefig(WEEK / '20260908.png', dpi=180, metadata={'Software': 'Matplotlib'})
    plt.close(fig)


def rank_crossings(rows):
    fig = canvas('A cappuccino takes longer to earn\nin India than in Switzerland',
        'India has the third-lowest mean cup price in this sample—but the longest work time.\nSwiss cafés report a higher mean cup price, but a shorter earning time.')
    ax = fig.add_axes([.30, .135, .40, .55], facecolor=PAPER)
    ax.set_xlim(-.03, 1.03); ax.set_ylim(37, 0); ax.axis('off')
    for x in [0,1]:
        ax.plot([x,x],[1,36],color=LINE,lw=1)
        for rank in [1,10,20,30,36]:
            ax.text(x + (.025 if x == 0 else -.025),rank,str(rank),size=7,color=MUTED,
                    ha='left' if x==0 else 'right',va='center')
    for row in sorted(rows, key=lambda r: r['country'] in COLORS):
        a,b = row['price_rank'],row['minutes_rank']
        color = COLORS.get(row['country'],LINE)
        verts = [(0,a),(.38,a),(.62,b),(1,b)]
        patch = PathPatch(MPath(verts,[MPath.MOVETO,MPath.CURVE4,MPath.CURVE4,MPath.CURVE4]),
                          facecolor='none',edgecolor=color,lw=2.5 if row['country'] in COLORS else .8,
                          alpha=1 if row['country'] in COLORS else .7)
        ax.add_patch(patch)
        if row['country'] in COLORS:
            ax.scatter([0,1],[a,b],s=38,c=color,zorder=4,edgecolors=PAPER,linewidths=1)
            ax.text(-.07,a,f"{row['country']}  £{row['price']:.2f}",ha='right',va='center',size=9,color=color,weight='bold')
            ax.text(1.07,b,f"{row['country']}  {row['minutes']:.1f} min",ha='left',va='center',size=9,color=color,weight='bold')
    fig.text(.075,.73,'MENU PRICE',size=10,weight='bold')
    fig.text(.075,.708,'Mean small cappuccino, GBP\nCheapest at the top',size=8,color=MUTED,linespacing=1.6)
    fig.text(.925,.73,'TIME TO EARN A CUP',size=10,weight='bold',ha='right')
    fig.text(.925,.708,'Price relative to barista pay\nShortest time at the top',size=8,color=MUTED,ha='right',linespacing=1.6)
    fig.text(.075,.095,'Each line is one country. Ranks among 36 countries with ≥10 cafés; highlighted: Australia n=171,\nSwitzerland n=18, Philippines n=11, India n=11. Rank gaps are not proportional to price or time.',
             size=8,color=MUTED,linespacing=1.6)
    save(fig)



if __name__ == '__main__':
    validate_published(summarise(min_cafes=1))
    rank_crossings(summarise())
    print('Validated all 87 country indices; saved 20260908.png (36 countries with at least 10 cafés).')
