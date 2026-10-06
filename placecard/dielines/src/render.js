// usage: node render.js in.svg out.png pxPerMm [clipx clipy clipw cliph in mm]
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs');
(async () => {
  const [,, inp, out, ppm, cx, cy, cw, ch] = process.argv;
  const svg = fs.readFileSync(inp, 'utf8');
  const m = svg.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/);
  const W = parseFloat(m[1]), H = parseFloat(m[2]); const s = parseFloat(ppm);
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const p = await b.newPage({ viewport: { width: Math.ceil(W * s), height: Math.ceil(H * s) } });
  const html = `<html><body style="margin:0;background:#fff">${svg.replace(/<\?xml[^>]*>/, '').replace(/width="[\d.]+mm" height="[\d.]+mm"/, `width="${W*s}" height="${H*s}"`)}</body></html>`;
  await p.setContent(html); await p.waitForTimeout(400);
  await p.evaluate(() => document.fonts.ready);
  const opt = { path: out };
  if (cx !== undefined) opt.clip = { x: cx*s, y: cy*s, width: cw*s, height: ch*s };
  await p.screenshot(opt);
  await b.close();
})();
