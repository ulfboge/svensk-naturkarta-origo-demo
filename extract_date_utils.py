# -*- coding: utf-8 -*-
"""Safe date extraction from NR_polygon.shp (fiona crashes on year-0 dates)."""
from datetime import date, datetime

import shapefile

DEFAULT_SHP = 'E:/NR/NR/NR_polygon.shp'


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


def load_nvrid_dates(shp=DEFAULT_SHP):
    """Return {NVRID: 'YYYY-MM-DD'} from shapefile."""
    reader = shapefile.Reader(shp, encoding='utf-8')
    index = {}
    for record in reader.iterRecords():
        row = record.as_dict()
        nvrid = str(row.get('NVRID') or '').strip()
        if not nvrid:
            continue
        index[nvrid] = format_date(row.get('URSBESLDAT'))
    return index
