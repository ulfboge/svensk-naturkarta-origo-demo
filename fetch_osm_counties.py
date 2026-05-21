# -*- coding: utf-8 -*-
"""
Fetch naturreservat from OpenStreetMap via Overpass API.
Used as fallback when NV WFS is down.
Outputs GeoJSON matching the same schema as NV WFS data.
"""
import urllib.request
import urllib.parse
import json
import math

OVERPASS_URL = 'https://overpass-api.de/api/interpreter'

# Uppsala Län bbox:        S, W, N, E
BBOXES = {
    'Uppsala':       (59.30, 15.80, 61.20, 19.60),
    'Ostergotland':  (57.40, 14.40, 59.00, 17.20),
}

OUTFILES = {
    'Uppsala':      'public/data/naturreservat-uppsala.geojson',
    'Ostergotland': 'public/data/naturreservat-ostergotland.geojson',
}

LAN_NAMES = {
    'Uppsala':      'Uppsala Län',
    'Ostergotland': 'Östergötlands Län',
}


def build_query(bbox):
    s, w, n, e = bbox
    bb = f'{s},{w},{n},{e}'
    return f"""
[out:json][timeout:90];
(
  way["boundary"="protected_area"]["protection_title"="Naturreservat"](bbox:{bb});
  relation["boundary"="protected_area"]["protection_title"="Naturreservat"](bbox:{bb});
  way["leisure"="nature_reserve"](bbox:{bb});
  relation["leisure"="nature_reserve"](bbox:{bb});
);
out body geom;
""".strip()


def ring_area_ha(coords):
    """Shoelace formula for polygon area in hectares (WGS84, approximate)."""
    n = len(coords)
    if n < 3:
        return 0
    R = 6378137
    area = 0
    for i in range(n):
        j = (i + 1) % n
        lon1, lat1 = math.radians(coords[i][0]), math.radians(coords[i][1])
        lon2, lat2 = math.radians(coords[j][0]), math.radians(coords[j][1])
        area += (lon2 - lon1) * (2 + math.sin(lat1) + math.sin(lat2))
    return abs(area * R * R / 2) / 10000


def way_to_ring(geom_nodes):
    return [[round(n['lon'], 5), round(n['lat'], 5)] for n in geom_nodes]


def elem_to_feature(elem, lan_name):
    tags = elem.get('tags', {})
    name = tags.get('name', '')
    if not name:
        return None

    etype = elem['type']
    coords = None

    if etype == 'way':
        nodes = elem.get('geometry', [])
        if len(nodes) < 3:
            return None
        ring = way_to_ring(nodes)
        if ring[0] != ring[-1]:
            ring.append(ring[0])
        coords = [ring]

    elif etype == 'relation':
        outer = []
        inner = []
        for m in elem.get('members', []):
            if m.get('type') != 'way' or 'geometry' not in m:
                continue
            ring = way_to_ring(m['geometry'])
            if len(ring) < 3:
                continue
            if ring[0] != ring[-1]:
                ring.append(ring[0])
            if m.get('role') == 'inner':
                inner.append(ring)
            else:
                outer.append(ring)
        if not outer:
            return None
        coords = outer + inner

    if not coords:
        return None

    area_ha = round(ring_area_ha(coords[0]), 1)

    return {
        'type': 'Feature',
        'geometry': {'type': 'Polygon', 'coordinates': coords},
        'properties': {
            'NVRID':              tags.get('ref:se:nvr', str(elem['id'])),
            'NAMN':               name,
            'SKYDDSTYP':          tags.get('protection_title', 'Naturreservat'),
            'BESLUTSSTATUS':      '',
            'LAN':                lan_name,
            'KOMMUN':             tags.get('addr:municipality', ''),
            'IUCNKATEGORI':       tags.get('iucn_level', ''),
            'FORVALTARE':         tags.get('operator', ''),
            'AREA_HA':            area_ha,
            'LAND_HA':            None,
            'VATTEN_HA':          None,
            'SKOG_HA':            None,
            'URSPR_BESLUTSDATUM': tags.get('start_date', ''),
        }
    }


def fetch(region):
    bbox = BBOXES[region]
    query = build_query(bbox)
    get_url = OVERPASS_URL + '?data=' + urllib.parse.quote(query)
    req = urllib.request.Request(get_url, headers={
        'User-Agent': 'NaturkartaPortfolioBot/1.0 (github.com/ulfboge/svensk-naturkarta-origo-demo)'
    })
    print(f'Querying Overpass for {region}...')
    with urllib.request.urlopen(req, timeout=120) as r:
        data = json.loads(r.read().decode('utf-8'))

    seen = set()
    features = []
    for elem in data.get('elements', []):
        fid = (elem['type'], elem['id'])
        if fid in seen:
            continue
        seen.add(fid)
        f = elem_to_feature(elem, LAN_NAMES[region])
        if f:
            features.append(f)

    fc = {'type': 'FeatureCollection', 'features': features}
    out = OUTFILES[region]
    with open(out, 'w', encoding='utf-8') as fh:
        json.dump(fc, fh, ensure_ascii=False, separators=(',', ':'))
    print(f'  {len(features)} naturreservat -> {out}')


fetch('Uppsala')
fetch('Ostergotland')
