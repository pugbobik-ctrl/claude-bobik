// Screenshot the built viewer page: node page_shot.cjs SITE_DIR OUT.png [--hash=fold.ridge] [--size=1400x900] [--dark] [--click=SELECTOR]
const fs = require('fs'), path = require('path'), http = require('http'), { execFileSync } = require('child_process');
const { chromium } = require('playwright');
const args = process.argv.slice(2);
const opt = Object.fromEntries(args.filter((a) => a.startsWith('--')).map((a) => a.slice(2).split('=')));
const [site, out] = args.filter((a) => !a.startsWith('--')).map((p) => path.resolve(p));
const types = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.json': 'application/json; charset=utf-8', '.webp': 'image/webp' };
const server = http.createServer((req, res) => {
  const f = path.join(site, decodeURIComponent(req.url.split('?')[0]).replace(/\/$/, '/index.html'));
  fs.readFile(f, (err, data) => {
    if (err) { res.writeHead(404); res.end(); return; }
    res.writeHead(200, { 'Content-Type': types[path.extname(f)] || 'application/octet-stream' }); res.end(data);
  });
});
server.listen(0, async () => {
  const [w, h] = (opt.size || '1400x900').split('x').map(Number);
  const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const page = await browser.newPage({ viewport: { width: w, height: h }, colorScheme: 'dark' in opt ? 'dark' : 'light' });
  const cache = path.join(require('os').homedir(), '.cache', 'fold3d-cdn');
  await page.route(/^https:\/\/(cdn\.jsdelivr\.net|fonts\.(googleapis|gstatic)\.com)\//, (route) => {
    const url = route.request().url();
    const f = path.join(cache, url.replace(/^https:\/\//, '').replace(/[?#].*$/, '').replace(/\/$/, '/_') + (url.includes('?') ? '_' + Buffer.from(url.split('?')[1]).toString('hex').slice(0, 40) : ''));
    try {
      if (!fs.existsSync(f)) { fs.mkdirSync(path.dirname(f), { recursive: true }); execFileSync('curl', ['-sSfL', '-A', 'Mozilla/5.0 Chrome/120', '-o', f, url]); }
      const ct = url.includes('fonts.googleapis') ? 'text/css' : f.endsWith('.js') ? 'text/javascript' : undefined;
      route.fulfill({ body: fs.readFileSync(f), contentType: ct, headers: { 'access-control-allow-origin': '*' } });
    } catch (e) { route.abort(); }
  });
  page.on('pageerror', (e) => console.error('page error:', e.message));
  await page.goto(`http://127.0.0.1:${server.address().port}/index.html${opt.hash ? '#' + opt.hash : ''}`);
  await page.waitForFunction(() => window.__ready || window.__error, null, { timeout: 120000 });
  const err = await page.evaluate(() => window.__error);
  if (err) console.error('viewer error:', err);
  if (opt.click) { for (const sel of opt.click.split('|')) { await page.click(sel); await page.waitForTimeout(1500); } }
  if (opt.t !== undefined) { await page.evaluate((t) => { const el = document.getElementById('t'); el.value = t; el.dispatchEvent(new Event('input')); }, opt.t); }
  await page.waitForTimeout(1500);
  await page.screenshot({ path: out });
  console.log(out);
  await browser.close(); server.close();
});
