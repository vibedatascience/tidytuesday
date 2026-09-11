"""TidyTuesday 2026-07-21: Themes tagged in near-death experience accounts. Reproduce the chart from the bundled source data."""
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
    fig.text(.07,.96,'TIDYTUESDAY  /  2026-07-21',fontsize=9,color=ACCENT,weight='bold')
    fig.text(.07,.90,textwrap.fill('Themes tagged in near-death experience accounts',48),fontsize=27,fontfamily='DejaVu Serif',va='top',linespacing=1.14)
    fig.text(.07,.77,subtitle,fontsize=10,va='top',linespacing=1.55)
    fig.text(.07,.035,textwrap.fill('Data: Near Death Experience Research Foundation archive · TidyTuesday. Graphic: vibedatascience.',110),fontsize=8,color=MUTED,linespacing=1.5)
    return fig

def axis(fig, rect=(.24,.18,.69,.49), grid='x'):
    ax=fig.add_axes(rect,facecolor=PAPER)
    for spine in ax.spines.values():spine.set_visible(False)
    ax.tick_params(length=0,pad=8)
    if grid:ax.grid(axis=grid,color=MUTED,alpha=.16,linewidth=.7)
    ax.set_axisbelow(True)
    return ax

def save(fig):
    fig.savefig(HERE / '20260721.png',dpi=170)
    plt.close(fig)
    print('2026-07-21: saved 20260721.png')

df=read('nde_experiences');assert not df.entry_id.duplicated().any()
labels={'ai_obe':'Out-of-body experience','ai_unity':'Unity','ai_clinical':'Clinical setting','ai_esp':'Extrasensory perception','ai_hellish':'Hellish experience','ai_past_lives':'Past lives','ai_world_future':'World future','ai_aliens':'Aliens'}
values=[]
for c,label in labels.items():
 s=df[c].dropna();assert s.isin([True,False]).all();values.append((label,100*s.mean(),int(s.sum()),len(s)))
values.sort(key=lambda x:x[1])
fig=figure('Share of the supplied accounts carrying each automated theme tag.\nThemes can overlap. These tags describe narratives, not independently verified events.',9)
ax=axis(fig,(.31,.23,.53,.40));y=np.arange(len(values));v=[r[1] for r in values]
ax.hlines(y,0,v,color=MUTED,alpha=.4,lw=2);ax.scatter(v,y,s=80,color=SECOND,zorder=3)
for i,(label,pct,n,total) in enumerate(values):ax.text(pct+2,i,f'{pct:.1f}%  ({n}/{total})',va='center',fontsize=9)
ax.set_yticks(y,[r[0] for r in values]);ax.set_xlim(0,115);ax.set_xticks([0,25,50,75,100]);ax.set_xlabel('Accounts with tag (%)',labelpad=12)
fig.text(.07,.10,f'{len(df)} archived accounts. Denominator is nonmissing tags per theme. Self-selection and automated tagging limit interpretation.',fontsize=8,color=MUTED)
save(fig)
