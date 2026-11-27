#!/usr/bin/env python3
"""Weekly site upkeep, run by .github/workflows/update-metrics.yml.

1. Reads citation, h-index and i10-index from Google Scholar (through SerpApi
   when the SERPAPI_KEY secret is set, otherwise directly) and stores them in
   data/metrics.json; the build puts them on the page. If Scholar blocks the
   request or returns implausible numbers, the old figures are kept.
2. New publications are handled by scripts/new_publications.py.

Standard library only. Exits with code 1 when Scholar has not been read for
28 days, so GitHub e-mails the repository owner.
"""
import datetime as dt, json, os, re, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(ROOT, "data", "metrics.json")
SCHOLAR = "https://scholar.google.com/citations?user=N8nlB4wAAAAJ&hl=en"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def get(url, accept="text/html"):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept,
                                               "Accept-Language": "en"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def serpapi_metrics(key):
    # Google Scholar profile via SerpApi (free plan: 100 searches a month)
    url = ("https://serpapi.com/search.json?engine=google_scholar_author"
           "&author_id=N8nlB4wAAAAJ&hl=en&api_key=" + key)
    table = json.loads(get(url, "application/json"))["cited_by"]["table"]
    t = {k: v["all"] for row in table for k, v in row.items()}
    return {"citations": int(t["citations"]), "h": int(t["h_index"]), "i10": int(t["i10_index"])}


def scholar_metrics():
    key = os.environ.get("SERPAPI_KEY", "").strip()
    if key:
        return serpapi_metrics(key)
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


def main():
    state = json.load(open(STATE))
    today = dt.date.today()
    state["last_checked"] = today.isoformat()
    try:
        m = scholar_metrics()
        if not plausible(m, state):
            raise ValueError(f"implausible values {m}, kept {state}")
        state.update(m, last_success=today.isoformat(), last_status="ok")
        print("Scholar:", m)
    except Exception as e:  # keep the old numbers
        state["last_status"] = f"skipped: {e}"
        print("Scholar not updated:", e)


    json.dump(state, open(STATE, "w"), indent=2, ensure_ascii=False)
    open(STATE, "a").write("\n")
    stale = (today - dt.date.fromisoformat(state["last_success"])).days
    if stale > 28:
        print(f"::error::Scholar figures have not been updated for {stale} days")
        sys.exit(1)


if __name__ == "__main__":
    main()
