#!/bin/sh
# Builds the pages served by GitHub Pages (index.html, about.html, research.html,
# publications.html, people.html, contact.html) from site.html.
cd "$(dirname "$0")"
python3 scripts/build_pages.py
