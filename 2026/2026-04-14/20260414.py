"""Seabird survey locations, 1969–1990. Run this file to reproduce the PNG offline."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.lines import Line2D
from matplotlib.path import Path as PlotPath
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
from shapely.geometry import box

HERE = Path(__file__).resolve().parent
ASSETS = HERE / 'assets'
PAPER, INK, MUTED = '#F4F0E6', '#183C3E', '#576C68'
OCEAN, LAND, COAST, GRID = '#E5EAE2', '#F4F0E6', '#86988C', '#BCCAC0'
TEAL, RUST = '#236568', '#AF4C2D'
TITLE = FontProperties(fname=ASSETS / 'Newsreader.ttf')
BODY = FontProperties(fname=ASSETS / 'Manrope-Regular.ttf')
plt.rcParams.update({'font.family': 'DejaVu Sans', 'text.color': INK,
                     'savefig.facecolor': PAPER, 'path.simplify': False})
GEO = ccrs.PlateCarree()
PROJECTION = ccrs.LambertAzimuthalEqualArea(central_longitude=145, central_latitude=-43)


def load_data():
    birds = pd.read_csv(HERE / 'data/birds.csv.gz', low_memory=False)
    ships = pd.read_csv(HERE / 'data/ships.csv.gz')
    assert ships.record_id.is_unique and birds.bird_observation_id.is_unique
    valid = (ships.latitude.between(-90, 90) & ships.longitude.between(0, 180)
             & ships.hemisphere.isin(['E', 'W']))
    surveys = ships.loc[valid].copy()
    surveys['lon'] = np.where(surveys.hemisphere.eq('W'), -surveys.longitude, surveys.longitude)
    surveys['lon_east'] = surveys.lon % 360
    assert len(surveys) == 12299 and len(ships) - len(surveys) == 11
    assert surveys.latitude.between(-72, -16).all()
    assert surveys.lon_east.between(48, 202).all()
    # Absence entries have no common name. Keep those census periods in the
    # coverage layer, but never count them as bird sightings.
    sightings = birds.loc[birds.species_common_name.notna()].merge(
        surveys, on='record_id', how='inner', validate='many_to_one')
    assert (~birds.record_id.isin(ships.record_id)).sum() == 1
    assert sightings.species_common_name.notna().all()
    return surveys, sightings


def text(fig, x, y, label, size=10, color=INK, serif=False, **kw):
    return fig.text(x, y, label, fontsize=size, color=color,
                    fontproperties=TITLE if serif else BODY, **kw)


def rule(fig, y, x0=.055, x1=.945, color=COAST, width=.6):
    fig.add_artist(Line2D([x0, x1], [y, y], transform=fig.transFigure,
                         color=color, linewidth=width))


def map_axes(fig, rect, land, small=False):
    ax = fig.add_axes(rect, projection=PROJECTION, facecolor=OCEAN)
    # Clip to a geographic rectangle; its curved edges preserve the projection.
    n = 200
    lon = np.r_[np.linspace(48, 202, n), np.full(n, 202),
                np.linspace(202, 48, n), np.full(n, 48)]
    lat = np.r_[np.full(n, -16), np.linspace(-16, -72, n),
                np.full(n, -72), np.linspace(-72, -16, n)]
    xy = PROJECTION.transform_points(GEO, lon, lat)[:, :2]
    ax.set_xlim(xy[:, 0].min(), xy[:, 0].max())
    ax.set_ylim(xy[:, 1].min(), xy[:, 1].max())
    ax.set_boundary(PlotPath(np.vstack([xy, xy[0]])), transform=ax.transData)
    ax.spines['geo'].set_edgecolor(GRID)
    ax.spines['geo'].set_linewidth(.45)
    ax.add_geometries(land, GEO, facecolor=LAND, edgecolor=COAST,
                      linewidth=.23 if small else .45, zorder=2)
    ax.gridlines(xlocs=[60, 90, 120, 150, 180, -150],
                 ylocs=[-20, -30, -40, -50, -60, -70], color=GRID,
                 linewidth=.3 if small else .5, linestyle=(0, (2, 4)), zorder=1)
    return ax


def points(ax, data, color, size, alpha=1, zorder=3):
    return ax.scatter(data.lon, data.latitude, transform=GEO, s=size,
                      color=color, alpha=alpha, edgecolors='none', zorder=zorder)


def geo_text(ax, lon, lat, label, size=9, color=MUTED, **kw):
    ax.text(lon, lat, label, transform=GEO, fontproperties=BODY,
            fontsize=size, color=color, ha='center', va='center', zorder=5, **kw)


def make_chart():
    surveys, sightings = load_data()
    # Clip away the projection antipode before projecting the land polygons.
    region = box(40, -80, 180, -10).union(box(-180, -80, -150, -10))
    land = [g.intersection(region) for g in Reader(ASSETS / 'ne_50m_land.shp').geometries()
            if g.intersects(region)]
    fig = plt.figure(figsize=(14, 15), facecolor=PAPER)
    text(fig, .055, .964, 'T I D Y T U E S D A Y   /   1 4  A P R I L  2 0 2 6', 9)
    text(fig, .945, .964, 'V I B E D A T A S C I E N C E', 9, ha='right')
    rule(fig, .95)
    text(fig, .055, .923, 'Seabirds at sea',  60, serif=True, va='top')
    text(fig, .945, .914, '1969–1990', 26, serif=True, ha='right', va='top')
    text(fig, .945, .881, 'SHIPBOARD OBSERVATIONS', 8.5, color=MUTED, ha='right')
    text(fig, .055, .847,
         'Seabird logbooks from Te Papa, New Zealand, record observations across the southern oceans.\n'
         'The map follows the survey coverage; the three species below reveal different recorded distributions.',
         11, linespacing=1.65, va='top')
    ax = map_axes(fig, [.035, .375, .93, .425], land)
    points(ax, surveys, TEAL, 3.7, .42)
    for args in [(134, -26, 'A U S T R A L I A', 12),
                 (186, -47, 'NEW\nZEALAND', 8.5),
                 (87, -43, 'I N D I A N\nO C E A N', 11),
                 (192, -28, 'S O U T H\nP A C I F I C', 10),
                 (154, -63, 'S O U T H E R N\nO C E A N', 10)]:
        geo_text(ax, *args, linespacing=1.7)
    ax.plot([176, 184], [-42, -46], transform=GEO, color=COAST, linewidth=.6, zorder=5)
    for lon in [60, 90, 120, 150, 180]:
        geo_text(ax, lon, -17.4, f'{lon}°E' if lon != 180 else '180°', 7.5)
    for lat in [-30, -50, -70]:
        geo_text(ax, 50.5, lat, f'{abs(lat)}°S', 7.5)
    text(fig, .055, .785, '01   SURVEY COVERAGE', 9, color=TEAL)
    text(fig, .945, .785, f'{len(surveys):,} located survey periods', 10, ha='right')
    text(fig, .055, .363,
         'Each teal dot marks one survey period, including periods with no birds recorded. Overlapping dots appear darker.',
         9, color=MUTED)
    rule(fig, .344)
    text(fig, .055, .324, '02   SELECTED SPECIES', 9, color=RUST)
    text(fig, .945, .324, 'Rust: species recorded   /   Grey: all survey locations', 9, ha='right', color=MUTED)
    species = [('Cape petrel', 'Daption capense'),
               ('Sooty shearwater', 'Puffinus griseus'),
               ("Buller's shearwater", 'Puffinus bulleri')]
    counts = {}
    for i, (common, scientific) in enumerate(species):
        left = .055 + i * .305
        found = sightings.loc[sightings.species_scientific_name.eq(scientific)].drop_duplicates('record_id')
        assert not found.empty and found.record_id.is_unique
        counts[common] = len(found)
        text(fig, left, .291, common, 23, serif=True)
        text(fig, left, .272, scientific, 9, color=MUTED)
        panel = map_axes(fig, [left - .013, .105, .302, .158], land, small=True)
        points(panel, surveys, '#9DAEAA', 1.25, .20)
        points(panel, found, RUST, 2.0, .65, zorder=4)
        text(fig, left, .097, f'{len(found):,} survey periods with this species', 9, color=RUST)
    rule(fig, .077)
    text(fig, .055, .057,
         'Recorded sightings reflect survey effort and identification. They do not estimate population size or species range.\n'
         'Species names follow the source. Each species is counted once per survey period; maps share a projection and extent.',
         8.5, color=MUTED, linespacing=1.65, va='top')
    text(fig, .055, .014, 'DATA  Te Papa Tongarewa · TidyTuesday     /     BASEMAP  Natural Earth', 8, color=MUTED)
    text(fig, .945, .014, 'Lambert azimuthal equal-area', 8, color=MUTED, ha='right')
    output = HERE / '20260414.png'
    fig.savefig(output, dpi=240, facecolor=PAPER)
    print(f'Saved {output.name}: {len(surveys):,} survey periods; species counts {counts}')
    return fig


if __name__ == '__main__':
    plt.close(make_chart())
