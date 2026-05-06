import { defineConfig } from 'vite';

// ─────────────────────────────────────────────────────────────────────────────
// vite.config.js
//
// Vite development server + build configuration.
//
// The most important section for GIS work is the `proxy` block:
// Any request from the browser starting with /geoserver or /qgis-server
// is silently forwarded to the local map server. This avoids CORS issues
// when running GeoServer or QGIS Server locally.
//
// External WMS services (Naturvårdsverket, Skogsstyrelsen) are fetched
// directly by the browser — no proxy needed because they support CORS.
// ─────────────────────────────────────────────────────────────────────────────

export default defineConfig({
  server: {
    port: 3000,

    proxy: {
      // Local GeoServer — Phase 5 (not needed until local PostGIS setup)
      '/geoserver': {
        target: 'http://localhost:8080',
        changeOrigin: true,
        secure: false,
      },
      // Local QGIS Server — Phase 5
      '/qgis-server': {
        target: 'http://localhost:8081',
        changeOrigin: true,
        secure: false,
      },
    },
  },

  build: {
    outDir: 'dist',
    rollupOptions: {
      output: {
        // Put Origo (+ OpenLayers) in its own chunk so it can be
        // cached independently of application code changes.
        manualChunks: {
          'origo-vendor': ['origo-map'],
        },
      },
    },
  },

  // Pre-bundle origo-map on `npm run dev` startup for faster cold starts.
  optimizeDeps: {
    include: ['origo-map'],
  },
});
