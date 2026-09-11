"""TidyTuesday 2026-05-05: Passenger-car production in Italy. Reproduce the chart from the bundled source data."""
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
    fig.text(.07,.96,'TIDYTUESDAY  /  2026-05-05',fontsize=9,color=ACCENT,weight='bold')
    fig.text(.07,.90,textwrap.fill('Passenger-car production in Italy',48),fontsize=27,fontfamily='DejaVu Serif',va='top',linespacing=1.14)
    fig.text(.07,.77,subtitle,fontsize=10,va='top',linespacing=1.55)
    fig.text(.07,.035,textwrap.fill('Data: ISTAT historical industrial production series · TidyTuesday. Graphic: vibedatascience.',110),fontsize=8,color=MUTED,linespacing=1.5)
    return fig

def axis(fig, rect=(.24,.18,.69,.49), grid='x'):
    ax=fig.add_axes(rect,facecolor=PAPER)
    for spine in ax.spines.values():spine.set_visible(False)
    ax.tick_params(length=0,pad=8)
    if grid:ax.grid(axis=grid,color=MUTED,alpha=.16,linewidth=.7)
    ax.set_axisbelow(True)
    return ax

def save(fig):
    fig.savefig(HERE / '20260505.png',dpi=170)
    plt.close(fig)
    print('2026-05-05: saved 20260505.png')

df=read('transport');d=df[['Year','Passenger_cars']].dropna().sort_values('Year');assert d.Passenger_cars.ge(0).all()
fig=figure('Annual passenger-car production in the historical ISTAT series.\nThe shaded period marks the Second World War; it is context, not a causal estimate.',9)
ax=axis(fig,(.12,.20,.77,.46),grid='y');ax.axvspan(1939,1945,color=MUTED,alpha=.15)
ax.fill_between(d.Year,d.Passenger_cars/1e6,color=ACCENT,alpha=.18);ax.plot(d.Year,d.Passenger_cars/1e6,color=ACCENT,lw=3)
peak=d.loc[d.Passenger_cars.idxmax()];ax.scatter(peak.Year,peak.Passenger_cars/1e6,color=INK,zorder=4)
ax.annotate(f'{int(peak.Year)}: {peak.Passenger_cars/1e6:.2f} million',xy=(peak.Year,peak.Passenger_cars/1e6),xytext=(peak.Year-30,peak.Passenger_cars/1e6*.88),arrowprops={'arrowstyle':'-','color':MUTED},fontsize=10)
ax.set_ylim(bottom=0);ax.set_ylabel('Passenger cars produced (millions)');ax.set_xlabel('Year',labelpad=12)
fig.text(.07,.09,f'Series shown: {int(d.Year.min())}–{int(d.Year.max())}. Years without a published value are omitted.',fontsize=8,color=MUTED)
save(fig)
