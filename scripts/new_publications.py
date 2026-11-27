#!/usr/bin/env python3
"""Find journal articles on the ORCID record that are not on the site yet and
add them to the publication list in site.html, formatted from Crossref.

Run by .github/workflows/update-metrics.yml, which opens a pull request with
the change so a person approves it. Writes pr_body.md when anything was
added. DOIs in data/orcid_ignore.txt are skipped (closing the pull request
without merging adds its DOIs there automatically).
"""
import html, json, os, re, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site.html")
IGNORE = os.path.join(ROOT, "data", "orcid_ignore.txt")
ORCID = "https://pub.orcid.org/v3.0/0000-0002-8855-5718/works"
UA = "PlantBiogeographySite/1.0 (static website upkeep)"
GEN = ("Noccaea|Ricotia|Heldreichia|Bornmuellera|Iberis|Hesperis|Matthiola|Brassica|Scilla|Chionodoxa|Puschkinia|"
       "Prospero|Campanula|Acantholimon|Marrubium|Knautia|Iljinskaea|Conringia|Aethionema|Pseudosempervivum|"
       "Chaenorhinum|Thlaspiceras|Arabis|Thlaspi|Carthamus|Astragalus|Dianthus|Thymus|Tanacetum|Allium|Erodium|"
       "Genista|Scrophularia|Veronica|Pinguicula|Umbilicus|Arabidopsis|Phyllolepidium|Asyneuma|Asphodeline|"
       "Gonocytisus|Schrenkiella|Chrysochamela|Bunias")
STOP = "sect|section|s|sl|and|from|in|with|species|complex|of|the|a|an|as|to|across|its|subsp|L|var|is|new|based"
GEN_RX = re.compile(r"\b(" + GEN + r")\b(\s+(?!(?:" + STOP + r")\b)[a-zçğıöşü][a-zçğıöşü-]+)?")


def get(url, accept="application/json"):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def italicise(t):
    t = html.escape(t, quote=False)
    return GEN_RX.sub(lambda m: "<i>" + m.group(1) + (m.group(2) or "") + "</i>", t)


def initials(given):
    parts = re.split(r"[\s\-]+", (given or "").replace(".", " ").strip())
    return "".join(p[0].upper() + "." for p in parts if p)


def authors(lst):
    names = [f'{a.get("family", "").strip()} {initials(a.get("given"))}'.strip() for a in lst]
    names = [n for n in names if n]
    if len(names) > 12:
        me = next((i for i, n in enumerate(names) if n.startswith("Özüdoğru") or n.startswith("Ozudogru")), None)
        keep = names[:3] + ["…"] + ([names[me], "…"] if me and 3 <= me < len(names) - 1 else []) + names[-1:]
        names = keep
    out = []
    for n in names:
        if re.match(r"(Özüdoğru|Ozudogru|Özüdogru)\b", n):
            out.append("<b>Özüdoğru B.</b>")
        else:
            out.append(html.escape(n))
    return ", ".join(out)


def entry(doi):
    w = get("https://api.crossref.org/works/" + urllib.parse.quote(doi))["message"]
    if w.get("type") != "journal-article":
        return None, w.get("type")
    title = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", (w.get("title") or [""])[0])).strip()
    year = None
    for k in ("published-print", "published-online", "issued"):
        dp = (w.get(k) or {}).get("date-parts")
        if dp and dp[0] and dp[0][0]:
            year = dp[0][0]
            break
    journal = html.escape((w.get("container-title") or [""])[0])
    ref = f"<i>{journal}</i>"
    if w.get("volume"):
        ref += " " + html.escape(w["volume"]) + (f'({html.escape(w["issue"])})' if w.get("issue") else "")
    if w.get("page"):
        ref += ": " + html.escape(w["page"]).replace("-", "–")
    elif w.get("article-number"):
        ref += ": " + html.escape(w["article-number"])
    ref += f' · <a href="https://doi.org/{html.escape(doi)}" target="_blank" rel="noopener">doi:{html.escape(doi)}</a>'
    li = (f'        <li data-y="{year}" data-tags=""><span class="yr">{year}</span><div>'
          f'<p class="t">{italicise(title)}</p><p class="a">{authors(w.get("author", []))}</p>'
          f'<p class="j">{ref}</p></div></li>')
    return (year or 0, li, title), None


def main():
    site = open(SITE, encoding="utf-8").read()
    low = site.lower()
    ignore = set()
    if os.path.exists(IGNORE):
        ignore = {l.strip().lower() for l in open(IGNORE, encoding="utf-8") if l.strip() and not l.startswith("#")}
    added, skipped = [], []
    for g in get(ORCID).get("group", []):
        dois = [e["external-id-value"].lower() for e in g.get("external-ids", {}).get("external-id", [])
                if e.get("external-id-type") == "doi"]
        if not dois or any(d in low or d in ignore for d in dois):
            continue
        doi = dois[0]
        try:
            res, kind = entry(doi)
        except Exception as e:
            print("Crossref lookup failed for", doi, e)
            continue
        if res is None:
            skipped.append((doi, kind))
        else:
            added.append((doi,) + res)
    for doi, kind in skipped:
        print(f"Not added automatically ({kind}): {doi}")
    if not added:
        print("No new journal articles.")
        return
    m = re.search(r'(<ol class="pubs" id="pubs">\n)(.*?)(\n\s*</ol>)', site, re.S)
    items = re.findall(r"        <li\b.*?</li>", m.group(2), re.S)
    for doi, year, li, title in sorted(added, key=lambda a: -a[1]):
        pos = next((i for i, it in enumerate(items)
                    if int((re.search(r'data-y="(\d*)"', it).group(1) or 0)) < year), len(items))
        items.insert(pos, li)
    site = site[:m.start(2)] + "\n".join(items) + site[m.end(2):]
    open(SITE, "w", encoding="utf-8").write(site)
    body = ["New journal articles found on the ORCID record and formatted from Crossref. "
            "Check the authors, title and italics in the diff, then merge to publish them. "
            "Closing this pull request without merging stops these DOIs from being suggested again.", ""]
    body += [f"- {y} · {t} · doi:{d}" for d, y, li, t in added]
    if skipped:
        body += ["", "Also on ORCID but not added automatically (not journal articles):"]
        body += [f"- {k} · https://doi.org/{d}" for d, k in skipped]
    open(os.path.join(ROOT, "pr_body.md"), "w", encoding="utf-8").write("\n".join(body) + "\n")
    print("Added", len(added), "articles")


if __name__ == "__main__":
    main()
