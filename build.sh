#!/bin/sh
# Fill the template with the content files, then split into the six pages.
set -e
cd "$(dirname "$0")"
python3 scripts/render_site.py
python3 scripts/build_pages.py
