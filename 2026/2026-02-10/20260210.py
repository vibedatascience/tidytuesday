"""TidyTuesday 2026-02-10: Competition days at the 2026 Winter Olympics. Reproduce the chart from the bundled source data."""
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
PAPER, INK, MUTED, ACCENT, SECOND = ('#142435', '#edf1ee', '#a3b3bc', '#e4b65c', '#58b7b0')
plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':10, 'text.color':INK,
 'axes.labelcolor':INK, 'xtick.color':MUTED, 'ytick.color':MUTED,
 'axes.edgecolor':MUTED, 'savefig.facecolor':PAPER})

def read(name):
    data = pd.read_csv(HERE / 'data' / (name + '.csv.gz'), low_memory=False)
    assert len(data), 'Empty source data'
    return data

def figure(subtitle, height=9):
    fig = plt.figure(figsize=(11,height), facecolor=PAPER)
    fig.text(.07,.96,'TIDYTUESDAY  /  2026-02-10',fontsize=9,color=ACCENT,weight='bold')
    fig.text(.07,.90,textwrap.fill('Competition days at the 2026 Winter Olympics',48),fontsize=27,fontfamily='DejaVu Serif',va='top',linespacing=1.14)
    fig.text(.07,.77,subtitle,fontsize=10,va='top',linespacing=1.55)
    fig.text(.07,.035,textwrap.fill('Data: Milano-Cortina 2026 event schedule · TidyTuesday. Graphic: vibedatascience.',110),fontsize=8,color=MUTED,linespacing=1.5)
    return fig

def axis(fig, rect=(.24,.18,.69,.49), grid='x'):
    ax=fig.add_axes(rect,facecolor=PAPER)
    for spine in ax.spines.values():spine.set_visible(False)
    ax.tick_params(length=0,pad=8)
    if grid:ax.grid(axis=grid,color=MUTED,alpha=.16,linewidth=.7)
    ax.set_axisbelow(True)
    return ax

def save(fig):
    fig.savefig(HERE / '20260210.png',dpi=170)
    plt.close(fig)
    print('2026-02-10: saved 20260210.png')

df=read('schedule');d=df.loc[~df.is_training].drop_duplicates(['event_code','date','start_datetime_local'])
d['date']=pd.to_datetime(d.date);days=pd.date_range(d.date.min(),d.date.max());sports=sorted(d.discipline_name.unique())
counts=d.groupby(['discipline_name','date']).size();medals=d.loc[d.is_medal_event].groupby(['discipline_name','date']).size()
fig=figure('One row per discipline. Circle area shows the number of scheduled competition records.\nGold centres mark dates containing at least one medal event; training is excluded.',10)
ax=axis(fig,(.29,.18,.63,.48),None)
for y,sport in enumerate(sports):
 ax.hlines(y,-.5,len(days)-.5,color=MUTED,alpha=.15)
 for x,date in enumerate(days):
  n=counts.get((sport,date),0)
  if n:ax.scatter(x,y,s=15*n,color=SECOND,alpha=.65)
  if medals.get((sport,date),0):ax.scatter(x,y,s=14,color=ACCENT,zorder=4)
ax.set_yticks(range(len(sports)),sports,fontsize=9);ax.invert_yaxis();ax.set_xticks(range(len(days)),[str(x.day) for x in days]);ax.set_xlabel('February 2026',labelpad=12);ax.set_xlim(-1,len(days))
for i,n in enumerate([1,5,10]):ax.scatter([],[],s=15*n,color=SECOND,label=f'{n} records')
ax.legend(loc='lower left',bbox_to_anchor=(0,1.03),ncol=3,frameon=False,fontsize=8)
fig.text(.07,.09,f'{len(d):,} competition records after removing exact event/date/start-time duplicates. Records are not medal counts.',fontsize=8,color=MUTED)
save(fig)
