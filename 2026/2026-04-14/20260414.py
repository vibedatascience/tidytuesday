"""TidyTuesday 2026-04-14: Where seabirds were recorded at sea. Reproduce the chart from the bundled source data."""
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
    fig.text(.07,.96,'TIDYTUESDAY  /  2026-04-14',fontsize=9,color=ACCENT,weight='bold')
    fig.text(.07,.90,textwrap.fill('Where seabirds were recorded at sea',48),fontsize=27,fontfamily='DejaVu Serif',va='top',linespacing=1.14)
    fig.text(.07,.77,subtitle,fontsize=10,va='top',linespacing=1.55)
    fig.text(.07,.035,textwrap.fill('Data: At-Sea Observations of Seabirds, New Zealand · TidyTuesday. Graphic: vibedatascience.',110),fontsize=8,color=MUTED,linespacing=1.5)
    return fig

def axis(fig, rect=(.24,.18,.69,.49), grid='x'):
    ax=fig.add_axes(rect,facecolor=PAPER)
    for spine in ax.spines.values():spine.set_visible(False)
    ax.tick_params(length=0,pad=8)
    if grid:ax.grid(axis=grid,color=MUTED,alpha=.16,linewidth=.7)
    ax.set_axisbelow(True)
    return ax

def save(fig):
    fig.savefig(HERE / '20260414.png',dpi=170)
    plt.close(fig)
    print('2026-04-14: saved 20260414.png')

birds=read('birds');ships=read('ships');assert not ships.record_id.duplicated().any()
n=birds.groupby('record_id').size().rename('records')
d=ships.join(n,on='record_id').dropna(subset=['latitude','longitude','records'])
# Source longitude is an unsigned magnitude with a separate E/W field.
d['lon_east']=np.where(d.hemisphere.eq('W'),360-d.longitude,d.longitude)
assert d.latitude.between(-90,90).all() and d.lon_east.between(0,360).all()
fig=figure('Survey positions with at least one bird record. Larger circles indicate more species-observation records.\nThis shows the footprint of the survey, not a map of seabird abundance.',10)
ax=axis(fig,(.10,.16,.80,.52),grid='both')
ax.scatter(d.lon_east,d.latitude,s=np.sqrt(d.records)*3,color=SECOND,alpha=.24,edgecolors='none')
ax.set_xlim(40,200);ax.set_ylim(-72,-15);ax.set_aspect(1/np.cos(np.deg2rad(45)))
ax.set_xticks([60,90,120,150,180],['60°E','90°E','120°E','150°E','180°']);ax.set_yticks([-70,-60,-50,-40,-30,-20],['70°S','60°S','50°S','40°S','30°S','20°S'])
ax.set_xlabel('Longitude',labelpad=10);ax.set_ylabel('Latitude',labelpad=10)
fig.text(.07,.085,f'{len(d):,} survey positions. Circle area scales with the square root of record count; repeated positions can overlap.',fontsize=8,color=MUTED)
save(fig)
