#!/usr/bin/env python3
"""Find journal articles on the ORCID record that are not on the site yet and
add them to the publication list in content/publications.yml, formatted
from Crossref.

Run by .github/workflows/weekly-publications.yml, which opens a pull request with
the change so a person approves it. Writes pr_body.md when anything was
added. DOIs in data/orcid_ignore.txt are skipped (closing the pull request
without merging adds its DOIs there automatically).
"""
import json, os, re, sys, urllib.parse, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content_io

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
    # genus and species names in italics (Markdown *...*)
    return GEN_RX.sub(lambda m: "*" + m.group(1) + (m.group(2) or "") + "*", t)


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
    # the site sets "Özüdoğru B." in bold by itself
    return ", ".join("Özüdoğru B." if re.match(r"(Özüdoğru|Ozudogru|Özüdogru)\b", n) else n for n in names)


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
    ref = "*" + (w.get("container-title") or [""])[0] + "*"
    if w.get("volume"):
        ref += " " + w["volume"] + (f'({w["issue"]})' if w.get("issue") else "")
    if w.get("page"):
        ref += ": " + w["page"].replace("-", "–")
    elif w.get("article-number"):
        ref += ": " + w["article-number"]
    item = {"year": year, "title": italicise(title), "authors": authors(w.get("author", [])),
            "journal": ref, "doi": doi}
    return (year or 0, item, title), None


def main():
    pubs = content_io.load("publications")
    # a DOI anywhere in the content (publication list, recent work, topics) counts as on the site
    low = " ".join(open(content_io.path(n), encoding="utf-8").read() for n in
                   ("publications", "home", "research", "projects")).lower()
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
    items = pubs.setdefault("articles", [])
    for doi, year, item, title in sorted(added, key=lambda a: -a[1]):
        # first among the articles of its year (the site lists newest first)
        pos = next((i for i, it in enumerate(items) if int(it.get("year") or 0) <= year), len(items))
        items.insert(pos, item)
    content_io.save("publications", pubs)
    body = ["New journal articles found on the ORCID record and formatted from Crossref. "
            "Check the authors, title and italics in the diff (content/publications.yml), then merge to "
            "publish them. Closing this pull request without merging stops these DOIs from being suggested again.", ""]
    body += [f"- {y} · {t} · doi:{d}" for d, y, it, t in added]
    if skipped:
        body += ["", "Also on ORCID but not added automatically (not journal articles):"]
        body += [f"- {k} · https://doi.org/{d}" for d, k in skipped]
    open(os.path.join(ROOT, "pr_body.md"), "w", encoding="utf-8").write("\n".join(body) + "\n")
    print("Added", len(added), "articles")


if __name__ == "__main__":
    main()
