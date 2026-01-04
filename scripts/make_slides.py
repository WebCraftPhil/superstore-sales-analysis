from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VIS = ROOT / 'visuals'
OUT = VIS

# simple slide generator: two slides
slide_w, slide_h = 1280, 720
bg = (255,255,255)
font_path = None
try:
    # try a common system font
    from matplotlib import font_manager
    font_path = font_manager.findfont('DejaVu Sans')
except Exception:
    font_path = None

font = ImageFont.truetype(font_path, 28) if font_path else ImageFont.load_default()
small = ImageFont.truetype(font_path, 18) if font_path else ImageFont.load_default()

# Slide 1: title + two charts
im = Image.new('RGB', (slide_w, slide_h), color=bg)
d = ImageDraw.Draw(im)
d.text((40,30), 'Shipping Performance — Key Charts', fill='black', font=font)

# paste histogram left
hist = Image.open(VIS / 'shipping_delay_hist.png').convert('RGB')
box = hist.resize((580,360))
im.paste(box, (40,80))

# paste boxplot right
bp = Image.open(VIS / 'shipping_delay_boxplot.png').convert('RGB')
box2 = bp.resize((580,360))
im.paste(box2, (660,80))

im.save(OUT / 'slide_01.png')

# Slide 2: sales vs delay + summary bullets
im2 = Image.new('RGB', (slide_w, slide_h), color=bg)
d2 = ImageDraw.Draw(im2)
d2.text((40,30), 'Customer & Business Signals', fill='black', font=font)

sv = Image.open(VIS / 'sales_vs_delay.png').convert('RGB')
svb = sv.resize((760,420))
im2.paste(svb, (40,80))

# summary text
summary = (VIS / 'summary.txt').read_text().splitlines()
y = 520
for line in summary[:6]:
    d2.text((820,y), line, fill='black', font=small)
    y += 26

im2.save(OUT / 'slide_02.png')

print('Slides written to', OUT)
