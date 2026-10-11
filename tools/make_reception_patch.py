#!/usr/bin/env python3
"""Generate reception-patch.json: turns the Claude Design export of the wedding invitation into the
reception invitation (nityawedsanuj.com/reception). Applied by tools/build.py --patch.
    make_reception_patch.py EXPORT_HTML OUT_JSON [--text-top 12%]
Images are referenced as __IMG:reception__ and __IMG:venue__ and supplied to build.py with --image.
"""
import argparse, json, re

ap = argparse.ArgumentParser()
ap.add_argument('src'); ap.add_argument('out')
ap.add_argument('--text-top', default='12%', help='top offset of the title block on the reception card (depends on the picture)')
a = ap.parse_args()

lines = open(a.src, encoding='utf-8').read().split('\n')
ti = next(i for i, l in enumerate(lines) if l.strip() == '<script type="__bundler/template">') + 1
t = json.loads(lines[ti])

P = []
def add(find, replace, count=1):
    n = t.count(find)
    assert n == count, 'expected %d match(es), found %d: %r' % (count, n, find[:80])
    P.append({'find': find, 'replace': replace, 'count': count})

VENUE = 'The Imperium'
ADDRESS = 'A-14, M.G. Road, Block A, Ashok Vihar, Delhi 110052'
MAPS_Q = 'The+Imperium,+A-14,+M.G.+Road,+Block+A,+Ashok+Vihar,+Delhi+110052'

# ---- 1. Opening envelope card and the invitation card
add('11 · 12 DECEMBER 2026 · KASAULI', 'RECEPTION · 19 DECEMBER 2026 · DELHI')
add('request the pleasure of your company at the wedding of', 'request the pleasure of your company at the wedding reception of')
add('Friday 11 and Saturday 12 December 2026', 'Saturday 19 December 2026')
add("font-size:3.6cqw;line-height:1.3;font-style:italic\">Fortune Select Forest Hill, Kasauli</div>",
    "font-size:3.6cqw;line-height:1.3;font-style:italic\">%s, Ashok Vihar, Delhi</div>" % VENUE)

# ---- 2. The two wedding-day sections become one reception section
start = t.index('  <section data-screen-label="04 Friday"')
end = t.index('  <section data-screen-label="06 Venue"')
days = t[start:end]
reception = '''  <section data-screen-label="04 Reception" style="background:#f4ead8">
    <div style="padding:64px 24px 36px;text-align:center;display:flex;flex-direction:column;align-items:center;gap:4px">
      <div style="font-family:'Imperial Script',cursive;font-weight:400;font-size:58px;line-height:1;color:#7a2a1c">In Delhi</div>
      <div style="font-family:'Jost',sans-serif;font-weight:500;font-size:12px;letter-spacing:.34em;color:#a8682e">SATURDAY, 19 DECEMBER</div>
    </div>
    <div style="position:relative;aspect-ratio:9/16;overflow:hidden;container-type:inline-size">
      <img src="__IMG:reception__" alt="Reception" style="width:100%;height:100%;object-fit:cover;display:block">
      <div style="position:absolute;left:12%;right:12%;top:TEXT_TOP;text-align:center;display:flex;flex-direction:column;align-items:center;gap:3cqw">
        <div style="display:flex;flex-direction:column;align-items:center;gap:0">
          <div style="font-family:'Imperial Script',cursive;font-weight:400;font-size:24cqw;line-height:.95;color:#fdeed6;text-shadow:0 2px 14px rgba(0,0,0,.18)">Reception</div>
          <div style="display:flex;align-items:center;gap:10px;margin-top:2px">
            <div style="width:6cqw;height:1px;background:#f6cf8a"></div>
            <div style="font-family:'Jost',sans-serif;font-weight:500;font-size:2.7cqw;letter-spacing:.32em;color:#f6cf8a">6:00 PM ONWARDS</div>
            <div style="width:6cqw;height:1px;background:#f6cf8a"></div>
          </div>
        </div>
        <div style="font-family:'Cormorant Garamond',serif;font-style:italic;font-size:4.4cqw;line-height:1.38;color:#fbe6cc;text-wrap:pretty">Dinner, music and the newly-weds, for everyone who could not make it to the hills and everyone who did.</div>
      </div>
    </div>
    <div style="padding:44px 32px;text-align:center;display:flex;flex-direction:column;align-items:center;gap:10px">
      <div style="width:40px;height:1px;background:#a8682e"></div>
      <div style="font-family:'Cormorant Garamond',serif;font-style:italic;font-size:24px;line-height:1.35;color:#7a2a1c">December in Delhi calls for the good shawl.</div>
      <div style="width:40px;height:1px;background:#a8682e"></div>
    </div>
  </section>

'''.replace('TEXT_TOP', a.text_top)
add(days, reception)

# ---- 3. Venue
add('<img src="e11d75ea-8a51-4255-a3c5-d638c4bf2e2a" alt="Fortune Select Forest Hill"', '<img src="__IMG:venue__" alt="%s"' % VENUE)
add("font-size:46px;line-height:1.05;color:#7a2a1c\">Fortune Select Forest Hill</div>", "font-size:46px;line-height:1.05;color:#7a2a1c\">%s</div>" % VENUE)
add('<div style="font-size:19px;font-style:italic">Kasauli, Himachal Pradesh</div>', '<div style="font-size:19px;font-style:italic">%s</div>' % ADDRESS)
add('https://www.google.com/maps?q=Fortune+Select+Forest+Hill+Kasauli&amp;output=embed', 'https://www.google.com/maps?q=%s&amp;output=embed' % MAPS_Q)
add('https://www.google.com/maps/dir/?api=1&amp;destination=Fortune+Select+Forest+Hill+Kasauli', 'https://www.google.com/maps/dir/?api=1&amp;destination=%s' % MAPS_Q)

# ---- 4. RSVP: the event is the reception, so no event chips; phone number field; its own saved response
add("ev: { Haldi: true, Sangeet: true, Varmala: true, Pheras: true, Afterparty: true }", "ev: { Reception: true }")
ev = re.search(r'            <div style="display:flex;flex-direction:column;gap:10px">\n              <span [^\n]*>EVENTS ATTENDING</span>\n(?:.*\n)*?            </div>\n', t)
assert ev, 'events block not found'
add(ev.group(0), '')
add("localStorage.getItem('na-rsvp')", "localStorage.getItem('na-rsvp-reception')")
add("localStorage.setItem('na-rsvp',", "localStorage.setItem('na-rsvp-reception',")
add("See you in Kasauli.", "See you in Delhi.")
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

# ---- 5. Closing card: countdown to the reception, shared album link once it starts
add("Date.parse('2026-12-11T14:30:00+05:30')", "Date.parse('2026-12-19T18:00:00+05:30')")
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

# validate sequential application
tt = t
for p in P:
    assert tt.count(p['find']) == p['count'], p['find'][:80]
    tt = tt.replace(p['find'], p['replace'])
for leftover in ('Haldi', 'Sangeet', 'Pheras', 'Afterparty', 'Kasauli', 'Fortune Select'):
    where = [m.start() for m in re.finditer(re.escape(leftover), tt)]
    assert not where or all('sangeetFx' in tt[w - 20:w + 20] for w in where), (leftover, where)
json.dump(P, open(a.out, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
print('wrote', a.out, 'with', len(P), 'edits')
