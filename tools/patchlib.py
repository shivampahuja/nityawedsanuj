"""Pieces shared by the patch generators (the kirtan page uses these; the wedding and reception
generators carry their own copies from before this file existed)."""

OLD_COUNTDOWN = """      <div style="font-family:'Jost',sans-serif;font-weight:500;font-size:2.7cqw;letter-spacing:.32em;color:#f0c98a">COUNTING DOWN</div>
      <div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;width:100%">
        <sc-for list="{{ countdown }}" as="u" hint-placeholder-count="4">
          <div style="display:flex;flex-direction:column;align-items:center;gap:8px">
            <div style="width:100%;aspect-ratio:1;border:1px solid rgba(240,201,138,.6);border-radius:50%;background:rgba(30,10,6,.35);display:flex;align-items:center;justify-content:center;font-family:'Jost',sans-serif;font-weight:500;font-size:24px;font-variant-numeric:tabular-nums">{{ u.v }}</div>
            <div style="font-family:'Jost',sans-serif;font-weight:500;font-size:11px;letter-spacing:.22em;color:#e3c79a">{{ u.l }}</div>
          </div>
        </sc-for>
      </div>"""

NEW_COUNTDOWN = """      <sc-if value="{{ albumClosed }}" hint-placeholder-val="{{ true }}">
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

ALBUM_VALS_OLD = "      heroMedia, countdown, events, yesBg, yesFg, noBg, noFg,"
ALBUM_VALS_NEW = ("      heroMedia, countdown, events, yesBg, yesFg, noBg, noFg,\n"
                  "      hasAlbum: !!this.props.albumUrl, albumUrl: this.props.albumUrl || '#', albumOpen: !!this.props.albumUrl && d <= 0, albumClosed: !(!!this.props.albumUrl && d <= 0),")

FOOT_OLD = '<div style="position:absolute;left:24px;right:24px;bottom:40px;display:flex;flex-direction:column;align-items:center;gap:18px;color:#fbefd9">'
FOOT_NEW = '<div style="position:absolute;left:24px;right:24px;bottom:28px;display:flex;flex-direction:column;align-items:center;gap:18px;color:#fbefd9">'

OLD_PEARL = """  <div ref="{{ pearlRef }}" style="position:absolute;top:0;left:0;width:24px;height:24px;z-index:6;pointer-events:none;will-change:transform;transform:translate(-200px,-200px);opacity:0;transition:opacity 1.2s ease">
    <div style="position:absolute;inset:-14px;border-radius:50%;background:radial-gradient(circle,rgba(255,238,205,.6) 0%,rgba(255,238,205,0) 62%)"></div>
    <div style="position:absolute;inset:0;border-radius:50%;background:radial-gradient(circle at 34% 30%,#ffffff 0%,#fbf6ee 14%,#ece2d3 42%,#cdbca8 74%,#9d8a74 100%);box-shadow:0 8px 14px rgba(40,20,10,.38),inset -3px -4px 7px rgba(110,80,50,.35)"></div>
    <div ref="{{ sheenRef }}" style="position:absolute;inset:0;border-radius:50%;background:conic-gradient(from 0deg,rgba(255,200,220,0),rgba(255,190,215,.32),rgba(190,220,255,.32),rgba(210,255,225,.26),rgba(255,230,190,.32),rgba(255,200,220,0));mix-blend-mode:soft-light"></div>
    <div style="position:absolute;left:5px;top:4px;width:8px;height:6px;border-radius:50%;background:rgba(255,255,255,.95);filter:blur(1px)"></div>
  </div>"""

def seal(outer='#c45e64 0%,#93303b 55%,#6b1e28 100%', inner='#a8414a,#7d2430', glow='255,205,190', ink='#fbe3d6'):
    """The wax seal that travels the thread, in the page's seal colours."""
    tpl = """  <div ref="{{ pearlRef }}" style="position:absolute;top:0;left:0;width:36px;height:36px;z-index:6;pointer-events:none;will-change:transform;transform:translate(-200px,-200px);opacity:0;transition:opacity 1.2s ease">
    <div style="position:absolute;inset:-16px;border-radius:50%;background:radial-gradient(circle,rgba(GLOW,.42) 0%,rgba(GLOW,0) 62%)"></div>
    <div style="position:absolute;inset:-2px;border-radius:47% 53% 50% 50% / 52% 46% 54% 48%;background:radial-gradient(circle at 36% 30%,OUTER);box-shadow:0 5px 10px rgba(60,15,25,.45),inset 0 -2px 4px rgba(0,0,0,.25)"></div>
    <div style="position:absolute;inset:3px;border-radius:50%;box-shadow:inset 0 1px 3px rgba(0,0,0,.35),inset 0 -1px 2px rgba(255,200,200,.35);background:radial-gradient(circle at 40% 35%,INNER)"></div>
    <div ref="{{ sheenRef }}" style="position:absolute;inset:-2px;border-radius:50%;background:conic-gradient(from 0deg,rgba(255,255,255,0),rgba(255,255,255,.24),rgba(255,255,255,0) 40%);mix-blend-mode:soft-light"></div>
    <div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;gap:1px;font-family:'Jost',sans-serif;font-weight:500;font-size:12px;line-height:1;color:INK;text-shadow:0 1px 1px rgba(0,0,0,.35)">A<span style="font-family:'Cormorant Garamond',serif;font-style:italic;font-size:8px;margin-top:2px">&amp;</span>N</div>
  </div>"""
    return tpl.replace('GLOW', glow).replace('OUTER', outer).replace('INNER', inner).replace('INK', ink)

HANDOFF_OLD = "    this.pearlRef.current.style.transform = 'translate(' + (q.x - 12) + 'px,' + (q.y - 12 + bob) + 'px)';"
HANDOFF_NEW = """    let px = q.x - 18, py = q.y - 18 + bob;
    if (this.state.revealed && !this.handoffDone) {  // the seal leaves the envelope and settles on the thread
      if (!this.handoffT0) this.handoffT0 = ts;
      const k = Math.min(1, (ts - this.handoffT0) / 1500), e = 1 - Math.pow(1 - k, 3);
      const s0 = root.children[0], sx = root.offsetWidth / 2 - 18, sy = s0.offsetHeight / 2 + s0.offsetWidth * .034 - 18;
      px = sx + (px - sx) * e; py = sy + (py - sy) * e;
      if (k >= 1) this.handoffDone = true;
    }
    this.pearlRef.current.style.transform = 'translate(' + px + 'px,' + py + 'px)';"""

PATH_START_OLD, PATH_START_NEW = "const pts = [{ x: W / 2, y: secs[0].offsetHeight - 46 }];", "const pts = [{ x: W / 2, y: secs[0].offsetHeight - 96 }];"
PATH_END_OLD, PATH_END_NEW = "pts.push({ x: W / 2, y: last.offsetTop + 160 });", "pts.push({ x: W / 2, y: last.offsetTop + 200 });"


# ---------------------------------------------------------------------------------------------
# One type scale for all three pages. The design export sets its leading tight (1.2 to 1.38) and
# lets some lines run at the browser default; these rules open every multi-line setting up to the
# same values, so the pages read alike:
#   running text in Cormorant Garamond ........ line-height 1.5
#   date, venue and address lines ............. line-height 1.45, balanced wrapping
#   script headings that can wrap (venue) ..... line-height 1.15, balanced wrapping
#   lists of names ............................ line-height 1.4
# They run last, on the patched text, so they reach the blocks each generator writes itself.

TYPE_RULES = [
    # (pattern, replacement, min matches, max matches)
    (r'font-size:3\.7cqw;line-height:1\.35;text-wrap:balance">With the blessings', 'font-size:3.7cqw;line-height:1.5;text-wrap:balance">With the blessings', 1, 1),
    (r'font-style:italic;font-size:4\.4cqw;line-height:1\.38;', 'font-style:italic;font-size:4.4cqw;line-height:1.5;', 1, 3),   # the event cards
    (r'font-style:italic;font-size:3\.5cqw;line-height:1\.3;', 'font-style:italic;font-size:3.5cqw;line-height:1.5;', 0, 2),    # Varmala and Pheras
    (r'font-size:3\.2cqw;line-height:1\.3;color:#4a1410">Pastels', 'font-size:3.2cqw;line-height:1.5;color:#4a1410">Pastels', 0, 1),
    (r'font-size:46px;line-height:1\.05;color:', 'font-size:46px;line-height:1.15;text-wrap:balance;color:', 1, 1),               # venue name
    (r'<div style="font-size:19px;font-style:italic">', '<div style="font-size:19px;line-height:1.45;font-style:italic;text-wrap:balance">', 1, 1),  # address
    (r'<div style="font-size:18px;line-height:1\.3">', '<div style="font-size:18px;line-height:1.4">', 0, 8),                    # RSVP hosts
    (r'<div style="font-style:italic;font-size:22px;color:', '<div style="font-style:italic;font-size:22px;line-height:1.45;color:', 1, 1),  # closing line
    (r'(top:56px;left:0;right:0;text-align:center;color:#[0-9a-f]{6};display:flex;flex-direction:column;gap:)8px', r'\g<1>10px', 1, 1),
    (r"font-style:italic;font-size:2[24]px;line-height:1\.(?:35|4);color:#7a2a1c(?:;max-width:330px)?\">", "font-style:italic;font-size:22px;line-height:1.5;color:#7a2a1c;max-width:330px;text-wrap:balance\">", 0, 1),  # the note under a day
    (r'font-size:15px;line-height:1\.35;color:#e3c79a', 'font-size:15px;line-height:1.5;color:#e3c79a', 1, 1),                   # album note
    (r'font-size:11px;letter-spacing:\.2em;color:(#[0-9a-f]{6})">', r'font-size:11px;line-height:1.6;letter-spacing:.2em;color:\1">', 1, 1),  # date line on the opening card, if it wraps
]

def type_polish(tt):
    """Apply TYPE_RULES to the patched template text; returns the exact-text edits (find, replace, count) for build.py."""
    import re
    edits = []
    for pat, repl, lo, hi in TYPE_RULES:
        found = {}
        for m in re.finditer(pat, tt):
            found.setdefault(m.group(0), 0); found[m.group(0)] += 1
        total = sum(found.values())
        assert lo <= total <= hi, 'type rule %r matched %d times, expected %d..%d' % (pat[:50], total, lo, hi)
        for text, n in found.items():
            edits.append((text, re.sub(pat, repl, text), n))
    return edits


def ik_onkar_svg(height_css, color='currentColor'):
    """Inline SVG of the Ik Onkar glyph, traced from GNU FreeSerif so it renders the same on every device."""
    from fontTools.ttLib import TTFont
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.boundsPen import BoundsPen
    f = TTFont('/usr/share/fonts/truetype/freefont/FreeSerif.ttf')
    g = f.getBestCmap()[0x0A74]; gs = f.getGlyphSet()
    pen = SVGPathPen(gs); gs[g].draw(pen)
    bp = BoundsPen(gs); gs[g].draw(bp); x0, y0, x1, y1 = bp.bounds
    return ('<svg viewBox="%d %d %d %d" style="height:HEIGHT;width:auto;display:block" aria-label="Ik Onkar" role="img">'
            '<path transform="translate(0,%d) scale(1,-1)" d="%s" fill="%s"/></svg>'
            % (x0 - 20, y0 - 20, x1 - x0 + 40, y1 - y0 + 40, y0 + y1, pen.getCommands(), color)).replace('HEIGHT', height_css)


# ---------------------------------------------------------------------------------------------
# Openers that replace the envelope: a rumala that lifts (kirtan) and a room whose lights come on
# (reception). Both show the card full-bleed from the start, under a cover that the tap removes.

NOISE = ("url('data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22200%22%20height%3D%22200%22%3E%3Cfilter%20id%3D%22n%22%3E"
         "%3CfeTurbulence%20type%3D%22fractalNoise%22%20baseFrequency%3D%22.9%22%20numOctaves%3D%222%22%20stitchTiles%3D%22stitch%22%2F%3E%3CfeColorMatrix%20values%3D"
         "%220%200%200%200%20.45%20%200%200%200%200%20.35%20%200%200%200%200%20.25%20%200%200%200%20.16%200%22%2F%3E%3C%2Ffilter%3E%3Crect%20width%3D%22100%25%22%20height%3D%22100%25%22%20filter%3D%22url(%23n)%22%2F%3E%3C%2Fsvg%3E')")

OPENER_KEYFRAMES = ("@keyframes clothLift{0%,12%{transform:translateY(0)}100%{transform:translateY(-108%)}}\n"
                    "@keyframes cardBreathe{0%,30%{transform:scale(1.06)}100%{transform:scale(1)}}\n"
                    "@keyframes lightsUp{0%,14%{opacity:1}100%{opacity:0}}\n"
                    "@keyframes glowIn{0%,18%{opacity:0}62%{opacity:1}100%{opacity:.6}}\n"
                    "@keyframes sparkIn{0%,45%{opacity:0}100%{opacity:1}}\n")

STYLE_ANCHOR = "input,textarea{font:inherit}"

REVEAL_OLD = "}, 5300);\n    clearTimeout(this.autoOpen);"
REVEAL_NEW = "}, 3300);\n    clearTimeout(this.autoOpen);"

VALS_OLD = """      cardAnim: op ? 'cardOut 5.4s cubic-bezier(.55,0,.25,1) forwards' : 'none',
      tiltAnim: op ? 'cardTilt 5.4s ease-in-out forwards' : 'none',
      shadowAnim: op ? 'cardShadow 5.4s ease forwards' : 'none',
      marginAnim: op ? 'margins 5.4s ease forwards' : 'none',
      glintAnim: op ? 'glint 5.4s ease-in-out forwards' : 'none',
      envAnim: op ? 'envDrop 5.4s cubic-bezier(.5,0,.3,1) forwards' : 'none',
      flapFrontAnim: op ? 'flapFront 5.4s cubic-bezier(.4,0,.2,1) forwards' : 'none',
      flapBackAnim: op ? 'flapBack 5.4s cubic-bezier(.2,0,.3,1) forwards' : 'none',
      sealAnim: op ? 'sealPop 5.4s cubic-bezier(.3,0,.3,1) forwards' : 'none',"""

def opener_vals(kind):
    cover = {'rumala': "'clothLift 2.8s cubic-bezier(.7,0,.2,1) forwards'", 'lights': "'lightsUp 2.6s ease-in-out forwards'"}[kind]
    return """      cardAnim: op ? 'cardBreathe 3.4s cubic-bezier(.2,.6,.2,1) forwards' : 'none',
      tiltAnim: 'none',
      shadowAnim: 'none',
      marginAnim: op ? 'margins 3.6s ease forwards' : 'none',
      glintAnim: op ? 'glint 3.2s ease-in-out forwards' : 'none',
      envAnim: op ? %s : 'none',
      flapFrontAnim: op ? 'glowIn 3s ease-out forwards' : 'none',
      flapBackAnim: op ? 'sparkIn 3s ease forwards' : 'none',
      sealAnim: op ? 'sealPop 2.4s cubic-bezier(.3,0,.3,1) forwards' : 'none',""" % cover


def ampersand(color):
    """The script ampersand that joins the names once they are married (the reception page)."""
    return "<div style=\"font-family:'Imperial Script',cursive;font-weight:400;font-size:clamp(30px,4.8svh,44px);line-height:1;color:%s\">&amp;</div>" % color


def opener_section(kind, invocation, names_color, label_color, date_text, ground, top_fade, margins, scroll_color,
                   hint_color, glint_alpha='.55', cover_html='', seal_html='', conj_html=None):
    """The 01 Opening section. `invocation` is the html above the names (Ik Onkar svg or the Devanagari line);
    `cover_html` is what hides the card until the tap (rumala or dark veil), `seal_html` an optional seal at the centre;
    `conj_html` is what sits between the names (default: the small 'weds' label)."""
    if conj_html is None:
        conj_html = "<div style=\"font-family:'Jost',sans-serif;font-weight:500;font-size:11px;letter-spacing:.34em;color:LABEL;text-transform:uppercase\">weds</div>"
    return '''  <section data-screen-label="01 Opening" style="position:relative;height:100svh;min-height:620px;max-height:900px;overflow:hidden;container-type:size;background:#0e1230">
    <div style="position:absolute;inset:0;z-index:2;transform-origin:50% 50%;animation:{{ cardAnim }}">
      <div style="position:absolute;inset:0;background:GROUND">
        {{ heroMedia }}
        <div style="position:absolute;left:0;right:0;top:0;height:24%;background:linear-gradient(180deg,TOP_FADE 0%,TOP_FADE_0 100%)"></div>
        <div style="position:absolute;top:0;left:0;right:0;height:clamp(150px,21%,210px);padding:8px 20px 0;text-align:center;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;color:NAMES">
          INVOCATION
          <div style="display:flex;align-items:baseline;justify-content:center;gap:12px;flex-wrap:wrap">
          <div style="font-family:'Imperial Script',cursive;font-weight:400;font-size:clamp(50px,8svh,74px);line-height:1;color:NAMES">Nitya</div>
          CONJ
          <div style="font-family:'Imperial Script',cursive;font-weight:400;font-size:clamp(50px,8svh,74px);line-height:1;color:NAMES">Anuj</div>
        </div>
          <div style="width:40px;height:1px;background:LABEL;margin:clamp(3px,.8svh,8px) 0"></div>
          <div style="font-family:'Jost',sans-serif;font-weight:500;font-size:11px;letter-spacing:.2em;color:LABEL">DATE_TEXT</div>
        </div>
        <div style="position:absolute;inset:0;box-shadow:MARGINS;animation:{{ marginAnim }}"></div>
        <div style="position:absolute;top:0;bottom:0;left:0;width:40%;background:linear-gradient(90deg,rgba(255,250,235,0),rgba(255,250,235,GLINT),rgba(255,250,235,0));opacity:0;animation:{{ glintAnim }}"></div>
      </div>
    </div>
COVER
SEAL
    <div sc-camel-on-click="{{ openCurtain }}" style="position:absolute;inset:0;z-index:4;pointer-events:{{ curtainPE }};cursor:pointer;opacity:{{ tapOpacity }};transition:opacity .6s ease">
      <div style="position:absolute;left:0;right:0;top:calc(50cqh + 60px);text-align:center;font-family:'Jost',sans-serif;font-weight:500;font-size:11px;letter-spacing:.34em;color:HINT;animation:bob 2.4s ease-in-out infinite">TAP TO BEGIN</div>
    </div>
    <div style="position:absolute;left:0;right:0;bottom:16px;z-index:5;display:flex;flex-direction:column;align-items:center;gap:4px;pointer-events:none;opacity:{{ scrollHintO }};transition:opacity 1.2s ease">
      <div style="font-family:'Jost',sans-serif;font-weight:500;font-size:10px;letter-spacing:.36em;color:SCROLL_COLOR">SCROLL DOWN</div>
      <div style="width:1px;height:22px;background:linear-gradient(180deg,SCROLL_COLOR,rgba(0,0,0,0));animation:bob 2.2s ease-in-out infinite"></div>
    </div>
  </section>

'''.replace('GROUND', ground).replace('TOP_FADE_0', top_fade.replace(',.72)', ',0)').replace(',.55)', ',0)')).replace('TOP_FADE', top_fade) \
   .replace('INVOCATION', invocation).replace('CONJ', conj_html).replace('NAMES', names_color).replace('LABEL', label_color).replace('DATE_TEXT', date_text) \
   .replace('MARGINS', margins).replace('GLINT', glint_alpha).replace('COVER', cover_html).replace('SEAL', seal_html) \
   .replace('HINT', hint_color).replace('SCROLL_COLOR', scroll_color)


def rumala_cover(emblem_html):
    """A saffron silk cloth with a zari hem and a fringe, the Ik Onkar embroidered at its centre; it lifts on the tap."""
    return '''    <div style="position:absolute;inset:0;z-index:3;pointer-events:none;animation:{{ envAnim }}">
      <div style="position:absolute;inset:0;background-image:NOISE,linear-gradient(168deg,#ec9436 0%,#dd7b22 55%,#c96a1c 100%);box-shadow:0 26px 60px rgba(60,30,10,.4)">
        <div style="position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(255,255,255,0) 0 7px,rgba(255,240,200,.07) 7px 8px),repeating-linear-gradient(90deg,rgba(255,255,255,0) 0 7px,rgba(120,50,0,.06) 7px 8px)"></div>
        <div style="position:absolute;left:0;right:0;bottom:0;height:30px;background:repeating-linear-gradient(90deg,#f6dc8f 0 5px,#c9a25e 5px 10px);box-shadow:0 -1px 0 #f6dc8f,0 -5px 0 #c9a25e,0 -6px 0 #f6dc8f"></div>
        <div style="position:absolute;left:0;right:0;top:100%;height:26px;background:repeating-linear-gradient(90deg,#e6bf66 0 3px,rgba(0,0,0,0) 3px 9px)"></div>
        <div style="position:absolute;left:50%;top:44%;transform:translate(-50%,-50%);color:#fff1c4;filter:drop-shadow(0 2px 2px rgba(110,50,0,.45))">EMBLEM</div>
      </div>
    </div>'''.replace('NOISE', NOISE).replace('EMBLEM', emblem_html)


def lights_cover():
    """Darkness that lifts, a warm glow that blooms at the top and a few chandelier glints that keep twinkling."""
    sparks = ''.join('<div style="position:absolute;left:%d%%;top:%d%%;width:14px;height:14px;animation:twinkle %ss ease-in-out %ss infinite;opacity:0">'
                     '<div style="position:absolute;left:6px;top:0;width:2px;height:14px;background:linear-gradient(transparent,#fff,transparent)"></div>'
                     '<div style="position:absolute;top:6px;left:0;height:2px;width:14px;background:linear-gradient(90deg,transparent,#fff,transparent)"></div></div>'
                     % (x, y, d, s) for x, y, d, s in [(14, 6, 2.6, 0), (31, 12, 3.1, .8), (52, 4, 2.4, 1.5), (70, 10, 2.9, .4), (86, 7, 2.5, 1.9), (42, 18, 3.4, 2.3), (62, 16, 2.7, 1.1)])
    return '''    <div style="position:absolute;inset:0;z-index:3;pointer-events:none">
      <div style="position:absolute;inset:0;opacity:0;animation:{{ flapBackAnim }}">SPARKS</div>
      <div style="position:absolute;inset:0;background:radial-gradient(ellipse 85% 48% at 50% 0%,rgba(255,214,150,.5) 0%,rgba(255,214,150,0) 72%);opacity:0;animation:{{ flapFrontAnim }}"></div>
      <div style="position:absolute;inset:0;background:#0b0f2a;animation:{{ envAnim }}"></div>
    </div>'''.replace('SPARKS', sparks)


def centre_seal(outer, inner):
    """The wax seal at the centre of the dark card, which pops as the lights come on."""
    return '''    <div style="position:absolute;left:50%;top:50%;width:80px;height:80px;transform:translate(-50%,-50%);z-index:3;pointer-events:none;animation:{{ sealAnim }}">
      <div style="position:absolute;inset:-5px;border-radius:47% 53% 50% 50% / 52% 46% 54% 48%;background:radial-gradient(circle at 36% 30%,OUTER);box-shadow:0 6px 14px rgba(0,0,0,.5),0 0 40px rgba(200,130,210,.25),inset 0 -3px 6px rgba(0,0,0,.25)"></div>
      <div style="position:absolute;inset:7px;border-radius:50%;box-shadow:inset 0 2px 4px rgba(0,0,0,.35),inset 0 -1px 2px rgba(255,190,240,.35);background:radial-gradient(circle at 40% 35%,INNER)"></div>
      <div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;gap:1px;font-family:'Jost',sans-serif;font-weight:500">
        <span style="font-size:27px;background:linear-gradient(135deg,#fbe3f3 0%,#e7a9d9 28%,#b76eaa 52%,#f3c7e6 74%,#a35d9a 100%);-webkit-background-clip:text;background-clip:text;color:transparent">A</span><span style="font-size:15px;font-style:italic;font-family:'Cormorant Garamond',serif;background:linear-gradient(135deg,#fbe3f3 0%,#e7a9d9 28%,#b76eaa 52%,#f3c7e6 74%,#a35d9a 100%);-webkit-background-clip:text;background-clip:text;color:transparent;margin-top:4px">&amp;</span><span style="font-size:27px;background:linear-gradient(135deg,#fbe3f3 0%,#e7a9d9 28%,#b76eaa 52%,#f3c7e6 74%,#a35d9a 100%);-webkit-background-clip:text;background-clip:text;color:transparent">N</span>
      </div>
    </div>'''.replace('OUTER', outer).replace('INNER', inner)
