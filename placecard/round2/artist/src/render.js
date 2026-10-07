const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const base = '/tmp/claude-0/-home-user-claude-bobik/6a3dcf92-132a-5018-88ad-a2068c46056a/scratchpad/round2/artist/';
(async () => {
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 1800, height: 1260 } });
  for (const n of process.argv.slice(2)) {
    await pg.goto('file://' + base + n + '.svg');
    await pg.waitForTimeout(500);
    await pg.screenshot({ path: base + n + '.png' });
  }
  await b.close();
})();
