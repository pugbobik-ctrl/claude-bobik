const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs=require('fs'), path=require('path');
(async()=>{
  const dir=__dirname; const only=process.argv.slice(2);
  const files=fs.readdirSync(path.join(dir,'svg')).filter(f=>f.endsWith('.svg')&&(only.length==0||only.some(o=>f.startsWith(o))));
  const b=await chromium.launch({executablePath:process.env.CHROMIUM||undefined});
  const ctx=await b.newContext({deviceScaleFactor:1.5, viewport:{width:1200,height:900}});
  for(const f of files){
    const p=await ctx.newPage();
    await p.goto('file://'+path.join(dir,'svg',f));
    await p.waitForTimeout(250);
    await p.evaluate(()=>document.fonts.ready);
    await p.screenshot({path:path.join(dir,'png',f.replace('.svg','.png')),clip:{x:0,y:0,width:1200,height:900}});
    await p.close(); console.log('ok',f);
  }
  await b.close();
})();
