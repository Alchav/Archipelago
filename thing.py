# Requires: pip install pillow
from PIL import Image, ImageDraw, ImageOps
import random

W, H = 1920, 1080
out_path = "random_lines.png"

img = Image.new("RGB", (W, H), (0, 0, 0))
draw = ImageDraw.Draw(img)

seen_rows = set()
seen_cols = set()

count = 0
while len(seen_rows) < H or len(seen_cols) < W:
    linetype = random.randrange(4)
    y = random.randrange(H)
    x = random.randrange(W)
    color = (random.randrange(256), random.randrange(256), random.randrange(256))
    if linetype == 0:
        draw.line([(x - H, y - W), (x + H, y + W)], fill=color, width=random.randrange(1) + 1)
    elif linetype == 1:
        draw.line([(x + H, y - W), (x - H, y + W)], fill=color, width=random.randrange(1) + 1)
    elif linetype == 2:
        y = random.randrange(H)
        color = (random.randrange(256), random.randrange(256), random.randrange(256))
        # Draw a 1-pixel horizontal line across the full width
        draw.line([(0, y), (W - 1, y)], fill=color, width=random.randrange(1) + 1)
        seen_rows.add(y)
    else:
        x = random.randrange(W)
        color = (random.randrange(256), random.randrange(256), random.randrange(256))
        # Draw a 1-pixel vertical line across the full height
        draw.line([(x, 0), (x, H - 1)], fill=color, width=random.randrange(1) + 1)
        seen_cols.add(x)

    count += 1
    # (Optional) simple progress print every 2000 lines
    if count % 2000 == 0:
        print(f"Drawn {count} lines... rows covered: {len(seen_rows)}/{H}, cols covered: {len(seen_cols)}/{W}")

img2 = Image.open("/home/alchav/Downloads/soft-warm-rainbow-radial-rgb-footage-139736497_iconl.webp").convert("RGB")
img2 = img2.resize(img.size)
blended = Image.blend(img, ImageOps.invert(img2), alpha=0.50)

blended.save(out_path, "PNG")
# img.save(out_path, "PNG")
print(f"Done. Drew {count} lines. Saved to {out_path}")