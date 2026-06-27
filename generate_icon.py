from PIL import Image, ImageDraw

def make_icon(size, path):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # rounded square bg
    margin = int(size * 0.1)
    r = int(size * 0.2)
    draw.rounded_rectangle(
        [margin, margin, size - margin, size - margin],
        radius=r,
        fill=(22, 33, 62, 255),
    )

    # envelope shape
    cx, cy = size // 2, size // 2
    w = int(size * 0.5)
    h = int(size * 0.35)
    x1, y1 = cx - w // 2, cy - h // 2
    x2, y2 = cx + w // 2, cy + h // 2

    draw.polygon(
        [(x1, y1), (x2, y1), (cx, y1 + h // 2)],
        fill=(0, 210, 255, 255),
    )
    draw.polygon(
        [(x1, y1), (cx, y1 + h // 2), (x2, y1), (x2, y2), (x1, y2)],
        fill=(0, 210, 255, 180),
    )

    img.save(path)

icon_dir = r"C:\email-summarizer\extension\icons"
make_icon(48, f"{icon_dir}\\icon48.png")
make_icon(128, f"{icon_dir}\\icon128.png")
