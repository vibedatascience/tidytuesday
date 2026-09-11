"""TidyTuesday 2026-03-10: How people interpret probability phrases. Reproduce the chart from the bundled source data."""
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
    fig.text(.07,.96,'TIDYTUESDAY  /  2026-03-10',fontsize=9,color=ACCENT,weight='bold')
    fig.text(.07,.90,textwrap.fill('How people interpret probability phrases',48),fontsize=27,fontfamily='DejaVu Serif',va='top',linespacing=1.14)
    fig.text(.07,.77,subtitle,fontsize=10,va='top',linespacing=1.55)
    fig.text(.07,.035,textwrap.fill('Data: Adam Kucharski, CAPphrase (2026) · TidyTuesday. Graphic: vibedatascience.',110),fontsize=8,color=MUTED,linespacing=1.5)
    return fig

def axis(fig, rect=(.24,.18,.69,.49), grid='x'):
    ax=fig.add_axes(rect,facecolor=PAPER)
    for spine in ax.spines.values():spine.set_visible(False)
    ax.tick_params(length=0,pad=8)
    if grid:ax.grid(axis=grid,color=MUTED,alpha=.16,linewidth=.7)
    ax.set_axisbelow(True)
    return ax

def save(fig):
    fig.savefig(HERE / '20260310.png',dpi=170)
    plt.close(fig)
    print('2026-03-10: saved 20260310.png')

df=read('absolute_judgements').dropna(subset=['term','probability']);assert df.probability.between(0,100).all()
order=df.groupby('term').probability.median().sort_values().index
fig=figure('Distributions of numerical estimates given to probability phrases.\nDots mark medians; thick segments show the middle half of responses.',12)
ax=axis(fig,(.25,.15,.66,.53))
for i,term in enumerate(order):
 v=df.loc[df.term==term,'probability'];q=v.quantile([.25,.5,.75]);p=ax.violinplot(v,positions=[i],vert=False,widths=.8,showextrema=False)
 for b in p['bodies']:b.set_facecolor(SECOND);b.set_alpha(.45)
 ax.plot([q.iloc[0],q.iloc[2]],[i,i],color=ACCENT,lw=3);ax.scatter(q.iloc[1],i,color=INK,s=25,zorder=3)
ax.set_yticks(range(len(order)),order,fontsize=9);ax.set_xlim(0,100);ax.set_xlabel('Assigned probability (%)',labelpad=12)
fig.text(.07,.085,f'{len(df):,} phrase ratings. Online quiz respondents are a self-selected sample. Width shows density, not respondent count.',fontsize=8,color=MUTED)
save(fig)
