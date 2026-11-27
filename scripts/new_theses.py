#!/usr/bin/env python3
"""Add theses found on YÖK (data/yok_theses.json, written by yok_theses.js)
that are not on the site yet to content/theses.yml, and write
pr_body.md for the pull request. Thesis numbers in data/thesis_ignore.txt
are skipped (closing the pull request without merging adds them there).
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content_io

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IGNORE = os.path.join(ROOT, "data", "thesis_ignore.txt")
UNI_EN = {"HACETTEPE ÜNİVERSİTESİ": "Hacettepe University", "EGE ÜNİVERSİTESİ": "Ege University"}
INST_EN = {"Fen Bilimleri Enstitüsü": "Graduate School of Science and Engineering"}


def tr_title(s):
    # "KOCAYİĞİT, FEVZİ RENAN" -> "Fevzi Renan Kocayiğit"
    def word(w):
        low = w.replace("I", "ı").replace("İ", "i").lower()
        first = w[0]
        return first + low[1:]
    if "," in s:
        last, first = [x.strip() for x in s.split(",", 1)]
        s = first + " " + last
    return " ".join(word(w) for w in s.split())


def tr_upper_title(s):
    return " ".join(w[0] + w[1:].replace("I", "ı").replace("İ", "i").lower() for w in s.split())


def main():
    data = json.load(open(os.path.join(ROOT, "data", "yok_theses.json"), encoding="utf-8"))
    th = content_io.load("theses")
    items = th.setdefault("list", [])
    have = {str(t.get("number") or "").strip() for t in items}
    ignore = set()
    if os.path.exists(IGNORE):
        ignore = {l.strip() for l in open(IGNORE, encoding="utf-8") if l.strip() and not l.startswith("#")}
    new = [t for t in data if t["no"] and t["no"] not in have and t["no"] not in ignore]
    if not new:
        print("No new theses.")
        return
    for t in new:
        parts = [p.strip() for p in t["place"].split("/")]
        uni_tr = tr_upper_title(parts[0])
        uni_en = UNI_EN.get(parts[0], uni_tr)
        if len(parts) > 1 and parts[1]:
            inst_tr = tr_upper_title(parts[1])
            uni_tr += ", " + inst_tr
            uni_en += ", " + INST_EN.get(inst_tr, inst_tr)
        co = [a.strip() for a in t["advisors"].split(";") if a.strip() and "ÖZÜDOĞRU" not in a.upper()]
        co_name = tr_upper_title(co[0]) if co else ""
        y = int(t["year"]) if t["year"] else 0
        pos = next((i for i, it in enumerate(items) if int(it.get("year") or 0) <= y), len(items))
        items.insert(pos, {"year": y or "", "title": {"en": t["title_en"] or t["title_tr"], "tr": t["title_tr"]},
                      "author": tr_title(t["author"]), "degree": t["type"] if t["type"] in ("phd", "msc") else "msc",
                      "university": {"en": uni_en, "tr": uni_tr}, "cosupervisor": {"en": co_name, "tr": co_name},
                      "number": t["no"]})
    content_io.save("theses", th)
    body = ["New theses found in the YÖK National Thesis Centre with Barış Özüdoğru as advisor or co-advisor. "
            "Titles come from YÖK as written there; fix capitalisation and italics (genus and species names) in the "
            "diff if needed, then merge. Closing without merging stops these theses from being suggested again.", ""]
    body += [f"- {t['year']} · {tr_title(t['author'])} · {t['title_tr']} · tez:{t['no']}" for t in new]
    open(os.path.join(ROOT, "pr_body.md"), "w", encoding="utf-8").write("\n".join(body) + "\n")
    print("Added", len(new), "theses")


if __name__ == "__main__":
    main()
