"""TidyTuesday 2026-01-20: Videos in the Astronomy Picture of the Day archive. Reproduce the chart from the bundled source data."""
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
    fig.text(.07,.96,'TIDYTUESDAY  /  2026-01-20',fontsize=9,color=ACCENT,weight='bold')
    fig.text(.07,.90,textwrap.fill('Videos in the Astronomy Picture of the Day archive',48),fontsize=27,fontfamily='DejaVu Serif',va='top',linespacing=1.14)
    fig.text(.07,.77,subtitle,fontsize=10,va='top',linespacing=1.55)
    fig.text(.07,.035,textwrap.fill('Data: NASA APOD archive / astropic · TidyTuesday. Graphic: vibedatascience.',110),fontsize=8,color=MUTED,linespacing=1.5)
    return fig

def axis(fig, rect=(.24,.18,.69,.49), grid='x'):
    ax=fig.add_axes(rect,facecolor=PAPER)
    for spine in ax.spines.values():spine.set_visible(False)
    ax.tick_params(length=0,pad=8)
    if grid:ax.grid(axis=grid,color=MUTED,alpha=.16,linewidth=.7)
    ax.set_axisbelow(True)
    return ax

def save(fig):
    fig.savefig(HERE / '20260120.png',dpi=170)
    plt.close(fig)
    print('2026-01-20: saved 20260120.png')

df=read('apod');df['date']=pd.to_datetime(df.date);assert not df.date.duplicated().any()
df['year']=df.date.dt.year;df['month']=df.date.dt.month;df['video']=df.media_type.eq('video')
p=df.groupby(['year','month']).video.mean().unstack().reindex(columns=range(1,13))*100
n=df.groupby(['year','month']).size().unstack().reindex_like(p)
fig=figure('Share of archived entries that are videos, by month and year.\nThe denominator includes every media type recorded in the archive.',10)
ax=axis(fig,(.13,.18,.72,.50),None)
im=ax.imshow(p,aspect='auto',cmap=LinearSegmentedColormap.from_list('video',[PAPER,ACCENT]),vmin=0,vmax=max(25,p.max().max()))
ax.set_xticks(range(12),['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],fontsize=9)
ax.set_yticks(range(len(p)),p.index);ax.tick_params(length=0)
for i in range(len(p)):
 for j in range(12):
  if pd.notna(p.iloc[i,j]):ax.text(j,i,f'{p.iloc[i,j]:.0f}',ha='center',va='center',fontsize=7,color=INK)
cax=fig.add_axes([.88,.18,.015,.50]);fig.colorbar(im,cax=cax,label='Video entries (%)')
fig.text(.07,.09,f'{len(df):,} archive records. Missing dates are not filled with assumed images. Cell labels are percentages.',fontsize=8,color=MUTED)
save(fig)
