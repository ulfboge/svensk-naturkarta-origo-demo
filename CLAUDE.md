# CLAUDE.md — AI Context for svensk-naturkarta-origo-demo

This file gives Claude (or any AI assistant) the context needed to help with this project without re-explaining from scratch every session.

---

## Project in one sentence

A portfolio web GIS application showing Swedish nature conservation data (naturskyddade områden, Natura 2000, skogsdata) using Origo Map — mimicking a realistic Swedish municipal/regional GIS portal.

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
| Map framework | `origo-map` npm package |
| Render engine | OpenLayers (bundled inside Origo) |
| Dev/build | Vite 5 |
| Entry point | `src/main.js` (imports Origo CSS + calls `Origo(config)`) |
| Map config | `public/config/origo.json` (JSON only — no code changes needed for layers) |
| Sample data | `public/data/*.geojson` |
| Styles | `src/style.css` (overrides on top of origo-map/css/origo.css) |
| Projection | EPSG:3857 now; plan to switch to EPSG:3006 (SWEREF99 TM) later |

---

## Current state (Phase 1 — complete)

- [x] Folder structure created
- [x] README, CLAUDE.md, docs/ written
- [x] package.json + vite.config.js
- [x] index.html (Origo mount point)
- [x] src/main.js — fetches origo.json, calls Origo(), exposes viewer on window
- [x] src/style.css — full-page map, nature-green loading screen
- [x] public/config/origo.json — OSM background + NV WMS layers + local GeoJSON
- [x] public/data/sample-skyddade.geojson — sample protected-area polygons
- [x] Git repository initialised

---

## What to do next (Phase 2)

1. Run `npm install` and `npm run dev` to verify the map loads
2. Open the GetCapabilities URLs in docs/02_data_sources.md and verify layer names
3. Update the layer names in origo.json based on actual GetCapabilities response
4. Test the Naturvårdsverket WMS layers (they should load with internet access)
5. Add Skogsstyrelsen WMS layer (avverkningsanmälningar or skogliga grunddata)
6. Check popup attributes on each WMS layer and update the `attributes` array

---

## Key constraints

- **No Docker** — everything runs locally on Windows
- **No PostGIS** — all data from external WMS/WFS or local GeoJSON for now
- **No backend code** — pure frontend; Vite proxy handles CORS for localhost services
- **Configuration-first** — prefer editing origo.json over writing JavaScript
- **Swedish geodata only** — all layers should relate to Swedish nature/forest themes

---

## Important patterns

### Adding a layer
Edit `public/config/origo.json` → `layers` array. No JS change needed.
The `name` must be unique. The `group` must match an entry in the `groups` array.

### Adding a style
Edit `public/config/origo.json` → `styles` object. Reference it with `"style": "style_name"` on a vector layer.

### Debugging
Open the browser console (F12). `window.viewer` exposes the Origo viewer.
`window.viewer.getMap()` returns the raw OpenLayers map object.

### CORS in development
External WMS services (Naturvårdsverket, Skogsstyrelsen) are fetched directly by the browser — they must support CORS. Most Swedish government WMS services do.
For localhost GeoServer/QGIS Server, the Vite proxy in vite.config.js handles it.

### Switching to EPSG:3006 (SWEREF99 TM)
1. `npm install proj4`
2. In src/main.js: register proj4 definition before calling Origo()
3. In origo.json: update map.projection, map.center (to SWEREF99 coords), map.resolutions
4. Switch background layer to Lantmäteriet WMTS

---

## File to edit most often

`public/config/origo.json` — the entire map is driven by this file.

---

## Commands

```powershell
npm run dev      # start dev server at localhost:3000
npm run build    # production build → dist/
npm run preview  # preview production build
```

---

## WMS services used (verify layer names via GetCapabilities)

| Service | GetCapabilities URL |
|---|---|
| Naturvårdsverket | https://geodata.naturvardsverket.se/naturvardsverket/ows?SERVICE=WMS&REQUEST=GetCapabilities |
| Skogsstyrelsen | https://geodata.skogsstyrelsen.se/arcgis/services/Skogliga_grunddata/MapServer/WmsServer?REQUEST=GetCapabilities |
| SGU | https://resource.sgu.se/service/wms/130/jordarter-25?REQUEST=GetCapabilities |

---

## Useful references

- Origo Map GitHub: https://github.com/origo-map/origo
- Origo documentation: https://github.com/origo-map/origo/wiki
- OpenLayers API: https://openlayers.org/en/latest/apidoc/
- Naturvårdsverket öppna data: https://www.naturvardsverket.se/om-oss/oppna-data-och-apier/
- Lantmäteriet öppna geodataprodukter: https://www.lantmateriet.se/sv/geodata/vara-produkter/
- SWEREF99 proj4 definition: +proj=utm +zone=33 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs
