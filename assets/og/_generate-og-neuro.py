"""Genera la OG image para el post de neurociencia.
Patron: gradiente brand-purple -> brand-green, headline serif grande, branding al pie.
Output: assets/og/2026-05-08-neurociencia.jpg (1200x630)
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
OUT = os.path.join(os.path.dirname(__file__), "2026-05-08-neurociencia.jpg")

# Brand colors (hex -> rgb)
PURPLE_DARK = (76, 29, 149)    # #4C1D95
PURPLE = (107, 33, 168)        # #6B21A8
GREEN = (5, 150, 105)          # #059669
GREEN_LIGHT = (16, 185, 129)   # #10B981
WHITE = (255, 255, 255)

img = Image.new("RGB", (W, H), PURPLE_DARK)
draw = ImageDraw.Draw(img)

# Vertical gradient: purple-dark (top) -> purple -> green (bottom-right)
# Use a diagonal blend by mixing two linear gradients
for y in range(H):
    t = y / (H - 1)
    # mix between purple-dark and green vertically
    r = int(PURPLE_DARK[0] + (GREEN[0] - PURPLE_DARK[0]) * t)
    g = int(PURPLE_DARK[1] + (GREEN[1] - PURPLE_DARK[1]) * t)
    b = int(PURPLE_DARK[2] + (GREEN[2] - PURPLE_DARK[2]) * t)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# Add a soft purple overlay on the left side for depth
overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ovd = ImageDraw.Draw(overlay)
for x in range(W // 2):
    alpha = int(60 * (1 - x / (W / 2)))
    ovd.line([(x, 0), (x, H)], fill=(76, 29, 149, alpha))
img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
draw = ImageDraw.Draw(img)

# Fonts
# Helvetica.ttc index 1 = Bold; load_default fallback
try:
    serif_big = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 78, index=1)
    serif_med = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 50, index=1)
    sans_small = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 26)
    sans_label = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 22, index=1)
except Exception:
    serif_big = ImageFont.load_default()
    serif_med = serif_big
    sans_small = serif_big
    sans_label = serif_big

# Eyebrow label
PADDING = 80
draw.text((PADDING, 110), "EDUCACIÓN MÉDICA · BLOG SIMACADEMY", fill=(255, 255, 255, 230), font=sans_label)

# Pequeña línea acento verde
draw.rectangle([(PADDING, 152), (PADDING + 60, 156)], fill=GREEN_LIGHT)

# Headline (3 líneas)
title_lines = [
    "Cómo la neurociencia",
    "está redefiniendo",
    "el aprendizaje en medicina",
]
y = 195
for i, line in enumerate(title_lines):
    font = serif_big if i < 2 else serif_med
    draw.text((PADDING, y), line, fill=WHITE, font=font)
    bbox = draw.textbbox((PADDING, y), line, font=font)
    y = bbox[3] + 8

# Subtítulo
sub = "Curva del olvido, práctica recuperativa y simulación clínica"
draw.text((PADDING, H - 130), sub, fill=(255, 255, 255, 220), font=sans_small)

# Branding bottom right
brand = "blog.simacademy.lat"
bbox = draw.textbbox((0, 0), brand, font=sans_small)
bw = bbox[2] - bbox[0]
draw.text((W - PADDING - bw, H - 60), brand, fill=(255, 255, 255, 200), font=sans_small)

# Pequeño dot acento
draw.ellipse([(W - PADDING - bw - 28, H - 56), (W - PADDING - bw - 12, H - 40)], fill=GREEN_LIGHT)

img.save(OUT, "JPEG", quality=88, optimize=True)
print(f"Wrote {OUT} ({os.path.getsize(OUT)} bytes)")
