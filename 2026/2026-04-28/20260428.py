"""TidyTuesday 2026-04-28: Duty-free agricultural tariff lines by product chapter. Reproduce the chart from the bundled source data."""
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
    fig.text(.07,.96,'TIDYTUESDAY  /  2026-04-28',fontsize=9,color=ACCENT,weight='bold')
    fig.text(.07,.90,textwrap.fill('Duty-free agricultural tariff lines by product chapter',48),fontsize=27,fontfamily='DejaVu Serif',va='top',linespacing=1.14)
    fig.text(.07,.77,subtitle,fontsize=10,va='top',linespacing=1.55)
    fig.text(.07,.035,textwrap.fill('Data: US International Trade Commission · TidyTuesday. Graphic: vibedatascience.',110),fontsize=8,color=MUTED,linespacing=1.5)
    return fig

def axis(fig, rect=(.24,.18,.69,.49), grid='x'):
    ax=fig.add_axes(rect,facecolor=PAPER)
    for spine in ax.spines.values():spine.set_visible(False)
    ax.tick_params(length=0,pad=8)
    if grid:ax.grid(axis=grid,color=MUTED,alpha=.16,linewidth=.7)
    ax.set_axisbelow(True)
    return ax

def save(fig):
    fig.savefig(HERE / '20260428.png',dpi=170)
    plt.close(fig)
    print('2026-04-28: saved 20260428.png')

df=read('tariff_agricultural');date='2025-01-01'
d=df[(df.agreement=='mfn')&(df.begin_effective_date<=date)&(df.end_effective_date>=date)].copy()
# Prefer the most recently effective record if histories overlap for an HTS code.
d=d.sort_values('begin_effective_date').drop_duplicates('hts8',keep='last');d['chapter']=d.hts8.astype(str).str.zfill(8).str[:2]
# Rate-type 0 explicitly means free; do not mistake a zero ad-valorem component for duty-free.
d['free']=d.rate_type_code.astype(str).eq('0')
p=d.groupby('chapter').agg(n=('hts8','size'),free=('free','sum'));p['pct']=100*p.free/p.n
labels=['Live animals','Meat','Fish & seafood','Dairy, eggs & honey','Other animal products','Live plants','Vegetables','Fruit & nuts','Coffee, tea & spices','Cereals','Milling products','Oil seeds & plants','Lac, gums & resins','Vegetable plaiting','Fats & oils','Meat & fish preparations','Sugar','Cocoa','Cereal preparations','Vegetable & fruit preparations','Other food preparations','Beverages','Food residues & feed','Tobacco']
fig=figure('MFN tariff lines explicitly marked duty-free on 1 January 2025.\nEach tariff line has equal weight; import values are not used.',12)
ax=axis(fig,(.34,.15,.52,.53));y=np.arange(len(p));ax.barh(y,p.pct,color=ACCENT,height=.62)
ax.set_yticks(y,[f'{c}  {labels[int(c)-1]}' for c in p.index],fontsize=9);ax.invert_yaxis();ax.set_xlim(0,110);ax.set_xticks([0,25,50,75,100]);ax.set_xlabel('Duty-free tariff lines (%)',labelpad=12)
for i,r in enumerate(p.itertuples()):ax.text(r.pct+1,i,f'{r.pct:.0f}%  ({r.free}/{r.n})',va='center',fontsize=8)
fig.text(.07,.08,'MFN schedule only. Specific, compound, conditional and other rate types are not treated as free; extra duties are not included.',fontsize=8,color=MUTED)
save(fig)
