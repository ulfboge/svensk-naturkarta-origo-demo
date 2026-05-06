# 04 — Tasks & Roadmap

Task log for the projekt. Add notes and dates as you complete items.

---

## Phase 1 — Project foundation ✅

**Goal:** A clean, documented, working skeleton that runs locally.

- [x] Create project folder structure
- [x] Write README.md
- [x] Write CLAUDE.md
- [x] Write docs/01_project_goal.md
- [x] Write docs/02_data_sources.md
- [x] Write docs/03_architecture.md
- [x] Write docs/04_tasks.md (this file)
- [x] Write package.json (origo-map + vite)
- [x] Write vite.config.js
- [x] Write index.html
- [x] Write src/main.js
- [x] Write src/style.css (green/nature theme)
- [x] Write public/config/origo.json (OSM background + NV WMS placeholders + GeoJSON)
- [x] Write public/data/sample-skyddade.geojson
- [x] Initialise Git repository, first commit

**Verify Phase 1:**
```powershell
cd C:\Users\galag\GitHub\svensk-naturkarta-origo-demo
npm install
npm run dev
# → map loads at localhost:3000
# → OSM tiles visible
# → sample GeoJSON points visible
# → layer switcher, coordinates, scale bar working
```

---

## Phase 2 — Real Swedish geodata layers

**Goal:** All major nature conservation WMS layers loaded and working with popups.

### 2.1 Verify WMS services
- [ ] Paste GetCapabilities URL for Naturvårdsverket into browser/QGIS
- [ ] Note the exact layer names from the XML response
- [ ] Paste GetCapabilities URL for Skogsstyrelsen, note layer names
- [ ] Test each WMS in QGIS to confirm it renders correctly

### 2.2 Naturvårdsverket layers
- [ ] Naturreservat — add to origo.json, verify popup attributes
- [ ] Nationalparker — add to origo.json
- [ ] Natura 2000 (habitatdirektivet) — add
- [ ] Natura 2000 (fågeldirektivet) — add
- [ ] Biotopskyddsområden — add
- [ ] Strandskydd — add (lower priority)

### 2.3 Skogsstyrelsen layers
- [ ] Avverkningsanmälningar — add to origo.json
- [ ] Nyckelbiotoper — add
- [ ] Skogliga grunddata (if performance allows) — add

### 2.4 Popup configuration
- [ ] For each WMS layer: run GetFeatureInfo manually to see attribute names
- [ ] Update `attributes` array in each layer config (Swedish labels)
- [ ] Confirm popup appears on click for each layer

### 2.5 Layer organisation
- [ ] Create logical groups: "Naturskydd", "Skog", "Bakgrundskartor"
- [ ] Set sensible default visibility (most layers off by default)
- [ ] Set sensible opacity for each layer

---

## Phase 3 — UI polish

**Goal:** Looks and feels like a real Swedish GIS portal.

### 3.1 Visual theme
- [ ] Green colour palette (nature/forest theme) in src/style.css
- [ ] Custom map title / header bar
- [ ] Origo control panel styled to match theme
- [ ] Loading screen matches theme

### 3.2 Swedish language
- [ ] All group titles in Swedish
- [ ] All layer titles in Swedish
- [ ] Popup attribute labels in Swedish
- [ ] Control tooltips in Swedish (check if Origo supports i18n)

### 3.3 Search
- [ ] Enable Origo `search` control
- [ ] Connect to Lantmäteriet ortnamn API (no key needed)
- [ ] Test: search "Abisko" → map zooms to Abisko nationalpark
- [ ] Test: search "Tyresta" → zooms to Tyresta nationalpark

### 3.4 Print / export
- [ ] Verify Origo `print` control works
- [ ] Test export to PDF / PNG

### 3.5 Measure tool
- [ ] Verify length measurement in metres
- [ ] Verify area measurement in hectares (standard for nature conservation)
- [ ] Check that units are labelled in Swedish (m, km, ha)

### 3.6 Legend
- [ ] Add `legend` control
- [ ] Verify WMS layers show GetLegendGraphic images
- [ ] Verify vector layers show symbol in legend

---

## Phase 4 — SWEREF99 TM + Lantmäteriet

**Goal:** Use the Swedish national projection and official topographic background map.

- [ ] Register for free Lantmäteriet API key at lantmateriet.se
- [ ] Install proj4: `npm install proj4`
- [ ] Register EPSG:3006 in src/main.js
- [ ] Update map.projection to EPSG:3006 in origo.json
- [ ] Update map.center to SWEREF99 coordinates (e.g. Stockholms central station: [677200, 6580500])
- [ ] Update map.resolutions to match Lantmäteriet tile grid
- [ ] Add Lantmäteriet topografisk webbkarta as WMTS background layer
- [ ] Add Lantmäteriet ortofoto as optional background
- [ ] Remove or demote OSM (keep as fallback)
- [ ] Verify all existing WMS layers still work in the new projection
- [ ] Update coordinate display to show SWEREF99 TM (EPSG:3006)

---

## Phase 5 — Local data (future)

**Goal:** Add PostGIS + GeoServer for locally hosted municipal data.

> **Not started. Do not begin until Phase 4 is complete.**

- [ ] Set up PostgreSQL + PostGIS locally
- [ ] Import a sample shapefile (e.g. kommunens naturreservat) into PostGIS
- [ ] Install GeoServer locally
- [ ] Publish PostGIS table as WMS + WFS in GeoServer
- [ ] Add the layer to origo.json (using Vite proxy)
- [ ] Write docs/05_geoserver_setup.md
- [ ] Add Docker Compose for PostgreSQL + GeoServer

---

## Icebox (ideas for later)

- [ ] Add SGU jordartskarta as a context layer
- [ ] Add SMHI hydrology layer (sjöar, vattendrag)
- [ ] Add Riksantikvarieämbetet fornlämningar (cultural heritage)
- [ ] Add time-slider for Skogsstyrelsen avverkningsanmälningar
- [ ] Investigate Origo plugins (draw, edit, analyse)
- [ ] Deploy as static site to GitHub Pages or Netlify
- [ ] Write a blog post about the project (portfolio content)

---

## Commit message conventions

Follow the [Conventional Commits](https://www.conventionalcommits.org/) format:

```
feat: add Naturvårdsverket naturreservat WMS layer
fix: correct layer name for Skogsstyrelsen avverkningar
docs: add GetCapabilities notes to 02_data_sources.md
style: apply green theme to loading screen
config: switch map projection to EPSG:3006
```

This makes the Git history readable and shows professional development habits.
