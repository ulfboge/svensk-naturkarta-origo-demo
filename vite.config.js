import { defineConfig } from 'vite';

// ─────────────────────────────────────────────────────────────────────────────
// vite.config.js
//
// Vite is used here purely as a development server and build tool.
// Origo itself is NOT an npm package — it is a pre-built browser bundle
// downloaded from github.com/origo-map/origo and placed in public/origo/.
//
// In development the proxy rules below forward /geoserver and /qgis-server
// requests to local map servers, avoiding CORS issues.
// External Swedish WMS services (Naturvårdsverket, Skogsstyrelsen) support
// CORS natively and are fetched directly by the browser.
// ─────────────────────────────────────────────────────────────────────────────

export default defineConfig({
  server: {
    port: 3000,
    proxy: {
      // Local GeoServer (Phase 5 — not needed yet)
      '/geoserver': {
        target: 'http://localhost:8080',
        changeOrigin: true,
        secure: false,
      },
      // Local QGIS Server (Phase 5 — not needed yet)
      '/qgis-server': {
        target: 'http://localhost:8081',
        changeOrigin: true,
        secure: false,
      },
    },
  },
  build: {
    outDir: 'dist',
  },
});
