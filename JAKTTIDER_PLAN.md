# Jakttider & jaktrestriktioner — implementationsplan

## Tillgänglig data

### Spatial (WMS — redan i befintlig NV-källa)
| Lager | Beskrivning |
|---|---|
| `Tilltradesforbud` | Områden med tillträdesförbud (inkl. jaktstoppzoner) |
| `Interimistiskt_forbud` | Interimistiska förbud (tidsbegränsade restriktioner) |

### Icke-spatial (länkdata)
- **NV Jakttider-sida**: `https://www.naturvardsverket.se/amnen/jakt-och-viltvard/jakttider/`
- **Per reservat**: `https://skyddadnatur.naturvardsverket.se/Geocache/?NVRID=XXXXX`
  (visas redan i popup via NVRID-länken — föreskrifter inkl. jaktregler finns här)

---

## Steg 1 — WMS-lager: Tilltradesforbud + Interimistiskt_forbud [✅ KLAR]
- Lägg till `Tilltradesforbud` i gruppen `nv_rikstackande`
- Lägg till `Interimistiskt_forbud` i gruppen `nv_rikstackande`
- Filerna: `public/config/origo.json`

## Steg 2 — Statistikpanel: Jakttider-sektion [✅ KLAR]
- Aktivera kommenterad sektion `<div id="stats-hunting">` i HTML
- Visa "Jakt i reservat" med länk till NV:s jakttider-sida
- Länktext: "Jakttider på NV ↗"
- Filer: `public/index.html`, `public/src/style.css`

## Steg 3 — README och Om kartan [✅ KLAR]
- Lägg till Tilltradesforbud i lagertabell i README
- Nämn jakttider i Om kartan
- Uppdatera roadmap: flytta jakttider till "Klart"
