"""Crawl durable-equipment products from the inspiration site into a JSON file.

Takes only facts: product name, brand, category and spec-table rows.
Does NOT take descriptions, photos or prices (by decision: Biozen writes its
own copy, uses its own photos and sets its own prices).

Polite by design: one request at a time with a delay, and every page is
cached on disk so re-runs don't re-fetch.

Usage: python3 -I crawl.py <cache_dir> <out.json>
"""
import html
import json
import os
import re
import sys
import time
import urllib.request

BASE = 'https://www.maesiopharmaceuticals.co.ke'
UA = 'Mozilla/5.0 (X11; Linux x86_64) catalogue-research'
DELAY = 1.0

# Maesio parent segment -> Biozen top-level category slug.
PARENTS = {
    'medical-supplies-patient-monitoring-life-support-equipment': 'patient-monitoring',
    'medical-supplies-hospital-furniture-ward-equipment': 'hospital-furniture',
    'medical-supplies-theatre-surgical-equipment': 'theatre-surgical',
    'medical-supplies-diagnostic-examination-equipment': 'diagnostic-examination',
    'medical-supplies-obstetric-neonatal-equipment': 'maternal-neonatal',
    'medical-supplies-dental-equipment': 'dental',
    'medical-supplies-ent-equipment': 'ent-ophthalmology',
    'medical-supplies-ophthalmology-equipment': 'ent-ophthalmology',
    'medical-supplies-sterilization-disinfection-equipment': 'sterilization',
    'medical-supplies-emergency-first-aid-equipment': 'emergency-first-aid',
    'medical-supplies-rehabilitation-physiotherapy-equipment': 'rehab-mobility',
    'medical-supplies-hospital-infrastructure-utilities': 'facility-infrastructure',
    'medical-supplies-accessories-spares': 'accessories-spares',
    'medical-supplies-laboratory-equipment': 'laboratory',
    'medical-supplies-radiology-imaging': 'imaging',
    'medical-supplies-dialysis-equipment': 'dialysis',
    'nursing-training-models': 'training-models',
}

# Leaf categories moved to a different Biozen top category.
OVERRIDES = {
    'oxygen-concentrators': 'respiratory-oxygen',
    'oxygen-cylinders-regulators': 'respiratory-oxygen',
    'nebulizers-humidifiers': 'respiratory-oxygen',
    'autoclaves-vertical-horizontal-tabletop': 'sterilization',
    'slit-lamps-lens-sets': 'ent-ophthalmology',
    'fundus-cameras': 'ent-ophthalmology',
    'snellen-eye-charts': 'ent-ophthalmology',
}

# Consumables / single-use / out-of-scope leaves (Biozen sells no drugs or consumables).
EXCLUDE = re.compile(
    r'consumables|rapid-kits|reagents|disposable|nebulizer-masks|reservoir-bags|'
    r'ventilator-circuits|uniforms|scrubs|linen|ureteral|stents|vascular|ivc-filter|'
    r'pta-balloon|grafts|urology|print-media|speculums-tongue|sterilization-indicators'
)

# Name-level safety net for consumables filed under equipment categories.
EXCLUDE_NAME = re.compile(
    r'\b(test strips?|strips|lancets?|reagents?|rapid test|test kits?|test cassettes?|'
    r'gloves?|disposable|single[- ]use|sachets?|electrodes?|gel|cannulas?|catheters?|'
    r'syringes?(?! pump)|needles?|swabs?|sutures?)\b',
    re.I,
)


def fetch(url, cache_dir):
    key = re.sub(r'[^a-z0-9]+', '_', url.lower())[-180:]
    path = os.path.join(cache_dir, key + '.html')
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            return f.read()
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept-Encoding': 'identity'})
            with urllib.request.urlopen(req, timeout=90) as r:
                body = r.read().decode('utf-8', 'replace')
            with open(path, 'w', encoding='utf-8') as f:
                f.write(body)
            time.sleep(DELAY)
            return body
        except Exception as e:  # network hiccup: back off and retry
            print(f'  retry {attempt + 1} {url}: {e}', flush=True)
            time.sleep(5 * (attempt + 1))
    return ''


def text(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()


def leaf_categories(sitemap_urls):
    slugs = [u.split('/shop/category/')[1] for u in sitemap_urls if '/shop/category/' in u]
    leaves = []
    for slug in slugs:
        for parent, top in PARENTS.items():
            rest = slug[len(parent) + 1:] if slug.startswith(parent + '-') else None
            if not rest:
                continue
            rest_name = '' if re.fullmatch(r'\d+', rest) else re.sub(r'-\d+$', '', rest)
            # Parent pages list their excluded children too, so only leaves are crawled.
            if not rest_name or EXCLUDE.search(slug):
                break
            # skip intermediate parents that have their own leaves (e.g. rapid-kits)
            top_final = next((v for k, v in OVERRIDES.items() if rest_name.startswith(k)), top)
            leaves.append({'slug': slug, 'top': top_final})
            break
    return leaves


def crawl_category(slug, cache_dir):
    found = {}
    page = 1
    title = ''
    while True:
        url = f'{BASE}/shop/category/{slug}' + (f'/page/{page}' if page > 1 else '')
        h = fetch(url, cache_dir)
        if not h:
            break
        if page == 1:
            m = re.search(r'<title>([^<|]+)', h)
            title = html.unescape(m.group(1)).strip() if m else slug
        before = len(found)
        for m in re.finditer(r'<form[^>]*oe_product_cart[^>]*aria-label="([^"]*)".*?href="/shop/(?:[^"/]+/)?([a-z0-9-]+-(\d+))"', h, re.S):
            found.setdefault(m.group(3), {'name': html.unescape(m.group(1)).strip(), 'path': m.group(2)})
        if len(found) == before or f'/page/{page + 1}"' not in h:
            break
        page += 1
    return title, found


SKIP_SPEC_KEYS = re.compile(r'price|listing|ksh|kes|stock|availability|delivery|warranty|supplier|confirm|order|payment|maesio', re.I)
CLEAN_VAL = re.compile(r',?\s*(according to (the )?(current )?(kenya )?listing|per (the )?(current )?listing|as listed|confirm[^.;]*)', re.I)


def parse_product(h):
    brand = ''
    specs = {}
    for table in re.findall(r'<table.*?</table>', h, re.S):
        rows = re.findall(r'<tr.*?</tr>', table, re.S)
        if not rows:
            continue
        head = text(rows[0]).lower()
        if 'specification' not in head and 'feature' not in head and 'parameter' not in head:
            continue
        for row in rows[1:]:
            cells = [text(c) for c in re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', row, re.S)]
            if len(cells) < 2 or not cells[0] or not cells[1]:
                continue
            k, v = cells[0][:60], CLEAN_VAL.sub('', cells[1]).strip(' ,;')[:160]
            if not v or SKIP_SPEC_KEYS.search(k) or SKIP_SPEC_KEYS.search(v):
                continue
            if k.lower() in ('brand', 'manufacturer', 'make'):
                brand = brand or v
            elif k.lower() not in ('product', 'product name', 'item', 'name', 'applications'):
                specs.setdefault(k, v)
        if specs or brand:
            break
    return brand, dict(list(specs.items())[:10])


def main():
    cache_dir, out_path = sys.argv[1], sys.argv[2]
    os.makedirs(cache_dir, exist_ok=True)
    sitemap = fetch(f'{BASE}/sitemap.xml', cache_dir)
    urls = re.findall(r'<loc>([^<]+)</loc>', sitemap)
    leaves = leaf_categories(urls)
    print(f'{len(leaves)} equipment categories', flush=True)

    products = {}
    for i, leaf in enumerate(leaves, 1):
        title, found = crawl_category(leaf['slug'], cache_dir)
        leaf['name'] = title
        new = 0
        for pid, p in found.items():
            if pid in products or EXCLUDE_NAME.search(p['name']):
                continue
            products[pid] = {**p, 'top': leaf['top'], 'sub': title, 'id': pid}
            new += 1
        print(f'[{i}/{len(leaves)}] {title}: {len(found)} listed, {new} new (total {len(products)})', flush=True)

    for i, p in enumerate(products.values(), 1):
        h = fetch(f"{BASE}/shop/{p['path']}", cache_dir)
        p['brand'], p['specs'] = parse_product(h) if h else ('', {})
        if i % 25 == 0:
            print(f'details {i}/{len(products)}', flush=True)

    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(list(products.values()), f, ensure_ascii=False, indent=1)
    print(f'DONE {len(products)} products -> {out_path}', flush=True)


if __name__ == '__main__':
    main()
