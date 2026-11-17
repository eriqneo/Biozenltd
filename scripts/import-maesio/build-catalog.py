"""Turn crawl output into Biozen's catalogue file (src/lib/data/catalog.json).

- Prices: none. Every product is "Price on quote" until Biozen sets its own.
- Copy: short original summary/description generated from the facts.
- Images: a Biozen illustration where one fits the subcategory, else none.

Usage: python3 -I build-catalog.py <products.json> <out catalog.json>
"""
import json
import re
import sys
from collections import Counter

TOPS = [
    ('patient-monitoring', 'Patient Monitoring', 'Monitors, ECG, defibrillators, infusion pumps and ventilators.'),
    ('respiratory-oxygen', 'Respiratory & Oxygen', 'Oxygen concentrators, cylinders, regulators and nebulizers.'),
    ('hospital-furniture', 'Hospital Furniture', 'Beds, trolleys, stretchers, lockers, IV stands and ward screens.'),
    ('theatre-surgical', 'Theatre & Surgical', 'Operating lights, cautery units, anaesthesia machines and instrument sets.'),
    ('diagnostic-examination', 'Diagnostic & Examination', 'Diagnostic sets, stethoscopes, thermometers, scales and exam lights.'),
    ('maternal-neonatal', 'Maternal & Neonatal', 'Infant warmers, incubators, phototherapy units and fetal dopplers.'),
    ('dental', 'Dental', 'Dental chairs, scalers, curing lights and handpieces.'),
    ('ent-ophthalmology', 'ENT & Ophthalmology', 'Otoscopes, laryngoscopes, slit lamps and refraction equipment.'),
    ('sterilization', 'Sterilization', 'Autoclaves, dry heat sterilizers and CSSD fittings.'),
    ('laboratory', 'Laboratory', 'Analyzers, centrifuges, microscopes, water baths and safety cabinets.'),
    ('imaging', 'Imaging', 'X-ray systems, ultrasound, CT and MRI.'),
    ('dialysis', 'Dialysis', 'Dialysis machines and dialysis chairs.'),
    ('rehab-mobility', 'Rehab & Mobility', 'Wheelchairs, walkers, commode chairs and physiotherapy equipment.'),
    ('emergency-first-aid', 'Emergency & First Aid', 'Resuscitators, spine boards, splints and first aid boxes.'),
    ('facility-infrastructure', 'Facility Infrastructure', 'Medical gas pipelines, RO water units, nurse call and cold chain.'),
    ('training-models', 'Training Models', 'CPR manikins, airway trainers and anatomical models.'),
    ('accessories-spares', 'Accessories & Spares', 'ECG leads, BP cuffs, SpO₂ sensors and bed accessories.'),
]

# Tops where Biozen offers delivery, installation and user training.
INSTALL_TOPS = {'patient-monitoring', 'hospital-furniture', 'theatre-surgical', 'maternal-neonatal', 'dental',
                'ent-ophthalmology', 'sterilization', 'laboratory', 'imaging', 'dialysis', 'facility-infrastructure'}

# Subcategory keyword -> Biozen illustration (public/images/products/*.svg).
ILLUSTRATIONS = [
    (r'multiparameter|vital signs|patient monitor', 'multiparameter-patient-monitor-12-inch'),
    (r'ecg|ekg', '12-channel-ecg-machine'),
    (r'defibrillator|aed', 'automated-external-defibrillator-aed'),
    (r'infusion pump', 'syringe-infusion-pump'),
    (r'blood pressure|bp monitor|stethoscopes', 'digital-blood-pressure-monitor-upper-arm'),
    (r'oxygen concentrator', 'oxygen-concentrator-5l'),
    (r'nebuli', 'compressor-nebulizer'),
    (r'hospital beds', 'electric-icu-bed-five-function'),
    (r'stretcher|trolley', 'emergency-stretcher-trolley'),
    (r'iv stand|drip pole', 'stainless-steel-iv-stand'),
    (r'diagnostic sets|otoscope|ophthalmoscope', 'wall-mounted-diagnostic-set'),
    (r'baby weighing|weighing scale', 'digital-baby-weighing-scale'),
    (r'infant warmer|radiant', 'infant-radiant-warmer'),
    (r'doppler', 'pocket-fetal-doppler'),
    (r'autoclave|steriliz', 'tabletop-autoclave-23l'),
    (r'centrifuge', 'benchtop-centrifuge-6000rpm'),
    (r'microscop', 'binocular-led-microscope'),
    (r'wheelchair', 'foldable-manual-wheelchair'),
    (r'crutch|walker|walking frame|cane', 'aluminium-walking-frame'),
    (r'cpr', 'adult-cpr-training-manikin'),
]


# Consumables that slipped into equipment categories (Biozen sells none).
CONSUMABLE = re.compile(
    r"x-?ray film|dry film|fuji .*film|autoclave tape|substrate solution|pipette tips|microscope slides|"
    r"pasteur pipette|brazing|biohazard|stress ball|patient plate|oxygen mask|suction filter|hepa filter|sediment.*filter|"
    r"delivery packs|puncture kit|skin traction|adhesive traction|\d+\s*(?:[’']s|sheets)\b",
    re.I,
)

# Brands recognised in product names (factual manufacturer names).
KNOWN_BRANDS = ['Omron', 'Yuwell', 'Sinocare', 'Accu-Chek', 'Mindray', 'Contec', 'Edan', 'Philips', 'Dräger', 'Drager',
                'Riester', 'Heine', 'Welch Allyn', 'Littmann', 'Hettich', 'Fuji', 'Finecare', 'Seamaty', 'Micropoint',
                'Joanlab', 'Wato', '3M', 'Ecomed', 'Laerdal', 'Seca', 'Longfian', 'Yonker', 'Comen', 'Appasamy',
                'Olympus', 'Rossmax', 'Beurer', 'Cerachek', 'Ipas', 'Roche', 'Folee', 'Bercann', 'Peakmed', 'Meditech', 'Keeler']
BRAND_ALIASES = {'appasamy associates': 'Appasamy', 'drager': 'Dräger', 'ecomed': 'EcoMed', 'joanlab': 'JOANLAB'}


def slugify(s):
    s = s.lower().replace('&', ' and ').replace('₂', '2')
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')[:80]


def clean_sub(title):
    """'Oxygen Concentrators (3L / 5L / 10L)' -> 'Oxygen Concentrators'."""
    t = re.sub(r'\s*\([^)]*\)', '', title).strip()
    return t or title


def tidy_name(name):
    """Drop marketing taglines: 'Bedside Cabinet (ABS) – Durable, Hygienic…' -> 'Bedside Cabinet (ABS)'."""
    name = re.sub(r'\s+', ' ', name).strip(' -–|')
    head = re.split(r'\s[–—|]\s|\s-(?=[A-Z])', name)[0].strip(' -–|')
    if len(head.split()) >= 2:
        name = head
    return name[:1].upper() + name[1:]


def tidy_brand(b):
    b = re.sub(r'\s*\(.*?\)', '', b).strip(' .,;')
    if not b or len(b) > 40 or re.search(r'various|generic|n/a|unbranded|confirm|assorted|multiple|dependent|^not\b|unspecified|unknown', b, re.I):
        return ''
    b = BRAND_ALIASES.get(b.lower(), b)
    return b if any(c.islower() for c in b) or len(b) <= 4 else b.title()


def brand_from_name(name):
    for b in KNOWN_BRANDS:
        if re.search(rf'(?<![A-Za-z]){re.escape(b)}(?![A-Za-z])', name, re.I):
            return BRAND_ALIASES.get(b.lower(), b)
    return ''


def main():
    src, out = sys.argv[1], sys.argv[2]
    raw = json.load(open(src, encoding='utf-8'))
    tops = {slug: name for slug, name, _ in TOPS}

    categories = [
        {'id': slug, 'slug': slug, 'name': name, 'description': desc, 'parent': '', 'icon': '', 'sort': i + 1}
        for i, (slug, name, desc) in enumerate(TOPS)
    ]
    subs = {}
    brands = {}
    products = []
    used_slugs = set()

    skipped = 0
    for p in raw:
        top = p['top']
        if top not in tops or CONSUMABLE.search(p['name']):
            skipped += 1
            continue
        sub_name = clean_sub(p['sub'])
        sub_slug = slugify(sub_name)
        sub_id = f'{top}--{sub_slug}'
        if sub_id not in subs:
            subs[sub_id] = {'id': sub_id, 'slug': sub_slug, 'name': sub_name, 'description': '', 'parent': top, 'icon': '', 'sort': 0}

        brand_name = tidy_brand(p.get('brand', '')) or brand_from_name(p['name'])
        brand_id = slugify(brand_name) if brand_name else ''
        if brand_id and brand_id not in brands:
            brands[brand_id] = {'id': brand_id, 'slug': brand_id, 'name': brand_name}

        name = tidy_name(p['name'])
        slug = slugify(name) or f"product-{p['id']}"
        if slug in used_slugs:
            slug = f"{slug}-{p['id']}"
        used_slugs.add(slug)

        specs = p.get('specs') or {}
        spec_bits = [f'{k}: {v}' for k, v in list(specs.items())[:2]]
        summary = ' · '.join(spec_bits) if spec_bits else f'{sub_name} — available on quotation.'
        by = f' by {brand_name}' if brand_name and brand_name.lower() not in name.lower() else ''
        description = (
            f'{name}{by}, supplied by Biozen K Limited for clinics, hospitals and home care. '
            f'Request a quotation and our team will confirm the exact model, specifications, lead time '
            f'and delivery{", installation and user training" if top in INSTALL_TOPS else ""} for your needs.'
        )

        image = next((img for pat, img in ILLUSTRATIONS if re.search(pat, sub_name + ' ' + name, re.I)), None)

        products.append({
            'id': f"m{p['id']}",
            'slug': slug,
            'name': name,
            'summary': summary[:160],
            'description': description,
            'category': sub_id,
            'brand': brand_id,
            'sku': f"BZ-{p['id']}",
            'price': 0,
            'quote_only': True,
            'stock': 'on_order',
            'warranty_months': 0,
            'installation_available': top in INSTALL_TOPS,
            'specs': specs,
            'in_the_box': [],
            'images': [f'/images/products/{image}.svg'] if image else [],
            'manuals': [],
            'featured': False,
            'created': '2026-11-17T00:00:00.000Z',
        })

    # Sort subcategories by product count within each top, biggest first.
    counts = Counter(p['category'] for p in products)
    sub_list = sorted(subs.values(), key=lambda s: (s['parent'], -counts[s['id']], s['name']))
    for i, s in enumerate(sub_list):
        s['sort'] = i + 1

    # Feature up to 8 products: one per top, preferring ones with specs and an illustration.
    featured, seen = 0, set()
    for p in sorted(products, key=lambda p: (not p['images'], bool(re.search(r'battery|spare|mortuary|accessor|cable|filter', p['name'], re.I)), -len(p['specs']))):
        top = p['category'].split('--')[0]
        if top in seen:
            continue
        p['featured'] = True
        seen.add(top)
        featured += 1
        if featured == 8:
            break

    data = {'categories': categories + sub_list, 'brands': sorted(brands.values(), key=lambda b: b['name']), 'products': products}
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
    print(f"skipped {skipped} consumables")
    print(f"{len(products)} products, {len(sub_list)} subcategories, {len(brands)} brands, "
          f"{sum(1 for p in products if p['specs'])} with specs, {sum(1 for p in products if p['images'])} illustrated")
    for slug, name in tops.items():
        print(f"  {name}: {sum(1 for p in products if p['category'].startswith(slug + '--'))}")


if __name__ == '__main__':
    main()
