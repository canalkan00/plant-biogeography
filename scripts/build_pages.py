#!/usr/bin/env python3
"""Build the multi-page site from site.html.

site.html is written by render_site.py from templates/site.html and the
content files; it holds every section, the shared header, footer, styles and
script (it is also the body of the Claude preview). This script splits it into
index.html (home), about.html, research.html, publications.html,
people.html and contact.html, rewriting in-page links to the right page.
Run both through build.sh.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site.html")
src = open(SITE, encoding="utf-8").read()

# ---------------------------------------------------------------------------
# Normalise site.html so hand edits and automatic additions stay consistent:
# publication tags and years, the "show more" split, the per-year bar strip
# and every count shown on the page are recomputed from the lists themselves.
# ---------------------------------------------------------------------------
SHOW = 14
BRAS = re.compile(r"Brassicaceae|Cruciferae|crucifer|Noccaea|Ricotia|Heldreichia|Bornmuellera|Iberis|Hesperis|"
                  r"Matthiola|Brassica|Aethionema|Pseudosempervivum|Thlaspi|Arabis|Iljinskaea|Phyllolepidium", re.I)
NEWT = re.compile(r"new species|new genus|new subspecies|new record|new crucifer|new bellflower|yeni bir|a new |"
                  r"an extraordinary new", re.I)
ECO = re.compile(r"fire|steppe|germination|community|trait|ethnobot|flora of|florası|pollen|seed science", re.I)


def normalise(s):
    m = re.search(r'(<ol class="pubs" id="pubs">\n)(.*?)(\n\s*</ol>)', s, re.S)
    items = re.findall(r"<li\b[^>]*>.*?</li>", m.group(2), re.S)
    out, years = [], {}
    for i, li in enumerate(items):
        inner = li[li.index(">") + 1:]
        y = (re.search(r'<span class="yr">(\d{4})</span>', inner) or [None, ""])[1]
        title = re.sub(r"<[^>]+>", "", (re.search(r'<p class="t">(.*?)</p>', inner, re.S) or [None, ""])[1])
        tags = [t for t, rx in (("bras", BRAS), ("new", NEWT), ("eco", ECO)) if rx.search(title)]
        extra = ' class="more" hidden' if i >= SHOW else ""
        out.append(f'        <li data-y="{y}" data-tags="{" ".join(tags)}"{extra}>{inner}')
        if y:
            years[int(y)] = years.get(int(y), 0) + 1
    s = s[:m.start(2)] + "\n".join(out) + s[m.end(2):]
    # per-year bar strip
    lo, hi, mx = min(years), max(years), max(years.values())
    bars = ""
    for y in range(lo, hi + 1):
        n = years.get(y, 0)
        if n:
            bars += (f'<button type="button" class="yb" data-y="{y}" style="--h:{n / mx * 100:.0f}%" '
                     f'aria-pressed="false" title="{y}: {n}"><span class="yb-bar"></span><span class="yb-n">{n}</span>'
                     f'<span class="yb-y">{str(y)[2:]}</span></button>')
        else:
            bars += f'<span class="yb empty" aria-hidden="true"><span class="yb-y">{str(y)[2:]}</span></span>'
    s = re.sub(r'(<div class="years"[^>]*>).*?(</div>)', lambda mm: mm.group(1) + bars + mm.group(2), s, count=1, flags=re.S)
    s = re.sub(r"(\.years\{display:grid;grid-template-columns:repeat\()\d+", lambda mm: mm.group(1) + str(hi - lo + 1), s)
    # counts
    counts = {"pubs": len(items), "projects": len(re.findall(r'class="tl-row ', s))}
    for k, v in counts.items():
        s = re.sub(rf'(<span data-count="{k}">)\d+(</span>)', rf"\g<1>{v}\g<2>", s)
    return s


normalised = normalise(src)
if normalised != src:
    open(SITE, "w", encoding="utf-8").write(normalised)
    src = normalised

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
