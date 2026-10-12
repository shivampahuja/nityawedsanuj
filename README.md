# Nitya weds Anuj

Wedding invitation site, served by GitHub Pages at https://nityawedsanuj.com

- `index.html` is the invitation (a self-contained export from Claude Design, with the images embedded)
- `og.jpg` is the link-preview image shown by WhatsApp and others
- `music.mp3` is the background music: the first 90 s of Lost in Love by Tech Panda & Kenzani (faded, level-matched, looped; starts when the envelope is opened)
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

`wall/index.html` is the screen for the venue: every picture in the shared Drive folder drifts slowly upward in columns, one picture at a time lifts to the middle of the screen and settles back, and new uploads rise into the stream with a gold edge and come forward first. The names, the running count and the QR code sit along the bottom. It adapts to landscape or portrait screens and handles hundreds of pictures (only the tiles on screen are in memory). It lists the folder through the Drive API every minute and needs a Google Cloud API key with the Drive API enabled, restricted to this site. The key is baked in with `python3 tools/wall-assemble.py <key>` from the repository root (the QR code is generated at the same time; `--folder ID --out reception/wall/index.html` builds the reception wall at `/reception/wall/`, which reads the `reception` sub-folder of the shared folder) (restricted to this site and to the Drive API, so it is safe in the page source). If the key, its restrictions or the API are set up wrong, the screen shows Google's own error line instead of photos. `?key=…` tests a key without baking it in, `?demo=1` shows sample images, `?refresh=10` shortens the refresh interval for testing. Press F or click for full screen. Fonts are embedded, so only the Drive calls need the internet.

## Type scale shared by the three pages

`tools/patchlib.py` ends with `TYPE_RULES`, applied last by every generator: running text in Cormorant Garamond at line-height 1.5, date, venue and address lines at 1.45 with balanced wrapping, script headings that can wrap (the venue names) at 1.15, lists of names at 1.4. Change a value there and rebuild all three pages.

## Reception page (`/reception/`)

`reception/index.html` is the Delhi reception invitation (Saturday 19 December 2026, The Imperium, Ashok Vihar), built from the same Claude Design export with `tools/reception-patch.json`, which `tools/make_reception_patch.py` generates: one reception card instead of the wedding-day cards, the venue, an RSVP without event chips (responses carry "Reception" in the events column of the same sheet), a countdown to 6 pm on the day, a photo button pointing at the `reception` sub-folder of the shared Drive folder (its own wall is at `/reception/wall/`), and a navy-and-gold night edition of the design in which the wax seal, not a pearl, travels the thread. Its pictures live in `assets/reception/`; `reception/music.mp3` is the 33 s piece that came with the design export (the wedding page's original music). To rebuild, from the repository root:

    python3 tools/make_reception_patch.py "$SRC" tools/reception-patch.json --text-top 30%
    python3 tools/build.py "$SRC" reception/index.html --endpoint "$FORM" --fields "$FIELDS" --base https://nityawedsanuj.com/reception --patch tools/reception-patch.json --music /reception/music.mp3 --album "https://drive.google.com/drive/folders/1X_BRyLVbhBucyDli2uiJsKIB16HyUtb7" --image reception=assets/reception/reception.jpg --image venue=assets/reception/venue.jpg --image closing=assets/reception/closing.jpg --resource ganesha=assets/reception/ganesha.jpg --prune --title "Nitya & Anuj · Reception" --description "Saturday 19 December 2026, 6:00 pm onwards, The Imperium, Ashok Vihar, Delhi. Open the invitation and send your RSVP."

## Kirtan and langar page (`/kirtan/`)

`kirtan/index.html` is the invitation to the kirtan and langar at Gurudwara Nanak Piao Sahib, Delhi (Sunday 6 December 2026, kirtan 11:30 am to 1:30 pm, langar from 1:30 pm), built from the same export with `tools/kirtan-patch.json` from `tools/make_kirtan_patch.py`: Ik Onkar (traced from GNU FreeSerif, see `tools/patchlib.py`) in place of the Ganesh invocation, the gurudwara with the invitation beneath it, a kirtan card and a langar card, the venue, no RSVP, and a countdown to 11:30 am on the day with the photo button pointing at the `kirtan` sub-folder of the shared Drive folder (its wall is at `/kirtan/wall/`). `tools/kirtan-pictures.py` prepares the pictures in `assets/kirtan/` from the generated artwork. `kirtan/music.mp3` is Ik Onkar from Rang De Basanti (trimmed, faded, level-matched to the wedding page's music), looped from the moment the envelope opens.
