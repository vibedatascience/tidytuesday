"""Sister-city connections: render three complete recorded city networks offline."""
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
import cartopy.crs as ccrs
from shapely.geometry import shape
from pyproj import Geod

HERE = Path(__file__).resolve().parent
ASSETS = HERE / 'assets'
PAPER, INK, MUTED = '#FAF0F2', '#3C2A49', '#75677D'
LAND, COAST, GRID = '#DDD2E1', '#FAF0F2', '#E5DBE7'
CORAL, TEAL, PURPLE = '#C94F55', '#257E79', '#7951A0'
TITLE = FontProperties(fname=ASSETS / 'Newsreader.ttf')
BODY = FontProperties(fname=ASSETS / 'Manrope-Regular.ttf')
GEO = ccrs.PlateCarree()
PROJ = ccrs.Robinson(central_longitude=-100)
GEOD = Geod(ellps='WGS84')
HUBS = [('Q5083', 'Seattle', CORAL, 17, 6),
        ('Q5465', 'Cape Town', TEAL, 13, 5),
        ('Q34600', 'Kyoto', PURPLE, 8, 4)]
plt.rcParams.update({'text.color': INK, 'savefig.facecolor': PAPER})


def load_data():
    cities = pd.read_csv(HERE / 'data/cities.csv.gz').set_index('id')
    raw = pd.read_csv(HERE / 'data/links.csv.gz')
    assert cities.index.is_unique and raw[['source', 'target']].notna().all().all()
    pairs = np.sort(raw[['source', 'target']].astype(str).to_numpy(), axis=1)
    edges = pd.DataFrame(pairs, columns=['a', 'b']).drop_duplicates()
    edges = edges[edges.a.ne(edges.b)]
    assert (set(edges.a) | set(edges.b)) <= set(cities.index)
    assert len(cities) == 5470 and len(edges) == 10596
    assert cities.lat.between(-90, 90).all() and cities.lng.between(-180, 180).all()
    return cities, edges


def partners(cities, edges, hub):
    ids = pd.concat([edges.loc[edges.a.eq(hub), 'b'], edges.loc[edges.b.eq(hub), 'a']])
    assert ids.is_unique and hub not in set(ids)
    return cities.loc[ids].sort_values(['continent', 'name'])


def text(fig, x, y, label, size=10, color=INK, serif=False, **kw):
    return fig.text(x, y, label, fontsize=size, color=color,
                    fontproperties=TITLE if serif else BODY, **kw)


def rule(fig, y, x0=.055, x1=.945):
    fig.add_artist(Line2D([x0, x1], [y, y], transform=fig.transFigure, color=LAND, linewidth=.8))


def map_axes(fig, rect, land):
    ax = fig.add_axes(rect, projection=PROJ, facecolor=PAPER)
    ax.set_global()
    ax.spines['geo'].set_color(LAND)
    ax.spines['geo'].set_linewidth(.7)
    ax.add_geometries(land, GEO, facecolor=LAND, edgecolor=COAST, linewidth=.2, zorder=2)
    ax.gridlines(xlocs=range(-180, 180, 30), ylocs=range(-60, 90, 30),
                 color=GRID, linewidth=.45, linestyle=(0, (2, 4)), zorder=1)
    return ax


def route(hub, destination):
    # Sample the shortest WGS84 geodesic; map-seam handling happens below.
    middle = GEOD.npts(hub.lng, hub.lat, destination.lng, destination.lat, 400)
    xy = np.array([(hub.lng, hub.lat), *middle, (destination.lng, destination.lat)])
    assert np.isfinite(xy).all()
    assert np.allclose(xy[0], [hub.lng, hub.lat])
    assert np.allclose(xy[-1], [destination.lng, destination.lat])
    return xy


def projected_route(hub, destination):
    xy = route(hub, destination)
    projected = PROJ.transform_points(GEO, xy[:, 0], xy[:, 1])[:, :2]
    # Draw in projected coordinates and explicitly break at the map seam.
    # Connecting wrapped longitudes in PlateCarree can create false horizontal
    # lines spanning the entire world, including at the international date line.
    width = PROJ.x_limits[1] - PROJ.x_limits[0]
    breaks = np.flatnonzero(np.abs(np.diff(projected[:, 0])) > width / 2) + 1
    return np.insert(projected, breaks, [np.nan, np.nan], axis=0)


def network(ax, cities, edges, ident, color, small=False):
    hub = cities.loc[ident]
    destinations = partners(cities, edges, ident)
    for _, destination in destinations.iterrows():
        xy = projected_route(hub, destination)
        ax.plot(xy[:, 0], xy[:, 1], color=color,
                linewidth=.75 if small else 1.15, alpha=.55, zorder=3)
    ax.scatter(destinations.lng, destinations.lat, transform=GEO,
               s=10 if small else 22, color=PAPER, edgecolors=color,
               linewidths=.6 if small else .9, zorder=5)
    ax.scatter([hub.lng], [hub.lat], transform=GEO, s=55 if small else 140,
               facecolors=PAPER, edgecolors=color, linewidths=1.0, zorder=7)
    ax.scatter([hub.lng], [hub.lat], transform=GEO, s=13 if small else 45,
               color=color, edgecolors='none', zorder=8)
    return destinations


def city_label(ax, cities, ident, offset, color=INK, size=10, hub=False):
    c = cities.loc[ident]
    ax.annotate(c['name'], xy=(c.lng, c.lat), xycoords=GEO._as_mpl_transform(ax),
                xytext=offset, textcoords='offset points',
                ha='left' if offset[0] >= 0 else 'right', va='center',
                fontsize=size, fontproperties=TITLE if hub else BODY, color=color,
                bbox=dict(facecolor=PAPER, edgecolor='none', alpha=.9, pad=1.8),
                arrowprops=dict(arrowstyle='-', color=color, linewidth=.45), zorder=9)


def make_chart():
    cities, edges = load_data()
    with gzip.open(ASSETS / 'land_50m.geojson.gz', 'rt') as f:
        land = [shape(g) for g in json.load(f)['geometries']]
    for ident, name, color, count, continents in HUBS:
        p = partners(cities, edges, ident)
        assert cities.loc[ident, 'name'] == name
        assert len(p) == count and p.continent.nunique() == continents
    fig = plt.figure(figsize=(16, 14), facecolor=PAPER)
    text(fig, .055, .964, 'T I D Y T U E S D A Y   /   1 2  M A Y  2 0 2 6', 9, color=CORAL)
    text(fig, .945, .964, 'V I B E D A T A S C I E N C E', 9, ha='right')
    rule(fig, .948)
    text(fig, .055, .923, 'Sister-city connections', 54, serif=True, va='top')
    text(fig, .055, .850,
         'Seattle connects to cities on six continents in the supplied Wikidata extract.\n'
         'Each line joins one recorded city pair. Cape Town and Kyoto offer two different geographic patterns.',
         11, color=MUTED, linespacing=1.65, va='top')
    text(fig, .055, .785, 'SEATTLE  /  UNITED STATES', 10, color=CORAL)
    main = map_axes(fig, [.045, .397, .705, .377], land)
    p = network(main, cities, edges, 'Q5083', CORAL)
    for ident, offset in [('Q5083', (12, 15)), ('Q48320', (-10, 12)),
                          ('Q79990', (10, -4)), ('Q518431', (10, -10)),
                          ('Q40194', (9, 6)), ('Q26793', (-15, 15)), ('Q225641', (-8, -13))]:
        city_label(main, cities, ident, offset, color=CORAL if ident == 'Q5083' else INK,
                   size=18 if ident == 'Q5083' else 9, hub=ident == 'Q5083')
    text(fig, .775, .771, '17', 46, color=CORAL, serif=True)
    text(fig, .84, .779, 'recorded partners\nacross 6 continents', 10, color=MUTED, linespacing=1.6)
    groups = [
        ('Asia', ['Beersheba · Cebu City', 'Haiphong · Kaohsiung', 'Kobe · Sihanoukville · Tashkent']),
        ('Europe', ['Bergen · Galway · Gdynia', 'Nantes · Perugia']),
        ('Africa', ['Limbe · Mombasa']),
        ('North America', ['Mazatlan']),
        ('South America', ['Chimbote']),
        ('Oceania', ['Christchurch'])]
    listed = []
    y = .715
    for continent, lines in groups:
        names = [name for line in lines for name in line.split(' · ')]
        assert set(names) == set(p[p.continent.eq(continent)]['name'])
        listed.extend(names)
        text(fig, .775, y, continent.upper(), 8.5, color=CORAL)
        y -= .020
        for line in lines:
            text(fig, .775, y, line, 9.5)
            y -= .019
        y -= .012
    assert len(listed) == len(p) == len(set(listed))
    text(fig, .055, .375, 'All 17 connections are drawn. Selected destination cities are labelled on the map; the full list appears at right.',
         9, color=MUTED)
    rule(fig, .354)
    for left, (ident, name, color, count, continents) in zip([.055, .54], HUBS[1:]):
        text(fig, left, .326, name, 28, serif=True, color=color)
        text(fig, left+.405, .326, f'{count} partners · {continents} continents', 10, color=MUTED, ha='right')
        ax = map_axes(fig, [left-.008, .106, .427, .205], land)
        network(ax, cities, edges, ident, color, small=True)
        city_label(ax, cities, ident, (-12, -10) if ident == 'Q5465' else (8, 10), color=color, size=12, hub=True)
    rule(fig, .089)
    text(fig, .055, .067,
         'Connections are undirected, with reciprocal and duplicate pairs counted once. All partners of each selected city are shown.\n'
         'These are relationships recorded in the extract, not a complete or independently verified list of current agreements. Lines are not travel routes.',
         8.5, color=MUTED, linespacing=1.65, va='top')
    text(fig, .055, .019, 'DATA  Wikidata · Twin Cities Explorer · TidyTuesday     /     BASEMAP  Natural Earth', 8, color=MUTED)
    text(fig, .945, .019, 'All maps: Robinson projection, centred at 100°W', 8, color=MUTED, ha='right')
    fig.savefig(HERE / '20260512.png', dpi=240, facecolor=PAPER)
    print('Saved 20260512.png: Seattle 17 partners / 6 continents; Cape Town 13 / 5; Kyoto 8 / 4')
    return fig


if __name__ == '__main__':
    plt.close(make_chart())
