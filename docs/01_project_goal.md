# 01 — Project Goal

## Vision

Build a **minimal but realistic Swedish nature-conservation GIS viewer** that could plausibly be deployed as an internal portal by a Swedish municipality, county administrative board (_länsstyrelse_), or the Swedish Forest Agency (_Skogsstyrelsen_).

The application should feel like something a Swedish GIS engineer has actually built for operational use — not a tutorial toy.

---

## Problem it solves

Swedish municipalities and regional authorities regularly need to give planners, ecologists, and forestry inspectors a simple map view of:

- Which areas are legally protected (naturreservat, nationalparker, Natura 2000)
- Where active or planned logging operations are notified
- What habitats or species are present in a given area
- How proposed development projects intersect conservation obligations

Today many such portals are built on Origo Map, because it is open-source, maintained by the Swedish municipality community, and requires only a JSON configuration file to set up new layers.

---

## Target persona

| Attribute | Description |
|---|---|
| Primary user | GIS coordinator / naturvårdsinspektör at a länsstyrelse or large municipality |
| Technical level | Comfortable with maps; not a developer |
| Device | Desktop browser (Chrome/Edge on Windows) |
| Language | Swedish |
| Expectation | Fast, clean, reliable — similar to the Länsstyrelsen GIS portal or Naturvårdsverkets Skyddad Natur viewer |

---

## Features in scope (Phase 1–3)

| Feature | Status |
|---|---|
| OSM background map | ✅ Phase 1 |
| Lantmäteriet topographic background | Phase 4 (needs free API key) |
| Naturvårdsverket naturreservat (WMS) | Phase 2 |
| Naturvårdsverket nationalparker (WMS) | Phase 2 |
| Naturvårdsverket Natura 2000 (WMS) | Phase 2 |
| Skogsstyrelsen avverkningsanmälningar (WMS) | Phase 2 |
| Click-popup with attributes (Swedish labels) | Phase 2 |
| Layer switcher (grouped) | ✅ Phase 1 |
| Coordinate display | ✅ Phase 1 |
| Scale bar | ✅ Phase 1 |
| Search (Lantmäteriet ortnamn / place names) | Phase 3 |
| Measure tool | ✅ Phase 1 |
| Responsive layout | Phase 3 |
| Print / export | Phase 3 |
| SWEREF99 TM projection | Phase 4 |

## Features out of scope (for now)

- User authentication
- Editing / digitising
- PostGIS / local database backend
- Docker
- Mobile-first design
- 3D terrain

---

## Portfolio objectives

This project demonstrates:

1. **Understanding of Swedish web GIS ecosystem** — Origo Map, Lantmäteriet, Naturvårdsverket, OGC standards
2. **Ability to consume WMS/WFS services** — the fundamental skill for any Swedish GIS web developer
3. **Configuration-over-code discipline** — mirrors how real Swedish municipalities work
4. **Modern frontend toolchain** — Vite, ES modules, npm, Git
5. **Documentation quality** — CLAUDE.md, docs/, README: skills that matter in professional settings
6. **Projection awareness** — EPSG:3857 vs EPSG:3006, a core Swedish GIS topic

---

## Definition of done (Phase 1)

- [ ] `npm install && npm run dev` loads a working map in the browser
- [ ] OSM tiles visible as background
- [ ] At least one WMS layer from Naturvårdsverket visible when toggled on
- [ ] Local GeoJSON layer visible with click-popup
- [ ] Layer switcher, coordinates, scale bar working
- [ ] README explains setup clearly for a developer unfamiliar with the project
- [ ] Git history started with a meaningful initial commit
