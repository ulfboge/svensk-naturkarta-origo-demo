# download_swedish_geodata.ps1
# Kör från projektroten: svensk-naturkarta-origo-demo

$ErrorActionPreference = "Stop"

$root = Get-Location
$dataRaw = Join-Path $root "data\raw"
$dataProcessed = Join-Path $root "data\processed"
$adminDir = Join-Path $dataRaw "scb_admin"
$scbDir = Join-Path $dataRaw "scb_geodata"
$lmDir = Join-Path $dataRaw "lantmateriet_geotorget_manual"

New-Item -ItemType Directory -Force -Path $adminDir, $scbDir, $lmDir, $dataProcessed | Out-Null

function Download-File {
    param(
        [string]$Url,
        [string]$OutFile
    )

    Write-Host "Downloading: $OutFile"
    Invoke-WebRequest -Uri $Url -OutFile $OutFile
}

# -----------------------------
# SCB: län, kommuner, LA-regioner
# SWEREF99 TM, shapefile zip
# Källa: SCB Digitala gränser
# -----------------------------
Download-File `
  -Url "https://www.scb.se/contentassets/3443fea3fa6640f7a57ea15d9a372d33/shape_svenska_260225.zip" `
  -OutFile (Join-Path $adminDir "scb_lan_kommun_la_shape_260225.zip")

# -----------------------------
# SCB: RegSO 2025 GeoPackage
# -----------------------------
Download-File `
  -Url "https://geodata.scb.se/geoserver/stat/wfs?REQUEST=GetFeature&TYPENAMES=stat%3ARegSO_2025&outputFormat=geopackage&service=WFS&version=1.1.0" `
  -OutFile (Join-Path $scbDir "scb_regso_2025.gpkg")

# -----------------------------
# SCB: Tätorter 2023 GeoPackage
# -----------------------------
Download-File `
  -Url "https://geodata.scb.se/geoserver/stat/wfs?REQUEST=GetFeature&TYPENAMES=stat%3ATatorter_2023&outputFormat=geopackage&service=WFS&version=1.1.0" `
  -OutFile (Join-Path $scbDir "scb_tatorter_2023.gpkg")

# -----------------------------
# Packa upp SCB shapefile-zip
# -----------------------------
$zip = Join-Path $adminDir "scb_lan_kommun_la_shape_260225.zip"
$extractDir = Join-Path $adminDir "scb_lan_kommun_la_shape_260225"

if (Test-Path $extractDir) {
    Remove-Item $extractDir -Recurse -Force
}

Expand-Archive -Path $zip -DestinationPath $extractDir -Force

# -----------------------------
# Lantmäteriet: manuell leveransplats
# -----------------------------
$readme = @"
# Lantmäteriet data

Lägg nedladdade filer från Geotorget här.

Rekommenderade produkter för naturportal.qgz:

1. Kommun, län och rike Nedladdning
   - Bättre för exakta administrativa gränser än SCB:s förenklade tematiska gränser.
   - Produkt via Geotorget.

2. Topografi 50 Nedladdning, vektor
   - Levereras som GeoPackage-filer.
   - Bra för bakgrundsdata: vägar, mark, hydrografi, byggnader m.m.

3. Eventuellt Topografi 10 om du vill ha mer detaljerat underlag.

När filerna är nedladdade:
- lägg .gpkg-filerna i denna mapp
- öppna dem i QGIS
- spara relevanta lager till qgis/gpkg/naturportal.gpkg
"@

Set-Content -Path (Join-Path $lmDir "README_LANTMATERIET.md") -Value $readme -Encoding UTF8

Write-Host ""
Write-Host "Klart."
Write-Host "SCB-data finns i: $scbDir och $adminDir"
Write-Host "Lantmäteriet-filer läggs manuellt i: $lmDir"