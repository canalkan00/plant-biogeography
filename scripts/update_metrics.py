#!/usr/bin/env python3
"""Weekly site upkeep, run by .github/workflows/update-metrics.yml.

1. Reads citation, h-index and i10-index from Google Scholar and writes them
   into site.html (elements marked data-metric="..."). If Scholar blocks the
   request or returns implausible numbers, the page is left as it is.
2. Lists works on the ORCID record whose DOI is not on the site yet and
   writes them to new_publications.md for the workflow to open as an issue.

Standard library only. Exits with code 1 when Scholar has not been read for
28 days, so GitHub e-mails the repository owner.
"""
import datetime as dt, json, os, re, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site.html")
STATE = os.path.join(ROOT, "data", "metrics.json")
SCHOLAR = "https://scholar.google.com/citations?user=N8nlB4wAAAAJ&hl=en"
ORCID = "https://pub.orcid.org/v3.0/0000-0002-8855-5718/works"
IGNORE = os.path.join(ROOT, "data", "orcid_ignore.txt")
MONTHS_TR = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz",
             "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def get(url, accept="text/html"):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept,
                                               "Accept-Language": "en"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def scholar_metrics():
    html = get(SCHOLAR)
    rows = re.findall(r'<td class="gsc_rsb_sc1"><a[^>]*>([^<]*)</a></td>'
                      r'<td class="gsc_rsb_std">(\d+)</td>', html)
    m = {k.strip(): int(v) for k, v in rows}
    out = {"citations": m.get("Citations"), "h": m.get("h-index"), "i10": m.get("i10-index")}
    if None in out.values():
        raise ValueError("metrics table not found (Scholar may have blocked the request)")
    return out


def plausible(new, old):
    # citations never drop much; reject parser errors or partial pages
    return (new["citations"] >= old["citations"] * 0.9 and new["h"] >= old["h"] - 1
            and new["i10"] >= old["i10"] - 2 and new["citations"] < old["citations"] * 3)


def write_site(m, today):
    s = open(SITE, encoding="utf-8").read()
    vals = {"citations": f'{m["citations"]:,}', "h": str(m["h"]), "i10": str(m["i10"]),
            "date-en": f"{today.day} {today.strftime('%B')} {today.year}",
            "date-tr": f"{today.day} {MONTHS_TR[today.month - 1]} {today.year}"}
    for key, val in vals.items():
        s, n = re.subn(rf'(data-metric="{key}">)[^<]*(<)', rf"\g<1>{val}\g<2>", s)
        if n != 1:
            raise RuntimeError(f"marker data-metric={key} found {n} times in site.html")
    open(SITE, "w", encoding="utf-8").write(s)


def new_orcid_works():
    data = json.loads(get(ORCID, "application/json"))
    site = open(SITE, encoding="utf-8").read().lower()
    ignore = {l.strip().lower() for l in open(IGNORE, encoding="utf-8")
              if l.strip() and not l.startswith("#")} if os.path.exists(IGNORE) else set()
    found = []
    for g in data.get("group", []):
        summ = g["work-summary"][0]
        dois = [e["external-id-value"].lower() for e in g.get("external-ids", {}).get("external-id", [])
                if e.get("external-id-type") == "doi"]
        if not dois or any(d in site or d in ignore for d in dois):
            continue
        title = (summ.get("title") or {}).get("title", {}).get("value", "")
        year = ((summ.get("publication-date") or {}).get("year") or {}).get("value", "")
        found.append(f"- {year} · {title} · https://doi.org/{dois[0]}")
    return found


def main():
    state = json.load(open(STATE))
    today = dt.date.today()
    state["last_checked"] = today.isoformat()
    try:
        m = scholar_metrics()
        if not plausible(m, state):
            raise ValueError(f"implausible values {m}, kept {state}")
        write_site(m, today)
        state.update(m, last_success=today.isoformat(), last_status="ok")
        print("Scholar:", m)
    except Exception as e:  # keep the old numbers
        state["last_status"] = f"skipped: {e}"
        print("Scholar not updated:", e)

    try:
        works = new_orcid_works()
        if works:
            open(os.path.join(ROOT, "new_publications.md"), "w", encoding="utf-8").write(
                "Works on ORCID whose DOI is not on the site yet. Check them and add "
                "the real ones to the publication list. To stop a DOI being reported, add it to "
                "data/orcid_ignore.txt.\n\n" + "\n".join(works) + "\n")
        print("ORCID works not on the site:", len(works))
    except Exception as e:
        print("ORCID check failed:", e)

    json.dump(state, open(STATE, "w"), indent=2, ensure_ascii=False)
    open(STATE, "a").write("\n")
    stale = (today - dt.date.fromisoformat(state["last_success"])).days
    if stale > 28:
        print(f"::error::Scholar figures have not been updated for {stale} days")
        sys.exit(1)


if __name__ == "__main__":
    main()
