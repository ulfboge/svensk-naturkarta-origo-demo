# Höjddata — Markhöjdmodell NH

## Status: ✅ Visningslager klart (2026-05-22)

## Implementerat

Två WMS-lager från Lantmäteriets **Markhöjdmodell Visning** (Nationella höjdmodellen, NH):

| Lager i origo.json | WMS LAYERS | Beskrivning |
|---|---|---|
| `lm_terrangskuggning` | `terrangskuggning` | Hillshade — bra som overlay på OSM/Topowebb |
| `lm_terranglutning` | `terranglutning` | Lutningskarta, gråton |

- **Grupp:** `Terräng & höjd` i lagerpanelen
- **Källa:** `https://minkarta.lantmateriet.se/map/hojdmodell/` (ingen API-nyckel krävs för visning)
- **Projektion:** EPSG:3857 (Web Mercator, samma som kartan)
- **Standard:** dolda — aktivera i lagerpanelen ovanpå valfri bakgrundskarta

### Test

1. Starta kartan, välj t.ex. Gävleborgs län
2. Slå på **Terrängskuggning (Markhöjdmodell NH)** under *Terräng & höjd*
3. Terrängrelief ska synas under naturreservaten

## Alternativ (kräver LM-konto)

| Produkt | Åtkomst | Användning |
|---|---|---|
| Markhöjdmodell Visning (auth) | `https://maps.lantmateriet.se/hojdmodell/wms/v1.1` | WMS med Basic Auth / OAuth2 |
| Markhöjdmodell Nedladdning | STAC API `https://api.lantmateriet.se/stac-hojd/v1/` | Grid 1 m — nedladdning, ej kartlager |

Registrera konto på [opendata.lantmateriet.se](https://opendata.lantmateriet.se/) och prenumerera i [API Portal](https://apimanager.lantmateriet.se/).

## Framtida förbättringar

- [ ] Höjdprofil i popup (punktquery mot NH grid via STAC/backend)
- [ ] Byt till autentiserad WMS om MinKarta-tjänsten ändras
- [ ] SWEREF99 TM-visning (fas 4)

## Referenser

- [Markhöjdmodell Visning](https://www.lantmateriet.se/sv/geodata/vara-produkter/produktlista/markhojdmodell-visning/)
- [Markhöjdmodell Nedladdning / STAC-hojd](https://www.lantmateriet.se/sv/geodata/vara-produkter/produktlista/markhojdmodell-nedladdning/)
- WMS GetCapabilities: `https://minkarta.lantmateriet.se/map/hojdmodell/?SERVICE=WMS&REQUEST=GetCapabilities&VERSION=1.1.1`
