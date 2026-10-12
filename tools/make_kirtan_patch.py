#!/usr/bin/env python3
"""Generate kirtan-patch.json: turns the Claude Design export of the wedding invitation into the
kirtan and langar invitation (nityawedsanuj.com/kirtan). Applied by tools/build.py --patch.
    make_kirtan_patch.py EXPORT_HTML OUT_JSON
Pictures are referenced as __IMG:invite__, __IMG:kirtan__, __IMG:langar__, __IMG:venue__ and
__IMG:closing__ (build.py --image); the envelope card's picture is the "ganesha" resource.
No RSVP on this page."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patchlib as L

src, out = sys.argv[1], sys.argv[2]
lines = open(src, encoding='utf-8').read().split('\n')
ti = next(i for i, l in enumerate(lines) if l.strip() == '<script type="__bundler/template">') + 1
t = json.loads(lines[ti])

P = []
def add(find, replace, count=1):
    n = t.count(find)
    assert n == count, 'expected %d match(es), found %d: %r' % (count, n, find[:80])
    P.append({'find': find, 'replace': replace, 'count': count})

VENUE = 'Gurudwara Nanak Piao Sahib'
ADDRESS = 'G.T. Karnal Road, Rana Pratap Bagh, Delhi 110033'
MAPS_Q = 'Gurudwara+Nanak+Piao+Sahib,+G.T.+Karnal+Road,+Rana+Pratap+Bagh,+Delhi+110033'

# ---- 1. Opening: no envelope; a saffron rumala with Ik Onkar embroidered on it lifts to reveal the card
op_start = t.index('  <section data-screen-label="01 Opening"')
op_end = t.index('  <section data-screen-label="02 Invitation"')
invocation = '<div style="height:clamp(22px,3.2svh,30px);color:#8a3a1c;margin-bottom:clamp(2px,.8svh,8px);display:flex;justify-content:center">%s</div>' % L.ik_onkar_svg('100%')
opener = L.opener_section('rumala', invocation, names_color='#6a1e14', label_color='#a8682e',
                          date_text='KIRTAN &amp; LANGAR · 6 DECEMBER 2026 · DELHI',
                          ground='radial-gradient(ellipse 90% 70% at 50% 30%,#f3daa0 0%,#ebcd8e 60%,#d9b072 100%)',
                          top_fade='rgba(245,222,170,.55)',
                          margins='inset 0 0 0 14px #fbf4e8,inset 0 0 0 15px #d8b98a,inset 0 0 0 19px #fbf4e8,inset 0 0 0 20px #e2c79c',
                          scroll_color='#6a1e14', hint_color='#fff1c4',
                          cover_html=L.rumala_cover(L.ik_onkar_svg('22cqw')))
add(t[op_start:op_end], opener)
add(L.STYLE_ANCHOR, L.OPENER_KEYFRAMES + L.STYLE_ANCHOR)
add(L.VALS_OLD, L.opener_vals('rumala'))
add(L.REVEAL_OLD, L.REVEAL_NEW)

# ---- 2. Invitation: the gurudwara, with the invitation beneath it
inv_start = t.index('  <section data-screen-label="02 Invitation"')
inv_end = t.index('  <section data-screen-label="04 Friday"')
invitation = '''  <section data-screen-label="02 Invitation" style="position:relative;aspect-ratio:9/19;overflow:hidden;background:#f1e6d2;container-type:inline-size">
    <img src="__IMG:invite__" alt="VENUE_NAME" style="width:100%;height:100%;object-fit:cover;object-position:50% 0%;display:block">
    <div style="position:absolute;left:11%;right:11%;top:64%;bottom:0;text-align:center;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2.4cqw;color:#4a2216">
      <div style="height:6cqw;color:#a8682e;display:flex;justify-content:center">IK_ONKAR</div>
      <p style="margin:0;font-family:'Cormorant Garamond',serif;font-size:3.7cqw;line-height:1.35;text-wrap:balance">With the blessings of our elders and of our beloved mother Chanchal Pahuja, who is always with us, the Pahuja family invites you to a kirtan and langar in prayer for the wedding of</p>
      <div style="font-family:'Imperial Script',cursive;font-weight:400;font-size:13cqw;line-height:1;color:#6a1e14">Nitya &amp; Anuj</div>
      <div style="display:flex;flex-direction:column;align-items:center;gap:1.2cqw">
        <div style="font-family:'Cormorant Garamond',serif;font-size:3.6cqw;line-height:1.45;text-wrap:balance">Sunday 6 December 2026</div>
        <div style="font-family:'Cormorant Garamond',serif;font-size:3.6cqw;line-height:1.45;font-style:italic;text-wrap:balance;color:#8a4a3a">VENUE_NAME, Delhi</div>
      </div>
    </div>
  </section>

'''.replace('VENUE_NAME', VENUE).replace('IK_ONKAR', L.ik_onkar_svg('100%'))
add(t[inv_start:inv_end], invitation)

# ---- 3. The two wedding-day sections become the Sunday: kirtan, then langar
start = t.index('  <section data-screen-label="04 Friday"')
end = t.index('  <section data-screen-label="06 Venue"')
def card(img, alt, title, time, line, top, title_size='24cqw'):
    return '''    <div style="position:relative;aspect-ratio:9/16;overflow:hidden;container-type:inline-size">
      <img src="%s" alt="%s" style="width:100%%;height:100%%;object-fit:cover;display:block">
      <div style="position:absolute;left:12%%;right:12%%;top:%s;text-align:center;display:flex;flex-direction:column;align-items:center;gap:3cqw">
        <div style="display:flex;flex-direction:column;align-items:center;gap:0">
          <div style="font-family:'Imperial Script',cursive;font-weight:400;font-size:%s;line-height:.95;color:#7a2a14;text-shadow:0 2px 14px rgba(0,0,0,.08)">%s</div>
          <div style="display:flex;align-items:center;gap:10px;margin-top:2px">
            <div style="width:6cqw;height:1px;background:#a8551c"></div>
            <div style="font-family:'Jost',sans-serif;font-weight:500;font-size:2.7cqw;letter-spacing:.32em;color:#a8551c">%s</div>
            <div style="width:6cqw;height:1px;background:#a8551c"></div>
          </div>
        </div>
        <div style="font-family:'Cormorant Garamond',serif;font-style:italic;font-size:4.4cqw;line-height:1.38;color:#5a2410;text-wrap:pretty">%s</div>
      </div>
    </div>
''' % (img, alt, top, title_size, title, time, line)
sunday = '''  <section data-screen-label="04 Sunday" style="background:#f4ead8">
    <div style="padding:64px 24px 36px;text-align:center;display:flex;flex-direction:column;align-items:center;gap:4px">
      <div style="font-family:'Imperial Script',cursive;font-weight:400;font-size:58px;line-height:1;color:#7a2a1c">In Delhi</div>
      <div style="font-family:'Jost',sans-serif;font-weight:500;font-size:12px;letter-spacing:.34em;color:#a8682e">SUNDAY, 6 DECEMBER</div>
    </div>
''' + card('__IMG:kirtan__', 'Kirtan', 'Kirtan', '11:30 AM TO 1:30 PM',
           'Shabad kirtan in the Darbar Sahib: the wedding week begins with a prayer.', '30%') \
  + card('__IMG:langar__', 'Langar', 'Langar', '1:30 PM ONWARDS',
         'Lunch from the Guru’s kitchen, served to everyone seated together.', '8%') + '''    <div style="padding:44px 32px;text-align:center;display:flex;flex-direction:column;align-items:center;gap:10px">
      <div style="width:40px;height:1px;background:#a8682e"></div>
      <div style="font-family:'Cormorant Garamond',serif;font-style:italic;font-size:22px;line-height:1.4;color:#7a2a1c;max-width:330px">Please cover your head inside the gurudwara and leave your shoes at the entrance. Scarves are available there.</div>
      <div style="width:40px;height:1px;background:#a8682e"></div>
    </div>
  </section>

'''
add(t[start:end], sunday)

# ---- 4. Venue
add('<img src="e11d75ea-8a51-4255-a3c5-d638c4bf2e2a" alt="Fortune Select Forest Hill" style="width:100%;height:100%;object-fit:cover;display:block">',
    '<img src="__IMG:venue__" alt="%s" style="width:100%%;height:100%%;object-fit:cover;object-position:50%% 0%%;display:block">' % VENUE)
add("font-size:46px;line-height:1.05;color:#7a2a1c\">Fortune Select Forest Hill</div>", "font-size:46px;line-height:1.05;color:#7a2a1c\">%s</div>" % VENUE)
add('<div style="font-size:19px;font-style:italic">Kasauli, Himachal Pradesh</div>', '<div style="font-size:19px;font-style:italic">%s</div>' % ADDRESS)
add('https://www.google.com/maps?q=Fortune+Select+Forest+Hill+Kasauli&amp;output=embed', 'https://www.google.com/maps?q=%s&amp;output=embed' % MAPS_Q)
add('https://www.google.com/maps/dir/?api=1&amp;destination=Fortune+Select+Forest+Hill+Kasauli', 'https://www.google.com/maps/dir/?api=1&amp;destination=%s' % MAPS_Q)

# ---- 5. No RSVP on this page
rs = t.index('  <section data-screen-label="07 RSVP"')
re_ = t.index('  <section data-screen-label="08 Closing"')
add(t[rs:re_], '')
add("ev: { Haldi: true, Sangeet: true, Varmala: true, Pheras: true, Afterparty: true }", "ev: {}")
add("See you in Kasauli.", "See you in Delhi.")
add("localStorage.getItem('na-rsvp')", "localStorage.getItem('na-rsvp-kirtan')")
add("localStorage.setItem('na-rsvp',", "localStorage.setItem('na-rsvp-kirtan',")

# ---- 6. Closing: the well, dark type on the light picture, countdown to the kirtan, the album folder
add('<img src="eb3ecb4f-8d88-4239-8965-bb56815d4b1b" alt="Nitya and Anuj"', '<img src="__IMG:closing__" alt="The well at Nanak Piao"')
add('background:linear-gradient(180deg,rgba(20,14,30,.6) 0%,rgba(0,0,0,0) 30%,rgba(0,0,0,0) 58%,rgba(30,10,6,.92) 100%)',
    'background:linear-gradient(180deg,rgba(0,0,0,0) 0%,rgba(0,0,0,0) 56%,rgba(30,10,6,.94) 100%)')
add('<div style="position:absolute;top:56px;left:0;right:0;text-align:center;color:#fbefd9;display:flex;flex-direction:column;gap:8px">',
    '<div style="position:absolute;top:56px;left:0;right:0;text-align:center;color:#6a1e14;display:flex;flex-direction:column;gap:8px">')
add('<div style="font-style:italic;font-size:22px;color:#f3dcb4">We can\'t wait to celebrate with you</div>',
    '<div style="font-style:italic;font-size:22px;color:#8a4a3a">We can\'t wait to celebrate with you</div>')
add("Date.parse('2026-12-11T14:30:00+05:30')", "Date.parse('2026-12-06T11:30:00+05:30')")
add(L.OLD_COUNTDOWN, L.NEW_COUNTDOWN)
add(L.ALBUM_VALS_OLD, L.ALBUM_VALS_NEW)
add(L.FOOT_OLD, L.FOOT_NEW)

# ---- 7. The wax seal travels the thread
add(L.OLD_PEARL, L.seal())
add(L.HANDOFF_OLD, L.HANDOFF_NEW)
add(L.PATH_START_OLD, L.PATH_START_NEW)
add(L.PATH_END_OLD, L.PATH_END_NEW)

# validate sequential application, then the type scale shared by every page
tt = t
for p in P:
    assert tt.count(p['find']) == p['count'], p['find'][:80]
    tt = tt.replace(p['find'], p['replace'])
for find, replace, count in L.type_polish(tt):
    P.append({'find': find, 'replace': replace, 'count': count}); tt = tt.replace(find, replace)
for leftover in ('Haldi', 'Sangeet', 'Pheras', 'Afterparty', 'Kasauli', 'Fortune Select', 'गणेशाय', '>RSVP<', 'KINDLY RESPOND'):
    where = [m.start() for m in re.finditer(re.escape(leftover), tt)]
    assert not where or all('sangeetFx' in tt[w - 20:w + 20] for w in where), (leftover, [tt[w - 60:w + 40] for w in where][:3])
json.dump(P, open(out, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
print('wrote', out, 'with', len(P), 'edits')
