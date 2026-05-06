// ─────────────────────────────────────────────────────────────────────────────
// src/main.js
//
// This module runs after origo.min.js has already registered the global
// Origo() function. Two jobs:
//   1. Import our green-theme CSS so Vite processes and serves it
//   2. Call Origo('/config/origo.json') to start the map
//
// Origo loads the JSON config itself, reads all layers/controls/styles from it,
// and renders everything into <div id="app-wrapper"> in index.html.
// ─────────────────────────────────────────────────────────────────────────────

// Our forest-green overrides on top of Origo's own CSS
import './style.css';

// Origo is a global set by /origo/js/origo.min.js (loaded before this module).
// Passing a path tells Origo to fetch the JSON itself.
// The second argument (optional options object) can override the target div id
// if you ever need to rename it from the default "app-wrapper".
const viewer = Origo('/config/origo.json');

// Expose on window so you can inspect the live map in the browser console:
//   window.viewer.getMap()       → OpenLayers Map instance
//   window.viewer.getLayers()    → array of layer objects
window.viewer = viewer;
