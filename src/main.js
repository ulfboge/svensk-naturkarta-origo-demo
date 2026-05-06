// ─────────────────────────────────────────────────────────────────────────────
// src/main.js — Application entry point
//
// Steps:
//   1. Import Origo's CSS (required — without this the UI renders broken)
//   2. Import our own CSS overrides
//   3. Fetch /config/origo.json (from public/ — served as-is by Vite)
//   4. Call Origo(config) to start the map
//
// Why fetch instead of import()?
//   The JSON config can be edited without touching JS or triggering a rebuild.
//   Origo is designed to be configuration-driven — this is the intended pattern.
// ─────────────────────────────────────────────────────────────────────────────

// Origo's own stylesheet — includes all control/popup/panel styles.
// If this import fails after `npm install`, check:
//   ls node_modules/origo-map/
// Common alternative path: 'origo-map/dist/origo.css'
import 'origo-map/css/origo.css';

// Our nature-themed overrides (full-page layout, green loading screen, etc.)
import './style.css';

// The Origo factory function
import Origo from 'origo-map';

async function initMap() {
  const loadingScreen = document.getElementById('loading-screen');

  try {
    // Fetch the map configuration from public/config/origo.json
    const response = await fetch('/config/origo.json');

    if (!response.ok) {
      throw new Error(
        `Kunde inte hämta kartkonfigurationen (HTTP ${response.status}). ` +
        `Kontrollera att filen public/config/origo.json finns.`
      );
    }

    const config = await response.json();

    // Remove the loading screen before Origo takes over the container
    if (loadingScreen) loadingScreen.remove();

    // Initialise the Origo viewer.
    // config.map.target tells Origo which DOM element to mount into.
    const viewer = Origo(config);

    // Expose the viewer for debugging in the browser console:
    //   window.viewer.getMap()      → raw OpenLayers Map object
    //   window.viewer.getLayers()   → all layer objects
    //   window.viewer.getControls() → all control objects
    window.viewer = viewer;

    console.info(
      '%c🌲 Naturkarta laddad',
      'color: #2d6a4f; font-weight: bold; font-size: 13px;'
    );

  } catch (error) {
    console.error('Fel vid laddning av naturkarta:', error);

    if (loadingScreen) {
      loadingScreen.innerHTML = `
        <div class="load-error">
          <div style="font-size: 2rem; margin-bottom: 1rem;">⚠️</div>
          <h2>Kartan kunde inte laddas</h2>
          <p>${error.message}</p>
          <small>Öppna webbkonsolen (F12) för mer information.</small>
        </div>
      `;
    }
  }
}

initMap();
