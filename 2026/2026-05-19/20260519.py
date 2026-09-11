"""TidyTuesday 2026-05-19: Metadata participation among Crossref members. Reproduce the chart from the bundled source data."""
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
    fig.text(.07,.96,'TIDYTUESDAY  /  2026-05-19',fontsize=9,color=ACCENT,weight='bold')
    fig.text(.07,.90,textwrap.fill('Metadata participation among Crossref members',48),fontsize=27,fontfamily='DejaVu Serif',va='top',linespacing=1.14)
    fig.text(.07,.77,subtitle,fontsize=10,va='top',linespacing=1.55)
    fig.text(.07,.035,textwrap.fill('Data: Crossref country-level participation statistics · TidyTuesday. Graphic: vibedatascience.',110),fontsize=8,color=MUTED,linespacing=1.5)
    return fig

def axis(fig, rect=(.24,.18,.69,.49), grid='x'):
    ax=fig.add_axes(rect,facecolor=PAPER)
    for spine in ax.spines.values():spine.set_visible(False)
    ax.tick_params(length=0,pad=8)
    if grid:ax.grid(axis=grid,color=MUTED,alpha=.16,linewidth=.7)
    ax.set_axisbelow(True)
    return ax

def save(fig):
    fig.savefig(HERE / '20260519.png',dpi=170)
    plt.close(fig)
    print('2026-05-19: saved 20260519.png')

df=read('member_participation_stats_by_country');date=df.current_up_to.max();d=df[df.current_up_to==date].nlargest(20,'total_members').copy();assert not d.iso3_code.duplicated().any()
cols=['deposits_ref','deposits_abstract','deposits_license','acknowledges_funding','deposits_orcid','deposits_ror_id']
p=d.set_index('iso3_code')[cols].div(d.set_index('iso3_code').total_members,axis=0)*100
assert ((p>=0)&(p<=100)).all().all()
fig=figure(f'Share of members that have deposited at least one work with each metadata type, {date}.\nThe 20 countries with the most active registering members are shown.',11)
ax=axis(fig,(.18,.16,.67,.51),None);im=ax.imshow(p,aspect='auto',vmin=0,vmax=100,cmap=LinearSegmentedColormap.from_list('meta',[PAPER,SECOND]))
for i in range(len(p)):
 for j in range(len(cols)):ax.text(j,i,f'{p.iloc[i,j]:.0f}',ha='center',va='center',fontsize=8,color='white' if p.iloc[i,j]>55 else INK)
ax.set_xticks(range(6),['References','Abstracts','Licenses','Funding','ORCID','ROR'],fontsize=9);ax.set_yticks(range(len(p)),[f'{r.iso3_code}  (n={int(r.total_members):,})' for r in d.itertuples()],fontsize=9)
cax=fig.add_axes([.89,.18,.015,.45]);fig.colorbar(im,cax=cax,label='Members (%)')
fig.text(.07,.08,'Country is the member’s location, not the authors’ location. Presence on at least one work does not imply completeness of all works.',fontsize=8,color=MUTED)
save(fig)
