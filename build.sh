#!/bin/sh
# Wraps site.html (the artifact body) into the standalone index.html served by GitHub Pages.
cd "$(dirname "$0")"
{
  printf '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover, interactive-widget=resizes-content">\n<meta name="color-scheme" content="light">\n'
  awk '/^<header class="top"/{print "</head>\n<body>"} {print}' site.html
  printf '</body>\n</html>\n'
} > index.html
