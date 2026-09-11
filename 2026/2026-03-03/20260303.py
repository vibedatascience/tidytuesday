"""TidyTuesday 2026-03-03: Female tortoises among recorded individuals. Reproduce the chart from the bundled source data."""
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
    fig.text(.07,.96,'TIDYTUESDAY  /  2026-03-03',fontsize=9,color=ACCENT,weight='bold')
    fig.text(.07,.90,textwrap.fill('Female tortoises among recorded individuals',48),fontsize=27,fontfamily='DejaVu Serif',va='top',linespacing=1.14)
    fig.text(.07,.77,subtitle,fontsize=10,va='top',linespacing=1.55)
    fig.text(.07,.035,textwrap.fill('Data: Golem Grad tortoise study, Ecology Letters (2026) · TidyTuesday. Graphic: vibedatascience.',110),fontsize=8,color=MUTED,linespacing=1.5)
    return fig

def axis(fig, rect=(.24,.18,.69,.49), grid='x'):
    ax=fig.add_axes(rect,facecolor=PAPER)
    for spine in ax.spines.values():spine.set_visible(False)
    ax.tick_params(length=0,pad=8)
    if grid:ax.grid(axis=grid,color=MUTED,alpha=.16,linewidth=.7)
    ax.set_axisbelow(True)
    return ax

def save(fig):
    fig.savefig(HERE / '20260303.png',dpi=170)
    plt.close(fig)
    print('2026-03-03: saved 20260303.png')

df=read('tortoise_body_condition_cleaned');d=df.dropna(subset=['individual','sex','locality','year']).drop_duplicates(['individual','year','locality'])
assert d.sex.isin(['f','m']).all()
p=d.assign(female=d.sex.eq('f')).groupby(['locality','year']).agg(female=('female','sum'),n=('individual','size'))
p['pct']=100*p.female/p.n
fig=figure('The percentage of recorded individuals that are female, by site and year.\nEach individual is counted once per site per year, even if measured in two seasons.',9)
ax=axis(fig,(.12,.20,.69,.45),grid='y')
for (name,g),color in zip(p.groupby(level=0),[ACCENT,SECOND,MUTED]):
 s=g.droplevel(0).reindex(range(int(df.year.min()),int(df.year.max())+1));ax.plot(s.index,s.pct,lw=2.5,color=color,marker='o',ms=4,label=name)
ax.set_ylim(0,100);ax.set_ylabel('Female share of recorded individuals (%)');ax.set_xlabel('Observation year',labelpad=12)
ax.legend(frameon=False,loc='upper right');ax.axhline(50,color=MUTED,ls=':',alpha=.5)
fig.text(.07,.09,'Observation shares are not population estimates. Differences in recapture and sampling can affect the apparent sex ratio.',fontsize=8,color=MUTED)
save(fig)
