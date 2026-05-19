# -*- coding: utf-8 -*-
"""Fetch naturreservat GeoJSON per county from NV WFS (POST with FES filter)."""
import urllib.request
import urllib.parse
import json
import math

WFS_URL = 'https://geodata.naturvardsverket.se/naturvardsregistret/wfs'

def post_wfs(lan_name):
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<wfs:GetFeature service="WFS" version="2.0.0" outputFormat="GEOJSON"
  xmlns:wfs="http://www.opengis.net/wfs/2.0"
  xmlns:fes="http://www.opengis.net/fes/2.0"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <wfs:Query typeNames="Naturvardsregistret_WFS:SkyddadeOmraden">
    <fes:Filter>
      <fes:And>
        <fes:PropertyIsEqualTo>
          <fes:ValueReference>LAN</fes:ValueReference>
          <fes:Literal>{lan_name}</fes:Literal>
        </fes:PropertyIsEqualTo>
        <fes:PropertyIsEqualTo>
          <fes:ValueReference>SKYDDSTYP</fes:ValueReference>
          <fes:Literal>Naturreservat</fes:Literal>
        </fes:PropertyIsEqualTo>
      </fes:And>
    </fes:Filter>
  </wfs:Query>
</wfs:GetFeature>"""

    req = urllib.request.Request(
        WFS_URL,
        data=xml.encode('utf-8'),
        headers={'Content-Type': 'application/xml; charset=UTF-8'}
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode('utf-8'))


def get_wfs_cql(lan_name):
    """Fallback: GET with CQL_FILTER (may fail on Swedish chars)."""
    params = urllib.parse.urlencode({
        'SERVICE': 'WFS',
        'VERSION': '2.0.0',
        'REQUEST': 'GetFeature',
        'TYPENAMES': 'Naturvardsregistret_WFS:SkyddadeOmraden',
        'outputFormat': 'GEOJSON',
        'CQL_FILTER': f"LAN='{lan_name}' AND SKYDDSTYP='Naturreservat'",
    })
    url = f"{WFS_URL}?{params}"
    with urllib.request.urlopen(url, timeout=120) as r:
        return json.loads(r.read().decode('utf-8'))


def round_coords(coords):
    if coords and isinstance(coords[0], list):
        return [round_coords(c) for c in coords]
    return [round(x, 5) for x in coords]


def save(data, out_file):
    for f in data['features']:
        geom = f.get('geometry') or {}
        if geom.get('coordinates'):
            geom['coordinates'] = round_coords(geom['coordinates'])
    with open(out_file, 'w', encoding='utf-8') as fh:
        json.dump(data, fh, ensure_ascii=False, separators=(',', ':'))


COUNTIES = [
    ('Uppsala Län',        'public/data/naturreservat-uppsala.geojson'),
    ('Östergötlands Län',  'public/data/naturreservat-ostergotland.geojson'),
]

for lan, path in COUNTIES:
    print(f'Fetching {lan}...')
    try:
        data = post_wfs(lan)
    except Exception as e:
        print(f'  POST failed: {e}, trying GET...')
        try:
            data = get_wfs_cql(lan)
        except Exception as e2:
            print(f'  GET also failed: {e2}')
            continue

    n = len(data.get('features', []))
    if n == 0:
        print(f'  WARNING: 0 features returned — check LAN value or SKYDDSTYP filter')
        print(f'  Raw (first 300): {json.dumps(data)[:300]}')
        continue

    save(data, path)
    print(f'  OK: {n} features -> {path}')
