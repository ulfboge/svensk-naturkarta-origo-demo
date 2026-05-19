# -*- coding: utf-8 -*-
"""Extract Västra Götaland + Skåne naturreservat from NR_polygon.shp."""
import json, fiona
from pyproj import Transformer

SHP = 'E:/NR/NR/NR_polygon.shp'
DATE_FIELDS = ['URSBESLDAT', 'IKRAFTDATF', 'URSGALLDAT', 'SENGALLDAT']
TR = Transformer.from_crs('EPSG:3006', 'EPSG:4326', always_xy=True)

COUNTIES = {
    'Västra Götalands Län': 'public/data/naturreservat-vastragotaland.geojson',
    'Skåne Län':            'public/data/naturreservat-skane.geojson',
}

def tr_coords(c):
    if isinstance(c[0], (list, tuple)):
        return [tr_coords(r) for r in c]
    lon, lat = TR.transform(c[0], c[1])
    return [round(lon, 5), round(lat, 5)]

buckets = {k: [] for k in COUNTIES}

with fiona.open(SHP, encoding='utf-8', ignore_fields=DATE_FIELDS) as src:
    print(f'Total: {len(src)} features')
    for feat in src:
        props = feat['properties']
        lan = (props.get('LAN') or '').strip()
        if lan not in COUNTIES:
            continue
        geom = feat.get('geometry')
        if not geom:
            continue
        try:
            coords = tr_coords(list(geom['coordinates']))
            geom_wgs84 = {'type': geom['type'], 'coordinates': coords}
        except Exception as e:
            print(f'  Skip: {e}')
            continue
        buckets[lan].append({
            'type': 'Feature',
            'geometry': geom_wgs84,
            'properties': {
                'NVRID':              str(props.get('NVRID') or ''),
                'NAMN':               str(props.get('NAMN') or ''),
                'SKYDDSTYP':          str(props.get('SKYDDSTYP') or ''),
                'BESLUTSSTATUS':      str(props.get('BESLSTATUS') or ''),
                'LAN':                lan,
                'KOMMUN':             str(props.get('KOMMUN') or ''),
                'IUCNKATEGORI':       str(props.get('IUCNKAT') or ''),
                'FORVALTARE':         str(props.get('FORVALTARE') or ''),
                'AREA_HA':            props.get('AREA_HA'),
                'URSPR_BESLUTSDATUM': '',
            }
        })

for lan, outfile in COUNTIES.items():
    feats = buckets[lan]
    with open(outfile, 'w', encoding='utf-8') as fh:
        json.dump({'type': 'FeatureCollection', 'features': feats},
                  fh, ensure_ascii=False, separators=(',', ':'))
    print(f'{lan}: {len(feats)} -> {outfile}')
