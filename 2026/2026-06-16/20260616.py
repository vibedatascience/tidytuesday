"""TidyTuesday 2026-06-16: Scotland’s most popular girls’ names over time. Reproduce the chart from the bundled source data."""
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
PAPER, INK, MUTED, ACCENT, SECOND = ('#f5edf0', '#462937', '#897380', '#aa4163', '#497f88')
plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':10, 'text.color':INK,
 'axes.labelcolor':INK, 'xtick.color':MUTED, 'ytick.color':MUTED,
 'axes.edgecolor':MUTED, 'savefig.facecolor':PAPER})

def read(name):
    data = pd.read_csv(HERE / 'data' / (name + '.csv.gz'), low_memory=False)
    assert len(data), 'Empty source data'
    return data

def figure(subtitle, height=9):
    fig = plt.figure(figsize=(11,height), facecolor=PAPER)
    fig.text(.07,.96,'TIDYTUESDAY  /  2026-06-16',fontsize=9,color=ACCENT,weight='bold')
    fig.text(.07,.90,textwrap.fill('Scotland’s most popular girls’ names over time',48),fontsize=27,fontfamily='DejaVu Serif',va='top',linespacing=1.14)
    fig.text(.07,.77,subtitle,fontsize=10,va='top',linespacing=1.55)
    fig.text(.07,.035,textwrap.fill('Data: National Records of Scotland · TidyTuesday. Graphic: vibedatascience.',110),fontsize=8,color=MUTED,linespacing=1.5)
    return fig

def axis(fig, rect=(.24,.18,.69,.49), grid='x'):
    ax=fig.add_axes(rect,facecolor=PAPER)
    for spine in ax.spines.values():spine.set_visible(False)
    ax.tick_params(length=0,pad=8)
    if grid:ax.grid(axis=grid,color=MUTED,alpha=.16,linewidth=.7)
    ax.set_axisbelow(True)
    return ax

def save(fig):
    fig.savefig(HERE / '20260616.png',dpi=170)
    plt.close(fig)
    print('2026-06-16: saved 20260616.png')

df=read('scotland_names');df=df[df.Sex=='Girl'];year=int(df.Year.max());top=df[df.Year==year].nlargest(6,'Number').Name.tolist()
assert len(top)==6
fig=figure(f'Rank histories of the six most frequently recorded girls’ names in {year}.\nA lower rank means a more popular name. Only ranks 1–100 are drawn.',11)
for i,name in enumerate(top):
 ax=axis(fig,(.11+(i%2)*.46,.48-(i//2)*.155,.35,.115),grid='y')
 d=df[df.Name==name].set_index('Year').sort_index();assert not d.index.duplicated().any()
 s=d.Rank.reindex(range(int(df.Year.min()),year+1));s=s.where(s<=100)
 ax.plot(s.index,s,color=ACCENT if i==0 else SECOND,lw=2);ax.set_ylim(102,-4);ax.set_xlim(df.Year.min(),year+2)
 ax.set_yticks([1,50,100]);ax.set_xticks([1980,2000,2020]);ax.tick_params(labelsize=8)
 ax.set_title(name,loc='left',fontsize=13,fontfamily='DejaVu Serif',pad=5)
 ax.scatter(year,s.loc[year],color=INK,s=18,zorder=4)
fig.text(.07,.08,'Gaps mean a name was outside the top 100 or absent from the published records. Ranks are not birth counts.',fontsize=8,color=MUTED)
save(fig)
