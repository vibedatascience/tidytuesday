"""TidyTuesday 2026-03-17: Monthly mortality in Norwegian salmon farming. Reproduce the chart from the bundled source data."""
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
    fig.text(.07,.96,'TIDYTUESDAY  /  2026-03-17',fontsize=9,color=ACCENT,weight='bold')
    fig.text(.07,.90,textwrap.fill('Monthly mortality in Norwegian salmon farming',48),fontsize=27,fontfamily='DejaVu Serif',va='top',linespacing=1.14)
    fig.text(.07,.77,subtitle,fontsize=10,va='top',linespacing=1.55)
    fig.text(.07,.035,textwrap.fill('Data: Norwegian Veterinary Institute · TidyTuesday. Graphic: vibedatascience.',110),fontsize=8,color=MUTED,linespacing=1.5)
    return fig

def axis(fig, rect=(.24,.18,.69,.49), grid='x'):
    ax=fig.add_axes(rect,facecolor=PAPER)
    for spine in ax.spines.values():spine.set_visible(False)
    ax.tick_params(length=0,pad=8)
    if grid:ax.grid(axis=grid,color=MUTED,alpha=.16,linewidth=.7)
    ax.set_axisbelow(True)
    return ax

def save(fig):
    fig.savefig(HERE / '20260317.png',dpi=170)
    plt.close(fig)
    print('2026-03-17: saved 20260317.png')

df=read('monthly_mortality_data');d=df[(df.geo_group=='country')&(df.region=='Norge')].copy();d['date']=pd.to_datetime(d.date)
assert not d.duplicated(['date','species']).any();assert (d.q1<=d['median']).all() and (d['median']<=d.q3).all()
fig=figure('Published national monthly estimates for salmon and rainbow trout.\nLines show medians; shaded bands show the published interquartile range.',9)
ax=axis(fig,(.12,.21,.78,.44),grid='y')
for (name,g),color in zip(d.groupby('species'),[SECOND,ACCENT]):
 g=g.sort_values('date');ax.fill_between(g.date,g.q1,g.q3,color=color,alpha=.18);ax.plot(g.date,g['median'],color=color,lw=2.2,label='Rainbow trout' if name=='rainbowtrout' else 'Salmon')
ax.set_ylim(bottom=0);ax.set_ylabel('Monthly mortality (%)');ax.xaxis.set_major_locator(mdates.YearLocator());ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'));ax.legend(frameon=False)
fig.text(.07,.10,'The band describes the published spread, not a confidence interval. Country-level data only; regional series are not summed.',fontsize=8,color=MUTED)
save(fig)
