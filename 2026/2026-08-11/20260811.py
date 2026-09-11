"""TidyTuesday 2026-08-11: Emission-line ratios in nearby galactic nuclei. Reproduce the chart from the bundled source data."""
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
PAPER, INK, MUTED, ACCENT, SECOND = ('#142435', '#edf1ee', '#a3b3bc', '#e4b65c', '#58b7b0')
plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':10, 'text.color':INK,
 'axes.labelcolor':INK, 'xtick.color':MUTED, 'ytick.color':MUTED,
 'axes.edgecolor':MUTED, 'savefig.facecolor':PAPER})

def read(name):
    data = pd.read_csv(HERE / 'data' / (name + '.csv.gz'), low_memory=False)
    assert len(data), 'Empty source data'
    return data

def figure(subtitle, height=9):
    fig = plt.figure(figsize=(11,height), facecolor=PAPER)
    fig.text(.07,.96,'TIDYTUESDAY  /  2026-08-11',fontsize=9,color=ACCENT,weight='bold')
    fig.text(.07,.90,textwrap.fill('Emission-line ratios in nearby galactic nuclei',48),fontsize=27,fontfamily='DejaVu Serif',va='top',linespacing=1.14)
    fig.text(.07,.77,subtitle,fontsize=10,va='top',linespacing=1.55)
    fig.text(.07,.035,textwrap.fill('Data: Ho, Filippenko & Sargent; Palomar spectroscopic survey · TidyTuesday. Graphic: vibedatascience.',110),fontsize=8,color=MUTED,linespacing=1.5)
    return fig

def axis(fig, rect=(.24,.18,.69,.49), grid='x'):
    ax=fig.add_axes(rect,facecolor=PAPER)
    for spine in ax.spines.values():spine.set_visible(False)
    ax.tick_params(length=0,pad=8)
    if grid:ax.grid(axis=grid,color=MUTED,alpha=.16,linewidth=.7)
    ax.set_axisbelow(True)
    return ax

def save(fig):
    fig.savefig(HERE / '20260811.png',dpi=170)
    plt.close(fig)
    print('2026-08-11: saved 20260811.png')

df=read('palomar_survey');d=df.dropna(subset=['log_nii_ha','log_oiii_hb','activity_type']).copy()
# Despite their names these columns contain linear ratios: confirmed by the source dictionary and cleaning script.
assert d.log_nii_ha.gt(0).all() and d.log_oiii_hb.gt(0).all()
d['log_nii_ha']=np.log10(d.log_nii_ha);d['log_oiii_hb']=np.log10(d.log_oiii_hb)
fig=figure('The [N II]/Hα and [O III]/Hβ line-ratio plane for galaxies with both measurements.\nColours show the activity classifications supplied with the survey.',9)
ax=axis(fig,(.13,.20,.62,.46),grid='both')
colors={'H II':SECOND,'Transition':'#af9768','LINER':ACCENT,'Seyfert':'#a185ce','Absorption':MUTED}
for label,color in colors.items():
 g=d[d.activity_type==label]
 if len(g):ax.scatter(g.log_nii_ha,g.log_oiii_hb,s=28,color=color,alpha=.65,edgecolors='none',label=f'{label} (n={len(g)})')
ax.set_xlabel('log₁₀([N II] λ6583 / Hα)',labelpad=12);ax.set_ylabel('log₁₀([O III] λ5007 / Hβ)',labelpad=12)
ax.legend(frameon=False,loc='center left',bbox_to_anchor=(1.02,.5),fontsize=9)
fig.text(.07,.09,f'{len(d)} complete line-ratio pairs of {len(df)} survey galaxies. Uncertain classifications are retained; no new classification is fitted.',fontsize=8,color=MUTED)
save(fig)
