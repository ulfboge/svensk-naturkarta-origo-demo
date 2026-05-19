# -*- coding: utf-8 -*-
"""Extract all national parks from NP_polygon.shp and export as WGS84 GeoJSON."""
import json
import fiona
from pyproj import Transformer

SHP = 'E:/NP/NP/NP_polygon.shp'
DATE_FIELDS = ['URSBESLDAT', 'IKRAFTDATF', 'URSGALLDAT', 'SENGALLDAT']

# SWEREF99 TM (E,N) → WGS84 (lon, lat)
TR = Transformer.from_crs('EPSG:3006', 'EPSG:4326', always_xy=True)


def tr_coords(c):
    """Recursively transform and round coordinate arrays."""
    if isinstance(c[0], (list, tuple)):
        return [tr_coords(ring) for ring in c]
    lon, lat = TR.transform(c[0], c[1])
    return [round(lon, 5), round(lat, 5)]


features = []
with fiona.open(SHP, encoding='utf-8', ignore_fields=DATE_FIELDS) as src:
    print(f'Total NP: {len(src)}')
    for feat in src:
        props = feat['properties']
        geom = feat.get('geometry')
        if not geom:
            continue
        try:
            coords_wgs84 = tr_coords(list(geom['coordinates']))
            geom_wgs84 = {'type': geom['type'], 'coordinates': coords_wgs84}
        except Exception as e:
            print(f'  Skipping {props.get("NAMN")}: {e}')
            continue

        lan = (props.get('LAN') or '').strip()
        features.append({
            'type': 'Feature',
            'geometry': geom_wgs84,
            'properties': {
                'NVRID':              str(props.get('NVRID') or ''),
                'NAMN':               str(props.get('NAMN') or ''),
                'SKYDDSTYP':          str(props.get('SKYDDSTYP') or 'Nationalpark'),
                'LAN':                lan,
                'KOMMUN':             str(props.get('KOMMUN') or ''),
                'IUCNKATEGORI':       str(props.get('IUCNKAT') or ''),
                'FORVALTARE':         str(props.get('FORVALTARE') or ''),
                'AREA_HA':            props.get('AREA_HA'),
                'URSPR_BESLUTSDATUM': '',
            }
        })
        print(f"  {props.get('NAMN')} | {lan[:60]}")

fc = {'type': 'FeatureCollection', 'features': features}
out = 'public/data/nationalparker-alla.geojson'
with open(out, 'w', encoding='utf-8') as fh:
    json.dump(fc, fh, ensure_ascii=False, separators=(',', ':'))
print(f'\n{len(features)} nationalparker -> {out}')
