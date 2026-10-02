const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => {
  const [,, file, out, w, h, scale] = process.argv;
  const b = await chromium.launch({ headless: true, proxy: { server: process.env.HTTPS_PROXY } });
  const ctx = await b.newContext({ viewport: { width: +w, height: h === 'auto' ? 800 : +h }, deviceScaleFactor: +(scale || 1) });
  const p = await ctx.newPage();
  await p.goto('file://' + file, { waitUntil: 'networkidle', timeout: 60000 });
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(500);
  let H = +h;
  if (h === 'auto') { H = await p.evaluate(() => Math.ceil(document.querySelector('.board').getBoundingClientRect().height)); await p.setViewportSize({ width: +w, height: H }); await p.waitForTimeout(300); }
  await p.screenshot({ path: out, clip: { x: 0, y: 0, width: +w, height: H } });
  console.log(out, w + 'x' + H);
  await b.close();
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
