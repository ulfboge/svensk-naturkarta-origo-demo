# Naturkarta — Skyddad natur

**[Öppna kartan →](https://ulfboge.github.io/svensk-naturkarta-origo-demo/)**

A portfolio web GIS application showing Swedish nature conservation data using [Origo Map](https://github.com/origo-map/origo) — the open-source GIS framework used by Swedish municipalities and county administrative boards (_länsstyrelser_).

> The application mimics a realistic Swedish municipal/regional nature conservation GIS portal.

---

## Screenshots

![Karta med lagerpanel öppen](docs/screenshot-overview.png)
*Naturreservat och nationalparker i Stockholms och Södermanlands län. Lagerpanel med undermapp och county-selector.*

![Popup på ett naturreservat](docs/screenshot-pop-up.png)
*Klickbar popup med namn, skyddstyp, IUCN-kategori, areal, beslutsdatum, kommun och förvaltare.*

---

## What it shows

| Lager | Källa | Typ | Klickbar |
|---|---|---|---|
| Naturreservat — Stockholms län | Naturvårdsverket (CC0) | GeoJSON | ✅ |
| Naturreservat — Södermanlands län | Naturvårdsverket (CC0) | GeoJSON | ✅ |
| Nationalparker — Stockholms/Södermanlands | Naturvårdsverket (CC0) | GeoJSON | ✅ |
| Natura 2000 SCI — Habitatdirektivet | Naturvårdsverket | WMS | — |
| Natura 2000 SPA — Fågeldirektivet | Naturvårdsverket | WMS | — |
| Biotopskyddsområden | Naturvårdsverket | WMS | — |
| Djur- och växtskyddsområden | Naturvårdsverket | WMS | — |
| OpenStreetMap / OpenTopoMap | OSM | Tile | — |
| Topowebb (Lantmäteriet) | Lantmäteriet (CC BY) | XYZ/WMTS | — |

**County selector** — knappar i kartans överdel filtrerar GeoJSON-lagren per län (Stockholms / Södermanlands / Båda) och zoomar kartan till valt läns utbredning.

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
    naturreservat-stockholm-v2.geojson   383 naturreservat, Stockholms län
    naturreservat-sodermanland.geojson   196 naturreservat, Södermanlands län
    nationalparker-sthlm-sod.geojson     3 nationalparker
  src/
    style.css     Custom nature-green theme overrides
  index.html      Loads origo.min.js, calls Origo('config/origo.json'), county selector JS
```

---

## How to run

```powershell
git clone https://github.com/ulfboge/svensk-naturkarta-origo-demo
cd svensk-naturkarta-origo-demo
python -m http.server 3000 --directory public
# Open http://localhost:3000
```

No install step. No compilation. Open and edit.

### Aktivera Lantmäteriet Topowebb (valfritt)

1. Registrera ett konto på [opendata.lantmateriet.se](https://opendata.lantmateriet.se/)
2. Skapa en applikation och kopiera din API-nyckel
3. Ersätt `DIN_API_NYCKEL` i `public/config/origo.json`:

```json
"url": "https://api.lantmateriet.se/open/topowebb-ccby/v1/wmts/token/DIN_API_NYCKEL/..."
```

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
    "name": "nv_biotopskydd",
    "title": "Biotopskyddsområden",
    "group": "nv_rikstackande",
    "type": "WMS",
    "source": "naturvardsverket",
    "id": "Ovrigt_biotopskyddsomrade",
    "format": "image/png",
    "sourceParams": { "TRANSPARENT": "true" },
    "visible": false,
    "queryable": false
  }
]
```

`"id"` becomes the `LAYERS=` WMS parameter. The layer's own `"url"` property is ignored by Origo — always use a named source.

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
    { "name": "NAMN",    "title": "Namn",       "prefix": ": " },
    { "name": "AREA_HA", "title": "Areal (ha)", "prefix": ": " }
  ]
}
```

---

## Data sources & licences

| Dataset | Leverantör | Licens |
|---|---|---|
| Naturreservat, Nationalparker, Natura 2000 | [Naturvårdsverket](https://www.naturvardsverket.se/om-oss/oppna-data-och-apier/) | CC0 |
| Biotopskydd, Djur- och växtskydd | [Naturvårdsverket](https://www.naturvardsverket.se/om-oss/oppna-data-och-apier/) | CC0 |
| Topowebb | [Lantmäteriet](https://opendata.lantmateriet.se/) | CC BY |
| Bakgrundskarta | [OpenStreetMap](https://www.openstreetmap.org/) contributors | ODbL |
| Bakgrundskarta | [OpenTopoMap](https://opentopomap.org/) | CC-BY-SA |

GeoJSON-filerna hämtades från Naturvårdsverkets WFS-tjänst med OGC XML spatial filter och koordinater rundade till 5 decimaler (~1 m precision).

---

## Architecture decisions

**Why Origo Map?**
Origo is the de facto standard framework for Swedish municipal web GIS. It is used by hundreds of Swedish _kommuner_ and _länsstyrelser_. Knowing Origo is a directly marketable skill — built on OpenLayers 9, so knowledge transfers to both ecosystems.

**Why no build step / no npm?**
Origo is distributed as a pre-built UMD bundle. The Python dev server mirrors how Swedish municipalities typically serve Origo in production environments.

**Why static GeoJSON instead of live WFS?**
Naturvårdsverket's WFS only accepts GML output formats — `application/json` returns an ExceptionReport. Pre-downloading as static GeoJSON loads faster, works offline, and avoids CORS issues.

**Why EPSG:3857?**
Web Mercator matches OSM and OpenTopoMap tile pyramids. Coordinate display is converted to SWEREF99 TM and WGS84 in the position control.

---

## Roadmap

### ✅ Klart

- [x] Origo Map v2.10 deployed as static site on GitHub Pages
- [x] OSM, OpenTopoMap och Lantmäteriet Topowebb som bakgrundskartor
- [x] Klickbara GeoJSON-lager — naturreservat (Stockholm + Södermanland) och nationalparker
- [x] Natura 2000 WMS (SCI Habitatdirektivet + SPA Fågeldirektivet)
- [x] Biotopskyddsområden och djur- och växtskyddsområden (NV WMS)
- [x] County selector — filtrera per Stockholms/Södermanlands/Båda länen
- [x] Undermapp "Naturreservat" i lagerpanelen under Skyddad natur

### Nästa steg

- [ ] Formaterad popup (tusenseparator för areal, datumformatering)
- [ ] Strandskydd (NV WMS)
- [ ] Fler län (Uppsala, Östergötland)
- [ ] Sökfunktion över reservatnamn
- [ ] Mobilanpassning av county selector

---

## WMS services used

| Tjänst | GetCapabilities |
|---|---|
| NV Naturvårdsregistret | [Länk](https://geodata.naturvardsverket.se/naturvardsregistret/wms?SERVICE=WMS&REQUEST=GetCapabilities) |
| NV Natura 2000 | [Länk](https://geodata.naturvardsverket.se/n2000/wms?SERVICE=WMS&REQUEST=GetCapabilities) |

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
