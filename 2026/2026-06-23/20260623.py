"""TidyTuesday 2026-06-23: Paragraph lengths in two papal encyclicals. Reproduce the chart from the bundled source data."""
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
    fig.text(.07,.96,'TIDYTUESDAY  /  2026-06-23',fontsize=9,color=ACCENT,weight='bold')
    fig.text(.07,.90,textwrap.fill('Paragraph lengths in two papal encyclicals',48),fontsize=27,fontfamily='DejaVu Serif',va='top',linespacing=1.14)
    fig.text(.07,.77,subtitle,fontsize=10,va='top',linespacing=1.55)
    fig.text(.07,.035,textwrap.fill('Data: The Holy See / Vatican.va · TidyTuesday. Graphic: vibedatascience.',110),fontsize=8,color=MUTED,linespacing=1.5)
    return fig

def axis(fig, rect=(.24,.18,.69,.49), grid='x'):
    ax=fig.add_axes(rect,facecolor=PAPER)
    for spine in ax.spines.values():spine.set_visible(False)
    ax.tick_params(length=0,pad=8)
    if grid:ax.grid(axis=grid,color=MUTED,alpha=.16,linewidth=.7)
    ax.set_axisbelow(True)
    return ax

def save(fig):
    fig.savefig(HERE / '20260623.png',dpi=170)
    plt.close(fig)
    print('2026-06-23: saved 20260623.png')

df=read('paragraph_counts').dropna(subset=['word_count']);assert df.word_count.ge(0).all()
fig=figure('Empirical distributions of the supplied paragraph word counts.\nA point on a curve gives the percentage of paragraphs at or below that length.',9)
ax=axis(fig,(.12,.21,.77,.44),grid='both')
for (name,g),color in zip(df.groupby('encyclical'),[SECOND,ACCENT]):
 vals=np.sort(g.word_count);y=100*np.arange(1,len(vals)+1)/len(vals)
 ax.step(vals,y,where='post',color=color,lw=2.7,label=f'{name} ({int(g.year.iloc[0])}; n={len(g)})')
 med=np.median(vals);ax.scatter(med,50,color=color,s=40,zorder=4)
ax.set_xlim(left=0);ax.set_ylim(0,103);ax.set_xlabel('Words per paragraph',labelpad=12);ax.set_ylabel('Cumulative share of paragraphs (%)');ax.legend(frameon=False,loc='lower right',fontsize=9)
fig.text(.07,.10,'Uses the published word counts; no retokenisation of the extracted text. Differences in paragraph structure do not establish readability.',fontsize=8,color=MUTED)
save(fig)
