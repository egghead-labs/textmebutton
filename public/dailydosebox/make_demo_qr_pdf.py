#!/usr/bin/env python3
"""
DailyDoseBox — box demo QR label (print & tape).
QR encodes the box's what3words-style setup URL. The three words are also
printed big so anyone can scan OR type them at dailydosebox.com/demo.

  DailyDoseBox-Box-QR.pdf
"""
import cairosvg, segno

WORDS  = "maple.river.otter"                 # the box's 3-word code (the ?box= value)
URL    = f"https://dailydosebox.com/setup?box={WORDS}"

PW, PH = 612, 792
NAVY="#0E2A3B"; TEAL="#14B8A6"; CORAL="#FF6B5E"; MUTED="#5B7180"

qr = segno.make(URL, error="h")
m = [list(r) for r in qr.matrix]; n = len(m)
QR_PT = 2.0*72; MOD = QR_PT/n
CARD_W = 408
card_x = (PW-CARD_W)/2
card_y = 140
cx = PW/2
qx = (PW-QR_PT)/2                 # QR centered on the page
qy = card_y + 86
rects = "".join(f'<rect x="{qx+c*MOD:.2f}" y="{qy+r*MOD:.2f}" width="{MOD:.2f}" height="{MOD:.2f}"/>'
                for r,row in enumerate(m) for c,v in enumerate(row) if v)

w1,w2,w3 = WORDS.split(".")
words_svg = (f'<tspan fill="{NAVY}">{w1}</tspan><tspan fill="{TEAL}">.</tspan>'
             f'<tspan fill="{NAVY}">{w2}</tspan><tspan fill="{TEAL}">.</tspan>'
             f'<tspan fill="{NAVY}">{w3}</tspan>')

or_y   = qy + QR_PT + 28
lbl_y  = or_y + 34
word_y = lbl_y + 34
url_y  = word_y + 32
CARD_H = (url_y + 26) - card_y

svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{PW}" height="{PH}" viewBox="0 0 {PW} {PH}" font-family="Helvetica, Arial, sans-serif">
  <rect width="{PW}" height="{PH}" fill="#FFFFFF"/>
  <text x="{cx}" y="98" text-anchor="middle" font-size="12" fill="{MUTED}">Print at 100% (Actual Size). Cut on the dashed line and tape to the box lid.</text>

  <rect x="{card_x}" y="{card_y}" width="{CARD_W}" height="{CARD_H}" rx="18" fill="#FFFFFF" stroke="{NAVY}" stroke-width="1.2" stroke-dasharray="5 4"/>

  <text x="{cx}" y="{card_y+34}" text-anchor="middle" font-size="13" fill="{TEAL}" font-weight="700" letter-spacing="3">DAILYDOSEBOX</text>
  <text x="{cx}" y="{card_y+62}" text-anchor="middle" font-size="20" fill="{NAVY}" font-weight="800">SCAN TO SET UP YOUR BOX</text>

  <g fill="{NAVY}">{rects}</g>

  <line x1="{card_x+50}" y1="{or_y-4}" x2="{cx-24}" y2="{or_y-4}" stroke="#E0E8EB" stroke-width="1.4"/>
  <text x="{cx}" y="{or_y}" text-anchor="middle" font-size="12" fill="{MUTED}" font-weight="700">OR</text>
  <line x1="{cx+24}" y1="{or_y-4}" x2="{card_x+CARD_W-50}" y2="{or_y-4}" stroke="#E0E8EB" stroke-width="1.4"/>

  <text x="{cx}" y="{lbl_y}" text-anchor="middle" font-size="12" fill="{MUTED}" letter-spacing="1">YOUR BOX SETUP CODE</text>
  <text x="{cx}" y="{word_y}" text-anchor="middle" font-size="26" font-weight="800" letter-spacing="0.5">{words_svg}</text>
  <text x="{cx}" y="{url_y}" text-anchor="middle" font-size="12.5" fill="{MUTED}">Go to dailydosebox.com/setup and type your three words.</text>
</svg>'''

cairosvg.svg2pdf(bytestring=svg.encode("utf-8"), write_to="DailyDoseBox-Box-QR.pdf")
print("wrote DailyDoseBox-Box-QR.pdf  ·  QR ->", URL)
