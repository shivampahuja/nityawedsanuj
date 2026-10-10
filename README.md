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

`wall/index.html` is the screen for the venue: a framed print of the latest upload, a pile of recent prints, and the invitation's QR card. It lists the shared Drive folder through the Drive API every minute. It needs a Google Cloud API key with the Drive API enabled, restricted to this site. To bake it in, run `python3 tools/wall-assemble.py <key>` from the repository root with `tools/wall.src.html`, `tools/wall-fonts.css` and `wall/qr-folder.svg` in place (the script expects them under `wall/`; copy `wall.src.html` and `wall-fonts.css` there first), or pass the key as `?key=…` for a quick test. `?demo=1` shows sample images. Press F or click for full screen. Fonts are embedded, so only the Drive calls need the internet.
