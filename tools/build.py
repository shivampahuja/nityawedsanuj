#!/usr/bin/env python3
"""Build a deployable copy of the Nitya & Anuj invite bundle.

Usage: build.py SOURCE_HTML OUT_HTML [--endpoint URL] [--base URL]

- Sets the page <title> (outer shell and the unpacked template)
- Adds link-preview (Open Graph) tags to the outer shell
- Bakes the RSVP endpoint (Google Apps Script web app URL) into the
  template's rsvpEndpoint prop default
"""
import argparse, html, json, re, sys

TITLE = 'Nitya weds Anuj'
DESCRIPTION = ('11 and 12 December 2026, Fortune Select Forest Hill, Kasauli. '
               'Open the invitation and send your RSVP.')

ap = argparse.ArgumentParser()
ap.add_argument('src'); ap.add_argument('out')
ap.add_argument('--endpoint', default='')
ap.add_argument('--fields', default='', help='JSON mapping of posted field names to the endpoint\'s names, '
                'e.g. {"name":"entry.123","submittedAt":""} (empty string drops a field); Google Forms needs this')
ap.add_argument('--base', default='', help='absolute site URL, used for og:image and og:url')
ap.add_argument('--patch', default='', help='JSON file: list of {"find","replace","count"} exact text edits applied to the page')
ap.add_argument('--music', default='', help='URL of the background music file (relative to the page, e.g. music.mp3); empty = no music')
ap.add_argument('--album', default='', help='URL of the shared photo/video folder or album; the page shows it once the countdown ends')
ap.add_argument('--resource', action='append', default=[], help='id=path.png: embed an image in the bundle, available to the page as window.__resources.<id>')
a = ap.parse_args()
if a.fields:
    json.loads(a.fields)  # must be valid JSON

text = open(a.src, encoding='utf-8').read()
lines = text.split('\n')

# ---- template (JSON string on its own line inside <script type="__bundler/template">)
ti = next(i for i, l in enumerate(lines) if l.strip() == '<script type="__bundler/template">') + 1
tpl = json.loads(lines[ti])

# content edits (copy and styling tweaks that are not in the design export)
if a.patch:
    for p in json.load(open(a.patch, encoding='utf-8')):
        n = tpl.count(p['find'])
        assert n == p.get('count', 1), 'patch %r matched %d times, expected %d' % (p['find'][:50], n, p.get('count', 1))
        tpl = tpl.replace(p['find'], p['replace'])

# title inside the unpacked document (the loader swaps the whole <html>)
if '<title>' not in tpl:
    tpl = tpl.replace('<meta name="viewport" content="width=device-width, initial-scale=1">',
                      '<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>%s</title>' % TITLE, 1)
    assert '<title>' in tpl, 'viewport meta not found in template'

# rsvpEndpoint default
m = re.search(r'data-props="([^"]*)"', tpl)
assert m, 'data-props not found'
props = json.loads(html.unescape(m.group(1)))
assert 'rsvpEndpoint' in props, 'rsvpEndpoint prop missing'
props['rsvpEndpoint']['default'] = a.endpoint
props['rsvpFields'] = {'editor': 'text', 'default': a.fields, 'tsType': 'string', 'section': 'RSVP'}
assert 'musicSrc' in props, 'musicSrc prop missing'
props['musicSrc']['default'] = a.music
props['albumUrl'] = {'editor': 'text', 'default': a.album, 'tsType': 'string', 'section': 'Photos'}
new_attr = html.escape(json.dumps(props, separators=(',', ':')), quote=True)
tpl = tpl[:m.start(1)] + new_attr + tpl[m.end(1):]

# submit(): post the fields under the names the endpoint expects (rsvpFields), dropping any mapped to ''
OLD_SUBMIT = """          const body = new URLSearchParams({ name: s.name, attending: s.going ? 'Yes' : 'No', guests: s.going ? s.guests : 0,
            events: s.going ? Object.keys(s.ev).filter(k => s.ev[k]).join(', ') : '', note: s.note, submittedAt: new Date().toISOString() });
          fetch(url, { method: 'POST', mode: 'no-cors', body }).catch(() => {});"""
NEW_SUBMIT = """          const data = { name: s.name, phone: s.phone || '', attending: s.going ? 'Yes' : 'No', guests: s.going ? s.guests : 0,
            events: s.going ? Object.keys(s.ev).filter(k => s.ev[k]).join(', ') : '', note: s.note, submittedAt: new Date().toISOString() };
          let map = {}; try { map = JSON.parse(this.props.rsvpFields || '{}') || {}; } catch (e) {}
          if ('phone' in map && !map.phone && data.phone) data.note = 'Phone: ' + data.phone + (data.note ? ' | ' + data.note : '');
          const body = new URLSearchParams();
          Object.keys(data).forEach(k => { const f = k in map ? map[k] : k; if (f) body.append(f, data[k]); });
          fetch(url, { method: 'POST', mode: 'no-cors', body }).catch(() => {});"""
assert tpl.count(OLD_SUBMIT) == 1, 'submit() code not found in template'
tpl = tpl.replace(OLD_SUBMIT, NEW_SUBMIT)

# the template rides inside a <script> element, so a literal "</" would end it early;
# the exporter escapes it as </ and so do we
lines[ti] = json.dumps(tpl).replace('</', '<\\u002F')
assert '</' not in lines[ti]

# ---- extra embedded resources (images the page's script references by id)
if a.resource:
    import base64, uuid, mimetypes
    mi = next(i for i, l in enumerate(lines) if l.strip() == '<script type="__bundler/manifest">') + 1
    ei = next(i for i, l in enumerate(lines) if l.strip() == '<script type="__bundler/ext_resources">') + 1
    manifest = json.loads(lines[mi]); ext = json.loads(lines[ei])
    for spec in a.resource:
        rid, path = spec.split('=', 1)
        mime = mimetypes.guess_type(path)[0] or 'application/octet-stream'
        u = str(uuid.uuid4())
        manifest[u] = {'mime': mime, 'compressed': False, 'data': base64.b64encode(open(path, 'rb').read()).decode('ascii')}
        ext = [x for x in ext if x.get('id') != rid] + [{'id': rid, 'uuid': u}]
    lines[mi] = json.dumps(manifest, separators=(',', ':')).replace('</', '<\\u002F')
    lines[ei] = json.dumps(ext, separators=(',', ':')).replace('</', '<\\u002F')

# ---- outer shell: title + link preview tags
shell = '\n'.join(lines)
base = a.base.rstrip('/')
og_image = (base + '/og.jpg') if base else 'og.jpg'
head_extra = '\n'.join([
    '  <title>%s</title>' % TITLE,
    '  <meta name="viewport" content="width=device-width, initial-scale=1">',
    '  <meta name="description" content="%s">' % html.escape(DESCRIPTION, quote=True),
    '  <meta name="robots" content="noindex">',
    '  <meta property="og:type" content="website">',
    '  <meta property="og:title" content="%s">' % TITLE,
    '  <meta property="og:description" content="%s">' % html.escape(DESCRIPTION, quote=True),
    '  <meta property="og:image" content="%s">' % og_image,
    '  <meta property="og:image:width" content="1200">',
    '  <meta property="og:image:height" content="630">',
] + (['  <meta property="og:url" content="%s/">' % base] if base else []) + [
    '  <meta name="twitter:card" content="summary_large_image">',
])
assert shell.count('<title>Bundled Page</title>') == 1
shell = shell.replace('  <title>Bundled Page</title>', head_extra, 1)

open(a.out, 'w', encoding='utf-8').write(shell)
print('wrote', a.out, len(shell.encode('utf-8')) // 1024, 'KB; endpoint =', repr(a.endpoint) or '(none)')
