"""TidyTuesday 2026-09-01: Recorded construction dates of castles and palaces. Reproduce the chart from the bundled source data."""
from pathlib import Path
import textwrap
import re
from collections import Counter
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter, MaxNLocator
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.patches import Patch

HERE = Path(__file__).resolve().parent
PAPER, INK, MUTED, ACCENT, SECOND = ('#f5f1e8', '#272b2b', '#72786f', '#b95137', '#287773')
plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':10, 'text.color':INK,
 'axes.labelcolor':INK, 'xtick.color':MUTED, 'ytick.color':MUTED,
 'axes.edgecolor':MUTED, 'savefig.facecolor':PAPER})

def read(name):
    data = pd.read_csv(HERE / 'data' / (name + '.csv.gz'), low_memory=False)
    assert len(data), 'Empty source data'
    return data

def figure(subtitle, height=9):
    fig = plt.figure(figsize=(11,height), facecolor=PAPER)
    fig.text(.07,.96,'TIDYTUESDAY  /  2026-09-01',fontsize=9,color=ACCENT,weight='bold')
    fig.text(.07,.90,textwrap.fill('Recorded construction dates of castles and palaces',48),fontsize=27,fontfamily='DejaVu Serif',va='top',linespacing=1.14)
    fig.text(.07,.77,subtitle,fontsize=10,va='top',linespacing=1.55)
    fig.text(.07,.035,textwrap.fill('Data: Castlemap, curated from Wikidata · TidyTuesday. Graphic: vibedatascience.',110),fontsize=8,color=MUTED,linespacing=1.5)
    return fig

def axis(fig, rect=(.24,.18,.69,.49), grid='x'):
    ax=fig.add_axes(rect,facecolor=PAPER)
    for spine in ax.spines.values():spine.set_visible(False)
    ax.tick_params(length=0,pad=8)
    if grid:ax.grid(axis=grid,color=MUTED,alpha=.16,linewidth=.7)
    ax.set_axisbelow(True)
    return ax

def save(fig):
    fig.savefig(HERE / '20260901.png',dpi=170)
    plt.close(fig)
    print('2026-09-01: saved 20260901.png')

df=read('world_castles');assert not df.qid.duplicated().any()
d=df[df.year.between(500,1999)].copy();bins=np.arange(500,2001,100)
fig=figure('Construction-year entries between AD 500 and 1999, grouped into centuries.\nThe four categories share the same axes; the source includes approximate and uncertain dates.',10)
maximum=max(np.histogram(g.year,bins=bins)[0].max() for _,g in d.groupby('category'))
for i,(cat,color) in enumerate(zip(['castle','palace','fortress','ruin'],[ACCENT,SECOND,'#967c50','#807092'])):
 ax=axis(fig,(.12+(i%2)*.45,.42-(i//2)*.24,.35,.18),grid='y');g=d[d.category==cat];n,_=np.histogram(g.year,bins=bins)
 ax.bar(bins[:-1]+50,n,width=80,color=color);ax.set_xlim(500,2000);ax.set_ylim(0,maximum*1.1);ax.set_xticks([500,1000,1500,2000]);ax.tick_params(labelsize=8)
 ax.set_title(f'{cat.title()} (n={len(g):,})',loc='left',fontsize=13,fontfamily='DejaVu Serif')
fig.text(.07,.085,f'{len(d):,} dated entries shown from {len(df):,} landmarks. Bars reflect catalogue coverage, not a complete historical building census.',fontsize=8,color=MUTED)
save(fig)
