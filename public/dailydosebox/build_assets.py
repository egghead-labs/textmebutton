#!/usr/bin/env python3
"""DailyDoseBox brand assets: QR card + QR composited on the real box lid."""
import numpy as np, segno
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BOX_ID = "maple.river.otter"
URL    = f"https://dailydosebox.com/setup?box={BOX_ID}"
NAVY=(14,42,59); TEAL=(20,184,166); CORAL=(255,107,94); PAPER=(255,255,255); MUTED=(91,113,128)
NAVY_H="#0E2A3B"

def font(sz, bold=True):
    p="/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf"
    return ImageFont.truetype(p, sz)

# ---------- QR card (marketing) ----------
qr = segno.make(URL, error="h")
qr.save("assets/_qr_tmp.png", scale=16, border=2, dark=NAVY_H, light="#FFFFFF")
qrimg = Image.open("assets/_qr_tmp.png").convert("RGBA")

CARD_W=760; n_modules=len(qr.matrix)
matrix=[list(r) for r in qr.matrix]; n=len(matrix); MOD=13; QR_PX=n*MOD
qr_x=(CARD_W-QR_PX)/2; qr_y=250; qr_bottom=qr_y+QR_PX
cta_y=qr_bottom+56; cta_h=74; sub_y=cta_y+cta_h+46; boxid_y=sub_y+58; url_y=boxid_y+32
CARD_H=int(url_y+44)
def rects(ox,oy):
    return "".join(f'<rect x="{ox+c*MOD:.1f}" y="{oy+r*MOD:.1f}" width="{MOD}" height="{MOD}"/>'
                   for r,row in enumerate(matrix) for c,v in enumerate(row) if v)
svg=f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{CARD_W}" height="{CARD_H}" viewBox="0 0 {CARD_W} {CARD_H}" font-family="Inter, Helvetica, Arial, sans-serif">
  <defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#F2F7F8"/></linearGradient></defs>
  <rect x="8" y="8" width="{CARD_W-16}" height="{CARD_H-16}" rx="34" fill="url(#bg)" stroke="{NAVY_H}" stroke-width="3"/>
  <text x="{CARD_W/2}" y="150" text-anchor="middle" font-size="58" fill="{NAVY_H}" font-weight="800">DailyDoseBox</text>
  <text x="{CARD_W/2}" y="196" text-anchor="middle" font-size="27" fill="#5B7180">The pill box that texts you back.</text>
  <rect x="{qr_x-22:.0f}" y="{qr_y-22}" width="{QR_PX+44:.0f}" height="{QR_PX+44:.0f}" rx="22" fill="#FFFFFF" stroke="#14B8A6" stroke-width="4"/>
  <g fill="{NAVY_H}">{rects(qr_x,qr_y)}</g>
  <rect x="{CARD_W/2-205:.0f}" y="{cta_y:.0f}" width="410" height="{cta_h}" rx="37" fill="#FF6B5E"/>
  <text x="{CARD_W/2}" y="{cta_y+49:.0f}" text-anchor="middle" font-size="30" fill="#FFFFFF" font-weight="700">Scan to set up this box</text>
  <text x="{CARD_W/2}" y="{sub_y:.0f}" text-anchor="middle" font-size="22" fill="#5B7180">Choose the dose window. Pick who gets the alert.</text>
  <text x="{CARD_W/2}" y="{boxid_y:.0f}" text-anchor="middle" font-size="22" fill="{NAVY_H}" font-weight="700" letter-spacing="2">BOX {BOX_ID}</text>
  <text x="{CARD_W/2}" y="{url_y:.0f}" text-anchor="middle" font-size="19" fill="#5B7180">{URL}</text>
</svg>'''
open("assets/qr-card.svg","w").write(svg)
import cairosvg
cairosvg.svg2png(url="assets/qr-card.svg", write_to="assets/qr-card.png", scale=2)
print("qr card done")

# ---------- composite on real lid ----------
base=Image.open("assets/box-real.jpg").convert("RGBA"); W,H=base.size
pad=60; qsize=780; cw=ch=qsize+2*pad
label=Image.new("RGBA",(cw,ch),(0,0,0,0)); d=ImageDraw.Draw(label)
d.rounded_rectangle([0,0,cw-1,ch-1],radius=40,fill=PAPER+(255,),outline=TEAL+(255,),width=7)
label.alpha_composite(qrimg.resize((qsize,qsize)),(pad,pad))
dst_frac=[(0.3255,0.2930),(0.7135,0.3145),(0.6927,0.5000),(0.3073,0.4668)]
dst=[(fx*W,fy*H) for fx,fy in dst_frac]
def coeffs(pa,pb):
    m=[]
    for (x,y),(u,v) in zip(pa,pb):
        m.append([x,y,1,0,0,0,-u*x,-u*y]); m.append([0,0,0,x,y,1,-v*x,-v*y])
    return np.linalg.solve(np.array(m,float), np.array(pb,float).reshape(8))
src=[(0,0),(cw,0),(cw,ch),(0,ch)]
warp=label.transform((W,H),Image.PERSPECTIVE,coeffs(dst,src),resample=Image.BICUBIC)
sh=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(sh).polygon([(x+6,y+10) for x,y in dst],fill=(0,0,0,90))
sh=sh.filter(ImageFilter.GaussianBlur(9))
out=base.copy(); out.alpha_composite(sh); out.alpha_composite(warp)
out.convert("RGB").save("assets/box-qr-composite.jpg",quality=92)
import os; os.remove("assets/_qr_tmp.png")
print("composite done", W, H)
