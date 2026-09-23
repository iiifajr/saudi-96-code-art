from PIL import Image, ImageDraw, ImageFont
import numpy as np

# --- Configuration ---
IMAGE_PATH = "input.jpg"
OUTPUT_PATH = "numeric_portrait.png"

# Scale factor: 2 = double size (1224x2156), 3 = triple size
SCALE = 2  

# Cell dimensions and font size
CELL_W = 8
CELL_H = 14
FONT_SIZE = 13

# Deep Saudi Green background
BG_COLOR = (7, 30, 15)

# --- Image Processing ---
img = Image.open(IMAGE_PATH).convert("L")
orig_w, orig_h = img.size

# Upscale image for higher resolution
w, h = orig_w * SCALE, orig_h * SCALE
img = img.resize((w, h), Image.Resampling.LANCZOS)

cols = w // CELL_W
rows = h // CELL_H

small_img = img.resize((cols, rows), Image.Resampling.BILINEAR)
arr = np.array(small_img)

canvas = Image.new("RGB", (cols * CELL_W, rows * CELL_H), BG_COLOR)
draw = ImageDraw.Draw(canvas)

try:
    font = ImageFont.load_default(size=FONT_SIZE)
except TypeError:
    font = ImageFont.load_default()

# Alternating characters: 9 and 6
chars = ["9", "6"]

# --- Draw Numeric Art ---
for r in range(rows):
    for c in range(cols):
        brightness = arr[r, c] / 255.0
        
        if brightness < 0.08:
            continue
            
        char = chars[(r + c) % 2]
        
        # Color mapping (Dark Green -> White / Bright Green)
        red = int(10 + brightness * 225)
        green = int(50 + brightness * 205)
        blue = int(20 + brightness * 225)
        
        draw.text((c * CELL_W, r * CELL_H), char, fill=(red, green, blue), font=font)

canvas.save(OUTPUT_PATH)
print("Done! Saved high-res image as:", OUTPUT_PATH)
