# svensk-naturkarta-origo-demo

> **Portfolio project** — A minimal Swedish web GIS viewer focused on nature conservation and forestry, built with [Origo Map](https://github.com/origo-map/origo) and [OpenLayers](https://openlayers.org/).

---

## What this project demonstrates

This application mimics a realistic **municipal or regional GIS portal** of the kind used by Swedish county administrative boards (_länsstyrelser_), municipalities, and forestry authorities. The focus area is nature conservation — showing protected areas, Natura 2000 sites, and forest data on top of a Swedish topographic base map.

**Portfolio value:**
- Configuration-driven web GIS (the way Swedish municipalities actually build these)
- Integration with Swedish open geodata services (Naturvårdsverket, Skogsstyrelsen, Lantmäteriet)
- OGC-standard WMS/WFS consumption
- Modern frontend toolchain (Vite + ES modules)
- Clean, documented, Git-tracked project structure

---

## Tech stack

| Layer | Technology |
|---|---|
| Map framework | [Origo Map](https://github.com/origo-map/origo) |
| Rendering engine | OpenLayers (via Origo) |
| Build / dev server | [Vite](https://vitejs.dev/) |
| Language | JavaScript (ES modules) |
| Styling | CSS (custom, on top of Origo's own CSS) |
| Data | Swedish open WMS/WFS services + local GeoJSON |
| Projection | EPSG:3857 (dev) → EPSG:3006 SWEREF99 TM (production) |
| Version control | Git |

---

## Data sources

All data used in this project is **open / freely accessible**:

| Source | What | URL |
|---|---|---|
| Naturvårdsverket | Naturreservat, Nationalparker, Natura 2000 | https://geodata.naturvardsverket.se |
| Skogsstyrelsen | Avverkningsanmälningar, skogliga grunddata | https://geodata.skogsstyrelsen.se |
| Lantmäteriet | Topografisk webbkarta (free API key) | https://www.lantmateriet.se |
| OpenStreetMap | Background tiles (no key needed) | https://tile.openstreetmap.org |

See [`docs/02_data_sources.md`](docs/02_data_sources.md) for full details, GetCapabilities URLs, and licence information.

---

## Project structure

```
svensk-naturkarta-origo-demo/
├── README.md                    ← this file
├── CLAUDE.md                    ← AI assistant context
├── .gitignore
│
├── docs/
│   ├── 01_project_goal.md       ← vision and scope
│   ├── 02_data_sources.md       ← Swedish geodata services + licences
│   ├── 03_architecture.md       ← technical design
│   └── 04_tasks.md              ← roadmap / task log
│
├── index.html                   ← HTML shell (Origo mounts here)
├── package.json                 ← npm deps + scripts
├── vite.config.js               ← dev server + CORS proxy
│
├── src/
│   ├── main.js                  ← imports Origo, fetches config, starts viewer
│   └── style.css                ← layout + nature-themed overrides
│
└── public/
    ├── config/
    │   └── origo.json           ← THE map config (layers, controls, styles)
    └── data/
        └── sample-skyddade.geojson  ← local sample features
```

The **single most important file** is `public/config/origo.json`. Adding a new layer, changing a style, or toggling a control requires only editing that JSON — no JavaScript needed.

---

## Installation (Windows / PowerShell)

### Prerequisites

| Tool | Version | Check |
|---|---|---|
| Node.js | 18 or higher | `node --version` |
| npm | bundled with Node | `npm --version` |
| Git | any | `git --version` |
| VS Code | recommended | — |

Download Node.js from [nodejs.org](https://nodejs.org/en/download) — choose the **LTS** installer.

### Step 1 — Clone or open the project

```powershell
# If you haven't already:
cd C:\Users\galag\GitHub
git clone <your-repo-url> svensk-naturkarta-origo-demo
cd svensk-naturkarta-origo-demo

# Or if you already have the folder:
cd C:\Users\galag\GitHub\svensk-naturkarta-origo-demo
```

### Step 2 — Install dependencies

```powershell
npm install
```

This downloads `origo-map` (which bundles OpenLayers) and `vite` into `node_modules/`. Expect ~200 MB — this is normal. `node_modules/` is excluded from Git via `.gitignore`.

If you see peer-dependency warnings:

```powershell
npm install --legacy-peer-deps
```

### Step 3 — Start the development server

```powershell
npm run dev
```

Vite starts at **http://localhost:3000** and opens a browser tab automatically. The map loads with:
- OpenStreetMap tiles as background
- Naturvårdsverket nature reserve boundaries (WMS — requires internet)
- Sample local vector points (works offline)

**Hot reload:** Any change you save to `public/config/origo.json` or `src/style.css` instantly refreshes the browser.

### Step 4 — Build for production

```powershell
npm run build
```

Output goes to `dist/`. To preview the production build locally:

```powershell
npm run preview
```

---

## Adding a WMS layer (quick reference)

Open `public/config/origo.json` and add to the `layers` array:

```json
{
  "name": "my_new_layer",
  "title": "Mitt nya lager",
  "group": "naturskydd",
  "type": "WMS",
  "url": "https://geodata.naturvardsverket.se/naturvardsverket/ows",
  "params": {
    "LAYERS": "NV.Naturreservat",
    "FORMAT": "image/png",
    "TRANSPARENT": true,
    "VERSION": "1.3.0"
  },
  "visible": true,
  "queryable": true
}
```

Then add `"naturskydd"` to the `groups` array if it doesn't exist yet. Save — done.

---

## Connecting to external WMS — verifying layer names

Before adding a WMS layer, always check what layers the service actually exposes:

```
https://geodata.naturvardsverket.se/naturvardsverket/ows?SERVICE=WMS&REQUEST=GetCapabilities
```

Open the URL in a browser or paste it into QGIS → *Layer* → *Add WMS/WMTS layer* → *Connect*. QGIS will list all available layers with their exact names.

---

## Roadmap

See [`docs/04_tasks.md`](docs/04_tasks.md) for the full task list. Planned phases:

- **Phase 1** ✅ Project structure + documentation + minimal working map
- **Phase 2** — Real Swedish WMS layers (Naturvårdsverket, Skogsstyrelsen)
- **Phase 3** — UI polish (green theme, Swedish labels, legend)
- **Phase 4** — SWEREF99 TM projection + Lantmäteriet background
- **Phase 5** — (Future) Local PostGIS data + GeoServer/QGIS Server

---

## Licence

Code: [MIT](LICENSE)
Geodata: see [`docs/02_data_sources.md`](docs/02_data_sources.md) for individual service licences.
