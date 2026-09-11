"""TidyTuesday 2026-01-06: Income inequality before and after taxes and benefits. Reproduce the chart from the bundled source data."""
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
    fig.text(.07,.96,'TIDYTUESDAY  /  2026-01-06',fontsize=9,color=ACCENT,weight='bold')
    fig.text(.07,.90,textwrap.fill('Income inequality before and after taxes and benefits',48),fontsize=27,fontfamily='DejaVu Serif',va='top',linespacing=1.14)
    fig.text(.07,.77,subtitle,fontsize=10,va='top',linespacing=1.55)
    fig.text(.07,.035,textwrap.fill('Data: Our World in Data; LIS and OECD · TidyTuesday. Graphic: vibedatascience.',110),fontsize=8,color=MUTED,linespacing=1.5)
    return fig

def axis(fig, rect=(.24,.18,.69,.49), grid='x'):
    ax=fig.add_axes(rect,facecolor=PAPER)
    for spine in ax.spines.values():spine.set_visible(False)
    ax.tick_params(length=0,pad=8)
    if grid:ax.grid(axis=grid,color=MUTED,alpha=.16,linewidth=.7)
    ax.set_axisbelow(True)
    return ax

def save(fig):
    fig.savefig(HERE / '20260106.png',dpi=170)
    plt.close(fig)
    print('2026-01-06: saved 20260106.png')

df=read('income_inequality_processed').dropna(subset=['gini_mi_eq','gini_dhi_eq'])
assert df[['gini_mi_eq','gini_dhi_eq']].ge(0).all().all() and df[['gini_mi_eq','gini_dhi_eq']].le(1).all().all()
# Compare a common year, with the largest number of available country pairs since 2015.
year=int(df.loc[df.Year>=2015].groupby('Year').Entity.nunique().sort_values(ascending=False,kind='stable').index[0])
d=df.loc[df.Year==year].copy();assert not d.Entity.duplicated().any()
d=d.sort_values('gini_dhi_eq',ascending=False)
fig=figure(f'Gini coefficients in {year}. Each line connects before-tax income with disposable income.\nWeek 1: a dataset from the 2025 TidyTuesday collection.',height=12)
ax=axis(fig,(.25,.14,.66,.55))
y=np.arange(len(d));ax.hlines(y,d.gini_dhi_eq,d.gini_mi_eq,color=MUTED,alpha=.5,lw=2)
ax.scatter(d.gini_mi_eq,y,color=SECOND,s=32,label='Before taxes and benefits',zorder=3)
ax.scatter(d.gini_dhi_eq,y,color=ACCENT,s=32,label='After taxes and benefits',zorder=3)
ax.set_yticks(y,d.Entity,fontsize=9);ax.invert_yaxis();ax.set_xlim(0,.65)
ax.set_xlabel('Gini coefficient · lower values indicate less inequality',labelpad=12)
ax.legend(loc='lower center',bbox_to_anchor=(.5,1.03),frameon=False,ncol=1,fontsize=9)
fig.text(.07,.077,f'{len(d)} countries with both measures in the same year. Definitions vary by source; see the original data notes.',fontsize=8,color=MUTED)
save(fig)
