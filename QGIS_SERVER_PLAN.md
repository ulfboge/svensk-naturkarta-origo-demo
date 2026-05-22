# QGIS Server — live WFS (Phase 5 pilot)

Ersätter statisk GeoJSON med vektor via lokal QGIS Server. **Alla 21 län** (5 993 naturreservat) publiceras som WFS.

## Snabbstart

```powershell
# 1. Bygg GeoPackage + QGIS-projekt (vid dataändring)
python scripts/build_qgis_wfs_project.py

# 2. Starta QGIS Server (Docker Desktop måste köra)
docker compose up -d

# 3. Starta Origo med QGIS-proxy (port 3000)
python scripts/dev_server.py
```

Öppna http://localhost:3000 → välj län i dropdown. Med QGIS Server igång används **WFS live** automatiskt (GeoJSON-lager döljs).

## Verifiera WFS manuellt

```powershell
# GetCapabilities
curl "http://localhost:8081/?MAP=/etc/qgisserver/naturkarta.qgs&SERVICE=WFS&REQUEST=GetCapabilities"

# GetFeature (GeoJSON, 2 st)
curl "http://localhost:8081/?MAP=/etc/qgisserver/naturkarta.qgs&SERVICE=WFS&VERSION=1.1.0&REQUEST=GetFeature&TYPENAME=naturreservat_gavleborg&OUTPUTFORMAT=application/json&MAXFEATURES=2"
```

## Arkitektur

```
Browser (Origo, :3000)
    /qgis-server/*  →  scripts/dev_server.py proxy
                            ↓
                    QGIS Server (Docker, :8081)
                            ↓
              qgis/server/naturkarta.qgs
              qgis/server/data/naturkarta.gpkg
```

- **Origo-källa:** `local_qgis_wfs` i `public/config/origo.json` (`filterType: qgis`)
- **Origo-lager:** `nv_wfs_gavleborg` (`type: WFS`, `id: naturreservat_gavleborg`)
- **CORS:** `qgis/server/apache-cors.conf` (monteras i containern)

## Filer

| Fil | Syfte |
|---|---|
| `docker-compose.yml` | camptocamp/qgis-server:3.34 på port 8081 |
| `qgis/server/naturkarta.qgs` | QGIS-projekt med WFS publicerat |
| `qgis/server/data/naturkarta.gpkg` | Vektordata (EPSG:3857) |
| `scripts/build_qgis_wfs_project.py` | GeoJSON → GPKG + .qgs |
| `scripts/dev_server.py` | Static server + `/qgis-server`-proxy |

## Nästa steg

1. Fler län i `PILOT_LAYERS` (build-script) + motsvarande WFS-lager i Origo
2. Byt county selector till WFS per län (lazy bbox-strategy)
3. PostGIS + WFST för redigering (municipal stack)
4. GitHub Pages: WFS fungerar inte i prod (ingen backend) — behåll GeoJSON där

## Felsökning

| Problem | Lösning |
|---|---|
| `502` på `/qgis-server` | `docker compose up -d` |
| Tomt WFS-lager | Kontrollera att GeoJSON-lager är av — undvik dubbel rendering |
| Docker pipe error | Starta Docker Desktop |
| Vite istället för dev_server | `vite.config.js` proxar redan `/qgis-server` → `:8081` |
