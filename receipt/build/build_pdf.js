// Print every strip to a vector PDF page at its real size: receipt/print/<name>.pdf
// (merge_pdf.py then joins them into dinner-receipts.pdf and the single pages can go)
//
//   node receipt/build/build_pdf.js        (needs playwright; then merge_pdf.py joins the pages)
//
// The web versions cut the paper edge with CSS masks and add a noise texture and a drop shadow,
// all of which Chrome would flatten to pixels in a PDF. For print they are swapped for vector
// clip paths and dropped, so type stays type and shapes stay shapes.
const path = require('path');
const fs = require('fs');
const { chromium } = require(process.env.PLAYWRIGHT || 'playwright');

const ROOT = path.join(__dirname, '..');
const OUT = path.join(ROOT, 'print');
const STRIPS = { index: 80, classic: 80, poster: 80, tickets: 72, order: 80, fiscal: 57, runner: 80 };

const PRINT_CSS = `
  html, body { background: none !important; }
  body { display: block !important; padding: 0 !important; min-height: 0 !important; }
  .roll { width: var(--mm) !important; filter: none !important; }
  .paper { -webkit-mask: none !important; mask: none !important; }
  .swirl { background-image: VAR_RINGS !important; }
  .paper + .paper::before { opacity: .5; }
`;

// zigzag top and bottom edge, as the CSS mask draws it, but as a vector clip path
function tear() {
  document.querySelectorAll('.paper').forEach((el) => {
    const W = el.offsetWidth, H = el.offsetHeight;
    if (getComputedStyle(el).getPropertyValue('--r').trim()) {
      // ticket stub: concave quarter circles in each corner
      const r = parseFloat(getComputedStyle(el).getPropertyValue('--r')) * W / 100 || 0.034 * W;
      el.style.clipPath = `path('M ${r} 0 H ${W - r} A ${r} ${r} 0 0 0 ${W} ${r} V ${H - r} A ${r} ${r} 0 0 0 ${W - r} ${H} H ${r} A ${r} ${r} 0 0 0 0 ${H - r} V ${r} A ${r} ${r} 0 0 0 ${r} 0 Z')`;
      return;
    }
    const z = W * 0.032, n = Math.round(W / z), s = W / n, p = [];
    for (let k = 0; k <= n; k++) { p.push(`${k * s}px ${z / 2}px`); if (k < n) p.push(`${(k + 0.5) * s}px 0px`); }
    for (let k = n; k >= 0; k--) { p.push(`${k * s}px ${H - z / 2}px`); if (k > 0) p.push(`${(k - 0.5) * s}px ${H}px`); }
    el.style.clipPath = `polygon(${p.join(',')})`;
  });
}

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch();
  for (const [name, mm] of Object.entries(STRIPS)) {
    const page = await browser.newPage({ viewport: { width: 800, height: 1000 } });
    if (process.env.FONT_VIA_CURL) {   // sandboxed builds: fetch Google Fonts through curl
      await page.route(/fonts\.(googleapis|gstatic)\.com/, (r) => {
        const body = require('child_process').execFileSync('curl', ['-sS', '-A', 'Mozilla/5.0 Chrome/130', r.request().url()]);
        r.fulfill({ body, contentType: r.request().url().includes('googleapis') ? 'text/css' : 'font/woff2', headers: { 'access-control-allow-origin': '*' } });
      });
    }
    await page.emulateMedia({ media: 'screen' });
    await page.goto('file://' + path.join(ROOT, name + '.html'));
    await page.evaluate(() => document.fonts.ready);
    // keep only the ring gradient of the swirl, drop the raster noise layer above it
    const rings = await page.evaluate(() => {
      const el = document.querySelector('.swirl');
      if (!el) return 'none';
      const bg = getComputedStyle(el).backgroundImage;
      const i = bg.indexOf('radial-gradient');
      return i < 0 ? 'none' : bg.slice(i);
    });
    await page.addStyleTag({ content: PRINT_CSS.replace('VAR_RINGS', rings) });
    await page.evaluate((mm) => document.documentElement.style.setProperty('--mm', mm + 'mm'), mm);
    await page.evaluate(tear);
    const h = await page.evaluate(() => document.querySelector('.roll').getBoundingClientRect().height);
    await page.pdf({
      path: path.join(OUT, name + '.pdf'),
      width: mm + 'mm', height: Math.ceil(h) + 'px',
      printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 },
      pageRanges: '1',
    });
    console.log(name, mm + 'mm ×', Math.round(h * 25.4 / 96) + 'mm');
    await page.close();
  }
  await browser.close();
})();
