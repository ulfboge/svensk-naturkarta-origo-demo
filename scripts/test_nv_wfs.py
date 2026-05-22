#!/usr/bin/env python3
import json
import re
import urllib.parse
import urllib.request

WFS = "https://geodata.naturvardsverket.se/naturvardsregistret/wfs"


def try_get(label, params):
    url = WFS + "?" + urllib.parse.urlencode(params)
    try:
        body = urllib.request.urlopen(url, timeout=60).read().decode("utf-8")
        if body.strip().startswith("{"):
            d = json.loads(body)
            print(f"{label}: OK {len(d.get('features', []))} features")
            return d
        match = re.search(r"ExceptionText[^>]*>([^<]+)", body)
        print(f"{label}: ERR {match.group(1)[:100] if match else body[:100]!r}")
    except Exception as e:
        print(f"{label}: EXC {e}")
    return None


def try_post(lan):
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<wfs:GetFeature service="WFS" version="2.0.0" outputFormat="GEOJSON"
  xmlns:wfs="http://www.opengis.net/wfs/2.0"
  xmlns:fes="http://www.opengis.net/fes/2.0">
  <wfs:Query typeNames="Naturvardsregistret_WFS:SkyddadeOmraden">
    <fes:Filter>
      <fes:And>
        <fes:PropertyIsEqualTo>
          <fes:ValueReference>LAN</fes:ValueReference>
          <fes:Literal>{lan}</fes:Literal>
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
        WFS, data=xml.encode("utf-8"), headers={"Content-Type": "application/xml; charset=UTF-8"}
    )
    d = json.loads(urllib.request.urlopen(req, timeout=120).read().decode("utf-8"))
    print(f"POST {lan!r}: {len(d.get('features', []))} features")


if __name__ == "__main__":
    try_get(
        "GET 1.1.0 GEOJSON",
        {
            "SERVICE": "WFS",
            "VERSION": "1.1.0",
            "REQUEST": "GetFeature",
            "TYPENAME": "Naturvardsregistret_WFS:SkyddadeOmraden",
            "outputFormat": "GEOJSON",
            "MAXFEATURES": "2",
            "SRSNAME": "EPSG:4326",
        },
    )
    try_get(
        "GET 2.0 CQL",
        {
            "SERVICE": "WFS",
            "VERSION": "2.0.0",
            "REQUEST": "GetFeature",
            "TYPENAMES": "Naturvardsregistret_WFS:SkyddadeOmraden",
            "outputFormat": "GEOJSON",
            "CQL_FILTER": "LAN='Gävleborgs Län' AND SKYDDSTYP='Naturreservat'",
        },
    )
    try_get(
        "GET 1.1.0 CQL",
        {
            "SERVICE": "WFS",
            "VERSION": "1.1.0",
            "REQUEST": "GetFeature",
            "TYPENAME": "Naturvardsregistret_WFS:SkyddadeOmraden",
            "outputFormat": "GEOJSON",
            "CQL_FILTER": "LAN='Gävleborgs Län' AND SKYDDSTYP='Naturreservat'",
        },
    )
    try_post("Gävleborgs Län")

    d = try_get(
        "GET sample props",
        {
            "SERVICE": "WFS",
            "VERSION": "2.0.0",
            "REQUEST": "GetFeature",
            "TYPENAMES": "Naturvardsregistret_WFS:SkyddadeOmraden",
            "outputFormat": "GEOJSON",
            "CQL_FILTER": "LAN='Gävleborgs Län' AND SKYDDSTYP='Naturreservat'",
            "count": "1",
        },
    )
    try_post("Västra Götalands Län")
    try_post("Norrbottens Län")
