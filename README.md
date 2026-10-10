# Nitya weds Anuj

Wedding invitation site, served by GitHub Pages at https://nityawedsanuj.com

- `index.html` is the invitation (a self-contained export from Claude Design, with the images embedded)
- `og.jpg` is the link-preview image shown by WhatsApp and others
- `CNAME` tells GitHub Pages the custom domain
- `rsvp/Code.gs` is an alternative RSVP backend (Google Apps Script appending to the AN sheet); the live page posts to a Google Form instead
- `tools/build.py` rebuilds `index.html` from a fresh export, setting the title, link-preview tags and the RSVP endpoint:

```
python3 tools/build.py export.html index.html \
  --endpoint https://docs.google.com/forms/d/e/<form id>/formResponse \
  --fields '{"name":"entry.…","attending":"entry.…","guests":"entry.…","events":"entry.…","note":"entry.…","submittedAt":""}' \
  --base https://nityawedsanuj.com
```
