# Artdatabanken-integration — implementationsplan

## API-val: GBIF Occurrence API
- Gratis, ingen API-nyckel
- Innehåller all svensk Artportalen-data (flödar in från Artdatabanken)
- Stöd för bounding box-filter och WKT-geometri

**Endpoint som används:**
```
GET https://api.gbif.org/v1/occurrence/search
  ?country=SE
  &decimalLatitude=MIN_LAT,MAX_LAT
  &decimalLongitude=MIN_LON,MAX_LON
  &year=2020,2025
  &limit=0
```
Svar: `{ "count": 1234, ... }` — ingen data behöver parsas, bara räknevärdet.

---

## Steg 1 — API-test [✅ KLAR]
- [ ] Testa GBIF-endpointen i webbläsaren med bbox för ett känt reservat
  - Exempelkoordinater: Tyresta (lat 59.18,59.23, lon 18.19,18.30)
  - Verifiera att `count` returneras korrekt
- [ ] Bekräfta svarstider (bör vara < 1–2 sek)
- [ ] Bekräfta att `year`-filter fungerar (senaste 5 åren)

---

## Steg 2 — Popup: artobservationer per reservat [✅ KLAR]
Triggas när användaren klickar på ett naturreservat.

**Teknisk approach:**
- Utöka den befintliga MutationObserver (som redan formaterar areal och datum)
- När ett nytt `.o-identify-content`-element läggs till i DOM:en:
  1. Hitta feature-namn från popup-titeln
  2. Slå upp feature i `searchIndex` → hämta geometrins bbox
  3. Räkna om bbox från EPSG:3857 → WGS84
  4. Lägg till `<li id="art-count">Artobservationer: laddar...</li>` i popup:en
  5. Anropa GBIF async → uppdatera `<li>` med count + länk till Artportalen

**HTML-utdata:**
```html
<li><b>Artobservationer</b>: 342 st (2020–2025)
  <a href="https://www.artportalen.se/..." target="_blank">→ Artportalen</a>
</li>
```

**Filer att ändra:**
- `public/index.html` — utöka MutationObserver + lägg till GBIF fetch-funktion

---

## Steg 3 — Statistikpanel: observationer per län [✅ KLAR]
Triggas när användare byter länval.

**Teknisk approach:**
- Aktivera den kommenterade `<div class="stats-section" id="stats-species">` i HTML:en
- Lägg till en rad i stats-sektionen: `Artobservationer | [count] st`
- COUNTY_BBOX-konstant i JS med WGS84-bbox per län
- Vid `selectCounty`: anropa GBIF med länets bbox → uppdatera stats-panel

**COUNTY_BBOX (WGS84 [minLat, maxLat, minLon, maxLon]):**
```javascript
var COUNTY_BBOX = {
    sthlm: [58.85, 60.22, 17.25, 19.80],
    sod:   [58.70, 59.60, 15.40, 18.00],
    upp:   [59.45, 60.80, 15.70, 19.10],
    ost:   [57.50, 59.00, 14.40, 16.90],
    vg:    [57.05, 60.00, 11.00, 14.90],
    skane: [55.25, 56.50, 12.40, 14.50],
    all:   [55.25, 60.80, 11.00, 19.80]
};
```

**Filer att ändra:**
- `public/index.html` — lägg till COUNTY_BBOX, uppdatera `updateStats`, utöka HTML

---

## Steg 4 — Loading-state och felhantering [✅ KLAR]
- Visa "laddar..." medan GBIF svarar
- Om GBIF returnerar fel (nätverk, timeout) → visa "—" utan att krascha
- CORS bör fungera (GBIF har öppna CORS-headers), men verifiera

---

## Steg 5 — Länk till Artportalen-sökning [ ]
Artportalen har djuplänkar:
```
https://www.artportalen.se/ViewSighting/SearchSighting
  ?searchArea=...
```
Lägg till direktlänk i popup och stats-panel.

---

## Steg 6 — README och Om kartan [ ]
- Uppdatera "Funktioner"-listan i Om kartan
- Uppdatera README roadmap (flytta Artdatabanken till "Klart")
- Ny screenshot av popup med artobservationer

---

## Prioritetsordning om tid är begränsad

**Minimalt men imponerande:**
Steg 1 + Steg 2 (popup) räcker — en livefråga mot GBIF i popup:en visar live API-integration tydligt.

**Komplett:**
Alla 6 steg — full integration i både popup och statistikpanel.
