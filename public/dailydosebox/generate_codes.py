#!/usr/bin/env python3
"""
DailyDoseBox 3-word box-code batch generator.
Mints N unique what3words-style codes, writes a CSV (code + setup URL) and a
print sheet PDF (8 cut-out QR cards per Letter page) for provisioning boxes.

  python3 generate_codes.py [N]      (default 8)

Note: production should use a curated 2048-word list (per HARDWARE-SPEC.md);
this ships a ~140-word clean starter list, enough for batches and demos.
"""
import sys, csv, random
import segno, cairosvg

BASE = "dailydosebox.com/demo"
N = int(sys.argv[1]) if len(sys.argv) > 1 else 8
random.seed(7)  # reproducible batches

WORDS = """maple river otter cedar harbor lantern willow pebble meadow cobalt
amber spruce falcon copper marble ember pine cove ridge dune brook
ivory slate basil olive coral aspen birch heron quartz cliff fern
glade haven indigo jade kelp larch moss nectar opal poppy quince
reef sage teal umber vine wren yarrow zephyr acorn beacon clover
delta echo flint grove hazel iris juniper kettle lily mango nimbus
oak petal raven sienna tide violet walnut comet drift onyx pearl
robin saffron thistle tulip velvet wheat anchor breeze cliffs daisy
elm forest garnet hollow inlet linen marsh north orchard pond
ripple shore timber valley willowy alder bramble cypress dewdrop
fennel ginger heather lupine mint nutmeg parsley rowan sorrel
clay frost gust lake mesa pier reed sand stone wave
""".split()
WORDS = sorted(set(WORDS))

# mint N unique 3-word codes
codes, seen = [], set()
while len(codes) < N:
    trio = ".".join(random.sample(WORDS, 3))
    if trio not in seen:
        seen.add(trio); codes.append(trio)

# CSV
with open("codes.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["three_words", "setup_url"])
    for c in codes:
        w.writerow([c, f"https://{BASE}/{c}"])

# print sheet (8 cards per Letter page; first 8 codes)
PW, PH = 612, 792
NAVY="#0E2A3B"; TEAL="#14B8A6"; MUTED="#5B7180"
COLS, ROWS = 2, 4
MX, MY = 44, 54
CW = (PW - 2*MX) / COLS
CH = (PH - 2*MY) / ROWS
QR = 92

def card(cx, cy, code):
    qr = segno.make(f"https://{BASE}/{code}", error="h")
    m = [list(r) for r in qr.matrix]; n = len(m); mod = QR/n
    qx = cx + (CW-QR)/2; qy = cy + 22
    rects = "".join(f'<rect x="{qx+c*mod:.2f}" y="{qy+r*mod:.2f}" width="{mod:.2f}" height="{mod:.2f}"/>'
                    for r,row in enumerate(m) for c,v in enumerate(row) if v)
    w1,w2,w3 = code.split(".")
    words = (f'<tspan fill="{NAVY}">{w1}</tspan><tspan fill="{TEAL}">.</tspan>'
             f'<tspan fill="{NAVY}">{w2}</tspan><tspan fill="{TEAL}">.</tspan>'
             f'<tspan fill="{NAVY}">{w3}</tspan>')
    ty = qy + QR + 22
    return (f'<rect x="{cx+8}" y="{cy+6}" width="{CW-16}" height="{CH-12}" rx="12" fill="#fff" '
            f'stroke="{NAVY}" stroke-width="1" stroke-dasharray="4 3"/>'
            f'<text x="{cx+CW/2}" y="{cy+18}" text-anchor="middle" font-size="8" fill="{TEAL}" '
            f'font-weight="700" letter-spacing="2">SCAN TO SET UP</text>'
            f'<g fill="{NAVY}">{rects}</g>'
            f'<text x="{cx+CW/2}" y="{ty}" text-anchor="middle" font-size="13" font-weight="800">{words}</text>')

cards = "".join(card(MX + col*CW, MY + row*CH, codes[i])
                for i in range(min(8, len(codes)))
                for col,row in [(i % COLS, i // COLS)])
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{PW}" height="{PH}" '
       f'viewBox="0 0 {PW} {PH}" font-family="Helvetica, Arial, sans-serif">'
       f'<rect width="{PW}" height="{PH}" fill="#fff"/>'
       f'<text x="{PW/2}" y="32" text-anchor="middle" font-size="12" fill="{MUTED}">'
       f'DailyDoseBox box codes — print at 100%, cut apart, one card per box lid.</text>'
       f'{cards}</svg>')
cairosvg.svg2pdf(bytestring=svg.encode("utf-8"), write_to="DailyDoseBox-Box-Codes-Sheet.pdf")

print(f"minted {N} codes -> codes.csv ; print sheet (first 8) -> DailyDoseBox-Box-Codes-Sheet.pdf")
for c in codes: print("  ", c)
