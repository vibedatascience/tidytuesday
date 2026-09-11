"""TidyTuesday 2026-03-24: Consecutive digit pairs in one million decimals of pi. Reproduce the chart from the bundled source data."""
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
    fig.text(.07,.96,'TIDYTUESDAY  /  2026-03-24',fontsize=9,color=ACCENT,weight='bold')
    fig.text(.07,.90,textwrap.fill('Consecutive digit pairs in one million decimals of pi',48),fontsize=27,fontfamily='DejaVu Serif',va='top',linespacing=1.14)
    fig.text(.07,.77,subtitle,fontsize=10,va='top',linespacing=1.55)
    fig.text(.07,.035,textwrap.fill('Data: One Million Digits of Pi, Eve Andersson collection · TidyTuesday. Graphic: vibedatascience.',110),fontsize=8,color=MUTED,linespacing=1.5)
    return fig

def axis(fig, rect=(.24,.18,.69,.49), grid='x'):
    ax=fig.add_axes(rect,facecolor=PAPER)
    for spine in ax.spines.values():spine.set_visible(False)
    ax.tick_params(length=0,pad=8)
    if grid:ax.grid(axis=grid,color=MUTED,alpha=.16,linewidth=.7)
    ax.set_axisbelow(True)
    return ax

def save(fig):
    fig.savefig(HERE / '20260324.png',dpi=170)
    plt.close(fig)
    print('2026-03-24: saved 20260324.png')

df=read('pi_digits').sort_values('digit_position');assert np.array_equal(df.digit_position,np.arange(1,len(df)+1))
# Position one is the integer 3; retain only the million decimal digits.
a=df.digit.to_numpy()[1:];assert len(a)==1000000 and np.isin(a,np.arange(10)).all()
c=np.bincount(a[:-1]*10+a[1:],minlength=100).reshape(10,10);assert c.sum()==len(a)-1
pct=100*c/c.sum();deviation=pct-1
fig=figure('Each cell counts a decimal digit followed immediately by another digit.\nExactly equal pair frequencies would place 1% of observations in every cell.',10)
ax=axis(fig,(.15,.16,.68,.52),None)
bound=np.abs(deviation).max();im=ax.imshow(deviation,cmap=LinearSegmentedColormap.from_list('pairs',[SECOND,PAPER,ACCENT]),vmin=-bound,vmax=bound)
for i in range(10):
 for j in range(10):ax.text(j,i,f'{c[i,j]:,}',ha='center',va='center',fontsize=8,color=INK)
ax.set_xticks(range(10));ax.set_yticks(range(10));ax.set_xlabel('Following digit',labelpad=10);ax.set_ylabel('First digit',labelpad=10)
cax=fig.add_axes([.86,.20,.018,.40]);fig.colorbar(im,cax=cax,label='Difference from 1% (percentage points)')
fig.text(.07,.09,'999,999 overlapping pairs; the integer part is excluded. Small deviations are descriptive and are not a test of normality.',fontsize=8,color=MUTED)
save(fig)
