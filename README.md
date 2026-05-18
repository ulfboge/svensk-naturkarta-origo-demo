# Naturkarta — Skyddad natur och skog

**[Öppna kartan](https://ulfboge.github.io/svensk-naturkarta-origo-demo/) →**

A portfolio web GIS application demonstrating Swedish nature conservation data using [Origo Map](https://github.com/origo-map/origo) — the open-source GIS framework used by Swedish municipalities and county administrative boards (_länsstyrelser_).

> The application mimics a realistic Swedish municipal/regional nature conservation GIS portal.

---

## What it shows

| Lager | Källa | Typ | Klickbar |
|---|---|---|---|
| Naturreservat (Sthlm + Sörmland) | Naturvårdsverket (CC0) | GeoJSON | ✅ |
| Nationalparker (Stockholms län) | Naturvårdsverket (CC0) | GeoJSON | ✅ |
| Natura 2000 SCI — Habitatdirektivet | Naturvårdsverket | WMS | — |
| Natura 2000 SPA — Fågeldirektivet | Naturvårdsverket | WMS | — |
| Biotopskyddsområden | Naturvårdsverket | WMS | — |
| Djur- och växtskyddsområden | Naturvårdsverket | WMS | — |
| Avverkningsanmälningar | Skogsstyrelsen | WMS | — |
| OpenStreetMap / OpenTopoMap | OSM | Tile | — |
| Topowebb (Lantmäteriet) | Lantmäteriet (CC BY) | XYZ/WMTS | — |

Klicka på ett naturreservat eller en nationalpark i Stockholmsområdet för popup med: namn, skyddstyp, IUCN-kategori, areal, beslutsdatum, län, kommun och förvaltare.

---

## Tech stack

| What | How |
|---|---|
| Map framework | [Origo Map v2.10](https://github.com/origo-map/origo/releases/tag/v2.10.0) |
| Rendering engine | OpenLayers 9 (bundled inside Origo) |
| Dev server | `python -m http.server` — no build step |
| Configuration | `public/config/origo.json` — one JSON file controls all layers, styles, and controls |
| Projection | EPSG:3857 display, coordinate readout in SWEREF99 TM + WGS84 |

**No npm. No bundler. No backend.** The same architecture used by many Swedish municipal GIS deployments.

---

## Project structure

```
public/
  css/            Origo CSS + SVG icon sprites (must be at web root)
  js/             origo.min.js — pre-built UMD bundle
  img/            Origo image assets
  config/
    origo.json    ← THE file to edit: layers, styles, controls
  data/
    naturreservat-stockholm.geojson   383 nature reserves, Stockholms Län
    sample-skyddade.geojson           8 handpicked national parks (points)
  src/
    style.css     Custom nature-green theme overrides
  index.html      Loads origo.min.js and calls Origo('config/origo.json')
```

---

## How to run

```powershell
git clone https://github.com/YOUR_USERNAME/svensk-naturkarta-origo-demo
cd svensk-naturkarta-origo-demo
python -m http.server 3000 --directory public
# Open http://localhost:3000
```

No install step. No compilation. Open and edit.

### Aktivera Lantmäteriet Topowebb (valfritt)

1. Registrera ett konto på [opendata.lantmateriet.se](https://opendata.lantmateriet.se/)
2. Skapa en applikation och kopiera din API-nyckel
3. Ersätt `DIN_API_NYCKEL` i `public/config/origo.json` (sök på strängen):

```json
"url": "https://api.lantmateriet.se/open/topowebb-ccby/v1/wmts/token/DIN_API_NYCKEL/..."
```

Lagret *Topowebb (Lantmäteriet)* visas direkt i bakgrundskarta-gruppen efter att nyckeln är insatt.

---

## How to add a WMS layer

All configuration lives in `public/config/origo.json`. The Origo WMS pattern uses a **named source** — the URL belongs in the top-level `source` object, not on the layer:

```json
"source": {
  "naturvardsverket": {
    "url": "https://geodata.naturvardsverket.se/naturvardsregistret/wms"
  }
},
"layers": [
  {
    "name": "nv_naturreservat",
    "title": "Naturreservat",
    "group": "naturskydd",
    "type": "WMS",
    "source": "naturvardsverket",
    "id": "Naturreservat",
    "format": "image/png",
    "sourceParams": { "TRANSPARENT": "true" },
    "visible": true,
    "queryable": false,
    "opacity": 0.75
  }
]
```

`"id"` becomes the `LAYERS=` WMS parameter. `"sourceParams"` maps to additional WMS query parameters. The layer's own `"url"` property is ignored by Origo — always use a named source.

## How to add a clickable GeoJSON layer

```json
{
  "name": "my_layer",
  "title": "Mitt lager",
  "group": "naturskydd",
  "type": "GEOJSON",
  "source": "data/my-file.geojson",
  "visible": true,
  "queryable": true,
  "zIndex": 10,
  "style": "my_style",
  "attributes": [
    { "name": "NAMN",    "title": "Namn",     "prefix": ": " },
    { "name": "AREA_HA", "title": "Areal (ha)", "prefix": ": " }
  ]
}
```

`"zIndex": 10` ensures the vector layer renders on top of tile basemaps. `"prefix": ": "` adds the separator between label and value in the popup.

---

## Data sources & licences

| Dataset | Leverantör | Licens |
|---|---|---|
| Naturreservat, Nationalparker, Natura 2000 | [Naturvårdsverket](https://www.naturvardsverket.se/om-oss/oppna-data-och-apier/) | CC0 |
| Biotopskydd, Djur- och växtskydd | [Naturvårdsverket](https://www.naturvardsverket.se/om-oss/oppna-data-och-apier/) | CC0 |
| Avverkningsanmälningar | [Skogsstyrelsen](https://www.skogsstyrelsen.se/sjalvservice/karttjanster/) | Öppen |
| Topowebb | [Lantmäteriet](https://opendata.lantmateriet.se/) | CC BY |
| Bakgrundskarta | [OpenStreetMap](https://www.openstreetmap.org/) contributors | ODbL |
| Bakgrundskarta | [OpenTopoMap](https://opentopomap.org/) | CC-BY-SA |

The GeoJSON file `naturreservat-stockholm.geojson` was fetched directly from Naturvårdsverket's WFS endpoint using an OGC XML spatial filter and converted with 5-decimal coordinate rounding (~1 m precision).

---

## Architecture decisions

**Why Origo Map?**
Origo is the de facto standard framework for Swedish municipal web GIS. It is used by hundreds of Swedish _kommuner_ and _länsstyrelser_. Knowing Origo is a directly marketable skill. It is built on OpenLayers 9, so knowledge transfers to both ecosystems.

**Why no build step / no npm?**
Origo is distributed as a pre-built UMD bundle. Adding Vite or webpack adds complexity with no functional gain for a configuration-driven app. The Python dev server mirrors how Swedish municipalities typically serve Origo in production environments.

**Why static GeoJSON instead of live WFS?**
Naturvårdsverket's WFS is an ESRI ArcGIS Server endpoint. Origo's WFS client hardcodes `outputFormat=application/json`, which the server rejects — it only accepts GML 3.2 output formats. Pre-downloading as static GeoJSON is the pragmatic solution: it loads faster, works offline, and avoids CORS issues.

**Why EPSG:3857?**
Web Mercator matches OSM and OpenTopoMap tile pyramids. Coordinate display is converted to SWEREF99 TM (Swedish national grid) and WGS84 in the position control.

---

## Roadmap

### Phase 2 — ✅ Klart

- [x] Klickbara GeoJSON-lager (naturreservat + nationalparker, Stockholms län)
- [x] Natura 2000 WMS (SCI + SPA)
- [x] Biotopskyddsområden och djur- och växtskyddsområden (NV WMS)
- [x] Avverkningsanmälningar (Skogsstyrelsen WMS)
- [x] Lantmäteriet Topowebb konfigurerad (kräver API-nyckel)
- [x] GitHub Pages-driftsättning via GitHub Actions

### Phase 3 — Nästa steg

- [ ] Verifiera WMS-lager på live-siten (layer-ID-kontroll)
- [ ] Strandskydd (NV WMS)
- [ ] Utöka GeoJSON-täckning till fler län
- [ ] Sökfunktion över reservatnamn

### Phase 4 — UX

- [ ] Formatted popup values (area with thousands separator, date localisation)
- [ ] Name search across reservat
- [ ] Print layout with Swedish map frame
- [ ] Mobile-responsive layout

### Phase 5 — Backend (future)

- [ ] QGIS Server serving a QGIS project as WMS/WFS
- [ ] PostGIS database with full NV dataset
- [ ] Docker Compose: QGIS Server + PostGIS
- [ ] GeoServer as alternative to QGIS Server

---

## WMS services used

| Tjänst | GetCapabilities |
|---|---|
| NV Naturvårdsregistret | [Länk](https://geodata.naturvardsverket.se/naturvardsregistret/wms?SERVICE=WMS&REQUEST=GetCapabilities) |
| NV Natura 2000 | [Länk](https://geodata.naturvardsverket.se/n2000/wms?SERVICE=WMS&REQUEST=GetCapabilities) |
| Skogsstyrelsen (avverkning) | [Länk](https://geodata.skogsstyrelsen.se/arcgis/services/Avverkningsanmalningar/MapServer/WmsServer?REQUEST=GetCapabilities) |

> ⚠️ Den gamla URL:en `geodata.naturvardsverket.se/naturvardsverket/ows` är **borttagen (404)**. Använd URL:erna ovan.

---

## Useful references

- [Origo Map documentation](https://github.com/origo-map/origo/wiki)
- [Origo v2.10 release](https://github.com/origo-map/origo/releases/tag/v2.10.0)
- [OpenLayers API docs](https://openlayers.org/en/latest/apidoc/)
- [Naturvårdsverket öppna data](https://www.naturvardsverket.se/om-oss/oppna-data-och-apier/)
- [Lantmäteriet öppna geodataprodukter](https://www.lantmateriet.se/sv/geodata/vara-produkter/)

---

## Licence

Code: [MIT](LICENSE)  
Geodata: see Data sources section above.
