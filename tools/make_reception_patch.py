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
NAVY = '#141a3a'        # dark sections and buttons (was maroon #3b1a12)
NAVY_DEEP = '#0e1230'   # closing card and envelope card ground (was #1e0a06)
NAVY_INK = '#1b2250'    # script headings on cream paper (was #7a2a1c)
GOLD = '#e8c88a'        # labels and rules on navy (was #a8682e on gold paper)
CREAM = '#f6ecdc'       # names on navy

# ---- 1. Opening envelope card and the invitation card
add('letter-spacing:.2em;color:#7a3b26">11 · 12 DECEMBER 2026 · KASAULI</div>', 'letter-spacing:.2em;color:%s">RECEPTION · 19 DECEMBER 2026 · DELHI</div>' % GOLD)
# the framed card gives way to the two of them under the chandeliers, with the invitation beneath
inv_start = t.index('  <section data-screen-label="02 Invitation"')
inv_end = t.index('  <section data-screen-label="04 Friday"')
invitation = '''  <section data-screen-label="02 Invitation" style="position:relative;aspect-ratio:1/2;overflow:hidden;background:#0e1230;container-type:inline-size">
    <img src="__IMG:invite__" alt="Nitya and Anuj" style="width:100%;height:100%;object-fit:cover;object-position:50% 0%;display:block">
    <div style="position:absolute;left:11%;right:11%;top:63%;bottom:0;text-align:center;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2.4cqw;color:CREAM">
      <div style="font-family:'Tiro Devanagari Hindi',serif;font-size:3.2cqw;color:GOLD">॥ श्री गणेशाय नमः ॥</div>
      <p style="margin:0;font-family:'Cormorant Garamond',serif;font-size:3.8cqw;line-height:1.35;text-wrap:balance">With the blessings of our elders, the Pahuja family requests the pleasure of your company at the wedding reception of</p>
      <div style="font-family:'Imperial Script',cursive;font-weight:400;font-size:13cqw;line-height:1;color:#fdeed6;text-shadow:0 2px 14px rgba(0,0,0,.25)">Nitya &amp; Anuj</div>
      <div style="display:flex;flex-direction:column;align-items:center;gap:.6cqw">
        <div style="font-family:'Cormorant Garamond',serif;font-size:3.6cqw;line-height:1.3">Saturday 19 December 2026</div>
        <div style="font-family:'Cormorant Garamond',serif;font-size:3.6cqw;line-height:1.3;font-style:italic;color:GOLD">VENUE_NAME, Ashok Vihar, Delhi</div>
      </div>
    </div>
  </section>

'''
add(t[inv_start:inv_end], invitation.replace('VENUE_NAME', VENUE).replace('CREAM', CREAM).replace('GOLD', GOLD))

# ---- 2. The two wedding-day sections become one reception section
start = t.index('  <section data-screen-label="04 Friday"')
end = t.index('  <section data-screen-label="06 Venue"')
days = t[start:end]
reception = '''  <section data-screen-label="04 Reception" style="background:#f4ead8">
    <div style="padding:64px 24px 36px;text-align:center;display:flex;flex-direction:column;align-items:center;gap:4px">
      <div style="font-family:'Imperial Script',cursive;font-weight:400;font-size:58px;line-height:1;color:NAVY_INK">In Delhi</div>
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
        <div style="font-family:'Cormorant Garamond',serif;font-style:italic;font-size:4.4cqw;line-height:1.38;color:#fbe6cc;text-wrap:pretty">An evening of dinner, music and dancing with the newly-weds.</div>
      </div>
    </div>
    <div style="height:56px"></div>
  </section>

'''.replace('TEXT_TOP', a.text_top).replace('NAVY_INK', NAVY_INK)
add(days, reception)

# ---- 3. Venue
add('<img src="e11d75ea-8a51-4255-a3c5-d638c4bf2e2a" alt="Fortune Select Forest Hill" style="width:100%;height:100%;object-fit:cover;display:block">',
    '<img src="__IMG:venue__" alt="%s" style="width:100%%;height:100%%;object-fit:cover;object-position:50%% 100%%;display:block">' % VENUE)  # the 4:5 window keeps the entrance, not the sky
add("font-size:46px;line-height:1.05;color:#7a2a1c\">Fortune Select Forest Hill</div>", "font-size:46px;line-height:1.05;color:%s\">%s</div>" % (NAVY_INK, VENUE))
add('min-height:52px;background:#3b1a12;color:#fbefd9', 'min-height:52px;background:%s;color:#fbefd9' % NAVY)
add('<div style="font-size:19px;font-style:italic">Kasauli, Himachal Pradesh</div>', '<div style="font-size:19px;font-style:italic">%s</div>' % ADDRESS)
add('https://www.google.com/maps?q=Fortune+Select+Forest+Hill+Kasauli&amp;output=embed', 'https://www.google.com/maps?q=%s&amp;output=embed' % MAPS_Q)
add('https://www.google.com/maps/dir/?api=1&amp;destination=Fortune+Select+Forest+Hill+Kasauli', 'https://www.google.com/maps/dir/?api=1&amp;destination=%s' % MAPS_Q)

# ---- 4. RSVP: hosted by the Pahuja family alone; the event is the reception, so no event chips; phone number field; its own saved response
fam_start = t.index('    <div style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:16px;text-align:center;padding-bottom:26px;border-bottom:1px solid rgba(240,201,138,.3)">')
fam_end = t.index('    <sc-if value="{{ submitted }}"')
add(t[fam_start:fam_end], '''    <div style="display:flex;flex-direction:column;align-items:center;gap:6px;text-align:center;padding-bottom:26px;border-bottom:1px solid rgba(240,201,138,.3)">
      <div style="font-family:'Jost',sans-serif;font-weight:500;font-size:11px;letter-spacing:.22em;color:#f0c98a;margin-bottom:4px">THE PAHUJA FAMILY</div>
      <div style="font-size:18px;line-height:1.3">Chanchal Pahuja</div>
      <div style="font-size:18px;line-height:1.3">Ashok Pahuja</div>
      <div style="font-size:18px;line-height:1.3">Shivam Pahuja</div>
      <div style="font-size:18px;line-height:1.3">Jorena Pahuja</div>
    </div>
''')
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
new_cd = new_cd.replace('rgba(30,10,6,.35)', 'rgba(14,18,48,.45)').replace('color:#3b1a12', 'color:' + NAVY)
add(old_cd, new_cd)
add("      heroMedia, countdown, events, yesBg, yesFg, noBg, noFg,",
    "      heroMedia, countdown, events, yesBg, yesFg, noBg, noFg,\n"
    "      hasAlbum: !!this.props.albumUrl, albumUrl: this.props.albumUrl || '#', albumOpen: !!this.props.albumUrl && d <= 0, albumClosed: !(!!this.props.albumUrl && d <= 0),")
add('<div style="position:absolute;left:24px;right:24px;bottom:40px;display:flex;flex-direction:column;align-items:center;gap:18px;color:#fbefd9">',
    '<div style="position:absolute;left:24px;right:24px;bottom:28px;display:flex;flex-direction:column;align-items:center;gap:18px;color:#fbefd9">')

# ---- 6. Night edition: midnight navy and champagne gold in place of maroon and gold paper
# envelope card (Ganesha) ground and type
add('background:radial-gradient(ellipse 90% 70% at 50% 30%,#f3daa0 0%,#ebcd8e 60%,#d9b072 100%)',
    'background:radial-gradient(ellipse 90% 70% at 50% 30%,#1e2756 0%,#151b3f 60%,#0e1230 100%)')
add('height:24%;background:linear-gradient(180deg,rgba(245,222,170,.55) 0%,rgba(245,222,170,0) 100%)',
    'height:24%;background:linear-gradient(180deg,rgba(14,18,48,.72) 0%,rgba(14,18,48,0) 100%)')
add('justify-content:center;gap:2px;color:#6a1e14">', 'justify-content:center;gap:2px;color:%s">' % CREAM)
add('font-size:clamp(13px,1.8svh,16px);color:#8a3a1c;', 'font-size:clamp(13px,1.8svh,16px);color:%s;' % GOLD)
add('font-size:clamp(50px,8svh,74px);line-height:1;color:#6a1e14">Nitya</div>', 'font-size:clamp(50px,8svh,74px);line-height:1;color:%s">Nitya</div>' % CREAM)
add('font-size:clamp(50px,8svh,74px);line-height:1;color:#6a1e14">Anuj</div>', 'font-size:clamp(50px,8svh,74px);line-height:1;color:%s">Anuj</div>' % CREAM)
add('font-size:11px;letter-spacing:.34em;color:#a8682e;text-transform:uppercase">weds</div>', 'font-size:11px;letter-spacing:.34em;color:%s;text-transform:uppercase">weds</div>' % GOLD)
add('width:40px;height:1px;background:#a8682e;margin:clamp(3px,.8svh,8px) 0', 'width:40px;height:1px;background:%s;margin:clamp(3px,.8svh,8px) 0' % GOLD)
add('box-shadow:inset 0 0 0 14px #fbf4e8,inset 0 0 0 15px #d8b98a,inset 0 0 0 19px #fbf4e8,inset 0 0 0 20px #e2c79c',
    'box-shadow:inset 0 0 0 14px #141a3a,inset 0 0 0 15px #e8c88a,inset 0 0 0 19px #141a3a,inset 0 0 0 20px #b8945a')
add('background:linear-gradient(90deg,rgba(255,250,235,0),rgba(255,250,235,.55),rgba(255,250,235,0))',
    'background:linear-gradient(90deg,rgba(255,250,235,0),rgba(255,250,235,.32),rgba(255,250,235,0))')
# plum wax seal
add('background:radial-gradient(circle at 36% 30%,#c45e64 0%,#93303b 55%,#6b1e28 100%)', 'background:radial-gradient(circle at 36% 30%,#a85aa6 0%,#6e2d7c 55%,#481a58 100%)')
add('background:radial-gradient(circle at 40% 35%,#a8414a,#7d2430)', 'background:radial-gradient(circle at 40% 35%,#8a3f92,#5b2468)')
# RSVP and closing card
add('background:linear-gradient(180deg,#f4ead8 0,#3b1a12 130px)', 'background:linear-gradient(180deg,#f4ead8 0,%s 130px)' % NAVY)
add('min-height:54px;background:#f0c98a;color:#3b1a12;border:0', 'min-height:54px;background:#f0c98a;color:%s;border:0' % NAVY)
add('aspect-ratio:9/16;overflow:hidden;background:#1e0a06">', 'aspect-ratio:9/16;overflow:hidden;background:%s">' % NAVY_DEEP)
add('background:linear-gradient(180deg,rgba(20,14,30,.6) 0%,rgba(0,0,0,0) 30%,rgba(0,0,0,0) 58%,rgba(30,10,6,.92) 100%)',
    'background:linear-gradient(180deg,rgba(14,18,48,.84) 0%,rgba(14,18,48,.5) 18%,rgba(0,0,0,0) 36%,rgba(0,0,0,0) 58%,rgba(14,18,48,.94) 100%)')
add('<div style="position:absolute;top:56px;left:0;right:0;text-align:center;color:#fbefd9;display:flex;flex-direction:column;gap:8px">',
    '<div style="position:absolute;top:56px;left:0;right:0;text-align:center;color:#fbefd9;display:flex;flex-direction:column;gap:8px;text-shadow:0 2px 14px rgba(10,12,40,.95),0 0 3px rgba(10,12,40,.8)">')

# closing card: the couple under the chandeliers instead of the hills; scroll hint readable on navy
add('<img src="eb3ecb4f-8d88-4239-8965-bb56815d4b1b" alt="Nitya and Anuj"', '<img src="__IMG:closing__" alt="Nitya and Anuj"')
add('font-size:10px;letter-spacing:.36em;color:#6a1e14">SCROLL DOWN</div>', 'font-size:10px;letter-spacing:.36em;color:%s">SCROLL DOWN</div>' % GOLD)
add('background:linear-gradient(180deg,#6a1e14,rgba(106,30,20,0));animation:bob', 'background:linear-gradient(180deg,%s,rgba(232,200,138,0));animation:bob' % GOLD)

# ---- 7. The wax seal, not a pearl, travels the thread: it leaves the envelope and settles on the string
old_pearl = """  <div ref="{{ pearlRef }}" style="position:absolute;top:0;left:0;width:24px;height:24px;z-index:6;pointer-events:none;will-change:transform;transform:translate(-200px,-200px);opacity:0;transition:opacity 1.2s ease">
    <div style="position:absolute;inset:-14px;border-radius:50%;background:radial-gradient(circle,rgba(255,238,205,.6) 0%,rgba(255,238,205,0) 62%)"></div>
    <div style="position:absolute;inset:0;border-radius:50%;background:radial-gradient(circle at 34% 30%,#ffffff 0%,#fbf6ee 14%,#ece2d3 42%,#cdbca8 74%,#9d8a74 100%);box-shadow:0 8px 14px rgba(40,20,10,.38),inset -3px -4px 7px rgba(110,80,50,.35)"></div>
    <div ref="{{ sheenRef }}" style="position:absolute;inset:0;border-radius:50%;background:conic-gradient(from 0deg,rgba(255,200,220,0),rgba(255,190,215,.32),rgba(190,220,255,.32),rgba(210,255,225,.26),rgba(255,230,190,.32),rgba(255,200,220,0));mix-blend-mode:soft-light"></div>
    <div style="position:absolute;left:5px;top:4px;width:8px;height:6px;border-radius:50%;background:rgba(255,255,255,.95);filter:blur(1px)"></div>
  </div>"""
new_seal = """  <div ref="{{ pearlRef }}" style="position:absolute;top:0;left:0;width:36px;height:36px;z-index:6;pointer-events:none;will-change:transform;transform:translate(-200px,-200px);opacity:0;transition:opacity 1.2s ease">
    <div style="position:absolute;inset:-16px;border-radius:50%;background:radial-gradient(circle,rgba(200,130,210,.4) 0%,rgba(200,130,210,0) 62%)"></div>
    <div style="position:absolute;inset:-2px;border-radius:47% 53% 50% 50% / 52% 46% 54% 48%;background:radial-gradient(circle at 36% 30%,#a85aa6 0%,#6e2d7c 55%,#481a58 100%);box-shadow:0 5px 10px rgba(40,10,50,.45),inset 0 -2px 4px rgba(0,0,0,.25)"></div>
    <div style="position:absolute;inset:3px;border-radius:50%;box-shadow:inset 0 1px 3px rgba(0,0,0,.35),inset 0 -1px 2px rgba(255,200,240,.3);background:radial-gradient(circle at 40% 35%,#8a3f92,#5b2468)"></div>
    <div ref="{{ sheenRef }}" style="position:absolute;inset:-2px;border-radius:50%;background:conic-gradient(from 0deg,rgba(255,255,255,0),rgba(255,255,255,.24),rgba(255,255,255,0) 40%);mix-blend-mode:soft-light"></div>
    <div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;gap:1px;font-family:'Jost',sans-serif;font-weight:500;font-size:12px;line-height:1;color:#f3d9ef;text-shadow:0 1px 1px rgba(0,0,0,.35)">A<span style="font-family:'Cormorant Garamond',serif;font-style:italic;font-size:8px;margin-top:2px">&amp;</span>N</div>
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
for leftover in ('Haldi', 'Sangeet', 'Pheras', 'Afterparty', 'Kasauli', 'Fortune Select'):
    where = [m.start() for m in re.finditer(re.escape(leftover), tt)]
    assert not where or all('sangeetFx' in tt[w - 20:w + 20] for w in where), (leftover, where)
json.dump(P, open(a.out, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
print('wrote', a.out, 'with', len(P), 'edits')
