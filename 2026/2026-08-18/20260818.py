"""TidyTuesday 2026-08-18: IELTS skill scores by first-language group. Reproduce the chart from the bundled source data."""
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
    fig.text(.07,.96,'TIDYTUESDAY  /  2026-08-18',fontsize=9,color=ACCENT,weight='bold')
    fig.text(.07,.90,textwrap.fill('IELTS skill scores by first-language group',48),fontsize=27,fontfamily='DejaVu Serif',va='top',linespacing=1.14)
    fig.text(.07,.77,subtitle,fontsize=10,va='top',linespacing=1.55)
    fig.text(.07,.035,textwrap.fill('Data: IELTS official test statistics · TidyTuesday. Graphic: vibedatascience.',110),fontsize=8,color=MUTED,linespacing=1.5)
    return fig

def axis(fig, rect=(.24,.18,.69,.49), grid='x'):
    ax=fig.add_axes(rect,facecolor=PAPER)
    for spine in ax.spines.values():spine.set_visible(False)
    ax.tick_params(length=0,pad=8)
    if grid:ax.grid(axis=grid,color=MUTED,alpha=.16,linewidth=.7)
    ax.set_axisbelow(True)
    return ax

def save(fig):
    fig.savefig(HERE / '20260818.png',dpi=170)
    plt.close(fig)
    print('2026-08-18: saved 20260818.png')

df=read('performance_by_first_language');year=sorted(df.year.unique())[-1]
d=df[(df.type=='Academic')&(df.year==year)]
p=d.pivot(index='language',columns='part',values='score');p=p.dropna(subset=['overall']).sort_values('overall',ascending=False)
# All language groups, sorted by supplied overall mean; scores are not weighted across groups.
fig=figure(f'Academic IELTS mean scores in {year}, grouped by candidates’ first language.\nRows are ordered by the supplied overall mean; colour uses the full 0–9 band scale.',14)
cols=['listening','reading','writing','speaking'];p=p[cols]
assert p.stack().between(0,9).all()
ax=axis(fig,(.27,.13,.56,.57),None);im=ax.imshow(p,aspect='auto',vmin=0,vmax=9,cmap=LinearSegmentedColormap.from_list('ielts',[PAPER,SECOND]))
for i in range(len(p)):
 for j in range(4):
  if pd.notna(p.iloc[i,j]):ax.text(j,i,f'{p.iloc[i,j]:.1f}',ha='center',va='center',fontsize=8,color='white' if p.iloc[i,j]>5 else INK)
ax.set_yticks(range(len(p)),p.index,fontsize=8);ax.set_xticks(range(4),['Listening','Reading','Writing','Speaking'],fontsize=9)
cax=fig.add_axes([.88,.19,.014,.42]);fig.colorbar(im,cax=cax,label='Mean IELTS band (0–9)')
fig.text(.07,.075,'These are test-taker averages, not population language proficiency. Group sample sizes and uncertainty are not supplied here.',fontsize=8,color=MUTED)
save(fig)
