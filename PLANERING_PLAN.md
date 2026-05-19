# Planerings- och dispensärenden — implementationsplan

## Tillgänglig data

| Källa | Tjänst | Status |
|---|---|---|
| NV Naturvårdsregistret WMS | `Beslutsstatus` | ✅ Fungerar (testat) |
| NV Naturvårdsregistret WMS | `Naturvardsomrade` | ✅ Fungerar (testat) |
| Boverket ArcGIS WMS | Riksintressen | ⚠️ Känd URL, kan ej testa från sandboxen |
| Boverket webb | Riksintressekarta (länk) | ✅ Gratis webblänk |
| Lantmäteriet | Detaljplaner | Kräver API-nyckel |

---

## Steg 1 — WMS-lager: NV planerings-/statuslager [✅ KLAR]
- Lägg till ny grupp `planering` ("Planering & skyddsstatus")
- Lägg till `Beslutsstatus` (NV) — visar status på skyddsbeslut
- Lägg till `Naturvardsomrade` (NV) — bredare skyddskategori
- Lägg till Boverket riksintressen WMS (med varningstetext att det kan kräva nätverksaccess)
- Filer: `public/config/origo.json`

## Steg 2 — Popup: planerings-länk [✅ KLAR]
- Lägg till länk till Boverket riksintressekarta i popup
- Länk till NV:s naturvårdsärenden per NVRID
- Filer: `public/index.html`

## Steg 3 — Statistikpanel: planeringsektion [✅ KLAR]
- Ny sektion "Planering" med länk till Boverkets riksintressekarta
- Länk till NV:s ärendehantering
- Filer: `public/index.html`

## Steg 4 — README och Om kartan [✅ KLAR]
- Uppdatera roadmap (flytta till klart)
- Uppdatera Om kartan med planerings-datakällor
