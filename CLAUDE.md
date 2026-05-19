# CLAUDE.md — AI Context for svensk-naturkarta-origo-demo

This file gives Claude (or any AI assistant) the context needed to help with this project without re-explaining from scratch every session.

---

## Project in one sentence

A portfolio web GIS application showing Swedish nature conservation data (naturskyddade områden, Natura 2000, skogsdata) using Origo Map v2.10 — mimicking a realistic Swedish municipal/regional GIS portal.

---

## Owner

- **Name:** Johan
- **Background:** GIS engineer/web GIS (beginner–intermediate web dev, strong GIS background)
- **Tools:** Windows 11, VS Code, PowerShell, QGIS, Git
- **Goal:** Strengthen portfolio for Swedish GIS/web GIS roles

---

## Tech stack

| What | How |
|---|---|
| Map framework | Origo Map v2.10 (pre-built UMD browser bundle — NOT via npm) |
| Render engine | OpenLayers 9 (bundled inside `origo.min.js`) |
| Dev server | Python: `python -m http.server 3000 --directory public` |
| Entry point | `public/index.html` (loads `js/origo.min.js`, calls `Origo('config/origo.json')`) |
| Map config | `public/config/origo.json` (JSON only — no code changes needed for layers) |
| Sample data | `public/data/*.geojson` |
| Custom styles | `public/src/style.css` (minimal overrides — nature-green theme) |
| Projection | EPSG:3857 (Web Mercator) |

**No npm. No Vite. No build step.** The Origo bundle is served as-is.

---

## Directory layout (critical — Origo hardcodes these paths)

```
public/
  css/            ← Origo CSS + SVG icons (MUST be at web root, not origo/css/)
    style.css
    svg/
      fa-icons.svg
      material-icons.svg
      ...
  js/             ← Origo JS bundle (MUST be at web root)
    origo.min.js
    origo.js      ← unminified, useful for debugging
  img/            ← Origo images (MUST be at web root)
    png/
      osm.png     ← image used by "karta_osm" style
      ...
  origo/          ← original Origo release zip contents (source of truth, not served directly)
  config/
    origo.json    ← THE main file to edit
  data/
    sample-skyddade.geojson
  src/
    style.css     ← custom green theme overrides
  index.html
```

Origo's JS requests `/css/svg/fa-icons.svg`, `/img/png/osm.png` etc. relative to the **page root**. If those folders are not at the root, you'll see 404 errors and a broken UI. The `origo/` folder is kept as a reference but the working files are copied to root-level `css/`, `js/`, `img/`.

---

## How to run

```powershell
cd C:\Users\galag\GitHub\svensk-naturkarta-origo-demo
python -m http.server 3000 --directory public
# open http://localhost:3000
```

---

## Current state (Phase 3 — COMPLETE ✅, 2026-05-19)

### Fase 1–2 ✅ (se git-historik för detaljer)

### Phase 3 ✅ — komplett portfolioapplikation

**GeoJSON-data (lokal NV-data, extraherat med fiona/pyproj från EPSG:3006→WGS84):**
- 1 845 naturreservat i 6 län: Stockholm (383), Södermanland (196), Uppsala (201), Östergötland (329), Västra Götaland (545), Skåne (391)
- 31 nationalparker rikstäckande (`nationalparker-alla.geojson`)
- Fältnamn: NVRID, NAAM, SKYDDSTYP, IUCNKATEGORI, AREA_HA, URSPR_BESLUTSDATUM, KOMMUN, FORVALTARE, LAN

**WMS-lager (11 st i 4 grupper):**
- `naturskydd`: Naturreservat-undermapp + Nationalparker
- `natura2000`: Habitatdirektivet, Fågeldirektivet
- `nv_rikstackande`: Biotopskydd, Djur/växt, Vattenskydd, Naturminnen (yta+punkt), Kommunala NR, Tilltradesforbud, Interimistiskt_forbud
- `planering`: Beslutsstatus, Naturvardsomrade, Riksintressen (Boverket)
- `lm_fastighet`: Fastighetsgränser (avgiftsbelagd, DIN_API_NYCKEL)

**Bakgrundskartor:**
- OSM (synlig som standard), OpenTopoMap (XYZ), Lantmäteriet Topowebb (WMTS, konfigurerad med riktig nyckel)

**UX-funktioner i `public/index.html`:**
- County selector (6 knappar) — styr synlighet, zoom, söklista, statistikpanel
- Reservatsökning — `<datalist>` filtrerad per valt län, `featuresloadend`-lyssning för lazy-load
- Statistikpanel (nedre vänster, 4 sektioner): Skyddad natur | GBIF artobs | Planering | Jakt & tillträde | Fastighetsdata
- GBIF live-API — per reservat (popup) och per valt län (stats), `fetch()` med bbox
- Popup-polish — `featureinfoTitle: "NAAM"`, formaterad areal (MutationObserver), datum (formatDatetime)
- Popup-länkar: NV Geocache, GBIF, Artportalen, MinKarta (LM), Boverket riksintressen, NV Ärenden
- Mobilanpassning — `flex-wrap`, `max-width: calc(100vw - 16px)`

**Kritisk Origo API-lärdom:**
`viewer.getMap()` finns INTE — använd alltid `viewer.api().getMap()`

**Datakällor (lokala filer för extraktion):**
- `E:/NR/NR/NR_polygon.shp` — alla svenska naturreservat (5 993 st, EPSG:3006)
- `E:/NP/NP/NP_polygon.shp` — alla svenska nationalparker (31 st, EPSG:3006)
- `E:/LM2026_Topo_50/naturvard_sverige/naturvard_sverige.gpkg` — Lantmäteriet topo (saknar NAAM)

---

## Möjliga nästa steg (Phase 4)

1. **Nya screenshots** — README-bilderna speglar inte nuläget (saknar stats-panel, planering, jakt m.m.)
2. **Fler län** — kör `extract_nr_extra.py` med ytterligare län från `NR_polygon.shp`
3. **SMHI öppna API** — väder/klimat per reservat (gratis, ingen nyckel)
4. **Artportalen djuplänk** — per reservat med NVRID som sökparameter
5. **QGIS Server** — ersätt statisk GeoJSON med live WFS (fas 4 i ursprungsplan)
6. **Prestandaoptimering** — lazy-load GeoJSON per county

---

## Key constraints

- **No npm / No build step** — pure static HTML served via Python http.server
- **No Docker, No PostGIS, No backend** — all data from external WMS or local GeoJSON
- **Configuration-first** — prefer editing origo.json over writing JavaScript
- **Swedish geodata only** — all layers should relate to Swedish nature/forest themes

---

## CRITICAL: Origo WMS layer pattern

**Wrong (does NOT work — `"url"` on a WMS layer is silently ignored by Origo):**
```json
{
  "name": "my_layer",
  "type": "WMS",
  "url": "https://example.com/wms",
  "params": { "LAYERS": "layer_name", "FORMAT": "image/png" }
}
```

**Correct (named source + `"id"` for the WMS LAYERS param):**
```json
{
  "source": {
    "my_server": { "url": "https://example.com/wms" }
  },
  "layers": [
    {
      "name": "my_layer",
      "type": "WMS",
      "source": "my_server",
      "id": "layer_name",
      "format": "image/png",
      "sourceParams": { "TRANSPARENT": "true" }
    }
  ]
}
```

**Why:** Origo's WMS handler gets the URL from `viewer.getMapSource()[layerOptions.source]` — the named source dictionary. The layer's own `"url"` property is never read. The `"id"` field becomes the `LAYERS=` WMS param. Extra WMS params go in `"sourceParams"` (not `"params"`).

**GeoJSON layers are different** — they still use `"source"` as a file path: `"source": "data/file.geojson"`.

---

## CRITICAL: index.html requirements

```html
<!-- #app-wrapper MUST be completely empty — Origo fills it entirely -->
<div id="app-wrapper"></div>
<script src="js/origo.min.js"></script>
<script type="text/javascript">
  var viewer = Origo('config/origo.json');
</script>
```

Any child element inside `#app-wrapper` will prevent Origo from rendering.

---

## CRITICAL: OSM layer requires karta_osm style

```json
{
  "name": "osm",
  "type": "OSM",
  "style": "karta_osm",
  "visible": true
}
```

```json
"styles": {
  "karta_osm": [[{ "image": { "src": "img/png/osm.png" } }]]
}
```

Without `"style": "karta_osm"`, the OSM layer renders no tiles.

---

## CRITICAL: resolutions array must start at 156543.03

```json
"resolutions": [
  156543.03, 78271.52, 39135.76, 19567.88, 9783.94,
  4891.97,   2445.98,  1222.99,  611.50,   305.75,
  152.87,    76.437,   38.219,   19.109,   9.5546,
  4.7773,    2.3887,   1.1943,   0.5972
]
```

A truncated resolutions array (e.g. starting at zoom level 11) causes a white screen — the initial zoom level has no matching resolution.

---

## Adding a layer

Edit `public/config/origo.json` → `layers` array. No JS change needed.
- `name` must be unique (used as Origo's internal identifier)
- `group` must match an entry in the `groups` array
- For WMS: use named source (see pattern above); `id` = WMS LAYERS param
- For GeoJSON: `source` = relative path to file, `style` = style name in `styles` object

---

## Debugging

Open browser console (F12). `window.viewer` exposes the Origo viewer.
`window.viewer.getMap()` returns the raw OpenLayers map object.

Common errors:
- **`TypeError: Cannot read properties of null (reading '0')` at `getLegendUrl`** → WMS layer is using `"url"` instead of a named source. Use the correct pattern above.
- **White screen, no tiles** → Check resolutions array starts at 156543.03; check OSM layer has `"style": "karta_osm"`
- **404 for `/css/svg/fa-icons.svg`** → The `css/` folder is not at the web root. Copy from `origo/css/`.
- **Green screen (loading stuck)** → `#app-wrapper` has a child element, or Origo crashed early (check console).

---

## WMS services used

| Service | GetCapabilities URL |
|---|---|
| NV Naturvardsregistret | https://geodata.naturvardsverket.se/naturvardsregistret/wms?SERVICE=WMS&REQUEST=GetCapabilities |
| NV Natura 2000 | https://geodata.naturvardsverket.se/n2000/wms?SERVICE=WMS&REQUEST=GetCapabilities |
| Skogsstyrelsen (avverkning) | https://geodata.skogsstyrelsen.se/arcgis/services/Avverkningsanmalningar/MapServer/WmsServer?REQUEST=GetCapabilities |
| Skogsstyrelsen (grunddata) | https://geodata.skogsstyrelsen.se/arcgis/services/Skogliga_grunddata/MapServer/WmsServer?REQUEST=GetCapabilities |

> **Note:** The old URL `geodata.naturvardsverket.se/naturvardsverket/ows` is **dead (404)**. Use the new URLs above.

---

## Useful references

- Origo Map GitHub: https://github.com/origo-map/origo
- Origo v2.10 release: https://github.com/origo-map/origo/releases/tag/v2.10.0
- OpenLayers API: https://openlayers.org/en/latest/apidoc/
- Naturvårdsverket öppna data: https://www.naturvardsverket.se/om-oss/oppna-data-och-apier/
- Lantmäteriet öppna geodataprodukter: https://www.lantmateriet.se/sv/geodata/vara-produkter/
- SWEREF99 proj4: `+proj=utm +zone=33 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs`
