# -*- coding: utf-8 -*-
"""Capture README screenshots (requires dev server on localhost:3000)."""
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
BASE = 'http://localhost:3000'


def wait_for_map(page, timeout_ms=20000):
    page.wait_for_function(
        '() => window.viewer && window.viewer.api && window.viewer.api().getMap()',
        timeout=timeout_ms,
    )


def wait_for_basemap_tiles(page, timeout_ms=45000):
    """Wait until OpenLayers has painted at least one basemap tile."""
    page.wait_for_function(
        """
        () => {
          const canvases = document.querySelectorAll('.ol-layer canvas');
          for (const c of canvases) {
            if (c.width > 64 && c.height > 64) return true;
          }
          const imgs = document.querySelectorAll('.ol-layer img');
          for (const img of imgs) {
            if (img.complete && img.naturalWidth > 0) return true;
          }
          return false;
        }
        """,
        timeout=timeout_ms,
    )


def wait_for_county_boundary(page, timeout_ms=15000):
    page.wait_for_function(
        """
        () => {
          const map = window.viewer.api().getMap();
          function find(name, arr) {
            for (const x of arr) {
              if (x.getLayers) { const h = find(name, x.getLayers().getArray()); if (h) return h; }
              if (x.get('name') === name) return x;
            }
            return null;
          }
          const lan = find('lan_grans', map.getLayerGroup().getLayers().getArray());
          return lan && lan.getVisible() && lan.getSource().getFeatures().length > 0;
        }
        """,
        timeout=timeout_ms,
    )


def wait_for_county_ready(page, county_label, timeout_ms=30000):
    """County selected — stats header and NR count should be populated."""
    page.wait_for_function(
        """
        (label) => {
          const header = document.getElementById('stats-county');
          const count = document.getElementById('stats-nr-count');
          if (!header || !count) return false;
          const headerOk = header.textContent && header.textContent.includes(label);
          const countText = (count.textContent || '').trim();
          const countOk = countText && countText !== '—' && countText !== '...';
          return headerOk && countOk;
        }
        """,
        arg=county_label,
        timeout=timeout_ms,
    )


def main():
    DOCS.mkdir(exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto(BASE, wait_until='load')
        wait_for_map(page)
        page.wait_for_timeout(4000)
        wait_for_basemap_tiles(page)

        # Overview — Gävleborgs län med NR + NP
        page.select_option('#county-select', 'gav')
        wait_for_county_ready(page, 'Gävleborg')
        wait_for_county_boundary(page)
        wait_for_basemap_tiles(page)
        page.wait_for_timeout(800)
        page.screenshot(path=str(DOCS / 'screenshot-overview.png'))

        # Stats + IUCN + slider synliga (samma vy, fokus nedre vänster)
        stats = page.locator('#stats-panel')
        stats.screenshot(path=str(DOCS / 'screenshot-stats.png'))

        # Tidslinje — dra till 1960
        slider = page.locator('#year-slider')
        slider.fill('1960')
        slider.dispatch_event('input')
        wait_for_basemap_tiles(page)
        page.wait_for_timeout(600)
        page.screenshot(path=str(DOCS / 'screenshot-timeline.png'))

        # Popup — zooma till ett känt reservat via sök
        page.select_option('#county-select', 'gav')
        wait_for_county_ready(page, 'Gävleborg')
        search = page.locator('#reservat-search')
        search.fill('Hamra')
        search.dispatch_event('change')
        page.wait_for_timeout(2500)
        page.locator('.ol-viewport').click(position={'x': 720, 'y': 420})
        page.wait_for_timeout(2000)
        popup = page.locator('.o-identify-content').first
        if popup.count():
            popup.screenshot(path=str(DOCS / 'screenshot-pop-up.png'))
        else:
            page.screenshot(path=str(DOCS / 'screenshot-pop-up.png'))

        browser.close()
    print('Screenshots saved to docs/')


if __name__ == '__main__':
    main()
