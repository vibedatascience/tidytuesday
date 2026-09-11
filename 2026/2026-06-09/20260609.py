"""TidyTuesday 2026-06-09: Critic scores and box office for video-game films. Reproduce the chart from the bundled source data."""
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
    fig.text(.07,.96,'TIDYTUESDAY  /  2026-06-09',fontsize=9,color=ACCENT,weight='bold')
    fig.text(.07,.90,textwrap.fill('Critic scores and box office for video-game films',48),fontsize=27,fontfamily='DejaVu Serif',va='top',linespacing=1.14)
    fig.text(.07,.77,subtitle,fontsize=10,va='top',linespacing=1.55)
    fig.text(.07,.035,textwrap.fill('Data: Wikipedia film adaptation tables · TidyTuesday. Graphic: vibedatascience.',110),fontsize=8,color=MUTED,linespacing=1.5)
    return fig

def axis(fig, rect=(.24,.18,.69,.49), grid='x'):
    ax=fig.add_axes(rect,facecolor=PAPER)
    for spine in ax.spines.values():spine.set_visible(False)
    ax.tick_params(length=0,pad=8)
    if grid:ax.grid(axis=grid,color=MUTED,alpha=.16,linewidth=.7)
    ax.set_axisbelow(True)
    return ax

def save(fig):
    fig.savefig(HERE / '20260609.png',dpi=170)
    plt.close(fig)
    print('2026-06-09: saved 20260609.png')

df=read('game_films');d=df[(df.category=='Theatrical releases')&(df.worldwide_box_office_currency=='$')].dropna(subset=['worldwide_box_office','rotten_tomatoes']);d=d[d.worldwide_box_office>0].drop_duplicates('title')
assert d.rotten_tomatoes.between(0,100).all()
fig=figure('Theatrical adaptations with both a Rotten Tomatoes score and a worldwide US-dollar gross.\nThe vertical scale is logarithmic; box-office totals are not adjusted for inflation.',9)
ax=axis(fig,(.12,.21,.78,.44),grid='y');ax.scatter(d.rotten_tomatoes,d.worldwide_box_office/1e6,s=45,alpha=.6,c=SECOND,edgecolors=PAPER)
ax.set_yscale('log');ax.set_xlim(-2,102);ax.set_xlabel('Rotten Tomatoes score (%)',labelpad=12);ax.set_ylabel('Worldwide gross (USD millions, log scale)')
for (_,r),(x,y) in zip(d.nlargest(4,'worldwide_box_office').iterrows(),[(.58,.98),(.36,.86),(.12,.97),(.70,.68)]):
 ax.annotate(textwrap.fill(r.title,23),xy=(r.rotten_tomatoes,r.worldwide_box_office/1e6),xytext=(x,y),textcoords='axes fraction',ha='left',va='top',fontsize=8,color=ACCENT,arrowprops={'arrowstyle':'-','color':MUTED,'lw':.7})
fig.text(.07,.09,f'{len(d)} films with complete paired data. Gross revenue is not profit; no trend or causal relationship is assumed.',fontsize=8,color=MUTED)
save(fig)
