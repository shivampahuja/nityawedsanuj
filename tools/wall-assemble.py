"""Assemble a photo wall from tools/wall.src.html (run from the repository root).
    python3 tools/wall-assemble.py API_KEY                       -> wall/index.html, the main folder
    python3 tools/wall-assemble.py API_KEY --folder ID --out reception/wall/index.html
Without a key the placeholder stays in and the page says it needs its Drive key.
The QR code pointing at the folder is generated here."""
import argparse, os, re
import qrcode, qrcode.image.svg

MAIN_FOLDER = '1oWoLtRB513iH9FUlIvNsBbGylcjif09z'
ap = argparse.ArgumentParser()
ap.add_argument('key', nargs='?', default='__API_KEY__')
ap.add_argument('--folder', default=MAIN_FOLDER, help='Drive folder id the wall reads')
ap.add_argument('--out', default='wall/index.html')
a = ap.parse_args()

src = open('tools/wall.src.html').read()
fonts = open('tools/wall-fonts.css').read()
svg = qrcode.make('https://drive.google.com/drive/folders/' + a.folder, image_factory=qrcode.image.svg.SvgPathImage, border=2).to_string(encoding='unicode')
vb = re.search(r'viewBox="([^"]+)"', svg).group(1)
svg = re.sub(r'<\?xml[^>]*>\s*', '', svg)
svg = re.sub(r'<svg[^>]*>', '<svg viewBox="%s" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="QR code to the shared photo folder">' % vb, svg, count=1)
assert src.count("folderId: '%s'" % MAIN_FOLDER) == 1
out = (src.replace('__QR_SVG__', svg).replace('__FONTS__', fonts).replace('__API_KEY__', a.key)
          .replace("folderId: '%s'" % MAIN_FOLDER, "folderId: '%s'" % a.folder))
assert '__QR_SVG__' not in out and '__FONTS__' not in out
os.makedirs(os.path.dirname(a.out) or '.', exist_ok=True)
open(a.out, 'w').write(out)
print(a.out, len(out) // 1024, 'KB; folder', a.folder, '; key', 'baked in' if a.key != '__API_KEY__' else 'placeholder')
