#!/usr/bin/env python3
import json
import urllib.parse
import urllib.request

WFS = "https://geodata.naturvardsverket.se/naturvardsregistret/wfs"
LAN = "Västra Götalands Län"
CQL = f"LAN='{LAN}' AND SKYDDSTYP='Naturreservat'"


def get(params):
    url = WFS + "?" + urllib.parse.urlencode(params)
    return json.loads(urllib.request.urlopen(url, timeout=120).read().decode("utf-8"))


for count in [500, 1000, 2000]:
    d = get(
        {
            "SERVICE": "WFS",
            "VERSION": "2.0.0",
            "REQUEST": "GetFeature",
            "TYPENAMES": "Naturvardsregistret_WFS:SkyddadeOmraden",
            "outputFormat": "GEOJSON",
            "CQL_FILTER": CQL,
            "count": str(count),
        }
    )
    print(f"count={count}: {len(d['features'])} features")

page1 = get(
    {
        "SERVICE": "WFS",
        "VERSION": "2.0.0",
        "REQUEST": "GetFeature",
        "TYPENAMES": "Naturvardsregistret_WFS:SkyddadeOmraden",
        "outputFormat": "GEOJSON",
        "CQL_FILTER": CQL,
        "count": "500",
        "startIndex": "0",
    }
)
page2 = get(
    {
        "SERVICE": "WFS",
        "VERSION": "2.0.0",
        "REQUEST": "GetFeature",
        "TYPENAMES": "Naturvardsregistret_WFS:SkyddadeOmraden",
        "outputFormat": "GEOJSON",
        "CQL_FILTER": CQL,
        "count": "500",
        "startIndex": "500",
    }
)
print(f"page1: {len(page1['features'])}, page2: {len(page2['features'])}, total: {len(page1['features']) + len(page2['features'])}")
