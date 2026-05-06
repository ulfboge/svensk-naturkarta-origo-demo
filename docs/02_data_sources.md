# 02 — Data Sources

All data sources used in this project are **publicly accessible** Swedish open geodata services. No API keys are required for the WMS services listed here, unless noted otherwise.

---

## 1. Naturvårdsverket (Swedish Environmental Protection Agency)

**Website:** https://www.naturvardsverket.se/om-oss/oppna-data-och-apier/

**WMS endpoint:**
```
https://geodata.naturvardsverket.se/naturvardsverket/ows
```

**GetCapabilities (paste into QGIS or browser to see all layers):**
```
https://geodata.naturvardsverket.se/naturvardsverket/ows?SERVICE=WMS&REQUEST=GetCapabilities&VERSION=1.3.0
```

**Key layers (verify exact names via GetCapabilities):**

| Layer name (approximate) | Description |
|---|---|
| `NV.Naturreservat` | Nature reserves — polygons |
| `NV.Nationalpark` | National parks |
| `NV.Natura2000` | EU Natura 2000 network — habitats + birds directives |
| `NV.Biotopskyddsomrade` | Biotope protection areas |
| `NV.Naturminne` | Natural monuments |
| `NV.Strandskydd` | Shore protection zones |
| `NV.Djurskyddsomrade` | Wildlife protection areas |

**WFS endpoint (for editable vector features):**
```
https://geodata.naturvardsverket.se/naturvardsverket/ows?SERVICE=WFS&REQUEST=GetCapabilities
```

**Licence:** Creative Commons CC0 (public domain) — free to use, no attribution required, but attribution is good practice.

**How to use in QGIS:**
1. Layer → Add Layer → Add WMS/WMTS Layer
2. Click New, paste the WMS URL
3. Click Connect → browse and add layers

---

## 2. Skogsstyrelsen (Swedish Forest Agency)

**Website:** https://www.skogsstyrelsen.se/skogsbruk/kartor-och-geodata/

**WMS — Skogliga grunddata:**
```
https://geodata.skogsstyrelsen.se/arcgis/services/Skogliga_grunddata/MapServer/WmsServer
```

**GetCapabilities:**
```
https://geodata.skogsstyrelsen.se/arcgis/services/Skogliga_grunddata/MapServer/WmsServer?REQUEST=GetCapabilities&SERVICE=WMS
```

**WMS — Avverkningsanmälningar (logging notifications):**
```
https://geodata.skogsstyrelsen.se/arcgis/services/Avverkningsanmalningar/MapServer/WmsServer
```

**Key layers (verify via GetCapabilities):**

| Layer | Description |
|---|---|
| Skogliga grunddata | Forest base data (tree height, volume, age) |
| Avverkningsanmälningar | Notified logging operations |
| Biotopskyddsomraden | Forestry biotope protections |
| Nyckelbiotoper | Key woodland habitats |

**Licence:** Open data — free for reuse. Check the Skogsstyrelsen website for current terms; most data is covered by the PSI directive (public sector information).

**Note on ArcGIS Server:** Skogsstyrelsen uses Esri ArcGIS Server. WMS calls work normally with Origo, but WMTS or REST calls may use different URL patterns. Stick to WMS for now.

---

## 3. Lantmäteriet (Swedish Mapping Authority)

**Website:** https://www.lantmateriet.se/sv/geodata/vara-produkter/

**Background maps (requires free API key):**

| Service | Format | Notes |
|---|---|---|
| Topografisk webbkarta | WMTS | Most common Swedish background map |
| Ortofoto | WMTS | Aerial imagery |
| Terrängkartan | WMTS | Detailed terrain map |

**How to get a free API key:**
1. Go to https://www.lantmateriet.se/geodatatjanster
2. Register a free account (privatperson or organisation)
3. Create an application — note the token
4. Use the token in the WMTS URL

**WMTS URL pattern (with token):**
```
https://api.lantmateriet.se/open/topowebb/v1/wmts?token=YOUR_TOKEN_HERE
```

**Open data downloads (no key needed):**
```
https://www.lantmateriet.se/sv/geodata/vara-produkter/produktlista/gsd-vagkartan/
```
GSD-Vägkartan and GSD-Terrängkartan are available for free download as shapefiles.

**Licence:** Lantmäteriet open data licence (allows reuse with attribution). See https://www.lantmateriet.se/sv/geodata/oppna-data/

**Place-name search API (ortnamn — no key needed for basic use):**
```
https://api.lantmateriet.se/distribution/produkter/ortnamn/v2.1/ortnamn
```
Used by the Origo `search` control with `type: "ortnamn"`.

---

## 4. SGU (Geological Survey of Sweden)

**Website:** https://www.sgu.se/en/products-and-services/gis-and-geodata/

**WMS endpoint:**
```
https://resource.sgu.se/service/wms/130/jordarter-25
```

**GetCapabilities:**
```
https://resource.sgu.se/service/wms/130/jordarter-25?SERVICE=WMS&REQUEST=GetCapabilities
```

**Useful layers:**
- Soil type map (jordartskarta) — useful context for nature conservation
- Groundwater (grundvatten)
- Bedrock (berggrund)

**Licence:** CC0 — public domain.

---

## 5. SMHI (Swedish Meteorological and Hydrological Institute)

**Website:** https://www.smhi.se/data/oppna-data

**WMS — Hydrologi:**
```
https://opendata-view.smhi.se/klim/klim_stationsnattverket/wms
```

**Open data portal:**
```
https://opendata.smhi.se/apidocs/
```

Useful for adding precipitation or flood-risk context layers.

**Licence:** CC BY (attribution required).

---

## 6. OpenStreetMap

**Tile URL (no key needed):**
```
https://tile.openstreetmap.org/{z}/{x}/{y}.png
```

Used as the default background in development. No API key required.

**Licence:** Open Database Licence (ODbL) — attribution required:
> © OpenStreetMap contributors

**Note:** OSM tiles should not be used for high-traffic production applications without caching. For production, use Lantmäteriet WMTS instead.

---

## How to verify a WMS service before adding it to origo.json

### Method 1 — Browser
Paste the GetCapabilities URL into your browser. Look for `<Layer>` elements — the `<Name>` tag inside each is what you put in `params.LAYERS`.

### Method 2 — QGIS (recommended)
1. Layer → Add Layer → Add WMS/WMTS Layer
2. New → paste URL → Connect
3. Browse the layer tree — QGIS shows titles + names
4. Add a layer to your QGIS canvas to verify it renders correctly before adding to Origo

### Method 3 — curl (PowerShell)
```powershell
Invoke-WebRequest `
  "https://geodata.naturvardsverket.se/naturvardsverket/ows?SERVICE=WMS&REQUEST=GetCapabilities" `
  -OutFile capabilities.xml
code capabilities.xml
```

---

## Summary table

| Source | Needs key | Licence | Type | Use case |
|---|---|---|---|---|
| Naturvårdsverket | No | CC0 | WMS/WFS | Protected areas, Natura 2000 |
| Skogsstyrelsen | No | Open PSI | WMS | Forest data, logging |
| Lantmäteriet background | Yes (free) | LM open | WMTS | Base map |
| Lantmäteriet ortnamn | No | LM open | REST | Place-name search |
| SGU | No | CC0 | WMS | Soil, geology |
| SMHI | No | CC BY | WMS | Hydrology |
| OpenStreetMap | No | ODbL | XYZ tiles | Dev background |
