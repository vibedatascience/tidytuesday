"""TidyTuesday 2026-05-12: Cross-continent links between twinned cities. Reproduce the chart from the bundled source data."""
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
    fig.text(.07,.96,'TIDYTUESDAY  /  2026-05-12',fontsize=9,color=ACCENT,weight='bold')
    fig.text(.07,.90,textwrap.fill('Cross-continent links between twinned cities',48),fontsize=27,fontfamily='DejaVu Serif',va='top',linespacing=1.14)
    fig.text(.07,.77,subtitle,fontsize=10,va='top',linespacing=1.55)
    fig.text(.07,.035,textwrap.fill('Data: Wikidata / Twin Cities Explorer · TidyTuesday. Graphic: vibedatascience.',110),fontsize=8,color=MUTED,linespacing=1.5)
    return fig

def axis(fig, rect=(.24,.18,.69,.49), grid='x'):
    ax=fig.add_axes(rect,facecolor=PAPER)
    for spine in ax.spines.values():spine.set_visible(False)
    ax.tick_params(length=0,pad=8)
    if grid:ax.grid(axis=grid,color=MUTED,alpha=.16,linewidth=.7)
    ax.set_axisbelow(True)
    return ax

def save(fig):
    fig.savefig(HERE / '20260512.png',dpi=170)
    plt.close(fig)
    print('2026-05-12: saved 20260512.png')

cities=read('cities');links=read('links');assert not cities.id.duplicated().any()
# Relationships are undirected: collapse reciprocal edges and drop self-links.
edges=pd.DataFrame(np.sort(links[['source','target']].astype(str).values,axis=1),columns=['a','b']).drop_duplicates();edges=edges[edges.a!=edges.b]
m=cities.set_index('id').continent;edges['ca']=edges.a.map(m);edges['cb']=edges.b.map(m);edges=edges.dropna(subset=['ca','cb'])
continents=sorted(set(edges.ca)|set(edges.cb));p=pd.DataFrame(0,index=continents,columns=continents)
for r in edges.itertuples():
 p.loc[r.ca,r.cb]+=1
 if r.ca!=r.cb:p.loc[r.cb,r.ca]+=1
fig=figure('Unique undirected twin-city relationships, grouped by the continents of the two cities.\nThe matrix is symmetric; each within-continent edge is counted once on the diagonal.',9)
ax=axis(fig,(.20,.20,.61,.43),None);im=ax.imshow(np.log1p(p),cmap=LinearSegmentedColormap.from_list('twins',[PAPER,SECOND]))
for i in range(len(p)):
 for j in range(len(p)):ax.text(j,i,f'{p.iloc[i,j]:,}',ha='center',va='center',fontsize=10,color='white' if np.log1p(p.iloc[i,j])>np.log1p(p.values.max())*.6 else INK)
ax.set_xticks(range(len(p)),p.columns,rotation=30,ha='right',fontsize=9);ax.set_yticks(range(len(p)),p.index,fontsize=9)
fig.text(.07,.09,f'{len(edges):,} links with known continents. Colour uses log(1 + count). Coverage reflects Wikidata, not all city partnerships.',fontsize=8,color=MUTED)
save(fig)
