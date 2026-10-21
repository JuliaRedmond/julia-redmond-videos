const {chromium}=require('/opt/node22/lib/node_modules/playwright');const fs=require('fs');
(async()=>{const [,,cfgPath,prefix]=process.argv;const cfg=JSON.parse(fs.readFileSync(cfgPath));
const br=await chromium.launch();const pg=await br.newPage({viewport:{width:1080,height:1920}});
pg.on('pageerror',e=>console.log('PAGEERROR',e.message));
await pg.goto('file://'+__dirname+'/page.html');await pg.evaluate(c=>build(c),cfg);
await pg.evaluate(()=>{document.getElementById('bg').style.left='0'});
console.log('BOUNDS',JSON.stringify(await pg.evaluate(()=>H.bounds)),'CHIP',JSON.stringify(await pg.evaluate(()=>H.chips.length?H.chips.map(c=>[c.sk,+c.cr.toFixed(2)]):+H.chipContrast.toFixed(2))));
await pg.evaluate(()=>document.body.classList.add('notext'));
for(const t of [0.5,cfg.duration*.3,cfg.duration*.6,cfg.beats.find(b=>b.type==='end').start-.5]){await pg.evaluate(t=>setT(t),t);await pg.screenshot({path:`${prefix}_bg_${t.toFixed(1)}.png`})}
await br.close()})()
