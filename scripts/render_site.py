#!/usr/bin/env python3
"""Write site.html from templates/site.html and the content files.

The text, lists and photos of the site live in content/*.yml (edited in the
Pages CMS panel or by hand). templates/site.html holds the layout, styles and
script. This script fills the template with the content and writes site.html,
which build_pages.py then splits into the six pages. Do not edit site.html by
hand: the next build overwrites it.

Text fields understand a little Markdown: *italic*, **bold**, [text](link),
and a blank line between paragraphs in the longer fields.
"""
import datetime as dt, glob, hashlib, html, json, os, re

import yaml
from jinja2 import ChainableUndefined, Environment, FileSystemLoader
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")
SIZED = "img/sized"
MONTHS_TR = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz",
             "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
MONTHS_EN = ["January", "February", "March", "April", "May", "June", "July",
             "August", "September", "October", "November", "December"]

# ---------------------------------------------------------------- text ------
ESC = re.compile(r"\\([\\`*_{}\[\]()#+\-.!|>~])")
LINK = re.compile(r"\[((?:[^\[\]]|\[[^\]]*\])+)\]\(\s*<?([^)\s>]+)>?\s*\)")
AUTOLINK = re.compile(r"<(https?://[^>\s]+)>")
TAG = re.compile(r"(<[A-Za-z/!][^>]*>)")


def _text(s):
    # escape &, < and > in text but leave real HTML tags and entities alone
    parts = TAG.split(s)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r"&(?!#?\w+;)", "&amp;", parts[i]).replace("<", "&lt;").replace(">", "&gt;")
    return "".join(parts)


def inline(s):
    """Markdown-lite for one paragraph: *italic*, _italic_, **bold**, [t](url)."""
    if s is None:
        return ""
    s = str(s).strip()
    keep = []

    def hold(x):
        keep.append(x)
        return f"\x00{len(keep) - 1}\x00"
    s = ESC.sub(lambda m: hold(html.escape(m.group(1), quote=False)), s)
    s = AUTOLINK.sub(lambda m: hold(f'<a href="{m.group(1)}" target="_blank" rel="noopener">{m.group(1)}</a>'), s)

    def link(m):
        url = m.group(2)
        ext = ' target="_blank" rel="noopener"' if re.match(r"https?://|mailto:", url) else ""
        return hold(f'<a href="{html.escape(url)}"{ext}>') + m.group(1) + hold("</a>")
    s = LINK.sub(link, s)
    s = _text(s)
    s = re.sub(r"\*\*(?=\S)(.+?)(?<=\S)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"__(?=\S)(.+?)(?<=\S)__", r"<b>\1</b>", s)
    s = re.sub(r"\*(?=\S)(.+?)(?<=\S)\*", r"<i>\1</i>", s)
    s = re.sub(r"(?<![\w\\])_(?=\S)(.+?)(?<=\S)_(?!\w)", r"<i>\1</i>", s)
    s = re.sub(r"(?:  |\\)\n", "<br>", s).replace("\n", "<br>")
    while "\x00" in s:
        s = re.sub(r"\x00(\d+)\x00", lambda m: keep[int(m.group(1))], s)
    return s


def paras(s):
    """Split a longer field into paragraphs (blank line between them)."""
    if not s:
        return []
    s = str(s).replace("\r\n", "\n").strip()
    return [inline(p) for p in re.split(r"\n\s*\n", s) if p.strip()]


def tr_or_en(d, key="tr"):
    if isinstance(d, dict):
        return d.get(key) or d.get("en") or ""
    return d or ""


def bi(d):
    """A field with an English and a Turkish version -> two spans."""
    if not isinstance(d, dict):
        d = {"en": d, "tr": d}
    return f'<span class="en">{inline(d.get("en") or d.get("tr"))}</span><span class="tr">{inline(tr_or_en(d))}</span>'


def pairs(d):
    """Paragraph pairs (English, Turkish) for a two-language long text."""
    en, tr = paras((d or {}).get("en")), paras((d or {}).get("tr"))
    n = max(len(en), len(tr))
    return [(en[i] if i < len(en) else "", tr[i] if i < len(tr) else "") for i in range(n)]


ME = re.compile(r"(?<![\w*])(Özüdoğru B\.)")


def authors(s):
    # Barış Özüdoğru's name is set in bold wherever it appears
    s = inline(s)
    if "<b>Özüdoğru B.</b>" not in s:
        s = ME.sub(r"<b>\1</b>", s)
    return s


def initials(name):
    words = [w for w in re.sub(r"^(Prof\.|Doç\.|Dr\.|Assoc\.|Asst\.|\s)+", "", name).split() if w]
    return (words[0][0] + words[-1][0]).upper() if len(words) > 1 else name[:2].upper()


def doi_url(x):
    x = (x or "").strip()
    if not x:
        return ""
    if x.startswith("http"):
        return x
    return "https://doi.org/" + re.sub(r"^doi:\s*", "", x)


def doi_text(x):
    return re.sub(r"^https?://(dx\.)?doi\.org/", "", (x or "").strip())


def attr(s):
    return html.escape(re.sub(r"<[^>]+>", "", inline(s)).replace("&amp;", "&"), quote=True)


# -------------------------------------------------------------- images ------
used_sized = set()


def _open(path):
    full = os.path.join(ROOT, path)
    if not os.path.exists(full):
        raise SystemExit(f"Image not found: {path}")
    im = Image.open(full)
    return ImageOps.exif_transpose(im)


def _sized(path, w):
    """A copy of the image at width w (made once, reused afterwards)."""
    full = os.path.join(ROOT, path)
    digest = hashlib.sha1(open(full, "rb").read()).hexdigest()[:8]
    stem = os.path.splitext(os.path.basename(path))[0]
    out = f"{SIZED}/{stem}-{digest}-{w}.jpg"
    used_sized.add(out)
    dest = os.path.join(ROOT, out)
    if not os.path.exists(dest):
        im = _open(path)
        h = round(im.height * w / im.width)
        im = im.convert("RGB").resize((w, h), Image.LANCZOS)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        im.save(dest, "JPEG", quality=82, optimize=True, progressive=True)
    return out


def _needs_copy(path, im):
    # very large files or formats browsers do not show get a resized JPEG copy
    return os.path.splitext(path)[1].lower() not in (".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif")


def picture(path, widths, sizes, alt, extra=""):
    """<img> with a srcset of resized copies; width and height read from the file."""
    im = _open(path)
    W, H = im.size
    srcs = []
    for w in sorted(widths):
        if w < W:
            srcs.append((_sized(path, w), w))
    top = max(widths)
    if W > top * 1.15 or _needs_copy(path, im):
        main_src, mw = _sized(path, min(top, W)), min(top, W)
        mh = round(H * mw / W)
        srcs = [s for s in srcs if s[1] < mw] + [(main_src, mw)]
    else:
        main_src, mw, mh = path, W, H
        srcs.append((path, W))
    srcset = ", ".join(f"{u} {w}w" for u, w in srcs)
    ss = f' srcset="{srcset}" sizes="{sizes}"' if len(srcs) > 1 else ""
    return (f'<img src="{main_src}"{ss} width="{mw}" height="{mh}" loading="lazy" '
            f'decoding="async" alt="{attr(alt)}"{extra}>')


def figure_img(path, alt):
    return picture(path, [1400], "", alt)


# ------------------------------------------------------------- projects -----
def year(x):
    m = re.search(r"\d{4}", str(x or ""))
    return int(m.group(0)) if m else 0


def newest(items, key="year"):
    """Newest first; entries from the same year keep the order they have in the file."""
    return sorted([i for i in (items or []) if i], key=lambda i: -year(i.get(key)))


def timeline(projects):
    rows = []
    for p in newest(projects, "start"):
        if not year(p.get("start")):
            continue
        start = year(p["start"])
        end = year(p.get("end")) or None
        rows.append((p, start, end))
    if not rows:
        return {"axis": [], "rows": []}
    this_year = dt.date.today().year
    lo = min(s for _, s, _ in rows)
    last = max((e if e else max(this_year, s)) for _, s, e in rows)
    span = -(-(last + 1 - lo) // 3) * 3
    hi = lo + span
    axis = [(f"{(y - lo) / span * 100:.2f}", y) for y in range(lo, hi + 1, 3)]
    out = []
    for p, s, e in rows:
        left = (s - lo) / span * 100
        width = ((e if e else hi) - s + (1 if e else 0)) / span * 100
        label = f"{s}–" if not e else (str(s) if e == s else f"{s}–{e}")
        out.append({"p": p, "left": f"{left:.2f}", "width": f"{width:.2f}", "label": label,
                    "end": left + width > 80})
    return {"axis": axis, "rows": out}


ROLES = {
    "phd": ("PhD student", "Doktora öğrencisi"),
    "msc": ("MSc student", "Yüksek lisans öğrencisi"),
    "bsc": ("Undergraduate student", "Lisans öğrencisi"),
    "postdoc": ("Postdoctoral researcher", "Doktora sonrası araştırmacı"),
    "researcher": ("Researcher", "Araştırmacı"),
}
FUNDERS = {"tub": "TÜBİTAK", "bap": "Hacettepe University BAP", "oth": "Other"}


def member_role(m):
    custom = m.get("role_custom") or {}
    if isinstance(custom, dict) and (custom.get("en") or custom.get("tr")):
        return bi(custom)
    en, tr = ROLES.get(m.get("role") or "msc", ROLES["msc"])
    return bi({"en": en, "tr": tr})


# ---------------------------------------------------------------- main ------
def load(name):
    with open(os.path.join(CONTENT, name + ".yml"), encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def metrics():
    m = json.load(open(os.path.join(ROOT, "data", "metrics.json"), encoding="utf-8"))
    d = dt.date.fromisoformat(m["last_success"])
    m["date_en"] = f"{d.day} {MONTHS_EN[d.month - 1]} {d.year}"
    m["date_tr"] = f"{d.day} {MONTHS_TR[d.month - 1]} {d.year}"
    m["citations_fmt"] = f'{m["citations"]:,}'
    return m


def render():
    env = Environment(loader=FileSystemLoader(os.path.join(ROOT, "templates")), autoescape=False,
                      undefined=ChainableUndefined, trim_blocks=True, lstrip_blocks=True, keep_trailing_newline=True)
    env.filters.update(md=inline, bi=bi, pairs=pairs, paras=paras, authors=authors, attr=attr,
                       initials=initials, newest=newest, doi_url=doi_url, doi_text=doi_text, role=member_role)
    env.globals.update(picture=picture, figure_img=figure_img, timeline=timeline, FUNDERS=FUNDERS)
    ctx = {n: load(n) for n in ("home", "about", "profile", "research", "projects", "publications",
                                "theses", "people", "contact", "photos")}
    ctx["metrics"] = metrics()
    out = env.get_template("site.html").render(**ctx)
    open(os.path.join(ROOT, "site.html"), "w", encoding="utf-8").write(out)
    # remove resized copies nothing uses any more
    for f in glob.glob(os.path.join(ROOT, SIZED, "*")):
        if os.path.relpath(f, ROOT).replace(os.sep, "/") not in used_sized:
            os.remove(f)


if __name__ == "__main__":
    render()
    print("site.html written from templates/site.html and content/")
