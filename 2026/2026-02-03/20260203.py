"""TidyTuesday 2026-02-03: Preferred soil pH ranges for edible plants. Reproduce the chart from the bundled source data."""
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
    fig.text(.07,.96,'TIDYTUESDAY  /  2026-02-03',fontsize=9,color=ACCENT,weight='bold')
    fig.text(.07,.90,textwrap.fill('Preferred soil pH ranges for edible plants',48),fontsize=27,fontfamily='DejaVu Serif',va='top',linespacing=1.14)
    fig.text(.07,.77,subtitle,fontsize=10,va='top',linespacing=1.55)
    fig.text(.07,.035,textwrap.fill('Data: GROW Observatory Edible Plant Database · TidyTuesday. Graphic: vibedatascience.',110),fontsize=8,color=MUTED,linespacing=1.5)
    return fig

def axis(fig, rect=(.24,.18,.69,.49), grid='x'):
    ax=fig.add_axes(rect,facecolor=PAPER)
    for spine in ax.spines.values():spine.set_visible(False)
    ax.tick_params(length=0,pad=8)
    if grid:ax.grid(axis=grid,color=MUTED,alpha=.16,linewidth=.7)
    ax.set_axisbelow(True)
    return ax

def save(fig):
    fig.savefig(HERE / '20260203.png',dpi=170)
    plt.close(fig)
    print('2026-02-03: saved 20260203.png')

df=read('edible_plants').dropna(subset=['common_name','preferred_ph_lower','preferred_ph_upper'])
d=df.drop_duplicates('common_name').sort_values(['preferred_ph_lower','common_name']).head(24)
assert d.preferred_ph_lower.le(d.preferred_ph_upper).all()
fig=figure('The 24 plants with the lowest lower pH limit in the supplied database.\nA line shows the full preferred range; the dotted line marks neutral soil.',12)
ax=axis(fig,(.31,.16,.59,.52));ax.axvline(7,color=MUTED,ls=':',lw=1.5)
y=np.arange(len(d));ax.hlines(y,d.preferred_ph_lower,d.preferred_ph_upper,color=ACCENT,lw=5,alpha=.7)
ax.scatter(d.preferred_ph_lower,y,color=ACCENT,s=28);ax.scatter(d.preferred_ph_upper,y,color=SECOND,s=28)
ax.set_yticks(y,d.common_name,fontsize=9);ax.invert_yaxis();ax.set_xlim(4,9);ax.set_xticks(np.arange(4,9.1,.5));ax.set_xlabel('Preferred soil pH',labelpad=12)
fig.text(.07,.083,'Selection sorted by lower bound, then plant name. Duplicate common names removed. Conditions are database guidance.',fontsize=8,color=MUTED)
save(fig)
