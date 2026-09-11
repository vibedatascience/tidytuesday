"""TidyTuesday 2026-07-07: How UFC fights ended over time. Reproduce the chart from the bundled source data."""
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
    fig.text(.07,.96,'TIDYTUESDAY  /  2026-07-07',fontsize=9,color=ACCENT,weight='bold')
    fig.text(.07,.90,textwrap.fill('How UFC fights ended over time',48),fontsize=27,fontfamily='DejaVu Serif',va='top',linespacing=1.14)
    fig.text(.07,.77,subtitle,fontsize=10,va='top',linespacing=1.55)
    fig.text(.07,.035,textwrap.fill('Data: UFCStats via fightr · TidyTuesday. Graphic: vibedatascience.',110),fontsize=8,color=MUTED,linespacing=1.5)
    return fig

def axis(fig, rect=(.24,.18,.69,.49), grid='x'):
    ax=fig.add_axes(rect,facecolor=PAPER)
    for spine in ax.spines.values():spine.set_visible(False)
    ax.tick_params(length=0,pad=8)
    if grid:ax.grid(axis=grid,color=MUTED,alpha=.16,linewidth=.7)
    ax.set_axisbelow(True)
    return ax

def save(fig):
    fig.savefig(HERE / '20260707.png',dpi=170)
    plt.close(fig)
    print('2026-07-07: saved 20260707.png')

df=read('ufc_fights').drop_duplicates('fight_url');df['date']=pd.to_datetime(df.date);df['year']=df.date.dt.year
# Restrict to complete years. Preserve nonstandard outcomes as Other.
d=df[df.year.between(1995,2025)].copy();d['period']=(d.year//5*5).astype(int)
def method(s):
 if str(s).startswith('Decision'):return 'Decision'
 if s in ['KO/TKO',"TKO - Doctor's Stoppage"]:return 'KO / TKO'
 if s=='Submission':return 'Submission'
 return 'Other'
d['outcome']=d.method.map(method);counts=pd.crosstab(d.period,d.outcome).reindex(columns=['KO / TKO','Submission','Decision','Other'],fill_value=0);pct=counts.div(counts.sum(axis=1),axis=0)*100
# 2025 alone is a partial five-year bin, so omit it from the five-year comparison.
pct=pct[pct.index<=2020];counts=counts.loc[pct.index]
fig=figure('Share of recorded fight outcomes in five-year groups, 1995–2024.\nEach fight is counted once. Doctor stoppages are grouped with KO/TKO.',9)
ax=axis(fig,(.15,.22,.73,.40),None);bottom=np.zeros(len(pct))
for col,color in zip(pct.columns,[ACCENT,SECOND,'#79879c','#c5c7c1']):
 ax.bar(range(len(pct)),pct[col],bottom=bottom,color=color,width=.65,label=col)
 for i,v in enumerate(pct[col]):
  if v>=10:ax.text(i,bottom[i]+v/2,f'{v:.0f}%',ha='center',va='center',color='white',fontsize=10)
 bottom+=pct[col].to_numpy()
assert np.allclose(bottom,100)
ax.set_xticks(range(len(pct)),[f'{y}–{str(y+4)[-2:]}\nn={int(counts.loc[y].sum()):,}' for y in pct.index],fontsize=9);ax.set_ylim(0,100);ax.set_ylabel('Fights (%)');ax.legend(loc='lower center',bbox_to_anchor=(.5,1.04),ncol=4,frameon=False,fontsize=9)
fig.text(.07,.10,'Other includes overturned results, disqualifications and nonstandard endings. Weight-class and rule changes are not controlled for.',fontsize=8,color=MUTED)
save(fig)
