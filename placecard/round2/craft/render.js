// usage: node render.js file.svg [file2.svg ...]  -> png/<name>.png
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path'); const fs = require('fs');
(async () => {
  const b = await chromium.launch();
  for (const f of process.argv.slice(2)) {
    const src = fs.readFileSync(f, 'utf8');
    const m = src.match(/width="([\d.]+)" height="([\d.]+)"/);
    const w = Math.ceil(+m[1]), h = Math.ceil(+m[2]);
    const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
    await p.setContent(`<html><body style="margin:0">${src}</body></html>`);
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(200);
    const out = path.join(__dirname, 'png', path.basename(f, '.svg') + '.png');
    await p.screenshot({ path: out });
    console.log(out, w, h);
    await p.close();
  }
  await b.close();
})();
