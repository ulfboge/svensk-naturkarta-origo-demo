# -*- coding: utf-8 -*-
"""Backfill URSPR_BESLUTSDATUM in county GeoJSON from NR_polygon.shp.

Fiona crashes on year-0 dates in the DBF; pyshp reads them safely.
"""
import json
import glob
from datetime import date, datetime

import shapefile

SHP = 'E:/NR/NR/NR_polygon.shp'
NP_SHP = 'E:/NP/NP/NP_polygon.shp'
DATA_DIR = 'public/data'


def format_date(value):
    if not value:
        return ''
    if isinstance(value, (date, datetime)):
        if value.year < 1:
            return ''
        return value.isoformat()
    text = str(value).strip()
    if not text or text.startswith('0000') or text.startswith('0-'):
        return ''
    return text[:10]


def load_date_index(shp=SHP):
    reader = shapefile.Reader(shp, encoding='utf-8')
    index = {}
    for record in reader.iterRecords():
        row = record.as_dict()
        nvrid = str(row.get('NVRID') or '').strip()
        if not nvrid:
            continue
        index[nvrid] = format_date(row.get('URSBESLDAT'))
    return index


def backfill_file(path, date_index):
    with open(path, encoding='utf-8') as fh:
        data = json.load(fh)

    updated = 0
    for feature in data.get('features', []):
        props = feature.get('properties', {})
        nvrid = str(props.get('NVRID') or '').strip()
        if not nvrid or nvrid not in date_index:
            continue
        new_date = date_index[nvrid]
        if new_date and props.get('URSPR_BESLUTSDATUM') != new_date:
            props['URSPR_BESLUTSDATUM'] = new_date
            updated += 1

    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(data, fh, ensure_ascii=False, separators=(',', ':'))

    features = data.get('features', [])
    filled = sum(1 for f in features if f.get('properties', {}).get('URSPR_BESLUTSDATUM'))
    return updated, len(features), filled


def main():
    date_index = load_date_index()
    print(f'Loaded {len(date_index)} NVRID date mappings from shapefile')

    total_updated = 0
    for path in sorted(glob.glob(f'{DATA_DIR}/naturreservat-*.geojson')):
        updated, count, filled = backfill_file(path, date_index)
        total_updated += updated
        print(f'  {path}: {updated} updated, {filled}/{count} with dates')

    np_path = f'{DATA_DIR}/nationalparker-alla.geojson'
    np_index = load_date_index(NP_SHP)
    updated, count, filled = backfill_file(np_path, np_index)
    total_updated += updated
    print(f'  {np_path}: {updated} updated, {filled}/{count} with dates')

    print(f'Done — {total_updated} features updated in total')


if __name__ == '__main__':
    main()
