# NV WFS — live data from Naturvårdsverket

Live naturreservat hämtas från [Naturvårdsverkets WFS](https://geodata.naturvardsverket.se/naturvardsregistret/wfs) när lokal QGIS Server inte körs.

## Datakällprioritet

1. **Lokal QGIS Server** (`docker compose up` + `scripts/dev_server.py`) — utveckling
2. **NV WFS** — live på GitHub Pages och utan Docker
3. **Statisk GeoJSON** — fallback om NV svarar fel, vid "Hela Sverige", eller län med >500 NR

## Tekniskt

| | |
|---|---|
| Endpoint | `https://geodata.naturvardsverket.se/naturvardsregistret/wfs` |
| Layer | `Naturvardsregistret_WFS:SkyddadeOmraden` |
| Filter | WFS 2.0 `CQL_FILTER` per län + `SKYDDSTYP='Naturreservat'` |
| LAN-format | `Stockholms Län` (stort L — inte `län`) |
| CORS | Ja (`Access-Control-Allow-Origin: *`) |
| Max per request | 500 features (NV begränsning) |

Län med fler än 500 naturreservat (Västra Götaland, Norrbotten) använder lokal GeoJSON automatiskt.

## Test

```powershell
python scripts/test_nv_wfs.py
```

## Källkod

Logik i `public/index.html`: `probeNvWfs`, `loadNvWfsIntoLayer`, `shouldLoadNvCounty`.
