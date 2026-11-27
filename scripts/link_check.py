#!/usr/bin/env python3
"""Check every outside link on the built pages and write broken_links.md if any
are broken. DOIs are checked against the DOI registry (publishers often refuse
automated visits, which says nothing about the link). Other links count as
broken only on a clear answer: page not found (404/410) or a site that does not
resolve. Run by .github/workflows/monthly-checks.yml.
"""
import glob, json, os, re, urllib.error, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0 Safari/537.36")
SKIP = ("fonts.googleapis.com", "fonts.gstatic.com")


def links():
    found = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "*.html"))):
        if os.path.basename(f) == "site.html":
            continue
        for u in re.findall(r'href="(https?://[^"]+)"', open(f, encoding="utf-8").read()):
            if not any(s in u for s in SKIP):
                found.setdefault(u.replace("&amp;", "&"), os.path.basename(f))
    return found


def check(url):
    doi = re.match(r"https?://(?:dx\.)?doi\.org/(.+)", url)
    if doi:
        api = "https://doi.org/api/handles/" + urllib.parse.quote(urllib.parse.unquote(doi.group(1)), safe="/")
        try:
            with urllib.request.urlopen(urllib.request.Request(api, headers={"User-Agent": UA}), timeout=30) as r:
                return None if json.load(r).get("responseCode") == 1 else "DOI not registered"
        except urllib.error.HTTPError as e:
            return "DOI not registered" if e.code == 404 else None
        except Exception:
            return None
    for attempt in range(2):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*"})
            with urllib.request.urlopen(req, timeout=30):
                return None
        except urllib.error.HTTPError as e:
            if e.code in (404, 410):
                return f"page not found ({e.code})"
            return None  # 403, 429, 5xx: the site answered; not proof of a broken link
        except urllib.error.URLError as e:
            reason = str(e.reason)
            if attempt == 1 and ("Name or service not known" in reason or "nodename" in reason or "getaddrinfo" in reason):
                return "site does not resolve"
        except Exception:
            pass
    return None


def main():
    found = links()
    broken = [(u, p, why) for u, p in found.items() for why in [check(u)] if why]
    print(f"Checked {len(found)} links, {len(broken)} broken.")
    path = os.path.join(ROOT, "broken_links.md")
    if broken:
        lines = ["These links on the site did not work in this month's check. Fix or remove them in site.html.", ""]
        lines += [f"- {why}: {u} (on {p})" for u, p, why in broken]
        open(path, "w", encoding="utf-8").write("\n".join(lines) + "\n")
        for u, p, why in broken:
            print(" -", why, u)
    elif os.path.exists(path):
        os.remove(path)


if __name__ == "__main__":
    main()
