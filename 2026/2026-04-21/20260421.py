"""TidyTuesday 2026-04-21: Household payments as a share of health spending. Reproduce the chart from the bundled source data."""
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
    fig.text(.07,.96,'TIDYTUESDAY  /  2026-04-21',fontsize=9,color=ACCENT,weight='bold')
    fig.text(.07,.90,textwrap.fill('Household payments as a share of health spending',48),fontsize=27,fontfamily='DejaVu Serif',va='top',linespacing=1.14)
    fig.text(.07,.77,subtitle,fontsize=10,va='top',linespacing=1.55)
    fig.text(.07,.035,textwrap.fill('Data: WHO Global Health Expenditure Database · TidyTuesday. Graphic: vibedatascience.',110),fontsize=8,color=MUTED,linespacing=1.5)
    return fig

def axis(fig, rect=(.24,.18,.69,.49), grid='x'):
    ax=fig.add_axes(rect,facecolor=PAPER)
    for spine in ax.spines.values():spine.set_visible(False)
    ax.tick_params(length=0,pad=8)
    if grid:ax.grid(axis=grid,color=MUTED,alpha=.16,linewidth=.7)
    ax.set_axisbelow(True)
    return ax

def save(fig):
    fig.savefig(HERE / '20260421.png',dpi=170)
    plt.close(fig)
    print('2026-04-21: saved 20260421.png')

df=read('financing_schemes');d=df[df.indicator_code.eq('hf3_che')].dropna(subset=['value']);year=int(d.year.max());d=d[d.year==year].nlargest(20,'value').sort_values('value')
assert d.value.between(0,100).all() and not d.iso3_code.duplicated().any()
fig=figure(f'The 20 highest reported shares of household out-of-pocket payments in {year}.\nValues are percentages of current health expenditure, not percentages of household income.',11)
ax=axis(fig,(.27,.16,.63,.53));y=np.arange(len(d));ax.barh(y,d.value,color=SECOND,height=.65)
for i,v in enumerate(d.value):ax.text(v+1,i,f'{v:.1f}%',va='center',fontsize=9)
ax.set_yticks(y,d.country_name,fontsize=9);ax.set_xlim(0,100);ax.set_xlabel('Out-of-pocket share of current health spending (%)',labelpad=12)
fig.text(.07,.08,'Countries without a reported value in the selected year are excluded. Spending shares do not measure access or quality of care.',fontsize=8,color=MUTED)
save(fig)
