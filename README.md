# Nitya weds Anuj

Wedding invitation site, served by GitHub Pages at https://nityawedsanuj.com

- `index.html` is the invitation (a self-contained export from Claude Design, with the images embedded)
- `og.jpg` is the link-preview image shown by WhatsApp and others
- `music.mp3` is the background music (33 s, looped; starts when the envelope is opened)
- `CNAME` tells GitHub Pages the custom domain
- `rsvp/Code.gs` is an alternative RSVP backend (Google Apps Script appending to the AN sheet); the live page posts to a Google Form instead
- `assets/ring.png` is the ring photo shown on the Sangeet evening card (embedded into the page at build time)
- `tools/make_patch.py` generates `tools/content-patch.json`, the copy, layout and behaviour edits applied on top of the export; `tools/build.py` rebuilds `index.html` from a fresh export, setting the title, link-preview tags and the RSVP endpoint:

```
python3 tools/build.py export.html index.html \
  --endpoint https://docs.google.com/forms/d/e/<form id>/formResponse \
  --fields '{"name":"entry.…","phone":"","attending":"entry.…","guests":"entry.…","events":"entry.…","note":"entry.…","submittedAt":""}' \
  --base https://nityawedsanuj.com \
  --patch tools/content-patch.json \
  --music music.mp3 \
  --resource ring=assets/ring.png \
  --album https://drive.google.com/drive/folders/<folder id>
```

The closing card shows the countdown until 2:30 pm IST on 11 December 2026, then replaces it with a button to the shared photo and video folder (`--album`).

A field mapped to an empty string is not sent; `phone` mapped to an empty string is folded into the note as `Phone: …` instead. `tools/content-patch.json` holds the copy and layout edits applied on top of the export.

## Photo wall (`/wall/`)

`wall/index.html` is the screen for the venue: every picture in the shared Drive folder drifts slowly upward in columns, one picture at a time lifts to the middle of the screen and settles back, and new uploads rise into the stream with a gold edge and come forward first. The names, the running count and the QR code sit along the bottom. It adapts to landscape or portrait screens and handles hundreds of pictures (only the tiles on screen are in memory). It lists the folder through the Drive API every minute and needs a Google Cloud API key with the Drive API enabled, restricted to this site. To bake it in: copy `tools/wall.src.html` to `wall/index.src.html` and `tools/wall-fonts.css` to `wall/fonts.css`, then run `python3 tools/wall-assemble.py <key>` from the repository root. `?key=…` tests a key without baking it in, `?demo=1` shows sample images, `?refresh=10` shortens the refresh interval for testing. Press F or click for full screen. Fonts are embedded, so only the Drive calls need the internet.
