# 03 — Architecture

## Overview

This is a **pure frontend web GIS application**. There is no backend server, no database, and no server-side code. All data comes from external OGC-standard WMS/WFS services or local files.

```
┌─────────────────────────────────────────────────────────────┐
│  BROWSER                                                     │
│                                                              │
│   index.html                                                 │
│       │                                                      │
│   src/main.js  ──imports──► origo-map (npm)                 │
│       │                          │                          │
│       │                     OpenLayers                      │
│       │                          │                          │
│   public/config/origo.json       │ renders tiles, vectors   │
│   (configuration)                │ handles interactions     │
│                                  │                          │
│   public/data/*.geojson          │ local vector data        │
│                                                              │
│   Talks to the internet:                                     │
│     WMS GetMap  ────────► Naturvårdsverket, Skogsstyrelsen  │
│     WMS GetFeatureInfo ► (click-popup attribute queries)     │
│     WFS GetFeature ────► (optional vector downloads)        │
│     XYZ tiles ─────────► OpenStreetMap (background)         │
│     WMTS ──────────────► Lantmäteriet (Phase 4)             │
└─────────────────────────────────────────────────────────────┘
```

---

## Frontend layer-cake

```
┌────────────────────────────────────┐
│  origo.json  (configuration)       │  ← edit this to change the map
├────────────────────────────────────┤
│  Origo Map  (map framework)        │  ← handles UI: panels, popups, controls
├────────────────────────────────────┤
│  OpenLayers  (rendering engine)    │  ← draws tiles, vectors, handles projections
├────────────────────────────────────┤
│  Browser (Chrome / Edge)           │  ← runs everything
└────────────────────────────────────┘
```

**Origo sits between OpenLayers and your JSON config.** It reads the config and builds the OpenLayers map, layer list, controls, and popups automatically. You rarely need to write OpenLayers code directly.

---

## File responsibilities

| File | Role |
|---|---|
| `index.html` | HTML shell — one `<div id="app-wrapper">`. Everything else is injected by Origo. |
| `src/main.js` | JavaScript entry: imports CSS, fetches `origo.json`, calls `Origo(config)`. |
| `src/style.css` | Layout (full-page map), loading screen, green-theme overrides on Origo's CSS. |
| `public/config/origo.json` | **The map itself** — layers, groups, controls, styles, projections. |
| `public/data/*.geojson` | Local vector data (no server needed). |
| `vite.config.js` | Dev server settings + CORS proxy for localhost map services. |
| `package.json` | npm dependencies and scripts. |

---

## How Origo initialises

```
npm run dev
    ↓
Vite serves index.html
    ↓
Browser loads src/main.js (ES module)
    ↓
main.js fetches /config/origo.json
    ↓
Origo(config) is called:
    ├─ Reads map.projection, map.center, map.zoom
    ├─ Creates an OpenLayers map instance
    ├─ Loops through layers[] → creates OL Layer objects
    ├─ Loops through controls[] → creates UI components
    ├─ Renders everything into <div id="app-wrapper">
    └─ Map is live
```

---

## Data flow — WMS layer

```
User pans/zooms the map
    ↓
OpenLayers calculates visible extent + zoom level
    ↓
WMS GetMap request is fired:
  GET https://geodata.naturvardsverket.se/naturvardsverket/ows
      ?SERVICE=WMS
      &REQUEST=GetMap
      &LAYERS=NV.Naturreservat
      &BBOX=<extent>
      &WIDTH=256&HEIGHT=256
      &FORMAT=image/png
      &TRANSPARENT=TRUE
    ↓
Naturvårdsverket server renders and returns a PNG tile
    ↓
OpenLayers draws the PNG on the map canvas
```

WMS returns **images**, not features. For attributes (click-popup), a separate `GetFeatureInfo` request is made at the clicked coordinate.

---

## Data flow — WFS / vector layer

```
Layer loads (or user triggers)
    ↓
WFS GetFeature request:
  GET https://.../?SERVICE=WFS&REQUEST=GetFeature&TYPENAME=...
    ↓
Server returns GeoJSON (or GML)
    ↓
OpenLayers parses and renders as vector features
    ↓
User clicks a feature → popup shows attributes
    (no extra network request needed — data is already in memory)
```

WFS is better for: clicking, filtering, styling individual features, and editing.
WFS is worse for: large datasets (all data transferred to browser).

---

## Development workflow

```
Edit origo.json  ──► Vite hot-reloads ──► map updates in < 1 second
Edit src/style.css ──► Vite hot-reloads ──► styles update instantly
Edit src/main.js ──► Vite rebuilds module ──► page reloads
```

This tight feedback loop is why Vite is used: no manual refreshing, no compile step for the JSON config.

---

## CORS handling

**External WMS services** (Naturvårdsverket, Skogsstyrelsen) must support CORS headers on their servers. Almost all Swedish government WMS services do support CORS — browsers can fetch them directly.

**Local map services** (GeoServer, QGIS Server on localhost) do not require CORS because Vite's development proxy intercepts those requests before they leave the browser:

```
Browser requests /geoserver/wms
    ↓
Vite proxy (vite.config.js) forwards to http://localhost:8080/geoserver/wms
    ↓
GeoServer responds
    ↓
Vite forwards response back to browser
```

In production, NGINX is typically used as the reverse proxy instead.

---

## Projection strategy

| Phase | Projection | Reason |
|---|---|---|
| 1–3 (now) | EPSG:3857 (Web Mercator) | Works out of the box with OSM tiles; no extra setup |
| 4+ | EPSG:3006 (SWEREF99 TM) | Swedish national standard; required for Lantmäteriet WMTS |

Switching projection requires:
1. Install `proj4` npm package
2. Register EPSG:3006 definition in `src/main.js` before calling `Origo()`
3. Update `map.projection`, `map.center` (in SWEREF99 m), and `map.resolutions` in `origo.json`
4. Replace OSM background with Lantmäteriet WMTS

---

## Future architecture (Phase 5+)

When local data and editing are needed, the backend stack becomes:

```
Browser (Origo)
    ↕ WMS / WFS
GeoServer or QGIS Server
    ↕ SQL
PostgreSQL + PostGIS
```

This is the standard Swedish municipal GIS stack. GeoServer reads spatial data from PostGIS and exposes it as WMS/WFS — the frontend code does not change.

Docker will be introduced at this stage to manage GeoServer + PostGIS versions consistently.

---

## Key design decisions

| Decision | Rationale |
|---|---|
| Configuration-first (JSON) | Matches how Swedish municipalities actually build Origo portals |
| No backend for Phase 1–4 | Keeps the demo deployable as static files on any server |
| External WMS only (Phase 1–3) | Real data immediately; no data preparation needed |
| Vite over Webpack | Faster dev server; simpler config; native ES modules |
| EPSG:3857 first | Unblocks development before Lantmäteriet API key is obtained |
