"""TidyTuesday 2026-04-07: Repair outcomes by type of item. Reproduce the chart from the bundled source data."""
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
    fig.text(.07,.96,'TIDYTUESDAY  /  2026-04-07',fontsize=9,color=ACCENT,weight='bold')
    fig.text(.07,.90,textwrap.fill('Repair outcomes by type of item',48),fontsize=27,fontfamily='DejaVu Serif',va='top',linespacing=1.14)
    fig.text(.07,.77,subtitle,fontsize=10,va='top',linespacing=1.55)
    fig.text(.07,.035,textwrap.fill('Data: Repair Monitor · TidyTuesday. Graphic: vibedatascience.',110),fontsize=8,color=MUTED,linespacing=1.5)
    return fig

def axis(fig, rect=(.24,.18,.69,.49), grid='x'):
    ax=fig.add_axes(rect,facecolor=PAPER)
    for spine in ax.spines.values():spine.set_visible(False)
    ax.tick_params(length=0,pad=8)
    if grid:ax.grid(axis=grid,color=MUTED,alpha=.16,linewidth=.7)
    ax.set_axisbelow(True)
    return ax

def save(fig):
    fig.savefig(HERE / '20260407.png',dpi=170)
    plt.close(fig)
    print('2026-04-07: saved 20260407.png')

df=read('repairs');df=df.loc[~df.repair_id.duplicated(keep=False)].copy();df['outcome']=df.repaired.replace({'ja':'yes'});d=df[df.outcome.isin(['yes','half','no'])]
assert not d.repair_id.duplicated().any()
top=d.kind_of_product.value_counts().head(15).index
counts=pd.crosstab(d.kind_of_product,d.outcome).reindex(top).reindex(columns=['yes','half','no'],fill_value=0)
pct=counts.div(counts.sum(axis=1),axis=0)*100;order=pct.yes.sort_values().index;pct=pct.loc[order];counts=counts.loc[order]
fig=figure('The 15 most frequently recorded product types with a known outcome.\nEach bar represents 100% of recorded repairs for that product type.',11)
ax=axis(fig,(.29,.18,.57,.48),None);left=np.zeros(len(pct))
for col,color,label in zip(['yes','half','no'],[ACCENT,SECOND,'#c8c5bc'],['Repaired','Partly repaired','Not repaired']):
 ax.barh(np.arange(len(pct)),pct[col],left=left,color=color,height=.67,label=label)
 if col=='yes':
  for i,v in enumerate(pct[col]):ax.text(v/2,i,f'{v:.0f}%',ha='center',va='center',color='white',fontsize=9)
 left+=pct[col].to_numpy()
assert np.allclose(left,100)
ax.set_yticks(range(len(pct)),pct.index,fontsize=9);ax.set_xlim(0,100);ax.set_xticks([0,25,50,75,100]);ax.set_xlabel('Share of recorded repairs (%)',labelpad=12)
for i,v in enumerate(counts.sum(axis=1)):ax.text(102,i,f'n={v:,}',va='center',fontsize=8)
ax.legend(loc='lower left',bbox_to_anchor=(0,1.02),frameon=False,ncol=3,fontsize=8)
fig.text(.07,.09,'“ja” means “yes”; ambiguous IDs and unknown outcomes excluded. Product mix, damage and participating cafés affect these comparisons.',fontsize=8,color=MUTED)
save(fig)
