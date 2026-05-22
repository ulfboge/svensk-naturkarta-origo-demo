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
    page.wait_for_timeout(1500)


def main():
    DOCS.mkdir(exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto(BASE)
        wait_for_map(page)

        # Overview — Gävleborgs län med NR + NP
        page.select_option('#county-select', 'gav')
        page.wait_for_timeout(2500)
        page.screenshot(path=str(DOCS / 'screenshot-overview.png'))

        # Stats + IUCN + slider synliga (samma vy, fokus nedre vänster)
        stats = page.locator('#stats-panel')
        stats.screenshot(path=str(DOCS / 'screenshot-stats.png'))

        # Tidslinje — dra till 1960
        slider = page.locator('#year-slider')
        slider.fill('1960')
        slider.dispatch_event('input')
        page.wait_for_timeout(1200)
        page.screenshot(path=str(DOCS / 'screenshot-timeline.png'))

        # Popup — zooma till ett känt reservat via sök
        page.select_option('#county-select', 'gav')
        page.wait_for_timeout(1500)
        search = page.locator('#reservat-search')
        search.fill('Hamra')
        search.dispatch_event('change')
        page.wait_for_timeout(2000)
        # Klicka ungefär där Hamra NP ligger (Gävleborg)
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
