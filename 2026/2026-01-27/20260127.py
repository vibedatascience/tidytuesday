"""TidyTuesday 2026-01-27: Declared capital by company size in Brazil. Reproduce the chart from the bundled source data."""
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
    fig.text(.07,.96,'TIDYTUESDAY  /  2026-01-27',fontsize=9,color=ACCENT,weight='bold')
    fig.text(.07,.90,textwrap.fill('Declared capital by company size in Brazil',48),fontsize=27,fontfamily='DejaVu Serif',va='top',linespacing=1.14)
    fig.text(.07,.77,subtitle,fontsize=10,va='top',linespacing=1.55)
    fig.text(.07,.035,textwrap.fill('Data: Receita Federal CNPJ registry · TidyTuesday. Graphic: vibedatascience.',110),fontsize=8,color=MUTED,linespacing=1.5)
    return fig

def axis(fig, rect=(.24,.18,.69,.49), grid='x'):
    ax=fig.add_axes(rect,facecolor=PAPER)
    for spine in ax.spines.values():spine.set_visible(False)
    ax.tick_params(length=0,pad=8)
    if grid:ax.grid(axis=grid,color=MUTED,alpha=.16,linewidth=.7)
    ax.set_axisbelow(True)
    return ax

def save(fig):
    fig.savefig(HERE / '20260127.png',dpi=170)
    plt.close(fig)
    print('2026-01-27: saved 20260127.png')

df=read('companies');assert not df.company_id.duplicated().any()
order=['micro-enterprise','small-enterprise','other'];d=df.loc[df.capital_stock.gt(0)&df.company_size.isin(order)].copy()
fig=figure('Distributions of positive declared share capital in the supplied company extract.\nThe horizontal axis is logarithmic: equal distances represent tenfold changes.',9)
ax=axis(fig,(.21,.23,.71,.42))
for i,group in enumerate(order):
 vals=np.log10(d.loc[d.company_size==group,'capital_stock']);assert len(vals)>10
 parts=ax.violinplot([vals],positions=[i],vert=False,widths=.65,showextrema=False)
 for b in parts['bodies']:b.set_facecolor([ACCENT,SECOND,MUTED][i]);b.set_alpha(.75)
 q=vals.quantile([.25,.5,.75]);ax.plot([q.iloc[0],q.iloc[2]],[i,i],color=INK,lw=3);ax.scatter(q.iloc[1],i,color=PAPER,s=28,zorder=3)
 ax.text(10.6,i,f'n={len(vals):,}',fontsize=9,va='center')
ax.set_yticks(range(3),['Micro-enterprise','Small enterprise','Other']);ax.invert_yaxis();ax.set_xlim(-1,11.5)
ax.set_xticks([0,2,4,6,8,10],['1','100','10,000','1 million','100 million','10 billion']);ax.set_xlabel('Declared share capital (BRL, logarithmic scale)',labelpad=14)
fig.text(.07,.10,f'{len(df)-len(d):,} zero, missing or out-of-scope records omitted. White dots: medians; dark segments: middle 50%.',fontsize=8,color=MUTED)
save(fig)
