// usage: node render.js scale in.svg [in2.svg ...]  -> writes in.png next to svg
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs=require('fs');
(async()=>{
  const scale=parseFloat(process.argv[2]);
  const browser=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome',args:['--allow-file-access-from-files']});
  for(const f0 of process.argv.slice(3)){ const f=require('path').resolve(f0);
    const svg=fs.readFileSync(f,'utf8');
    const m=svg.match(/viewBox="([\d.\- ]+)"/); const vb=m[1].split(/\s+/).map(Number);
    const W=Math.round(vb[2]*scale), H=Math.round(vb[3]*scale);
    const page=await browser.newPage({viewport:{width:W,height:H}});
    const html=`<html><body style="margin:0;background:#fff">${svg.replace(/width="[\d.]+" height="[\d.]+"/,`width="${W}" height="${H}"`)}</body></html>`;
    fs.writeFileSync(f+'.html',html);
    await page.goto('file://'+f+'.html'); await page.waitForTimeout(400);
    await page.screenshot({path:f.replace(/\.svg$/,'.png')});
    fs.unlinkSync(f+'.html'); await page.close();
  }
  await browser.close();
})();
