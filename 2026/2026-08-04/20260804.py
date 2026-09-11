"""TidyTuesday 2026-08-04: Recorded imports of Lesotho wool by destination. Reproduce the chart from the bundled source data."""
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
    fig.text(.07,.96,'TIDYTUESDAY  /  2026-08-04',fontsize=9,color=ACCENT,weight='bold')
    fig.text(.07,.90,textwrap.fill('Recorded imports of Lesotho wool by destination',48),fontsize=27,fontfamily='DejaVu Serif',va='top',linespacing=1.14)
    fig.text(.07,.77,subtitle,fontsize=10,va='top',linespacing=1.55)
    fig.text(.07,.035,textwrap.fill('Data: UN Comtrade mirror trade statistics · TidyTuesday. Graphic: vibedatascience.',110),fontsize=8,color=MUTED,linespacing=1.5)
    return fig

def axis(fig, rect=(.24,.18,.69,.49), grid='x'):
    ax=fig.add_axes(rect,facecolor=PAPER)
    for spine in ax.spines.values():spine.set_visible(False)
    ax.tick_params(length=0,pad=8)
    if grid:ax.grid(axis=grid,color=MUTED,alpha=.16,linewidth=.7)
    ax.set_axisbelow(True)
    return ax

def save(fig):
    fig.savefig(HERE / '20260804.png',dpi=170)
    plt.close(fig)
    print('2026-08-04: saved 20260804.png')

df=read('basotho_wool');d=df[(df.cmd_code==5101)&(df.flow_code=='M')].copy();assert d.primary_value.ge(0).all()
assert not d.duplicated(['ref_year','ref_month','reporter_iso','cmd_code']).any()
p=d.pivot_table(index='ref_year',columns='reporter_desc',values='primary_value',aggfunc='sum',dropna=False).sort_index()/1e6
fig=figure('Annual primary trade value reported by importing partners, for uncarded wool (HS 5101).\nThese mirror records describe reported imports from Lesotho, in nominal US dollars.',9)
ax=axis(fig,(.13,.22,.69,.43),grid='y')
for (country,s),color in zip(p.items(),[ACCENT,SECOND,'#8c729f','#a18e64']):
 ax.plot(s.index,s,color=color,lw=2.7,marker='o',ms=3,label=country)
ax.set_ylim(bottom=0);ax.set_ylabel('Recorded import value (USD millions)');ax.set_xlabel('Year',labelpad=12);ax.legend(frameon=False,fontsize=9)
fig.text(.07,.10,'Missing country-years are gaps, not zero trade. Annual totals sum available months; reporting completeness may vary.',fontsize=8,color=MUTED)
save(fig)
