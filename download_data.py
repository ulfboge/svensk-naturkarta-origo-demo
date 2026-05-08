"""
Laddar ner naturreservat från Naturvårdsverket och sparar som GeoJSON.
Kör: python download_data.py
"""

import json
import os
import urllib.request
import urllib.parse

OUT_DIR = os.path.join(os.path.dirname(__file__), "public", "data")
os.makedirs(OUT_DIR, exist_ok=True)

KEEP_PROPS = {
    "NAMN", "SKYDDSTYP", "IUCNKATEGORI", "AREA_HA",
    "URSPR_BESLUTSDATUM", "LAN", "KOMMUN", "FORVALTARE"
}

WFS_BASE = "https://geodata.naturvardsverket.se/naturvardsregistret/wfs"


def get(url):
    """Hämtar URL och returnerar (status, content_type, body_str)."""
    proxy_handler = urllib.request.ProxyHandler({})
    opener = urllib.request.build_opener(proxy_handler)
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept": "application/json, */*",
        },
    )
    with opener.open(req, timeout=90) as resp:
        body = resp.read().decode("utf-8")
        return resp.status, resp.headers.get("Content-Type", ""), body


def try_wfs(label, params):
    url = WFS_BASE + "?" + params
    print(f"\n[{label}]")
    print(f"  {url[:110]}...")
    try:
        status, ct, body = get(url)
        print(f"  HTTP {status}  |  {len(body)} tecken  |  {body[:80]!r}")
        if body.strip().startswith("{"):
            d = json.loads(body)
            n = len(d.get("features", []))
            print(f"  Features: {n}")
            return d if n > 0 else None
        else:
            print(f"  Icke-JSON svar: {body[:200]}")
    except Exception as e:
        print(f"  FEL: {e}")
    return None


def round_coords(geom):
    t = geom["type"]
    if t == "MultiPolygon":
        geom["coordinates"] = [
            [[[round(c, 5) for c in pt] for pt in ring] for ring in poly]
            for poly in geom["coordinates"]
        ]
    elif t == "Polygon":
        geom["coordinates"] = [
            [[round(c, 5) for c in pt] for pt in ring]
            for ring in geom["coordinates"]
        ]


def save(data, filename):
    """Filtrera på Stockholm+Naturreservat, spara till public/data/."""
    filtered = [
        f for f in data["features"]
        if f["properties"].get("SKYDDSTYP") == "Naturreservat"
        and str(f["properties"].get("LAN", "")).startswith("Stockholms")
    ]
    data["features"] = filtered

    for feature in data["features"]:
        feature["properties"] = {
            k: v for k, v in feature["properties"].items() if k in KEEP_PROPS
        }
        round_coords(feature["geometry"])

    out = os.path.join(OUT_DIR, filename)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    kb = os.path.getsize(out) // 1024
    print(f"\n  Sparad: {out}  ({kb} KB, {len(data['features'])} naturreservat)")
    return len(data["features"])


# ── WFS-varianter att testa ───────────────────────────────────────────────

VARIANTS = [
    # WFS 2.0 med namespace
    ("WFS 2.0 + namespace",
     "SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature"
     "&TYPENAMES=Naturvardsregistret_WFS:SkyddadeOmraden"
     "&OUTPUTFORMAT=GEOJSON&COUNT=5"),

    # WFS 2.0 utan namespace
    ("WFS 2.0 utan namespace",
     "SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature"
     "&TYPENAMES=SkyddadeOmraden"
     "&OUTPUTFORMAT=GEOJSON&COUNT=5"),

    # WFS 1.1.0
    ("WFS 1.1.0",
     "SERVICE=WFS&VERSION=1.1.0&REQUEST=GetFeature"
     "&TYPENAME=Naturvardsregistret_WFS:SkyddadeOmraden"
     "&OUTPUTFORMAT=GEOJSON&MAXFEATURES=5"),

    # WFS 1.0.0
    ("WFS 1.0.0",
     "SERVICE=WFS&VERSION=1.0.0&REQUEST=GetFeature"
     "&TYPENAME=Naturvardsregistret_WFS:SkyddadeOmraden"
     "&OUTPUTFORMAT=GEOJSON&MAXFEATURES=5"),
]


if __name__ == "__main__":
    print("Testar NV WFS med 5 features (COUNT=5)...\n")

    working = None
    for label, params in VARIANTS:
        result = try_wfs(label, params)
        if result is not None:
            print(f"  --> FUNGERAR med varianten '{label}'")
            working = (label, params.replace("COUNT=5", "COUNT=100000")
                                     .replace("MAXFEATURES=5", "MAXFEATURES=100000"))
            break

    if working is None:
        print("\n\nINGEN VARIANT FUNGERADE.")
        print("Prova att klistra in denna URL i Chrome och se om du får data:")
        print()
        print("  " + WFS_BASE +
              "?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature"
              "&TYPENAMES=Naturvardsregistret_WFS:SkyddadeOmraden"
              "&OUTPUTFORMAT=GEOJSON&COUNT=2")
        print()
        print("Återkoppla vad du ser i webbläsaren.")
    else:
        label, full_params = working
        print(f"\nHämtar ALLT med varianten '{label}'...")
        data = try_wfs("Fullständig hämtning", full_params)
        if data and len(data["features"]) > 0:
            n = save(data, "naturreservat-stockholm.geojson")
            if n > 0:
                print("\nKlart! Starta servern: python -m http.server 3000 --directory public")
            else:
                print("\nData hämtad men inga Naturreservat i Stockholms Län hittades.")
        else:
            print("\nKunde inte hämta fullständig data.")
