"""TidyTuesday 2026-07-14: Penguin bill and wing measurements by genus. Reproduce the chart from the bundled source data."""
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
    fig.text(.07,.96,'TIDYTUESDAY  /  2026-07-14',fontsize=9,color=ACCENT,weight='bold')
    fig.text(.07,.90,textwrap.fill('Penguin bill and wing measurements by genus',48),fontsize=27,fontfamily='DejaVu Serif',va='top',linespacing=1.14)
    fig.text(.07,.77,subtitle,fontsize=10,va='top',linespacing=1.55)
    fig.text(.07,.035,textwrap.fill('Data: AVONET morphological data · TidyTuesday. Graphic: vibedatascience.',110),fontsize=8,color=MUTED,linespacing=1.5)
    return fig

def axis(fig, rect=(.24,.18,.69,.49), grid='x'):
    ax=fig.add_axes(rect,facecolor=PAPER)
    for spine in ax.spines.values():spine.set_visible(False)
    ax.tick_params(length=0,pad=8)
    if grid:ax.grid(axis=grid,color=MUTED,alpha=.16,linewidth=.7)
    ax.set_axisbelow(True)
    return ax

def save(fig):
    fig.savefig(HERE / '20260714.png',dpi=170)
    plt.close(fig)
    print('2026-07-14: saved 20260714.png')

df=read('many_penguins');d=df.dropna(subset=['beak.length_culmen','wing.length']);assert d['beak.length_culmen'].gt(0).all() and d['wing.length'].gt(0).all()
genera=sorted(d.genus.unique());colors=[ACCENT,SECOND,'#a18452','#7b6599','#60889c','#a65a7a']
fig=figure('Individual specimen measurements from the supplied penguin extract.\nColour identifies genus; each point is a specimen with both measurements.',9)
ax=axis(fig,(.13,.21,.64,.44),grid='both')
for genus,color in zip(genera,colors):
 g=d[d.genus==genus];ax.scatter(g['beak.length_culmen'],g['wing.length'],s=45,color=color,alpha=.8,label=f'{genus} (n={len(g)})',edgecolors=PAPER,linewidths=.6)
ax.set_xlabel('Culmen length (mm)',labelpad=12);ax.set_ylabel('Wing length (mm)');ax.legend(loc='center left',bbox_to_anchor=(1.01,.5),frameon=False,fontsize=8)
fig.text(.07,.09,f'{len(d)} complete specimens of {d.species.nunique()} species. Repeated species are separate measured specimens, not independent species means.',fontsize=8,color=MUTED)
save(fig)
