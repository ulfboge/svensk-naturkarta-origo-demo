# -*- coding: utf-8 -*-
"""Extract alla 15 återstående svenska län från NR_polygon.shp.
Skriver GeoJSON-filer + en JSON-sammanfattning med bbox/stats för index.html.
"""
import json, math, fiona
from pyproj import Transformer

SHP = 'E:/NR/NR/NR_polygon.shp'
DATE_FIELDS = ['URSBESLDAT', 'IKRAFTDATF', 'URSGALLDAT', 'SENGALLDAT']

TR_4326 = Transformer.from_crs('EPSG:3006', 'EPSG:4326', always_xy=True)
TR_3857 = Transformer.from_crs('EPSG:3006', 'EPSG:3857', always_xy=True)

# lan-namn → (kort-kod, filnamn-suffix)
NEW_COUNTIES = {
    'Blekinge Län':        ('ble', 'blekinge'),
    'Dalarnas Län':        ('dal', 'dalarna'),
    'Gotlands Län':        ('got', 'gotland'),
    'Gävleborgs Län':      ('gav', 'gavleborg'),
    'Hallands Län':        ('hal', 'halland'),
    'Jämtlands Län':       ('jam', 'jamtland'),
    'Jönköpings Län':      ('jon', 'jonkoping'),
    'Kalmar Län':          ('kal', 'kalmar'),
    'Kronobergs Län':      ('kro', 'kronoberg'),
    'Norrbottens Län':     ('nrb', 'norrbotten'),
    'Värmlands Län':       ('vrm', 'varmland'),
    'Västerbottens Län':   ('vbo', 'vasterbotten'),
    'Västernorrlands Län': ('vnr', 'vasternorrland'),
    'Västmanlands Län':    ('vml', 'vastmanland'),
    'Örebro Län':          ('ore', 'orebro'),
}

def tr_coords_4326(c):
    if isinstance(c[0], (list, tuple)):
        return [tr_coords_4326(r) for r in c]
    lon, lat = TR_4326.transform(c[0], c[1])
    return [round(lon, 5), round(lat, 5)]

def to_3857(lon, lat):
    x = lon * 20037508.34 / 180
    y = math.log(math.tan((90 + lat) * math.pi / 360)) * 20037508.34 / math.pi
    return x, y

buckets   = {lan: [] for lan in NEW_COUNTIES}
bbox_3006 = {lan: [float('inf'), float('inf'), float('-inf'), float('-inf')] for lan in NEW_COUNTIES}
areas     = {lan: 0.0 for lan in NEW_COUNTIES}

print('Läser shapefile …')
with fiona.open(SHP, encoding='utf-8', ignore_fields=DATE_FIELDS) as src:
    print(f'  Totalt {len(src)} features')
    for feat in src:
        props = feat['properties']
        lan = (props.get('LAN') or '').strip()
        if lan not in NEW_COUNTIES:
            continue
        geom = feat.get('geometry')
        if not geom:
            continue

        # Samla bbox i EPSG:3006 för snabb beräkning
        coords_flat = []
        def flatten(c):
            if isinstance(c[0], (list, tuple)):
                for r in c: flatten(r)
            else:
                coords_flat.append(c)
        flatten(geom['coordinates'])
        xs = [p[0] for p in coords_flat]
        ys = [p[1] for p in coords_flat]
        b = bbox_3006[lan]
        b[0] = min(b[0], min(xs)); b[1] = min(b[1], min(ys))
        b[2] = max(b[2], max(xs)); b[3] = max(b[3], max(ys))

        area = props.get('AREA_HA') or 0
        areas[lan] += float(area) if area else 0

        try:
            coords_wgs = tr_coords_4326(list(geom['coordinates']))
            geom_wgs84 = {'type': geom['type'], 'coordinates': coords_wgs}
        except Exception as e:
            print(f'  Skip ({lan}): {e}')
            continue

        buckets[lan].append({
            'type': 'Feature',
            'geometry': geom_wgs84,
            'properties': {
                'NVRID':              str(props.get('NVRID') or ''),
                'NAMN':               str(props.get('NAMN') or ''),
                'SKYDDSTYP':          str(props.get('SKYDDSTYP') or ''),
                'LAN':                lan,
                'KOMMUN':             str(props.get('KOMMUN') or ''),
                'IUCNKATEGORI':       str(props.get('IUCNKAT') or ''),
                'FORVALTARE':         str(props.get('FORVALTARE') or ''),
                'AREA_HA':            props.get('AREA_HA'),
                'URSPR_BESLUTSDATUM': '',
            }
        })

# Skriv GeoJSON-filer
print('\nSkriver GeoJSON …')
summary = {}
for lan, (code, suffix) in NEW_COUNTIES.items():
    feats = buckets[lan]
    outfile = f'public/data/naturreservat-{suffix}.geojson'
    with open(outfile, 'w', encoding='utf-8') as fh:
        json.dump({'type': 'FeatureCollection', 'features': feats},
                  fh, ensure_ascii=False, separators=(',', ':'))
    print(f'  {lan}: {len(feats)} st -> {outfile}')

    # Beräkna WGS84-bbox och EPSG:3857-extent från 3006-bbox
    b = bbox_3006[lan]
    minLon, minLat = TR_4326.transform(b[0], b[1])
    maxLon, maxLat = TR_4326.transform(b[2], b[3])
    minX, minY = to_3857(minLon, minLat)
    maxX, maxY = to_3857(maxLon, maxLat)

    summary[code] = {
        'lan':    lan,
        'count':  len(feats),
        'area':   round(areas[lan]),
        'wgs84':  {'minLat': round(minLat,3), 'maxLat': round(maxLat,3),
                   'minLon': round(minLon,3), 'maxLon': round(maxLon,3)},
        'e3857':  [round(minX), round(minY), round(maxX), round(maxY)],
        'layer':  f'nv_naturreservat_{suffix}',
        'file':   outfile,
    }

# Skriv sammanfattning
with open('_lan_summary.json', 'w', encoding='utf-8') as fh:
    json.dump(summary, fh, ensure_ascii=False, indent=2)
print('\nSammanfattning sparad i _lan_summary.json')

# Skriv JS-snippet
print('\n=== JS-konstanter (kopiera till index.html) ===')
print('// COUNTY_STATS tillägg:')
for code, d in summary.items():
    print(f"    {code}: {{ nr: {d['count']:4d}, area: {d['area']:7d}, np: 0 }},")

print('\n// COUNTY_BBOX tillägg:')
for code, d in summary.items():
    w = d['wgs84']
    print(f"    {code}: {{ minLat: {w['minLat']}, maxLat: {w['maxLat']}, minLon: {w['minLon']}, maxLon: {w['maxLon']} }},")

print('\n// EXTENTS tillägg:')
for code, d in summary.items():
    e = d['e3857']
    print(f"    {code}: [{e[0]}, {e[1]}, {e[2]}, {e[3]}],")
