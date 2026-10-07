// Render stills and animation frames for every card in a built site.
//   node render_frames.cjs SITE_DIR OUT_DIR [--size=900x600] [--artist="Tanya Andrianova"] [--video] [--fps=12]
// Writes OUT_DIR/<set>/<design>/{stills.json, s_*.png, v_*.png}.
const fs = require('fs'), path = require('path'), http = require('http'), { execFileSync } = require('child_process');
const { chromium } = require('playwright');
const args = process.argv.slice(2);
const opt = Object.fromEntries(args.filter((a) => a.startsWith('--')).map((a) => { const i = a.indexOf('='); return i < 0 ? [a.slice(2), true] : [a.slice(2, i), a.slice(i + 1)]; }));
const [site, outDir] = args.filter((a) => !a.startsWith('--')).map((p) => path.resolve(p));
const ROOT = path.resolve(__dirname, '..');
const types = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.json': 'application/json', '.webp': 'image/webp' };
const server = http.createServer((req, res) => {
  const u = decodeURIComponent(req.url.split('?')[0]);
  const f = u.startsWith('/site/') ? path.join(site, u.slice(6)) : path.join(ROOT, u);
  fs.readFile(f, (err, data) => {
    if (err) { res.writeHead(404); res.end(); return; }
    res.writeHead(200, { 'Content-Type': types[path.extname(f)] || 'application/octet-stream' }); res.end(data);
  });
});
server.listen(0, async () => {
  const [w, h] = (opt.size || '900x600').split('x').map(Number);
  const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const page = await browser.newPage({ viewport: { width: w, height: h } });
  const cache = path.join(require('os').homedir(), '.cache', 'fold3d-cdn');
  await page.route(/^https:\/\/cdn\.jsdelivr\.net\//, (route) => {
    const url = route.request().url();
    const f = path.join(cache, url.replace(/^https:\/\//, ''));
    if (!fs.existsSync(f)) { fs.mkdirSync(path.dirname(f), { recursive: true }); execFileSync('curl', ['-sSfL', '-o', f, url]); }
    route.fulfill({ body: fs.readFileSync(f), contentType: 'text/javascript' });
  });
  page.on('pageerror', (e) => console.error('page error:', e.message));
  await page.goto(`http://127.0.0.1:${server.address().port}/render.html`);
  await page.waitForFunction(() => window.__ready, null, { timeout: 120000 });
  const fps = Number(opt.fps || 12);
  for (const set of ['system', 'fold', 'edge', 'optic']) {
    const data = JSON.parse(fs.readFileSync(path.join(site, 'data', set + '.json'), 'utf8'));
    for (const d of data.designs) {
      const card = d.cards.find((c) => c.artist === (opt.artist || 'Tanya Andrianova')) || d.cards[0];
      const dir = path.join(outDir, set, d.id);
      fs.mkdirSync(dir, { recursive: true });
      const info = await page.evaluate(([s, tex]) => window.load(s, tex), [card.spec, `/site/tex/${set}`]);
      const n = info.maxStep, stills = [];
      const shot = async (t, view, name) => {
        await page.evaluate(([t, v]) => window.frame(t, v), [t, view]);
        await page.screenshot({ path: path.join(dir, name) });
      };
      await shot(0, 'top', 's_0.png'); stills.push({ file: 's_0.png', t: 0, label: 'Развёртка' });
      for (let k = 1; k <= n; k++) {
        await shot(k - 0.5, 'travel', `s_${k}a.png`); stills.push({ file: `s_${k}a.png`, t: k - 0.5, label: `Шаг ${k}`, caption: info.steps[k - 1] || '' });
      }
      await shot(n, 'orbit', 's_done.png'); stills.push({ file: 's_done.png', t: n, label: 'Собрано' });
      await shot(n, 'seat', 's_seat.png'); stills.push({ file: 's_seat.png', t: n, label: 'С места гостя' });
      fs.writeFileSync(path.join(dir, 'stills.json'), JSON.stringify({ set: data.title, design: d.title, rank: d.rank, blurb: d.blurb,
        artist: card.artist, steps: info.steps, stills }));
      if (opt.video) {
        const frames = [];
        let i = 0;
        const put = async (t, view) => {
          const name = `v_${String(i++).padStart(4, '0')}.png`;
          await shot(t, view, name);
          frames.push({ file: name, t, view });
        };
        // flat sheet, each step over 1.6 s, a pause, then the view from the guest's seat
        for (let j = 0; j < Math.round(fps * 0.8); j++) await put(0, 'travel');
        const per = Math.round(fps * 1.6);
        for (let f = 1; f <= n * per; f++) await put(f / per, 'travel');
        for (let j = 0; j < Math.round(fps * 0.6); j++) await put(n, 'travel');
        for (let j = 0; j < Math.round(fps * 1.4); j++) await put(n, 'seat');
        fs.writeFileSync(path.join(dir, 'frames.json'), JSON.stringify(frames));
      }
      console.log(set, d.id, n, 'steps');
    }
  }
  await browser.close(); server.close();
});
