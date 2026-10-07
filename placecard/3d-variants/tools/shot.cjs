// Screenshot a fold spec in the 3D viewer.
//   node shot.cjs SPEC.json OUT.png [--t=STEP] [--view=seat|front|side|top|orbit|back] [--size=1200x900]
// Textures are rendered on first use into <spec dir>/tex from <spec dir>/../final/<svg>.
const fs = require('fs'), path = require('path'), http = require('http'), { execFileSync } = require('child_process');
const { chromium } = require('playwright');

const args = process.argv.slice(2);
const opt = Object.fromEntries(args.filter((a) => a.startsWith('--')).map((a) => a.slice(2).split('=')));
const [specPath, out] = args.filter((a) => !a.startsWith('--')).map((p) => path.resolve(p));
const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));
const specDir = path.dirname(specPath);
const texDir = opt.tex ? path.resolve(opt.tex) : path.join(specDir, 'tex');
const stem = spec.svg.replace(/\.svg$/, '');
const acetate = spec.sheets.some((s) => s.stock === 'acetate');
const need = [`${stem}.webp`, `${stem}.size.json`].concat(acetate ? [`${stem}_clear.webp`] : []);
if (!need.every((f) => fs.existsSync(path.join(texDir, f)))) {
  const svg = opt.svg ? path.resolve(opt.svg) : path.join(specDir, '..', 'final', spec.svg);
  execFileSync('python3', [path.join(__dirname, 'textures.py'), texDir, svg].concat(acetate ? ['--clear'] : []), { stdio: 'inherit' });
}
const ROOT = path.resolve(__dirname, '..');
const types = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.webp': 'image/webp', '.png': 'image/png' };
const server = http.createServer((req, res) => {
  const u = decodeURIComponent(req.url.split('?')[0]);
  const f = u.startsWith('/@fs/') ? u.slice(4) : path.join(ROOT, u);
  fs.readFile(f, (err, data) => {
    if (err) { res.writeHead(404); res.end(); return; }
    res.writeHead(200, { 'Content-Type': types[path.extname(f)] || 'application/octet-stream' });
    res.end(data);
  });
});
server.listen(0, async () => {
  const port = server.address().port;
  const [w, h] = (opt.size || '1200x900').split('x').map(Number);
  const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const page = await browser.newPage({ viewport: { width: w, height: h } });
  // the browser has no proxy settings: serve CDN files from a local cache, fetched with curl
  const cache = path.join(require('os').homedir(), '.cache', 'fold3d-cdn');
  await page.route(/^https:\/\/(cdn\.jsdelivr\.net|fonts\.(googleapis|gstatic)\.com)\//, (route) => {
    const url = route.request().url();
    const f = path.join(cache, url.replace(/^https:\/\//, '').replace(/[?#].*$/, ''));
    try {
      if (!fs.existsSync(f)) {
        fs.mkdirSync(path.dirname(f), { recursive: true });
        execFileSync('curl', ['-sSfL', '-o', f, url]);
      }
      route.fulfill({ body: fs.readFileSync(f), contentType: f.endsWith('.js') ? 'text/javascript' : undefined });
    } catch (e) { route.abort(); }
  });
  page.on('pageerror', (e) => console.error('page error:', e.message));
  const q = new URLSearchParams({ spec: '/@fs' + specPath, tex: '/@fs' + texDir, view: opt.view || 'orbit' });
  if (opt.t !== undefined) q.set('t', opt.t);
  await page.goto(`http://127.0.0.1:${port}/shot.html?${q}`);
  await page.waitForFunction(() => window.__ready, null, { timeout: 120000 });
  const err = await page.evaluate(() => window.__error);
  if (err) { console.error('viewer error:', err); process.exitCode = 1; }
  else {
    await page.waitForTimeout(300);
    await page.screenshot({ path: out });
    const info = await page.evaluate(() => window.__info);
    console.log(`${out}  steps=${info.maxStep}`);
  }
  await browser.close();
  server.close();
});
