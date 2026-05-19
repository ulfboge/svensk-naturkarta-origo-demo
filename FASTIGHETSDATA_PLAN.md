# Lantmäteriet fastighetsdata — implementationsplan

## Tillgänglig data

| Tjänst | Tillgång | Kräver |
|---|---|---|
| Fastighetsindelning WMS (fastighetsgränser) | API | LM API-nyckel (samma som Topowebb) |
| Fastighetsregistret (ägare, areal etc.) | REST API | LM API-nyckel + avtal |
| MinKarta (webbvisning) | Fri webblänk | Nej |

**Varför API-nyckel?** Lantmäteriet kräver registrering på opendata.lantmateriet.se för alla WMS/WMTS-tjänster. Fastighetsindelning CC BY använder samma nyckel som Topowebb.

---

## Steg 1 — WMS-lager: Fastighetsindelning [✅ KLAR]
- Lägg till ny källa `lm_fastighetsindelning` i `source`-blocket i origo.json
- WMS URL: `https://api.lantmateriet.se/open/fastighetsindelning-ccby/v1/wms/token/DIN_API_NYCKEL`
- Lägg till lager under grupp `background` (bakgrundsinfo) eller ny grupp
- Lagret är av som standard, kräver API-nyckel — märks i titel: "Fastighetsgränser (kräver API-nyckel)"
- Filer: `public/config/origo.json`

## Steg 2 — Popup: länk till MinKarta [✅ KLAR]
- Beräkna mittpunkt av klickat reservat (lastClickBbox centroid → WGS84)
- Lägg till rad i popup: "Visa fastighetsgränser ↗" → öppnar MinKarta på koordinaten
- MinKarta URL: `https://minkarta.lantmateriet.se/?lat={lat}&lon={lon}&zoom=14`
- Filer: `public/index.html`

## Steg 3 — Statistikpanel: Lantmäteriet-sektion [✅ KLAR]
- Ny sektion "Fastighetsdata (LM)" i stats-panelen
- Rad: "Fastighetsgränser — se karta" med länk till MinKarta för valt läns centrum
- Rad: länk till LM:s fastighetsinfo
- Filer: `public/index.html`

## Steg 4 — README och Om kartan [✅ KLAR]
- Nämn fastighetsindelning i lagertabell
- Uppdatera roadmap
- Nämn LM-integration i Om kartan

---

## Aktivering

Samma nyckel som Topowebb — ersätt `DIN_API_NYCKEL` i origo.json:
1. Registrera på opendata.lantmateriet.se
2. Skapa applikation
3. Ersätt alla `DIN_API_NYCKEL` med din nyckel
