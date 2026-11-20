# AX GAIA Intelligence website

Static company website for axgaiaintelligence.com: the company, Ter-AX, GAIA and Data & Sources, in English and Greek (`/el/`).

## Editing

- Page text lives in `tools/build_site.py`; the GAIA page body is `tools/gaia_main_en.html`.
- Rebuild the pages after any change: `python tools/build_site.py`.
- Styles: `assets/index.css` (shared) and `assets/pages.css` (company, Ter-AX and Data & Sources pages).

## Local preview

`powershell -NoProfile -ExecutionPolicy Bypass -File .\preview.ps1`, then open http://localhost:8000.
It serves only the public site files and binds to this computer only.

## Publishing

Pushing to `main` publishes the site. Work on a separate branch and merge only when the change is approved.
