#!/usr/bin/env python3
"""Generate content-patch.json: the copy, layout and behaviour edits applied on top of the
Claude Design export by tools/build.py --patch. Run against the export to validate:
    make_patch.py EXPORT_HTML OUT_JSON
"""
import json, re, sys

src, out = sys.argv[1], sys.argv[2]
lines = open(src, encoding='utf-8').read().split('\n')
ti = next(i for i, l in enumerate(lines) if l.strip() == '<script type="__bundler/template">') + 1
t = json.loads(lines[ti])

P = []
def add(find, replace, count=1):
    n = t.count(find)
    assert n == count, 'expected %d match(es), found %d: %r' % (count, n, find[:80])
    P.append({'find': find, 'replace': replace, 'count': count})

LABEL = "IF YOU'D LIKE TO MATCH"
def label_div(color):
    return ("<div style=\"font-family:'Jost',sans-serif;font-weight:500;font-size:2.3cqw;letter-spacing:.34em;color:%s;opacity:.85\">%s</div>" % (color, LABEL))
def card_anchor(next_img_uuid, next_alt):
    a = '\n      </div>\n    </div>\n    <div style="position:relative;aspect-ratio:9/16;overflow:hidden">\n      <img src="%s" alt="%s"' % (next_img_uuid, next_alt)
    assert t.count(a) == 1, 'card anchor not found: ' + next_alt
    return a
def with_bottom(anchor, block, band=None):
    """Insert a bottom-anchored block (and an optional darkening band) inside the card, before it closes."""
    inner = '\n      </div>\n      ' + (band + '\n      ' if band else '') + block + anchor[len('\n      </div>'):]
    return inner

# ---- 1. Dress-code copy: suggestions, not rules
add('Come in shades of yellow and orange. Expect to leave in a little more of it.',
    'Shades of yellow and orange if you feel like it. Expect to leave in a little more of it regardless.')
# Sangeet and Afterparty: the dress sentence goes entirely; the palette dots at the foot of the card remain
add(' Dark shades and Indo-western are the order of the evening.', '')
add(' Western wear suits the handover.', '')

# ---- 2. Haldi, Sangeet, Afterparty: palette moves from under the text to the foot of the card
dress = re.compile(r'        <div style="display:flex;flex-direction:column;align-items:center;gap:8px;margin-top:4px">\n'
                   r'          <div style="[^"]*letter-spacing:\.34em;color:(#[0-9a-f]{6})">DRESS CODE</div>\n'
                   r'          <div style="display:flex;gap:7px;justify-content:center">((?:<div style="width:4\.4cqw;height:4\.4cqw;border-radius:50%;background:#[0-9a-f]{6};box-shadow:[^"]*"></div>)+)</div>\n'
                   r'        </div>')
cards = {  # keyed by the alt of the image that follows the card
    'Haldi ceremony': dict(next='217e590f-35da-46ea-b59b-86c03fcfe658', label='#a8551c', bottom='69cqw', band=None),
    'Sangeet evening': dict(next='61209456-71ee-4c1d-8dbd-5dd554058677', label=None, bottom='8cqw',
                            band='<div style="position:absolute;left:0;right:0;bottom:0;height:30%;background:linear-gradient(180deg,rgba(30,8,4,0) 0%,rgba(30,8,4,.72) 100%);pointer-events:none"></div>'),
    'Afterparty': dict(next='b56eac68-4253-40b3-bc7b-ff3704a3b047', label=None, bottom='8cqw',
                       band='<div style="position:absolute;left:0;right:0;bottom:0;height:30%;background:linear-gradient(180deg,rgba(10,12,8,0) 0%,rgba(10,12,8,.72) 100%);pointer-events:none"></div>'),
}
found = {}
for m in dress.finditer(t):
    after = t[m.end():m.end() + 400]
    alt = re.search(r'alt="([^"]*)"', after).group(1)
    found[alt] = m
assert set(found) == set(cards), found.keys()
for alt, cfg in cards.items():
    m = found[alt]
    color = cfg['label'] or m.group(1)
    swatches = m.group(2).replace('width:4.4cqw;height:4.4cqw', 'width:3.6cqw;height:3.6cqw')
    block = ('<div style="position:absolute;left:0;right:0;bottom:%s;display:flex;flex-direction:column;align-items:center;gap:8px;text-align:center">'
             '%s<div style="display:flex;gap:7px;justify-content:center">%s</div></div>') % (cfg['bottom'], label_div(color), swatches)
    add(m.group(0), '')                                   # out of the text block
    anchor = card_anchor(cfg['next'], alt)
    add(anchor, with_bottom(anchor, block, cfg['band']))  # into the foot of the card

# ---- 3. Varmala and Pheras card: block centred in the open sky, pastel note at the foot; no caption on the mandap photo
add("font-size:14.5cqw;line-height:.95;color:#6a1416;text-shadow:0 2px 14px rgba(0,0,0,.08)\">Varmala</div>",
    "font-size:12.5cqw;line-height:.95;color:#6a1416;text-shadow:0 2px 14px rgba(0,0,0,.08)\">Varmala</div>")
add("font-size:14.5cqw;line-height:.95;color:#6a1416;text-shadow:0 2px 14px rgba(0,0,0,.08)\">Pheras</div>",
    "font-size:12.5cqw;line-height:.95;color:#6a1416;text-shadow:0 2px 14px rgba(0,0,0,.08)\">Pheras</div>")
add('<div style="position:absolute;left:11%;right:11%;top:16.5%;text-align:center;display:flex;flex-direction:column;align-items:center;gap:1.6cqw">',
    '<div style="position:absolute;inset:0;padding:0 11% 42cqw;text-align:center;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:1cqw">')
add("font-size:3.9cqw;line-height:1.3;color:#4a1410;text-wrap:pretty\">Nitya and Anuj exchange garlands",
    "font-size:3.5cqw;line-height:1.3;color:#4a1410;text-wrap:pretty\">Nitya and Anuj exchange garlands")
add('<div style="display:flex;align-items:center;gap:8px;margin:2px 0"><div style="width:7cqw;height:1px;background:#8e2a20"></div><div style="width:5px;height:5px;transform:rotate(45deg);background:#8e2a20"></div><div style="width:7cqw;height:1px;background:#8e2a20"></div></div>',
    '<div style="display:flex;align-items:center;gap:8px;margin:5cqw 0"><div style="width:7cqw;height:1px;background:#8e2a20"></div><div style="width:5px;height:5px;transform:rotate(45deg);background:#8e2a20"></div><div style="width:7cqw;height:1px;background:#8e2a20"></div></div>')
add("font-size:3.9cqw;line-height:1.3;color:#4a1410;text-wrap:pretty\">Vows around the sacred fire",
    "font-size:3.5cqw;line-height:1.3;color:#4a1410;text-wrap:pretty\">Vows around the sacred fire")
pm = re.search(r'<div style="display:flex;align-items:center;gap:8px;margin-top:2px"><div style="display:flex;gap:7px;justify-content:center">((?:<div style="width:4\.4cqw;height:4\.4cqw;border-radius:50%;background:#[0-9a-f]{6};box-shadow:[^"]*"></div>)+)</div><div style="[^"]*">PASTELS</div></div>', t)
assert pm, 'pastel wrapper not found'
pastel_block = ('<div style="position:absolute;left:0;right:0;bottom:12cqw;display:flex;flex-direction:column;align-items:center;gap:1.4cqw;text-align:center">'
                '<div style="display:flex;gap:7px;justify-content:center">%s</div>'
                "<div style=\"font-family:'Cormorant Garamond',serif;font-style:italic;font-size:3.2cqw;line-height:1.3;color:#4a1410\">Pastels welcome, never required.</div></div>"
                % pm.group(1).replace('width:4.4cqw;height:4.4cqw', 'width:3.6cqw;height:3.6cqw'))
add(pm.group(0), '')
anchor = card_anchor('4209f1c1-5ea3-4223-8e54-837cc71dd8f6', 'Varmala under the mandap')
add(anchor, with_bottom(anchor, pastel_block))
add('<div style="position:absolute;left:0;right:0;top:0;padding:30px 28px 70px;background:linear-gradient(180deg,rgba(255,250,240,.82) 0%,rgba(255,250,240,0) 100%);'
    "text-align:center;font-family:'Cormorant Garamond',serif;font-style:italic;font-size:19px;line-height:1.35;color:#4a1410\">Please wear light pastels for the Varmala and the Pheras.</div>", '')
assert t.count('width:4.4cqw;height:4.4cqw') == 15  # every swatch is rewritten above

# ---- 4. Sangeet evening: the real ring photo instead of the drawn one
add("    k.push(e('div', { key: 'ring', style: { position: 'absolute', left: '50%', top: '36%', width: 120, height: 140, animation: 'ringFloat 4.5s ease-in-out infinite', filter: 'drop-shadow(0 10px 18px rgba(0,0,0,.45))' } }, band, prong, gem, ...glints));",
    "    const ringImg = e('img', { key: 'ringimg', src: (window.__resources && window.__resources.ring) || 'ring.png', alt: '', style: { position: 'absolute', left: 0, top: 0, width: 180, height: 180, objectFit: 'contain' } });\n"
    "    k.push(e('div', { key: 'ring', style: { position: 'absolute', left: '50%', top: '36%', width: 180, height: 180, animation: 'ringFloat 4.5s ease-in-out infinite', filter: 'drop-shadow(0 14px 20px rgba(0,0,0,.55))' } }, ringImg, ...glints));")
add("    const glints = [[26, 4, 0], [88, 10, .7], [60, -14, 1.4], [8, 30, 2.1], [100, 40, 1.0]].map(",
    "    const glints = [[34, 2, 0], [104, 6, .7], [70, -16, 1.4], [14, 30, 2.1], [124, 36, 1.0]].map(")

# ---- 5. RSVP: no events preselected; phone number field
add("ev: { Haldi: true, Sangeet: true, Varmala: true, Pheras: true, Afterparty: true }",
    "ev: { Haldi: false, Sangeet: false, Varmala: false, Pheras: false, Afterparty: false }")
name_input = '''          <input value="{{ name }}" sc-camel-on-change="{{ setName }}" placeholder="Full name" style="min-height:50px;background:transparent;border:0;border-bottom:1px solid rgba(240,201,138,.6);color:#fbefd9;font-size:20px;outline:none;padding:0 2px">
        </label>'''
add(name_input, name_input + '''
        <label style="display:flex;flex-direction:column;gap:8px">
          <span style="font-family:'Jost',sans-serif;font-weight:500;font-size:12px;letter-spacing:.2em;color:#e3c79a">PHONE NUMBER</span>
          <input value="{{ phone }}" sc-camel-on-change="{{ setPhone }}" type="tel" inputmode="tel" autocomplete="tel" placeholder="With country code" style="min-height:50px;background:transparent;border:0;border-bottom:1px solid rgba(240,201,138,.6);color:#fbefd9;font-size:20px;outline:none;padding:0 2px">
        </label>''')
add("state = { now: Date.now(), name: '', going: null,", "state = { now: Date.now(), name: '', phone: '', going: null,")
add("      name: s.name, guests: s.guests, note: s.note,", "      name: s.name, phone: s.phone, guests: s.guests, note: s.note,")
add("      setName: e => this.setState({ name: e.target.value }),",
    "      setName: e => this.setState({ name: e.target.value }),\n      setPhone: e => this.setState({ phone: e.target.value }),")
add("const r = { name: s.name, going: s.going, guests: s.guests, note: s.note, ev: s.ev, submitted: true };",
    "const r = { name: s.name, phone: s.phone, going: s.going, guests: s.guests, note: s.note, ev: s.ev, submitted: true };")

# ---- 6. Closing card: shared album link, shown only once the countdown has ended
old_cd = """      <div style="font-family:'Jost',sans-serif;font-weight:500;font-size:2.7cqw;letter-spacing:.32em;color:#f0c98a">COUNTING DOWN</div>
      <div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;width:100%">
        <sc-for list="{{ countdown }}" as="u" hint-placeholder-count="4">
          <div style="display:flex;flex-direction:column;align-items:center;gap:8px">
            <div style="width:100%;aspect-ratio:1;border:1px solid rgba(240,201,138,.6);border-radius:50%;background:rgba(30,10,6,.35);display:flex;align-items:center;justify-content:center;font-family:'Jost',sans-serif;font-weight:500;font-size:24px;font-variant-numeric:tabular-nums">{{ u.v }}</div>
            <div style="font-family:'Jost',sans-serif;font-weight:500;font-size:11px;letter-spacing:.22em;color:#e3c79a">{{ u.l }}</div>
          </div>
        </sc-for>
      </div>"""
new_cd = """      <sc-if value="{{ albumClosed }}" hint-placeholder-val="{{ true }}">
        <div style="display:flex;flex-direction:column;align-items:center;gap:14px;width:100%">
          <div style="font-family:'Jost',sans-serif;font-weight:500;font-size:2.7cqw;letter-spacing:.32em;color:#f0c98a">COUNTING DOWN</div>
          <div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;width:100%">
            <sc-for list="{{ countdown }}" as="u" hint-placeholder-count="4">
              <div style="display:flex;flex-direction:column;align-items:center;gap:8px">
                <div style="width:100%;aspect-ratio:1;border:1px solid rgba(240,201,138,.6);border-radius:50%;background:rgba(30,10,6,.35);display:flex;align-items:center;justify-content:center;font-family:'Jost',sans-serif;font-weight:500;font-size:24px;font-variant-numeric:tabular-nums">{{ u.v }}</div>
                <div style="font-family:'Jost',sans-serif;font-weight:500;font-size:11px;letter-spacing:.22em;color:#e3c79a">{{ u.l }}</div>
              </div>
            </sc-for>
          </div>
          <sc-if value="{{ hasAlbum }}" hint-placeholder-val="{{ false }}">
            <a href="{{ albumUrl }}" target="_blank" rel="noopener" style="display:flex;align-items:center;justify-content:center;width:calc(100% - 112px);min-height:48px;margin-top:6px;background:#f0c98a;color:#3b1a12;text-decoration:none;font-family:'Jost',sans-serif;font-weight:500;font-size:13px;letter-spacing:.26em">ADD PHOTOS &amp; VIDEOS</a>
          </sc-if>
        </div>
      </sc-if>
      <sc-if value="{{ albumOpen }}" hint-placeholder-val="{{ false }}">
        <div style="display:flex;flex-direction:column;align-items:center;gap:16px;width:100%">
          <div style="font-family:'Jost',sans-serif;font-weight:500;font-size:2.7cqw;letter-spacing:.32em;color:#f0c98a">SHARE YOUR MOMENTS</div>
          <a href="{{ albumUrl }}" target="_blank" rel="noopener" style="display:flex;align-items:center;justify-content:center;width:100%;min-height:54px;background:#f0c98a;color:#3b1a12;text-decoration:none;font-family:'Jost',sans-serif;font-weight:500;font-size:14px;letter-spacing:.26em">ADD PHOTOS &amp; VIDEOS</a>
          <div style="font-family:'Cormorant Garamond',serif;font-style:italic;font-size:15px;line-height:1.35;color:#e3c79a;opacity:.9;max-width:300px">Everything you capture at the celebrations goes into our shared folder.</div>
        </div>
      </sc-if>"""
add(old_cd, new_cd)
add("      heroMedia, countdown, events, yesBg, yesFg, noBg, noFg,",
    "      heroMedia, countdown, events, yesBg, yesFg, noBg, noFg,\n"
    "      hasAlbum: !!this.props.albumUrl, albumUrl: this.props.albumUrl || '#', albumOpen: !!this.props.albumUrl && d <= 0, albumClosed: !(!!this.props.albumUrl && d <= 0),")

add('<div style="position:absolute;left:24px;right:24px;bottom:40px;display:flex;flex-direction:column;align-items:center;gap:18px;color:#fbefd9">',
    '<div style="position:absolute;left:24px;right:24px;bottom:28px;display:flex;flex-direction:column;align-items:center;gap:18px;color:#fbefd9">')

# ---- 7. The wax seal, not a pearl, travels the thread: it leaves the envelope and settles on the string
old_pearl = """  <div ref="{{ pearlRef }}" style="position:absolute;top:0;left:0;width:24px;height:24px;z-index:6;pointer-events:none;will-change:transform;transform:translate(-200px,-200px);opacity:0;transition:opacity 1.2s ease">
    <div style="position:absolute;inset:-14px;border-radius:50%;background:radial-gradient(circle,rgba(255,238,205,.6) 0%,rgba(255,238,205,0) 62%)"></div>
    <div style="position:absolute;inset:0;border-radius:50%;background:radial-gradient(circle at 34% 30%,#ffffff 0%,#fbf6ee 14%,#ece2d3 42%,#cdbca8 74%,#9d8a74 100%);box-shadow:0 8px 14px rgba(40,20,10,.38),inset -3px -4px 7px rgba(110,80,50,.35)"></div>
    <div ref="{{ sheenRef }}" style="position:absolute;inset:0;border-radius:50%;background:conic-gradient(from 0deg,rgba(255,200,220,0),rgba(255,190,215,.32),rgba(190,220,255,.32),rgba(210,255,225,.26),rgba(255,230,190,.32),rgba(255,200,220,0));mix-blend-mode:soft-light"></div>
    <div style="position:absolute;left:5px;top:4px;width:8px;height:6px;border-radius:50%;background:rgba(255,255,255,.95);filter:blur(1px)"></div>
  </div>"""
new_seal = """  <div ref="{{ pearlRef }}" style="position:absolute;top:0;left:0;width:36px;height:36px;z-index:6;pointer-events:none;will-change:transform;transform:translate(-200px,-200px);opacity:0;transition:opacity 1.2s ease">
    <div style="position:absolute;inset:-16px;border-radius:50%;background:radial-gradient(circle,rgba(255,205,190,.42) 0%,rgba(255,205,190,0) 62%)"></div>
    <div style="position:absolute;inset:-2px;border-radius:47% 53% 50% 50% / 52% 46% 54% 48%;background:radial-gradient(circle at 36% 30%,#c45e64 0%,#93303b 55%,#6b1e28 100%);box-shadow:0 5px 10px rgba(80,20,25,.45),inset 0 -2px 4px rgba(0,0,0,.25)"></div>
    <div style="position:absolute;inset:3px;border-radius:50%;box-shadow:inset 0 1px 3px rgba(0,0,0,.35),inset 0 -1px 2px rgba(255,190,180,.35);background:radial-gradient(circle at 40% 35%,#a8414a,#7d2430)"></div>
    <div ref="{{ sheenRef }}" style="position:absolute;inset:-2px;border-radius:50%;background:conic-gradient(from 0deg,rgba(255,255,255,0),rgba(255,255,255,.24),rgba(255,255,255,0) 40%);mix-blend-mode:soft-light"></div>
    <div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;gap:1px;font-family:'Jost',sans-serif;font-weight:500;font-size:12px;line-height:1;color:#fbe3d6;text-shadow:0 1px 1px rgba(0,0,0,.35)">A<span style="font-family:'Cormorant Garamond',serif;font-style:italic;font-size:8px;margin-top:2px">&amp;</span>N</div>
  </div>"""
add(old_pearl, new_seal)
add("""    this.pearlRef.current.style.transform = 'translate(' + (q.x - 12) + 'px,' + (q.y - 12 + bob) + 'px)';""",
    """    let px = q.x - 18, py = q.y - 18 + bob;
    if (this.state.revealed && !this.handoffDone) {  // the seal leaves the envelope and settles on the thread
      if (!this.handoffT0) this.handoffT0 = ts;
      const k = Math.min(1, (ts - this.handoffT0) / 1500), e = 1 - Math.pow(1 - k, 3);
      const s0 = root.children[0], sx = root.offsetWidth / 2 - 18, sy = s0.offsetHeight / 2 + s0.offsetWidth * .034 - 18;
      px = sx + (px - sx) * e; py = sy + (py - sy) * e;
      if (k >= 1) this.handoffDone = true;
    }
    this.pearlRef.current.style.transform = 'translate(' + px + 'px,' + py + 'px)';""")
add("const pts = [{ x: W / 2, y: secs[0].offsetHeight - 46 }];", "const pts = [{ x: W / 2, y: secs[0].offsetHeight - 96 }];")  # the seal waits above the scroll hint
add("pts.push({ x: W / 2, y: last.offsetTop + 160 });", "pts.push({ x: W / 2, y: last.offsetTop + 200 });")  # and rests under the names on the closing card

# validate sequential application
tt = t
for p in P:
    assert tt.count(p['find']) == p['count'], p['find'][:80]
    tt = tt.replace(p['find'], p['replace'])
json.dump(P, open(out, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
print('wrote', out, 'with', len(P), 'edits')
