// Lists every thesis in the Council of Higher Education National Thesis Centre
// (YÖK Ulusal Tez Merkezi) with Barış Özüdoğru as advisor or co-advisor and
// writes them to data/yok_theses.json. The search form needs a real browser.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('https://tez.yok.gov.tr/UlusalTezMerkezi/tarama.jsp', { timeout: 90000 });
  await page.waitForTimeout(2000);
  await page.locator('input[name=DanismanAdSoyad]').fill('BARIŞ ÖZÜDOĞRU', { force: true });
  await page.evaluate(() => {
    const form = document.querySelector('input[name=DanismanAdSoyad]').form;
    [...form.querySelectorAll('button,input[type=submit],a')].find((x) => /Bul/.test(x.innerText || x.value)).click();
  });
  await page.waitForSelector('.result-card', { timeout: 60000 });
  await page.waitForTimeout(2000);
  const cards = await page.evaluate(() => [...document.querySelectorAll('.result-card')].map((c) => {
    const lines = c.innerText.split('\n').map((l) => l.trim()).filter(Boolean);
    return { kayit: c.dataset.kayitno, tez: c.dataset.tezno, no: (c.innerText.match(/Tez No: (\d+)/) || [])[1] || '',
      title_tr: lines[0] || '', title_en: lines[1] || '' };
  }));
  const out = [];
  for (const c of cards) {
    const raw = await page.evaluate(async ([k, t]) => (await fetch('tezBilgiDetay.jsp?kayitNo=' + k + '&tezNo=' + t)).text(), [c.kayit, c.tez]);
    let d = {};
    try { d = JSON.parse(raw.match(/\{[\s\S]*\}/)[0]); } catch (e) { /* keep the card data */ }
    const strip = (x) => String(x || '').replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
    const apa = strip(d.apa_ref), mla = strip(d.mla_ref);
    out.push({
      no: c.no || (apa.match(/Tez No\. (\d+)/) || [])[1] || '',
      title_tr: c.title_tr, title_en: c.title_en,
      author: (mla.match(/^([^.]+?)\./) || [])[1] || '',
      year: (apa.match(/\((\d{4})\)/) || [])[1] || '',
      type: /Doktora/i.test(apa) ? 'phd' : /Yüksek lisans/i.test(apa) ? 'msc' : 'other',
      advisors: strip(d.danisman).replace(/^Danışman:\s*/i, ''),
      place: strip(d.yer),
    });
  }
  await browser.close();
  const file = path.join(__dirname, '..', 'data', 'yok_theses.json');
  fs.writeFileSync(file, JSON.stringify(out, null, 2) + '\n');
  console.log('Theses found on YÖK:', out.length);
})().catch((e) => { console.error('YÖK search failed:', e.message); process.exit(1); });
