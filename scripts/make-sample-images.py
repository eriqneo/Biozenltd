"""Generates placeholder product illustrations (SVG) for the sample catalogue.
Delete public/images/products/*.svg once real supplier photos are uploaded."""
import os

OUT = os.path.join(os.path.dirname(__file__), '..', 'public', 'images', 'products')
S = '#475569'   # stroke
B = '#e2e8f0'   # body
W = '#ffffff'
A = '#2563eb'   # brand accent
D = '#0f172a'   # screen
G = '#22c55e'   # trace

def frame(inner):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300">
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#eff6ff"/><stop offset="1" stop-color="#e2e8f0"/></linearGradient></defs>
<rect width="400" height="300" fill="url(#bg)"/>
<ellipse cx="200" cy="262" rx="130" ry="10" fill="#94a3b8" opacity=".25"/>
<g stroke="{S}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round">{inner}</g>
</svg>'''

ecg = f'<polyline fill="none" stroke="{G}" stroke-width="3" points="{{pts}}"/>'
def trace(x, y, w):
    p = []
    seg = w / 4
    for i in range(4):
        x0 = x + i * seg
        p += [(x0, y), (x0 + seg*.35, y), (x0 + seg*.45, y-18), (x0 + seg*.55, y+12), (x0 + seg*.62, y), (x0+seg, y)]
    return ecg.format(pts=' '.join(f'{a:.0f},{b:.0f}' for a, b in p))

def wheel(cx, cy, r, fill=D):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>'

img = {}

img['multiparameter-patient-monitor-12-inch'] = f'''
<rect x="90" y="60" width="220" height="160" rx="14" fill="{B}"/>
<rect x="105" y="74" width="150" height="110" rx="6" fill="{D}"/>
{trace(112, 108, 136)}
<polyline fill="none" stroke="#38bdf8" stroke-width="3" points="112,150 130,140 148,155 166,138 184,152 202,140 220,150 248,144"/>
<rect x="265" y="80" width="32" height="14" rx="3" fill="{A}" stroke="none"/>
<rect x="265" y="102" width="32" height="14" rx="3" fill="{W}"/>
<rect x="265" y="124" width="32" height="14" rx="3" fill="{W}"/>
<circle cx="281" cy="166" r="12" fill="{W}"/>
<rect x="150" y="220" width="100" height="14" rx="4" fill="{B}"/>
<rect x="130" y="234" width="140" height="22" rx="6" fill="{B}"/>'''

img['12-channel-ecg-machine'] = f'''
<rect x="80" y="110" width="240" height="130" rx="16" fill="{B}"/>
<rect x="100" y="126" width="110" height="70" rx="6" fill="{D}"/>
{trace(106, 160, 98)}
<g fill="{W}"><rect x="225" y="130" width="22" height="14" rx="3"/><rect x="253" y="130" width="22" height="14" rx="3"/><rect x="281" y="130" width="22" height="14" rx="3"/>
<rect x="225" y="152" width="22" height="14" rx="3"/><rect x="253" y="152" width="22" height="14" rx="3"/><rect x="281" y="152" width="22" height="14" rx="3"/></g>
<rect x="225" y="176" width="78" height="20" rx="5" fill="{A}" stroke="none"/>
<path d="M130 110 L130 60 L270 60 L270 110" fill="{W}"/>
<polyline fill="none" stroke="#ef4444" stroke-width="2.5" points="140,85 160,85 166,70 172,96 178,85 200,85 206,72 212,96 218,85 240,85 246,70 252,96 258,85 262,85"/>
<path d="M100 240 q-30 10 -40 -20" fill="none"/>'''

img['automated-external-defibrillator-aed'] = f'''
<rect x="110" y="60" width="180" height="190" rx="28" fill="#facc15"/>
<rect x="135" y="85" width="130" height="100" rx="14" fill="{W}"/>
<path d="M200 105 c-14 -16 -40 -4 -30 16 l30 28 l30 -28 c10 -20 -16 -32 -30 -16z" fill="#ef4444"/>
<polyline fill="none" stroke="{W}" stroke-width="4" points="182,125 194,125 200,114 206,136 212,125 220,125"/>
<circle cx="170" cy="215" r="16" fill="{A}"/>
<circle cx="230" cy="215" r="16" fill="#ef4444"/>
<text x="200" y="180" text-anchor="middle" font-family="sans-serif" font-size="16" font-weight="700" fill="{S}" stroke="none">AED</text>'''

img['syringe-infusion-pump'] = f'''
<rect x="70" y="100" width="260" height="120" rx="16" fill="{B}"/>
<rect x="90" y="118" width="150" height="34" rx="6" fill="{W}"/>
<rect x="100" y="126" width="110" height="18" rx="3" fill="#bfdbfe"/>
<rect x="210" y="122" width="40" height="26" rx="3" fill="{W}"/>
<line x1="250" y1="135" x2="300" y2="135"/>
<rect x="90" y="166" width="70" height="36" rx="6" fill="{D}"/>
<text x="125" y="190" text-anchor="middle" font-family="monospace" font-size="16" fill="{G}" stroke="none">5.0</text>
<g fill="{W}"><circle cx="190" cy="184" r="10"/><circle cx="220" cy="184" r="10"/></g>
<circle cx="275" cy="184" r="16" fill="{A}"/>'''

img['digital-blood-pressure-monitor-upper-arm'] = f'''
<rect x="200" y="80" width="130" height="150" rx="22" fill="{W}"/>
<rect x="218" y="98" width="94" height="70" rx="8" fill="#dbeafe"/>
<text x="265" y="132" text-anchor="middle" font-family="monospace" font-size="22" font-weight="700" fill="{D}" stroke="none">120</text>
<text x="265" y="158" text-anchor="middle" font-family="monospace" font-size="18" fill="{D}" stroke="none">80</text>
<circle cx="265" cy="198" r="16" fill="{A}"/>
<path d="M200 190 C150 200 140 150 110 160" fill="none" stroke-width="4"/>
<rect x="60" y="120" width="80" height="100" rx="14" fill="#93c5fd"/>
<line x1="70" y1="140" x2="130" y2="140" stroke-dasharray="4 6"/>'''

img['oxygen-concentrator-5l'] = f'''
<rect x="130" y="50" width="140" height="200" rx="24" fill="{W}"/>
<rect x="150" y="70" width="100" height="40" rx="8" fill="{D}"/>
<text x="200" y="97" text-anchor="middle" font-family="monospace" font-size="18" fill="{G}" stroke="none">93%</text>
<rect x="150" y="122" width="40" height="56" rx="8" fill="#bfdbfe"/>
<line x1="170" y1="132" x2="170" y2="170" stroke="{A}" stroke-width="4"/>
<g fill="{B}"><rect x="205" y="122" width="45" height="8" rx="3"/><rect x="205" y="138" width="45" height="8" rx="3"/><rect x="205" y="154" width="45" height="8" rx="3"/><rect x="205" y="170" width="45" height="8" rx="3"/></g>
<rect x="160" y="196" width="80" height="34" rx="8" fill="#dbeafe"/>
{wheel(152, 254, 8)}{wheel(248, 254, 8)}
<path d="M270 120 C320 120 330 200 300 230" fill="none" stroke="#38bdf8"/>'''

img['compressor-nebulizer'] = f'''
<rect x="70" y="140" width="190" height="100" rx="30" fill="{W}"/>
<g fill="{B}"><rect x="95" y="165" width="70" height="8" rx="3"/><rect x="95" y="181" width="70" height="8" rx="3"/><rect x="95" y="197" width="70" height="8" rx="3"/></g>
<circle cx="215" cy="190" r="18" fill="{A}"/>
<path d="M260 180 C300 170 290 120 300 100" fill="none" stroke="#38bdf8" stroke-width="4"/>
<rect x="285" y="60" width="30" height="44" rx="8" fill="#bfdbfe"/>
<path d="M300 60 q-30 -20 -10 -40 M300 60 q10 -25 30 -30" fill="none" stroke="#94a3b8" stroke-dasharray="3 6"/>'''

bed_base = lambda extra='': f'''
<rect x="70" y="150" width="260" height="22" rx="8" fill="{B}"/>
<rect x="80" y="132" width="240" height="20" rx="8" fill="#bfdbfe"/>
<rect x="60" y="100" width="16" height="110" rx="5" fill="{W}"/>
<rect x="324" y="115" width="16" height="95" rx="5" fill="{W}"/>
<line x1="110" y1="172" x2="110" y2="235"/><line x1="290" y1="172" x2="290" y2="235"/>
{wheel(110, 245, 10)}{wheel(290, 245, 10)}{extra}'''

img['electric-icu-bed-five-function'] = bed_base(f'''
<path d="M86 132 L130 92 L150 102 L120 132z" fill="#93c5fd"/>
<rect x="160" y="112" width="120" height="10" rx="4" fill="{W}"/>
<line x1="170" y1="112" x2="170" y2="132"/><line x1="270" y1="112" x2="270" y2="132"/>
<rect x="200" y="182" width="44" height="26" rx="5" fill="{A}"/>
<line x1="222" y1="172" x2="222" y2="182"/>''')

img['manual-hospital-bed-two-crank'] = bed_base(f'''
<path d="M86 132 L120 104 L140 112 L116 132z" fill="#93c5fd"/>
<circle cx="350" cy="195" r="10" fill="{W}"/><line x1="340" y1="190" x2="350" y2="195"/>
<line x1="350" y1="195" x2="362" y2="200"/>''')

img['emergency-stretcher-trolley'] = f'''
<rect x="60" y="120" width="280" height="18" rx="9" fill="#93c5fd"/>
<rect x="70" y="138" width="260" height="14" rx="5" fill="{B}"/>
<path d="M70 120 L110 90 L125 98 L95 120z" fill="#bfdbfe"/>
<line x1="90" y1="110" x2="320" y2="110" stroke="{A}"/>
<line x1="150" y1="152" x2="250" y2="225"/><line x1="250" y1="152" x2="150" y2="225"/>
<rect x="130" y="225" width="140" height="10" rx="4" fill="{B}"/>
{wheel(140, 248, 10)}{wheel(260, 248, 10)}'''

img['stainless-steel-iv-stand'] = f'''
<line x1="200" y1="55" x2="200" y2="235" stroke-width="6"/>
<path d="M170 55 q-12 0 -12 12 M230 55 q12 0 12 12 M185 55 q-6 0 -6 10 M215 55 q6 0 6 10" fill="none"/>
<line x1="165" y1="55" x2="235" y2="55" stroke-width="5"/>
<rect x="232" y="70" width="40" height="60" rx="10" fill="#dbeafe"/>
<line x1="252" y1="130" x2="252" y2="170" stroke="#38bdf8"/>
<line x1="200" y1="235" x2="140" y2="250"/><line x1="200" y1="235" x2="260" y2="250"/><line x1="200" y1="235" x2="200" y2="255"/>
{wheel(140, 252, 7)}{wheel(260, 252, 7)}{wheel(200, 257, 7)}'''

img['wall-mounted-diagnostic-set'] = f'''
<rect x="110" y="60" width="180" height="70" rx="14" fill="{W}"/>
<rect x="130" y="76" width="60" height="38" rx="6" fill="{B}"/><rect x="210" y="76" width="60" height="38" rx="6" fill="{B}"/>
<rect x="150" y="96" width="20" height="90" rx="8" fill="{D}"/><rect x="230" y="96" width="20" height="90" rx="8" fill="{D}"/>
<path d="M150 96 l-6 -26 h32 l-6 26z" fill="{A}"/>
<circle cx="240" cy="78" r="16" fill="{A}"/><circle cx="240" cy="78" r="6" fill="{W}"/>
<path d="M160 186 C160 230 240 230 240 186" fill="none" stroke-dasharray="2 6"/>'''

img['digital-baby-weighing-scale'] = f'''
<rect x="80" y="180" width="240" height="56" rx="14" fill="{W}"/>
<rect x="160" y="196" width="80" height="26" rx="5" fill="{D}"/>
<text x="200" y="215" text-anchor="middle" font-family="monospace" font-size="16" fill="{G}" stroke="none">3.45</text>
<path d="M70 150 C90 190 310 190 330 150 L310 140 C290 170 110 170 90 140z" fill="#bfdbfe"/>
<line x1="200" y1="170" x2="200" y2="180"/>'''

img['infant-radiant-warmer'] = f'''
<line x1="120" y1="230" x2="120" y2="60" stroke-width="7"/>
<rect x="110" y="48" width="170" height="34" rx="10" fill="{W}"/>
<rect x="125" y="78" width="140" height="10" rx="4" fill="#f97316" stroke="none"/>
<path d="M150 98 v30 M195 98 v30 M240 98 v30" stroke="#fdba74" stroke-dasharray="4 6"/>
<rect x="140" y="150" width="160" height="40" rx="8" fill="#bfdbfe"/>
<rect x="150" y="140" width="140" height="14" rx="6" fill="{W}"/>
<rect x="130" y="190" width="180" height="40" rx="8" fill="{B}"/>
<rect x="135" y="110" width="40" height="26" rx="5" fill="{D}"/>
{wheel(140, 245, 9)}{wheel(300, 245, 9)}'''

img['pocket-fetal-doppler'] = f'''
<rect x="110" y="70" width="110" height="170" rx="24" fill="{W}"/>
<rect x="128" y="92" width="74" height="50" rx="8" fill="{D}"/>
<text x="165" y="124" text-anchor="middle" font-family="monospace" font-size="20" fill="{G}" stroke="none">142</text>
<circle cx="165" cy="190" r="18" fill="{A}"/>
<path d="M220 160 C260 160 250 220 280 220" fill="none"/>
<rect x="270" y="196" width="44" height="54" rx="20" fill="#bfdbfe"/>
<path d="M290 120 q14 14 0 28 M302 112 q24 22 0 44" fill="none" stroke="#ef4444"/>'''

img['tabletop-autoclave-23l'] = f'''
<rect x="60" y="80" width="280" height="160" rx="18" fill="{W}"/>
<circle cx="160" cy="160" r="58" fill="{B}"/>
<circle cx="160" cy="160" r="40" fill="#cbd5e1"/>
<rect x="232" y="100" width="88" height="40" rx="6" fill="{D}"/>
<text x="276" y="126" text-anchor="middle" font-family="monospace" font-size="16" fill="{G}" stroke="none">134°C</text>
<g fill="{A}" stroke="none"><circle cx="248" cy="165" r="9"/><circle cx="276" cy="165" r="9"/><circle cx="304" cy="165" r="9"/></g>
<rect x="232" y="190" width="88" height="30" rx="6" fill="{B}"/>'''

img['benchtop-centrifuge-6000rpm'] = f'''
<path d="M80 150 C80 110 320 110 320 150 L320 225 Q320 240 305 240 L95 240 Q80 240 80 225z" fill="{W}"/>
<ellipse cx="200" cy="150" rx="110" ry="30" fill="#bfdbfe"/>
<ellipse cx="200" cy="150" rx="40" ry="10" fill="{B}"/>
<rect x="120" y="190" width="70" height="30" rx="5" fill="{D}"/>
<text x="155" y="211" text-anchor="middle" font-family="monospace" font-size="15" fill="{G}" stroke="none">6000</text>
<circle cx="250" cy="205" r="14" fill="{A}"/><circle cx="285" cy="205" r="10" fill="{B}"/>'''

img['binocular-led-microscope'] = f'''
<rect x="120" y="225" width="170" height="22" rx="8" fill="{W}"/>
<path d="M250 225 C270 160 250 110 210 90" fill="none" stroke-width="18" stroke="{B}"/>
<path d="M250 225 C270 160 250 110 210 90" fill="none"/>
<rect x="170" y="70" width="70" height="40" rx="10" fill="{W}"/>
<line x1="180" y1="70" x2="160" y2="40" stroke-width="10" stroke="{D}"/><line x1="200" y1="70" x2="190" y2="38" stroke-width="10" stroke="{D}"/>
<rect x="180" y="110" width="30" height="40" rx="5" fill="{A}"/>
<rect x="140" y="160" width="110" height="10" rx="3" fill="{B}"/>
<circle cx="195" cy="200" r="10" fill="#fde047"/>'''

img['foldable-manual-wheelchair'] = f'''
<circle cx="170" cy="190" r="58" fill="none" stroke-width="6"/>
<circle cx="170" cy="190" r="46" fill="none" stroke="#94a3b8"/>
<circle cx="170" cy="190" r="6" fill="{D}"/>
<path d="M140 80 L150 160 L250 160 L260 210" fill="none" stroke-width="5"/>
<path d="M150 160 L148 110 L230 110" fill="none" stroke-width="5"/>
<rect x="152" y="140" width="96" height="16" rx="5" fill="{A}"/>
<rect x="138" y="88" width="16" height="60" rx="5" fill="{A}"/>
<line x1="140" y1="80" x2="120" y2="78" stroke-width="5"/>
{wheel(270, 240, 10)}
<line x1="250" y1="210" x2="290" y2="215" stroke-width="5"/>'''

img['aluminium-walking-frame'] = f'''
<path d="M130 250 L150 80 L250 80 L270 250" fill="none" stroke-width="7"/>
<path d="M150 80 L160 250 M250 80 L240 250" fill="none" stroke-width="5" stroke="#94a3b8"/>
<rect x="140" y="72" width="30" height="20" rx="6" fill="{A}"/><rect x="230" y="72" width="30" height="20" rx="6" fill="{A}"/>
<line x1="145" y1="160" x2="255" y2="160" stroke-width="5"/>
<g fill="{D}"><rect x="122" y="246" width="18" height="10" rx="4"/><rect x="262" y="246" width="18" height="10" rx="4"/></g>'''

img['adult-cpr-training-manikin'] = f'''
<ellipse cx="110" cy="170" rx="40" ry="44" fill="#fde2c8"/>
<path d="M95 165 h10 M118 165 h10 M100 190 q12 8 24 0" fill="none"/>
<path d="M150 130 L330 130 Q345 130 345 145 L345 215 Q345 230 330 230 L150 230 Q140 210 140 180 Q140 150 150 130z" fill="#fde2c8"/>
<rect x="210" y="150" width="70" height="60" rx="10" fill="{A}" opacity=".85"/>
<g fill="{W}" stroke="none"><rect x="238" y="158" width="14" height="44" rx="3"/><rect x="223" y="173" width="44" height="14" rx="3"/></g>
<rect x="150" y="234" width="200" height="14" rx="6" fill="{B}"/>'''

os.makedirs(OUT, exist_ok=True)
for slug, inner in img.items():
    with open(os.path.join(OUT, f'{slug}.svg'), 'w') as f:
        f.write(frame(inner))
print(len(img), 'images written')
