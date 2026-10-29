#!/usr/bin/env python3
"""
parse_calendar.py — Convert the Pleasure Island Design Instagram planning
workbook (.xlsx) into a structured content-calendar.json.

Dependency-free: reads the .xlsx (a zip of XML) with the standard library only,
so it runs anywhere Python 3 is available — no pip install required.

Usage:
    python3 automation/instagram/parse_calendar.py <path-to.xlsx> [out.json]

Output (default: automation/instagram/content-calendar.json):
    {
      "source": "<xlsx filename>",
      "generated_by": "parse_calendar.py",
      "sheets": {
        "<sheet name>": [ { "<header>": "<cell>", ... }, ... ]
      },
      "posts": [ ... rows from the first calendar-shaped sheet ... ]
    }

The first sheet whose header row contains a "Caption" column is treated as the
posting calendar and surfaced under "posts". Every sheet is also emitted in full
under "sheets" so nothing in the workbook is lost.
"""
import sys
import os
import re
import json
import html
import zipfile
import datetime


# Excel's day 0 is 1899-12-30 (the offset absorbs Excel's fictional 1900 leap day).
_EXCEL_EPOCH = datetime.date(1899, 12, 30)


def _excel_serial_to_iso(value):
    """Convert an Excel date serial (e.g. '45880' or '45880.0') to 'YYYY-MM-DD'.
    Returns the original string if it doesn't look like a serial in a sane range."""
    if not re.fullmatch(r'\d+(\.\d+)?', value):
        return value
    days = int(float(value))
    # Guard against plain small integers that aren't dates.
    if days < 20000 or days > 80000:  # ~1954 .. ~2119
        return value
    return (_EXCEL_EPOCH + datetime.timedelta(days=days)).isoformat()


def _normalize_dates(records):
    """In-place: convert any column whose header contains 'date' from an Excel
    serial to an ISO date string, so downstream tooling gets real dates."""
    for rec in records:
        for key in rec:
            if 'date' in key.lower() and isinstance(rec[key], str):
                rec[key] = _excel_serial_to_iso(rec[key])
    return records


def _col_to_index(col_letters):
    n = 0
    for ch in col_letters:
        n = n * 26 + (ord(ch) - 64)
    return n - 1


def _load_shared_strings(zf):
    strings = []
    if 'xl/sharedStrings.xml' not in zf.namelist():
        return strings
    data = zf.read('xl/sharedStrings.xml').decode('utf-8')
    for si in re.findall(r'<si>(.*?)</si>', data, re.S):
        parts = re.findall(r'<t[^>]*>(.*?)</t>', si, re.S)
        strings.append(html.unescape(''.join(parts)))
    return strings


def _sheet_targets(zf):
    """Return [(sheet_name, worksheet_path), ...] in workbook order."""
    wb = zf.read('xl/workbook.xml').decode('utf-8')
    rels = zf.read('xl/_rels/workbook.xml.rels').decode('utf-8')
    rid_to_target = dict(re.findall(
        r'<Relationship[^>]*Id="([^"]+)"[^>]*Target="([^"]+)"', rels))
    out = []
    for name, rid in re.findall(r'<sheet[^>]*name="([^"]+)"[^>]*r:id="([^"]+)"', wb):
        target = rid_to_target.get(rid, '').lstrip('/')
        if target.startswith('xl/'):
            target = target[3:]
        out.append((html.unescape(name), target))
    return out


def _parse_rows(zf, path, shared):
    xml = zf.read('xl/' + path).decode('utf-8')
    rows = []
    for row_xml in re.findall(r'<row[^>]*>(.*?)</row>', xml, re.S):
        cells = {}
        for attrs, inner in re.findall(r'<c\b([^>]*)>(.*?)</c>', row_xml, re.S):
            ref = re.search(r'r="([A-Z]+)\d+"', attrs)
            if not ref:
                continue
            idx = _col_to_index(ref.group(1))
            typ = re.search(r't="([^"]+)"', attrs)
            val = re.search(r'<v>(.*?)</v>', inner, re.S)
            if typ and typ.group(1) == 's' and val:
                cells[idx] = shared[int(val.group(1))]
            elif typ and typ.group(1) == 'inlineStr':
                parts = re.findall(r'<t[^>]*>(.*?)</t>', inner, re.S)
                cells[idx] = html.unescape(''.join(parts))
            elif val:
                cells[idx] = html.unescape(val.group(1))
        if cells:
            width = max(cells) + 1
            rows.append([cells.get(i, '').strip() for i in range(width)])
        else:
            rows.append([])
    return rows


def _rows_to_records(rows):
    """First non-empty row is the header; subsequent non-empty rows become dicts."""
    header = None
    records = []
    for row in rows:
        if not any(c for c in row):
            continue
        if header is None:
            header = [c or f'col_{i}' for i, c in enumerate(row)]
            continue
        rec = {}
        for i, key in enumerate(header):
            rec[key] = row[i] if i < len(row) else ''
        if any(v for v in rec.values()):
            records.append(rec)
    return header or [], records


def parse(xlsx_path):
    zf = zipfile.ZipFile(xlsx_path)
    shared = _load_shared_strings(zf)
    result = {
        'source': os.path.basename(xlsx_path),
        'generated_by': 'parse_calendar.py',
        'sheets': {},
        'posts': [],
    }
    posts_found = False
    for name, path in _sheet_targets(zf):
        rows = _parse_rows(zf, path, shared)
        header, records = _rows_to_records(rows)
        records = _normalize_dates(records)
        result['sheets'][name] = records
        if not posts_found and any(h.lower() == 'caption' for h in header):
            result['posts'] = records
            posts_found = True
    return result


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 1
    xlsx_path = argv[1]
    out_path = argv[2] if len(argv) > 2 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'content-calendar.json')
    if not os.path.exists(xlsx_path):
        print(f"[ERROR] File not found: {xlsx_path}")
        return 1
    data = parse(xlsx_path)
    with open(out_path, 'w', encoding='utf-8') as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
    n_posts = len(data['posts'])
    n_sheets = len(data['sheets'])
    print(f"[OK] Parsed {n_sheets} sheet(s), {n_posts} calendar post(s).")
    print(f"[OK] Wrote {out_path}")
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
