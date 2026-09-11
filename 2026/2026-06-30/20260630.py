"""Wrecks around Ireland: reproduce the map and timeline from bundled data."""
from pathlib import Path
import gzip
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
import cartopy.crs as ccrs
from shapely.geometry import shape

HERE = Path(__file__).resolve().parent
ASSETS = HERE / 'assets'
NAVY, IVORY, MUTED = '#122631', '#EFE7D4', '#A4B5B8'
LAND, COAST, GRID = '#CED0BB', '#E0DDC8', '#405661'
COPPER, TEAL, UNKNOWN = '#D59B72', '#74BDB8', '#748994'
ERAS = [('Before 1900', COPPER), ('1900–1949', IVORY), ('1950 onwards', TEAL), ('Year unknown', UNKNOWN)]
TITLE = FontProperties(fname=ASSETS / 'Newsreader.ttf')
BODY = FontProperties(fname=ASSETS / 'Manrope-Regular.ttf')
GEO = ccrs.PlateCarree()
PROJ = ccrs.LambertConformal(central_longitude=-9, central_latitude=53, standard_parallels=(49, 57))
EXTENT = (-13.5, -4.5, 50, 56.5)
plt.rcParams.update({'text.color': IVORY, 'axes.labelcolor': MUTED,
                     'xtick.color': MUTED, 'ytick.color': MUTED, 'savefig.facecolor': NAVY})


def load_data():
    all_records = pd.read_csv(HERE / 'data/wreck_inventory.csv.gz', low_memory=False)
    assert all_records.wreck_no.is_unique
    valid = (all_records.latitude.between(-90, 90) & all_records.longitude.between(-180, 180)
             & all_records.latitude.ne(0) & all_records.longitude.ne(0))
    located = all_records.loc[valid].copy()
    assert len(all_records) == 17981 and len(located) == 3564
    located['era'] = np.select([located.year.lt(1900), located.year.between(1900, 1949),
                                located.year.ge(1950)], [0, 1, 2], default=3)
    coastal = located[located.longitude.between(EXTENT[0], EXTENT[1])
                      & located.latitude.between(EXTENT[2], EXTENT[3])]
    assert len(coastal) == 2872
    assert located.latitude.between(46, 58).all() and located.longitude.between(-26, -4).all()
    assert located[located.era.eq(3)].year.isna().all()
    return all_records, located, coastal


def text(fig, x, y, label, size=10, color=IVORY, serif=False, **kw):
    return fig.text(x, y, label, fontsize=size, color=color,
                    fontproperties=TITLE if serif else BODY, **kw)


def rule(fig, y, x0=.055, x1=.945):
    fig.add_artist(Line2D([x0, x1], [y, y], transform=fig.transFigure,
                         color=GRID, linewidth=.7))


def map_axes(fig, rect, land, extent, small=False):
    ax = fig.add_axes(rect, projection=PROJ, facecolor=NAVY)
    # Densify the geographic perimeter: projecting only corner endpoints can
    # clip records near the middle of a curved latitude boundary.
    x0, x1, y0, y1 = extent
    t = np.linspace(0, 1, 401)
    lon = np.r_[x0+(x1-x0)*t, np.full_like(t,x1), x1-(x1-x0)*t, np.full_like(t,x0)]
    lat = np.r_[np.full_like(t,y0), y0+(y1-y0)*t, np.full_like(t,y1), y1-(y1-y0)*t]
    xy = PROJ.transform_points(GEO, lon, lat)[:, :2]
    low, high = xy.min(axis=0), xy.max(axis=0)
    pad = (high-low)*.002
    ax.set_xlim(low[0]-pad[0], high[0]+pad[0])
    ax.set_ylim(low[1]-pad[1], high[1]+pad[1])
    ax.spines['geo'].set_visible(False)
    ax.add_geometries(land, GEO, facecolor=LAND if not small else '#304550',
                      edgecolor=COAST if not small else '#647C83',
                      linewidth=.45 if not small else .3, zorder=2)
    ax.gridlines(xlocs=range(-30, 1, 2 if not small else 5), ylocs=range(44, 61, 2 if not small else 5),
                 linewidth=.45, linestyle=(0, (1, 5)), color=GRID, zorder=1)
    return ax


def draw_wrecks(ax, records, size=8, alpha=.65):
    # Undated records sit behind dated records, so they remain visible without
    # hiding the temporal pattern. Each mark represents one inventory ID.
    for era in [3, 0, 2, 1]:
        d = records[records.era.eq(era)]
        ax.scatter(d.longitude, d.latitude, transform=GEO, s=size,
                   color=ERAS[era][1], alpha=alpha if era != 3 else alpha * .65,
                   edgecolors='none', zorder=3 + (era != 3))


def geo_label(ax, lon, lat, label, size=10, color=MUTED, **kw):
    ax.text(lon, lat, label, transform=GEO, fontsize=size, fontproperties=BODY,
            color=color, ha='center', va='center', zorder=6, **kw)


def annotate_wreck(ax, records, ident, name, year, label_at, align='left', on_land=False):
    row = records.set_index('wreck_no').loc[ident]
    assert int(row.year) == year
    x, y = label_at
    color = NAVY if on_land else ERAS[int(row.era)][1]
    ax.scatter([row.longitude], [row.latitude], s=80, facecolors='none', edgecolors=color,
               linewidths=.9, transform=GEO, zorder=7)
    ax.plot([row.longitude, x], [row.latitude, y - .11], transform=GEO,
            color=color, linewidth=.7, alpha=.85, zorder=6)
    ax.text(x, y, f'{name} · {year}', transform=GEO, ha=align, va='bottom',
            fontproperties=TITLE, fontsize=15, color=color, zorder=8,
            bbox=dict(facecolor=LAND if on_land else NAVY, edgecolor='none', pad=2, alpha=.93))


def make_chart():
    records, located, coastal = load_data()
    with gzip.open(ASSETS / 'land_10m.geojson.gz', 'rt') as f:
        land = [shape(g) for g in json.load(f)['geometries']]
    fig = plt.figure(figsize=(14, 16), facecolor=NAVY)
    text(fig, .055, .964, 'T I D Y T U E S D A Y   /   3 0  J U N E  2 0 2 6', 9, color=COPPER)
    text(fig, .945, .964, 'V I B E D A T A S C I E N C E', 9, ha='right')
    rule(fig, .948)
    text(fig, .055, .923, 'Wrecks around Ireland',  50, serif=True, va='top')
    text(fig, .055, .857,
         'The Wreck Inventory of Ireland preserves thousands of records of maritime losses.\n'
         'Only a fifth have coordinates. Their recorded locations trace a partial history along the coast and into the Atlantic.',
         11, color=MUTED, linespacing=1.65, va='top')

    text(fig, .055, .775, f'{len(records):,}', 38, serif=True)
    text(fig, .055, .753, 'inventory entries', 10, color=MUTED)
    text(fig, .055, .698, f'{len(located):,}', 38, color=COPPER, serif=True)
    text(fig, .055, .676, 'have coordinates', 10, color=MUTED)
    fraction = len(located) / len(records)
    fig.add_artist(Rectangle((.055, .651), .18, .004, transform=fig.transFigure, color=GRID, linewidth=0))
    fig.add_artist(Rectangle((.055, .651), .18*fraction, .004, transform=fig.transFigure, color=COPPER, linewidth=0))
    text(fig, .055, .634, f'{fraction:.1%} of the inventory', 9, color=MUTED)
    text(fig, .055, .594, 'RECORDED LOSS YEAR', 9, color=COPPER)
    for i, (label, color) in enumerate(ERAS):
        y = .566 - i*.027
        fig.add_artist(Line2D([.06], [y+.003], marker='o', markersize=5,
                             markeredgewidth=0, color=color, transform=fig.transFigure))
        text(fig, .074, y, label, 10, color=color)
    text(fig, .055, .437, 'ATLANTIC OVERVIEW', 9, color=COPPER)
    overview = map_axes(fig, [.044, .299, .21, .133], land, (-26, -4, 46, 58), small=True)
    draw_wrecks(overview, located, size=1.5, alpha=.8)
    x0,x1,y0,y1 = EXTENT
    overview.plot([x0,x1,x1,x0,x0], [y0,y0,y1,y1,y0], transform=GEO,
                  color=COPPER, linewidth=.8, zorder=6)
    text(fig, .055, .287, 'Box marks the coastal view.\nAll 3,564 located records appear here.',
         8.5, color=MUTED, linespacing=1.5)

    ax = map_axes(fig, [.265, .286, .70, .526], land, EXTENT)
    draw_wrecks(ax, coastal)
    geo_label(ax, -8.15, 53.32, 'I R E L A N D', 18, color='#465D59')
    geo_label(ax, -11.95, 53.2, 'N O R T H\nA T L A N T I C', 10, linespacing=1.7)
    geo_label(ax, -8.8, 50.2, 'C E L T I C   S E A', 9)
    geo_label(ax, -5.05, 54.3, 'IRISH\nSEA', 8.5, linespacing=1.5)
    annotate_wreck(ax, coastal, 'W07428', 'Laurentic', 1917, (-11.25, 55.5))
    annotate_wreck(ax, coastal, 'W00805', 'Tayleur', 1854, (-8.8, 54.05), on_land=True)
    annotate_wreck(ax, coastal, 'W02039', 'Leinster', 1918, (-6.8, 51.25))
    annotate_wreck(ax, coastal, 'W08561', 'Lusitania', 1915, (-11.7, 50.4))
    text(fig, .945, .815, f'{len(coastal):,} records in this coastal view', 9, ha='right', color=MUTED)

    rule(fig, .266)
    text(fig, .055, .244, 'RECORDED LOSSES BY DECADE', 9, color=COPPER)
    text(fig, .945, .244, '1800–2019  /  All dated entries, with the located subset in colour', 9, color=MUTED, ha='right')
    years = np.arange(1800, 2020, 10)
    def decades(frame):
        d = frame[frame.year.between(1800, 2019)]
        return d.groupby((d.year//10*10).astype(int)).size().reindex(years, fill_value=0)
    all_counts, located_counts = decades(records), decades(located)
    assert all_counts.sum() == 12768 and located_counts.sum() == 1886
    assert (located_counts <= all_counts).all()
    timeline = fig.add_axes([.092, .116, .85, .104], facecolor=NAVY)
    timeline.bar(years, all_counts, width=7.5, color='#435B66', zorder=2)
    colors = [COPPER if y < 1900 else IVORY if y < 1950 else TEAL for y in years]
    timeline.bar(years, located_counts, width=7.5, color=colors, zorder=3)
    timeline.set(xlim=(1793, 2019), ylim=(0, 1600), xticks=np.arange(1800, 2020, 20), yticks=[0,500,1000,1500])
    timeline.set_yticklabels(['0','500','1,000','1,500'])
    timeline.grid(axis='y', color=GRID, linewidth=.4, zorder=1)
    timeline.tick_params(length=0, pad=7, labelsize=8)
    for tick in timeline.get_xticklabels()+timeline.get_yticklabels():tick.set_fontproperties(BODY);tick.set_fontsize(8)
    for spine in timeline.spines.values():spine.set_visible(False)
    text(fig, .055, .081,
         'One dot represents one inventory entry, including aircraft and unidentified wrecks. Positions may be approximate or describe wreckage.\n'
         'The timeline omits 1,910 entries dated before 1800 and 3,303 without a parsed year.\n'
         'The inventory focuses on pre-1946 wrecks; later coverage is selective. Counts are not a complete history of losses.',
         8.5, color=MUTED, linespacing=1.6, va='top')
    rule(fig, .035)
    text(fig, .055, .017, 'DATA  National Monuments Service · TidyTuesday     /     BASEMAP  Natural Earth', 8, color=MUTED)
    text(fig, .945, .017, 'Lambert conformal conic', 8, color=MUTED, ha='right')
    fig.savefig(HERE / '20260630.png', dpi=240, facecolor=NAVY)
    print(f'Saved 20260630.png: {len(records)} records, {len(located)} located, {len(coastal)} coastal; timeline {all_counts.sum()}/{located_counts.sum()}')
    return fig


if __name__ == '__main__':
    plt.close(make_chart())
