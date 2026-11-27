#!/usr/bin/env python3
"""Add theses found on YÖK (data/yok_theses.json, written by yok_theses.js)
that are not on the site yet to the theses list in site.html, and write
pr_body.md for the pull request. Thesis numbers in data/thesis_ignore.txt
are skipped (closing the pull request without merging adds them there).
"""
import html, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site.html")
IGNORE = os.path.join(ROOT, "data", "thesis_ignore.txt")
UNI_EN = {"HACETTEPE ÜNİVERSİTESİ": "Hacettepe University", "EGE ÜNİVERSİTESİ": "Ege University"}


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


def bi(en, tr):
    return f'<span class="en">{en}</span><span class="tr">{tr}</span>'


def main():
    data = json.load(open(os.path.join(ROOT, "data", "yok_theses.json"), encoding="utf-8"))
    site = open(SITE, encoding="utf-8").read()
    have = set(re.findall(r"Tez No: (\d+)", site))
    ignore = set()
    if os.path.exists(IGNORE):
        ignore = {l.strip() for l in open(IGNORE, encoding="utf-8") if l.strip() and not l.startswith("#")}
    new = [t for t in data if t["no"] and t["no"] not in have and t["no"] not in ignore]
    if not new:
        print("No new theses.")
        return
    m = re.search(r'(<ol class="pubs theses">\n)(.*?)(\n\s*</ol>)', site, re.S)
    items = re.findall(r"\s*<li>.*?</li>", m.group(2), re.S)
    items = [i.strip() for i in items]
    for t in new:
        uni_tr = t["place"].split("/")[0].strip()
        uni_en = UNI_EN.get(uni_tr, uni_tr.title())
        kind = {"phd": ("PhD thesis", "Doktora tezi"), "msc": ("MSc thesis", "Yüksek lisans tezi")}.get(t["type"], ("Thesis", "Tez"))
        co = [a.strip() for a in t["advisors"].split(";") if "ÖZÜDOĞRU" not in a.upper()]
        note_en = (f"Co-supervisor: {html.escape(co[0].title())} · " if co else "") + f"Thesis no. {t['no']}"
        note_tr = (f"Eş danışman: {html.escape(co[0].title())} · " if co else "") + f"Tez No: {t['no']}"
        li = (f'<li><span class="yr">{t["year"]}</span><div><p class="t">'
              + bi(html.escape(t["title_en"] or t["title_tr"]), html.escape(t["title_tr"]))
              + f'</p><p class="a"><b>{html.escape(tr_title(t["author"]))}</b> · ' + bi(*kind) + " · "
              + bi(html.escape(uni_en), html.escape(uni_tr.title()))
              + '</p><p class="m data">' + bi(note_en, note_tr) + "</p></div></li>")
        pos = next((i for i, it in enumerate(items)
                    if int((re.search(r'class="yr">(\d{4})', it) or [0, 0])[1]) < int(t["year"] or 0)), len(items))
        items.insert(pos, li)
    site = site[:m.start(2)] + "\n".join("            " + i for i in items) + site[m.end(2):]
    open(SITE, "w", encoding="utf-8").write(site)
    body = ["New theses found in the YÖK National Thesis Centre with Barış Özüdoğru as advisor or co-advisor. "
            "Titles come from YÖK as written there; fix capitalisation and italics (genus and species names) in the "
            "diff if needed, then merge. Closing without merging stops these theses from being suggested again.", ""]
    body += [f"- {t['year']} · {tr_title(t['author'])} · {t['title_tr']} · tez:{t['no']}" for t in new]
    open(os.path.join(ROOT, "pr_body.md"), "w", encoding="utf-8").write("\n".join(body) + "\n")
    print("Added", len(new), "theses")


if __name__ == "__main__":
    main()
