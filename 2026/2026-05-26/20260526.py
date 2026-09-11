"""TidyTuesday 2026-05-26: The rural–urban gap in electricity access. Reproduce the chart from the bundled source data."""
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
    fig.text(.07,.96,'TIDYTUESDAY  /  2026-05-26',fontsize=9,color=ACCENT,weight='bold')
    fig.text(.07,.90,textwrap.fill('The rural–urban gap in electricity access',48),fontsize=27,fontfamily='DejaVu Serif',va='top',linespacing=1.14)
    fig.text(.07,.77,subtitle,fontsize=10,va='top',linespacing=1.55)
    fig.text(.07,.035,textwrap.fill('Data: SE4ALL / World Bank · TidyTuesday. Graphic: vibedatascience.',110),fontsize=8,color=MUTED,linespacing=1.5)
    return fig

def axis(fig, rect=(.24,.18,.69,.49), grid='x'):
    ax=fig.add_axes(rect,facecolor=PAPER)
    for spine in ax.spines.values():spine.set_visible(False)
    ax.tick_params(length=0,pad=8)
    if grid:ax.grid(axis=grid,color=MUTED,alpha=.16,linewidth=.7)
    ax.set_axisbelow(True)
    return ax

def save(fig):
    fig.savefig(HERE / '20260526.png',dpi=170)
    plt.close(fig)
    print('2026-05-26: saved 20260526.png')

df=read('energy_cleaned')
aggregates={'Caucasus and Central Asia','Eastern Asia (including Japan)','Eastern Asia (not including Japan)','Eastern Europe','Europe','High income','High income: OECD','High income: nonOECD','Latin America and Caribbean','Low & middle income','Low income','Lower middle income','Middle income','Northern Africa','Nothern America','Oceania','Oceania (not including Australia and New Zealand)','South Eastern Asia','Southern Asia','Sub-Saharan Africa','Upper middle income','Western Asia','World'}
df=df.loc[~df.country_name.isin(aggregates)]
a='access_electricity_rural_pop_pct';b='access_electricity_urban_pop_pct'
d=df.dropna(subset=[a,b]);year=int(d.yr.max());d=d[d.yr==year].copy();d['gap']=d[b]-d[a];d=d.nlargest(20,'gap').sort_values('gap')
assert d[[a,b]].ge(0).all().all() and d[[a,b]].le(100.01).all().all()
fig=figure(f'The 20 largest urban-minus-rural gaps among countries with paired estimates in {year}.\nEach line connects access rates for rural and urban residents.',11)
ax=axis(fig,(.28,.16,.62,.50));y=np.arange(len(d));ax.hlines(y,d[a],d[b],color=MUTED,alpha=.5,lw=2)
ax.scatter(d[a],y,s=42,color=ACCENT,label='Rural',zorder=3);ax.scatter(d[b],y,s=42,color=SECOND,label='Urban',zorder=3)
ax.set_yticks(y,d.country_name,fontsize=9);ax.set_xlim(0,104);ax.set_xticks([0,25,50,75,100]);ax.set_xlabel('Population with electricity access (%)',labelpad=12);ax.legend(frameon=False,loc='lower center',bbox_to_anchor=(.5,1.02),ncol=2)
fig.text(.07,.08,'A gap is a percentage-point difference, not a population count. Countries with missing rural or urban estimates are excluded.',fontsize=8,color=MUTED)
save(fig)
