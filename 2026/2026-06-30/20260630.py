"""TidyTuesday 2026-06-30: Recorded ship losses around Ireland by decade. Reproduce the chart from the bundled source data."""
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
PAPER, INK, MUTED, ACCENT, SECOND = ('#edf3f5', '#1c3346', '#6a7d86', '#256f99', '#d27b3e')
plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':10, 'text.color':INK,
 'axes.labelcolor':INK, 'xtick.color':MUTED, 'ytick.color':MUTED,
 'axes.edgecolor':MUTED, 'savefig.facecolor':PAPER})

def read(name):
    data = pd.read_csv(HERE / 'data' / (name + '.csv.gz'), low_memory=False)
    assert len(data), 'Empty source data'
    return data

def figure(subtitle, height=9):
    fig = plt.figure(figsize=(11,height), facecolor=PAPER)
    fig.text(.07,.96,'TIDYTUESDAY  /  2026-06-30',fontsize=9,color=ACCENT,weight='bold')
    fig.text(.07,.90,textwrap.fill('Recorded ship losses around Ireland by decade',48),fontsize=27,fontfamily='DejaVu Serif',va='top',linespacing=1.14)
    fig.text(.07,.77,subtitle,fontsize=10,va='top',linespacing=1.55)
    fig.text(.07,.035,textwrap.fill('Data: National Monuments Service Wreck Inventory of Ireland · TidyTuesday. Graphic: vibedatascience.',110),fontsize=8,color=MUTED,linespacing=1.5)
    return fig

def axis(fig, rect=(.24,.18,.69,.49), grid='x'):
    ax=fig.add_axes(rect,facecolor=PAPER)
    for spine in ax.spines.values():spine.set_visible(False)
    ax.tick_params(length=0,pad=8)
    if grid:ax.grid(axis=grid,color=MUTED,alpha=.16,linewidth=.7)
    ax.set_axisbelow(True)
    return ax

def save(fig):
    fig.savefig(HERE / '20260630.png',dpi=170)
    plt.close(fig)
    print('2026-06-30: saved 20260630.png')

df=read('wreck_inventory');assert not df.wreck_no.duplicated().any()
d=df[df.year.between(1800,2024)].copy();d['decade']=(d.year//10*10).astype(int)
n=d.groupby('decade').size().reindex(range(1800,2030,10),fill_value=0)
fig=figure('Wreck inventory entries with a recorded loss year between 1800 and 2024.\nThe inventory includes many undated entries, which are not assigned to a decade.',9)
ax=axis(fig,(.12,.21,.78,.43),grid='y');colors=[ACCENT if y in [1910,1940] else SECOND for y in n.index]
ax.bar(n.index,n,width=8,color=colors);ax.set_xlim(1793,2028);ax.set_xticks(range(1800,2030,20));ax.set_ylabel('Inventory entries');ax.set_xlabel('Decade of recorded loss',labelpad=12)
for year in [1910,1940]:ax.text(year,n.loc[year]+n.max()*.03,f'{n.loc[year]:,}',ha='center',fontsize=10,color=ACCENT)
fig.text(.07,.09,f'{len(d):,} entries shown from {len(df):,} total. Counts reflect surviving records and dating coverage, not a complete loss history.',fontsize=8,color=MUTED)
save(fig)
