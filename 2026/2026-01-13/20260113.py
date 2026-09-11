"""TidyTuesday 2026-01-13: Native speakers of widely spoken African languages. Reproduce the chart from the bundled source data."""
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
    fig.text(.07,.96,'TIDYTUESDAY  /  2026-01-13',fontsize=9,color=ACCENT,weight='bold')
    fig.text(.07,.90,textwrap.fill('Native speakers of widely spoken African languages',48),fontsize=27,fontfamily='DejaVu Serif',va='top',linespacing=1.14)
    fig.text(.07,.77,subtitle,fontsize=10,va='top',linespacing=1.55)
    fig.text(.07,.035,textwrap.fill('Data: Wikipedia; data prepared by Muwanga Robert · TidyTuesday. Graphic: vibedatascience.',110),fontsize=8,color=MUTED,linespacing=1.5)
    return fig

def axis(fig, rect=(.24,.18,.69,.49), grid='x'):
    ax=fig.add_axes(rect,facecolor=PAPER)
    for spine in ax.spines.values():spine.set_visible(False)
    ax.tick_params(length=0,pad=8)
    if grid:ax.grid(axis=grid,color=MUTED,alpha=.16,linewidth=.7)
    ax.set_axisbelow(True)
    return ax

def save(fig):
    fig.savefig(HERE / '20260113.png',dpi=170)
    plt.close(fig)
    print('2026-01-13: saved 20260113.png')

df=read('africa')
# Each country row repeats the same Africa-wide speaker count. Count each language once.
d=df.drop_duplicates(['language','family','native_speakers']).nlargest(18,'native_speakers').sort_values('native_speakers')
assert not d.language.duplicated().any()
fig=figure('The 18 largest language entries in the supplied Wikipedia extract.\nCounts refer to native speakers within Africa, not the population of each listed country.',11)
ax=axis(fig,(.23,.16,.66,.52));v=d.native_speakers/1e6;y=np.arange(len(d))
ax.hlines(y,0,v,color=MUTED,alpha=.3,lw=2);ax.scatter(v,y,s=75,c=ACCENT,zorder=3)
ax.set_yticks(y,d.language);ax.set_xlim(0,v.max()*1.17);ax.set_xlabel('Native speakers (millions)',labelpad=12)
for i,x in enumerate(v):ax.text(x+v.max()*.02,i,f'{x:,.1f}',va='center',fontsize=9)
fig.text(.07,.08,'Repeated country entries removed. These source estimates are not a complete census of African languages.',fontsize=8,color=MUTED)
save(fig)
