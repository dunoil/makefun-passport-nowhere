#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import random, math, os

W, H = 2048, 1448
FW, FH = 1024, 724
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FD = "/usr/share/fonts/truetype/dejavu"
def font(name, size): return ImageFont.truetype(os.path.join(FD, name), size)
SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
MONO = lambda s: font("DejaVuSansMono.ttf", s)

NAVY = (28, 42, 78)
BURG = (110, 32, 48)
GREY = (90, 92, 98)
DARK = (30, 30, 34)
LABEL = (110, 112, 118)
PAPER = (246, 243, 235)
PAPER2 = (242, 239, 230)

img = Image.new("RGB", (W, H), (210, 208, 200))
d = ImageDraw.Draw(img, "RGBA")

# pages
d.rectangle([24, 24, W-24, H-24], fill=PAPER)
# guilloche-like border: repeated arcs/lines around edges
for i in range(0, 22):
    off = 36 + i*4
    col = (180, 175, 190, 26) if i % 2 == 0 else (170, 150, 155, 20)
    d.rectangle([off, off, W-off, H-off], outline=col, width=1)
for x in range(60, W-60, 28):
    d.line([(x, 40), (x+14, 70)], fill=(180,175,190,50), width=1)
    d.line([(x, H-70), (x+14, H-40)], fill=(180,175,190,50), width=1)

# spine shadow
for i in range(50):
    a = int(70 * (1 - i/50))
    d.line([(W//2 - 25 + i, 24), (W//2 - 25 + i, H-24)], fill=(0,0,0,a), width=1)
    d.line([(W//2 + 25 - i, 24), (W//2 + 25 - i, H-24)], fill=(0,0,0,a), width=1)
d.line([(W//2, 24), (W//2, H-24)], fill=(120,118,110), width=2)

# paper grain
random.seed(7)
for _ in range(9000):
    x, y = random.randint(30, W-30), random.randint(30, H-30)
    v = random.randint(-8, 8)
    d.point((x, y), fill=(246+v, 243+v, 235+v))

LX, RX = 70, W//2 + 60  # left/right page origins
PW = W//2 - 110  # page usable width

def label_value(x, y, label, value, lw=420):
    d.text((x, y), label, font=SANS(22), fill=LABEL)
    d.text((x, y+28), value, font=SANS_B(34), fill=DARK)
    d.line([(x, y+72), (x+lw, y+72)], fill=(190,188,180), width=1)

# ---------- LEFT PAGE: VISAS ----------
d.text((LX, 70), "VISAS", font=SERIF_B(52), fill=NAVY)
d.line([(LX, 145), (LX+PW, 145)], fill=NAVY, width=3)
d.text((LX, 160), "Visa and border stamps  /  Visas et cachets", font=SERIF(24), fill=GREY)

def oval_stamp(cx, cy, w, h, color, lines, angle=0):
    # draw on overlay then rotate for faded stamp feel
    ov = Image.new("RGBA", (w+40, h+40), (0,0,0,0))
    od = ImageDraw.Draw(ov)
    od.ellipse([20, 20, w+20, h+20], outline=color+(190,), width=5)
    od.ellipse([32, 32, w+8, h+8], outline=color+(150,), width=2)
    ty = h//2 - len(lines)*22 + 10
    for ln, fnt in lines:
        tw = od.textlength(ln, font=fnt)
        od.text(((w+40-tw)/2, ty), ln, font=fnt, fill=color+(200,))
        ty += 44
    ov = ov.rotate(angle, expand=True, resample=Image.BICUBIC)
    img.paste(ov, (int(cx - ov.width/2), int(cy - ov.height/2)), ov)

def round_stamp(cx, cy, r, color, lines, angle=0):
    sz = r*2+40
    ov = Image.new("RGBA", (sz, sz), (0,0,0,0))
    od = ImageDraw.Draw(ov)
    od.ellipse([20, 20, sz-20, sz-20], outline=color+(185,), width=5)
    od.ellipse([32, 32, sz-32, sz-32], outline=color+(140,), width=2)
    ty = sz//2 - len(lines)*22
    for ln, fnt in lines:
        tw = od.textlength(ln, font=fnt)
        od.text(((sz-tw)/2, ty), ln, font=fnt, fill=color+(195,))
        ty += 44
    ov = ov.rotate(angle, expand=True, resample=Image.BICUBIC)
    img.paste(ov, (int(cx - ov.width/2), int(cy - ov.height/2)), ov)

d = ImageDraw.Draw(img, "RGBA")
BLUE = (45, 75, 130); TEAL = (35, 95, 95); PLUM = (110, 50, 90); SLATE = (70, 80, 105)
round_stamp(LX+230, 420, 165, BLUE, [("KINGDOM OF WAKE", SANS_B(26)), ("ENTRY", SANS_B(30)), ("18 JUN 2024", SANS(28))], angle=-8)
oval_stamp(LX+620, 430, 340, 210, SLATE, [("KINGDOM OF WAKE", SANS_B(26)), ("EXIT", SANS_B(30)), ("02 JUL 2024", SANS(28))], angle=6)
round_stamp(LX+250, 800, 165, PLUM, [("VESPERIA", SANS_B(30)), ("ENTRY", SANS_B(30)), ("09 NOV 2024", SANS(28))], angle=5)
oval_stamp(LX+630, 810, 340, 210, TEAL, [("VESPERIA", SANS_B(28)), ("EXIT", SANS_B(30)), ("21 NOV 2024", SANS(28))], angle=-6)
d = ImageDraw.Draw(img, "RGBA")

# red rectangular condition stamp
ov = Image.new("RGBA", (760, 170), (0,0,0,0))
od = ImageDraw.Draw(ov)
od.rectangle([8, 8, 752, 162], outline=(178, 30, 38, 210), width=6)
od.text((28, 28), "CONDITION: BEARER MUST", font=SANS_B(40), fill=(178,30,38,215))
od.text((28, 82), "NAP ON ARRIVAL", font=SANS_B(40), fill=(178,30,38,215))
ov = ov.rotate(-4, expand=True, resample=Image.BICUBIC)
img.paste(ov, (LX+40, 1030), ov)
d = ImageDraw.Draw(img, "RGBA")
d.text((LX, 1330), "This page is reserved for visas and official stamps.", font=SERIF(22), fill=GREY)

# ---------- RIGHT PAGE: DATA ----------
d.text((RX, 60), "REPUBLIC OF SOMNIA", font=SERIF_B(50), fill=NAVY)
d.text((RX, 122), "PASSPORT  /  PASSEPORT", font=SERIF(30), fill=BURG)
d.line([(RX, 172), (RX+PW, 172)], fill=NAVY, width=3)

# photo box (portrait drawn on its own layer, clipped to the box)
PX, PY, PWd, PHt = RX, 205, 260, 380
photo = Image.new("RGB", (PWd, PHt), (198, 208, 218))
pd = ImageDraw.Draw(photo)
pd.ellipse([35, 245, 225, 420], fill=(88, 72, 92))
pd.rectangle([35, 330, 225, PHt], fill=(88, 72, 92))
pd.polygon([(110, 330), (130, 378), (150, 330)], fill=(240, 238, 232))
pd.rectangle([112, 195, 148, 270], fill=(216, 178, 152))
pd.ellipse([65, 55, 195, 225], fill=(226, 188, 160))
pd.arc([58, 38, 202, 180], start=180, end=360, fill=(62, 44, 36), width=26)
pd.rectangle([58, 95, 80, 210], fill=(62, 44, 36))
pd.rectangle([180, 95, 202, 210], fill=(62, 44, 36))
pd.ellipse([98, 135, 112, 145], fill=DARK)
pd.ellipse([148, 135, 162, 145], fill=DARK)
pd.line([(130, 145), (126, 170)], fill=(170, 130, 105), width=3)
pd.arc([108, 172, 152, 198], start=15, end=165, fill=(150, 80, 80), width=3)
img.paste(photo, (PX, PY))
d = ImageDraw.Draw(img, "RGBA")
d.rectangle([PX, PY, PX+PWd, PY+PHt], outline=NAVY, width=3)

# fields right of photo
FX = RX + 295
label_value(FX, 200, "Type / Type", "P", lw=105)
label_value(FX+135, 200, "Code / Code", "SMN", lw=115)
label_value(FX+280, 200, "Passport No.", "S0424177", lw=250)
label_value(FX, 300, "Surname / Nom", "MARLOWE", lw=530)
label_value(FX, 400, "Given names / Prenoms", "JUNE AURELIA", lw=530)
label_value(FX, 500, "Nationality / Nationalite", "SOMNIAN", lw=530)

# full-width fields below photo
label_value(RX, 615, "Date of birth / Date de naissance", "14 MAR 1991", lw=390)
label_value(RX+420, 615, "Sex / Sexe", "F", lw=110)
label_value(RX+560, 615, "Place of birth / Lieu", "DROWSE", lw=265)
label_value(RX, 715, "Date of issue / Date de delivrance", "02 MAY 2023", lw=390)
label_value(RX+420, 715, "Date of expiry / Date d'expiration", "02 MAY 2033", lw=405)
label_value(RX, 815, "Authority / Autorite", "MINISTRY OF REST, DROWSE", lw=825)

# MRZ
MRZ_Y = 1180
d.rectangle([RX-10, MRZ_Y-16, RX+PW+10, H-50], fill=(238, 236, 228))
d.line([(RX-10, MRZ_Y-16), (RX+PW+10, MRZ_Y-16)], fill=GREY, width=2)
l1 = "P<SMNMARLOWE<<JUNE<AURELIA<<<<<<<<<<<<<<<<<<<<<<"
l2 = "S0424177<4SMN9103142F3305022<<<<<<<<<<<<<<08"
l1 = (l1 + "<"*44)[:44]; l2 = (l2 + "<"*44)[:44]
mf = MONO(31)
# scale check: fit within page width
d.text((RX, MRZ_Y+10), l1, font=mf, fill=(20,20,20))
d.text((RX, MRZ_Y+70), l2, font=mf, fill=(20,20,20))

img = img.resize((FW, FH), Image.LANCZOS)
img.save(OUT, optimize=True)
print(f"saved {OUT} {os.path.getsize(OUT)} bytes {img.size}")
print("MRZ1", len(l1), l1)
print("MRZ2", len(l2), l2)
