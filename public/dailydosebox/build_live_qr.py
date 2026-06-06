#!/usr/bin/env python3
"""Live setup QR -> the working demo setup flow on Cloudflare Pages.
Outputs a standalone PNG + a print card PDF."""
import segno, cairosvg

WORDS = "maple.river.otter"
URL   = f"https://dailydosebox.pages.dev/setup?box={WORDS}"   # LIVE, working setup
NAVY="#0E2A3B"; TEAL="#14B8A6"; MUTED="#5B7180"

# standalone PNG
segno.make(URL, error="h").save("assets/setup-qr-live.png", scale=14, border=3,
                                dark=NAVY, light="#FFFFFF")

# print card PDF
qr = segno.make(URL, error="h"); m=[list(r) for r in qr.matrix]; n=len(m)
PW,PH=612,792; QRPT=2.1*72; MOD=QRPT/n
cx=PW/2; qx=(PW-QRPT)/2; cy=150; qy=cy+86
rects="".join(f'<rect x="{qx+c*MOD:.2f}" y="{qy+r*MOD:.2f}" width="{MOD:.2f}" height="{MOD:.2f}"/>'
              for r,row in enumerate(m) for c,v in enumerate(row) if v)
w1,w2,w3=WORDS.split(".")
words=(f'<tspan fill="{NAVY}">{w1}</tspan><tspan fill="{TEAL}">.</tspan>'
       f'<tspan fill="{NAVY}">{w2}</tspan><tspan fill="{TEAL}">.</tspan>'
       f'<tspan fill="{NAVY}">{w3}</tspan>')
wy=qy+QRPT+58; uy=wy+30; CARD_W=420; cardx=(PW-CARD_W)/2; CARD_H=(uy+26)-cy
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{PW}" height="{PH}" viewBox="0 0 {PW} {PH}" font-family="Helvetica, Arial, sans-serif">
<rect width="{PW}" height="{PH}" fill="#FFFFFF"/>
<text x="{cx}" y="100" text-anchor="middle" font-size="12" fill="{MUTED}">Scan to open the live DailyDoseBox setup. Works now.</text>
<rect x="{cardx}" y="{cy}" width="{CARD_W}" height="{CARD_H}" rx="18" fill="#FFFFFF" stroke="{NAVY}" stroke-width="1.2" stroke-dasharray="5 4"/>
<text x="{cx}" y="{cy+34}" text-anchor="middle" font-size="13" fill="{TEAL}" font-weight="700" letter-spacing="3">DAILYDOSEBOX</text>
<text x="{cx}" y="{cy+62}" text-anchor="middle" font-size="20" fill="{NAVY}" font-weight="800">SCAN TO SET UP YOUR BOX</text>
<g fill="{NAVY}">{rects}</g>
<text x="{cx}" y="{wy}" text-anchor="middle" font-size="26" font-weight="800">{words}</text>
<text x="{cx}" y="{uy}" text-anchor="middle" font-size="11" fill="{MUTED}">dailydosebox.pages.dev/setup?box={WORDS}</text>
</svg>'''
cairosvg.svg2pdf(bytestring=svg.encode("utf-8"), write_to="DailyDoseBox-Setup-QR-live.pdf")
print("wrote assets/setup-qr-live.png + DailyDoseBox-Setup-QR-live.pdf ->", URL)
