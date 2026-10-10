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
  --resource ring=assets/ring.png
```

A field mapped to an empty string is not sent; `phone` mapped to an empty string is folded into the note as `Phone: …` instead. `tools/content-patch.json` holds the copy and layout edits applied on top of the export.
