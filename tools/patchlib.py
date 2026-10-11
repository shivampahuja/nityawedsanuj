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
