# ─────────────────────────────────────────────────────────────────────────────
# scripts/download-origo.ps1
#
# Downloads the Origo Map pre-built bundle from GitHub and places it in
# public/origo/. Run this once after cloning the repository.
#
# Usage (from the project root):
#   PowerShell -ExecutionPolicy Bypass -File scripts\download-origo.ps1
#
# The public/origo/ folder is excluded from Git (.gitignore) because the
# files are large (8 MB JS bundle) and can be re-downloaded at any time.
# ─────────────────────────────────────────────────────────────────────────────

param(
    [string]$Version = "v2.10.0"
)

$ErrorActionPreference = "Stop"

$projectRoot = Split-Path $PSScriptRoot -Parent
$dest        = Join-Path $projectRoot "public\origo"
$zipUrl      = "https://api.github.com/repos/origo-map/origo/zipball/$Version"
$zipPath     = Join-Path $env:TEMP "origo-$Version.zip"
$extractPath = Join-Path $env:TEMP "origo-extract"

Write-Host ""
Write-Host "=== Origo Map Setup Script ===" -ForegroundColor Green
Write-Host "Version : $Version"
Write-Host "Target  : $dest"
Write-Host ""

# ── Download ─────────────────────────────────────────────────────────────────
if (Test-Path $zipPath) {
    Write-Host "Using cached download: $zipPath"
} else {
    Write-Host "Downloading Origo $Version from GitHub..." -NoNewline
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12
    $wc = New-Object System.Net.WebClient
    $wc.Headers.Add("User-Agent", "origo-download-script")
    $wc.DownloadFile($zipUrl, $zipPath)
    $sizeMB = [math]::Round((Get-Item $zipPath).Length / 1MB, 1)
    Write-Host " $sizeMB MB" -ForegroundColor Green
}

# ── Extract ───────────────────────────────────────────────────────────────────
Write-Host "Extracting..." -NoNewline
if (Test-Path $extractPath) { Remove-Item $extractPath -Recurse -Force }
Expand-Archive $zipPath -DestinationPath $extractPath -Force
Write-Host " done" -ForegroundColor Green

# ── Copy build/ → public/origo/ ──────────────────────────────────────────────
$topLevel = (Get-ChildItem $extractPath -Directory | Select-Object -First 1).FullName
$buildSrc = Join-Path $topLevel "build"

if (-not (Test-Path $buildSrc)) {
    Write-Error "build/ folder not found in the downloaded archive. Unexpected structure."
    exit 1
}

Write-Host "Copying bundle to $dest..." -NoNewline
if (Test-Path $dest) { Remove-Item $dest -Recurse -Force }
New-Item -ItemType Directory -Force -Path $dest | Out-Null
Copy-Item -Path "$buildSrc\*" -Destination $dest -Recurse -Force
Write-Host " done" -ForegroundColor Green

# ── Summary ───────────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "=== Installed files ===" -ForegroundColor Green
Get-ChildItem $dest | ForEach-Object { Write-Host "  $($_.Name)" }
Write-Host ""
Write-Host "Origo $Version is ready. Run 'npm run dev' to start the map." -ForegroundColor Green
Write-Host ""
