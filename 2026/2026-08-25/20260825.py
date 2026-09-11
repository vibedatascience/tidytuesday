"""TidyTuesday 2026-08-25: Common words in country-music lyrics. Reproduce the chart from the bundled source data."""
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
    fig.text(.07,.96,'TIDYTUESDAY  /  2026-08-25',fontsize=9,color=ACCENT,weight='bold')
    fig.text(.07,.90,textwrap.fill('Common words in country-music lyrics',48),fontsize=27,fontfamily='DejaVu Serif',va='top',linespacing=1.14)
    fig.text(.07,.77,subtitle,fontsize=10,va='top',linespacing=1.55)
    fig.text(.07,.035,textwrap.fill('Data: Country Lyrics Amazing Spreadsheet · TidyTuesday. Graphic: vibedatascience.',110),fontsize=8,color=MUTED,linespacing=1.5)
    return fig

def axis(fig, rect=(.24,.18,.69,.49), grid='x'):
    ax=fig.add_axes(rect,facecolor=PAPER)
    for spine in ax.spines.values():spine.set_visible(False)
    ax.tick_params(length=0,pad=8)
    if grid:ax.grid(axis=grid,color=MUTED,alpha=.16,linewidth=.7)
    ax.set_axisbelow(True)
    return ax

def save(fig):
    fig.savefig(HERE / '20260825.png',dpi=170)
    plt.close(fig)
    print('2026-08-25: saved 20260825.png')

source=HERE/'data/country_lyrics.csv.gz'
raw=pd.read_csv(source if source.exists() else 'https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2026/2026-08-25/country_lyrics.csv')
df=raw.dropna(subset=['lyrics']).drop_duplicates(['song','artist'])
stop=set('a about after again all am an and any are as at away back be because been before being but by can cant come could day did do does dont down each even ever every for from get gets getting go going gonna got had has have he her here hers hey him his how i id if ill im in into is it its ive just know knows let lets like little look made make man me more most much my na never new no not now of off oh on one only or our out over own really right said say says see she should so some something still such take tell than that the their them then there these they thing think this those through time to too up us very wanna want was way we well were what when where which who why will with wont would yeah year yes yet you your youre youve'.split())
counts=Counter()
for text in df.lyrics:
 tokens=set(re.findall(r"[a-z]+(?:'[a-z]+)?",str(text).lower().replace('’',"'")))
 tokens={t.replace("'",'') for t in tokens}
 counts.update(t for t in tokens if len(t)>2 and t not in stop and t!='aint')
top=counts.most_common(20)[::-1];fig=figure('The 20 most frequent non-stopwords, counted once per song rather than once per repetition.\nA repeated chorus therefore does not increase a word’s count within a song.',11)
ax=axis(fig,(.21,.16,.66,.51));vals=[100*n/len(df) for _,n in top];y=np.arange(len(top));ax.barh(y,vals,color=ACCENT,height=.6)
ax.set_yticks(y,[w for w,_ in top],fontsize=11);ax.set_xlim(0,max(vals)*1.18);ax.set_xlabel('Songs containing the word (%)',labelpad=12)
for i,(word,n) in enumerate(top):ax.text(vals[i]+1,i,f'{vals[i]:.1f}%  ({n})',va='center',fontsize=8)
fig.text(.07,.08,f'{len(df)} unique song–artist entries with lyrics. Lowercase alphabetic tokens, length >2; the full stopword list is in the code.',fontsize=8,color=MUTED)
save(fig)
