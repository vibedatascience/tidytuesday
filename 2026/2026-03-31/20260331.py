"""TidyTuesday 2026-03-31: Seasonal ocean temperatures at different depths. Reproduce the chart from the bundled source data."""
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
    fig.text(.07,.96,'TIDYTUESDAY  /  2026-03-31',fontsize=9,color=ACCENT,weight='bold')
    fig.text(.07,.90,textwrap.fill('Seasonal ocean temperatures at different depths',48),fontsize=27,fontfamily='DejaVu Serif',va='top',linespacing=1.14)
    fig.text(.07,.77,subtitle,fontsize=10,va='top',linespacing=1.55)
    fig.text(.07,.035,textwrap.fill('Data: Nova Scotia coastal monitoring, Lunenburg County · TidyTuesday. Graphic: vibedatascience.',110),fontsize=8,color=MUTED,linespacing=1.5)
    return fig

def axis(fig, rect=(.24,.18,.69,.49), grid='x'):
    ax=fig.add_axes(rect,facecolor=PAPER)
    for spine in ax.spines.values():spine.set_visible(False)
    ax.tick_params(length=0,pad=8)
    if grid:ax.grid(axis=grid,color=MUTED,alpha=.16,linewidth=.7)
    ax.set_axisbelow(True)
    return ax

def save(fig):
    fig.savefig(HERE / '20260331.png',dpi=170)
    plt.close(fig)
    print('2026-03-31: saved 20260331.png')

df=read('ocean_temperature');df['date']=pd.to_datetime(df.date);df['month']=df.date.dt.month
assert not df.duplicated(['date','sensor_depth_at_low_tide_m']).any()
p=df.groupby(['sensor_depth_at_low_tide_m','month']).mean_temperature_degree_c.mean().unstack().reindex(columns=range(1,13))
fig=figure('Mean of the reported daily temperatures for each calendar month, pooled across years.\nAll seven sensor depths use the same temperature scale.',9)
ax=axis(fig,(.14,.24,.72,.36),None)
im=ax.imshow(p,aspect='auto',cmap=LinearSegmentedColormap.from_list('sea',[ACCENT,PAPER,SECOND]))
for i in range(len(p)):
 for j in range(12):
  if pd.notna(p.iloc[i,j]):ax.text(j,i,f'{p.iloc[i,j]:.1f}',ha='center',va='center',fontsize=10)
ax.set_yticks(range(len(p)),[f'{x} m' for x in p.index]);ax.set_xticks(range(12),['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']);ax.set_ylabel('Sensor depth at low tide',labelpad=12)
cax=fig.add_axes([.89,.24,.016,.36]);fig.colorbar(im,cax=cax,label='Temperature (°C)')
fig.text(.07,.10,f'Recorded dates: {df.date.min():%Y-%m-%d} to {df.date.max():%Y-%m-%d}. Each daily mean has equal weight; coverage varies by depth.',fontsize=8,color=MUTED)
save(fig)
