#!/usr/bin/env python3
"""Build the multi-page site from site.html.

site.html holds every section, the shared header, footer, styles and script
(it is also the body of the Claude preview). This script splits it into
index.html (home), about.html, research.html, publications.html,
people.html and contact.html, rewriting in-page links to the right page.
Run it through build.sh after any edit to site.html.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(ROOT, "site.html"), encoding="utf-8").read()

head = src[:src.index('<header class="top"')]
header = src[src.index('<header class="top"'):src.index("</header>") + len("</header>")]
main = src[src.index("<main>") + len("<main>"):src.index("</main>")]
footer = src[src.index("<footer>"):src.index("</footer>") + len("</footer>")]
script = src[src.rindex("<script>"):src.rindex("</script>") + len("</script>")]

# main is a run of <section> blocks, some preceded by an <!-- NAME --> comment
sections = {}
for m in re.finditer(r'(?:  <!-- [A-Z ]+ -->\n)?  <section class="[^"]*" id="([^"]+)".*?\n  </section>\n', main, re.S):
    sections[m.group(1)] = m.group(0)

PAGES = [
    # file, data-page, titles (en, tr), section ids
    ("index.html", "home", None, None, ["top", "highlights"]),
    ("about.html", "about", "About", "Hakkımızda", ["about", "habitat-heldreichia"]),
    ("research.html", "research", "Research", "Araştırma", ["research", "projects", "habitat-alpine"]),
    ("publications.html", "research", "Publications", "Yayınlar", ["publications", "theses"]),
    ("people.html", "people", "People", "Ekip", ["people"]),
    ("contact.html", "contact", "Contact", "İletişim", ["contact"]),
]
WHERE = {}
for f, _, _, _, ids in PAGES:
    for i in ids:
        WHERE[i] = f
# anchors that live inside a section
WHERE.update({"methods": "about.html", "pi": "about.html", "topics": "research.html",
              "team": "people.html", "alumni": "people.html", "collaborations": "people.html",
              "visit": "contact.html", "pubs": "publications.html"})
FIRST = {"about", "research", "publications", "people", "contact"}  # ids whose page opens on them


def relink(html, here):
    opening = FIRST | {"top"}

    def fix(m):
        anchor = m.group(1)
        target = WHERE.get(anchor)
        if not target:
            return m.group(0)
        if anchor in opening:
            return f'href="{target}"'
        if target == here:
            return f'href="#{anchor}"'
        return f'href="{target}#{anchor}"'
    return re.sub(r'href="#([A-Za-z0-9_-]+)"', fix, html)


def promote_heading(html):
    # the first section heading on a sub-page becomes the page's h1
    m = re.search(r'<(h2|h3) class="(sec-title|sub-head)" id="([^"]+)">(.*?)</\1>', html, re.S)
    if not m:
        return html
    return html[:m.start()] + f'<h1 class="sec-title" id="{m.group(3)}">{m.group(4)}</h1>' + html[m.end():]


SKELETON = ('<!doctype html>\n<html lang="en" data-page="{page}"{titles}>\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover, '
            'interactive-widget=resizes-content">\n<meta name="color-scheme" content="light">\n')

HASH_REDIRECT = """<script>
(function(){var m={%s};var h=location.hash.slice(1);if(m[h])location.replace(m[h]+(m[h].indexOf('#')<0&&h!==m[h].split('.')[0]?'#'+h:''));})();
</script>
""" % ",".join(f'"{k}":"{v}"' for k, v in sorted(WHERE.items()) if v != "index.html")

for fname, page, t_en, t_tr, ids in PAGES:
    body = "".join(sections[i] for i in ids)
    if fname != "index.html":
        body = promote_heading(body)
    titles = f' data-title-en="{t_en}" data-title-tr="{t_tr}"' if t_en else ""
    h = head
    if t_en:
        h = h.replace("<title>Plant Biogeography</title>", f"<title>{t_en} · Plant Biogeography</title>", 1)
    doc = (SKELETON.format(page=page, titles=titles) + h + "</head>\n<body>\n"
           + (HASH_REDIRECT if fname == "index.html" else "")
           + header + "\n\n<main>\n" + body + "</main>\n\n" + footer + "\n\n" + script + "\n</body>\n</html>\n")
    doc = relink(doc, fname)
    open(os.path.join(ROOT, fname), "w", encoding="utf-8").write(doc)

# body-only copy of the home page for the Claude preview (it adds its own skeleton)
home = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
preview = home[home.index("<title>"):home.index("</head>")] + "\n" + home[home.index("<body>\n") + 7:home.index("</body>")]
preview = preview.replace('<header class="top"', '<script>document.documentElement.dataset.page="home"</script>\n<header class="top"', 1)
os.makedirs(os.path.join(ROOT, ".preview"), exist_ok=True)
open(os.path.join(ROOT, ".preview", "home.html"), "w", encoding="utf-8").write(preview)
print("built:", ", ".join(p[0] for p in PAGES))
