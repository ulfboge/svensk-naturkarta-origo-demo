# Naturkarta — Skyddad natur

**[Öppna kartan →](https://ulfboge.github.io/svensk-naturkarta-origo-demo/)**

A portfolio web GIS application showing Swedish nature conservation data across **all 21 counties** using [Origo Map](https://github.com/origo-map/origo) — the open-source GIS framework used by Swedish municipalities and county administrative boards (_länsstyrelser_).

> Mimics a realistic Swedish municipal/regional nature conservation GIS portal: county filter, live external APIs, WMS overlays, and statistics panel.

---

## Screenshots

![Karta med länselector, tidslinje och statistikpanel](docs/screenshot-overview.png)
*5 993 naturreservat och 31 nationalparker i alla 21 län. Dropdown, reservatsökning, tidslinje-slider (1908–2026) och statistikpanel.*

![Statistikpanel för valt län](docs/screenshot-stats.png)
*Statistikpanel (nedre vänster): skyddad natur, GBIF-artobs, planering, jakt & tillträde, IUCN-diagram och väder — uppdateras vid länsbyte och tidslinje.*

![Tidslinje-slider filtrerar karta och statistik](docs/screenshot-timeline.png)
*Datumslidern visar etablerade naturreservat och nationalparker t.o.m. valt år. Statistik och IUCN-fördelning följer med.*

![Popup med reservatinformation och externa länkar](docs/screenshot-pop-up.png)
*Klickbar popup: namn, skyddstyp, IUCN, areal, beslutsdatum, NV-länk, GBIF, Artportalen, planering och väder.*

---

## Architecture

Static site (GitHub Pages) with **no backend** — data is loaded client-side with automatic source selection:

```
                    ┌─────────────────────┐
                    │   public/index.html  │
                    │   county selector    │
                    └──────────┬──────────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         ▼                     ▼                     ▼
  QGIS Server WFS      NV WFS (live)         GeoJSON (lazy)
  localhost:8081       GitHub Pages          fallback / alla län
  docker + dev_server  per county select     on demand per län
```

| Environment | Naturreservat source | How |
|---|---|---|
| **GitHub Pages** | NV WFS → GeoJSON fallback | `probeNvWfs()` at startup; live fetch per county; static GeoJSON if NV cap (>500) or offline |
| **Local + Docker** | QGIS Server WFS | `probeQgisWfs()` via `scripts/dev_server.py` proxy |
| **Static only** | GeoJSON lazy-load | `python -m http.server` — files fetched when county is selected |

GeoJSON layers start as `empty.geojson` in `origo.json` to avoid loading 5 993 polygons at page load. Real county files are fetched in JavaScript when a län is activated.

See [NV_WFS_PLAN.md](NV_WFS_PLAN.md) and [QGIS_SERVER_PLAN.md](QGIS_SERVER_PLAN.md).

---

## GBIF vs Artportalen

Both appear in the statistics panel and popup, but serve different roles:

| | **GBIF** | **Artportalen** |
|---|---|---|
| **What** | Global biodiversity database | Sweden's national species observation portal (Artdatabanken/SLU) |
| **In this app** | Live count (2020–2025) via API | Deep link only — no count fetched |
| **Filter** | Bounding box of selected county/reserve | County code, or NVRID in popup |
| **Best for** | Quick overview, API integration demo | Detailed Swedish records, citizen science |

---

## What it shows

**5 993 naturreservat** and **31 nationalparker** in all 21 Swedish counties (table abbreviated):

| Län | NR | NP | Län | NR | NP |
|---|---|---|---|---|---|
| Stockholms | 383 | 3 | Gävleborgs | 252 | 2 |
| Västra Götalands | 545 | 4 | Norrbottens | 529 | 8 |
| Skåne | 391 | 3 | … | … | … |

Full county table in [CLAUDE.md](CLAUDE.md). National parks are filtered per county via the `LAN` attribute.

**WMS layers (nationwide):** Natura 2000, biotopskydd, vattenskydd, naturminnen, planering (NV + Boverket riksintressen), tillträdesförbud, terräng/höjd (Lantmäteriet NH).

---

## Key features

- **County dropdown** — 21 län + Hela Sverige; zoom, legend filter, lazy data load
- **Timeline slider (1908–2026)** — filters NR/NP by establishment year; live stats + IUCN chart
- **Reserve search** — autocomplete per county, zoom to feature
- **Statistics panel** — NR count/area, national parks, GBIF observations, planning links, IUCN bars, weather
- **Popup** — NV, GBIF, Artportalen (NVRID), Boverket, Open-Meteo weather
- **Three basemaps** — OSM, OpenTopoMap, Lantmäteriet Topowebb
- **Legend** — hides duplicate WFS/GeoJSON entries; county-aware layer list

---

## Tech stack

| What | How |
|---|---|
| Map framework | [Origo Map v2.10](https://github.com/origo-map/origo/releases/tag/v2.10.0) |
| Rendering | OpenLayers 9 (bundled in Origo) |
| Dev server | `python -m http.server` or `scripts/dev_server.py` — **no npm, no build step** |
| Config | `public/config/origo.json` |
| Projection | EPSG:3857 display; SWEREF99 TM + WGS84 in coordinate readout |
| Data pipeline | Python + fiona/pyproj — shapefile → WGS84 GeoJSON |

---

## Project structure

```
public/
  config/origo.json          ← layers, styles, controls (GeoJSON → empty.geojson stubs)
  data/
    naturreservat-*.geojson  ← 21 counties (lazy-loaded)
    nationalparker-alla.geojson
    empty.geojson            ← placeholder until county selected
  index.html                 ← county selector, lazy load, stats, APIs
  src/style.css
scripts/
  build_qgis_wfs_project.py  ← QGIS GPKG + WFS layer sync
  capture_screenshots.py     ← Playwright README images
  dev_server.py              ← static + QGIS proxy
docker-compose.yml           ← QGIS Server (optional local WFS)
```

---

## How to run

```powershell
git clone https://github.com/ulfboge/svensk-naturkarta-origo-demo
cd svensk-naturkarta-origo-demo
python -m http.server 3000 --directory public
# Open http://localhost:3000
```

### QGIS Server (local WFS, optional)

Requires Docker Desktop. See [QGIS_SERVER_PLAN.md](QGIS_SERVER_PLAN.md).

```powershell
docker compose up -d
python scripts/dev_server.py
# Open http://localhost:3000
```

### Live NV WFS (GitHub Pages)

Without Docker, naturreservat are fetched live from Naturvårdsverket when a county is selected. See [NV_WFS_PLAN.md](NV_WFS_PLAN.md).

### Update screenshots

```powershell
python -m http.server 3000 --directory public
pip install playwright && python -m playwright install chromium
python scripts/capture_screenshots.py
```

Wait for OSM tiles to load — the script checks for rendered basemap tiles before capture.

---

## Data sources & licences

| Dataset | Provider | Licence |
|---|---|---|
| Naturreservat, Nationalparker, Natura 2000 | [Naturvårdsverket](https://www.naturvardsverket.se/om-oss/oppna-data-och-apier/) | CC0 |
| Artobservationer (count) | [GBIF](https://www.gbif.org) API | CC BY |
| Artobservationer (links) | [Artportalen](https://www.artportalen.se) | — |
| Weather | [Open-Meteo](https://open-meteo.com) | CC BY 4.0 |
| Topowebb, Markhöjd NH | [Lantmäteriet](https://opendata.lantmateriet.se/) | CC BY |
| Basemap | [OpenStreetMap](https://www.openstreetmap.org/) | ODbL |

---

## Roadmap

### Done

- [x] 5 993 NR + 31 NP in all 21 counties
- [x] WMS layers (Natura 2000, planning, hunting, terrain)
- [x] County dropdown, search, stats, timeline, IUCN chart
- [x] GBIF live API + Artportalen deep links
- [x] QGIS Server WFS (local) + NV WFS (GitHub Pages)
- [x] Legend county filter, README screenshots with basemap
- [x] Lazy-load GeoJSON per county (performance)

### Possible next steps

- [ ] SWEREF99 TM as display projection
- [ ] SMHI open API instead of Open-Meteo
- [ ] Artportalen count if open API available
- [ ] Share map / permalink (Origo built-in)

---

## Useful references

- [Origo Map documentation](https://github.com/origo-map/origo/wiki)
- [Naturvårdsverket öppna data](https://www.naturvardsverket.se/om-oss/oppna-data-och-apier/)
- [AI context for contributors](CLAUDE.md)

---

## Licence

Code: [MIT](LICENSE)  
Geodata: see Data sources section above.
