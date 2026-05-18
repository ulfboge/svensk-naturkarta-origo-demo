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

## Current state (Phase 2 — COMPLETE ✅)

### Phase 1 ✅
- [x] Origo v2.10 bundle deployed at `public/js/`, `public/css/`, `public/img/`
- [x] `public/index.html` correctly mounts Origo
- [x] Git repository initialised
- [x] OSM basemap renders; Origo UI controls all present; zero console errors

### Phase 2 ✅
- [x] **GeoJSON layers** — `naturreservat-stockholm.geojson` + `nationalparker-stockholm.geojson` (Stockholms län, real NV data)
  - Attributes verified: NAMN, SKYDDSTYP, IUCNKAT, AREA_HA, URSBESLDAT, LAN, KOMMUN, FORVALTARE — all match
  - Styles: green polygon (naturreservat), brown polygon (nationalpark)
- [x] **Natura 2000 WMS** — SCI (Habitatdirektivet) + SPA (Fågeldirektivet) from `https://geodata.naturvardsverket.se/n2000/wms`
  - Layer IDs: `N2000_SCI`, `N2000_SPA`
- [x] **Naturvårdsregistret WMS** — Biotopskyddsområden + Djur- och växtskyddsområden from `https://geodata.naturvardsverket.se/naturvardsregistret/wms`
  - Layer IDs: `Ovrigt_biotopskyddsomrade`, `Djur_och_vaxtskyddsomrade`
- [x] **Skogsstyrelsen WMS** — Avverkningsanmälningar from ArcGIS MapServer, layer ID `0`
- [x] **5 layer groups** in sidebar (background, naturskydd, natura2000, nv_rikstackande, skog)
- [x] **GitHub Pages** — `.github/workflows/deploy.yml` already configured; `public/.nojekyll` added

### ⚠️ Layer names to verify in browser
The following WMS layer IDs were determined from GetCapabilities / educated guesses — toggle them on and check browser console/network tab:
- `N2000_SCI`, `N2000_SPA` (Natura 2000) — fetch `https://geodata.naturvardsverket.se/n2000/wms?SERVICE=WMS&REQUEST=GetCapabilities` if they fail
- `0` (Skogsstyrelsen avverkning) — standard ArcGIS MapServer first-layer ID, likely correct

---

## What to do next (Phase 3)

1. Open the live site on GitHub Pages and verify all WMS layers render correctly
2. Fix any layer IDs that fail (see ⚠️ above)
3. Consider adding Lantmäteriet Topowebb WMTS as a Swedish basemap alternative
4. Consider adding search/geocoding control (Origo has a `search` control for NV/SMHI APIs)
5. Polish the "Om kartan" about-text and add screenshots to README for portfolio

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
