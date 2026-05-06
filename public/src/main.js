// src/main.js — Naturkarta entry point
// ─────────────────────────────────────────────────────────────────────────────
// Plain JavaScript — no ES modules, no build tool required.
// Origo() is a global function registered by origo/js/origo.min.js,
// which is loaded as a <script> tag before this file in index.html.
//
// All this file does:
//   1. Verify the Origo global is available
//   2. Call Origo('config/origo.json') to boot the map
//   3. Expose window.viewer for browser-console debugging
//   4. Handle errors with a friendly on-screen message
//
// To debug in the browser console (F12):
//   window.viewer.getMap()      — the underlying OpenLayers Map object
//   window.viewer.getLayers()   — array of Origo layer objects
// ─────────────────────────────────────────────────────────────────────────────

(function () {
  'use strict';

  var loadingScreen = document.getElementById('loading-screen');

  // Display a friendly error card inside the loading screen
  function showError(message) {
    if (loadingScreen) {
      loadingScreen.innerHTML =
        '<div class="load-error">' +
          '<h2>⚠️ Kartan kunde inte laddas</h2>' +
          '<p>' + message + '</p>' +
          '<small>Se konsolen (F12) för mer information.</small>' +
        '</div>';
    }
    console.error('[Naturkarta]', message);
  }

  // Guard: Origo must be loaded before this script runs
  if (typeof Origo === 'undefined') {
    showError(
      'Origo-biblioteket saknas. ' +
      'Kontrollera att filen public/origo/js/origo.min.js finns ' +
      'och att du kör från public/-katalogen.'
    );
    return;
  }

  try {
    // Remove the loading screen before Origo takes over #app-wrapper
    if (loadingScreen) {
      loadingScreen.parentNode.removeChild(loadingScreen);
    }

    // Boot the map.
    // 'config/origo.json' is a URL relative to the page root (public/).
    // Origo fetches it, reads layers/controls/styles, and renders into
    // the <div id="app-wrapper"> element defined in index.html.
    var viewer = Origo('config/origo.json');

    // Expose for live inspection in the browser console
    window.viewer = viewer;

    console.info(
      '%c Naturkarta startad',
      'background:#2d6a4f;color:#d8f3dc;font-weight:bold;padding:2px 6px;border-radius:3px'
    );

  } catch (err) {
    showError('Fel vid initiering av kartan: ' + (err.message || err));
  }

}());
