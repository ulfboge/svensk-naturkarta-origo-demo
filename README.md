# Naturkarta — Skyddad natur

**[Öppna kartan →](https://ulfboge.github.io/svensk-naturkarta-origo-demo/)**

A portfolio web GIS application showing Swedish nature conservation data across six counties using [Origo Map](https://github.com/origo-map/origo) — the open-source GIS framework used by Swedish municipalities and county administrative boards (_länsstyrelser_).

> The application mimics a realistic Swedish municipal/regional nature conservation GIS portal.

---

## Screenshots

![Karta med lagerpanel och statistikpanel](docs/screenshot-overview.png)
*1 845 naturreservat och 31 nationalparker i sex län. County-selector, sökfunktion och statistikpanel.*

![Popup med reservatinformation och länk till Naturvårdsverket](docs/screenshot-pop-up.png)
*Klickbar popup med namn, skyddstyp, IUCN-kategori, areal, beslutsdatum, förvaltare och direktlänk till Naturvårdsverkets databas.*

---

## What it shows

**1 845 naturreservat** och **31 nationalparker** i sex svenska län:

| Län | Naturreservat | Nationalparker |
|---|---|---|
| Stockholms | 383 | 3 (Tyresta, Ängsö, Nämndö) |
| Södermanlands | 196 | — |
| Uppsala | 201 | 1 (Färnebofjärden, del) |
| Östergötlands | 329 | — |
| Västra Götalands | 545 | 4 (Tresticklan, Djurö, Kosterhavet, Tiveden) |
| Skåne | 391 | 3 (Dalby Söderskog, Söderåsen, Stenshuvud) |

**WMS-lager (rikstäckande):**

| Lager | Källa | Typ |
|---|---|---|
| Natura 2000 SCI — Habitatdirektivet | Naturvårdsverket | WMS |
| Natura 2000 SPA — Fågeldirektivet | Naturvårdsverket | WMS |
| Biotopskyddsområden | Naturvårdsverket | WMS |
| Djur- och växtskyddsområden | Naturvårdsverket | WMS |
| Vattenskyddsområden | Naturvårdsverket | WMS |
| Naturminnen (ytor + punkter) | Naturvårdsverket | WMS |
| Kommunala naturreservat | Naturvårdsverket | WMS |

---

## Key features

- **County selector** — 6 knappar filtrerar GeoJSON-lagren per län och zoomar kartan
- **Reservatsökning** — sök på namn bland alla 1 845 reservat; kartan zoomar direkt till träffen
- **Statistikpanel** — visar antal reservat, total areal (ha) och antal nationalparker för valt län; utformad för att byggas ut med Artdatabanken, jakttider m.m.
- **Klickbar popup** — namn, skyddstyp, IUCN-kategori, areal, beslutsdatum, förvaltare + direktlänk till Naturvårdsverkets databas per reservat
- **Tre bakgrundskartor** — OSM, OpenTopoMap, Lantmäteriet Topowebb (kräver API-nyckel)

---

## Tech stack

| What | How |
|---|---|
| Map framework | [Origo Map v2.10](https://github.com/origo-map/origo/releases/tag/v2.10.0) |
| Rendering engine | OpenLayers 9 (bundled inside Origo) |
| Dev server | `python -m http.server` — no build step |
| Configuration | `public/config/origo.json` — one JSON file controls all layers, styles, and controls |
| Projection | EPSG:3857 display, coordinate readout in SWEREF99 TM + WGS84 |
| Data pipeline | Python + fiona + pyproj — shapefile → WGS84 GeoJSON |

**No npm. No bundler. No backend.** The same architecture used by many Swedish municipal GIS deployments.

---

## Project structure

```
public/
  config/origo.json       ← layers, styles, controls — main config file
  data/
    naturreservat-stockholm-v2.geojson    383 NR, Stockholms län
    naturreservat-sodermanland.geojson    196 NR, Södermanlands län
    naturreservat-uppsala.geojson         201 NR, Uppsala län
    naturreservat-ostergotland.geojson    329 NR, Östergötlands län
    naturreservat-vastragotaland.geojson  545 NR, Västra Götalands län
    naturreservat-skane.geojson           391 NR, Skåne län
    nationalparker-alla.geojson            31 NP, hela Sverige
  src/style.css           custom nature-green theme
  index.html              county selector, search, stats panel (inline JS)
```

---

## How to run

```powershell
git clone https://github.com/ulfboge/svensk-naturkarta-origo-demo
cd svensk-naturkarta-origo-demo
python -m http.server 3000 --directory public
# Open http://localhost:3000
```

### Aktivera Lantmäteriet Topowebb (valfritt)

Ersätt `DIN_API_NYCKEL` i `public/config/origo.json` med din nyckel från [opendata.lantmateriet.se](https://opendata.lantmateriet.se/).

---

## Data sources & licences

| Dataset | Leverantör | Licens |
|---|---|---|
| Naturreservat, Nationalparker, Natura 2000 | [Naturvårdsverket](https://www.naturvardsverket.se/om-oss/oppna-data-och-apier/) | CC0 |
| Biotopskydd, Djur- och växtskydd m.fl. | [Naturvårdsverket](https://www.naturvardsverket.se/om-oss/oppna-data-och-apier/) | CC0 |
| Topowebb | [Lantmäteriet](https://opendata.lantmateriet.se/) | CC BY |
| Bakgrundskarta | [OpenStreetMap](https://www.openstreetmap.org/) contributors | ODbL |

---

## Architecture decisions

**Why Origo Map?**
Origo is the de facto standard framework for Swedish municipal web GIS — used by hundreds of _kommuner_ and _länsstyrelser_. Built on OpenLayers 9, so knowledge transfers to both ecosystems.

**Why no build step?**
Origo is distributed as a pre-built UMD bundle. The Python dev server mirrors how Swedish municipalities typically serve Origo in production.

**Why static GeoJSON?**
Naturvårdsverket's WFS uses GML output only — `application/json` returns an exception. Pre-downloading as GeoJSON loads faster, works offline, and avoids CORS. Data is processed with fiona + pyproj (EPSG:3006 → WGS84).

---

## Roadmap

### ✅ Klart

- [x] Origo Map v2.10 deployed on GitHub Pages
- [x] 1 845 naturreservat i 6 län (GeoJSON, klickbara, sökbara)
- [x] 31 nationalparker (rikstäckande)
- [x] 7 WMS-lager (Natura 2000, biotopskydd, vattenskydd, naturminnen m.fl.)
- [x] County selector med länsbegränsad zoom
- [x] Reservatsökning (namn-autocomplete)
- [x] Statistikpanel (count, areal, NP per valt län)
- [x] Popup-polish (featureinfoTitle, NV-länk, stilade attributrader)
- [x] Mobilanpassning

### Kommande

- [ ] Artdatabanken API — artobservationer per reservat i statistikpanelen
- [ ] Jakttider/jaktrestriktioner (Naturvårdsverket)
- [ ] Fler län
- [ ] Lantmäteriets fastighetsdata — markägare per reservat
- [ ] Planerings- och dispensärenden (kommunala GIS-tjänster)

---

## Useful references

- [Origo Map documentation](https://github.com/origo-map/origo/wiki)
- [Origo v2.10 release](https://github.com/origo-map/origo/releases/tag/v2.10.0)
- [OpenLayers API docs](https://openlayers.org/en/latest/apidoc/)
- [Naturvårdsverket öppna data](https://www.naturvardsverket.se/om-oss/oppna-data-och-apier/)

---

## Licence

Code: [MIT](LICENSE)
Geodata: see Data sources section above.
