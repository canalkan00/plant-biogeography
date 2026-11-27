// Opens every built page in a headless browser and fails if something is broken:
// a script error, a missing menu or footer, an empty publication list, or a page
// that scrolls sideways on a phone. Run after build.sh: node scripts/smoke_test.js
const { chromium } = require('playwright');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const PAGES = ['index', 'about', 'research', 'publications', 'people', 'contact'];
const MUST = {
  index: ['#relief', '#highlights .hl'],
  about: ['#about', '#pi'],
  research: ['#topics', '#projects .tl-row'],
  publications: ['#pubs > li', '#theses li'],
  people: ['#team .member', '#alumni li'],
  contact: ['#mail', '#visit'],
};

(async () => {
  const browser = await chromium.launch();
  const problems = [];
  for (const name of PAGES) {
    for (const [label, viewport] of [['desktop', { width: 1440, height: 900 }], ['phone', { width: 390, height: 844 }]]) {
      const page = await browser.newPage({ viewport });
      const errors = [];
      page.on('pageerror', (e) => errors.push(e.message));
      page.on('console', (m) => { if (m.type() === 'error' && !/fonts\.g|ERR_|net::/.test(m.text())) errors.push(m.text()); });
      await page.goto('file://' + path.join(ROOT, name + '.html'));
      await page.waitForTimeout(800);
      const where = `${name}.html (${label})`;
      errors.forEach((e) => problems.push(`${where}: script error: ${e}`));
      for (const sel of ['#nav', 'main', 'footer', ...MUST[name]]) {
        if (!(await page.$(sel))) problems.push(`${where}: missing ${sel}`);
      }
      const width = await page.evaluate(() => document.documentElement.scrollWidth);
      if (width > viewport.width + 2) problems.push(`${where}: page is ${width}px wide, wider than the ${viewport.width}px screen`);
      await page.close();
    }
  }
  await browser.close();
  if (problems.length) {
    console.error('Site check failed:\n- ' + problems.join('\n- '));
    process.exit(1);
  }
  console.log('Site check passed: ' + PAGES.length + ' pages, desktop and phone.');
})();
