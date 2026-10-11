"""Prepare the kirtan page's pictures from the generated artwork (run from the repository root).
    python3 tools/kirtan-pictures.py halo.png gurudwara.png darbar.png langar.png well.png
Writes assets/kirtan/{ganesha,invite,kirtan,langar,venue,closing}.jpg. The Ik Onkar is set into the
halo here (traced from GNU FreeSerif), so the symbol is always drawn correctly."""
import sys, os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
halo, gurudwara, darbar, langar, well = sys.argv[1:6]
os.makedirs('assets/kirtan', exist_ok=True)
def fit(path, w=900, h=1600):
    im = Image.open(path).convert('RGB'); W, H = im.size
    tw = min(W, H * w / h); th = min(H, W * h / w); l = (W - tw) / 2; t = (H - th) / 2
    return im.crop((int(l), int(t), int(l + tw), int(t + th))).resize((w, h), Image.LANCZOS)

# the envelope card: the picture is pushed down under the names (plain paper added above the garland),
# then Ik Onkar is set in gold paper inside the halo
im = fit(halo); W, H = im.size
a = np.asarray(im).astype(np.float32); LIFT = 340
rng = random.Random(7); rows = []; y = 0
while y < LIFT + 60:
    th = min(100, LIFT + 60 - y); sy = rng.randint(1250, 1600 - th); strip = a[sy:sy + th].copy()
    if rng.random() < .5: strip = strip[:, ::-1]
    rows.append(strip); y += th
top = np.concatenate(rows)[:LIFT + 60]
canvas = np.zeros((H + LIFT, W, 3), np.float32); canvas[:LIFT + 60] = top; canvas[LIFT + 60:] = a[60:]
m = np.zeros((H + LIFT, W), np.float32); m[LIFT + 20:] = 1
m = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(16))).astype(np.float32) / 255
low = np.zeros_like(canvas); low[:LIFT] = top[:LIFT]; low[LIFT:] = a
canvas = canvas * (1 - m[..., None]) + low * m[..., None]
im = Image.fromarray(canvas[:H].clip(0, 255).astype(np.uint8))
cx, cy = int(W * .5), int(H * .46) + LIFT
font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSerif.ttf', int(W * .34))
layer = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
bb = d.textbbox((0, 0), 'ੴ', font=font); gw, gh = bb[2] - bb[0], bb[3] - bb[1]
x, y = cx - gw / 2 - bb[0], cy - gh / 2 - bb[1]
shadow = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(shadow).text((x + 6, y + 9), 'ੴ', font=font, fill=(90, 50, 20, 110))
shadow = shadow.filter(ImageFilter.GaussianBlur(5))
d.text((x, y), 'ੴ', font=font, fill=(184, 137, 58, 255))
# paper grain on the gold
grain = (np.random.default_rng(1).normal(0, 9, (H, W, 1))).clip(-30, 30)
g = np.asarray(layer).astype(np.float32); g[..., :3] = (g[..., :3] + grain).clip(0, 255); layer = Image.fromarray(g.astype(np.uint8))
out = Image.alpha_composite(Image.alpha_composite(im.convert('RGBA'), shadow), layer).convert('RGB')
out.save('assets/kirtan/ganesha.jpg', quality=88, optimize=True)
# link preview: the symbol in its halo, 1200x630
og = out.crop((0, cy - 315 * W // 1200 - 0, W, cy + 315 * W // 1200)).resize((1200, 630), Image.LANCZOS) if W >= 900 else None
og = out.resize((1200, int(1200 * H / W)), Image.LANCZOS); c = int(cy * 1200 / W); og = og.crop((0, c - 315, 1200, c + 315))
og.save('kirtan/og.jpg', quality=85, optimize=True)

# the invitation: the gurudwara picture carried down to 9:19 with its own cream walkway paper
im = fit(gurudwara); a = np.asarray(im).astype(np.float32)
target = int(900 * 19 / 9); ext = target - 1600
band = a[1380:1600]  # plain cream walkway
random.seed(5); rows = []
y = 0
while y < ext + 80:
    th = min(110, ext + 80 - y); sy = random.randint(0, band.shape[0] - th)
    strip = band[sy:sy + th].copy()
    if random.random() < .5: strip = strip[:, ::-1]
    rows.append(strip); y += th
tex = np.concatenate(rows)[:ext + 80]
canvas = np.zeros((target, 900, 3), np.float32); canvas[:1600] = a; canvas[1600:] = tex[80:]
m = np.zeros((target, 900), np.float32); m[1600 - 40:] = 1
m = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(18))).astype(np.float32) / 255
join = canvas.copy(); join[1600 - 80:] = tex
inv = canvas * (1 - m[..., None]) + join * m[..., None]
Image.fromarray(inv.clip(0, 255).astype(np.uint8)).save('assets/kirtan/invite.jpg', quality=86, optimize=True)
im.save('assets/kirtan/venue.jpg', quality=86, optimize=True)
fit(darbar).save('assets/kirtan/kirtan.jpg', quality=86, optimize=True)
fit(langar).save('assets/kirtan/langar.jpg', quality=86, optimize=True)
fit(well).save('assets/kirtan/closing.jpg', quality=86, optimize=True)
print('assets/kirtan ready')
