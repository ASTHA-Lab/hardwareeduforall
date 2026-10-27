# Hardware Security for All

Local course site for the nine hardware-security modules. It is static HTML, CSS, and one short script. No build step is required to browse it after the pages exist.

## GitHub Pages

This folder is the root of [ASTHA-Lab/hardwareeduforall](https://github.com/ASTHA-Lab/hardwareeduforall). In the repository, open Settings, then Pages. Deploy from the `main` branch, folder `/ (root)`. The public site is [https://astha-lab.github.io/hardwareeduforall/](https://astha-lab.github.io/hardwareeduforall/).

## Open it locally

From this folder:

```powershell
python -m http.server 8765
```

Then open http://localhost:8765/

Opening the HTML files directly in a browser also works. The local server is the better check, because it matches how the site will behave once it is hosted.

## Regenerate

`build_site.py` rewrites the HTML and recopies student materials from the project archive.

```powershell
python build_site.py
```

Edit page text in `content_pages.py`. Edit shared layout in `build_site.py`. Edit appearance in `css/site.css`.

## What is included

Student handouts, lecture decks, starter VHDL and C, the reverse-engineering binary, and the three VHDL lab manuals.

## What is left in the archive on purpose

Instructor solution files, solved homework, the NSF proposal, raw evaluation reports, and the Spring 2023 lecture recordings. A published tutorial PDF and a third-party gem5 cache script are not redistributed. The Results and Adopt pages say this in plain language.
