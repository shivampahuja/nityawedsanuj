"""Assemble wall/index.html from tools/wall.src.html.
Usage (from the repository root): python3 tools/wall-assemble.py [API_KEY]
Without a key the placeholder stays in and the page says it needs its Drive key."""
import re, sys
src = open('tools/wall.src.html').read()
svg = open('wall/qr-folder.svg').read()
svg = re.sub(r'<svg[^>]*>', '<svg viewBox="0 0 41 41" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="QR code to the shared photo folder">', svg, count=1)
fonts = open('tools/wall-fonts.css').read()
key = sys.argv[1] if len(sys.argv) > 1 else '__API_KEY__'
out = src.replace('__QR_SVG__', svg).replace('__FONTS__', fonts).replace('__API_KEY__', key)
assert '__QR_SVG__' not in out and '__FONTS__' not in out
open('wall/index.html', 'w').write(out)
print('wall/index.html', len(out) // 1024, 'KB; key', 'baked in' if key != '__API_KEY__' else 'placeholder')
