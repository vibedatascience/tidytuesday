"""TidyTuesday 2026-02-24: Research grant commitments in Ireland. Reproduce the chart from the bundled source data."""
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
    fig.text(.07,.96,'TIDYTUESDAY  /  2026-02-24',fontsize=9,color=ACCENT,weight='bold')
    fig.text(.07,.90,textwrap.fill('Research grant commitments in Ireland',48),fontsize=27,fontfamily='DejaVu Serif',va='top',linespacing=1.14)
    fig.text(.07,.77,subtitle,fontsize=10,va='top',linespacing=1.55)
    fig.text(.07,.035,textwrap.fill('Data: Science Foundation Ireland historical grants · TidyTuesday. Graphic: vibedatascience.',110),fontsize=8,color=MUTED,linespacing=1.5)
    return fig

def axis(fig, rect=(.24,.18,.69,.49), grid='x'):
    ax=fig.add_axes(rect,facecolor=PAPER)
    for spine in ax.spines.values():spine.set_visible(False)
    ax.tick_params(length=0,pad=8)
    if grid:ax.grid(axis=grid,color=MUTED,alpha=.16,linewidth=.7)
    ax.set_axisbelow(True)
    return ax

def save(fig):
    fig.savefig(HERE / '20260224.png',dpi=170)
    plt.close(fig)
    print('2026-02-24: saved 20260224.png')

df=read('sfi_grants');df['year']=pd.to_datetime(df.start_date).dt.year
assert np.isfinite(df.current_total_commitment).all()  # Retain signed commitments, including negative records.
top=df.groupby('research_body').current_total_commitment.sum().nlargest(6).index
fig=figure('The six research bodies with the largest total commitments in the supplied records.\nBars assign the full grant value to its start year; they are not annual spending.',11)
short={'Trinity College Dublin (TCD)':'Trinity College Dublin','University College Dublin (UCD)':'University College Dublin','University College Cork (UCC)':'University College Cork','University of Galway (NUIG)':'University of Galway'}
years=range(int(df.year.min()),int(df.year.max())+1)
maximum=max(df[df.research_body.isin(top)].groupby(['research_body','year']).current_total_commitment.sum())/1e6
for i,name in enumerate(top):
 ax=axis(fig,(.10+(i%2)*.46,.49-(i//2)*.16,.37,.12),grid='y')
 s=df.loc[df.research_body==name].groupby('year').current_total_commitment.sum().reindex(years,fill_value=0)/1e6
 ax.bar(s.index,s,color=ACCENT if i==0 else SECOND,width=.8)
 ax.set_ylim(min(0,s.min())*1.1,maximum*1.08);ax.set_title(textwrap.fill(short.get(name,name),34),loc='left',fontsize=10,color=INK,pad=6)
 ax.set_xticks([2005,2015,2024]);ax.tick_params(labelsize=8)
fig.text(.10,.085,'Grant commitments by start year (EUR millions). Signed values, including negative records, retained. Nominal values.',fontsize=8,color=MUTED)
save(fig)
