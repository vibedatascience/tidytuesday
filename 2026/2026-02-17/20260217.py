"""TidyTuesday 2026-02-17: Sheep and cattle numbers in New Zealand. Reproduce the chart from the bundled source data."""
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
    fig.text(.07,.96,'TIDYTUESDAY  /  2026-02-17',fontsize=9,color=ACCENT,weight='bold')
    fig.text(.07,.90,textwrap.fill('Sheep and cattle numbers in New Zealand',48),fontsize=27,fontfamily='DejaVu Serif',va='top',linespacing=1.14)
    fig.text(.07,.77,subtitle,fontsize=10,va='top',linespacing=1.55)
    fig.text(.07,.035,textwrap.fill('Data: Stats NZ via Figure.NZ · TidyTuesday. Graphic: vibedatascience.',110),fontsize=8,color=MUTED,linespacing=1.5)
    return fig

def axis(fig, rect=(.24,.18,.69,.49), grid='x'):
    ax=fig.add_axes(rect,facecolor=PAPER)
    for spine in ax.spines.values():spine.set_visible(False)
    ax.tick_params(length=0,pad=8)
    if grid:ax.grid(axis=grid,color=MUTED,alpha=.16,linewidth=.7)
    ax.set_axisbelow(True)
    return ax

def save(fig):
    fig.savefig(HERE / '20260217.png',dpi=170)
    plt.close(fig)
    print('2026-02-17: saved 20260217.png')

df=read('dataset');names={'Total Sheep':'Sheep','Total Dairy Cattle (including Bobby Calves)':'Dairy cattle','Total Beef Cattle':'Beef cattle'}
d=df[df.measure.isin(names)].pivot(index='year_ended_june',columns='measure',values='value').sort_index();assert len(d)>20
fig=figure('Annual livestock counts, in millions of animals.\nOnly reported years are shown; breaks indicate missing observations.',9)
ax=axis(fig,(.12,.20,.69,.45),grid='y')
for (column,name),color in zip(names.items(),[ACCENT,SECOND,MUTED]):
 s=d[column].reindex(range(d.index.min(),d.index.max()+1))/1e6
 ax.plot(s.index,s,color=color,lw=2.8)
 valid=s.dropna();ax.scatter(valid.index[-1],valid.iloc[-1],color=color,s=35)
 label_y={'Sheep':valid.iloc[-1],'Dairy cattle':10,'Beef cattle':2}[name]
 ax.annotate(f'{name} {valid.iloc[-1]:.1f}m',xy=(valid.index[-1],valid.iloc[-1]),xytext=(d.index.max()+2,label_y),color=color,fontsize=9,va='center',arrowprops={'arrowstyle':'-','color':color,'lw':.8})
ax.set_xlim(d.index.min(),d.index.max()+12);ax.set_ylim(bottom=0);ax.set_xlabel('Year ended June',labelpad=12);ax.set_ylabel('Animals (millions)',labelpad=12)
fig.text(.07,.09,'Beef and dairy cattle are separate published series. Missing years remain missing; no population estimates are added.',fontsize=8,color=MUTED)
save(fig)
