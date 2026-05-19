# -*- coding: utf-8 -*-
"""
Extract naturreservat per county from local NR_polygon.shp (NV data, EPSG:3006)
and export as WGS84 GeoJSON matching the origo.json attribute schema.
"""
import json
import fiona
from fiona.transform import transform_geom

SHP = 'E:/NR/NR/NR_polygon.shp'

# Skip problematic date fields (fiona crashes on year-0 dates in the DBF)
DATE_FIELDS = ['URSBESLDAT', 'IKRAFTDATF', 'URSGALLDAT', 'SENGALLDAT']

COUNTIES = {
    'Uppsala':       ('Uppsala Län',        'public/data/naturreservat-uppsala.geojson'),
    'Ostergotland':  ('Östergötlands Län',  'public/data/naturreservat-ostergotland.geojson'),
}


def round_coords(coords):
    if not coords:
        return coords
    if isinstance(coords[0], (list, tuple)):
        return [round_coords(c) for c in coords]
    return [round(coords[0], 5), round(coords[1], 5)]


def round_geom(geom):
    if geom is None:
        return geom
    g = dict(geom)
    g['coordinates'] = round_coords(geom['coordinates'])
    return g


with fiona.open(SHP, encoding='utf-8', ignore_fields=DATE_FIELDS) as src:
    print(f'Total features: {len(src)}, CRS: {src.crs}')

    buckets = {k: [] for k in COUNTIES}

    for feat in src:
        props = feat['properties']
        lan = (props.get('LAN') or '').strip()

        for key, (lan_name, _) in COUNTIES.items():
            if lan != lan_name:
                continue

            geom = feat.get('geometry')
            if not geom:
                continue

            try:
                geom_wgs84 = transform_geom('EPSG:3006', 'EPSG:4326', geom)
            except Exception as e:
                print(f'  Skipping geom transform error: {e}')
                continue

            buckets[key].append({
                'type': 'Feature',
                'geometry': round_geom(geom_wgs84),
                'properties': {
                    'NVRID':               str(props.get('NVRID') or ''),
                    'NAMN':                str(props.get('NAMN') or ''),
                    'SKYDDSTYP':           str(props.get('SKYDDSTYP') or ''),
                    'BESLUTSSTATUS':       str(props.get('BESLSTATUS') or ''),
                    'LAN':                 lan,
                    'KOMMUN':              str(props.get('KOMMUN') or ''),
                    'IUCNKATEGORI':        str(props.get('IUCNKAT') or ''),
                    'FORVALTARE':          str(props.get('FORVALTARE') or ''),
                    'AREA_HA':             props.get('AREA_HA'),
                    'URSPR_BESLUTSDATUM':  '',   # skipped (year-0 dates crash fiona)
                },
            })

for key, (lan_name, outfile) in COUNTIES.items():
    feats = buckets[key]
    fc = {'type': 'FeatureCollection', 'features': feats}
    with open(outfile, 'w', encoding='utf-8') as fh:
        json.dump(fc, fh, ensure_ascii=False, separators=(',', ':'))
    print(f'{lan_name}: {len(feats)} features -> {outfile}')
