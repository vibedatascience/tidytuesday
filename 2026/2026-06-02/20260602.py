"""TidyTuesday 2026-06-02: Co-parent leave duration across Europe. Reproduce the chart from the bundled source data."""
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
    fig.text(.07,.96,'TIDYTUESDAY  /  2026-06-02',fontsize=9,color=ACCENT,weight='bold')
    fig.text(.07,.90,textwrap.fill('Co-parent leave duration across Europe',48),fontsize=27,fontfamily='DejaVu Serif',va='top',linespacing=1.14)
    fig.text(.07,.77,subtitle,fontsize=10,va='top',linespacing=1.55)
    fig.text(.07,.035,textwrap.fill('Data: Spitzer et al., EPLP Dataset (2025), doi:10.5281/zenodo.17648712 · TidyTuesday. Graphic: vibedatascience.',110),fontsize=8,color=MUTED,linespacing=1.5)
    return fig

def axis(fig, rect=(.24,.18,.69,.49), grid='x'):
    ax=fig.add_axes(rect,facecolor=PAPER)
    for spine in ax.spines.values():spine.set_visible(False)
    ax.tick_params(length=0,pad=8)
    if grid:ax.grid(axis=grid,color=MUTED,alpha=.16,linewidth=.7)
    ax.set_axisbelow(True)
    return ax

def save(fig):
    fig.savefig(HERE / '20260602.png',dpi=170)
    plt.close(fig)
    print('2026-06-02: saved 20260602.png')

df=read('eplp');df['co_ld']=df.co_ld.mask(df.co_ld<0);assert not df.duplicated(['country','year']).any()
p=df.pivot(index='country',columns='year',values='co_ld');p=p.loc[p.iloc[:,-1].sort_values(ascending=False).index]
fig=figure('Maximum co-parent leave duration, in weeks, from 1970 to 2024.\nColour shows duration, not payment generosity; missing values remain blank.',10)
ax=axis(fig,(.13,.18,.73,.49),None);cmap=LinearSegmentedColormap.from_list('leave',[PAPER,SECOND]);cmap.set_bad('#d1cfc8')
im=ax.imshow(p,aspect='auto',cmap=cmap,vmin=0,vmax=np.nanmax(p))
labels={'AT':'Austria','BE':'Belgium','CH':'Switzerland','CZ':'Czechia','DE':'Germany','DK':'Denmark','ES':'Spain','FI':'Finland','FR':'France','GB':'UK','GR':'Greece','HU':'Hungary','IE':'Ireland','IS':'Iceland','IT':'Italy','LU':'Luxembourg','NL':'Netherlands','NO':'Norway','PL':'Poland','PT':'Portugal','SE':'Sweden','SK':'Slovakia','EE':'Estonia','LT':'Lithuania','SI':'Slovenia','UK':'UK'}
ax.set_yticks(range(len(p)),[labels.get(c,c) for c in p.index],fontsize=9)
inds=[i for i,y in enumerate(p.columns) if y%10==0 or y==p.columns[-1]];ax.set_xticks(inds,[p.columns[i] for i in inds])
cax=fig.add_axes([.89,.20,.018,.44]);fig.colorbar(im,cax=cax,label='Maximum duration (weeks)')
fig.text(.07,.09,'Negative not-applicable codes are treated as missing. Zero means no co-parent leave in this variable; other leave schemes may exist.',fontsize=8,color=MUTED)
save(fig)
