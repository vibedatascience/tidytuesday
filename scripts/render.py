"""Three independently implemented designs. Rebuild from the committed CSV inputs."""
import csv
import json
import shutil
import sys
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.path import Path as MPath
from matplotlib.patches import PathPatch
from analyse import ROOT, WEEK, summarise, validate_published

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
OUT = WEEK / 'plots'
OUT.mkdir(exist_ok=True)


def canvas(title, subtitle, label, height=12):
    fig = plt.figure(figsize=(10, height), facecolor=PAPER)
    fig.text(.075, .958, 'VIBEDATASCIENCE     /     TIDYTUESDAY 2026', size=9, weight='bold', color=BLUE)
    fig.text(.925, .958, 'NO. 36', ha='right', size=9, color=MUTED)
    fig.text(.075, .91, title, size=34, fontfamily='DejaVu Serif', va='top', linespacing=1.06)
    fig.text(.075, .804, subtitle, size=10, va='top', linespacing=1.6)
    fig.text(.075, .055, label, size=8, weight='bold', color=MUTED)
    fig.text(.075, .032, 'Data: James Hoffmann · TidyTuesday, 08 Sep 2026. Tips excluded. Voluntary café sample.\nOriginal graphic: vibedatascience. Design references and methodology in the repository.',
             size=7, linespacing=1.6, color=MUTED)
    return fig


def save(fig, name):
    fig.savefig(OUT / f'{name}.svg', metadata={'Date': None})
    fig.savefig(OUT / f'{name}.png', dpi=180, metadata={'Software': 'Matplotlib'})
    plt.close(fig)


def rank_crossings(rows):
    fig = canvas('A cappuccino takes longer to earn\nin India than in Switzerland',
        'India has the third-lowest mean cup price in this sample—but the longest work time.\nSwiss cafés report a higher mean cup price, but a shorter earning time.', '01 / RANK CROSSINGS — SELECTED')
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
    save(fig,'01-rank-crossings')


def mobile_crossings(rows):
    """A dedicated narrow layout with readable labels, without repeating the page heading."""
    fig = plt.figure(figsize=(4.5, 7.5), facecolor=PAPER)
    ax = fig.add_axes([.34, .10, .32, .76], facecolor=PAPER)
    ax.set_xlim(-.03, 1.03); ax.set_ylim(38, -1); ax.axis('off')
    highlighted = {'India', 'Switzerland', 'Australia'}
    fig.text(.055, .965, 'CUP PRICE', size=10, weight='bold', va='top')
    fig.text(.055, .933, 'Mean, GBP', size=9, color=MUTED, va='top')
    fig.text(.945, .965, 'WORK TIME', size=10, weight='bold', ha='right', va='top')
    fig.text(.945, .933, 'Minutes per cup', size=9, color=MUTED, ha='right', va='top')
    for x in [0,1]:ax.plot([x,x],[1,36],color=LINE,lw=1)
    for row in sorted(rows, key=lambda r:r['country'] in highlighted):
        a,b=row['price_rank'],row['minutes_rank']
        color=COLORS[row['country']] if row['country'] in highlighted else LINE
        ax.add_patch(PathPatch(MPath([(0,a),(.38,a),(.62,b),(1,b)],
            [MPath.MOVETO,MPath.CURVE4,MPath.CURVE4,MPath.CURVE4]),
            facecolor='none',edgecolor=color,lw=2 if row['country'] in highlighted else .6))
        if row['country'] in highlighted:
            ax.scatter([0,1],[a,b],s=25,c=color,zorder=4,edgecolors=PAPER,linewidths=.8)
            for x,y,value,align in [(-.12,a,f"£{row['price']:.2f}",'right'),(1.12,b,f"{row['minutes']:.1f} min",'left')]:
                ax.text(x,y-.6,row['country'],ha=align,va='bottom',size=10.5,color=color,weight='bold')
                ax.text(x,y+.2,value,ha=align,va='top',size=10,color=color)
    fig.text(.055,.065,'Cheapest / shortest at the top.',size=9,color=MUTED)
    fig.text(.055,.035,'36 countries · ≥10 cafés each · Tips excluded',size=8.5,color=MUTED)
    fig.savefig(OUT/'01-rank-crossings-mobile.svg',metadata={'Date':None})
    plt.close(fig)


def time_ledger(rows):
    fig = canvas('Minutes of work needed\nto buy a cappuccino',
        'The sample’s index runs from 10 minutes in Australia to 172 minutes in India.\nA common scale makes the size of the gap visible.', '02 / TIME LEDGER')
    ax = fig.add_axes([.21,.16,.61,.54],facecolor=PAPER)
    ax.set_xlim(0,185);ax.set_ylim(len(rows)-.3,-1)
    for i,row in enumerate(rows):
        color=COLORS.get(row['country'],MUTED)
        ax.plot([0,row['minutes']],[i,i],color=LINE,lw=1.5)
        ax.scatter([row['minutes']],[i],color=color,s=20,zorder=3)
        ax.text(-5,i,row['country'],ha='right',va='center',size=8,color=color)
        ax.text(191,i,f"{row['minutes']:5.1f}",ha='right',va='center',size=8,color=color)
        ax.text(213,i,str(row['n']),ha='right',va='center',size=8,color=MUTED)
    for x in [0,30,60,90,120,150,180]:ax.axvline(x,color=LINE,lw=.5,zorder=0)
    ax.set_xticks([0,30,60,90,120,150,180]);ax.tick_params(axis='x',length=0,labelsize=8,pad=8)
    ax.set_yticks([]);ax.set_xlabel('Minutes of barista pay for one small cappuccino',size=9,labelpad=12)
    for spine in ax.spines.values():spine.set_visible(False)
    ax.text(191,-1.5,'MIN',ha='right',size=7,weight='bold',color=MUTED)
    ax.text(213,-1.5,'CAFÉS',ha='right',size=7,weight='bold',color=MUTED)
    fig.text(.075,.097,'36 countries with ≥10 cafés. Index = 60 × sum of prices / sum of hourly wages.\nThese are sample comparisons, not nationally representative estimates.',size=8,color=MUTED,linespacing=1.6)
    save(fig,'02-time-ledger')


def country_cards(rows):
    selected=['Australia','Italy','Switzerland','UK','USA','Mexico','Philippines','India']
    by={r['country']:r for r in rows}
    fig = canvas('Cappuccino prices and barista pay\nin eight countries',
        'Eight countries, one shared clock. Each bar shows the minutes of pay for a cup.\nMean cup prices and hourly wages are shown below each bar.', '03 / SHARED CLOCKS')
    for i,name in enumerate(selected):
        row=by[name];left=.075+(i%2)*.46;bottom=.585-(i//2)*.145
        ax=fig.add_axes([left,bottom,.39,.12],facecolor=PAPER)
        ax.set_xlim(0,180);ax.set_ylim(0,1);ax.axis('off')
        color=COLORS.get(name,INK)
        ax.text(0,.95,name,size=12,weight='bold',color=color)
        ax.text(180,.95,f"{row['minutes']:.1f} min",ha='right',size=12,color=color)
        ax.plot([0,180],[.53,.53],color=LINE,lw=8,solid_capstyle='butt')
        ax.plot([0,row['minutes']],[.53,.53],color=color,lw=8,solid_capstyle='butt')
        for x in [0,60,120,180]:ax.plot([x,x],[.42,.63],color=PAPER,lw=1)
        ax.text(0,.15,f"£{row['price']:.2f} a cup · £{row['wage']:.2f}/hour · n={row['n']}",size=8,color=MUTED)
    fig.text(.075,.102,'Every bar uses the same 0–180 minute scale. Eight illustrative countries, selected to show contrasts.\nMean prices and wages in GBP. All have ≥10 cafés; see the full 36-country comparison online.',size=8,color=MUTED,linespacing=1.6)
    save(fig,'03-shared-clocks')


def main():
    rows=summarise();validate_published(rows)
    rank_crossings(rows);mobile_crossings(rows);time_ledger(rows);country_cards(rows)
    (WEEK/'summary.json').write_text(json.dumps(rows,indent=2)+'\n')
    with (WEEK/'summary.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    target=ROOT/'docs'/'2026'/'2026-09-08'
    target.mkdir(parents=True,exist_ok=True)
    for p in OUT.iterdir():shutil.copyfile(p,target/p.name)
    shutil.copyfile(WEEK/'summary.json',target/'summary.json')
    shutil.copyfile(WEEK/'summary.csv',target/'summary.csv')
    print(f'Rendered three designs from {len(rows)} validated country summaries.')


if __name__ == '__main__':main()
