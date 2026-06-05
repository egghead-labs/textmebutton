#!/usr/bin/env python3
"""DailyDoseBox ad creatives (Maya): 1:1 feed + 9:16 story, from the real box."""
from PIL import Image, ImageDraw, ImageFont
SRC="assets/box-qr-composite.jpg"
NAVY=(14,42,59); TEAL=(20,184,166); CORAL=(255,107,94); PAPER=(255,255,255); MUTED=(200,214,220)
def font(sz,bold=True):
    p="/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf"
    return ImageFont.truetype(p,sz)
def vgrad(size,ta,ba,color=(8,24,33)):
    w,h=size; g=Image.new("L",(1,h))
    for y in range(h): g.putpixel((0,y),int(ta+(ba-ta)*(y/(h-1))))
    g=g.resize((w,h)); ov=Image.new("RGBA",(w,h),color+(0,)); ov.putalpha(g); return ov
base=Image.open(SRC).convert("RGB"); W,H=base.size
def crop(box,sz): return base.crop(box).resize(sz,Image.LANCZOS).convert("RGBA")
# 1:1
S=1200; sq=crop((250,700,2950,3400),(S,S))
sq.alpha_composite(vgrad((S,S//2),200,0),(0,0)); sq.alpha_composite(vgrad((S,S//2),0,220),(0,S//2))
d=ImageDraw.Draw(sq)
d.text((58,54),"DAILYDOSEBOX",font=font(30),fill=TEAL)
d.text((60,S-300),"The pill box that",font=font(64),fill=PAPER)
d.text((60,S-232),"texts you back.",font=font(64),fill=PAPER)
d.rounded_rectangle([60,S-130,520,S-58],radius=36,fill=CORAL)
d.text((92,S-118),"dailydosebox.com",font=font(36),fill=PAPER)
d.text((60,S-44),"A daily check-in aid. Not a medical device.",font=font(22,False),fill=MUTED)
sq.convert("RGB").save("assets/ad-square.jpg",quality=92); print("ad-square.jpg")
# 9:16
W9,H9=1080,1920; st=crop((300,300,2750,4058),(W9,H9))
st.alpha_composite(vgrad((W9,700),210,0),(0,0)); st.alpha_composite(vgrad((W9,760),0,230),(0,H9-760))
d=ImageDraw.Draw(st)
d.text((60,70),"DAILYDOSEBOX",font=font(34),fill=TEAL)
d.text((60,250),"Scan the lid. Remember 3 words.",font=font(38,False),fill=PAPER)
d.text((60,H9-470),"The pill box",font=font(92),fill=PAPER)
d.text((60,H9-376),"that texts",font=font(92),fill=PAPER)
d.text((60,H9-282),"you back.",font=font(92),fill=CORAL)
d.rounded_rectangle([60,H9-150,600,H9-66],radius=42,fill=CORAL)
d.text((100,H9-138),"dailydosebox.com",font=font(46),fill=PAPER)
d.text((60,H9-50),"A daily check-in aid. Not a medical device.",font=font(24,False),fill=MUTED)
st.convert("RGB").save("assets/ad-story.jpg",quality=92); print("ad-story.jpg")
