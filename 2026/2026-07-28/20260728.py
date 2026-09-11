"""TidyTuesday 2026-07-28: Overnight tourism across Australian regions. Reproduce the chart from the bundled source data."""
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
PAPER, INK, MUTED, ACCENT, SECOND = ('#eff2e6', '#233e30', '#6f806f', '#397f55', '#b67742')
plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':10, 'text.color':INK,
 'axes.labelcolor':INK, 'xtick.color':MUTED, 'ytick.color':MUTED,
 'axes.edgecolor':MUTED, 'savefig.facecolor':PAPER})

def read(name):
    data = pd.read_csv(HERE / 'data' / (name + '.csv.gz'), low_memory=False)
    assert len(data), 'Empty source data'
    return data

def figure(subtitle, height=9):
    fig = plt.figure(figsize=(11,height), facecolor=PAPER)
    fig.text(.07,.96,'TIDYTUESDAY  /  2026-07-28',fontsize=9,color=ACCENT,weight='bold')
    fig.text(.07,.90,textwrap.fill('Overnight tourism across Australian regions',48),fontsize=27,fontfamily='DejaVu Serif',va='top',linespacing=1.14)
    fig.text(.07,.77,subtitle,fontsize=10,va='top',linespacing=1.55)
    fig.text(.07,.035,textwrap.fill('Data: ecotourism R package · TidyTuesday. Graphic: vibedatascience.',110),fontsize=8,color=MUTED,linespacing=1.5)
    return fig

def axis(fig, rect=(.24,.18,.69,.49), grid='x'):
    ax=fig.add_axes(rect,facecolor=PAPER)
    for spine in ax.spines.values():spine.set_visible(False)
    ax.tick_params(length=0,pad=8)
    if grid:ax.grid(axis=grid,color=MUTED,alpha=.16,linewidth=.7)
    ax.set_axisbelow(True)
    return ax

def save(fig):
    fig.savefig(HERE / '20260728.png',dpi=170)
    plt.close(fig)
    print('2026-07-28: saved 20260728.png')

df=read('tourism');keys=['region_id','year','quarter','purpose'];assert not df.duplicated(keys).any()
# Compare the same regional panel over every complete-year quarter, avoiding changing coverage.
d=df[df.year.between(2015,2021)].copy();periods=28
eligible=d.groupby(['region_id','purpose']).size();eligible=eligible[eligible==periods].index
parts=[]
for purpose in ['Business','Holiday']:
 ids=[r for r,p in eligible if p==purpose];g=d[(d.purpose==purpose)&d.region_id.isin(ids)].copy();g['date']=pd.to_datetime(g.year.astype(str)+'-'+((g.quarter-1)*3+1).astype(str)+'-01')
 s=g.groupby('date').trips.sum()/1000;parts.append((purpose,s,len(ids)))
assert all(n>0 for _,_,n in parts)
fig=figure('Quarterly overnight trips in the regions with observations in every quarter of 2015–2021.\nA fixed panel is used separately for each travel purpose; it is not a national total.',9)
ax=axis(fig,(.13,.21,.77,.44),grid='y');ax.axvspan(pd.Timestamp('2020-01-01'),pd.Timestamp('2021-12-31'),color=MUTED,alpha=.10)
for (name,s,n),color in zip(parts,[SECOND,ACCENT]):ax.plot(s.index,s,color=color,lw=2.6,marker='o',ms=3,label=f'{name} ({n} regions)')
ax.set_ylim(bottom=0);ax.set_ylabel('Overnight trips (millions)');ax.xaxis.set_major_locator(mdates.YearLocator());ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'));ax.legend(frameon=False)
fig.text(.07,.10,'Source trips are in thousands. Shading marks 2020–2021. Regional coverage is fixed within purpose, but differs between purposes.',fontsize=8,color=MUTED)
save(fig)
